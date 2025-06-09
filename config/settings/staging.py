from .base import *

DEBUG = False
SECRET_KEY = os.getenv("STAGING_SECRET_KEY")

# Staging database
DATABASE_CONFIG = {
    "ENGINE": "postgresql",
    "NAME": "staging_db",
    "USER": os.getenv("STAGING_DB_USER"),
    "PASSWORD": os.getenv("STAGING_DB_PASSWORD")
}