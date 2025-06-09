from typing import Any, Optional
from .interface import CacheStrategy
from ..drivers.base import BaseDriver

class TieredCache(CacheStrategy):
    """Implementasi tiered caching (L1, L2, etc.)"""
    
    def __init__(self, *drivers: BaseDriver):
        self.drivers = drivers  # Ordered from fastest to slowest
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache tiers"""
        for i, driver in enumerate(self.drivers):
            value = driver.get(key)
            if value is not None:
                # Populate higher tiers
                self._populate_higher_tiers(key, value, i)
                return value
        return None
    
    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> bool:
        """Set value in all cache tiers"""
        success = True
        for driver in self.drivers:
            if not driver.set(key, value, timeout):
                success = False
        return success
    
    def _populate_higher_tiers(self, key: str, value: Any, found_tier: int):
        """Populate value to higher (faster) tiers"""
        for i in range(found_tier - 1, -1, -1):
            self.drivers[i].set(key, value)