import sqlite3

def db_conn(db_path="fplbuddy.db"):
    conn = sqlite3.connect(db_path)
    return conn

def init_db(db_path="fplbuddy.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_id INTEGER UNIQUE,
        season TEXT,
        matchday INTEGER,
        competition TEXT,
        type TEXT,
        match_date TEXT,
        status TEXT,
        home_team_full_name TEXT,
        home_team_short_name TEXT,
        home_team_abbr TEXT,
        home_team_crest TEXT,
        away_team_full_name TEXT,
        away_team_short_name TEXT,
        away_team_abbr TEXT,
        away_team_crest TEXT,
        home_team_ht_score INTEGER,
        away_team_ht_score INTEGER,
        home_team_ft_score INTEGER,
        away_team_ft_score INTEGER,
        winner TEXT,
        referee TEXT,
        inserted_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS table_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        snapshot_id INTEGER,
        type TEXT,               -- 'overall', 'home', 'away', 'form5', 'form10'
        team_name TEXT,
        played INTEGER,
        wins INTEGER,
        draws INTEGER,
        losses INTEGER,
        goals_for INTEGER,
        goals_against INTEGER,
        goal_difference INTEGER,
        points INTEGER,
        generated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    conn.commit()
    conn.close()

def insert_match_row(data, table_name, db_path="fplbuddy.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    sql = f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, tuple(data.values()))
    conn.commit()
    conn.close()

def insert_row_snapshot(data, table_name, db_path="fplbuddy.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, tuple(data.values()))
    conn.commit()
    conn.close()

def get_last_stored_matchweek(db_path="fplbuddy.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT MAX(matchday) FROM matches")
    row = cur.fetchone()
    conn.close()

    return row[0] if row[0] else 0


init_db()

