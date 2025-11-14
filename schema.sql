CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE,
  password_hash TEXT
);

DROP TABLE IF EXISTS pokemon;
DROP TABLE IF EXISTS pokemon_stats;
DROP TABLE IF EXISTS pokemon_types;

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
  value TEXT
);

CREATE TABLE pokemon_types (
  id INTEGER PRIMARY KEY,
  pokemon_id INTEGER REFERENCES pokemon(id) ON DELETE CASCADE,
  type TEXT
);
