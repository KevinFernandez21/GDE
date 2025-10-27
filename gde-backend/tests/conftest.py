"""
Pytest configuration and shared fixtures.
"""
import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db, Base
from app.core.config import settings


# Test database URL (use in-memory SQLite for fast tests)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    """Create a test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine) -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with dependency overrides."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_token(client: TestClient, db_session: Session) -> str:
    """Create a test user and return authentication token."""
    from app.models.user import Profile
    from app.core.security import get_password_hash
    
    # Create test user
    test_user = Profile(
        id="test-user-id-123",
        email="test@example.com",
        nombre_completo="Test User",
        rol="contable",
        activo=True
    )
    db_session.add(test_user)
    db_session.commit()
    
    # Generate token (simplified for testing)
    from app.core.security import create_access_token
    token = create_access_token(data={"sub": test_user.id})
    
    return f"Bearer {token}"


@pytest.fixture
def admin_user_token(client: TestClient, db_session: Session) -> str:
    """Create an admin user and return authentication token."""
    from app.models.user import Profile
    
    # Create admin user
    admin_user = Profile(
        id="admin-user-id-123",
        email="admin@example.com",
        nombre_completo="Admin User",
        rol="admin",
        activo=True
    )
    db_session.add(admin_user)
    db_session.commit()
    
    # Generate token
    from app.core.security import create_access_token
    token = create_access_token(data={"sub": admin_user.id})
    
    return f"Bearer {token}"


@pytest.fixture
def sample_product(db_session: Session):
    """Create a sample product for testing."""
    from app.models.product import Product, Categoria
    
    # Create category first
    category = Categoria(
        nombre="Test Category",
        descripcion="Test category description",
        activo=True
    )
    db_session.add(category)
    db_session.flush()
    
    # Create product
    product = Product(
        code="TEST001",
        name="Test Product",
        descripcion="Test product description",
        categoria_id=category.id,
        precio_compra=100.00,
        precio_venta=150.00,
        stock_actual=50,
        stock_minimo=10,
        unidad_medida="unidad",
        activo=True
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    
    return product


@pytest.fixture
def sample_guia(db_session: Session, sample_product):
    """Create a sample guia for testing."""
    from app.models.guia import Guia, GuiaDetalle
    
    guia = Guia(
        numero_guia="GDE-TEST-001",
        fecha_emision="2025-10-25",
        destinatario_nombre="Test Client",
        destinatario_rut="12345678-9",
        destinatario_direccion="Test Address 123",
        destinatario_comuna="Test Comuna",
        destinatario_ciudad="Test City",
        transportista_nombre="Test Transporter",
        transportista_rut="98765432-1",
        estado="borrador"
    )
    db_session.add(guia)
    db_session.flush()
    
    # Add detail
    detalle = GuiaDetalle(
        guia_id=guia.id,
        product_id=sample_product.id,
        cantidad=10,
        precio_unitario=150.00
    )
    db_session.add(detalle)
    db_session.commit()
    db_session.refresh(guia)
    
    return guia


@pytest.fixture(autouse=True)
def reset_db(db_session: Session):
    """Reset database state before each test."""
    # This fixture runs automatically before each test
    # Add any cleanup logic here if needed
    yield
    # Cleanup after test
    db_session.rollback()

