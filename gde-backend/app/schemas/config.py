"""
Configuration schemas.
"""
from typing import Optional, Dict, Any
from pydantic import Field, EmailStr

from .common import BaseSchema


class CompanyConfigBase(BaseSchema):
    """Base company config schema."""
    nombre_empresa: str = Field(..., max_length=200, description="Company name")
    ruc: str = Field(..., max_length=20, description="Company RUC")
    direccion: Optional[str] = Field(None, description="Company address")
    telefono: Optional[str] = Field(None, max_length=20, description="Company phone")
    email: Optional[EmailStr] = Field(None, description="Company email")
    website: Optional[str] = Field(None, max_length=200, description="Company website")
    logo_url: Optional[str] = Field(None, description="Logo URL")
    moneda: str = Field(default="USD", max_length=10, description="Currency")
    idioma: str = Field(default="es", max_length=10, description="Language")
    zona_horaria: str = Field(default="America/Guayaquil", max_length=50, description="Time zone")
    configuraciones: Dict[str, Any] = Field(default_factory=dict, description="Additional configurations")


class CompanyConfigCreate(CompanyConfigBase):
    """Company config creation schema."""
    pass


class CompanyConfigUpdate(BaseSchema):
    """Company config update schema."""
    nombre_empresa: Optional[str] = Field(None, max_length=200, description="Company name")
    ruc: Optional[str] = Field(None, max_length=20, description="Company RUC")
    direccion: Optional[str] = Field(None, description="Company address")
    telefono: Optional[str] = Field(None, max_length=20, description="Company phone")
    email: Optional[EmailStr] = Field(None, description="Company email")
    website: Optional[str] = Field(None, max_length=200, description="Company website")
    logo_url: Optional[str] = Field(None, description="Logo URL")
    moneda: Optional[str] = Field(None, max_length=10, description="Currency")
    idioma: Optional[str] = Field(None, max_length=10, description="Language")
    zona_horaria: Optional[str] = Field(None, max_length=50, description="Time zone")
    configuraciones: Optional[Dict[str, Any]] = Field(None, description="Additional configurations")


class CompanyConfigResponse(CompanyConfigBase):
    """Company config response schema."""
    id: int = Field(description="Config ID")
    created_at: str = Field(description="Creation timestamp")
    updated_at: str = Field(description="Last update timestamp")


class UserPreferencesBase(BaseSchema):
    """Base user preferences schema."""
    tema: str = Field(default="claro", description="Theme preference")
    idioma: str = Field(default="es", description="Language preference")
    zona_horaria: str = Field(default="America/Guayaquil", description="Time zone preference")
    notificaciones_email: bool = Field(default=True, description="Email notifications enabled")
    notificaciones_push: bool = Field(default=True, description="Push notifications enabled")
    pagina_inicio: str = Field(default="dashboard", description="Home page preference")
    configuraciones: Dict[str, Any] = Field(default_factory=dict, description="Additional preferences")


class UserPreferencesCreate(UserPreferencesBase):
    """User preferences creation schema."""
    user_id: str = Field(..., description="User ID")


class UserPreferencesUpdate(BaseSchema):
    """User preferences update schema."""
    tema: Optional[str] = Field(None, description="Theme preference")
    idioma: Optional[str] = Field(None, description="Language preference")
    zona_horaria: Optional[str] = Field(None, description="Time zone preference")
    notificaciones_email: Optional[bool] = Field(None, description="Email notifications enabled")
    notificaciones_push: Optional[bool] = Field(None, description="Push notifications enabled")
    pagina_inicio: Optional[str] = Field(None, description="Home page preference")
    configuraciones: Optional[Dict[str, Any]] = Field(None, description="Additional preferences")


class UserPreferencesResponse(UserPreferencesBase):
    """User preferences response schema."""
    id: int = Field(description="Preferences ID")
    user_id: str = Field(description="User ID")
    created_at: str = Field(description="Creation timestamp")
    updated_at: str = Field(description="Last update timestamp")


class SystemSettingsResponse(BaseSchema):
    """System settings response schema."""
    company_config: CompanyConfigResponse = Field(description="Company configuration")
    default_preferences: UserPreferencesResponse = Field(description="Default user preferences")
    available_themes: list = Field(description="Available themes")
    available_languages: list = Field(description="Available languages")
    available_timezones: list = Field(description="Available time zones")
    supported_currencies: list = Field(description="Supported currencies")
