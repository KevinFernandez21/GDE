"""
Tests for dashboard API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestDashboardEndpoints:
    """Tests for /api/v1/dashboard endpoints."""
    
    def test_get_dashboard_stats(self, client: TestClient, test_user_token: str, 
                                  sample_product, sample_guia, db_session: Session):
        """Test getting dashboard statistics."""
        response = client.get(
            "/api/v1/dashboard/stats",
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check that expected fields are present
        assert "total_products" in data or "productos" in data
        assert "total_guias" in data or "guias" in data
    
    def test_get_recent_activity(self, client: TestClient, test_user_token: str):
        """Test getting recent activity."""
        response = client.get(
            "/api/v1/dashboard/recent-activity",
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_low_stock_alerts(self, client: TestClient, test_user_token: str, db_session: Session):
        """Test getting low stock alerts."""
        from app.models.product import Product, Categoria
        
        # Create a product with low stock
        category = Categoria(
            nombre="Test Cat",
            descripcion="Test",
            activo=True
        )
        db_session.add(category)
        db_session.flush()
        
        low_stock_product = Product(
            code="LOW001",
            name="Low Stock Product",
            categoria_id=category.id,
            precio_compra=100.00,
            precio_venta=150.00,
            stock_actual=3,  # Below minimum
            stock_minimo=10,
            unidad_medida="unidad",
            activo=True
        )
        db_session.add(low_stock_product)
        db_session.commit()
        
        response = client.get(
            "/api/v1/dashboard/low-stock",
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Should include our low stock product
        assert any(p["code"] == "LOW001" for p in data)
    
    def test_get_sales_summary(self, client: TestClient, test_user_token: str):
        """Test getting sales summary."""
        response = client.get(
            "/api/v1/dashboard/sales-summary",
            params={"days": 30},
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        # Structure may vary based on implementation
        assert isinstance(data, (dict, list))
    
    def test_get_costos_summary(self, client: TestClient, test_user_token: str):
        """Test getting costs summary."""
        response = client.get(
            "/api/v1/dashboard/costos-summary",
            params={"days": 30},
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
    
    def test_unauthorized_dashboard_access(self, client: TestClient):
        """Test accessing dashboard without authentication."""
        response = client.get("/api/v1/dashboard/stats")
        
        assert response.status_code == 401

