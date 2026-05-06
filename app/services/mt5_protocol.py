from __future__ import annotations

from typing import Any, Optional, Protocol, Sequence


class MT5AccountInfo(Protocol):
    balance: float
    equity: float
    profit: float


class MT5Position(Protocol):
    ticket: int
    symbol: str
    volume: float
    type: int  # 0=BUY, 1=SELL (MT5 convention)
    profit: float


class MT5Tick(Protocol):
    bid: float
    ask: float
    time: int


class MT5Client(Protocol):
    # Market / account
    def account_info(self) -> Optional[MT5AccountInfo]: ...
    def positions_get(self, **kwargs: Any) -> Optional[Sequence[MT5Position]]: ...
    def symbol_info_tick(self, symbol: str) -> Optional[MT5Tick]: ...
    def symbol_select(self, symbol: str, enable: bool) -> bool: ...
    def symbol_info(self, symbol: str) -> Any: ...

    # Trading / history
    def order_send(self, request: dict) -> Any: ...
    def history_deals_get(self, **kwargs: Any) -> Any: ...
    def last_error(self) -> Any: ...

    # Constants (exposed by mt5linux client)
    TRADE_ACTION_DEAL: int
    ORDER_TYPE_BUY: int
    ORDER_TYPE_SELL: int
    ORDER_TIME_GTC: int
    ORDER_FILLING_FOK: int
    ORDER_FILLING_IOC: int
    ORDER_FILLING_RETURN: int
    TRADE_RETCODE_DONE: int

