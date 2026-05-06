from fastapi import APIRouter
from fastapi.params import Depends

from app.core.logging import logger
from app.schemas.trade import OpenTradeRequest, CloseTradeRequest
from app.services.dependencies import get_mt5_client
from app.services.risk_engine import validate_trade
from app.services.trade_logger import log_trade_open, update_trade_close, get_trades
router = APIRouter()

def get_filling_mode(mt5, symbol):
    info = mt5.symbol_info(symbol)

    if info is None:
        return mt5.ORDER_FILLING_RETURN  # safest fallback

    # MT5 returns bitmask-like values depending on broker
    filling = info.filling_mode

    if filling == 1:
        return mt5.ORDER_FILLING_FOK
    elif filling == 2:
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
def open_trade(payload: OpenTradeRequest, mt5=Depends(get_mt5_client)):
    logger.info("Open trade request: symbol=%s lot=%s side=%s", payload.symbol, payload.lot, payload.order_type)
    if mt5 is None:
        return {"status": "error", "message": "MT5 not connected"}

    ok, msg = validate_trade(payload.symbol, payload.lot, mt5=mt5)
    if not ok:
        return {"status": "rejected", "message": msg}

    if not mt5.symbol_select(payload.symbol, True):
        return {"status": "error", "message": "Symbol not available"}

    tick = mt5.symbol_info_tick(payload.symbol)
    if tick is None:
        return {"status": "error", "message": "No tick data"}

    price = tick.ask if payload.order_type == "BUY" else tick.bid


    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": payload.symbol,
        "volume": float(payload.lot),
        "type": mt5.ORDER_TYPE_BUY if payload.order_type == "BUY" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": 20,
        "magic": 123456,
        "comment": "api_trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": get_filling_mode(mt5,payload.symbol),
    }

    result = mt5.order_send(request)

    if result is None:
        return {"status": "error", "message": str(mt5.last_error())}

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logger.warning("Open trade failed: retcode=%s", result.retcode)
        return {
            "status": "error",
            "message": f"Trade failed: {result.retcode}",
        }

    log_trade_open(
        ticket=result.order,
        symbol=payload.symbol,
        type_=payload.order_type,
        volume=payload.lot,
        price=price,
    )

    return {
        "status": "success",
        "data": {
            "ticket": result.order,
            "price": price,
            "retcode": result.retcode,
        },
    }


@router.post("/trade/close")
def close_trade(payload: CloseTradeRequest, mt5=Depends(get_mt5_client)):
    logger.info("Close trade request: ticket=%s", payload.ticket)
    if mt5 is None:
        return {"status": "error", "message": "MT5 not connected"}

    positions = mt5.positions_get(ticket=payload.ticket)
    if not positions:
        return {"status": "error", "message": "Position not found"}

    pos = positions[0]

    tick = mt5.symbol_info_tick(pos.symbol)
    if tick is None:
        return {"status": "error", "message": "Price unavailable"}

    price = tick.bid if pos.type == 0 else tick.ask

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": pos.symbol,
        "volume": float(pos.volume),
        "type": mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY,
        "position": pos.ticket,
        "price": price,
        "deviation": 20,
        "magic": 123456,
        "comment": "close_trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": get_filling_mode(mt5, pos.symbol), 
    }

    result = mt5.order_send(request)

    if result is None:
        return {"status": "error", "message": str(mt5.last_error())}

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logger.warning("Close trade failed: retcode=%s ticket=%s", result.retcode, payload.ticket)
        return {
            "status": "error",
            "message": f"Close failed: {result.retcode}",
        }

    # FIXED HISTORY QUERY
    deals = mt5.history_deals_get(position=pos.ticket)

    profit = sum(d.profit for d in deals) if deals else 0.0

    update_trade_close(
        ticket=payload.ticket,
        close_price=price,
        profit=profit,
    )

    return {
        "status": "success",
        "data": {
            "ticket": payload.ticket,
            "symbol": pos.symbol,
            "close_price": price,
            "profit": profit,
        },
    }

@router.get("/trades/open")
def open_positions(mt5=Depends(get_mt5_client)):
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


@router.get("/trades/history")
def trade_history():
    try:
        trades = get_trades()
        return {
            "status": "success",
            "data": [
                {
                    "id": t.id,
                    "ticket": t.ticket,
                    "symbol": t.symbol,
                    "type": t.side,
                    "volume": t.volume,
                    "open_price": t.open_price,
                    "close_price": t.close_price,
                    "profit": t.profit,
                    "status": t.status,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                }
                for t in trades
            ],
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
