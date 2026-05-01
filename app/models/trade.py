from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False, index=True)
    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=True, index=True)
    symbol = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False)
    type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    close_price = Column(Float, nullable=True)
    profit = Column(Float, nullable=True)
    swap = Column(Float, nullable=True)
    commission = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    strategy = relationship("Strategy", back_populates="trades")
    signal = relationship("Signal", back_populates="trades")
