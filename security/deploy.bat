@echo off
REM FLORA Deployment Script for Windows

echo 🚀 Desplegando FLORA Crypto System...

REM Crear directorio de aplicación
mkdir C:\flora
cd C:\flora

REM Clonar repositorio
git clone https://github.com/flora-crypto/flora.git .

REM Crear entorno virtual
python -m venv venv
call venv\Scripts\activate

REM Instalar dependencias
pip install -r api\requirements.txt

REM Configurar variables de entorno
set FLORA_ENV=production
set FLORA_DEBUG=False
set FLORA_LOG_LEVEL=INFO

REM Crear servicio de Windows
sc create "FLORA API" binPath="C:\flora\venv\Scripts\python.exe C:\flora\api\main.py" start=auto

REM Iniciar servicio
sc start "FLORA API"

echo ✅ FLORA desplegado exitosamente
