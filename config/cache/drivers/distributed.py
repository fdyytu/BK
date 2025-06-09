from typing import Any, Optional
from .base import BaseDriver
from ..exceptions import CacheException

class DistributedDriver(BaseDriver):
    """Implementation untuk distributed caching dengan consistent hashing"""
    
    def __init__(self, nodes: list, replicas: int = 3):
        super().__init__()
        self.nodes = nodes
        self.replicas = replicas
        self._setup_hash_ring()
    
    def _setup_hash_ring(self):
        """Setup consistent hashing ring"""
        self.ring = {}
        for node in self.nodes:
            for i in range(self.replicas):
                key = self._hash(f"{node}:{i}")
                self.ring[key] = node
                
    def _get_node(self, key: str) -> str:
        """Get node for key using consistent hashing"""
        if not self.ring:
            raise CacheException("No nodes available")
        hash_key = self._hash(key)
        for node_hash in sorted(self.ring.keys()):
            if hash_key <= node_hash:
                return self.ring[node_hash]
        return self.ring[min(self.ring.keys())]