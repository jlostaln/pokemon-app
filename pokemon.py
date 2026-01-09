import db

def get_pokemon_by_id(pokemon_id):
    sql = '''SELECT pokemon.id,
                    pokemon.name,
                    pokemon.owner_id,
                    pokemon.flavor_text,
                    pokemon.nickname,
                    pokemon.next_evolution,
                    GROUP_CONCAT(pokemon_types.type, ', ') as types
             FROM pokemon
             LEFT JOIN pokemon_types
                    ON pokemon.id = pokemon_types.pokemon_id
             WHERE pokemon.id = ?
             GROUP BY pokemon.id'''
    pokemon = db.query(sql, [pokemon_id])
    return pokemon[0] if pokemon else None

def get_pokemon_stats(pokemon_id):
    sql = "SELECT id, stat, value, is_base_stat FROM pokemon_stats WHERE pokemon_id = ?"
    stats = db.query(sql, [pokemon_id])
    return stats

def get_pokemon_sprite(pokemon_id):
    sql = "SELECT sprite FROM pokemon WHERE id = ?"
    result = db.query(sql, [pokemon_id])
    return result[0][0] if result else None

def get_listed_pokemon(page, page_size, query=None, owner_id=None):
    sql = '''SELECT listed_pokemon.id as listed_pokemon_id,
                    pokemon.id,
                    pokemon.owner_id,
                    users.username,
                    pokemon.name,
                    pokemon.nickname,
                    pokemon.flavor_text,
                    GROUP_CONCAT(pokemon_types.type, ', ') as types
            FROM listed_pokemon
            JOIN pokemon
                    ON pokemon.id = listed_pokemon.id
            JOIN users
                    ON users.id = pokemon.owner_id
            JOIN pokemon_types
                    ON pokemon.id = pokemon_types.pokemon_id
            WHERE 1 = 1'''
    params = []

    if query:
        sql += '''
            AND (pokemon.name LIKE ?
                    OR EXISTS ( SELECT 1
                                FROM pokemon_types
                                WHERE pokemon_types.pokemon_id = pokemon.id
                                AND pokemon_types.type LIKE ?))'''
        like = query + "%"
        params.extend([like, like])

    if owner_id:
        sql += '''
            AND pokemon.owner_id != ?'''
        params.append(owner_id)

    sql += '''
            GROUP BY pokemon.id
            ORDER BY pokemon.id DESC
            LIMIT ? OFFSET ?'''

    limit = page_size + 1
    offset = page_size * (page - 1)
    params.extend([limit, offset])

    result = db.query(sql, params)
    has_next = len(result) > page_size
    result = result[:page_size]

    return result, has_next


def set_nickname(nickname, pokemon_id):
    sql = "UPDATE pokemon SET nickname = ? WHERE id = ?"
    db.execute(sql, [nickname, pokemon_id])

def add_pokemon_status(pokemon_id):
    sql = "INSERT INTO pokemon_status (pokemon_id) VALUES (?)"
    db.execute(sql, [pokemon_id])

def add_stat(pokemon_id, stat_name, stat_value, is_base_stat=0):
    sql = "INSERT INTO pokemon_stats (pokemon_id, stat, value, is_base_stat) VALUES (?, ?, ?, ?)"
    db.execute(sql, [pokemon_id, stat_name, stat_value, is_base_stat])

def add_type(pokemon_id, type_name):
    sql = '''INSERT INTO pokemon_types (pokemon_id, type)
            VALUES (?, ?)'''
    db.execute(sql, [pokemon_id, type_name])

def add_pokemon(name, owner_id, height, weight, base_experience,
                next_evolution, flavor_text, sprite):

    sql = '''INSERT INTO pokemon (name, owner_id, height, weight, base_experience,
                                    next_evolution, flavor_text, sprite)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    db.execute(sql, [name, owner_id, height, weight, base_experience,
                     next_evolution, flavor_text, sprite])

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

def update_listed_pokemon(status, pokemon_id):
    sql = "SELECT id FROM listed_pokemon WHERE id = ?"
    result = db.query(sql, [pokemon_id])
    id_exists = result[0][0] if result else None

    if id_exists:
        if status != "Listed for trading":
            sql = "DELETE FROM listed_pokemon WHERE id = ?"
            db.execute(sql, [pokemon_id])
    else:
        if status == "Listed for trading":
            sql = "INSERT INTO listed_pokemon (id) VALUES (?)"
            db.execute(sql, [pokemon_id])


def get_pokemon_status(pokemon_id):
    sql = "SELECT id, value FROM pokemon_status WHERE pokemon_id = ?"
    status = db.query(sql, [pokemon_id])
    return status[0][0], status[0][1] if status else None
