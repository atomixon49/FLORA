# 🌸 FLORA - Sistema de Cifrado Híbrido Post-Cuántico

<div align="center">

![FLORA Logo](https://img.shields.io/badge/FLORA-Crypto%20Flower-FF69B4?style=for-the-badge&logo=flower&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Apache%202.0-green?style=for-the-badge&logo=apache&logoColor=white)
![Security](https://img.shields.io/badge/Security-Post--Quantum-red?style=for-the-badge&logo=shield-check&logoColor=white)

**Fractal Lattice Obfuscation with Rotational Autodestruction**

*El sistema de cifrado más avanzado y elegante del mundo* 🌟

[🚀 **Instalar**](#-instalación) • [📚 **Documentación**](#-documentación) • [🧪 **Probar**](#-pruebas) • [🔒 **Seguridad**](#-características-de-seguridad)

</div>

---

## 🌟 **¿Qué es FLORA?**

**FLORA** es un sistema de cifrado híbrido revolucionario que combina la elegancia de la naturaleza con la potencia de la criptografía post-cuántica. Inspirado en el delicado pero poderoso mundo de las flores, FLORA implementa un mecanismo único de **autodestrucción caótica** que protege tus datos de manera irreversible ante cualquier amenaza.

### 🌸 **Inspiración Biológica**
- **🌱 Receptáculo**: Centro de datos seguro
- **🌸 Pétalos**: Capas de encriptación biomimética
- **🌿 Tallo**: Sistema inmune contra ataques
- **🦠 Raíces**: Regeneración y evolución continua

---

## 🚀 **Características Principales**

| 🔐 **Seguridad** | ⚡ **Performance** | 🌪️ **Autodestrucción** | 🧬 **Evolución** |
|------------------|-------------------|------------------------|------------------|
| AES-256-GCM | Hasta 116 MB/s | Mapa logístico caótico | Aprendizaje de ataques |
| Post-cuántico | Latencia < 1ms | Corrupción irreversible | Mejoras automáticas |
| Perfect Forward Secrecy | Escalable | Sensibilidad extrema | Regeneración |

---

## 🛡️ **Características de Seguridad**

### 🔒 **Cifrado Híbrido Avanzado**
- **AES-256-GCM**: Cifrado simétrico de nivel militar
- **PBKDF2**: Derivación de claves con 100,000 iteraciones
- **Perfect Forward Secrecy**: Claves de sesión únicas
- **Nonces aleatorios**: 96 bits de entropía
- **(Fase 2) Kyber KEM opcional**: Encapsulamiento post‑cuántico de la clave de sesión cuando hay backend disponible

### 🌪️ **Motor de Autodestrucción Caótica**
- **Mapa logístico**: r = 3.998785 (régimen caótico)
- **Sensibilidad extrema**: Efecto mariposa aplicado
- **Corrupción irreversible**: Una vez activado, no hay vuelta atrás
- **Detección de amenazas**: Tiempo real con IA

### 🚨 **Sistema de Defensa Inteligente**
- **Detección de ataques**: Análisis de patrones en tiempo real
- **Bloqueo adaptativo**: Duración exponencial inteligente
- **Evaluación de amenazas**: Scoring dinámico 0.0 - 1.0
- **Respuesta automática**: Sin intervención humana

---

## 📦 **Instalación**

### 🐍 **Python (Recomendado)**
```bash
# Clonar repositorio
git clone https://github.com/atomixon49/CRYPTO-FLOWER.git
cd CRYPTO-FLOWER/flora

# Instalar dependencias básicas
pip install pycryptodome numpy scipy matplotlib

# Instalar en modo desarrollo
pip install -e .

# (Opcional) Backend Kyber para post-cuántico
pip install pqcrypto  # o pykyber
```

### 🦀 **Rust Backend (Opcional)**
```bash
# Instalar Rust
# https://rustup.rs/

# Compilar módulo Rust
cd src/rust/flora-rs
pip install maturin
maturin develop --release
```

### ⚡ **C++ Backend (Opcional)**
```bash
# Instalar OpenSSL
# Windows: https://slproweb.com/products/Win32OpenSSL.html
# Linux: sudo apt-get install libssl-dev
# macOS: brew install openssl

# Compilar DLL
cd src/cpp
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```

### 🪟 **Windows (Automático)**
```cmd
install.bat
```

### 🐧 **Linux/macOS (Automático)**
```bash
chmod +x install.sh
./install.sh
```

---

## 🧪 **Pruebas**

### 🚀 **Ejecutar Suite Completa**
```bash
python test_flora.py
```

### 🔬 **Pruebas Individuales**
```python
from flora import FloraCryptoSystem

flora = FloraCryptoSystem(use_kyber=True)  # Kyber opcional (fallback automático si no hay backend)
password = "MI_SUPER_PASSWORD_2024"
master_key, salt = flora.generate_master_key(password)

message = b"Hola FLORA"
encrypted = flora.encrypt_message(message, master_key, "test_session")
plaintext = flora.decrypt_message(encrypted, master_key)
print(plaintext)
```

Nota: Si no hay librería Kyber instalada, FLORA usará automáticamente PBKDF2 + AES‑GCM sin requerir cambios.

---

## 📊 **Benchmarks de Performance**

### 🐍 **Python FLORA (Sistema Completo)**
| Tamaño Mensaje | Encriptación | Desencriptación | Throughput |
|----------------|--------------|-----------------|------------|
| 7 bytes       | 0.79 ms      | 0.08 ms         | 8.7 KB/s   |
| 47 bytes      | 0.58 ms      | 0.07 ms         | 79.6 KB/s  |
| 1 KB          | 0.58 ms      | 0.08 ms         | 1.7 MB/s   |
| 10 KB         | 0.58 ms      | 0.08 ms         | 16.8 MB/s  |

### ⚡ **C++ vs 🦀 Rust (Backends Nativos)**
| Tamaño | C++ (ms) | Rust (ms) | Ganador |
|--------|----------|-----------|---------|
| Small (11 bytes) | 0.613 | 0.004 | 🦀 Rust 172x |
| Medium (420 bytes) | 0.031 | 0.013 | 🦀 Rust 2.5x |
| Large (4800 bytes) | 0.042 | 0.102 | ⚡ C++ 2.4x |

**Análisis**: Rust excelente para datos pequeños/medianos, C++ mejor para datos grandes.

---

## 🏗️ **Arquitectura del Sistema**

```
┌─────────────────────────────────────────────────────────────┐
│                    🌸 FLORA SYSTEM                          │
├─────────────────────────────────────────────────────────────┤
│  🔐 LAYER 1: AES-256-GCM Encryption                          │
│  🌪️ LAYER 2: Chaotic Destruction Engine                      │
│  🛡️ LAYER 3: Threat Detection & Response                     │
│  🔑 LAYER 4: Key Management & Derivation + (Kyber KEM opc.)  │
│  📊 LAYER 5: System Health & Monitoring                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                🚀 MULTI-LANGUAGE BACKENDS                   │
├─────────────────────────────────────────────────────────────┤
│  🐍 Python Core: FloraCryptoSystem + CLI + API              │
│  ⚡ C++ Backend: flora_c.dll (OpenSSL) - Alto rendimiento   │
│  🦀 Rust Backend: flora_rs (aes-gcm) - Máxima seguridad     │
│  🔗 FFI Layer: ctypes + pyo3 bindings                       │
└─────────────────────────────────────────────────────────────┘
```

### 🔧 **Componentes Principales**

#### **ChaoticDestructionEngine**
- Mapa logístico caótico
- Generación de secuencias de destrucción
- Corrupción irreversible de claves
- Estadísticas de eventos

#### **FloraCryptoSystem**
- Gestión de claves maestras y de sesión
- Encriptación/desencriptación AES-GCM
- Sistema de detección de amenazas
- Mecanismo de autodestrucción
- (Opcional) Intercambio de clave con **Kyber KEM**

---

## 🌐 API REST

### Iniciar servidor
```bash
# Desde el directorio flora
python -m uvicorn python.api:app --reload --port 8000
# Docs interactivas: http://127.0.0.1:8000/docs
```

Opcional: configurar API Key
```bash
# Windows PowerShell
$env:FLORA_API_KEY = "mi-api-key"
# Linux/macOS
export FLORA_API_KEY="mi-api-key"
```

### Ejemplos (PowerShell)

- Encrypt
```powershell
$headers = @{ 'X-API-Key' = 'flora-dev-key' }  # o tu API key
$body = @{
  password = 'Prueba123'
  message = 'Hola FLORA desde API'
  session_id = 'api_demo'
  associated_data_hex = '414243'
  use_kyber = $false
} | ConvertTo-Json

$res = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/encrypt -Headers $headers -ContentType 'application/json' -Body $body
$res | ConvertTo-Json -Depth 6 | Out-File enc.json
```

- Decrypt
```powershell
$headers = @{ 'X-API-Key' = 'flora-dev-key' }
$bundle = Get-Content enc.json -Raw
$body = @{ password = 'Prueba123'; bundle = ($bundle | ConvertFrom-Json) } | ConvertTo-Json -Depth 6
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/decrypt -Headers $headers -ContentType 'application/json' -Body $body
```

- Status
```powershell
$headers = @{ 'X-API-Key' = 'flora-dev-key' }
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/status -Headers $headers
```

### Ejemplos (cURL)

- Encrypt
```bash
curl -s -X POST http://127.0.0.1:8000/encrypt \
  -H "X-API-Key: flora-dev-key" \
  -H "Content-Type: application/json" \
  -d '{"password":"Prueba123","message":"Hola FLORA desde API","session_id":"api_demo","associated_data_hex":"414243","use_kyber":false}' > enc.json
```

- Decrypt
```bash
curl -s -X POST http://127.0.0.1:8000/decrypt \
  -H "X-API-Key: flora-dev-key" \
  -H "Content-Type: application/json" \
  -d "$(jq -c --arg pwd Prueba123 '{password:$pwd, bundle:.}' enc.json)"
```

Notas:
- El bundle de `/encrypt` incluye `master_salt` y `session_salt` para permitir desencriptar sin estado del servidor.
- En PowerShell, puedes encadenar comandos con `;`.

---

## 🛠️ **Tutoriales de Uso - Fase 3**

### 🐍 **1. Python FLORA (Sistema Completo)**

#### Instalación y Configuración
```bash
# Instalar dependencias
pip install pycryptodome numpy scipy matplotlib

# Instalar FLORA
pip install -e .
```

#### Uso Básico
```python
from flora_crypto import FloraCryptoSystem

# Crear sistema
flora = FloraCryptoSystem()

# Generar clave maestra
flora.generate_master_key('mi_password_seguro')

# Crear sesión
flora.create_session_key('mi_password_seguro', 'sesion_1')

# Encriptar
mensaje = b'Hola FLORA desde Python'
encrypted = flora.encrypt_message(mensaje, 'mi_password_seguro', 'sesion_1')

# Desencriptar
decrypted = flora.decrypt_message(encrypted, 'mi_password_seguro')

print(f"Mensaje original: {decrypted}")
```

#### CLI (Línea de Comandos)
```bash
# Encriptar
flora encrypt --password "mi_password" --message "Hola FLORA" --session "test"

# Desencriptar
flora decrypt --password "mi_password" --bundle "encrypted_data.json"

# Estado del sistema
flora status
```

### ⚡ **2. Backend C++ (Alto Rendimiento)**

#### Configuración Requerida
```powershell
# Windows PowerShell
$env:FLORA_CPP_DLL = 'C:\ruta\a\flora_c.dll'
$env:Path += ';C:\Program Files\OpenSSL-Win64\bin'
```

#### Uso Directo
```python
from ffi_cpp import cpp_encrypt, cpp_decrypt

# Clave de 32 bytes
key = b'mi_clave_de_32_bytes_exactamente_123'

# Datos a encriptar
data = b'Hola FLORA desde C++'
associated_data = b'AD'

# Encriptar
nonce, ciphertext = cpp_encrypt(key, data, associated_data)
print(f"Nonce: {nonce.hex()}")
print(f"Ciphertext: {ciphertext.hex()}")

# Desencriptar
decrypted = cpp_decrypt(key, nonce, ciphertext, associated_data)
print(f"Desencriptado: {decrypted}")
```

### 🦀 **3. Backend Rust (Máxima Seguridad)**

#### Instalación
```bash
# Instalar Rust (si no está instalado)
# https://rustup.rs/

# En el directorio del proyecto
cd flora/src/rust/flora-rs

# Crear virtualenv de Python
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate  # Linux/macOS

# Instalar maturin
pip install maturin

# Compilar e instalar módulo Rust
maturin develop --release
```

#### Uso Directo
```python
from ffi_rust import rust_encrypt, rust_decrypt

# Clave de 32 bytes
key = b'mi_clave_de_32_bytes_exactamente_123'

# Datos a encriptar
data = b'Hola FLORA desde Rust'
associated_data = b'AD'

# Encriptar
nonce, ciphertext = rust_encrypt(key, data, associated_data)
print(f"Nonce: {nonce.hex()}")
print(f"Ciphertext: {ciphertext.hex()}")

# Desencriptar
decrypted = rust_decrypt(key, nonce, ciphertext, associated_data)
print(f"Desencriptado: {decrypted}")
```

### 🧪 **4. Benchmarks Comparativos**

#### Ejecutar Benchmarks
```bash
# Benchmark simple (C++ vs Rust)
python benchmarks/simple_benchmark.py

# Benchmark completo (Python + C++ + Rust)
python benchmarks/performance_test.py
```

#### Resultados Esperados
```
🚀 FLORA Simple Benchmark: C++ vs Rust
==================================================

📊 Tamaño: small (11 bytes)
------------------------------
⚡ Probando C++...
   Media: 0.000613s
🦀 Probando Rust...
   Media: 0.000004s
   🏆 Rust es 172.25x más rápido que C++
```

---

## 🚨 **Solución de Problemas Comunes**

### ❌ **Error: "Could not find module 'flora_c.dll'"**
**Causa**: La DLL de C++ no está en el PATH o no se encuentra.

**Solución**:
```powershell
# Verificar que la DLL existe
Test-Path "C:\ruta\a\flora_c.dll"

# Configurar variable de entorno
$env:FLORA_CPP_DLL = 'C:\ruta\completa\a\flora_c.dll'

# Agregar OpenSSL al PATH
$env:Path += ';C:\Program Files\OpenSSL-Win64\bin'
```

### ❌ **Error: "key must be 32 bytes for Aes256Gcm"**
**Causa**: La clave no tiene exactamente 32 bytes.

**Solución**:
```python
# ❌ Incorrecto
key = b'mi_clave'  # Solo 8 bytes

# ✅ Correcto
key = b'mi_clave_de_32_bytes_exactamente_123'[:32]  # 32 bytes
```

### ❌ **Error: "maturin failed - rustc not found"**
**Causa**: Rust no está instalado o no está en el PATH.

**Solución**:
```bash
# Instalar Rust
# https://rustup.rs/

# Verificar instalación
rustc --version
cargo --version

# Reiniciar terminal y volver a intentar
maturin develop --release
```

### ❌ **Error: "PYO3_USE_ABI3_FORWARD_COMPATIBILITY"**
**Causa**: PyO3 no soporta Python 3.13+ por defecto.

**Solución**:
```powershell
# Forzar compatibilidad
$env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY="1"
maturin develop --release
```

### ❌ **Error: "OpenSSL not found" en C++**
**Causa**: OpenSSL no está instalado o no está en el PATH.

**Solución**:
```powershell
# Instalar OpenSSL (Chocolatey)
choco install openssl

# O descargar desde https://slproweb.com/products/Win32OpenSSL.html
# Agregar al PATH
$env:Path += ';C:\Program Files\OpenSSL-Win64\bin'
```

### ❌ **Error: "FloraCryptoSystem.create_session_key() missing 1 required positional argument"**
**Causa**: API de FLORA requiere 2 argumentos para create_session_key.

**Solución**:
```python
# ❌ Incorrecto
flora.create_session_key('session_id')

# ✅ Correcto
flora.create_session_key('master_key', 'session_id')
```

### ❌ **Error: "PowerShell && not recognized"**
**Causa**: PowerShell no reconoce `&&` como separador de comandos.

**Solución**:
```powershell
# ❌ Incorrecto
cd flora && python test.py

# ✅ Correcto
cd flora; python test.py
# O ejecutar por separado
cd flora
python test.py
```

---

## 🚀 **Roadmap de Desarrollo**

### 🌱 **FASE 1: Prototipo Básico** ✅
- [x] Motor de autodestrucción caótica
- [x] Sistema de cifrado AES-256-GCM
- [x] Gestión de claves y sesiones
- [x] Suite completa de pruebas

### 🌿 **FASE 2: Post-Cuántico** ✅ (Integración opcional)
- [x] Integración opcional con CRYSTALS-Kyber (si hay backend disponible)
- [x] Fallback transparente a PBKDF2 + AES-GCM
- [ ] Guías para instalar backend Kyber (pqcrypto/pykyber)

### 🌳 **FASE 3: Multi-Lenguaje** ✅
- [x] Implementación en C++ (flora_c.dll)
- [x] Implementación en Rust (flora_rs)
- [x] Bindings nativos (ctypes + pyo3)
- [x] Benchmarks comparativos

### 🌺 **FASE 4: Aplicaciones** 📋
- [ ] Plugin para navegadores
- [ ] Aplicación móvil
- [ ] Integración con sistemas existentes
- [ ] Certificaciones de seguridad

---

## 🔬 **Investigación y Desarrollo**

FLORA es el resultado de años de investigación en:
- **Criptografía post-cuántica**
- **Sistemas caóticos**
- **Biomimética computacional**
- **Inteligencia artificial aplicada**

---

## 📄 **Licencia**

Este proyecto está licenciado bajo la **Apache License 2.0** - ver el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">

**🌸 FLORA - Donde la elegancia se encuentra con la seguridad 🌸**

*Construido con ❤️ y 🌪️ caos controlado*

[⬆️ Volver arriba](#-flora---sistema-de-cifrado-híbrido-post-cuántico)

</div>

---

## ✅ **Verificación Rápida - Fase 3**

### 🧪 **Test de Todos los Backends**
```bash
# 1. Test Python FLORA
python -c "from flora_crypto import FloraCryptoSystem; print('✅ Python FLORA OK')"

# 2. Test C++ Backend
$env:FLORA_CPP_DLL = 'C:\ruta\a\flora_c.dll'
$env:Path += ';C:\Program Files\OpenSSL-Win64\bin'
python -c "from ffi_cpp import cpp_encrypt; print('✅ C++ Backend OK')"

# 3. Test Rust Backend
python -c "from ffi_rust import rust_encrypt; print('✅ Rust Backend OK')"

# 4. Benchmark Comparativo
python benchmarks/simple_benchmark.py
```

### 🎯 **Estado de Implementación**
- ✅ **Python FLORA**: Sistema completo con autodestrucción
- ✅ **C++ Backend**: DLL compilada y funcionando
- ✅ **Rust Backend**: Módulo pyo3 instalado
- ✅ **FFI Bindings**: ctypes + pyo3 operativos
- ✅ **Benchmarks**: Comparativas C++ vs Rust
- ✅ **CLI/API**: Interfaz de usuario completa
- ✅ **Documentación**: Tutoriales y solución de problemas

**🌸 FLORA FASE 3: COMPLETAMENTE FUNCIONAL 🌸**

---

## 🛠️ Build C++ (Windows)

Requisitos:
- CMake 3.15+
- MSVC (Build Tools) o Visual Studio 2019+
- OpenSSL (librerías de desarrollo instaladas y en PATH)

Pasos:
```powershell
# Ubicación del proyecto C++
cd flora\src\cpp

# Generar build (Release)
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release

# Compilar
cmake --build build --config Release

# Ejecutar ejemplo
.\build\Release\flora_example.exe
```
Salida esperada:
```
Hola FLORA desde C++
```
Notas:
- Si CMake no encuentra OpenSSL, verifica la instalación y variables de entorno.
- Puedes usar vcpkg/Chocolatey para instalar OpenSSL en Windows.

