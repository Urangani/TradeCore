from typing import Optional

from app.core.config import Settings
from app.core.logging import logger
from app.services.mt5_protocol import MT5Client

class RiskPolicy:
    def __init__(self, config: Settings, mt5: Optional[MT5Client]):
        self.config = config
        self.mt5 = mt5

    def validate_trade(self, symbol: str, lot: float) -> tuple[bool, str]:
        if self.mt5 is None:
            logger.warning("Risk check failed: MT5 not connected")
            return False, "MT5 not connected"

        # ───── SYMBOL CHECK ─────
        if symbol not in self.config.RISK_ALLOWED_SYMBOLS:
            logger.info("Risk reject: symbol not allowed (%s)", symbol)
            return False, f"Symbol not allowed: {symbol}"

        # ───── LOT SIZE CHECK ─────
        if lot <= 0 or lot > self.config.RISK_MAX_LOT:
            logger.info("Risk reject: lot out of bounds (%s)", lot)
            return False, f"Lot size exceeds limit ({self.config.RISK_MAX_LOT})"

        # ───── OPEN TRADES LIMIT ─────
        positions = self.mt5.positions_get()
        if positions and len(positions) >= self.config.RISK_MAX_OPEN_TRADES:
            logger.info("Risk reject: max open trades reached (%s)", len(positions))
            return False, "Max open trades reached"

        # ───── DAILY LOSS CHECK ─────
        account = self.mt5.account_info()

        if account:
            equity_change = account.equity - account.balance
            if equity_change < self.config.RISK_MAX_DAILY_LOSS:
                logger.info("Risk reject: daily loss limit hit (%s)", equity_change)
                return False, "Daily loss limit hit"

        return True, "OK"