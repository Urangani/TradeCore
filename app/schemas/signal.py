from pydantic import BaseModel
from datetime import datetime
from app.models.signal import SignalDirection

class SignalEvent(BaseModel):
    strategy_id: int
    source: str
    symbol: str
    signal: SignalDirection
    confidence: float | None = None
    timestamp: datetime
