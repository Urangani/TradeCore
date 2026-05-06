from typing import Generator
from fastapi import Depends
from app.db.session import SessionLocal
from app.core.config import config
from app.services.dependencies import get_mt5_client
from app.services.risk_engine import RiskPolicy

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_risk_policy(mt5=Depends(get_mt5_client)) -> RiskPolicy:
    return RiskPolicy(config=config, mt5=mt5)
