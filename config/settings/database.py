from pathlib import Path
from .environment import get_env

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Database Settings
DB_FILE = get_env("DB_FILE", "db.sqlite3")
DB_PATH = BASE_DIR / DB_FILE

# SQLite Database URL
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Additional Settings
DB_ECHO = get_env("DB_ECHO", "False").lower() == "true"  # SQL query logging
DB_POOL_SIZE = int(get_env("DB_POOL_SIZE", "5"))
DB_MAX_OVERFLOW = int(get_env("DB_MAX_OVERFLOW", "10"))

# SQLite specific settings
SQLITE_PRAGMA = {
    "journal_mode": "wal",  # Write-Ahead Logging for better concurrency
    "cache_size": -1 * 64000,  # 64MB cache size
    "foreign_keys": "ON",  # Enable foreign key constraint checking
    "synchronous": "NORMAL"  # Safe but faster synchronization mode
}