from typing import List, Optional
from datetime import timedelta
from pydantic import BaseModel, SecretStr
from enum import Enum
from .environment import EnvironmentSettings

class AuthProvider(str, Enum):
    LOCAL = "local"
    OAUTH = "oauth"
    JWT = "jwt"
    SESSION = "session"

class OAuthSettings(BaseModel):
    """OAuth provider settings."""
    enabled: bool = False
    client_id: str = ""
    client_secret: SecretStr
    authorize_url: str = ""
    token_url: str = ""
    userinfo_url: str = ""
    redirect_uri: str = ""
    scope: List[str] = ["email", "profile"]

class JWTSettings(BaseModel):
    """JWT authentication settings."""
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire: timedelta = timedelta(minutes=15)
    refresh_token_expire: timedelta = timedelta(days=7)
    token_type: str = "Bearer"
    blacklist_enabled: bool = True
    blacklist_grace_period: timedelta = timedelta(minutes=1)

class SessionSettings(BaseModel):
    """Session authentication settings."""
    secret_key: SecretStr
    session_cookie: str = "session"
    permanent_session: bool = True
    session_lifetime: timedelta = timedelta(days=1)
    secure_cookie: bool = True
    httponly: bool = True
    samesite: str = "lax"
    
class PasswordSettings(BaseModel):
    """Password policy settings."""
    min_length: int = 8
    max_length: int = 72
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digit: bool = True
    require_special: bool = True
    password_history: int = 3
    max_attempts: int = 5
    lockout_duration: timedelta = timedelta(minutes=15)

class AuthSettings(BaseModel):
    """Authentication settings configuration."""
    
    provider: AuthProvider = AuthProvider.JWT
    oauth: OAuthSettings
    jwt: JWTSettings
    session: SessionSettings
    password: PasswordSettings
    
    # MFA Settings
    mfa_enabled: bool = False
    mfa_issuer: str = "MyApp"
    mfa_digits: int = 6
    mfa_interval: int = 30
    
    # Token Settings
    verify_email_token_expire: timedelta = timedelta(days=1)
    reset_password_token_expire: timedelta = timedelta(hours=1)
    
    # Session Management
    max_sessions: int = 5
    revoke_old_sessions: bool = True
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "AuthSettings":
        """Create settings from environment."""
        return cls(
            provider=AuthProvider(env.get_env("AUTH_PROVIDER", "jwt")),
            oauth=OAuthSettings(
                enabled=env.get_env("OAUTH_ENABLED", "false").lower() == "true",
                client_id=env.get_env("OAUTH_CLIENT_ID", ""),
                client_secret=SecretStr(env.get_env("OAUTH_CLIENT_SECRET", "")),
            ),
            jwt=JWTSettings(
                secret_key=env.secret_key,
                access_token_expire=timedelta(
                    minutes=int(env.get_env("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
                )
            ),
            session=SessionSettings(
                secret_key=env.secret_key,
                secure_cookie=env.is_production
            ),
            password=PasswordSettings()
        )