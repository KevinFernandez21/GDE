"""
Product and inventory schemas.
"""
from typing import Optional, List, Dict, Any
from pydantic import Field
from datetime import datetime
from decimal import Decimal

from .common import BaseSchema


class CategoryBase(BaseSchema):
    """Base category schema."""
    name: str = Field(..., max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    parent_id: Optional[int] = Field(None, description="Parent category ID")
    color: Optional[str] = Field(None, max_length=7, description="Hex color code")
    icon: Optional[str] = Field(None, max_length=50, description="Icon name")
    sort_order: int = Field(default=0, description="Sort order")
    is_active: bool = Field(default=True, description="Whether category is active")


class CategoryCreate(CategoryBase):
    """Category creation schema."""
    pass


class CategoryUpdate(BaseSchema):
    """Category update schema."""
    name: Optional[str] = Field(None, max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    parent_id: Optional[int] = Field(None, description="Parent category ID")
    color: Optional[str] = Field(None, max_length=7, description="Hex color code")
    icon: Optional[str] = Field(None, max_length=50, description="Icon name")
    sort_order: Optional[int] = Field(None, description="Sort order")
    is_active: Optional[bool] = Field(None, description="Whether category is active")


class CategoryResponse(CategoryBase):
    """Category response schema."""
    id: int = Field(description="Category ID")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class ProductBase(BaseSchema):
    """Base product schema."""
    code: str = Field(..., max_length=50, description="Product code")
    name: str = Field(..., max_length=200, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category_id: Optional[int] = Field(None, description="Category ID")
    stock_actual: int = Field(default=0, description="Current stock")
    stock_minimo: int = Field(default=10, description="Minimum stock")
    stock_maximo: Optional[int] = Field(None, description="Maximum stock")
    precio_compra: Decimal = Field(default=0, description="Purchase price")
    precio_venta: Decimal = Field(default=0, description="Sale price")
    ubicacion_bodega: Optional[str] = Field(None, max_length=100, description="Warehouse location")
    proveedor: Optional[str] = Field(None, max_length=100, description="Supplier")
    marca: Optional[str] = Field(None, max_length=100, description="Brand")
    modelo: Optional[str] = Field(None, max_length=100, description="Model")
    unidad_medida: str = Field(default="UNIDAD", max_length=20, description="Unit of measure")
    peso: Optional[Decimal] = Field(None, description="Weight")
    dimensiones: Optional[Dict[str, Any]] = Field(None, description="Dimensions")
    codigo_barras: Optional[str] = Field(None, max_length=100, description="Barcode")
    imagenes: Optional[List[str]] = Field(None, description="Image URLs")
    status: str = Field(default="active", description="Product status")
    extra_data: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ProductCreate(ProductBase):
    """Product creation schema."""
    pass


class ProductUpdate(BaseSchema):
    """Product update schema."""
    code: Optional[str] = Field(None, max_length=50, description="Product code")
    name: Optional[str] = Field(None, max_length=200, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category_id: Optional[int] = Field(None, description="Category ID")
    stock_actual: Optional[int] = Field(None, description="Current stock")
    stock_minimo: Optional[int] = Field(None, description="Minimum stock")
    stock_maximo: Optional[int] = Field(None, description="Maximum stock")
    precio_compra: Optional[Decimal] = Field(None, description="Purchase price")
    precio_venta: Optional[Decimal] = Field(None, description="Sale price")
    ubicacion_bodega: Optional[str] = Field(None, max_length=100, description="Warehouse location")
    proveedor: Optional[str] = Field(None, max_length=100, description="Supplier")
    marca: Optional[str] = Field(None, max_length=100, description="Brand")
    modelo: Optional[str] = Field(None, max_length=100, description="Model")
    unidad_medida: Optional[str] = Field(None, max_length=20, description="Unit of measure")
    peso: Optional[Decimal] = Field(None, description="Weight")
    dimensiones: Optional[Dict[str, Any]] = Field(None, description="Dimensions")
    codigo_barras: Optional[str] = Field(None, max_length=100, description="Barcode")
    imagenes: Optional[List[str]] = Field(None, description="Image URLs")
    status: Optional[str] = Field(None, description="Product status")
    extra_data: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ProductResponse(ProductBase):
    """Product response schema."""
    id: int = Field(description="Product ID")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class KardexBase(BaseSchema):
    """Base kardex schema."""
    product_id: int = Field(..., description="Product ID")
    tipo_movimiento: str = Field(..., description="Movement type")
    documento_asociado: Optional[str] = Field(None, max_length=100, description="Associated document")
    referencia: Optional[str] = Field(None, max_length=200, description="Reference")
    cantidad: int = Field(..., description="Quantity")
    saldo_anterior: int = Field(..., description="Previous balance")
    saldo_actual: int = Field(..., description="Current balance")
    costo_unitario: Optional[Decimal] = Field(None, description="Unit cost")
    costo_promedio: Optional[Decimal] = Field(None, description="Average cost")
    valor_total: Optional[Decimal] = Field(None, description="Total value")
    fecha_movimiento: Optional[datetime] = Field(None, description="Movement date")
    observaciones: Optional[str] = Field(None, description="Observations")


class KardexCreate(KardexBase):
    """Kardex creation schema."""
    pass


class KardexResponse(KardexBase):
    """Kardex response schema."""
    id: int = Field(description="Kardex ID")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class StockAlertResponse(BaseSchema):
    """Stock alert response schema."""
    product_id: int = Field(description="Product ID")
    product_name: str = Field(description="Product name")
    current_stock: int = Field(description="Current stock")
    minimum_stock: int = Field(description="Minimum stock")
    alert_type: str = Field(description="Alert type (low_stock, out_of_stock)")
    severity: str = Field(description="Alert severity (warning, critical)")


class InventoryReportResponse(BaseSchema):
    """Inventory report response schema."""
    total_products: int = Field(description="Total number of products")
    total_value: Decimal = Field(description="Total inventory value")
    low_stock_products: int = Field(description="Number of low stock products")
    out_of_stock_products: int = Field(description="Number of out of stock products")
    categories_summary: List[Dict[str, Any]] = Field(description="Summary by category")
