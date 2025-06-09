# Validation Settings
VALIDATION_SCHEMAS = {
    "DEFAULT_STRING_LENGTH": 255,
    "MAX_STRING_LENGTH": 1000,
    "MIN_PASSWORD_LENGTH": 8,
    "MAX_PASSWORD_LENGTH": 128,
    "USERNAME_PATTERN": r"^[a-zA-Z0-9_-]{3,16}$",
    "EMAIL_PATTERN": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
}

# Input Sanitization
SANITIZATION_RULES = {
    "strip_html": True,
    "remove_scripts": True,
    "escape_sql": True
}

# Custom Validators
CUSTOM_VALIDATORS = {
    "phone": r"^\+?1?\d{9,15}$",
    "url": r"^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$"
}