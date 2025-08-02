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
rem -- Paso 3: Verificar e instalar pywin32 si es necesario --
rem -------------------------------------------------------
echo.
echo Verificando si "pywin32" esta instalado...
python -c "import win32com" >nul 2>&1

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo La libreria "pywin32" no se encontro. Instalando...
    pip install pywin32
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo "pywin32" se instalo correctamente.
    ) else (
        echo.
        echo Ocurrio un error al instalar "pywin32".
        pause
        exit /b 1
    )
) else (
    echo.
    echo "pywin32" ya esta instalado.
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