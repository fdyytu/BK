from typing import Dict, Optional
from pathlib import Path
from pydantic import BaseModel, DirectoryPath
from .environment import EnvironmentSettings

class LoggingSettings(BaseModel):
    """Logging configuration with validation"""
    
    # Log Paths
    log_dir: DirectoryPath
    error_log: Path
    access_log: Path
    
    # Log Levels
    default_level: str = "INFO"
    error_level: str = "ERROR"
    
    # Formatters
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    
    # Rotation Settings
    max_bytes: int = 10485760  # 10MB
    backup_count: int = 5
    
    # Extras
    json_format: bool = False
    include_correlation_id: bool = True
    
    class Config:
        env_prefix = "LOG_"
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "LoggingSettings":
        """Create settings from environment"""
        base_dir = Path(__file__).parent.parent.parent
        log_dir = base_dir / "logs"
        
        settings = cls(
            log_dir=log_dir,
            error_log=log_dir / "error.log",
            access_log=log_dir / "access.log"
        )
        
        # Override settings based on environment
        if env.is_development:
            settings.default_level = "DEBUG"
            settings.json_format = False
            
        if env.is_production:
            settings.json_format = True
            settings.backup_count = 10
            
        return settings