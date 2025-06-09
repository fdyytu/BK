from .environment import get_env

# Email Server Settings
SMTP_HOST = get_env("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(get_env("SMTP_PORT", "587"))
SMTP_USERNAME = get_env("SMTP_USERNAME", "")
SMTP_PASSWORD = get_env("SMTP_PASSWORD", "")
SMTP_USE_TLS = True

# Email Content Settings
EMAIL_SENDER_NAME = get_env("EMAIL_SENDER_NAME", "My API")
EMAIL_SENDER_ADDRESS = get_env("EMAIL_SENDER_ADDRESS", "noreply@myapi.com")
EMAIL_TEMPLATES_DIR = "templates/email"

# Email Timeout Settings
EMAIL_TIMEOUT = 30  # seconds
EMAIL_RETRY_COUNT = 3