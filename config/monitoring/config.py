class MonitoringConfig:
    def __init__(self, env: str):
        self.env = env
        self.config = {
            # ... existing config ...
            "apm": {
                "jaeger_host": "localhost",
                "jaeger_port": 6831,
                "service_name": "ppob-api",
                "sampling_rate": 1.0
            },
            "security": {
                "security_check_interval": 60,
                "threat_patterns_path": "config/security/patterns.json",
                "max_failed_logins": 5,
                "suspicious_amount_threshold": 10000000
            },
            "sla": {
                "sla_targets": {
                    "availability": 99.9,
                    "response_time": 500,  # ms
                    "error_rate": 0.1      # %
                },
                "measurement_interval": 60  # seconds
            },
            "capacity": {
                "prediction_window": 30,    # days
                "alert_threshold": 80,      # %
                "scaling_threshold": 75     # %
            },
            "cost": {
                "budget_alert_threshold": 90,  # %
                "anomaly_threshold": 2.0,      # standard deviations
                "prediction_window": 90        # days
            }
        }