from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from app.core import config
from app.services.mt5_service import get_mt5
from app.services.state import state
from app.services.connection_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/market")
async def market(ws: WebSocket):
    await manager.connect(ws)
    print("[WS] client connected")

    symbol = config.STREAM_SYMBOL

    try:
        while True:
            mt5 = get_mt5()
            if mt5 is None:
                # Broadcast a degraded status so the UI badge can reflect it,
                # then retry — do NOT break, which would close the socket.
                await manager.broadcast({"type": "status", "data": {"mt5_connected": False}})
                await asyncio.sleep(2)
                continue

            # Broadcast recovery once MT5 is back
            await manager.broadcast({"type": "status", "data": {"mt5_connected": True}})

            mt5.symbol_select(symbol, True)

            tick = mt5.symbol_info_tick(symbol)
            if tick:
                price = {"symbol": symbol, "bid": tick.bid, "ask": tick.ask}
                if state["price"] != price:
                    state["price"] = price
                    await manager.broadcast({"type": "price", "data": price})

            account = mt5.account_info()
            if account:
                acc = {
                    "balance": account.balance,
                    "equity": account.equity,
                    "profit": account.profit,
                    "margin": getattr(account, "margin", 0),
                    "margin_free": getattr(account, "margin_free", 0),
                    "margin_level": getattr(account, "margin_level", 0),
                }
                if state["account"] != acc:
                    state["account"] = acc
                    await manager.broadcast({"type": "account", "data": acc})

            raw_positions = mt5.positions_get() or []
            positions = [
                {
                    "ticket": p.ticket,
                    "symbol": p.symbol,
                    "type": "BUY" if p.type == 0 else "SELL",
                    "volume": p.volume,
                    "profit": p.profit,
                    "open_price": getattr(p, "price_open", None),
                    "current_price": getattr(p, "price_current", None),
                    "sl": getattr(p, "sl", None),
                    "tp": getattr(p, "tp", None),
                }
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

