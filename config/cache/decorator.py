from functools import wraps
from typing import Optional, Union, Callable
from datetime import timedelta
from .client import CacheClient
from .exceptions import CacheException

def cached(
    key_prefix: str = "",
    timeout: Optional[Union[int, timedelta]] = None,
    cache_client: Optional[CacheClient] = None,
    key_builder: Optional[Callable] = None
):
    """Decorator untuk cache function results
    
    Args:
        key_prefix: Prefix untuk cache key
        timeout: Waktu cache expire
        cache_client: Instance CacheClient custom
        key_builder: Function untuk generate cache key
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cache_client is None:
                client = CacheClient()
            else:
                client = cache_client

            # Build cache key
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                args_key = ':'.join(str(arg) for arg in args)
                kwargs_key = ':'.join(f"{k}={v}" for k, v in sorted(kwargs.items()))
                cache_key = f"{key_prefix}:{func.__name__}:{args_key}:{kwargs_key}"

            # Try to get from cache
            cached_value = client.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Execute function and cache result
            result = func(*args, **kwargs)
            client.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator

def cache_invalidate(
    key_pattern: str,
    cache_client: Optional[CacheClient] = None
):
    """Decorator untuk invalidate cache
    
    Args:
        key_pattern: Pattern untuk cache keys yang akan diinvalidate
        cache_client: Instance CacheClient custom
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cache_client is None:
                client = CacheClient()
            else:
                client = cache_client

            result = func(*args, **kwargs)
            client.delete_pattern(key_pattern)
            return result
        return wrapper
    return decorator