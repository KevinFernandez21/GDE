"""
Notification schemas.
"""
from typing import Optional, Dict, Any
from pydantic import Field
from datetime import datetime
import uuid

from .common import BaseSchema


class NotificationBase(BaseSchema):
    """Base notification schema."""
    title: str = Field(..., max_length=200, description="Notification title")
    message: str = Field(..., description="Notification message")
    type: Optional[str] = Field(None, description="Notification type")
    priority: str = Field(default="normal", description="Notification priority")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional notification data")


class NotificationCreate(NotificationBase):
    """Notification creation schema."""
    user_id: uuid.UUID = Field(..., description="User ID")


class NotificationUpdate(BaseSchema):
    """Notification update schema."""
    is_read: Optional[bool] = Field(None, description="Whether notification is read")
    read_at: Optional[datetime] = Field(None, description="Read timestamp")


class NotificationResponse(NotificationBase):
    """Notification response schema."""
    id: int = Field(description="Notification ID")
    user_id: uuid.UUID = Field(description="User ID")
    is_read: bool = Field(description="Whether notification is read")
    sent_at: datetime = Field(description="Sent timestamp")
    read_at: Optional[datetime] = Field(None, description="Read timestamp")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class NotificationSettingsBase(BaseSchema):
    """Base notification settings schema."""
    email_notifications: bool = Field(default=True, description="Enable email notifications")
    push_notifications: bool = Field(default=True, description="Enable push notifications")
    stock_alerts: bool = Field(default=True, description="Enable stock alerts")
    guide_updates: bool = Field(default=True, description="Enable guide updates")
    system_notifications: bool = Field(default=True, description="Enable system notifications")


class NotificationSettingsUpdate(NotificationSettingsBase):
    """Notification settings update schema."""
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    stock_alerts: Optional[bool] = None
    guide_updates: Optional[bool] = None
    system_notifications: Optional[bool] = None


class NotificationSettingsResponse(NotificationSettingsBase):
    """Notification settings response schema."""
    id: int = Field(description="Settings ID")
    user_id: uuid.UUID = Field(description="User ID")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class BulkNotificationCreate(BaseSchema):
    """Bulk notification creation schema."""
    title: str = Field(..., max_length=200, description="Notification title")
    message: str = Field(..., description="Notification message")
    type: Optional[str] = Field(None, description="Notification type")
    priority: str = Field(default="normal", description="Notification priority")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional notification data")
    user_ids: list[uuid.UUID] = Field(..., description="List of user IDs")






