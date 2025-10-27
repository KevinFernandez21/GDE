"""
Guias API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime

from ...core.database import get_db
from ...models.user import Profile
from ...schemas.guia import (
    GuiaCreate, GuiaUpdate, GuiaResponse,
    GuiaItemCreate, GuiaItemUpdate, GuiaItemResponse,
    GuiaMovementCreate, GuiaMovementResponse,
    GuiaStatusUpdate, GuiaTrackingResponse
)
from ...services.guia_service import GuiaService
from ..dependencies import get_current_user, require_contable

router = APIRouter(prefix="/guias", tags=["guias"])


@router.post("/", response_model=GuiaResponse, status_code=status.HTTP_201_CREATED)
async def create_guia(
    guia_data: GuiaCreate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Create a new guia.
    
    Args:
        guia_data: Guia creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        GuiaResponse: Created guia
    """
    service = GuiaService(db)
    guia = service.create_guia(guia_data, str(current_user.id))
    return guia


@router.get("/", response_model=List[GuiaResponse])
async def get_guias(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search term for codigo or cliente_nombre"),
    estado: Optional[str] = Query(None, description="Filter by estado"),
    fecha_desde: Optional[datetime] = Query(None, description="Filter by creation date from"),
    fecha_hasta: Optional[datetime] = Query(None, description="Filter by creation date to")
):
    """
    Get guias with optional filtering.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Number of records to return
        search: Search term for codigo or cliente_nombre
        estado: Filter by estado
        fecha_desde: Filter by creation date from
        fecha_hasta: Filter by creation date to
        
    Returns:
        List[GuiaResponse]: List of guias
    """
    service = GuiaService(db)
    guias = service.get_guias(
        skip=skip,
        limit=limit,
        search=search,
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    return guias


@router.get("/{guia_id}", response_model=GuiaResponse)
async def get_guia(
    guia_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get guia by ID.
    
    Args:
        guia_id: Guia ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        GuiaResponse: Guia details
        
    Raises:
        HTTPException: If guia not found
    """
    service = GuiaService(db)
    guia = service.get_guia(guia_id)
    
    if not guia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guia not found"
        )
    
    return guia


@router.put("/{guia_id}", response_model=GuiaResponse)
async def update_guia(
    guia_id: int,
    guia_data: GuiaUpdate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Update guia.
    
    Args:
        guia_id: Guia ID
        guia_data: Guia update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        GuiaResponse: Updated guia
        
    Raises:
        HTTPException: If guia not found
    """
    service = GuiaService(db)
    guia = service.update_guia(guia_id, guia_data, str(current_user.id))
    
    if not guia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guia not found"
        )
    
    return guia


@router.patch("/{guia_id}/status", response_model=GuiaResponse)
async def update_guia_status(
    guia_id: int,
    status_data: GuiaStatusUpdate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Update guia status.
    
    Args:
        guia_id: Guia ID
        status_data: Status update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        GuiaResponse: Updated guia
        
    Raises:
        HTTPException: If guia not found
    """
    service = GuiaService(db)
    guia = service.update_guia_status(guia_id, status_data, str(current_user.id))
    
    if not guia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guia not found"
        )
    
    return guia


@router.delete("/{guia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guia(
    guia_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Delete guia.
    
    Args:
        guia_id: Guia ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If guia not found
    """
    service = GuiaService(db)
    success = service.delete_guia(guia_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guia not found"
        )


# Guia Items endpoints
@router.post("/{guia_id}/items", response_model=GuiaItemResponse, status_code=status.HTTP_201_CREATED)
async def add_guia_item(
    guia_id: int,
    item_data: GuiaItemCreate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Add item to guia.
    
    Args:
        guia_id: Guia ID
        item_data: Guia item data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        GuiaItemResponse: Created guia item
    """
    # Ensure guia_id matches
    item_data.guia_id = guia_id
    
    service = GuiaService(db)
    item = service.add_guia_item(item_data, str(current_user.id))
    return item


@router.get("/{guia_id}/items", response_model=List[GuiaItemResponse])
async def get_guia_items(
    guia_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get all items for a guia.
    
    Args:
        guia_id: Guia ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List[GuiaItemResponse]: List of guia items
    """
    service = GuiaService(db)
    items = service.get_guia_items(guia_id)
    return items


@router.put("/items/{item_id}", response_model=GuiaItemResponse)
async def update_guia_item(
    item_id: int,
    item_data: GuiaItemUpdate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Update guia item.
    
    Args:
        item_id: Guia item ID
        item_data: Guia item update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        GuiaItemResponse: Updated guia item
        
    Raises:
        HTTPException: If guia item not found
    """
    service = GuiaService(db)
    item = service.update_guia_item(item_id, item_data)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guia item not found"
        )
    
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guia_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Delete guia item.
    
    Args:
        item_id: Guia item ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If guia item not found
    """
    service = GuiaService(db)
    success = service.delete_guia_item(item_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guia item not found"
        )


# Guia Movements endpoints
@router.post("/{guia_id}/movements", response_model=GuiaMovementResponse, status_code=status.HTTP_201_CREATED)
async def add_guia_movement(
    guia_id: int,
    movement_data: GuiaMovementCreate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Add movement to guia.
    
    Args:
        guia_id: Guia ID
        movement_data: Guia movement data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        GuiaMovementResponse: Created guia movement
    """
    # Ensure guia_id matches
    movement_data.guia_id = guia_id
    
    service = GuiaService(db)
    movement = service.add_guia_movement(movement_data, str(current_user.id))
    return movement


@router.get("/{guia_id}/movements", response_model=List[GuiaMovementResponse])
async def get_guia_movements(
    guia_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get all movements for a guia.
    
    Args:
        guia_id: Guia ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List[GuiaMovementResponse]: List of guia movements
    """
    service = GuiaService(db)
    movements = service.get_guia_movements(guia_id)
    return movements


# Tracking endpoint (public or with optional auth)
@router.get("/tracking/{codigo}", response_model=GuiaTrackingResponse)
async def track_guia(
    codigo: str,
    db: Session = Depends(get_db)
):
    """
    Track guia by codigo (public endpoint).
    
    Args:
        codigo: Guia codigo
        db: Database session
        
    Returns:
        GuiaTrackingResponse: Guia tracking information
        
    Raises:
        HTTPException: If guia not found
    """
    service = GuiaService(db)
    tracking = service.get_guia_tracking(codigo)
    
    if not tracking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guia not found"
        )
    
    return tracking






