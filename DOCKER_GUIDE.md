# 🐳 GDE - Guía Completa de Docker

## 📋 Resumen

Esta guía te ayudará a ejecutar el proyecto GDE completo usando Docker y Docker Compose.

---

## 🚀 Inicio Rápido (3 minutos)

```bash
# 1. Dar permisos de ejecución al script
chmod +x docker-manage.sh

# 2. Configurar variables de entorno
./docker-manage.sh setup

# 3. Construir y iniciar todos los servicios
./docker-manage.sh build
./docker-manage.sh start

# 4. Acceder a la aplicación
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## 📦 ¿Qué incluye el Stack Docker?

### Servicios Principales

1. **PostgreSQL Database** (Puerto 5432)
   - Base de datos principal
   - Volumen persistente
   - Health checks automáticos

2. **Redis Cache** (Puerto 6379)
   - Cache para mejorar rendimiento
   - Persistencia opcional

3. **Backend API** (Puerto 8000)
   - FastAPI application
   - Auto-reload en desarrollo
   - Health checks

4. **Frontend** (Puerto 3000)
   - Next.js application
   - Hot reload habilitado
   - Optimización de build

5. **Nginx** (Puerto 80)
   - Reverse proxy
   - Load balancing
   - Compresión gzip

6. **PgAdmin** (Puerto 5050) - Opcional
   - Gestión de base de datos
   - Interface web

---

## 🛠️ Prerrequisitos

### Instalar Docker

**Windows:**
- Descargar [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop)
- Ejecutar instalador
- Reiniciar sistema

**macOS:**
- Descargar [Docker Desktop para Mac](https://www.docker.com/products/docker-desktop)
- Instalar aplicación
- Iniciar Docker

**Linux (Ubuntu/Debian):**
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

### Verificar Instalación

```bash
docker --version
docker-compose --version
```

---

## 📝 Configuración Paso a Paso

### 1. Preparar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.docker.example .env.docker

# O usar el script
./docker-manage.sh setup
```

El archivo `.env.docker` contiene todas las configuraciones necesarias:

```env
# Database
POSTGRES_DB=gde_db
POSTGRES_USER=gde_user
POSTGRES_PASSWORD=tu_password_seguro

# Backend
SECRET_KEY=tu_secret_key_super_segura
DEBUG=True
ENVIRONMENT=development

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 2. Construir Contenedores

```bash
# Método 1: Usar script de gestión
./docker-manage.sh build

# Método 2: Docker Compose directo
docker-compose --env-file .env.docker build
```

### 3. Iniciar Servicios

```bash
# Iniciar todos los servicios
./docker-manage.sh start

# O en primer plano (para ver logs)
docker-compose --env-file .env.docker up
```

### 4. Verificar Estado

```bash
# Ver estado de servicios
./docker-manage.sh status

# Ver logs
./docker-manage.sh logs

# Ver logs de un servicio específico
./docker-manage.sh logs backend
./docker-manage.sh logs frontend
```

---

## 🎮 Comandos Disponibles

### Script de Gestión (`docker-manage.sh`)

```bash
# Configuración inicial
./docker-manage.sh setup

# Build y Deploy
./docker-manage.sh build      # Construir contenedores
./docker-manage.sh start      # Iniciar servicios
./docker-manage.sh stop       # Detener servicios
./docker-manage.sh restart    # Reiniciar servicios

# Monitoreo
./docker-manage.sh status     # Ver estado
./docker-manage.sh logs       # Ver todos los logs
./docker-manage.sh logs backend  # Logs específicos

# Acceso a contenedores
./docker-manage.sh exec backend   # Shell en backend
./docker-manage.sh exec frontend  # Shell en frontend
./docker-manage.sh exec db        # Shell en database

# Base de datos
./docker-manage.sh backup     # Backup de BD
./docker-manage.sh restore backup.sql  # Restaurar BD

# Limpieza
./docker-manage.sh clean      # Limpiar todo
```

### Docker Compose Directo

```bash
# Iniciar servicios
docker-compose --env-file .env.docker up -d

# Ver logs
docker-compose --env-file .env.docker logs -f

# Detener servicios
docker-compose --env-file .env.docker down

# Reconstruir servicios
docker-compose --env-file .env.docker up -d --build

# Ver estado
docker-compose --env-file .env.docker ps

# Ejecutar comando en contenedor
docker-compose --env-file .env.docker exec backend sh
docker-compose --env-file .env.docker exec frontend sh
```

---

## 🌐 Acceso a los Servicios

Una vez iniciados los servicios:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend | http://localhost:3000 | Aplicación Next.js |
| Backend | http://localhost:8000 | API FastAPI |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Redoc | http://localhost:8000/redoc | Redoc UI |
| Nginx | http://localhost:80 | Reverse Proxy |
| PostgreSQL | localhost:5432 | Base de datos |
| Redis | localhost:6379 | Cache |
| PgAdmin | http://localhost:5050 | Admin de BD |

### Credenciales por Defecto

**PgAdmin:**
- Email: `admin@gde-system.com`
- Password: `admin123`

**PostgreSQL:**
- Host: `localhost`
- Port: `5432`
- Database: `gde_db`
- User: `gde_user`
- Password: (ver `.env.docker`)

---

## 🔧 Configuración Avanzada

### Modo Desarrollo vs Producción

**Desarrollo (actual):**
```yaml
# docker-compose.yml usa Dockerfile.dev
# Hot reload habilitado
# Volumes montados para cambios en tiempo real
```

**Producción:**
```bash
# Usar docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml up -d
```

### Perfiles de Docker Compose

```bash
# Iniciar con herramientas adicionales (PgAdmin)
docker-compose --profile tools up -d

# Sin herramientas
docker-compose up -d
```

### Variables de Entorno Personalizadas

Puedes sobrescribir cualquier variable:

```bash
# Archivo .env.docker
POSTGRES_PASSWORD=mi_password_super_seguro
SECRET_KEY=clave_secreta_muy_larga_y_segura

# O en línea de comandos
POSTGRES_PASSWORD=mipass docker-compose up -d
```

---

## 🗄️ Gestión de Base de Datos

### Backup de Base de Datos

```bash
# Backup automático con timestamp
./docker-manage.sh backup

# O manual
docker-compose exec -T db pg_dump -U gde_user gde_db > backup.sql
```

### Restaurar Base de Datos

```bash
# Usando script
./docker-manage.sh restore backup.sql

# O manual
docker-compose exec -T db psql -U gde_user gde_db < backup.sql
```

### Acceder a PostgreSQL

```bash
# Método 1: Usando script
./docker-manage.sh exec db

# Método 2: Docker Compose
docker-compose exec db psql -U gde_user -d gde_db

# Método 3: Cliente externo
psql -h localhost -p 5432 -U gde_user -d gde_db
```

### Ejecutar Scripts SQL

```bash
# Desde archivo
docker-compose exec -T db psql -U gde_user -d gde_db < script.sql

# Desde comando
docker-compose exec db psql -U gde_user -d gde_db -c "SELECT * FROM users;"
```

---

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real

```bash
# Todos los servicios
docker-compose logs -f

# Servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend

# Últimas 100 líneas
docker-compose logs --tail=100 backend
```

### Inspeccionar Contenedores

```bash
# Estado detallado
docker-compose ps

# Inspeccionar contenedor
docker inspect gde-backend

# Estadísticas en tiempo real
docker stats

# Procesos en contenedor
docker-compose exec backend ps aux
```

---

## 🧹 Limpieza y Mantenimiento

### Limpiar Contenedores Detenidos

```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar también volúmenes
docker-compose down -v

# Eliminar todo (incluyendo imágenes)
docker-compose down -v --rmi all
```

### Limpiar Sistema Docker

```bash
# Eliminar contenedores detenidos
docker container prune

# Eliminar imágenes sin usar
docker image prune -a

# Eliminar volúmenes sin usar
docker volume prune

# Limpiar todo
docker system prune -a --volumes
```

### Script de Limpieza Completa

```bash
./docker-manage.sh clean
```

---

## 🔍 Troubleshooting

### Problema: Puerto en uso

```bash
# Error: bind: address already in use

# Solución 1: Identificar proceso
lsof -i :3000
lsof -i :8000

# Solución 2: Cambiar puertos en docker-compose.yml
ports:
  - "3001:3000"  # Usar puerto 3001 en lugar de 3000
```

### Problema: Contenedor no inicia

```bash
# Ver logs del contenedor
docker-compose logs backend

# Ver estado
docker-compose ps

# Reiniciar servicio específico
docker-compose restart backend

# Reconstruir
docker-compose up -d --build backend
```

### Problema: Base de datos no conecta

```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps db

# Ver logs de PostgreSQL
docker-compose logs db

# Probar conexión
docker-compose exec db pg_isready -U gde_user

# Reiniciar base de datos
docker-compose restart db
```

### Problema: Frontend no actualiza cambios

```bash
# 1. Verificar que el volumen esté montado
docker-compose exec frontend ls -la /app

# 2. Reiniciar frontend
docker-compose restart frontend

# 3. Reconstruir si es necesario
docker-compose up -d --build frontend
```

### Problema: Permisos de volúmenes

```bash
# Linux: ajustar permisos
sudo chown -R $USER:$USER ./gde-backend/uploads
sudo chown -R $USER:$USER ./gde-backend/logs

# O en el contenedor
docker-compose exec backend chown -R node:node /app/uploads
```

---

## 🚀 Despliegue a Producción

### Preparar para Producción

1. **Actualizar .env.docker:**
```env
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=clave_super_segura_generada_con_openssl
POSTGRES_PASSWORD=password_muy_seguro
```

2. **Usar docker-compose.prod.yml:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. **Habilitar HTTPS en Nginx:**
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... resto de configuración
}
```

4. **Backup Automático:**
```bash
# Crear cron job para backups
0 2 * * * cd /path/to/gde && ./docker-manage.sh backup
```

---

## 📈 Optimización y Performance

### Optimizar Builds

```bash
# Build paralelo
COMPOSE_PARALLEL_LIMIT=4 docker-compose build

# Usar cache de build
docker-compose build --parallel

# Build sin cache (cuando hay problemas)
docker-compose build --no-cache
```

### Limitar Recursos

```yaml
# En docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### Monitoreo de Recursos

```bash
# Estadísticas en tiempo real
docker stats

# Ver uso de disco
docker system df

# Analizar tamaño de imágenes
docker images --format "{{.Repository}}:{{.Tag}}\t{{.Size}}"
```

---

## ✅ Checklist de Producción

- [ ] Variables de entorno configuradas
- [ ] Passwords seguros generados
- [ ] HTTPS habilitado
- [ ] Backups automáticos configurados
- [ ] Health checks funcionando
- [ ] Logs centralizados
- [ ] Monitoreo activo
- [ ] Recursos limitados
- [ ] Firewall configurado
- [ ] Volúmenes con backup
- [ ] Actualizaciones automáticas
- [ ] Plan de disaster recovery

---

## 📚 Recursos Adicionales

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Redis Docker Image](https://hub.docker.com/_/redis)
- [Nginx Docker Image](https://hub.docker.com/_/nginx)

---

## 🆘 Obtener Ayuda

Si encuentras problemas:

1. Revisa los logs: `./docker-manage.sh logs`
2. Verifica el estado: `./docker-manage.sh status`
3. Consulta esta guía
4. Revisa Issues en GitHub
5. Contacta al equipo de desarrollo

---

**GDE System - Docker Guide v1.0.0**  
© 2025 - Sistema Completo con Docker 🐳

