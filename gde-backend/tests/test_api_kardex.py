"""
Tests for kardex API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from decimal import Decimal


class TestKardexEndpoints:
    """Tests for /api/v1/kardex endpoints."""
    
    def test_create_kardex_entry(self, client: TestClient, admin_user_token: str, sample_product):
        """Test creating a kardex entry."""
        params = {
            "product_id": sample_product.id,
            "tipo_movimiento": "entrada",
            "cantidad": 20,
            "costo_unitario": 100.00,
            "documento_asociado": "PO-TEST-001",
            "observaciones": "Test purchase order"
        }
        
        response = client.post(
            "/api/v1/kardex/",
            params=params,
            headers={"Authorization": admin_user_token}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["tipo_movimiento"] == "entrada"
        assert data["cantidad"] == 20
    
    def test_get_product_kardex(self, client: TestClient, test_user_token: str, sample_product):
        """Test getting kardex entries for a product."""
        # Create a kardex entry first
        from app.services.kardex_service import KardexService
        from app.core.database import SessionLocal
        
        db = SessionLocal()
        try:
            service = KardexService(db)
            service.create_kardex_entry(
                product_id=sample_product.id,
                tipo_movimiento="entrada",
                cantidad=10
            )
            db.commit()
        finally:
            db.close()
        
        response = client.get(
            f"/api/v1/kardex/product/{sample_product.id}",
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_kardex_summary(self, client: TestClient, test_user_token: str):
        """Test getting kardex summary."""
        response = client.get(
            "/api/v1/kardex/summary",
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "total_movimientos" in data
    
    def test_adjust_stock(self, client: TestClient, admin_user_token: str, sample_product):
        """Test stock adjustment."""
        params = {
            "product_id": sample_product.id,
            "new_stock": 100,
            "observaciones": "Physical inventory count adjustment"
        }
        
        response = client.post(
            "/api/v1/kardex/adjust-stock",
            params=params,
            headers={"Authorization": admin_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["tipo_movimiento"] == "ajuste"
        assert data["saldo_actual"] == 100
    
    def test_transfer_stock(self, client: TestClient, admin_user_token: str, sample_product):
        """Test stock transfer."""
        params = {
            "product_id": sample_product.id,
            "cantidad": 10,
            "destino": "Bodega B",
            "observaciones": "Transfer to secondary warehouse"
        }
        
        response = client.post(
            "/api/v1/kardex/transfer-stock",
            params=params,
            headers={"Authorization": admin_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["tipo_movimiento"] == "transferencia"
    
    def test_product_movements_report(self, client: TestClient, test_user_token: str, sample_product):
        """Test getting product movements report."""
        response = client.get(
            f"/api/v1/kardex/product/{sample_product.id}/report",
            params={"days": 30},
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "product_id" in data
        assert "total_movements" in data
    
    def test_insufficient_stock_error(self, client: TestClient, admin_user_token: str, sample_product):
        """Test that trying to remove more stock than available returns error."""
        params = {
            "product_id": sample_product.id,
            "tipo_movimiento": "salida",
            "cantidad": sample_product.stock_actual + 1000  # More than available
        }
        
        response = client.post(
            "/api/v1/kardex/",
            params=params,
            headers={"Authorization": admin_user_token}
        )
        
        assert response.status_code == 400  # Business logic error
    
    def test_unauthorized_kardex_creation(self, client: TestClient, sample_product):
        """Test that unauthorized users cannot create kardex entries."""
        params = {
            "product_id": sample_product.id,
            "tipo_movimiento": "entrada",
            "cantidad": 10
        }
        
        response = client.post("/api/v1/kardex/", params=params)
        
        assert response.status_code == 401

