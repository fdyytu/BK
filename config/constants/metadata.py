"""
Constants Metadata
Author: fdygt
Created: 2025-06-04 16:25:57
"""

from typing import Dict, Any
from datetime import datetime

# Version Control
VERSION = {
    'MAJOR': 1,
    'MINOR': 0,
    'PATCH': 0,
    'RELEASE': 'stable'
}

# Metadata Information
METADATA: Dict[str, Any] = {
    'name': 'Application Constants',
    'version': f"{VERSION['MAJOR']}.{VERSION['MINOR']}.{VERSION['PATCH']}-{VERSION['RELEASE']}",
    'author': 'fdygt',
    'created_at': '2025-06-04 16:25:57',
    'updated_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
    'description': 'Professional constant definitions for the application',
    'license': 'MIT',
    'repository': 'https://github.com/fdygt/app-constants'
}

# Documentation Links
DOCS = {
    'API': 'https://api.docs.example.com',
    'WIKI': 'https://wiki.example.com',
    'CHANGELOG': 'https://changelog.example.com'
}

# Support Information
SUPPORT = {
    'email': 'support@example.com',
    'website': 'https://support.example.com',
    'hours': '24/7'
}