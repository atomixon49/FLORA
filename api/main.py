"""
FLORA API - Enterprise Integration System
Sistema de APIs REST para integración empresarial con cifrado híbrido post-cuántico
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
import uvicorn
import logging
from datetime import datetime, timedelta
import hashlib
import secrets
import string

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="FLORA API",
    description="Sistema de APIs para integración empresarial con cifrado híbrido post-cuántico",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema de autenticación
security = HTTPBearer()

# Base de datos simulada (en producción usar PostgreSQL)
fake_db = {
    "users": {},
    "encryption_keys": {},
    "api_keys": {},
    "audit_logs": []
}

# Crear API key de prueba
test_api_key = "test_api_key_12345678901234567890"
fake_db["api_keys"][test_api_key] = {
    "key_id": "test_key_001",
    "name": "API Key de Prueba",
    "permissions": ["encrypt", "decrypt", "read"],
    "expires_at": datetime.now() + timedelta(days=365),
    "created_at": datetime.now()
}

# Funciones de autenticación
def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verificar API key"""
    api_key = credentials.credentials
    
    # Simulación de verificación (en producción usar base de datos)
    if api_key not in fake_db["api_keys"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida"
        )
    
    key_data = fake_db["api_keys"][api_key]
    if key_data["expires_at"] < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key expirada"
        )
    
    return key_data

def simulate_encryption(data: str, key_id: str) -> str:
    """Simular cifrado híbrido post-cuántico"""
    # En producción, usar el motor Rust de FLORA
    key_hash = hashlib.sha256(key_id.encode()).hexdigest()[:16]
    return f"FLORA:{key_hash}:{data.encode().hex()}"

def simulate_decryption(encrypted_data: str, key_id: str) -> str:
    """Simular desifrado híbrido post-cuántico"""
    # En producción, usar el motor Rust de FLORA
    if not encrypted_data.startswith("FLORA:"):
        raise ValueError("Formato de datos cifrados inválido")
    
    parts = encrypted_data.split(":")
    if len(parts) != 3:
        raise ValueError("Formato de datos cifrados inválido")
    
    try:
        decrypted_bytes = bytes.fromhex(parts[2])
        return decrypted_bytes.decode('utf-8')
    except:
        raise ValueError("Error al desifrar datos")

# Endpoints principales
@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "🌸 FLORA API - Sistema de Cifrado Híbrido Post-Cuántico",
        "version": "1.0.0",
        "status": "active",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Verificación de salud del sistema"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "encryption": "active",
            "database": "active",
            "authentication": "active"
        }
    }

@app.post("/api/v1/encrypt")
async def encrypt_data(
    data: dict,
    api_key_data: dict = Depends(verify_api_key)
):
    """Cifrar datos usando cifrado híbrido post-cuántico"""
    try:
        text_data = data.get("data", "")
        if not text_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campo 'data' requerido"
            )
        
        # Generar ID de clave único
        key_id = f"key_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{api_key_data['key_id']}"
        
        # Simular cifrado
        encrypted_data = simulate_encryption(text_data, key_id)
        
        # Almacenar en base de datos simulada
        fake_db["encryption_keys"][key_id] = {
            "algorithm": "hybrid_post_quantum",
            "created_at": datetime.now(),
            "api_key_id": api_key_data["key_id"]
        }
        
        # Registrar en auditoría
        fake_db["audit_logs"].append({
            "action": "encrypt",
            "key_id": key_id,
            "api_key_id": api_key_data["key_id"],
            "timestamp": datetime.now(),
            "data_size": len(text_data)
        })
        
        return {
            "encrypted_data": encrypted_data,
            "key_id": key_id,
            "algorithm": "hybrid_post_quantum",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error en cifrado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cifrar datos: {str(e)}"
        )

@app.post("/api/v1/decrypt")
async def decrypt_data(
    data: dict,
    api_key_data: dict = Depends(verify_api_key)
):
    """Desifrar datos usando cifrado híbrido post-cuántico"""
    try:
        encrypted_data = data.get("encrypted_data", "")
        key_id = data.get("key_id", "")
        
        if not encrypted_data or not key_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campos 'encrypted_data' y 'key_id' requeridos"
            )
        
        # Verificar que la clave existe
        if key_id not in fake_db["encryption_keys"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clave de cifrado no encontrada"
            )
        
        # Simular desifrado
        decrypted_data = simulate_decryption(encrypted_data, key_id)
        
        # Registrar en auditoría
        fake_db["audit_logs"].append({
            "action": "decrypt",
            "key_id": key_id,
            "api_key_id": api_key_data["key_id"],
            "timestamp": datetime.now(),
            "data_size": len(decrypted_data)
        })
        
        return {
            "decrypted_data": decrypted_data,
            "key_id": key_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error en desifrado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desifrar datos: {str(e)}"
        )

@app.get("/api/v1/stats")
async def get_statistics(api_key_data: dict = Depends(verify_api_key)):
    """Obtener estadísticas de uso"""
    user_logs = [
        log for log in fake_db["audit_logs"]
        if log["api_key_id"] == api_key_data["key_id"]
    ]
    
    encrypt_count = len([log for log in user_logs if log["action"] == "encrypt"])
    decrypt_count = len([log for log in user_logs if log["action"] == "decrypt"])
    
    return {
        "total_operations": len(user_logs),
        "encrypt_operations": encrypt_count,
        "decrypt_operations": decrypt_count,
        "api_key_id": api_key_data["key_id"],
        "created_at": api_key_data["created_at"].isoformat()
    }

@app.get("/api/v1/audit")
async def get_audit_logs(api_key_data: dict = Depends(verify_api_key)):
    """Obtener logs de auditoría"""
    user_logs = [
        log for log in fake_db["audit_logs"]
        if log["api_key_id"] == api_key_data["key_id"]
    ]
    
    return {
        "logs": user_logs[-10:],  # Últimos 10 logs
        "total": len(user_logs)
    }

# Manejo de errores globales
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Error global: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

if __name__ == "__main__":
    logger.info("🌸 FLORA API iniciada")
    logger.info(f"API Key de prueba: {test_api_key}")
    logger.info("Documentación disponible en: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
