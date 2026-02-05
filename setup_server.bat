@echo off
REM Quick Deployment Script for Buscador-Rate-Leads (Windows)
REM This script helps you set up the project on your Windows server

echo ================================================================
echo 🚀 Buscador Rate Leads - Quick Setup Script (Windows)
echo ================================================================
echo.

REM Check Python
echo 📋 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.10 or higher.
    echo Download from: https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ %PYTHON_VERSION% found
echo.

REM Get project directory
set PROJECT_DIR=%~dp0
echo 📂 Project directory: %PROJECT_DIR%
echo.

REM Create virtual environment
echo 🔧 Creating virtual environment...
if not exist "%PROJECT_DIR%venv" (
    python -m venv "%PROJECT_DIR%venv"
    echo ✅ Virtual environment created
) else (
    echo ⚠️  Virtual environment already exists, skipping...
)
echo.

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call "%PROJECT_DIR%venv\Scripts\activate.bat"
echo.

REM Install dependencies
echo 📦 Installing dependencies...
python -m pip install --upgrade pip -q
pip install -r "%PROJECT_DIR%execution\requirements.txt" -q
echo ✅ Dependencies installed
echo.

REM Setup .env file
if not exist "%PROJECT_DIR%.env" (
    echo 📝 Creating .env file...
    copy "%PROJECT_DIR%.env.template" "%PROJECT_DIR%.env"
    echo ⚠️  IMPORTANT: Edit .env file with your API keys:
    echo    notepad "%PROJECT_DIR%.env"
    echo.
) else (
    echo ✅ .env file already exists
    echo.
)

REM Test installation
echo 🧪 Testing installation...
echo Running a quick test (this may take a moment)...
echo.

python -c "import requests; import bs4; import google.auth; print('✅ All required modules are available')"

echo.
echo ================================================================
echo ✅ SETUP COMPLETE!
echo ================================================================
echo.
echo 📋 Next steps:
echo.
echo 1. Configure your API keys:
echo    notepad "%PROJECT_DIR%.env"
echo.
echo 2. Test the pipeline:
echo    cd %PROJECT_DIR%
echo    venv\Scripts\activate
echo    python execution\scrape_gmb_api.py --query "abogados en Vigo" --max-results 5 --format json
echo.
echo 3. Note your project path for n8n configuration:
echo    %PROJECT_DIR%
echo.
echo 4. Import the workflow in n8n:
echo    File: %PROJECT_DIR%workflows\n8n_simple_workflow.json
echo.
echo ================================================================
pause
