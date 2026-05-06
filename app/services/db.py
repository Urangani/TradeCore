def init_db():
    # Initialize (or upgrade) the database schema via SQLAlchemy.
    # NOTE: For a serious production platform, Alembic migrations should replace create_all.
    from app.db.session import engine
    from app.db.base import Base

    # Import models so they're registered on Base.metadata
    from app.models.trade import Trade  # noqa: F401
    from app.models.signal import Signal  # noqa: F401
    from app.models.order_event import OrderEvent  # noqa: F401
    from app.models.position import Position  # noqa: F401
    from app.models.market_data import Tick, Candle  # noqa: F401
    from app.models.research import MarketDataset, BacktestRun, PerformanceSnapshot  # noqa: F401
    from app.models.strategy_telemetry import (  # noqa: F401
        Feature,
        StrategyDecision,
        RiskEvent,
        MarketContext,
    )

    Base.metadata.create_all(bind=engine)