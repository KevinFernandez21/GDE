# Entidades de la Base de Datos GDE

## 👥 Gestión de Usuarios

### `profiles`
Perfiles de usuario que extienden la tabla `auth.users` de Supabase.

**Campos principales:**
- `id`: UUID (FK a auth.users)
- `username`: Nombre de usuario único
- `full_name`: Nombre completo
- `role`: Rol del usuario (admin, contable, programador)
- `avatar_url`: URL del avatar
- `is_active`: Estado activo/inactivo
- `last_login`: Último acceso

**Relaciones:**
- Referenciado por: `products.created_by`, `guias.created_by`, `costos.created_by`

### `roles`
Roles y permisos del sistema.

**Campos principales:**
- `name`: Nombre del rol
- `permissions`: JSONB con permisos específicos
- `description`: Descripción del rol

### `user_preferences`
Configuraciones personales de cada usuario.

**Campos principales:**
- `user_id`: FK a profiles
- `tema`: Tema de interfaz (claro, oscuro, auto)
- `idioma`: Idioma preferido
- `notificaciones_email`: Preferencias de email
- `configuraciones`: JSONB con configuraciones adicionales

## 📦 Inventario y Productos

### `categories`
Categorías jerárquicas de productos.

**Campos principales:**
- `name`: Nombre de la categoría
- `description`: Descripción
- `parent_id`: FK a categories (jerarquía)
- `color`: Color hexadecimal para UI
- `icon`: Icono para UI
- `sort_order`: Orden de visualización

### `products`
Catálogo completo de productos con información de inventario.

**Campos principales:**
- `code`: Código único del producto
- `name`: Nombre del producto
- `category_id`: FK a categories
- `stock_actual`: Stock actual
- `stock_minimo`: Stock mínimo
- `stock_maximo`: Stock máximo
- `precio_compra`: Precio de compra
- `precio_venta`: Precio de venta
- `ubicacion_bodega`: Ubicación en bodega
- `proveedor`: Proveedor
- `codigo_barras`: Código de barras
- `imagenes`: Array de URLs de imágenes
- `metadata`: JSONB con datos adicionales

### `kardex`
Registro cronológico de movimientos de inventario.

**Campos principales:**
- `product_id`: FK a products
- `tipo_movimiento`: entrada, salida, ajuste, transferencia
- `documento_asociado`: Documento que origina el movimiento
- `cantidad`: Cantidad movida
- `saldo_anterior`: Stock anterior
- `saldo_actual`: Stock actual
- `costo_unitario`: Costo unitario
- `costo_promedio`: Costo promedio ponderado
- `valor_total`: Valor total del movimiento

## 📋 Gestión Documental

### `guias`
Guías de despacho con seguimiento completo.

**Campos principales:**
- `codigo`: Código único de la guía
- `estado`: pendiente, en_transito, entregada, devuelta, cancelada
- `cliente_nombre`: Nombre del cliente
- `cliente_ruc`: RUC del cliente
- `cliente_direccion`: Dirección del cliente
- `direccion_entrega`: Dirección de entrega
- `fecha_creacion`: Fecha de creación
- `fecha_estimada_entrega`: Fecha estimada
- `fecha_entrega_real`: Fecha real de entrega
- `transportista`: Empresa transportista
- `peso_total`: Peso total
- `valor_declarado`: Valor declarado

### `guia_items`
Items específicos en cada guía.

**Campos principales:**
- `guia_id`: FK a guias
- `product_id`: FK a products
- `cantidad`: Cantidad del producto
- `precio_unitario`: Precio unitario
- `descuento`: Descuento aplicado
- `subtotal`: Subtotal calculado

### `guia_movimientos`
Historial de ubicaciones y estados de las guías.

**Campos principales:**
- `guia_id`: FK a guias
- `usuario_id`: FK a profiles
- `accion`: Acción realizada
- `ubicacion`: Ubicación actual
- `evidencias`: Array de URLs de fotos/comprobantes
- `fecha_movimiento`: Fecha del movimiento

## 🔫 Pistoleo en Tiempo Real

### `pistoleo_sessions`
Sesiones de escaneo activas.

**Campos principales:**
- `codigo_qr`: Código QR único de la sesión
- `usuario_id`: FK a profiles
- `nombre_sesion`: Nombre descriptivo
- `fecha_inicio`: Fecha de inicio
- `fecha_fin`: Fecha de finalización
- `estado`: active, completed, cancelled
- `escaneos_totales`: Contador de escaneos
- `guias_procesadas`: Contador de guías procesadas
- `ubicacion`: Ubicación de la sesión

### `escaneos`
Registro individual de cada escaneo.

**Campos principales:**
- `session_id`: FK a pistoleo_sessions
- `guia_id`: FK a guias (opcional)
- `codigo_barras`: Código escaneado
- `tipo_codigo`: Tipo de código (CODE128, QR, etc.)
- `fecha_escaneo`: Timestamp del escaneo
- `dispositivo`: Información del dispositivo
- `ubicacion`: Ubicación GPS
- `latitud/longitud`: Coordenadas GPS
- `imagen_url`: URL de imagen del escaneo
- `estado_escaneo`: success, error, duplicate
- `metadata`: JSONB con datos adicionales

## 💰 Contabilidad

### `cost_categories`
Categorías contables jerárquicas.

**Campos principales:**
- `name`: Nombre de la categoría
- `tipo`: gasto, ingreso, costo
- `parent_id`: FK a cost_categories (jerarquía)
- `color`: Color para UI
- `sort_order`: Orden de visualización

### `costos`
Movimientos monetarios y gastos.

**Campos principales:**
- `fecha`: Fecha del movimiento
- `categoria_id`: FK a cost_categories
- `descripcion`: Descripción del movimiento
- `monto`: Monto del movimiento
- `proveedor`: Proveedor
- `documento`: Tipo de documento
- `numero_documento`: Número del documento
- `estado`: pendiente, pagado, anulado
- `metodo_pago`: efectivo, transferencia, tarjeta, cheque
- `evidencias`: Array de URLs de documentos

## 🔍 Auditoría y Logs

### `audit_logs`
Auditoría completa de todas las acciones del sistema.

**Campos principales:**
- `usuario_id`: FK a profiles
- `accion`: Acción realizada
- `tabla_afectada`: Tabla modificada
- `registro_id`: ID del registro afectado
- `valores_anteriores`: JSONB con valores anteriores
- `valores_nuevos`: JSONB con valores nuevos
- `ip_address`: Dirección IP
- `user_agent`: User agent del navegador

### `import_logs`
Logs de importación de archivos CSV/Excel.

**Campos principales:**
- `usuario_id`: FK a profiles
- `archivo`: Nombre del archivo
- `tipo_archivo`: csv, excel, json
- `entidad`: Tabla de destino
- `registros_totales`: Total de registros
- `registros_exitosos`: Registros procesados exitosamente
- `registros_fallidos`: Registros con errores
- `errores`: JSONB con detalle de errores
- `estado`: processing, completed, failed

## ⚙️ Configuración

### `company_config`
Configuración de la empresa.

**Campos principales:**
- `nombre_empresa`: Nombre de la empresa
- `ruc`: RUC de la empresa
- `direccion`: Dirección
- `telefono`: Teléfono
- `email`: Email
- `moneda`: Moneda por defecto
- `idioma`: Idioma por defecto
- `zona_horaria`: Zona horaria
- `configuraciones`: JSONB con configuraciones adicionales

## 🔗 Relaciones Principales

```
profiles (1) ←→ (N) products
profiles (1) ←→ (N) guias
profiles (1) ←→ (N) costos
profiles (1) ←→ (1) user_preferences

categories (1) ←→ (N) products
categories (1) ←→ (N) categories (parent_id)

products (1) ←→ (N) kardex
products (1) ←→ (N) guia_items

guias (1) ←→ (N) guia_items
guias (1) ←→ (N) guia_movimientos
guias (1) ←→ (N) escaneos

pistoleo_sessions (1) ←→ (N) escaneos

cost_categories (1) ←→ (N) costos
cost_categories (1) ←→ (N) cost_categories (parent_id)
```

