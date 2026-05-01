from fastapi import FastAPI
from api import account, trades, logs ,stream,journal
from services.mt5_service import init, shutdown
from fastapi.middleware.cors import CORSMiddleware
from services.db import init_db


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
    init_db()

@app.on_event("shutdown")
def shutdown_event():
    shutdown()

app.include_router(account.router)
app.include_router(trades.router)
app.include_router(logs.router)
app.include_router(stream.router)  
app.include_router(journal.router)


