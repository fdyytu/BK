# Middleware Settings
MIDDLEWARE = [
    "middleware.cors.CORSMiddleware",
    "middleware.auth.AuthenticationMiddleware",
    "middleware.security.SecurityHeadersMiddleware",
    "middleware.logging.RequestLoggingMiddleware",
    "middleware.error.ErrorHandlingMiddleware"
]

# Middleware Configuration
MIDDLEWARE_CONFIG = {
    "TIMEOUT": 30,
    "EXEMPT_PATHS": ["/health", "/metrics"],
    "RATE_LIMIT_PATHS": ["/api/*"]
}