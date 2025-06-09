"""
JWT Constants
Created: 2025-06-04 16:27:17
Author: fdygt
"""

from datetime import timedelta

# JWT Configuration
JWT = {
    'ALGORITHM': 'HS256',
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'UPDATE_LAST_LOGIN': True
}

# JWT Claims
CLAIMS = {
    'ISSUER': 'your-app-name',
    'AUDIENCE': ['web', 'mobile', 'api'],
    'REQUIRED_CLAIMS': ['exp', 'iat', 'sub']
}

# Token Types
TOKEN_TYPES = {
    'ACCESS': 'access',
    'REFRESH': 'refresh',
    'RESET_PASSWORD': 'reset_password',
    'EMAIL_VERIFICATION': 'email_verification'
}

# Blacklist Configuration
BLACKLIST = {
    'ENABLED': True,
    'GRACE_PERIOD': timedelta(minutes=5),
    'CLEANUP_INTERVAL': timedelta(hours=24)
}