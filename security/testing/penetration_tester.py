"""
FLORA Penetration Testing Suite
Suite automatizada de pruebas de penetración para FLORA
"""

import requests
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import concurrent.futures
import threading
from urllib.parse import urljoin, urlparse
import ssl
import socket

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestSeverity(Enum):
    """Severidad de las pruebas"""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TestCategory(Enum):
    """Categorías de pruebas"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    INPUT_VALIDATION = "input_validation"
    CRYPTOGRAPHY = "cryptography"
    NETWORK = "network"
    CONFIGURATION = "configuration"
    BUSINESS_LOGIC = "business_logic"

@dataclass
class TestResult:
    """Resultado de una prueba"""
    test_id: str
    test_name: str
    category: TestCategory
    severity: TestSeverity
    status: str  # "passed", "failed", "error"
    description: str
    evidence: List[str]
    recommendation: str
    timestamp: datetime
    target: str

@dataclass
class PenetrationTestReport:
    """Reporte de pruebas de penetración"""
    report_id: str
    target: str
    start_time: datetime
    end_time: datetime
    total_tests: int
    passed_tests: int
    failed_tests: int
    error_tests: int
    critical_findings: int
    high_findings: int
    medium_findings: int
    low_findings: int
    results: List[TestResult]
    summary: str
    recommendations: List[str]

class PenetrationTester:
    """Suite de pruebas de penetración"""
    
    def __init__(self, target_url: str, api_key: str = None):
        self.target_url = target_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FLORA-PenTest/1.0',
            'Content-Type': 'application/json'
        })
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}'
            })
        
        self.results = []
        self.lock = threading.Lock()
    
    def run_comprehensive_test(self) -> PenetrationTestReport:
        """Ejecutar suite completa de pruebas"""
        logger.info(f"Iniciando pruebas de penetración contra {self.target_url}")
        start_time = datetime.now()
        
        # Ejecutar todas las categorías de pruebas
        test_categories = [
            self._test_authentication,
            self._test_authorization,
            self._test_input_validation,
            self._test_cryptography,
            self._test_network_security,
            self._test_configuration,
            self._test_business_logic
        ]
        
        # Ejecutar pruebas en paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(test_func) for test_func in test_categories]
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    category_results = future.result()
                    with self.lock:
                        self.results.extend(category_results)
                except Exception as e:
                    logger.error(f"Error en categoría de pruebas: {e}")
        
        end_time = datetime.now()
        
        # Generar reporte
        report = self._generate_report(start_time, end_time)
        
        logger.info(f"Pruebas completadas. {report.failed_tests} fallos encontrados")
        return report
    
    def _test_authentication(self) -> List[TestResult]:
        """Pruebas de autenticación"""
        results = []
        
        # Test 1: Autenticación sin API key
        try:
            response = requests.post(f"{self.target_url}/api/v1/encrypt", 
                                   json={"data": "test"})
            if response.status_code == 401:
                results.append(TestResult(
                    test_id="AUTH-001",
                    test_name="Autenticación Requerida",
                    category=TestCategory.AUTHENTICATION,
                    severity=TestSeverity.INFO,
                    status="passed",
                    description="API requiere autenticación",
                    evidence=[f"Status code: {response.status_code}"],
                    recommendation="Correcto: API protegida con autenticación",
                    timestamp=datetime.now(),
                    target=self.target_url
                ))
            else:
                results.append(TestResult(
                    test_id="AUTH-001",
                    test_name="Autenticación Requerida",
                    category=TestCategory.AUTHENTICATION,
                    severity=TestSeverity.HIGH,
                    status="failed",
                    description="API no requiere autenticación",
                    evidence=[f"Status code: {response.status_code}"],
                    recommendation="Implementar autenticación obligatoria",
                    timestamp=datetime.now(),
                    target=self.target_url
                ))
        except Exception as e:
            results.append(TestResult(
                test_id="AUTH-001",
                test_name="Autenticación Requerida",
                category=TestCategory.AUTHENTICATION,
                severity=TestSeverity.MEDIUM,
                status="error",
                description=f"Error al probar autenticación: {str(e)}",
                evidence=[],
                recommendation="Verificar conectividad y configuración",
                timestamp=datetime.now(),
                target=self.target_url
            ))
        
        # Test 2: API key inválida
        if self.api_key:
            invalid_session = requests.Session()
            invalid_session.headers.update({
                'Authorization': 'Bearer invalid_key_12345',
                'Content-Type': 'application/json'
            })
            
            try:
                response = invalid_session.post(f"{self.target_url}/api/v1/encrypt",
                                             json={"data": "test"})
                if response.status_code == 401:
                    results.append(TestResult(
                        test_id="AUTH-002",
                        test_name="API Key Inválida Rechazada",
                        category=TestCategory.AUTHENTICATION,
                        severity=TestSeverity.INFO,
                        status="passed",
                        description="API rechaza claves inválidas",
                        evidence=[f"Status code: {response.status_code}"],
                        recommendation="Correcto: Validación de API key funciona",
                        timestamp=datetime.now(),
                        target=self.target_url
                    ))
                else:
                    results.append(TestResult(
                        test_id="AUTH-002",
                        test_name="API Key Inválida Rechazada",
                        category=TestCategory.AUTHENTICATION,
                        severity=TestSeverity.CRITICAL,
                        status="failed",
                        description="API acepta claves inválidas",
                        evidence=[f"Status code: {response.status_code}"],
                        recommendation="Corregir validación de API key",
                        timestamp=datetime.now(),
                        target=self.target_url
                    ))
            except Exception as e:
                results.append(TestResult(
                    test_id="AUTH-002",
                    test_name="API Key Inválida Rechazada",
                    category=TestCategory.AUTHENTICATION,
                    severity=TestSeverity.MEDIUM,
                    status="error",
                    description=f"Error al probar API key inválida: {str(e)}",
                    evidence=[],
                    recommendation="Verificar conectividad",
                    timestamp=datetime.now(),
                    target=self.target_url
                ))
        
        return results
    
    def _test_authorization(self) -> List[TestResult]:
        """Pruebas de autorización"""
        results = []
        
        # Test 3: Acceso a endpoints sin autorización
        endpoints = ["/api/v1/encrypt", "/api/v1/decrypt", "/api/v1/stats", "/api/v1/audit"]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.target_url}{endpoint}")
                if response.status_code == 401:
                    results.append(TestResult(
                        test_id=f"AUTHZ-001-{endpoint.replace('/', '_')}",
                        test_name=f"Endpoint {endpoint} Protegido",
                        category=TestCategory.AUTHORIZATION,
                        severity=TestSeverity.INFO,
                        status="passed",
                        description=f"Endpoint {endpoint} requiere autorización",
                        evidence=[f"Status code: {response.status_code}"],
                        recommendation="Correcto: Endpoint protegido",
                        timestamp=datetime.now(),
                        target=self.target_url
                    ))
                else:
                    results.append(TestResult(
                        test_id=f"AUTHZ-001-{endpoint.replace('/', '_')}",
                        test_name=f"Endpoint {endpoint} Protegido",
                        category=TestCategory.AUTHORIZATION,
                        severity=TestSeverity.HIGH,
                        status="failed",
                        description=f"Endpoint {endpoint} accesible sin autorización",
                        evidence=[f"Status code: {response.status_code}"],
                        recommendation="Implementar autorización en endpoint",
                        timestamp=datetime.now(),
                        target=self.target_url
                    ))
            except Exception as e:
                results.append(TestResult(
                    test_id=f"AUTHZ-001-{endpoint.replace('/', '_')}",
                    test_name=f"Endpoint {endpoint} Protegido",
                    category=TestCategory.AUTHORIZATION,
                    severity=TestSeverity.MEDIUM,
                    status="error",
                    description=f"Error al probar {endpoint}: {str(e)}",
                    evidence=[],
                    recommendation="Verificar conectividad",
                    timestamp=datetime.now(),
                    target=self.target_url
                ))
        
        return results
    
    def _test_input_validation(self) -> List[TestResult]:
        """Pruebas de validación de entrada"""
        results = []
        
        if not self.api_key:
            return results
        
        # Test 4: Inyección SQL (simulado)
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "<script>alert('xss')</script>",
            "../../../etc/passwd",
            "{{7*7}}",
            "${7*7}"
        ]
        
        for i, malicious_input in enumerate(malicious_inputs):
            try:
                response = self.session.post(f"{self.target_url}/api/v1/encrypt",
                                           json={"data": malicious_input})
                
                # Verificar si la respuesta indica que la entrada fue procesada de forma segura
                if response.status_code in [200, 400]:  # 400 es esperado para entradas inválidas
                    results.append(TestResult(
                        test_id=f"INPUT-{i+1:03d}",
                        test_name=f"Validación de Entrada Maliciosa {i+1}",
                        category=TestCategory.INPUT_VALIDATION,
                        severity=TestSeverity.INFO,
                        status="passed",
                        description=f"Entrada maliciosa manejada correctamente",
                        evidence=[f"Input: {malicious_input[:50]}...", f"Status: {response.status_code}"],
                        recommendation="Correcto: Validación de entrada funciona",
                        timestamp=datetime.now(),
                        target=self.target_url
                    ))
                else:
                    results.append(TestResult(
                        test_id=f"INPUT-{i+1:03d}",
                        test_name=f"Validación de Entrada Maliciosa {i+1}",
                        category=TestCategory.INPUT_VALIDATION,
                        severity=TestSeverity.MEDIUM,
                        status="failed",
                        description=f"Respuesta inesperada para entrada maliciosa",
                        evidence=[f"Input: {malicious_input[:50]}...", f"Status: {response.status_code}"],
                        recommendation="Revisar validación de entrada",
                        timestamp=datetime.now(),
                        target=self.target_url
                    ))
            except Exception as e:
                results.append(TestResult(
                    test_id=f"INPUT-{i+1:03d}",
                    test_name=f"Validación de Entrada Maliciosa {i+1}",
                    category=TestCategory.INPUT_VALIDATION,
                    severity=TestSeverity.LOW,
                    status="error",
                    description=f"Error al probar entrada: {str(e)}",
                    evidence=[],
                    recommendation="Verificar conectividad",
                    timestamp=datetime.now(),
                    target=self.target_url
                ))
        
        return results
    
    def _test_cryptography(self) -> List[TestResult]:
        """Pruebas de criptografía"""
        results = []
        
        if not self.api_key:
            return results
        
        # Test 5: Verificar uso de HTTPS
        try:
            parsed_url = urlparse(self.target_url)
            if parsed_url.scheme == 'https':
                # Verificar certificado SSL
                context = ssl.create_default_context()
                with socket.create_connection((parsed_url.hostname, parsed_url.port or 443), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=parsed_url.hostname) as ssock:
                        cert = ssock.getpeercert()
                        if cert:
                            results.append(TestResult(
                                test_id="CRYPTO-001",
                                test_name="Certificado SSL Válido",
                                category=TestCategory.CRYPTOGRAPHY,
                                severity=TestSeverity.INFO,
                                status="passed",
                                description="Certificado SSL válido encontrado",
                                evidence=[f"Subject: {cert.get('subject', 'N/A')}", f"Issuer: {cert.get('issuer', 'N/A')}"],
                                recommendation="Correcto: HTTPS configurado correctamente",
                                timestamp=datetime.now(),
                                target=self.target_url
                            ))
                        else:
                            results.append(TestResult(
                                test_id="CRYPTO-001",
                                test_name="Certificado SSL Válido",
                                category=TestCategory.CRYPTOGRAPHY,
                                severity=TestSeverity.HIGH,
                                status="failed",
                                description="No se pudo obtener certificado SSL",
                                evidence=[],
                                recommendation="Verificar configuración SSL",
                                timestamp=datetime.now(),
                                target=self.target_url
                            ))
            else:
                results.append(TestResult(
                    test_id="CRYPTO-001",
                    test_name="Uso de HTTPS",
                    category=TestCategory.CRYPTOGRAPHY,
                    severity=TestSeverity.CRITICAL,
                    status="failed",
                    description="API no usa HTTPS",
                    evidence=[f"URL: {self.target_url}"],
                    recommendation="Implementar HTTPS obligatorio",
                    timestamp=datetime.now(),
                    target=self.target_url
                ))
        except Exception as e:
            results.append(TestResult(
                test_id="CRYPTO-001",
                test_name="Verificación SSL",
                category=TestCategory.CRYPTOGRAPHY,
                severity=TestSeverity.MEDIUM,
                status="error",
                description=f"Error al verificar SSL: {str(e)}",
                evidence=[],
                recommendation="Verificar conectividad y configuración SSL",
                timestamp=datetime.now(),
                target=self.target_url
            ))
        
        # Test 6: Verificar headers de seguridad
        try:
            response = self.session.get(f"{self.target_url}/api/v1/stats")
            security_headers = {
                'Strict-Transport-Security': 'HSTS',
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': 'XSS Protection',
                'Content-Security-Policy': 'CSP'
            }
            
            missing_headers = []
            for header, description in security_headers.items():
                if header not in response.headers:
                    missing_headers.append(f"{header} ({description})")
            
            if not missing_headers:
                results.append(TestResult(
                    test_id="CRYPTO-002",
                    test_name="Headers de Seguridad",
                    category=TestCategory.CRYPTOGRAPHY,
                    severity=TestSeverity.INFO,
                    status="passed",
                    description="Todos los headers de seguridad presentes",
                    evidence=["Todos los headers de seguridad configurados"],
                    recommendation="Correcto: Headers de seguridad implementados",
                    timestamp=datetime.now(),
                    target=self.target_url
                ))
            else:
                results.append(TestResult(
                    test_id="CRYPTO-002",
                    test_name="Headers de Seguridad",
                    category=TestCategory.CRYPTOGRAPHY,
                    severity=TestSeverity.MEDIUM,
                    status="failed",
                    description=f"Headers de seguridad faltantes: {', '.join(missing_headers)}",
                    evidence=missing_headers,
                    recommendation="Implementar headers de seguridad faltantes",
                    timestamp=datetime.now(),
                    target=self.target_url
                ))
        except Exception as e:
            results.append(TestResult(
                test_id="CRYPTO-002",
                test_name="Headers de Seguridad",
                category=TestCategory.CRYPTOGRAPHY,
                severity=TestSeverity.LOW,
                status="error",
                description=f"Error al verificar headers: {str(e)}",
                evidence=[],
                recommendation="Verificar conectividad",
                timestamp=datetime.now(),
                target=self.target_url
            ))
        
        return results
    
    def _test_network_security(self) -> List[TestResult]:
        """Pruebas de seguridad de red"""
        results = []
        
        # Test 7: Verificar rate limiting
        if self.api_key:
            try:
                # Enviar múltiples requests rápidamente
                rapid_requests = []
                for i in range(10):
                    rapid_requests.append(
                        self.session.post(f"{self.target_url}/api/v1/encrypt",
                                        json={"data": f"test_{i}"})
                    )
                
                # Verificar si algún request fue rechazado por rate limiting
                rate_limited = any(r.status_code == 429 for r in rapid_requests)
                
                if rate_limited:
                    results.append(TestResult(
                        test_id="NET-001",
                        test_name="Rate Limiting",
                        category=TestCategory.NETWORK,
                        severity=TestSeverity.INFO,
                        status="passed",
                        description="Rate limiting implementado",
                        evidence=["Algunos requests recibieron status 429"],
                        recommendation="Correcto: Rate limiting activo",
                        timestamp=datetime.now(),
                        target=self.target_url
                    ))
                else:
                    results.append(TestResult(
                        test_id="NET-001",
                        test_name="Rate Limiting",
                        category=TestCategory.NETWORK,
                        severity=TestSeverity.MEDIUM,
                        status="failed",
                        description="Rate limiting no detectado",
                        evidence=["Todos los requests fueron procesados"],
                        recommendation="Implementar rate limiting",
                        timestamp=datetime.now(),
                        target=self.target_url
                    ))
            except Exception as e:
                results.append(TestResult(
                    test_id="NET-001",
                    test_name="Rate Limiting",
                    category=TestCategory.NETWORK,
                    severity=TestSeverity.LOW,
                    status="error",
                    description=f"Error al probar rate limiting: {str(e)}",
                    evidence=[],
                    recommendation="Verificar conectividad",
                    timestamp=datetime.now(),
                    target=self.target_url
                ))
        
        return results
    
    def _test_configuration(self) -> List[TestResult]:
        """Pruebas de configuración"""
        results = []
        
        # Test 8: Verificar información sensible en headers
        try:
            response = self.session.get(f"{self.target_url}/api/v1/stats")
            
            sensitive_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version']
            exposed_info = []
            
            for header in sensitive_headers:
                if header in response.headers:
                    exposed_info.append(f"{header}: {response.headers[header]}")
            
            if not exposed_info:
                results.append(TestResult(
                    test_id="CONFIG-001",
                    test_name="Información del Servidor",
                    category=TestCategory.CONFIGURATION,
                    severity=TestSeverity.INFO,
                    status="passed",
                    description="No se expone información sensible del servidor",
                    evidence=["Headers sensibles no presentes"],
                    recommendation="Correcto: Configuración segura",
                    timestamp=datetime.now(),
                    target=self.target_url
                ))
            else:
                results.append(TestResult(
                    test_id="CONFIG-001",
                    test_name="Información del Servidor",
                    category=TestCategory.CONFIGURATION,
                    severity=TestSeverity.LOW,
                    status="failed",
                    description="Se expone información del servidor",
                    evidence=exposed_info,
                    recommendation="Ocultar headers que revelen información del servidor",
                    timestamp=datetime.now(),
                    target=self.target_url
                ))
        except Exception as e:
            results.append(TestResult(
                test_id="CONFIG-001",
                test_name="Información del Servidor",
                category=TestCategory.CONFIGURATION,
                severity=TestSeverity.LOW,
                status="error",
                description=f"Error al verificar headers: {str(e)}",
                evidence=[],
                recommendation="Verificar conectividad",
                timestamp=datetime.now(),
                target=self.target_url
            ))
        
        return results
    
    def _test_business_logic(self) -> List[TestResult]:
        """Pruebas de lógica de negocio"""
        results = []
        
        if not self.api_key:
            return results
        
        # Test 9: Verificar funcionalidad de cifrado/descifrado
        try:
            # Cifrar datos
            encrypt_response = self.session.post(f"{self.target_url}/api/v1/encrypt",
                                               json={"data": "test_business_logic"})
            
            if encrypt_response.status_code == 200:
                encrypt_data = encrypt_response.json()
                encrypted_data = encrypt_data.get('encrypted_data')
                key_id = encrypt_data.get('key_id')
                
                if encrypted_data and key_id:
                    # Intentar descifrar
                    decrypt_response = self.session.post(f"{self.target_url}/api/v1/decrypt",
                                                       json={
                                                           "encrypted_data": encrypted_data,
                                                           "key_id": key_id
                                                       })
                    
                    if decrypt_response.status_code == 200:
                        decrypt_data = decrypt_response.json()
                        decrypted_data = decrypt_data.get('decrypted_data')
                        
                        if decrypted_data == "test_business_logic":
                            results.append(TestResult(
                                test_id="BIZ-001",
                                test_name="Funcionalidad Cifrado/Descifrado",
                                category=TestCategory.BUSINESS_LOGIC,
                                severity=TestSeverity.INFO,
                                status="passed",
                                description="Cifrado y descifrado funcionan correctamente",
                                evidence=["Datos cifrados y descifrados exitosamente"],
                                recommendation="Correcto: Lógica de negocio funciona",
                                timestamp=datetime.now(),
                                target=self.target_url
                            ))
                        else:
                            results.append(TestResult(
                                test_id="BIZ-001",
                                test_name="Funcionalidad Cifrado/Descifrado",
                                category=TestCategory.BUSINESS_LOGIC,
                                severity=TestSeverity.HIGH,
                                status="failed",
                                description="Datos descifrados no coinciden con original",
                                evidence=[f"Original: test_business_logic", f"Descifrado: {decrypted_data}"],
                                recommendation="Revisar implementación de cifrado/descifrado",
                                timestamp=datetime.now(),
                                target=self.target_url
                            ))
                    else:
                        results.append(TestResult(
                            test_id="BIZ-001",
                            test_name="Funcionalidad Cifrado/Descifrado",
                            category=TestCategory.BUSINESS_LOGIC,
                            severity=TestSeverity.HIGH,
                            status="failed",
                            description="Error al descifrar datos",
                            evidence=[f"Status code: {decrypt_response.status_code}"],
                            recommendation="Revisar implementación de descifrado",
                            timestamp=datetime.now(),
                            target=self.target_url
                        ))
                else:
                    results.append(TestResult(
                        test_id="BIZ-001",
                        test_name="Funcionalidad Cifrado/Descifrado",
                        category=TestCategory.BUSINESS_LOGIC,
                        severity=TestSeverity.HIGH,
                        status="failed",
                        description="Respuesta de cifrado incompleta",
                        evidence=[f"Response: {encrypt_data}"],
                        recommendation="Revisar implementación de cifrado",
                        timestamp=datetime.now(),
                        target=self.target_url
                    ))
            else:
                results.append(TestResult(
                    test_id="BIZ-001",
                    test_name="Funcionalidad Cifrado/Descifrado",
                    category=TestCategory.BUSINESS_LOGIC,
                    severity=TestSeverity.HIGH,
                    status="failed",
                    description="Error al cifrar datos",
                    evidence=[f"Status code: {encrypt_response.status_code}"],
                    recommendation="Revisar implementación de cifrado",
                    timestamp=datetime.now(),
                    target=self.target_url
                ))
        except Exception as e:
            results.append(TestResult(
                test_id="BIZ-001",
                test_name="Funcionalidad Cifrado/Descifrado",
                category=TestCategory.BUSINESS_LOGIC,
                severity=TestSeverity.MEDIUM,
                status="error",
                description=f"Error al probar lógica de negocio: {str(e)}",
                evidence=[],
                recommendation="Verificar conectividad y configuración",
                timestamp=datetime.now(),
                target=self.target_url
            ))
        
        return results
    
    def _generate_report(self, start_time: datetime, end_time: datetime) -> PenetrationTestReport:
        """Generar reporte de pruebas"""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.status == "passed"])
        failed_tests = len([r for r in self.results if r.status == "failed"])
        error_tests = len([r for r in self.results if r.status == "error"])
        
        critical_findings = len([r for r in self.results if r.severity == TestSeverity.CRITICAL and r.status == "failed"])
        high_findings = len([r for r in self.results if r.severity == TestSeverity.HIGH and r.status == "failed"])
        medium_findings = len([r for r in self.results if r.severity == TestSeverity.MEDIUM and r.status == "failed"])
        low_findings = len([r for r in self.results if r.severity == TestSeverity.LOW and r.status == "failed"])
        
        # Generar resumen
        if critical_findings > 0:
            summary = f"CRÍTICO: {critical_findings} vulnerabilidades críticas encontradas"
        elif high_findings > 0:
            summary = f"ALTO: {high_findings} vulnerabilidades de alta severidad encontradas"
        elif medium_findings > 0:
            summary = f"MEDIO: {medium_findings} vulnerabilidades de severidad media encontradas"
        elif failed_tests > 0:
            summary = f"BAJO: {failed_tests} problemas menores encontrados"
        else:
            summary = "EXCELENTE: No se encontraron vulnerabilidades"
        
        # Generar recomendaciones
        recommendations = []
        if critical_findings > 0:
            recommendations.append("URGENTE: Corregir vulnerabilidades críticas inmediatamente")
        if high_findings > 0:
            recommendations.append("ALTA PRIORIDAD: Abordar vulnerabilidades de alta severidad")
        if medium_findings > 0:
            recommendations.append("MEDIA PRIORIDAD: Planificar corrección de vulnerabilidades medias")
        if not any([critical_findings, high_findings, medium_findings]):
            recommendations.append("Mantener buenas prácticas de seguridad")
            recommendations.append("Realizar pruebas regulares de penetración")
        
        return PenetrationTestReport(
            report_id=f"PENTEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            target=self.target_url,
            start_time=start_time,
            end_time=end_time,
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            error_tests=error_tests,
            critical_findings=critical_findings,
            high_findings=high_findings,
            medium_findings=medium_findings,
            low_findings=low_findings,
            results=self.results,
            summary=summary,
            recommendations=recommendations
        )
    
    def save_report(self, report: PenetrationTestReport, filename: str = None):
        """Guardar reporte en archivo"""
        if filename is None:
            filename = f"pentest_report_{report.report_id}.json"
        
        report_data = {
            "report_id": report.report_id,
            "target": report.target,
            "start_time": report.start_time.isoformat(),
            "end_time": report.end_time.isoformat(),
            "total_tests": report.total_tests,
            "passed_tests": report.passed_tests,
            "failed_tests": report.failed_tests,
            "error_tests": report.error_tests,
            "critical_findings": report.critical_findings,
            "high_findings": report.high_findings,
            "medium_findings": report.medium_findings,
            "low_findings": report.low_findings,
            "summary": report.summary,
            "recommendations": report.recommendations,
            "results": [
                {
                    "test_id": r.test_id,
                    "test_name": r.test_name,
                    "category": r.category.value,
                    "severity": r.severity.value,
                    "status": r.status,
                    "description": r.description,
                    "evidence": r.evidence,
                    "recommendation": r.recommendation,
                    "timestamp": r.timestamp.isoformat(),
                    "target": r.target
                }
                for r in report.results
            ]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Reporte guardado en {filename}")

# Función de conveniencia
def run_penetration_test(target_url: str, api_key: str = None) -> PenetrationTestReport:
    """Ejecutar prueba de penetración"""
    tester = PenetrationTester(target_url, api_key)
    return tester.run_comprehensive_test()

# Ejemplo de uso
if __name__ == "__main__":
    # Ejecutar prueba de penetración
    report = run_penetration_test("http://localhost:8000", "test_api_key_12345678901234567890")
    
    print(f"Reporte de Penetración: {report.report_id}")
    print(f"Resumen: {report.summary}")
    print(f"Total de pruebas: {report.total_tests}")
    print(f"Fallos: {report.failed_tests}")
    print(f"Vulnerabilidades críticas: {report.critical_findings}")
    
    # Guardar reporte
    tester = PenetrationTester("http://localhost:8000", "test_api_key_12345678901234567890")
    tester.save_report(report)
