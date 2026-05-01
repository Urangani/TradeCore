import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    OPEN = "OPEN"
    CANCELLED = "CANCELLED"


class Order(Base):
    __tablename__ = "orders"

    ticket = Column(Integer, primary_key=True)
    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=False, index=True)
    symbol = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)
    volume = Column(Float, nullable=False)
    open_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    signal = relationship("Signal")
