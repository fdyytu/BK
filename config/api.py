from typing import Any, Dict, List, Optional
from pydantic import BaseModel, AnyHttpUrl
from .settings import get_settings

settings = get_settings()

class APISettings(BaseModel):
    """API configuration settings."""
    
    # API Information
    title: str = settings.app.name
    description: str = settings.app.description
    version: str = settings.app.version
    
    # API Documentation
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    
    # CORS Settings
    cors_origins: List[AnyHttpUrl] = []
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Rate Limiting
    rate_limit_enabled: bool = settings.security.rate_limit_enabled 
    rate_limit_by: str = settings.security.rate_limit_by
    rate_limit_period: int = settings.security.rate_limit_period
    rate_limit_max_requests: int = settings.security.rate_limit_max_requests
    
    # Response Settings
    default_response_model: Dict[str, Any] = {
        "success": True,
        "message": "",
        "data": None,
        "meta": {
            "timestamp": "",
            "version": version
        }
    }
    
    # Middleware Configuration
    middleware_config: Dict[str, Any] = {
        "cors": {
            "allow_origins": cors_origins,
            "allow_credentials": cors_allow_credentials,
            "allow_methods": cors_allow_methods,
            "allow_headers": cors_allow_headers
        },
        "authentication": {
            "secret_key": settings.security.secret_key.get_secret_value(),
            "algorithm": settings.security.algorithm
        },
        "rate_limit": {
            "enabled": rate_limit_enabled,
            "by": rate_limit_by,
            "period": rate_limit_period,
            "max_requests": rate_limit_max_requests
        }
    }