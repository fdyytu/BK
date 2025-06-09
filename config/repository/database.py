from typing import TypeVar, Generic, List, Optional, Type, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from .base import BaseModel

T = TypeVar('T')

class DatabaseRepository(Generic[T]):
    """Generic database repository implementation."""
    
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session
        
    async def create(self, data: dict) -> Optional[T]:
        try:
            instance = self.model(**data)
            self.session.add(instance)
            await self.session.commit()
            await self.session.refresh(instance)
            return instance
        except SQLAlchemyError:
            await self.session.rollback()
            return None
            
    async def get_by_id(self, id: Any) -> Optional[T]:
        try:
            return await self.session.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError:
            return None
            
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        try:
            return await self.session.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError:
            return []
            
    async def update(self, id: Any, data: dict) -> Optional[T]:
        try:
            instance = await self.get_by_id(id)
            if instance:
                for key, value in data.items():
                    setattr(instance, key, value)
                await self.session.commit()
                await self.session.refresh(instance)
            return instance
        except SQLAlchemyError:
            await self.session.rollback()
            return None
            
    async def delete(self, id: Any) -> bool:
        try:
            instance = await self.get_by_id(id)
            if instance:
                await self.session.delete(instance)
                await self.session.commit()
                return True
            return False
        except SQLAlchemyError:
            await self.session.rollback()
            return False