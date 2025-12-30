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

def get_trade(trade_id):
    sql = '''SELECT trades.id,
                    trades.requester_id,
                    trades.responder_id,
                    trades.status
            FROM trades
            WHERE trades.id = ?'''
    trade = db.query(sql, [trade_id])
    return trade[0] if trade else None

def get_user_trade_count(user_id, filter=None):
    sql = '''SELECT count(*)
            FROM trades
            WHERE (trades.requester_id = ?
                    OR trades.responder_id = ?)'''
    params = [user_id, user_id]

    if filter:
        sql += '''AND trades.status LIKE ?'''
        like = "%" + filter + "%"
        params.extend([like])

    return db.query(sql, params)[0][0]

def get_user_trades(user_id, page, page_size, filter=None):
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
            WHERE trades.id in (SELECT id
                                FROM trades
                                WHERE (trades.requester_id = ? OR trades.responder_id = ?)'''
    params = [user_id, user_id]

    if filter:
        sql += '''              AND trades.status LIKE ?'''
        like = "%" + filter + "%"
        params.extend([like])

    sql += '''
                                ORDER BY id DESC
                                LIMIT ? OFFSET ?)
            ORDER BY trades.id DESC'''

    limit = page_size
    offset = page_size * (page - 1)
    params.extend([limit, offset])

    return db.query(sql, params)

def swap_owners(trade_id, requester_id, responder_id):
    sql = '''UPDATE pokemon SET owner_id = ?
            WHERE id IN (SELECT pokemon_id
                        FROM trade_pokemon
                        WHERE trade_id = ?
                        AND side = 'responder')'''
    db.execute(sql, [requester_id, trade_id])

    sql = '''UPDATE pokemon SET owner_id = ?
            WHERE id IN (SELECT pokemon_id
                        FROM trade_pokemon
                        WHERE trade_id = ?
                        AND side = 'requester')'''
    db.execute(sql, [responder_id, trade_id])

def set_trade_status(trade_id, status):
    sql = "UPDATE trades SET status = ? WHERE id = ?"
    db.execute(sql, [status, trade_id])

def accept_trade(trade_id, requester_id, responder_id):
    set_trade_status(trade_id, "accepted")
    add_trade_history(trade_id, "accepted")
    swap_owners(trade_id, requester_id, responder_id)
    set_trade_status(trade_id, "completed")
    add_trade_history(trade_id, "completed")

def reject_trade(trade_id):
    set_trade_status(trade_id, "rejected")
    add_trade_history(trade_id, "rejected")

def cancel_trade(trade_id):
    sql = "DELETE FROM trades WHERE id = ?"
    db.execute(sql, [trade_id])
