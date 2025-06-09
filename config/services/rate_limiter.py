from datetime import datetime
from typing import Optional, Tuple
from redis import Redis
from ..settings import get_settings

settings = get_settings()

class RateLimiter:
    """Redis-based rate limiter implementation."""
    
    def __init__(self):
        self.client = Redis.from_url(str(settings.cache.redis_url))
        self.max_requests = settings.security.rate_limit_max_requests
        self.period = settings.security.rate_limit_period
    
    def get_key(self, identifier: str) -> str:
        """Generate rate limit key."""
        return f"rate_limit:{identifier}"
    
    async def is_allowed(self, identifier: str) -> Tuple[bool, Optional[int]]:
        """Check if request is allowed and return remaining attempts."""
        key = self.get_key(identifier)
        
        pipe = self.client.pipeline()
        now = datetime.utcnow().timestamp()
        
        # Clean old requests
        pipe.zremrangebyscore(key, 0, now - self.period)
        
        # Count requests in current window
        pipe.zcard(key)
        
        # Add current request
        pipe.zadd(key, {str(now): now})
        
        # Set expiry
        pipe.expire(key, self.period)
        
        # Execute pipeline
        _, current_requests, _, _ = await pipe.execute()
        
        is_allowed = current_requests <= self.max_requests
        remaining = max(0, self.max_requests - current_requests)
        
        return is_allowed, remaining