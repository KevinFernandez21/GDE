#!/usr/bin/env python3
"""
Startup script for GDE Backend API.
"""
import os
import sys
import uvicorn
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent.parent
sys.path.insert(0, str(app_dir))

from app.core.config import settings


def main():
    """Start the FastAPI application."""
    print("🚀 Starting GDE Backend API...")
    print(f"📊 Environment: {settings.environment}")
    print(f"🔧 Debug mode: {settings.debug}")
    print(f"🌐 Host: 0.0.0.0")
    print(f"🔌 Port: 8000")
    print(f"📚 Docs: http://localhost:8000/docs")
    print(f"❤️  Health: http://localhost:8000/health")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
        access_log=True
    )


if __name__ == "__main__":
    main()
