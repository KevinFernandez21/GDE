"""
Tests for database models.
"""
import pytest
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.product import Product, Categoria, Kardex
from app.models.guia import Guia, GuiaDetalle
from app.models.costo import Costo
from app.models.user import Profile
from app.models.notification import Notification


class TestProductModel:
    """Tests for Product model."""
    
    def test_create_product(self, db_session: Session):
        """Test creating a product."""
        category = Categoria(
            nombre="Electronics",
            descripcion="Electronic products",
            activo=True
        )
        db_session.add(category)
        db_session.flush()
        
        product = Product(
            code="ELEC001",
            name="Laptop",
            descripcion="Gaming laptop",
            categoria_id=category.id,
            precio_compra=Decimal("800.00"),
            precio_venta=Decimal("1200.00"),
            stock_actual=10,
            stock_minimo=5,
            unidad_medida="unidad",
            activo=True
        )
        db_session.add(product)
        db_session.commit()
        
        assert product.id is not None
        assert product.code == "ELEC001"
        assert product.name == "Laptop"
        assert product.precio_compra == Decimal("800.00")
        assert product.stock_actual == 10
    
    def test_product_relationships(self, db_session: Session, sample_product):
        """Test product relationships."""
        # Add a kardex entry
        kardex = Kardex(
            product_id=sample_product.id,
            tipo_movimiento="entrada",
            cantidad=20,
            saldo_anterior=sample_product.stock_actual,
            saldo_actual=sample_product.stock_actual + 20,
            costo_unitario=Decimal("100.00"),
            costo_promedio=Decimal("100.00"),
            valor_total=Decimal("2000.00")
        )
        db_session.add(kardex)
        db_session.commit()
        
        db_session.refresh(sample_product)
        assert len(sample_product.kardex) == 1
        assert sample_product.kardex[0].tipo_movimiento == "entrada"
    
    def test_categoria_relationship(self, db_session: Session):
        """Test categoria to products relationship."""
        category = Categoria(
            nombre="Tools",
            descripcion="Hardware tools",
            activo=True
        )
        db_session.add(category)
        db_session.flush()
        
        product1 = Product(
            code="TOOL001",
            name="Hammer",
            categoria_id=category.id,
            precio_compra=Decimal("15.00"),
            precio_venta=Decimal("25.00"),
            stock_actual=100,
            stock_minimo=20,
            unidad_medida="unidad",
            activo=True
        )
        product2 = Product(
            code="TOOL002",
            name="Screwdriver",
            categoria_id=category.id,
            precio_compra=Decimal("8.00"),
            precio_venta=Decimal("15.00"),
            stock_actual=150,
            stock_minimo=30,
            unidad_medida="unidad",
            activo=True
        )
        db_session.add_all([product1, product2])
        db_session.commit()
        
        db_session.refresh(category)
        assert len(category.productos) == 2


class TestGuiaModel:
    """Tests for Guia model."""
    
    def test_create_guia(self, db_session: Session):
        """Test creating a guia."""
        guia = Guia(
            numero_guia="GDE-2025-001",
            fecha_emision=datetime.utcnow().date(),
            destinatario_nombre="John Doe",
            destinatario_rut="12345678-9",
            destinatario_direccion="Main St 123",
            destinatario_comuna="Santiago",
            destinatario_ciudad="Santiago",
            transportista_nombre="Fast Delivery",
            transportista_rut="98765432-1",
            estado="borrador"
        )
        db_session.add(guia)
        db_session.commit()
        
        assert guia.id is not None
        assert guia.numero_guia == "GDE-2025-001"
        assert guia.estado == "borrador"
    
    def test_guia_with_details(self, db_session: Session, sample_product):
        """Test guia with details."""
        guia = Guia(
            numero_guia="GDE-2025-002",
            fecha_emision=datetime.utcnow().date(),
            destinatario_nombre="Jane Smith",
            destinatario_rut="11111111-1",
            destinatario_direccion="Second St 456",
            destinatario_comuna="Valparaiso",
            destinatario_ciudad="Valparaiso",
            transportista_nombre="Express Transport",
            transportista_rut="22222222-2",
            estado="emitida"
        )
        db_session.add(guia)
        db_session.flush()
        
        detalle = GuiaDetalle(
            guia_id=guia.id,
            product_id=sample_product.id,
            cantidad=5,
            precio_unitario=Decimal("150.00")
        )
        db_session.add(detalle)
        db_session.commit()
        
        db_session.refresh(guia)
        assert len(guia.detalles) == 1
        assert guia.detalles[0].cantidad == 5
        assert guia.detalles[0].subtotal == Decimal("750.00")


class TestCostoModel:
    """Tests for Costo model."""
    
    def test_create_costo(self, db_session: Session):
        """Test creating a cost entry."""
        costo = Costo(
            fecha=datetime.utcnow().date(),
            categoria="combustible",
            subcategoria="diesel",
            monto=Decimal("50000.00"),
            descripcion="Fuel for truck",
            proveedor="Gas Station XYZ",
            documento="FACTURA-123"
        )
        db_session.add(costo)
        db_session.commit()
        
        assert costo.id is not None
        assert costo.categoria == "combustible"
        assert costo.monto == Decimal("50000.00")


class TestKardexModel:
    """Tests for Kardex model."""
    
    def test_create_kardex_entry(self, db_session: Session, sample_product):
        """Test creating a kardex entry."""
        kardex = Kardex(
            product_id=sample_product.id,
            tipo_movimiento="entrada",
            cantidad=30,
            saldo_anterior=sample_product.stock_actual,
            saldo_actual=sample_product.stock_actual + 30,
            costo_unitario=Decimal("100.00"),
            costo_promedio=Decimal("100.00"),
            valor_total=Decimal("3000.00"),
            documento_asociado="PO-123",
            referencia="Purchase order"
        )
        db_session.add(kardex)
        db_session.commit()
        
        assert kardex.id is not None
        assert kardex.tipo_movimiento == "entrada"
        assert kardex.cantidad == 30
        assert kardex.valor_total == Decimal("3000.00")


class TestUserModel:
    """Tests for User/Profile model."""
    
    def test_create_user(self, db_session: Session):
        """Test creating a user profile."""
        user = Profile(
            id="user-uuid-123",
            email="newuser@example.com",
            nombre_completo="New User",
            rol="contable",
            activo=True
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id == "user-uuid-123"
        assert user.email == "newuser@example.com"
        assert user.rol == "contable"
        assert user.activo is True


class TestNotificationModel:
    """Tests for Notification model."""
    
    def test_create_notification(self, db_session: Session):
        """Test creating a notification."""
        notification = Notification(
            usuario_id="user-123",
            tipo="stock_bajo",
            titulo="Low Stock Alert",
            mensaje="Product XYZ is running low on stock",
            datos_adicionales={"product_id": 1, "current_stock": 5},
            leida=False
        )
        db_session.add(notification)
        db_session.commit()
        
        assert notification.id is not None
        assert notification.tipo == "stock_bajo"
        assert notification.leida is False
        assert notification.datos_adicionales["product_id"] == 1

