# GDE - Sistema de Gestión de Inventario y Despacho

## 📋 Resumen General

GDE es un sistema completo de gestión de inventario, guías de despacho, pistoleo en tiempo real y contabilidad. Diseñado con una arquitectura moderna que combina la potencia de Supabase para operaciones simples y FastAPI para procesamiento complejo.

## 🏗️ Arquitectura del Sistema

### Stack Tecnológico
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python 3.11+
- **Base de Datos**: PostgreSQL (Supabase)
- **Autenticación**: Supabase Auth
- **Hosting**: Vercel (Frontend) + Railway/Render (Backend)

### Flujo de Comunicación
```
Frontend (Next.js) ←→ Supabase (Directo) ←→ PostgreSQL
     ↓
Backend (FastAPI) ←→ Supabase ←→ PostgreSQL
     ↓
Servicios Externos (Notificaciones, Archivos)
```

## 🎯 Funcionalidades Principales

### 1. Gestión de Inventario
- ✅ CRUD de productos con categorías jerárquicas
- ✅ Control de stock con alertas automáticas
- ✅ Historial de movimientos (Kardex)
- ✅ Códigos de barras y QR
- ✅ Ubicaciones en bodega

### 2. Guías de Despacho
- ✅ Creación y gestión de guías
- ✅ Seguimiento en tiempo real
- ✅ Estados y transiciones
- ✅ Evidencias fotográficas
- ✅ Integración con transportistas

### 3. Pistoleo en Tiempo Real
- ✅ Escaneo de códigos QR/barras
- ✅ Sesiones de trabajo
- ✅ Validación en tiempo real
- ✅ Geolocalización GPS
- ✅ Sincronización automática

### 4. Contabilidad
- ✅ Registro de costos y gastos
- ✅ Categorías contables
- ✅ Reportes financieros
- ✅ Evidencias documentales
- ✅ Análisis de rentabilidad

### 5. Notificaciones
- ✅ Push notifications
- ✅ Email notifications
- ✅ Alertas de stock
- ✅ Notificaciones de sistema

## 📁 Estructura del Proyecto

```
GDE_UNPULSED/
├── gde-frontend/           # Frontend Next.js
│   ├── app/               # App Router
│   ├── components/        # Componentes UI
│   ├── lib/              # Configuración y utils
│   ├── types/            # Tipos TypeScript
│   └── hooks/            # Custom hooks
├── gde-backend/           # Backend FastAPI
│   ├── app/              # Aplicación principal
│   │   ├── api/          # Endpoints REST
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Lógica de negocio
│   │   └── core/         # Configuración
│   ├── tests/            # Tests
│   └── scripts/          # Scripts de utilidad
├── docs/                 # Documentación
│   ├── database/         # Documentación de BD
│   ├── frontend/         # Documentación Frontend
│   ├── backend/          # Documentación Backend
│   ├── api/              # Documentación API
│   └── deployment/       # Guías de despliegue
├── base_datos.md         # Scripts SQL
└── contrato.md           # Especificaciones técnicas
```

## 🚀 Inicio Rápido

### Prerrequisitos
- Node.js 18+
- Python 3.11+
- PostgreSQL (o Supabase)
- Git

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/your-username/GDE_UNPULSED.git
cd GDE_UNPULSED
```

2. **Configurar Frontend**
```bash
cd gde-frontend
npm install
cp .env.example .env.local
# Configurar variables de entorno
npm run dev
```

3. **Configurar Backend**
```bash
cd gde-backend
pip install -r requirements.txt
cp .env.example .env
# Configurar variables de entorno
uvicorn app.main:app --reload
```

4. **Configurar Base de Datos**
```bash
# Ejecutar scripts SQL en Supabase
# Ver docs/database/README.md para más detalles
```

## 📚 Documentación

### Base de Datos
- [README](docs/database/README.md) - Resumen general
- [Entidades](docs/database/entities.md) - Descripción de tablas
- [Seguridad](docs/database/security.md) - RLS y permisos

### Frontend
- [README](docs/frontend/README.md) - Arquitectura y configuración
- [Componentes](docs/frontend/components.md) - Guía de componentes

### Backend
- [README](docs/backend/README.md) - Arquitectura y configuración

### API
- [README](docs/api/README.md) - Documentación completa de endpoints

### Despliegue
- [README](docs/deployment/README.md) - Guía completa de despliegue

## 🔧 Desarrollo

### Comandos Útiles

**Frontend:**
```bash
npm run dev          # Servidor de desarrollo
npm run build        # Build de producción
npm run test         # Ejecutar tests
npm run lint         # Linting
```

**Backend:**
```bash
uvicorn app.main:app --reload    # Servidor de desarrollo
pytest                           # Ejecutar tests
black .                          # Formatear código
flake8 .                         # Linting
```

### Estructura de Commits
```
feat: nueva funcionalidad
fix: corrección de bug
docs: documentación
style: formato de código
refactor: refactorización
test: tests
chore: tareas de mantenimiento
```

## 🧪 Testing

### Frontend
- **Unit Tests**: Jest + React Testing Library
- **E2E Tests**: Playwright
- **Coverage**: Mínimo 80%

### Backend
- **Unit Tests**: pytest
- **Integration Tests**: pytest + FastAPI TestClient
- **Coverage**: Mínimo 80%

## 🚀 Despliegue

### Ambientes
- **Development**: Local
- **Staging**: Railway + Vercel (preview)
- **Production**: Railway + Vercel (production)

### CI/CD
- **GitHub Actions**: Automatización completa
- **Deploy automático**: Push a main/develop
- **Tests automáticos**: En cada PR

## 🔒 Seguridad

### Autenticación
- **Supabase Auth**: JWT tokens
- **Roles**: admin, contable, programador
- **Permisos**: RLS en base de datos

### Validación
- **Frontend**: Zod schemas
- **Backend**: Pydantic models
- **Sanitización**: Automática

### Rate Limiting
- **API**: 1000 requests/hora
- **Burst**: 100 requests/minuto

## 📊 Monitoreo

### Métricas
- **Performance**: Response times
- **Errors**: Error rates
- **Usage**: Request counts
- **Health**: System status

### Logs
- **Application**: Structured logging
- **Access**: Request logs
- **Errors**: Error tracking
- **Audit**: User actions

## 🤝 Contribución

### Proceso
1. Fork del repositorio
2. Crear feature branch
3. Commit de cambios
4. Push a branch
5. Crear Pull Request

### Estándares
- **Código**: ESLint + Prettier (Frontend), Black + Flake8 (Backend)
- **Commits**: Conventional Commits
- **Tests**: Cobertura mínima 80%
- **Documentación**: Actualizar docs

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 👥 Equipo

- **Desarrollador Principal**: [Tu Nombre]
- **Diseñador UI/UX**: [Nombre]
- **DevOps**: [Nombre]

## 📞 Soporte

- **Email**: support@gde-system.com
- **Documentación**: [docs.gde-system.com](https://docs.gde-system.com)
- **Issues**: [GitHub Issues](https://github.com/your-username/GDE_UNPULSED/issues)

## 🗺️ Roadmap

### v1.0 (Actual)
- ✅ Gestión básica de inventario
- ✅ Guías de despacho
- ✅ Pistoleo básico
- ✅ Contabilidad básica

### v1.1 (Próximo)
- 🔄 Integración con APIs externas
- 🔄 Reportes avanzados
- 🔄 Notificaciones push
- 🔄 PWA completa

### v2.0 (Futuro)
- 📋 IA para predicción de stock
- 📋 Integración con ERPs
- 📋 Módulo de ventas
- 📋 App móvil nativa

## 🙏 Agradecimientos

- **Supabase**: Por la excelente plataforma de backend
- **Vercel**: Por el hosting y deploy automático
- **Railway**: Por el hosting del backend
- **Comunidad Open Source**: Por las librerías utilizadas

---

**GDE System** - Gestión de Inventario y Despacho Moderna 🚀





