from prometheus_client import Counter, Gauge, Histogram
from typing import Dict, Any

class PrometheusMetrics:
    def __init__(self):
        # Transaction metrics
        self.transaction_counter = Counter(
            'ppob_transactions_total',
            'Total number of transactions',
            ['status', 'product_type']
        )
        
        # Response time metrics
        self.response_time = Histogram(
            'ppob_response_time_seconds',
            'Response time in seconds',
            ['endpoint']
        )
        
        # System metrics
        self.system_memory_usage = Gauge(
            'ppob_memory_usage_bytes',
            'Memory usage in bytes'
        )
        
        self.system_cpu_usage = Gauge(
            'ppob_cpu_usage_percent',
            'CPU usage percentage'
        )

    def track_transaction(self, status: str, product_type: str) -> None:
        """Track transaction metrics"""
        self.transaction_counter.labels(
            status=status,
            product_type=product_type
        ).inc()

    def track_response_time(self, endpoint: str, duration: float) -> None:
        """Track API response time"""
        self.response_time.labels(
            endpoint=endpoint
        ).observe(duration)

    def update_system_metrics(self, metrics: Dict[str, Any]) -> None:
        """Update system metrics"""
        self.system_memory_usage.set(metrics['memory']['used_bytes'])
        self.system_cpu_usage.set(metrics['cpu']['usage_percent'])