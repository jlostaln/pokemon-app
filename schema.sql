CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE,
  password_hash TEXT
);

DROP TABLE IF EXISTS pokemon;
DROP TABLE IF EXISTS pokemon_stats;
DROP TABLE IF EXISTS pokemon_types;
DROP TABLE IF EXISTS pokemon_status;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS trades;
DROP TABLE IF EXISTS trade_pokemon;
DROP TABLE IF EXISTS trade_history;

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
  sprite TEXT
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
  owner_id INTEGER REFERENCES users(id),
  value TEXT
);

CREATE TABLE trades (
  id INTEGER PRIMARY KEY,
  requester_id INTEGER REFERENCES users(id),
  responder_id INTEGER REFERENCES users(id),
  status TEXT CHECK(status IN ('pending', 'cancelled', 'rejected', 'accepted', 'completed'))
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
  status TEXT CHECK(status IN ('pending', 'cancelled', 'rejected', 'accepted', 'completed')),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
