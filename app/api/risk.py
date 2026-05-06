from fastapi import APIRouter

from app.core.config import config

router = APIRouter()


@router.get("/risk/limits")
def risk_limits():
    return {
        "status": "success",
        "data": {
            "max_lot": config.RISK_MAX_LOT,
            "max_open_trades": config.RISK_MAX_OPEN_TRADES,
            "max_daily_loss": config.RISK_MAX_DAILY_LOSS,
            "allowed_symbols": config.RISK_ALLOWED_SYMBOLS,
        },
    }

