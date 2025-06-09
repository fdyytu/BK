import json
import logging
from typing import Dict, Any
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON
        
        Includes:
        - Timestamp (ISO format)
        - Log level
        - Logger name
        - Message
        - Additional context
        - Exception info if present
        """
        output: Dict[str, Any] = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }

        if hasattr(record, 'props'):
            output.update(record.props)

        if record.exc_info:
            output['exception'] = self.formatException(record.exc_info)

        return json.dumps(output)