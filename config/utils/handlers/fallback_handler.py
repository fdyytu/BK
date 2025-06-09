from typing import Any, Dict, Generic, List, Optional, TypeVar
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

T = TypeVar('T')

class FallbackStrategy(ABC, Generic[T]):
    """Abstract base class for fallback strategies following ISP."""
    
    @abstractmethod
    async def get_fallback(self, key: str) -> Optional[T]:
        """Get fallback value for key."""
        pass
    
    @abstractmethod
    async def store_fallback(self, key: str, value: T) -> None:
        """Store fallback value for key."""
        pass

class CachingFallbackStrategy(FallbackStrategy[T]):
    """Fallback strategy using in-memory cache."""
    
    def __init__(self, ttl: int = 300) -> None:
        self._cache: Dict[str, tuple[T, datetime]] = {}
        self._ttl = ttl
    
    async def get_fallback(self, key: str) -> Optional[T]:
        """Get cached fallback value if not expired."""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if datetime.utcnow() - timestamp < timedelta(seconds=self._ttl):
                return value
            del self._cache[key]
        return None
    
    async def store_fallback(self, key: str, value: T) -> None:
        """Store value in cache with timestamp."""
        self._cache[key] = (value, datetime.utcnow())

class FileFallbackStrategy(FallbackStrategy[T]):
    """Fallback strategy using file storage."""
    
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._cache = CachingFallbackStrategy[T]()
    
    async def get_fallback(self, key: str) -> Optional[T]:
        """Get fallback value from file or cache."""
        # Try cache first
        value = await self._cache.get_fallback(key)
        if value:
            return value
            
        # Try file
        try:
            with open(self._file_path, 'r') as f:
                import json
                data = json.load(f)
                if key in data:
                    value = data[key]
                    await self._cache.store_fallback(key, value)
                    return value
        except:
            return None
    
    async def store_fallback(self, key: str, value: T) -> None:
        """Store fallback value in file and cache."""
        try:
            # Update file
            with open(self._file_path, 'r+') as f:
                import json
                try:
                    data = json.load(f)
                except:
                    data = {}
                data[key] = value
                f.seek(0)
                json.dump(data, f)
                f.truncate()
            
            # Update cache
            await self._cache.store_fallback(key, value)
        except:
            pass

class FallbackHandler(Generic[T]):
    """Handler for managing fallback values following SRP."""
    
    def __init__(
        self,
        strategies: Optional[List[FallbackStrategy[T]]] = None,
        max_attempts: int = 3
    ) -> None:
        self._strategies = strategies or []
        self._max_attempts = max_attempts
        self._attempt_count: Dict[str, int] = {}
    
    async def get_value(
        self,
        key: str,
        default: Optional[T] = None
    ) -> Optional[T]:
        """Get value from fallback strategies."""
        # Check attempt count
        if self._attempt_count.get(key, 0) >= self._max_attempts:
            return default
        
        # Try each strategy
        for strategy in self._strategies:
            value = await strategy.get_fallback(key)
            if value is not None:
                return value
        
        # Increment attempt count
        self._attempt_count[key] = self._attempt_count.get(key, 0) + 1
        
        return default
    
    async def store_value(self, key: str, value: T) -> None:
        """Store value in all fallback strategies."""
        for strategy in self._strategies:
            await strategy.store_fallback(key, value)
        
        # Reset attempt count
        self._attempt_count[key] = 0
    
    def add_strategy(self, strategy: FallbackStrategy[T]) -> None:
        """Add fallback strategy."""
        self._strategies.append(strategy)
    
    def reset_attempts(self, key: Optional[str] = None) -> None:
        """Reset attempt count for key or all keys."""
        if key:
            self._attempt_count.pop(key, None)
        else:
            self._attempt_count.clear()