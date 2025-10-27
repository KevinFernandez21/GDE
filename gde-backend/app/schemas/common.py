"""
Common Pydantic schemas.
"""
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime

DataT = TypeVar('DataT')


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PaginationParams(BaseSchema):
    """Pagination parameters."""
    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=100, ge=1, le=1000, description="Number of records to return")


class PaginatedResponse(BaseSchema, Generic[DataT]):
    """Paginated response schema."""
    items: List[DataT] = Field(description="List of items")
    total: int = Field(description="Total number of items")
    skip: int = Field(description="Number of items skipped")
    limit: int = Field(description="Number of items returned")
    has_next: bool = Field(description="Whether there are more items")
    has_prev: bool = Field(description="Whether there are previous items")


class ErrorResponse(BaseSchema):
    """Error response schema."""
    message: str = Field(description="Error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Error details")
    code: Optional[str] = Field(default=None, description="Error code")


class SuccessResponse(BaseSchema):
    """Success response schema."""
    message: str = Field(description="Success message")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Response data")


class HealthCheckResponse(BaseSchema):
    """Health check response schema."""
    status: str = Field(description="Service status")
    timestamp: datetime = Field(description="Current timestamp")
    version: str = Field(description="API version")
    environment: str = Field(description="Environment")
