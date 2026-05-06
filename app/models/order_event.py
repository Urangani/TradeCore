import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.sql import func

from app.db.base import Base


class OrderEvent(Base):
    __tablename__ = "order_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # MT5 order ticket / internal ticket identifier
    ticket = Column(String, index=True, nullable=False)

    # created/sent/accepted/partially_filled/filled/modified/rejected/cancelled
    event_type = Column(String, index=True, nullable=False)

    payload = Column(JSON, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

