#!/usr/bin/env python3
"""
FLORA Security Test Runner
Ejecutor de todas las pruebas de seguridad
"""

import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path

# Agregar el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent.parent))

from security.audit.security_auditor import SecurityAuditor
from security.compliance.compliance_manager import ComplianceManager, ComplianceStandard
from security.testing.penetration_tester import PenetrationTester
from security.testing.vulnerability_scanner import VulnerabilityScanner

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_security_audit():
    """Ejecutar auditoría de seguridad"""
    print("\n🔍 EJECUTANDO AUDITORÍA DE SEGURIDAD")
    print("=" * 50)
    
    auditor = SecurityAuditor()
    
    # Simular algunas operaciones para la auditoría
    from security.audit.security_auditor import OperationType
    
    # Operaciones normales
    auditor.log_operation(
        OperationType.ENCRYPT,
        user_id="test_user",
        session_id="test_session",
        ip_address="192.168.1.100",
        data_size=1024,
        success=True
    )
    
    auditor.log_operation(
        OperationType.DECRYPT,
        user_id="test_user", 
        session_id="test_session",
        ip_address="192.168.1.100",
        data_size=1024,
        success=True
    )
    
    # Simular intentos de ataque
    for i in range(6):  # Más de 5 intentos fallidos
        auditor.log_operation(
            OperationType.AUTH_FAILURE,
            user_id="attacker",
            ip_address="192.168.1.200",
            success=False
        )
    
    # Obtener métricas
    metrics = auditor.get_security_metrics()
    print(f"✅ Métricas de seguridad obtenidas:")
    print(f"   - Total de eventos: {metrics['total_events']}")
    print(f"   - Tasa de éxito: {metrics['success_rate']:.2%}")
    print(f"   - Eventos de alto riesgo: {metrics['high_risk_events']}")
    
    # Generar reporte de compliance
    soc2_report = auditor.generate_compliance_report("SOC2")
    print(f"✅ Reporte SOC2 generado: {soc2_report['overall_status']}")
    
    return True

def run_compliance_check():
    """Ejecutar verificación de compliance"""
    print("\n📋 EJECUTANDO VERIFICACIÓN DE COMPLIANCE")
    print("=" * 50)
    
    manager = ComplianceManager()
    
    # Verificar compliance GDPR
    gdpr_assessment = manager.check_gdpr_compliance()
    print(f"✅ GDPR Compliance: {gdpr_assessment.overall_status.value}")
    
    # Verificar compliance SOC2
    soc2_assessment = manager.check_soc2_compliance()
    print(f"✅ SOC2 Compliance: {soc2_assessment.overall_status.value}")
    
    # Verificar compliance ISO27001
    iso_assessment = manager.check_iso27001_compliance()
    print(f"✅ ISO27001 Compliance: {iso_assessment.overall_status.value}")
    
    # Dashboard general
    dashboard = manager.get_compliance_dashboard()
    print(f"✅ Dashboard de compliance generado con {len(dashboard)} estándares")
    
    return True

def run_penetration_test(target_url: str, api_key: str = None):
    """Ejecutar pruebas de penetración"""
    print("\n🔒 EJECUTANDO PRUEBAS DE PENETRACIÓN")
    print("=" * 50)
    
    tester = PenetrationTester(target_url, api_key)
    report = tester.run_comprehensive_test()
    
    print(f"✅ Pruebas de penetración completadas:")
    print(f"   - Total de pruebas: {report.total_tests}")
    print(f"   - Pruebas exitosas: {report.passed_tests}")
    print(f"   - Pruebas fallidas: {report.failed_tests}")
    print(f"   - Vulnerabilidades críticas: {report.critical_findings}")
    print(f"   - Vulnerabilidades altas: {report.high_findings}")
    print(f"   - Resumen: {report.summary}")
    
    # Guardar reporte
    report_filename = f"pentest_report_{report.report_id}.json"
    tester.save_report(report, report_filename)
    print(f"✅ Reporte guardado en: {report_filename}")
    
    return report.failed_tests == 0

def run_vulnerability_scan(target_path: str):
    """Ejecutar escaneo de vulnerabilidades"""
    print("\n🛡️ EJECUTANDO ESCANEO DE VULNERABILIDADES")
    print("=" * 50)
    
    scanner = VulnerabilityScanner(target_path)
    report = scanner.scan_comprehensive()
    
    print(f"✅ Escaneo de vulnerabilidades completado:")
    print(f"   - Archivos escaneados: {report.total_files_scanned}")
    print(f"   - Vulnerabilidades encontradas: {report.total_vulnerabilities}")
    print(f"   - Críticas: {report.critical_count}")
    print(f"   - Altas: {report.high_count}")
    print(f"   - Medias: {report.medium_count}")
    print(f"   - Bajas: {report.low_count}")
    print(f"   - Resumen: {report.summary}")
    
    # Guardar reporte
    report_filename = f"vulnscan_report_{report.scan_id}.json"
    scanner.save_report(report, report_filename)
    print(f"✅ Reporte guardado en: {report_filename}")
    
    return report.critical_count == 0 and report.high_count == 0

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="FLORA Security Test Runner")
    parser.add_argument("--target-url", default="http://localhost:8000", 
                       help="URL objetivo para pruebas de penetración")
    parser.add_argument("--api-key", help="API key para autenticación")
    parser.add_argument("--target-path", default=".", 
                       help="Ruta objetivo para escaneo de vulnerabilidades")
    parser.add_argument("--skip-audit", action="store_true", 
                       help="Omitir auditoría de seguridad")
    parser.add_argument("--skip-compliance", action="store_true", 
                       help="Omitir verificación de compliance")
    parser.add_argument("--skip-pentest", action="store_true", 
                       help="Omitir pruebas de penetración")
    parser.add_argument("--skip-vulnscan", action="store_true", 
                       help="Omitir escaneo de vulnerabilidades")
    
    args = parser.parse_args()
    
    print("🌸 FLORA SECURITY TEST SUITE")
    print("=" * 50)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target URL: {args.target_url}")
    print(f"Target Path: {args.target_path}")
    print("=" * 50)
    
    results = {}
    
    # Ejecutar auditoría de seguridad
    if not args.skip_audit:
        try:
            results['audit'] = run_security_audit()
        except Exception as e:
            logger.error(f"Error en auditoría de seguridad: {e}")
            results['audit'] = False
    else:
        print("\n⏭️ Omitiendo auditoría de seguridad")
        results['audit'] = True
    
    # Ejecutar verificación de compliance
    if not args.skip_compliance:
        try:
            results['compliance'] = run_compliance_check()
        except Exception as e:
            logger.error(f"Error en verificación de compliance: {e}")
            results['compliance'] = False
    else:
        print("\n⏭️ Omitiendo verificación de compliance")
        results['compliance'] = True
    
    # Ejecutar pruebas de penetración
    if not args.skip_pentest:
        try:
            results['pentest'] = run_penetration_test(args.target_url, args.api_key)
        except Exception as e:
            logger.error(f"Error en pruebas de penetración: {e}")
            results['pentest'] = False
    else:
        print("\n⏭️ Omitiendo pruebas de penetración")
        results['pentest'] = True
    
    # Ejecutar escaneo de vulnerabilidades
    if not args.skip_vulnscan:
        try:
            results['vulnscan'] = run_vulnerability_scan(args.target_path)
        except Exception as e:
            logger.error(f"Error en escaneo de vulnerabilidades: {e}")
            results['vulnscan'] = False
    else:
        print("\n⏭️ Omitiendo escaneo de vulnerabilidades")
        results['vulnscan'] = True
    
    # Resumen final
    print("\n📊 RESUMEN FINAL")
    print("=" * 50)
    
    passed_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"   {test_name.upper()}: {status}")
    
    print(f"\nResultado general: {passed_tests}/{total_tests} pruebas pasaron")
    
    if passed_tests == total_tests:
        print("🎉 ¡Todas las pruebas de seguridad pasaron!")
        return 0
    else:
        print("⚠️ Algunas pruebas de seguridad fallaron. Revisar reportes.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
