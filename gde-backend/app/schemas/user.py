"""
User and authentication schemas.
"""
from typing import Optional, Dict, Any
from pydantic import Field, EmailStr
from datetime import datetime
import uuid

from .common import BaseSchema


class ProfileBase(BaseSchema):
    """Base profile schema."""
    username: Optional[str] = Field(None, max_length=50, description="Username")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    role: str = Field(default="contable", description="User role")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    is_active: bool = Field(default=True, description="Whether user is active")


class ProfileCreate(ProfileBase):
    """Profile creation schema."""
    username: str = Field(..., max_length=50, description="Username")
    full_name: str = Field(..., max_length=100, description="Full name")


class ProfileUpdate(BaseSchema):
    """Profile update schema."""
    username: Optional[str] = Field(None, max_length=50, description="Username")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    role: Optional[str] = Field(None, description="User role")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    is_active: Optional[bool] = Field(None, description="Whether user is active")


class ProfileResponse(ProfileBase):
    """Profile response schema."""
    id: uuid.UUID = Field(description="User ID")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class RoleBase(BaseSchema):
    """Base role schema."""
    name: str = Field(..., max_length=50, description="Role name")
    description: Optional[str] = Field(None, description="Role description")
    permissions: Dict[str, Any] = Field(default_factory=dict, description="Role permissions")


class RoleCreate(RoleBase):
    """Role creation schema."""
    pass


class RoleUpdate(BaseSchema):
    """Role update schema."""
    name: Optional[str] = Field(None, max_length=50, description="Role name")
    description: Optional[str] = Field(None, description="Role description")
    permissions: Optional[Dict[str, Any]] = Field(None, description="Role permissions")


class RoleResponse(RoleBase):
    """Role response schema."""
    id: int = Field(description="Role ID")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class LoginRequest(BaseSchema):
    """Login request schema."""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., min_length=6, description="Password")


class LoginResponse(BaseSchema):
    """Login response schema."""
    access_token: str = Field(description="JWT access token")
    refresh_token: str = Field(description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(description="Token expiration time in seconds")
    user: ProfileResponse = Field(description="User profile")


class TokenRefreshRequest(BaseSchema):
    """Token refresh request schema."""
    refresh_token: str = Field(..., description="Refresh token")


class PasswordResetRequest(BaseSchema):
    """Password reset request schema."""
    email: EmailStr = Field(..., description="User email")


class PasswordResetConfirm(BaseSchema):
    """Password reset confirmation schema."""
    token: str = Field(..., description="Reset token")
    new_password: str = Field(..., min_length=6, description="New password")


class ChangePasswordRequest(BaseSchema):
    """Change password request schema."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=6, description="New password")
