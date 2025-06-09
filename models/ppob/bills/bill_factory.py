from typing import Dict, Type
from .bill_base import BillBase
from .bpjs import BPJSBill
from .pdam import PDAMBill
from .telkom import TelkomBill

class BillFactory:
    """Factory for creating bill payment handlers."""
    
    _handlers: Dict[str, Type[BillBase]] = {
        'bpjs': BPJSBill,
        'pdam': PDAMBill,
        'telkom': TelkomBill
    }
    
    @classmethod
    def create(cls, 
               bill_type: str, 
               api_key: str, 
               sandbox: bool = False) -> BillBase:
        """Create bill payment handler."""
        handler_class = cls._handlers.get(bill_type.lower())
        
        if not handler_class:
            raise ValueError(f"Unsupported bill type: {bill_type}")
            
        return handler_class(api_key, sandbox)
    
    @classmethod
    def register_handler(cls, 
                        bill_type: str, 
                        handler_class: Type[BillBase]) -> None:
        """Register new bill payment handler."""
        cls._handlers[bill_type.lower()] = handler_class