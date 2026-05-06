from fastapi import APIRouter
from app.services.mt5_service import get_mt5

router = APIRouter()

def get_account_info(mt5):
    info = mt5.account_info()
    if info is None:
        return None

    return {
        "name": getattr(info, "name", None),
        "login": getattr(info, "login", None),
        "balance": info.balance,
        "equity": info.equity,
        "profit": info.profit,
        "margin": info.margin,
        "currency": getattr(info, "currency", None),
        "leverage": getattr(info, "leverage", None),
    }

@router.get("/account/summary")
def account_summary():
    mt5 = get_mt5()

    if mt5 is None:
        return {"status": "error", "message": "MT5 not connected"}

    info = get_account_info(mt5)

    if info is None:
        return {"status": "error", "message": "Failed to fetch account"}

    return {
        "status": "success",
        "data": info
    }