from fastapi import APIRouter
from services.mt5_service import get_account_info

router = APIRouter()

@router.get("/account/summary")
def account_summary():
    return get_account_info()