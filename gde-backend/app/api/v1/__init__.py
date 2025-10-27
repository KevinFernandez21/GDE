"""
API v1 package.
"""
from .auth import router as auth_router
from .products import router as products_router
from .guias import router as guias_router
from .kardex import router as kardex_router
from .pistoleo import router as pistoleo_router
from .costos import router as costos_router
from .notifications import router as notifications_router
from .reports import router as reports_router
from .files import router as files_router
from .audit import router as audit_router

__all__ = [
    "auth_router",
    "products_router",
    "guias_router",
    "kardex_router",
    "pistoleo_router",
    "costos_router",
    "notifications_router",
    "reports_router",
    "files_router",
    "audit_router",
]
