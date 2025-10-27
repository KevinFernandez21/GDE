# GDE Backend API

Backend API para el sistema GDE - Gestión de Inventario y Despacho.

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.11+
- PostgreSQL (o Supabase)
- Git

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/your-username/GDE_UNPULSED.git
cd GDE_UNPULSED/gde-backend
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar la aplicación**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentación

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🏗️ Estructura del Proyecto

```
gde-backend/
├── app/
│   ├── api/              # Endpoints REST
│   │   ├── v1/          # Versión 1 de la API
│   │   │   ├── auth.py
│   │   │   ├── products.py
│   │   │   └── ...
│   │   └── dependencies.py
│   ├── core/            # Configuración
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── exceptions.py
│   ├── models/          # SQLAlchemy models
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── ...
│   ├── schemas/         # Pydantic schemas
│   │   ├── common.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── ...
│   ├── services/        # Lógica de negocio
│   │   ├── product_service.py
│   │   ├── file_service.py
│   │   └── ...
│   └── main.py         # Punto de entrada
├── tests/              # Tests
├── scripts/            # Scripts de utilidad
├── requirements.txt    # Dependencias
└── env.example         # Variables de entorno
```

## 🔧 Desarrollo

### Comandos Útiles

```bash
# Servidor de desarrollo
uvicorn app.main:app --reload

# Ejecutar tests
pytest

# Formatear código
black .

# Linting
flake8 .

# Verificación de tipos
mypy .
```

### Git y Versionado

El proyecto incluye archivos `.gitignore` completos que excluyen:

- **Archivos de Python**: `__pycache__/`, `*.pyc`, `*.pyo`, etc.
- **Entornos virtuales**: `venv/`, `.env`, etc.
- **Archivos de IDE**: `.vscode/`, `.idea/`, etc.
- **Archivos del sistema**: `.DS_Store`, `Thumbs.db`, etc.
- **Logs y archivos temporales**: `*.log`, `tmp/`, etc.
- **Archivos sensibles**: `*.pem`, `*.key`, `secrets/`, etc.
- **Base de datos**: `*.sqlite`, `*.db`, `backup_*.sql`
- **Docker**: `docker-compose.override.yml`

**Importante**: Nunca commites archivos `.env` o credenciales al repositorio.

### Variables de Entorno

Copia `env.example` a `.env` y configura las siguientes variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/gde_db
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
ENVIRONMENT=development
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con coverage
pytest --cov=app

# Ejecutar tests específicos
pytest tests/test_products.py
```

## 🚀 Despliegue

### Docker

```bash
# Construir imagen
docker build -t gde-backend .

# Ejecutar contenedor
docker run -p 8000:8000 gde-backend
```

### Railway/Render

1. Conecta tu repositorio
2. Configura las variables de entorno
3. Deploy automático

## 📊 API Endpoints

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/refresh` - Renovar token
- `POST /api/v1/auth/logout` - Cerrar sesión

### Productos
- `GET /api/v1/products/` - Listar productos
- `POST /api/v1/products/` - Crear producto
- `GET /api/v1/products/{id}` - Obtener producto
- `PUT /api/v1/products/{id}` - Actualizar producto
- `DELETE /api/v1/products/{id}` - Eliminar producto

### Categorías
- `GET /api/v1/products/categories/` - Listar categorías
- `POST /api/v1/products/categories/` - Crear categoría
- `GET /api/v1/products/categories/{id}` - Obtener categoría
- `PUT /api/v1/products/categories/{id}` - Actualizar categoría
- `DELETE /api/v1/products/categories/{id}` - Eliminar categoría

## 🔒 Seguridad

- **Autenticación**: JWT tokens
- **Autorización**: Role-based access control (RBAC)
- **Validación**: Pydantic schemas
- **CORS**: Configurado para frontend
- **Rate Limiting**: Implementado

## 📝 Logs

Los logs se configuran automáticamente según el nivel especificado en `LOG_LEVEL`.

## 🤝 Contribución

1. Fork del repositorio
2. Crear feature branch
3. Commit de cambios
4. Push a branch
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
