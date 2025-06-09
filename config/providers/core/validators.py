from typing import Dict, Any, Optional
import re
from .exceptions import ValidationError

class ProviderValidator:
    """Validator for provider requests"""

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        pattern = r'^08[1-9][0-9]{8,10}$'
        if not re.match(pattern, phone):
            raise ValidationError("Invalid phone number format")
        return True

    @staticmethod
    def validate_customer_id(customer_id: str, provider_type: str) -> bool:
        """Validate customer ID format"""
        patterns = {
            'pln': r'^[0-9]{12}$',
            'pdam': r'^[0-9]{6,12}$',
            'internet': r'^[A-Z0-9]{8,15}$'
        }
        
        if provider_type not in patterns:
            raise ValidationError(f"Unknown provider type: {provider_type}")
            
        pattern = patterns[provider_type]
        if not re.match(pattern, customer_id):
            raise ValidationError(f"Invalid {provider_type} customer ID format")
            
        return True

    @staticmethod
    def validate_amount(amount: float, min_amount: float, max_amount: float) -> bool:
        """Validate transaction amount"""
        if not isinstance(amount, (int, float)):
            raise ValidationError("Amount must be a number")
            
        if amount < min_amount or amount > max_amount:
            raise ValidationError(
                f"Amount must be between {min_amount} and {max_amount}"
            )
            
        return True

    @staticmethod
    def validate_product_code(code: str, prefix: str) -> bool:
        """Validate product code format"""
        pattern = f'^{prefix}[A-Za-z0-9]+$'
        if not re.match(pattern, code):
            raise ValidationError(f"Invalid product code format for {prefix}")
        return True