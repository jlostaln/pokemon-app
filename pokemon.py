import db

def get_pokemon_by_id(pokemon_id):
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
    return pokemon

def get_pokemon_stats(pokemon_id):
    sql = "SELECT id, stat, value, is_base_stat FROM pokemon_stats WHERE pokemon_id = ?"
    stats = db.query(sql, [pokemon_id])
    return stats

def get_listed_pokemon():
    sql = '''SELECT pokemon.id,
                    pokemon.owner_id,
                    pokemon.name,
                    pokemon.nickname,
                    pokemon.flavor_text,
                    pokemon.sprite,
                    GROUP_CONCAT(pokemon_types.type, ', ') as types
            FROM pokemon
            LEFT JOIN pokemon_types
                    ON pokemon.id = pokemon_types.pokemon_id
            WHERE pokemon.id in ( SELECT pokemon_id
                                FROM pokemon_status
                                WHERE value = ?)
            GROUP BY pokemon.id
            ORDER BY pokemon.id DESC'''
    result = db.query(sql, ['Listattu'])
    return result

def set_nickname(nickname, pokemon_id):
    sql = "UPDATE pokemon SET nickname = ? WHERE id = ?"
    db.execute(sql, [nickname, pokemon_id])

def add_pokemon_status(pokemon_id, owner_id):
    sql = "INSERT INTO pokemon_status (pokemon_id, owner_id) VALUES (?, ?)"
    db.execute(sql, [pokemon_id, owner_id])

def add_stat(pokemon_id, stat_name, stat_value, is_base_stat=0):
    sql = "INSERT INTO pokemon_stats (pokemon_id, stat, value, is_base_stat) VALUES (?, ?, ?, ?)"
    db.execute(sql, [pokemon_id, stat_name, stat_value, is_base_stat])

def add_type(pokemon_id, type_name):
    sql = '''INSERT INTO pokemon_types (pokemon_id, type)
            VALUES (?, ?)'''
    db.execute(sql, [pokemon_id, type_name])

def add_pokemon(name, owner_id, height, weight, base_experience, next_evolution, flavor_text, sprite):

    sql = '''INSERT INTO pokemon (name, owner_id, height, weight, base_experience, next_evolution, flavor_text, sprite)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    db.execute(sql, [name, owner_id, height, weight, base_experience, next_evolution, flavor_text, sprite])

def remove_pokemon(pokemon_id):
    sql = "DELETE FROM pokemon WHERE id = ?"
    db.execute(sql, [pokemon_id])

def remove_stat(stat_id):
    sql = "DELETE FROM pokemon_stats WHERE id = ? AND is_base_stat = 0"
    db.execute(sql, [stat_id])

def get_all_statuses():
    sql = "SELECT value FROM status ORDER BY id DESC"
    statuses = db.query(sql)
    return statuses

def set_pokemon_status(status, status_id):
    sql = "UPDATE pokemon_status SET value = ? WHERE id = ?"
    db.execute(sql, [status, status_id])

def get_pokemon_status(pokemon_id):
    sql = "SELECT id, value FROM pokemon_status WHERE pokemon_id = ?"
    status = db.query(sql, [pokemon_id])[0]
    return status[0], status[1]
