from typing import Any, Optional, Union
from datetime import timedelta
from ..interface import CacheInterface
from ..exceptions import CacheException

class BaseDriver(CacheInterface):
    """Base class untuk cache drivers"""
    
    def __init__(self, namespace: str = ""):
        self.namespace = namespace
        
    def _make_key(self, key: str) -> str:
        """Generate key dengan namespace"""
        return f"{self.namespace}:{key}" if self.namespace else key
    
    def _validate_key(self, key: str) -> None:
        """Validasi format key"""
        if not isinstance(key, str):
            raise CacheKeyError("Cache key must be string")
        if len(key) > 250:
            raise CacheKeyError("Cache key is too long")
        if ' ' in key:
            raise CacheKeyError("Cache key cannot contain spaces")
            
    def _validate_timeout(self, timeout: Optional[Union[int, timedelta]]) -> Optional[int]:
        """Konversi dan validasi timeout"""
        if timeout is None:
            return None
        if isinstance(timeout, timedelta):
            timeout = int(timeout.total_seconds())
        if not isinstance(timeout, int):
            raise CacheTimeoutError("Timeout must be int or timedelta")
        if timeout < 0:
            raise CacheTimeoutError("Timeout cannot be negative")
        return timeout