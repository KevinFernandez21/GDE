"""
Custom exceptions for the GDE Backend API.
"""
from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class GDEException(Exception):
    """Base exception for GDE application."""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(GDEException):
    """Validation error exception."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class NotFoundError(GDEException):
    """Resource not found exception."""
    
    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            message=f"{resource} with id {identifier} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class ConflictError(GDEException):
    """Resource conflict exception."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            details=details
        )


class UnauthorizedError(GDEException):
    """Unauthorized access exception."""
    
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class ForbiddenError(GDEException):
    """Forbidden access exception."""
    
    def __init__(self, message: str = "Forbidden access"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )


class BusinessLogicError(GDEException):
    """Business logic violation exception."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class FileProcessingError(GDEException):
    """File processing error exception."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class DatabaseError(GDEException):
    """Database operation error exception."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class ExternalServiceError(GDEException):
    """External service error exception."""
    
    def __init__(self, service: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"External service error ({service}): {message}",
            status_code=status.HTTP_502_BAD_GATEWAY,
            details=details
        )


# Exception handlers
def handle_gde_exception(exc: GDEException) -> HTTPException:
    """Convert GDE exception to HTTP exception."""
    return HTTPException(
        status_code=exc.status_code,
        detail={
            "message": exc.message,
            "details": exc.details
        }
    )
