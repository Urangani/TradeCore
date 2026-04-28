from fastapi import APIRouter

router = APIRouter()

@router.get("/signals")
async def get_signals():
    return {"message": "List of signals"}
