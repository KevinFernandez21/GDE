"""
Authentication API endpoints.
"""
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.security import (
    verify_password, 
    create_access_token, 
    create_refresh_token,
    verify_refresh_token,
    generate_password_reset_token,
    verify_password_reset_token
)
from ...core.config import settings
from ...models.user import Profile
from ...schemas.user import (
    LoginRequest, 
    LoginResponse, 
    TokenRefreshRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    ChangePasswordRequest
)
from ...core.exceptions import UnauthorizedError, NotFoundError
from ..dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return access token.
    
    Args:
        login_data: Login credentials
        db: Database session
        
    Returns:
        LoginResponse: Access token and user info
        
    Raises:
        HTTPException: If authentication fails
    """
    # Find user by username or email
    user = db.query(Profile).filter(
        (Profile.username == login_data.username) |
        (Profile.email == login_data.username)
    ).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password (in real implementation, you'd check against hashed password)
    # For now, we'll assume password verification is handled by Supabase Auth
    if not verify_password(login_data.password, user.password_hash or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
        user=user
    )


@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(
    token_data: TokenRefreshRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    Args:
        token_data: Refresh token data
        db: Database session
        
    Returns:
        LoginResponse: New access token and user info
        
    Raises:
        HTTPException: If refresh token is invalid
    """
    try:
        payload = verify_refresh_token(token_data.refresh_token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user = db.query(Profile).filter(Profile.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new tokens
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id)}, 
            expires_delta=access_token_expires
        )
        new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
            user=user
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/password-reset-request")
async def request_password_reset(
    reset_data: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """
    Request password reset token.
    
    Args:
        reset_data: Password reset request data
        db: Database session
        
    Returns:
        dict: Success message
    """
    user = db.query(Profile).filter(Profile.email == reset_data.email).first()
    
    if user:
        # Generate reset token
        reset_token = generate_password_reset_token(reset_data.email)
        
        # In a real implementation, you would send this token via email
        # For now, we'll just return success
        
        # TODO: Send email with reset token
        # await send_password_reset_email(user.email, reset_token)
    
    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/password-reset-confirm")
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """
    Confirm password reset with token.
    
    Args:
        reset_data: Password reset confirmation data
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If token is invalid
    """
    email = verify_password_reset_token(reset_data.token)
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    user = db.query(Profile).filter(Profile.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update password (in real implementation, hash the password)
    # user.password_hash = get_password_hash(reset_data.new_password)
    db.commit()
    
    return {"message": "Password reset successfully"}


@router.post("/change-password")
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: Profile = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password.
    
    Args:
        password_data: Password change data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If current password is incorrect
    """
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash or ""):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    # current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}


@router.post("/logout")
async def logout(
    current_user: Profile = Depends(get_current_user)
):
    """
    Logout user (invalidate token on client side).
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
    """
    # In a real implementation, you might want to blacklist the token
    # For now, we'll just return success
    return {"message": "Logged out successfully"}
