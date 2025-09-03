@echo off
REM 🌸 FLORA - Script de Instalación Rápida para Windows
REM Instala el sistema de cifrado FLORA con todas las dependencias

echo.
echo ============================================================
echo 🌸 FLORA - Sistema de Cifrado Híbrido Post-Cuántico
echo ============================================================
echo.

echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo 💡 Por favor instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

echo.
echo 🔧 Instalando dependencias...
echo.

echo 📦 Instalando pycryptodome...
pip install pycryptodome>=3.15.0

echo 📦 Instalando numpy...
pip install numpy>=1.21.0

echo 📦 Instalando scipy...
pip install scipy>=1.7.0

echo 📦 Instalando matplotlib...
pip install matplotlib>=3.5.0

echo 📦 Instalando otras dependencias...
pip install cryptography>=3.4.8
pip install click>=8.0.0
pip install rich>=10.12.0
pip install tqdm>=4.62.0

echo.
echo 🧪 Instalando herramientas de testing...
pip install pytest>=6.2.5
pip install pytest-cov>=2.12.0
pip install black>=21.7b0
pip install flake8>=3.9.0

echo.
echo 🚀 Instalando FLORA en modo desarrollo...
pip install -e .

echo.
echo ============================================================
echo ✅ INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ============================================================
echo.
echo 🧪 Para ejecutar las pruebas:
echo    python test_flora.py
echo.
echo 🚀 Para usar FLORA en tu código:
echo    from flora import FloraCryptoSystem
echo.
echo 📚 Para más información, consulta README_FLORA.md
echo.
echo 🌸 ¡Gracias por instalar FLORA - Crypto Flower!
echo.

pause
