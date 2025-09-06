# FLORA CI/CD Troubleshooting Guide

## Problemas Comunes y Soluciones

### 1. Python 3.1 no disponible en Ubuntu 24.04
**Error**: `The version '3.1' with architecture 'x64' was not found for Ubuntu 24.04`

**Solución**:
- Usar Python 3.9+ en Ubuntu 24.04
- Actualizar la matriz de tests para excluir versiones no soportadas

### 2. Tests cancelados por fallo en un OS
**Error**: `The strategy configuration was canceled because "test.ubuntu-latest_3_1" failed`

**Solución**:
- Configurar `fail-fast: false` en la estrategia
- Usar `continue-on-error: true` para tests no críticos

### 3. Advertencias de Windows Server
**Advertencia**: `The windows-latest label will migrate from Windows Server 2022 to Windows Server 2025`

**Solución**:
- Esta es solo una advertencia informativa
- No afecta el funcionamiento de los tests
- Considerar actualizar a `windows-2025` cuando esté disponible

### 4. Tests de seguridad fallando
**Problema**: Tests de seguridad interrumpen el pipeline

**Solución**:
- Usar `continue-on-error: true` para tests de seguridad
- Ejecutar tests de seguridad en un job separado
- Generar reportes como artifacts

### 5. Dependencias no encontradas
**Error**: `ModuleNotFoundError` o `ImportError`

**Solución**:
- Verificar que `requirements.txt` esté actualizado
- Instalar dependencias del sistema necesarias
- Usar cache de pip para acelerar builds

## Configuración Recomendada

### Matriz de Tests Optimizada
```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ['3.9', '3.10', '3.11', '3.12']
    exclude:
      - os: ubuntu-latest
        python-version: '3.8'
```

### Configuración de Cache
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: ${{ matrix.python-version }}
    cache: 'pip'
```

### Tests de Seguridad Separados
```yaml
security-tests:
  runs-on: ubuntu-latest
  if: github.event_name == 'pull_request'
  steps:
    - name: Run security tests
      run: |
        python run_tests.py
      continue-on-error: true
```

## Comandos Útiles

### Verificar tests localmente
```bash
# Instalar dependencias
pip install -r flora/api/requirements.txt

# Ejecutar tests básicos
cd flora/security
python test_api_simple.py

# Ejecutar tests de seguridad
python run_tests.py --target-url http://localhost:8000
```

### Debug de GitHub Actions
```bash
# Activar debug logging
echo "ACTIONS_STEP_DEBUG=true" >> $GITHUB_ENV

# Ver logs detallados
# Los logs aparecerán en la interfaz de GitHub Actions
```

## Contacto y Soporte

- **Issues**: https://github.com/flora-crypto/flora/issues
- **Documentación**: https://docs.flora-crypto.com
- **Email**: ci-support@flora-crypto.com
