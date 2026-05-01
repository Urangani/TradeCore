from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.signal_repository import SignalRepository
from app.schemas.signal import SignalEvent

router = APIRouter()


@router.get("/signals")
async def get_signals(db: Session = Depends(get_db)):
    repo = SignalRepository(db)
    return repo.list()


@router.post("/signals")
async def create_signal(event: SignalEvent, db: Session = Depends(get_db)):
    repo = SignalRepository(db)
    return repo.create_from_event(event)
