from enum import Enum
from typing import Dict, Any
from datetime import datetime

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"

class OrderStatus(str, Enum):
    CREATED = "created"
    PAID = "paid"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ProductType(str, Enum):
    DIGITAL = "digital"
    PHYSICAL = "physical"
    SERVICE = "service"
    SUBSCRIPTION = "subscription"

class UserRole(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    USER = "user"
    GUEST = "guest"

class ErrorCodes:
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    AUTHORIZATION_ERROR = "AUTHORIZATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"

# Application Constants
APP_CONSTANTS: Dict[str, Any] = {
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATE_FORMAT": "%Y-%m-%d",
    "TIME_FORMAT": "%H:%M:%S",
    "TIMEZONE": "UTC",
    "DEFAULT_LANGUAGE": "id",
    "SUPPORTED_LANGUAGES": ["id", "en"],
    "DEFAULT_CURRENCY": "IDR",
    "PAGINATION": {
        "DEFAULT_PAGE": 1,
        "DEFAULT_SIZE": 10,
        "MAX_SIZE": 100
    },
    "FILE_UPLOAD": {
        "MAX_SIZE": 5 * 1024 * 1024,  # 5MB
        "ALLOWED_EXTENSIONS": ["jpg", "jpeg", "png", "pdf"],
        "UPLOAD_DIR": "uploads"
    }
}