"""
Costos API endpoints for accounting and cost management.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date

from ...core.database import get_db
from ...models.user import Profile
from ...schemas.costo import (
    CostoCreate, CostoUpdate, CostoResponse,
    CostCategoryCreate, CostCategoryUpdate, CostCategoryResponse
)
from ...services.costo_service import CostoService
from ..dependencies import get_current_user, require_contable

router = APIRouter(prefix="/costos", tags=["costos"])


# Costo endpoints
@router.post("/", response_model=CostoResponse, status_code=status.HTTP_201_CREATED)
async def create_costo(
    costo_data: CostoCreate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Create a new costo.
    
    Args:
        costo_data: Costo creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        CostoResponse: Created costo
    """
    service = CostoService(db)
    costo = service.create_costo(costo_data, str(current_user.id))
    return costo


@router.get("/", response_model=List[CostoResponse])
async def get_costos(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    categoria_id: Optional[int] = Query(None, description="Filter by category ID"),
    estado: Optional[str] = Query(None, description="Filter by estado"),
    fecha_desde: Optional[date] = Query(None, description="Filter by date from"),
    fecha_hasta: Optional[date] = Query(None, description="Filter by date to"),
    search: Optional[str] = Query(None, description="Search term for descripcion or proveedor")
):
    """
    Get costos with optional filtering.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Number of records to return
        categoria_id: Filter by category ID
        estado: Filter by estado
        fecha_desde: Filter by date from
        fecha_hasta: Filter by date to
        search: Search term for descripcion or proveedor
        
    Returns:
        List[CostoResponse]: List of costos
    """
    service = CostoService(db)
    costos = service.get_costos(
        skip=skip,
        limit=limit,
        categoria_id=categoria_id,
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        search=search
    )
    return costos


@router.get("/{costo_id}", response_model=CostoResponse)
async def get_costo(
    costo_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get costo by ID.
    
    Args:
        costo_id: Costo ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        CostoResponse: Costo details
        
    Raises:
        HTTPException: If costo not found
    """
    service = CostoService(db)
    costo = service.get_costo(costo_id)
    
    if not costo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Costo not found"
        )
    
    return costo


@router.put("/{costo_id}", response_model=CostoResponse)
async def update_costo(
    costo_id: int,
    costo_data: CostoUpdate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Update costo.
    
    Args:
        costo_id: Costo ID
        costo_data: Costo update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        CostoResponse: Updated costo
        
    Raises:
        HTTPException: If costo not found
    """
    service = CostoService(db)
    costo = service.update_costo(costo_id, costo_data)
    
    if not costo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Costo not found"
        )
    
    return costo


@router.delete("/{costo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_costo(
    costo_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Delete costo.
    
    Args:
        costo_id: Costo ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If costo not found
    """
    service = CostoService(db)
    success = service.delete_costo(costo_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Costo not found"
        )


@router.get("/summary/statistics")
async def get_costos_summary(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    fecha_desde: Optional[date] = Query(None, description="Filter by date from"),
    fecha_hasta: Optional[date] = Query(None, description="Filter by date to")
):
    """
    Get costos summary statistics.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        fecha_desde: Filter by date from
        fecha_hasta: Filter by date to
        
    Returns:
        dict: Costos summary
    """
    service = CostoService(db)
    summary = service.get_costos_summary(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    return summary


@router.get("/summary/by-category")
async def get_costos_by_category(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    fecha_desde: Optional[date] = Query(None, description="Filter by date from"),
    fecha_hasta: Optional[date] = Query(None, description="Filter by date to")
):
    """
    Get costos grouped by category.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        fecha_desde: Filter by date from
        fecha_hasta: Filter by date to
        
    Returns:
        List[dict]: Costos grouped by category
    """
    service = CostoService(db)
    summary = service.get_costos_by_category(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    return summary


@router.get("/reports/monthly")
async def get_monthly_report(
    year: int = Query(..., description="Year"),
    month: int = Query(..., ge=1, le=12, description="Month"),
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get monthly financial report.
    
    Args:
        year: Year
        month: Month (1-12)
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Monthly report
    """
    service = CostoService(db)
    report = service.get_monthly_report(year=year, month=month)
    return report


# Category endpoints
@router.post("/categories", response_model=CostCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CostCategoryCreate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Create a new cost category.
    
    Args:
        category_data: Category creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        CostCategoryResponse: Created category
    """
    service = CostoService(db)
    category = service.create_category(category_data)
    return category


@router.get("/categories", response_model=List[CostCategoryResponse])
async def get_categories(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    active_only: bool = Query(True, description="Return only active categories")
):
    """
    Get cost categories.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        active_only: Whether to return only active categories
        
    Returns:
        List[CostCategoryResponse]: List of categories
    """
    service = CostoService(db)
    categories = service.get_categories(active_only=active_only)
    return categories


@router.get("/categories/{category_id}", response_model=CostCategoryResponse)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get category by ID.
    
    Args:
        category_id: Category ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        CostCategoryResponse: Category details
        
    Raises:
        HTTPException: If category not found
    """
    service = CostoService(db)
    category = service.get_category(category_id)
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return category


@router.put("/categories/{category_id}", response_model=CostCategoryResponse)
async def update_category(
    category_id: int,
    category_data: CostCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Update cost category.
    
    Args:
        category_id: Category ID
        category_data: Category update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        CostCategoryResponse: Updated category
        
    Raises:
        HTTPException: If category not found
    """
    service = CostoService(db)
    category = service.update_category(category_id, category_data)
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return category


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Delete cost category.
    
    Args:
        category_id: Category ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If category not found or has associated costos
    """
    service = CostoService(db)
    success = service.delete_category(category_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )






