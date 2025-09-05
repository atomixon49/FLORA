@echo off
REM FLORA Browser Extension - Build WebAssembly (Windows)

echo 🌸 Building FLORA WebAssembly for Browser Extension

REM Verificar que Rust está instalado
rustc --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Rust no está instalado. Instala desde https://rustup.rs/
    exit /b 1
)

REM Verificar que wasm-pack está instalado
wasm-pack --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Instalando wasm-pack...
    cargo install wasm-pack
)

REM Navegar al directorio del proyecto WASM
cd ..\..\src\rust\flora-wasm

echo 🔨 Compilando Rust a WebAssembly...

REM Compilar con wasm-pack
wasm-pack build --target web --out-dir ..\..\..\browser-extension\pkg

if %errorlevel% equ 0 (
    echo ✅ WebAssembly compilado exitosamente
    echo 📁 Archivos generados en: browser-extension\pkg\
    
    REM Mover archivos a la ubicación correcta
    copy ..\..\..\browser-extension\pkg\flora_wasm.js ..\..\..\browser-extension\
    copy ..\..\..\browser-extension\pkg\flora_wasm_bg.wasm ..\..\..\browser-extension\flora-wasm.wasm
    
    echo 📋 Archivos listos para la extensión:
    echo    - flora-wasm.js
    echo    - flora-wasm.wasm
    
) else (
    echo ❌ Error compilando WebAssembly
    exit /b 1
)

echo 🌸 Build completado
pause

