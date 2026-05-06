from fastapi import APIRouter

router = APIRouter()

@router.get("/logs")
def logs():
    # Lightweight endpoint for the dashboard. In production, this should be backed by an append-only
    # event store (order_events, risk_events, strategy_decisions) with pagination.
    return {
        "status": "success",
        "data": [
            {"time": "12:01", "event": "Order placed"},
            {"time": "12:05", "event": "SL hit"},
        ],
    }