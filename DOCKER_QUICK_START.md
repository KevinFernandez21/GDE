# 🚀 GDE - Inicio Rápido con Docker

## ⚡ Iniciar en 3 Comandos (Windows)

```powershell
# 1. Construir imágenes (solo primera vez)
docker-compose --env-file .env.docker build

# 2. Iniciar todos los servicios
docker-compose --env-file .env.docker up -d

# 3. Ver estado
docker-compose --env-file .env.docker ps
```

## 🌐 Acceder a la Aplicación

Una vez iniciado (espera 1-2 minutos):

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Nginx**: http://localhost:80
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **PgAdmin**: http://localhost:5050 (con profile tools)

## 📝 Comandos Útiles

### Ver Logs
```powershell
# Todos los servicios
docker-compose --env-file .env.docker logs -f

# Servicio específico
docker-compose --env-file .env.docker logs -f backend
docker-compose --env-file .env.docker logs -f frontend
```

### Detener Servicios
```powershell
# Detener pero mantener datos
docker-compose --env-file .env.docker stop

# Detener y eliminar contenedores
docker-compose --env-file .env.docker down
```

### Reiniciar Servicios
```powershell
# Reiniciar todo
docker-compose --env-file .env.docker restart

# Reiniciar servicio específico
docker-compose --env-file .env.docker restart backend
```

### Acceder a Contenedores
```powershell
# Backend
docker-compose --env-file .env.docker exec backend sh

# Frontend
docker-compose --env-file .env.docker exec frontend sh

# Base de datos
docker-compose --env-file .env.docker exec db psql -U gde_user -d gde_db
```

## 🗄️ Base de Datos

### Backup
```powershell
docker-compose --env-file .env.docker exec -T db pg_dump -U gde_user gde_db > backup.sql
```

### Restaurar
```powershell
Get-Content backup.sql | docker-compose --env-file .env.docker exec -T db psql -U gde_user gde_db
```

## 🧹 Limpieza Completa

```powershell
# Detener y eliminar todo (incluyendo volúmenes)
docker-compose --env-file .env.docker down -v

# Eliminar también imágenes
docker-compose --env-file .env.docker down -v --rmi all
```

## ⚙️ Configuración

### Editar Variables de Entorno

Archivo: `.env.docker`

```env
# Cambiar passwords
POSTGRES_PASSWORD=tu_password_seguro
SECRET_KEY=tu_clave_secreta

# Cambiar puertos si están en uso
# En docker-compose.yml:
ports:
  - "3001:3000"  # Frontend en puerto 3001
  - "8001:8000"  # Backend en puerto 8001
```

## 🔍 Troubleshooting

### Puerto en Uso
```powershell
# Ver qué proceso usa el puerto
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Cambiar puerto en docker-compose.yml
```

### Contenedor no Inicia
```powershell
# Ver logs de error
docker-compose --env-file .env.docker logs backend

# Reiniciar
docker-compose --env-file .env.docker restart backend

# Reconstruir
docker-compose --env-file .env.docker up -d --build backend
```

### Base de Datos no Conecta
```powershell
# Verificar estado
docker-compose --env-file .env.docker exec db pg_isready -U gde_user

# Ver logs
docker-compose --env-file .env.docker logs db

# Reiniciar
docker-compose --env-file .env.docker restart db
```

## 📚 Más Información

- **Guía Completa**: Ver `DOCKER_GUIDE.md`
- **Configuración**: Ver `docker-compose.yml`
- **Variables**: Ver `.env.docker`

---

**¡Listo para usar!** 🎉

