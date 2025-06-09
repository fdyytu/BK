from dataclasses import dataclass
from decimal import Decimal
from typing import List
from ...common.exceptions import ValidationError

@dataclass(frozen=True)
class PulsaAmount:
    """Value object representing pulsa amount."""
    
    amount: Decimal
    
    def __post_init__(self):
        self.validate()
    
    def validate(self) -> None:
        """Validate pulsa amount."""
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, 'amount', Decimal(str(self.amount)))
            
        if self.amount <= 0:
            raise ValidationError("Amount must be positive")
            
        if self.amount not in self.valid_amounts():
            raise ValidationError("Invalid pulsa amount")
    
    @staticmethod
    def valid_amounts() -> List[Decimal]:
        """Get list of valid pulsa amounts."""
        return [
            Decimal('5000'), Decimal('10000'), 
            Decimal('20000'), Decimal('25000'),
            Decimal('50000'), Decimal('100000'),
            Decimal('200000'), Decimal('500000'),
            Decimal('1000000')
        ]