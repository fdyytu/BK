from typing import Dict, List, Optional
from pydantic import BaseModel, AnyHttpUrl, EmailStr, SecretStr
from .environment import EnvironmentSettings

class APISettings(BaseModel):
    """API configuration with validation"""
    
    # API Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    reload: bool = False
    
    # API Documentation
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    title: str = "Digital Product & PPOB API"
    description: str = "API for Digital Product and PPOB Platform"
    version: str = "1.0.0"
    
    # Security
    secret_key: SecretStr
    allowed_hosts: List[str] = ["*"]
    cors_origins: List[AnyHttpUrl] = []
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 3600  # 1 hour
    
    # Response
    default_response: Dict = {
        "success": True,
        "message": "",
        "data": None
    }
    
    # Pagination
    default_page_size: int = 10
    max_page_size: int = 100
    
    # Monitoring
    enable_metrics: bool = False
    metrics_path: str = "/metrics"
    
    class Config:
        env_prefix = "API_"
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "APISettings":
        """Create settings from environment"""
        settings = cls(
            secret_key=SecretStr("your-secret-key-here")
        )
        
        # Override settings based on environment
        if env.is_development:
            settings.reload = True
            settings.cors_origins = ["http://localhost:3000"]
            settings.enable_metrics = True
            
        if env.is_production:
            settings.workers = 8
            settings.rate_limit_enabled = True
            settings.enable_metrics = True
            settings.allowed_hosts = ["api.yourdomain.com"]
            
        return settings