# 🚀 FLORA Deployment Guide

## **📋 GUÍA DE DESPLIEGUE COMPLETA**

Esta guía te llevará paso a paso para desplegar FLORA Crypto System en diferentes entornos.

---

## **🏗️ ARQUITECTURA DE DESPLIEGUE**

### **Entorno de Desarrollo**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FLORA API     │    │ Security        │    │   Mobile App    │
│   (FastAPI)     │◄──►│ Dashboard       │    │   (Expo)        │
│   Port: 8000    │    │ Port: 8080      │    │   Port: 19000   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   SQLite DB     │    │   SQLite DB     │
│   (Audit)       │    │   (Compliance)  │
└─────────────────┘    └─────────────────┘
```

### **Entorno de Producción**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   FLORA API     │    │   Security      │
│   (Nginx)       │◄──►│   (FastAPI)     │◄──►│   Dashboard     │
│   Port: 80/443  │    │   Port: 8000    │    │   Port: 8080    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │   Redis Cache   │    │   File Storage  │
│   (Primary DB)  │    │   (Sessions)    │    │   (Encrypted)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## **🔧 REQUISITOS DEL SISTEMA**

### **Mínimos**
- **OS**: Windows 10+, Ubuntu 18.04+, macOS 10.15+
- **RAM**: 4GB
- **CPU**: 2 cores
- **Disco**: 10GB libres
- **Python**: 3.8+

### **Recomendados**
- **OS**: Ubuntu 20.04+ LTS
- **RAM**: 8GB+
- **CPU**: 4+ cores
- **Disco**: 50GB+ SSD
- **Python**: 3.11+

### **Dependencias del Sistema**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git cmake build-essential
sudo apt install -y libssl-dev pkg-config

# Windows
# Instalar Python 3.11+ desde python.org
# Instalar Visual Studio Build Tools
# Instalar Git desde git-scm.com

# macOS
brew install python3 cmake pkg-config openssl
```

---

## **📦 INSTALACIÓN PASO A PASO**

### **1. Preparación del Entorno**

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/flora-crypto.git
cd flora-crypto

# Crear entorno virtual
python -m venv flora-env

# Activar entorno virtual
# Windows
flora-env\Scripts\activate
# Linux/macOS
source flora-env/bin/activate

# Actualizar pip
python -m pip install --upgrade pip
```

### **2. Instalación de Dependencias**

```bash
# Dependencias principales
pip install -r requirements.txt

# Dependencias de seguridad
cd security
pip install -r requirements-security.txt

# Dependencias de API
cd ../api
pip install -r requirements.txt
```

### **3. Compilación de Backends**

#### **C++ Backend**
```bash
cd src/cpp

# Configurar build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release

# Compilar
cmake --build build --config Release

# Verificar compilación
./build/Release/flora_example.exe  # Windows
./build/flora_example              # Linux/macOS
```

#### **Rust Backend**
```bash
cd src/rust/flora-rs

# Compilar
cargo build --release

# Instalar bindings de Python
maturin develop --release

# Verificar instalación
python -c "import flora_rs; print('Rust backend OK')"
```

### **4. Inicialización de Bases de Datos**

```bash
cd security

# Inicializar bases de datos
python init_databases.py

# Verificar inicialización
python -c "from audit.security_auditor import SecurityAuditor; print('DB OK')"
```

---

## **🚀 DESPLIEGUE POR ENTORNOS**

### **🛠️ DESARROLLO**

#### **1. Iniciar Servicios Básicos**
```bash
# Terminal 1: API REST
cd api
python main.py

# Terminal 2: Dashboard de Seguridad
cd security/dashboard
python security_dashboard.py

# Terminal 3: Mobile App (opcional)
cd mobile-app
npx expo start
```

#### **2. Verificar Funcionamiento**
```bash
# Probar API
curl http://localhost:8000/health

# Probar Dashboard
curl http://localhost:8080/api/security/health

# Probar CLI
flora status
```

#### **3. Ejecutar Pruebas**
```bash
cd security
python run_tests.py --target-url http://localhost:8000
```

### **🧪 TESTING**

#### **1. Configuración de Testing**
```bash
# Variables de entorno para testing
export FLORA_ENV=testing
export FLORA_DEBUG=1
export FLORA_LOG_LEVEL=DEBUG

# Base de datos de testing
cp security_audit.db security_audit_test.db
cp compliance.db compliance_test.db
```

#### **2. Ejecutar Suite de Pruebas**
```bash
# Pruebas unitarias
python -m pytest tests/ -v

# Pruebas de integración
python security/run_tests.py --target-url http://localhost:8000

# Pruebas de rendimiento
python benchmarks/performance_test.py
```

### **🏭 PRODUCCIÓN**

#### **1. Configuración de Producción**
```bash
# Variables de entorno
export FLORA_ENV=production
export FLORA_DEBUG=0
export FLORA_LOG_LEVEL=INFO
export FLORA_SECRET_KEY="your-secret-key-here"
export FLORA_DB_URL="postgresql://user:pass@localhost/flora"
```

#### **2. Configuración de Base de Datos**
```bash
# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib

# Crear base de datos
sudo -u postgres createdb flora_production
sudo -u postgres createdb flora_audit
sudo -u postgres createdb flora_compliance

# Configurar usuario
sudo -u postgres psql -c "CREATE USER flora_user WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE flora_production TO flora_user;"
```

#### **3. Configuración de Nginx**
```nginx
# /etc/nginx/sites-available/flora
server {
    listen 80;
    server_name flora.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name flora.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    
    # API Backend
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Security Dashboard
    location /security/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### **4. Configuración de Systemd**
```ini
# /etc/systemd/system/flora-api.service
[Unit]
Description=FLORA API Service
After=network.target

[Service]
Type=simple
User=flora
WorkingDirectory=/opt/flora/api
Environment=FLORA_ENV=production
ExecStart=/opt/flora/flora-env/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```ini
# /etc/systemd/system/flora-security.service
[Unit]
Description=FLORA Security Dashboard
After=network.target

[Service]
Type=simple
User=flora
WorkingDirectory=/opt/flora/security/dashboard
Environment=FLORA_ENV=production
ExecStart=/opt/flora/flora-env/bin/python security_dashboard.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### **5. Iniciar Servicios**
```bash
# Habilitar servicios
sudo systemctl enable flora-api
sudo systemctl enable flora-security

# Iniciar servicios
sudo systemctl start flora-api
sudo systemctl start flora-security

# Verificar estado
sudo systemctl status flora-api
sudo systemctl status flora-security
```

---

## **🔒 CONFIGURACIÓN DE SEGURIDAD**

### **1. Certificados SSL**
```bash
# Usando Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d flora.yourdomain.com
```

### **2. Firewall**
```bash
# Configurar UFW
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### **3. Monitoreo de Seguridad**
```bash
# Instalar fail2ban
sudo apt install fail2ban

# Configurar fail2ban para FLORA
sudo nano /etc/fail2ban/jail.d/flora.conf
```

```ini
[flora-api]
enabled = true
port = 8000
filter = flora-api
logpath = /var/log/flora/api.log
maxretry = 5
bantime = 3600
```

---

## **📊 MONITOREO Y MANTENIMIENTO**

### **1. Logs del Sistema**
```bash
# Ver logs de la API
sudo journalctl -u flora-api -f

# Ver logs de seguridad
sudo journalctl -u flora-security -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### **2. Monitoreo de Recursos**
```bash
# CPU y memoria
htop

# Espacio en disco
df -h

# Conexiones de red
netstat -tulpn
```

### **3. Backup de Datos**
```bash
# Script de backup
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/flora"

# Crear directorio de backup
mkdir -p $BACKUP_DIR

# Backup de bases de datos
pg_dump flora_production > $BACKUP_DIR/flora_production_$DATE.sql
pg_dump flora_audit > $BACKUP_DIR/flora_audit_$DATE.sql
pg_dump flora_compliance > $BACKUP_DIR/flora_compliance_$DATE.sql

# Backup de configuración
tar -czf $BACKUP_DIR/flora_config_$DATE.tar.gz /opt/flora/

# Limpiar backups antiguos (más de 30 días)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### **4. Actualizaciones**
```bash
# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Actualizar sistema
sudo apt update && sudo apt upgrade

# Reiniciar servicios después de actualizaciones
sudo systemctl restart flora-api
sudo systemctl restart flora-security
```

---

## **🚨 TROUBLESHOOTING**

### **Problemas Comunes**

#### **1. API no responde**
```bash
# Verificar estado del servicio
sudo systemctl status flora-api

# Ver logs de error
sudo journalctl -u flora-api --since "1 hour ago"

# Verificar puerto
sudo netstat -tulpn | grep 8000
```

#### **2. Dashboard sin datos**
```bash
# Verificar bases de datos
ls -la security_audit.db compliance.db

# Reinicializar bases de datos
cd security
python init_databases.py
```

#### **3. Errores de compilación**
```bash
# Limpiar build de C++
cd src/cpp
rm -rf build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release

# Limpiar build de Rust
cd src/rust/flora-rs
cargo clean
cargo build --release
```

#### **4. Problemas de permisos**
```bash
# Corregir permisos
sudo chown -R flora:flora /opt/flora/
sudo chmod -R 755 /opt/flora/
```

---

## **📞 SOPORTE**

### **Recursos de Ayuda**
- **Documentación**: [README_FINAL.md](README_FINAL.md)
- **Reporte de Seguridad**: [SECURITY_REPORT.md](SECURITY_REPORT.md)
- **API Docs**: `http://localhost:8000/docs`
- **Security Dashboard**: `http://localhost:8080`

### **Contacto**
- **Soporte Técnico**: support@flora-crypto.com
- **Seguridad**: security@flora-crypto.com
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/flora-crypto/issues)

---

**🌸 FLORA - Guía de Despliegue Completa**

*Desarrollado para facilitar el despliegue en cualquier entorno*

