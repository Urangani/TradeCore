from pydantic import BaseModel, Field
from typing import Literal


class OpenTradeRequest(BaseModel):
    symbol: str
    lot: float = Field(gt=0)
    order_type: Literal["BUY", "SELL"]


class CloseTradeRequest(BaseModel):
    ticket: int


class TradeResponse(BaseModel):
    status: str
    message: str | None = None
    data: dict | None = None