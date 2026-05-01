from fastapi import APIRouter
from services.trade_logger import get_trades

router = APIRouter()

@router.get("/journal/trades")
def journal():
    rows = get_trades()

    return {
        "status": "success",
        "data": [
            {
                "id": r[0],
                "ticket": r[1],
                "symbol": r[2],
                "type": r[3],
                "volume": r[4],
                "open_price": r[5],
                "close_price": r[6],
                "profit": r[7],
                "status": r[8],
                "created_at": r[9],
            }
            for r in rows
        ]
    }