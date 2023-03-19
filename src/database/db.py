import sqlite_utils

# Create a new SQLite database file
db = sqlite_utils.Database("../src/database/db.db")
# db = sqlite_utils.Database("../src/database/db.db")

db.execute("CREATE TABLE IF NOT EXISTS users (nickname text PRIMARY KEY, password text)")
db.execute("CREATE TABLE IF NOT EXISTS user_data (id INTEGER PRIMARY KEY, user_nickname text, vitorias INTEGER, derrotas INTEGER, empates INTEGER, FOREIGN KEY(user_nickname) REFERENCES users(nickname))")

# Insert data into the `users` and `user_data` tables
db["users"].insert_all([
    {"nickname": "a------------------------", "password": "a"},
    {"nickname": "user1--------------------", "password": "password1"},
    {"nickname": "user2--------------------", "password": "password2"},
    {"nickname": "user3--------------------", "password": "password3"},
    {"nickname": "user4--------------------", "password": "password3"},
    {"nickname": "user5--------------------", "password": "password3"},
    {"nickname": "user6--------------------", "password": "password3"},
    {"nickname": "user7--------------------", "password": "password3"},
    {"nickname": "user8--------------------", "password": "password3"},
    {"nickname": "user9--------------------", "password": "password3"},
    {"nickname": "user10-------------------", "password": "password3"},
    {"nickname": "user11-------------------", "password": "password3"},
    {"nickname": "user12-------------------", "password": "password3"},
    {"nickname": "user13-------------------", "password": "password3"},
])

db["user_data"].insert_all([
    {"user_nickname": "a------------------------", "vitorias": 1, "derrotas": 5, "empates": 3},
    {"user_nickname": "user1--------------------", "vitorias": 10, "derrotas": 5, "empates": 3},
    {"user_nickname": "user2--------------------", "vitorias": 7, "derrotas": 8, "empates": 2},
    {"user_nickname": "user3--------------------", "vitorias": 12, "derrotas": 3, "empates": 1},
    {"user_nickname": "user4--------------------", "vitorias": 12, "derrotas": 3, "empates": 1},
    {"user_nickname": "user5--------------------", "vitorias": 12, "derrotas": 3, "empates": 1},
    {"user_nickname": "user6--------------------", "vitorias": 12, "derrotas": 3, "empates": 1},
    {"user_nickname": "user7--------------------", "vitorias": 12, "derrotas": 3, "empates": 1},
    {"user_nickname": "user8--------------------", "vitorias": 12, "derrotas": 3, "empates": 1},
    {"user_nickname": "user9--------------------", "vitorias": 12, "derrotas": 3, "empates": 1},
    {"user_nickname": "user10-------------------", "vitorias": 12, "derrotas": 3, "empates": 1},
    {"user_nickname": "user11-------------------", "vitorias": 12, "derrotas": 3, "empates": 1},
    {"user_nickname": "user12-------------------", "vitorias": 12, "derrotas": 3, "empates": 1},
    {"user_nickname": "user13-------------------", "vitorias": 12, "derrotas": 3, "empates": 1},
])