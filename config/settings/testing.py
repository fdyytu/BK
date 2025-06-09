from typing import Dict, Any, List
from pydantic import BaseModel, DirectoryPath
from pathlib import Path
from .environment import EnvironmentSettings

class TestDatabaseSettings(BaseModel):
    """Test database settings."""
    use_test_db: bool = True
    test_db_suffix: str = "_test"
    preserve_test_db: bool = False
    
class TestUserSettings(BaseModel):
    """Test user settings."""
    test_username: str = "test_user"
    test_password: str = "test_password"
    test_email: str = "test@example.com"
    
class TestingSettings(BaseModel):
    """Testing configuration settings."""
    
    # Test Environment
    test_env: str = "testing"
    parallel: bool = True
    workers: int = 4
    
    # Test Database
    database: TestDatabaseSettings = TestDatabaseSettings()
    
    # Test Users
    users: TestUserSettings = TestUserSettings()
    
    # Test Directories
    test_dir: DirectoryPath = Path("tests")
    fixture_dir: DirectoryPath = Path("tests/fixtures")
    
    # Test Data
    mock_external_apis: bool = True
    use_vcr_cassettes: bool = True
    
    # Coverage Settings
    coverage_enabled: bool = True
    coverage_report: str = "html"
    coverage_fail_under: float = 80.0
    coverage_exclude: List[str] = [
        "tests/*",
        "migrations/*",
        "__init__.py"
    ]
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "TestingSettings":
        """Create settings from environment."""
        if not env.is_testing:
            raise ValueError("TestingSettings can only be used in testing environment")
            
        return cls(
            parallel=env.get_env("TEST_PARALLEL", "true").lower() == "true",
            workers=int(env.get_env("TEST_WORKERS", "4")),
            coverage_fail_under=float(env.get_env("COVERAGE_FAIL_UNDER", "80.0"))
        )