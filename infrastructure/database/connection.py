from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .exceptions import DatabaseConnectionError

class DatabaseConnection:
    """Database connection manager."""
    
    def __init__(self, settings: DatabaseSettings):
        self._settings = settings
        self._engine = self._create_engine()
        self._session_factory = sessionmaker(
            self._engine, 
            class_=AsyncSession,
            expire_on_commit=False
        )
        
    def _create_engine(self):
        return create_async_engine(
            self._settings.connection_url,
            echo=self._settings.debug,
            pool_size=self._settings.pool_size,
            max_overflow=self._settings.max_overflow,
            pool_timeout=self._settings.pool_timeout,
            pool_recycle=self._settings.pool_recycle
        )
        
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session with automatic cleanup."""
        session: AsyncSession = self._session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise DatabaseConnectionError(f"Database error: {str(e)}")
        finally:
            await session.close()