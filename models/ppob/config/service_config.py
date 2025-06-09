from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class PaymentConfig(BaseModel):
    """Payment service configuration."""
    
    # Bank Transfer
    BANK_TRANSFER_API_KEY: str
    BANK_TRANSFER_MERCHANT_ID: str
    BANK_TRANSFER_SANDBOX: bool = True
    
    # E-Wallet
    EWALLET_API_KEY: str
    EWALLET_MERCHANT_ID: str
    EWALLET_SANDBOX: bool = True
    
    # Credit Card
    CREDIT_CARD_API_KEY: str
    CREDIT_CARD_MERCHANT_ID: str
    CREDIT_CARD_SANDBOX: bool = True

class NotificationConfig(BaseModel):
    """Notification service configuration."""
    
    # SMS
    SMS_API_KEY: str
    SMS_SENDER_ID: str
    SMS_SANDBOX: bool = True
    
    # Email
    EMAIL_SMTP_HOST: str
    EMAIL_SMTP_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    
    # Push Notification
    PUSH_API_KEY: str
    PUSH_APP_ID: str
    PUSH_SANDBOX: bool = True

class ProviderConfig(BaseModel):
    """Provider service configuration."""
    
    # Telco
    TELCO_API_KEY: str
    TELCO_MERCHANT_ID: str
    TELCO_SANDBOX: bool = True
    
    # Game
    GAME_API_KEY: str
    GAME_MERCHANT_ID: str
    GAME_SANDBOX: bool = True
    
    # Bill Payment
    BILL_API_KEY: str
    BILL_MERCHANT_ID: str
    BILL_SANDBOX: bool = True