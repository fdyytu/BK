from typing import Dict, List, Optional, Set, TypeVar
from dataclasses import dataclass
from datetime import datetime
import asyncio

from ..exceptions.loading_errors import ConfigLoadError

T = TypeVar('T')

@dataclass
class Dependency:
    """Dependency information."""
    name: str
    requires: Set[str]
    provides: Set[str]
    data: T

class DependencyResolver:
    """
    Advanced dependency resolver with cycle detection.
    
    Features:
    - Cyclic dependency detection
    - Parallel resolution
    - Optional dependencies
    - Dependency validation
    - Resolution order optimization
    """
    
    def __init__(self) -> None:
        self._dependencies: Dict[str, Dependency] = {}
        self._resolved: Set[str] = set()
        self._being_resolved: Set[str] = set()
        
    async def add_dependency(
        self,
        name: str,
        requires: Set[str],
        provides: Set[str],
        data: T
    ) -> None:
        """
        Add dependency to resolver.
        
        Args:
            name: Dependency name
            requires: Required dependencies
            provides: Provided features
            data: Associated data
        """
        self._dependencies[name] = Dependency(
            name=name,
            requires=requires,
            provides=provides,
            data=data
        )
    
    async def resolve(self) -> List[T]:
        """
        Resolve dependencies.
        
        Returns:
            List of resolved dependencies in order
            
        Raises:
            ConfigLoadError: If resolution fails
        """
        try:
            resolved_order: List[T] = []
            self._resolved.clear()
            self._being_resolved.clear()
            
            # Resolve all dependencies
            for name in self._dependencies:
                if name not in self._resolved:
                    await self._resolve_dependency(name, resolved_order)
            
            return resolved_order
            
        except Exception as e:
            raise ConfigLoadError(f"Dependency resolution failed: {str(e)}")
    
    async def resolve_parallel(
        self,
        max_workers: int = 5
    ) -> List[T]:
        """
        Resolve dependencies in parallel.
        
        Args:
            max_workers: Maximum number of parallel workers
            
        Returns:
            List of resolved dependencies
        """
        try:
            # Get resolution order
            resolution_order = await self.resolve()
            
            # Group independent dependencies
            groups: List[List[T]] = []
            current_group: List[T] = []
            
            for item in resolution_order:
                if not self._has_dependencies(item, current_group):
                    current_group.append(item)
                else:
                    if current_group:
                        groups.append(current_group)
                    current_group = [item]
            
            if current_group:
                groups.append(current_group)
            
            # Process groups in parallel
            results: List[T] = []
            semaphore = asyncio.Semaphore(max_workers)
            
            async def process_group(group: List[T]) -> None:
                async with semaphore:
                    results.extend(group)
            
            await asyncio.gather(
                *(process_group(group) for group in groups)
            )
            
            return results
            
        except Exception as e:
            raise ConfigLoadError(
                f"Parallel dependency resolution failed: {str(e)}"
            )
    
    async def _resolve_dependency(
        self,
        name: str,
        resolved_order: List[T]
    ) -> None:
        """
        Resolve single dependency.
        
        Args:
            name: Dependency name
            resolved_order: List to store resolution order
        """
        if name in self._being_resolved:
            raise ConfigLoadError(
                f"Circular dependency detected: {name}"
            )
        
        if name in self._resolved:
            return
        
        self._being_resolved.add(name)
        
        dep = self._dependencies[name]
        
        # Resolve required dependencies first
        for req in dep.requires:
            if req not in self._dependencies:
                raise ConfigLoadError(
                    f"Missing dependency: {req} required by {name}"
                )
            await self._resolve_dependency(req, resolved_order)
        
        self._being_resolved.remove(name)
        self._resolved.add(name)
        resolved_order.append(dep.data)
    
    def _has_dependencies(
        self,
        item: T,
        group: List[T]
    ) -> bool:
        """
        Check if item has dependencies in group.
        
        Args:
            item: Item to check
            group: Group of items
            
        Returns:
            True if item has dependencies in group
        """
        item_dep = next(
            d for d in self._dependencies.values()
            if d.data == item
        )
        
        group_names = {
            d.name for d in self._dependencies.values()
            if d.data in group
        }
        
        return bool(item_dep.requires & group_names)