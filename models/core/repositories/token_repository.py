from typing import Optional, List
from models.core.base.repository_base import RepositoryBase
from models.core.authentication.token import Token
from datetime import datetime

class TokenRepository(RepositoryBase[Token]):
    """Token repository implementation."""
    
    def __init__(self, database_connection):
        self._db = database_connection
    
    def get_by_id(self, id: int) -> Optional[Token]:
        """Get token by ID."""
        token_data = self._db.execute(
            "SELECT * FROM tokens WHERE id = ?",
            (id,)
        )
        if token_data:
            return Token(token_data['token'])
        return None
    
    def get_all(self) -> List[Token]:
        """Get all valid tokens."""
        tokens = []
        now = datetime.utcnow()
        token_data_list = self._db.execute(
            "SELECT * FROM tokens WHERE expires_at > ?",
            (now,)
        )
        for token_data in token_data_list:
            tokens.append(Token(token_data['token']))
        return tokens
    
    def add(self, entity: Token) -> Token:
        """Store new token."""
        self._db.execute(
            """INSERT INTO tokens (token, created_at, expires_at) 
            VALUES (?, ?, ?)""",
            (
                entity.token,
                entity.created_at,
                entity.expires_at
            )
        )
        return entity
    
    def update(self, entity: Token) -> bool:
        """Update token expiration."""
        result = self._db.execute(
            "UPDATE tokens SET expires_at = ? WHERE token = ?",
            (entity.expires_at, entity.token)
        )
        return result.rowcount > 0
    
    def delete(self, id: int) -> bool:
        """Delete token."""
        result = self._db.execute(
            "DELETE FROM tokens WHERE id = ?",
            (id,)
        )
        return result.rowcount > 0
    
    def exists(self, id: int) -> bool:
        """Check if token exists and is valid."""
        now = datetime.utcnow()
        result = self._db.execute(
            """SELECT COUNT(*) FROM tokens 
            WHERE id = ? AND expires_at > ?""",
            (id, now)
        )
        return result[0][0] > 0
    
    def invalidate_all_for_user(self, user_id: int) -> bool:
        """Invalidate all tokens for user."""
        now = datetime.utcnow()
        result = self._db.execute(
            """UPDATE tokens SET expires_at = ? 
            WHERE user_id = ? AND expires_at > ?""",
            (now, user_id, now)
        )
        return result.rowcount > 0