from typing import Dict, Any, Optional
from decimal import Decimal
from datetime import datetime
from .payment_interface import IPayment
from .bank_transfer import BankTransfer
from .ewallet import EWallet
from ..common.exceptions import PaymentError

class PaymentService:
    """Service for managing payments."""
    
    def __init__(self, config: Dict[str, Dict[str, str]]):
        self.config = config
        self.payment_methods: Dict[str, IPayment] = {}
        self._initialize_payment_methods()
    
    def _initialize_payment_methods(self) -> None:
        """Initialize payment methods."""
        if 'bank_transfer' in self.config:
            self.payment_methods['bank_transfer'] = BankTransfer(
                api_key=self.config['bank_transfer']['api_key'],
                merchant_id=self.config['bank_transfer']['merchant_id'],
                sandbox=self.config['bank_transfer'].get('sandbox', False)
            )
            
        if 'ewallet' in self.config:
            self.payment_methods['ewallet'] = EWallet(
                api_key=self.config['ewallet']['api_key'],
                merchant_id=self.config['ewallet']['merchant_id'],
                sandbox=self.config['ewallet'].get('sandbox', False)
            )
    
    async def create_payment(self,
                           amount: Decimal,
                           payment_type: str,
                           description: str,
                           metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create payment transaction."""
        payment_method = self.payment_methods.get(payment_type)
        
        if not payment_method:
            raise PaymentError(
                f"Unsupported payment type: {payment_type}"
            )
            
        return await payment_method.create_payment(
            amount,
            'IDR',  # Default to Indonesian Rupiah
            description,
            metadata
        )
    
    async def process_payment(self,
                            payment_id: str,
                            payment_type: str,
                            method: str) -> Dict[str, Any]:
        """Process payment transaction."""
        payment_method = self.payment_methods.get(payment_type)
        
        if not payment_method:
            raise PaymentError(
                f"Unsupported payment type: {payment_type}"
            )
            
        return await payment_method.process_payment(payment_id, method)
    
    async def check_status(self,
                          payment_id: str,
                          payment_type: str) -> Dict[str, Any]:
        """Check payment status."""
        payment_method = self.payment_methods.get(payment_type)
        
        if not payment_method:
            raise PaymentError(
                f"Unsupported payment type: {payment_type}"
            )
            
        return await payment_method.check_status(payment_id)
    
    async def process_refund(self,
                           payment_id: str,
                           payment_type: str,
                           amount: Optional[Decimal] = None) -> Dict[str, Any]:
        """Process payment refund."""
        payment_method = self.payment_methods.get(payment_type)
        
        if not payment_method:
            raise PaymentError(
                f"Unsupported payment type: {payment_type}"
            )
            
        return await payment_method.refund(payment_id, amount)