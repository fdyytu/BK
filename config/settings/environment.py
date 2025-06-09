import os
from typing import Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_env(key: str, default: Any = None) -> str:
    """Get environment variable value
    
    Args:
        key (str): Environment variable key
        default (Any, optional): Default value if key not found
        
    Returns:
        str: Environment variable value
    """
    return os.getenv(key, default)

# Environment Type
ENV = get_env("ENV", "development")
IS_DEVELOPMENT = ENV == "development"
IS_PRODUCTION = ENV == "production"
IS_TESTING = ENV == "testing"