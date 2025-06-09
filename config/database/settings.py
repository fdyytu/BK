import os

# Database settings
DB_NAME = os.getenv('DB_NAME', 'application.db')
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', DB_NAME)

# Timeout settings
DB_TIMEOUT = 30

# Connection settings
DB_CHECK_SAME_THREAD = False
DB_ISOLATION_LEVEL = None  # Autocommit mode