"""
Validation Constants
Author: fdygt
Created: 2025-06-04 16:24:30
"""

import re

# Regular Expressions
REGEX = {
    'EMAIL': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
    'PASSWORD': re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$'),
    'PHONE': re.compile(r'^\+?1?\d{9,15}$'),
    'USERNAME': re.compile(r'^[a-zA-Z0-9_]{3,16}$'),
    'URL': re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'),
    'UUID': re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')
}

# Field Constraints
LENGTH = {
    'USERNAME': {
        'MIN': 3,
        'MAX': 16
    },
    'PASSWORD': {
        'MIN': 8,
        'MAX': 128
    },
    'EMAIL': {
        'MAX': 254
    },
    'TITLE': {
        'MIN': 3,
        'MAX': 100
    },
    'DESCRIPTION': {
        'MIN': 10,
        'MAX': 1000
    }
}

# File Upload
FILE = {
    'MAX_SIZE': 10 * 1024 * 1024,  # 10MB
    'ALLOWED_EXTENSIONS': {
        'IMAGE': {'jpg', 'jpeg', 'png', 'gif'},
        'DOCUMENT': {'pdf', 'doc', 'docx', 'txt'},
        'SPREADSHEET': {'xls', 'xlsx', 'csv'}
    }
}

# Input Sanitization
SANITIZE = {
    'STRIP_TAGS': True,
    'ESCAPE_HTML': True,
    'NORMALIZE_WHITESPACE': True
}

# Date Formats
DATE_FORMATS = {
    'DEFAULT': '%Y-%m-%d',
    'DATETIME': '%Y-%m-%d %H:%M:%S',
    'ISO': '%Y-%m-%dT%H:%M:%SZ',
    'DISPLAY': '%B %d, %Y'
}