"""
Currency Constants
Author: fdygt
Created: 2025-06-04 16:25:57
"""

from typing import Dict, Any

# Currency Codes
CURRENCIES: Dict[str, Dict[str, Any]] = {
    'USD': {
        'name': 'US Dollar',
        'symbol': '$',
        'decimals': 2
    },
    'EUR': {
        'name': 'Euro',
        'symbol': '€',
        'decimals': 2
    },
    'GBP': {
        'name': 'British Pound',
        'symbol': '£',
        'decimals': 2
    },
    'JPY': {
        'name': 'Japanese Yen',
        'symbol': '¥',
        'decimals': 0
    }
}

# Currency Formatting
FORMAT = {
    'DECIMAL_SEPARATOR': '.',
    'THOUSAND_SEPARATOR': ',',
    'SYMBOL_POSITION': 'before'  # 'before' or 'after'
}

# Exchange Rate Sources
EXCHANGE_RATE_PROVIDERS = {
    'DEFAULT': 'exchangeratesapi',
    'FALLBACK': 'openexchangerates',
    'UPDATE_INTERVAL': 3600  # seconds
}