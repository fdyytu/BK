"""
Application Constants
Author: fdygt
Created: 2025-06-04 16:23:39
"""

from typing import Dict, Any

# Application Information
APP_NAME = "My API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Professional REST API"
APP_AUTHOR = "fdygt"

# Environment Settings
ENVIRONMENT = {
    'DEVELOPMENT': 'development',
    'STAGING': 'staging',
    'PRODUCTION': 'production',
    'TESTING': 'testing'
}

# API Settings
API = {
    'VERSION': 'v1',
    'PREFIX': '/api',
    'TIMEOUT': 30,  # seconds
    'MAX_PAGE_SIZE': 100,
    'DEFAULT_PAGE_SIZE': 10
}

# Response Status Codes
STATUS = {
    'SUCCESS': 200,
    'CREATED': 201,
    'ACCEPTED': 202,
    'NO_CONTENT': 204,
    'BAD_REQUEST': 400,
    'UNAUTHORIZED': 401,
    'FORBIDDEN': 403,
    'NOT_FOUND': 404,
    'METHOD_NOT_ALLOWED': 405,
    'CONFLICT': 409,
    'UNPROCESSABLE_ENTITY': 422,
    'TOO_MANY_REQUESTS': 429,
    'SERVER_ERROR': 500,
    'SERVICE_UNAVAILABLE': 503
}

# Default Response Format
DEFAULT_RESPONSE: Dict[str, Any] = {
    'success': True,
    'message': '',
    'data': None,
    'errors': None,
    'meta': {
        'timestamp': '',
        'api_version': API['VERSION']
    }
}

# Content Types
CONTENT_TYPE = {
    'JSON': 'application/json',
    'FORM': 'application/x-www-form-urlencoded',
    'MULTIPART': 'multipart/form-data',
    'TEXT': 'text/plain',
    'HTML': 'text/html'
}

# Supported Languages
LANGUAGES = {
    'EN': 'en',
    'ES': 'es',
    'ID': 'id'
}

# Time Constants
TIME = {
    'SECOND': 1,
    'MINUTE': 60,
    'HOUR': 3600,
    'DAY': 86400,
    'WEEK': 604800,
    'MONTH': 2592000  # 30 days
}