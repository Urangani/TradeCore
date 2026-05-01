from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.db.base import Base


class Tick(Base):
    __tablename__ = "ticks"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False, index=True)
    bid = Column(Float, nullable=False)
    ask = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
