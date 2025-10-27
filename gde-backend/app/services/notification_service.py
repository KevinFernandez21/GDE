"""
Notification service for managing user notifications.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from ..models.notification import Notification, NotificationSettings
from ..schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationSettingsUpdate,
    BulkNotificationCreate
)
from ..core.exceptions import NotFoundError


class NotificationService:
    """Service for managing notifications."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_notification(self, notification_data: NotificationCreate) -> Notification:
        """
        Create a new notification.
        
        Args:
            notification_data: Notification creation data
            
        Returns:
            Notification: Created notification
        """
        notification = Notification(**notification_data.model_dump())
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
    
    def create_bulk_notifications(self, bulk_data: BulkNotificationCreate) -> List[Notification]:
        """
        Create multiple notifications for different users.
        
        Args:
            bulk_data: Bulk notification creation data
            
        Returns:
            List[Notification]: Created notifications
        """
        notifications = []
        
        for user_id in bulk_data.user_ids:
            notification = Notification(
                user_id=user_id,
                title=bulk_data.title,
                message=bulk_data.message,
                type=bulk_data.type,
                priority=bulk_data.priority,
                data=bulk_data.data
            )
            self.db.add(notification)
            notifications.append(notification)
        
        self.db.commit()
        
        for notification in notifications:
            self.db.refresh(notification)
        
        return notifications
    
    def get_user_notifications(
        self,
        user_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        is_read: Optional[bool] = None,
        type_filter: Optional[str] = None
    ) -> List[Notification]:
        """
        Get notifications for a user.
        
        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Number of records to return
            is_read: Filter by read status
            type_filter: Filter by notification type
            
        Returns:
            List[Notification]: List of notifications
        """
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        
        if is_read is not None:
            query = query.filter(Notification.is_read == is_read)
        
        if type_filter:
            query = query.filter(Notification.type == type_filter)
        
        return query.order_by(Notification.sent_at.desc()).offset(skip).limit(limit).all()
    
    def get_notification(self, notification_id: int) -> Optional[Notification]:
        """
        Get notification by ID.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            Optional[Notification]: Notification if found
        """
        return self.db.query(Notification).filter(Notification.id == notification_id).first()
    
    def mark_as_read(self, notification_id: int) -> Optional[Notification]:
        """
        Mark notification as read.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            Optional[Notification]: Updated notification if found
        """
        notification = self.get_notification(notification_id)
        if not notification:
            return None
        
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(notification)
        
        return notification
    
    def mark_all_as_read(self, user_id: uuid.UUID) -> int:
        """
        Mark all notifications as read for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            int: Number of notifications marked as read
        """
        unread_notifications = self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).all()
        
        count = 0
        for notification in unread_notifications:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            count += 1
        
        if count > 0:
            self.db.commit()
        
        return count
    
    def delete_notification(self, notification_id: int) -> bool:
        """
        Delete notification.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        notification = self.get_notification(notification_id)
        if not notification:
            return False
        
        self.db.delete(notification)
        self.db.commit()
        
        return True
    
    def get_unread_count(self, user_id: uuid.UUID) -> int:
        """
        Get count of unread notifications for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            int: Number of unread notifications
        """
        return self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).count()
    
    # Notification Settings
    def get_user_settings(self, user_id: uuid.UUID) -> Optional[NotificationSettings]:
        """
        Get notification settings for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[NotificationSettings]: User notification settings if found
        """
        return self.db.query(NotificationSettings).filter(
            NotificationSettings.user_id == user_id
        ).first()
    
    def create_default_settings(self, user_id: uuid.UUID) -> NotificationSettings:
        """
        Create default notification settings for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            NotificationSettings: Created settings
        """
        settings = NotificationSettings(user_id=user_id)
        
        self.db.add(settings)
        self.db.commit()
        self.db.refresh(settings)
        
        return settings
    
    def update_user_settings(
        self,
        user_id: uuid.UUID,
        settings_data: NotificationSettingsUpdate
    ) -> NotificationSettings:
        """
        Update notification settings for a user.
        
        Args:
            user_id: User ID
            settings_data: Settings update data
            
        Returns:
            NotificationSettings: Updated settings
        """
        settings = self.get_user_settings(user_id)
        
        if not settings:
            settings = self.create_default_settings(user_id)
        
        update_data = settings_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(settings, field, value)
        
        self.db.commit()
        self.db.refresh(settings)
        
        return settings
    
    # Utility methods for creating specific notification types
    def create_stock_alert(
        self,
        user_id: uuid.UUID,
        product_name: str,
        current_stock: int,
        minimum_stock: int
    ) -> Notification:
        """
        Create a stock alert notification.
        
        Args:
            user_id: User ID
            product_name: Product name
            current_stock: Current stock level
            minimum_stock: Minimum stock level
            
        Returns:
            Notification: Created notification
        """
        return self.create_notification(NotificationCreate(
            user_id=user_id,
            title=f"Stock Bajo: {product_name}",
            message=f"El producto {product_name} tiene stock bajo. Stock actual: {current_stock}, Stock mínimo: {minimum_stock}",
            type="stock_alert",
            priority="high" if current_stock == 0 else "normal",
            data={
                "product_name": product_name,
                "current_stock": current_stock,
                "minimum_stock": minimum_stock
            }
        ))
    
    def create_guide_status_notification(
        self,
        user_id: uuid.UUID,
        guide_code: str,
        old_status: str,
        new_status: str
    ) -> Notification:
        """
        Create a guide status change notification.
        
        Args:
            user_id: User ID
            guide_code: Guide code
            old_status: Old status
            new_status: New status
            
        Returns:
            Notification: Created notification
        """
        return self.create_notification(NotificationCreate(
            user_id=user_id,
            title=f"Actualización de Guía: {guide_code}",
            message=f"La guía {guide_code} cambió de estado: {old_status} → {new_status}",
            type="guide_status",
            priority="normal",
            data={
                "guide_code": guide_code,
                "old_status": old_status,
                "new_status": new_status
            }
        ))
    
    def create_system_notification(
        self,
        user_ids: List[uuid.UUID],
        title: str,
        message: str,
        priority: str = "normal"
    ) -> List[Notification]:
        """
        Create a system notification for multiple users.
        
        Args:
            user_ids: List of user IDs
            title: Notification title
            message: Notification message
            priority: Notification priority
            
        Returns:
            List[Notification]: Created notifications
        """
        return self.create_bulk_notifications(BulkNotificationCreate(
            title=title,
            message=message,
            type="system",
            priority=priority,
            data={},
            user_ids=user_ids
        ))






