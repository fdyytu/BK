import logging
from typing import Dict, Any
from datetime import datetime

class TransactionLogger:
    def __init__(self):
        self.logger = logging.getLogger('transaction')
    
    def log_transaction(
        self,
        transaction_id: str,
        type: str,
        amount: float,
        status: str,
        user_id: str,
        **kwargs: Any
    ) -> None:
        """
        Log PPOB transaction details
        
        Args:
            transaction_id: Unique transaction identifier
            type: Transaction type (topup, payment, transfer)
            amount: Transaction amount
            status: Transaction status
            user_id: User performing transaction
            **kwargs: Additional transaction metadata
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'transaction_id': transaction_id,
            'type': type,
            'amount': amount,
            'status': status,
            'user_id': user_id,
            **kwargs
        }
        
        self.logger.info('Transaction processed', extra=log_data)