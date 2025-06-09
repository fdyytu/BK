from typing import Dict, Any, Optional
from pydantic import BaseModel, PostgresDsn, RedisDsn, validator
from enum import Enum
from pathlib import Path
from .environment import EnvironmentSettings

class DatabaseType(str, Enum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"

class DatabaseSettings(BaseModel):
    """Database configuration settings."""
    
    # Database Type
    type: DatabaseType = DatabaseType.POSTGRESQL
    
    # Connection Settings
    host: str = "localhost"
    port: int = 5432
    username: str = "postgres"
    password: str = "postgres"
    database: str = "myapp"
    
    # Connection URL
    url: Optional[PostgresDsn] = None
    
    # Pool Settings
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 1800
    
    # Query Settings
    echo: bool = False
    echo_pool: bool = False
    
    # Migration Settings
    auto_migrate: bool = True
    migration_dir: Path = Path("migrations")
    
    # SQLite Settings
    sqlite_path: Optional[Path] = None
    sqlite_pragma: Dict[str, Any] = {
        "journal_mode": "wal",
        "cache_size": -1 * 64000,
        "foreign_keys": "ON",
        "synchronous": "NORMAL"
    }
    
    # PostgreSQL Settings
    pg_schema: str = "public"
    pg_extensions: list = ["uuid-ossp", "pgcrypto"]
    
    # Connection Retry Settings
    retry_limit: int = 3
    retry_interval: int = 5
    
    @validator("url", pre=True)
    def assemble_db_url(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """Assemble database URL from components."""
        if isinstance(v, str):
            return v
            
        if values.get("type") == DatabaseType.SQLITE:
            sqlite_path = values.get("sqlite_path") or Path("db.sqlite3")
            return f"sqlite:///{sqlite_path}"
            
        return PostgresDsn.build(
            scheme=values.get("type"),
            user=values.get("username"),
            password=values.get("password"),
            host=values.get("host"),
            port=str(values.get("port")),
            path=f"/{values.get('database')}"
        )
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "DatabaseSettings":
        """Create settings from environment."""
        settings = cls(
            type=DatabaseType(env.get_env("DB_TYPE", "postgresql")),
            host=env.get_env("DB_HOST", "localhost"),
            port=int(env.get_env("DB_PORT", "5432")),
            username=env.get_env("DB_USER", "postgres"),
            password=env.get_env("DB_PASSWORD", "postgres"),
            database=env.get_env("DB_NAME", "myapp"),
            pool_size=int(env.get_env("DB_POOL_SIZE", "5")),
            echo=env.is_development,
            auto_migrate=env.is_development
        )
        
        if settings.type == DatabaseType.SQLITE:
            settings.sqlite_path = Path(env.get_env("DB_FILE", "db.sqlite3"))
            
        return settings