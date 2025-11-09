CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE initiatives (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT,
    created_at TEXT,
    user_id INTEGER REFERENCES users,
    initiative_id INTEGER REFERENCES initiatives
);