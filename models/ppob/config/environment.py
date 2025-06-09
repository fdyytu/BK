from enum import Enum
from typing import Dict, Any, Optional
from functools import lru_cache
from .base_config import BaseConfig
from .service_config import PaymentConfig, NotificationConfig, ProviderConfig

class Environment(str, Enum):
    """Environment enumeration."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class EnvironmentConfig(BaseConfig):
    """Environment-specific configuration."""
    
    # Environment
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    
    # Service Configs
    PAYMENT: PaymentConfig
    NOTIFICATION: NotificationConfig
    PROVIDER: ProviderConfig
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_ENABLED: bool = False
    
    # Cache
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 300  # seconds
    
    @property
    def is_development(self) -> bool:
        """Check if environment is development."""
        return self.ENVIRONMENT == Environment.DEVELOPMENT
    
    @property
    def is_staging(self) -> bool:
        """Check if environment is staging."""
        return self.ENVIRONMENT == Environment.STAGING
    
    @property
    def is_production(self) -> bool:
        """Check if environment is production."""
        return self.ENVIRONMENT == Environment.PRODUCTION
    
    def get_service_config(self, service: str) -> Dict[str, Any]:
        """Get service configuration."""
        service_map = {
            'payment': self.PAYMENT,
            'notification': self.NOTIFICATION,
            'provider': self.PROVIDER
        }
        return service_map[service].dict()

@lru_cache()
def get_config() -> EnvironmentConfig:
    """Get cached configuration instance."""
    return EnvironmentConfig()