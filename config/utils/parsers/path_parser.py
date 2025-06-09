from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import os
import re
from datetime import datetime

from ..abstracts.base_parser import BaseParser
from ..exceptions.validation_errors import ConfigValidationError

class PathParser(BaseParser[str, Path]):
    """
    Path parser with advanced features.
    
    Features:
    - Path normalization
    - Environment variable expansion
    - Relative path resolution
    - Path validation
    - Cross-platform compatibility
    - Security checks
    """
    
    def __init__(
        self,
        base_path: Optional[Union[str, Path]] = None,
        allow_absolute: bool = True,
        security_check: bool = True,
        create_missing: bool = False
    ) -> None:
        super().__init__()
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.allow_absolute = allow_absolute
        self.security_check = security_check
        self.create_missing = create_missing
        self._cached_paths: Dict[str, Path] = {}
        
    async def parse(self, data: str) -> Path:
        """
        Parse path string into Path object.
        
        Args:
            data: Path string to parse
            
        Returns:
            Resolved Path object
            
        Raises:
            ConfigValidationError: If path is invalid or security check fails
        """
        try:
            # Check cache
            if data in self._cached_paths:
                return self._cached_paths[data]
            
            # Expand environment variables
            expanded = os.path.expandvars(data)
            expanded = os.path.expanduser(expanded)
            
            # Create initial path
            path = Path(expanded)
            
            # Handle absolute vs relative paths
            if not path.is_absolute():
                path = self.base_path / path
            elif not self.allow_absolute:
                raise ConfigValidationError(
                    f"Absolute paths not allowed: {data}"
                )
            
            # Normalize path
            path = path.resolve()
            
            # Security check
            if self.security_check:
                self._security_check(path)
            
            # Create directories if needed
            if self.create_missing:
                self._create_dirs(path)
            
            # Cache result
            self._cached_paths[data] = path
            return path
            
        except Exception as e:
            raise ConfigValidationError(f"Failed to parse path: {str(e)}")
    
    async def serialize(self, data: Path) -> str:
        """
        Serialize Path object to string.
        
        Args:
            data: Path object to serialize
            
        Returns:
            Path string
        """
        try:
            # Try to make path relative to base_path
            try:
                return str(data.relative_to(self.base_path))
            except ValueError:
                # If that fails, return absolute path if allowed
                if self.allow_absolute:
                    return str(data)
                raise ConfigValidationError(
                    f"Cannot serialize absolute path: {data}"
                )
                
        except Exception as e:
            raise ConfigValidationError(f"Failed to serialize path: {str(e)}")
    
    def _security_check(self, path: Path) -> None:
        """
        Perform security checks on path.
        
        Args:
            path: Path to check
            
        Raises:
            ConfigValidationError: If security check fails
        """
        # Check for directory traversal attempts
        if '..' in path.parts:
            raise ConfigValidationError(
                f"Directory traversal not allowed: {path}"
            )
        
        # Check if path is within base directory
        try:
            path.relative_to(self.base_path)
        except ValueError:
            raise ConfigValidationError(
                f"Path must be within base directory: {path}"
            )
        
        # Check for suspicious file names
        suspicious_patterns = [
            r'.*\.exe$',
            r'.*\.dll$',
            r'.*\.so$',
            r'.*\.sh$',
            r'.*\.bat$'
        ]
        
        path_str = str(path)
        for pattern in suspicious_patterns:
            if re.match(pattern, path_str, re.IGNORECASE):
                raise ConfigValidationError(
                    f"Suspicious file extension detected: {path}"
                )
    
    def _create_dirs(self, path: Path) -> None:
        """
        Create missing directories in path.
        
        Args:
            path: Path to create directories for
        """
        if path.suffix:  # If path includes a file
            path.parent.mkdir(parents=True, exist_ok=True)
        else:  # If path is a directory
            path.mkdir(parents=True, exist_ok=True)