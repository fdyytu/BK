from elasticsearch import Elasticsearch
from typing import Dict, Any
import json

class LogShipper:
    def __init__(self, es_host: str, es_port: int, index_prefix: str):
        self.es = Elasticsearch([{'host': es_host, 'port': es_port}])
        self.index_prefix = index_prefix

    def ship_logs(self, log_data: Dict[str, Any]) -> None:
        """Ship logs to Elasticsearch"""
        index_name = f"{self.index_prefix}-{datetime.utcnow().strftime('%Y.%m.%d')}"
        
        try:
            self.es.index(
                index=index_name,
                body=json.dumps(log_data),
                doc_type='_doc'
            )
        except Exception as e:
            fallback_logger = logging.getLogger('fallback')
            fallback_logger.error(f'Failed to ship logs: {str(e)}')