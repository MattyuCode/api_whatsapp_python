@echo off
cd /d "%~dp0"
REM WhatsApp Group Inviter - Instalador Automático con Python 3.13.5

REM Versión 2.1 Mejorada

:: Configuración
set APP_NAME=WhatsApp Group Inviter
set PYTHON_VERSION=3.13.5
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe
set PYTHON_INSTALLER=python_installer.exe

:: Verificar permisos de administrador
net session >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Ejecuta como administrador
    echo Haz clic derecho -> "Ejecutar como administrador"
    echo.
    pause
    exit /b 1
)

:: Encabezado
echo ****************************************
echo %APP_NAME% - Instalador Automático
echo Python %PYTHON_VERSION%
echo ****************************************
echo.

:: Paso 1: Verificar Python
echo [1/3] Verificando Python...
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Python ya está instalado.
    goto INSTALL_DEPS
)

:: Paso 2: Instalar Python
echo [2/3] Instalando Python %PYTHON_VERSION%...
echo Descargando instalador...
curl -o %PYTHON_INSTALLER% %PYTHON_URL% --silent
if not exist %PYTHON_INSTALLER% (
    echo Error al descargar Python.
    pause
    exit /b 1
)

echo Instalando (espere unos minutos)...
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_launcher=1
del %PYTHON_INSTALLER%

:: Verificar instalación
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Instalación de Python falló.
    echo Instala manualmente desde:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

:INSTALL_DEPS
:: Paso 3: Instalar dependencias directamente
echo [3/3] Instalando dependencias...
echo Actualizando pip...
python -m pip install --upgrade pip --quiet

echo Instalando Flask y Selenium...
pip install flask==3.0.2 selenium==4.21.0 --quiet

:: Validar existencia de main.py
if not exist main.py (
    echo ERROR: No se encontró el archivo main.py
    pause
    exit /b 1
)

:: Paso 4: Iniciar aplicación
echo.
echo Instalación completada!
echo Iniciando la aplicación...
start http://127.0.0.1:5000
start python main.py

echo.
echo Aplicación ejecutándose en:
echo http://127.0.0.1:5000
echo.
pause
