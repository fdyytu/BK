"""
Feature Flags Constants
Created: 2025-06-04 16:27:17
Author: fdygt
"""

from typing import Dict, Any

FEATURES: Dict[str, Dict[str, Any]] = {
    'NEW_UI': {
        'enabled': True,
        'percentage': 100,
        'description': 'New user interface rollout'
    },
    'BETA_FEATURES': {
        'enabled': False,
        'whitelist': ['beta_users', 'developers'],
        'description': 'Beta features access'
    },
    'MAINTENANCE_MODE': {
        'enabled': False,
        'bypass_roles': ['admin', 'maintainer'],
        'description': 'System maintenance mode'
    }
}

FEATURE_TOGGLES = {
    'USE_NEW_ALGORITHM': True,
    'ENABLE_CACHING': True,
    'DEBUG_MODE': False,
    'STRICT_VALIDATION': True
}

ROLLOUT_STRATEGIES = {
    'ALL_USERS': 'all_users',
    'PERCENTAGE': 'percentage',
    'WHITELIST': 'whitelist',
    'GRADUAL': 'gradual'
}