"""
Kardex service for inventory movements.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta
from decimal import Decimal

from ..models.product import Product, Kardex
from ..schemas.product import KardexCreate
from ..core.exceptions import NotFoundError, BusinessLogicError


class KardexService:
    """Service for managing inventory movements (Kardex)."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_kardex_entry(
        self,
        product_id: int,
        tipo_movimiento: str,
        cantidad: int,
        documento_asociado: Optional[str] = None,
        referencia: Optional[str] = None,
        costo_unitario: Optional[Decimal] = None,
        usuario_id: Optional[str] = None,
        observaciones: Optional[str] = None
    ) -> Kardex:
        """
        Create a kardex entry for inventory movement.
        
        Args:
            product_id: Product ID
            tipo_movimiento: Movement type (entrada, salida, ajuste, transferencia)
            cantidad: Quantity (positive or negative)
            documento_asociado: Associated document
            referencia: Reference
            costo_unitario: Unit cost
            usuario_id: User performing the movement
            observaciones: Observations
            
        Returns:
            Kardex: Created kardex entry
            
        Raises:
            NotFoundError: If product not found
            BusinessLogicError: If invalid movement
        """
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise NotFoundError("Product", product_id)
        
        # Validate movement type and cantidad
        if tipo_movimiento in ["salida", "transferencia"] and cantidad > product.stock_actual:
            raise BusinessLogicError(
                f"Insufficient stock for {tipo_movimiento}. Available: {product.stock_actual}, Requested: {cantidad}"
            )
        
        # Get previous balance
        saldo_anterior = product.stock_actual
        
        # Calculate new balance
        if tipo_movimiento == "entrada":
            saldo_actual = saldo_anterior + cantidad
        elif tipo_movimiento in ["salida", "transferencia"]:
            saldo_actual = saldo_anterior - cantidad
        else:  # ajuste
            saldo_actual = cantidad  # For adjustments, cantidad is the new total
            cantidad = saldo_actual - saldo_anterior
        
        # Calculate average cost
        if costo_unitario and tipo_movimiento == "entrada":
            valor_anterior = saldo_anterior * (product.precio_compra or 0)
            valor_nuevo = cantidad * costo_unitario
            valor_total = valor_anterior + valor_nuevo
            costo_promedio = valor_total / saldo_actual if saldo_actual > 0 else 0
        else:
            costo_promedio = product.precio_compra or 0
        
        # Create kardex entry
        kardex = Kardex(
            product_id=product_id,
            tipo_movimiento=tipo_movimiento,
            documento_asociado=documento_asociado,
            referencia=referencia,
            cantidad=abs(cantidad),
            saldo_anterior=saldo_anterior,
            saldo_actual=saldo_actual,
            costo_unitario=costo_unitario,
            costo_promedio=costo_promedio,
            valor_total=abs(cantidad) * (costo_unitario or costo_promedio),
            usuario_id=usuario_id,
            observaciones=observaciones
        )
        
        self.db.add(kardex)
        
        # Update product stock and average cost
        product.stock_actual = saldo_actual
        if costo_promedio:
            product.precio_compra = costo_promedio
        
        self.db.commit()
        self.db.refresh(kardex)
        
        return kardex
    
    def get_kardex_by_product(
        self,
        product_id: int,
        skip: int = 0,
        limit: int = 100,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None
    ) -> List[Kardex]:
        """
        Get kardex entries for a product.
        
        Args:
            product_id: Product ID
            skip: Number of records to skip
            limit: Number of records to return
            fecha_desde: Filter by date from
            fecha_hasta: Filter by date to
            
        Returns:
            List[Kardex]: List of kardex entries
        """
        query = self.db.query(Kardex).filter(Kardex.product_id == product_id)
        
        if fecha_desde:
            query = query.filter(Kardex.fecha_movimiento >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(Kardex.fecha_movimiento <= fecha_hasta)
        
        return query.order_by(desc(Kardex.fecha_movimiento)).offset(skip).limit(limit).all()
    
    def get_kardex_summary(
        self,
        product_id: Optional[int] = None,
        tipo_movimiento: Optional[str] = None,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None
    ) -> dict:
        """
        Get kardex summary statistics.
        
        Args:
            product_id: Optional product ID filter
            tipo_movimiento: Optional movement type filter
            fecha_desde: Filter by date from
            fecha_hasta: Filter by date to
            
        Returns:
            dict: Kardex summary statistics
        """
        query = self.db.query(Kardex)
        
        if product_id:
            query = query.filter(Kardex.product_id == product_id)
        
        if tipo_movimiento:
            query = query.filter(Kardex.tipo_movimiento == tipo_movimiento)
        
        if fecha_desde:
            query = query.filter(Kardex.fecha_movimiento >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(Kardex.fecha_movimiento <= fecha_hasta)
        
        entries = query.all()
        
        total_entradas = sum(
            k.cantidad for k in entries if k.tipo_movimiento == "entrada"
        )
        total_salidas = sum(
            k.cantidad for k in entries if k.tipo_movimiento == "salida"
        )
        total_ajustes = sum(
            k.cantidad for k in entries if k.tipo_movimiento == "ajuste"
        )
        
        return {
            "total_movimientos": len(entries),
            "total_entradas": total_entradas,
            "total_salidas": total_salidas,
            "total_ajustes": total_ajustes,
            "saldo_neto": total_entradas - total_salidas
        }
    
    def get_product_movements_report(
        self,
        product_id: int,
        days: int = 30
    ) -> dict:
        """
        Get product movements report for the last N days.
        
        Args:
            product_id: Product ID
            days: Number of days to look back
            
        Returns:
            dict: Product movements report
        """
        fecha_desde = datetime.utcnow() - timedelta(days=days)
        
        movements = self.get_kardex_by_product(
            product_id=product_id,
            fecha_desde=fecha_desde,
            limit=1000
        )
        
        product = self.db.query(Product).filter(Product.id == product_id).first()
        
        return {
            "product_id": product_id,
            "product_code": product.code if product else None,
            "product_name": product.name if product else None,
            "current_stock": product.stock_actual if product else 0,
            "period_days": days,
            "total_movements": len(movements),
            "movements": movements
        }
    
    def adjust_stock(
        self,
        product_id: int,
        new_stock: int,
        usuario_id: str,
        observaciones: str
    ) -> Kardex:
        """
        Adjust product stock to a specific value.
        
        Args:
            product_id: Product ID
            new_stock: New stock value
            usuario_id: User performing the adjustment
            observaciones: Reason for adjustment
            
        Returns:
            Kardex: Created kardex entry
        """
        return self.create_kardex_entry(
            product_id=product_id,
            tipo_movimiento="ajuste",
            cantidad=new_stock,
            documento_asociado="AJUSTE",
            usuario_id=usuario_id,
            observaciones=observaciones
        )
    
    def transfer_stock(
        self,
        product_id: int,
        cantidad: int,
        destino: str,
        usuario_id: str,
        observaciones: Optional[str] = None
    ) -> Kardex:
        """
        Transfer stock (reduce from current location).
        
        Args:
            product_id: Product ID
            cantidad: Quantity to transfer
            destino: Destination location
            usuario_id: User performing the transfer
            observaciones: Transfer observations
            
        Returns:
            Kardex: Created kardex entry
        """
        return self.create_kardex_entry(
            product_id=product_id,
            tipo_movimiento="transferencia",
            cantidad=cantidad,
            documento_asociado="TRANSFERENCIA",
            referencia=f"Destino: {destino}",
            usuario_id=usuario_id,
            observaciones=observaciones
        )






