from typing import Dict, Any, Optional
from pydantic import BaseModel
from .environment import EnvironmentSettings

class ServiceConfig(BaseModel):
    enabled: bool = True
    timeout: int = 30
    retry_attempts: int = 3
    retry_delay: int = 5
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: int = 60

class PaymentServiceSettings(ServiceConfig):
    provider: str = "stripe"
    api_version: str = "2025-01-01"
    webhook_secret: Optional[str] = None
    success_url: str = "/payment/success"
    cancel_url: str = "/payment/cancel"

class NotificationServiceSettings(ServiceConfig):
    provider: str = "firebase"
    template_dir: str = "templates/notifications"
    batch_size: int = 1000
    cooldown_period: int = 300

class CacheServiceSettings(ServiceConfig):
    provider: str = "redis"
    ttl: int = 300
    max_size: int = 1000
    serialize_format: str = "json"