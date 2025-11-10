import sqlite3
from flask import Flask, abort
from flask import render_template, request, redirect, session 
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import pokeapi

app = Flask(__name__)

app.secret_key = config.secret_key
base_url = config.BASE_URL
api = pokeapi.PokeApi()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/location-area/")
def redirect_to_start():
    return redirect("/location-area/start")

@app.route("/location-area/<string:direction>")
def get_location_areas(direction):
    if 'next_locations_url' not in session:
        session['next_locations_url'] = None
    if 'previous_locations_url' not in session:
        session['previous_locations_url'] = None

    if direction == "next" and session["next_locations_url"]:
        url = session["next_locations_url"]
    elif direction == "previous" and session["previous_locations_url"]:
        url = session["previous_locations_url"]
    elif direction == "start":
        url = base_url + "/location-area/"
    else:
        abort(404)

    result = api.get_location_areas(url)
    areas = result[0]
    session["next_locations_url"] = result[1]
    session["previous_locations_url"] = result[2]

    return render_template("location-areas.html", areas=areas)

@app.route("/location-details/<string:area_name>")
def get_location_details(area_name):
    url = base_url + "/location-area/" + area_name
    encounters = api.get_encounters(url)

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
