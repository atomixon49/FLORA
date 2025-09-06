#!/usr/bin/env python3
"""
FLORA Security Verify Fix
Script para verificar que las correcciones funcionan
"""

import sys
import os
from pathlib import Path

def verify_imports():
    """Verificar que las importaciones funcionan"""
    print("🔍 Verificando importaciones...")
    
    try:
        # Verificar security_auditor
        from audit.security_auditor import SecurityAuditor, create_security_auditor
        print("✅ SecurityAuditor importado correctamente")
        
        # Verificar compliance_manager
        from compliance.compliance_manager import ComplianceManager, create_compliance_manager
        print("✅ ComplianceManager importado correctamente")
        
        # Verificar penetration_tester
        from testing.penetration_tester import PenetrationTester, run_penetration_test
        print("✅ PenetrationTester importado correctamente")
        
        # Verificar vulnerability_scanner
        from testing.vulnerability_scanner import VulnerabilityScanner, scan_vulnerabilities
        print("✅ VulnerabilityScanner importado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def verify_syntax():
    """Verificar sintaxis de archivos Python"""
    print("🔍 Verificando sintaxis...")
    
    python_files = [
        "audit/security_auditor.py",
        "compliance/compliance_manager.py", 
        "testing/penetration_tester.py",
        "testing/vulnerability_scanner.py",
        "__init__.py"
    ]
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Compilar para verificar sintaxis
            compile(content, file_path, 'exec')
            print(f"✅ {file_path} - Sintaxis correcta")
            
        except SyntaxError as e:
            print(f"❌ {file_path} - Error de sintaxis: {e}")
            return False
        except Exception as e:
            print(f"⚠️ {file_path} - Error: {e}")
    
    return True

def test_basic_functionality():
    """Probar funcionalidad básica"""
    print("🔍 Probando funcionalidad básica...")
    
    try:
        # Probar SecurityAuditor
        from audit.security_auditor import SecurityAuditor, OperationType
        auditor = SecurityAuditor()
        event_id = auditor.log_operation(OperationType.ENCRYPT, user_id="test", success=True)
        print(f"✅ SecurityAuditor - Evento creado: {event_id}")
        
        # Probar ComplianceManager
        from compliance.compliance_manager import ComplianceManager
        manager = ComplianceManager()
        dashboard = manager.get_compliance_dashboard()
        print(f"✅ ComplianceManager - Dashboard generado: {len(dashboard)} estándares")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en funcionalidad: {e}")
        return False

def main():
    """Función principal"""
    # print("FLORA Security Verify Fix")
    print("=" * 40)
    
    # Cambiar al directorio correcto
    os.chdir(Path(__file__).parent)
    
    # 1. Verificar sintaxis
    if not verify_syntax():
        print("\n❌ Errores de sintaxis encontrados")
        return 1
    
    # 2. Verificar importaciones
    if not verify_imports():
        print("\n❌ Errores de importación encontrados")
        return 1
    
    # 3. Probar funcionalidad
    if not test_basic_functionality():
        print("\n❌ Errores de funcionalidad encontrados")
        return 1
    
    print("\n🎉 Todas las verificaciones pasaron exitosamente")
    print("✅ Los archivos están corregidos y funcionando")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
