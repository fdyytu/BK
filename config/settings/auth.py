from datetime import timedelta
from .environment import get_env

# JWT Settings
JWT_SECRET_KEY = get_env("JWT_SECRET_KEY", "your-secret-key")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE = timedelta(minutes=30)
JWT_REFRESH_TOKEN_EXPIRE = timedelta(days=7)

# Password Settings
PASSWORD_MIN_LENGTH = 8
PASSWORD_SCHEMES = ["bcrypt"]
PASSWORD_HASH_ROUNDS = 12

# Session Settings
SESSION_LIFETIME = timedelta(days=1)
SESSION_COOKIE_NAME = "session_id"