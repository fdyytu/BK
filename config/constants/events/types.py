"""
Event Type Constants
Created: 2025-06-04 16:27:17
Author: fdygt
"""

# System Events
SYSTEM_EVENTS = {
    'STARTUP': 'system.startup',
    'SHUTDOWN': 'system.shutdown',
    'MAINTENANCE': 'system.maintenance',
    'ERROR': 'system.error'
}

# User Events
USER_EVENTS = {
    'REGISTRATION': 'user.registration',
    'LOGIN': 'user.login',
    'LOGOUT': 'user.logout',
    'PASSWORD_CHANGE': 'user.password_change',
    'PROFILE_UPDATE': 'user.profile_update'
}

# Data Events
DATA_EVENTS = {
    'CREATED': 'data.created',
    'UPDATED': 'data.updated',
    'DELETED': 'data.deleted',
    'RESTORED': 'data.restored'
}

# Integration Events
INTEGRATION_EVENTS = {
    'SYNC_STARTED': 'integration.sync_started',
    'SYNC_COMPLETED': 'integration.sync_completed',
    'SYNC_FAILED': 'integration.sync_failed',
    'WEBHOOK_RECEIVED': 'integration.webhook_received'
}