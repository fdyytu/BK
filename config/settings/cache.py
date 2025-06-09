from typing import Optional, Dict, Any, Union
from pydantic import BaseModel, RedisDsn
from .environment import EnvironmentSettings

class CacheSettings(BaseModel):
    enabled: bool = True
    backend: str = "simple"  # simple, redis, memcached
    timeout: int = 300
    key_prefix: str = "myapi_"
    
    # Redis specific
    redis_url: Optional[RedisDsn] = None
    redis_db: int = 0
    redis_password: Optional[str] = None
    redis_socket_timeout: int = 5
    redis_retry_on_timeout: bool = True
    
    # Memcached specific
    memcached_servers: list = ["localhost:11211"]
    memcached_binary: bool = True
    memcached_behaviors: Dict[str, Any] = {
        "tcp_nodelay": True,
        "ketama": True
    }
    
    # Key patterns
    key_patterns: Dict[str, str] = {
        "user_profile": "user:profile:{}",
        "user_settings": "user:settings:{}",
        "api_response": "api:response:{}",
        "rate_limit": "rate:limit:{}",
        "session": "session:{}"
    }
    
    # Cache regions
    regions: Dict[str, Dict[str, Union[int, str]]] = {
        "default": {
            "timeout": 300
        },
        "static": {
            "timeout": 3600
        },
        "dynamic": {
            "timeout": 60
        }
    }
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "CacheSettings":
        settings = cls()
        
        if env.is_production:
            settings.backend = "redis"
            settings.timeout = 600
            settings.redis_url = "redis://prod-cache:6379/0"
            
        return settings