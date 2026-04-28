import os

API_KEY = os.getenv("API_KEY", "dev_key")
DB_URL = os.getenv("DB_URL", "sqlite:///./trading.db")
