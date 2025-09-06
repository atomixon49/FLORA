#!/usr/bin/env python3
"""
FLORA Syntax Fix Complete
Corregir todos los errores de sintaxis en run_tests.py
"""

import re
from pathlib import Path

def fix_run_tests_syntax():
    """Corregir todos los errores de sintaxis en run_tests.py"""
    print("🔧 Corrigiendo errores de sintaxis...")
    
    run_tests_file = Path("run_tests.py")
    if not run_tests_file.exists():
        print("❌ No se encontró run_tests.py")
        return False
    
    try:
        with open(run_tests_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corregir cadenas de texto mal formadas
        content = re.sub(r'print\("\\n\n([^"]+)"\)', r'print("\\n\1")', content)
        content = re.sub(r'print\("\\n\n([^"]+)"\)', r'print("\\n\1")', content)
        
        # Corregir mensajes específicos
        content = content.replace('print("\\n\n📋 EJECUTANDO VERIFICACIÓN DE COMPLIANCE")', 'print("\\n📋 EJECUTANDO VERIFICACIÓN DE COMPLIANCE")')
        content = content.replace('print("\\n\n🔒 EJECUTANDO PRUEBAS DE PENETRACIÓN")', 'print("\\n🔒 EJECUTANDO PRUEBAS DE PENETRACIÓN")')
        content = content.replace('print("\\n\n🛡️ EJECUTANDO ESCANEO DE VULNERABILIDADES")', 'print("\\n🛡️ EJECUTANDO ESCANEO DE VULNERABILIDADES")')
        content = content.replace('print("\\n\n📊 RESUMEN FINAL")', 'print("\\n📊 RESUMEN FINAL")')
        
        # Corregir líneas de separación
        content = content.replace('print("\\n=" * 50)', 'print("=" * 50)')
        
        # Reemplazar mensajes genéricos con mensajes específicos
        content = content.replace('print("\\n✅ Operación completada")', 'print("✅ Operación completada")')
        
        with open(run_tests_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Errores de sintaxis corregidos")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo sintaxis: {e}")
        return False

def main():
    """Función principal"""
    print("FLORA SYNTAX FIX COMPLETE")
    print("=" * 40)
    
    if fix_run_tests_syntax():
        print("✅ Sintaxis corregida exitosamente")
        print("\n📋 Próximos pasos:")
        print("   1. Ejecutar pruebas: python run_tests.py")
        return 0
    else:
        print("❌ Error corrigiendo sintaxis")
        return 1

if __name__ == "__main__":
    main()
