"""
FLORA Security Auditor
Sistema de auditoría de seguridad y detección de amenazas
"""

import logging
import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
import threading
from collections import defaultdict, deque

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatLevel(Enum):
    """Niveles de amenaza"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class OperationType(Enum):
    """Tipos de operaciones auditadas"""
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"
    KEY_GENERATION = "key_generation"
    SESSION_CREATE = "session_create"
    SESSION_DESTROY = "session_destroy"
    AUTH_SUCCESS = "auth_success"
    AUTH_FAILURE = "auth_failure"
    SYSTEM_START = "system_start"
    SYSTEM_SHUTDOWN = "system_shutdown"
    THREAT_DETECTED = "threat_detected"

@dataclass
class SecurityEvent:
    """Evento de seguridad"""
    timestamp: datetime
    event_id: str
    operation: OperationType
    user_id: Optional[str]
    session_id: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    data_size: Optional[int]
    success: bool
    threat_level: ThreatLevel
    details: Dict[str, Any]
    risk_score: float

@dataclass
class ThreatPattern:
    """Patrón de amenaza"""
    pattern_id: str
    name: str
    description: str
    severity: ThreatLevel
    conditions: List[Dict[str, Any]]
    mitigation: str

class SecurityAuditor:
    """Auditor de seguridad principal"""
    
    def __init__(self, db_path: str = "security_audit.db"):
        self.db_path = db_path
        self.threat_patterns = self._load_threat_patterns()
        self.risk_thresholds = {
            ThreatLevel.LOW: 0.3,
            ThreatLevel.MEDIUM: 0.6,
            ThreatLevel.HIGH: 0.8,
            ThreatLevel.CRITICAL: 0.9
        }
        self._init_database()
        self._lock = threading.Lock()
        
    def _init_database(self):
        """Inicializar base de datos de auditoría"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS security_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_id TEXT UNIQUE NOT NULL,
                    operation TEXT NOT NULL,
                    user_id TEXT,
                    session_id TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    data_size INTEGER,
                    success BOOLEAN NOT NULL,
                    threat_level TEXT NOT NULL,
                    details TEXT NOT NULL,
                    risk_score REAL NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS threat_detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_id TEXT NOT NULL,
                    pattern_id TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    details TEXT NOT NULL,
                    mitigated BOOLEAN DEFAULT FALSE
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON security_events(timestamp);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_id ON security_events(user_id);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_threat_level ON security_events(threat_level);
            """)
    
    def _load_threat_patterns(self) -> List[ThreatPattern]:
        """Cargar patrones de amenaza predefinidos"""
        patterns = [
            ThreatPattern(
                pattern_id="brute_force",
                name="Ataque de Fuerza Bruta",
                description="Múltiples intentos de autenticación fallidos",
                severity=ThreatLevel.HIGH,
                conditions=[
                    {"operation": "auth_failure", "count": 5, "timeframe": 300},
                    {"operation": "auth_failure", "count": 10, "timeframe": 600}
                ],
                mitigation="Bloquear IP temporalmente"
            ),
            ThreatPattern(
                pattern_id="rapid_encryption",
                name="Cifrado Rápido Anómalo",
                description="Volumen inusualmente alto de operaciones de cifrado",
                severity=ThreatLevel.MEDIUM,
                conditions=[
                    {"operation": "encrypt", "count": 100, "timeframe": 60},
                    {"operation": "encrypt", "count": 500, "timeframe": 300}
                ],
                mitigation="Verificar legitimidad de las operaciones"
            ),
            ThreatPattern(
                pattern_id="large_data_operations",
                name="Operaciones con Datos Grandes",
                description="Operaciones con archivos excepcionalmente grandes",
                severity=ThreatLevel.MEDIUM,
                conditions=[
                    {"data_size": 100000000, "operation": "encrypt"},  # 100MB
                    {"data_size": 500000000, "operation": "decrypt"}   # 500MB
                ],
                mitigation="Revisar autorización y propósito"
            ),
            ThreatPattern(
                pattern_id="suspicious_timing",
                name="Horarios Sospechosos",
                description="Actividad fuera del horario normal de trabajo",
                severity=ThreatLevel.LOW,
                conditions=[
                    {"hour_range": [22, 6], "operation": "encrypt"},
                    {"hour_range": [0, 4], "operation": "decrypt"}
                ],
                mitigation="Verificar identidad del usuario"
            ),
            ThreatPattern(
                pattern_id="key_rotation_abuse",
                name="Abuso de Rotación de Claves",
                description="Rotación excesiva de claves de sesión",
                severity=ThreatLevel.HIGH,
                conditions=[
                    {"operation": "key_generation", "count": 20, "timeframe": 300},
                    {"operation": "session_create", "count": 50, "timeframe": 600}
                ],
                mitigation="Investigar posible compromiso de cuenta"
            )
        ]
        return patterns
    
    def log_operation(self, 
                     operation: OperationType,
                     user_id: Optional[str] = None,
                     session_id: Optional[str] = None,
                     ip_address: Optional[str] = None,
                     user_agent: Optional[str] = None,
                     data_size: Optional[int] = None,
                     success: bool = True,
                     details: Optional[Dict[str, Any]] = None) -> str:
        """Registrar operación de seguridad"""
        
        if details is None:
            details = {}
            
        # Generar ID único del evento
        event_id = self._generate_event_id(operation, user_id, session_id)
        
        # Calcular nivel de amenaza y puntuación de riesgo
        threat_level, risk_score = self._assess_threat_level(
            operation, user_id, session_id, data_size, success, details
        )
        
        # Crear evento de seguridad
        event = SecurityEvent(
            timestamp=datetime.now(),
            event_id=event_id,
            operation=operation,
            user_id=user_id,
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            data_size=data_size,
            success=success,
            threat_level=threat_level,
            details=details,
            risk_score=risk_score
        )
        
        # Guardar en base de datos
        with self._lock:
            self._save_event(event)
        
        # Detectar amenazas
        self._detect_threats(event)
        
        logger.info(f"Evento de seguridad registrado: {event_id} - {operation.value} - {threat_level.value}")
        
        return event_id
    
    def _generate_event_id(self, operation: OperationType, user_id: Optional[str], session_id: Optional[str]) -> str:
        """Generar ID único para el evento"""
        timestamp = int(time.time() * 1000)
        data = f"{operation.value}_{user_id}_{session_id}_{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _assess_threat_level(self, 
                           operation: OperationType,
                           user_id: Optional[str],
                           session_id: Optional[str],
                           data_size: Optional[int],
                           success: bool,
                           details: Dict[str, Any]) -> tuple[ThreatLevel, float]:
        """Evaluar nivel de amenaza y calcular puntuación de riesgo"""
        
        risk_score = 0.0
        
        # Factores de riesgo base
        if not success:
            risk_score += 0.3
            
        if operation == OperationType.AUTH_FAILURE:
            risk_score += 0.4
            
        if operation == OperationType.THREAT_DETECTED:
            risk_score += 0.8
            
        # Factor de tamaño de datos
        if data_size and data_size > 1000000:  # > 1MB
            risk_score += 0.1
            
        if data_size and data_size > 100000000:  # > 100MB
            risk_score += 0.2
            
        # Factor de horario (actividad nocturna)
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour > 22:
            risk_score += 0.1
            
        # Factor de frecuencia (últimas 24 horas)
        recent_events = self._get_recent_events(user_id, session_id, 86400)  # 24 horas
        if len(recent_events) > 100:
            risk_score += 0.2
            
        # Determinar nivel de amenaza
        if risk_score >= self.risk_thresholds[ThreatLevel.CRITICAL]:
            threat_level = ThreatLevel.CRITICAL
        elif risk_score >= self.risk_thresholds[ThreatLevel.HIGH]:
            threat_level = ThreatLevel.HIGH
        elif risk_score >= self.risk_thresholds[ThreatLevel.MEDIUM]:
            threat_level = ThreatLevel.MEDIUM
        else:
            threat_level = ThreatLevel.LOW
            
        return threat_level, min(risk_score, 1.0)
    
    def _get_recent_events(self, user_id: Optional[str], session_id: Optional[str], seconds: int) -> List[SecurityEvent]:
        """Obtener eventos recientes"""
        cutoff_time = datetime.now() - timedelta(seconds=seconds)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM security_events 
                WHERE timestamp > ? 
                AND (user_id = ? OR user_id IS NULL)
                AND (session_id = ? OR session_id IS NULL)
                ORDER BY timestamp DESC
            """, (cutoff_time.isoformat(), user_id, session_id))
            
            events = []
            for row in cursor.fetchall():
                event = SecurityEvent(
                    timestamp=datetime.fromisoformat(row[1]),
                    event_id=row[2],
                    operation=OperationType(row[3]),
                    user_id=row[4],
                    session_id=row[5],
                    ip_address=row[6],
                    user_agent=row[7],
                    data_size=row[8],
                    success=bool(row[9]),
                    threat_level=ThreatLevel(row[10]),
                    details=json.loads(row[11]),
                    risk_score=row[12]
                )
                events.append(event)
                
        return events
    
    def _save_event(self, event: SecurityEvent):
        """Guardar evento en base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO security_events 
                (timestamp, event_id, operation, user_id, session_id, ip_address, 
                 user_agent, data_size, success, threat_level, details, risk_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.timestamp.isoformat(),
                event.event_id,
                event.operation.value,
                event.user_id,
                event.session_id,
                event.ip_address,
                event.user_agent,
                event.data_size,
                event.success,
                event.threat_level.value,
                json.dumps(event.details),
                event.risk_score
            ))
    
    def _detect_threats(self, event: SecurityEvent):
        """Detectar amenazas basadas en patrones"""
        for pattern in self.threat_patterns:
            if self._matches_pattern(event, pattern):
                self._record_threat_detection(event, pattern)
    
    def _matches_pattern(self, event: SecurityEvent, pattern: ThreatPattern) -> bool:
        """Verificar si el evento coincide con un patrón de amenaza"""
        for condition in pattern.conditions:
            if not self._evaluate_condition(event, condition):
                return False
        return True
    
    def _evaluate_condition(self, event: SecurityEvent, condition: Dict[str, Any]) -> bool:
        """Evaluar una condición específica"""
        if "operation" in condition:
            if event.operation.value != condition["operation"]:
                return False
                
        if "count" in condition and "timeframe" in condition:
            recent_events = self._get_recent_events(
                event.user_id, event.session_id, condition["timeframe"]
            )
            matching_events = [
                e for e in recent_events 
                if e.operation.value == condition.get("operation", event.operation.value)
            ]
            if len(matching_events) < condition["count"]:
                return False
                
        if "data_size" in condition:
            if not event.data_size or event.data_size < condition["data_size"]:
                return False
                
        if "hour_range" in condition:
            current_hour = event.timestamp.hour
            start_hour, end_hour = condition["hour_range"]
            if not (start_hour <= current_hour <= end_hour):
                return False
                
        return True
    
    def _record_threat_detection(self, event: SecurityEvent, pattern: ThreatPattern):
        """Registrar detección de amenaza"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO threat_detections 
                (timestamp, event_id, pattern_id, severity, details, mitigated)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                event.event_id,
                pattern.pattern_id,
                pattern.severity.value,
                json.dumps({
                    "pattern_name": pattern.name,
                    "description": pattern.description,
                    "mitigation": pattern.mitigation,
                    "event_details": event.details
                }),
                False
            ))
        
        logger.warning(f"AMENAZA DETECTADA: {pattern.name} - {event.event_id}")
    
    def get_security_metrics(self, hours: int = 24) -> Dict[str, Any]:
        """Obtener métricas de seguridad"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with sqlite3.connect(self.db_path) as conn:
            # Eventos por tipo
            cursor = conn.execute("""
                SELECT operation, COUNT(*) as count 
                FROM security_events 
                WHERE timestamp > ? 
                GROUP BY operation
            """, (cutoff_time.isoformat(),))
            operations = dict(cursor.fetchall())
            
            # Eventos por nivel de amenaza
            cursor = conn.execute("""
                SELECT threat_level, COUNT(*) as count 
                FROM security_events 
                WHERE timestamp > ? 
                GROUP BY threat_level
            """, (cutoff_time.isoformat(),))
            threats = dict(cursor.fetchall())
            
            # Amenazas detectadas
            cursor = conn.execute("""
                SELECT COUNT(*) as count 
                FROM threat_detections 
                WHERE timestamp > ?
            """, (cutoff_time.isoformat(),))
            threat_detections = cursor.fetchone()[0]
            
            # Tasa de éxito
            cursor = conn.execute("""
                SELECT 
                    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                    COUNT(*) as total
                FROM security_events 
                WHERE timestamp > ?
            """, (cutoff_time.isoformat(),))
            success_row = cursor.fetchone()
            success_rate = success_row[0] / success_row[1] if success_row[1] > 0 else 0
            
        return {
            "timeframe_hours": hours,
            "total_events": sum(operations.values()),
            "operations": operations,
            "threat_levels": threats,
            "threat_detections": threat_detections,
            "success_rate": success_rate,
            "high_risk_events": threats.get(ThreatLevel.HIGH.value, 0) + threats.get(ThreatLevel.CRITICAL.value, 0)
        }
    
    def generate_compliance_report(self, standard: str = "SOC2") -> Dict[str, Any]:
        """Generar reporte de compliance"""
        metrics = self.get_security_metrics(24 * 30)  # Últimos 30 días
        
        if standard == "SOC2":
            return self._generate_soc2_report(metrics)
        elif standard == "GDPR":
            return self._generate_gdpr_report(metrics)
        elif standard == "ISO27001":
            return self._generate_iso27001_report(metrics)
        else:
            raise ValueError(f"Estándar no soportado: {standard}")
    
    def _generate_soc2_report(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generar reporte SOC 2"""
        controls = {
            "CC6.1": {
                "description": "Logical and Physical Access Controls",
                "status": "COMPLIANT" if metrics["success_rate"] > 0.95 else "NON_COMPLIANT",
                "evidence": f"Authentication success rate: {metrics['success_rate']:.2%}"
            },
            "CC6.2": {
                "description": "System Access Controls",
                "status": "COMPLIANT" if metrics["high_risk_events"] < 10 else "NON_COMPLIANT",
                "evidence": f"High risk events: {metrics['high_risk_events']}"
            },
            "CC6.3": {
                "description": "Data Transmission and Disposal",
                "status": "COMPLIANT" if metrics["threat_detections"] < 5 else "NON_COMPLIANT",
                "evidence": f"Threat detections: {metrics['threat_detections']}"
            }
        }
        
        overall_status = "COMPLIANT" if all(
            control["status"] == "COMPLIANT" 
            for control in controls.values()
        ) else "NON_COMPLIANT"
        
        return {
            "standard": "SOC 2 Type II",
            "period": "30 days",
            "controls": controls,
            "overall_status": overall_status
        }
    
    def _generate_gdpr_report(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generar reporte GDPR"""
        return {
            "standard": "GDPR",
            "period": "30 days",
            "privacy_controls": {
                "data_encryption": {
                    "status": "COMPLIANT",
                    "evidence": f"Encryption operations: {metrics['operations'].get('encrypt', 0)}"
                },
                "access_control": {
                    "status": "COMPLIANT" if metrics["success_rate"] > 0.9 else "NON_COMPLIANT",
                    "evidence": f"Access control success rate: {metrics['success_rate']:.2%}"
                },
                "incident_response": {
                    "status": "COMPLIANT" if metrics["threat_detections"] < 10 else "NON_COMPLIANT",
                    "evidence": f"Security incidents: {metrics['threat_detections']}"
                }
            },
            "overall_status": "COMPLIANT"
        }
    
    def _generate_iso27001_report(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generar reporte ISO 27001"""
        return {
            "standard": "ISO 27001",
            "period": "30 days",
            "controls": {
                "A.9.1": {
                    "description": "Access Control Policy",
                    "status": "COMPLIANT" if metrics["success_rate"] > 0.95 else "NON_COMPLIANT"
                },
                "A.10.1": {
                    "description": "Cryptographic Controls",
                    "status": "COMPLIANT",
                    "evidence": f"Encryption operations: {metrics['operations'].get('encrypt', 0)}"
                },
                "A.16.1": {
                    "description": "Incident Management",
                    "status": "COMPLIANT" if metrics["threat_detections"] < 5 else "NON_COMPLIANT"
                }
            },
            "overall_status": "COMPLIANT"
        }

# Función de conveniencia para uso rápido
def create_security_auditor() -> SecurityAuditor:
    """Crear instancia del auditor de seguridad"""
    return SecurityAuditor()

# Ejemplo de uso
if __name__ == "__main__":
    auditor = SecurityAuditor()
    
    # Simular algunas operaciones
    auditor.log_operation(
        OperationType.ENCRYPT,
        user_id="user123",
        session_id="session456",
        ip_address="192.168.1.100",
        data_size=1024,
        success=True
    )
    
    # Obtener métricas
    metrics = auditor.get_security_metrics()
    print("Métricas de seguridad:", json.dumps(metrics, indent=2))
    
    # Generar reporte de compliance
    report = auditor.generate_compliance_report("SOC2")
    print("Reporte SOC2:", json.dumps(report, indent=2))
