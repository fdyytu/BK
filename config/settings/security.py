from typing import List, Optional
from pydantic import BaseModel, SecretStr
from datetime import timedelta
from .environment import EnvironmentSettings

class SecuritySettings(BaseModel):
    secret_key: SecretStr
    algorithm: str = "HS256"
    
    # Token settings
    access_token_expire: timedelta = timedelta(minutes=15)
    refresh_token_expire: timedelta = timedelta(days=7)
    
    # Password settings
    password_min_length: int = 8
    password_max_length: int = 72
    password_require_uppercase: bool = True
    password_require_lowercase: bool = True
    password_require_digit: bool = True
    password_require_special: bool = True
    
    # Session settings
    session_cookie_name: str = "session"
    session_cookie_secure: bool = True
    session_cookie_httponly: bool = True
    session_cookie_samesite: str = "lax"
    
    # CSRF settings
    csrf_enabled: bool = True
    csrf_token_name: str = "csrf_token"
    csrf_header_name: str = "X-CSRF-Token"
    
    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_by: str = "ip"
    rate_limit_period: int = 3600
    rate_limit_max_requests: int = 100
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "SecuritySettings":
        settings = cls(
            secret_key=SecretStr("your-secret-key-here")
        )
        
        if env.is_development:
            settings.session_cookie_secure = False
            settings.rate_limit_enabled = False
            
        if env.is_production:
            settings.csrf_enabled = True
            settings.session_cookie_samesite = "strict"
            settings.rate_limit_max_requests = 1000
            
        return settings