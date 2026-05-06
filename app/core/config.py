import os
from typing import List

class Settings:
    API_KEY: str = os.getenv("API_KEY", "dev_key")
    DB_URL: str = os.getenv("DB_URL", "sqlite:///./trading.db")

    # Risk policy
    RISK_MAX_LOT: float = float(os.getenv("RISK_MAX_LOT", "0.5"))
    RISK_MAX_OPEN_TRADES: int = int(os.getenv("RISK_MAX_OPEN_TRADES", "5"))
    RISK_MAX_DAILY_LOSS: float = float(os.getenv("RISK_MAX_DAILY_LOSS", "-50"))
    
    @property
    def RISK_ALLOWED_SYMBOLS(self) -> List[str]:
        return [
            s.strip()
            for s in os.getenv("RISK_ALLOWED_SYMBOLS", "EURUSD,GBPUSD,USDJPY").split(",")
            if s.strip()
        ]

    # Streaming / market data
    STREAM_SYMBOL: str = os.getenv("STREAM_SYMBOL", "EURUSD")
    STREAM_POLL_SECONDS: float = float(os.getenv("STREAM_POLL_SECONDS", "0.5"))

config = Settings()
