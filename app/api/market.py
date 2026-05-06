from fastapi import APIRouter, HTTPException, Query, Depends
from app.core import config
from app.core.logging import logger
from app.services.dependencies import get_mt5_client

router = APIRouter()

_TIMEFRAME_MAP = {
    "M1": "TIMEFRAME_M1",
    "M5": "TIMEFRAME_M5",
    "M15": "TIMEFRAME_M15",
    "M30": "TIMEFRAME_M30",
    "H1": "TIMEFRAME_H1",
    "H4": "TIMEFRAME_H4",
    "D1": "TIMEFRAME_D1",
}


@router.get("/symbols")
def list_symbols(mt5=Depends(get_mt5_client)):
    """Return the list of tradeable symbols.

    Falls back to the configured RISK_ALLOWED_SYMBOLS when MT5 is unavailable
    so the UI always has something to display.
    """
    if mt5 is None:
        logger.warning("GET /symbols: MT5 unavailable, returning config fallback")
        return {"status": "degraded", "data": config.RISK_ALLOWED_SYMBOLS}

    try:
        all_syms = mt5.symbols_get() or []
        # Return only visible/selectable symbols to keep the list manageable
        names = sorted({s.name for s in all_syms if getattr(s, "visible", True)})
        return {"status": "success", "data": names}
    except Exception as exc:
        logger.exception("GET /symbols error: %s", exc)
        return {"status": "degraded", "data": config.RISK_ALLOWED_SYMBOLS}


@router.get("/symbols/{symbol}/tick")
def symbol_tick(symbol: str, mt5=Depends(get_mt5_client)):
    """Return the latest bid/ask for a single symbol (for preview in the selector)."""
    if mt5 is None:
        raise HTTPException(status_code=503, detail="MT5 not connected")

    if not mt5.symbol_select(symbol, True):
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not available")

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise HTTPException(status_code=404, detail=f"No tick data for '{symbol}'")

    return {
        "status": "success",
        "data": {
            "symbol": symbol,
            "bid": tick.bid,
            "ask": tick.ask,
            "time": tick.time,
        },
    }


@router.get("/market/candles")
def candles(
    symbol: str = Query(..., description="e.g. EURUSD"),
    timeframe: str = Query(default="M5", description="M1 | M5 | M15 | M30 | H1 | H4 | D1"),
    count: int = Query(default=100, ge=10, le=500),
    mt5=Depends(get_mt5_client),
):
    """Return OHLCV bars for charting in the execution panel."""
    if mt5 is None:
        raise HTTPException(status_code=503, detail="MT5 not connected")

    tf_attr = _TIMEFRAME_MAP.get(timeframe.upper())
    if tf_attr is None:
        raise HTTPException(status_code=400, detail=f"Unknown timeframe '{timeframe}'")

    tf_const = getattr(mt5, tf_attr, None)
    if tf_const is None:
        raise HTTPException(status_code=500, detail="Timeframe constant unavailable")

    if not mt5.symbol_select(symbol, True):
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not available")

    rates = mt5.copy_rates_from_pos(symbol, tf_const, 0, count)
    if rates is None or len(rates) == 0:
        return {"status": "success", "data": []}

    return {
        "status": "success",
        "data": [
            {
                "time": int(r["time"]),
                "open": float(r["open"]),
                "high": float(r["high"]),
                "low": float(r["low"]),
                "close": float(r["close"]),
                "volume": int(r["tick_volume"]),
            }
            for r in rates
        ],
    }
