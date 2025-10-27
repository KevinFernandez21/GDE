"""
Guia (dispatch guide) schemas.
"""
from typing import Optional, List
from pydantic import Field, EmailStr
from datetime import datetime, date
from decimal import Decimal

from .common import BaseSchema


class GuiaBase(BaseSchema):
    """Base guia schema."""
    codigo: str = Field(..., max_length=100, description="Guide code")
    estado: str = Field(default="pendiente", description="Guide status")
    cliente_nombre: str = Field(..., max_length=200, description="Client name")
    cliente_ruc: Optional[str] = Field(None, max_length=20, description="Client RUC")
    cliente_direccion: Optional[str] = Field(None, description="Client address")
    cliente_telefono: Optional[str] = Field(None, max_length=20, description="Client phone")
    cliente_email: Optional[EmailStr] = Field(None, description="Client email")
    direccion_entrega: Optional[str] = Field(None, description="Delivery address")
    fecha_estimada_entrega: Optional[date] = Field(None, description="Estimated delivery date")
    ubicacion_actual: Optional[str] = Field(None, max_length=100, description="Current location")
    transportista: Optional[str] = Field(None, max_length=100, description="Carrier")
    numero_guia_transportista: Optional[str] = Field(None, max_length=100, description="Carrier guide number")
    peso_total: Optional[Decimal] = Field(None, description="Total weight")
    volumen_total: Optional[Decimal] = Field(None, description="Total volume")
    valor_declarado: Optional[Decimal] = Field(None, description="Declared value")
    observaciones: Optional[str] = Field(None, description="Observations")


class GuiaCreate(GuiaBase):
    """Guia creation schema."""
    pass


class GuiaUpdate(BaseSchema):
    """Guia update schema."""
    codigo: Optional[str] = Field(None, max_length=100, description="Guide code")
    estado: Optional[str] = Field(None, description="Guide status")
    cliente_nombre: Optional[str] = Field(None, max_length=200, description="Client name")
    cliente_ruc: Optional[str] = Field(None, max_length=20, description="Client RUC")
    cliente_direccion: Optional[str] = Field(None, description="Client address")
    cliente_telefono: Optional[str] = Field(None, max_length=20, description="Client phone")
    cliente_email: Optional[EmailStr] = Field(None, description="Client email")
    direccion_entrega: Optional[str] = Field(None, description="Delivery address")
    fecha_estimada_entrega: Optional[date] = Field(None, description="Estimated delivery date")
    fecha_entrega_real: Optional[datetime] = Field(None, description="Actual delivery date")
    ubicacion_actual: Optional[str] = Field(None, max_length=100, description="Current location")
    transportista: Optional[str] = Field(None, max_length=100, description="Carrier")
    numero_guia_transportista: Optional[str] = Field(None, max_length=100, description="Carrier guide number")
    peso_total: Optional[Decimal] = Field(None, description="Total weight")
    volumen_total: Optional[Decimal] = Field(None, description="Total volume")
    valor_declarado: Optional[Decimal] = Field(None, description="Declared value")
    observaciones: Optional[str] = Field(None, description="Observations")


class GuiaResponse(GuiaBase):
    """Guia response schema."""
    id: int = Field(description="Guia ID")
    fecha_creacion: datetime = Field(description="Creation date")
    fecha_entrega_real: Optional[datetime] = Field(None, description="Actual delivery date")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class GuiaItemBase(BaseSchema):
    """Base guia item schema."""
    guia_id: int = Field(..., description="Guia ID")
    product_id: int = Field(..., description="Product ID")
    cantidad: int = Field(..., description="Quantity")
    precio_unitario: Optional[Decimal] = Field(None, description="Unit price")
    descuento: Decimal = Field(default=0, description="Discount")
    subtotal: Optional[Decimal] = Field(None, description="Subtotal")
    observaciones: Optional[str] = Field(None, description="Observations")


class GuiaItemCreate(GuiaItemBase):
    """Guia item creation schema."""
    pass


class GuiaItemUpdate(BaseSchema):
    """Guia item update schema."""
    product_id: Optional[int] = Field(None, description="Product ID")
    cantidad: Optional[int] = Field(None, description="Quantity")
    precio_unitario: Optional[Decimal] = Field(None, description="Unit price")
    descuento: Optional[Decimal] = Field(None, description="Discount")
    subtotal: Optional[Decimal] = Field(None, description="Subtotal")
    observaciones: Optional[str] = Field(None, description="Observations")


class GuiaItemResponse(GuiaItemBase):
    """Guia item response schema."""
    id: int = Field(description="Guia item ID")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class GuiaMovementBase(BaseSchema):
    """Base guia movement schema."""
    guia_id: int = Field(..., description="Guia ID")
    accion: str = Field(..., max_length=50, description="Action")
    ubicacion: Optional[str] = Field(None, max_length=100, description="Location")
    observaciones: Optional[str] = Field(None, description="Observations")
    evidencias: Optional[List[str]] = Field(None, description="Evidence URLs")
    fecha_movimiento: Optional[datetime] = Field(None, description="Movement date")


class GuiaMovementCreate(GuiaMovementBase):
    """Guia movement creation schema."""
    pass


class GuiaMovementUpdate(BaseSchema):
    """Guia movement update schema."""
    accion: Optional[str] = Field(None, max_length=50, description="Action")
    ubicacion: Optional[str] = Field(None, max_length=100, description="Location")
    observaciones: Optional[str] = Field(None, description="Observations")
    evidencias: Optional[List[str]] = Field(None, description="Evidence URLs")
    fecha_movimiento: Optional[datetime] = Field(None, description="Movement date")


class GuiaMovementResponse(GuiaMovementBase):
    """Guia movement response schema."""
    id: int = Field(description="Guia movement ID")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class GuiaStatusUpdate(BaseSchema):
    """Guia status update schema."""
    estado: str = Field(..., description="New status")
    observaciones: Optional[str] = Field(None, description="Status change observations")
    ubicacion: Optional[str] = Field(None, description="Current location")
    evidencias: Optional[List[str]] = Field(None, description="Evidence URLs")


class GuiaTrackingResponse(BaseSchema):
    """Guia tracking response schema."""
    guia_id: int = Field(description="Guia ID")
    codigo: str = Field(description="Guide code")
    estado: str = Field(description="Current status")
    ubicacion_actual: Optional[str] = Field(None, description="Current location")
    fecha_creacion: datetime = Field(description="Creation date")
    fecha_estimada_entrega: Optional[date] = Field(None, description="Estimated delivery date")
    fecha_entrega_real: Optional[datetime] = Field(None, description="Actual delivery date")
    movimientos: List[GuiaMovementResponse] = Field(description="Movement history")
