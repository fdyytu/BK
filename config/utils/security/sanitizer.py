from typing import Any, Dict, List, Optional, Set, Union
import re
from html import escape
import bleach
from datetime import datetime

class ConfigSanitizer:
    """
    Advanced configuration value sanitizer.
    
    Features:
    - HTML escaping
    - SQL injection prevention
    - Command injection prevention
    - Path traversal prevention
    - Custom sanitization rules
    """
    
    def __init__(
        self,
        html_escape: bool = True,
        allow_html_tags: Optional[List[str]] = None,
        strip_comments: bool = True
    ) -> None:
        self.html_escape = html_escape
        self.allow_html_tags = allow_html_tags or []
        self.strip_comments = strip_comments
        
        # Compile patterns
        self._sql_pattern = re.compile(
            r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER)\b)|(-{2})',
            re.IGNORECASE
        )
        self._traversal_pattern = re.compile(r'\.{2}[/\\]')
        self._command_pattern = re.compile(
            r'[;&|`]|(\$\()|(\b(eval|exec)\b)',
            re.IGNORECASE
        )
    
    def sanitize(self, data: Any) -> Any:
        """
        Sanitize configuration value.
        
        Args:
            data: Value to sanitize
            
        Returns:
            Sanitized value
        """
        if isinstance(data, dict):
            return {k: self.sanitize(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.sanitize(v) for v in data]
        elif isinstance(data, str):
            return self._sanitize_string(data)
        else:
            return data
    
    def _sanitize_string(self, value: str) -> str:
        """
        Sanitize string value.
        
        Args:
            value: String to sanitize
            
        Returns:
            Sanitized string
        """
        # Strip comments
        if self.strip_comments:
            value = self._strip_comments(value)
        
        # Prevent SQL injection
        if self._sql_pattern.search(value):
            value = self._sql_pattern.sub('', value)
        
        # Prevent path traversal
        if self._traversal_pattern.search(value):
            value = self._traversal_pattern.sub('', value)
        
        # Prevent command injection
        if self._command_pattern.search(value):
            value = self._command_pattern.sub('', value)
        
        # HTML escaping
        if self.html_escape:
            if self.allow_html_tags:
                # Use bleach for selective HTML escaping
                value = bleach.clean(
                    value,
                    tags=self.allow_html_tags,
                    strip=True
                )
            else:
                # Escape all HTML
                value = escape(value)
        
        return value
    
    def _strip_comments(self, value: str) -> str:
        """
        Strip comments from string.
        
        Args:
            value: String to process
            
        Returns:
            String without comments
        """
        # Remove single-line comments
        value = re.sub(r'//.*$', '', value, flags=re.MULTILINE)
        
        # Remove multi-line comments
        value = re.sub(r'/\*.*?\*/', '', value, flags=re.DOTALL)
        
        # Remove hash comments
        value = re.sub(r'#.*$', '', value, flags=re.MULTILINE)
        
        return value.strip()