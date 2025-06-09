from typing import Dict, Any, Optional, List
from datetime import datetime
from .voucher_interface import IVoucher
from .base_voucher import BaseVoucher
from .game_voucher import GameVoucher
from .streaming_voucher import StreamingVoucher
from ..common.exceptions import VoucherException

class VoucherService:
    """Service for managing vouchers."""
    
    def __init__(self):
        self.vouchers: Dict[str, IVoucher] = {}
        
    def create_voucher(self, voucher_type: str, data: Dict[str, Any]) -> IVoucher:
        """Create new voucher."""
        voucher: Optional[IVoucher] = None
        
        if voucher_type == "GAME":
            voucher = GameVoucher(**data)
        elif voucher_type == "STREAMING":
            voucher = StreamingVoucher(**data)
        else:
            voucher = BaseVoucher(**data)
            
        self.vouchers[voucher.code] = voucher
        return voucher
    
    def get_voucher(self, code: str) -> Optional[IVoucher]:
        """Get voucher by code."""
        return self.vouchers.get(code)
    
    def validate_voucher(self, 
                        code: str,
                        user_id: str,
                        amount: float) -> Dict[str, Any]:
        """Validate voucher for use."""
        voucher = self.get_voucher(code)
        
        if not voucher:
            raise VoucherException("Voucher not found")
            
        if not voucher.is_valid():
            raise VoucherException("Voucher is not valid")
            
        if not voucher.can_be_used_by(user_id):
            raise VoucherException("Voucher cannot be used by this user")
            
        try:
            final_amount = voucher.apply_discount(amount)
            return {
                'valid': True,
                'original_amount': amount,
                'final_amount': final_amount,
                'discount': amount - final_amount
            }
        except VoucherException as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def use_voucher(self,
                    code: str,
                    user_id: str,
                    transaction_id: str,
                    amount: float) -> Dict[str, Any]:
        """Use voucher for transaction."""
        validation = self.validate_voucher(code, user_id, amount)
        
        if not validation['valid']:
            raise VoucherException(validation['error'])
            
        voucher = self.get_voucher(code)
        voucher.mark_as_used(user_id, transaction_id)
        
        return {
            'success': True,
            'transaction_id': transaction_id,
            'voucher_code': code,
            'discount_applied': validation['discount'],
            'final_amount': validation['final_amount']
        }
    
    def get_valid_vouchers(self, 
                          user_id: str,
                          voucher_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of valid vouchers for user."""
        valid_vouchers = []
        
        for voucher in self.vouchers.values():
            if not voucher.is_valid():
                continue
                
            if not voucher.can_be_used_by(user_id):
                continue
                
            if voucher_type:
                if not isinstance(voucher, 
                    GameVoucher if voucher_type == "GAME" 
                    else StreamingVoucher if voucher_type == "STREAMING"
                    else BaseVoucher):
                    continue
                    
            valid_vouchers.append({
                'code': voucher.code,
                'discount_amount': voucher.discount_amount,
                'discount_type': voucher.discount_type,
                'expires_at': voucher.end_date.isoformat(),
                'min_purchase': voucher.min_purchase,
                'max_discount': voucher.max_discount
            })
            
        return valid_vouchers