from typing import Any, TypeVar, Type
from pathlib import Path
import yaml
import json
import toml

T = TypeVar('T')

def load_config_file(path: Path, config_type: Type[T]) -> T:
    """Load and validate configuration file"""
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
        
    content = path.read_text()
    
    if path.suffix == '.yaml':
        data = yaml.safe_load(content)
    elif path.suffix == '.json':
        data = json.loads(content)
    elif path.suffix == '.toml':
        data = toml.loads(content)
    else:
        raise ValueError(f"Unsupported config format: {path.suffix}")
        
    return config_type.parse_obj(data)

def merge_configs(*configs: dict[str, Any]) -> dict[str, Any]:
    """Deep merge multiple configuration dictionaries"""
    result = {}
    
    for config in configs:
        for key, value in config.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_configs(result[key], value)
            else:
                result[key] = value
                
    return result