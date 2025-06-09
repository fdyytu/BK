from typing import Dict, Any, Optional
import json
from pathlib import Path
from .environment import EnvironmentConfig, Environment, get_config

class ConfigManager:
    """Configuration manager."""
    
    def __init__(self):
        self.config = get_config()
        self._cache: Dict[str, Any] = {}
    
    def get_service_settings(self, service: str) -> Dict[str, Any]:
        """Get service settings."""
        if service not in self._cache:
            self._cache[service] = self.config.get_service_config(service)
        return self._cache[service]
    
    def get_database_settings(self) -> Dict[str, Any]:
        """Get database settings."""
        if 'database' not in self._cache:
            self._cache['database'] = self.config.get_mongodb_settings()
        return self._cache['database']
    
    def get_redis_settings(self) -> Dict[str, Any]:
        """Get Redis settings."""
        if 'redis' not in self._cache:
            self._cache['redis'] = self.config.get_redis_settings()
        return self._cache['redis']
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': self.config.LOG_FORMAT
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                    'level': self.config.LOG_LEVEL
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': 'ppob.log',
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5,
                    'formatter': 'default',
                    'level': self.config.LOG_LEVEL
                }
            },
            'root': {
                'handlers': ['console', 'file'],
                'level': self.config.LOG_LEVEL
            }
        }
    
    def save_config(self, config_path: Path) -> None:
        """Save current configuration to file."""
        config_data = {
            'environment': self.config.ENVIRONMENT,
            'database': self.get_database_settings(),
            'redis': self.get_redis_settings(),
            'services': {
                'payment': self.get_service_settings('payment'),
                'notification': self.get_service_settings('notification'),
                'provider': self.get_service_settings('provider')
            }
        }
        
        with config_path.open('w') as f:
            json.dump(config_data, f, indent=2)
    
    @classmethod
    def load_config(cls, config_path: Path) -> 'ConfigManager':
        """Load configuration from file."""
        with config_path.open('r') as f:
            config_data = json.load(f)
            
        # Update environment variables
        for key, value in config_data.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    import os
                    os.environ[f"{key.upper()}_{k.upper()}"] = str(v)
            else:
                os.environ[key.upper()] = str(value)
                
        return cls()