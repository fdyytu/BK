from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient
from .transaction import Transaction, TransactionStatus

class TransactionRepository:
    """Repository for handling transaction data."""
    
    def __init__(self, mongodb_url: str, database: str):
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client[database]
        self.collection = self.db.transactions
    
    async def create(self, transaction: Transaction) -> Transaction:
        """Create new transaction."""
        transaction_dict = transaction.dict()
        await self.collection.insert_one(transaction_dict)
        return transaction
    
    async def update(self, transaction: Transaction) -> Transaction:
        """Update existing transaction."""
        transaction.updated_at = datetime.utcnow()
        transaction_dict = transaction.dict()
        
        await self.collection.update_one(
            {"id": transaction.id},
            {"$set": transaction_dict}
        )
        return transaction
    
    async def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        """Get transaction by ID."""
        result = await self.collection.find_one({"id": transaction_id})
        return Transaction(**result) if result else None
    
    async def get_by_user(self,
                         user_id: str,
                         limit: int = 10,
                         skip: int = 0) -> List[Transaction]:
        """Get transactions by user ID."""
        cursor = self.collection.find({"user_id": user_id})
        cursor = cursor.sort("created_at", -1).skip(skip).limit(limit)
        
        transactions = []
        async for doc in cursor:
            transactions.append(Transaction(**doc))
        return transactions
    
    async def get_by_status(self,
                           status: TransactionStatus,
                           start_date: datetime,
                           end_date: datetime) -> List[Transaction]:
        """Get transactions by status and date range."""
        cursor = self.collection.find({
            "status": status,
            "created_at": {
                "$gte": start_date,
                "$lte": end_date
            }
        })
        
        transactions = []
        async for doc in cursor:
            transactions.append(Transaction(**doc))
        return transactions