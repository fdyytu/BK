# Database Configuration Constants
DEFAULT_DB_NAME = "application.db"
MAX_CONNECTIONS = 100
TIMEOUT = 30
RETRY_COUNT = 3

# Query Constants
MAX_QUERY_EXECUTION_TIME = 30  # seconds
BATCH_SIZE = 1000

# SQLite Specific Constants
SQLITE_PRAGMA = {
    "foreign_keys": "ON",
    "journal_mode": "WAL",
    "synchronous": "NORMAL",
    "cache_size": -64000,  # 64MB
    "temp_store": "MEMORY"
}

# Table Names
USER_TABLE = "users"
PROFILE_TABLE = "profiles"
LOG_TABLE = "logs"

# Column Types
COLUMN_TYPES = {
    "TEXT": "TEXT",
    "INTEGER": "INTEGER",
    "REAL": "REAL",
    "BLOB": "BLOB",
    "NULL": "NULL",
    "BOOLEAN": "INTEGER",  # SQLite tidak punya tipe boolean native
    "TIMESTAMP": "TEXT"    # Untuk timestamp dalam format ISO
}