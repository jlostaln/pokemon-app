from werkzeug.security import generate_password_hash, check_password_hash
import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None

def get_my_pokemon(owner_id):
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
    return result
