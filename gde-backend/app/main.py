"""
Main FastAPI application for GDE Backend.
"""
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .core.config import settings
from .core.database import create_tables
from .core.exceptions import GDEException, handle_gde_exception
from .api.v1.auth import router as auth_router
from .api.v1.dashboard import router as dashboard_router
from .api.v1.products import router as products_router
from .api.v1.guias import router as guias_router
from .api.v1.kardex import router as kardex_router
from .api.v1.pistoleo import router as pistoleo_router
from .api.v1.costos import router as costos_router
from .api.v1.notifications import router as notifications_router
from .api.v1.reports import router as reports_router
from .api.v1.files import router as files_router
from .api.v1.audit import router as audit_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    
    Args:
        app: FastAPI application instance
    """
    # Startup
    logger.info("Starting GDE Backend API...")
    
    # Create database tables
    try:
        create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
    
    logger.info("GDE Backend API started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down GDE Backend API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API para el sistema GDE - Gestión de Inventario y Despacho",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# Add trusted host middleware
if not settings.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure with your domain in production
    )


# Exception handlers
@app.exception_handler(GDEException)
async def gde_exception_handler(request: Request, exc: GDEException):
    """Handle GDE custom exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "details": exc.details
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Validation error",
            "details": exc.errors()
        }
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "details": {}
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error",
            "details": {}
        }
    )


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version,
        "environment": settings.environment
    }


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint.
    
    Returns:
        dict: API information
    """
    return {
        "message": "GDE Backend API",
        "version": settings.app_version,
        "docs_url": "/docs" if settings.debug else "Documentation not available in production",
        "health_check": "/health"
    }


# Include API routers
app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    dashboard_router,
    prefix="/api/v1"
)

app.include_router(
    products_router,
    prefix="/api/v1"
)

app.include_router(
    guias_router,
    prefix="/api/v1"
)

app.include_router(
    kardex_router,
    prefix="/api/v1"
)

app.include_router(
    pistoleo_router,
    prefix="/api/v1"
)

app.include_router(
    costos_router,
    prefix="/api/v1"
)

app.include_router(
    notifications_router,
    prefix="/api/v1"
)

app.include_router(
    reports_router,
    prefix="/api/v1"
)

app.include_router(
    files_router,
    prefix="/api/v1"
)

app.include_router(
    audit_router,
    prefix="/api/v1"
)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
