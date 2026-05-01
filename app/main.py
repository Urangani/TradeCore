from fastapi import FastAPI
from api import account, trades, logs
from services.mt5_service import init, shutdown
from fastapi.middleware.cors import CORSMiddleware

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
    init()

@app.on_event("shutdown")
def shutdown_event():
    shutdown()

app.include_router(account.router)
app.include_router(trades.router)
app.include_router(logs.router)


