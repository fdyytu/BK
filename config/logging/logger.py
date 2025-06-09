import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional

def setup_logger(
    name: str = __name__,
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Setup logger dengan konfigurasi yang fleksibel
    
    Args:
        name: Nama logger
        level: Level logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path file log (optional)
        max_bytes: Ukuran maksimal file log sebelum rotasi
        backup_count: Jumlah file backup yang disimpan
        format_string: Format custom untuk log message
    
    Returns:
        Logger instance yang sudah dikonfigurasi
    """
    
    # Buat logger
    logger = logging.getLogger(name)
    
    # Hindari duplikasi handler jika logger sudah ada
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Format default
    if format_string is None:
        format_string = (
            '%(asctime)s - %(name)s - %(levelname)s - '
            '[%(filename)s:%(lineno)d] - %(message)s'
        )
    
    formatter = logging.Formatter(
        format_string,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (jika log_file diberikan)
    if log_file:
        try:
            # Buat direktori jika belum ada
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            
            # Rotating file handler
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
        except Exception as e:
            logger.warning(f"Tidak dapat membuat file log {log_file}: {e}")
    
    return logger

def get_app_logger(app_name: str = "BK") -> logging.Logger:
    """
    Mendapatkan logger khusus untuk aplikasi dengan konfigurasi standar
    
    Args:
        app_name: Nama aplikasi
    
    Returns:
        Logger instance untuk aplikasi
    """
    
    # Tentukan level berdasarkan environment
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    log_level = logging.DEBUG if debug_mode else logging.INFO
    
    # Path file log
    log_dir = os.path.join(os.getcwd(), 'logs')
    log_file = os.path.join(log_dir, f'{app_name.lower()}.log')
    
    return setup_logger(
        name=app_name,
        level=log_level,
        log_file=log_file,
        format_string=(
            '%(asctime)s - %(name)s - %(levelname)s - '
            '[%(process)d:%(thread)d] - %(message)s'
        )
    )

def get_request_logger() -> logging.Logger:
    """
    Logger khusus untuk request HTTP
    
    Returns:
        Logger instance untuk request
    """
    
    log_dir = os.path.join(os.getcwd(), 'logs')
    log_file = os.path.join(log_dir, 'requests.log')
    
    return setup_logger(
        name="requests",
        level=logging.INFO,
        log_file=log_file,
        format_string=(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
    )

def get_error_logger() -> logging.Logger:
    """
    Logger khusus untuk error
    
    Returns:
        Logger instance untuk error
    """
    
    log_dir = os.path.join(os.getcwd(), 'logs')
    log_file = os.path.join(log_dir, 'errors.log')
    
    return setup_logger(
        name="errors",
        level=logging.ERROR,
        log_file=log_file,
        format_string=(
            '%(asctime)s - %(name)s - %(levelname)s - '
            '[%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s'
        )
    )

# Logger default untuk aplikasi
app_logger = get_app_logger()
request_logger = get_request_logger()
error_logger = get_error_logger()

# Fungsi helper untuk logging cepat
def log_info(message: str, logger_name: str = "BK"):
    """Log pesan info"""
    logging.getLogger(logger_name).info(message)

def log_error(message: str, logger_name: str = "BK", exc_info: bool = False):
    """Log pesan error"""
    logging.getLogger(logger_name).error(message, exc_info=exc_info)

def log_warning(message: str, logger_name: str = "BK"):
    """Log pesan warning"""
    logging.getLogger(logger_name).warning(message)

def log_debug(message: str, logger_name: str = "BK"):
    """Log pesan debug"""
    logging.getLogger(logger_name).debug(message)

# Export fungsi utama
__all__ = [
    'setup_logger',
    'get_app_logger', 
    'get_request_logger',
    'get_error_logger',
    'log_info',
    'log_error', 
    'log_warning',
    'log_debug',
    'app_logger',
    'request_logger',
    'error_logger'
]
