# FLORA Mobile App - Test Installation Script
# PowerShell script para probar la aplicación móvil

Write-Host "🌸 FLORA Mobile App - Instalación de Prueba" -ForegroundColor Magenta
Write-Host "===============================================" -ForegroundColor Magenta

# Verificar si Node.js está instalado
Write-Host "`n🔍 Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js encontrado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js no encontrado. Instala Node.js desde https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Verificar si npm está instalado
Write-Host "`n🔍 Verificando npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "✅ npm encontrado: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm no encontrado" -ForegroundColor Red
    exit 1
}

# Crear directorio de prueba
Write-Host "`n📁 Creando directorio de prueba..." -ForegroundColor Yellow
$testDir = "flora-test-app"
if (Test-Path $testDir) {
    Remove-Item $testDir -Recurse -Force
}
New-Item -ItemType Directory -Path $testDir | Out-Null
Set-Location $testDir

# Crear package.json para prueba
Write-Host "`n📦 Creando package.json..." -ForegroundColor Yellow
$packageJson = @"
{
  "name": "flora-test-app",
  "version": "1.0.0",
  "description": "FLORA Test App",
  "main": "test-app.js",
  "scripts": {
    "start": "npx expo start",
    "android": "npx expo start --android",
    "ios": "npx expo start --ios",
    "web": "npx expo start --web"
  },
  "dependencies": {
    "expo": "~49.0.0",
    "react": "18.2.0",
    "react-native": "0.72.6",
    "expo-status-bar": "~1.6.0"
  },
  "devDependencies": {
    "@babel/core": "^7.20.0"
  },
  "private": true
}
"@

$packageJson | Out-File -FilePath "package.json" -Encoding UTF8

# Crear app.json para Expo
Write-Host "`n⚙️ Creando configuración de Expo..." -ForegroundColor Yellow
$appJson = @"
{
  "expo": {
    "name": "FLORA Test",
    "slug": "flora-test",
    "version": "1.0.0",
    "orientation": "portrait",
    "userInterfaceStyle": "light",
    "splash": {
      "resizeMode": "contain",
      "backgroundColor": "#667eea"
    },
    "assetBundlePatterns": [
      "**/*"
    ],
    "ios": {
      "supportsTablet": true
    },
    "android": {
      "adaptiveIcon": {
        "backgroundColor": "#667eea"
      }
    },
    "web": {
      "favicon": "./assets/favicon.png"
    }
  }
}
"@

$appJson | Out-File -FilePath "app.json" -Encoding UTF8

# Copiar el archivo de prueba
Write-Host "`n📋 Copiando aplicación de prueba..." -ForegroundColor Yellow
Copy-Item "../test-app.js" -Destination "App.js"

# Instalar dependencias
Write-Host "`n📥 Instalando dependencias..." -ForegroundColor Yellow
Write-Host "Esto puede tomar unos minutos..." -ForegroundColor Cyan
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
} else {
    Write-Host "❌ Error al instalar dependencias" -ForegroundColor Red
    exit 1
}

# Crear script de inicio
Write-Host "`n🚀 Creando script de inicio..." -ForegroundColor Yellow
$startScript = @"
# FLORA Test App - Script de Inicio
Write-Host "🌸 Iniciando FLORA Test App..." -ForegroundColor Magenta
Write-Host "`nOpciones disponibles:" -ForegroundColor Yellow
Write-Host "1. Web (navegador)" -ForegroundColor Cyan
Write-Host "2. Android (requiere Android Studio)" -ForegroundColor Cyan
Write-Host "3. iOS (requiere Xcode)" -ForegroundColor Cyan
Write-Host "`nPresiona Ctrl+C para salir" -ForegroundColor Red
Write-Host "`nIniciando servidor de desarrollo..." -ForegroundColor Green
npx expo start
"@

$startScript | Out-File -FilePath "start.ps1" -Encoding UTF8

# Crear README de prueba
Write-Host "`n📖 Creando documentación..." -ForegroundColor Yellow
$readme = @"
# 🌸 FLORA Test App

Aplicación de prueba para FLORA Mobile.

## 🚀 Cómo usar

1. **Iniciar la aplicación:**
   ```powershell
   .\start.ps1
   ```

2. **O usar comandos directos:**
   ```bash
   npm start          # Iniciar servidor
   npm run web        # Abrir en navegador
   npm run android    # Abrir en Android
   npm run ios        # Abrir en iOS
   ```

## 📱 Funcionalidades de Prueba

- ✅ Cifrado de texto
- ✅ Desifrado de texto
- ✅ Interfaz simple
- ✅ Validación de entrada
- ✅ Manejo de errores

## 🔧 Requisitos

- Node.js 16+
- Navegador web (para prueba web)
- Android Studio (para Android)
- Xcode (para iOS)

## 📞 Soporte

Si tienes problemas, verifica:
1. Node.js está instalado
2. Las dependencias se instalaron correctamente
3. El puerto 8081 está disponible
"@

$readme | Out-File -FilePath "README.md" -Encoding UTF8

Write-Host "`n🎉 ¡Instalación completada!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host "`n📱 Para probar la aplicación:" -ForegroundColor Yellow
Write-Host "1. Ejecuta: .\start.ps1" -ForegroundColor Cyan
Write-Host "2. O ejecuta: npm start" -ForegroundColor Cyan
Write-Host "3. Escanea el código QR con Expo Go" -ForegroundColor Cyan
Write-Host "4. O presiona 'w' para abrir en navegador" -ForegroundColor Cyan

Write-Host "`n📁 Archivos creados:" -ForegroundColor Yellow
Write-Host "• package.json - Configuración del proyecto" -ForegroundColor White
Write-Host "• app.json - Configuración de Expo" -ForegroundColor White
Write-Host "• App.js - Aplicación de prueba" -ForegroundColor White
Write-Host "• start.ps1 - Script de inicio" -ForegroundColor White
Write-Host "• README.md - Documentación" -ForegroundColor White

Write-Host "`n🌸 ¡FLORA está listo para probar!" -ForegroundColor Magenta

