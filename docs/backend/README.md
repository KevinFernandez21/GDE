# Backend GDE - FastAPI

## 📋 Resumen General

El backend de GDE está construido con FastAPI y Python, diseñado para manejar procesamiento complejo, cálculos contables, procesamiento de archivos y operaciones que requieren mayor potencia de cómputo. Se conecta a la base de datos PostgreSQL a través de Supabase.

## 🏗️ Arquitectura

### Stack Tecnológico
- **Framework**: FastAPI
- **Lenguaje**: Python 3.11+
- **ORM**: SQLAlchemy 2.0 + asyncpg
- **Base de Datos**: PostgreSQL (Supabase)
- **Validación**: Pydantic v2
- **Archivos**: python-multipart
- **Procesamiento**: pandas + openpyxl (CSV/Excel)
- **Imágenes**: opencv-python + pyzbar
- **Notificaciones**: pywebpush
- **Autenticación**: python-jose + bcrypt

## 📁 Estructura de Carpetas

```
gde-backend/
├── app/
│   ├── api/              # Endpoints REST
│   │   ├── v1/          # Versión 1 de la API
│   │   │   ├── auth.py
│   │   │   ├── products.py
│   │   │   ├── guias.py
│   │   │   ├── pistoleo.py
│   │   │   ├── costos.py
│   │   │   ├── reports.py
│   │   │   └── files.py
│   │   └── dependencies.py
│   ├── models/          # SQLAlchemy models
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── guia.py
│   │   ├── pistoleo.py
│   │   ├── costo.py
│   │   └── audit.py
│   ├── schemas/         # Pydantic schemas
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── guia.py
│   │   ├── pistoleo.py
│   │   ├── costo.py
│   │   └── common.py
│   ├── services/        # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── product_service.py
│   │   ├── guia_service.py
│   │   ├── pistoleo_service.py
│   │   ├── costo_service.py
│   │   ├── report_service.py
│   │   ├── file_service.py
│   │   └── notification_service.py
│   ├── core/           # Configuración
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── exceptions.py
│   └── main.py         # Punto de entrada
├── tests/              # Tests
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/            # Scripts de utilidad
│   ├── init_db.py
│   ├── seed_data.py
│   └── backup.py
├── requirements.txt    # Dependencias
├── Dockerfile         # Container
└── .env.example       # Variables de entorno
```

## 🎯 Funcionalidades Principales

### 1. Procesamiento de Archivos
- Importación de Excel/CSV
- Validación de datos
- Procesamiento por lotes
- Logs de importación

### 2. Cálculos Contables
- Promedios ponderados
- Cálculos de costos
- Reportes financieros
- Análisis de rentabilidad

### 3. Procesamiento de Imágenes
- Detección de códigos QR/barras
- Procesamiento con OpenCV
- Optimización de imágenes
- Extracción de metadatos

### 4. Generación de Reportes
- Reportes financieros
- Análisis de inventario
- Reportes de guías
- Exportación a PDF/Excel

### 5. Notificaciones
- Push notifications
- Email notifications
- Alertas de stock
- Notificaciones de sistema

### 6. Tareas Programadas
- Alertas de stock bajo
- Limpieza de logs
- Backups automáticos
- Sincronización de datos

## 🔄 Flujos de Comunicación

### Backend → Supabase
- Operaciones complejas de BD
- Transacciones
- Procedimientos almacenados
- Agregaciones pesadas

### Backend → Frontend
- Respuestas de API
- Archivos procesados
- Reportes generados
- Notificaciones

### Backend → Servicios Externos
- APIs de terceros
- Servicios de notificación
- Servicios de almacenamiento
- Integraciones contables

## 🛠️ Configuración

### Variables de Entorno
```env
# Database
DATABASE_URL=postgresql://user:password@host:port/database
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Security
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External Services
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email
SMTP_PASSWORD=your_password

# File Storage
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB

# Notifications
FCM_SERVER_KEY=your_fcm_key
WEBHOOK_URL=your_webhook_url
```

### Configuración de Base de Datos
```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 🚀 Desarrollo

### Comandos Principales
```bash
# Instalación
pip install -r requirements.txt

# Desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Tests
pytest

# Linting
black .
flake8 .

# Type checking
mypy .
```

### Scripts Disponibles
- `uvicorn app.main:app --reload`: Servidor de desarrollo
- `pytest`: Ejecutar tests
- `black .`: Formatear código
- `flake8 .`: Linting
- `mypy .`: Verificación de tipos

## 📊 Modelos de Datos

### Base Model
```python
# app/models/base.py
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Product Model
```python
# app/models/product.py
from sqlalchemy import Column, String, Integer, Decimal, Text, JSON
from .base import BaseModel

class Product(BaseModel):
    __tablename__ = "products"
    
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"))
    stock_actual = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=10)
    stock_maximo = Column(Integer)
    precio_compra = Column(Decimal(10, 2), default=0)
    precio_venta = Column(Decimal(10, 2), default=0)
    ubicacion_bodega = Column(String(100))
    proveedor = Column(String(100))
    codigo_barras = Column(String(100))
    imagenes = Column(JSON)
    metadata = Column(JSON)
```

## 🔧 Servicios

### Product Service
```python
# app/services/product_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_product(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.dict())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def get_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()
    
    def get_product(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def update_product(self, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        product = self.get_product(product_id)
        if product:
            for field, value in product_data.dict(exclude_unset=True).items():
                setattr(product, field, value)
            self.db.commit()
            self.db.refresh(product)
        return product
    
    def delete_product(self, product_id: int) -> bool:
        product = self.get_product(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False
```

### File Service
```python
# app/services/file_service.py
import pandas as pd
from typing import List, Dict, Any
from app.models.import_log import ImportLog

class FileService:
    def __init__(self, db: Session):
        self.db = db
    
    def process_excel_file(self, file_path: str, entity_type: str) -> Dict[str, Any]:
        try:
            # Leer archivo Excel
            df = pd.read_excel(file_path)
            
            # Validar datos
            validated_data = self._validate_data(df, entity_type)
            
            # Procesar datos
            processed_data = self._process_data(validated_data, entity_type)
            
            # Crear log de importación
            import_log = ImportLog(
                archivo=file_path,
                tipo_archivo='excel',
                entidad=entity_type,
                registros_totales=len(df),
                registros_exitosos=len(processed_data['success']),
                registros_fallidos=len(processed_data['errors']),
                errores=processed_data['errors']
            )
            self.db.add(import_log)
            self.db.commit()
            
            return processed_data
            
        except Exception as e:
            raise Exception(f"Error procesando archivo: {str(e)}")
    
    def _validate_data(self, df: pd.DataFrame, entity_type: str) -> pd.DataFrame:
        # Validaciones específicas por tipo de entidad
        if entity_type == 'products':
            required_columns = ['code', 'name', 'stock_actual']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Columnas faltantes: {missing_columns}")
        
        return df
    
    def _process_data(self, df: pd.DataFrame, entity_type: str) -> Dict[str, Any]:
        success = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Procesar cada fila según el tipo de entidad
                if entity_type == 'products':
                    processed_row = self._process_product_row(row)
                    success.append(processed_row)
                else:
                    raise ValueError(f"Tipo de entidad no soportado: {entity_type}")
                    
            except Exception as e:
                errors.append({
                    'row': index + 1,
                    'error': str(e),
                    'data': row.to_dict()
                })
        
        return {
            'success': success,
            'errors': errors
        }
```

## 🔒 Autenticación y Seguridad

### JWT Authentication
```python
# app/core/security.py
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Dependency Injection
```python
# app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.models.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(credentials.credentials)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user
```

## 📊 Endpoints de la API

### Products API
```python
# app/api/v1/products.py
from fastapi import APIRouter, Depends, HTTPException
from app.services.product_service import ProductService
from app.schemas.product import Product, ProductCreate, ProductUpdate

router = APIRouter()

@router.get("/", response_model=List[Product])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = ProductService(db)
    return service.get_products(skip=skip, limit=limit)

@router.post("/", response_model=Product)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ProductService(db)
    return service.create_product(product)

@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    service = ProductService(db)
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ProductService(db)
    updated_product = service.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ProductService(db)
    success = service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
```

## 🧪 Testing

### Unit Tests
```python
# tests/unit/test_product_service.py
import pytest
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate

def test_create_product():
    # Arrange
    product_data = ProductCreate(
        code="TEST001",
        name="Test Product",
        stock_actual=100
    )
    
    # Act
    service = ProductService(db)
    product = service.create_product(product_data)
    
    # Assert
    assert product.code == "TEST001"
    assert product.name == "Test Product"
    assert product.stock_actual == 100
```

### Integration Tests
```python
# tests/integration/test_products_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_product():
    response = client.post(
        "/api/v1/products/",
        json={
            "code": "TEST001",
            "name": "Test Product",
            "stock_actual": 100
        }
    )
    assert response.status_code == 200
    assert response.json()["code"] == "TEST001"
```

## 🚀 Despliegue

### Docker
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Railway/Render
- Deploy automático desde Git
- Variables de entorno
- Health checks
- Logs automáticos

## 📚 Próximos Pasos

1. Configurar proyecto FastAPI
2. Instalar dependencias
3. Configurar base de datos
4. Implementar modelos
5. Crear servicios
6. Implementar endpoints
7. Configurar autenticación
8. Testing y optimización





