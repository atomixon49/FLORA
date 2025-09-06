# GitHub Actions Migration Guide

## Migración de Actions Deprecadas

### 1. actions/upload-artifact@v3 → v4

**Cambios principales:**
- Nuevo parámetro `retention-days` (por defecto 90 días)
- Mejor manejo de archivos grandes
- Soporte mejorado para paths con wildcards

**Antes (v3):**
```yaml
- name: Upload reports
  uses: actions/upload-artifact@v3
  with:
    name: security-reports
    path: |
      bandit-report.json
      safety-report.json
```

**Después (v4):**
```yaml
- name: Upload reports
  uses: actions/upload-artifact@v4
  with:
    name: security-reports
    path: |
      bandit-report.json
      safety-report.json
    retention-days: 7
```

### 2. actions/setup-python@v4 → v5

**Cambios principales:**
- Mejor cache de pip
- Soporte para Python 3.13
- Mejor detección automática de versiones

**Antes (v4):**
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'
    cache: 'pip'
```

**Después (v5):**
```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'
```

### 3. actions/checkout@v3 → v4

**Cambios principales:**
- Mejor rendimiento
- Soporte para Git LFS mejorado
- Mejor manejo de submodules

**Antes (v3):**
```yaml
- uses: actions/checkout@v3
```

**Después (v4):**
```yaml
- uses: actions/checkout@v4
```

## Checklist de Migración

- [ ] Actualizar actions/checkout a v4
- [ ] Actualizar actions/setup-python a v5
- [ ] Actualizar actions/upload-artifact a v4
- [ ] Actualizar actions/download-artifact a v4
- [ ] Actualizar actions/cache a v4
- [ ] Probar en branch de desarrollo
- [ ] Verificar que todos los tests pasen
- [ ] Mergear a main

## Comandos Útiles

### Verificar versiones actuales
```bash
# Buscar actions deprecadas en workflows
grep -r "actions/.*@v[0-3]" .github/workflows/

# Buscar upload-artifact específicamente
grep -r "upload-artifact@v3" .github/workflows/
```

### Actualizar automáticamente
```bash
# Reemplazar upload-artifact v3 por v4
sed -i 's/upload-artifact@v3/upload-artifact@v4/g' .github/workflows/*.yml

# Reemplazar checkout v3 por v4
sed -i 's/checkout@v3/checkout@v4/g' .github/workflows/*.yml
```

## Troubleshooting

### Error: "This request has been automatically failed because it uses a deprecated version"
**Solución**: Actualizar la action a la versión más reciente

### Error: "retention-days is not a valid input"
**Solución**: Asegurarse de usar actions/upload-artifact@v4 o superior

### Error: "Cache not found"
**Solución**: Verificar que actions/cache esté en v4 o superior

## Recursos

- [GitHub Actions Changelog](https://github.blog/changelog/)
- [Actions Marketplace](https://github.com/marketplace?type=actions)
- [Migration Guide](https://docs.github.com/en/actions)
