@echo off
REM Script de Instalación Rápida - Lead Generator (Windows)

echo ========================================
echo 🚀 Lead Generator - Instalación Rápida
echo ========================================
echo.

REM Verificar Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker no está instalado.
    echo 📥 Descarga Docker Desktop desde: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Docker detectado

REM Verificar que Docker está corriendo
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker no está corriendo. Por favor, inicia Docker Desktop.
    pause
    exit /b 1
)

echo ✅ Docker está corriendo
echo.

REM Crear .env si no existe
if not exist .env (
    echo 📝 Creando archivo .env...
    if exist .env.template (
        copy .env.template .env
        echo ⚠️  IMPORTANTE: Edita el archivo .env con tus API keys antes de continuar
        echo.
        pause
    ) else (
        echo ❌ No se encontró .env.template
        pause
        exit /b 1
    )
) else (
    echo ✅ Archivo .env ya existe
)

REM Crear directorio output
if not exist output mkdir output
echo ✅ Directorio output\ creado

REM Construir imagen Docker
echo.
echo 🔨 Construyendo imagen Docker (esto puede tardar 2-3 minutos)...
docker-compose build

if errorlevel 1 (
    echo ❌ Error al construir la imagen Docker
    pause
    exit /b 1
)

echo ✅ Imagen construida correctamente

REM Levantar contenedor
echo.
echo 🚀 Levantando contenedor...
docker-compose up -d

if errorlevel 1 (
    echo ❌ Error al levantar el contenedor
    pause
    exit /b 1
)

echo ✅ Contenedor levantado correctamente
echo.
echo ========================================
echo ✅ ¡Instalación completada!
echo.
echo 🌐 Accede a N8N en: http://localhost:5678
echo 👤 Usuario: admin
echo 🔑 Contraseña: (revisa docker-compose.yml)
echo.
echo 📚 Próximos pasos:
echo    1. Accede a http://localhost:5678
echo    2. Importa el workflow desde: workflows\n8n_pipeline_workflow.json
echo    3. Configura Google Sheets credentials (opcional)
echo    4. ¡Ejecuta tu primer workflow!
echo.
echo 📖 Documentación completa: directives\DOCKER_SETUP.md
echo 🐛 Ver logs: docker logs n8n-lead-generator
echo 🛑 Detener: docker-compose down
echo ========================================
echo.
pause
