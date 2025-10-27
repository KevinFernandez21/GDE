"""
Pistoleo API endpoints for scanning sessions.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.user import Profile
from ...schemas.pistoleo import (
    PistoleoSessionCreate, PistoleoSessionUpdate, PistoleoSessionResponse,
    EscaneoCreate, EscaneoResponse
)
from ...services.pistoleo_service import PistoleoService
from ..dependencies import get_current_user, require_contable

router = APIRouter(prefix="/pistoleo", tags=["pistoleo"])


# Session endpoints
@router.post("/sessions", response_model=PistoleoSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: PistoleoSessionCreate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Create a new pistoleo session.
    
    Args:
        session_data: Session creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        PistoleoSessionResponse: Created session
    """
    service = PistoleoService(db)
    session = service.create_session(session_data, str(current_user.id))
    return session


@router.get("/sessions", response_model=List[PistoleoSessionResponse])
async def get_sessions(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    estado: Optional[str] = Query(None, description="Filter by estado")
):
    """
    Get pistoleo sessions.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Number of records to return
        estado: Filter by estado
        
    Returns:
        List[PistoleoSessionResponse]: List of sessions
    """
    service = PistoleoService(db)
    sessions = service.get_sessions(
        skip=skip,
        limit=limit,
        estado=estado,
        user_id=str(current_user.id) if current_user.role != "admin" else None
    )
    return sessions


@router.get("/sessions/{session_id}", response_model=PistoleoSessionResponse)
async def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get session by ID.
    
    Args:
        session_id: Session ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        PistoleoSessionResponse: Session details
        
    Raises:
        HTTPException: If session not found
    """
    service = PistoleoService(db)
    session = service.get_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return session


@router.get("/sessions/qr/{codigo_qr}", response_model=PistoleoSessionResponse)
async def get_session_by_qr(
    codigo_qr: str,
    db: Session = Depends(get_db)
):
    """
    Get session by QR code (public endpoint for scanning).
    
    Args:
        codigo_qr: QR code
        db: Database session
        
    Returns:
        PistoleoSessionResponse: Session details
        
    Raises:
        HTTPException: If session not found
    """
    service = PistoleoService(db)
    session = service.get_session_by_qr(codigo_qr)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return session


@router.put("/sessions/{session_id}", response_model=PistoleoSessionResponse)
async def update_session(
    session_id: int,
    session_data: PistoleoSessionUpdate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Update pistoleo session.
    
    Args:
        session_id: Session ID
        session_data: Session update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        PistoleoSessionResponse: Updated session
        
    Raises:
        HTTPException: If session not found
    """
    service = PistoleoService(db)
    session = service.update_session(session_id, session_data)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return session


@router.post("/sessions/{session_id}/complete", response_model=PistoleoSessionResponse)
async def complete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Mark session as completed.
    
    Args:
        session_id: Session ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        PistoleoSessionResponse: Updated session
        
    Raises:
        HTTPException: If session not found
    """
    service = PistoleoService(db)
    session = service.complete_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return session


@router.post("/sessions/{session_id}/cancel", response_model=PistoleoSessionResponse)
async def cancel_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Cancel session.
    
    Args:
        session_id: Session ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        PistoleoSessionResponse: Updated session
        
    Raises:
        HTTPException: If session not found
    """
    service = PistoleoService(db)
    session = service.cancel_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return session


# Scan endpoints
@router.post("/sessions/{session_id}/scans", response_model=EscaneoResponse, status_code=status.HTTP_201_CREATED)
async def create_scan(
    session_id: int,
    scan_data: EscaneoCreate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Create a new scan in a session.
    
    Args:
        session_id: Session ID
        scan_data: Scan data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        EscaneoResponse: Created scan
    """
    service = PistoleoService(db)
    scan = service.create_scan(scan_data, session_id, str(current_user.id))
    return scan


@router.get("/sessions/{session_id}/scans", response_model=List[EscaneoResponse])
async def get_session_scans(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    estado_escaneo: Optional[str] = Query(None, description="Filter by scan status")
):
    """
    Get scans for a session.
    
    Args:
        session_id: Session ID
        db: Database session
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Number of records to return
        estado_escaneo: Filter by scan status
        
    Returns:
        List[EscaneoResponse]: List of scans
    """
    service = PistoleoService(db)
    scans = service.get_session_scans(
        session_id=session_id,
        skip=skip,
        limit=limit,
        estado_escaneo=estado_escaneo
    )
    return scans


@router.get("/sessions/{session_id}/statistics")
async def get_session_statistics(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get session statistics.
    
    Args:
        session_id: Session ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Session statistics
    """
    service = PistoleoService(db)
    stats = service.get_session_statistics(session_id)
    
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return stats






