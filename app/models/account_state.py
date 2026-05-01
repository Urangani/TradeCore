from sqlalchemy import Column, DateTime, Float, Integer
from sqlalchemy.sql import func

from app.db.base import Base


class AccountState(Base):
    __tablename__ = "account_state"

    id = Column(Integer, primary_key=True)
    balance = Column(Float, nullable=False)
    equity = Column(Float, nullable=False)
    margin = Column(Float, nullable=False)
    free_margin = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
