import sqlite3

DB_PATH = "data/srznuvp.sqlite"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
