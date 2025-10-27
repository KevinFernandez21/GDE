# Testing Documentation - GDE Backend

## 📋 Overview

Comprehensive testing suite for the GDE Backend API, covering unit tests, integration tests, and end-to-end testing scenarios.

## 🎯 Test Coverage

### Completed Test Modules

✅ **Configuration and Setup**
- `tests/__init__.py` - Package initialization
- `tests/conftest.py` - Pytest fixtures and configuration
- `tests/pytest.ini` - Pytest settings
- `tests/utils.py` - Test utilities and helpers
- `requirements-test.txt` - Testing dependencies

✅ **Unit Tests**
- `tests/test_models.py` - Database model tests
  - Product model tests
  - Categoria model tests
  - Guia model tests
  - Costo model tests
  - Kardex model tests
  - User model tests
  - Notification model tests

- `tests/test_services.py` - Service layer tests
  - ProductService tests
  - KardexService tests
  - GuiaService tests
  - CostoService tests

✅ **Integration Tests (API Endpoints)**
- `tests/test_api_auth.py` - Authentication endpoints
- `tests/test_api_products.py` - Product and category endpoints
- `tests/test_api_kardex.py` - Inventory movement endpoints
- `tests/test_api_guias.py` - Delivery guide endpoints
- `tests/test_api_costos.py` - Cost tracking endpoints
- `tests/test_api_dashboard.py` - Dashboard statistics endpoints

## 🔧 Quick Start

### Install Test Dependencies

```bash
cd gde-backend
pip install -r requirements-test.txt
```

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

### View Coverage Report

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## 📊 Test Statistics

- **Total Test Files**: 11
- **Test Categories**:
  - Unit Tests: 2 files
  - Integration Tests: 6 files
  - Configuration: 3 files

## 🧪 Key Features

### Shared Fixtures
- `db_session` - Fresh database session for each test
- `client` - FastAPI test client with mocked dependencies
- `test_user_token` - Authentication token for regular user
- `admin_user_token` - Authentication token for admin user
- `sample_product` - Pre-created product for testing
- `sample_guia` - Pre-created guia with details

### Test Utilities
- `TestDataFactory` - Factory class for creating test data
- Data generation helpers
- Response validation helpers
- Custom JSON encoder for tests
- Authentication header builders

### Test Markers
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.{module}` - Module-specific tests

## 🚀 Running Specific Tests

```bash
# Run only model tests
pytest tests/test_models.py -v

# Run only service tests
pytest tests/test_services.py -v

# Run only API tests
pytest tests/test_api_*.py -v

# Run tests for specific module
pytest -m products -v

# Run with specific marker
pytest -m "unit and not slow" -v

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Run in parallel
pytest -n auto
```

## 📈 Coverage Goals

- **Overall Coverage**: 80%+
- **Critical Paths**: 100%
- **Services Layer**: 90%+
- **API Endpoints**: 85%+
- **Models**: 95%+

## 🔄 Continuous Integration

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Changes to backend code

CI workflow includes:
- ✅ Running full test suite
- ✅ Code coverage reporting
- ✅ Linting and code formatting checks
- ✅ Security vulnerability scanning
- ✅ Type checking with mypy

See `.github/workflows/backend-tests.yml` for details.

## 🛠️ Test Database

Tests use an in-memory SQLite database by default for:
- Fast execution
- Isolation between tests
- No external dependencies
- Automatic cleanup

Configuration in `conftest.py`:
```python
TEST_DATABASE_URL = "sqlite:///:memory:"
```

## 📝 Writing New Tests

### Example: Testing a New Endpoint

```python
# tests/test_api_myfeature.py

def test_create_item(client: TestClient, admin_user_token: str):
    """Test creating a new item."""
    # Arrange
    item_data = {
        "name": "Test Item",
        "value": 100
    }
    
    # Act
    response = client.post(
        "/api/v1/items/",
        json=item_data,
        headers={"Authorization": admin_user_token}
    )
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["value"] == 100
```

### Example: Testing a Service

```python
# tests/test_services.py

def test_item_service(db_session: Session):
    """Test item service logic."""
    from app.services.item_service import ItemService
    
    service = ItemService(db_session)
    item = service.create_item(name="Test", value=50)
    
    assert item.id is not None
    assert item.name == "Test"
```

## 🐛 Debugging

### Enable verbose output
```bash
pytest -vv
```

### Show print statements
```bash
pytest -s
```

### Drop into debugger on failure
```bash
pytest --pdb
```

### Show local variables on failure
```bash
pytest -l
```

### Run with logging
```bash
pytest --log-cli-level=DEBUG
```

## 📚 Test Documentation

Each test file includes:
- Module docstring explaining purpose
- Test class organization
- Individual test docstrings
- Clear arrange-act-assert structure
- Meaningful test names

Example:
```python
"""
Tests for product API endpoints.
"""

class TestProductsEndpoints:
    """Tests for /api/v1/products endpoints."""
    
    def test_list_products(self, client: TestClient, test_user_token: str):
        """Test listing products returns correct data."""
        # Test implementation
```

## 🔐 Security Testing

Security tests include:
- Authentication/authorization checks
- Input validation
- SQL injection prevention
- XSS prevention
- CSRF protection

Security scanning via:
- `bandit` - Security linter
- `safety` - Dependency vulnerability checks

## ⚡ Performance Testing

Performance considerations:
- Fast unit tests (< 1 second each)
- Parallel test execution support
- Database connection pooling
- Efficient fixtures

## 🎓 Best Practices

1. **Test Independence**: Each test should run independently
2. **Clear Naming**: Use descriptive test names
3. **AAA Pattern**: Arrange-Act-Assert structure
4. **DRY Principle**: Use fixtures and utilities
5. **Fast Tests**: Keep tests fast and focused
6. **Clean Code**: Follow PEP 8 and project standards
7. **Documentation**: Document complex scenarios
8. **Maintenance**: Update tests with code changes

## 📖 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Test README](tests/README.md) - Detailed testing guide

## 🤝 Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain coverage standards
4. Update documentation
5. Add appropriate test markers

## ✅ Pre-commit Checklist

Before committing:
- [ ] All tests pass: `pytest`
- [ ] Coverage is adequate: `pytest --cov=app`
- [ ] Linting passes: `flake8 app tests`
- [ ] Formatting is correct: `black --check app tests`
- [ ] Imports are sorted: `isort --check app tests`
- [ ] Types are correct: `mypy app`

## 🔄 Next Steps

Future enhancements:
- [ ] Add performance/load tests
- [ ] Add more edge case tests
- [ ] Increase coverage to 90%+
- [ ] Add E2E tests with real database
- [ ] Add API contract tests
- [ ] Add mutation testing
- [ ] Add property-based testing

---

**Last Updated**: October 2025  
**Test Suite Version**: 1.0.0

