from enum import Enum

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class RoleType(Enum):
    ADMIN = "admin"
    OWNER = "owner"
    SELLER = "seller"
    BUYER = "buyer"