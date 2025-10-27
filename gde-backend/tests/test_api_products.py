"""
Tests for products API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from decimal import Decimal


class TestProductsEndpoints:
    """Tests for /api/v1/products endpoints."""
    
    def test_list_products(self, client: TestClient, test_user_token: str, sample_product):
        """Test listing products."""
        response = client.get(
            "/api/v1/products/",
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_product(self, client: TestClient, test_user_token: str, sample_product):
        """Test getting a single product."""
        response = client.get(
            f"/api/v1/products/{sample_product.id}",
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_product.id
        assert data["code"] == sample_product.code
        assert data["name"] == sample_product.name
    
    def test_get_product_not_found(self, client: TestClient, test_user_token: str):
        """Test getting non-existent product."""
        response = client.get(
            "/api/v1/products/999999",
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 404
    
    def test_create_product(self, client: TestClient, admin_user_token: str, db_session: Session):
        """Test creating a product."""
        from app.models.product import Categoria
        
        # Create a category first
        category = Categoria(
            nombre="New Category",
            descripcion="Test category",
            activo=True
        )
        db_session.add(category)
        db_session.commit()
        
        product_data = {
            "code": "NEW001",
            "name": "New Product",
            "descripcion": "A new test product",
            "categoria_id": category.id,
            "precio_compra": 50.00,
            "precio_venta": 75.00,
            "stock_actual": 20,
            "stock_minimo": 5,
            "unidad_medida": "unidad",
            "activo": True
        }
        
        response = client.post(
            "/api/v1/products/",
            json=product_data,
            headers={"Authorization": admin_user_token}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == "NEW001"
        assert data["name"] == "New Product"
    
    def test_update_product(self, client: TestClient, admin_user_token: str, sample_product):
        """Test updating a product."""
        update_data = {
            "name": "Updated Product Name",
            "precio_venta": 200.00
        }
        
        response = client.put(
            f"/api/v1/products/{sample_product.id}",
            json=update_data,
            headers={"Authorization": admin_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Product Name"
    
    def test_delete_product(self, client: TestClient, admin_user_token: str, sample_product):
        """Test deleting (deactivating) a product."""
        response = client.delete(
            f"/api/v1/products/{sample_product.id}",
            headers={"Authorization": admin_user_token}
        )
        
        assert response.status_code == 200
    
    def test_search_products(self, client: TestClient, test_user_token: str, sample_product):
        """Test searching products."""
        response = client.get(
            "/api/v1/products/search",
            params={"query": "Test"},
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_unauthorized_access(self, client: TestClient, sample_product):
        """Test accessing products without authentication."""
        response = client.get("/api/v1/products/")
        
        assert response.status_code == 401


class TestCategoriesEndpoints:
    """Tests for /api/v1/products/categories endpoints."""
    
    def test_list_categories(self, client: TestClient, test_user_token: str, sample_product):
        """Test listing categories."""
        response = client.get(
            "/api/v1/products/categories/",
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_category(self, client: TestClient, admin_user_token: str):
        """Test creating a category."""
        category_data = {
            "nombre": "Electronics",
            "descripcion": "Electronic products and accessories",
            "activo": True
        }
        
        response = client.post(
            "/api/v1/products/categories/",
            json=category_data,
            headers={"Authorization": admin_user_token}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Electronics"
    
    def test_get_category(self, client: TestClient, test_user_token: str, sample_product):
        """Test getting a single category."""
        categoria_id = sample_product.categoria_id
        
        response = client.get(
            f"/api/v1/products/categories/{categoria_id}",
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == categoria_id

