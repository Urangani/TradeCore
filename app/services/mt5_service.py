import mt5linux
import time

def get_mt5(max_attempts=10, delay=2):
    """
    Try to connect to the MT5Linux bridge with retries.
    max_attempts: number of times to retry before giving up
    delay: seconds to wait between attempts
    """
    for attempt in range(1, max_attempts + 1):
        try:
            return mt5linux.MetaTrader5()
        except ConnectionRefusedError:
            print(f"[WARN] MT5 bridge not available (attempt {attempt}/{max_attempts})")
            time.sleep(delay)
    print("[ERROR] Could not connect to MT5 bridge after retries.")
    return None


# Example usage
mt5 = get_mt5()

def init():
    if mt5 is None:
        raise Exception("MT5Linux bridge not available")
    if not mt5.initialize():
        raise Exception("MT5Linux connection failed")
    print(mt5.account_info())

def shutdown():
    if mt5:
        mt5.shutdown()

def get_account_info():
    if mt5 is None:
        return None
    info = mt5.account_info()
    if info is None:
        return None
    return {
        "balance": info.balance,
        "equity": info.equity,
        "margin": info.margin,
        "profit": info.profit,
    }

def get_open_positions():
    if mt5 is None:
        return []
    positions = mt5.positions_get()
    if positions is None:
        return []
    return [
        {
            "symbol": p.symbol,
            "volume": p.volume,
            "type": "BUY" if p.type == 0 else "SELL",
            "profit": p.profit,
        }
        for p in positions
    ]
