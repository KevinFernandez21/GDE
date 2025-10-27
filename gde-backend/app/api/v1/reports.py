"""
Reports API endpoints for analytics and business intelligence.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from ...core.database import get_db
from ...models.user import Profile
from ...services.report_service import ReportService
from ..dependencies import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/inventory/stock")
async def get_inventory_stock_report(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    categoria_id: Optional[int] = Query(None, description="Filter by category ID"),
    almacen: Optional[str] = Query(None, description="Filter by warehouse"),
    low_stock_only: bool = Query(False, description="Show only low stock items"),
    include_zero: bool = Query(False, description="Include items with zero stock")
):
    """
    Get inventory stock report.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        categoria_id: Filter by category ID
        almacen: Filter by warehouse
        low_stock_only: Show only low stock items
        include_zero: Include items with zero stock
        
    Returns:
        dict: Inventory stock report
    """
    service = ReportService(db)
    report = service.get_inventory_report(
        categoria_id=categoria_id,
        almacen=almacen,
        low_stock_only=low_stock_only,
        include_zero=include_zero
    )
    return report


@router.get("/inventory/movements")
async def get_inventory_movements_report(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    fecha_desde: date = Query(..., description="Start date"),
    fecha_hasta: date = Query(..., description="End date"),
    producto_id: Optional[int] = Query(None, description="Filter by product ID"),
    tipo_movimiento: Optional[str] = Query(None, description="Filter by movement type"),
    almacen: Optional[str] = Query(None, description="Filter by warehouse")
):
    """
    Get inventory movements report.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        fecha_desde: Start date
        fecha_hasta: End date
        producto_id: Filter by product ID
        tipo_movimiento: Filter by movement type
        almacen: Filter by warehouse
        
    Returns:
        dict: Inventory movements report
    """
    service = ReportService(db)
    report = service.get_movements_report(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        producto_id=producto_id,
        tipo_movimiento=tipo_movimiento,
        almacen=almacen
    )
    return report


@router.get("/guides/statistics")
async def get_guides_statistics(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    fecha_desde: Optional[date] = Query(None, description="Start date"),
    fecha_hasta: Optional[date] = Query(None, description="End date"),
    tipo_movimiento: Optional[str] = Query(None, description="Filter by movement type"),
    estado: Optional[str] = Query(None, description="Filter by status")
):
    """
    Get guides statistics report.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        fecha_desde: Start date
        fecha_hasta: End date
        tipo_movimiento: Filter by movement type
        estado: Filter by status
        
    Returns:
        dict: Guides statistics
    """
    service = ReportService(db)
    report = service.get_guides_report(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        tipo_movimiento=tipo_movimiento,
        estado=estado
    )
    return report


@router.get("/pistoleo/statistics")
async def get_pistoleo_statistics(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    fecha_desde: Optional[date] = Query(None, description="Start date"),
    fecha_hasta: Optional[date] = Query(None, description="End date"),
    user_id: Optional[str] = Query(None, description="Filter by user ID")
):
    """
    Get pistoleo (scanning) statistics report.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        fecha_desde: Start date
        fecha_hasta: End date
        user_id: Filter by user ID
        
    Returns:
        dict: Pistoleo statistics
    """
    service = ReportService(db)
    report = service.get_pistoleo_report(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        user_id=user_id
    )
    return report


@router.get("/costs/summary")
async def get_costs_summary(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    fecha_desde: date = Query(..., description="Start date"),
    fecha_hasta: date = Query(..., description="End date"),
    categoria_id: Optional[int] = Query(None, description="Filter by category ID"),
    estado: Optional[str] = Query(None, description="Filter by status")
):
    """
    Get costs summary report.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        fecha_desde: Start date
        fecha_hasta: End date
        categoria_id: Filter by category ID
        estado: Filter by status
        
    Returns:
        dict: Costs summary
    """
    service = ReportService(db)
    report = service.get_costs_report(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        categoria_id=categoria_id,
        estado=estado
    )
    return report


@router.get("/costs/by-category")
async def get_costs_by_category(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    fecha_desde: date = Query(..., description="Start date"),
    fecha_hasta: date = Query(..., description="End date")
):
    """
    Get costs grouped by category.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        fecha_desde: Start date
        fecha_hasta: End date
        
    Returns:
        dict: Costs by category
    """
    service = ReportService(db)
    report = service.get_costs_by_category(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    return report


@router.get("/costs/trends")
async def get_costs_trends(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    fecha_desde: date = Query(..., description="Start date"),
    fecha_hasta: date = Query(..., description="End date"),
    group_by: str = Query("month", description="Group by: day, week, month, year")
):
    """
    Get costs trends over time.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        fecha_desde: Start date
        fecha_hasta: End date
        group_by: Grouping period (day, week, month, year)
        
    Returns:
        dict: Costs trends
    """
    service = ReportService(db)
    report = service.get_costs_trends(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        group_by=group_by
    )
    return report


@router.get("/dashboard/summary")
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get dashboard summary with key metrics.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Dashboard summary
    """
    service = ReportService(db)
    summary = service.get_dashboard_summary()
    return summary


@router.get("/user/activity")
async def get_user_activity_report(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    fecha_desde: Optional[date] = Query(None, description="Start date"),
    fecha_hasta: Optional[date] = Query(None, description="End date"),
    user_id: Optional[str] = Query(None, description="Filter by user ID")
):
    """
    Get user activity report.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        fecha_desde: Start date
        fecha_hasta: End date
        user_id: Filter by user ID
        
    Returns:
        dict: User activity report
    """
    service = ReportService(db)
    report = service.get_user_activity_report(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        user_id=user_id
    )
    return report


@router.get("/export/inventory")
async def export_inventory_report(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    format: str = Query("csv", description="Export format: csv, excel, pdf")
):
    """
    Export inventory report to file.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        format: Export format (csv, excel, pdf)
        
    Returns:
        File: Exported report file
    """
    service = ReportService(db)
    # This would typically return a file response
    # For now, we'll return the data that would be exported
    report = service.get_inventory_report()
    return {
        "message": f"Export to {format} format",
        "data": report
    }


@router.get("/export/costs")
async def export_costs_report(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    fecha_desde: date = Query(..., description="Start date"),
    fecha_hasta: date = Query(..., description="End date"),
    format: str = Query("csv", description="Export format: csv, excel, pdf")
):
    """
    Export costs report to file.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        fecha_desde: Start date
        fecha_hasta: End date
        format: Export format (csv, excel, pdf)
        
    Returns:
        File: Exported report file
    """
    service = ReportService(db)
    # This would typically return a file response
    # For now, we'll return the data that would be exported
    report = service.get_costs_report(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    return {
        "message": f"Export to {format} format",
        "data": report
    }






