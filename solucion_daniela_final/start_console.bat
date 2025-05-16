@echo off
REM Este script simplemente abre una ventana de consola en la carpeta del proyecto
REM Útil cuando el script principal falla y se cierra inmediatamente

echo === Consola para el Asistente Virtual CASA DEL MUEBLE ===
echo.
echo Desde aquí puedes ejecutar comandos manualmente.
echo.
echo Comandos útiles:
echo - py main.py                          (Iniciar el asistente)
echo - py prepare_knowledge_base.py         (Preparar base de conocimientos)
echo - py indexer.py                       (Indexar documentos)
echo - py test_connection.py                (Probar conexión)
echo.

cmd /k "echo La consola permanecerá abierta. Para salir escribe 'exit'"
