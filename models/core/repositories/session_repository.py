from typing import Optional, List
from models.core.base.repository_base import RepositoryBase
from models.core.authentication.session import Session
import uuid

class SessionRepository(RepositoryBase[Session]):
    """Session repository implementation."""
    
    def __init__(self, database_connection):
        self._db = database_connection
    
    def get_by_id(self, id: int) -> Optional[Session]:
        """Get session by ID."""
        session_data = self._db.execute(
            "SELECT * FROM sessions WHERE session_id = ?",
            (id,)
        )
        if session_data:
            return Session(
                session_data['session_id'],
                session_data['user_id']
            )
        return None
    
    def get_all(self) -> List[Session]:
        """Get all active sessions."""
        sessions = []
        session_data_list = self._db.execute(
            "SELECT * FROM sessions WHERE is_active = TRUE"
        )
        for session_data in session_data_list:
            sessions.append(
                Session(
                    session_data['session_id'],
                    session_data['user_id']
                )
            )
        return sessions
    
    def add(self, entity: Session) -> Session:
        """Create new session."""
        session_id = str(uuid.uuid4())
        self._db.execute(
            """INSERT INTO sessions 
            (session_id, user_id, created_at, expires_at, is_active) 
            VALUES (?, ?, ?, ?, ?)""",
            (
                session_id,
                entity.user_id,
                entity.created_at,
                entity.expires_at,
                entity.is_active
            )
        )
        entity.session_id = session_id
        return entity
    
    def update(self, entity: Session) -> bool:
        """Update session status."""
        result = self._db.execute(
            """UPDATE sessions 
            SET is_active = ?, expires_at = ? 
            WHERE session_id = ?""",
            (
                entity.is_active,
                entity.expires_at,
                entity.session_id
            )
        )
        return result.rowcount > 0
    
    def delete(self, id: int) -> bool:
        """Delete session."""
        result = self._db.execute(
            "DELETE FROM sessions WHERE session_id = ?",
            (id,)
        )
        return result.rowcount > 0
    
    def exists(self, id: int) -> bool:
        """Check if session exists and is active."""
        result = self._db.execute(
            """SELECT COUNT(*) FROM sessions 
            WHERE session_id = ? AND is_active = TRUE""",
            (id,)
        )
        return result[0][0] > 0
    
    def get_active_by_user_id(self, user_id: int) -> List[Session]:
        """Get all active sessions for user."""
        sessions = []
        session_data_list = self._db.execute(
            """SELECT * FROM sessions 
            WHERE user_id = ? AND is_active = TRUE""",
            (user_id,)
        )
        for session_data in session_data_list:
            sessions.append(
                Session(
                    session_data['session_id'],
                    session_data['user_id']
                )
            )
        return sessions