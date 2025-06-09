from typing import Optional, List
from models.core.base.repository_base import RepositoryBase
from models.core.base.user_entity import UserEntity
from models.core.authentication.credential import Credential

class UserRepository(RepositoryBase[UserEntity]):
    """User repository implementation."""
    
    def __init__(self, database_connection):
        self._db = database_connection
    
    def get_by_id(self, id: int) -> Optional[UserEntity]:
        """Get user by ID."""
        # Implement database query
        user_data = self._db.execute("SELECT * FROM users WHERE id = ?", (id,))
        if user_data:
            return UserEntity(user_data['id'], user_data['username'])
        return None
    
    def get_all(self) -> List[UserEntity]:
        """Get all users."""
        users = []
        # Implement database query
        user_data_list = self._db.execute("SELECT * FROM users")
        for user_data in user_data_list:
            users.append(UserEntity(user_data['id'], user_data['username']))
        return users
    
    def add(self, entity: UserEntity) -> UserEntity:
        """Add new user."""
        # Implement database insert
        user_id = self._db.execute(
            "INSERT INTO users (username) VALUES (?)",
            (entity.username,)
        )
        entity.user_id = user_id
        return entity
    
    def update(self, entity: UserEntity) -> bool:
        """Update existing user."""
        # Implement database update
        result = self._db.execute(
            "UPDATE users SET username = ? WHERE id = ?",
            (entity.username, entity.user_id)
        )
        return result.rowcount > 0
    
    def delete(self, id: int) -> bool:
        """Delete user by ID."""
        # Implement database delete
        result = self._db.execute("DELETE FROM users WHERE id = ?", (id,))
        return result.rowcount > 0
    
    def exists(self, id: int) -> bool:
        """Check if user exists."""
        result = self._db.execute(
            "SELECT COUNT(*) FROM users WHERE id = ?", 
            (id,)
        )
        return result[0][0] > 0
    
    def get_by_username(self, username: str) -> Optional[UserEntity]:
        """Get user by username."""
        # Implement database query
        user_data = self._db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        if user_data:
            return UserEntity(user_data['id'], user_data['username'])
        return None