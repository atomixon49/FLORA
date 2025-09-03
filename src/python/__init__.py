# 🌸 FLORA - Sistema de Cifrado Híbrido Post-Cuántico
# Módulo principal de Python

from .chaotic_map import ChaoticDestructionEngine
from .flora_crypto import FloraCryptoSystem

__version__ = "0.1.0-alpha"
__author__ = "Crypto Flower Team"
__description__ = "Sistema de cifrado híbrido con autodestrucción caótica"

__all__ = [
    'ChaoticDestructionEngine',
    'FloraCryptoSystem',
    '__version__',
    '__author__',
    '__description__'
]

# Función de conveniencia para crear instancia del sistema
def create_flora_system(key_size: int = 32, 
                       salt_size: int = 32, 
                       iterations: int = 100000) -> FloraCryptoSystem:
    """
    Crea una instancia del sistema FLORA con configuración por defecto.
    
    Args:
        key_size: Tamaño de clave en bytes (32 = 256 bits)
        salt_size: Tamaño del salt para derivación de claves
        iterations: Iteraciones para PBKDF2
        
    Returns:
        Instancia configurada de FloraCryptoSystem
    """
    return FloraCryptoSystem(
        key_size=key_size,
        salt_size=salt_size,
        iterations=iterations
    )

# Función de conveniencia para testing rápido
def quick_test():
    """Ejecuta una prueba rápida del sistema FLORA."""
    try:
        from .flora_crypto import test_flora_system
        test_flora_system()
        return True
    except Exception as e:
        print(f"❌ Error durante prueba rápida: {e}")
        return False
