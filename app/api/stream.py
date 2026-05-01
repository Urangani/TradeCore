from fastapi import APIRouter, WebSocket
import asyncio
from services.mt5_service import get_mt5

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
                await ws.send_json({
                    "type": "error",
                    "message": "MT5 not connected"
                })
                await asyncio.sleep(2)
                continue

            # ensure symbol
            mt5.symbol_select(symbol, True)

            tick = mt5.symbol_info_tick(symbol)
            account = mt5.account_info()
            positions = mt5.positions_get()

            # ───── PRICE ─────
            if tick:
                await ws.send_json({
                    "type": "price",
                    "data": {
                        "symbol": symbol,
                        "bid": tick.bid,
                        "ask": tick.ask,
                    }
                })

            # ───── ACCOUNT ─────
            if account:
                await ws.send_json({
                    "type": "account",
                    "data": {
                        "balance": account.balance,
                        "equity": account.equity,
                        "profit": account.profit,
                    }
                })

            # ───── POSITIONS ─────
            if positions:
                await ws.send_json({
                    "type": "positions",
                    "data": [
                        {
                            "ticket": p.ticket,
                            "symbol": p.symbol,
                            "type": "BUY" if p.type == 0 else "SELL",
                            "volume": p.volume,
                            "profit": p.profit,
                        }
                        for p in positions
                    ]
                })

        except Exception as e:
            await ws.send_json({
                "type": "error",
                "message": str(e)
            })

        await asyncio.sleep(1)