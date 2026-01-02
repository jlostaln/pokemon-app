import random
import sqlite3
import users
import urllib.request
from app import app

# Test config
USER_COUNT = 1000
POKEMON_COUNT = 10**6
TYPES = ["fire", "water", "grass", "electric", "psychic", "normal", "rock", "ground", "bug", "poison"]
STATUS_VALUES = ["Listed for trading"]
STATS = ["hp", "attack", "defense", "special-attack", "special-defence", "speed"]
TRADE_COUNT = 10**6
PIKACHU_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
with urllib.request.urlopen(PIKACHU_URL) as response:
    pikachu_sprite = response.read()

db = sqlite3.connect("database.db")

print("Clearing tables...")
tables = [
    "trade_history", "trade_pokemon", "trades",
    "pokemon_stats", "pokemon_types", "pokemon_status",
    "pokemon", "users"
]
for t in tables:
    db.execute(f"DELETE FROM {t}")

db.commit()
db.close()

print("Create username=test, password=test...")
with app.app_context():
    users.create_user("test", "test") # test user (id=1) to login with

db = sqlite3.connect("database.db")

print("Inserting users...")
for i in range(1, USER_COUNT + 1):
    db.execute("INSERT INTO users (username) VALUES (?)", ["user" + str(i)])

print("Inserting Pokémon...")
for i in range(1, POKEMON_COUNT + 1):
    owner_id = random.randint(1, USER_COUNT)
    name = f"pikachu"
    nickname = f"pika{i}"
    height = i
    weight = i
    base_exp = i
    next_evo = "next"
    flavor = f"Flavor text {i}"
    sprite = pikachu_sprite

    db.execute('''
        INSERT INTO pokemon (name, owner_id, nickname, height, weight, base_experience,
                             next_evolution, flavor_text, sprite)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', [name, owner_id, nickname, height, weight, base_exp, next_evo, flavor, sprite])

print("Inserting Pokémon types...")
for pokemon_id in range(1, POKEMON_COUNT + 1):
    pokemon_type = random.choice(TYPES)
    db.execute('''
        INSERT INTO pokemon_types (pokemon_id, type)
        VALUES (?, ?)
    ''', [pokemon_id, pokemon_type])

print("Inserting Pokémon stats...")
for pokemon_id in range(1, POKEMON_COUNT + 1):
    for stat in STATS:
        value = random.randint(10, 200)
        db.execute('''
            INSERT INTO pokemon_stats (pokemon_id, stat, value, is_base_stat)
            VALUES (?, ?, ?, 1)
        ''', [pokemon_id, stat, value])

print("Inserting Pokémon statuses...")
for pokemon_id in range(1, POKEMON_COUNT + 1):
    status = STATUS_VALUES[0]
    db.execute('''
        INSERT INTO pokemon_status (pokemon_id, value)
        VALUES (?, ?)
    ''', [pokemon_id, status])

    db.execute('''
        INSERT INTO listed_pokemon (id)
        VALUES (?)
    ''', [pokemon_id])

print("Inserting trades...")
for i in range(1, TRADE_COUNT + 1):
    requester = random.randint(1, USER_COUNT)
    responder = random.randint(1, USER_COUNT)
    status = random.choice(["pending", "rejected", "completed"])

    db.execute('''
        INSERT INTO trades (requester_id, responder_id, status)
        VALUES (?, ?, ?)
    ''', [requester, responder, status])

print("Inserting trade Pokémon...")
for trade_id in range(1, TRADE_COUNT + 1):
    p1 = random.randint(1, POKEMON_COUNT)
    db.execute('''
        INSERT INTO trade_pokemon (trade_id, pokemon_id, pokemon_name, side)
        VALUES (?, ?, ?, 'requester')
    ''', [trade_id, p1, f"pokemon{p1}"])

    p2 = random.randint(1, POKEMON_COUNT)
    db.execute('''
        INSERT INTO trade_pokemon (trade_id, pokemon_id, pokemon_name, side)
        VALUES (?, ?, ?, 'responder')
    ''', [trade_id, p2, f"pokemon{p2}"])

print("Inserting trade history...")
for trade_id in range(1, TRADE_COUNT + 1):
    for _ in range(random.randint(1, 3)):
        status = random.choice(["pending", "rejected", "completed"])
        db.execute('''
            INSERT INTO trade_history (trade_id, status)
            VALUES (?, ?)
        ''', [trade_id, status])

print("Committing...")
db.commit()
db.close()
print("Done! Large test dataset created.")
