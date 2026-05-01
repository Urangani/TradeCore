from fastapi import APIRouter
from services.mt5_service import get_open_positions

router = APIRouter()

@router.get("/trades/open")
def open_trades():
    return get_open_positions()