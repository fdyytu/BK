#!/usr/bin/env python3
"""
BK API Server - Versi Sederhana
Server FastAPI yang bersih tanpa dependencies kompleks
"""

import os
import sys
import logging
import asyncio
from datetime import datetime
from typing import Optional

# FastAPI imports
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Setup logging sederhana
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Konfigurasi sederhana
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8000))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Inisialisasi FastAPI app
app = FastAPI(
    title="BK API Server",
    description="Backend API untuk aplikasi BK - Versi Sederhana",
    version="1.0.0",
    debug=DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware untuk logging request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()
    
    # Log request
    logger.info(f"📥 {request.method} {request.url}")
    
    # Process request
    response = await call_next(request)
    
    # Log response time
    process_time = (datetime.utcnow() - start_time).total_seconds()
    logger.info(f"📤 {response.status_code} - ⏱️  {process_time:.3f}s")
    
    return response

# Health check endpoint
@app.get("/health")
async def health_check():
    """Endpoint untuk mengecek status server"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "server": "BK API Server"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🚀 BK API Server berjalan dengan baik!",
        "timestamp": datetime.utcnow().isoformat(),
        "debug_mode": DEBUG,
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# API Info endpoint
@app.get("/api/info")
async def api_info():
    """Informasi API"""
    return {
        "name": "BK API Server",
        "version": "1.0.0",
        "description": "Backend API untuk aplikasi BK",
        "debug": DEBUG,
        "base_dir": BASE_DIR,
        "python_version": sys.version,
        "available_endpoints": [
            {"path": "/", "method": "GET", "description": "Root endpoint"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/api/info", "method": "GET", "description": "API information"},
            {"path": "/docs", "method": "GET", "description": "API documentation"},
            {"path": "/redoc", "method": "GET", "description": "ReDoc documentation"}
        ]
    }

# Test endpoint untuk PPOB
@app.get("/api/ppob/test")
async def ppob_test():
    """Test endpoint untuk PPOB"""
    return {
        "message": "PPOB endpoint test berhasil",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "ready"
    }

# Test endpoint untuk payment
@app.get("/api/payment/test")
async def payment_test():
    """Test endpoint untuk payment"""
    return {
        "message": "Payment endpoint test berhasil",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "ready"
    }

# Exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )





if __name__ == "__main__":
    # Informasi startup
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    current_user = os.getenv("USER", "system")
    
    print(f"\n🚀 === BK API Server ===")
    print(f"📅 Waktu Start (UTC): {current_time}")
    print(f"👤 User: {current_user}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Base Dir: {BASE_DIR}")
    print(f"🐛 Debug Mode: {'Enabled' if DEBUG else 'Disabled'}")
    
    print(f"\n🌐 Server Configuration:")
    print(f"├── Framework: FastAPI")
    print(f"├── Host: {HOST}")
    print(f"├── Port: {PORT}")
    print(f"├── Hot Reload: {'Enabled' if DEBUG else 'Disabled'}")
    print(f"└── CORS: Enabled")
    
    print(f"\n📚 Available Endpoints:")
    print(f"├── API Docs: http://localhost:{PORT}/docs")
    print(f"├── ReDoc: http://localhost:{PORT}/redoc")
    print(f"├── Health Check: http://localhost:{PORT}/health")
    print(f"├── API Info: http://localhost:{PORT}/api/info")
    print(f"└── Root: http://localhost:{PORT}/")
    
    print(f"\n🔧 Untuk testing:")
    print(f"curl http://localhost:{PORT}/health")
    print(f"curl http://localhost:{PORT}/api/info")
    
    # Jalankan server
    try:
        uvicorn.run(
            "server_simple:app",
            host=HOST,
            port=PORT,
            reload=DEBUG,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Server dihentikan oleh user")
    except Exception as e:
        print(f"\n\n❌ Error menjalankan server: {e}")
        logger.error(f"Server error: {e}")
