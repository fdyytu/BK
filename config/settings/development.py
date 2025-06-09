from .base import *

# Override base settings
DEBUG = True
SECRET_KEY = "dev-secret-key"

# Development database
DATABASE_CONFIG = {
    "ENGINE": "sqlite3",
    "NAME": "dev.sqlite3"
}

# More detailed logging
LOGGING["handlers"]["file"] = {
    "class": "logging.FileHandler",
    "filename": "dev.log"
}