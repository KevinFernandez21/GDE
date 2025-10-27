"""
Report service for generating analytics and reports.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, date, timedelta
from decimal import Decimal

from ..models.product import Product, Kardex
from ..models.guia import Guia, GuiaItem
from ..models.costo import Costo, CostCategory
from ..models.pistoleo import PistoleoSession, Escaneo


class ReportService:
    """Service for generating reports and analytics."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """
        Get dashboard summary with key metrics.
        
        Returns:
            Dict[str, Any]: Dashboard summary
        """
        # Products summary
        total_products = self.db.query(Product).filter(Product.status == "active").count()
        low_stock_products = self.db.query(Product).filter(
            Product.stock_actual <= Product.stock_minimo,
            Product.status == "active"
        ).count()
        out_of_stock_products = self.db.query(Product).filter(
            Product.stock_actual == 0,
            Product.status == "active"
        ).count()
        
        # Inventory value
        products = self.db.query(Product).filter(Product.status == "active").all()
        inventory_value = sum(
            (p.stock_actual or 0) * (p.precio_compra or 0) for p in products
        )
        
        # Guias summary (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        total_guias = self.db.query(Guia).filter(
            Guia.fecha_creacion >= thirty_days_ago
        ).count()
        
        guias_pendientes = self.db.query(Guia).filter(
            Guia.estado == "pendiente"
        ).count()
        
        guias_en_transito = self.db.query(Guia).filter(
            Guia.estado == "en_transito"
        ).count()
        
        guias_entregadas = self.db.query(Guia).filter(
            Guia.fecha_creacion >= thirty_days_ago,
            Guia.estado == "entregada"
        ).count()
        
        # Recent movements
        recent_movements = self.db.query(Kardex).order_by(
            Kardex.fecha_movimiento.desc()
        ).limit(10).all()
        
        return {
            "products": {
                "total": total_products,
                "low_stock": low_stock_products,
                "out_of_stock": out_of_stock_products,
                "inventory_value": float(inventory_value)
            },
            "guias": {
                "total_last_30_days": total_guias,
                "pendientes": guias_pendientes,
                "en_transito": guias_en_transito,
                "entregadas_last_30_days": guias_entregadas
            },
            "recent_movements": [
                {
                    "id": m.id,
                    "product_id": m.product_id,
                    "tipo_movimiento": m.tipo_movimiento,
                    "cantidad": m.cantidad,
                    "fecha_movimiento": m.fecha_movimiento
                }
                for m in recent_movements
            ]
        }
    
    def get_inventory_report(
        self,
        category_id: Optional[int] = None,
        low_stock_only: bool = False
    ) -> Dict[str, Any]:
        """
        Get detailed inventory report.
        
        Args:
            category_id: Optional category filter
            low_stock_only: Whether to show only low stock products
            
        Returns:
            Dict[str, Any]: Inventory report
        """
        query = self.db.query(Product).filter(Product.status == "active")
        
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        if low_stock_only:
            query = query.filter(Product.stock_actual <= Product.stock_minimo)
        
        products = query.all()
        
        total_value = sum(
            (p.stock_actual or 0) * (p.precio_compra or 0) for p in products
        )
        
        total_units = sum(p.stock_actual or 0 for p in products)
        
        products_by_category = {}
        for product in products:
            if product.category_id:
                if product.category_id not in products_by_category:
                    products_by_category[product.category_id] = []
                products_by_category[product.category_id].append(product)
        
        return {
            "total_products": len(products),
            "total_units": total_units,
            "total_value": float(total_value),
            "products": [
                {
                    "id": p.id,
                    "code": p.code,
                    "name": p.name,
                    "stock_actual": p.stock_actual,
                    "stock_minimo": p.stock_minimo,
                    "precio_compra": float(p.precio_compra or 0),
                    "valor_inventario": float((p.stock_actual or 0) * (p.precio_compra or 0))
                }
                for p in products
            ]
        }
    
    def get_sales_report(
        self,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Get sales report based on guide items.
        
        Args:
            fecha_desde: Start date
            fecha_hasta: End date
            
        Returns:
            Dict[str, Any]: Sales report
        """
        # Default to last 30 days if no dates provided
        if not fecha_desde:
            fecha_desde = date.today() - timedelta(days=30)
        if not fecha_hasta:
            fecha_hasta = date.today()
        
        # Get guias in date range
        guias = self.db.query(Guia).filter(
            Guia.fecha_creacion >= datetime.combine(fecha_desde, datetime.min.time()),
            Guia.fecha_creacion <= datetime.combine(fecha_hasta, datetime.max.time())
        ).all()
        
        # Get all items from these guias
        guia_ids = [g.id for g in guias]
        items = self.db.query(GuiaItem).filter(GuiaItem.guia_id.in_(guia_ids)).all() if guia_ids else []
        
        total_items = len(items)
        total_quantity = sum(item.cantidad for item in items)
        total_value = sum(float(item.subtotal or 0) for item in items)
        
        # Group by product
        products_sold = {}
        for item in items:
            if item.product_id not in products_sold:
                products_sold[item.product_id] = {
                    "product_id": item.product_id,
                    "quantity": 0,
                    "value": 0
                }
            products_sold[item.product_id]["quantity"] += item.cantidad
            products_sold[item.product_id]["value"] += float(item.subtotal or 0)
        
        return {
            "period": {
                "fecha_desde": fecha_desde.isoformat(),
                "fecha_hasta": fecha_hasta.isoformat()
            },
            "summary": {
                "total_guias": len(guias),
                "total_items": total_items,
                "total_quantity": total_quantity,
                "total_value": total_value
            },
            "products_sold": list(products_sold.values()),
            "guias_by_status": {
                "pendiente": len([g for g in guias if g.estado == "pendiente"]),
                "en_transito": len([g for g in guias if g.estado == "en_transito"]),
                "entregada": len([g for g in guias if g.estado == "entregada"]),
                "devuelta": len([g for g in guias if g.estado == "devuelta"]),
                "cancelada": len([g for g in guias if g.estado == "cancelada"])
            }
        }
    
    def get_financial_report(
        self,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Get financial report with income, expenses, and profit.
        
        Args:
            fecha_desde: Start date
            fecha_hasta: End date
            
        Returns:
            Dict[str, Any]: Financial report
        """
        # Default to current month if no dates provided
        if not fecha_desde:
            fecha_desde = date.today().replace(day=1)
        if not fecha_hasta:
            fecha_hasta = date.today()
        
        query = self.db.query(Costo).filter(
            Costo.fecha >= fecha_desde,
            Costo.fecha <= fecha_hasta
        )
        
        costos = query.all()
        
        # Categorize by type
        ingresos = []
        gastos = []
        costos_directos = []
        
        for costo in costos:
            category = self.db.query(CostCategory).filter(
                CostCategory.id == costo.categoria_id
            ).first()
            
            if category:
                if category.tipo == "ingreso":
                    ingresos.append(costo)
                elif category.tipo == "gasto":
                    gastos.append(costo)
                else:
                    costos_directos.append(costo)
        
        total_ingresos = sum(float(c.monto) for c in ingresos)
        total_gastos = sum(float(c.monto) for c in gastos)
        total_costos = sum(float(c.monto) for c in costos_directos)
        
        utilidad_bruta = total_ingresos - total_costos
        utilidad_neta = utilidad_bruta - total_gastos
        
        return {
            "period": {
                "fecha_desde": fecha_desde.isoformat(),
                "fecha_hasta": fecha_hasta.isoformat()
            },
            "ingresos": {
                "total": total_ingresos,
                "count": len(ingresos)
            },
            "costos": {
                "total": total_costos,
                "count": len(costos_directos)
            },
            "gastos": {
                "total": total_gastos,
                "count": len(gastos)
            },
            "utilidad_bruta": utilidad_bruta,
            "utilidad_neta": utilidad_neta,
            "margen_bruto": (utilidad_bruta / total_ingresos * 100) if total_ingresos > 0 else 0,
            "margen_neto": (utilidad_neta / total_ingresos * 100) if total_ingresos > 0 else 0
        }
    
    def get_scanning_report(
        self,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get scanning activity report.
        
        Args:
            fecha_desde: Start datetime
            fecha_hasta: End datetime
            
        Returns:
            Dict[str, Any]: Scanning report
        """
        # Default to last 7 days if no dates provided
        if not fecha_desde:
            fecha_desde = datetime.utcnow() - timedelta(days=7)
        if not fecha_hasta:
            fecha_hasta = datetime.utcnow()
        
        sessions = self.db.query(PistoleoSession).filter(
            PistoleoSession.fecha_inicio >= fecha_desde,
            PistoleoSession.fecha_inicio <= fecha_hasta
        ).all()
        
        scans = self.db.query(Escaneo).filter(
            Escaneo.fecha_escaneo >= fecha_desde,
            Escaneo.fecha_escaneo <= fecha_hasta
        ).all()
        
        total_sessions = len(sessions)
        active_sessions = len([s for s in sessions if s.estado == "active"])
        completed_sessions = len([s for s in sessions if s.estado == "completed"])
        
        total_scans = len(scans)
        successful_scans = len([s for s in scans if s.estado_escaneo == "success"])
        error_scans = len([s for s in scans if s.estado_escaneo == "error"])
        duplicate_scans = len([s for s in scans if s.estado_escaneo == "duplicate"])
        
        return {
            "period": {
                "fecha_desde": fecha_desde.isoformat(),
                "fecha_hasta": fecha_hasta.isoformat()
            },
            "sessions": {
                "total": total_sessions,
                "active": active_sessions,
                "completed": completed_sessions
            },
            "scans": {
                "total": total_scans,
                "successful": successful_scans,
                "errors": error_scans,
                "duplicates": duplicate_scans,
                "success_rate": (successful_scans / total_scans * 100) if total_scans > 0 else 0
            }
        }
    
    def get_top_products(
        self,
        limit: int = 10,
        by: str = "sales"  # sales, stock_value, movements
    ) -> List[Dict[str, Any]]:
        """
        Get top products by different criteria.
        
        Args:
            limit: Number of products to return
            by: Criteria (sales, stock_value, movements)
            
        Returns:
            List[Dict[str, Any]]: Top products
        """
        if by == "stock_value":
            products = self.db.query(Product).filter(Product.status == "active").all()
            products_with_value = [
                {
                    "id": p.id,
                    "code": p.code,
                    "name": p.name,
                    "stock_actual": p.stock_actual,
                    "precio_compra": float(p.precio_compra or 0),
                    "value": float((p.stock_actual or 0) * (p.precio_compra or 0))
                }
                for p in products
            ]
            products_with_value.sort(key=lambda x: x["value"], reverse=True)
            return products_with_value[:limit]
        
        elif by == "movements":
            # Get products with most kardex movements
            result = self.db.query(
                Kardex.product_id,
                func.count(Kardex.id).label("movement_count")
            ).group_by(Kardex.product_id).order_by(
                func.count(Kardex.id).desc()
            ).limit(limit).all()
            
            top_products = []
            for product_id, count in result:
                product = self.db.query(Product).filter(Product.id == product_id).first()
                if product:
                    top_products.append({
                        "id": product.id,
                        "code": product.code,
                        "name": product.name,
                        "movement_count": count
                    })
            
            return top_products
        
        else:  # by sales
            # Get products most sold (from guia_items)
            result = self.db.query(
                GuiaItem.product_id,
                func.sum(GuiaItem.cantidad).label("total_quantity"),
                func.sum(GuiaItem.subtotal).label("total_value")
            ).group_by(GuiaItem.product_id).order_by(
                func.sum(GuiaItem.cantidad).desc()
            ).limit(limit).all()
            
            top_products = []
            for product_id, quantity, value in result:
                product = self.db.query(Product).filter(Product.id == product_id).first()
                if product:
                    top_products.append({
                        "id": product.id,
                        "code": product.code,
                        "name": product.name,
                        "quantity_sold": quantity,
                        "sales_value": float(value or 0)
                    })
            
            return top_products






