# 🌸 FLORA - Mapa Caótico para Autodestrucción
# Implementación del mapa logístico para corrupción irreversible de claves

import numpy as np
import hashlib
from typing import Tuple, List, Optional
import time

class ChaoticDestructionEngine:
    """
    Motor de autodestrucción basado en el mapa logístico caótico.
    
    Este sistema utiliza la sensibilidad extrema a las condiciones iniciales
    para garantizar que cualquier perturbación mínima resulte en corrupción
    total e irreversible de las claves criptográficas.
    """
    
    def __init__(self, r_param: float = 3.9987654321098765):
        """
        Inicializa el motor de autodestrucción caótica.
        
        Args:
            r_param: Parámetro de control del mapa logístico (3.57 < r < 4.0)
                     Valores más cercanos a 4.0 producen comportamiento más caótico
        """
        if not (3.57 < r_param < 4.0):
            raise ValueError("r_param debe estar en el rango (3.57, 4.0) para comportamiento caótico")
        
        self.r_param = r_param
        self.initial_conditions = None
        self.destruction_history = []
        
    def initialize_chaos_seed(self, key_material: bytes, timestamp: Optional[float] = None) -> Tuple[float, float]:
        """
        Inicializa la semilla caótica a partir del material de clave.
        
        Args:
            key_material: Material de clave para generar semilla
            timestamp: Timestamp opcional para mayor entropía
            
        Returns:
            Tuple con (r_perturbado, x0_perturbado)
        """
        # Generar hash del material de clave
        key_hash = hashlib.sha256(key_material).digest()
        
        # Convertir hash a valores flotantes para el mapa caótico
        hash_int = int.from_bytes(key_hash[:8], 'big')
        x0 = (hash_int % 1000000) / 1000000.0  # Normalizar a [0, 1)
        
        # Perturbar ligeramente el parámetro r para mayor entropía
        r_perturbed = self.r_param + (hash_int % 1000) / 10000000.0
        
        # Asegurar que r permanezca en rango caótico
        r_perturbed = max(3.57, min(3.999, r_perturbed))
        
        self.initial_conditions = (r_perturbed, x0)
        
        return r_perturbed, x0
    
    def logistic_map_iteration(self, x: float, r: float) -> float:
        """
        Una iteración del mapa logístico: x_{n+1} = r * x_n * (1 - x_n)
        
        Args:
            x: Valor actual del estado
            r: Parámetro de control
            
        Returns:
            Nuevo valor del estado
        """
        return r * x * (1 - x)
    
    def generate_destruction_sequence(self, 
                                    iterations: int = 10000,
                                    perturbation_hash: Optional[bytes] = None) -> List[float]:
        """
        Genera secuencia de destrucción usando el mapa caótico.
        
        Args:
            iterations: Número de iteraciones para generar secuencia
            perturbation_hash: Hash del intento de ataque para perturbar el sistema
            
        Returns:
            Lista de valores caóticos para corrupción
        """
        if self.initial_conditions is None:
            raise RuntimeError("Debe inicializar la semilla caótica primero")
        
        r, x = self.initial_conditions
        
        # Si hay perturbación (intento de ataque), modificar parámetros
        if perturbation_hash:
            r, x = self._apply_attack_perturbation(r, x, perturbation_hash)
        
        # Generar secuencia caótica
        sequence = []
        current_x = x
        
        for i in range(iterations):
            current_x = self.logistic_map_iteration(current_x, r)
            sequence.append(current_x)
            
            # Cada 1000 iteraciones, registrar el estado para debugging
            if i % 1000 == 0:
                self.destruction_history.append({
                    'iteration': i,
                    'x_value': current_x,
                    'r_value': r,
                    'timestamp': time.time()
                })
        
        return sequence
    
    def _apply_attack_perturbation(self, r: float, x: float, attack_hash: bytes) -> Tuple[float, float]:
        """
        Aplica perturbación del ataque a los parámetros caóticos.
        
        Args:
            r: Parámetro r original
            x: Estado x original
            attack_hash: Hash del intento de ataque
            
        Returns:
            Parámetros perturbados (r_perturbado, x_perturbado)
        """
        # Convertir hash a valores de perturbación
        hash_int = int.from_bytes(attack_hash[:8], 'big')
        
        # Perturbación no reversible usando XOR
        r_perturbed = r + (hash_int % 1000) / 1000000.0
        x_perturbed = x + ((hash_int >> 8) % 1000) / 1000000.0
        
        # Asegurar que los valores permanezcan en rangos válidos
        r_perturbed = max(3.57, min(3.999, r_perturbed))
        x_perturbed = max(0.0, min(0.999, x_perturbed))
        
        return r_perturbed, x_perturbed
    
    def corrupt_key_material(self, 
                           key_material: bytes, 
                           attack_hash: Optional[bytes] = None) -> bytes:
        """
        Corrompe irreversiblemente el material de clave usando caos.
        
        Args:
            key_material: Material de clave a corromper
            attack_hash: Hash del intento de ataque (opcional)
            
        Returns:
            Material de clave corrompido (irreversible)
        """
        # Generar secuencia de destrucción
        destruction_sequence = self.generate_destruction_sequence(
            iterations=len(key_material) * 10,  # Más iteraciones que bytes
            perturbation_hash=attack_hash
        )
        
        # Convertir secuencia caótica a bytes de corrupción
        corruption_bytes = self._sequence_to_corruption_bytes(destruction_sequence)
        
        # Aplicar corrupción XOR al material de clave
        corrupted_material = bytearray()
        for i, key_byte in enumerate(key_material):
            corruption_byte = corruption_bytes[i % len(corruption_bytes)]
            corrupted_byte = key_byte ^ corruption_byte
            corrupted_material.append(corrupted_byte)
        
        return bytes(corrupted_material)
    
    def _sequence_to_corruption_bytes(self, sequence: List[float]) -> bytes:
        """
        Convierte secuencia caótica a bytes de corrupción.
        
        Args:
            sequence: Lista de valores flotantes caóticos
            
        Returns:
            Bytes de corrupción
        """
        corruption_bytes = bytearray()
        
        for value in sequence:
            # Convertir valor flotante [0, 1) a byte [0, 255]
            byte_value = int(value * 256) % 256
            corruption_bytes.append(byte_value)
        
        return bytes(corruption_bytes)
    
    def get_destruction_statistics(self) -> dict:
        """
        Obtiene estadísticas del proceso de destrucción.
        
        Returns:
            Diccionario con estadísticas de destrucción
        """
        if not self.destruction_history:
            return {"status": "No destruction events recorded"}
        
        x_values = [event['x_value'] for event in self.destruction_history]
        r_values = [event['r_value'] for event in self.destruction_history]
        
        return {
            "total_events": len(self.destruction_history),
            "x_range": (min(x_values), max(x_values)),
            "r_range": (min(r_values), max(r_values)),
            "x_variance": np.var(x_values),
            "r_variance": np.var(r_values),
            "last_event": self.destruction_history[-1] if self.destruction_history else None
        }
    
    def reset_destruction_engine(self):
        """Resetea el motor de destrucción a estado inicial."""
        self.initial_conditions = None
        self.destruction_history.clear()


# Función de utilidad para testing
def test_chaotic_destruction():
    """Función de prueba para el motor de autodestrucción caótica."""
    print("🧪 Probando Motor de Autodestrucción Caótica...")
    
    # Crear instancia del motor
    engine = ChaoticDestructionEngine()
    
    # Material de clave de prueba
    test_key = b"FLORA_TEST_KEY_2024_CRYPTO_FLOWER"
    
    # Inicializar semilla caótica
    r, x0 = engine.initialize_chaos_seed(test_key)
    print(f"✅ Semilla caótica inicializada: r={r:.6f}, x0={x0:.6f}")
    
    # Simular ataque (hash de intento de manipulación)
    attack_hash = hashlib.sha256(b"ATTACK_ATTEMPT").digest()
    
    # Generar secuencia de destrucción
    destruction_seq = engine.generate_destruction_sequence(
        iterations=1000, 
        perturbation_hash=attack_hash
    )
    print(f"✅ Secuencia de destrucción generada: {len(destruction_seq)} valores")
    
    # Corromper material de clave
    corrupted_key = engine.corrupt_key_material(test_key, attack_hash)
    print(f"✅ Clave corrompida: {corrupted_key[:20].hex()}...")
    
    # Verificar que la corrupción es irreversible
    original_hash = hashlib.sha256(test_key).hexdigest()
    corrupted_hash = hashlib.sha256(corrupted_key).hexdigest()
    
    print(f"🔍 Hash original: {original_hash}")
    print(f"🔍 Hash corrompido: {corrupted_hash}")
    print(f"🔍 ¿Son diferentes? {original_hash != corrupted_hash}")
    
    # Estadísticas de destrucción
    stats = engine.get_destruction_statistics()
    print(f"📊 Estadísticas: {stats}")
    
    print("✅ Prueba del motor de autodestrucción completada exitosamente!")


if __name__ == "__main__":
    test_chaotic_destruction()

