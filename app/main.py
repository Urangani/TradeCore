from fastapi import FastAPI
from app.api import trade, signal, health

app = FastAPI()

app.include_router(trade.router)
app.include_router(signal.router)
app.include_router(health.router)
