from datetime import timedelta
from typing import Optional, Union
from pydantic import BaseModel, RedisDsn
from .environment import EnvironmentSettings

class CacheSettings(BaseModel):
    """Cache configuration with validation"""
    
    # Redis Connection
    redis_url: Optional[RedisDsn] = None
    prefix: str = "cache:"
    
    # Cache Settings
    default_timeout: timedelta = timedelta(minutes=5)
    key_func: str = "default"  # default key function name
    
    # Local Cache Settings (fallback)
    local_cache_size: int = 1000
    local_cache_ttl: timedelta = timedelta(minutes=1)
    
    class Config:
        env_prefix = "CACHE_"
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "CacheSettings":
        """Create settings from environment"""
        settings = cls()
        
        # Override settings based on environment
        if env.is_development:
            settings.redis_url = "redis://localhost:6379/0"
            settings.default_timeout = timedelta(hours=1)
        
        return settings