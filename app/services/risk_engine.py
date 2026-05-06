from typing import Optional

from app.core import config
from app.core.logging import logger
from app.services.mt5_protocol import MT5Client
from app.services.mt5_service import get_mt5

def validate_trade(symbol: str, lot: float, mt5: Optional[MT5Client] = None):
    mt5 = mt5 or get_mt5()

    if mt5 is None:
        logger.warning("Risk check failed: MT5 not connected")
        return False, "MT5 not connected"

    # ───── SYMBOL CHECK ─────
    if symbol not in config.RISK_ALLOWED_SYMBOLS:
        logger.info("Risk reject: symbol not allowed (%s)", symbol)
        return False, f"Symbol not allowed: {symbol}"

    # ───── LOT SIZE CHECK ─────
    if lot <= 0 or lot > config.RISK_MAX_LOT:
        logger.info("Risk reject: lot out of bounds (%s)", lot)
        return False, f"Lot size exceeds limit ({config.RISK_MAX_LOT})"

    # ───── OPEN TRADES LIMIT ─────
    positions = mt5.positions_get()
    if positions and len(positions) >= config.RISK_MAX_OPEN_TRADES:
        logger.info("Risk reject: max open trades reached (%s)", len(positions))
        return False, "Max open trades reached"

    # ───── DAILY LOSS CHECK ─────
    account = mt5.account_info()

    if account:
        equity_change = account.equity - account.balance
        if equity_change < config.RISK_MAX_DAILY_LOSS:
            logger.info("Risk reject: daily loss limit hit (%s)", equity_change)
            return False, "Daily loss limit hit"

    return True, "OK"