"""
Database Constants
Author: fdygt
Created: 2025-06-04 16:24:30
"""

# Database Engines
DB_ENGINE = {
    'POSTGRESQL': 'postgresql',
    'MYSQL': 'mysql',
    'SQLITE': 'sqlite',
    'MONGODB': 'mongodb'
}

# Database Connection Settings
DB_POOL = {
    'MIN_SIZE': 5,
    'MAX_SIZE': 20,
    'OVERFLOW': 10,
    'TIMEOUT': 30,
    'RECYCLE': 3600
}

# Query Limits
QUERY_LIMITS = {
    'MAX_RESULTS': 1000,
    'DEFAULT_PAGE_SIZE': 50,
    'MAX_PAGE_SIZE': 100
}

# Database Operations
OPERATIONS = {
    'SELECT': 'SELECT',
    'INSERT': 'INSERT',
    'UPDATE': 'UPDATE',
    'DELETE': 'DELETE',
    'TRUNCATE': 'TRUNCATE',
    'CREATE': 'CREATE',
    'DROP': 'DROP',
    'ALTER': 'ALTER'
}

# Table Constraints
CONSTRAINTS = {
    'PRIMARY_KEY': 'PRIMARY KEY',
    'FOREIGN_KEY': 'FOREIGN KEY',
    'UNIQUE': 'UNIQUE',
    'NOT_NULL': 'NOT NULL',
    'CHECK': 'CHECK',
    'DEFAULT': 'DEFAULT'
}

# Data Types
DATA_TYPES = {
    'STRING': 'VARCHAR',
    'TEXT': 'TEXT',
    'INTEGER': 'INTEGER',
    'FLOAT': 'FLOAT',
    'BOOLEAN': 'BOOLEAN',
    'DATE': 'DATE',
    'DATETIME': 'TIMESTAMP',
    'BINARY': 'BLOB',
    'JSON': 'JSONB'
}