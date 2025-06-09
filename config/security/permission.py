class Role:
    def __init__(self, name: str):
        self.name = name

class Permission:
    def __init__(self, action: str, resource: str):
        self.action = action
        self.resource = resource

class PermissionManager:
    def assign_role(self, user_id: str, role: Role):
        pass

    def check_permission(self, user_id: str, permission: Permission) -> bool:
        pass

    def remove_role(self, user_id: str, role: Role):
        pass