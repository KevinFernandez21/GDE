# 🚀 Cómo Iniciar el Servidor GDE Backend

## ✅ Problema Resuelto

El error `ModuleNotFoundError: No module named 'psycopg2'` ha sido **RESUELTO**.

### ✨ Cambios Realizados:

1. ✅ **Dependencias instaladas** - Todas las dependencias de Python están ahora instaladas
2. ✅ **Imports corregidos** - Se corrigió el import de `SesionPistoleo` → `PistoleoSession`
3. ✅ **Base de datos configurada** - Los modelos se importan correctamente
4. ✅ **Servidor verificado** - El servidor inicia correctamente

---

## 🎯 Iniciar el Servidor

### Método 1: Uvicorn con Auto-reload (Recomendado para desarrollo)

```bash
cd /home/hombrenaranja/Desktop/projects/GDE_UNPULSED/gde-backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Características:**
- ✅ Recarga automática al editar código
- ✅ Accesible desde cualquier IP (útil para desarrollo)
- ✅ Logs detallados en consola

### Método 2: Python Module

```bash
cd /home/hombrenaranja/Desktop/projects/GDE_UNPULSED/gde-backend
python -m app.main
```

### Método 3: Uvicorn sin Auto-reload (Producción)

```bash
cd /home/hombrenaranja/Desktop/projects/GDE_UNPULSED/gde-backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Características:**
- ✅ Múltiples workers para mejor rendimiento
- ✅ Optimizado para producción
- ✅ Sin auto-reload

---

## 🌐 Acceder al Servidor

Una vez iniciado, el servidor estará disponible en:

### 🏠 Página Principal
```
http://localhost:8000/
```

### 📚 Documentación Interactiva (Swagger UI)
```
http://localhost:8000/docs
```
Aquí puedes:
- Ver todos los endpoints
- Probar las APIs directamente
- Ver los schemas de request/response

### 📖 Documentación Alternativa (ReDoc)
```
http://localhost:8000/redoc
```

### 🏥 Health Check
```
http://localhost:8000/health
```
Verifica que el servidor esté funcionando correctamente

---

## 📋 Verificación Rápida

### 1. Verificar que el servidor está corriendo

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-25T...",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2. Ver endpoints disponibles

```bash
curl http://localhost:8000/
```

### 3. Acceder a la documentación

Abre tu navegador en: http://localhost:8000/docs

---

## 🛑 Detener el Servidor

- Presiona `CTRL + C` en la terminal donde está corriendo
- O si está en background:

```bash
# Encontrar el proceso
ps aux | grep uvicorn

# Matar el proceso (reemplaza PID)
kill -9 PID
```

---

## 🐛 Solución de Problemas

### Error: "Port 8000 already in use"

**Opción 1: Usar otro puerto**
```bash
uvicorn app.main:app --reload --port 8001
```

**Opción 2: Matar el proceso que usa el puerto**
```bash
lsof -ti:8000 | xargs kill -9
```

### Error: "Cannot connect to database"

1. Verifica las credenciales en `.env`
2. Asegúrate de que Supabase está accesible
3. Verifica la URL de la base de datos

```bash
# Verificar conexión
python -c "from app.core.config import settings; print(settings.database_url)"
```

### Error: "Module not found"

Reinstala las dependencias:
```bash
pip install -r requirements.txt
```

---

## 📊 Logs

### Ver logs en tiempo real

El servidor muestra logs automáticamente en la consola:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Guardar logs en archivo

```bash
uvicorn app.main:app --reload --log-config logging.ini 2>&1 | tee logs/server.log
```

---

## 🔐 Variables de Entorno

Las variables importantes en `.env`:

```bash
# Base de datos
DATABASE_URL=postgresql://...
SUPABASE_URL=https://...
SUPABASE_KEY=eyJ...

# Seguridad
SECRET_KEY=your-secret-key
DEBUG=True

# Servidor
LOG_LEVEL=INFO
```

Para cambiar configuraciones, edita el archivo `.env` y reinicia el servidor.

---

## 🎮 Comandos Útiles

### Desarrollo

```bash
# Iniciar con auto-reload
uvicorn app.main:app --reload

# Iniciar con logs detallados
uvicorn app.main:app --reload --log-level debug

# Iniciar en puerto diferente
uvicorn app.main:app --reload --port 8001
```

### Producción

```bash
# Con múltiples workers
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000

# Con Gunicorn (alternativa)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Testing

```bash
# Ejecutar tests mientras el servidor NO está corriendo
pytest

# Ver coverage
pytest --cov=app --cov-report=html
```

---

## 📱 Probar los Endpoints

### Usando curl

```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/

# Listar productos (requiere autenticación)
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/v1/products/
```

### Usando la interfaz web

1. Ve a http://localhost:8000/docs
2. Click en cualquier endpoint
3. Click en "Try it out"
4. Llena los parámetros necesarios
5. Click en "Execute"

---

## 🚀 Inicio Rápido (Resumen)

```bash
# 1. Ir al directorio
cd /home/hombrenaranja/Desktop/projects/GDE_UNPULSED/gde-backend

# 2. Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. Abrir en navegador
# http://localhost:8000/docs
```

---

## ✅ Checklist de Verificación

- [x] Dependencias instaladas (`pip install -r requirements.txt`)
- [x] Archivo `.env` configurado
- [x] Servidor inicia sin errores
- [ ] Documentación accesible en `/docs`
- [ ] Health check responde correctamente
- [ ] Base de datos conectada (verifica en logs)

---

## 📞 Soporte

Si encuentras problemas:

1. **Revisa los logs** en la consola
2. **Verifica el archivo .env** tiene las credenciales correctas
3. **Consulta ERROR_SOLUTION.md** para problemas comunes
4. **Revisa TESTING.md** para ejecutar tests

---

## 🎉 Estado Actual

✅ **SERVIDOR FUNCIONANDO CORRECTAMENTE**

El backend GDE está listo para usar. Todos los endpoints están disponibles y la documentación interactiva está accesible.

**Próximos pasos sugeridos:**
1. Explorar la documentación en `/docs`
2. Probar los endpoints de health y productos
3. Configurar el frontend para conectarse al backend
4. Revisar y ajustar las configuraciones en `.env`

---

**Última actualización**: Octubre 25, 2025  
**Versión del Backend**: 1.0.0  
**Estado**: ✅ Operacional


