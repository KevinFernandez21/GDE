"""
Test utilities and helper functions.
"""
from typing import Dict, Any
from datetime import datetime, date
from decimal import Decimal
import json


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for handling special types in tests."""
    
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


def assert_dict_contains(actual: Dict[str, Any], expected: Dict[str, Any]) -> None:
    """
    Assert that actual dict contains all keys and values from expected dict.
    
    Args:
        actual: Actual dictionary
        expected: Expected dictionary (subset)
    """
    for key, value in expected.items():
        assert key in actual, f"Key '{key}' not found in actual dict"
        assert actual[key] == value, f"Value mismatch for key '{key}': {actual[key]} != {value}"


def create_test_product_data(**overrides) -> Dict[str, Any]:
    """
    Create test product data with optional overrides.
    
    Args:
        **overrides: Key-value pairs to override default values
        
    Returns:
        Dict[str, Any]: Product data dictionary
    """
    default_data = {
        "code": "TEST001",
        "name": "Test Product",
        "descripcion": "Test product description",
        "precio_compra": 100.00,
        "precio_venta": 150.00,
        "stock_actual": 50,
        "stock_minimo": 10,
        "unidad_medida": "unidad",
        "activo": True
    }
    default_data.update(overrides)
    return default_data


def create_test_guia_data(product_id: int, **overrides) -> Dict[str, Any]:
    """
    Create test guia data with optional overrides.
    
    Args:
        product_id: Product ID for guia details
        **overrides: Key-value pairs to override default values
        
    Returns:
        Dict[str, Any]: Guia data dictionary
    """
    default_data = {
        "numero_guia": "GDE-TEST-001",
        "fecha_emision": datetime.utcnow().date().isoformat(),
        "destinatario_nombre": "Test Client",
        "destinatario_rut": "12345678-9",
        "destinatario_direccion": "Test Address 123",
        "destinatario_comuna": "Test Comuna",
        "destinatario_ciudad": "Test City",
        "transportista_nombre": "Test Transporter",
        "transportista_rut": "98765432-1",
        "estado": "borrador",
        "detalles": [
            {
                "product_id": product_id,
                "cantidad": 10,
                "precio_unitario": 150.00
            }
        ]
    }
    default_data.update(overrides)
    return default_data


def create_test_costo_data(**overrides) -> Dict[str, Any]:
    """
    Create test costo data with optional overrides.
    
    Args:
        **overrides: Key-value pairs to override default values
        
    Returns:
        Dict[str, Any]: Costo data dictionary
    """
    default_data = {
        "fecha": datetime.utcnow().date().isoformat(),
        "categoria": "combustible",
        "subcategoria": "diesel",
        "monto": 50000.00,
        "descripcion": "Test expense",
        "proveedor": "Test Provider",
        "documento": "TEST-DOC-001"
    }
    default_data.update(overrides)
    return default_data


def create_test_user_data(rol: str = "contable", **overrides) -> Dict[str, Any]:
    """
    Create test user data with optional overrides.
    
    Args:
        rol: User role (admin, contable, programador)
        **overrides: Key-value pairs to override default values
        
    Returns:
        Dict[str, Any]: User data dictionary
    """
    default_data = {
        "id": "test-user-uuid",
        "email": "test@example.com",
        "nombre_completo": "Test User",
        "rol": rol,
        "activo": True
    }
    default_data.update(overrides)
    return default_data


def clean_response_data(data: Any) -> Any:
    """
    Clean response data by removing None values and converting types.
    
    Args:
        data: Response data (dict, list, or primitive)
        
    Returns:
        Any: Cleaned data
    """
    if isinstance(data, dict):
        return {k: clean_response_data(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [clean_response_data(item) for item in data]
    elif isinstance(data, Decimal):
        return float(data)
    elif isinstance(data, (datetime, date)):
        return data.isoformat()
    return data


def assert_response_schema(response_data: Dict[str, Any], required_fields: list) -> None:
    """
    Assert that response data contains all required fields.
    
    Args:
        response_data: Response data dictionary
        required_fields: List of required field names
    """
    for field in required_fields:
        assert field in response_data, f"Required field '{field}' not found in response"


def get_pagination_params(page: int = 1, page_size: int = 10) -> Dict[str, int]:
    """
    Get pagination parameters for API requests.
    
    Args:
        page: Page number (1-indexed)
        page_size: Number of items per page
        
    Returns:
        Dict[str, int]: Pagination parameters
    """
    skip = (page - 1) * page_size
    return {
        "skip": skip,
        "limit": page_size
    }


def assert_date_format(date_string: str) -> None:
    """
    Assert that a string is in valid ISO date format.
    
    Args:
        date_string: Date string to validate
    """
    try:
        datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except (ValueError, AttributeError) as e:
        raise AssertionError(f"Invalid date format: {date_string}") from e


def assert_decimal_equal(actual: float, expected: float, places: int = 2) -> None:
    """
    Assert that two decimal/float values are equal within a tolerance.
    
    Args:
        actual: Actual value
        expected: Expected value
        places: Number of decimal places for comparison
    """
    actual_rounded = round(actual, places)
    expected_rounded = round(expected, places)
    assert actual_rounded == expected_rounded, \
        f"Decimal values not equal: {actual} != {expected} (rounded to {places} places)"


def create_auth_headers(token: str) -> Dict[str, str]:
    """
    Create authorization headers for API requests.
    
    Args:
        token: Authentication token (with or without 'Bearer ' prefix)
        
    Returns:
        Dict[str, str]: Headers dictionary
    """
    if not token.startswith("Bearer "):
        token = f"Bearer {token}"
    
    return {
        "Authorization": token,
        "Content-Type": "application/json"
    }


def mock_supabase_user(user_id: str, email: str, rol: str = "contable") -> Dict[str, Any]:
    """
    Create mock Supabase user data for testing.
    
    Args:
        user_id: User UUID
        email: User email
        rol: User role
        
    Returns:
        Dict[str, Any]: Mock user data
    """
    return {
        "id": user_id,
        "email": email,
        "user_metadata": {
            "rol": rol,
            "nombre_completo": f"Test User {email}"
        },
        "app_metadata": {},
        "aud": "authenticated",
        "created_at": datetime.utcnow().isoformat()
    }


class TestDataFactory:
    """Factory class for creating test data."""
    
    @staticmethod
    def create_category(db_session, **kwargs):
        """Create a test category."""
        from app.models.product import Categoria
        
        default_data = {
            "nombre": "Test Category",
            "descripcion": "Test category description",
            "activo": True
        }
        default_data.update(kwargs)
        
        category = Categoria(**default_data)
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)
        
        return category
    
    @staticmethod
    def create_product(db_session, categoria_id: int, **kwargs):
        """Create a test product."""
        from app.models.product import Product
        
        default_data = {
            "code": f"TEST{datetime.utcnow().timestamp()}",
            "name": "Test Product",
            "categoria_id": categoria_id,
            "precio_compra": Decimal("100.00"),
            "precio_venta": Decimal("150.00"),
            "stock_actual": 50,
            "stock_minimo": 10,
            "unidad_medida": "unidad",
            "activo": True
        }
        default_data.update(kwargs)
        
        product = Product(**default_data)
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        return product
    
    @staticmethod
    def create_kardex(db_session, product_id: int, **kwargs):
        """Create a test kardex entry."""
        from app.models.product import Kardex
        
        default_data = {
            "product_id": product_id,
            "tipo_movimiento": "entrada",
            "cantidad": 10,
            "saldo_anterior": 50,
            "saldo_actual": 60,
            "costo_unitario": Decimal("100.00"),
            "costo_promedio": Decimal("100.00"),
            "valor_total": Decimal("1000.00")
        }
        default_data.update(kwargs)
        
        kardex = Kardex(**default_data)
        db_session.add(kardex)
        db_session.commit()
        db_session.refresh(kardex)
        
        return kardex
    
    @staticmethod
    def create_guia(db_session, **kwargs):
        """Create a test guia."""
        from app.models.guia import Guia
        
        default_data = {
            "numero_guia": f"GDE-{datetime.utcnow().timestamp()}",
            "fecha_emision": datetime.utcnow().date(),
            "destinatario_nombre": "Test Client",
            "destinatario_rut": "12345678-9",
            "destinatario_direccion": "Test Address",
            "destinatario_comuna": "Test Comuna",
            "destinatario_ciudad": "Test City",
            "transportista_nombre": "Test Transporter",
            "transportista_rut": "98765432-1",
            "estado": "borrador"
        }
        default_data.update(kwargs)
        
        guia = Guia(**default_data)
        db_session.add(guia)
        db_session.commit()
        db_session.refresh(guia)
        
        return guia
    
    @staticmethod
    def create_costo(db_session, **kwargs):
        """Create a test costo entry."""
        from app.models.costo import Costo
        
        default_data = {
            "fecha": datetime.utcnow().date(),
            "categoria": "combustible",
            "monto": Decimal("50000.00"),
            "descripcion": "Test expense"
        }
        default_data.update(kwargs)
        
        costo = Costo(**default_data)
        db_session.add(costo)
        db_session.commit()
        db_session.refresh(costo)
        
        return costo

