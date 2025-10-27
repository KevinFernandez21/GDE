"""
Pistoleo (scanning) schemas.
"""
from typing import Optional, Dict, Any
from pydantic import Field
from datetime import datetime
from decimal import Decimal

from .common import BaseSchema


class PistoleoSessionBase(BaseSchema):
    """Base pistoleo session schema."""
    codigo_qr: str = Field(..., max_length=100, description="QR code")
    nombre_sesion: Optional[str] = Field(None, max_length=100, description="Session name")
    ubicacion: Optional[str] = Field(None, max_length=100, description="Location")
    observaciones: Optional[str] = Field(None, description="Observations")


class PistoleoSessionCreate(PistoleoSessionBase):
    """Pistoleo session creation schema."""
    pass


class PistoleoSessionUpdate(BaseSchema):
    """Pistoleo session update schema."""
    nombre_sesion: Optional[str] = Field(None, max_length=100, description="Session name")
    estado: Optional[str] = Field(None, description="Session status")
    ubicacion: Optional[str] = Field(None, max_length=100, description="Location")
    observaciones: Optional[str] = Field(None, description="Observations")


class PistoleoSessionResponse(PistoleoSessionBase):
    """Pistoleo session response schema."""
    id: int = Field(description="Session ID")
    fecha_inicio: datetime = Field(description="Start date")
    fecha_fin: Optional[datetime] = Field(None, description="End date")
    estado: str = Field(description="Session status")
    escaneos_totales: int = Field(description="Total scans")
    guias_procesadas: int = Field(description="Processed guides")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class EscaneoBase(BaseSchema):
    """Base escaneo schema."""
    session_id: int = Field(..., description="Session ID")
    guia_id: Optional[int] = Field(None, description="Guia ID")
    codigo_barras: str = Field(..., max_length=100, description="Barcode")
    tipo_codigo: str = Field(default="CODE128", max_length=20, description="Code type")
    dispositivo: Optional[str] = Field(None, max_length=100, description="Device")
    ubicacion: Optional[str] = Field(None, max_length=100, description="Location")
    latitud: Optional[Decimal] = Field(None, description="Latitude")
    longitud: Optional[Decimal] = Field(None, description="Longitude")
    precision_gps: Optional[Decimal] = Field(None, description="GPS precision")
    imagen_url: Optional[str] = Field(None, description="Image URL")
    estado_escaneo: str = Field(default="success", description="Scan status")
    mensaje_error: Optional[str] = Field(None, description="Error message")
    extra_data: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class EscaneoCreate(EscaneoBase):
    """Escaneo creation schema."""
    pass


class EscaneoUpdate(BaseSchema):
    """Escaneo update schema."""
    guia_id: Optional[int] = Field(None, description="Guia ID")
    codigo_barras: Optional[str] = Field(None, max_length=100, description="Barcode")
    tipo_codigo: Optional[str] = Field(None, max_length=20, description="Code type")
    dispositivo: Optional[str] = Field(None, max_length=100, description="Device")
    ubicacion: Optional[str] = Field(None, max_length=100, description="Location")
    latitud: Optional[Decimal] = Field(None, description="Latitude")
    longitud: Optional[Decimal] = Field(None, description="Longitude")
    precision_gps: Optional[Decimal] = Field(None, description="GPS precision")
    imagen_url: Optional[str] = Field(None, description="Image URL")
    estado_escaneo: Optional[str] = Field(None, description="Scan status")
    mensaje_error: Optional[str] = Field(None, description="Error message")
    extra_data: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class EscaneoResponse(EscaneoBase):
    """Escaneo response schema."""
    id: int = Field(description="Escaneo ID")
    fecha_escaneo: datetime = Field(description="Scan date")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class SessionStartRequest(BaseSchema):
    """Session start request schema."""
    nombre_sesion: str = Field(..., max_length=100, description="Session name")
    ubicacion: Optional[str] = Field(None, max_length=100, description="Location")
    observaciones: Optional[str] = Field(None, description="Observations")


class SessionEndRequest(BaseSchema):
    """Session end request schema."""
    observaciones: Optional[str] = Field(None, description="End observations")


class ScanRequest(BaseSchema):
    """Scan request schema."""
    codigo_barras: str = Field(..., max_length=100, description="Barcode to scan")
    guia_id: Optional[int] = Field(None, description="Associated guia ID")
    ubicacion: Optional[str] = Field(None, max_length=100, description="Scan location")
    latitud: Optional[Decimal] = Field(None, description="Latitude")
    longitud: Optional[Decimal] = Field(None, description="Longitude")
    precision_gps: Optional[Decimal] = Field(None, description="GPS precision")
    imagen_url: Optional[str] = Field(None, description="Image URL")
    extra_data: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ScanResponse(BaseSchema):
    """Scan response schema."""
    success: bool = Field(description="Whether scan was successful")
    escaneo: Optional[EscaneoResponse] = Field(None, description="Scan record")
    message: str = Field(description="Response message")
    validation_errors: Optional[Dict[str, Any]] = Field(None, description="Validation errors")


class SessionStatsResponse(BaseSchema):
    """Session statistics response schema."""
    session_id: int = Field(description="Session ID")
    total_scans: int = Field(description="Total number of scans")
    successful_scans: int = Field(description="Number of successful scans")
    failed_scans: int = Field(description="Number of failed scans")
    duplicate_scans: int = Field(description="Number of duplicate scans")
    guides_processed: int = Field(description="Number of guides processed")
    session_duration: Optional[int] = Field(None, description="Session duration in minutes")
    start_time: datetime = Field(description="Session start time")
    end_time: Optional[datetime] = Field(None, description="Session end time")
