from datetime import datetime, timedelta, timezone

from fastapi import APIRouter
from sqlalchemy import func, select

from app.db.session import SessionLocal
from app.models.trade import Trade

router = APIRouter()


@router.get("/review/summary")
def review_summary(days: int = 7):
    since = datetime.now(timezone.utc) - timedelta(days=days)

    db = SessionLocal()
    try:
        # SQLite stores timezone-naive; using created_at >= since is still useful for relative windows.
        total_stmt = select(func.count()).select_from(Trade).where(Trade.created_at >= since)
        total = db.execute(total_stmt).scalar_one()

        pnl_stmt = select(func.coalesce(func.sum(Trade.profit), 0.0)).where(Trade.created_at >= since)
        net_pnl = float(db.execute(pnl_stmt).scalar_one())

        wins_stmt = select(func.count()).select_from(Trade).where(
            Trade.created_at >= since,
            Trade.profit.is_not(None),
            Trade.profit > 0,
        )
        wins = db.execute(wins_stmt).scalar_one()

        win_rate = float(wins) / float(total) * 100.0 if total else 0.0

        return {
            "status": "success",
            "data": {
                "window_days": days,
                "trades": int(total),
                "win_rate": win_rate,
                "net_pnl": net_pnl,
            },
        }
    finally:
        db.close()

