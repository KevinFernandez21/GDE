"""
Guia (dispatch guide) service for business logic.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime

from ..models.guia import Guia, GuiaItem, GuiaMovement
from ..models.product import Product
from ..schemas.guia import (
    GuiaCreate, GuiaUpdate,
    GuiaItemCreate, GuiaItemUpdate,
    GuiaMovementCreate, GuiaStatusUpdate
)
from ..core.exceptions import NotFoundError, BusinessLogicError


class GuiaService:
    """Service for managing dispatch guides."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_guia(self, guia_data: GuiaCreate, user_id: str) -> Guia:
        """
        Create a new guia.
        
        Args:
            guia_data: Guia creation data
            user_id: User creating the guia
            
        Returns:
            Guia: Created guia
            
        Raises:
            BusinessLogicError: If guia code already exists
        """
        # Check if codigo already exists
        existing = self.db.query(Guia).filter(Guia.codigo == guia_data.codigo).first()
        if existing:
            raise BusinessLogicError(f"Guia with code {guia_data.codigo} already exists")
        
        guia = Guia(
            **guia_data.model_dump(),
            created_by=user_id
        )
        
        self.db.add(guia)
        self.db.commit()
        self.db.refresh(guia)
        
        # Create initial movement
        movement = GuiaMovement(
            guia_id=guia.id,
            usuario_id=user_id,
            accion="Creada",
            observaciones="Guía creada en el sistema"
        )
        self.db.add(movement)
        self.db.commit()
        
        return guia
    
    def get_guias(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        estado: Optional[str] = None,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None
    ) -> List[Guia]:
        """
        Get guias with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Number of records to return
            search: Search term for codigo or cliente_nombre
            estado: Filter by estado
            fecha_desde: Filter by creation date from
            fecha_hasta: Filter by creation date to
            
        Returns:
            List[Guia]: List of guias
        """
        query = self.db.query(Guia)
        
        if search:
            query = query.filter(
                or_(
                    Guia.codigo.ilike(f"%{search}%"),
                    Guia.cliente_nombre.ilike(f"%{search}%")
                )
            )
        
        if estado:
            query = query.filter(Guia.estado == estado)
        
        if fecha_desde:
            query = query.filter(Guia.fecha_creacion >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(Guia.fecha_creacion <= fecha_hasta)
        
        return query.offset(skip).limit(limit).all()
    
    def get_guia(self, guia_id: int) -> Optional[Guia]:
        """
        Get guia by ID.
        
        Args:
            guia_id: Guia ID
            
        Returns:
            Optional[Guia]: Guia if found
        """
        return self.db.query(Guia).filter(Guia.id == guia_id).first()
    
    def get_guia_by_codigo(self, codigo: str) -> Optional[Guia]:
        """
        Get guia by codigo.
        
        Args:
            codigo: Guia codigo
            
        Returns:
            Optional[Guia]: Guia if found
        """
        return self.db.query(Guia).filter(Guia.codigo == codigo).first()
    
    def update_guia(self, guia_id: int, guia_data: GuiaUpdate, user_id: str) -> Optional[Guia]:
        """
        Update guia.
        
        Args:
            guia_id: Guia ID
            guia_data: Guia update data
            user_id: User updating the guia
            
        Returns:
            Optional[Guia]: Updated guia if found
        """
        guia = self.get_guia(guia_id)
        if not guia:
            return None
        
        update_data = guia_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(guia, field, value)
        
        self.db.commit()
        self.db.refresh(guia)
        
        return guia
    
    def update_guia_status(self, guia_id: int, status_data: GuiaStatusUpdate, user_id: str) -> Optional[Guia]:
        """
        Update guia status and create movement record.
        
        Args:
            guia_id: Guia ID
            status_data: Status update data
            user_id: User updating the status
            
        Returns:
            Optional[Guia]: Updated guia if found
        """
        guia = self.get_guia(guia_id)
        if not guia:
            return None
        
        old_estado = guia.estado
        guia.estado = status_data.estado
        
        if status_data.ubicacion:
            guia.ubicacion_actual = status_data.ubicacion
        
        # Create movement record
        movement = GuiaMovement(
            guia_id=guia.id,
            usuario_id=user_id,
            accion=f"Cambio de estado: {old_estado} → {status_data.estado}",
            ubicacion=status_data.ubicacion,
            observaciones=status_data.observaciones,
            evidencias=status_data.evidencias
        )
        self.db.add(movement)
        
        # If delivered, set delivery date
        if status_data.estado == "entregada" and not guia.fecha_entrega_real:
            guia.fecha_entrega_real = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(guia)
        
        return guia
    
    def delete_guia(self, guia_id: int) -> bool:
        """
        Delete guia.
        
        Args:
            guia_id: Guia ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        guia = self.get_guia(guia_id)
        if not guia:
            return False
        
        self.db.delete(guia)
        self.db.commit()
        
        return True
    
    # Guia Items
    def add_guia_item(self, item_data: GuiaItemCreate, user_id: str) -> GuiaItem:
        """
        Add item to guia.
        
        Args:
            item_data: Guia item data
            user_id: User adding the item
            
        Returns:
            GuiaItem: Created guia item
            
        Raises:
            NotFoundError: If guia or product not found
            BusinessLogicError: If insufficient stock
        """
        guia = self.get_guia(item_data.guia_id)
        if not guia:
            raise NotFoundError("Guia", item_data.guia_id)
        
        product = self.db.query(Product).filter(Product.id == item_data.product_id).first()
        if not product:
            raise NotFoundError("Product", item_data.product_id)
        
        # Check stock
        if product.stock_actual < item_data.cantidad:
            raise BusinessLogicError(
                f"Insufficient stock for product {product.name}. Available: {product.stock_actual}"
            )
        
        # Calculate subtotal
        item = GuiaItem(**item_data.model_dump())
        if item_data.precio_unitario:
            item.subtotal = item_data.precio_unitario * item_data.cantidad - item_data.descuento
        
        self.db.add(item)
        
        # Update product stock
        product.stock_actual -= item_data.cantidad
        
        self.db.commit()
        self.db.refresh(item)
        
        return item
    
    def get_guia_items(self, guia_id: int) -> List[GuiaItem]:
        """
        Get all items for a guia.
        
        Args:
            guia_id: Guia ID
            
        Returns:
            List[GuiaItem]: List of guia items
        """
        return self.db.query(GuiaItem).filter(GuiaItem.guia_id == guia_id).all()
    
    def update_guia_item(self, item_id: int, item_data: GuiaItemUpdate) -> Optional[GuiaItem]:
        """
        Update guia item.
        
        Args:
            item_id: Guia item ID
            item_data: Guia item update data
            
        Returns:
            Optional[GuiaItem]: Updated guia item if found
        """
        item = self.db.query(GuiaItem).filter(GuiaItem.id == item_id).first()
        if not item:
            return None
        
        update_data = item_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)
        
        self.db.commit()
        self.db.refresh(item)
        
        return item
    
    def delete_guia_item(self, item_id: int) -> bool:
        """
        Delete guia item.
        
        Args:
            item_id: Guia item ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        item = self.db.query(GuiaItem).filter(GuiaItem.id == item_id).first()
        if not item:
            return False
        
        # Restore product stock
        product = self.db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock_actual += item.cantidad
        
        self.db.delete(item)
        self.db.commit()
        
        return True
    
    # Guia Movements
    def add_guia_movement(self, movement_data: GuiaMovementCreate, user_id: str) -> GuiaMovement:
        """
        Add movement to guia.
        
        Args:
            movement_data: Guia movement data
            user_id: User adding the movement
            
        Returns:
            GuiaMovement: Created guia movement
            
        Raises:
            NotFoundError: If guia not found
        """
        guia = self.get_guia(movement_data.guia_id)
        if not guia:
            raise NotFoundError("Guia", movement_data.guia_id)
        
        movement = GuiaMovement(
            **movement_data.model_dump(),
            usuario_id=user_id
        )
        
        self.db.add(movement)
        self.db.commit()
        self.db.refresh(movement)
        
        return movement
    
    def get_guia_movements(self, guia_id: int) -> List[GuiaMovement]:
        """
        Get all movements for a guia.
        
        Args:
            guia_id: Guia ID
            
        Returns:
            List[GuiaMovement]: List of guia movements
        """
        return self.db.query(GuiaMovement).filter(
            GuiaMovement.guia_id == guia_id
        ).order_by(GuiaMovement.fecha_movimiento.desc()).all()
    
    def get_guia_tracking(self, codigo: str) -> Optional[dict]:
        """
        Get guia tracking information.
        
        Args:
            codigo: Guia codigo
            
        Returns:
            Optional[dict]: Guia tracking information if found
        """
        guia = self.get_guia_by_codigo(codigo)
        if not guia:
            return None
        
        movements = self.get_guia_movements(guia.id)
        
        return {
            "guia_id": guia.id,
            "codigo": guia.codigo,
            "estado": guia.estado,
            "ubicacion_actual": guia.ubicacion_actual,
            "fecha_creacion": guia.fecha_creacion,
            "fecha_estimada_entrega": guia.fecha_estimada_entrega,
            "fecha_entrega_real": guia.fecha_entrega_real,
            "movimientos": movements
        }






