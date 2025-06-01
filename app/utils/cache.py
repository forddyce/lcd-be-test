from datetime import datetime, timedelta
from typing import Any, Dict

class InMemoryCache:
    def __init__(self, ttl_minutes: int):
        """
        initializes cache with a specified time-to-live.
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = timedelta(minutes=ttl_minutes)

    def get(self, key: str) -> Any | None:
        """
        get an item from the cache or None
        """
        if key in self.cache:
            data, timestamp = self.cache[key]['data'], self.cache[key]['timestamp']
            if datetime.now() - timestamp < self.ttl:
                return data
            else:
                # item expired, remove it from cache
                self.delete(key)
        return None

    def set(self, key: str, value: Any):
        """
        stores an item in the cache with the current timestamp
        """
        self.cache[key] = {'data': value, 'timestamp': datetime.now()}

    def delete(self, key: str):
        """
        removes an item from the cache.
        """
        if key in self.cache:
            del self.cache[key]

    def invalidate(self, key: str):
        """
        force delete (invalidate) an item from cache
        """
        self.delete(key)