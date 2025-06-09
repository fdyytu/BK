import os
import sys
import logging
import asyncio
from datetime import datetime
from typing import List, Optional

# FastAPI imports
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# Uvicorn untuk server
import uvicorn
from uvicorn.config import Config

# Import konfigurasi lokal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from config.settings.base import *
except ImportError:
    # Fallback ke konfigurasi sederhana jika ada masalah import
    DEBUG = True
    SECRET_KEY = "fallback-secret-key"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from config.logging.logger import setup_logger
except ImportError:
    # Fallback logger sederhana
    def setup_logger(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

# Setup logging
logger = setup_logger(__name__)

# Inisialisasi FastAPI app
app = FastAPI(
    title="BK API Server",
    description="Backend API untuk aplikasi BK",
    version="1.0.0",
    debug=DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Sesuaikan dengan domain yang diizinkan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware untuk logging request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Process request
    response = await call_next(request)
    
    # Log response time
    process_time = (datetime.utcnow() - start_time).total_seconds()
    logger.info(f"Response: {response.status_code} - Time: {process_time:.3f}s")
    
    return response

# Health check endpoint
@app.get("/health")
async def health_check():
    """Endpoint untuk mengecek status server"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "BK API Server berjalan dengan baik",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# Import dan register routes
try:
    from routes import register_routes
    register_routes(app)
    logger.info("Routes berhasil didaftarkan")
except ImportError as e:
    logger.warning(f"Routes tidak dapat dimuat: {e}")
    logger.info("Server akan berjalan tanpa routes tambahan")

# Exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("=== BK API Server Starting ===")
    logger.info(f"Debug mode: {DEBUG}")
    logger.info(f"Base directory: {BASE_DIR}")
    logger.info("Server siap menerima request")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("=== BK API Server Shutting Down ===")

if __name__ == "__main__":
    # Informasi startup
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    current_user = os.getenv("USER", "system")
    
    print(f"\n=== BK API Server ===")
    print(f"📅 Waktu Start (UTC): {current_time}")
    print(f"👤 User: {current_user}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Base Dir: {BASE_DIR}")
    
    # Direktori yang akan dimonitor untuk hot reload
    reload_dirs = [
        "./routes",
        "./models", 
        "./services",
        "./config",
        "./utils"
    ]
    
    print("\n🔍 Monitoring Direktori:")
    for dir_path in reload_dirs:
        if os.path.exists(dir_path):
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path} (tidak ditemukan)")
    
    print("\n🚀 Server Configuration:")
    print("├── Framework: FastAPI")
    print("├── Host: 0.0.0.0")
    print("├── Port: 8000")
    print("├── Hot Reload: Enabled")
    print("└── Debug Mode: " + ("Enabled" if DEBUG else "Disabled"))
    
    print("\n📚 Available Endpoints:")
    print("├── API Docs: http://localhost:8000/docs")
    print("├── ReDoc: http://localhost:8000/redoc")
    print("├── Health Check: http://localhost:8000/health")
    print("└── Root: http://localhost:8000/")
    
    # Konfigurasi uvicorn
    config = Config(
        app="server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[d for d in reload_dirs if os.path.exists(d)],
        log_level="info",
        access_log=True
    )
    
    # Jalankan server
    try:
        server = uvicorn.Server(config)
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        print("\n\n🛑 Server dihentikan oleh user")
    except Exception as e:
        print(f"\n\n❌ Error menjalankan server: {e}")
        logger.error(f"Server error: {e}")
