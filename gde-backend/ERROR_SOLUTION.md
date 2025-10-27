# 🔧 Solución del Error de Inicio del Backend

## ❌ Error Encontrado

```
ModuleNotFoundError: No module named 'psycopg2'
```

## 🔍 Causa del Problema

El error ocurre porque faltan las dependencias de Python instaladas, específicamente el driver de PostgreSQL (`psycopg2-binary`).

## ✅ Solución Paso a Paso

### 1. Verificar archivo .env
El archivo `.env` ya fue creado automáticamente. Si necesitas revisarlo:

```bash
cd /home/hombrenaranja/Desktop/projects/GDE_UNPULSED/gde-backend
cat .env
```

### 2. Instalar Dependencias

**Opción A: Usando pip (recomendado)**

```bash
cd /home/hombrenaranja/Desktop/projects/GDE_UNPULSED/gde-backend

# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar que psycopg2 esté instalado
pip list | grep psycopg2
```

**Opción B: Instalar solo lo necesario primero**

```bash
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary pydantic pydantic-settings python-dotenv supabase
```

### 3. Verificar la instalación

```bash
python -c "import psycopg2; print('✅ psycopg2 instalado correctamente')"
python -c "from app.main import app; print('✅ App cargada correctamente')"
```

### 4. Iniciar el servidor

**Opción A: Usando uvicorn directamente**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Opción B: Usando el módulo main**

```bash
python -m app.main
```

**Opción C: Usando el Makefile** (si existe)

```bash
make run
```

### 5. Verificar que funcione

Abre tu navegador en:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000/

## 🐳 Alternativa: Usar Docker

Si prefieres usar Docker (recomendado para producción):

```bash
cd /home/hombrenaranja/Desktop/projects/GDE_UNPULSED/gde-backend

# Construir imagen
docker-compose build

# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend
```

## 📋 Comandos de Verificación

```bash
# 1. Verificar Python
python --version  # Debe ser 3.11+

# 2. Verificar pip
pip --version

# 3. Verificar variables de entorno
cat .env

# 4. Verificar estructura de archivos
ls -la app/

# 5. Verificar imports
python -c "from app.core.config import settings; print('Config OK')"
python -c "from app.core.database import engine; print('Database OK')"
python -c "from app.main import app; print('App OK')"
```

## 🔧 Solución Rápida (Todo en uno)

```bash
#!/bin/bash

# Script de solución rápida
cd /home/hombrenaranja/Desktop/projects/GDE_UNPULSED/gde-backend

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo "🔍 Verificando instalación..."
python -c "import psycopg2; print('✅ psycopg2 OK')"
python -c "from app.main import app; print('✅ App OK')"

echo "🚀 Iniciando servidor..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Guarda esto en un archivo `quick_fix.sh`, dale permisos y ejecútalo:

```bash
chmod +x quick_fix.sh
./quick_fix.sh
```

## 🐛 Otros Problemas Comunes

### Error: "DATABASE_URL not found"
**Solución**: Asegúrate de que el archivo `.env` existe y contiene las variables necesarias.

```bash
# Verificar que existe
ls -la .env

# Si no existe, copiarlo del ejemplo
cp env.example .env
```

### Error: "Cannot connect to database"
**Solución**: Verifica las credenciales de Supabase en el archivo `.env`.

```bash
# Editar el archivo .env
nano .env

# O usar tu editor favorito
code .env
```

### Error: "Port 8000 already in use"
**Solución**: Cambia el puerto o detén el proceso que lo está usando.

```bash
# Ver qué está usando el puerto 8000
lsof -i :8000

# Matar el proceso (reemplaza PID con el número real)
kill -9 PID

# O usar otro puerto
uvicorn app.main:app --reload --port 8001
```

## ✅ Checklist de Verificación

Antes de iniciar el servidor, verifica:

- [ ] Python 3.11+ instalado
- [ ] Archivo `.env` existe y está configurado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] `psycopg2-binary` instalado
- [ ] Credenciales de Supabase correctas
- [ ] Puerto 8000 disponible
- [ ] Directorios `uploads/` y `logs/` creados

## 🎯 Resumen

**El error principal es**: Falta instalar las dependencias de Python.

**La solución es**:
```bash
cd /home/hombrenaranja/Desktop/projects/GDE_UNPULSED/gde-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📚 Recursos Adicionales

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Documentación Uvicorn](https://www.uvicorn.org/)
- [Documentación SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentación Supabase](https://supabase.com/docs)

---

**Última actualización**: Octubre 2025


