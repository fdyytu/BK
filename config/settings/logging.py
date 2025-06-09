import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel
from pathlib import Path
from .environment import EnvironmentSettings

class LogSettings(BaseModel):
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    
    # File logging
    file_enabled: bool = True
    file_path: Optional[Path] = None
    max_bytes: int = 10485760  # 10MB
    backup_count: int = 5
    
    # Sentry logging
    sentry_enabled: bool = False
    sentry_dsn: Optional[str] = None
    sentry_traces_sample_rate: float = 1.0
    
    # Configuration by logger name
    loggers: Dict[str, Dict[str, Any]] = {
        "uvicorn": {
            "level": "INFO",
            "propagate": False
        },
        "sqlalchemy.engine": {
            "level": "WARNING",
            "propagate": False
        },
        "alembic": {
            "level": "INFO",
            "propagate": False
        }
    }
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "LogSettings":
        settings = cls()
        
        if env.is_development:
            settings.level = "DEBUG"
            settings.file_enabled = False
            
        if env.is_production:
            settings.level = "WARNING"
            settings.file_path = Path("/var/log/app/app.log")
            settings.sentry_enabled = True
            
        return settings

    def get_config(self) -> Dict[str, Any]:
        """Get logging configuration dictionary."""
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": self.format,
                    "datefmt": self.date_format
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout"
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": str(self.file_path or "app.log"),
                    "maxBytes": self.max_bytes,
                    "backupCount": self.backup_count
                } if self.file_enabled else None
            },
            "loggers": self.loggers,
            "root": {
                "level": self.level,
                "handlers": ["console", "file"] if self.file_enabled else ["console"]
            }
        }