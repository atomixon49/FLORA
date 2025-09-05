# FLORA Mobile App - Quick Test
Write-Host "🌸 FLORA Mobile App - Prueba Rápida" -ForegroundColor Magenta
Write-Host "=====================================" -ForegroundColor Magenta

# Verificar Node.js
Write-Host "`n🔍 Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js encontrado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js no encontrado. Instala desde https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Crear directorio de prueba
Write-Host "`n📁 Creando directorio de prueba..." -ForegroundColor Yellow
$testDir = "flora-test"
if (Test-Path $testDir) {
    Remove-Item $testDir -Recurse -Force
}
New-Item -ItemType Directory -Path $testDir | Out-Null
Set-Location $testDir

# Crear package.json
Write-Host "`n📦 Creando package.json..." -ForegroundColor Yellow
@"
{
  "name": "flora-test",
  "version": "1.0.0",
  "main": "App.js",
  "scripts": {
    "start": "npx expo start",
    "web": "npx expo start --web"
  },
  "dependencies": {
    "expo": "~49.0.0",
    "react": "18.2.0",
    "react-native": "0.72.6"
  }
}
"@ | Out-File -FilePath "package.json" -Encoding UTF8

# Crear app.json
@"
{
  "expo": {
    "name": "FLORA Test",
    "slug": "flora-test",
    "version": "1.0.0",
    "orientation": "portrait"
  }
}
"@ | Out-File -FilePath "app.json" -Encoding UTF8

# Copiar App.js
Write-Host "`n📋 Copiando aplicación..." -ForegroundColor Yellow
Copy-Item "../test-app.js" -Destination "App.js"

# Instalar dependencias
Write-Host "`n📥 Instalando dependencias..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Instalación completada!" -ForegroundColor Green
    Write-Host "`n🚀 Para probar:" -ForegroundColor Yellow
    Write-Host "1. Ejecuta: npm start" -ForegroundColor Cyan
    Write-Host "2. Presiona 'w' para abrir en navegador" -ForegroundColor Cyan
    Write-Host "3. O escanea el QR con Expo Go" -ForegroundColor Cyan
} else {
    Write-Host "❌ Error en la instalación" -ForegroundColor Red
}

