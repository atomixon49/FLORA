"""
FLORA Security Dashboard
Dashboard web para monitoreo de seguridad en tiempo real
"""

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sqlite3
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="FLORA Security Dashboard",
    description="Dashboard de monitoreo de seguridad en tiempo real",
    version="1.0.0"
)

# Configurar templates
templates = Jinja2Templates(directory="templates")

# Base de datos de auditoría
AUDIT_DB = "../security_audit.db"
COMPLIANCE_DB = "../compliance.db"

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Página principal del dashboard"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "title": "FLORA Security Dashboard",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.get("/api/security/metrics")
async def get_security_metrics():
    """Obtener métricas de seguridad"""
    try:
        with sqlite3.connect(AUDIT_DB) as conn:
            # Eventos de las últimas 24 horas
            cutoff_time = datetime.now() - timedelta(hours=24)
            
            # Total de eventos
            cursor = conn.execute("""
                SELECT COUNT(*) FROM security_events 
                WHERE timestamp > ?
            """, (cutoff_time.isoformat(),))
            total_events = cursor.fetchone()[0]
            
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
            
            # Amenazas detectadas
            cursor = conn.execute("""
                SELECT COUNT(*) FROM threat_detections 
                WHERE timestamp > ?
            """, (cutoff_time.isoformat(),))
            threat_detections = cursor.fetchone()[0]
            
            # Eventos recientes (últimos 10)
            cursor = conn.execute("""
                SELECT timestamp, operation, threat_level, success, details
                FROM security_events 
                WHERE timestamp > ?
                ORDER BY timestamp DESC
                LIMIT 10
            """, (cutoff_time.isoformat(),))
            recent_events = [
                {
                    "timestamp": row[0],
                    "operation": row[1],
                    "threat_level": row[2],
                    "success": bool(row[3]),
                    "details": json.loads(row[4]) if row[4] else {}
                }
                for row in cursor.fetchall()
            ]
            
        return {
            "total_events": total_events,
            "operations": operations,
            "threat_levels": threats,
            "success_rate": success_rate,
            "threat_detections": threat_detections,
            "recent_events": recent_events,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error al obtener métricas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/compliance/status")
async def get_compliance_status():
    """Obtener estado de compliance"""
    try:
        with sqlite3.connect(COMPLIANCE_DB) as conn:
            # Obtener controles por estándar
            cursor = conn.execute("""
                SELECT standard, implementation_status, COUNT(*) as count
                FROM compliance_controls
                GROUP BY standard, implementation_status
            """)
            
            compliance_data = {}
            for row in cursor.fetchall():
                standard, status, count = row
                if standard not in compliance_data:
                    compliance_data[standard] = {}
                compliance_data[standard][status] = count
            
            # Calcular porcentajes de compliance
            compliance_percentages = {}
            for standard, statuses in compliance_data.items():
                total = sum(statuses.values())
                compliant = statuses.get("compliant", 0)
                compliance_percentages[standard] = (compliant / total * 100) if total > 0 else 0
            
            return {
                "compliance_data": compliance_data,
                "compliance_percentages": compliance_percentages,
                "timestamp": datetime.now().isoformat()
            }
    
    except Exception as e:
        logger.error(f"Error al obtener estado de compliance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/threats/detected")
async def get_detected_threats():
    """Obtener amenazas detectadas"""
    try:
        with sqlite3.connect(AUDIT_DB) as conn:
            # Amenazas de las últimas 24 horas
            cutoff_time = datetime.now() - timedelta(hours=24)
            
            cursor = conn.execute("""
                SELECT timestamp, pattern_id, severity, details, mitigated
                FROM threat_detections 
                WHERE timestamp > ?
                ORDER BY timestamp DESC
                LIMIT 20
            """, (cutoff_time.isoformat(),))
            
            threats = [
                {
                    "timestamp": row[0],
                    "pattern_id": row[1],
                    "severity": row[2],
                    "details": json.loads(row[3]) if row[3] else {},
                    "mitigated": bool(row[4])
                }
                for row in cursor.fetchall()
            ]
            
            return {
                "threats": threats,
                "total_threats": len(threats),
                "timestamp": datetime.now().isoformat()
            }
    
    except Exception as e:
        logger.error(f"Error al obtener amenazas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/security/health")
async def get_security_health():
    """Obtener estado de salud de seguridad"""
    try:
        # Verificar conectividad a bases de datos
        audit_health = False
        compliance_health = False
        
        try:
            with sqlite3.connect(AUDIT_DB) as conn:
                conn.execute("SELECT 1")
            audit_health = True
        except:
            pass
        
        try:
            with sqlite3.connect(COMPLIANCE_DB) as conn:
                conn.execute("SELECT 1")
            compliance_health = True
        except:
            pass
        
        # Obtener métricas rápidas
        with sqlite3.connect(AUDIT_DB) as conn:
            cursor = conn.execute("""
                SELECT COUNT(*) FROM security_events 
                WHERE timestamp > ?
            """, ((datetime.now() - timedelta(hours=1)).isoformat(),))
            recent_events = cursor.fetchone()[0]
            
            cursor = conn.execute("""
                SELECT COUNT(*) FROM threat_detections 
                WHERE timestamp > ? AND mitigated = 0
            """, ((datetime.now() - timedelta(hours=1)).isoformat(),))
            active_threats = cursor.fetchone()[0]
        
        health_score = 100
        if not audit_health:
            health_score -= 30
        if not compliance_health:
            health_score -= 20
        if active_threats > 0:
            health_score -= min(active_threats * 10, 50)
        
        status = "healthy" if health_score >= 80 else "warning" if health_score >= 60 else "critical"
        
        return {
            "status": status,
            "health_score": health_score,
            "audit_db": audit_health,
            "compliance_db": compliance_health,
            "recent_events": recent_events,
            "active_threats": active_threats,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error al obtener salud de seguridad: {e}")
        return {
            "status": "error",
            "health_score": 0,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/api/threats/mitigate/{threat_id}")
async def mitigate_threat(threat_id: str):
    """Marcar amenaza como mitigada"""
    try:
        with sqlite3.connect(AUDIT_DB) as conn:
            conn.execute("""
                UPDATE threat_detections 
                SET mitigated = 1 
                WHERE pattern_id = ?
            """, (threat_id,))
            
            if conn.total_changes > 0:
                return {"status": "success", "message": "Amenaza marcada como mitigada"}
            else:
                raise HTTPException(status_code=404, detail="Amenaza no encontrada")
    
    except Exception as e:
        logger.error(f"Error al mitigar amenaza: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/generate")
async def generate_security_report():
    """Generar reporte de seguridad"""
    try:
        # Obtener métricas de las últimas 24 horas
        with sqlite3.connect(AUDIT_DB) as conn:
            cutoff_time = datetime.now() - timedelta(hours=24)
            
            # Estadísticas generales
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_events,
                    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_events,
                    COUNT(DISTINCT user_id) as unique_users,
                    COUNT(DISTINCT session_id) as unique_sessions
                FROM security_events 
                WHERE timestamp > ?
            """, (cutoff_time.isoformat(),))
            
            stats = cursor.fetchone()
            
            # Top operaciones
            cursor = conn.execute("""
                SELECT operation, COUNT(*) as count
                FROM security_events 
                WHERE timestamp > ?
                GROUP BY operation
                ORDER BY count DESC
                LIMIT 5
            """, (cutoff_time.isoformat(),))
            
            top_operations = dict(cursor.fetchall())
            
            # Amenazas por severidad
            cursor = conn.execute("""
                SELECT severity, COUNT(*) as count
                FROM threat_detections 
                WHERE timestamp > ?
                GROUP BY severity
            """, (cutoff_time.isoformat(),))
            
            threats_by_severity = dict(cursor.fetchall())
        
        report = {
            "report_id": f"SECURITY-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "period": "24 hours",
            "generated_at": datetime.now().isoformat(),
            "statistics": {
                "total_events": stats[0],
                "successful_events": stats[1],
                "success_rate": stats[1] / stats[0] if stats[0] > 0 else 0,
                "unique_users": stats[2],
                "unique_sessions": stats[3]
            },
            "top_operations": top_operations,
            "threats_by_severity": threats_by_severity
        }
        
        return report
    
    except Exception as e:
        logger.error(f"Error al generar reporte: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Crear directorio de templates si no existe
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)

# Crear template HTML básico
dashboard_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .metric-label {
            color: #666;
            margin-top: 5px;
        }
        .status-healthy { color: #28a745; }
        .status-warning { color: #ffc107; }
        .status-critical { color: #dc3545; }
        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 20px;
        }
        .refresh-btn:hover {
            background: #5a6fd8;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌸 FLORA Security Dashboard</h1>
        <p>Monitoreo de Seguridad en Tiempo Real - {{ timestamp }}</p>
    </div>
    
    <button class="refresh-btn" onclick="loadData()">🔄 Actualizar Datos</button>
    
    <div class="metrics-grid" id="metricsGrid">
        <!-- Las métricas se cargarán aquí -->
    </div>
    
    <div class="chart-container">
        <h3>📊 Eventos Recientes</h3>
        <div id="recentEvents">
            <!-- Los eventos se cargarán aquí -->
        </div>
    </div>
    
    <div class="chart-container">
        <h3>🛡️ Estado de Compliance</h3>
        <div id="complianceStatus">
            <!-- El estado de compliance se cargará aquí -->
        </div>
    </div>
    
    <div class="chart-container">
        <h3>⚠️ Amenazas Detectadas</h3>
        <div id="threatsDetected">
            <!-- Las amenazas se cargarán aquí -->
        </div>
    </div>

    <script>
        async function loadData() {
            try {
                // Cargar métricas de seguridad
                const metricsResponse = await fetch('/api/security/metrics');
                const metrics = await metricsResponse.json();
                
                // Cargar estado de compliance
                const complianceResponse = await fetch('/api/compliance/status');
                const compliance = await complianceResponse.json();
                
                // Cargar amenazas detectadas
                const threatsResponse = await fetch('/api/threats/detected');
                const threats = await threatsResponse.json();
                
                // Cargar salud de seguridad
                const healthResponse = await fetch('/api/security/health');
                const health = await healthResponse.json();
                
                updateMetrics(metrics, health);
                updateRecentEvents(metrics);
                updateCompliance(compliance);
                updateThreats(threats);
                
            } catch (error) {
                console.error('Error al cargar datos:', error);
            }
        }
        
        function updateMetrics(metrics, health) {
            const grid = document.getElementById('metricsGrid');
            grid.innerHTML = `
                <div class="metric-card">
                    <div class="metric-value">${metrics.total_events}</div>
                    <div class="metric-label">Eventos (24h)</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${(metrics.success_rate * 100).toFixed(1)}%</div>
                    <div class="metric-label">Tasa de Éxito</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value status-${health.status}">${health.health_score}</div>
                    <div class="metric-label">Puntuación de Salud</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${metrics.threat_detections}</div>
                    <div class="metric-label">Amenazas Detectadas</div>
                </div>
            `;
        }
        
        function updateRecentEvents(metrics) {
            const container = document.getElementById('recentEvents');
            const events = metrics.recent_events.slice(0, 5);
            
            container.innerHTML = events.map(event => `
                <div style="padding: 10px; border-left: 4px solid ${event.success ? '#28a745' : '#dc3545'}; margin-bottom: 10px; background: #f8f9fa;">
                    <strong>${event.operation}</strong> - ${event.threat_level} - ${event.timestamp}
                </div>
            `).join('');
        }
        
        function updateCompliance(compliance) {
            const container = document.getElementById('complianceStatus');
            const percentages = compliance.compliance_percentages;
            
            container.innerHTML = Object.entries(percentages).map(([standard, percentage]) => `
                <div style="margin-bottom: 10px;">
                    <strong>${standard.toUpperCase()}:</strong> 
                    <span class="status-${percentage >= 80 ? 'healthy' : percentage >= 60 ? 'warning' : 'critical'}">
                        ${percentage.toFixed(1)}%
                    </span>
                </div>
            `).join('');
        }
        
        function updateThreats(threats) {
            const container = document.getElementById('threatsDetected');
            const threatList = threats.threats.slice(0, 5);
            
            if (threatList.length === 0) {
                container.innerHTML = '<p>✅ No hay amenazas activas</p>';
                return;
            }
            
            container.innerHTML = threatList.map(threat => `
                <div style="padding: 10px; border-left: 4px solid ${threat.severity === 'critical' ? '#dc3545' : threat.severity === 'high' ? '#fd7e14' : '#ffc107'}; margin-bottom: 10px; background: #f8f9fa;">
                    <strong>${threat.pattern_id}</strong> - ${threat.severity} - ${threat.timestamp}
                    ${threat.mitigated ? '<span style="color: #28a745;">✅ Mitigada</span>' : '<span style="color: #dc3545;">⚠️ Activa</span>'}
                </div>
            `).join('');
        }
        
        // Cargar datos al cargar la página
        loadData();
        
        // Actualizar cada 30 segundos
        setInterval(loadData, 30000);
    </script>
</body>
</html>
"""

# Escribir template HTML
with open(templates_dir / "dashboard.html", "w", encoding="utf-8") as f:
    f.write(dashboard_html)

if __name__ == "__main__":
    print("🌸 Iniciando FLORA Security Dashboard...")
    print("📊 Dashboard disponible en: http://localhost:8080")
    print("🔍 API disponible en: http://localhost:8080/docs")
    
    uvicorn.run(
        "security_dashboard:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
