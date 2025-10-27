"""
Audit and logging schemas.
"""
from typing import Optional, Dict, Any
from pydantic import Field
from datetime import datetime

from .common import BaseSchema


class AuditLogResponse(BaseSchema):
    """Audit log response schema."""
    id: int = Field(description="Audit log ID")
    usuario_id: Optional[str] = Field(None, description="User ID")
    accion: str = Field(description="Action performed")
    tabla_afectada: Optional[str] = Field(None, description="Affected table")
    registro_id: Optional[int] = Field(None, description="Record ID")
    valores_anteriores: Optional[Dict[str, Any]] = Field(None, description="Previous values")
    valores_nuevos: Optional[Dict[str, Any]] = Field(None, description="New values")
    ip_address: Optional[str] = Field(None, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent")
    fecha: datetime = Field(description="Action date")
    created_at: datetime = Field(description="Creation timestamp")


class ImportLogResponse(BaseSchema):
    """Import log response schema."""
    id: int = Field(description="Import log ID")
    usuario_id: str = Field(description="User ID")
    archivo: str = Field(description="File name")
    tipo_archivo: str = Field(description="File type")
    entidad: str = Field(description="Entity type")
    registros_totales: int = Field(description="Total records")
    registros_exitosos: int = Field(description="Successful records")
    registros_fallidos: int = Field(description="Failed records")
    errores: Optional[Dict[str, Any]] = Field(None, description="Error details")
    fecha_importacion: datetime = Field(description="Import date")
    fecha_procesamiento: Optional[datetime] = Field(None, description="Processing date")
    estado: str = Field(description="Processing status")
    created_at: datetime = Field(description="Creation timestamp")


class AuditLogFilter(BaseSchema):
    """Audit log filter schema."""
    usuario_id: Optional[str] = Field(None, description="User ID filter")
    accion: Optional[str] = Field(None, description="Action filter")
    tabla_afectada: Optional[str] = Field(None, description="Table filter")
    fecha_inicio: Optional[datetime] = Field(None, description="Start date filter")
    fecha_fin: Optional[datetime] = Field(None, description="End date filter")
    ip_address: Optional[str] = Field(None, description="IP address filter")


class ImportLogFilter(BaseSchema):
    """Import log filter schema."""
    usuario_id: Optional[str] = Field(None, description="User ID filter")
    tipo_archivo: Optional[str] = Field(None, description="File type filter")
    entidad: Optional[str] = Field(None, description="Entity filter")
    estado: Optional[str] = Field(None, description="Status filter")
    fecha_inicio: Optional[datetime] = Field(None, description="Start date filter")
    fecha_fin: Optional[datetime] = Field(None, description="End date filter")


class SystemStatsResponse(BaseSchema):
    """System statistics response schema."""
    total_users: int = Field(description="Total number of users")
    active_users: int = Field(description="Number of active users")
    total_products: int = Field(description="Total number of products")
    total_guias: int = Field(description="Total number of guides")
    total_scans: int = Field(description="Total number of scans")
    total_costs: int = Field(description="Total number of cost records")
    system_uptime: str = Field(description="System uptime")
    last_backup: Optional[datetime] = Field(None, description="Last backup date")
    database_size: Optional[str] = Field(None, description="Database size")
