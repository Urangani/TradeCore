from typing import Optional, Any

class StateService:
    def __init__(self):
        self._cache = {
            "account": None,
            "positions": None,
            "price": None,
        }

    def get(self, key: str) -> Optional[Any]:
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value

    def has_changed(self, key: str, value: Any) -> bool:
        return self._cache.get(key) != value

# Singleton instance for simple in-memory caching
state_cache = StateService()