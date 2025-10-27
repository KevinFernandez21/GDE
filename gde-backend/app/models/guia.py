"""
Guia (dispatch guide) models.
"""
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Numeric, Date, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from decimal import Decimal

from .base import BaseModel


class Guia(BaseModel):
    """Dispatch guide model."""
    
    __tablename__ = "guias"
    
    codigo = Column(String(100), unique=True, nullable=False, index=True)
    estado = Column(String(20), default="pendiente")  # pendiente, en_transito, entregada, devuelta, cancelada
    cliente_nombre = Column(String(200), nullable=False)
    cliente_ruc = Column(String(20))
    cliente_direccion = Column(Text)
    cliente_telefono = Column(String(20))
    cliente_email = Column(String(100))
    direccion_entrega = Column(Text)
    fecha_creacion = Column(DateTime(timezone=True), default="now()")
    fecha_estimada_entrega = Column(Date)
    fecha_entrega_real = Column(DateTime(timezone=True))
    ubicacion_actual = Column(String(100))
    transportista = Column(String(100))
    numero_guia_transportista = Column(String(100))
    peso_total = Column(Numeric(8, 2))
    volumen_total = Column(Numeric(8, 2))
    valor_declarado = Column(Numeric(10, 2))
    observaciones = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    
    # Relationships
    creator = relationship("Profile", back_populates="guias")
    items = relationship("GuiaItem", back_populates="guia", cascade="all, delete-orphan")
    movimientos = relationship("GuiaMovement", back_populates="guia", cascade="all, delete-orphan")
    escaneos = relationship("Escaneo", back_populates="guia")
    
    def __repr__(self) -> str:
        return f"<Guia(id={self.id}, codigo={self.codigo}, estado={self.estado})>"


class GuiaItem(BaseModel):
    """Guia item model."""
    
    __tablename__ = "guia_items"
    
    guia_id = Column(Integer, ForeignKey("guias.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2))
    descuento = Column(Numeric(10, 2), default=0)
    subtotal = Column(Numeric(12, 2))
    observaciones = Column(Text)
    
    # Relationships
    guia = relationship("Guia", back_populates="items")
    product = relationship("Product", back_populates="guia_items")
    
    def __repr__(self) -> str:
        return f"<GuiaItem(id={self.id}, guia_id={self.guia_id}, product_id={self.product_id})>"


class GuiaMovement(BaseModel):
    """Guia movement/history model."""
    
    __tablename__ = "guia_movimientos"
    
    guia_id = Column(Integer, ForeignKey("guias.id"), nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    accion = Column(String(50), nullable=False)
    ubicacion = Column(String(100))
    observaciones = Column(Text)
    evidencias = Column(ARRAY(String))  # URLs of photos/receipts
    fecha_movimiento = Column(DateTime(timezone=True), default="now()")
    
    # Relationships
    guia = relationship("Guia", back_populates="movimientos")
    user = relationship("Profile")
    
    def __repr__(self) -> str:
        return f"<GuiaMovement(id={self.id}, guia_id={self.guia_id}, accion={self.accion})>"
