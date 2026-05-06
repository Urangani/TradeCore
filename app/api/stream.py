from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from app.core import config
from app.services.mt5_service import get_mt5
from app.services.state import state
from app.services.connection_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()   # <-- instantiate here

@router.websocket("/ws/market")
async def market(ws: WebSocket):
    await manager.connect(ws)
    print("[WS] client connected")

    symbol = config.STREAM_SYMBOL

    try:
        while True:
            mt5 = get_mt5()
            if mt5 is None:
                break

            mt5.symbol_select(symbol, True)

            tick = mt5.symbol_info_tick(symbol)
            if tick:
                price = {"symbol": symbol, "bid": tick.bid, "ask": tick.ask}
                if state["price"] != price:
                    state["price"] = price
                    await manager.broadcast({"type": "price", "data": price})

            account = mt5.account_info()
            if account:
                acc = {"balance": account.balance, "equity": account.equity, "profit": account.profit}
                if state["account"] != acc:
                    state["account"] = acc
                    await manager.broadcast({"type": "account", "data": acc})

            raw_positions = mt5.positions_get() or []
            positions = [
                {"ticket": p.ticket, "symbol": p.symbol,
                 "type": "BUY" if p.type == 0 else "SELL",
                 "volume": p.volume, "profit": p.profit}
                for p in raw_positions
            ]
            if state["positions"] != positions:
                state["positions"] = positions
                await manager.broadcast({"type": "positions", "data": positions})

            await asyncio.sleep(config.STREAM_POLL_SECONDS)

    except WebSocketDisconnect:
        print("[WS] client disconnected")
        manager.disconnect(ws)
    finally:
        print("[WS] closed cleanly")

