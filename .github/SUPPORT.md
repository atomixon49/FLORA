# 🌸 Guía de Soporte para FLORA

¡Bienvenido a la guía de soporte de FLORA! 🌟 Estamos aquí para ayudarte a resolver cualquier problema o responder tus preguntas.

## 🚀 Tabla de Contenidos

- [📞 Contacto Directo](#-contacto-directo)
- [❓ Preguntas Frecuentes](#-preguntas-frecuentes)
- [🔧 Solución de Problemas](#-solución-de-problemas)
- [📚 Recursos de Ayuda](#-recursos-de-ayuda)
- [🤝 Comunidad](#-comunidad)

## 📞 Contacto Directo

### 📧 Email de Soporte

**Soporte General**: [support@cryptoflower.dev](mailto:support@cryptoflower.dev)

**Soporte Técnico**: [tech@cryptoflower.dev](mailto:tech@cryptoflower.dev)

**Soporte de Seguridad**: [security@cryptoflower.dev](mailto:security@cryptoflower.dev)

### ⏱️ Tiempos de Respuesta

- **Crítico**: 2-4 horas
- **Alto**: 8-24 horas
- **Medio**: 24-48 horas
- **Bajo**: 3-5 días hábiles

## ❓ Preguntas Frecuentes

### 🔐 **¿Qué es FLORA?**

FLORA es un sistema de cifrado híbrido post-cuántico que combina AES-256-GCM con un motor de autodestrucción caótica. Es el sistema de cifrado más avanzado y elegante del mundo.

### 🚀 **¿Cómo instalo FLORA?**

```bash
# Clonar repositorio
git clone https://github.com/atomixon49/CRYPTO-FLOWER.git
cd CRYPTO-FLOWER/flora

# Instalar dependencias
pip install -r requirements.txt
pip install -e .
```

### 🧪 **¿Cómo ejecuto las pruebas?**

```bash
# Suite completa
python test_flora.py

# Con pytest
pytest
```

### 🔒 **¿FLORA es seguro para producción?**

FLORA está en fase alpha (0.1.0). Aunque implementa algoritmos criptográficos estándar, se recomienda usar solo para desarrollo y testing hasta que se complete la auditoría de seguridad.

### 🌪️ **¿Qué es la autodestrucción caótica?**

Es un mecanismo único que corrompe irreversiblemente las claves cuando se detecta un ataque, usando sistemas caóticos matemáticos para garantizar que la corrupción sea completa e irreversible.

### 🐍 **¿Qué versiones de Python soporta?**

FLORA requiere Python 3.8 o superior. Se recomienda Python 3.11+ para mejor rendimiento.

## 🔧 Solución de Problemas

### ❌ **Error: "ModuleNotFoundError: No module named 'flora'"**

**Solución**:
```bash
# Asegúrate de estar en el directorio correcto
cd flora

# Instala en modo desarrollo
pip install -e .

# O agrega el path manualmente
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### ❌ **Error: "ImportError: cannot import name 'ChaoticDestructionEngine'"**

**Solución**:
```bash
# Verifica que las dependencias estén instaladas
pip install -r requirements.txt

# Reinstala FLORA
pip uninstall flora-crypto
pip install -e .
```

### ❌ **Error: "AES key must be 16, 24, or 32 bytes long"**

**Solución**:
```python
# Asegúrate de usar la clave correcta
from flora import FloraCryptoSystem

flora = FloraCryptoSystem()
password = "MI_PASSWORD_2024"
master_key, salt = flora.generate_master_key(password)  # Esto genera una clave de 32 bytes
```

### ❌ **Error: "Authentication failed"**

**Solución**:
```python
# Verifica que uses la misma clave maestra
# La clave debe ser exactamente la misma que se usó para encriptar
master_key, salt = flora.generate_master_key(password, salt)  # Usa el mismo salt
```

### ❌ **Error: "System compromised - autodestruction activated"**

**Solución**:
```python
# El sistema detectó una amenaza y se autodestruyó
# Necesitas crear una nueva instancia
flora = FloraCryptoSystem()
# Y generar nuevas claves
```

## 📚 Recursos de Ayuda

### 📖 Documentación

- **README Principal**: [README.md](README.md)
- **Guía de Contribución**: [CONTRIBUTING.md](.github/CONTRIBUTING.md)
- **Política de Seguridad**: [SECURITY.md](.github/SECURITY.md)
- **Código de Conducta**: [CODE_OF_CONDUCT.md](.github/CODE_OF_CONDUCT.md)

### 🎥 Tutoriales

- **Instalación**: [docs.cryptoflower.dev/installation](https://docs.cryptoflower.dev/installation)
- **Uso Básico**: [docs.cryptoflower.dev/usage](https://docs.cryptoflower.dev/usage)
- **API Reference**: [docs.cryptoflower.dev/api](https://docs.cryptoflower.dev/api)
- **Ejemplos**: [docs.cryptoflower.dev/examples](https://docs.cryptoflower.dev/examples)

### 🔍 Búsqueda

- **GitHub Issues**: [Buscar problemas existentes](https://github.com/atomixon49/CRYPTO-FLOWER/issues)
- **GitHub Discussions**: [Buscar discusiones](https://github.com/atomixon49/CRYPTO-FLOWER/discussions)
- **Wiki**: [Documentación adicional](https://github.com/atomixon49/CRYPTO-FLOWER/wiki)

## 🤝 Comunidad

### 💬 Canales de Comunicación

- **GitHub Issues**: [Reportar problemas](https://github.com/atomixon49/CRYPTO-FLOWER/issues)
- **GitHub Discussions**: [Discutir ideas](https://github.com/atomixon49/CRYPTO-FLOWER/discussions)
- **Discord**: [Servidor de la comunidad](https://discord.gg/flora-crypto)
- **Reddit**: [r/FLORAcrypto](https://reddit.com/r/FLORAcrypto)

### 🌟 Contribuir

- **Reportar bugs**: [Crear issue](https://github.com/atomixon49/CRYPTO-FLOWER/issues/new)
- **Sugerir características**: [Crear issue](https://github.com/atomixon49/CRYPTO-FLOWER/issues/new)
- **Contribuir código**: [Fork y PR](https://github.com/atomixon49/CRYPTO-FLOWER/fork)
- **Mejorar documentación**: [Editar archivos](https://github.com/atomixon49/CRYPTO-FLOWER/edit/main)

### 🎯 Etiquetas Útiles

- **`good first issue`**: Para principiantes
- **`help wanted`**: Necesita ayuda
- **`bug`**: Reporte de bug
- **`enhancement`**: Nueva característica
- **`documentation`**: Mejoras de docs
- **`question`**: Pregunta general

## 🆘 Casos de Emergencia

### 🚨 **Sistema Comprometido**

Si sospechas que tu sistema FLORA ha sido comprometido:

1. **Desconecta** inmediatamente del internet
2. **Contacta** al equipo de seguridad: [security@cryptoflower.dev](mailto:security@cryptoflower.dev)
3. **Documenta** todo lo que puedas
4. **No** intentes recuperar datos por tu cuenta

### 💥 **Vulnerabilidad Crítica**

Si descubres una vulnerabilidad crítica:

1. **NO** abras issues públicos
2. **Contacta** inmediatamente: [security@cryptoflower.dev](mailto:security@cryptoflower.dev)
3. **Proporciona** detalles completos
4. **Mantén** la confidencialidad

## 📊 Estado del Sistema

### 🟢 **Operativo**
- **Servicios principales**: Funcionando normalmente
- **Performance**: Óptima
- **Seguridad**: Sin amenazas detectadas

### 🟡 **Mantenimiento**
- **Servicios**: Funcionando con limitaciones
- **Performance**: Reducida
- **Seguridad**: Monitoreo aumentado

### 🔴 **Crítico**
- **Servicios**: Interrumpidos
- **Performance**: No disponible
- **Seguridad**: Amenaza activa

## 🌸 Agradecimientos

Gracias por usar FLORA y por ser parte de nuestra comunidad. Tu feedback y contribuciones nos ayudan a hacer FLORA mejor cada día.

---

**¿Necesitas más ayuda?** ¡No dudes en contactarnos! Estamos aquí para ayudarte. 🌟

**Recuerda**: En FLORA, todos crecemos y florecemos juntos. 🌸✨
