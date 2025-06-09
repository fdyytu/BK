from typing import Optional, Any
from datetime import timedelta
import json
from redis import Redis
from ..settings import get_settings

settings = get_settings()

class CacheService:
    """Redis cache service implementation."""
    
    def __init__(self):
        self.client = Redis.from_url(
            url=str(settings.cache.redis_url),
            db=settings.cache.redis_db,
            socket_timeout=settings.cache.redis_socket_timeout,
            retry_on_timeout=settings.cache.redis_retry_on_timeout
        )
        self.default_ttl = settings.cache.timeout
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            data = await self.client.get(key)
            return json.loads(data) if data else None
        except (json.JSONDecodeError, Exception):
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Set value in cache."""
        try:
            ttl = ttl or self.default_ttl
            return await self.client.setex(
                key,
                ttl,
                json.dumps(value)
            )
        except Exception:
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        try:
            return bool(await self.client.delete(key))
        except Exception:
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        try:
            return bool(await self.client.exists(key))
        except Exception:
            return False
    
    async def clear_pattern(self, pattern: str) -> bool:
        """Clear all keys matching pattern."""
        try:
            keys = await self.client.keys(pattern)
            if keys:
                return bool(await self.client.delete(*keys))
            return True
        except Exception:
            return False