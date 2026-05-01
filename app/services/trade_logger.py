from services.db import get_conn


def log_trade_open(ticket, symbol, type_, volume, price):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO trades (ticket, symbol, type, volume, open_price, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (ticket, symbol, type_, volume, price, "OPEN"))

    conn.commit()
    conn.close()


def update_trade_close(ticket, close_price, profit):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE trades
        SET close_price = ?, profit = ?, status = 'CLOSED'
        WHERE ticket = ?
    """, (close_price, profit, ticket))

    conn.commit()
    conn.close()


def get_trades():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM trades ORDER BY created_at DESC")
    rows = cur.fetchall()

    conn.close()

    return rows
