import uuid

from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.sql import func

from app.db.base import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    symbol = Column(String, index=True, nullable=False)
    strategy_id = Column(String, index=True, nullable=True)

    mt5_position_id = Column(String, index=True, nullable=True)

    # BUY / SELL (and later NET / HEDGE modes if needed)
    side = Column(String, nullable=False)

    volume = Column(Float, nullable=False)
    avg_entry = Column(Float, nullable=True)

    unrealized_pnl = Column(Float, nullable=True)
    realized_pnl = Column(Float, nullable=True)

    status = Column(String, index=True, nullable=False, default="OPEN")  # OPEN / CLOSED

    opened_at = Column(DateTime(timezone=True), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

