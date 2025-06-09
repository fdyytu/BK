from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from enum import Enum
from .environment import EnvironmentSettings

class MetricsProvider(str, Enum):
    PROMETHEUS = "prometheus"
    DATADOG = "datadog"
    NEWRELIC = "newrelic"

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class PrometheusSettings(BaseModel):
    """Prometheus configuration."""
    endpoint: str = "/metrics"
    port: int = 9090
    
class DatadogSettings(BaseModel):
    """Datadog configuration."""
    api_key: str
    app_key: str
    service_name: str
    environment: str
    
class NewRelicSettings(BaseModel):
    """New Relic configuration."""
    license_key: str
    app_name: str
    environment: str

class MonitoringSettings(BaseModel):
    """Monitoring and metrics configuration."""
    
    enabled: bool = True
    provider: MetricsProvider = MetricsProvider.PROMETHEUS
    
    # Logging Configuration
    log_level: LogLevel = LogLevel.INFO
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = None
    
    # Metrics Settings
    metrics_enabled: bool = True
    metrics_interval: int = 60
    custom_metrics: Dict[str, Any] = {}
    
    # Tracing Settings
    tracing_enabled: bool = True
    trace_sample_rate: float = 1.0
    
    # Health Check
    health_check_enabled: bool = True
    health_check_path: str = "/health"
    health_check_interval: int = 60
    
    # Alert Settings
    alerts_enabled: bool = True
    alert_channels: List[str] = ["email"]
    alert_thresholds: Dict[str, Any] = {
        "cpu_usage": 80,
        "memory_usage": 80,
        "error_rate": 5,
        "response_time": 2000
    }
    
    # Provider Specific Settings
    prometheus: Optional[PrometheusSettings]
    datadog: Optional[DatadogSettings]
    newrelic: Optional[NewRelicSettings]
    
    @classmethod
    def from_env(cls, env: EnvironmentSettings) -> "MonitoringSettings":
        """Create settings from environment."""
        provider = MetricsProvider(env.get_env("METRICS_PROVIDER", "prometheus"))
        settings = cls(
            enabled=env.get_env("MONITORING_ENABLED", "true").lower() == "true",
            provider=provider,
            log_level=LogLevel(env.get_env("LOG_LEVEL", "INFO"))
        )
        
        if provider == MetricsProvider.PROMETHEUS:
            settings.prometheus = PrometheusSettings(
                port=int(env.get_env("PROMETHEUS_PORT", "9090"))
            )
            
        return settings