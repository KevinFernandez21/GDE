"""
Notification models.
"""
from sqlalchemy import Column, String, Text, ForeignKey, Boolean, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import BaseModel


class Notification(BaseModel):
    """Notification model."""
    
    __tablename__ = "notifications"
    
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50))  # stock_alert, guide_status, system, security
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    data = Column(JSON)  # Additional notification data
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    is_read = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True), default="now()")
    read_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("Profile", back_populates="notifications")
    
    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, title={self.title}, type={self.type})>"


class NotificationSettings(BaseModel):
    """Notification settings model."""
    
    __tablename__ = "notification_settings"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), unique=True, nullable=False)
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    stock_alerts = Column(Boolean, default=True)
    guide_updates = Column(Boolean, default=True)
    system_notifications = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("Profile", back_populates="notification_settings")
    
    def __repr__(self) -> str:
        return f"<NotificationSettings(id={self.id}, user_id={self.user_id})>"


