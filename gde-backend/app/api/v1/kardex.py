"""
Kardex API endpoints for inventory movements.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

from ...core.database import get_db
from ...models.user import Profile
from ...schemas.product import KardexCreate, KardexResponse
from ...services.kardex_service import KardexService
from ..dependencies import get_current_user, require_contable

router = APIRouter(prefix="/kardex", tags=["kardex"])


@router.post("/", response_model=KardexResponse, status_code=status.HTTP_201_CREATED)
async def create_kardex_entry(
    product_id: int = Query(..., description="Product ID"),
    tipo_movimiento: str = Query(..., description="Movement type"),
    cantidad: int = Query(..., description="Quantity"),
    documento_asociado: Optional[str] = Query(None, description="Associated document"),
    referencia: Optional[str] = Query(None, description="Reference"),
    costo_unitario: Optional[Decimal] = Query(None, description="Unit cost"),
    observaciones: Optional[str] = Query(None, description="Observations"),
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Create a kardex entry.
    
    Args:
        product_id: Product ID
        tipo_movimiento: Movement type (entrada, salida, ajuste, transferencia)
        cantidad: Quantity
        documento_asociado: Associated document
        referencia: Reference
        costo_unitario: Unit cost
        observaciones: Observations
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        KardexResponse: Created kardex entry
    """
    service = KardexService(db)
    kardex = service.create_kardex_entry(
        product_id=product_id,
        tipo_movimiento=tipo_movimiento,
        cantidad=cantidad,
        documento_asociado=documento_asociado,
        referencia=referencia,
        costo_unitario=costo_unitario,
        usuario_id=str(current_user.id),
        observaciones=observaciones
    )
    return kardex


@router.get("/product/{product_id}", response_model=List[KardexResponse])
async def get_product_kardex(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    fecha_desde: Optional[datetime] = Query(None, description="Filter by date from"),
    fecha_hasta: Optional[datetime] = Query(None, description="Filter by date to")
):
    """
    Get kardex entries for a product.
    
    Args:
        product_id: Product ID
        db: Database session
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Number of records to return
        fecha_desde: Filter by date from
        fecha_hasta: Filter by date to
        
    Returns:
        List[KardexResponse]: List of kardex entries
    """
    service = KardexService(db)
    kardex = service.get_kardex_by_product(
        product_id=product_id,
        skip=skip,
        limit=limit,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    return kardex


@router.get("/summary")
async def get_kardex_summary(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    product_id: Optional[int] = Query(None, description="Filter by product ID"),
    tipo_movimiento: Optional[str] = Query(None, description="Filter by movement type"),
    fecha_desde: Optional[datetime] = Query(None, description="Filter by date from"),
    fecha_hasta: Optional[datetime] = Query(None, description="Filter by date to")
):
    """
    Get kardex summary statistics.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        product_id: Filter by product ID
        tipo_movimiento: Filter by movement type
        fecha_desde: Filter by date from
        fecha_hasta: Filter by date to
        
    Returns:
        dict: Kardex summary statistics
    """
    service = KardexService(db)
    summary = service.get_kardex_summary(
        product_id=product_id,
        tipo_movimiento=tipo_movimiento,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    return summary


@router.get("/product/{product_id}/report")
async def get_product_movements_report(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    days: int = Query(30, ge=1, le=365, description="Number of days to look back")
):
    """
    Get product movements report.
    
    Args:
        product_id: Product ID
        db: Database session
        current_user: Current authenticated user
        days: Number of days to look back
        
    Returns:
        dict: Product movements report
    """
    service = KardexService(db)
    report = service.get_product_movements_report(product_id=product_id, days=days)
    return report


@router.post("/adjust-stock", response_model=KardexResponse)
async def adjust_stock(
    product_id: int = Query(..., description="Product ID"),
    new_stock: int = Query(..., description="New stock value"),
    observaciones: str = Query(..., description="Reason for adjustment"),
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Adjust product stock to a specific value.
    
    Args:
        product_id: Product ID
        new_stock: New stock value
        observaciones: Reason for adjustment
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        KardexResponse: Created kardex entry
    """
    service = KardexService(db)
    kardex = service.adjust_stock(
        product_id=product_id,
        new_stock=new_stock,
        usuario_id=str(current_user.id),
        observaciones=observaciones
    )
    return kardex


@router.post("/transfer-stock", response_model=KardexResponse)
async def transfer_stock(
    product_id: int = Query(..., description="Product ID"),
    cantidad: int = Query(..., description="Quantity to transfer"),
    destino: str = Query(..., description="Destination location"),
    observaciones: Optional[str] = Query(None, description="Transfer observations"),
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_contable)
):
    """
    Transfer stock to another location.
    
    Args:
        product_id: Product ID
        cantidad: Quantity to transfer
        destino: Destination location
        observaciones: Transfer observations
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        KardexResponse: Created kardex entry
    """
    service = KardexService(db)
    kardex = service.transfer_stock(
        product_id=product_id,
        cantidad=cantidad,
        destino=destino,
        usuario_id=str(current_user.id),
        observaciones=observaciones
    )
    return kardex






