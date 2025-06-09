from typing import List, Set
from uuid import UUID
from ..interfaces import AuthorizationPolicy
from ..exceptions import PermissionDenied

class AuthorizationService:
    """Authorization service."""
    
    def __init__(self, policy: AuthorizationPolicy):
        self.policy = policy
        
    async def check_permission(
        self,
        user_id: UUID,
        required_permissions: Set[str]
    ) -> bool:
        """Check if user has required permissions."""
        user_permissions = await self.policy.get_user_permissions(user_id)
        
        if not required_permissions.issubset(user_permissions):
            missing = required_permissions - user_permissions
            raise PermissionDenied(
                f"Missing required permissions: {', '.join(missing)}"
            )
            
        return True
        
    async def assign_role(
        self,
        user_id: UUID,
        role_name: str
    ) -> None:
        """Assign role to user."""
        await self.policy.assign_user_role(user_id, role_name)