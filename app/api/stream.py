from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from services.mt5_service import get_mt5, open_trade, close_trade
from services.state import state

router = APIRouter()

@router.websocket("/ws/market")
async def market(ws: WebSocket):
    await ws.accept()
    print("[WS] connected")

    symbol = "EURUSD"

    try:
        while True:
            # --- Receive commands from client ---
            try:
                msg = await ws.receive_json()
                if msg["type"] == "trade":
                    action = msg["action"]
                    if action in ["BUY", "SELL"]:
                        result = open_trade(msg["symbol"], msg["lot"], action)
                        await ws.send_json({"type": "trade_result", "data": result})
                    elif action == "CLOSE":
                        result = close_trade(msg["ticket"])
                        await ws.send_json({"type": "trade_result", "data": result})
            except Exception:
                # ignore if no message received this cycle
                pass

            # --- Stream market/account/positions as before ---
            mt5 = get_mt5()
            if mt5 is None:
                break

            mt5.symbol_select(symbol, True)

            tick = mt5.symbol_info_tick(symbol)
            if tick:
                price = {"symbol": symbol, "bid": tick.bid, "ask": tick.ask}
                if state["price"] != price:
                    state["price"] = price
                    await ws.send_json({"type": "price", "data": price})

            account = mt5.account_info()
            if account:
                acc = {"balance": account.balance, "equity": account.equity, "profit": account.profit}
                if state["account"] != acc:
                    state["account"] = acc
                    await ws.send_json({"type": "account", "data": acc})

            raw_positions = mt5.positions_get() or []
            positions = [
                {"ticket": p.ticket, "symbol": p.symbol, "type": "BUY" if p.type == 0 else "SELL",
                 "volume": p.volume, "profit": p.profit}
                for p in raw_positions
            ]
            if state["positions"] != positions:
                state["positions"] = positions
                await ws.send_json({"type": "positions", "data": positions})

            await asyncio.sleep(0.5)

    except WebSocketDisconnect:
        print("[WS] client disconnected")
    finally:
        print("[WS] closed cleanly")
