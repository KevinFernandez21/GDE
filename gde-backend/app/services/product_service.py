"""
Product service for business logic.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from decimal import Decimal

from ..models.product import Product, Category, Kardex
from ..schemas.product import (
    ProductCreate, 
    ProductUpdate, 
    CategoryCreate, 
    CategoryUpdate,
    KardexCreate
)
from ..core.exceptions import NotFoundError, BusinessLogicError, ConflictError


class ProductService:
    """Service for product-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Product operations
    def create_product(self, product_data: ProductCreate, user_id: str) -> Product:
        """
        Create a new product.
        
        Args:
            product_data: Product creation data
            user_id: ID of the user creating the product
            
        Returns:
            Product: Created product
            
        Raises:
            ConflictError: If product code already exists
        """
        # Check if product code already exists
        existing_product = self.db.query(Product).filter(
            Product.code == product_data.code
        ).first()
        
        if existing_product:
            raise ConflictError(
                f"Product with code '{product_data.code}' already exists"
            )
        
        # Create product
        product = Product(
            **product_data.dict(),
            created_by=user_id
        )
        
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        
        # Create initial kardex entry
        self._create_kardex_entry(
            product_id=product.id,
            tipo_movimiento="entrada",
            documento_asociado="CREACION",
            cantidad=product.stock_actual,
            saldo_anterior=0,
            saldo_actual=product.stock_actual,
            costo_unitario=product.precio_compra,
            usuario_id=user_id
        )
        
        return product
    
    def get_products(
        self, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Product]:
        """
        Get products with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Number of records to return
            search: Search term for name or code
            category_id: Filter by category
            status: Filter by status
            
        Returns:
            List[Product]: List of products
        """
        query = self.db.query(Product)
        
        # Apply filters
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.code.ilike(f"%{search}%")
                )
            )
        
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        if status:
            query = query.filter(Product.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """
        Get product by ID.
        
        Args:
            product_id: Product ID
            
        Returns:
            Optional[Product]: Product if found
        """
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_product_by_code(self, code: str) -> Optional[Product]:
        """
        Get product by code.
        
        Args:
            code: Product code
            
        Returns:
            Optional[Product]: Product if found
        """
        return self.db.query(Product).filter(Product.code == code).first()
    
    def update_product(
        self, 
        product_id: int, 
        product_data: ProductUpdate,
        user_id: str
    ) -> Optional[Product]:
        """
        Update product.
        
        Args:
            product_id: Product ID
            product_data: Product update data
            user_id: ID of the user updating the product
            
        Returns:
            Optional[Product]: Updated product if found
            
        Raises:
            NotFoundError: If product not found
            ConflictError: If new code already exists
        """
        product = self.get_product(product_id)
        if not product:
            raise NotFoundError("Product", product_id)
        
        # Check if new code conflicts with existing product
        if product_data.code and product_data.code != product.code:
            existing_product = self.get_product_by_code(product_data.code)
            if existing_product:
                raise ConflictError(
                    f"Product with code '{product_data.code}' already exists"
                )
        
        # Store old stock for kardex
        old_stock = product.stock_actual
        
        # Update product
        update_data = product_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        self.db.commit()
        self.db.refresh(product)
        
        # Create kardex entry if stock changed
        if product_data.stock_actual is not None and product_data.stock_actual != old_stock:
            self._create_kardex_entry(
                product_id=product.id,
                tipo_movimiento="ajuste",
                documento_asociado="ACTUALIZACION",
                cantidad=abs(product_data.stock_actual - old_stock),
                saldo_anterior=old_stock,
                saldo_actual=product_data.stock_actual,
                costo_unitario=product.precio_compra,
                usuario_id=user_id
            )
        
        return product
    
    def delete_product(self, product_id: int) -> bool:
        """
        Delete product.
        
        Args:
            product_id: Product ID
            
        Returns:
            bool: True if deleted
            
        Raises:
            NotFoundError: If product not found
            BusinessLogicError: If product has associated records
        """
        product = self.get_product(product_id)
        if not product:
            raise NotFoundError("Product", product_id)
        
        # Check if product has associated records
        # (In a real implementation, you'd check for guia_items, etc.)
        
        self.db.delete(product)
        self.db.commit()
        return True
    
    def update_stock(
        self, 
        product_id: int, 
        cantidad: int, 
        tipo_movimiento: str,
        documento_asociado: str,
        usuario_id: str,
        observaciones: Optional[str] = None
    ) -> Product:
        """
        Update product stock and create kardex entry.
        
        Args:
            product_id: Product ID
            cantidad: Quantity to add/subtract
            tipo_movimiento: Type of movement
            documento_asociado: Associated document
            usuario_id: User ID
            observaciones: Observations
            
        Returns:
            Product: Updated product
            
        Raises:
            NotFoundError: If product not found
            BusinessLogicError: If insufficient stock
        """
        product = self.get_product(product_id)
        if not product:
            raise NotFoundError("Product", product_id)
        
        old_stock = product.stock_actual
        
        # Calculate new stock
        if tipo_movimiento == "entrada":
            new_stock = old_stock + cantidad
        elif tipo_movimiento == "salida":
            new_stock = old_stock - cantidad
            if new_stock < 0:
                raise BusinessLogicError(
                    f"Insufficient stock. Available: {old_stock}, Required: {cantidad}"
                )
        else:
            new_stock = cantidad
        
        # Update product stock
        product.stock_actual = new_stock
        self.db.commit()
        
        # Create kardex entry
        self._create_kardex_entry(
            product_id=product_id,
            tipo_movimiento=tipo_movimiento,
            documento_asociado=documento_asociado,
            cantidad=cantidad,
            saldo_anterior=old_stock,
            saldo_actual=new_stock,
            costo_unitario=product.precio_compra,
            usuario_id=usuario_id,
            observaciones=observaciones
        )
        
        self.db.refresh(product)
        return product
    
    def get_low_stock_products(self, threshold: Optional[int] = None) -> List[Product]:
        """
        Get products with low stock.
        
        Args:
            threshold: Stock threshold (uses product's stock_minimo if not provided)
            
        Returns:
            List[Product]: Products with low stock
        """
        query = self.db.query(Product).filter(Product.status == "active")
        
        if threshold:
            query = query.filter(Product.stock_actual <= threshold)
        else:
            query = query.filter(Product.stock_actual <= Product.stock_minimo)
        
        return query.all()
    
    def get_inventory_summary(self) -> Dict[str, Any]:
        """
        Get inventory summary statistics.
        
        Returns:
            Dict[str, Any]: Inventory summary
        """
        total_products = self.db.query(Product).count()
        active_products = self.db.query(Product).filter(Product.status == "active").count()
        
        low_stock_count = self.db.query(Product).filter(
            and_(
                Product.status == "active",
                Product.stock_actual <= Product.stock_minimo
            )
        ).count()
        
        out_of_stock_count = self.db.query(Product).filter(
            and_(
                Product.status == "active",
                Product.stock_actual == 0
            )
        ).count()
        
        # Calculate total value
        total_value = self.db.query(
            func.sum(Product.stock_actual * Product.precio_compra)
        ).filter(Product.status == "active").scalar() or Decimal('0')
        
        return {
            "total_products": total_products,
            "active_products": active_products,
            "low_stock_products": low_stock_count,
            "out_of_stock_products": out_of_stock_count,
            "total_value": total_value
        }
    
    # Category operations
    def create_category(self, category_data: CategoryCreate) -> Category:
        """
        Create a new category.
        
        Args:
            category_data: Category creation data
            
        Returns:
            Category: Created category
        """
        category = Category(**category_data.dict())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def get_categories(self, active_only: bool = True) -> List[Category]:
        """
        Get categories.
        
        Args:
            active_only: Whether to return only active categories
            
        Returns:
            List[Category]: List of categories
        """
        query = self.db.query(Category)
        if active_only:
            query = query.filter(Category.is_active == True)
        return query.order_by(Category.sort_order, Category.name).all()
    
    def get_category(self, category_id: int) -> Optional[Category]:
        """
        Get category by ID.
        
        Args:
            category_id: Category ID
            
        Returns:
            Optional[Category]: Category if found
        """
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def update_category(
        self, 
        category_id: int, 
        category_data: CategoryUpdate
    ) -> Optional[Category]:
        """
        Update category.
        
        Args:
            category_id: Category ID
            category_data: Category update data
            
        Returns:
            Optional[Category]: Updated category if found
        """
        category = self.get_category(category_id)
        if not category:
            return None
        
        update_data = category_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def delete_category(self, category_id: int) -> bool:
        """
        Delete category.
        
        Args:
            category_id: Category ID
            
        Returns:
            bool: True if deleted
        """
        category = self.get_category(category_id)
        if not category:
            return False
        
        # Check if category has products
        product_count = self.db.query(Product).filter(
            Product.category_id == category_id
        ).count()
        
        if product_count > 0:
            raise BusinessLogicError(
                f"Cannot delete category with {product_count} products"
            )
        
        self.db.delete(category)
        self.db.commit()
        return True
    
    # Private methods
    def _create_kardex_entry(
        self,
        product_id: int,
        tipo_movimiento: str,
        documento_asociado: str,
        cantidad: int,
        saldo_anterior: int,
        saldo_actual: int,
        costo_unitario: Optional[Decimal],
        usuario_id: str,
        observaciones: Optional[str] = None
    ) -> Kardex:
        """
        Create kardex entry.
        
        Args:
            product_id: Product ID
            tipo_movimiento: Movement type
            documento_asociado: Associated document
            cantidad: Quantity
            saldo_anterior: Previous balance
            saldo_actual: Current balance
            costo_unitario: Unit cost
            usuario_id: User ID
            observaciones: Observations
            
        Returns:
            Kardex: Created kardex entry
        """
        kardex = Kardex(
            product_id=product_id,
            tipo_movimiento=tipo_movimiento,
            documento_asociado=documento_asociado,
            cantidad=cantidad,
            saldo_anterior=saldo_anterior,
            saldo_actual=saldo_actual,
            costo_unitario=costo_unitario,
            valor_total=costo_unitario * cantidad if costo_unitario else None,
            usuario_id=usuario_id,
            observaciones=observaciones
        )
        
        self.db.add(kardex)
        self.db.commit()
        self.db.refresh(kardex)
        return kardex
