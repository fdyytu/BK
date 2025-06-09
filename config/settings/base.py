# Base settings yang digunakan di semua environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Default settings
DEBUG = False
SECRET_KEY = "your-secret-key"

# Database default
DATABASE_CONFIG = {
    "ENGINE": "sqlite3",
    "NAME": "db.sqlite3"
}

# Cache settings
CACHE_TIMEOUT = 300  # 5 minutes

# Logging basic config
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    }
}