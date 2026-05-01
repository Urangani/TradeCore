from fastapi import APIRouter

router = APIRouter()

@router.get("/logs")
def logs():
    return [
        {"time": "12:01", "event": "Order placed"},
        {"time": "12:05", "event": "SL hit"},
    ]