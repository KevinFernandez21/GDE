#!/bin/bash

# Script para configurar el entorno del backend GDE

echo "🚀 Configurando GDE Backend..."

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cp env.example .env
    echo "✅ Archivo .env creado"
    echo "⚠️  IMPORTANTE: Revisa y actualiza las credenciales en .env"
else
    echo "✅ Archivo .env ya existe"
fi

# Crear directorio de uploads si no existe
if [ ! -d uploads ]; then
    echo "📁 Creando directorio uploads..."
    mkdir -p uploads
    echo "✅ Directorio uploads creado"
fi

# Crear directorio de logs si no existe
if [ ! -d logs ]; then
    echo "📁 Creando directorio logs..."
    mkdir -p logs
    echo "✅ Directorio logs creado"
fi

echo ""
echo "✨ Configuración completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Revisa el archivo .env y actualiza las credenciales"
echo "2. Instala las dependencias: pip install -r requirements.txt"
echo "3. Ejecuta el servidor: python -m app.main"
echo "   O usa: uvicorn app.main:app --reload"
echo ""


