from sqlalchemy.orm import Session

from app.models.signal import Signal
from app.repositories.base import Repository
from app.schemas.signal import SignalEvent


class SignalRepository(Repository[Signal]):
    def __init__(self, db: Session):
        super().__init__(Signal, db)

    def create_from_event(self, event: SignalEvent) -> Signal:
        signal = Signal(
            strategy_id=event.strategy_id,
            source=event.source,
            symbol=event.symbol,
            signal=event.signal,
            confidence=event.confidence,
            timestamp=event.timestamp,
        )
        return self.create(signal)
