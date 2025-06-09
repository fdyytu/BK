from functools import lru_cache
from typing import Dict, Any
from pydantic import BaseSettings
from .app import AppSettings
from .database import DatabaseSettings
from .cache import CacheSettings
from .logging import LogSettings
from .celery import CelerySettings
from .security import SecuritySettings
from .environment import EnvironmentSettings

class Settings(BaseSettings):
    """Global application settings."""
    
    env: EnvironmentSettings
    app: AppSettings
    db: DatabaseSettings
    cache: CacheSettings
    log: LogSettings
    celery: CelerySettings
    security: SecuritySettings
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
    @property
    def dict_config(self) -> Dict[str, Any]:
        """Get all settings as dictionary."""
        return {
            "env": self.env.dict(),
            "app": self.app.dict(),
            "db": self.db.dict(),
            "cache": self.cache.dict(),
            "log": self.log.dict(),
            "celery": self.celery.dict(),
            "security": self.security.dict()
        }

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    env = EnvironmentSettings()
    return Settings(
        env=env,
        app=AppSettings.from_env(env),
        db=DatabaseSettings.from_env(env),
        cache=CacheSettings.from_env(env),
        log=LogSettings.from_env(env),
        celery=CelerySettings.from_env(env),
        security=SecuritySettings.from_env(env)
    )