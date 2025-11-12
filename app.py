import sqlite3
from flask import Flask
from flask import render_template, request, redirect, session 
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import pokeapi

app = Flask(__name__)

app.secret_key = config.secret_key
api = pokeapi.PokeApi()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inspect/<string:pokemon_name>")
def inspect(pokemon_name):
    pokemon = api.get_pokemon_details(pokemon_name)
    additional_information = api.get_pokemon_additional_info(pokemon)
    pokemon.update(additional_information)
    return render_template("inspect.html", pokemon=pokemon)

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

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")
