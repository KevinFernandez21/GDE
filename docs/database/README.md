# Base de Datos GDE - Documentación

## 📋 Resumen General

La base de datos GDE está diseñada para gestionar un sistema completo de inventario, guías de despacho, pistoleo en tiempo real y contabilidad. Utiliza PostgreSQL como motor de base de datos a través de Supabase.

## 🏗️ Arquitectura de la Base de Datos

### Tecnologías Utilizadas
- **Motor de BD**: PostgreSQL 15+
- **Hosting**: Supabase
- **Seguridad**: Row Level Security (RLS)
- **Autenticación**: Supabase Auth

## 📊 Entidades Principales

### 1. Gestión de Usuarios
- **`profiles`**: Perfiles de usuario que extienden auth.users
- **`roles`**: Roles y permisos del sistema
- **`user_preferences`**: Configuraciones personales de usuarios

### 2. Inventario y Productos
- **`categories`**: Categorías jerárquicas de productos
- **`products`**: Catálogo completo de productos con stock
- **`kardex`**: Registro cronológico de movimientos de inventario

### 3. Gestión Documental
- **`guias`**: Guías de despacho con seguimiento
- **`guia_items`**: Items específicos en cada guía
- **`guia_movimientos`**: Historial de ubicaciones y estados

### 4. Pistoleo en Tiempo Real
- **`pistoleo_sessions`**: Sesiones de escaneo activas
- **`escaneos`**: Registro individual de cada escaneo

### 5. Contabilidad
- **`cost_categories`**: Categorías contables jerárquicas
- **`costos`**: Movimientos monetarios y gastos

### 6. Auditoría y Logs
- **`audit_logs`**: Auditoría completa del sistema
- **`import_logs`**: Logs de importación de archivos

### 7. Configuración
- **`company_config`**: Configuración de la empresa
- **`user_preferences`**: Preferencias de usuario

## 🔐 Seguridad y Permisos

### Row Level Security (RLS)
Todas las tablas tienen RLS habilitado con políticas específicas:

- **Admin**: Acceso completo a todas las funcionalidades
- **Contable**: Acceso a módulos financieros y de inventario
- **Programador**: Acceso técnico y de configuración

### Políticas de Acceso
```sql
-- Ejemplo: Política para productos
CREATE POLICY "Admin full access to products" ON products FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin')
);
```

## 📈 Optimizaciones

### Índices Creados
- Índices en campos de búsqueda frecuente (códigos, fechas)
- Índices compuestos para consultas complejas
- Índices parciales para optimizar consultas específicas

### Triggers Automáticos
- **`update_updated_at_column()`**: Actualiza automáticamente timestamps
- **`registrar_kardex()`**: Registra movimientos en kardex automáticamente

## 🔄 Flujos de Datos

### 1. Gestión de Inventario
```
Producto → Kardex → Stock Actualizado
```

### 2. Proceso de Guías
```
Guía → Items → Movimientos → Estado Final
```

### 3. Pistoleo
```
Sesión → Escaneos → Validación → Actualización
```

## 📋 Datos Iniciales

### Roles Predefinidos
- **admin**: Acceso total al sistema
- **contable**: Acceso a módulos financieros
- **programador**: Acceso técnico

### Categorías de Ejemplo
- Electrónicos, Ropa, Alimentos, Hogar, Oficina

### Configuración de Empresa
- Datos básicos de la empresa GDE System

## 🚀 Próximos Pasos

1. Configurar conexión a Supabase
2. Ejecutar scripts de creación de tablas
3. Configurar políticas RLS
4. Insertar datos iniciales
5. Configurar triggers y funciones

## 📚 Archivos Relacionados

- `base_datos.md`: Scripts SQL completos
- `docs/api/`: Documentación de endpoints
- `docs/deployment/`: Guías de despliegue
