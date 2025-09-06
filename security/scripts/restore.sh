#!/bin/bash
# FLORA Restore Script

BACKUP_FILE=$1
BACKUP_DIR="/opt/flora/backups"

if [ -z "$BACKUP_FILE" ]; then
    echo "❌ Uso: $0 <archivo_de_backup>"
    exit 1
fi

if [ ! -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    echo "❌ Archivo de backup no encontrado: $BACKUP_DIR/$BACKUP_FILE"
    exit 1
fi

echo "🔄 Restaurando FLORA desde: $BACKUP_FILE"

# Detener servicios
systemctl stop flora-api

# Crear backup de seguridad actual
CURRENT_BACKUP="current_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf $BACKUP_DIR/$CURRENT_BACKUP /opt/flora/

# Restaurar desde backup
cd /
tar -xzf $BACKUP_DIR/$BACKUP_FILE

# Restaurar permisos
chown -R flora:flora /opt/flora
chmod +x /opt/flora/scripts/*.sh

# Iniciar servicios
systemctl start flora-api

echo "✅ Restauración completada"
