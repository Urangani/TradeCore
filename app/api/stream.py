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

            mt5 = get_mt5()

            if mt5 is None:
                break

            mt5.symbol_select(symbol, True)

            # PRICE
            tick = mt5.symbol_info_tick(symbol)

            if tick:
                price = {
                    "symbol": symbol,
                    "bid": tick.bid,
                    "ask": tick.ask,
                }

                if state["price"] != price:
                    state["price"] = price
                    await ws.send_json({
                        "type": "price",
                        "data": price
                    })

            # ACCOUNT
            account = mt5.account_info()

            if account:
                acc = {
                    "balance": account.balance,
                    "equity": account.equity,
                    "profit": account.profit,
                }

                if state["account"] != acc:
                    state["account"] = acc
                    await ws.send_json({
                        "type": "account",
                        "data": acc
                    })

            # POSITIONS
            raw_positions = mt5.positions_get() or []

            positions = [
                {
                    "ticket": p.ticket,
                    "symbol": p.symbol,
                    "type": "BUY" if p.type == 0 else "SELL",
                    "volume": p.volume,
                    "profit": p.profit,
                }
                for p in raw_positions
            ]

            if state["positions"] != positions:
                state["positions"] = positions
                await ws.send_json({
                    "type": "positions",
                    "data": positions
                })

            await asyncio.sleep(0.5)

    except WebSocketDisconnect:
        print("[WS] client disconnected")

    except Exception as e:
        print("[WS ERROR]", e)

    finally:
        print("[WS] closed cleanly")