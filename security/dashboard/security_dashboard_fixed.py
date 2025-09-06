"""
FLORA Security Dashboard (fixed and formatted)
FastAPI app serving a security dashboard with Jinja2 templates.
"""
from __future__ import annotations

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import logging
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List
import uvicorn

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
BASE_DIR = Path(__file__).resolve().parent
SECURITY_ROOT = BASE_DIR.parent  # .../security
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Databases (use local files placed next to this module)
# Usar las bases de datos del directorio security raíz (las que rellenan los tests)
AUDIT_DB = SECURITY_ROOT / "security_audit.db"
COMPLIANCE_DB = SECURITY_ROOT / "compliance.db"

# App
app = FastAPI(
    title="FLORA Security Dashboard",
    description="Dashboard de monitoreo de seguridad en tiempo real",
    version="1.0.0",
)

# Templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Static (optional)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _connect_db(db_path: Path) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"No se pudo conectar a la base de datos {db_path}: {e}")
        raise


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Página principal del dashboard"""
    context = {
        "request": request,
        "title": "FLORA Security Dashboard",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return templates.TemplateResponse("dashboard.html", context)


@app.get("/api/security/metrics")
async def get_security_metrics() -> Dict[str, Any]:
    """Obtener métricas de seguridad desde la base de datos de auditoría."""
    if not AUDIT_DB.exists():
        return {
            "total_events": 0,
            "operations": {},
            "threats": {},
            "success_rate": 0.0,
            "success_ratio": 0.0,
            "threat_detections": 0,
            "recent_events": [],
            "note": "AUDIT_DB no existe aún",
        }

    try:
        with _connect_db(AUDIT_DB) as conn:
            cutoff_time = datetime.now() - timedelta(hours=24)

            # Total de eventos
            try:
                cur = conn.execute(
                    "SELECT COUNT(*) FROM security_events WHERE timestamp > ?",
                    (cutoff_time.isoformat(),),
                )
                total_events = cur.fetchone()[0]
            except Exception:
                total_events = 0

            # Eventos por operación
            try:
                cur = conn.execute(
                    """
                    SELECT operation, COUNT(*) AS count
                    FROM security_events
                    WHERE timestamp > ?
                    GROUP BY operation
                    """,
                    (cutoff_time.isoformat(),),
                )
                operations = {row[0]: row[1] for row in cur.fetchall()}
            except Exception:
                operations = {}

            # Eventos por nivel de amenaza
            try:
                cur = conn.execute(
                    """
                    SELECT threat_level, COUNT(*) AS count
                    FROM security_events
                    WHERE timestamp > ?
                    GROUP BY threat_level
                    """,
                    (cutoff_time.isoformat(),),
                )
                threats = {row[0]: row[1] for row in cur.fetchall()}
            except Exception:
                threats = {}

            # Tasa de éxito
            try:
                cur = conn.execute(
                    """
                    SELECT SUM(CASE WHEN success=1 THEN 1 ELSE 0 END) AS successful,
                           COUNT(*) AS total
                    FROM security_events
                    WHERE timestamp > ?
                    """,
                    (cutoff_time.isoformat(),),
                )
                row = cur.fetchone() or (0, 0)
                successful = (row[0] or 0)
                total = (row[1] or 0)
                success_ratio = (successful / total) if total else 0.0
            except Exception:
                success_ratio = 0.0

            # Últimos eventos
            try:
                cur = conn.execute(
                    """
                    SELECT id, event_id, operation, success, threat_level, timestamp
                    FROM security_events
                    ORDER BY timestamp DESC
                    LIMIT 50
                    """
                )
                recent_events = [dict(r) for r in cur.fetchall()]
            except Exception:
                recent_events = []

            return {
                "total_events": total_events,
                "operations": operations,
                "threats": threats,
                # Mantener compatibilidad y lo que espera el template
                "success_rate": round(success_ratio, 3),
                "success_ratio": round(success_ratio, 3),
                "threat_detections": sum(threats.get(k, 0) for k in ("high", "critical")),
                "recent_events": recent_events,
            }
    except Exception as e:
        logger.error(f"Error obteniendo métricas: {e}")
        # Responder con valores por defecto para no romper el dashboard
        return {
            "total_events": 0,
            "operations": {},
            "threats": {},
            "success_rate": 0.0,
            "success_ratio": 0.0,
            "threat_detections": 0,
            "recent_events": [],
            "note": "error_loading_metrics",
        }


@app.get("/api/security/compliance")
async def get_compliance_summary() -> Dict[str, Any]:
    """Resumen de cumplimiento (opcional, si existe base de datos de compliance)."""
    if not COMPLIANCE_DB.exists():
        return {"status": "unknown", "note": "COMPLIANCE_DB no existe"}

    try:
        with _connect_db(COMPLIANCE_DB) as conn:
            cur = conn.execute(
                """
                SELECT requirement, status, updated_at
                FROM compliance_status
                ORDER BY updated_at DESC
                LIMIT 50
                """
            )
            rows = [dict(r) for r in cur.fetchall()]
            return {"status": "ok", "entries": rows}
    except Exception as e:
        logger.error(f"Error obteniendo compliance: {e}")
        # No fallar fuerte si la tabla no existe
        return {"status": "unknown", "note": str(e)}


@app.get("/api/compliance/status")
async def get_compliance_status() -> Dict[str, Any]:
    """Endpoint esperado por el template: retorna porcentajes de cumplimiento por estándar."""
    # Heurística simple basada en métricas de auditoría
    metrics = await get_security_metrics()
    total = metrics.get("total_events", 0) or 0
    success_rate = metrics.get("success_rate", 0.0) or 0.0
    high_threats = metrics.get("threats", {}).get("high", 0) + metrics.get("threats", {}).get("critical", 0)

    soc2 = min(100.0, max(0.0, success_rate * 100 - high_threats))
    gdpr = min(100.0, max(0.0, (success_rate * 100) - (high_threats * 2)))
    iso27001 = min(100.0, max(0.0, (success_rate * 100) - (high_threats * 1.5)))

    return {
        "status": "ok",
        "total_events": total,
        "compliance_percentages": {
            "soc2": round(soc2, 1),
            "gdpr": round(gdpr, 1),
            "iso27001": round(iso27001, 1),
        },
    }


@app.get("/api/threats/detected")
async def get_threats_detected() -> Dict[str, Any]:
    """Endpoint esperado por el template: lista de amenazas detectadas desde la tabla threat_detections."""
    threats: List[Dict[str, Any]] = []
    db_path = AUDIT_DB
    if not db_path.exists():
        return {"threats": []}

    try:
        with _connect_db(db_path) as conn:
            cur = conn.execute(
                """
                SELECT timestamp, event_id, pattern_id, severity, details, mitigated
                FROM threat_detections
                ORDER BY timestamp DESC
                LIMIT 50
                """
            )
            for row in cur.fetchall():
                threats.append({
                    "timestamp": row[0],
                    "event_id": row[1],
                    "pattern_id": row[2],
                    "severity": row[3],
                    "details": row[4],
                    "mitigated": bool(row[5]),
                })
    except Exception as e:
        logger.error(f"Error leyendo threat_detections: {e}")
        return {"threats": []}

    return {"threats": threats}


@app.get("/api/security/health")
async def get_security_health() -> Dict[str, Any]:
    """Endpoint esperado por el template: calcula un puntaje de salud en base a métricas."""
    metrics = await get_security_metrics()
    total = metrics.get("total_events", 0) or 0
    success_rate = metrics.get("success_rate", 0.0) or 0.0
    high_threats = metrics.get("threats", {}).get("high", 0) + metrics.get("threats", {}).get("critical", 0)

    # Health score simple: pondera éxito y penaliza amenazas altas
    base = success_rate * 100
    penalty = min(40.0, high_threats * 5.0)
    health_score = max(0.0, min(100.0, base - penalty))

    status = "healthy"
    if health_score < 60:
        status = "critical"
    elif health_score < 80:
        status = "warning"

    return {
        "status": status,
        "health_score": round(health_score, 1),
        "total_events": total,
        "success_rate": round(success_rate, 3),
        "high_threats": high_threats,
    }


if __name__ == "__main__":
    uvicorn.run(
        "security_dashboard_fixed:app",
        host="127.0.0.1",
        port=9000,
        log_level="info",
        reload=False,
        server_header=False,
        date_header=False,
    )
