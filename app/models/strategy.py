from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)
    version = Column(String, nullable=False, default="1.0.0")
    params = Column(JSON, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    signals = relationship("Signal", back_populates="strategy")
    trades = relationship("Trade", back_populates="strategy")
