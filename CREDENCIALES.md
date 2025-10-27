# 🔐 Credenciales de Supabase - GDE System

## 📊 Base de Datos
- **Host**: `aws-1-us-east-1.pooler.supabase.com`
- **Puerto**: `6543`
- **Usuario**: `postgres.bkiddfhxebqtlsxvfztq`
- **Contraseña**: `2121`
- **Base de datos**: `postgres`

## 🌐 Supabase
- **URL**: `https://bkiddfhxebqtlsxvfztq.supabase.co`
- **Anon Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJraWRkZmh4ZWJxdGxzeHZmenRxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjExOTE2NDUsImV4cCI6MjA3Njc2NzY0NX0.hOqIxmYXCXzz2C9tAuNQqs7KYEqm40odO0Juzkcd3nY`

## 🔧 Configuración para Frontend

### Archivo `.env.local` (gde-frontend)
```bash
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://bkiddfhxebqtlsxvfztq.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJraWRkZmh4ZWJxdGxzeHZmenRxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjExOTE2NDUsImV4cCI6MjA3Njc2NzY0NX0.hOqIxmYXCXzz2C9tAuNQqs7KYEqm40odO0Juzkcd3nY

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1

# Application Settings
NEXT_PUBLIC_APP_NAME=GDE System
NEXT_PUBLIC_APP_VERSION=1.0.0
NEXT_PUBLIC_ENVIRONMENT=development
```

## 🚀 URLs del Sistema

### Backend API
- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health
- **Documentación**: http://localhost:8000/docs
- **Products API**: http://localhost:8000/api/v1/products/
- **Auth API**: http://localhost:8000/api/v1/auth/

### Supabase Dashboard
- **Dashboard**: https://supabase.com/dashboard/project/bkiddfhxebqtlsxvfztq
- **SQL Editor**: https://supabase.com/dashboard/project/bkiddfhxebqtlsxvfztq/sql
- **Table Editor**: https://supabase.com/dashboard/project/bkiddfhxebqtlsxvfztq/editor

## 📋 Estado del Sistema

### ✅ Backend
- [x] FastAPI ejecutándose en puerto 8000
- [x] Base de datos conectada
- [x] 15 tablas creadas
- [x] Autenticación JWT funcionando
- [x] Endpoints protegidos

### ✅ Base de Datos
- [x] PostgreSQL 17.6 conectado
- [x] Todas las tablas creadas
- [x] Índices y relaciones configurados
- [x] RLS (Row Level Security) preparado

### 🔄 Frontend
- [ ] Next.js por configurar
- [ ] Supabase client por instalar
- [ ] Autenticación por implementar
- [ ] Componentes por crear

## 🛠️ Comandos Útiles

### Backend
```bash
# Ejecutar servidor
cd gde-backend
uv run uvicorn app.main:app --reload

# Con Docker
make dev

# Health check
curl http://localhost:8000/health
```

### Frontend (próximos pasos)
```bash
# Instalar dependencias
cd gde-frontend
npm install

# Configurar variables de entorno
cp .env.example .env.local

# Ejecutar servidor de desarrollo
npm run dev
```

## 🔒 Seguridad

- ✅ Variables de entorno configuradas
- ✅ Credenciales protegidas en `.env`
- ✅ Autenticación JWT implementada
- ✅ CORS configurado
- ✅ Rate limiting preparado

---

**Última actualización**: 2025-10-23
**Estado**: Backend completamente funcional, Frontend pendiente
