from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from enum import Enum
from datetime import time, timedelta
from pathlib import Path
from .environment import EnvironmentSettings

class BackupProvider(str, Enum):
    LOCAL = "local"
    S3 = "s3"
    GCS = "gcs"
    AZURE = "azure"

class BackupType(str, Enum):
    FULL = "full"
    INCREMENTAL = "incremental"

class RetentionPolicy(BaseModel):
    """Backup retention configuration."""
    daily_backups: int = 7
    weekly_backups: int = 4
    monthly_backups: int = 6
    yearly_backups: int = 1

class S3Settings(BaseModel):
    """AWS S3 backup settings."""
    bucket: str
    access_key: str
    secret_key: str
    region: str = "us-east-1"
    
class GCSSettings(BaseModel):
    """Google Cloud Storage settings."""
    bucket: str
    credentials_file: Path
    project_id: str
    
class AzureSettings(BaseModel):
    """Azure Blob Storage settings."""
    container: str
    connection_string: str

class BackupSettings(BaseModel):
    """Backup configuration settings."""
    
    enabled: bool = True
    provider: BackupProvider = BackupProvider.LOCAL
    
    # Backup Schedule
    schedule_enabled: bool = True
    schedule_time: time = time(hour=1, minute=0)  # 1 AM
    backup_type: BackupType = BackupType.FULL
    
    # Local Backup Settings
    backup_dir: Path = Path("backups")
    compression_enabled: bool = True
    compression_type: str = "gzip"
    
    # Retention Settings
    retention: RetentionPolicy = RetentionPolicy()
    
    # Encryption Settings
    encryption_enabled: bool = True
    encryption_key: Optional[str] = None
    
    # Provider Specific Settings
    s3: Optional[S3Settings]
    gcs: Optional[GCSSettings]
    azure: Optional[AzureSettings]
    
    # Notification Settings
    notify_on_success: bool = True
    notify_on_failure: bool = True
    notification_channels: List[str] = ["email"]
    
    # Performance Settings
    max_concurrent_uploads: int = 4
    chunk_size: int = 8 * 1024 * 1024  # 8MB
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "BackupSettings":
        """Create settings from environment."""
        provider = BackupProvider(env.get_env("BACKUP_PROVIDER", "local"))
        settings = cls(
            enabled=env.get_env("BACKUP_ENABLED", "true").lower() == "true",
            provider=provider,
            encryption_enabled=env.is_production
        )
        
        if provider == BackupProvider.S3:
            settings.s3 = S3Settings(
                bucket=env.get_env("BACKUP_S3_BUCKET"),
                access_key=env.get_env("AWS_ACCESS_KEY"),
                secret_key=env.get_env("AWS_SECRET_KEY")
            )
            
        return settings