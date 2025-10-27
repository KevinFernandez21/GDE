"""
Pistoleo (scanning) models.
"""
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Numeric, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from decimal import Decimal

from .base import BaseModel


class PistoleoSession(BaseModel):
    """Pistoleo session model."""
    
    __tablename__ = "pistoleo_sessions"
    
    codigo_qr = Column(String(100), unique=True, nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    nombre_sesion = Column(String(100))
    fecha_inicio = Column(DateTime(timezone=True), default="now()")
    fecha_fin = Column(DateTime(timezone=True))
    estado = Column(String(20), default="active")  # active, completed, cancelled
    escaneos_totales = Column(Integer, default=0)
    guias_procesadas = Column(Integer, default=0)
    ubicacion = Column(String(100))
    observaciones = Column(Text)
    
    # Relationships
    user = relationship("Profile", back_populates="pistoleo_sessions")
    escaneos = relationship("Escaneo", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<PistoleoSession(id={self.id}, codigo_qr={self.codigo_qr}, estado={self.estado})>"


class Escaneo(BaseModel):
    """Scan record model."""
    
    __tablename__ = "escaneos"
    
    session_id = Column(Integer, ForeignKey("pistoleo_sessions.id"), nullable=False)
    guia_id = Column(Integer, ForeignKey("guias.id"))
    codigo_barras = Column(String(100), nullable=False)
    tipo_codigo = Column(String(20), default="CODE128")
    fecha_escaneo = Column(DateTime(timezone=True), default="now()")
    dispositivo = Column(String(100))
    ubicacion = Column(String(100))
    latitud = Column(Numeric(10, 8))
    longitud = Column(Numeric(11, 8))
    precision_gps = Column(Numeric(5, 2))
    imagen_url = Column(Text)
    estado_escaneo = Column(String(20), default="success")  # success, error, duplicate
    mensaje_error = Column(Text)
    extra_data = Column(JSON)
    
    # Relationships
    session = relationship("PistoleoSession", back_populates="escaneos")
    guia = relationship("Guia", back_populates="escaneos")
    user = relationship("Profile", back_populates="escaneos")
    
    def __repr__(self) -> str:
        return f"<Escaneo(id={self.id}, session_id={self.session_id}, codigo_barras={self.codigo_barras})>"
