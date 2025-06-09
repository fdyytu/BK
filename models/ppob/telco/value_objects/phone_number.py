from dataclasses import dataclass
from typing import Optional
import re
from ...common.exceptions import ValidationError

@dataclass(frozen=True)
class PhoneNumber:
    """Value object representing a phone number."""
    
    number: str
    country_code: str = "62"  # Default to Indonesia
    
    def __post_init__(self):
        self.validate()
    
    def validate(self) -> None:
        """Validate phone number format."""
        # Remove any spaces or special characters
        cleaned = re.sub(r'[^\d]', '', self.number)
        
        # Validate format
        if not re.match(r'^(?:62|0)[8][1-9][0-9]{8,10}$', cleaned):
            raise ValidationError("Invalid phone number format")
    
    @property
    def formatted(self) -> str:
        """Get formatted phone number."""
        cleaned = re.sub(r'[^\d]', '', self.number)
        
        # Remove leading zeros or country code
        if cleaned.startswith('0'):
            cleaned = cleaned[1:]
        elif cleaned.startswith('62'):
            cleaned = cleaned[2:]
            
        return f"+{self.country_code}{cleaned}"
    
    @property
    def provider(self) -> Optional[str]:
        """Get telco provider based on prefix."""
        prefix_map = {
            '811': 'Telkomsel', '812': 'Telkomsel', '813': 'Telkomsel',
            '821': 'Telkomsel', '822': 'Telkomsel', '823': 'Telkomsel',
            '851': 'Telkomsel', '852': 'Telkomsel', '853': 'Telkomsel',
            '814': 'Indosat', '815': 'Indosat', '816': 'Indosat',
            '855': 'Indosat', '856': 'Indosat', '857': 'Indosat',
            '858': 'Indosat',
            '817': 'XL', '818': 'XL', '819': 'XL',
            '859': 'XL', '877': 'XL', '878': 'XL',
            '831': 'Axis', '832': 'Axis', '833': 'Axis',
            '838': 'Axis',
            '895': 'Three', '896': 'Three', '897': 'Three',
            '898': 'Three', '899': 'Three',
            '881': 'Smartfren', '882': 'Smartfren', '883': 'Smartfren',
            '884': 'Smartfren', '885': 'Smartfren', '886': 'Smartfren',
            '887': 'Smartfren', '888': 'Smartfren', '889': 'Smartfren'
        }
        
        cleaned = re.sub(r'[^\d]', '', self.number)
        if cleaned.startswith('0'):
            prefix = cleaned[1:4]
        elif cleaned.startswith('62'):
            prefix = cleaned[2:5]
        else:
            prefix = cleaned[:3]
            
        return prefix_map.get(prefix)