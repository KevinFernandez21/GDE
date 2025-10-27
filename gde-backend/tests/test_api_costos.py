"""
Tests for costos API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal


class TestCostosEndpoints:
    """Tests for /api/v1/costos endpoints."""
    
    def test_list_costos(self, client: TestClient, test_user_token: str):
        """Test listing costos."""
        response = client.get(
            "/api/v1/costos/",
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_costo(self, client: TestClient, admin_user_token: str):
        """Test creating a costo."""
        costo_data = {
            "fecha": datetime.utcnow().date().isoformat(),
            "categoria": "combustible",
            "subcategoria": "diesel",
            "monto": 50000.00,
            "descripcion": "Fuel for delivery truck",
            "proveedor": "Gas Station XYZ",
            "documento": "FACT-12345"
        }
        
        response = client.post(
            "/api/v1/costos/",
            json=costo_data,
            headers={"Authorization": admin_user_token}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["categoria"] == "combustible"
        assert float(data["monto"]) == 50000.00
    
    def test_get_costo(self, client: TestClient, test_user_token: str, db_session: Session):
        """Test getting a single costo."""
        from app.models.costo import Costo
        
        # Create a costo first
        costo = Costo(
            fecha=datetime.utcnow().date(),
            categoria="peaje",
            monto=Decimal("5000.00"),
            descripcion="Highway toll"
        )
        db_session.add(costo)
        db_session.commit()
        
        response = client.get(
            f"/api/v1/costos/{costo.id}",
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == costo.id
    
    def test_update_costo(self, client: TestClient, admin_user_token: str, db_session: Session):
        """Test updating a costo."""
        from app.models.costo import Costo
        
        # Create a costo first
        costo = Costo(
            fecha=datetime.utcnow().date(),
            categoria="mantenimiento",
            monto=Decimal("25000.00"),
            descripcion="Vehicle maintenance"
        )
        db_session.add(costo)
        db_session.commit()
        
        update_data = {
            "monto": 30000.00,
            "descripcion": "Updated vehicle maintenance"
        }
        
        response = client.put(
            f"/api/v1/costos/{costo.id}",
            json=update_data,
            headers={"Authorization": admin_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert float(data["monto"]) == 30000.00
    
    def test_delete_costo(self, client: TestClient, admin_user_token: str, db_session: Session):
        """Test deleting a costo."""
        from app.models.costo import Costo
        
        # Create a costo first
        costo = Costo(
            fecha=datetime.utcnow().date(),
            categoria="otro",
            monto=Decimal("10000.00"),
            descripcion="Miscellaneous expense"
        )
        db_session.add(costo)
        db_session.commit()
        
        response = client.delete(
            f"/api/v1/costos/{costo.id}",
            headers={"Authorization": admin_user_token}
        )
        
        assert response.status_code == 200
    
    def test_get_costos_summary(self, client: TestClient, test_user_token: str, db_session: Session):
        """Test getting costos summary."""
        from app.models.costo import Costo
        
        # Create some costos
        costos = [
            Costo(fecha=datetime.utcnow().date(), categoria="combustible", 
                  monto=Decimal("20000.00"), descripcion="Fuel"),
            Costo(fecha=datetime.utcnow().date(), categoria="peaje", 
                  monto=Decimal("5000.00"), descripcion="Toll"),
        ]
        db_session.add_all(costos)
        db_session.commit()
        
        response = client.get(
            "/api/v1/costos/summary",
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "by_category" in data
    
    def test_filter_costos_by_categoria(self, client: TestClient, test_user_token: str):
        """Test filtering costos by categoria."""
        response = client.get(
            "/api/v1/costos/",
            params={"categoria": "combustible"},
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_filter_costos_by_date_range(self, client: TestClient, test_user_token: str):
        """Test filtering costos by date range."""
        fecha_desde = (datetime.utcnow().date()).isoformat()
        fecha_hasta = (datetime.utcnow().date()).isoformat()
        
        response = client.get(
            "/api/v1/costos/",
            params={
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta
            },
            headers={"Authorization": test_user_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

