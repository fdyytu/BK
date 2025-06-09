from typing import Any, Dict, List, Optional, Pattern
import re
from copy import deepcopy

class ConfigMasking:
    """
    Configuration value masking with advanced features.
    
    Features:
    - Pattern-based masking
    - Custom masking rules
    - Nested object support
    - Selective field masking
    - Masking preservation
    """
    
    def __init__(
        self,
        mask_char: str = '*',
        preserve_length: bool = True,
        sensitive_fields: Optional[List[str]] = None
    ) -> None:
        self._mask_char = mask_char
        self._preserve_length = preserve_length
        self._sensitive_fields = sensitive_fields or [
            'password', 'secret', 'key', 'token', 'auth',
            'credential', 'private', 'certificate'
        ]
        self._patterns: Dict[str, Pattern] = {}
        self._compile_patterns()
    
    def mask_value(self, value: str, field_name: str = '') -> str:
        """
        Mask a single value based on field name or content.
        
        Args:
            value: Value to mask
            field_name: Optional field name for context
            
        Returns:
            Masked value
        """
        if not isinstance(value, str):
            return value
            
        # Check if field name indicates sensitive data
        if any(sensitive in field_name.lower() 
               for sensitive in self._sensitive_fields):
            return self._apply_mask(value)
        
        # Check against patterns
        for pattern in self._patterns.values():
            if pattern.search(value):
                return self._apply_mask(value)
        
        return value
    
    def mask_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mask sensitive values in configuration.
        
        Args:
            config: Configuration to mask
            
        Returns:
            Configuration with masked values
        """
        masked = deepcopy(config)
        
        def _mask_dict(d: Dict[str, Any]) -> None:
            for key, value in d.items():
                if isinstance(value, dict):
                    _mask_dict(value)
                elif isinstance(value, (list, tuple)):
                    d[key] = [
                        self.mask_value(v, key) if isinstance(v, str)
                        else v for v in value
                    ]
                elif isinstance(value, str):
                    d[key] = self.mask_value(value, key)
        
        _mask_dict(masked)
        return masked
    
    def add_pattern(self, name: str, pattern: str) -> None:
        """
        Add custom masking pattern.
        
        Args:
            name: Pattern name
            pattern: Regex pattern
        """
        self._patterns[name] = re.compile(pattern)
    
    def _compile_patterns(self) -> None:
        """Compile default masking patterns."""
        default_patterns = {
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'phone': r'\b\+?1?\d{9,15}\b'
        }
        
        for name, pattern in default_patterns.items():
            self.add_pattern(name, pattern)
    
    def _apply_mask(self, value: str) -> str:
        """Apply masking to value."""
        if not value:
            return value
            
        if self._preserve_length:
            return self._mask_char * len(value)
        
        # Show first and last character
        if len(value) <= 4:
            return self._mask_char * len(value)
        return f"{value[0]}{self._mask_char * (len(value)-2)}{value[-1]}"