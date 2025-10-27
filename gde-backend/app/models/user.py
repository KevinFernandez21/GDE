"""
User and authentication models.
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .base import BaseModel


class Profile(BaseModel):
    """User profile model."""
    
    __tablename__ = "profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, index=True)
    full_name = Column(String(100))
    email = Column(String(120), unique=True, index=True)
    password_hash = Column(Text)
    role = Column(String(20), default="contable")
    avatar_url = Column(Text)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    products = relationship("Product", back_populates="creator")
    guias = relationship("Guia", back_populates="creator")
    costos = relationship("Costo", back_populates="creator")
    pistoleo_sessions = relationship("PistoleoSession", back_populates="user")
    escaneos = relationship("Escaneo", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    import_logs = relationship("ImportLog", back_populates="user")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)
    notifications = relationship("Notification", back_populates="user")
    notification_settings = relationship("NotificationSettings", back_populates="user", uselist=False)
    
    def __repr__(self) -> str:
        return f"<Profile(id={self.id}, username={self.username}, role={self.role})>"


class Role(BaseModel):
    """Role and permissions model."""
    
    __tablename__ = "roles"
    
    name = Column(String(50), unique=True, nullable=False)
    permissions = Column(JSON, nullable=False, default=dict)
    description = Column(Text)
    
    def __repr__(self) -> str:
        return f"<Role(name={self.name})>"
