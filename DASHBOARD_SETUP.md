# Dashboard Setup Guide

Este documento describe cómo configurar y ejecutar el dashboard en tiempo real del sistema GDE.

## Estructura del Dashboard

El dashboard muestra las siguientes métricas en tiempo real:

### 📦 Inventario y Stock
- **Total Productos**: Cantidad total de productos registrados
- **Stock OK**: Productos con stock por encima del mínimo
- **Stock Bajo**: Productos que requieren atención
- **Agotados**: Productos sin stock que necesitan reposición urgente

### 💰 Métricas Financieras
- **Valor Inventario**: Valor total del inventario al costo de compra
- **Valor Venta Potencial**: Valor potencial de venta del inventario
- **Margen Potencial**: Diferencia entre valor de venta y costo
- **Costos Totales**: Suma de gastos operacionales
- **Capital Total**: Aportes y préstamos registrados

### 📋 Seguimiento de Guías
- **Total Guías Master**: Cantidad de guías maestras
- **Escaneadas**: Guías que ya fueron escaneadas
- **Pendientes**: Guías por escanear
- **Desconocidas**: Guías duplicadas o no reconocidas
- **Porcentaje Completado**: Progreso del escaneo

### 📱 Actividad de Escaneo (Hoy)
- **Sesiones Activas**: Sesiones de pistola activas hoy
- **Total Escaneos**: Cantidad total de escaneos realizados
- **Guías Únicas**: Guías únicas escaneadas
- **Productos**: Cantidad de productos escaneados

### 🚚 Guías de Despacho (Último mes)
- **Total**: Total de guías del último mes
- **Pendientes**: Guías por despachar
- **En Tránsito**: Guías en proceso de entrega
- **Entregadas**: Guías ya entregadas

## Configuración del Backend

### 1. Endpoint creado

Se creó el endpoint `/api/v1/dashboard/metrics` que retorna todas las métricas del dashboard.

### 2. Archivo: `gde-backend/app/api/v1/dashboard.py`

Este archivo contiene:
- `GET /api/v1/dashboard/metrics`: Retorna todas las métricas del dashboard
- `GET /api/v1/dashboard/activity-summary`: Retorna resumen de actividad de las últimas 24 horas

### 3. Registro en `main.py`

El router de dashboard ya está registrado en el archivo principal de la aplicación.

## Configuración del Frontend

### 1. Variables de Entorno

Crea un archivo `.env.local` en `gde-frontend/` con:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Para producción, cambia la URL a la dirección de tu servidor backend.

### 2. Archivos creados

- **`src/types/dashboard.ts`**: Definiciones de tipos TypeScript para las métricas
- **`src/lib/api.ts`**: Cliente API para comunicación con el backend
- **`src/app/dashboard/page.tsx`**: Página del dashboard actualizada con datos en tiempo real

### 3. Funcionalidades

- **Auto-refresh**: El dashboard se actualiza automáticamente cada 30 segundos
- **Formato de moneda**: Usa formato chileno (CLP) para valores monetarios
- **Loading state**: Muestra un spinner mientras carga los datos
- **Error handling**: Muestra mensajes de error si hay problemas de conexión

## Cómo ejecutar

### Backend

```bash
cd gde-backend

# Instalar dependencias (primera vez)
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
python -m app.main

# O usando uvicorn directamente
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en `http://localhost:8000`

### Frontend

```bash
cd gde-frontend

# Instalar dependencias (primera vez)
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:3000`

### Acceder al Dashboard

1. Abre tu navegador en `http://localhost:3000/dashboard`
2. El dashboard cargará automáticamente las métricas desde el backend
3. Las métricas se actualizarán cada 30 segundos

## Estructura de la Respuesta del API

```typescript
{
  "inventario_stock": {
    "total_productos": 0,
    "total_stock": 0,
    "stock_ok": 0,
    "stock_bajo": 0,
    "agotados": 0,
    "porcentaje_stock_saludable": 0.0
  },
  "metricas_financieras": {
    "valor_inventario": 0.0,
    "valor_venta_potencial": 0.0,
    "margen_potencial": 0.0,
    "costos_totales": 0.0,
    "capital_total": 0.0,
    "capital_aportes": 0.0,
    "capital_prestamos": 0.0
  },
  "seguimiento_guias": {
    "total_guias_master": 0,
    "escaneadas": 0,
    "pendientes": 0,
    "desconocidas": 0,
    "duplicadas": 0,
    "porcentaje_completado": 0.0
  },
  "actividad_escaneo_hoy": {
    "sesiones_activas": 0,
    "total_escaneos": 0,
    "guias_escaneadas": 0,
    "productos_escaneados": 0
  },
  "guias_despacho_mes": {
    "total": 0,
    "pendientes": 0,
    "en_transito": 0,
    "entregadas": 0,
    "porcentaje_entregadas": 0.0
  },
  "timestamp": "2025-10-23T12:00:00.000000",
  "periodo": {
    "mes_inicio": "2025-09-23T12:00:00.000000",
    "hoy_inicio": "2025-10-23T00:00:00.000000"
  }
}
```

## Troubleshooting

### Error: "Failed to fetch"

**Problema**: El frontend no puede conectarse al backend.

**Solución**:
1. Verifica que el backend esté corriendo en `http://localhost:8000`
2. Revisa que la variable `NEXT_PUBLIC_API_URL` en `.env.local` sea correcta
3. Verifica que CORS esté configurado correctamente en el backend

### Error: "Unauthorized"

**Problema**: El endpoint requiere autenticación.

**Solución**:
1. Asegúrate de estar autenticado
2. El token de autenticación debe ser pasado al cliente API usando `apiClient.setToken(token)`

### El dashboard muestra "0" en todas las métricas

**Problema**: La base de datos está vacía.

**Solución**:
1. Verifica que la base de datos tenga datos
2. Ejecuta el script de inicialización si existe
3. Agrega productos y guías de prueba

## Próximos Pasos

1. **Autenticación**: Integrar el sistema de autenticación con Supabase o JWT
2. **Gráficas**: Agregar gráficas visuales para tendencias
3. **Filtros**: Permitir filtrar métricas por fecha, categoría, etc.
4. **Exportación**: Permitir exportar datos a Excel/PDF
5. **Notificaciones**: Agregar notificaciones en tiempo real para alertas de stock
6. **WebSockets**: Implementar WebSockets para actualizaciones en tiempo real más eficientes

## Documentación Adicional

- **Backend API**: Ver documentación en `http://localhost:8000/docs` (Swagger UI)
- **Frontend**: Ver `docs/frontend/dashboard.md` para más detalles
- **Base de Datos**: Ver `docs/database/` para esquemas y relaciones

