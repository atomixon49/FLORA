#!/usr/bin/env python3
"""
FLORA Security - Inicializador de Bases de Datos
Script para inicializar las bases de datos de seguridad
"""

import sqlite3
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_audit_database():
    """Inicializar base de datos de auditoría"""
    db_path = "security_audit.db"
    
    with sqlite3.connect(db_path) as conn:
        # Tabla de eventos de seguridad
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
        
        # Tabla de detecciones de amenazas
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
        
        # Índices para mejor rendimiento
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON security_events(timestamp);
        """)
        
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_id ON security_events(user_id);
        """)
        
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_threat_level ON security_events(threat_level);
        """)
    
    logger.info(f"✅ Base de datos de auditoría inicializada: {db_path}")

def init_compliance_database():
    """Inicializar base de datos de compliance"""
    db_path = "compliance.db"
    
    with sqlite3.connect(db_path) as conn:
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
                FOREIGN KEY (control_id) REFERENCES compliance_controls (control_id)
            )
        """)
    
    logger.info(f"✅ Base de datos de compliance inicializada: {db_path}")

def main():
    """Función principal"""
    print("🌸 FLORA Security - Inicializando Bases de Datos")
    print("=" * 50)
    
    try:
        # Inicializar bases de datos
        init_audit_database()
        init_compliance_database()
        
        print("\n✅ Todas las bases de datos han sido inicializadas correctamente")
        print("📊 Ahora puedes ejecutar el dashboard de seguridad")
        print("🚀 Comando: python dashboard/security_dashboard.py")
        
    except Exception as e:
        logger.error(f"Error al inicializar bases de datos: {e}")
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
