import mt5linux
import time


mt5 = None


def connect(max_attempts=5, delay=1):
    global mt5

    for attempt in range(1, max_attempts + 1):
        try:
            mt5 = mt5linux.MetaTrader5()
            if mt5.initialize():
                print("[INFO] MT5 connected")
                return mt5
        except Exception as e:
            print(f"[WARN] Connection failed ({attempt}): {e}")

        time.sleep(delay)

    print("[ERROR] Could not connect to MT5")
    mt5 = None
    return None


def get_mt5():
    global mt5

    # reconnect if lost
    if mt5 is None:
        return connect()

    return mt5




def init():
    mt5 = connect()

    if mt5:
        print("[STARTUP] MT5 connected")
        info = mt5.account_info()
        if info:
            print(f"[ACCOUNT] Balance: {info.balance}")
    else:
        print("[STARTUP WARNING] MT5 not available at startup")



def shutdown():
    global mt5

    if mt5:
        try:
            mt5.shutdown()
            print("[SHUTDOWN] MT5 connection closed")
        except Exception as e:
            print(f"[SHUTDOWN ERROR] {e}")



def get_account_info():
    mt5 = get_mt5()
    if mt5 is None:
        return {"error": "MT5 not connected"}

    info = mt5.account_info()
    if info is None:
        return {"error": "Failed to fetch account info"}

    return {
        "balance": info.balance,
        "equity": info.equity,
        "margin": info.margin,
        "profit": info.profit,
    }



def get_open_positions(symbol: str = None):
    mt5 = get_mt5()
    if mt5 is None:
        return []
    positions = mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()
    if positions is None:
        return []
    return [
        {
            "symbol": p.symbol,
            "volume": p.volume,
            "type": "BUY" if p.type == 0 else "SELL",
            "profit": p.profit,
            "ticket": p.ticket,
        }
        for p in positions
    ]




def open_trade(symbol: str, lot: float, order_type: str):
    mt5 = get_mt5()
    if mt5 is None:
        return {"error": "MT5 not connected"}

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return {"error": "Symbol not found"}

    price = tick.ask if order_type == "BUY" else tick.bid

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY if order_type == "BUY" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": 10,
        "magic": 123456,
        "comment": "app_trade",
    }

    result = mt5.order_send(request)

    if result is None:
        return {"error": mt5.last_error()}

    return {"status": result.retcode}


def close_trade(ticket: int):
    mt5 = get_mt5()
    if mt5 is None:
        return {"error": "MT5 not connected"}

    positions = mt5.positions_get(ticket=ticket)
    if not positions:
        return {"error": "Position not found"}

    pos = positions[0]
    tick = mt5.symbol_info_tick(pos.symbol)

    close_type = mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY
    price = tick.bid if pos.type == 0 else tick.ask

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": pos.symbol,
        "volume": pos.volume,
        "type": close_type,
        "position": pos.ticket,
        "price": price,
        "deviation": 10,
        "magic": 123456,
    }

    result = mt5.order_send(request)

    if result is None:
        return {"error": mt5.last_error()}

    return {"status": result.retcode}

def get_symbol_price(symbol: str):
    mt5 = get_mt5()
    if mt5 is None:
        return None
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return None
    return {"symbol": symbol, "bid": tick.bid, "ask": tick.ask, "time": tick.time}

