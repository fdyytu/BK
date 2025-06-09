from typing import List, Optional
from pydantic import BaseModel
from .environment import EnvironmentSettings

class MiddlewareSettings(BaseModel):
    """Middleware configuration with validation"""
    
    # Common Middleware
    trust_proxy: bool = False
    allow_credentials: bool = True
    expose_headers: List[str] = ["*"]
    max_age: int = 600
    
    # Security Middleware
    csrf_enabled: bool = True
    csrf_methods: List[str] = ["POST", "PUT", "PATCH", "DELETE"]
    csrf_cookie_name: str = "csrf_token"
    csrf_header_name: str = "X-CSRF-Token"
    
    # Session Middleware
    session_enabled: bool = True
    session_key: str = "session"
    session_max_age: int = 86400  # 1 day
    session_http_only: bool = True
    session_secure: bool = True
    
    # Cache Middleware
    cache_enabled: bool = True
    cache_max_age: int = 300  # 5 minutes
    cache_control: str = "public"
    
    # Compression
    compression_enabled: bool = True
    compression_level: int = 6
    min_size: int = 1024  # 1KB
    
    # Logging Middleware
    request_logging: bool = True
    response_logging: bool = True
    error_logging: bool = True
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_by: str = "ip"  # ip, user, custom
    rate_limit_storage: str = "memory"  # memory, redis
    
    class Config:
        env_prefix = "MIDDLEWARE_"
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "MiddlewareSettings":
        """Create settings from environment"""
        settings = cls()
        
        # Override settings based on environment
        if env.is_development:
            settings.csrf_enabled = False
            settings.session_secure = False
            settings.compression_enabled = False
            
        if env.is_production:
            settings.trust_proxy = True
            settings.rate_limit_storage = "redis"
            settings.cache_max_age = 3600  # 1 hour in production
            
        return settings