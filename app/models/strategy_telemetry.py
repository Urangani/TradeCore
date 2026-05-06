import uuid

from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.sql import func

from app.db.base import Base


class Feature(Base):
    __tablename__ = "features"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    symbol = Column(String, index=True, nullable=False)
    timeframe = Column(String, index=True, nullable=True)
    feature_name = Column(String, index=True, nullable=False)
    feature_value = Column(Float, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class StrategyDecision(Base):
    __tablename__ = "strategy_decisions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    strategy_id = Column(String, index=True, nullable=False)
    market_context = Column(JSON, nullable=True)
    decision = Column(String, nullable=False)
    confidence = Column(Float, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class RiskEvent(Base):
    __tablename__ = "risk_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    strategy_id = Column(String, index=True, nullable=True)
    event_type = Column(String, index=True, nullable=False)
    reason = Column(String, nullable=True)
    payload = Column(JSON, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class MarketContext(Base):
    __tablename__ = "market_context"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    symbol = Column(String, index=True, nullable=False)
    session = Column(String, index=True, nullable=True)
    spread = Column(Float, nullable=True)
    volatility = Column(Float, nullable=True)
    news_event = Column(String, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

