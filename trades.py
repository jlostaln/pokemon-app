import db

def add_trade_pending(requester_id, responder_id):
    sql = "INSERT INTO trades (requester_id, responder_id, status) VALUES (?, ?, ?)"
    db.execute(sql, [requester_id, responder_id, "pending"])

def add_trade_history(trade_id, status):
    sql = "INSERT INTO trade_history (trade_id, status) VALUES (?, ?)"
    db.execute(sql, [trade_id, status])

def add_pokemon(trade_id, pokemon_id, pokemon_name, side):
    sql = "INSERT INTO trade_pokemon (trade_id, pokemon_id, pokemon_name, side) VALUES (?, ?, ?, ?)"
    db.execute(sql, [trade_id, pokemon_id, pokemon_name, side])

def get_user_trades(user_id):
    sql = '''SELECT trades.id as trade_id,
                    trades.requester_id,
                    trades.responder_id,
                    trades.status,
                    trade_pokemon.id as trade_pokemon_id,
                    trade_pokemon.pokemon_id,
                    trade_pokemon.pokemon_name,
                    trade_pokemon.side
            FROM trades
            JOIN trade_pokemon
                  ON trades.id = trade_pokemon.trade_id
            WHERE trades.requester_id = ?
                    OR trades.responder_id = ?'''
    return db.query(sql, [user_id, user_id])
