"""
Notifications API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.user import Profile
from ...schemas.notification import (
    NotificationCreate, NotificationUpdate, NotificationResponse,
    NotificationSettingsUpdate, NotificationSettingsResponse
)
from ...services.notification_service import NotificationService
from ..dependencies import get_current_user, require_admin

router = APIRouter(prefix="/notifications", tags=["notifications"])


# Notification endpoints
@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin)
):
    """
    Create a new notification (admin only).
    
    Args:
        notification_data: Notification creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        NotificationResponse: Created notification
    """
    service = NotificationService(db)
    notification = service.create_notification(notification_data)
    return notification


@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    is_read: Optional[bool] = Query(None, description="Filter by read status"),
    notification_type: Optional[str] = Query(None, description="Filter by notification type"),
    priority: Optional[str] = Query(None, description="Filter by priority")
):
    """
    Get notifications for the current user.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Number of records to return
        is_read: Filter by read status
        notification_type: Filter by notification type
        priority: Filter by priority
        
    Returns:
        List[NotificationResponse]: List of notifications
    """
    service = NotificationService(db)
    notifications = service.get_user_notifications(
        user_id=str(current_user.id),
        skip=skip,
        limit=limit,
        is_read=is_read,
        notification_type=notification_type,
        priority=priority
    )
    return notifications


@router.get("/unread/count")
async def get_unread_count(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get count of unread notifications for the current user.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Unread count
    """
    service = NotificationService(db)
    count = service.get_unread_count(str(current_user.id))
    return {"unread_count": count}


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get notification by ID.
    
    Args:
        notification_id: Notification ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        NotificationResponse: Notification details
        
    Raises:
        HTTPException: If notification not found or unauthorized
    """
    service = NotificationService(db)
    notification = service.get_notification(notification_id)
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    # Check if notification belongs to current user
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to this notification is forbidden"
        )
    
    return notification


@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: int,
    notification_data: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Update notification.
    
    Args:
        notification_id: Notification ID
        notification_data: Notification update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        NotificationResponse: Updated notification
        
    Raises:
        HTTPException: If notification not found or unauthorized
    """
    service = NotificationService(db)
    
    # Check if notification belongs to current user
    notification = service.get_notification(notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to this notification is forbidden"
        )
    
    notification = service.update_notification(notification_id, notification_data)
    return notification


@router.post("/{notification_id}/mark-read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Mark notification as read.
    
    Args:
        notification_id: Notification ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        NotificationResponse: Updated notification
        
    Raises:
        HTTPException: If notification not found or unauthorized
    """
    service = NotificationService(db)
    
    # Check if notification belongs to current user
    notification = service.get_notification(notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to this notification is forbidden"
        )
    
    notification = service.mark_as_read(notification_id)
    return notification


@router.post("/mark-all-read", status_code=status.HTTP_200_OK)
async def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Mark all user notifications as read.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
    """
    service = NotificationService(db)
    service.mark_all_as_read(str(current_user.id))
    return {"message": "All notifications marked as read"}


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Delete notification.
    
    Args:
        notification_id: Notification ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If notification not found or unauthorized
    """
    service = NotificationService(db)
    
    # Check if notification belongs to current user
    notification = service.get_notification(notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to this notification is forbidden"
        )
    
    service.delete_notification(notification_id)


# Notification Settings endpoints
@router.get("/settings/me", response_model=NotificationSettingsResponse)
async def get_notification_settings(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get notification settings for the current user.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        NotificationSettingsResponse: User's notification settings
    """
    service = NotificationService(db)
    settings = service.get_user_settings(str(current_user.id))
    
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification settings not found"
        )
    
    return settings


@router.put("/settings/me", response_model=NotificationSettingsResponse)
async def update_notification_settings(
    settings_data: NotificationSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Update notification settings for the current user.
    
    Args:
        settings_data: Notification settings update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        NotificationSettingsResponse: Updated notification settings
    """
    service = NotificationService(db)
    settings = service.update_user_settings(str(current_user.id), settings_data)
    
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification settings not found"
        )
    
    return settings






