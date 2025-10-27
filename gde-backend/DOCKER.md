# 🐳 Docker Setup para GDE Backend

Esta guía te ayudará a ejecutar el backend de GDE usando Docker y Docker Compose.

## 📋 Prerrequisitos

- Docker 20.10+
- Docker Compose 2.0+
- Make (opcional, para usar comandos simplificados)

## 🚀 Inicio Rápido

### 1. Clonar y Configurar

```bash
cd gde-backend
cp env.docker .env
# Editar .env con tus configuraciones si es necesario
```

### 2. Ejecutar en Modo Desarrollo

```bash
# Opción 1: Usando Make (recomendado)
make dev

# Opción 2: Usando Docker Compose directamente
docker-compose up --build
```

### 3. Acceder a los Servicios

- **Backend API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **PgAdmin**: http://localhost:5050 (admin@gde-system.com / admin123)
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 🛠️ Comandos Útiles

### Usando Make (Recomendado)

```bash
# Desarrollo
make dev              # Ejecutar en modo desarrollo
make dev-detached     # Ejecutar en background
make logs             # Ver logs del backend
make shell            # Acceder al shell del contenedor
make test             # Ejecutar tests
make lint             # Ejecutar linting
make format           # Formatear código

# Base de datos
make init-db          # Inicializar base de datos
make backup-db        # Hacer backup
make restore-db FILE=backup.sql  # Restaurar backup

# Producción
make prod             # Ejecutar en modo producción
make deploy           # Desplegar en producción

# Limpieza
make clean            # Limpiar contenedores e imágenes
make down             # Detener servicios
```

### Usando Docker Compose

```bash
# Desarrollo
docker-compose up --build
docker-compose up -d
docker-compose logs -f backend
docker-compose exec backend /bin/bash

# Producción
docker-compose -f docker-compose.prod.yml up --build
docker-compose -f docker-compose.prod.yml up -d

# Base de datos
docker-compose exec backend python scripts/init_db.py
docker-compose exec postgres pg_dump -U gde_user gde_db > backup.sql
```

## 🏗️ Arquitectura de Contenedores

### Servicios Incluidos

1. **Backend API** (`gde-backend`)
   - FastAPI con hot reload en desarrollo
   - Puerto: 8000
   - Health check incluido

2. **PostgreSQL** (`gde-postgres`)
   - Base de datos principal
   - Puerto: 5432
   - Datos persistentes en volumen

3. **Redis** (`gde-redis`)
   - Cache y sesiones
   - Puerto: 6379
   - Datos persistentes en volumen

4. **PgAdmin** (`gde-pgadmin`)
   - Interfaz web para PostgreSQL
   - Puerto: 5050
   - Credenciales: admin@gde-system.com / admin123

5. **Nginx** (solo en producción)
   - Reverse proxy
   - Rate limiting
   - SSL termination

## 🔧 Configuración

### Variables de Entorno

Copia `env.docker` a `.env` y ajusta según necesites:

```env
# Database
POSTGRES_DB=gde_db
POSTGRES_USER=gde_user
POSTGRES_PASSWORD=gde_password

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
ENVIRONMENT=development
```

### Volúmenes Persistentes

- `postgres_data`: Datos de PostgreSQL
- `redis_data`: Datos de Redis
- `uploads_data`: Archivos subidos
- `logs_data`: Logs de la aplicación
- `pgadmin_data`: Configuración de PgAdmin

## 🧪 Testing

```bash
# Ejecutar tests
make test

# Tests con coverage
make test-cov

# Linting
make lint

# Formatear código
make format
```

## 📊 Monitoreo

### Health Checks

```bash
# Verificar salud de todos los servicios
make health

# Verificar solo backend
curl http://localhost:8000/health
```

### Logs

```bash
# Logs del backend
make logs

# Logs de todos los servicios
docker-compose logs -f

# Logs específicos
docker-compose logs -f postgres
docker-compose logs -f redis
```

## 🚀 Despliegue en Producción

### 1. Configurar Variables de Producción

```bash
cp env.docker .env.prod
# Editar .env.prod con valores de producción
```

### 2. Desplegar

```bash
# Usando Make
make deploy

# Usando Docker Compose
docker-compose -f docker-compose.prod.yml up --build -d
```

### 3. Verificar Despliegue

```bash
# Verificar servicios
make status-prod

# Verificar salud
curl http://localhost/health
```

## 🔒 Seguridad

### Configuración de Producción

1. **Cambiar credenciales por defecto**
2. **Configurar SSL/TLS**
3. **Usar secrets de Docker**
4. **Configurar firewall**
5. **Habilitar rate limiting**

### Secrets de Docker

```bash
# Crear secrets
echo "your-secret-key" | docker secret create secret_key -
echo "your-db-password" | docker secret create db_password -

# Usar en docker-compose.prod.yml
secrets:
  - secret_key
  - db_password
```

## 🐛 Troubleshooting

### Problemas Comunes

1. **Puerto ya en uso**
   ```bash
   # Cambiar puertos en docker-compose.yml
   ports:
     - "8001:8000"  # Cambiar 8000 por 8001
   ```

2. **Error de permisos**
   ```bash
   # Dar permisos al directorio
   sudo chown -R $USER:$USER .
   ```

3. **Base de datos no conecta**
   ```bash
   # Verificar que PostgreSQL esté corriendo
   docker-compose ps postgres
   
   # Ver logs de PostgreSQL
   docker-compose logs postgres
   ```

4. **Contenedor no inicia**
   ```bash
   # Ver logs detallados
   docker-compose logs backend
   
   # Reconstruir imagen
   docker-compose build --no-cache backend
   ```

### Limpiar Todo

```bash
# Detener y eliminar todo
make clean

# O manualmente
docker-compose down -v --rmi all
docker system prune -f
```

## 📚 Recursos Adicionales

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Docker Guide](https://fastapi.tiangolo.com/deployment/docker/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crear feature branch
3. Hacer cambios
4. Probar con Docker
5. Crear Pull Request

```bash
# Clonar tu fork
git clone https://github.com/tu-usuario/GDE_UNPULSED.git
cd GDE_UNPULSED/gde-backend

# Crear branch
git checkout -b feature/nueva-funcionalidad

# Hacer cambios y probar
make dev
make test

# Commit y push
git add .
git commit -m "feat: nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```
