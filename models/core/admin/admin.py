from typing import List, Optional
from ..base.user import User
from .value_objects import AdminRole, Permission

class Admin(User):
    """Admin aggregate root."""
    
    def __init__(self, username: str, email: str, role: AdminRole, id: UUID = None):
        super().__init__(username, email, id)
        self._role = role
        self._permissions: List[Permission] = []
        
    def add_permission(self, permission: Permission) -> None:
        if permission not in self._permissions:
            self._permissions.append(permission)
            
    def has_permission(self, permission: Permission) -> bool:
        return permission in self._permissions