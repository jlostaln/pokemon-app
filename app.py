import sqlite3
from flask import Flask
from flask import render_template, request, redirect, session, abort
import users
import config
import db
import pokemon
import trades
import pokeapi
import random
import json

app = Flask(__name__)

app.secret_key = config.secret_key
api = pokeapi.PokeApi()

def require_login():
    if "user_id" not in session:
        abort(403)

def check_access(owner_id):
    if owner_id != session["user_id"]:
        abort(403)

def handle_none(obj):
    if not obj:
       abort(404)
    return obj

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/trade/<int:trade_id>/accept", methods=["POST"])
def accept_trade(trade_id):
    require_login()
    trade = handle_none(trades.get_trade(trade_id))
    check_access(trade["responder_id"])
    requester_id = trade["requester_id"]
    responder_id = trade["responder_id"]
    trades.accept_trade(trade_id, requester_id, responder_id)
    return redirect("/my_trades")

@app.route("/trade/<int:trade_id>/reject", methods=["POST"])
def reject_trade(trade_id):
    require_login()
    trade = handle_none(trades.get_trade(trade_id))
    check_access(trade["responder_id"])
    trades.reject_trade(trade_id)
    return redirect("/my_trades")

@app.route("/trade/<int:trade_id>/cancel", methods=["POST"])
def cancel_trade(trade_id):
    require_login()
    trade = handle_none(trades.get_trade(trade_id))
    check_access(trade["requester_id"])
    trades.cancel_trade(trade_id)
    return redirect("/my_trades")

@app.route("/my_trades")
def my_trades():
    require_login()
    user_id = session["user_id"]
    query = request.args.get("query")
    transactions = trades.get_user_trades(user_id, query)
    return render_template("my_trades.html", transactions=transactions, query=query)

@app.route("/submit_request", methods=["POST"])
def submit_trade():
    require_login()
    target_pokemon_id = request.form.get("requested_pokemon_id")
    offer_pokemon_ids = request.form.getlist("requester_pokemon_ids")
    requester_id = session["user_id"]
    target = handle_none(pokemon.get_pokemon_by_id(target_pokemon_id))
    offer_pokemon = []
    for offer_id in offer_pokemon_ids:
        offer = handle_none(pokemon.get_pokemon_by_id(offer_id))
        check_access(offer["owner_id"])
        offer_pokemon.append(offer)

    try:
        trades.add_trade_pending(requester_id, target["owner_id"])
        trade_id = db.last_insert_id()
        trades.add_trade_history(trade_id, "pending")
        trades.add_pokemon(trade_id, target["id"], target["name"], "responder")
        for offer in offer_pokemon:
            trades.add_pokemon(trade_id, offer["id"], offer["name"], "requester")
    except Exception as e:
        return f"VIRHE: {e}"
    return redirect("/my_trades")

@app.route("/trading/<int:pokemon_id>")
def trade_view(pokemon_id):
    require_login()
    requester_id = session["user_id"]
    requested_pokemon = handle_none(pokemon.get_pokemon_by_id(pokemon_id))
    if requested_pokemon["owner_id"] == requester_id:
        abort(403)
    _, pokemon_status = pokemon.get_pokemon_status(pokemon_id)
    if pokemon_status != "Listattu":
        abort(404)

    requester_pokemon = users.get_my_pokemon(requester_id)
    return render_template("create_proposal.html", requested_pokemon=requested_pokemon, requester_pokemon=requester_pokemon)

@app.route("/trading/")
def view_trade_listings():
    require_login()
    query = request.args.get("query")
    result = pokemon.get_listed_pokemon(query)
    return render_template("/trading.html", pokemons=result, query=query)

@app.route("/my_pokemon/")
def my_pokemon():
    require_login()
    owner_id = session["user_id"]
    result = users.get_my_pokemon(owner_id)
    statuses = pokemon.get_all_statuses()
    return render_template("/my_pokemon.html", pokemons=result, statuses=statuses)

@app.route("/my_pokemon/change_status/<int:pokemon_id>", methods=["POST"])
def change_status(pokemon_id):
    require_login()
    target = handle_none(pokemon.get_pokemon_by_id(pokemon_id))
    check_access(target["owner_id"])
    status = request.form.get("status")
    status_rows = pokemon.get_all_statuses()
    all_statuses = []
    for row in status_rows:
        all_statuses.append(row["value"])
    if status not in all_statuses:
        abort(403)
    status_id, pokemon_status = pokemon.get_pokemon_status(pokemon_id)
    if status == pokemon_status:
        return redirect(f"/my_pokemon#pokemon-{pokemon_id}")
    pokemon.set_pokemon_status(status, status_id)
    return redirect(f"/my_pokemon#pokemon-{pokemon_id}")

@app.route("/my_pokemon/stats/<string:pokemon_type>")
def my_pokemon_by_type(pokemon_type):
    require_login()
    owner_id = session["user_id"]
    result = users.get_my_pokemon_by_type(owner_id, pokemon_type)
    statuses = pokemon.get_all_statuses()
    return render_template("/my_pokemon.html", pokemons=result, statuses=statuses)

@app.route("/my_pokemon/stats/")
def my_pokemon_stats():
    require_login()
    owner_id = session["user_id"]
    count = handle_none(users.get_pokemon_count(owner_id))
    count_by_type = users.get_pokemon_count_by_type(owner_id)
    return render_template("/my_stats.html", count=count, count_by_type=count_by_type)


@app.route("/my_pokemon/edit_pokemon/<int:pokemon_id>")
def edit_pokemon(pokemon_id):
    require_login()
    result = handle_none(pokemon.get_pokemon_by_id(pokemon_id))
    check_access(result["owner_id"])
    stats = pokemon.get_pokemon_stats(pokemon_id)
    return render_template("edit_pokemon.html", pokemon=result, stats=stats)

@app.route("/my_pokemon/update/<int:pokemon_id>", methods=["POST"])
def update_pokemon(pokemon_id):
    require_login()
    result = handle_none(pokemon.get_pokemon_by_id(pokemon_id))
    check_access(result["owner_id"])
    nickname = request.form.get("nickname")
    new_stat = request.form.get("new_stat")
    new_stat_value = request.form.get("new_stat_value")

    if nickname and nickname.strip():
        if len(nickname) > 20:
            abort(403)
        pokemon.set_nickname(nickname, pokemon_id)

    if new_stat and new_stat.strip() != "" and new_stat_value:
        if len(new_stat) > 20:
            abort(403)
        try:
            new_stat_value = int(new_stat_value)
            if new_stat_value > 200:
                raise ValueError
        except ValueError:
            print("Tilaston arvon oltava kokonaisluku ja enintään 200!") # Pitää muuttaa flash():ksi devauksen edetessä
            return redirect(f"/my_pokemon/edit_pokemon/{pokemon_id}")

        pokemon.add_stat(pokemon_id, new_stat, new_stat_value)
    return redirect(f"/my_pokemon/edit_pokemon/{pokemon_id}")

@app.route("/my_pokemon/delete/<int:pokemon_id>", methods=["POST"])
def delete_pokemon(pokemon_id):
    require_login()
    result = handle_none(pokemon.get_pokemon_by_id(pokemon_id))
    check_access(result["owner_id"])
    pokemon.remove_pokemon(pokemon_id)
    return redirect("/my_pokemon/")

@app.route("/my_pokemon/delete_stat/<int:pokemon_id>/<int:stat_id>", methods=["POST"])
def delete_stat(pokemon_id, stat_id):
    require_login()
    result = handle_none(pokemon.get_pokemon_by_id(pokemon_id))
    check_access(result["owner_id"])
    pokemon.remove_stat(stat_id)
    return redirect(f"/my_pokemon/edit_pokemon/{pokemon_id}")

@app.route("/capture_pokemon/<string:pokemon_name>", methods=["POST"])
def capture_pokemon(pokemon_name):
    require_login()
    success = random.randint(0, 100) < 50
    if success:
        name = request.form["name"]
        owner_id = session["user_id"]
        height = request.form["height"]
        weight = request.form["weight"]
        base_experience = request.form["base_experience"]
        next_evolution = request.form["next_evolution"]
        flavor_text = request.form["flavor_text"]
        sprite = request.form["sprite"]
        stats = json.loads(request.form["stats"])
        is_base_stat = 1
        types = json.loads(request.form["types"])

        try:
            pokemon.add_pokemon(name, owner_id, height, weight, base_experience, next_evolution, flavor_text, sprite)
            pokemon_id = db.last_insert_id()

            for stat in stats:
                pokemon.add_stat(pokemon_id, stat["stat"]["name"], stat["base_stat"], is_base_stat)

            for t in types:
                pokemon.add_type(pokemon_id, t["type"]["name"])

            pokemon.add_pokemon_status(pokemon_id)

        except Exception as e:
            return f"VIRHE: {e}"

        session["capture_result"] = True
    else:
        session["capture_result"] = False
    return redirect(f"/inspect/{pokemon_name}")

@app.route("/inspect/<string:pokemon_name>")
def inspect(pokemon_name):
    require_login()
    pokemon = api.get_pokemon_details(pokemon_name)
    if pokemon is None:
        return redirect(f'/encounters/{session["current_area"]}')
    additional_information = api.get_pokemon_additional_info(pokemon)
    pokemon.update(additional_information)
    capture_result = session.pop("capture_result", None)
    return render_template("inspect.html", pokemon=pokemon, capture_result=capture_result)

@app.route("/location-area/")
def redirect_to_start():
    require_login()
    return redirect("/location-area/start")

@app.route("/location-area/<string:direction>")
def get_location_areas(direction):
    require_login()
    session.setdefault("next_locations_url", None)
    session.setdefault("previous_locations_url", None)
    session.setdefault("current_locations_url", None)

    directions = {
        "next": session["next_locations_url"],
        "previous": session["previous_locations_url"],
        "current": session["current_locations_url"],
        "start": None
    }

    page_url = directions.get(direction)

    areas, next_url, previous_url, current_url = api.get_location_areas(page_url)
    session["next_locations_url"] = next_url
    session["previous_locations_url"] = previous_url
    session["current_locations_url"] = current_url
    return render_template("location-areas.html", areas=areas)

@app.route("/encounters/<string:area_name>")
def get_location_encounters(area_name):
    require_login()
    session["current_area"] = area_name
    encounters = api.get_encounters(area_name)
    return render_template("encounters.html", encounters=encounters)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            print("VIRHE: väärä tunnus tai salasana") # flashiksi kehityksen edetessä
            return redirect("/login")

    return redirect("/")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")
