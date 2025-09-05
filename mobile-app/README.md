# 🌸 FLORA Mobile App

Aplicación móvil para el sistema de cifrado híbrido post-cuántico FLORA.

## 🚀 Características

- **Cifrado Seguro**: Cifrado AES-256-GCM con derivación de claves PBKDF2
- **Interfaz Intuitiva**: Diseño moderno y fácil de usar
- **Gestión de Archivos**: Organiza y gestiona tus archivos cifrados
- **Centro de Seguridad**: Monitorea el estado de seguridad de la app
- **Configuración Flexible**: Personaliza la experiencia según tus necesidades

## 📱 Pantallas Principales

### 🏠 Inicio
- Dashboard con estadísticas de uso
- Acciones rápidas para cifrar/desifrar
- Actividad reciente
- Estado de seguridad

### 🔐 Cifrar
- Cifrado de texto con contraseña
- Interfaz intuitiva para entrada de datos
- Copia y comparte texto cifrado
- Información de seguridad

### 🔓 Desifrar
- Desifrado de texto con contraseña
- Soporte para pegar desde portapapeles
- Validación de formato FLORA
- Copia de texto desifrado

### 📁 Archivos
- Gestión de archivos cifrados
- Vista de detalles de archivos
- Acciones de cifrado/desifrado
- Eliminación segura

### 🛡️ Seguridad
- Puntuación de seguridad en tiempo real
- Configuración de medidas de seguridad
- Detección de amenazas
- Consejos de seguridad

### ⚙️ Configuración
- Personalización de la app
- Gestión de datos
- Soporte y ayuda
- Información legal

## 🛠️ Instalación

### Prerrequisitos

- Node.js 16 o superior
- React Native CLI
- Android Studio (para Android)
- Xcode (para iOS)

### Pasos de Instalación

1. **Instalar dependencias:**
   ```bash
   npm install
   ```

2. **Configurar Android:**
   ```bash
   npx react-native run-android
   ```

3. **Configurar iOS:**
   ```bash
   npx react-native run-ios
   ```

## 🔧 Configuración del Proyecto

### Estructura de Archivos

```
src/
├── screens/
│   ├── HomeScreen.tsx          # Pantalla principal
│   ├── EncryptScreen.tsx       # Cifrado de texto
│   ├── DecryptScreen.tsx       # Desifrado de texto
│   ├── FilesScreen.tsx         # Gestión de archivos
│   ├── SecurityScreen.tsx      # Centro de seguridad
│   └── SettingsScreen.tsx      # Configuración
├── components/                 # Componentes reutilizables
├── utils/                      # Utilidades y helpers
└── types/                      # Definiciones de tipos
```

### Dependencias Principales

- **React Native**: Framework base
- **React Navigation**: Navegación entre pantallas
- **AsyncStorage**: Almacenamiento local
- **React Native Vector Icons**: Iconografía
- **React Native Linear Gradient**: Gradientes
- **React Native Keychain**: Almacenamiento seguro

## 🔐 Seguridad

### Medidas Implementadas

- **Cifrado Local**: Todos los datos se cifran localmente
- **Almacenamiento Seguro**: Uso de Keychain para datos sensibles
- **Validación de Entrada**: Validación robusta de datos de usuario
- **Auditoría**: Registro de actividades de seguridad

### Configuración de Seguridad

- Autenticación biométrica
- Bloqueo automático
- Modo seguro
- Cifrado de datos
- Registro de auditoría

## 📊 Estadísticas y Monitoreo

La app incluye un sistema de monitoreo que rastrea:

- Archivos cifrados
- Sesiones de uso
- Nivel de seguridad
- Actividad reciente
- Amenazas detectadas

## 🎨 Personalización

### Temas Disponibles

- Por defecto
- Oscuro
- Azul
- Verde

### Idiomas Soportados

- Español (es)
- English (en)
- Français (fr)

## 🚀 Scripts Disponibles

```bash
# Desarrollo
npm start                    # Iniciar Metro bundler
npm run android             # Ejecutar en Android
npm run ios                 # Ejecutar en iOS

# Construcción
npm run build-android       # Build para Android
npm run build-ios           # Build para iOS

# Calidad
npm test                    # Ejecutar tests
npm run lint               # Linter
```

## 🔄 Integración con FLORA

La app móvil se integra con el sistema FLORA mediante:

- **Motor de Cifrado**: Uso del motor Rust de FLORA
- **Protocolos Seguros**: Implementación de protocolos post-cuánticos
- **Sincronización**: Sincronización segura entre dispositivos
- **APIs**: Integración con APIs de FLORA

## 📱 Compatibilidad

### Android
- Mínimo: API 21 (Android 5.0)
- Recomendado: API 30+ (Android 11+)

### iOS
- Mínimo: iOS 11.0
- Recomendado: iOS 14.0+

## 🐛 Solución de Problemas

### Problemas Comunes

1. **Error de Metro Bundler:**
   ```bash
   npx react-native start --reset-cache
   ```

2. **Error de Android:**
   ```bash
   cd android && ./gradlew clean
   ```

3. **Error de iOS:**
   ```bash
   cd ios && xcodebuild clean
   ```

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Para soporte técnico:

- Email: support@flora.app
- Sitio Web: https://flora.app/support
- GitHub Issues: [Crear issue](https://github.com/flora-app/mobile/issues)

---

**FLORA** - Protegiendo la privacidad digital con cifrado post-cuántico 🌸

