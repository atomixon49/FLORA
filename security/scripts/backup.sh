#!/bin/bash
# FLORA Backup Script

BACKUP_DIR="/opt/flora/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="flora_backup_$DATE.tar.gz"

echo "🔄 Iniciando backup de FLORA..."

# Crear directorio de backup
mkdir -p $BACKUP_DIR

# Backup de la aplicación
tar -czf $BACKUP_DIR/$BACKUP_FILE \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='logs' \
    /opt/flora/

# Backup de la base de datos (si existe)
if [ -f "/opt/flora/data/flora.db" ]; then
    cp /opt/flora/data/flora.db $BACKUP_DIR/flora_db_$DATE.db
fi

# Backup de logs
if [ -d "/opt/flora/logs" ]; then
    tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /opt/flora/logs/
fi

# Limpiar backups antiguos (mantener solo 7 días)
find $BACKUP_DIR -name "flora_backup_*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "flora_db_*.db" -mtime +7 -delete
find $BACKUP_DIR -name "logs_*.tar.gz" -mtime +7 -delete

echo "✅ Backup completado: $BACKUP_FILE"

# Enviar notificación (opcional)
# curl -X POST -H 'Content-type: application/json' \
#     --data '{"text":"FLORA backup completado: '$BACKUP_FILE'"}' \
#     $SLACK_WEBHOOK_URL
