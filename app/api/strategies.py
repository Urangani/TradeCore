from fastapi import APIRouter

from app.services.strategy_registry import list_strategies, toggle_strategy

router = APIRouter()


@router.get("/strategies")
def strategies():
    return {
        "status": "success",
        "data": [
            {"id": s.id, "name": s.name, "enabled": s.enabled}
            for s in list_strategies()
        ],
    }


@router.post("/strategies/{strategy_id}/toggle")
def toggle(strategy_id: str):
    s = toggle_strategy(strategy_id)
    if s is None:
        return {"status": "error", "message": "Unknown strategy"}
    return {"status": "success", "data": {"id": s.id, "name": s.name, "enabled": s.enabled}}

