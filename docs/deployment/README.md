# Despliegue GDE - Guía Completa

## 📋 Resumen General

Esta guía cubre el despliegue completo del sistema GDE, incluyendo frontend, backend y base de datos. El sistema está diseñado para ser desplegado en múltiples plataformas con alta disponibilidad y escalabilidad.

## 🏗️ Arquitectura de Despliegue

### Componentes del Sistema
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Base de       │
│   (Next.js)     │    │   (FastAPI)     │    │   Datos         │
│                 │    │                 │    │   (Supabase)    │
│   Vercel        │◄──►│   Railway/      │◄──►│   PostgreSQL    │
│   Hosting       │    │   Render        │    │   + Auth        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Flujo de Datos
1. **Frontend** → **Supabase** (operaciones simples)
2. **Frontend** → **Backend** → **Supabase** (procesamiento complejo)
3. **Backend** → **Servicios Externos** (notificaciones, archivos)

## 🚀 Plataformas de Despliegue

### Frontend - Vercel (Recomendado)
- **Ventajas**: Deploy automático, CDN global, optimizaciones automáticas
- **Configuración**: Conectado a GitHub para CI/CD
- **Dominio**: `gde-frontend.vercel.app`

### Backend - Railway/Render
- **Railway**: Deploy automático, escalado automático, logs integrados
- **Render**: Alternativa robusta con buena documentación
- **Dominio**: `gde-backend.railway.app`

### Base de Datos - Supabase
- **Ventajas**: PostgreSQL gestionado, autenticación integrada, RLS
- **Configuración**: Proyecto dedicado con backups automáticos
- **Dominio**: `gde-database.supabase.co`

## 📋 Checklist de Despliegue

### Pre-requisitos
- [ ] Cuenta de GitHub
- [ ] Cuenta de Vercel
- [ ] Cuenta de Railway/Render
- [ ] Cuenta de Supabase
- [ ] Dominio personalizado (opcional)

### Configuración Inicial
- [ ] Crear repositorio en GitHub
- [ ] Configurar variables de entorno
- [ ] Configurar base de datos
- [ ] Configurar autenticación
- [ ] Configurar dominios

## 🔧 Configuración de Variables de Entorno

### Frontend (Next.js)
```env
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=https://gde-backend.railway.app
NEXT_PUBLIC_APP_URL=https://gde-frontend.vercel.app
```

### Backend (FastAPI)
```env
# .env
DATABASE_URL=postgresql://user:password@host:port/database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External Services
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email
SMTP_PASSWORD=your-password

# File Storage
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760

# Notifications
FCM_SERVER_KEY=your-fcm-key
WEBHOOK_URL=your-webhook-url
```

## 🗄️ Configuración de Base de Datos

### 1. Crear Proyecto en Supabase
```bash
# Instalar Supabase CLI
npm install -g supabase

# Inicializar proyecto
supabase init

# Conectar a proyecto remoto
supabase link --project-ref your-project-ref
```

### 2. Ejecutar Migraciones
```bash
# Aplicar migraciones
supabase db push

# Ejecutar scripts de datos iniciales
supabase db reset
```

### 3. Configurar RLS
```sql
-- Habilitar RLS en todas las tablas
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
-- ... resto de tablas

-- Crear políticas de seguridad
CREATE POLICY "Users can view all profiles" ON profiles FOR SELECT USING (true);
-- ... resto de políticas
```

### 4. Configurar Storage
```sql
-- Crear bucket para archivos
INSERT INTO storage.buckets (id, name, public) VALUES ('uploads', 'uploads', true);

-- Configurar políticas de storage
CREATE POLICY "Users can upload files" ON storage.objects FOR INSERT WITH CHECK (auth.role() = 'authenticated');
```

## 🖥️ Despliegue del Frontend

### 1. Configurar Vercel
```bash
# Instalar Vercel CLI
npm install -g vercel

# Login en Vercel
vercel login

# Deploy inicial
vercel

# Configurar variables de entorno
vercel env add NEXT_PUBLIC_SUPABASE_URL
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY
vercel env add NEXT_PUBLIC_API_URL
```

### 2. Configurar GitHub Actions
```yaml
# .github/workflows/deploy-frontend.yml
name: Deploy Frontend

on:
  push:
    branches: [main]
    paths: ['gde-frontend/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd gde-frontend
          npm ci
      - name: Build
        run: |
          cd gde-frontend
          npm run build
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: gde-frontend
```

### 3. Configurar Dominio Personalizado
```bash
# En Vercel Dashboard
# 1. Ir a Project Settings
# 2. Agregar dominio personalizado
# 3. Configurar DNS records
```

## 🐍 Despliegue del Backend

### 1. Configurar Railway
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login en Railway
railway login

# Inicializar proyecto
railway init

# Deploy
railway up
```

### 2. Configurar Variables de Entorno
```bash
# En Railway Dashboard o CLI
railway variables set DATABASE_URL=postgresql://...
railway variables set SECRET_KEY=your-secret-key
railway variables set SUPABASE_URL=https://...
```

### 3. Configurar Docker
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Configurar GitHub Actions
```yaml
# .github/workflows/deploy-backend.yml
name: Deploy Backend

on:
  push:
    branches: [main]
    paths: ['gde-backend/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd gde-backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd gde-backend
          pytest
      - name: Deploy to Railway
        uses: railway-app/railway-deploy@v1
        with:
          railway-token: ${{ secrets.RAILWAY_TOKEN }}
          service: gde-backend
```

## 🔒 Configuración de Seguridad

### 1. SSL/TLS
- **Vercel**: SSL automático
- **Railway**: SSL automático
- **Supabase**: SSL automático

### 2. CORS
```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://gde-frontend.vercel.app",
        "http://localhost:3000"  # Solo para desarrollo
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Rate Limiting
```python
# app/middleware/rate_limit.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/v1/products")
@limiter.limit("100/minute")
async def get_products(request: Request):
    # Endpoint con rate limiting
    pass
```

## 📊 Monitoreo y Logs

### 1. Logs de Aplicación
```python
# app/core/logging.py
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)
```

### 2. Health Checks
```python
# app/api/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@router.get("/health/db")
async def database_health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
```

### 3. Métricas
```python
# app/middleware/metrics.py
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(duration)
    
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## 🔄 CI/CD Pipeline

### 1. Pipeline Completo
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install Frontend Dependencies
        run: |
          cd gde-frontend
          npm ci
      
      - name: Install Backend Dependencies
        run: |
          cd gde-backend
          pip install -r requirements.txt
      
      - name: Run Frontend Tests
        run: |
          cd gde-frontend
          npm run test
      
      - name: Run Backend Tests
        run: |
          cd gde-backend
          pytest
      
      - name: Run Linting
        run: |
          cd gde-frontend && npm run lint
          cd gde-backend && black . && flake8 .
  
  deploy-staging:
    if: github.ref == 'refs/heads/develop'
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Staging
        run: |
          echo "Deploying to staging environment"
  
  deploy-production:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Production
        run: |
          echo "Deploying to production environment"
```

## 🚨 Backup y Recuperación

### 1. Backup de Base de Datos
```bash
# Script de backup automático
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="gde_backup_$DATE.sql"

# Crear backup
pg_dump $DATABASE_URL > $BACKUP_FILE

# Subir a storage
aws s3 cp $BACKUP_FILE s3://gde-backups/database/

# Limpiar backups antiguos (mantener últimos 30 días)
aws s3 ls s3://gde-backups/database/ | awk '$1 < "'$(date -d '30 days ago' +%Y-%m-%d)'" {print $4}' | xargs -I {} aws s3 rm s3://gde-backups/database/{}
```

### 2. Backup de Archivos
```bash
# Backup de archivos de usuario
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)

# Sincronizar con S3
aws s3 sync /app/uploads s3://gde-backups/files/ --delete
```

### 3. Recuperación de Desastres
```bash
# Script de recuperación
#!/bin/bash

# Restaurar base de datos
psql $DATABASE_URL < backup_file.sql

# Restaurar archivos
aws s3 sync s3://gde-backups/files/ /app/uploads

# Reiniciar servicios
railway restart
```

## 📈 Escalabilidad

### 1. Escalado Horizontal
```yaml
# railway.toml
[build]
builder = "dockerfile"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "always"

[deploy.scaling]
minInstances = 1
maxInstances = 10
targetCPU = 70
targetMemory = 80
```

### 2. Cache
```python
# app/core/cache.py
from redis import Redis
import json

redis_client = Redis(host='redis-host', port=6379, db=0)

def cache_key(prefix: str, *args) -> str:
    return f"{prefix}:{':'.join(str(arg) for arg in args)}"

def get_cached_data(key: str):
    data = redis_client.get(key)
    return json.loads(data) if data else None

def set_cached_data(key: str, data: dict, ttl: int = 3600):
    redis_client.setex(key, ttl, json.dumps(data))
```

### 3. Load Balancing
```nginx
# nginx.conf
upstream backend {
    server backend1.railway.app;
    server backend2.railway.app;
    server backend3.railway.app;
}

server {
    listen 80;
    server_name api.gde-system.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔧 Mantenimiento

### 1. Actualizaciones
```bash
# Script de actualización
#!/bin/bash

# Actualizar frontend
cd gde-frontend
npm update
npm run build
vercel --prod

# Actualizar backend
cd gde-backend
pip install -r requirements.txt --upgrade
railway up

# Actualizar base de datos
supabase db push
```

### 2. Monitoreo de Performance
```python
# app/middleware/performance.py
import time
from fastapi import Request

@app.middleware("http")
async def performance_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    if duration > 1.0:  # Log requests slower than 1 second
        logger.warning(f"Slow request: {request.url.path} took {duration:.2f}s")
    
    return response
```

### 3. Limpieza de Logs
```bash
# Script de limpieza
#!/bin/bash

# Limpiar logs antiguos
find /app/logs -name "*.log" -mtime +30 -delete

# Limpiar archivos temporales
find /app/temp -type f -mtime +7 -delete

# Limpiar cache
redis-cli FLUSHDB
```

## 📚 Próximos Pasos

1. Configurar repositorio en GitHub
2. Configurar Supabase
3. Desplegar backend en Railway
4. Desplegar frontend en Vercel
5. Configurar dominios personalizados
6. Configurar monitoreo
7. Configurar backups
8. Configurar CI/CD
9. Pruebas de carga
10. Documentación de operaciones





