# 🌸 Guía de Contribución para FLORA

¡Gracias por tu interés en contribuir a FLORA! 🌟 Este documento te guiará a través del proceso de contribución.

## 🚀 Tabla de Contenidos

- [🌱 Primeros Pasos](#-primeros-pasos)
- [🔧 Configuración del Entorno](#-configuración-del-entorno)
- [📝 Flujo de Trabajo](#-flujo-de-trabajo)
- [🧪 Testing](#-testing)
- [📚 Documentación](#-documentación)
- [🔒 Seguridad](#-seguridad)
- [🤝 Comunidad](#-comunidad)

## 🌱 Primeros Pasos

### 📋 Requisitos Previos

- **Python 3.8+** instalado
- **Git** configurado
- Conocimientos básicos de **criptografía**
- Entusiasmo por la **seguridad digital** 🌸

### 🎯 Tipos de Contribuciones

- 🐛 **Reportar bugs**
- 💡 **Sugerir nuevas características**
- 🔧 **Mejorar el código existente**
- 📚 **Mejorar la documentación**
- 🧪 **Agregar pruebas**
- 🌐 **Traducciones**
- 🎨 **Mejoras de UI/UX**

## 🔧 Configuración del Entorno

### 1️⃣ Fork y Clone

```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/TU_USUARIO/CRYPTO-FLOWER.git
cd CRYPTO-FLOWER

# Agrega el repositorio original como upstream
git remote add upstream https://github.com/atomixon49/CRYPTO-FLOWER.git
```

### 2️⃣ Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install -e .
```

### 3️⃣ Pre-commit Hooks

```bash
# Instalar pre-commit
pip install pre-commit

# Instalar hooks
pre-commit install

# Ejecutar en todos los archivos
pre-commit run --all-files
```

## 📝 Flujo de Trabajo

### 🔄 Flujo de Desarrollo

1. **Sincronizar** con upstream
2. **Crear** una nueva rama
3. **Desarrollar** tu característica
4. **Probar** tu código
5. **Commit** con mensajes claros
6. **Push** a tu fork
7. **Crear** Pull Request

### 🌿 Convenciones de Ramas

```bash
# Formato: tipo/descripción-breve
feature/chaotic-destruction-engine
bugfix/fix-aes-encryption
docs/update-readme
test/add-performance-tests
```

### 📝 Convenciones de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Formato: tipo(alcance): descripción
feat(chaos): implement chaotic destruction engine
fix(crypto): resolve AES-GCM nonce generation
docs(readme): add installation instructions
test(engine): add chaos engine unit tests
style(code): format with black
refactor(core): simplify key derivation
perf(encryption): optimize AES operations
```

### 🔍 Pull Request Guidelines

- **Título descriptivo** que resuma el cambio
- **Descripción detallada** del problema y solución
- **Referencias** a issues relacionados
- **Capturas de pantalla** si es aplicable
- **Tests** que cubran el nuevo código
- **Documentación** actualizada

## 🧪 Testing

### 🚀 Ejecutar Tests

```bash
# Suite completa
python test_flora.py

# Con pytest
pytest

# Con coverage
pytest --cov=flora --cov-report=html

# Tests específicos
pytest tests/test_chaotic_map.py -v
```

### 📊 Cobertura de Código

- **Mínimo**: 80% de cobertura
- **Objetivo**: 90%+ de cobertura
- **Crítico**: 100% para módulos de seguridad

### 🧪 Escribir Tests

```python
def test_chaotic_destruction_engine():
    """Test del motor de autodestrucción caótica."""
    engine = ChaoticDestructionEngine()
    
    # Arrange
    test_key = b"TEST_KEY_2024"
    
    # Act
    r, x0 = engine.initialize_chaos_seed(test_key)
    
    # Assert
    assert 3.5 < r < 4.0
    assert 0.0 < x0 < 1.0
```

## 📚 Documentación

### 📖 Estándares de Documentación

- **Docstrings** en formato Google
- **README** actualizado
- **Ejemplos** de uso
- **Diagramas** cuando sea necesario

### 🔧 Generar Documentación

```bash
# Instalar dependencias de docs
pip install -e ".[docs]"

# Generar documentación
cd docs
make html
```

## 🔒 Seguridad

### 🚨 Reportar Vulnerabilidades

**NO** abras issues públicos para vulnerabilidades de seguridad.

**Email**: [security@cryptoflower.dev](mailto:security@cryptoflower.dev)

### 🔐 Guidelines de Seguridad

- **Nunca** commitees claves o secretos
- **Siempre** valida entradas de usuario
- **Usa** algoritmos criptográficos estándar
- **Implementa** principios de menor privilegio

## 🤝 Comunidad

### 💬 Canales de Comunicación

- **GitHub Issues**: [Reportar problemas](https://github.com/atomixon49/CRYPTO-FLOWER/issues)
- **GitHub Discussions**: [Discutir ideas](https://github.com/atomixon49/CRYPTO-FLOWER/discussions)
- **Email**: [team@cryptoflower.dev](mailto:team@cryptoflower.dev)

### 🌟 Reconocimiento

- **Contribuidores** aparecen en el README
- **Commits** son reconocidos en el historial
- **Pull Requests** exitosos son destacados

### 🎉 Celebración

- **Releases** con notas de contribuidores
- **Badges** para contribuidores activos
- **Menciones** en redes sociales

## 📋 Checklist de Contribución

Antes de enviar tu Pull Request, asegúrate de:

- [ ] **Código** sigue las convenciones del proyecto
- [ ] **Tests** pasan y cubren el nuevo código
- [ ] **Documentación** está actualizada
- [ ] **Pre-commit hooks** pasan
- [ ] **Linting** no muestra errores
- [ ] **Commits** siguen el formato convencional
- [ ] **Mensaje** del PR es claro y descriptivo

## 🚀 Próximos Pasos

1. **Lee** el [README](README.md)
2. **Explora** los [issues](https://github.com/atomixon49/CRYPTO-FLOWER/issues)
3. **Únete** a la [comunidad](https://github.com/atomixon49/CRYPTO-FLOWER/discussions)
4. **Empieza** con un issue marcado como "good first issue"

## 🙏 Agradecimientos

¡Gracias por hacer de FLORA un proyecto mejor! 🌸

Tu contribución ayuda a crear un sistema de cifrado más seguro y elegante para todos.

---

**¿Tienes preguntas?** ¡No dudes en preguntar! Estamos aquí para ayudarte. 🌟


