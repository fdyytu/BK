"""
HTTP Headers Constants
Author: fdygt
Created: 2025-06-04 16:25:57
"""

# Standard HTTP Headers
HEADERS = {
    'ACCEPT': 'Accept',
    'ACCEPT_ENCODING': 'Accept-Encoding',
    'AUTHORIZATION': 'Authorization',
    'CACHE_CONTROL': 'Cache-Control',
    'CONTENT_TYPE': 'Content-Type',
    'ORIGIN': 'Origin',
    'USER_AGENT': 'User-Agent',
    'X_REQUEST_ID': 'X-Request-ID'
}

# Security Headers
SECURITY_HEADERS = {
    'CONTENT_SECURITY_POLICY': 'Content-Security-Policy',
    'STRICT_TRANSPORT_SECURITY': 'Strict-Transport-Security',
    'X_CONTENT_TYPE_OPTIONS': 'X-Content-Type-Options',
    'X_FRAME_OPTIONS': 'X-Frame-Options',
    'X_XSS_PROTECTION': 'X-XSS-Protection'
}

# Custom Headers
CUSTOM_HEADERS = {
    'X_API_KEY': 'X-API-Key',
    'X_CLIENT_ID': 'X-Client-ID',
    'X_DEVICE_ID': 'X-Device-ID',
    'X_CORRELATION_ID': 'X-Correlation-ID'
}