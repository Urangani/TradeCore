from sqlalchemy.orm import Session

from app.models.trade import Trade
from app.repositories.base import Repository
from app.schemas.trade import TradeEvent


class TradeRepository(Repository[Trade]):
    def __init__(self, db: Session):
        super().__init__(Trade, db)

    def create_from_event(self, event: TradeEvent) -> Trade:
        trade = Trade(
            strategy_id=event.strategy_id,
            symbol=event.symbol,
            action=event.action,
            type=event.type,
            price=event.price,
            volume=event.volume,
            timestamp=event.timestamp,
        )
        return self.create(trade)
