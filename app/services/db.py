import sqlite3

DB_NAME = "trading.db"


def get_conn():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket INTEGER,
        symbol TEXT,
        type TEXT,
        volume REAL,
        open_price REAL,
        close_price REAL,
        profit REAL,
        status TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()