from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    strategy_id = Column(String)
    symbol = Column(String)
    action = Column(String)
    type = Column(String)
    price = Column(Float)
    volume = Column(Float)
    timestamp = Column(String)
