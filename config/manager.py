from typing import Dict, Type
from config.base import BaseConfig

class ConfigManager:
    """Central configuration manager"""
    
    _instance = None
    _configs: Dict[str, BaseConfig] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register(self, name: str, config: BaseConfig) -> None:
        """Register a configuration"""
        if name in self._configs:
            raise KeyError(f"Config {name} already registered")
        self._configs[name] = config
        
    def get_config(self, name: str) -> BaseConfig:
        """Get configuration by name"""
        if name not in self._configs:
            raise KeyError(f"Config {name} not found")
        return self._configs[name]
        
    def load_all(self) -> None:
        """Load all configurations"""
        for config in self._configs.values():
            config.load()
            
    def validate_all(self) -> bool:
        """Validate all configurations"""
        return all(config.validate() for config in self._configs.values())