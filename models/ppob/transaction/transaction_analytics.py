from typing import Dict, Any, List
from datetime import datetime, timedelta
from decimal import Decimal
from .transaction_repository import TransactionRepository
from .transaction import TransactionStatus, TransactionType

class TransactionAnalytics:
    """Analytics service for transactions."""
    
    def __init__(self, repository: TransactionRepository):
        self.repository = repository
    
    async def get_daily_stats(self, date: datetime) -> Dict[str, Any]:
        """Get daily transaction statistics."""
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        # Get transactions for the day
        transactions = await self.repository.get_by_date_range(
            start_date,
            end_date
        )
        
        # Calculate statistics
        total_count = len(transactions)
        successful_count = sum(
            1 for t in transactions 
            if t.status == TransactionStatus.SUCCESS
        )
        failed_count = sum(
            1 for t in transactions 
            if t.status == TransactionStatus.FAILED
        )
        total_amount = sum(
            t.amount for t in transactions 
            if t.status == TransactionStatus.SUCCESS
        )
        
        return {
            'date': start_date.date().isoformat(),
            'total_transactions': total_count,
            'successful_transactions': successful_count,
            'failed_transactions': failed_count,
            'success_rate': (successful_count / total_count) if total_count > 0 else 0,
            'total_amount': str(total_amount),
            'average_amount': str(total_amount / successful_count) if successful_count > 0 else "0"
        }
    
    async def get_product_performance(self,
                                    start_date: datetime,
                                    end_date: datetime) -> List[Dict[str, Any]]:
        """Get product performance statistics."""
        transactions = await self.repository.get_by_date_range(
            start_date,
            end_date
        )
        
        # Group by product
        product_stats = {}
        for transaction in transactions:
            if transaction.status != TransactionStatus.SUCCESS:
                continue
                
            if transaction.product_code not in product_stats:
                product_stats[transaction.product_code] = {
                    'count': 0,
                    'total_amount': Decimal('0')
                }
                
            stats = product_stats[transaction.product_code]
            stats['count'] += 1
            stats['total_amount'] += transaction.amount
        
        # Format results
        return [
            {
                'product_code': code,
                'transaction_count': stats['count'],
                'total_amount': str(stats['total_amount']),
                'average_amount': str(stats['total_amount'] / stats['count'])
            }
            for code, stats in product_stats.items()
        ]