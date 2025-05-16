@echo off
REM Script básico para ejecutar el Asistente Virtual de CASA DEL MUEBLE
REM Esta versión asume que ya has preparado todo el entorno

REM Activar entorno virtual si existe
if exist venv (
    call venv\Scripts\activate.bat
)

REM Ejecutar el asistente
echo Iniciando Asistente Virtual CASA DEL MUEBLE...
echo.
py main.py

REM Pausa para ver resultados
echo.
echo Presiona cualquier tecla para salir...
pause > nul
