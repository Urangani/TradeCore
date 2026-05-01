from fastapi import APIRouter, WebSocket
import asyncio
from services.mt5_service import get_mt5
from services.state import state

router = APIRouter()

@router.websocket("/ws/market")
async def market(ws: WebSocket):
    await ws.accept()
    print("[WS] connected")

    symbol = "EURUSD"

    while True:
        try:
            mt5 = get_mt5()

            if mt5 is None:
                await ws.send_json({"type": "error", "message": "MT5 not connected"})
                await asyncio.sleep(2)
                continue

            mt5.symbol_select(symbol, True)

            tick = mt5.symbol_info_tick(symbol)
            account = mt5.account_info()
            positions = mt5.positions_get()

            # ───── PRICE (only if changed) ─────
            if tick:
                new_price = {
                    "symbol": symbol,
                    "bid": tick.bid,
                    "ask": tick.ask,
                }

                if state["price"] != new_price:
                    state["price"] = new_price
                    await ws.send_json({
                        "type": "price",
                        "data": new_price
                    })

            # ───── ACCOUNT (only if changed) ─────
            if account:
                new_account = {
                    "balance": account.balance,
                    "equity": account.equity,
                    "profit": account.profit,
                }

                if state["account"] != new_account:
                    state["account"] = new_account
                    await ws.send_json({
                        "type": "account",
                        "data": new_account
                    })

            # ───── POSITIONS (only if changed) ─────
            if positions:
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

                if state["positions"] != new_positions:
                    state["positions"] = new_positions
                    await ws.send_json({
                        "type": "positions",
                        "data": new_positions
                    })

        except Exception as e:
            await ws.send_json({
                "type": "error",
                "message": str(e)
            })

        await asyncio.sleep(0.5)  # faster loop but smarter output