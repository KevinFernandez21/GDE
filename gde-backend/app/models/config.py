"""
Configuration models.
"""
from sqlalchemy import Column, String, Text, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import BaseModel


class CompanyConfig(BaseModel):
    """Company configuration model."""
    
    __tablename__ = "company_config"
    
    nombre_empresa = Column(String(200), nullable=False)
    ruc = Column(String(20), nullable=False)
    direccion = Column(Text)
    telefono = Column(String(20))
    email = Column(String(100))
    website = Column(String(200))
    logo_url = Column(Text)
    moneda = Column(String(10), default="USD")
    idioma = Column(String(10), default="es")
    zona_horaria = Column(String(50), default="America/Guayaquil")
    configuraciones = Column(JSON, default=dict)
    
    def __repr__(self) -> str:
        return f"<CompanyConfig(id={self.id}, nombre={self.nombre_empresa})>"


class UserPreferences(BaseModel):
    """User preferences model."""
    
    __tablename__ = "user_preferences"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), unique=True, nullable=False)
    tema = Column(String(10), default="claro")  # claro, oscuro, auto
    idioma = Column(String(10), default="es")
    zona_horaria = Column(String(50), default="America/Guayaquil")
    notificaciones_email = Column(Boolean, default=True)
    notificaciones_push = Column(Boolean, default=True)
    pagina_inicio = Column(String(50), default="dashboard")
    configuraciones = Column(JSON, default=dict)
    
    # Relationships
    user = relationship("Profile", back_populates="preferences")
    
    def __repr__(self) -> str:
        return f"<UserPreferences(id={self.id}, user_id={self.user_id})>"
