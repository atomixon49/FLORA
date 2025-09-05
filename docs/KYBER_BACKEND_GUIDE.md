# Guía: Backend Kyber para FLORA

Esta guía explica cómo habilitar Kyber KEM como backend opcional en FLORA.

## Opción A: pqcrypto (recomendado si está disponible)

1. Instalar
```bash
pip install pqcrypto
```

2. Verificar instalación
```python
from pqcrypto.kem import kyber512
pk, sk = kyber512.generate_keypair()
ct, ss = kyber512.encrypt(pk)
ss2 = kyber512.decrypt(ct, sk)
assert ss == ss2
```

3. Uso en FLORA
- FLORA detecta `pqcrypto.kem.kyber512` automáticamente.
- Activar en CLI con `--use-kyber` (ya es default) o en código con `FloraCryptoSystem(use_kyber=True)`.

## Opción B: pykyber (si existe en tu ecosistema)

1. Instalar (el nombre del paquete puede variar según distribución/lab)
```bash
pip install pykyber  # o nombre equivalente
```

2. Verificar
```python
import pykyber as kyb
pk, sk = kyb.generate_keypair()
ct, ss = kyb.encrypt(pk)
ss2 = kyb.decrypt(sk, ct)
assert ss == ss2
```

3. Uso en FLORA
- FLORA intenta `import pykyber` como primer backend.

## Comprobación en FLORA
```python
from flora import FloraCryptoSystem
flora = FloraCryptoSystem(use_kyber=True)
print("Kyber habilitado:", bool(getattr(flora, 'kyber_enabled', False)))
```

## Notas y compatibilidad
- Si no hay backend Kyber disponible, FLORA hace fallback a `PBKDF2 + AES-GCM` automáticamente.
- Para despliegues reproducibles, congela dependencias con `requirements.txt` o `poetry.lock`.

## Seguridad
- Kyber aporta encapsulamiento post-cuántico de la clave de sesión.
- Se recomienda aplicar un KDF (SHA-256 aplicado ya en FLORA) sobre `ss` antes de usar como clave.

## Soporte
- Issues: abrir un ticket en el repositorio con detalles de tu entorno OS/Python.




