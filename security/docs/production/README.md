# FLORA Crypto System - Production Guide

## 🚀 Despliegue en Producción

### Requisitos del Sistema
- Ubuntu 20.04+ / CentOS 8+ / RHEL 8+
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM mínimo
- 20GB espacio en disco
- Certificado SSL válido

### Despliegue Rápido

1. **Clonar repositorio**
   ```bash
   git clone https://github.com/flora-crypto/flora.git
   cd flora
   ```

2. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

3. **Desplegar con Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Verificar despliegue**
   ```bash
   curl https://tu-dominio.com/health
   ```

### Despliegue en Kubernetes

1. **Aplicar configuraciones**
   ```bash
   kubectl apply -f k8s/
   ```

2. **Verificar pods**
   ```bash
   kubectl get pods -n flora
   ```

### Monitoreo

- **Grafana**: http://tu-dominio.com:3000
- **Prometheus**: http://tu-dominio.com:9090
- **API Health**: http://tu-dominio.com/health

### Backup y Restauración

- **Backup automático**: Diario a las 2:00 AM
- **Backup manual**: `./scripts/backup.sh`
- **Restaurar**: `./scripts/restore.sh <archivo_backup>`

### Seguridad

- Todos los endpoints requieren autenticación
- Rate limiting habilitado
- Headers de seguridad configurados
- Logs de seguridad en tiempo real

### Soporte

- **Documentación**: https://docs.flora-crypto.com
- **Issues**: https://github.com/flora-crypto/flora/issues
- **Email**: support@flora-crypto.com
