from .environment import get_env

# Security Headers
SECURITY_HEADERS = {
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "X-Content-Type-Options": "nosniff",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

# SSL/TLS Settings
SSL_ENABLED = get_env("SSL_ENABLED", "False").lower() == "true"
SSL_CERT_FILE = get_env("SSL_CERT_FILE", "")
SSL_KEY_FILE = get_env("SSL_KEY_FILE", "")

# API Security
API_KEY_HEADER = "X-API-Key"
API_KEY_PREFIX = "sk_"
MAX_REQUEST_SIZE = 10 * 1024 * 1024  # 10MB

# Authentication Settings
AUTH_SCHEMES = ["bearer", "api_key"]
TOKEN_BLACKLIST_ENABLED = True
TOKEN_BLACKLIST_GRACE_PERIOD = 900  # 15 minutes