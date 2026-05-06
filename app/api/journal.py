from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.trade_logger import get_trades
from app.api.dependencies import get_db

router = APIRouter()

@router.get("/journal/trades")
def journal(db: Session = Depends(get_db)):
    trades = get_trades(db)

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