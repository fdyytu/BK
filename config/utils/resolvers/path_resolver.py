from typing import Dict, List, Optional, Set, Union
from pathlib import Path
import os
from datetime import datetime

from ..exceptions.loading_errors import ConfigLoadError

class PathResolver:
    """
    Advanced path resolution with caching and validation.
    
    Features:
    - Path existence validation
    - Path permission checking
    - Path normalization
    - Circular symlink detection
    - Cache with TTL
    """
    
    def __init__(
        self,
        base_path: Optional[Union[str, Path]] = None,
        cache_ttl: int = 300
    ) -> None:
        self._base_path = Path(base_path) if base_path else Path.cwd()
        self._cache_ttl = cache_ttl
        self._cache: Dict[str, tuple[Path, datetime]] = {}
        self._visited: Set[Path] = set()
    
    async def resolve(
        self,
        path: Union[str, Path],
        must_exist: bool = True,
        check_permissions: bool = True
    ) -> Path:
        """
        Resolve and validate path.
        
        Args:
            path: Path to resolve
            must_exist: Whether path must exist
            check_permissions: Whether to check permissions
            
        Returns:
            Resolved Path object
        """
        try:
            # Check cache
            cache_key = str(path)
            if cache_key in self._cache:
                cached_path, timestamp = self._cache[cache_key]
                if (datetime.utcnow() - timestamp).seconds < self._cache_ttl:
                    return cached_path
            
            # Convert to Path
            if isinstance(path, str):
                path = Path(path)
            
            # Make absolute if relative
            if not path.is_absolute():
                path = self._base_path / path
            
            # Normalize path
            resolved_path = self._resolve_path(path)
            
            # Validation
            if must_exist and not resolved_path.exists():
                raise ConfigLoadError(f"Path does not exist: {resolved_path}")
            
            if check_permissions:
                self._check_permissions(resolved_path)
            
            # Cache result
            self._cache[cache_key] = (resolved_path, datetime.utcnow())
            
            return resolved_path
            
        except Exception as e:
            raise ConfigLoadError(f"Path resolution failed: {str(e)}")
    
    def _resolve_path(self, path: Path) -> Path:
        """
        Resolve path with circular symlink detection.
        
        Args:
            path: Path to resolve
            
        Returns:
            Resolved Path
        """
        try:
            # Clear visited set for new resolution
            self._visited.clear()
            
            # Resolve path parts
            current = self._base_path
            for part in path.parts[1:] if path.is_absolute() else path.parts:
                current = current / part
                
                # Check for symlinks
                if current.is_symlink():
                    real_path = current.resolve()
                    if real_path in self._visited:
                        raise ConfigLoadError(
                            f"Circular symlink detected: {current}"
                        )
                    self._visited.add(real_path)
                    current = real_path
            
            return current.resolve()
            
        except Exception as e:
            if not isinstance(e, ConfigLoadError):
                raise ConfigLoadError(f"Path resolution failed: {str(e)}")
            raise
    
    def _check_permissions(self, path: Path) -> None:
        """
        Check path permissions.
        
        Args:
            path: Path to check
            
        Raises:
            ConfigLoadError: If permissions are insufficient
        """
        try:
            if path.exists():
                # Check read permission
                if not os.access(path, os.R_OK):
                    raise ConfigLoadError(
                        f"No read permission: {path}"
                    )
                
                # Check write permission for directories
                if path.is_dir() and not os.access(path, os.W_OK):
                    raise ConfigLoadError(
                        f"No write permission: {path}"
                    )
        except Exception as e:
            if not isinstance(e, ConfigLoadError):
                raise ConfigLoadError(f"Permission check failed: {str(e)}")
            raise