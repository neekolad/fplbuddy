import sqlite3

DB_PATH = "fplbuddy.db"  # change this if your DB file is elsewhere

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # allows dict-style access
    return conn