from enum import Enum
from typing import Dict

class ConfigMessages(Enum):
    """Configuration-related messages."""
    
    # Error messages
    INVALID_CONFIG = "Invalid configuration: {}"
    MISSING_REQUIRED = "Missing required field: {}"
    TYPE_MISMATCH = "Type mismatch for {}: expected {}, got {}"
    VALIDATION_FAILED = "Validation failed: {}"
    LOAD_ERROR = "Failed to load configuration: {}"
    SAVE_ERROR = "Failed to save configuration: {}"
    PARSE_ERROR = "Failed to parse configuration: {}"
    
    # Warning messages
    DEPRECATED_FIELD = "Field {} is deprecated, use {} instead"
    INSECURE_VALUE = "Insecure value detected for field {}"
    PERFORMANCE_WARN = "Performance warning: {}"
    
    # Info messages
    CONFIG_LOADED = "Configuration loaded successfully from {}"
    CONFIG_SAVED = "Configuration saved successfully to {}"
    OVERRIDE_APPLIED = "Override applied for {}: {}"
    FALLBACK_USED = "Using fallback value for {}: {}"
    
    def format(self, *args: str) -> str:
        """Format message with arguments."""
        return self.value.format(*args)

class ValidationMessages(Enum):
    """Validation-related messages."""
    
    INVALID_TYPE = "Invalid type for {}: expected {}, got {}"
    VALUE_REQUIRED = "Value required for field {}"
    PATTERN_MISMATCH = "Value {} does not match pattern {}"
    RANGE_ERROR = "Value {} is not in allowed range {}"
    LENGTH_ERROR = "Length of {} must be between {} and {}"
    UNIQUE_ERROR = "Value {} must be unique"
    DEPENDENCY_ERROR = "Field {} requires field {}"
    
    def format(self, *args: str) -> str:
        """Format message with arguments."""
        return self.value.format(*args)

class SecurityMessages(Enum):
    """Security-related messages."""
    
    INVALID_PERMISSION = "Invalid permission: {}"
    ACCESS_DENIED = "Access denied for {}"
    ENCRYPTION_ERROR = "Encryption failed: {}"
    DECRYPTION_ERROR = "Decryption failed: {}"
    INVALID_TOKEN = "Invalid token: {}"
    EXPIRED_TOKEN = "Token expired at {}"
    INTEGRITY_ERROR = "Integrity check failed: {}"
    
    def format(self, *args: str) -> str:
        """Format message with arguments."""
        return self.value.format(*args)

# Message metadata
MESSAGE_METADATA: Dict[Enum, Dict[str, str]] = {
    ConfigMessages.INVALID_CONFIG: {
        'level': 'ERROR',
        'code': 'CFG001',
        'category': 'Configuration'
    },
    ValidationMessages.INVALID_TYPE: {
        'level': 'ERROR',
        'code': 'VAL001',
        'category': 'Validation'
    },
    SecurityMessages.ACCESS_DENIED: {
        'level': 'ERROR',
        'code': 'SEC001',
        'category': 'Security'
    }
}