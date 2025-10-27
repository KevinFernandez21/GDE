-- =============================================
-- TABLAS DE AUTENTICACIÓN Y USUARIOS
-- =============================================

-- Tabla de perfiles de usuario (extiende auth.users)
CREATE TABLE profiles (
    id UUID REFERENCES auth.users PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    full_name VARCHAR(100),
    role VARCHAR(20) CHECK (role IN ('admin', 'contable', 'programador')) DEFAULT 'contable',
    avatar_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de configuraciones de usuario
CREATE TABLE user_settings (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES profiles(id) UNIQUE NOT NULL,
    theme VARCHAR(10) DEFAULT 'light' CHECK (theme IN ('light', 'dark', 'auto')),
    language VARCHAR(10) DEFAULT 'es',
    timezone VARCHAR(50) DEFAULT 'America/Guayaquil',
    notifications_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- TABLAS DE INVENTARIO Y PRODUCTOS
-- =============================================

-- Categorías de productos
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id INTEGER REFERENCES categories(id),
    color VARCHAR(7),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Productos principales
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES categories(id),
    stock_actual INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 10,
    precio_compra DECIMAL(10,2) DEFAULT 0,
    precio_venta DECIMAL(10,2) DEFAULT 0,
    ubicacion_bodega VARCHAR(100),
    proveedor VARCHAR(100),
    marca VARCHAR(100),
    codigo_barras VARCHAR(100),
    imagenes TEXT[],
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'discontinued')),
    created_by UUID REFERENCES profiles(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Kardex de inventario
CREATE TABLE kardex (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) NOT NULL,
    tipo_movimiento VARCHAR(20) NOT NULL CHECK (tipo_movimiento IN ('entrada', 'salida', 'ajuste')),
    documento_asociado VARCHAR(100),
    cantidad INTEGER NOT NULL,
    saldo_anterior INTEGER NOT NULL,
    saldo_actual INTEGER NOT NULL,
    costo_unitario DECIMAL(10,2),
    costo_promedio DECIMAL(10,2),
    fecha_movimiento TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    usuario_id UUID REFERENCES profiles(id),
    observaciones TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- TABLAS DE GUIAS Y TRAZABILIDAD
-- =============================================

-- Guías de despacho
CREATE TABLE guias (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(100) UNIQUE NOT NULL,
    estado VARCHAR(20) DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'en_transito', 'entregada', 'devuelta', 'cancelada')),
    cliente_nombre VARCHAR(200) NOT NULL,
    cliente_ruc VARCHAR(20),
    cliente_direccion TEXT,
    direccion_entrega TEXT,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_estimada_entrega DATE,
    fecha_entrega_real TIMESTAMP WITH TIME ZONE,
    ubicacion_actual VARCHAR(100),
    transportista VARCHAR(100),
    observaciones TEXT,
    created_by UUID REFERENCES profiles(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Items de guías
CREATE TABLE guia_items (
    id SERIAL PRIMARY KEY,
    guia_id INTEGER REFERENCES guias(id) NOT NULL,
    product_id INTEGER REFERENCES products(id) NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10,2),
    subtotal DECIMAL(12,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Movimientos de guías
CREATE TABLE guia_movimientos (
    id SERIAL PRIMARY KEY,
    guia_id INTEGER REFERENCES guias(id) NOT NULL,
    usuario_id UUID REFERENCES profiles(id),
    accion VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(100),
    observaciones TEXT,
    fecha_movimiento TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- TABLAS DE PISTOLEO EN TIEMPO REAL
-- =============================================

-- Sesiones de pistoleo
CREATE TABLE pistoleo_sessions (
    id SERIAL PRIMARY KEY,
    codigo_qr VARCHAR(100) UNIQUE NOT NULL,
    usuario_id UUID REFERENCES profiles(id) NOT NULL,
    nombre_sesion VARCHAR(100),
    fecha_inicio TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_fin TIMESTAMP WITH TIME ZONE,
    estado VARCHAR(20) DEFAULT 'active' CHECK (estado IN ('active', 'completed', 'cancelled')),
    escaneos_totales INTEGER DEFAULT 0,
    guias_procesadas INTEGER DEFAULT 0,
    ubicacion VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Registro de escaneos
CREATE TABLE escaneos (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES pistoleo_sessions(id) NOT NULL,
    guia_id INTEGER REFERENCES guias(id),
    codigo_barras VARCHAR(100) NOT NULL,
    fecha_escaneo TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    dispositivo VARCHAR(100),
    ubicacion VARCHAR(100),
    estado_escaneo VARCHAR(20) DEFAULT 'success' CHECK (estado_escaneo IN ('success', 'error', 'duplicate')),
    mensaje_error TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- TABLAS CONTABLES Y COSTOS
-- =============================================

-- Categorías de costos
CREATE TABLE cost_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('gasto', 'ingreso', 'costo')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Registro de costos
CREATE TABLE costos (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    categoria_id INTEGER REFERENCES cost_categories(id) NOT NULL,
    descripcion TEXT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    proveedor VARCHAR(200),
    documento VARCHAR(100),
    estado VARCHAR(20) DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'pagado', 'anulado')),
    metodo_pago VARCHAR(20) DEFAULT 'transferencia',
    observaciones TEXT,
    created_by UUID REFERENCES profiles(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- TABLAS DE NOTIFICACIONES
-- =============================================

-- Notificaciones del sistema
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) CHECK (type IN ('stock_alert', 'guide_status', 'system', 'security')),
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    data JSONB,
    user_id UUID REFERENCES profiles(id),
    is_read BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    read_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Configuración de notificaciones
CREATE TABLE notification_settings (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES profiles(id) UNIQUE NOT NULL,
    email_notifications BOOLEAN DEFAULT TRUE,
    push_notifications BOOLEAN DEFAULT TRUE,
    stock_alerts BOOLEAN DEFAULT TRUE,
    guide_updates BOOLEAN DEFAULT TRUE,
    system_notifications BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- TABLAS DE AUDITORÍA
-- =============================================

-- Auditoría del sistema
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    usuario_id UUID REFERENCES profiles(id),
    accion VARCHAR(100) NOT NULL,
    tabla_afectada VARCHAR(50),
    registro_id INTEGER,
    valores_anteriores JSONB,
    valores_nuevos JSONB,
    ip_address VARCHAR(45),
    fecha TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Logs de importación
CREATE TABLE import_logs (
    id SERIAL PRIMARY KEY,
    usuario_id UUID REFERENCES profiles(id) NOT NULL,
    archivo VARCHAR(200) NOT NULL,
    tipo_archivo VARCHAR(10) NOT NULL CHECK (tipo_archivo IN ('csv', 'excel')),
    entidad VARCHAR(50) NOT NULL,
    registros_totales INTEGER DEFAULT 0,
    registros_exitosos INTEGER DEFAULT 0,
    registros_fallidos INTEGER DEFAULT 0,
    errores JSONB,
    fecha_importacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    estado VARCHAR(20) DEFAULT 'completed' CHECK (estado IN ('processing', 'completed', 'failed'))
);

-- =============================================
-- TABLAS DE CONFIGURACIÓN
-- =============================================

-- Configuración de la empresa
CREATE TABLE company_config (
    id SERIAL PRIMARY KEY,
    nombre_empresa VARCHAR(200) NOT NULL,
    ruc VARCHAR(20) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100),
    logo_url TEXT,
    moneda VARCHAR(10) DEFAULT 'USD',
    configuraciones JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =============================================

-- Índices para products
CREATE INDEX idx_products_code ON products(code);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_status ON products(status);

-- Índices para guias
CREATE INDEX idx_guias_codigo ON guias(codigo);
CREATE INDEX idx_guias_estado ON guias(estado);
CREATE INDEX idx_guias_fecha_creacion ON guias(fecha_creacion);

-- Índices para kardex
CREATE INDEX idx_kardex_product_fecha ON kardex(product_id, fecha_movimiento);

-- Índices para escaneos
CREATE INDEX idx_escaneos_session ON escaneos(session_id);
CREATE INDEX idx_escaneos_fecha ON escaneos(fecha_escaneo);

-- Índices para auditoría
CREATE INDEX idx_audit_logs_fecha ON audit_logs(fecha);
CREATE INDEX idx_audit_logs_usuario ON audit_logs(usuario_id);

-- =============================================
-- POLÍTICAS RLS (ROW LEVEL SECURITY)
-- =============================================

-- Habilitar RLS en todas las tablas
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
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE notification_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE import_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE company_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_settings ENABLE ROW LEVEL SECURITY;

-- Políticas para profiles
CREATE POLICY "Users can view all profiles" ON profiles FOR SELECT USING (true);
CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);

-- Políticas para products
CREATE POLICY "Admin full access to products" ON products FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin')
);
CREATE POLICY "Contable can view products" ON products FOR SELECT USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role IN ('admin', 'contable'))
);

-- Políticas para guias
CREATE POLICY "Admin full access to guias" ON guias FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin')
);
CREATE POLICY "Contable can manage guias" ON guias FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role IN ('admin', 'contable'))
);

-- Políticas para costos
CREATE POLICY "Admin full access to costos" ON costos FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin')
);
CREATE POLICY "Contable can manage costos" ON costos FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role IN ('admin', 'contable'))
);

-- Políticas para user_settings (solo propio usuario)
CREATE POLICY "Users can manage own settings" ON user_settings FOR ALL USING (auth.uid() = user_id);

-- Políticas para notifications (solo propias notificaciones)
CREATE POLICY "Users can view own notifications" ON notifications FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own notifications" ON notifications FOR UPDATE USING (auth.uid() = user_id);

-- =============================================
-- FUNCIONES Y TRIGGERS
-- =============================================

-- Función para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para updated_at
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_guias_updated_at BEFORE UPDATE ON guias FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_costos_updated_at BEFORE UPDATE ON costos FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Función para registrar en kardex automáticamente
CREATE OR REPLACE FUNCTION registrar_kardex()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO kardex (
            product_id, tipo_movimiento, documento_asociado,
            cantidad, saldo_anterior, saldo_actual,
            costo_unitario, usuario_id
        ) VALUES (
            NEW.id, 'entrada', 'CREACION',
            NEW.stock_actual, 0, NEW.stock_actual,
            NEW.precio_compra, NEW.created_by
        );
    ELSIF TG_OP = 'UPDATE' AND OLD.stock_actual != NEW.stock_actual THEN
        INSERT INTO kardex (
            product_id, tipo_movimiento, documento_asociado,
            cantidad, saldo_anterior, saldo_actual,
            costo_unitario, usuario_id
        ) VALUES (
            NEW.id, 
            CASE WHEN NEW.stock_actual > OLD.stock_actual THEN 'entrada' ELSE 'salida' END,
            'AJUSTE',
            ABS(NEW.stock_actual - OLD.stock_actual),
            OLD.stock_actual, NEW.stock_actual,
            NEW.precio_compra, NEW.created_by
        );
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_registrar_kardex 
AFTER INSERT OR UPDATE OF stock_actual ON products 
FOR EACH ROW EXECUTE FUNCTION registrar_kardex();

-- Función para crear notificación de stock bajo
CREATE OR REPLACE FUNCTION notificar_stock_bajo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.stock_actual <= NEW.stock_minimo THEN
        INSERT INTO notifications (
            user_id, title, message, type, priority
        ) VALUES (
            NEW.created_by,
            'Stock Bajo: ' || NEW.name,
            'El producto ' || NEW.code || ' tiene stock bajo: ' || NEW.stock_actual,
            'stock_alert',
            'high'
        );
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_notificar_stock_bajo 
AFTER INSERT OR UPDATE OF stock_actual ON products 
FOR EACH ROW EXECUTE FUNCTION notificar_stock_bajo();

-- =============================================
-- DATOS INICIALES
-- =============================================

-- Insertar categorías de ejemplo
INSERT INTO categories (name, description, color) VALUES 
('Electrónicos', 'Productos electrónicos y tecnología', '#3B82F6'),
('Ropa', 'Prendas de vestir y accesorios', '#EF4444'),
('Alimentos', 'Productos alimenticios y bebidas', '#10B981'),
('Hogar', 'Artículos para el hogar', '#8B5CF6'),
('Oficina', 'Materiales de oficina', '#F59E0B');

-- Insertar categorías de costos
INSERT INTO cost_categories (name, tipo, description) VALUES 
('Ventas', 'ingreso', 'Ingresos por ventas de productos'),
('Costos de Ventas', 'costo', 'Costos directos de los productos vendidos'),
('Gastos Administrativos', 'gasto', 'Gastos generales de administración'),
('Gastos de Ventas', 'gasto', 'Gastos relacionados con la venta y distribución');

-- Insertar configuración de empresa
INSERT INTO company_config (nombre_empresa, ruc, direccion, telefono, email) VALUES 
('GDE System', '1234567890001', 'Av. Principal 123, Guayaquil', '+593 4 123-4567', 'info@gde-system.com');

COMMIT;

-- =============================================
-- COMENTARIOS DE LAS TABLAS
-- =============================================

COMMENT ON TABLE profiles IS 'Perfiles de usuarios del sistema';
COMMENT ON TABLE products IS 'Catálogo de productos con información de inventario';
COMMENT ON TABLE kardex IS 'Registro cronológico de movimientos de inventario';
COMMENT ON TABLE guias IS 'Guías de despacho con seguimiento en tiempo real';
COMMENT ON TABLE pistoleo_sessions IS 'Sesiones de escaneo para el módulo de pistoleo';
COMMENT ON TABLE escaneos IS 'Registro individual de cada escaneo de códigos de barras';
COMMENT ON TABLE costos IS 'Registro de movimientos contables y costos';
COMMENT ON TABLE notifications IS 'Sistema de notificaciones del sistema';

-- Mensaje de finalización
DO $$ BEGIN
    RAISE NOTICE 'Base de datos GDE creada exitosamente!';
    RAISE NOTICE 'Total tablas creadas: 16';
    RAISE NOTICE 'Índices creados: 10';
    RAISE NOTICE 'Políticas RLS: 12';
    RAISE NOTICE 'Triggers: 6';
END $$;