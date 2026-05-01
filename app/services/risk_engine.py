from services.mt5_service import get_mt5

# ─────────────────────────────
# CONFIG (start simple)
# ─────────────────────────────
MAX_LOT = 0.5
MAX_OPEN_TRADES = 5
MAX_DAILY_LOSS = -50  # adjust to account currency
ALLOWED_SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY"]

# simple in-memory tracking (upgrade later to DB)
daily_pnl = 0


def validate_trade(symbol: str, lot: float):
    mt5 = get_mt5()

    if mt5 is None:
        return False, "MT5 not connected"

    # ───── SYMBOL CHECK ─────
    if symbol not in ALLOWED_SYMBOLS:
        return False, f"Symbol not allowed: {symbol}"

    # ───── LOT SIZE CHECK ─────
    if lot <= 0 or lot > MAX_LOT:
        return False, f"Lot size exceeds limit ({MAX_LOT})"

    # ───── OPEN TRADES LIMIT ─────
    positions = mt5.positions_get()
    if positions and len(positions) >= MAX_OPEN_TRADES:
        return False, "Max open trades reached"

    # ───── DAILY LOSS CHECK ─────
    global daily_pnl
    account = mt5.account_info()

    if account:
        equity_change = account.equity - account.balance
        if equity_change < MAX_DAILY_LOSS:
            return False, "Daily loss limit hit"

    return True, "OK"