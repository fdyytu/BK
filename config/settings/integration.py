from typing import Dict, Any, Optional
from pydantic import BaseModel, HttpUrl
from enum import Enum
from .environment import EnvironmentSettings

class IntegrationType(str, Enum):
    PAYMENT = "payment"
    SMS = "sms"
    STORAGE = "storage"
    ANALYTICS = "analytics"
    MAP = "map"

class PaymentGateway(BaseModel):
    """Payment gateway configuration."""
    provider: str
    api_key: str
    secret_key: str
    webhook_secret: Optional[str]
    sandbox_mode: bool = True
    
class SMSProvider(BaseModel):
    """SMS service configuration."""
    provider: str
    account_sid: str
    auth_token: str
    from_number: str
    
class StorageProvider(BaseModel):
    """Cloud storage configuration."""
    provider: str
    bucket: str
    credentials: Dict[str, Any]
    
class AnalyticsProvider(BaseModel):
    """Analytics service configuration."""
    provider: str
    tracking_id: str
    api_key: Optional[str]
    
class MapProvider(BaseModel):
    """Map service configuration."""
    provider: str
    api_key: str
    libraries: List[str] = []

class IntegrationSettings(BaseModel):
    """Third-party integration settings."""
    
    # Payment Integration
    payment: Dict[str, PaymentGateway] = {
        "stripe": PaymentGateway(
            provider="stripe",
            api_key="",
            secret_key="",
            webhook_secret=""
        ),
        "midtrans": PaymentGateway(
            provider="midtrans",
            api_key="",
            secret_key="",
            webhook_secret=""
        )
    }
    
    # SMS Integration
    sms: Dict[str, SMSProvider] = {
        "twilio": SMSProvider(
            provider="twilio",
            account_sid="",
            auth_token="",
            from_number=""
        )
    }
    
    # Storage Integration
    storage: Dict[str, StorageProvider] = {
        "s3": StorageProvider(
            provider="s3",
            bucket="",
            credentials={}
        )
    }
    
    # Analytics Integration
    analytics: Dict[str, AnalyticsProvider] = {
        "google": AnalyticsProvider(
            provider="google",
            tracking_id="",
            api_key=""
        )
    }
    
    # Map Integration
    map: Dict[str, MapProvider] = {
        "google": MapProvider(
            provider="google",
            api_key="",
            libraries=["places", "geometry"]
        )
    }
    
    # API Rate Limits
    rate_limits: Dict[str, int] = {
        "stripe": 100,
        "twilio": 100,
        "google": 500
    }
    
    # Webhook Settings
    webhook_timeout: int = 30
    webhook_retry_attempts: int = 3
    
    # Cache Settings
    cache_enabled: bool = True
    cache_ttl: int = 3600
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "IntegrationSettings":
        """Create settings from environment."""
        settings = cls()
        
        # Configure payment integration
        if env.get_env("STRIPE_ENABLED", "false").lower() == "true":
            settings.payment["stripe"].api_key = env.get_env("STRIPE_API_KEY")
            settings.payment["stripe"].secret_key = env.get_env("STRIPE_SECRET_KEY")
            settings.payment["stripe"].sandbox_mode = not env.is_production
            
        return settings