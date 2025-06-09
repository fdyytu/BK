from typing import Any, Optional
from datetime import timedelta
import json
from redis.asyncio import Redis
from .exceptions import CacheError

class RedisCache:
    """Redis cache implementation."""
    
    def __init__(self, settings: CacheSettings):
        self._settings = settings
        self._client: Optional[Redis] = None
        
    async def connect(self) -> None:
        """Initialize Redis connection."""
        try:
            self._client = Redis(
                host=self._settings.HOST,
                port=self._settings.PORT,
                password=self._settings.PASSWORD.get_secret_value(),
                db=self._settings.DB,
                decode_responses=True,
                encoding='utf-8'
            )
            await self._client.ping()
        except Exception as e:
            raise CacheError(f"Redis connection error: {str(e)}")
            
    async def get(self, key: str) -> Any:
        """Get value from cache."""
        try:
            value = await self._client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            raise CacheError(f"Cache get error: {str(e)}")
            
    async def set(
        self, 
        key: str, 
        value: Any,
        expire: timedelta = None
    ) -> None:
        """Set value in cache."""
        try:
            await self._client.set(
                key,
                json.dumps(value),
                ex=int(expire.total_seconds()) if expire else None
            )
        except Exception as e:
            raise CacheError(f"Cache set error: {str(e)}")