#!/bin/bash

# Script de solución rápida para el error de inicio del backend
# Uso: ./quick_fix.sh

set -e  # Salir si hay algún error

echo "🔧 GDE Backend - Script de Solución Rápida"
echo "=========================================="
echo ""

# Cambiar al directorio del script
cd "$(dirname "$0")"

# 1. Verificar Python
echo "1️⃣  Verificando Python..."
if ! command -v python &> /dev/null; then
    echo "❌ Python no encontrado. Por favor instala Python 3.11+"
    exit 1
fi

PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION encontrado"
echo ""

# 2. Verificar archivo .env
echo "2️⃣  Verificando archivo .env..."
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde env.example..."
    cp env.example .env
    echo "✅ Archivo .env creado"
    echo "⚠️  IMPORTANTE: Revisa y actualiza las credenciales en .env"
else
    echo "✅ Archivo .env existe"
fi
echo ""

# 3. Crear directorios necesarios
echo "3️⃣  Creando directorios necesarios..."
mkdir -p uploads logs
echo "✅ Directorios creados"
echo ""

# 4. Instalar dependencias
echo "4️⃣  Instalando dependencias..."
echo "   (Esto puede tomar varios minutos...)"

# Actualizar pip
python -m pip install --upgrade pip --quiet

# Instalar dependencias del requirements.txt
pip install -r requirements.txt --quiet

echo "✅ Dependencias instaladas"
echo ""

# 5. Verificar instalación
echo "5️⃣  Verificando instalación..."

# Verificar psycopg2
if python -c "import psycopg2" 2>/dev/null; then
    echo "✅ psycopg2 instalado correctamente"
else
    echo "❌ Error: psycopg2 no se instaló correctamente"
    echo "   Intenta: pip install psycopg2-binary"
    exit 1
fi

# Verificar configuración
if python -c "from app.core.config import settings; print('Config loaded')" 2>/dev/null; then
    echo "✅ Configuración cargada correctamente"
else
    echo "❌ Error al cargar la configuración"
    echo "   Verifica el archivo .env"
    exit 1
fi

# Verificar app
if python -c "from app.main import app; print('App loaded')" 2>/dev/null; then
    echo "✅ Aplicación cargada correctamente"
else
    echo "⚠️  Advertencia: Error al cargar la aplicación"
    echo "   Puede que haya problemas de conexión a la base de datos"
    echo "   Verifica las credenciales en .env"
fi

echo ""
echo "=========================================="
echo "✅ ¡Configuración completada!"
echo "=========================================="
echo ""
echo "🚀 Para iniciar el servidor, ejecuta uno de estos comandos:"
echo ""
echo "   Opción 1 (Recomendado):"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "   Opción 2:"
echo "   python -m app.main"
echo ""
echo "📝 Notas importantes:"
echo "   - Verifica las credenciales en el archivo .env"
echo "   - El servidor estará disponible en http://localhost:8000"
echo "   - La documentación API estará en http://localhost:8000/docs"
echo "   - Health check en http://localhost:8000/health"
echo ""


