# 🌸 FLORA Browser Extension

Extensión de navegador que implementa el sistema de cifrado FLORA directamente en el navegador web.

## 🚀 **Características**

- 🔐 **Cifrado automático** de campos sensibles
- 🌪️ **Autodestrucción** en caso de detección de amenazas
- 🛡️ **Protección en tiempo real** de formularios
- 📱 **Sincronización** con aplicación móvil (próximamente)
- 🎨 **Interfaz minimalista** y no intrusiva

## 📦 **Instalación**

### **Desarrollo (Chrome/Edge)**

1. **Compilar WebAssembly**:
   ```bash
   # Windows
   build-wasm.bat
   
   # Linux/macOS
   chmod +x build-wasm.sh
   ./build-wasm.sh
   ```

2. **Cargar extensión**:
   - Abrir Chrome/Edge
   - Ir a `chrome://extensions/`
   - Activar "Modo de desarrollador"
   - Hacer clic en "Cargar extensión sin empaquetar"
   - Seleccionar la carpeta `browser-extension/`

### **Desarrollo (Firefox)**

1. **Compilar WebAssembly** (mismo proceso que Chrome)

2. **Cargar extensión**:
   - Abrir Firefox
   - Ir a `about:debugging`
   - Hacer clic en "Este Firefox"
   - Hacer clic en "Cargar complemento temporal"
   - Seleccionar el archivo `manifest.json`

## 🛠️ **Desarrollo**

### **Estructura del Proyecto**

```
browser-extension/
├── manifest.json          # Configuración de la extensión
├── popup.html             # Interfaz del popup
├── popup.css              # Estilos del popup
├── popup.js               # Lógica del popup
├── content.js             # Script de contenido
├── background.js          # Service worker
├── content.css            # Estilos del contenido
├── flora-wasm.js          # Módulo WebAssembly (generado)
├── flora-wasm.wasm        # Binario WebAssembly (generado)
├── icons/                 # Iconos de la extensión
└── build-wasm.*           # Scripts de compilación
```

### **Compilar WebAssembly**

```bash
# Instalar dependencias
cd src/rust/flora-wasm
cargo install wasm-pack

# Compilar
wasm-pack build --target web --out-dir ../../../browser-extension/pkg
```

### **Testing**

1. **Cargar extensión** en modo desarrollador
2. **Abrir cualquier página web** con formularios
3. **Hacer clic en el icono de FLORA** en la barra de herramientas
4. **Configurar una clave maestra** (32 bytes en hex)
5. **Probar cifrado/desifrado** de campos

## 🔧 **Configuración**

### **Clave Maestra**

- **Longitud**: 32 bytes (64 caracteres hexadecimales)
- **Generación**: Automática o manual
- **Almacenamiento**: Chrome Storage API (sincronizado)

### **Protección Automática**

- **Detección**: Campos con nombres sensibles (password, secret, etc.)
- **Cifrado**: Automático al detectar campos sensibles
- **Indicadores**: Icono 🌸 en campos protegibles

### **Autodestrucción**

- **Activación**: Detección de actividad sospechosa
- **Acción**: Limpieza completa de claves y datos
- **Recuperación**: Requiere reconfiguración manual

## 🎯 **Uso**

### **Cifrado Manual**

1. **Abrir popup** de la extensión
2. **Configurar clave maestra** (si no está configurada)
3. **Hacer clic en "Cifrar Página"**
4. **Los campos sensibles** se cifrarán automáticamente

### **Desifrado**

1. **Hacer clic en "Desifrar Página"**
2. **Los campos cifrados** volverán a su estado original

### **Protección Automática**

1. **Activar "Protección automática"** en el popup
2. **Los campos sensibles** se protegerán automáticamente
3. **Hacer clic en el icono 🌸** para cifrar manualmente

## 🔒 **Seguridad**

### **Almacenamiento**

- **Claves**: Chrome Storage API (encriptado por el navegador)
- **Datos temporales**: Memoria del content script
- **Limpieza**: Automática al cerrar pestañas

### **Cifrado**

- **Algoritmo**: AES-256-GCM (WebAssembly)
- **Claves**: Derivadas de clave maestra
- **Nonces**: Aleatorios por cada cifrado

### **Privacidad**

- **Sin telemetría**: No se envían datos a servidores externos
- **Local**: Todo el procesamiento es local
- **Open Source**: Código completamente auditable

## 🐛 **Solución de Problemas**

### **Error: "WASM module not loaded"**

**Solución**:
1. Verificar que `flora-wasm.js` y `flora-wasm.wasm` existen
2. Recompilar WebAssembly con `build-wasm.bat/sh`
3. Recargar la extensión

### **Error: "Invalid key length"**

**Solución**:
1. La clave debe tener exactamente 64 caracteres hexadecimales
2. Usar el botón "Generar" para crear una clave automáticamente

### **Error: "Content script not responding"**

**Solución**:
1. Recargar la página web
2. Verificar que la extensión está habilitada
3. Comprobar la consola del navegador para errores

### **Campos no se cifran automáticamente**

**Solución**:
1. Verificar que "Protección automática" está activada
2. Los campos deben tener nombres sensibles (password, secret, etc.)
3. Hacer clic manualmente en el icono 🌸

## 📊 **Estadísticas**

La extensión rastrea:
- **Elementos cifrados**: Contador de campos protegidos
- **Tiempo de sesión**: Duración de la sesión activa
- **Eventos de seguridad**: Logs de actividad

## 🚀 **Próximas Características**

- [ ] **Sincronización** con aplicación móvil
- [ ] **Cifrado de archivos** arrastrados
- [ ] **Protección de imágenes** sensibles
- [ ] **Integración** con gestores de contraseñas
- [ ] **Modo incógnito** mejorado

## 🤝 **Contribuir**

1. **Fork** el repositorio
2. **Crear rama** para nueva característica
3. **Implementar** cambios
4. **Probar** en múltiples navegadores
5. **Crear Pull Request**

## 📄 **Licencia**

Apache License 2.0 - Ver [LICENSE](../../LICENSE) para más detalles.

---

**🌸 FLORA Browser Extension - Cifrado seguro en tu navegador 🌸**
