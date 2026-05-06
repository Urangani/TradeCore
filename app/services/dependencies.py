from __future__ import annotations

from typing import Optional

from fastapi import Depends

from app.services.mt5_protocol import MT5Client
from app.services.mt5_service import get_mt5


def get_mt5_client() -> Optional[MT5Client]:
    # Keep current behavior (global client + reconnect), but type it as an interface.
    return get_mt5()


MT5 = Depends(get_mt5_client)

