@echo off

rem =======================================================
rem === Script para iniciar la aplicacion de Python     ===
rem === Fetches, merge, instala dependencias y ejecuta  ===
rem =======================================================

rem -------------------------------------------------------
rem -- Paso 1: Actualizar el repositorio de Git          --
rem -------------------------------------------------------
echo.
echo Actualizando el repositorio...
git fetch
git merge origin/main

rem -------------------------------------------------------
rem -- Paso 2: Activar el entorno virtual                --
rem -------------------------------------------------------
echo.
echo Activando el entorno virtual...
rem La forma mas segura de activar el venv es con 'call' para que el script continue
call .venv\Scripts\activate.bat

rem -------------------------------------------------------
rem -- Paso 3: Instalar dependencias desde requirements.txt --
rem -------------------------------------------------------
echo.
echo Instalando dependencias desde requirements.txt...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ocurrio un error al instalar las dependencias.
    pause
    exit /b 1
) else (
    echo.
    echo Todas las dependencias se instalaron correctamente.
)

rem -------------------------------------------------------
rem -- Paso 4: Ejecutar la aplicacion principal          --
rem -------------------------------------------------------
echo.
echo Iniciando la aplicacion...
python main.py

echo.
echo Proceso finalizado.
pause