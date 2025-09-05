"""
FLORA API - Configuration
Configuración del sistema de APIs
"""

import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Database
    database_url: str = "postgresql://flora_user:flora_password@localhost:5432/flora_db"
    redis_url: str = "redis://localhost:6379/0"
    
    # Security
    secret_key: str = "your-super-secret-key-here-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    
    # CORS
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://flora.app"
    ]
    
    # Monitoring
    sentry_dsn: str = ""
    prometheus_port: int = 9090
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    rate_limit_burst: int = 200
    
    # Encryption
    encryption_algorithm: str = "hybrid_post_quantum"
    key_rotation_days: int = 90
    
    # Webhooks
    webhook_timeout_seconds: int = 30
    webhook_retry_attempts: int = 3
    
    # Development
    debug: bool = False
    reload: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Instancia global de configuración
settings = Settings()

