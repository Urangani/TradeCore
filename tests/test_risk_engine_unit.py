import unittest


class FakeAccount:
    def __init__(self, *, balance: float, equity: float):
        self.balance = balance
        self.equity = equity
        self.profit = equity - balance


class FakeMT5:
    def __init__(self, *, open_positions: int = 0, balance: float = 1000.0, equity: float = 1000.0):
        self._open_positions = open_positions
        self._account = FakeAccount(balance=balance, equity=equity)

    def positions_get(self, **kwargs):
        return [object() for _ in range(self._open_positions)]

    def account_info(self):
        return self._account


class RiskEngineUnitTests(unittest.TestCase):
    def test_rejects_disallowed_symbol(self):
        from app.services.risk_engine import validate_trade

        ok, msg = validate_trade("XAUUSD", 0.1, mt5=FakeMT5())
        self.assertFalse(ok)
        self.assertIn("Symbol not allowed", msg)

    def test_rejects_lot_over_limit(self):
        from app.services.risk_engine import validate_trade

        ok, msg = validate_trade("EURUSD", 999.0, mt5=FakeMT5())
        self.assertFalse(ok)
        self.assertIn("Lot size exceeds limit", msg)

    def test_rejects_max_open_trades(self):
        from app.services.risk_engine import validate_trade

        ok, msg = validate_trade("EURUSD", 0.1, mt5=FakeMT5(open_positions=999))
        self.assertFalse(ok)
        self.assertIn("Max open trades reached", msg)

    def test_rejects_daily_loss(self):
        from app.services.risk_engine import validate_trade

        ok, msg = validate_trade("EURUSD", 0.1, mt5=FakeMT5(balance=1000.0, equity=0.0))
        self.assertFalse(ok)
        self.assertIn("Daily loss limit hit", msg)


if __name__ == "__main__":
    unittest.main()

