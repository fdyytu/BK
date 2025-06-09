from enum import Enum
from typing import Any, Dict
from pydantic import BaseModel, SecretStr
from functools import lru_cache
import os
from pathlib import Path
from dotenv import load_dotenv

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

class EnvironmentSettings(BaseModel):
    """Environment configuration settings."""
    
    # Environment Type
    type: EnvironmentType = EnvironmentType.DEVELOPMENT
    debug: bool = True
    testing: bool = False
    
    # Path Settings
    base_dir: Path = Path(__file__).parent.parent.parent
    logs_dir: Path = base_dir / "logs"
    temp_dir: Path = base_dir / "temp"
    uploads_dir: Path = base_dir / "uploads"
    
    # Secret Management
    secret_key: SecretStr
    encryption_key: SecretStr
    
    # Feature Flags
    features: Dict[str, bool] = {
        "maintenance_mode": False,
        "beta_features": False,
        "api_docs": True,
        "debug_toolbar": False
    }
    
    @property
    def is_development(self) -> bool:
        return self.type == EnvironmentType.DEVELOPMENT
    
    @property
    def is_production(self) -> bool:
        return self.type == EnvironmentType.PRODUCTION
    
    @property
    def is_testing(self) -> bool:
        return self.type == EnvironmentType.TESTING
    
    @property
    def is_staging(self) -> bool:
        return self.type == EnvironmentType.STAGING
    
    def get_feature_flag(self, feature: str) -> bool:
        """Get feature flag value."""
        return self.features.get(feature, False)
    
    @classmethod
    def load_env(cls) -> "EnvironmentSettings":
        """Load environment settings from .env file."""
        load_dotenv()
        
        return cls(
            type=EnvironmentType(os.getenv("ENV", "development")),
            debug=os.getenv("DEBUG", "True").lower() == "true",
            testing=os.getenv("TESTING", "False").lower() == "true",
            secret_key=SecretStr(os.getenv("SECRET_KEY", "your-secret-key")),
            encryption_key=SecretStr(os.getenv("ENCRYPTION_KEY", "your-encryption-key"))
        )

@lru_cache()
def get_environment() -> EnvironmentSettings:
    """Get cached environment settings."""
    return EnvironmentSettings.load_env()