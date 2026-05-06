from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class StrategyMeta:
    id: str
    name: str
    enabled: bool = False


_strategies: Dict[str, StrategyMeta] = {
    "london_breakout": StrategyMeta(id="london_breakout", name="London Breakout", enabled=True),
    "ny_reversal": StrategyMeta(id="ny_reversal", name="NY Reversal", enabled=False),
}


def list_strategies() -> List[StrategyMeta]:
    return list(_strategies.values())


def toggle_strategy(strategy_id: str) -> StrategyMeta | None:
    s = _strategies.get(strategy_id)
    if s is None:
        return None
    s.enabled = not s.enabled
    return s

