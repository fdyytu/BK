from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from flask import Flask as FlaskApp
from django.core.asgi import get_asgi_application
from django.conf import settings
import django
from typing import List
import datetime
import logging
import os
import sys
from watchfiles import watch

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Konfigurasi watchfiles untuk monitoring perubahan file
WATCHED_DIRECTORIES = [
    "./routes",
    "./models",
    "./services",
    "./config",
    "./utils"
]

def log_file_change(changed_files):
    """Mencatat file yang berubah ke log"""
    for change_type, file_path in changed_files:
        logger.info(f"Terdeteksi perubahan: {change_type} - {file_path}")
        
# Kelas untuk menangani reload
class AutoReloader:
    def __init__(self, app):
        self.app = app
        self.last_reload = datetime.datetime.utcnow()
        
    async def watch_files(self):
        """Memantau perubahan file"""
        try:
            async for changes in watch(*WATCHED_DIRECTORIES, recursive=True):
                current_time = datetime.datetime.utcnow()
                # Mencegah multiple reload dalam 2 detik
                if (current_time - self.last_reload).total_seconds() > 2:
                    log_file_change(changes)
                    self.last_reload = current_time
                    # Reload aplikasi
                    self.reload_app()
        except Exception as e:
            logger.error(f"Error dalam pemantauan file: {str(e)}")

    def reload_app(self):
        """Melakukan reload aplikasi"""
        logger.info(f"[{datetime.datetime.utcnow()}] Memulai reload aplikasi...")
        try:
            # Reload modul-modul yang berubah
            for module in list(sys.modules.keys()):
                if any(module.startswith(dir_name) for dir_name in WATCHED_DIRECTORIES):
                    try:
                        reload(sys.modules[module])
                        logger.info(f"Berhasil reload modul: {module}")
                    except:
                        pass
            logger.info("Reload aplikasi selesai")
        except Exception as e:
            logger.error(f"Error saat reload: {str(e)}")

# Inisialisasi aplikasi seperti sebelumnya...
[kode sebelumnya tetap sama]

if __name__ == "__main__":
    import uvicorn
    from uvicorn.config import Config
    import asyncio
    
    # Informasi startup
    current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    current_user = os.getenv("USER", "fdyytu")
    
    print(f"\n=== Server Status ===")
    print(f"📅 Waktu Start (UTC): {current_time}")
    print(f"👤 User: {current_user}")
    print("\n🔍 Monitoring Direktori:")
    for dir_path in WATCHED_DIRECTORIES:
        print(f"   └── {dir_path}")
    
    print("\n🚀 Server mulai dengan konfigurasi:")
    print("├── FastAPI: API utama dan endpoints")
    print("├── Django: Admin panel dan reporting")
    print("└── Flask: Payment gateway dan webhooks")
    
    # Konfigurasi uvicorn dengan hot reload
    config = Config(
        "server:fastapi_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=WATCHED_DIRECTORIES,
        log_level="info"
    )
    
    # Inisialisasi AutoReloader
    reloader = AutoReloader(fastapi_app)
    
    # Jalankan server dengan fitur reload
    server = uvicorn.Server(config)
    
    # Jalankan pemantau file dalam task terpisah
    async def run_server():
        await asyncio.gather(
            server.serve(),
            reloader.watch_files()
        )
    
    # Jalankan server dengan asyncio
    asyncio.run(run_server())