from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StrategyMeta:
    id: str
    name: str
    enabled: bool = False
    description: str = ""
    params: Dict[str, Any] = field(default_factory=dict)


_strategies: Dict[str, StrategyMeta] = {
    "london_breakout": StrategyMeta(
        id="london_breakout",
        name="London Breakout",
        enabled=True,
        description="Trades breakouts at the London session open.",
        params={"lot": 0.1, "sl_pips": 20, "tp_pips": 40},
    ),
    "ny_reversal": StrategyMeta(
        id="ny_reversal",
        name="NY Reversal",
        enabled=False,
        description="Mean-reversion strategy at New York session open.",
        params={"lot": 0.05, "sl_pips": 15, "tp_pips": 30},
    ),
}


def list_strategies() -> List[StrategyMeta]:
    return list(_strategies.values())


def get_strategy(strategy_id: str) -> Optional[StrategyMeta]:
    return _strategies.get(strategy_id)


def toggle_strategy(strategy_id: str) -> Optional[StrategyMeta]:
    s = _strategies.get(strategy_id)
    if s is None:
        return None
    s.enabled = not s.enabled
    return s


def create_strategy(
    id: str,
    name: str,
    description: str = "",
    params: Optional[Dict[str, Any]] = None,
) -> Optional[StrategyMeta]:
    """Returns None if the id already exists."""
    if id in _strategies:
        return None
    s = StrategyMeta(id=id, name=name, description=description, params=params or {})
    _strategies[id] = s
    return s


def delete_strategy(strategy_id: str) -> bool:
    """Returns True if deleted, False if not found."""
    if strategy_id not in _strategies:
        return False
    del _strategies[strategy_id]
    return True

