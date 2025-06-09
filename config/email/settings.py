from typing import Optional, List
from pydantic import BaseModel, EmailStr, SecretStr
from .environment import EnvironmentSettings

class EmailSettings(BaseModel):
    """Email configuration with validation"""
    
    # SMTP Settings
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[SecretStr] = None
    smtp_use_tls: bool = True
    
    # Email Defaults
    default_from_email: EmailStr
    default_from_name: str = "PPOB System"
    reply_to: Optional[EmailStr] = None
    
    # Template Settings
    template_dir: str = "templates/email"
    template_engine: str = "jinja2"
    
    # Sending Settings
    connection_timeout: int = 10
    send_timeout: int = 30
    max_retries: int = 3
    retry_delay: int = 5
    
    # Testing
    test_email: Optional[EmailStr] = None
    suppress_send: bool = False
    
    # Notification Settings
    admin_emails: List[EmailStr] = []
    error_notify: bool = True
    
    class Config:
        env_prefix = "EMAIL_"
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "EmailSettings":
        """Create settings from environment"""
        settings = cls(
            default_from_email=EmailStr("noreply@yourdomain.com")
        )
        
        # Override settings based on environment
        if env.is_development:
            settings.suppress_send = True
            settings.test_email = EmailStr("dev@yourdomain.com")
            
        if env.is_testing:
            settings.suppress_send = True
            
        if env.is_production:
            settings.error_notify = True
            settings.admin_emails = [
                EmailStr("admin@yourdomain.com")
            ]
            
        return settings