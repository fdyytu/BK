"""
Application Constants
Author: fdygt
Created: 2025-06-04 16:23:39
Updated: 2025-06-09 14:22:34
"""

from typing import Dict, Any
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = 'development'
    STAGING = 'staging'
    PRODUCTION = 'production'
    TESTING = 'testing'

class ContentType(str, Enum):
    JSON = 'application/json'
    FORM = 'application/x-www-form-urlencoded'
    MULTIPART = 'multipart/form-data'
    TEXT = 'text/plain'
    HTML = 'text/html'

class Language(str, Enum):
    EN = 'en'
    ES = 'es'
    ID = 'id'

class HttpStatus:
    SUCCESS = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503

# API Information
API_INFO = {
    'NAME': "Digital Product & PPOB API",
    'VERSION': 'v1',
    'PREFIX': '/api',
    'TIMEOUT': 30,
    'MAX_PAGE_SIZE': 100,
    'DEFAULT_PAGE_SIZE': 10
}

# Time Constants (in seconds)
class Time:
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800
    MONTH = 2592000  # 30 days
    YEAR = 31536000  # 365 days

# Default Response Format
DEFAULT_RESPONSE: Dict[str, Any] = {
    'success': True,
    'message': '',
    'data': None,
    'errors': None,
    'meta': {
        'timestamp': '',
        'api_version': API_INFO['VERSION'],
        'request_id': ''
    }
}

# Regular Expressions
REGEX = {
    'EMAIL': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'PHONE': r'^\+?[\d\s-]{10,}$',
    'PASSWORD': r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$'
}