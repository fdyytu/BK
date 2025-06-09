from typing import Any, Dict
from pydantic import BaseSettings, SecretStr
from functools import lru_cache

class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    HOST: str
    PORT: int
    NAME: str
    USER: str
    PASSWORD: SecretStr
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 1800
    
    @property
    def connection_url(self) -> str:
        """Get database connection URL."""
        return (
            f"postgresql+asyncpg://{self.USER}:"
            f"{self.PASSWORD.get_secret_value()}@"
            f"{self.HOST}:{self.PORT}/{self.NAME}"
        )
    
    class Config:
        """Pydantic configuration."""
        env_prefix = "DB_"
        case_sensitive = True

class CacheSettings(BaseSettings):
    """Cache configuration settings."""
    
    HOST: str
    PORT: int
    PASSWORD: SecretStr
    DB: int = 0
    POOL_SIZE: int = 10
    TIMEOUT: int = 3
    
    class Config:
        """Pydantic configuration."""
        env_prefix = "CACHE_"