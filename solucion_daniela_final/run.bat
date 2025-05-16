@echo off
REM Script para preparar y ejecutar el Asistente Virtual de CASA DEL MUEBLE
setlocal EnableDelayedExpansion

echo === Asistente Virtual CASA DEL MUEBLE - Iniciando... ===
echo.

REM Verificar si Python está instalado
py --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python no está instalado o no está en el PATH.
    echo Por favor instala Python 3.9+ y asegúrate que esté en el PATH.
    echo.
    pause
    exit /b 1
)
echo Python detectado correctamente.
echo.

REM 1. Verificar entorno virtual
echo Verificando entorno virtual...
if not exist venv (
    echo Creando entorno virtual...
    py -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)
echo Entorno virtual activado.
echo.

REM 2. Preparar la base de conocimientos
echo Preparando base de conocimientos...
py prepare_knowledge_base.py
if %ERRORLEVEL% NEQ 0 (
    echo Error al preparar la base de conocimientos.
    echo.
    pause
    exit /b 1
)
echo Base de conocimientos preparada.
echo.

REM 3. Ejecutar el indexador
echo Indexando base de conocimientos...
py indexer.py
if %ERRORLEVEL% NEQ 0 (
    echo Error al indexar la base de conocimientos.
    echo.
    pause
    exit /b 1
)
echo Indexacion completada.
echo.

REM 4. Iniciar el asistente
echo Iniciando el asistente virtual...
echo.
py main.py

REM 5. Pausa para ver resultados o errores
echo.
echo Presiona cualquier tecla para salir...
pause > nul
