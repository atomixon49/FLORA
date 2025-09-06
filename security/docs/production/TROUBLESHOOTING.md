# FLORA Troubleshooting Guide

## Problemas Comunes

### 1. API no responde
```bash
# Verificar logs
docker-compose logs flora-api

# Verificar salud
curl http://localhost:8000/health

# Reiniciar servicio
docker-compose restart flora-api
```

### 2. Errores de autenticación
- Verificar API key en headers
- Comprobar formato: `Authorization: Bearer <api_key>`
- Verificar que la API key esté en la configuración

### 3. Rate limiting
- Verificar límites en configuración
- Comprobar IP en logs
- Ajustar límites si es necesario

### 4. Problemas de rendimiento
- Verificar recursos del sistema
- Revisar métricas en Grafana
- Ajustar número de workers

### 5. Backup fallido
- Verificar permisos en directorio de backup
- Comprobar espacio en disco
- Revisar logs de backup

## Logs Importantes

- **API**: `/var/log/flora/api.log`
- **Nginx**: `/var/log/nginx/access.log`
- **Sistema**: `journalctl -u flora-api`
- **Docker**: `docker-compose logs`

## Comandos Útiles

```bash
# Ver estado de servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar todos los servicios
docker-compose restart

# Actualizar imagen
docker-compose pull && docker-compose up -d

# Backup manual
./scripts/backup.sh

# Restaurar desde backup
./scripts/restore.sh flora_backup_20241206_020000.tar.gz
```
