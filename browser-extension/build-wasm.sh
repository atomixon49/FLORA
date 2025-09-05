#!/bin/bash
# FLORA Browser Extension - Build WebAssembly

echo "🌸 Building FLORA WebAssembly for Browser Extension"

# Verificar que Rust está instalado
if ! command -v rustc &> /dev/null; then
    echo "❌ Rust no está instalado. Instala desde https://rustup.rs/"
    exit 1
fi

# Verificar que wasm-pack está instalado
if ! command -v wasm-pack &> /dev/null; then
    echo "📦 Instalando wasm-pack..."
    cargo install wasm-pack
fi

# Navegar al directorio del proyecto WASM
cd ../src/rust/flora-wasm

echo "🔨 Compilando Rust a WebAssembly..."

# Compilar con wasm-pack
wasm-pack build --target web --out-dir ../../../browser-extension/pkg

if [ $? -eq 0 ]; then
    echo "✅ WebAssembly compilado exitosamente"
    echo "📁 Archivos generados en: browser-extension/pkg/"
    
    # Mover archivos a la ubicación correcta
    cp ../../../browser-extension/pkg/flora_wasm.js ../../../browser-extension/
    cp ../../../browser-extension/pkg/flora_wasm_bg.wasm ../../../browser-extension/flora-wasm.wasm
    
    echo "📋 Archivos listos para la extensión:"
    echo "   - flora-wasm.js"
    echo "   - flora-wasm.wasm"
    
else
    echo "❌ Error compilando WebAssembly"
    exit 1
fi

echo "🌸 Build completado"

