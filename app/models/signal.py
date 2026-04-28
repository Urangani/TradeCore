from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True)
    strategy_id = Column(String)
    source = Column(String)
    symbol = Column(String)
    signal = Column(String)
    confidence = Column(Float)
    timestamp = Column(String)
