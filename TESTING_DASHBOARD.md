# Testing Dashboard Integration

Esta guía describe cómo probar la integración completa del dashboard.

## Pre-requisitos

1. Python 3.9+ instalado
2. Node.js 18+ instalado
3. PostgreSQL o SQLite configurado
4. Variables de entorno configuradas

## Paso 1: Verificar Backend

### 1.1 Iniciar el backend

```bash
cd gde-backend
python -m app.main
```

Deberías ver:
```
INFO:     Starting GDE Backend API...
INFO:     Database tables created successfully
INFO:     GDE Backend API started successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 1.2 Probar el endpoint de salud

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T...",
  "version": "1.0.0",
  "environment": "development"
}
```

### 1.3 Probar el endpoint del dashboard (sin autenticación)

**Nota**: Si el endpoint requiere autenticación, necesitarás primero obtener un token.

```bash
curl http://localhost:8000/api/v1/dashboard/metrics
```

Si recibes un error 401, necesitas autenticarte primero:

```bash
# 1. Crear un usuario (si no existe)
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User"
  }'

# 2. Obtener token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'

# 3. Usar el token en las peticiones
curl http://localhost:8000/api/v1/dashboard/metrics \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 1.4 Verificar la estructura de la respuesta

La respuesta debe tener esta estructura:

```json
{
  "inventario_stock": {
    "total_productos": 0,
    "total_stock": 0,
    "stock_ok": 0,
    "stock_bajo": 0,
    "agotados": 0,
    "porcentaje_stock_saludable": 0.0
  },
  "metricas_financieras": { ... },
  "seguimiento_guias": { ... },
  "actividad_escaneo_hoy": { ... },
  "guias_despacho_mes": { ... },
  "timestamp": "...",
  "periodo": { ... }
}
```

## Paso 2: Verificar Frontend

### 2.1 Crear archivo de variables de entorno

En `gde-frontend/`, crea `.env.local`:

```bash
cd gde-frontend
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
```

### 2.2 Instalar dependencias

```bash
npm install
```

### 2.3 Iniciar el servidor de desarrollo

```bash
npm run dev
```

Deberías ver:
```
▲ Next.js 16.0.0
- Local:        http://localhost:3000
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

### 2.4 Abrir el dashboard en el navegador

Navega a: `http://localhost:3000/dashboard`

## Paso 3: Verificar la Integración

### 3.1 Verificar que el dashboard cargue

✅ **Éxito**: Deberías ver un banner verde que dice "✓ Conectado"

❌ **Error**: Si ves un banner rojo con un error, verifica:
- Que el backend esté corriendo
- Que la URL en `.env.local` sea correcta
- Que no haya problemas de CORS

### 3.2 Verificar que los datos se muestren

Con una base de datos vacía, deberías ver:
- Todos los contadores en 0
- Todos los valores monetarios en $0
- Todos los porcentajes en 0.0%

### 3.3 Agregar datos de prueba

Para verificar que los datos se actualicen, puedes agregar productos de prueba:

```bash
# Usando curl (reemplaza YOUR_TOKEN_HERE con tu token)
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": "PROD001",
    "nombre": "Producto de Prueba",
    "precio_costo": 10000,
    "precio_venta": 15000,
    "stock_actual": 50,
    "stock_minimo": 10,
    "categoria_id": 1
  }'
```

Después de agregar productos:
1. Espera 30 segundos (auto-refresh) o recarga la página
2. Verifica que "Total Productos" ahora muestre 1
3. Verifica que "Stock OK" muestre 1
4. Verifica que "Valor Inventario" muestre $10.000

### 3.4 Verificar auto-refresh

1. Abre las Developer Tools del navegador (F12)
2. Ve a la pestaña "Network"
3. Espera 30 segundos
4. Deberías ver una nueva petición a `/api/v1/dashboard/metrics`

## Paso 4: Pruebas de Carga

### 4.1 Probar con múltiples productos

Crea un script para agregar múltiples productos:

```python
# test_populate.py
import requests
import random

API_URL = "http://localhost:8000"
TOKEN = "YOUR_TOKEN_HERE"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

for i in range(100):
    product = {
        "codigo": f"PROD{i:04d}",
        "nombre": f"Producto {i}",
        "precio_costo": random.randint(5000, 50000),
        "precio_venta": random.randint(8000, 80000),
        "stock_actual": random.randint(0, 100),
        "stock_minimo": 10,
        "categoria_id": 1
    }
    
    response = requests.post(
        f"{API_URL}/api/v1/products/",
        json=product,
        headers=headers
    )
    
    if response.status_code == 200:
        print(f"✓ Producto {i} creado")
    else:
        print(f"✗ Error creando producto {i}: {response.text}")

print("\n✓ Productos de prueba creados")
```

Ejecutar:
```bash
python test_populate.py
```

### 4.2 Verificar el rendimiento

1. Abre el dashboard
2. Abre Developer Tools > Performance
3. Graba un perfil durante 10 segundos
4. Verifica que no haya lags o problemas de rendimiento

## Paso 5: Verificar Errores Comunes

### Error: CORS

Si ves un error de CORS en la consola del navegador:

```
Access to fetch at 'http://localhost:8000/api/v1/dashboard/metrics' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solución**: Verifica la configuración de CORS en `gde-backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Agregar frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Error: Connection Refused

Si ves:
```
Error: Failed to fetch
```

**Solución**:
1. Verifica que el backend esté corriendo
2. Verifica que la URL sea correcta
3. Verifica que no haya firewall bloqueando el puerto 8000

### Error: 401 Unauthorized

Si recibes 401:

**Solución**:
1. El endpoint requiere autenticación
2. Necesitas implementar el flujo de login primero
3. O temporalmente modificar el endpoint para no requerir autenticación (solo para desarrollo)

En `gde-backend/app/api/v1/dashboard.py`, cambia:
```python
# De:
async def get_dashboard_metrics(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)  # <-- Requiere auth
)

# A (solo para testing):
async def get_dashboard_metrics(
    db: Session = Depends(get_db)  # <-- Sin auth
)
```

## Paso 6: Verificación Final

### Checklist de Funcionalidades

- [ ] Backend arranca sin errores
- [ ] Endpoint `/health` responde correctamente
- [ ] Endpoint `/api/v1/dashboard/metrics` retorna datos
- [ ] Frontend arranca sin errores
- [ ] Dashboard carga y muestra datos
- [ ] Auto-refresh funciona cada 30 segundos
- [ ] Formato de moneda es correcto (CLP)
- [ ] Todas las secciones del dashboard muestran datos
- [ ] Agregar productos actualiza las métricas
- [ ] No hay errores en la consola del navegador
- [ ] No hay errores de linter críticos

### Resultado Esperado

✅ **Éxito Total**: Todos los items del checklist están marcados

⚠️ **Éxito Parcial**: Algunos items fallan pero el dashboard funciona

❌ **Fallo**: El dashboard no carga o hay errores críticos

## Siguientes Pasos

Una vez que la integración esté funcionando:

1. **Implementar autenticación completa**
2. **Agregar más datos de prueba**
3. **Configurar base de datos de producción**
4. **Deploy a servidor de staging**
5. **Configurar monitoreo y logs**

## Soporte

Si encuentras problemas:

1. Revisa los logs del backend
2. Revisa la consola del navegador
3. Verifica la configuración de red
4. Consulta la documentación en `/docs`

