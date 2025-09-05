# 🌸 FLORA API - Sistema de Integración Empresarial

Sistema de APIs REST para integración empresarial con cifrado híbrido post-cuántico.

## 🚀 Características

- **APIs REST** completas para cifrado/desifrado
- **Autenticación** con API keys
- **Auditoría** completa de operaciones
- **Webhooks** para notificaciones
- **Estadísticas** de uso en tiempo real
- **Documentación** automática con Swagger
- **Monitoreo** y logging avanzado

## 📋 Endpoints Principales

### 🔐 Cifrado y Desifrado
- `POST /api/v1/encrypt` - Cifrar datos
- `POST /api/v1/decrypt` - Desifrar datos

### 🔑 Gestión de API Keys
- `POST /api/v1/keys` - Crear API key
- `GET /api/v1/keys` - Listar API keys

### 📊 Monitoreo y Auditoría
- `GET /api/v1/audit` - Logs de auditoría
- `GET /api/v1/stats` - Estadísticas de uso
- `GET /health` - Estado del sistema

### 🔗 Webhooks
- `POST /api/v1/webhooks` - Crear webhook

## 🛠️ Instalación

### Prerrequisitos
- Python 3.8+
- pip
- PostgreSQL (opcional, para producción)

### Pasos de Instalación

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

3. **Ejecutar el servidor:**
   ```bash
   python main.py
   ```

4. **Acceder a la documentación:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🧪 Pruebas

### Ejecutar Tests
```bash
python test_api.py
```

### Probar Manualmente
```bash
# Health check
curl http://localhost:8000/health

# Cifrar datos
curl -X POST "http://localhost:8000/api/v1/encrypt" \
  -H "Authorization: Bearer test_api_key_12345678901234567890" \
  -H "Content-Type: application/json" \
  -d '{"data": "Mensaje secreto", "algorithm": "hybrid_post_quantum"}'
```

## 📖 Uso de la API

### 1. Crear API Key
```python
import requests

response = requests.post("http://localhost:8000/api/v1/keys", json={
    "name": "Mi API Key",
    "permissions": ["encrypt", "decrypt", "read"],
    "expires_in_days": 365
})

api_key = response.json()["api_key"]
```

### 2. Cifrar Datos
```python
headers = {"Authorization": f"Bearer {api_key}"}
data = {"data": "Información confidencial"}

response = requests.post(
    "http://localhost:8000/api/v1/encrypt",
    headers=headers,
    json=data
)

encrypted_data = response.json()["encrypted_data"]
key_id = response.json()["key_id"]
```

### 3. Desifrar Datos
```python
data = {
    "encrypted_data": encrypted_data,
    "key_id": key_id
}

response = requests.post(
    "http://localhost:8000/api/v1/decrypt",
    headers=headers,
    json=data
)

decrypted_data = response.json()["decrypted_data"]
```

## 🔒 Seguridad

### Autenticación
- API keys con expiración
- Permisos granulares
- Rate limiting

### Cifrado
- Algoritmo híbrido post-cuántico
- Rotación automática de claves
- Almacenamiento seguro

### Auditoría
- Log de todas las operaciones
- Trazabilidad completa
- Alertas de seguridad

## 📊 Monitoreo

### Métricas Disponibles
- Operaciones de cifrado/desifrado
- Uso de API keys
- Errores y excepciones
- Tiempo de respuesta

### Logs
- Estructurados en JSON
- Niveles configurables
- Integración con Sentry

## 🔗 Webhooks

### Eventos Soportados
- `encrypt` - Datos cifrados
- `decrypt` - Datos desifrados
- `error` - Errores del sistema
- `key_rotation` - Rotación de claves

### Configuración
```python
webhook_data = {
    "url": "https://tu-servidor.com/webhook",
    "events": ["encrypt", "decrypt", "error"]
}

response = requests.post(
    "http://localhost:8000/api/v1/webhooks",
    headers=headers,
    json=webhook_data
)
```

## 🚀 Despliegue

### Docker
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

### Producción
- Usar PostgreSQL para base de datos
- Configurar Redis para caché
- Implementar load balancer
- Configurar SSL/TLS
- Monitoreo con Prometheus

## 📚 Documentación

### Swagger UI
- URL: http://localhost:8000/docs
- Interfaz interactiva
- Pruebas en vivo

### ReDoc
- URL: http://localhost:8000/redoc
- Documentación legible
- Esquemas detallados

## 🤝 Integración

### SDKs Disponibles
- Python SDK
- JavaScript SDK
- Go SDK
- Java SDK

### Ejemplos de Integración
- Aplicaciones web
- Aplicaciones móviles
- Sistemas empresariales
- Microservicios

## 🐛 Solución de Problemas

### Errores Comunes
1. **401 Unauthorized**: Verificar API key
2. **404 Not Found**: Verificar URL del endpoint
3. **500 Internal Server Error**: Revisar logs del servidor

### Logs
```bash
# Ver logs en tiempo real
tail -f logs/flora-api.log

# Buscar errores
grep "ERROR" logs/flora-api.log
```

## 📞 Soporte

- **Documentación**: http://localhost:8000/docs
- **Issues**: GitHub Issues
- **Email**: support@flora.app
- **Discord**: FLORA Community

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

---

**FLORA API** - Protegiendo la privacidad digital con cifrado post-cuántico 🌸

