CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE initiatives (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users,
    votes INTEGER DEFAULT 0
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT,
    created_at TEXT,
    user_id INTEGER REFERENCES users,
    initiative_id INTEGER REFERENCES initiatives
);

CREATE TABLE hashtags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE initiative_hashtags (
    initiative_id INTEGER NOT NULL,
    hashtag_id INTEGER NOT NULL,
    FOREIGN KEY (initiative_id) REFERENCES initiatives(id),
    FOREIGN KEY (hashtag_id) REFERENCES hashtags(id),
    UNIQUE(initiative_id, hashtag_id)
);


CREATE TABLE initiative_votes (
    initiative_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    UNIQUE(user_id, initiative_id),
    FOREIGN KEY (initiative_id) REFERENCES initiatives(id)
);
