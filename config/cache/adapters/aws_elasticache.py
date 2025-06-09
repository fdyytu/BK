from typing import Any, Optional
from boto3 import client
from ..drivers.base import BaseDriver

class ElastiCacheAdapter(BaseDriver):
    """Adapter untuk AWS ElastiCache"""
    
    def __init__(self, cluster_id: str, region: str):
        super().__init__()
        self.elasticache = client('elasticache', region_name=region)
        self.cluster_id = cluster_id
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize connection to ElastiCache"""
        response = self.elasticache.describe_cache_clusters(
            CacheClusterId=self.cluster_id,
            ShowCacheNodeInfo=True
        )
        nodes = response['CacheClusters'][0]['CacheNodes']
        self.endpoints = [node['Endpoint'] for node in nodes]