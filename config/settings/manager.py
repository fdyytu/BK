from typing import Dict, Type, TypeVar
from pydantic import BaseModel
from .environment import EnvironmentSettings
from .app import AppSettings
from .auth import AuthSettings

T = TypeVar("T", bound=BaseModel)

class SettingsManager:
    """Central settings manager to avoid duplication"""
    
    def __init__(self):
        self._env = EnvironmentSettings()
        self._settings: Dict[Type[BaseModel], BaseModel] = {}
        
    @property
    def environment(self) -> EnvironmentSettings:
        return self._env
        
    def get(self, settings_type: Type[T]) -> T:
        """Get settings by type"""
        if settings_type not in self._settings:
            self._settings[settings_type] = settings_type.from_env(self._env)
        return self._settings[settings_type]
    
    @property  
    def app(self) -> AppSettings:
        return self.get(AppSettings)
        
    @property
    def auth(self) -> AuthSettings:
        return self.get(AuthSettings)

# Global settings instance
settings = SettingsManager()