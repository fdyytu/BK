from typing import Dict, Any, Optional
from pydantic import BaseSettings, Field
from functools import lru_cache

class BaseConfig(BaseSettings):
    """Base configuration settings."""
    
    # Application
    APP_NAME: str = "PPOB Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    MONGODB_URL: str
    MONGODB_DB: str
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    class Config:
        env_file = ".env"
        
    @lru_cache()
    def get_mongodb_settings(self) -> Dict[str, Any]:
        """Get MongoDB connection settings."""
        return {
            "url": self.MONGODB_URL,
            "db": self.MONGODB_DB
        }
    
    @lru_cache()
    def get_redis_settings(self) -> Dict[str, Any]:
        """Get Redis connection settings."""
        return {
            "host": self.REDIS_HOST,
            "port": self.REDIS_PORT,
            "password": self.REDIS_PASSWORD,
            "db": self.REDIS_DB
        }