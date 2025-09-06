"""
FLORA Compliance Manager
Sistema de gestión de compliance para estándares de seguridad
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComplianceStandard(Enum):
    """Estándares de compliance soportados"""
    GDPR = "gdpr"
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    FIPS140_2 = "fips140_2"
    COMMON_CRITERIA = "common_criteria"
    PCI_DSS = "pci_dss"
    HIPAA = "hipaa"

class ComplianceStatus(Enum):
    """Estados de compliance"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NOT_ASSESSED = "not_assessed"

@dataclass
class ComplianceControl:
    """Control de compliance"""
    control_id: str
    standard: ComplianceStandard
    category: str
    title: str
    description: str
    requirements: List[str]
    implementation_status: ComplianceStatus
    evidence: List[str]
    last_assessed: datetime
    assessor: str
    notes: str

@dataclass
class ComplianceAssessment:
    """Evaluación de compliance"""
    assessment_id: str
    standard: ComplianceStandard
    assessment_date: datetime
    assessor: str
    overall_status: ComplianceStatus
    controls: List[ComplianceControl]
    findings: List[str]
    recommendations: List[str]
    next_assessment: datetime

class ComplianceManager:
    """Gestor de compliance principal"""
    
    def __init__(self, db_path: str = "compliance.db"):
        self.db_path = db_path
        self._init_database()
        self._load_default_controls()
    
    def _init_database(self):
        """Inicializar base de datos de compliance"""
        with sqlite3.connect(self.db_path) as conn:
            # Tabla de controles
            conn.execute("""
                CREATE TABLE IF NOT EXISTS compliance_controls (
                    control_id TEXT PRIMARY KEY,
                    standard TEXT NOT NULL,
                    category TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    requirements TEXT NOT NULL,
                    implementation_status TEXT NOT NULL,
                    evidence TEXT NOT NULL,
                    last_assessed TEXT NOT NULL,
                    assessor TEXT NOT NULL,
                    notes TEXT
                )
            """)
            
            # Tabla de evaluaciones
            conn.execute("""
                CREATE TABLE IF NOT EXISTS compliance_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    standard TEXT NOT NULL,
                    assessment_date TEXT NOT NULL,
                    assessor TEXT NOT NULL,
                    overall_status TEXT NOT NULL,
                    findings TEXT NOT NULL,
                    recommendations TEXT NOT NULL,
                    next_assessment TEXT NOT NULL
                )
            """)
            
            # Tabla de evidencia
            conn.execute("""
                CREATE TABLE IF NOT EXISTS compliance_evidence (
                    evidence_id TEXT PRIMARY KEY,
                    control_id TEXT NOT NULL,
                    evidence_type TEXT NOT NULL,
                    file_path TEXT,
                    description TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    created_by TEXT NOT NULL,
                    FOREIGN KEY (control_id) REFERENCES compliance_controls(control_id)
                )
            """)
    
    def _load_default_controls(self):
        """Cargar controles por defecto para cada estándar"""
        # Controles GDPR
        gdpr_controls = [
            ComplianceControl(
                control_id="GDPR-001",
                standard=ComplianceStandard.GDPR,
                category="Data Protection",
                title="Data Encryption",
                description="Personal data must be encrypted in transit and at rest",
                requirements=[
                    "AES-256 encryption for data at rest",
                    "TLS 1.3 for data in transit",
                    "Key management according to industry standards"
                ],
                implementation_status=ComplianceStatus.COMPLIANT,
                evidence=["Encryption implementation in FLORA core", "TLS configuration"],
                last_assessed=datetime.now(),
                assessor="Security Team",
                notes="Implemented with AES-256-GCM"
            ),
            ComplianceControl(
                control_id="GDPR-002",
                standard=ComplianceStandard.GDPR,
                category="Data Subject Rights",
                title="Right to Erasure",
                description="Data subjects have the right to request data deletion",
                requirements=[
                    "Data deletion procedures",
                    "Audit trail of deletions",
                    "Verification of complete removal"
                ],
                implementation_status=ComplianceStatus.PARTIALLY_COMPLIANT,
                evidence=["Data deletion API endpoint"],
                last_assessed=datetime.now(),
                assessor="Security Team",
                notes="API implemented, audit trail pending"
            )
        ]
        
        # Controles SOC2
        soc2_controls = [
            ComplianceControl(
                control_id="SOC2-CC6.1",
                standard=ComplianceStandard.SOC2,
                category="Logical and Physical Access Controls",
                title="Access Control Policy",
                description="Logical and physical access to information assets is restricted",
                requirements=[
                    "Access control policies documented",
                    "User access reviews performed",
                    "Privileged access management"
                ],
                implementation_status=ComplianceStatus.COMPLIANT,
                evidence=["Access control documentation", "User access review logs"],
                last_assessed=datetime.now(),
                assessor="Security Team",
                notes="Comprehensive access controls implemented"
            ),
            ComplianceControl(
                control_id="SOC2-CC6.2",
                standard=ComplianceStandard.SOC2,
                category="System Access Controls",
                title="System Access Management",
                description="System access is restricted to authorized users",
                requirements=[
                    "Multi-factor authentication",
                    "Session management",
                    "Access logging and monitoring"
                ],
                implementation_status=ComplianceStatus.COMPLIANT,
                evidence=["MFA implementation", "Session management logs"],
                last_assessed=datetime.now(),
                assessor="Security Team",
                notes="MFA and session controls active"
            )
        ]
        
        # Controles ISO27001
        iso27001_controls = [
            ComplianceControl(
                control_id="ISO27001-A.10.1",
                standard=ComplianceStandard.ISO27001,
                category="Cryptography",
                title="Cryptographic Controls",
                description="Cryptographic controls are used to protect information",
                requirements=[
                    "Cryptographic policy",
                    "Key management procedures",
                    "Cryptographic algorithm selection"
                ],
                implementation_status=ComplianceStatus.COMPLIANT,
                evidence=["Cryptographic policy document", "Key management procedures"],
                last_assessed=datetime.now(),
                assessor="Security Team",
                notes="Post-quantum cryptography implemented"
            )
        ]
        
        # Guardar controles en base de datos
        for control in gdpr_controls + soc2_controls + iso27001_controls:
            self._save_control(control)
    
    def _save_control(self, control: ComplianceControl):
        """Guardar control en base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO compliance_controls 
                (control_id, standard, category, title, description, requirements, 
                 implementation_status, evidence, last_assessed, assessor, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                control.control_id,
                control.standard.value,
                control.category,
                control.title,
                control.description,
                json.dumps(control.requirements),
                control.implementation_status.value,
                json.dumps(control.evidence),
                control.last_assessed.isoformat(),
                control.assessor,
                control.notes
            ))
    
    def get_controls_by_standard(self, standard: ComplianceStandard) -> List[ComplianceControl]:
        """Obtener controles por estándar"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM compliance_controls 
                WHERE standard = ? 
                ORDER BY control_id
            """, (standard.value,))
            
            controls = []
            for row in cursor.fetchall():
                control = ComplianceControl(
                    control_id=row[0],
                    standard=ComplianceStandard(row[1]),
                    category=row[2],
                    title=row[3],
                    description=row[4],
                    requirements=json.loads(row[5]),
                    implementation_status=ComplianceStatus(row[6]),
                    evidence=json.loads(row[7]),
                    last_assessed=datetime.fromisoformat(row[8]),
                    assessor=row[9],
                    notes=row[10]
                )
                controls.append(control)
        
        return controls
    
    def update_control_status(self, control_id: str, status: ComplianceStatus, 
                            evidence: List[str] = None, notes: str = "", 
                            assessor: str = "System"):
        """Actualizar estado de un control"""
        with sqlite3.connect(self.db_path) as conn:
            # Obtener control actual
            cursor = conn.execute("""
                SELECT evidence FROM compliance_controls WHERE control_id = ?
            """, (control_id,))
            row = cursor.fetchone()
            
            if row:
                current_evidence = json.loads(row[0])
                if evidence:
                    current_evidence.extend(evidence)
                
                conn.execute("""
                    UPDATE compliance_controls 
                    SET implementation_status = ?, evidence = ?, last_assessed = ?, 
                        assessor = ?, notes = ?
                    WHERE control_id = ?
                """, (
                    status.value,
                    json.dumps(current_evidence),
                    datetime.now().isoformat(),
                    assessor,
                    notes,
                    control_id
                ))
                
                logger.info(f"Control {control_id} actualizado a {status.value}")
    
    def perform_assessment(self, standard: ComplianceStandard, 
                          assessor: str = "Security Team") -> ComplianceAssessment:
        """Realizar evaluación de compliance"""
        controls = self.get_controls_by_standard(standard)
        
        # Calcular estado general
        compliant_count = sum(1 for c in controls if c.implementation_status == ComplianceStatus.COMPLIANT)
        total_count = len(controls)
        
        if compliant_count == total_count:
            overall_status = ComplianceStatus.COMPLIANT
        elif compliant_count == 0:
            overall_status = ComplianceStatus.NON_COMPLIANT
        else:
            overall_status = ComplianceStatus.PARTIALLY_COMPLIANT
        
        # Generar hallazgos y recomendaciones
        findings = []
        recommendations = []
        
        for control in controls:
            if control.implementation_status == ComplianceStatus.NON_COMPLIANT:
                findings.append(f"Control {control.control_id} ({control.title}) no está implementado")
                recommendations.append(f"Implementar {control.title}: {control.description}")
            elif control.implementation_status == ComplianceStatus.PARTIALLY_COMPLIANT:
                findings.append(f"Control {control.control_id} ({control.title}) implementado parcialmente")
                recommendations.append(f"Completar implementación de {control.title}")
        
        assessment = ComplianceAssessment(
            assessment_id=f"ASSESS-{standard.value.upper()}-{datetime.now().strftime('%Y%m%d')}",
            standard=standard,
            assessment_date=datetime.now(),
            assessor=assessor,
            overall_status=overall_status,
            controls=controls,
            findings=findings,
            recommendations=recommendations,
            next_assessment=datetime.now() + timedelta(days=365)
        )
        
        # Guardar evaluación
        self._save_assessment(assessment)
        return assessment
    
    def _save_assessment(self, assessment: ComplianceAssessment):
        """Guardar evaluación en base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO compliance_assessments 
                (assessment_id, standard, assessment_date, assessor, overall_status, 
                 findings, recommendations, next_assessment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id,
                assessment.standard.value,
                assessment.assessment_date.isoformat(),
                assessment.assessor,
                assessment.overall_status.value,
                json.dumps(assessment.findings),
                json.dumps(assessment.recommendations),
                assessment.next_assessment.isoformat()
            ))
    
    def get_compliance_dashboard(self) -> Dict[str, Any]:
        """Obtener dashboard de compliance"""
        dashboard = {}
        
        for standard in ComplianceStandard:
            controls = self.get_controls_by_standard(standard)
            if controls:
                compliant = sum(1 for c in controls if c.implementation_status == ComplianceStatus.COMPLIANT)
                total = len(controls)
                compliance_rate = compliant / total if total > 0 else 0
                
                dashboard[standard.value] = {
                    "total_controls": total,
                    "compliant_controls": compliant,
                    "compliance_rate": compliance_rate,
                    "status": ComplianceStatus.COMPLIANT if compliance_rate == 1.0 
                             else ComplianceStatus.PARTIALLY_COMPLIANT if compliance_rate > 0 
                             else ComplianceStatus.NON_COMPLIANT
                }
        
        return dashboard
    
    def generate_compliance_report(self, standard: ComplianceStandard, format: str = "json") -> str:
        """Generar reporte de compliance"""
        assessment = self.perform_assessment(standard)
        
        if format == "json":
            return json.dumps({
                "assessment_id": assessment.assessment_id,
                "standard": assessment.standard.value,
                "assessment_date": assessment.assessment_date.isoformat(),
                "assessor": assessment.assessor,
                "overall_status": assessment.overall_status.value,
                "compliance_rate": sum(1 for c in assessment.controls if c.implementation_status == ComplianceStatus.COMPLIANT) / len(assessment.controls),
                "controls": [
                    {
                        "control_id": c.control_id,
                        "title": c.title,
                        "status": c.implementation_status.value,
                        "evidence": c.evidence
                    }
                    for c in assessment.controls
                ],
                "findings": assessment.findings,
                "recommendations": assessment.recommendations,
                "next_assessment": assessment.next_assessment.isoformat()
            }, indent=2)
        elif format == "html":
            return self._generate_html_report(assessment)
        else:
            raise ValueError(f"Formato no soportado: {format}")
    
    def _generate_html_report(self, assessment: ComplianceAssessment) -> str:
        """Generar reporte HTML"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reporte de Compliance - {assessment.standard.value.upper()}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .status-compliant {{ color: green; font-weight: bold; }}
                .status-non-compliant {{ color: red; font-weight: bold; }}
                .status-partially-compliant {{ color: orange; font-weight: bold; }}
                .control {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 3px; }}
                .findings {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .recommendations {{ background-color: #d1ecf1; padding: 15px; border-radius: 5px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Reporte de Compliance - {assessment.standard.value.upper()}</h1>
                <p><strong>Fecha:</strong> {assessment.assessment_date.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Evaluador:</strong> {assessment.assessor}</p>
                <p><strong>Estado General:</strong> <span class="status-{assessment.overall_status.value}">{assessment.overall_status.value.upper()}</span></p>
            </div>
            
            <h2>Controles Evaluados</h2>
        """
        
        for control in assessment.controls:
            status_class = f"status-{control.implementation_status.value}"
            html += f"""
            <div class="control">
                <h3>{control.control_id}: {control.title}</h3>
                <p><strong>Estado:</strong> <span class="{status_class}">{control.implementation_status.value.upper()}</span></p>
                <p><strong>Descripción:</strong> {control.description}</p>
                <p><strong>Evidencia:</strong></p>
                <ul>
            """
            for evidence in control.evidence:
                html += f"<li>{evidence}</li>"
            html += "</ul></div>"
        
        if assessment.findings:
            html += """
            <h2>Hallazgos</h2>
            <div class="findings">
                <ul>
            """
            for finding in assessment.findings:
                html += f"<li>{finding}</li>"
            html += "</ul></div>"
        
        if assessment.recommendations:
            html += """
            <h2>Recomendaciones</h2>
            <div class="recommendations">
                <ul>
            """
            for recommendation in assessment.recommendations:
                html += f"<li>{recommendation}</li>"
            html += "</ul></div>"
        
        html += f"""
            <div class="header">
                <p><strong>Próxima Evaluación:</strong> {assessment.next_assessment.strftime('%Y-%m-%d')}</p>
            </div>
        </body>
        </html>
        """
        return html
    
    def check_gdpr_compliance(self) -> Dict[str, Any]:
        """Verificar compliance GDPR"""
        return self.perform_assessment(ComplianceStandard.GDPR)
    
    def check_soc2_compliance(self) -> Dict[str, Any]:
        """Verificar compliance SOC2"""
        return self.perform_assessment(ComplianceStandard.SOC2)
    
    def check_iso27001_compliance(self) -> Dict[str, Any]:
        """Verificar compliance ISO27001"""
        return self.perform_assessment(ComplianceStandard.ISO27001)

# Función de conveniencia
def create_compliance_manager() -> ComplianceManager:
    """Crear instancia del gestor de compliance"""
    return ComplianceManager()

# Ejemplo de uso
if __name__ == "__main__":
    manager = ComplianceManager()
    
    # Verificar compliance GDPR
    gdpr_report = manager.check_gdpr_compliance()
    print("GDPR Compliance:", json.dumps(gdpr_report, indent=2, default=str))
    
    # Dashboard general
    dashboard = manager.get_compliance_dashboard()
    print("Dashboard de Compliance:", json.dumps(dashboard, indent=2, default=str))
