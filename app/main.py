from fastapi import FastAPI
from app.api import account, trades, logs, stream, journal, health, risk, strategies, review
from app.services.mt5_service import init, shutdown
from fastapi.middleware.cors import CORSMiddleware
from app.services.db import init_db
from app.core.logging import logger


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    logger.info("TradeCore startup: initializing services")
    init()
    init_db()
    logger.info("TradeCore startup complete")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("TradeCore shutdown: closing services")
    shutdown()
    logger.info("TradeCore shutdown complete")

app.include_router(account.router)
app.include_router(trades.router)
app.include_router(logs.router)
app.include_router(stream.router)  
app.include_router(journal.router)
app.include_router(health.router)
app.include_router(risk.router)
app.include_router(strategies.router)
app.include_router(review.router)


