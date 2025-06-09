from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, validator
from enum import Enum
from .environment import EnvironmentSettings

class EmailProvider(str, Enum):
    SMTP = "smtp"
    SENDGRID = "sendgrid"
    MAILGUN = "mailgun"
    SES = "ses"

class SMTPSettings(BaseModel):
    """SMTP server settings."""
    host: str = "smtp.gmail.com"
    port: int = 587
    username: str
    password: str
    use_tls: bool = True
    use_ssl: bool = False
    timeout: int = 30
    
class SendGridSettings(BaseModel):
    """SendGrid settings."""
    api_key: str
    sender_name: str
    templates: Dict[str, str] = {}
    
class MailgunSettings(BaseModel):
    """Mailgun settings."""
    api_key: str
    domain: str
    api_url: str = "https://api.mailgun.net/v3"
    
class SESSettings(BaseModel):
    """Amazon SES settings."""
    access_key: str
    secret_key: str
    region: str = "us-east-1"

class EmailSettings(BaseModel):
    """Email configuration settings."""
    
    enabled: bool = True
    provider: EmailProvider = EmailProvider.SMTP
    default_sender: EmailStr
    default_sender_name: str
    
    # Provider Specific Settings
    smtp: Optional[SMTPSettings]
    sendgrid: Optional[SendGridSettings]
    mailgun: Optional[MailgunSettings]
    ses: Optional[SESSettings]
    
    # Email Templates
    template_dir: str = "templates/email"
    templates: Dict[str, str] = {
        "welcome": "welcome.html",
        "reset_password": "reset_password.html",
        "verify_email": "verify_email.html",
        "notification": "notification.html"
    }
    
    # Sending Settings
    rate_limit: int = 100  # emails per minute
    batch_size: int = 50
    retry_attempts: int = 3
    retry_delay: int = 5  # seconds
    
    # Content Settings
    max_attachment_size: int = 10 * 1024 * 1024  # 10MB
    allowed_attachment_types: List[str] = [
        "application/pdf",
        "image/jpeg",
        "image/png",
        "text/plain"
    ]
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "EmailSettings":
        """Create settings from environment."""
        provider = EmailProvider(env.get_env("EMAIL_PROVIDER", "smtp"))
        settings = cls(
            enabled=env.get_env("EMAIL_ENABLED", "true").lower() == "true",
            provider=provider,
            default_sender=env.get_env("EMAIL_SENDER", "noreply@example.com"),
            default_sender_name=env.get_env("EMAIL_SENDER_NAME", "MyApp")
        )
        
        if provider == EmailProvider.SMTP:
            settings.smtp = SMTPSettings(
                host=env.get_env("SMTP_HOST"),
                port=int(env.get_env("SMTP_PORT", "587")),
                username=env.get_env("SMTP_USERNAME"),
                password=env.get_env("SMTP_PASSWORD")
            )
            
        return settings