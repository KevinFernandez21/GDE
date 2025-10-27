"""
Audit API endpoints for system auditing and logging.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime

from ...core.database import get_db
from ...models.user import Profile
from ...models.audit import AuditLog, ImportLog
from ...schemas.audit import AuditLogResponse, ImportLogResponse
from ..dependencies import get_current_user, require_admin

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/logs", response_model=list[AuditLogResponse])
async def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    usuario_id: Optional[str] = Query(None, description="Filter by user ID"),
    accion: Optional[str] = Query(None, description="Filter by action"),
    tabla_afectada: Optional[str] = Query(None, description="Filter by affected table"),
    fecha_desde: Optional[datetime] = Query(None, description="Filter by date from"),
    fecha_hasta: Optional[datetime] = Query(None, description="Filter by date to")
):
    """
    Get audit logs (admin only).
    
    Args:
        db: Database session
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Number of records to return
        usuario_id: Filter by user ID
        accion: Filter by action
        tabla_afectada: Filter by affected table
        fecha_desde: Filter by date from
        fecha_hasta: Filter by date to
        
    Returns:
        list[AuditLogResponse]: List of audit logs
    """
    query = db.query(AuditLog)
    
    if usuario_id:
        query = query.filter(AuditLog.usuario_id == usuario_id)
    
    if accion:
        query = query.filter(AuditLog.accion == accion)
    
    if tabla_afectada:
        query = query.filter(AuditLog.tabla_afectada == tabla_afectada)
    
    if fecha_desde:
        query = query.filter(AuditLog.fecha >= fecha_desde)
    
    if fecha_hasta:
        query = query.filter(AuditLog.fecha <= fecha_hasta)
    
    # Order by most recent first
    query = query.order_by(AuditLog.fecha.desc())
    
    logs = query.offset(skip).limit(limit).all()
    return logs


@router.get("/logs/{log_id}", response_model=AuditLogResponse)
async def get_audit_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin)
):
    """
    Get audit log by ID (admin only).
    
    Args:
        log_id: Audit log ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        AuditLogResponse: Audit log details
        
    Raises:
        HTTPException: If audit log not found
    """
    log = db.query(AuditLog).filter(AuditLog.id == log_id).first()
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit log not found"
        )
    
    return log


@router.get("/logs/user/{user_id}", response_model=list[AuditLogResponse])
async def get_user_audit_logs(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
):
    """
    Get audit logs for a specific user (admin only).
    
    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Number of records to return
        
    Returns:
        list[AuditLogResponse]: List of user audit logs
    """
    logs = db.query(AuditLog).filter(
        AuditLog.usuario_id == user_id
    ).order_by(
        AuditLog.fecha.desc()
    ).offset(skip).limit(limit).all()
    
    return logs


@router.get("/logs/table/{table_name}", response_model=list[AuditLogResponse])
async def get_table_audit_logs(
    table_name: str,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
):
    """
    Get audit logs for a specific table (admin only).
    
    Args:
        table_name: Table name
        db: Database session
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Number of records to return
        
    Returns:
        list[AuditLogResponse]: List of table audit logs
    """
    logs = db.query(AuditLog).filter(
        AuditLog.tabla_afectada == table_name
    ).order_by(
        AuditLog.fecha.desc()
    ).offset(skip).limit(limit).all()
    
    return logs


@router.get("/logs/record/{table_name}/{record_id}", response_model=list[AuditLogResponse])
async def get_record_audit_logs(
    table_name: str,
    record_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin)
):
    """
    Get audit logs for a specific record (admin only).
    
    Args:
        table_name: Table name
        record_id: Record ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        list[AuditLogResponse]: List of record audit logs
    """
    logs = db.query(AuditLog).filter(
        AuditLog.tabla_afectada == table_name,
        AuditLog.registro_id == record_id
    ).order_by(
        AuditLog.fecha.desc()
    ).all()
    
    return logs


@router.get("/import-logs", response_model=list[ImportLogResponse])
async def get_import_logs(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    entidad: Optional[str] = Query(None, description="Filter by entity"),
    estado: Optional[str] = Query(None, description="Filter by status")
):
    """
    Get import logs.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Number of records to return
        entidad: Filter by entity
        estado: Filter by status
        
    Returns:
        list[ImportLogResponse]: List of import logs
    """
    query = db.query(ImportLog)
    
    # Non-admin users can only see their own import logs
    if current_user.role != "admin":
        query = query.filter(ImportLog.usuario_id == current_user.id)
    
    if entidad:
        query = query.filter(ImportLog.entidad == entidad)
    
    if estado:
        query = query.filter(ImportLog.estado == estado)
    
    # Order by most recent first
    query = query.order_by(ImportLog.fecha_importacion.desc())
    
    logs = query.offset(skip).limit(limit).all()
    return logs


@router.get("/import-logs/{log_id}", response_model=ImportLogResponse)
async def get_import_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    Get import log by ID.
    
    Args:
        log_id: Import log ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        ImportLogResponse: Import log details
        
    Raises:
        HTTPException: If import log not found or unauthorized
    """
    log = db.query(ImportLog).filter(ImportLog.id == log_id).first()
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Import log not found"
        )
    
    # Non-admin users can only access their own import logs
    if current_user.role != "admin" and log.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to this import log is forbidden"
        )
    
    return log


@router.get("/statistics/actions")
async def get_action_statistics(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin),
    fecha_desde: Optional[datetime] = Query(None, description="Filter by date from"),
    fecha_hasta: Optional[datetime] = Query(None, description="Filter by date to")
):
    """
    Get action statistics (admin only).
    
    Args:
        db: Database session
        current_user: Current authenticated user
        fecha_desde: Filter by date from
        fecha_hasta: Filter by date to
        
    Returns:
        dict: Action statistics
    """
    from sqlalchemy import func
    
    query = db.query(
        AuditLog.accion,
        func.count(AuditLog.id).label("count")
    )
    
    if fecha_desde:
        query = query.filter(AuditLog.fecha >= fecha_desde)
    
    if fecha_hasta:
        query = query.filter(AuditLog.fecha <= fecha_hasta)
    
    results = query.group_by(AuditLog.accion).all()
    
    return {
        "statistics": [
            {"action": row.accion, "count": row.count}
            for row in results
        ]
    }


@router.get("/statistics/tables")
async def get_table_statistics(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin),
    fecha_desde: Optional[datetime] = Query(None, description="Filter by date from"),
    fecha_hasta: Optional[datetime] = Query(None, description="Filter by date to")
):
    """
    Get table modification statistics (admin only).
    
    Args:
        db: Database session
        current_user: Current authenticated user
        fecha_desde: Filter by date from
        fecha_hasta: Filter by date to
        
    Returns:
        dict: Table statistics
    """
    from sqlalchemy import func
    
    query = db.query(
        AuditLog.tabla_afectada,
        func.count(AuditLog.id).label("count")
    )
    
    if fecha_desde:
        query = query.filter(AuditLog.fecha >= fecha_desde)
    
    if fecha_hasta:
        query = query.filter(AuditLog.fecha <= fecha_hasta)
    
    results = query.group_by(AuditLog.tabla_afectada).all()
    
    return {
        "statistics": [
            {"table": row.tabla_afectada, "count": row.count}
            for row in results
        ]
    }


@router.get("/statistics/users")
async def get_user_statistics(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin),
    fecha_desde: Optional[datetime] = Query(None, description="Filter by date from"),
    fecha_hasta: Optional[datetime] = Query(None, description="Filter by date to")
):
    """
    Get user activity statistics (admin only).
    
    Args:
        db: Database session
        current_user: Current authenticated user
        fecha_desde: Filter by date from
        fecha_hasta: Filter by date to
        
    Returns:
        dict: User statistics
    """
    from sqlalchemy import func
    
    query = db.query(
        AuditLog.usuario_id,
        func.count(AuditLog.id).label("count")
    ).join(Profile, AuditLog.usuario_id == Profile.id)
    
    if fecha_desde:
        query = query.filter(AuditLog.fecha >= fecha_desde)
    
    if fecha_hasta:
        query = query.filter(AuditLog.fecha <= fecha_hasta)
    
    results = query.group_by(AuditLog.usuario_id, Profile.username).all()
    
    return {
        "statistics": [
            {"user_id": str(row.usuario_id), "count": row.count}
            for row in results
        ]
    }






