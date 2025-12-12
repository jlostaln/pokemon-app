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


