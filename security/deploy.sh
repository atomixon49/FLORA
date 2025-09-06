#!/bin/bash
# FLORA Deployment Script

echo "🚀 Desplegando FLORA Crypto System..."

# Crear directorio de aplicación
mkdir -p /opt/flora
cd /opt/flora

# Clonar repositorio
git clone https://github.com/flora-crypto/flora.git .

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r api/requirements.txt

# Configurar variables de entorno
export FLORA_ENV=production
export FLORA_DEBUG=False
export FLORA_LOG_LEVEL=INFO

# Crear usuario del sistema
useradd -r -s /bin/false flora

# Configurar permisos
chown -R flora:flora /opt/flora
chmod +x /opt/flora/scripts/*.sh

# Iniciar servicio
systemctl enable flora-api
systemctl start flora-api

echo "✅ FLORA desplegado exitosamente"
