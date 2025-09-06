#!/usr/bin/env python3
"""
FLORA Logging Fix
Corregir mensajes de logging en run_tests.py
"""

import re
from pathlib import Path

def fix_run_tests_logging():
    """Corregir mensajes de logging en run_tests.py"""
    print("🔧 Corrigiendo mensajes de logging...")
    
    run_tests_file = Path("run_tests.py")
    if not run_tests_file.exists():
        print("❌ No se encontró run_tests.py")
        return False
    
    try:
        with open(run_tests_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar todos los logger.info("Mensaje") con mensajes apropiados
        replacements = [
            (r'logger\.info\("Mensaje"\)\s*\n\s*print\("=" \* 50\)', 'print("\\n🔍 EJECUTANDO AUDITORÍA DE SEGURIDAD")\n    print("=" * 50)'),
            (r'logger\.info\("Mensaje"\)\s*\n\s*print\("=" \* 50\)', 'print("\\n📋 EJECUTANDO VERIFICACIÓN DE COMPLIANCE")\n    print("=" * 50)'),
            (r'logger\.info\("Mensaje"\)\s*\n\s*print\("=" \* 50\)', 'print("\\n🔒 EJECUTANDO PRUEBAS DE PENETRACIÓN")\n    print("=" * 50)'),
            (r'logger\.info\("Mensaje"\)\s*\n\s*print\("=" \* 50\)', 'print("\\n🛡️ EJECUTANDO ESCANEO DE VULNERABILIDADES")\n    print("=" * 50)'),
            (r'logger\.info\("Mensaje"\)\s*\n\s*print\("=" \* 50\)', 'print("\\n📊 RESUMEN FINAL")\n    print("=" * 50)'),
            (r'logger\.info\("Mensaje")', 'print("✅ Operación completada")'),
        ]
        
        # Aplicar reemplazos específicos
        content = re.sub(r'logger\.info\("Mensaje"\)\s*\n\s*print\("=" \* 50\)', 'print("\\n🔍 EJECUTANDO AUDITORÍA DE SEGURIDAD")\n    print("=" * 50)', content, count=1)
        content = re.sub(r'logger\.info\("Mensaje"\)\s*\n\s*print\("=" \* 50\)', 'print("\\n📋 EJECUTANDO VERIFICACIÓN DE COMPLIANCE")\n    print("=" * 50)', content, count=1)
        content = re.sub(r'logger\.info\("Mensaje"\)\s*\n\s*print\("=" \* 50\)', 'print("\\n🔒 EJECUTANDO PRUEBAS DE PENETRACIÓN")\n    print("=" * 50)', content, count=1)
        content = re.sub(r'logger\.info\("Mensaje"\)\s*\n\s*print\("=" \* 50\)', 'print("\\n🛡️ EJECUTANDO ESCANEO DE VULNERABILIDADES")\n    print("=" * 50)', content, count=1)
        content = re.sub(r'logger\.info\("Mensaje"\)\s*\n\s*print\("=" \* 50\)', 'print("\\n📊 RESUMEN FINAL")\n    print("=" * 50)', content, count=1)
        
        # Reemplazar los logger.info("Mensaje") restantes
        content = re.sub(r'logger\.info\("Mensaje"\)', 'print("✅ Operación completada")', content)
        
        with open(run_tests_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Mensajes de logging corregidos")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo logging: {e}")
        return False

def main():
    """Función principal"""
    print("FLORA LOGGING FIX")
    print("=" * 30)
    
    if fix_run_tests_logging():
        print("✅ Logging corregido exitosamente")
        print("\n📋 Próximos pasos:")
        print("   1. Ejecutar pruebas: python run_tests.py")
        return 0
    else:
        print("❌ Error corrigiendo logging")
        return 1

if __name__ == "__main__":
    main()
