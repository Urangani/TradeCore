from fastapi import APIRouter
from schemas.trade import OpenTradeRequest, CloseTradeRequest
from services.mt5_service import get_mt5
from services.risk_engine import validate_trade

router = APIRouter()

def get_filling_mode(mt5, symbol):
    info = mt5.symbol_info(symbol)

    if info is None:
        return mt5.ORDER_FILLING_IOC

    # safest fallback logic
    if info.filling_mode == 1:
        return mt5.ORDER_FILLING_FOK
    elif info.filling_mode == 2:
        return mt5.ORDER_FILLING_IOC
    else:
        return mt5.ORDER_FILLING_RETURN

def safe_result(result):
    return {
        "retcode": result.retcode,
        "deal": result.deal,
        "order": result.order,
        "volume": result.volume,
        "price": result.price,
        "bid": result.bid,
        "ask": result.ask,
        "comment": result.comment,
    }

@router.post("/trade/open")
def open_trade(payload: OpenTradeRequest):
    mt5 = get_mt5()

    if mt5 is None:
        return {"status": "error", "message": "MT5 not connected"}

    # ─────────────────────────────
    # 1. RISK CHECK (NEW)
    # ─────────────────────────────
    ok, msg = validate_trade(payload.symbol, payload.lot)
    if not ok:
        return {
            "status": "rejected",
            "message": msg
        }

    # ─────────────────────────────
    # 2. SYMBOL VALIDATION (HARDENED)
    # ─────────────────────────────
    if not mt5.symbol_select(payload.symbol, True):
        return {
            "status": "error",
            "message": "Symbol not available for trading"
        }

    tick = mt5.symbol_info_tick(payload.symbol)
    if tick is None:
        return {"status": "error", "message": "No tick data"}

    price = tick.ask if payload.order_type == "BUY" else tick.bid

    # ─────────────────────────────
    # 3. ORDER REQUEST (HARDENED)
    # ─────────────────────────────
    request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": payload.symbol,
    "volume": payload.lot,
    "type": mt5.ORDER_TYPE_BUY if payload.order_type == "BUY" else mt5.ORDER_TYPE_SELL,
    "price": price,
    "deviation": 20,
    "magic": 123456,
    "comment": "api_trade",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": get_filling_mode(mt5, payload.symbol),
    }

    result = mt5.order_send(request)

    if result.retcode == 10030:  # invalid filling mode
        request["type_filling"] = mt5.ORDER_FILLING_RETURN
        result = mt5.order_send(request)
    

    # ─────────────────────────────
    # 4. FAILURE HANDLING (IMPROVED)
    # ─────────────────────────────
    if result is None:
        return {
            "status": "error",
            "message": str(mt5.last_error())
        }

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return {
            "status": "error",
            "message": f"Trade failed: {result.retcode}",
            "raw": safe_result(result)
        }

    # ─────────────────────────────
    # 5. SUCCESS
    # ─────────────────────────────
    return {
        "status": "success",
        "data": safe_result(result)
    }



@router.post("/trade/close")
def close_trade(payload: CloseTradeRequest):
    mt5 = get_mt5()
    if mt5 is None:
        return {"status": "error", "message": "MT5 not connected"}

    positions = mt5.positions_get(ticket=payload.ticket)
    if not positions:
        return {"status": "error", "message": "Position not found"}

    pos = positions[0]
    tick = mt5.symbol_info_tick(pos.symbol)

    if tick is None:
        return {"status": "error", "message": "Price unavailable"}

    close_type = (
        mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY
    )

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
        "comment": "close_trade",
    }

    result = mt5.order_send(request)

    if result is None:
        return {"status": "error", "message": str(mt5.last_error())}

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return {
            "status": "error",
            "message": f"Close failed: {result.retcode}"
        }

    return {"status": "success"}


@router.get("/trades/open")
def open_positions():
    mt5 = get_mt5()
    if mt5 is None:
        return {"status": "error", "data": []}

    positions = mt5.positions_get()
    if not positions:
        return {"status": "success", "data": []}

    return {
        "status": "success",
        "data": [
            {
                "ticket": p.ticket,
                "symbol": p.symbol,
                "volume": p.volume,
                "type": "BUY" if p.type == 0 else "SELL",
                "profit": p.profit,
            }
            for p in positions
        ],
    }