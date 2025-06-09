import re
from typing import Dict, Pattern

# Regex patterns for common validations
PATTERNS: Dict[str, Pattern] = {
    'email': re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    ),
    'url': re.compile(
        r'^https?:\/\/'
        r'(?:www\.)?'
        r'[-a-zA-Z0-9@:%._\+~#=]{1,256}'
        r'\.[a-zA-Z0-9()]{1,6}'
        r'\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$'
    ),
    'ip_address': re.compile(
        r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    ),
    'hostname': re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}'
        r'[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    ),
    'uuid': re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-'
        r'[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
    ),
    'datetime': re.compile(
        r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}'
        r'(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?$'
    ),
    'semantic_version': re.compile(
        r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)'
        r'(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
        r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
        r'(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
    ),
    'path': re.compile(
        r'^(?:/?[a-zA-Z0-9]+)+/?$'
    ),
    'env_var': re.compile(
        r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    )
}

# Security-related patterns
SECURITY_PATTERNS: Dict[str, Pattern] = {
    'password': re.compile(
        r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])'
        r'[A-Za-z\d@$!%*#?&]{8,}$'
    ),
    'api_key': re.compile(
        r'^[A-Za-z0-9_-]{32,}$'
    ),
    'jwt_token': re.compile(
        r'^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]*$'
    ),
    'ssh_key': re.compile(
        r'^ssh-(?:rsa|dss|ed25519) AAAA[0-9A-Za-z+/]+[=]{0,3}'
        r'(?:[ \t]+.+)?$'
    )
}

# Validation patterns
VALIDATION_PATTERNS: Dict[str, Pattern] = {
    'variable_name': re.compile(
        r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    ),
    'hex_color': re.compile(
        r'^#(?:[0-9a-fA-F]{3}){1,2}$'
    ),
    'phone': re.compile(
        r'^\+?1?\d{9,15}$'
    ),
    'credit_card': re.compile(
        r'^\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}$'
    )
}

# File patterns
FILE_PATTERNS: Dict[str, Pattern] = {
    'python_file': re.compile(r'\.py$'),
    'yaml_file': re.compile(r'\.ya?ml$'),
    'json_file': re.compile(r'\.json$'),
    'env_file': re.compile(r'\.env(?:\.|$)'),
    'config_file': re.compile(r'\.(?:conf|cfg|ini)$')
}