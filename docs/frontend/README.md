# Frontend GDE - Next.js 14

## 📋 Resumen General

El frontend de GDE está construido con Next.js 14 utilizando el App Router, TypeScript y una arquitectura moderna de componentes. Se conecta directamente a Supabase para operaciones simples y al backend FastAPI para procesamiento complejo.

## 🏗️ Arquitectura

### Stack Tecnológico
- **Framework**: Next.js 14 (App Router)
- **Lenguaje**: TypeScript
- **Estilos**: Tailwind CSS + Shadcn/ui
- **Estado**: Zustand
- **Fetching**: TanStack Query
- **Forms**: React Hook Form + Zod
- **Tablas**: TanStack Table
- **Gráficos**: Recharts
- **Notificaciones**: react-hot-toast
- **QR**: qrcode
- **Escaneo**: jsQR
- **PWA**: next-pwa
- **DB Client**: @supabase/supabase-js

## 📁 Estructura de Carpetas

```
gde-frontend/
├── app/                    # App Router (Next.js 14)
│   ├── (auth)/            # Rutas de autenticación
│   ├── (dashboard)/       # Rutas del dashboard
│   ├── api/               # API routes (proxy al backend)
│   ├── globals.css        # Estilos globales
│   ├── layout.tsx         # Layout principal
│   └── page.tsx           # Página de inicio
├── components/            # Componentes UI reutilizables
│   ├── ui/               # Componentes base (Shadcn/ui)
│   ├── forms/            # Formularios específicos
│   ├── tables/           # Tablas con TanStack Table
│   ├── charts/           # Gráficos con Recharts
│   └── layout/           # Componentes de layout
├── lib/                  # Configuración y utilidades
│   ├── supabase.ts       # Cliente de Supabase
│   ├── utils.ts          # Utilidades generales
│   ├── validations.ts    # Esquemas de validación Zod
│   └── constants.ts      # Constantes de la aplicación
├── types/               # Tipos TypeScript
│   ├── database.ts      # Tipos de la base de datos
│   ├── api.ts           # Tipos de la API
│   └── common.ts        # Tipos comunes
├── hooks/               # Custom hooks
│   ├── useAuth.ts       # Hook de autenticación
│   ├── useProducts.ts   # Hook de productos
│   └── useGuias.ts      # Hook de guías
└── public/              # Archivos estáticos
    ├── icons/           # Iconos
    └── images/          # Imágenes
```

## 🎯 Funcionalidades Principales

### 1. Autenticación
- Login/Logout con Supabase Auth
- Protección de rutas
- Gestión de sesiones
- Roles y permisos

### 2. Dashboard
- Métricas en tiempo real
- Gráficos de inventario
- Estado de guías
- Notificaciones

### 3. Gestión de Inventario
- CRUD de productos
- Categorías jerárquicas
- Control de stock
- Historial de movimientos (Kardex)

### 4. Guías de Despacho
- Creación de guías
- Seguimiento en tiempo real
- Estados y transiciones
- Evidencias fotográficas

### 5. Pistoleo
- Escaneo de códigos QR/barras
- Sesiones de trabajo
- Validación en tiempo real
- Geolocalización

### 6. Contabilidad
- Registro de costos
- Categorías contables
- Reportes financieros
- Evidencias documentales

## 🔄 Flujos de Comunicación

### Frontend → Supabase (Directo)
- Consultas simples de datos
- Autenticación de usuarios
- Operaciones CRUD básicas
- Suscripciones en tiempo real
- Storage de archivos

### Frontend → Backend (API Calls)
- Subida de archivos Excel/CSV
- Cálculos contables complejos
- Generación de reportes financieros
- Procesamiento avanzado de imágenes
- Gestión de notificaciones
- Agregaciones de datos pesadas

## 🎨 Sistema de Diseño

### Shadcn/ui Components
- Componentes base consistentes
- Tema personalizable
- Accesibilidad integrada
- Responsive design

### Tailwind CSS
- Utility-first CSS
- Diseño responsive
- Tema claro/oscuro
- Animaciones suaves

### Iconos
- Lucide React para iconos
- Iconos personalizados en `/public/icons/`

## 📱 PWA (Progressive Web App)

### Características
- Instalable en dispositivos móviles
- Funcionalidad offline básica
- Notificaciones push
- Sincronización automática

### Configuración
- Service Worker automático
- Cache de recursos estáticos
- Estrategias de cache inteligentes

## 🔧 Configuración

### Variables de Entorno
```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_API_URL=your_backend_api_url
```

### Configuración de Supabase
```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

## 🚀 Desarrollo

### Comandos Principales
```bash
# Instalación
npm install

# Desarrollo
npm run dev

# Build
npm run build

# Producción
npm start

# Linting
npm run lint

# Type checking
npm run type-check
```

### Scripts Disponibles
- `dev`: Servidor de desarrollo
- `build`: Build de producción
- `start`: Servidor de producción
- `lint`: ESLint
- `type-check`: Verificación de tipos
- `test`: Tests unitarios

## 📊 Estado Global

### Zustand Store
```typescript
// stores/authStore.ts
interface AuthState {
  user: User | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
}
```

### TanStack Query
- Cache inteligente de datos
- Sincronización automática
- Optimistic updates
- Error handling

## 🔒 Seguridad

### Autenticación
- JWT tokens de Supabase
- Protección de rutas
- Roles y permisos
- Refresh automático

### Validación
- Zod schemas en frontend
- Validación en tiempo real
- Sanitización de inputs
- Error handling

## 📱 Responsive Design

### Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Componentes Adaptativos
- Tablas responsivas
- Navegación móvil
- Formularios optimizados
- Gráficos adaptativos

## 🧪 Testing

### Estrategia de Testing
- Unit tests con Jest
- Component tests con React Testing Library
- E2E tests con Playwright
- Visual regression tests

### Cobertura
- Mínimo 80% de cobertura
- Tests críticos de negocio
- Tests de integración
- Tests de accesibilidad

## 🚀 Despliegue

### Vercel (Recomendado)
- Deploy automático desde Git
- Preview deployments
- Edge functions
- Analytics integrado

### Configuración
- Variables de entorno
- Build optimizations
- CDN automático
- SSL/TLS

## 📚 Próximos Pasos

1. Configurar proyecto Next.js
2. Instalar dependencias
3. Configurar Supabase
4. Implementar autenticación
5. Crear componentes base
6. Implementar funcionalidades principales
7. Configurar PWA
8. Testing y optimización





