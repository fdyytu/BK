"""
Path Constants
Author: fdygt
Created: 2025-06-04 16:24:30
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
STORAGE_DIR = os.path.join(BASE_DIR, 'storage')

# Application Paths
PATHS = {
    'LOGS': os.path.join(STORAGE_DIR, 'logs'),
    'MEDIA': os.path.join(STORAGE_DIR, 'media'),
    'TEMP': os.path.join(STORAGE_DIR, 'temp'),
    'CACHE': os.path.join(STORAGE_DIR, 'cache'),
    'UPLOADS': os.path.join(STORAGE_DIR, 'uploads'),
    'DOWNLOADS': os.path.join(STORAGE_DIR, 'downloads'),
    'BACKUPS': os.path.join(STORAGE_DIR, 'backups')
}

# Template Paths
TEMPLATES = {
    'EMAIL': os.path.join(BASE_DIR, 'templates', 'email'),
    'PDF': os.path.join(BASE_DIR, 'templates', 'pdf'),
    'EXCEL': os.path.join(BASE_DIR, 'templates', 'excel')
}

# Static Paths
STATIC = {
    'CSS': '/static/css',
    'JS': '/static/js',
    'IMG': '/static/img',
    'FONTS': '/static/fonts'
}

# API Endpoints
API_ENDPOINTS = {
    'AUTH': '/api/v1/auth',
    'USERS': '/api/v1/users',
    'PRODUCTS': '/api/v1/products',
    'ORDERS': '/api/v1/orders',
    'PAYMENTS': '/api/v1/payments'
}

# External URLs
EXTERNAL_URLS = {
    'CDN': 'https://cdn.example.com',
    'API_DOCS': 'https://docs.example.com',
    'SUPPORT': 'https://support.example.com'
}