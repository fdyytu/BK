"""
Message Constants
Author: fdygt
Created: 2025-06-04 16:24:30
"""

# Success Messages
SUCCESS = {
    'CREATED': 'Resource created successfully',
    'UPDATED': 'Resource updated successfully',
    'DELETED': 'Resource deleted successfully',
    'FETCHED': 'Resource fetched successfully',
    'PROCESSED': 'Request processed successfully'
}

# Error Messages
ERROR = {
    'NOT_FOUND': 'Resource not found',
    'BAD_REQUEST': 'Invalid request parameters',
    'UNAUTHORIZED': 'Unauthorized access',
    'FORBIDDEN': 'Access forbidden',
    'VALIDATION': 'Validation error occurred',
    'DATABASE': 'Database error occurred',
    'SERVER': 'Internal server error',
    'TIMEOUT': 'Request timeout',
    'DUPLICATE': 'Resource already exists'
}

# Validation Messages
VALIDATION = {
    'REQUIRED': '{field} is required',
    'MIN_LENGTH': '{field} must be at least {min} characters',
    'MAX_LENGTH': '{field} must not exceed {max} characters',
    'INVALID_EMAIL': 'Invalid email format',
    'INVALID_DATE': 'Invalid date format',
    'INVALID_PHONE': 'Invalid phone number format',
    'PASSWORD_MISMATCH': 'Passwords do not match',
    'WEAK_PASSWORD': 'Password does not meet security requirements'
}

# Authentication Messages
AUTH = {
    'LOGIN_SUCCESS': 'Login successful',
    'LOGIN_FAILED': 'Invalid credentials',
    'LOGOUT_SUCCESS': 'Logout successful',
    'TOKEN_EXPIRED': 'Token has expired',
    'TOKEN_INVALID': 'Invalid token',
    'ACCOUNT_LOCKED': 'Account has been locked',
    'PASSWORD_RESET': 'Password reset instructions sent'
}

# Email Messages
EMAIL = {
    'WELCOME': 'Welcome to {app_name}',
    'VERIFY_EMAIL': 'Please verify your email address',
    'PASSWORD_RESET': 'Password reset request',
    'ACCOUNT_LOCKED': 'Your account has been locked',
    'NOTIFICATION': 'New notification from {app_name}'
}