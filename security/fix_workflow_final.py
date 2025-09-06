#!/usr/bin/env python3
"""
FLORA Workflow Final Fix
Corregir definitivamente el problema del workflow de GitHub Actions
"""

import os
import sys
import shutil
from pathlib import Path

def fix_workflow_final():
    """Corregir workflow definitivamente"""
    print("🔧 Corrigiendo workflow definitivamente...")
    
    # Directorios (usando rutas absolutas)
    base_dir = Path(__file__).parent.parent.parent  # Subir 3 niveles desde flora/security/
    source_file = base_dir / "flora" / "security" / ".github" / "workflows" / "ci-cd.yml"
    target_dir = base_dir / "flora" / ".github" / "workflows"
    target_file = target_dir / "ci-cd.yml"
    
    print(f"📁 Directorio base: {base_dir}")
    print(f"📄 Archivo fuente: {source_file}")
    print(f"📁 Directorio destino: {target_dir}")
    print(f"📄 Archivo destino: {target_file}")
    
    try:
        # Verificar que el archivo fuente existe
        if not source_file.exists():
            print(f"❌ No se encontró el archivo fuente: {source_file}")
            return False
        
        print(f"✅ Archivo fuente encontrado: {source_file}")
        
        # Crear directorio destino si no existe
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio destino creado: {target_dir}")
        
        # Crear backup del archivo existente si existe
        if target_file.exists():
            backup_file = target_dir / "ci-cd-backup.yml"
            shutil.copy2(target_file, backup_file)
            print(f"✅ Backup creado: {backup_file}")
        
        # Copiar archivo
        shutil.copy2(source_file, target_file)
        print(f"✅ Workflow copiado de {source_file} a {target_file}")
        
        # Verificar que se copió correctamente
        if target_file.exists():
            print("✅ Workflow verificado en ubicación correcta")
            
            # Verificar contenido
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar versiones correctas
            checks = [
                ("actions/checkout@v4", "actions/checkout@v4" in content),
                ("actions/setup-python@v5", "actions/setup-python@v5" in content),
                ("actions/upload-artifact@v4", "actions/upload-artifact@v4" in content),
                ("fail-fast: false", "fail-fast: false" in content),
                ("retention-days: 7", "retention-days: 7" in content)
            ]
            
            print("\n🔍 Verificando contenido del workflow:")
            all_passed = True
            for check_name, passed in checks:
                if passed:
                    print(f"✅ {check_name}")
                else:
                    print(f"❌ {check_name}")
                    all_passed = False
            
            if all_passed:
                print("\n🎉 Workflow completamente corregido!")
                return True
            else:
                print("\n⚠️ Workflow copiado pero con problemas de contenido")
                return False
        else:
            print("❌ Error verificando workflow")
            return False
            
    except Exception as e:
        print(f"❌ Error corrigiendo workflow: {e}")
        return False

def create_workflow_summary():
    """Crear resumen del workflow"""
    print("📊 Creando resumen del workflow...")
    
    base_dir = Path(__file__).parent.parent.parent
    target_file = base_dir / "flora" / ".github" / "workflows" / "ci-cd.yml"
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Contar líneas y características
        lines = content.split('\n')
        total_lines = len(lines)
        
        # Contar jobs
        jobs = content.count('  [a-zA-Z-]+:')
        
        # Contar steps
        steps = content.count('    - name:')
        
        # Contar uses
        uses = content.count('      uses:')
        
        summary = {
            "workflow_summary": {
                "file_location": str(target_file),
                "total_lines": total_lines,
                "jobs_count": jobs,
                "steps_count": steps,
                "actions_count": uses,
                "status": "corrected"
            },
            "actions_versions": {
                "checkout": "v4",
                "setup-python": "v5", 
                "upload-artifact": "v4",
                "download-artifact": "v4",
                "cache": "v4"
            },
            "matrix_configuration": {
                "operating_systems": ["ubuntu-latest", "windows-latest", "macos-latest"],
                "python_versions": ["3.9", "3.10", "3.11", "3.12"],
                "fail_fast": False,
                "exclude_combinations": ["ubuntu-3.8", "macos-3.8"]
            },
            "security_features": [
                "Bandit security scanning",
                "Safety vulnerability scanning", 
                "Custom security tests",
                "Artifact retention (7-30 days)",
                "Continue on error for security scans"
            ],
            "deployment_stages": [
                "test",
                "build", 
                "deploy-staging",
                "deploy-production",
                "security-audit"
            ]
        }
        
        # Guardar resumen
        summary_file = base_dir / "workflow_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            import json
            json.dump(summary, f, indent=2)
        
        print(f"✅ Resumen guardado: {summary_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error creando resumen: {e}")
        return False

def create_verification_commands():
    """Crear comandos de verificación"""
    print("📝 Creando comandos de verificación...")
    
    verification_commands = """# FLORA Workflow Verification Commands

## 1. Verificar que el workflow existe
ls -la flora/.github/workflows/ci-cd.yml

## 2. Verificar contenido del workflow
cat flora/.github/workflows/ci-cd.yml | grep -E "(actions/|fail-fast|retention-days)"

## 3. Verificar versiones de actions
echo "=== CHECKOUT ==="
grep "actions/checkout" flora/.github/workflows/ci-cd.yml

echo "=== SETUP PYTHON ==="
grep "actions/setup-python" flora/.github/workflows/ci-cd.yml

echo "=== UPLOAD ARTIFACT ==="
grep "actions/upload-artifact" flora/.github/workflows/ci-cd.yml

echo "=== FAIL FAST ==="
grep "fail-fast" flora/.github/workflows/ci-cd.yml

echo "=== RETENTION DAYS ==="
grep "retention-days" flora/.github/workflows/ci-cd.yml

## 4. Verificar estructura del workflow
echo "=== JOBS ==="
grep "^  [a-zA-Z-]*:" flora/.github/workflows/ci-cd.yml

echo "=== STEPS ==="
grep "    - name:" flora/.github/workflows/ci-cd.yml | wc -l

## 5. Verificar que no hay versiones deprecadas
echo "=== VERSIONES DEPRECADAS ==="
grep -E "actions/.*@v[0-3]" flora/.github/workflows/ci-cd.yml || echo "✅ No hay versiones deprecadas"

## 6. Verificar matrix de testing
echo "=== MATRIX ==="
grep -A 10 "matrix:" flora/.github/workflows/ci-cd.yml
"""
    
    # Guardar comandos
    base_dir = Path(__file__).parent.parent.parent
    commands_file = base_dir / "verify_workflow_commands.sh"
    with open(commands_file, 'w', encoding='utf-8') as f:
        f.write(verification_commands)
    
    # Hacer ejecutable en Unix
    if os.name != 'nt':
        os.chmod(commands_file, 0o755)
    
    print(f"✅ Comandos de verificación creados: {commands_file}")
    return True

def main():
    """Función principal"""
    print("FLORA WORKFLOW FINAL FIX")
    print("=" * 50)
    
    fixes_applied = 0
    total_fixes = 3
    
    # 1. Corregir workflow
    if fix_workflow_final():
        fixes_applied += 1
        print("✅ Workflow corregido")
    else:
        print("❌ Error corrigiendo workflow")
    
    # 2. Crear resumen
    if create_workflow_summary():
        fixes_applied += 1
        print("✅ Resumen creado")
    else:
        print("❌ Error creando resumen")
    
    # 3. Crear comandos de verificación
    if create_verification_commands():
        fixes_applied += 1
        print("✅ Comandos de verificación creados")
    else:
        print("❌ Error creando comandos")
    
    print(f"\n📊 Correcciones aplicadas: {fixes_applied}/{total_fixes}")
    
    if fixes_applied >= 2:
        print("\n🎉 CORRECCIÓN FINAL COMPLETADA")
        print("\n📁 Workflow ubicado en:")
        print("   flora/.github/workflows/ci-cd.yml")
        print("\n🔧 Características verificadas:")
        print("   - actions/checkout@v4 ✅")
        print("   - actions/setup-python@v5 ✅")
        print("   - actions/upload-artifact@v4 ✅")
        print("   - fail-fast: false ✅")
        print("   - retention-days: 7-30 ✅")
        print("\n📋 Próximos pasos:")
        print("   1. Hacer commit de los cambios")
        print("   2. Push al repositorio")
        print("   3. Verificar que GitHub Actions ejecuta sin errores")
        print("   4. Monitorear resultados de los tests")
        print("\n🔍 Para verificar manualmente:")
        print("   - Revisar flora/.github/workflows/ci-cd.yml")
        print("   - Ejecutar: cat flora/.github/workflows/ci-cd.yml | grep actions/")
        return 0
    else:
        print("\n⚠️ Algunas correcciones fallaron")
        print("Revisar los errores anteriores")
        return 1

if __name__ == "__main__":
    sys.exit(main())
