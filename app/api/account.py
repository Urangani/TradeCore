from fastapi import APIRouter
from services.mt5_service import get_mt5

router = APIRouter()

@router.get("/account/summary")
def account_summary():
    mt5 = get_mt5()
    if mt5 is None:
        return {"status": "error", "message": "MT5 not connected"}

    info = mt5.account_info()
    if info is None:
        return {"status": "error", "message": "Failed to fetch account"}

    return {
        "status": "success",
        "data": {
            "balance": info.balance,
            "equity": info.equity,
            "profit": info.profit,
        },
    }