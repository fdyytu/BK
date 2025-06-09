"""
Default Value Constants
Created: 2025-06-04 16:27:17
Author: fdygt
"""

from datetime import timedelta
from typing import Dict, Any

# Application Defaults
APP_DEFAULTS: Dict[str, Any] = {
    'TIMEZONE': 'UTC',
    'LANGUAGE': 'en',
    'CURRENCY': 'USD',
    'PAGE_SIZE': 20,
    'MAX_UPLOAD_SIZE': 10 * 1024 * 1024  # 10MB
}

# Security Defaults
SECURITY_DEFAULTS = {
    'PASSWORD_MIN_LENGTH': 8,
    'PASSWORD_MAX_LENGTH': 128,
    'SESSION_TIMEOUT': timedelta(hours=24),
    'LOGIN_ATTEMPTS': 3,
    'LOCKOUT_DURATION': timedelta(minutes=15)
}

# Cache Defaults
CACHE_DEFAULTS = {
    'TIMEOUT': 300,  # 5 minutes
    'KEY_PREFIX': 'myapp',
    'VERSION': 1,
    'NULL_TIMEOUT': 60  # 1 minute
}

# API Defaults
API_DEFAULTS = {
    'VERSION': 'v1',
    'TIMEOUT': 30,  # seconds
    'RATE_LIMIT': 100,  # requests per minute
    'MAX_PAGE_SIZE': 100
}