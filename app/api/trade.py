from fastapi import APIRouter

router = APIRouter()

@router.get("/trades")
async def get_trades():
    return {"message": "List of trades"}
