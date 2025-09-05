#!/usr/bin/env python3
"""
FLORA Security - Instalador de Dependencias
Script para instalar dependencias de seguridad
"""

import subprocess
import sys
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install_package(package):
    """Instalar un paquete usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        logger.info(f"✅ {package} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error al instalar {package}: {e}")
        return False

def main():
    """Función principal"""
    print("🌸 FLORA Security - Instalando Dependencias")
    print("=" * 50)
    
    # Dependencias esenciales para seguridad
    essential_packages = [
        "requests",
        "sqlite3",  # Ya viene con Python
        "fastapi",
        "uvicorn",
        "jinja2"
    ]
    
    # Dependencias opcionales para análisis avanzado
    optional_packages = [
        "safety",  # Para escaneo de dependencias
        "bandit",  # Para análisis de código Python
        "semgrep",  # Para análisis de código
        "pip-audit"  # Para auditoría de paquetes
    ]
    
    print("📦 Instalando dependencias esenciales...")
    essential_success = 0
    for package in essential_packages:
        if package != "sqlite3":  # sqlite3 ya viene con Python
            if install_package(package):
                essential_success += 1
    
    print(f"\n✅ Dependencias esenciales: {essential_success}/{len(essential_packages)-1} instaladas")
    
    print("\n📦 Instalando dependencias opcionales...")
    optional_success = 0
    for package in optional_packages:
        if install_package(package):
            optional_success += 1
    
    print(f"\n✅ Dependencias opcionales: {optional_success}/{len(optional_packages)} instaladas")
    
    if essential_success == len(essential_packages) - 1:
        print("\n🎉 ¡Todas las dependencias esenciales instaladas!")
        print("🚀 Ahora puedes ejecutar las pruebas de seguridad")
        return 0
    else:
        print("\n⚠️ Algunas dependencias esenciales no se pudieron instalar")
        print("🔧 Revisa los errores anteriores e instala manualmente si es necesario")
        return 1

if __name__ == "__main__":
    exit(main())
