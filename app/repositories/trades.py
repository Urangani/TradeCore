from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.trade import Trade


@dataclass(frozen=True)
class TradeCreate:
    ticket: int
    symbol: str
    side: str
    volume: float
    open_price: Optional[float] = None
    strategy_id: Optional[str] = None


class TradeRepository:
    def __init__(self, db: Session):
        self._db = db

    def create_open(self, data: TradeCreate) -> Trade:
        trade = Trade(
            ticket=data.ticket,
            symbol=data.symbol,
            side=data.side,
            volume=data.volume,
            open_price=data.open_price,
            status="OPEN",
            strategy_id=data.strategy_id,
        )
        self._db.add(trade)
        self._db.commit()
        self._db.refresh(trade)
        return trade

    def mark_closed(self, *, ticket: int, close_price: float, profit: float) -> int:
        stmt = select(Trade).where(Trade.ticket == ticket).order_by(desc(Trade.created_at))
        trade = self._db.execute(stmt).scalars().first()
        if trade is None:
            return 0
        trade.close_price = close_price
        trade.profit = profit
        trade.status = "CLOSED"
        self._db.commit()
        return 1

    def list_recent(self, limit: int = 500) -> List[Trade]:
        stmt = select(Trade).order_by(desc(Trade.created_at)).limit(limit)
        return list(self._db.execute(stmt).scalars().all())

