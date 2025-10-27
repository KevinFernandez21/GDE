"""
Audit and logging models.
"""
from sqlalchemy import Column, String, Integer, Text, ForeignKey, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import BaseModel


class AuditLog(BaseModel):
    """Audit log model."""
    
    __tablename__ = "audit_logs"
    
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    accion = Column(String(100), nullable=False)
    tabla_afectada = Column(String(50))
    registro_id = Column(Integer)
    valores_anteriores = Column(JSON)
    valores_nuevos = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    fecha = Column(DateTime(timezone=True), default="now()")
    
    # Relationships
    user = relationship("Profile", back_populates="audit_logs")
    
    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, accion={self.accion}, tabla={self.tabla_afectada})>"


class ImportLog(BaseModel):
    """Import log model."""
    
    __tablename__ = "import_logs"
    
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    archivo = Column(String(200), nullable=False)
    tipo_archivo = Column(String(10), nullable=False)  # csv, excel, json
    entidad = Column(String(50), nullable=False)  # products, guias, costos, etc.
    registros_totales = Column(Integer, default=0)
    registros_exitosos = Column(Integer, default=0)
    registros_fallidos = Column(Integer, default=0)
    errores = Column(JSON)  # Error details
    fecha_importacion = Column(DateTime(timezone=True), default="now()")
    fecha_procesamiento = Column(DateTime(timezone=True))
    estado = Column(String(20), default="processing")  # processing, completed, failed
    
    # Relationships
    user = relationship("Profile", back_populates="import_logs")
    
    def __repr__(self) -> str:
        return f"<ImportLog(id={self.id}, archivo={self.archivo}, entidad={self.entidad})>"
