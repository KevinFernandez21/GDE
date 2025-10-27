"""
Pydantic schemas for request/response validation.
"""
from .common import BaseSchema, PaginationParams, PaginatedResponse
from .user import ProfileCreate, ProfileUpdate, ProfileResponse, RoleCreate, RoleResponse
from .product import (
    ProductCreate, ProductUpdate, ProductResponse, 
    CategoryCreate, CategoryUpdate, CategoryResponse,
    KardexCreate, KardexResponse
)
from .guia import (
    GuiaCreate, GuiaUpdate, GuiaResponse,
    GuiaItemCreate, GuiaItemUpdate, GuiaItemResponse,
    GuiaMovementCreate, GuiaMovementResponse
)
from .pistoleo import (
    PistoleoSessionCreate, PistoleoSessionUpdate, PistoleoSessionResponse,
    EscaneoCreate, EscaneoUpdate, EscaneoResponse
)
from .costo import (
    CostoCreate, CostoUpdate, CostoResponse,
    CostCategoryCreate, CostCategoryUpdate, CostCategoryResponse
)
from .audit import AuditLogResponse, ImportLogResponse
from .config import (
    CompanyConfigCreate, CompanyConfigUpdate, CompanyConfigResponse,
    UserPreferencesCreate, UserPreferencesUpdate, UserPreferencesResponse
)
from .notification import (
    NotificationCreate, NotificationUpdate, NotificationResponse,
    NotificationSettingsUpdate, NotificationSettingsResponse
)

__all__ = [
    "BaseSchema",
    "PaginationParams", 
    "PaginatedResponse",
    "ProfileCreate",
    "ProfileUpdate", 
    "ProfileResponse",
    "RoleCreate",
    "RoleResponse",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "CategoryCreate",
    "CategoryUpdate", 
    "CategoryResponse",
    "KardexCreate",
    "KardexResponse",
    "GuiaCreate",
    "GuiaUpdate",
    "GuiaResponse",
    "GuiaItemCreate",
    "GuiaItemUpdate",
    "GuiaItemResponse", 
    "GuiaMovementCreate",
    "GuiaMovementResponse",
    "PistoleoSessionCreate",
    "PistoleoSessionUpdate",
    "PistoleoSessionResponse",
    "EscaneoCreate",
    "EscaneoUpdate",
    "EscaneoResponse",
    "CostoCreate",
    "CostoUpdate",
    "CostoResponse",
    "CostCategoryCreate",
    "CostCategoryUpdate",
    "CostCategoryResponse",
    "AuditLogResponse",
    "ImportLogResponse",
    "CompanyConfigCreate",
    "CompanyConfigUpdate",
    "CompanyConfigResponse",
    "UserPreferencesCreate",
    "UserPreferencesUpdate",
    "UserPreferencesResponse",
    "NotificationCreate",
    "NotificationUpdate",
    "NotificationResponse",
    "NotificationSettingsUpdate",
    "NotificationSettingsResponse",
]
