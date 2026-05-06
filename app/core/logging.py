import logging
import os
from logging.config import dictConfig


def _resolve_level() -> str:
    return os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "filename": "logs/app.log",
                    "formatter": "default",
                },
            },
            "root": {
                "level": _resolve_level(),
                "handlers": ["console", "file"],
            },
        }
    )


setup_logging()
logger = logging.getLogger("tradecore")
