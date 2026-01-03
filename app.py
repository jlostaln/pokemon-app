import urllib.request
import math
import time
from datetime import datetime
import secrets
import sqlite3
from flask import Flask
from flask import render_template, request, redirect, session, abort, flash, g, make_response
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

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/my_pokemon/stats")
    return render_template("index.html")

@app.route("/pokemon_sprite/<int:pokemon_id>")
def show_image(pokemon_id):
    require_login()
    pokemon_sprite = handle_none(pokemon.get_pokemon_sprite(pokemon_id))
    response = make_response(bytes(pokemon_sprite))
    response.headers.set("Content-Type", "image/png")
    return response


@app.route("/trade/<int:trade_id>/accept", methods=["POST"])
def accept_trade(trade_id):
    require_login()
    check_csrf()
    trade = handle_none(trades.get_trade(trade_id))
    check_access(trade["responder_id"])
    requester_id = trade["requester_id"]
    responder_id = trade["responder_id"]
    trades.accept_trade(trade_id, requester_id, responder_id)
    flash(f"Trade {trade_id} accepted! Deal is now completed.", "success")
    query = request.form.get("query")
    page = request.form.get("page")
    if not page:
        page = 1
    if query:
        return redirect(f"/my_trades/{page}?query={query}")
    return redirect(f"/my_trades/{page}")

@app.route("/trade/<int:trade_id>/reject", methods=["POST"])
def reject_trade(trade_id):
    require_login()
    check_csrf()
    trade = handle_none(trades.get_trade(trade_id))
    check_access(trade["responder_id"])
    trades.reject_trade(trade_id)
    flash(f"Trade {trade_id} rejected!", "success")
    query = request.form.get("query")
    page = request.form.get("page")
    if not page:
        page = 1
    if query:
        return redirect(f"/my_trades/{page}?query={query}")
    return redirect(f"/my_trades/{page}")

@app.route("/trade/<int:trade_id>/cancel", methods=["POST"])
def cancel_trade(trade_id):
    require_login()
    check_csrf()
    trade = handle_none(trades.get_trade(trade_id))
    check_access(trade["requester_id"])
    trades.cancel_trade(trade_id)
    flash(f"Trade {trade_id} canceled!", "success")
    query = request.form.get("query")
    page = request.form.get("page")
    if not page:
        page = 1
    if query:
        return redirect(f"/my_trades/{page}?query={query}")
    return redirect(f"/my_trades/{page}")

@app.route("/my_trades/")
@app.route("/my_trades/<int:page>")
def my_trades(page=1):
    require_login()
    user_id = session["user_id"]
    query = request.args.get("query")
    page_size = 3
    trade_count = trades.get_user_trade_count(user_id, query)
    page_count = max(math.ceil(trade_count /  page_size), 1)

    if page < 1:
        return redirect("/my_trades/1")
    if page > page_count:
        if query:
            return redirect(f"/my_trades/{page_count}?query={query}")
        return redirect(f"/my_trades/{page_count}")

    transactions = trades.get_user_trades(user_id, page, page_size, query)
    return render_template("my_trades.html", transactions=transactions, query=query, page=page, page_count=page_count)

@app.route("/submit_request", methods=["POST"])
def submit_trade():
    require_login()
    check_csrf()
    target_pokemon_id = request.form.get("requested_pokemon_id")
    offer_pokemon_selections_json = request.form.getlist("selected_ids")
    offer_pokemon_selections = [json.loads(item) for item in offer_pokemon_selections_json]
    new_selections_json = request.form.getlist("requester_pokemon_ids")
    new_selections = [json.loads(item) for item in new_selections_json]
    for new_id in new_selections:
        if new_id not in offer_pokemon_selections:
            offer_pokemon_selections.append(new_id)
    requester_id = session["user_id"]
    target = handle_none(pokemon.get_pokemon_by_id(target_pokemon_id))
    offer_pokemon = []
    pokemon_in_other_offers = []
    for offer_selection in offer_pokemon_selections:
        offer = handle_none(pokemon.get_pokemon_by_id(offer_selection["id"]))
        check_access(offer["owner_id"])
        in_other_offer = trades.get_pokemon_in_pending_trade(offer["id"])
        if in_other_offer:
            pokemon_in_other_offers.append(offer["name"])
        offer_pokemon.append(offer)
    if pokemon_in_other_offers:
        flash(f"Your pokémon {pokemon_in_other_offers} are part of other pending trades. A completed trade involving these pokémon will cause the other trades to be automatically rejected", "info")


    try:
        trades.add_trade_pending(requester_id, target["owner_id"])
        trade_id = db.last_insert_id()
        trades.add_trade_history(trade_id, "pending")
        trades.add_pokemon(trade_id, target["id"], target["name"], "responder")
        for offer in offer_pokemon:
            trades.add_pokemon(trade_id, offer["id"], offer["name"], "requester")
    except Exception as e:
        flash(f"ERROR: {e}", "error")
        return redirect("/my_trades")
    flash("Trade proposal successfully submitted!", "success")
    return redirect("/my_trades")

@app.route("/trading/make_offer/<int:pokemon_id>/", methods = ["GET", "POST"])
@app.route("/trading/make_offer/<int:pokemon_id>/page/<int:page>", methods = ["GET", "POST"])
def trade_view(pokemon_id, page=1):
    require_login()
    if request.method == "POST":
        check_csrf()
    requester_id = session["user_id"]
    selections_json = request.form.getlist("selected_ids")
    selections = [json.loads(item) for item in selections_json]
    new_selections_json = request.form.getlist("requester_pokemon_ids")
    new_selections = [json.loads(item) for item in new_selections_json]
    id_set = [item["id"] for item in selections]
    filtered = []
    for item in selections:
        if item["page"] != page:
            filtered.append(item)
    selected_ids = filtered
    for new_id in new_selections:
        if new_id not in selected_ids:
            offer = handle_none(pokemon.get_pokemon_by_id(new_id["id"]))
            check_access(offer["owner_id"])
            selected_ids.append(new_id)
    requested_pokemon = handle_none(pokemon.get_pokemon_by_id(pokemon_id))
    in_other_offers = trades.get_pokemon_in_pending_trade(pokemon_id)
    if in_other_offers:
        flash(f"Target pokémon {requested_pokemon['name']} already part of another pending trade. This offer will be automatically rejected if any of the other offers get accepted", "info")
    if requested_pokemon["owner_id"] == requester_id:
        abort(403)
    _, pokemon_status = pokemon.get_pokemon_status(pokemon_id)
    if pokemon_status != "Listed for trading":
        abort(404)
    page_size = 9
    pokemon_count = users.get_my_pokemon_count(requester_id)
    page_count = max(math.ceil(pokemon_count /  page_size), 1)

    if page < 1:
        return redirect(f"/trading/make_offer/{pokemon_id}/page/1")
    if page > page_count:
        return redirect(f"/trading/make_offer/{pokemon_id}/page/" + str(page_count))

    requester_pokemon = users.get_my_pokemon(requester_id, page, page_size)
    return render_template(
        "create_proposal.html",
        requested_pokemon=requested_pokemon,
        requester_pokemon=requester_pokemon,
        page=page,
        page_count=page_count,
        selected_ids=selected_ids,
        id_set=id_set
    )

@app.route("/trading/")
@app.route("/trading/<int:page>")
def view_trade_listings(page=1):
    require_login()
    query = request.args.get("query")
    exclude_owner = request.args.get("exclude_owner")
    page_size = 9
    owner_to_excluded = None
    if exclude_owner:
        owner_to_excluded = session["user_id"]
    result, has_next = pokemon.get_listed_pokemon(page, page_size, query, owner_to_excluded)

    if page < 1:
        return redirect("/trading/1")
    if page > 1 and not result and not has_next:
        return redirect(f"/trading/{page - 1}")

    return render_template("/trading.html", pokemons=result, query=query, exclude_owner=exclude_owner, page=page, has_next=has_next)

@app.route("/my_pokemon/")
@app.route("/my_pokemon/<int:page>")
def my_pokemon(page=1):
    require_login()
    query = request.args.get("query")
    if not query:
        query = ""
    owner_id = session["user_id"]
    page_size = 9
    pokemon_count = users.get_my_pokemon_count(owner_id, query)
    page_count = max(math.ceil(pokemon_count /  page_size), 1)

    if page < 1:
        return redirect("/my_pokemon/1")
    if page > page_count:
        return redirect("/my_pokemon/" + str(page_count))

    result = users.get_my_pokemon(owner_id, page, page_size, query)
    statuses = pokemon.get_all_statuses()
    return render_template("/my_pokemon.html", pokemons=result, statuses=statuses, query=query, page=page, page_count=page_count)

@app.route("/my_pokemon/change_status/<int:pokemon_id>", methods=["POST"])
def change_status(pokemon_id):
    require_login()
    check_csrf()
    target = handle_none(pokemon.get_pokemon_by_id(pokemon_id))
    check_access(target["owner_id"])
    status = request.form.get("status")
    page = request.form.get("page")
    query = request.form.get("query")
    status_rows = pokemon.get_all_statuses()
    all_statuses = []
    for row in status_rows:
        all_statuses.append(row["value"])
    if status not in all_statuses:
        abort(403)
    status_id, pokemon_status = pokemon.get_pokemon_status(pokemon_id)
    if status == pokemon_status:
        return redirect(f"/my_pokemon/{page}?query={query}")
    pokemon.set_pokemon_status(status, status_id)
    pokemon.update_listed_pokemon(status, pokemon_id)
    return redirect(f"/my_pokemon/{page}?query={query}")

@app.route("/my_pokemon/stats/<string:pokemon_type>")
def my_pokemon_by_type(pokemon_type):
    require_login()
    owner_id = session["user_id"]
    result = users.get_my_pokemon_by_type(owner_id, pokemon_type)
    statuses = pokemon.get_all_statuses()
    return render_template("/my_pokemon.html", pokemons=result, statuses=statuses, query=pokemon_type)

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
    check_csrf()
    result = handle_none(pokemon.get_pokemon_by_id(pokemon_id))
    check_access(result["owner_id"])
    nickname = request.form.get("nickname")
    new_stat = request.form.get("new_stat")
    new_stat_value = request.form.get("new_stat_value")

    if nickname and nickname.strip():
        if len(nickname) > 20:
            abort(403)
        pokemon.set_nickname(nickname, pokemon_id)

    if new_stat_value and not new_stat:
        flash("A new skill must have a name", "error")
        return redirect(f"/my_pokemon/edit_pokemon/{pokemon_id}")

    if new_stat and new_stat.strip() != "":
        if not new_stat_value:
            flash("You must provide a value for a new skill", "error")
            return redirect(f"/my_pokemon/edit_pokemon/{pokemon_id}")
        if len(new_stat) > 20:
            abort(403)
        try:
            new_stat_value = int(new_stat_value)
            if new_stat_value > 200:
                raise ValueError
        except ValueError:
            flash("Value must be an integer with maximum value of 200", "error")
            return redirect(f"/my_pokemon/edit_pokemon/{pokemon_id}")

        pokemon.add_stat(pokemon_id, new_stat, new_stat_value)
    flash(f"{result['name']} successfully updated!", "success")
    return redirect(f"/my_pokemon/edit_pokemon/{pokemon_id}")

@app.route("/my_pokemon/delete/<int:pokemon_id>", methods=["POST"])
def delete_pokemon(pokemon_id):
    require_login()
    check_csrf()
    result = handle_none(pokemon.get_pokemon_by_id(pokemon_id))
    check_access(result["owner_id"])
    pokemon.remove_pokemon(pokemon_id)
    flash(f"{result['name']} successfully deleted!", "success")
    return redirect("/my_pokemon/")

@app.route("/my_pokemon/delete_stat/<int:pokemon_id>/<int:stat_id>", methods=["POST"])
def delete_stat(pokemon_id, stat_id):
    require_login()
    check_csrf()
    result = handle_none(pokemon.get_pokemon_by_id(pokemon_id))
    check_access(result["owner_id"])
    pokemon.remove_stat(stat_id)
    flash("A skill successfully removed!", "success")
    return redirect(f"/my_pokemon/edit_pokemon/{pokemon_id}")

@app.route("/capture_pokemon/<string:pokemon_name>", methods=["POST"])
def capture_pokemon(pokemon_name):
    require_login()
    check_csrf()
    success = random.randint(0, 100) < 80
    if success:
        name = request.form["name"]
        owner_id = session["user_id"]
        height = request.form["height"]
        weight = request.form["weight"]
        base_experience = request.form["base_experience"]
        next_evolution = request.form["next_evolution"]
        flavor_text = request.form["flavor_text"]
        sprite_url = request.form["sprite"]
        with urllib.request.urlopen(sprite_url) as response:
            sprite = response.read()

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

        flash(f"{pokemon_name.capitalize()} successfully captured! ({datetime.now().strftime('%H:%M:%S')})", "success")
    else:
        flash(f"DARN IT! {pokemon_name.capitalize()} escaped! Try again. ({datetime.now().strftime('%H:%M:%S')})", "error")
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
        flash("Passwords do not match", "error")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("Username is already taken", "error")
        return redirect("/register")

    flash(f"Account for username {username} was successfully created!", "success")
    return redirect("/login")

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
            session["csrf_token"] = secrets.token_hex(16)
            flash("You are logged in", "info")
            return redirect("/")
        else:
            flash("Wrong username or password", "error")
            return redirect("/login")

    return redirect("/")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    flash("You are logged out", "info")
    return redirect("/")

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response
