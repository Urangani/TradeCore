from pydantic import BaseModel
from datetime import datetime

class SignalEvent(BaseModel):
    strategy_id: str
    source: str
    symbol: str
    signal: str
    confidence: float | None = None
    timestamp: datetime
