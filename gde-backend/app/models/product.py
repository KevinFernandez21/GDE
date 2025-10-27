"""
Product and inventory models.
"""
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Numeric, Boolean, JSON, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from decimal import Decimal

from .base import BaseModel


class Category(BaseModel):
    """Product category model."""
    
    __tablename__ = "categories"
    
    name = Column(String(100), nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("categories.id"))
    color = Column(String(7))  # Hex color code
    icon = Column(String(50))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    parent = relationship("Category", remote_side="Category.id", back_populates="children")
    children = relationship("Category", back_populates="parent")
    products = relationship("Product", back_populates="category")
    
    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name={self.name})>"


class Product(BaseModel):
    """Product model."""
    
    __tablename__ = "products"
    
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"))
    stock_actual = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=10)
    stock_maximo = Column(Integer)
    precio_compra = Column(Numeric(10, 2), default=0)
    precio_venta = Column(Numeric(10, 2), default=0)
    ubicacion_bodega = Column(String(100))
    proveedor = Column(String(100))
    marca = Column(String(100))
    modelo = Column(String(100))
    unidad_medida = Column(String(20), default="UNIDAD")
    peso = Column(Numeric(8, 2))
    dimensiones = Column(JSON)
    codigo_barras = Column(String(100))
    imagenes = Column(ARRAY(String))
    status = Column(String(20), default="active")
    extra_data = Column(JSON)
    created_by = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    
    # Relationships
    category = relationship("Category", back_populates="products")
    creator = relationship("Profile", back_populates="products")
    kardex_entries = relationship("Kardex", back_populates="product")
    guia_items = relationship("GuiaItem", back_populates="product")
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, code={self.code}, name={self.name})>"


class Kardex(BaseModel):
    """Inventory movement (Kardex) model."""
    
    __tablename__ = "kardex"
    
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    tipo_movimiento = Column(String(20), nullable=False)  # entrada, salida, ajuste, transferencia
    documento_asociado = Column(String(100))
    referencia = Column(String(200))
    cantidad = Column(Integer, nullable=False)
    saldo_anterior = Column(Integer, nullable=False)
    saldo_actual = Column(Integer, nullable=False)
    costo_unitario = Column(Numeric(10, 2))
    costo_promedio = Column(Numeric(10, 2))
    valor_total = Column(Numeric(12, 2))
    fecha_movimiento = Column(String, default="now()")
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    observaciones = Column(Text)
    
    # Relationships
    product = relationship("Product", back_populates="kardex_entries")
    user = relationship("Profile")
    
    def __repr__(self) -> str:
        return f"<Kardex(id={self.id}, product_id={self.product_id}, tipo={self.tipo_movimiento})>"
