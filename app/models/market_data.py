import uuid

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.db.base import Base


class Tick(Base):
    __tablename__ = "ticks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    symbol = Column(String, index=True, nullable=False)
    bid = Column(Float, nullable=True)
    ask = Column(Float, nullable=True)
    spread = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    source = Column(String, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Candle(Base):
    __tablename__ = "candles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, index=True, nullable=False)
    timeframe = Column(String, index=True, nullable=False)

    open = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    close = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)

    timestamp = Column(DateTime(timezone=True), index=True, nullable=False)

