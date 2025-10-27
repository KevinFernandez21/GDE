"""
API dependencies for authentication and authorization.
"""
from typing import Optional, Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError

from ..core.database import get_db
from ..core.security import verify_token
from ..models.user import Profile
from ..core.exceptions import UnauthorizedError, ForbiddenError

# Security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Profile:
    """
    Get current authenticated user.
    
    Args:
        credentials: HTTP authorization credentials
        db: Database session
        
    Returns:
        Profile: Current user profile
        
    Raises:
        HTTPException: If authentication fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(credentials.credentials)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(Profile).filter(Profile.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


async def get_current_active_user(
    current_user: Profile = Depends(get_current_user)
) -> Profile:
    """
    Get current active user.
    
    Args:
        current_user: Current user from get_current_user
        
    Returns:
        Profile: Active user profile
        
    Raises:
        HTTPException: If user is not active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def require_role(required_role: str):
    """
    Dependency factory for role-based access control.
    
    Args:
        required_role: Required role for access
        
    Returns:
        Dependency function
    """
    async def role_checker(
        current_user: Profile = Depends(get_current_active_user)
    ) -> Profile:
        """
        Check if user has required role.
        
        Args:
            current_user: Current user
            
        Returns:
            Profile: User profile if authorized
            
        Raises:
            HTTPException: If user doesn't have required role
        """
        if current_user.role != required_role and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required role: {required_role}"
            )
        return current_user
    
    return role_checker


def require_roles(required_roles: list):
    """
    Dependency factory for multiple role-based access control.
    
    Args:
        required_roles: List of required roles for access
        
    Returns:
        Dependency function
    """
    async def roles_checker(
        current_user: Profile = Depends(get_current_active_user)
    ) -> Profile:
        """
        Check if user has one of the required roles.
        
        Args:
            current_user: Current user
            
        Returns:
            Profile: User profile if authorized
            
        Raises:
            HTTPException: If user doesn't have any of the required roles
        """
        if current_user.role not in required_roles and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required roles: {', '.join(required_roles)}"
            )
        return current_user
    
    return roles_checker


# Common role dependencies
require_admin = require_role("admin")
require_contable = require_roles(["admin", "contable"])
require_programador = require_roles(["admin", "programador"])


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[Profile]:
    """
    Get current user if authenticated, otherwise return None.
    
    Args:
        credentials: Optional HTTP authorization credentials
        db: Database session
        
    Returns:
        Optional[Profile]: User profile if authenticated, None otherwise
    """
    if not credentials:
        return None
    
    try:
        payload = verify_token(credentials.credentials)
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None
    
    user = db.query(Profile).filter(Profile.id == user_id).first()
    return user if user and user.is_active else None


def get_pagination_params(
    skip: int = 0,
    limit: int = 100
) -> dict:
    """
    Get pagination parameters.
    
    Args:
        skip: Number of records to skip
        limit: Number of records to return
        
    Returns:
        dict: Pagination parameters
    """
    return {
        "skip": max(0, skip),
        "limit": min(1000, max(1, limit))
    }
