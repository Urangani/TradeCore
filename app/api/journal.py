from fastapi import APIRouter
from app.services.trade_logger import get_trades

router = APIRouter()

@router.get("/journal/trades")
def journal():
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