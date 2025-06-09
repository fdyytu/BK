from typing import Dict, Any

class BaseLoggingConfig:
    @staticmethod
    def get_config() -> Dict[str, Any]:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": "config.logging.formatters.json_formatter.JsonFormatter"
                },
                "verbose": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "verbose"
                },
                "file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": "/var/log/api/app.log",
                    "when": "midnight",
                    "interval": 1,
                    "backupCount": 30,
                    "formatter": "json"
                },
                "error_file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": "/var/log/api/error.log",
                    "when": "midnight",
                    "interval": 1,
                    "backupCount": 90,
                    "formatter": "json"
                }
            },
            "loggers": {
                "": {  # Root logger
                    "handlers": ["console", "file"],
                    "level": "INFO"
                },
                "error": {
                    "handlers": ["error_file"],
                    "level": "ERROR",
                    "propagate": False
                }
            }
        }