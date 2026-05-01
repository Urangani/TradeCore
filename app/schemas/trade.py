from pydantic import BaseModel
from datetime import datetime

class TradeEvent(BaseModel):
    strategy_id: int
    symbol: str
    action: str
    type: str
    price: float
    volume: float
    timestamp: datetime
