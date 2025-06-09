import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'nama_database'),
    'user': os.getenv('DB_USER', 'username'),
    'password': os.getenv('DB_PASSWORD', 'password')
}