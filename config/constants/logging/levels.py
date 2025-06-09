"""
Logging Level Constants
Created: 2025-06-04 16:27:17
Author: fdygt
"""

import logging
from typing import Dict, Any

# Log Levels
LEVELS: Dict[str, Dict[str, Any]] = {
    'DEBUG': {
        'level': logging.DEBUG,
        'description': 'Detailed information for debugging',
        'color': '\033[36m'  # Cyan
    },
    'INFO': {
        'level': logging.INFO,
        'description': 'General information about program execution',
        'color': '\033[32m'  # Green
    },
    'WARNING': {
        'level': logging.WARNING,
        'description': 'Indication of a potential problem',
        'color': '\033[33m'  # Yellow
    },
    'ERROR': {
        'level': logging.ERROR,
        'description': 'Serious problem that needs attention',
        'color': '\033[31m'  # Red
    },
    'CRITICAL': {
        'level': logging.CRITICAL,
        'description': 'Program may not be able to continue',
        'color': '\033[35m'  # Magenta
    }
}

# Log Categories
CATEGORIES = {
    'SECURITY': 'security',
    'PERFORMANCE': 'performance',
    'DATABASE': 'database',
    'API': 'api',
    'BACKGROUND': 'background'
}