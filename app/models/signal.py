import enum
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class SignalDirection(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"
    EXIT = "EXIT"


class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False, index=True)
    source = Column(String, nullable=False)
    symbol = Column(String, nullable=False, index=True)
    signal = Column(Enum(SignalDirection), nullable=False)
    confidence = Column(Float)
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    strategy = relationship("Strategy", back_populates="signals")
    trades = relationship("Trade", back_populates="signal")
