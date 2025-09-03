#!/bin/bash

# 🌸 FLORA - Script de Instalación para Linux/Mac
# Instala el sistema de cifrado FLORA con todas las dependencias

echo ""
echo "============================================================"
echo "🌸 FLORA - Sistema de Cifrado Híbrido Post-Cuántico"
echo "============================================================"
echo ""

# Verificar Python
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    echo "💡 Por favor instala Python 3.8+ usando tu gestor de paquetes"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "   macOS: brew install python3"
    exit 1
fi

echo "✅ Python encontrado"
python3 --version

# Verificar pip
echo ""
echo "🔍 Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado"
    echo "💡 Instalando pip3..."
    if command -v apt &> /dev/null; then
        sudo apt install python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install python3-pip
    elif command -v brew &> /dev/null; then
        brew install python3
    else
        echo "❌ No se pudo instalar pip3 automáticamente"
        exit 1
    fi
fi

echo "✅ pip encontrado"
pip3 --version

echo ""
echo "🔧 Instalando dependencias..."
echo ""

# Instalar dependencias principales
echo "📦 Instalando pycryptodome..."
pip3 install "pycryptodome>=3.15.0"

echo "📦 Instalando numpy..."
pip3 install "numpy>=1.21.0"

echo "📦 Instalando scipy..."
pip3 install "scipy>=1.7.0"

echo "📦 Instalando matplotlib..."
pip3 install "matplotlib>=3.5.0"

echo "📦 Instalando otras dependencias..."
pip3 install "cryptography>=3.4.8"
pip3 install "click>=8.0.0"
pip3 install "rich>=10.12.0"
pip3 install "tqdm>=4.62.0"

echo ""
echo "🧪 Instalando herramientas de testing..."
pip3 install "pytest>=6.2.5"
pip3 install "pytest-cov>=2.12.0"
pip3 install "black>=21.7b0"
pip3 install "flake8>=3.9.0"

echo ""
echo "🚀 Instalando FLORA en modo desarrollo..."
pip3 install -e .

echo ""
echo "============================================================"
echo "✅ INSTALACIÓN COMPLETADA EXITOSAMENTE"
echo "============================================================"
echo ""
echo "🧪 Para ejecutar las pruebas:"
echo "   python3 test_flora.py"
echo ""
echo "🚀 Para usar FLORA en tu código:"
echo "   from flora import FloraCryptoSystem"
echo ""
echo "📚 Para más información, consulta README_FLORA.md"
echo ""
echo "🌸 ¡Gracias por instalar FLORA - Crypto Flower!"
echo ""

# Hacer el script ejecutable
chmod +x test_flora.py
