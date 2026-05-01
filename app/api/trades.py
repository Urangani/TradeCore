from fastapi import APIRouter
from schemas.trade import OpenTradeRequest, CloseTradeRequest
from services.mt5_service import get_mt5

router = APIRouter()


@router.post("/trade/open")
def open_trade(payload: OpenTradeRequest):
    mt5 = get_mt5()
    if mt5 is None:
        return {"status": "error", "message": "MT5 not connected"}

    tick = mt5.symbol_info_tick(payload.symbol)
    if tick is None:
        return {"status": "error", "message": "Invalid symbol"}

    price = tick.ask if payload.order_type == "BUY" else tick.bid

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": payload.symbol,
        "volume": payload.lot,
        "type": mt5.ORDER_TYPE_BUY if payload.order_type == "BUY" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": 10,
        "magic": 123456,
        "comment": "api_trade",
    }

    result = mt5.order_send(request)

    if result is None:
        return {
            "status": "error",
            "message": str(mt5.last_error())
        }

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return {
            "status": "error",
            "message": f"Trade failed: {result.retcode}"
        }

    return {
        "status": "success",
        "data": result._asdict()
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