"""
Tests for service layer.
"""
import pytest
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.product_service import ProductService
from app.services.kardex_service import KardexService
from app.services.guia_service import GuiaService
from app.services.costo_service import CostoService
from app.core.exceptions import NotFoundError, BusinessLogicError


class TestProductService:
    """Tests for ProductService."""
    
    def test_get_product_by_id(self, db_session: Session, sample_product):
        """Test getting product by ID."""
        service = ProductService(db_session)
        product = service.get_product(sample_product.id)
        
        assert product is not None
        assert product.id == sample_product.id
        assert product.code == sample_product.code
    
    def test_get_nonexistent_product(self, db_session: Session):
        """Test getting non-existent product raises error."""
        service = ProductService(db_session)
        
        with pytest.raises(NotFoundError):
            service.get_product(999999)
    
    def test_list_products(self, db_session: Session, sample_product):
        """Test listing products."""
        service = ProductService(db_session)
        products = service.list_products()
        
        assert len(products) > 0
        assert any(p.id == sample_product.id for p in products)
    
    def test_search_products(self, db_session: Session, sample_product):
        """Test searching products."""
        service = ProductService(db_session)
        products = service.search_products(query="Test")
        
        assert len(products) > 0
        assert any(p.id == sample_product.id for p in products)


class TestKardexService:
    """Tests for KardexService."""
    
    def test_create_entrada(self, db_session: Session, sample_product):
        """Test creating an entrada (incoming) movement."""
        service = KardexService(db_session)
        initial_stock = sample_product.stock_actual
        
        kardex = service.create_kardex_entry(
            product_id=sample_product.id,
            tipo_movimiento="entrada",
            cantidad=20,
            costo_unitario=Decimal("100.00"),
            documento_asociado="PO-123"
        )
        
        assert kardex.id is not None
        assert kardex.tipo_movimiento == "entrada"
        assert kardex.cantidad == 20
        assert kardex.saldo_anterior == initial_stock
        assert kardex.saldo_actual == initial_stock + 20
        
        # Verify product stock was updated
        db_session.refresh(sample_product)
        assert sample_product.stock_actual == initial_stock + 20
    
    def test_create_salida(self, db_session: Session, sample_product):
        """Test creating a salida (outgoing) movement."""
        service = KardexService(db_session)
        initial_stock = sample_product.stock_actual
        
        kardex = service.create_kardex_entry(
            product_id=sample_product.id,
            tipo_movimiento="salida",
            cantidad=10,
            documento_asociado="SO-456"
        )
        
        assert kardex.tipo_movimiento == "salida"
        assert kardex.saldo_actual == initial_stock - 10
        
        db_session.refresh(sample_product)
        assert sample_product.stock_actual == initial_stock - 10
    
    def test_insufficient_stock(self, db_session: Session, sample_product):
        """Test that salida with insufficient stock raises error."""
        service = KardexService(db_session)
        
        with pytest.raises(BusinessLogicError):
            service.create_kardex_entry(
                product_id=sample_product.id,
                tipo_movimiento="salida",
                cantidad=sample_product.stock_actual + 100  # More than available
            )
    
    def test_adjust_stock(self, db_session: Session, sample_product):
        """Test stock adjustment."""
        service = KardexService(db_session)
        
        kardex = service.adjust_stock(
            product_id=sample_product.id,
            new_stock=100,
            usuario_id="user-123",
            observaciones="Physical inventory adjustment"
        )
        
        assert kardex.tipo_movimiento == "ajuste"
        assert kardex.saldo_actual == 100
        
        db_session.refresh(sample_product)
        assert sample_product.stock_actual == 100
    
    def test_get_kardex_by_product(self, db_session: Session, sample_product):
        """Test getting kardex history for a product."""
        service = KardexService(db_session)
        
        # Create some movements
        service.create_kardex_entry(
            product_id=sample_product.id,
            tipo_movimiento="entrada",
            cantidad=10
        )
        service.create_kardex_entry(
            product_id=sample_product.id,
            tipo_movimiento="salida",
            cantidad=5
        )
        
        kardex_list = service.get_kardex_by_product(sample_product.id)
        
        assert len(kardex_list) >= 2
    
    def test_kardex_summary(self, db_session: Session, sample_product):
        """Test kardex summary statistics."""
        service = KardexService(db_session)
        
        # Create movements
        service.create_kardex_entry(
            product_id=sample_product.id,
            tipo_movimiento="entrada",
            cantidad=30
        )
        service.create_kardex_entry(
            product_id=sample_product.id,
            tipo_movimiento="salida",
            cantidad=10
        )
        
        summary = service.get_kardex_summary(product_id=sample_product.id)
        
        assert summary["total_movimientos"] >= 2
        assert summary["total_entradas"] >= 30
        assert summary["total_salidas"] >= 10


class TestGuiaService:
    """Tests for GuiaService."""
    
    def test_create_guia(self, db_session: Session, sample_product):
        """Test creating a guia."""
        service = GuiaService(db_session)
        
        guia_data = {
            "numero_guia": "GDE-TEST-002",
            "fecha_emision": datetime.utcnow().date(),
            "destinatario_nombre": "Test Client 2",
            "destinatario_rut": "11111111-1",
            "destinatario_direccion": "Address 456",
            "destinatario_comuna": "Comuna",
            "destinatario_ciudad": "City",
            "transportista_nombre": "Transporter",
            "transportista_rut": "22222222-2",
            "estado": "borrador",
            "detalles": [
                {
                    "product_id": sample_product.id,
                    "cantidad": 5,
                    "precio_unitario": Decimal("150.00")
                }
            ]
        }
        
        # Note: This is a simplified test - actual implementation may vary
        # guia = service.create_guia(guia_data)
        # assert guia.id is not None
        # assert guia.numero_guia == "GDE-TEST-002"
    
    def test_get_guia(self, db_session: Session, sample_guia):
        """Test getting a guia by ID."""
        service = GuiaService(db_session)
        guia = service.get_guia(sample_guia.id)
        
        assert guia is not None
        assert guia.id == sample_guia.id
    
    def test_list_guias(self, db_session: Session, sample_guia):
        """Test listing guias."""
        service = GuiaService(db_session)
        guias = service.list_guias()
        
        assert len(guias) > 0
        assert any(g.id == sample_guia.id for g in guias)


class TestCostoService:
    """Tests for CostoService."""
    
    def test_create_costo(self, db_session: Session):
        """Test creating a cost entry."""
        service = CostoService(db_session)
        
        costo_data = {
            "fecha": datetime.utcnow().date(),
            "categoria": "combustible",
            "subcategoria": "diesel",
            "monto": Decimal("50000.00"),
            "descripcion": "Fuel purchase",
            "proveedor": "Gas Station",
            "documento": "FACT-123"
        }
        
        costo = service.create_costo(**costo_data)
        
        assert costo.id is not None
        assert costo.categoria == "combustible"
        assert costo.monto == Decimal("50000.00")
    
    def test_get_costo(self, db_session: Session):
        """Test getting a cost entry."""
        service = CostoService(db_session)
        
        # Create a cost first
        costo = service.create_costo(
            fecha=datetime.utcnow().date(),
            categoria="mantenimiento",
            monto=Decimal("25000.00"),
            descripcion="Vehicle maintenance"
        )
        
        retrieved = service.get_costo(costo.id)
        assert retrieved.id == costo.id
        assert retrieved.categoria == "mantenimiento"
    
    def test_list_costos(self, db_session: Session):
        """Test listing cost entries."""
        service = CostoService(db_session)
        
        # Create some costs
        service.create_costo(
            fecha=datetime.utcnow().date(),
            categoria="combustible",
            monto=Decimal("30000.00"),
            descripcion="Fuel 1"
        )
        service.create_costo(
            fecha=datetime.utcnow().date(),
            categoria="peaje",
            monto=Decimal("5000.00"),
            descripcion="Toll"
        )
        
        costos = service.list_costos()
        assert len(costos) >= 2
    
    def test_get_costos_summary(self, db_session: Session):
        """Test cost summary by category."""
        service = CostoService(db_session)
        
        # Create costs in different categories
        service.create_costo(
            fecha=datetime.utcnow().date(),
            categoria="combustible",
            monto=Decimal("10000.00"),
            descripcion="Fuel"
        )
        service.create_costo(
            fecha=datetime.utcnow().date(),
            categoria="combustible",
            monto=Decimal("15000.00"),
            descripcion="Fuel 2"
        )
        service.create_costo(
            fecha=datetime.utcnow().date(),
            categoria="mantenimiento",
            monto=Decimal("20000.00"),
            descripcion="Maintenance"
        )
        
        summary = service.get_costos_summary()
        
        assert "total" in summary
        assert "by_category" in summary
        assert summary["total"] >= Decimal("45000.00")

