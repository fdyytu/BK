from typing import List
from .environment import get_env

# CORS Settings
CORS_ORIGINS: List[str] = get_env("CORS_ORIGINS", "*").split(",")
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
CORS_HEADERS = ["*"]
CORS_CREDENTIALS = True