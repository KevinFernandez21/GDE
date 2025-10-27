GDE - Stack Tecnológico (Solo Frontend + Backend)
🏗️ Arquitectura Simplificada
Frontend (Next.js 14 + TypeScript)
text
gde-frontend/
├── app/                    # App Router
├── components/            # Componentes UI
├── lib/                  # Configuración, Supabase client, utils
├── types/               # Tipos TypeScript
└── hooks/               # Custom hooks
Backend (FastAPI + Python)
text
gde-backend/
├── app/
│   ├── api/             # Endpoints REST
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Lógica de negocio
│   └── core/           # Configuración
└── requirements.txt
🎯 Entidades Principales
Gestión de Usuarios
User - Perfiles de usuario

Role - Roles (admin, contable, programador)

Inventario
Product - Productos con stock

Category - Categorías

Kardex - Movimientos de inventario

Gestión Documental
Guide - Guías de despacho

GuideItem - Items en guías

GuideMovement - Historial

Pistoleo
PistoleoSession - Sesiones de escaneo

Scan - Registro de escaneos

Contabilidad
Cost - Costos y gastos

CostCategory - Categorías contables

Notificaciones
Notification - Notificaciones del sistema

NotificationSetting - Configuraciones

Auditoría
AuditLog - Logs de auditoría

ImportLog - Logs de importación

🔧 División de Funcionalidades
🖥️ Frontend (Next.js) - Responsabilidades:
text
✅ Interfaz de usuario completa
✅ Dashboard en tiempo real
✅ Gestión de formularios (React Hook Form + Zod)
✅ Tablas y listados (TanStack Table)
✅ Gráficos y reportes (Recharts)
✅ Generación de QR codes
✅ Escaneo de códigos con cámara (jsQR)
✅ Notificaciones en UI (react-hot-toast)
✅ PWA para funcionalidad móvil
✅ Conexión directa a Supabase (consultas simples)
✅ Estado global (Zustand)
✅ Autenticación (Supabase Auth)
🐍 Backend (FastAPI) - Responsabilidades:
text
✅ Procesamiento de archivos Excel/CSV (pandas)
✅ Cálculos contables complejos
✅ Procesamiento de imágenes (OpenCV + pyzbar)
✅ Generación de reportes financieros
✅ Servicio de notificaciones
✅ Validaciones de negocio complejas
✅ Tareas programadas (alertas de stock)
✅ Integraciones externas
✅ Procesamiento por lotes
✅ Cálculo de promedios ponderados
🔄 Flujos de Comunicación
Frontend → Supabase (Directo):
Consultas simples de datos

Autenticación de usuarios

Operaciones CRUD básicas

Suscripciones en tiempo real

Storage de archivos

Frontend → Backend (API Calls):
text
📁 Subida de archivos Excel/CSV
🧮 Cálculos contables complejos
📊 Generación de reportes financieros
🖼️ Procesamiento avanzado de imágenes
🔔 Gestión de notificaciones
📈 Agregaciones de datos pesadas
🛠️ Stack Tecnológico
Frontend:
Framework: Next.js 14 (App Router)

Lenguaje: TypeScript

Estilos: Tailwind CSS + Shadcn/ui

Estado: Zustand

Fetching: TanStack Query

Forms: React Hook Form + Zod

Tablas: TanStack Table

Gráficos: Recharts

Notificaciones: react-hot-toast

QR: qrcode

Escaneo Cámara: jsQR

PWA: next-pwa

DB Client: @supabase/supabase-js

Backend:
Framework: FastAPI

Lenguaje: Python 3.11+

ORM: SQLAlchemy 2.0 + asyncpg

DB: PostgreSQL (Supabase)

Validación: Pydantic v2

Archivos: python-multipart

Procesamiento:

pandas + openpyxl (CSV/Excel)

opencv-python + pyzbar (imágenes)

ultralytics (YOLO - opcional)

Notificaciones: pywebpush

Auth: python-jose + bcrypt

Infraestructura:
Base de datos: Supabase

Hosting Frontend: Vercel

Hosting Backend: Railway/Render

Storage: Supabase Storage

Auth: Supabase Authentication

