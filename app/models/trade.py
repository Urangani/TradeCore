import uuid

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.db.base import Base


class Trade(Base):
    __tablename__ = "trades"

    # Canonical, persisted record used by the journal and history endpoints.
    # Note: keep columns aligned with API payloads (ticket/open/close/profit/status/timestamps).
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    ticket = Column(Integer, index=True, nullable=False)
    symbol = Column(String, index=True, nullable=False)
    side = Column(String, nullable=False)  # BUY / SELL
    volume = Column(Float, nullable=False)

    open_price = Column(Float, nullable=True)
    close_price = Column(Float, nullable=True)
    profit = Column(Float, nullable=True)

    status = Column(String, nullable=False, default="OPEN")  # OPEN / CLOSED

    # Future-facing fields (used by attribution / analytics later)
    strategy_id = Column(String, index=True, nullable=True)

    opened_at = Column(DateTime(timezone=True), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
