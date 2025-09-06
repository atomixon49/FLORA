#!/bin/bash
# FLORA Workflow Verification Script

echo "🔍 Verificando workflow de GitHub Actions..."

# Verificar que el archivo existe
if [ ! -f "flora/.github/workflows/ci-cd.yml" ]; then
    echo "❌ Workflow no encontrado en ubicación correcta"
    exit 1
fi

echo "✅ Workflow encontrado"

# Verificar versiones de actions
echo "🔍 Verificando versiones de actions..."

# Checkout v4
if grep -q "actions/checkout@v4" flora/.github/workflows/ci-cd.yml; then
    echo "✅ actions/checkout@v4"
else
    echo "❌ actions/checkout no está en v4"
fi

# Setup Python v5
if grep -q "actions/setup-python@v5" flora/.github/workflows/ci-cd.yml; then
    echo "✅ actions/setup-python@v5"
else
    echo "❌ actions/setup-python no está en v5"
fi

# Upload Artifact v4
if grep -q "actions/upload-artifact@v4" flora/.github/workflows/ci-cd.yml; then
    echo "✅ actions/upload-artifact@v4"
else
    echo "❌ actions/upload-artifact no está en v4"
fi

# Fail-fast false
if grep -q "fail-fast: false" flora/.github/workflows/ci-cd.yml; then
    echo "✅ fail-fast: false configurado"
else
    echo "❌ fail-fast no está configurado"
fi

# Retention days
if grep -q "retention-days:" flora/.github/workflows/ci-cd.yml; then
    echo "✅ retention-days configurado"
else
    echo "❌ retention-days no está configurado"
fi

echo "🎉 Verificación completada"
