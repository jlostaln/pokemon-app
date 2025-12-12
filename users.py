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
                    pokemon.owner_id,
                    pokemon.name,
                    pokemon.nickname,
                    pokemon.flavor_text,
                    pokemon.sprite,
                    GROUP_CONCAT(pokemon_types.type, ', ') as types,
                    pokemon_status.value as status
            FROM pokemon
            LEFT JOIN pokemon_types
                    ON pokemon.id = pokemon_types.pokemon_id
            LEFT JOIN pokemon_status
                    ON pokemon.id = pokemon_status.pokemon_id
            WHERE pokemon.owner_id = ?
            GROUP BY pokemon.id
            ORDER BY pokemon.id DESC'''
    result = db.query(sql, [owner_id])
    return result

def get_my_pokemon_by_type(owner_id, pokemon_type):
    sql = '''SELECT pokemon.id,
                    pokemon.name,
                    pokemon.nickname,
                    pokemon.flavor_text,
                    pokemon.sprite,
                    GROUP_CONCAT(pokemon_types.type, ', ') as types,
                    pokemon_status.value as status
            FROM pokemon
            LEFT JOIN pokemon_types
                    ON pokemon.id = pokemon_types.pokemon_id
            LEFT JOIN pokemon_status
                    ON pokemon.id = pokemon_status.pokemon_id
            WHERE pokemon.id in (SELECT pokemon.id
                                FROM pokemon, pokemon_types
                                WHERE pokemon.owner_id = ?
                                AND pokemon.id = pokemon_types.pokemon_id
                                And pokemon_types.type = ?)
            GROUP BY pokemon.id
            ORDER BY pokemon.id DESC'''
    result = db.query(sql, [owner_id, pokemon_type])
    return result

def get_pokemon_count(owner_id):
    sql = '''SELECT count(*) as total_count
            FROM pokemon
            WHERE pokemon.owner_id = ?'''
    result = db.query(sql, [owner_id])[0]
    return result

def get_pokemon_count_by_type(owner_id):
    sql = '''SELECT pokemon_types.type,
                    count(*) as type_count
            FROM pokemon
            LEFT JOIN pokemon_types
                    ON pokemon.id = pokemon_types.pokemon_id
            WHERE pokemon.owner_id = ?
            GROUP BY pokemon_types.type
            ORDER BY type_count DESC, pokemon_types.type'''
    result = db.query(sql, [owner_id])
    return result
