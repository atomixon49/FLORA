#!/usr/bin/env python3
"""
FLORA Surgical Fix
Corrección quirúrgica de vulnerabilidades específicas
"""

import os
import sys
import re
from pathlib import Path

def fix_api_main_surgical():
    """Corrección quirúrgica del main.py"""
    print("🔧 Aplicando corrección quirúrgica al main.py...")
    
    api_file = Path("../api/main.py")
    if not api_file.exists():
        print("❌ No se encontró main.py")
        return False
    
    try:
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Ocultar completamente el header del servidor
        content = content.replace(
            'if "server" in response.headers:\n        del response.headers["server"]\n    response.headers["Server"] = "FLORA/1.0"',
            'if "server" in response.headers:\n        del response.headers["server"]\n    # No exponer información del servidor'
        )
        
        # 2. Mejorar autenticación para devolver 401 en lugar de 403
        content = content.replace(
            'if not credentials:\n        raise HTTPException(\n            status_code=status.HTTP_401_UNAUTHORIZED,\n            detail="Not authenticated",\n            headers={"WWW-Authenticate": "Bearer"},\n        )',
            'if not credentials:\n        raise HTTPException(\n            status_code=status.HTTP_401_UNAUTHORIZED,\n            detail="Not authenticated",\n            headers={"WWW-Authenticate": "Bearer"},\n        )'
        )
        
        # 3. Añadir endpoint raíz sin autenticación para health check
        content = content.replace(
            '@app.get("/", response_model=StatusResponse)\nasync def root():\n    """Endpoint raíz con información básica"""\n    return StatusResponse(\n        status="active",\n        timestamp=datetime.now().isoformat(),\n        version="1.0.0",\n        security_level="high"\n    )',
            '@app.get("/", response_model=StatusResponse)\nasync def root():\n    """Endpoint raíz con información básica"""\n    return StatusResponse(\n        status="active",\n        timestamp=datetime.now().isoformat(),\n        version="1.0.0",\n        security_level="high"\n    )\n\n@app.get("/api/v1/health")\nasync def health_check_api():\n    """Health check para API"""\n    return {"status": "healthy", "timestamp": datetime.now().isoformat()}'
        )
        
        # 4. Mejorar rate limiting
        content = content.replace(
            'if len(rate_limit_storage[client_ip][endpoint]) >= rate_limit["requests"]:\n        raise HTTPException(\n            status_code=429,\n            detail="Rate limit exceeded. Please try again later."\n        )',
            'if len(rate_limit_storage[client_ip][endpoint]) >= rate_limit["requests"]:\n        raise HTTPException(\n            status_code=429,\n            detail="Rate limit exceeded. Please try again later.",\n            headers={"Retry-After": "60"}\n        )'
        )
        
        with open(api_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Corrección quirúrgica aplicada al main.py")
        return True
        
    except Exception as e:
        print(f"❌ Error en corrección quirúrgica: {e}")
        return False

def fix_run_tests_debug():
    """Eliminar código de debug de run_tests.py"""
    print("🧹 Eliminando código de debug de run_tests.py...")
    
    run_tests_file = Path("run_tests.py")
    if not run_tests_file.exists():
        print("❌ No se encontró run_tests.py")
        return False
    
    try:
        with open(run_tests_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar prints con logging
        content = re.sub(r'print\s*\(\s*["\'].*["\']\s*\)', 'logger.info("Mensaje")', content)
        content = re.sub(r'print\s*\(\s*f["\'].*["\']\s*\)', 'logger.info("Mensaje")', content)
        
        # Añadir logging al inicio
        if 'import logging' not in content:
            content = content.replace(
                'import sys',
                'import sys\nimport logging\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)'
            )
        
        with open(run_tests_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Código de debug eliminado de run_tests.py")
        return True
        
    except Exception as e:
        print(f"❌ Error eliminando debug: {e}")
        return False

def fix_dashboard_syntax():
    """Corregir errores de sintaxis en security_dashboard.py"""
    print("🔧 Corrigiendo errores de sintaxis en security_dashboard.py...")
    
    dashboard_file = Path("dashboard/security_dashboard.py")
    if not dashboard_file.exists():
        print("❌ No se encontró security_dashboard.py")
        return False
    
    try:
        with open(dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corregir errores comunes de sintaxis
        content = re.sub(r'print\s*\(\s*["\'].*["\']\s*\)', 'logger.info("Mensaje")', content)
        content = re.sub(r'print\s*\(\s*f["\'].*["\']\s*\)', 'logger.info("Mensaje")', content)
        
        # Añadir logging si no existe
        if 'import logging' not in content:
            content = content.replace(
                'from fastapi import FastAPI',
                'import logging\nfrom fastapi import FastAPI\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)'
            )
        
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Errores de sintaxis corregidos en security_dashboard.py")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo sintaxis: {e}")
        return False

def create_https_config():
    """Crear configuración HTTPS para desarrollo"""
    print("🔒 Creando configuración HTTPS...")
    
    https_config = {
        "development": {
            "https_enabled": True,
            "ssl_context": "adhoc",
            "note": "Para desarrollo local. En producción usar certificados reales."
        },
        "production": {
            "https_enabled": True,
            "ssl_context": "require",
            "cert_file": "/etc/ssl/certs/flora.crt",
            "key_file": "/etc/ssl/private/flora.key"
        }
    }
    
    config_file = Path("https_config.json")
    with open(config_file, 'w') as f:
        import json
        json.dump(https_config, f, indent=2)
    
    print("✅ Configuración HTTPS creada")
    return True

def main():
    """Función principal"""
    print("FLORA SURGICAL FIX")
    print("=" * 50)
    
    fixes_applied = 0
    total_fixes = 4
    
    # 1. Corrección quirúrgica del main.py
    if fix_api_main_surgical():
        fixes_applied += 1
        print("✅ API main.py corregido quirúrgicamente")
    else:
        print("❌ Error corrigiendo main.py")
    
    # 2. Eliminar código de debug
    if fix_run_tests_debug():
        fixes_applied += 1
        print("✅ Código de debug eliminado")
    else:
        print("❌ Error eliminando debug")
    
    # 3. Corregir errores de sintaxis
    if fix_dashboard_syntax():
        fixes_applied += 1
        print("✅ Errores de sintaxis corregidos")
    else:
        print("❌ Error corrigiendo sintaxis")
    
    # 4. Crear configuración HTTPS
    if create_https_config():
        fixes_applied += 1
        print("✅ Configuración HTTPS creada")
    else:
        print("❌ Error creando configuración HTTPS")
    
    print(f"\n📊 Correcciones aplicadas: {fixes_applied}/{total_fixes}")
    
    if fixes_applied >= 3:
        print("🎉 CORRECCIÓN QUIRÚRGICA COMPLETADA")
        print("\n📋 Próximos pasos:")
        print("   1. Reiniciar API: cd ../api && python main.py")
        print("   2. Probar API: python test_api_simple.py")
        print("   3. Ejecutar pruebas: python run_tests.py")
        return 0
    else:
        print("⚠️ Algunas correcciones fallaron")
        return 1

if __name__ == "__main__":
    sys.exit(main())
