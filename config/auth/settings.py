from typing import List, Optional
from datetime import timedelta
from pydantic import BaseModel, SecretStr

class AuthSettings(BaseModel):
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire: timedelta = timedelta(minutes=15)
    refresh_token_expire: timedelta = timedelta(days=7)
    
    password_min_length: int = 8
    password_max_length: int = 72
    password_require_uppercase: bool = True
    password_require_lowercase: bool = True
    password_require_digit: bool = True
    password_require_special: bool = True
    
    allowed_roles: List[str] = ["admin", "user", "guest"]
    default_role: str = "user"
    super_admin_role: str = "admin"