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
                await ws.send_json({"error": "MT5 not connected"})
                await asyncio.sleep(2)
                continue

            # ⚠️ DO NOT assume symbol_select always works
            try:
                mt5.symbol_select(symbol, True)
            except Exception as e:
                await ws.send_json({"error": f"symbol_select failed: {str(e)}"})
                await asyncio.sleep(2)
                continue

            tick = mt5.symbol_info_tick(symbol)

            if tick is None:
                await ws.send_json({"error": "No tick data"})
            else:
                await ws.send_json({
                    "symbol": symbol,
                    "bid": tick.bid,
                    "ask": tick.ask,
                })

        except Exception as e:
            # 🔥 THIS prevents silent crash = your issue
            print("[WS ERROR]", e)
            await ws.send_json({"error": str(e)})

        await asyncio.sleep(1)