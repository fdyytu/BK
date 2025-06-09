import redis
from typing import Any, Optional, Union
from datetime import timedelta
from .base import BaseDriver
from ..exceptions import CacheConnectionError, CacheException

class RedisDriver(BaseDriver):
    """Redis cache driver implementation"""
    
    def __init__(
        self, 
        host: str = 'localhost',
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        socket_timeout: int = 5,
        namespace: str = ""
    ):
        super().__init__(namespace)
        try:
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                socket_timeout=socket_timeout,
                decode_responses=True
            )
            self.client.ping()  # Test connection
        except redis.ConnectionError as e:
            raise CacheConnectionError(f"Redis connection failed: {str(e)}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from Redis"""
        try:
            key = self._make_key(key)
            self._validate_key(key)
            value = self.client.get(key)
            return value if value is not None else default
        except redis.RedisError as e:
            raise CacheException(f"Redis get error: {str(e)}")
            
    def set(
        self, 
        key: str, 
        value: Any, 
        timeout: Optional[Union[int, timedelta]] = None
    ) -> bool:
        """Set value in Redis"""
        try:
            key = self._make_key(key)
            self._validate_key(key)
            timeout = self._validate_timeout(timeout)
            return self.client.set(key, value, ex=timeout)
        except redis.RedisError as e:
            raise CacheException(f"Redis set error: {str(e)}")