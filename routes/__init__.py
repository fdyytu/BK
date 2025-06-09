"""
Routes module untuk BK API Server
Mengatur semua endpoint dan routing aplikasi
"""

from fastapi import FastAPI
from typing import List
import os
import importlib
import logging

logger = logging.getLogger(__name__)

def register_routes(app: FastAPI) -> None:
    """
    Mendaftarkan semua routes ke aplikasi FastAPI
    
    Args:
        app: Instance FastAPI
    """
    
    # Import dan register routes dari berbagai modul
    route_modules = [
        'auth',      # Authentication routes
        'user',      # User management routes  
        'ppob',      # PPOB transaction routes
        'payment',   # Payment processing routes
        'admin',     # Admin panel routes
        'webhook',   # Webhook handlers
    ]
    
    registered_routes = []
    
    for module_name in route_modules:
        try:
            # Coba import modul route
            module_path = f"routes.{module_name}"
            route_module = importlib.import_module(module_path)
            
            # Cari router dalam modul
            if hasattr(route_module, 'router'):
                # Include router dengan prefix
                prefix = f"/{module_name}" if module_name != 'auth' else "/api/auth"
                app.include_router(
                    route_module.router,
                    prefix=prefix,
                    tags=[module_name.title()]
                )
                registered_routes.append(module_name)
                logger.info(f"✅ Route {module_name} berhasil didaftarkan dengan prefix {prefix}")
            else:
                logger.warning(f"⚠️  Modul {module_name} tidak memiliki router")
                
        except ImportError as e:
            logger.warning(f"⚠️  Route {module_name} tidak ditemukan: {e}")
        except Exception as e:
            logger.error(f"❌ Error mendaftarkan route {module_name}: {e}")
    
    # Log summary
    if registered_routes:
        logger.info(f"📋 Total routes terdaftar: {len(registered_routes)} - {', '.join(registered_routes)}")
    else:
        logger.info("📋 Tidak ada routes tambahan yang terdaftar")

def get_available_routes() -> List[str]:
    """
    Mendapatkan daftar routes yang tersedia
    
    Returns:
        List nama routes yang tersedia
    """
    
    routes_dir = os.path.dirname(__file__)
    available_routes = []
    
    for file in os.listdir(routes_dir):
        if file.endswith('.py') and file != '__init__.py':
            route_name = file[:-3]  # Remove .py extension
            available_routes.append(route_name)
    
    return available_routes

# Export fungsi utama
__all__ = ['register_routes', 'get_available_routes']
