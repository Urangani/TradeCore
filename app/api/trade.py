from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.trade_repository import TradeRepository
from app.schemas.trade import TradeEvent

router = APIRouter()


@router.get("/trades")
async def get_trades(db: Session = Depends(get_db)):
    repo = TradeRepository(db)
    return repo.list()


@router.post("/trades")
async def create_trade(event: TradeEvent, db: Session = Depends(get_db)):
    repo = TradeRepository(db)
    return repo.create_from_event(event)
