from typing import Dict, Any, Optional
from datetime import datetime
import logging
import json
from .transaction import Transaction

class TransactionLogger:
    """Logger for transaction events."""
    
    def __init__(self, log_path: str):
        self.logger = logging.getLogger('transaction_logger')
        self.logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.INFO)
        
        # Format
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    def log_event(self,
                  event_type: str,
                  transaction: Transaction,
                  additional_data: Optional[Dict[str, Any]] = None) -> None:
        """Log transaction event."""
        log_data = {
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'transaction_id': str(transaction.id),
            'user_id': transaction.user_id,
            'transaction_type': transaction.transaction_type,
            'amount': str(transaction.amount),
            'status': transaction.status,
            'product_code': transaction.product_code
        }
        
        if additional_data:
            log_data.update(additional_data)
            
        self.logger.info(json.dumps(log_data))
    
    def log_error(self,
                  error_type: str,
                  transaction: Transaction,
                  error_message: str,
                  stack_trace: Optional[str] = None) -> None:
        """Log transaction error."""
        log_data = {
            'event_type': 'ERROR',
            'error_type': error_type,
            'timestamp': datetime.utcnow().isoformat(),
            'transaction_id': str(transaction.id),
            'user_id': transaction.user_id,
            'status': transaction.status,
            'error_message': error_message
        }
        
        if stack_trace:
            log_data['stack_trace'] = stack_trace
            
        self.logger.error(json.dumps(log_data))