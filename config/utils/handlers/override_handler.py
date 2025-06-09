from typing import Any, Dict, List, Optional, Set
from abc import ABC, abstractmethod
from datetime import datetime
import logging

class OverrideSource(ABC):
    """Abstract base class for override sources following ISP."""
    
    @abstractmethod
    async def get_overrides(self) -> Dict[str, Any]:
        """Get all overrides from source."""
        pass
    
    @abstractmethod
    async def set_override(self, key: str, value: Any) -> None:
        """Set override value in source."""
        pass

class EnvironmentOverride(OverrideSource):
    """Override source using environment variables."""
    
    def __init__(self, prefix: str = 'OVERRIDE_') -> None:
        self.prefix = prefix
        self._logger = logging.getLogger(__name__)
    
    async def get_overrides(self) -> Dict[str, Any]:
        """Get overrides from environment variables."""
        import os
        overrides = {}
        for key, value in os.environ.items():
            if key.startswith(self.prefix):
                config_key = key[len(self.prefix):].lower()
                overrides[config_key] = value
        return overrides
    
    async def set_override(self, key: str, value: Any) -> None:
        """Set override in environment."""
        import os
        env_key = f"{self.prefix}{key.upper()}"
        os.environ[env_key] = str(value)

class FileOverride(OverrideSource):
    """Override source using file storage."""
    
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self._logger = logging.getLogger(__name__)
    
    async def get_overrides(self) -> Dict[str, Any]:
        """Get overrides from file."""
        try:
            import json
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self._logger.error(f"Failed to load overrides: {e}")
            return {}
    
    async def set_override(self, key: str, value: Any) -> None:
        """Set override in file."""
        try:
            import json
            overrides = await self.get_overrides()
            overrides[key] = value
            with open(self.file_path, 'w') as f:
                json.dump(overrides, f, indent=2)
        except Exception as e:
            self._logger.error(f"Failed to set override: {e}")

class OverrideMetadata:
    """Metadata for configuration overrides."""
    
    def __init__(
        self,
        value: Any,
        source: str,
        timestamp: datetime,
        user: str,
        reason: Optional[str] = None
    ) -> None:
        self.value = value
        self.source = source
        self.timestamp = timestamp
        self.user = user
        self.reason = reason

class OverrideHandler:
    """Handler for managing configuration overrides following SRP."""
    
    def __init__(
        self,
        sources: Optional[List[OverrideSource]] = None,
        track_history: bool = True,
        max_history: int = 100
    ) -> None:
        self._sources = sources or []
        self._track_history = track_history
        self._max_history = max_history
        self._overrides: Dict[str, OverrideMetadata] = {}
        self._history: Dict[str, List[OverrideMetadata]] = {}
        self._logger = logging.getLogger(__name__)
    
    async def get_override(
        self,
        key: str,
        default: Any = None
    ) -> Optional[Any]:
        """Get override value for key."""
        # Check current overrides
        if key in self._overrides:
            return self._overrides[key].value
        
        # Check sources
        for source in self._sources:
            overrides = await source.get_overrides()
            if key in overrides:
                value = overrides[key]
                await self.set_override(
                    key,
                    value,
                    source=source.__class__.__name__
                )
                return value
        
        return default
    
    async def set_override(
        self,
        key: str,
        value: Any,
        source: str,
        reason: Optional[str] = None
    ) -> None:
        """Set override value with metadata."""
        metadata = OverrideMetadata(
            value=value,
            source=source,
            timestamp=datetime.utcnow(),
            user="fdyytu",
            reason=reason
        )
        
        # Update current override
        self._overrides[key] = metadata
        
        # Update history if enabled
        if self._track_history:
            if key not in self._history:
                self._history[key] = []
            self._history[key].append(metadata)
            
            # Trim history if needed
            if len(self._history[key]) > self._max_history:
                self._history[key] = self._history[key][-self._max_history:]
        
        # Update sources
        for source in self._sources:
            try:
                await source.set_override(key, value)
            except Exception as e:
                self._logger.error(f"Failed to set override in {source.__class__.__name__}: {e}")
    
    def get_history(
        self,
        key: str,
        limit: Optional[int] = None
    ) -> List[OverrideMetadata]:
        """Get override history for key."""
        if not self._track_history or key not in self._history:
            return []
            
        history = self._history[key]
        if limit:
            history = history[-limit:]
            
        return history
    
    def add_source(self, source: OverrideSource) -> None:
        """Add override source."""
        self._sources.append(source)
    
    async def clear_overrides(
        self,
        keys: Optional[Set[str]] = None
    ) -> None:
        """Clear specified or all overrides."""
        if keys is None:
            keys = set(self._overrides.keys())
            
        for key in keys:
            self._overrides.pop(key, None)
            if self._track_history:
                self._history.pop(key, None)
            
        # Clear sources
        for source in self._sources:
            try:
                overrides = await source.get_overrides()
                for key in keys:
                    if key in overrides:
                        await source.set_override(key, None)
            except Exception as e:
                self._logger.error(f"Failed to clear overrides in {source.__class__.__name__}: {e}")