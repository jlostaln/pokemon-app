import sqlite3
from flask import Flask
from flask import render_template, request, redirect, session 
import users
import config
import db
import pokemon
import pokeapi
import random
import json

app = Flask(__name__)

app.secret_key = config.secret_key
api = pokeapi.PokeApi()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/my_pokemon/")
def my_pokemon():
    owner_id = session["user_id"]
    result = users.get_my_pokemon(owner_id)
    statuses = pokemon.get_all_statuses()
    return render_template("/my_pokemon.html", pokemons=result, statuses=statuses)

@app.route("/my_pokemon/change_status/<int:pokemon_id>", methods=["POST"])
def change_status(pokemon_id):
    status = request.form.get("status")
    status_id, pokemon_status = pokemon.get_pokemon_status(pokemon_id)
    if status == pokemon_status:
        return redirect(f"/my_pokemon#pokemon-{pokemon_id}")
    pokemon.set_pokemon_status(status, status_id)
    return redirect(f"/my_pokemon#pokemon-{pokemon_id}")

@app.route("/my_pokemon/<string:pokemon_type>")
def my_pokemon_by_type(pokemon_type):
    owner_id = session["user_id"]
    result = users.get_my_pokemon_by_type(owner_id, pokemon_type)
    statuses = pokemon.get_all_statuses()
    return render_template("/my_pokemon.html", pokemons=result, statuses=statuses)

@app.route("/my_pokemon/stats/")
def my_pokemon_stats():
    owner_id = session["user_id"]
    count = users.get_pokemon_count(owner_id)[0]
    count_by_type = users. get_pokemon_count_by_type(owner_id)
    return render_template("/my_stats.html", count=count, count_by_type=count_by_type)


@app.route("/my_pokemon/edit_pokemon/<int:pokemon_id>")
def edit_pokemon(pokemon_id):
    result = pokemon.get_pokemon_by_id(pokemon_id)
    stats = pokemon.get_pokemon_stats(pokemon_id)
    return render_template("edit_pokemon.html", pokemon=result, stats=stats)

@app.route("/my_pokemon/update/<int:pokemon_id>", methods=["POST"])
def update_pokemon(pokemon_id):
    nickname = request.form.get("nickname")
    new_stat = request.form.get("new_stat")
    new_stat_value = request.form.get("new_stat_value")

    if nickname is not None and nickname.strip() != "":
        pokemon.set_nickname(nickname, pokemon_id)

    if new_stat and new_stat.strip() != "" and new_stat_value:
        try:
            new_stat_value = int(new_stat_value)
        except ValueError:
            print("Tilaston arvon oltava kokonaisluku!") # Pitää muuttaa flash():ksi devauksen edetessä
            return redirect(f"/my_pokemon/edit_pokemon/{pokemon_id}")

        pokemon.add_stat(pokemon_id, new_stat, new_stat_value)
    return redirect(f"/my_pokemon/edit_pokemon/{pokemon_id}")

@app.route("/my_pokemon/delete/<int:pokemon_id>", methods=["POST"])
def delete_pokemon(pokemon_id):
    pokemon.remove_pokemon(pokemon_id)
    return redirect("/my_pokemon/")

@app.route("/my_pokemon/delete_stat/<int:pokemon_id>/<int:stat_id>", methods=["POST"])
def delete_stat(pokemon_id, stat_id):
    pokemon.remove_stat(stat_id)
    return redirect(f"/my_pokemon/edit_pokemon/{pokemon_id}")

@app.route("/capture_pokemon/<string:pokemon_name>", methods=["POST"])
def capture_pokemon(pokemon_name):
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

            pokemon.add_pokemon_status(pokemon_id, owner_id)

        except Exception as e:
            return f"VIRHE: {e}"

        session["capture_result"] = True
    else:
        session["capture_result"] = False
    return redirect(f"/inspect/{pokemon_name}")

@app.route("/inspect/<string:pokemon_name>")
def inspect(pokemon_name):
    pokemon = api.get_pokemon_details(pokemon_name)
    if pokemon is None:
        return redirect(f'/encounters/{session["current_area"]}')
    additional_information = api.get_pokemon_additional_info(pokemon)
    pokemon.update(additional_information)
    capture_result = session.pop("capture_result", None)
    return render_template("inspect.html", pokemon=pokemon, capture_result=capture_result)

@app.route("/location-area/")
def redirect_to_start():
    return redirect("/location-area/start")

@app.route("/location-area/<string:direction>")
def get_location_areas(direction):
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
