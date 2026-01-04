DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS pokemon;
DROP TABLE IF EXISTS pokemon_stats;
DROP TABLE IF EXISTS pokemon_types;
DROP TABLE IF EXISTS pokemon_status;
DROP TABLE IF EXISTS listed_pokemon;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS trades;
DROP TABLE IF EXISTS trade_pokemon;
DROP TABLE IF EXISTS trade_history;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE,
  password_hash TEXT
);

CREATE TABLE pokemon (
  id INTEGER PRIMARY KEY,
  owner_id INTEGER REFERENCES users(id),
  name TEXT,
  nickname TEXT,
  height REAL,
  weight REAL,
  base_experience INTEGER,
  next_evolution TEXT,
  flavor_text TEXT,
  sprite BLOB
);

CREATE TABLE pokemon_stats (
  id INTEGER PRIMARY KEY,
  pokemon_id INTEGER REFERENCES pokemon(id) ON DELETE CASCADE,
  stat TEXT,
  value TEXT,
  is_base_stat INTEGER DEFAULT 0
);

CREATE TABLE pokemon_types (
  id INTEGER PRIMARY KEY,
  pokemon_id INTEGER REFERENCES pokemon(id) ON DELETE CASCADE,
  type TEXT
);

CREATE TABLE status (
  id INTEGER PRIMARY KEY,
  value TEXT
);

CREATE TABLE pokemon_status (
  id INTEGER PRIMARY KEY,
  pokemon_id INTEGER REFERENCES pokemon(id) ON DELETE CASCADE,
  value TEXT
);

CREATE TABLE listed_pokemon (
  id INTEGER PRIMARY KEY REFERENCES pokemon(id) ON DELETE CASCADE
);

CREATE TABLE trades (
  id INTEGER PRIMARY KEY,
  requester_id INTEGER REFERENCES users(id),
  responder_id INTEGER REFERENCES users(id),
  status TEXT CHECK(status IN ('pending', 'rejected', 'accepted', 'completed'))
);

CREATE TABLE trade_pokemon (
  id INTEGER PRIMARY KEY,
  trade_id INTEGER REFERENCES trades(id) ON DELETE CASCADE,
  pokemon_id INTEGER REFERENCES pokemon(id) ON DELETE SET NULL,
  pokemon_name TEXT,
  side TEXT CHECK(side IN ('requester','responder'))
);

CREATE TABLE trade_history (
  id INTEGER PRIMARY KEY,
  trade_id INTEGER REFERENCES trades(id) ON DELETE CASCADE,
  status TEXT CHECK(status IN ('pending', 'rejected', 'accepted', 'completed')),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);

CREATE INDEX idx_pokemon_owner_id ON pokemon(owner_id);
CREATE INDEX idx_pokemon_name ON pokemon(name);

CREATE INDEX idx_pokemon_types_pokemon_id ON pokemon_types(pokemon_id);
CREATE INDEX idx_pokemon_types_type ON pokemon_types(type);

CREATE INDEX idx_pokemon_status_pokemon_id ON pokemon_status(pokemon_id);
CREATE INDEX idx_pokemon_status_value ON pokemon_status(value);

CREATE INDEX idx_pokemon_stats_pokemon_id ON pokemon_stats(pokemon_id);

CREATE INDEX idx_trades_requester_id ON trades(requester_id);
CREATE INDEX idx_trades_responder_id ON trades(responder_id);
CREATE INDEX idx_trades_status ON trades(status);
CREATE INDEX idx_trades_requester_status ON trades(requester_id, status);
CREATE INDEX idx_trades_responder_status ON trades(responder_id, status);

CREATE INDEX idx_trade_pokemon_trade_id ON trade_pokemon(trade_id);
CREATE INDEX idx_trade_pokemon_pokemon_id ON trade_pokemon(pokemon_id);

CREATE INDEX idx_trade_history_trade_id ON trade_history(trade_id);
