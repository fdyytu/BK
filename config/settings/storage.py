from .environment import get_env

# Storage Settings
STORAGE_TYPE = get_env("STORAGE_TYPE", "local")  # local, s3, gcs
STORAGE_ROOT = get_env("STORAGE_ROOT", "storage")

# File Upload Settings
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "doc", "docx"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
UPLOAD_FOLDER = "uploads"

# Cloud Storage Settings
CLOUD_STORAGE = {
    "aws": {
        "access_key": get_env("AWS_ACCESS_KEY", ""),
        "secret_key": get_env("AWS_SECRET_KEY", ""),
        "bucket_name": get_env("AWS_BUCKET_NAME", ""),
        "region": get_env("AWS_REGION", "us-east-1")
    }
}