import sqlite_utils

# Create a new SQLite database file
db = sqlite_utils.Database("../src/database/my_database.db")
# db = sqlite_utils.Database("../src/database/db.db")

# Create the `users` table
db.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        nickname TEXT UNIQUE,
        password TEXT
    )
    """
)

# Create the `user_data` table
db.execute(
    """
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY,
        user_nickname TEXT,
        vitorias INTEGER,
        derrotas INTEGER,
        empates INTEGER,
        FOREIGN KEY(user_nickname) REFERENCES users(nickname)
    )
    """
)

# Insert data into the `users` and `user_data` tables
db["users"].insert_all([
    {"nickname": "a", "password": "a"},
    {"nickname": "user1", "password": "password1"},
    {"nickname": "user2", "password": "password2"},
    {"nickname": "user3", "password": "password3"}
])

db["user_data"].insert_all([
    {"user_nickname": "a", "vitorias": 1, "derrotas": 5, "empates": 3},
    {"user_nickname": "user1", "vitorias": 10, "derrotas": 5, "empates": 3},
    {"user_nickname": "user2", "vitorias": 7, "derrotas": 8, "empates": 2},
    {"user_nickname": "user3", "vitorias": 12, "derrotas": 3, "empates": 1}
])