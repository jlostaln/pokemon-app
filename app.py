import sqlite3
from flask import Flask
from flask import render_template, request, redirect, session 
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
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
    sql = '''SELECT pokemon.id,
                    pokemon.name,
                    pokemon.nickname,
                    pokemon.flavor_text,
                    pokemon.sprite,
                    GROUP_CONCAT(pokemon_types.type, ', ') as types
            FROM pokemon
            LEFT JOIN pokemon_types
                    ON pokemon.id = pokemon_types.pokemon_id
            WHERE pokemon.owner_id = ?
            GROUP BY pokemon.id
            ORDER BY pokemon.id DESC'''
    result = db.query(sql, [owner_id])
    return render_template("/my_pokemon.html", pokemons=result)

@app.route("/my_pokemon/edit_pokemon/<int:pokemon_id>")
def edit_pokemon(pokemon_id):
    sql = '''SELECT pokemon.id,
                    pokemon.name,
                    pokemon.flavor_text,
                    pokemon.sprite,
                    pokemon.nickname,
                    pokemon.next_evolution,
                    GROUP_CONCAT(pokemon_types.type, ', ') as types
             FROM pokemon
             LEFT JOIN pokemon_types
                    ON pokemon.id = pokemon_types.pokemon_id
             WHERE pokemon.id = ?
             GROUP BY pokemon.id'''
    pokemon = db.query(sql, [pokemon_id])[0]
    sql = "SELECT stat, value FROM pokemon_stats WHERE pokemon_id = ?"
    stats = db.query(sql, [pokemon_id])

    return render_template("edit_pokemon.html", pokemon=pokemon, stats=stats)

@app.route("/my_pokemon/update/<int:pokemon_id>", methods=["POST"])
def update_pokemon(pokemon_id):
    nickname = request.form.get("nickname")
    new_stat = request.form.get("new_stat")
    new_stat_value = request.form.get("new_stat_value")

    if nickname is not None and nickname.strip() != "":
        sql = "UPDATE pokemon SET nickname = ? WHERE id = ?"
        db.execute(sql, [nickname, pokemon_id])

    if new_stat and new_stat.strip() != "" and new_stat_value:
        try:
            new_stat_value = int(new_stat_value)
        except ValueError:
            print("Tilaston arvon oltava kokonaisluku!") # Pitää muuttaa flash():ksi devauksen edetessä
            return redirect(f"/my_pokemon/edit_pokemon/{pokemon_id}")

        sql = "INSERT INTO pokemon_stats (pokemon_id, stat, value) VALUES (?, ?, ?)"
        db.execute(sql, [pokemon_id, new_stat, new_stat_value])

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
        types = json.loads(request.form["types"])

        try:
            sql = '''INSERT INTO pokemon (name, owner_id, height, weight, base_experience, next_evolution, flavor_text, sprite)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
            db.execute(sql, [name, owner_id, height, weight, base_experience, next_evolution, flavor_text, sprite])
            pokemon_id = db.last_insert_id()

            for stat in stats:
                sql = '''INSERT INTO pokemon_stats (pokemon_id, stat, value)
                        VALUES (?, ?, ?)'''
                db.execute(sql, [pokemon_id, stat["stat"]["name"], stat["base_stat"]])

            for t in types:
                sql = '''INSERT INTO pokemon_types (pokemon_id, type)
                        VALUES (?, ?)'''
                db.execute(sql, [pokemon_id, t["type"]["name"]])

        except sqlite3.IntegrityError:
            return "VIRHE: tallennus pokemon-tauluun epäonnistui"

        session["capture_result"] = True
    else:
        session["capture_result"] = False
    return redirect(f"/inspect/{pokemon_name}")

@app.route("/inspect/<string:pokemon_name>")
def inspect(pokemon_name):
    pokemon = api.get_pokemon_details(pokemon_name)
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
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
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

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        results = db.query(sql, [username])

        if results:
            result = results[0]
            user_id = result["id"]
            password_hash = result["password_hash"]

            if check_password_hash(password_hash, password):
                session["user_id"] = user_id
                session["username"] = username
                return redirect("/")
            else:
                return "VIRHE: väärä tunnus tai salasana"
        else:
            return "VIRHE: käyttäjätunnusta ei löytynyt"

    return redirect("/")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")
