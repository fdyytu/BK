from typing import Optional, List
from pathlib import Path
from pydantic import BaseModel, DirectoryPath, AnyHttpUrl
from .environment import EnvironmentSettings

class StorageSettings(BaseModel):
    """File storage configuration with validation"""
    
    # Storage Backend
    storage_backend: str = "local"  # local, s3, or gcs
    
    # Local Storage
    upload_dir: DirectoryPath
    serve_path: str = "/media/"
    
    # AWS S3 Settings
    aws_access_key: Optional[str] = None
    aws_secret_key: Optional[str] = None
    aws_region: Optional[str] = None
    s3_bucket: Optional[str] = None
    
    # Google Cloud Storage
    gcs_credentials_file: Optional[Path] = None
    gcs_bucket: Optional[str] = None
    
    # File Upload Settings
    max_upload_size: int = 5242880  # 5MB
    allowed_extensions: List[str] = [".jpg", ".jpeg", ".png", ".pdf"]
    
    # Image Processing
    image_max_dimension: int = 2000
    image_quality: int = 85
    thumbnail_sizes: dict = {
        "small": (100, 100),
        "medium": (300, 300),
        "large": (600, 600)
    }
    
    # CDN Settings
    use_cdn: bool = False
    cdn_url: Optional[AnyHttpUrl] = None
    
    class Config:
        env_prefix = "STORAGE_"
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "StorageSettings":
        """Create settings from environment"""
        base_dir = Path(__file__).parent.parent.parent
        
        settings = cls(
            upload_dir=base_dir / "media"
        )
        
        # Override settings based on environment
        if env.is_development:
            settings.max_upload_size = 10485760  # 10MB for development
            
        if env.is_production:
            settings.use_cdn = True
            settings.storage_backend = "s3"  # Use S3 in production
            settings.cdn_url = AnyHttpUrl("https://cdn.yourdomain.com")
            
        return settings