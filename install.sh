#!/bin/bash

# Script de Instalación Rápida - Lead Generator
# Compatible con Mac, Linux y Git Bash en Windows

echo "🚀 Lead Generator - Instalación Rápida"
echo "========================================"
echo ""

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado."
    echo "📥 Descarga Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✅ Docker detectado"

# Verificar que Docker está corriendo
if ! docker info &> /dev/null; then
    echo "❌ Docker no está corriendo. Por favor, inicia Docker Desktop."
    exit 1
fi

echo "✅ Docker está corriendo"
echo ""

# Crear .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    if [ -f .env.template ]; then
        cp .env.template .env
        echo "⚠️  IMPORTANTE: Edita el archivo .env con tus API keys antes de continuar"
        echo ""
        read -p "Presiona Enter cuando hayas configurado .env..."
    else
        echo "❌ No se encontró .env.template"
        exit 1
    fi
else
    echo "✅ Archivo .env ya existe"
fi

# Crear directorio output
mkdir -p output
echo "✅ Directorio output/ creado"

# Construir imagen Docker
echo ""
echo "🔨 Construyendo imagen Docker (esto puede tardar 2-3 minutos)..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Error al construir la imagen Docker"
    exit 1
fi

echo "✅ Imagen construida correctamente"

# Levantar contenedor
echo ""
echo "🚀 Levantando contenedor..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Error al levantar el contenedor"
    exit 1
fi

echo "✅ Contenedor levantado correctamente"
echo ""
echo "========================================"
echo "✅ ¡Instalación completada!"
echo ""
echo "🌐 Accede a N8N en: http://localhost:5678"
echo "👤 Usuario: admin"
echo "🔑 Contraseña: (revisa docker-compose.yml)"
echo ""
echo "📚 Próximos pasos:"
echo "   1. Accede a http://localhost:5678"
echo "   2. Importa el workflow desde: workflows/n8n_pipeline_workflow.json"
echo "   3. Configura Google Sheets credentials (opcional)"
echo "   4. ¡Ejecuta tu primer workflow!"
echo ""
echo "📖 Documentación completa: directives/DOCKER_SETUP.md"
echo "🐛 Ver logs: docker logs n8n-lead-generator"
echo "🛑 Detener: docker-compose down"
echo "========================================"
