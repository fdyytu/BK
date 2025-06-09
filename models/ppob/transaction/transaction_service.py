from typing import Dict, Any, Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from .transaction import Transaction, TransactionStatus, TransactionType
from .transaction_repository import TransactionRepository
from .transaction_logger import TransactionLogger
from ..common.exceptions import TransactionError

class TransactionService:
    """Service for managing transactions."""
    
    def __init__(self,
                 repository: TransactionRepository,
                 logger: TransactionLogger):
        self.repository = repository
        self.logger = logger
    
    async def create_transaction(self,
                               user_id: str,
                               transaction_type: TransactionType,
                               product_code: str,
                               amount: Decimal,
                               customer_number: str,
                               provider: str,
                               metadata: Optional[Dict[str, Any]] = None) -> Transaction:
        """Create new transaction."""
        try:
            transaction = Transaction(
                user_id=user_id,
                transaction_type=transaction_type,
                product_code=product_code,
                amount=amount,
                customer_number=customer_number,
                provider=provider,
                metadata=metadata or {}
            )
            
            # Save to database
            saved_transaction = await self.repository.create(transaction)
            
            # Log creation
            self.logger.log_event('CREATED', saved_transaction)
            
            return saved_transaction
            
        except Exception as e:
            self.logger.log_error(
                'CREATION_FAILED',
                transaction,
                str(e)
            )
            raise TransactionError(f"Failed to create transaction: {str(e)}")
    
    async def update_status(self,
                          transaction_id: UUID,
                          status: TransactionStatus,
                          additional_data: Optional[Dict[str, Any]] = None) -> Transaction:
        """Update transaction status."""
        transaction = await self.repository.get_by_id(transaction_id)
        
        if not transaction:
            raise TransactionError(f"Transaction not found: {transaction_id}")
            
        transaction.status = status
        
        if additional_data:
            transaction.metadata.update(additional_data)
            
        if status in [TransactionStatus.SUCCESS, TransactionStatus.FAILED]:
            transaction.completed_at = datetime.utcnow()
            
        # Save changes
        updated_transaction = await self.repository.update(transaction)
        
        # Log status change
        self.logger.log_event(
            'STATUS_UPDATED',
            updated_transaction,
            {'new_status': status}
        )
        
        return updated_transaction
    
    async def get_user_transactions(self,
                                  user_id: str,
                                  limit: int = 10,
                                  skip: int = 0) -> List[Transaction]:
        """Get user's transactions."""
        return await self.repository.get_by_user(user_id, limit, skip)
    
    async def get_transaction_details(self,
                                    transaction_id: UUID) -> Optional[Transaction]:
        """Get transaction details."""
        return await self.repository.get_by_id(transaction_id)
    
    async def process_refund(self,
                           transaction_id: UUID,
                           refund_reason: str) -> Transaction:
        """Process transaction refund."""
        transaction = await self.repository.get_by_id(transaction_id)
        
        if not transaction:
            raise TransactionError(f"Transaction not found: {transaction_id}")
            
        if transaction.status != TransactionStatus.SUCCESS:
            raise TransactionError(
                "Only successful transactions can be refunded"
            )
            
        # Update status and add refund details
        transaction.status = TransactionStatus.REFUNDED
        transaction.metadata['refund'] = {
            'reason': refund_reason,
            'refunded_at': datetime.utcnow().isoformat()
        }
        
        # Save changes
        updated_transaction = await self.repository.update(transaction)
        
        # Log refund
        self.logger.log_event(
            'REFUNDED',
            updated_transaction,
            {'reason': refund_reason}
        )
        
        return updated_transaction