"""
Cost and accounting schemas.
"""
from typing import Optional, List
from pydantic import Field
from datetime import date
from decimal import Decimal

from .common import BaseSchema


class CostCategoryBase(BaseSchema):
    """Base cost category schema."""
    name: str = Field(..., max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    parent_id: Optional[int] = Field(None, description="Parent category ID")
    tipo: str = Field(..., description="Category type (gasto, ingreso, costo)")
    color: Optional[str] = Field(None, max_length=7, description="Hex color code")
    is_active: bool = Field(default=True, description="Whether category is active")
    sort_order: int = Field(default=0, description="Sort order")


class CostCategoryCreate(CostCategoryBase):
    """Cost category creation schema."""
    pass


class CostCategoryUpdate(BaseSchema):
    """Cost category update schema."""
    name: Optional[str] = Field(None, max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    parent_id: Optional[int] = Field(None, description="Parent category ID")
    tipo: Optional[str] = Field(None, description="Category type")
    color: Optional[str] = Field(None, max_length=7, description="Hex color code")
    is_active: Optional[bool] = Field(None, description="Whether category is active")
    sort_order: Optional[int] = Field(None, description="Sort order")


class CostCategoryResponse(CostCategoryBase):
    """Cost category response schema."""
    id: int = Field(description="Category ID")
    created_at: str = Field(description="Creation timestamp")
    updated_at: str = Field(description="Last update timestamp")


class CostoBase(BaseSchema):
    """Base costo schema."""
    fecha: date = Field(..., description="Date")
    categoria_id: int = Field(..., description="Category ID")
    subcategoria: Optional[str] = Field(None, max_length=100, description="Subcategory")
    descripcion: str = Field(..., description="Description")
    monto: Decimal = Field(..., description="Amount")
    proveedor: Optional[str] = Field(None, max_length=200, description="Supplier")
    documento: Optional[str] = Field(None, max_length=100, description="Document type")
    numero_documento: Optional[str] = Field(None, max_length=100, description="Document number")
    tipo_documento: Optional[str] = Field(None, description="Document type")
    fecha_documento: Optional[date] = Field(None, description="Document date")
    estado: str = Field(default="pendiente", description="Status")
    metodo_pago: str = Field(default="transferencia", description="Payment method")
    observaciones: Optional[str] = Field(None, description="Observations")
    evidencias: Optional[List[str]] = Field(None, description="Evidence URLs")


class CostoCreate(CostoBase):
    """Costo creation schema."""
    pass


class CostoUpdate(BaseSchema):
    """Costo update schema."""
    fecha: Optional[date] = Field(None, description="Date")
    categoria_id: Optional[int] = Field(None, description="Category ID")
    subcategoria: Optional[str] = Field(None, max_length=100, description="Subcategory")
    descripcion: Optional[str] = Field(None, description="Description")
    monto: Optional[Decimal] = Field(None, description="Amount")
    proveedor: Optional[str] = Field(None, max_length=200, description="Supplier")
    documento: Optional[str] = Field(None, max_length=100, description="Document type")
    numero_documento: Optional[str] = Field(None, max_length=100, description="Document number")
    tipo_documento: Optional[str] = Field(None, description="Document type")
    fecha_documento: Optional[date] = Field(None, description="Document date")
    estado: Optional[str] = Field(None, description="Status")
    metodo_pago: Optional[str] = Field(None, description="Payment method")
    observaciones: Optional[str] = Field(None, description="Observations")
    evidencias: Optional[List[str]] = Field(None, description="Evidence URLs")


class CostoResponse(CostoBase):
    """Costo response schema."""
    id: int = Field(description="Costo ID")
    created_at: str = Field(description="Creation timestamp")
    updated_at: str = Field(description="Last update timestamp")


class FinancialReportRequest(BaseSchema):
    """Financial report request schema."""
    fecha_inicio: date = Field(..., description="Start date")
    fecha_fin: date = Field(..., description="End date")
    categoria_id: Optional[int] = Field(None, description="Category ID filter")
    tipo: Optional[str] = Field(None, description="Type filter")
    estado: Optional[str] = Field(None, description="Status filter")
    group_by: Optional[str] = Field(None, description="Group by field")


class FinancialReportResponse(BaseSchema):
    """Financial report response schema."""
    periodo: str = Field(description="Report period")
    total_ingresos: Decimal = Field(description="Total income")
    total_gastos: Decimal = Field(description="Total expenses")
    total_costos: Decimal = Field(description="Total costs")
    balance: Decimal = Field(description="Balance")
    categorias: List[dict] = Field(description="Summary by category")
    tendencia: List[dict] = Field(description="Trend data")


class CostAnalysisResponse(BaseSchema):
    """Cost analysis response schema."""
    categoria_id: int = Field(description="Category ID")
    categoria_nombre: str = Field(description="Category name")
    total_monto: Decimal = Field(description="Total amount")
    cantidad_registros: int = Field(description="Number of records")
    promedio_monto: Decimal = Field(description="Average amount")
    porcentaje_total: Decimal = Field(description="Percentage of total")
    tendencia_mensual: List[dict] = Field(description="Monthly trend")


class BudgetAlertResponse(BaseSchema):
    """Budget alert response schema."""
    categoria_id: int = Field(description="Category ID")
    categoria_nombre: str = Field(description="Category name")
    presupuesto: Decimal = Field(description="Budget amount")
    gastado: Decimal = Field(description="Spent amount")
    porcentaje_usado: Decimal = Field(description="Percentage used")
    alerta_tipo: str = Field(description="Alert type")
    severidad: str = Field(description="Alert severity")
