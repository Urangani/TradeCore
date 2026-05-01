from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from services.mt5_service import get_mt5
from services.state import state

router = APIRouter()

@router.websocket("/ws/market")
async def market(ws: WebSocket):
    await ws.accept()
    print("[WS] connected")

    symbol = "EURUSD"

    try:
        while True:

            # ─────────────────────────────
            # 1. CONNECTION GUARD
            # ─────────────────────────────
            if ws.client_state.name != "CONNECTED":
                break

            mt5 = get_mt5()

            if mt5 is None:
                await ws.send_json({
                    "type": "error",
                    "message": "MT5 not connected"
                })
                await asyncio.sleep(2)
                continue

            # ─────────────────────────────
            # 2. SYMBOL
            # ─────────────────────────────
            mt5.symbol_select(symbol, True)
            tick = mt5.symbol_info_tick(symbol)

            # ─────────────────────────────
            # 3. PRICE STREAM
            # ─────────────────────────────
            if tick:
                new_price = {
                    "symbol": symbol,
                    "bid": tick.bid,
                    "ask": tick.ask,
                }

                if state.get("price") != new_price:
                    state["price"] = new_price

                    await ws.send_json({
                        "type": "price",
                        "data": new_price
                    })

            # ─────────────────────────────
            # 4. ACCOUNT STREAM
            # ─────────────────────────────
            account = mt5.account_info()

            if account:
                new_account = {
                    "balance": account.balance,
                    "equity": account.equity,
                    "profit": account.profit,
                }

                if state.get("account") != new_account:
                    state["account"] = new_account

                    await ws.send_json({
                        "type": "account",
                        "data": new_account
                    })

            # ─────────────────────────────
            # 5. POSITIONS STREAM
            # ─────────────────────────────
            positions = mt5.positions_get() or []

            new_positions = [
                {
                    "ticket": p.ticket,
                    "symbol": p.symbol,
                    "type": "BUY" if p.type == 0 else "SELL",
                    "volume": p.volume,
                    "profit": p.profit,
                }
                for p in positions
            ]

            if state.get("positions") != new_positions:
                state["positions"] = new_positions

                await ws.send_json({
                    "type": "positions",
                    "data": new_positions
                })

            await asyncio.sleep(0.5)

    except WebSocketDisconnect:
        print("[WS] client disconnected")

    except Exception as e:
        print("[WS ERROR]", e)

    finally:
        print("[WS] closed cleanly")