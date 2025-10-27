"""
Cost and accounting models.
"""
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Numeric, Date, ARRAY, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from decimal import Decimal

from .base import BaseModel


class CostCategory(BaseModel):
    """Cost category model."""
    
    __tablename__ = "cost_categories"
    
    name = Column(String(100), nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("cost_categories.id"))
    tipo = Column(String(20), nullable=False)  # gasto, ingreso, costo
    color = Column(String(7))  # Hex color code
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    
    # Relationships
    parent = relationship("CostCategory", remote_side="CostCategory.id", back_populates="children")
    children = relationship("CostCategory", back_populates="parent")
    costos = relationship("Costo", back_populates="category")
    
    def __repr__(self) -> str:
        return f"<CostCategory(id={self.id}, name={self.name}, tipo={self.tipo})>"


class Costo(BaseModel):
    """Cost/expense model."""
    
    __tablename__ = "costos"
    
    fecha = Column(Date, nullable=False)
    categoria_id = Column(Integer, ForeignKey("cost_categories.id"), nullable=False)
    subcategoria = Column(String(100))
    descripcion = Column(Text, nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    proveedor = Column(String(200))
    documento = Column(String(100))
    numero_documento = Column(String(100))
    tipo_documento = Column(String(20))  # factura, recibo, nota_credito, nota_debito, otros
    fecha_documento = Column(Date)
    estado = Column(String(20), default="pendiente")  # pendiente, pagado, anulado
    metodo_pago = Column(String(20), default="transferencia")  # efectivo, transferencia, tarjeta, cheque
    observaciones = Column(Text)
    evidencias = Column(ARRAY(String))  # URLs of scanned documents
    created_by = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    
    # Relationships
    category = relationship("CostCategory", back_populates="costos")
    creator = relationship("Profile", back_populates="costos")
    
    def __repr__(self) -> str:
        return f"<Costo(id={self.id}, descripcion={self.descripcion}, monto={self.monto})>"
