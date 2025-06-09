from typing import Generic, TypeVar, Optional, List, Type
from pydantic import BaseModel
from sqlalchemy.orm import Session

T = TypeVar('T')
M = TypeVar('M', bound=BaseModel)

class Repository(Generic[T, M]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session
    
    async def create(self, schema: M) -> T:
        instance = self.model(**schema.dict())
        self.session.add(instance)
        await self.session.commit()
        return instance
    
    async def get_by_id(self, id: int) -> Optional[T]:
        return await self.session.get(self.model, id)
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        return await self.session.query(self.model).offset(skip).limit(limit).all()