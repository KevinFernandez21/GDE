# GDE Backend Tests

Comprehensive test suite for the GDE Backend API.

## 📁 Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Pytest configuration and fixtures
├── pytest.ini               # Pytest settings
├── utils.py                 # Test utilities and helpers
├── README.md                # This file
│
├── test_models.py           # Database model tests
├── test_services.py         # Service layer tests
│
├── test_api_auth.py         # Authentication endpoint tests
├── test_api_products.py     # Product endpoint tests
├── test_api_kardex.py       # Kardex endpoint tests
├── test_api_guias.py        # Guia endpoint tests
├── test_api_costos.py       # Costo endpoint tests
└── test_api_dashboard.py    # Dashboard endpoint tests
```

## 🚀 Running Tests

### Run All Tests

```bash
# From the gde-backend directory
pytest

# With verbose output
pytest -v

# With coverage
pytest --cov=app --cov-report=html
```

### Run Specific Test Files

```bash
# Run only model tests
pytest tests/test_models.py

# Run only API tests
pytest tests/test_api_*.py

# Run specific test class
pytest tests/test_models.py::TestProductModel

# Run specific test function
pytest tests/test_models.py::TestProductModel::test_create_product
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only product-related tests
pytest -m products

# Run all except slow tests
pytest -m "not slow"
```

### Run with Different Output Options

```bash
# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Show local variables on failure
pytest -l

# Run in parallel (requires pytest-xdist)
pytest -n auto
```

## 🧪 Test Categories

### Unit Tests

Test individual components in isolation:
- **Model tests** (`test_models.py`): Database model creation, relationships, validation
- **Service tests** (`test_services.py`): Business logic, data processing

Run with: `pytest -m unit`

### Integration Tests

Test API endpoints and component interactions:
- **Authentication tests** (`test_api_auth.py`): Login, logout, token management
- **Product tests** (`test_api_products.py`): CRUD operations for products and categories
- **Kardex tests** (`test_api_kardex.py`): Inventory movements, stock management
- **Guia tests** (`test_api_guias.py`): Delivery guide operations
- **Costo tests** (`test_api_costos.py`): Cost tracking and reporting
- **Dashboard tests** (`test_api_dashboard.py`): Dashboard statistics and summaries

Run with: `pytest -m integration`

## 🛠️ Test Fixtures

Common fixtures are defined in `conftest.py`:

### Database Fixtures
- `engine`: Test database engine (SQLite in-memory)
- `db_session`: Fresh database session for each test
- `client`: FastAPI test client with dependency overrides

### Authentication Fixtures
- `test_user_token`: JWT token for a regular user (contable role)
- `admin_user_token`: JWT token for an admin user

### Data Fixtures
- `sample_product`: A pre-created product for testing
- `sample_guia`: A pre-created guia with details
- `reset_db`: Automatic database cleanup after each test

## 📝 Writing Tests

### Basic Test Structure

```python
def test_something(client: TestClient, test_user_token: str):
    """Test description."""
    # Arrange
    data = {"field": "value"}
    
    # Act
    response = client.post(
        "/api/v1/endpoint",
        json=data,
        headers={"Authorization": test_user_token}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["field"] == "value"
```

### Using Test Utilities

```python
from tests.utils import (
    create_test_product_data,
    assert_dict_contains,
    TestDataFactory
)

def test_with_utilities(db_session: Session):
    # Create test data easily
    product_data = create_test_product_data(name="Custom Name")
    
    # Use factory for complex objects
    category = TestDataFactory.create_category(db_session)
    product = TestDataFactory.create_product(
        db_session, 
        categoria_id=category.id
    )
    
    # Assert partial matches
    assert_dict_contains(
        actual=product.__dict__,
        expected={"name": "Test Product"}
    )
```

### Marking Tests

```python
import pytest

@pytest.mark.unit
@pytest.mark.products
def test_product_model():
    """Unit test for product model."""
    pass

@pytest.mark.integration
@pytest.mark.slow
def test_complex_workflow():
    """Slow integration test."""
    pass
```

## 🔧 Test Configuration

### Environment Variables

Tests use an in-memory SQLite database by default. To use a different database:

```bash
# Set test database URL
export TEST_DATABASE_URL="postgresql://user:pass@localhost/test_db"
pytest
```

### Pytest Options

Configure in `pytest.ini`:
- Test discovery patterns
- Output formatting
- Markers
- Coverage options
- Warning filters

## 📊 Coverage

Generate coverage reports:

```bash
# Run tests with coverage
pytest --cov=app

# Generate HTML report
pytest --cov=app --cov-report=html

# Open HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

Coverage goals:
- **Unit tests**: 80%+ coverage
- **Integration tests**: Cover all main workflows
- **Critical paths**: 100% coverage

## 🐛 Debugging Tests

### Using pytest debugger

```bash
# Drop into debugger on failure
pytest --pdb

# Drop into debugger at start of test
pytest --trace
```

### Print debugging

```bash
# Show print statements
pytest -s

# Capture only on failure
pytest --capture=no
```

### Logging

```bash
# Show log output
pytest --log-cli-level=DEBUG
```

## 🚨 Common Issues

### Import Errors

If you get import errors, make sure you're in the correct directory:

```bash
cd gde-backend
pytest
```

### Database Errors

If tests fail with database errors:
1. Check that models are properly imported in conftest.py
2. Verify Base.metadata includes all models
3. Check for circular imports

### Fixture Errors

If fixtures aren't working:
1. Make sure conftest.py is in the tests directory
2. Check fixture scopes (function, session, module)
3. Verify fixture dependencies

## 📚 Best Practices

1. **Isolation**: Each test should be independent
2. **Clarity**: Use descriptive test names and docstrings
3. **Arrange-Act-Assert**: Follow the AAA pattern
4. **DRY**: Use fixtures and utilities to avoid repetition
5. **Fast**: Keep unit tests fast (< 1 second each)
6. **Deterministic**: Tests should always produce the same result
7. **Clean**: Clean up after tests (fixtures handle this)
8. **Coverage**: Aim for high coverage but don't sacrifice quality
9. **Documentation**: Document complex test scenarios
10. **Maintenance**: Update tests when code changes

## 🔄 Continuous Integration

Tests run automatically in CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=app --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## 📖 Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html)

## 🤝 Contributing

When adding new features:
1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain or improve coverage
4. Update test documentation
5. Add appropriate markers

## 📞 Support

For questions about testing:
- Check this README
- Review existing tests for examples
- Consult pytest documentation
- Ask the team

---

**Last Updated**: October 2025

