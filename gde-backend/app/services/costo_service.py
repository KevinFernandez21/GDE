"""
Costo service for accounting and cost management.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, extract
from datetime import datetime, date
from decimal import Decimal

from ..models.costo import Costo, CostCategory
from ..schemas.costo import (
    CostoCreate, CostoUpdate,
    CostCategoryCreate, CostCategoryUpdate
)
from ..core.exceptions import NotFoundError, BusinessLogicError


class CostoService:
    """Service for managing costs and expenses."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_costo(self, costo_data: CostoCreate, user_id: str) -> Costo:
        """
        Create a new costo.
        
        Args:
            costo_data: Costo creation data
            user_id: User creating the costo
            
        Returns:
            Costo: Created costo
            
        Raises:
            NotFoundError: If category not found
        """
        # Verify category exists
        category = self.db.query(CostCategory).filter(
            CostCategory.id == costo_data.categoria_id
        ).first()
        if not category:
            raise NotFoundError("CostCategory", costo_data.categoria_id)
        
        costo = Costo(
            **costo_data.model_dump(),
            created_by=user_id
        )
        
        self.db.add(costo)
        self.db.commit()
        self.db.refresh(costo)
        
        return costo
    
    def get_costos(
        self,
        skip: int = 0,
        limit: int = 100,
        categoria_id: Optional[int] = None,
        estado: Optional[str] = None,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        search: Optional[str] = None
    ) -> List[Costo]:
        """
        Get costos with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Number of records to return
            categoria_id: Filter by category ID
            estado: Filter by estado
            fecha_desde: Filter by date from
            fecha_hasta: Filter by date to
            search: Search term for descripcion or proveedor
            
        Returns:
            List[Costo]: List of costos
        """
        query = self.db.query(Costo)
        
        if categoria_id:
            query = query.filter(Costo.categoria_id == categoria_id)
        
        if estado:
            query = query.filter(Costo.estado == estado)
        
        if fecha_desde:
            query = query.filter(Costo.fecha >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(Costo.fecha <= fecha_hasta)
        
        if search:
            query = query.filter(
                or_(
                    Costo.descripcion.ilike(f"%{search}%"),
                    Costo.proveedor.ilike(f"%{search}%")
                )
            )
        
        return query.order_by(Costo.fecha.desc()).offset(skip).limit(limit).all()
    
    def get_costo(self, costo_id: int) -> Optional[Costo]:
        """
        Get costo by ID.
        
        Args:
            costo_id: Costo ID
            
        Returns:
            Optional[Costo]: Costo if found
        """
        return self.db.query(Costo).filter(Costo.id == costo_id).first()
    
    def update_costo(self, costo_id: int, costo_data: CostoUpdate) -> Optional[Costo]:
        """
        Update costo.
        
        Args:
            costo_id: Costo ID
            costo_data: Costo update data
            
        Returns:
            Optional[Costo]: Updated costo if found
        """
        costo = self.get_costo(costo_id)
        if not costo:
            return None
        
        update_data = costo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(costo, field, value)
        
        self.db.commit()
        self.db.refresh(costo)
        
        return costo
    
    def delete_costo(self, costo_id: int) -> bool:
        """
        Delete costo.
        
        Args:
            costo_id: Costo ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        costo = self.get_costo(costo_id)
        if not costo:
            return False
        
        self.db.delete(costo)
        self.db.commit()
        
        return True
    
    def get_costos_summary(
        self,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ) -> dict:
        """
        Get costos summary statistics.
        
        Args:
            fecha_desde: Filter by date from
            fecha_hasta: Filter by date to
            
        Returns:
            dict: Costos summary
        """
        query = self.db.query(Costo)
        
        if fecha_desde:
            query = query.filter(Costo.fecha >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(Costo.fecha <= fecha_hasta)
        
        costos = query.all()
        
        # Group by tipo (from category)
        gastos = []
        ingresos = []
        costos_directos = []
        
        for costo in costos:
            category = self.db.query(CostCategory).filter(
                CostCategory.id == costo.categoria_id
            ).first()
            
            if category:
                if category.tipo == "gasto":
                    gastos.append(costo)
                elif category.tipo == "ingreso":
                    ingresos.append(costo)
                else:
                    costos_directos.append(costo)
        
        total_gastos = sum(c.monto for c in gastos)
        total_ingresos = sum(c.monto for c in ingresos)
        total_costos = sum(c.monto for c in costos_directos)
        
        # Status summary
        pendientes = sum(c.monto for c in costos if c.estado == "pendiente")
        pagados = sum(c.monto for c in costos if c.estado == "pagado")
        
        return {
            "total_registros": len(costos),
            "total_gastos": float(total_gastos),
            "total_ingresos": float(total_ingresos),
            "total_costos": float(total_costos),
            "total_pendiente": float(pendientes),
            "total_pagado": float(pagados),
            "utilidad_bruta": float(total_ingresos - total_costos),
            "utilidad_neta": float(total_ingresos - total_costos - total_gastos)
        }
    
    def get_costos_by_category(
        self,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ) -> List[dict]:
        """
        Get costos grouped by category.
        
        Args:
            fecha_desde: Filter by date from
            fecha_hasta: Filter by date to
            
        Returns:
            List[dict]: Costos grouped by category
        """
        query = self.db.query(
            CostCategory.name,
            CostCategory.tipo,
            func.count(Costo.id).label("count"),
            func.sum(Costo.monto).label("total")
        ).join(Costo).group_by(CostCategory.id, CostCategory.name, CostCategory.tipo)
        
        if fecha_desde:
            query = query.filter(Costo.fecha >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(Costo.fecha <= fecha_hasta)
        
        results = query.all()
        
        return [
            {
                "categoria": r.name,
                "tipo": r.tipo,
                "cantidad": r.count,
                "total": float(r.total or 0)
            }
            for r in results
        ]
    
    def get_monthly_report(self, year: int, month: int) -> dict:
        """
        Get monthly financial report.
        
        Args:
            year: Year
            month: Month (1-12)
            
        Returns:
            dict: Monthly report
        """
        query = self.db.query(Costo).filter(
            extract('year', Costo.fecha) == year,
            extract('month', Costo.fecha) == month
        )
        
        costos = query.all()
        
        # Group by category type
        gastos = []
        ingresos = []
        costos_directos = []
        
        for costo in costos:
            category = self.db.query(CostCategory).filter(
                CostCategory.id == costo.categoria_id
            ).first()
            
            if category:
                if category.tipo == "gasto":
                    gastos.append(costo)
                elif category.tipo == "ingreso":
                    ingresos.append(costo)
                else:
                    costos_directos.append(costo)
        
        total_gastos = sum(c.monto for c in gastos)
        total_ingresos = sum(c.monto for c in ingresos)
        total_costos = sum(c.monto for c in costos_directos)
        
        return {
            "year": year,
            "month": month,
            "total_ingresos": float(total_ingresos),
            "total_gastos": float(total_gastos),
            "total_costos": float(total_costos),
            "utilidad_bruta": float(total_ingresos - total_costos),
            "utilidad_neta": float(total_ingresos - total_costos - total_gastos),
            "margen_bruto": float((total_ingresos - total_costos) / total_ingresos * 100) if total_ingresos > 0 else 0,
            "margen_neto": float((total_ingresos - total_costos - total_gastos) / total_ingresos * 100) if total_ingresos > 0 else 0
        }
    
    # Category operations
    def create_category(self, category_data: CostCategoryCreate) -> CostCategory:
        """
        Create a new cost category.
        
        Args:
            category_data: Category creation data
            
        Returns:
            CostCategory: Created category
        """
        category = CostCategory(**category_data.model_dump())
        
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        
        return category
    
    def get_categories(self, active_only: bool = True) -> List[CostCategory]:
        """
        Get cost categories.
        
        Args:
            active_only: Whether to return only active categories
            
        Returns:
            List[CostCategory]: List of categories
        """
        query = self.db.query(CostCategory)
        
        if active_only:
            query = query.filter(CostCategory.is_active == True)
        
        return query.order_by(CostCategory.sort_order, CostCategory.name).all()
    
    def get_category(self, category_id: int) -> Optional[CostCategory]:
        """
        Get category by ID.
        
        Args:
            category_id: Category ID
            
        Returns:
            Optional[CostCategory]: Category if found
        """
        return self.db.query(CostCategory).filter(CostCategory.id == category_id).first()
    
    def update_category(
        self,
        category_id: int,
        category_data: CostCategoryUpdate
    ) -> Optional[CostCategory]:
        """
        Update cost category.
        
        Args:
            category_id: Category ID
            category_data: Category update data
            
        Returns:
            Optional[CostCategory]: Updated category if found
        """
        category = self.get_category(category_id)
        if not category:
            return None
        
        update_data = category_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        
        self.db.commit()
        self.db.refresh(category)
        
        return category
    
    def delete_category(self, category_id: int) -> bool:
        """
        Delete cost category.
        
        Args:
            category_id: Category ID
            
        Returns:
            bool: True if deleted, False if not found
            
        Raises:
            BusinessLogicError: If category has associated costos
        """
        category = self.get_category(category_id)
        if not category:
            return False
        
        # Check if category has costos
        costos_count = self.db.query(Costo).filter(
            Costo.categoria_id == category_id
        ).count()
        
        if costos_count > 0:
            raise BusinessLogicError(
                f"Cannot delete category with {costos_count} associated costs"
            )
        
        self.db.delete(category)
        self.db.commit()
        
        return True






