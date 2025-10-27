# Seguridad de la Base de Datos GDE

## 🔐 Row Level Security (RLS)

### Concepto
Row Level Security es una característica de PostgreSQL que permite controlar el acceso a nivel de fila. En GDE, todas las tablas tienen RLS habilitado para garantizar que los usuarios solo puedan acceder a los datos que tienen permisos para ver.

### Tablas con RLS Habilitado
```sql
-- Todas las tablas principales tienen RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE guias ENABLE ROW LEVEL SECURITY;
ALTER TABLE guia_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE guia_movimientos ENABLE ROW LEVEL SECURITY;
ALTER TABLE pistoleo_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE escaneos ENABLE ROW LEVEL SECURITY;
ALTER TABLE costos ENABLE ROW LEVEL SECURITY;
ALTER TABLE cost_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE import_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE company_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;
```

## 👥 Roles y Permisos

### Estructura de Roles

#### 1. **Admin**
- **Acceso**: Completo a todas las funcionalidades
- **Permisos**: 
  - Crear, leer, actualizar, eliminar en todas las tablas
  - Gestión de usuarios y roles
  - Configuración del sistema
  - Acceso a logs de auditoría

#### 2. **Contable**
- **Acceso**: Módulos financieros y de inventario
- **Permisos**:
  - Gestión completa de productos e inventario
  - Gestión de guías de despacho
  - Gestión de costos y movimientos contables
  - Acceso a reportes financieros
  - No puede gestionar usuarios ni configuración del sistema

#### 3. **Programador**
- **Acceso**: Funcionalidades técnicas
- **Permisos**:
  - Lectura de datos para desarrollo
  - Acceso a logs técnicos
  - Configuraciones técnicas
  - No puede modificar datos de negocio

## 🛡️ Políticas de Seguridad

### Políticas para Profiles
```sql
-- Todos pueden ver perfiles
CREATE POLICY "Users can view all profiles" ON profiles 
FOR SELECT USING (true);

-- Solo pueden actualizar su propio perfil
CREATE POLICY "Users can update own profile" ON profiles 
FOR UPDATE USING (auth.uid() = id);
```

### Políticas para Products
```sql
-- Admin tiene acceso completo
CREATE POLICY "Admin full access to products" ON products 
FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin')
);

-- Contable puede ver productos
CREATE POLICY "Contable can view products" ON products 
FOR SELECT USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role IN ('admin', 'contable'))
);
```

### Políticas para Guías
```sql
-- Admin acceso completo
CREATE POLICY "Admin full access to guias" ON guias 
FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin')
);

-- Contable puede gestionar guías
CREATE POLICY "Contable can manage guias" ON guias 
FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role IN ('admin', 'contable'))
);
```

### Políticas para Costos
```sql
-- Admin acceso completo
CREATE POLICY "Admin full access to costos" ON costos 
FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin')
);

-- Contable puede gestionar costos
CREATE POLICY "Contable can manage costos" ON costos 
FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role IN ('admin', 'contable'))
);
```

### Políticas para User Preferences
```sql
-- Solo pueden gestionar sus propias preferencias
CREATE POLICY "Users can manage own preferences" ON user_preferences 
FOR ALL USING (auth.uid() = user_id);
```

## 🔑 Autenticación

### Supabase Auth Integration
- **Proveedor**: Supabase Authentication
- **Métodos**: Email/Password, OAuth (Google, GitHub)
- **Sesiones**: JWT tokens con expiración
- **Refresh**: Tokens de renovación automática

### Flujo de Autenticación
1. Usuario se autentica con Supabase Auth
2. Se obtiene JWT token con `auth.uid()`
3. RLS usa `auth.uid()` para determinar permisos
4. Políticas verifican rol del usuario en `profiles`

## 📊 Auditoría de Seguridad

### Audit Logs
Todas las acciones importantes se registran en `audit_logs`:

```sql
-- Ejemplo de registro de auditoría
INSERT INTO audit_logs (
    usuario_id, accion, tabla_afectada, registro_id,
    valores_anteriores, valores_nuevos, ip_address
) VALUES (
    auth.uid(), 'UPDATE', 'products', 123,
    '{"stock_actual": 50}', '{"stock_actual": 45}',
    '192.168.1.100'
);
```

### Campos de Auditoría
- **usuario_id**: Quién realizó la acción
- **accion**: Tipo de acción (INSERT, UPDATE, DELETE)
- **tabla_afectada**: Tabla modificada
- **registro_id**: ID del registro afectado
- **valores_anteriores**: Estado anterior (JSONB)
- **valores_nuevos**: Estado nuevo (JSONB)
- **ip_address**: Dirección IP del usuario
- **user_agent**: Información del navegador

## 🔒 Buenas Prácticas de Seguridad

### 1. Validación de Datos
- Usar Pydantic schemas en el backend
- Validar todos los inputs en el frontend
- Sanitizar datos antes de insertar en BD

### 2. Manejo de Errores
- No exponer información sensible en errores
- Logs detallados solo en servidor
- Mensajes de error genéricos para usuarios

### 3. Conexiones Seguras
- Usar HTTPS en producción
- Conexiones encriptadas a la base de datos
- Variables de entorno para credenciales

### 4. Backup y Recuperación
- Backups automáticos diarios
- Pruebas de recuperación regulares
- Versionado de esquemas de BD

## 🚨 Incidentes de Seguridad

### Procedimiento de Respuesta
1. **Detección**: Monitoreo de logs de auditoría
2. **Contención**: Bloqueo temporal de usuarios sospechosos
3. **Análisis**: Revisión de logs y actividades
4. **Recuperación**: Restauración desde backups si es necesario
5. **Mejora**: Actualización de políticas de seguridad

### Alertas Automáticas
- Múltiples intentos de login fallidos
- Acceso desde IPs no reconocidas
- Modificaciones masivas de datos
- Acceso fuera del horario laboral

## 📋 Checklist de Seguridad

### Configuración Inicial
- [ ] RLS habilitado en todas las tablas
- [ ] Políticas de seguridad implementadas
- [ ] Roles y permisos configurados
- [ ] Auditoría habilitada
- [ ] Conexiones encriptadas

### Mantenimiento Regular
- [ ] Revisión de logs de auditoría
- [ ] Actualización de políticas
- [ ] Rotación de credenciales
- [ ] Pruebas de penetración
- [ ] Backup de seguridad

### Monitoreo Continuo
- [ ] Alertas de seguridad configuradas
- [ ] Monitoreo de accesos anómalos
- [ ] Revisión de permisos de usuarios
- [ ] Actualización de dependencias
- [ ] Análisis de vulnerabilidades
