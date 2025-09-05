@echo off
echo 🌸 FLORA Mobile App - Setup Test
echo =====================================

echo.
echo 🔍 Verificando Node.js...
node --version
if %errorlevel% neq 0 (
    echo ❌ Node.js no encontrado. Instala desde https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js encontrado

echo.
echo 📁 Creando directorio de prueba...
if exist flora-test rmdir /s /q flora-test
mkdir flora-test
cd flora-test

echo.
echo 📦 Creando package.json...
echo {> package.json
echo   "name": "flora-test",>> package.json
echo   "version": "1.0.0",>> package.json
echo   "main": "App.js",>> package.json
echo   "scripts": {>> package.json
echo     "start": "npx expo start",>> package.json
echo     "web": "npx expo start --web">> package.json
echo   },>> package.json
echo   "dependencies": {>> package.json
echo     "expo": "~49.0.0",>> package.json
echo     "react": "18.2.0",>> package.json
echo     "react-native": "0.72.6">> package.json
echo   }>> package.json
echo }>> package.json

echo.
echo ⚙️ Creando app.json...
echo {> app.json
echo   "expo": {>> app.json
echo     "name": "FLORA Test",>> app.json
echo     "slug": "flora-test",>> app.json
echo     "version": "1.0.0",>> app.json
echo     "orientation": "portrait">> app.json
echo   }>> app.json
echo }>> app.json

echo.
echo 📋 Copiando aplicación...
copy ..\test-app.js App.js

echo.
echo 📥 Instalando dependencias...
echo Esto puede tomar unos minutos...
npm install

if %errorlevel% equ 0 (
    echo.
    echo ✅ Instalación completada!
    echo.
    echo 🚀 Para probar:
    echo 1. Ejecuta: npm start
    echo 2. Presiona 'w' para abrir en navegador
    echo 3. O escanea el QR con Expo Go
    echo.
    echo Presiona cualquier tecla para iniciar...
    pause >nul
    npm start
) else (
    echo ❌ Error en la instalación
    pause
)

