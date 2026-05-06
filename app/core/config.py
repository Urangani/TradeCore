import os

API_KEY = os.getenv("API_KEY", "dev_key")
DB_URL = os.getenv("DB_URL", "sqlite:///./trading.db")

# Risk policy (kept simple and env-driven for now)
RISK_MAX_LOT = float(os.getenv("RISK_MAX_LOT", "0.5"))
RISK_MAX_OPEN_TRADES = int(os.getenv("RISK_MAX_OPEN_TRADES", "5"))
RISK_MAX_DAILY_LOSS = float(os.getenv("RISK_MAX_DAILY_LOSS", "-50"))
RISK_ALLOWED_SYMBOLS = [
    s.strip()
    for s in os.getenv("RISK_ALLOWED_SYMBOLS", "EURUSD,GBPUSD,USDJPY").split(",")
    if s.strip()
]

# Streaming / market data
STREAM_SYMBOL = os.getenv("STREAM_SYMBOL", "EURUSD")
STREAM_POLL_SECONDS = float(os.getenv("STREAM_POLL_SECONDS", "0.5"))
