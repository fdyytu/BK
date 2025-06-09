from typing import Dict, Any
from .environment import get_env

# Application Settings
APP_NAME = get_env("APP_NAME", "My API")
APP_VERSION = get_env("APP_VERSION", "1.0.0")
DEBUG = get_env("DEBUG", "False").lower() == "true"
API_PREFIX = "/api/v1"

# Server Settings
HOST = get_env("HOST", "0.0.0.0")
PORT = int(get_env("PORT", "8000"))
WORKERS = int(get_env("WORKERS", "4"))

# Response Settings
DEFAULT_RESPONSES: Dict[str, Any] = {
    "success": True,
    "message": "",
    "data": None
}

# Rate Limiting
RATE_LIMIT = {
    "requests": int(get_env("RATE_LIMIT_REQUESTS", "100")),
    "period": int(get_env("RATE_LIMIT_PERIOD", "3600"))
}

# Pagination
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100