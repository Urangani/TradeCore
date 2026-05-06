import uuid

from sqlalchemy import Column, Date, DateTime, Float, String
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.sql import func

from app.db.base import Base


class MarketDataset(Base):
    __tablename__ = "market_datasets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    symbol = Column(String, index=True, nullable=False)
    timeframe = Column(String, index=True, nullable=False)
    source = Column(String, nullable=True)
    checksum = Column(String, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class BacktestRun(Base):
    __tablename__ = "backtests"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    strategy_id = Column(String, index=True, nullable=False)
    strategy_version = Column(String, nullable=True)
    dataset_id = Column(String, index=True, nullable=True)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    params = Column(JSON, nullable=True)

    initial_balance = Column(Float, nullable=True)
    final_balance = Column(Float, nullable=True)
    sharpe = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class PerformanceSnapshot(Base):
    __tablename__ = "performance_snapshots"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    strategy_id = Column(String, index=True, nullable=True)

    pnl = Column(Float, nullable=True)
    win_rate = Column(Float, nullable=True)
    drawdown = Column(Float, nullable=True)
    sharpe = Column(Float, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

