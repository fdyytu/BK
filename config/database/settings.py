from typing import Optional
from pydantic import BaseModel, DirectoryPath, FilePath
from pathlib import Path
from .environment import EnvironmentSettings

class DatabaseSettings(BaseModel):
    """Database configuration with validation"""
    
    # Database Connection
    name: str = "application.db"
    path: Path
    timeout: int = 30
    check_same_thread: bool = False
    isolation_level: Optional[str] = None  # None for autocommit
    
    # Connection Pool
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 1800  # 30 minutes
    
    # Migration Settings
    migrations_dir: DirectoryPath
    
    class Config:
        env_prefix = "DB_"
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "DatabaseSettings":
        """Create settings from environment"""
        base_dir = Path(__file__).parent.parent.parent
        
        settings = cls(
            path=base_dir / "data" / cls.model_fields["name"].default,
            migrations_dir=base_dir / "migrations"
        )
        
        # Override settings based on environment
        if env.is_testing:
            settings.name = "test.db"
            settings.path = base_dir / "tests" / "data" / settings.name
            
        return settings