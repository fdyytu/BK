from .base import *

# Secure settings
DEBUG = False
SECRET_KEY = os.getenv("SECRET_KEY")

# Production database
DATABASE_CONFIG = {
    "ENGINE": "postgresql",
    "NAME": os.getenv("DB_NAME"),
    "USER": os.getenv("DB_USER"),
    "PASSWORD": os.getenv("DB_PASSWORD"),
    "HOST": os.getenv("DB_HOST"),
    "PORT": os.getenv("DB_PORT")
}

# Production logging
LOGGING["handlers"]["file"] = {
    "class": "logging.FileHandler",
    "filename": "/var/log/app/prod.log"
}