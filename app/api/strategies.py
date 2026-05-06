from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional

from app.core.logging import logger
from app.services.strategy_registry import (
    list_strategies,
    get_strategy,
    toggle_strategy,
    create_strategy,
    delete_strategy,
)

router = APIRouter()


class StrategyCreateRequest(BaseModel):
    id: str
    name: str
    description: str = ""
    params: Optional[Dict[str, Any]] = None


def _serialize(s):
    return {
        "id": s.id,
        "name": s.name,
        "enabled": s.enabled,
        "description": s.description,
        "params": s.params,
    }


@router.get("/strategies")
def strategies():
    return {
        "status": "success",
        "data": [_serialize(s) for s in list_strategies()],
    }


@router.get("/strategies/{strategy_id}")
def get_one(strategy_id: str):
    s = get_strategy(strategy_id)
    if s is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return {"status": "success", "data": _serialize(s)}


@router.post("/strategies")
def create(payload: StrategyCreateRequest):
    s = create_strategy(
        id=payload.id,
        name=payload.name,
        description=payload.description,
        params=payload.params,
    )
    if s is None:
        raise HTTPException(status_code=409, detail=f"Strategy '{payload.id}' already exists")
    logger.info("Strategy created: %s", payload.id)
    return {"status": "success", "data": _serialize(s)}


@router.post("/strategies/{strategy_id}/toggle")
def toggle(strategy_id: str):
    s = toggle_strategy(strategy_id)
    if s is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    logger.info("Strategy toggled: %s → enabled=%s", strategy_id, s.enabled)
    return {"status": "success", "data": _serialize(s)}


@router.post("/strategies/{strategy_id}/run")
def run_strategy(strategy_id: str):
    s = get_strategy(strategy_id)
    if s is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if not s.enabled:
        return {"status": "error", "message": f"Strategy '{s.name}' is disabled. Enable it first."}
    # In production this would import and invoke the actual strategy module.
    logger.info("Strategy manual run triggered: %s", strategy_id)
    return {
        "status": "success",
        "message": f"Strategy '{s.name}' run triggered.",
        "data": _serialize(s),
    }


@router.delete("/strategies/{strategy_id}")
def delete(strategy_id: str):
    ok = delete_strategy(strategy_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Strategy not found")
    logger.info("Strategy deleted: %s", strategy_id)
    return {"status": "success", "message": f"Strategy '{strategy_id}' deleted."}

