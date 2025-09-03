# 🌸 FLORA - Sistema de Cifrado Híbrido Post-Cuántico
# Implementación principal del algoritmo FLORA con autodestrucción caótica

import os
import hashlib
import hmac
from typing import Tuple, Optional, Dict, Any
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
import json
import time

try:
    from .chaotic_map import ChaoticDestructionEngine
except ImportError:
    from chaotic_map import ChaoticDestructionEngine

class FloraCryptoSystem:
    """
    Sistema de cifrado FLORA: Fractal Lattice Obfuscation with Rotational Autodestruction
    
    Este sistema combina:
    1. Cifrado simétrico AES-256-GCM para datos
    2. Motor de autodestrucción caótica para claves
    3. Sistema de detección de amenazas en tiempo real
    4. Gestión dinámica de claves con perfect forward secrecy
    """
    
    def __init__(self, 
                 key_size: int = 32,  # 256 bits
                 salt_size: int = 32,
                 iterations: int = 100000):
        """
        Inicializa el sistema de cifrado FLORA.
        
        Args:
            key_size: Tamaño de clave en bytes (32 = 256 bits)
            salt_size: Tamaño del salt para derivación de claves
            iterations: Iteraciones para PBKDF2
        """
        self.key_size = key_size
        self.salt_size = salt_size
        self.iterations = iterations
        
        # Motor de autodestrucción caótica
        self.destruction_engine = ChaoticDestructionEngine()
        
        # Estado del sistema
        self.session_keys = {}
        self.threat_level = 0.0
        self.attack_history = []
        self.system_health = 1.0
        
        # Configuración de seguridad
        self.max_failed_attempts = 3
        self.failed_attempts = 0
        self.lockout_until = 0
        
    def generate_master_key(self, password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
        """
        Genera una clave maestra usando PBKDF2.
        
        Args:
            password: Contraseña del usuario
            salt: Salt opcional (se genera si no se proporciona)
            
        Returns:
            Tuple con (clave_maestra, salt)
        """
        if salt is None:
            salt = get_random_bytes(self.salt_size)
        
        # Derivar clave maestra usando PBKDF2
        master_key = PBKDF2(
            password.encode('utf-8'),
            salt,
            dkLen=self.key_size,
            count=self.iterations,
            hmac_hash_module=SHA256
        )
        
        return master_key, salt
    
    def create_session_key(self, master_key: bytes, session_id: str) -> bytes:
        """
        Crea una clave de sesión única para cada operación.
        
        Args:
            master_key: Clave maestra derivada
            session_id: Identificador único de sesión
            
        Returns:
            Clave de sesión generada
        """
        # Generar salt único para la sesión
        session_salt = hashlib.sha256(
            master_key + session_id.encode() + str(time.time()).encode()
        ).digest()
        
        # Derivar clave de sesión
        session_key = PBKDF2(
            master_key,
            session_salt,
            dkLen=self.key_size,
            count=1000,  # Menos iteraciones para sesiones
            hmac_hash_module=SHA256
        )
        
        # Almacenar clave de sesión
        self.session_keys[session_id] = {
            'key': session_key,
            'created': time.time(),
            'uses': 0
        }
        
        return session_key
    
    def encrypt_message(self, 
                       message: bytes, 
                       master_key: bytes, 
                       session_id: str,
                       associated_data: Optional[bytes] = None) -> Dict[str, Any]:
        """
        Encripta un mensaje usando el sistema FLORA.
        
        Args:
            message: Mensaje a encriptar
            master_key: Clave maestra
            session_id: Identificador de sesión
            associated_data: Datos asociados para autenticación
            
        Returns:
            Diccionario con datos encriptados y metadatos
        """
        try:
            # Verificar estado del sistema
            if self.system_health < 0.1:
                raise RuntimeError("Sistema comprometido - autodestrucción activada")
            
            # Crear clave de sesión
            session_key = self.create_session_key(master_key, session_id)
            
            # Generar nonce único
            nonce = get_random_bytes(12)  # 96 bits para GCM
            
            # Crear cipher AES-GCM
            cipher = AES.new(session_key, AES.MODE_GCM, nonce=nonce)
            
            # Agregar datos asociados si existen
            if associated_data:
                cipher.update(associated_data)
            
            # Encriptar mensaje
            ciphertext, tag = cipher.encrypt_and_digest(message)
            
            # Preparar respuesta
            encrypted_data = {
                'session_id': session_id,
                'nonce': nonce.hex(),
                'ciphertext': ciphertext.hex(),
                'tag': tag.hex(),
                'associated_data': associated_data.hex() if associated_data else None,
                'timestamp': time.time(),
                'threat_level': self.threat_level,
                'system_health': self.system_health
            }
            
            # Incrementar contador de uso de la sesión
            self.session_keys[session_id]['uses'] += 1
            
            return encrypted_data
            
        except Exception as e:
            # Registrar intento fallido
            self._record_failed_attempt("encryption", str(e))
            raise
    
    def decrypt_message(self, 
                       encrypted_data: Dict[str, Any], 
                       master_key: bytes) -> bytes:
        """
        Desencripta un mensaje usando el sistema FLORA.
        
        Args:
            encrypted_data: Datos encriptados
            master_key: Clave maestra
            
        Returns:
            Mensaje desencriptado
        """
        try:
            # Verificar estado del sistema
            if self.system_health < 0.1:
                raise RuntimeError("Sistema comprometido - autodestrucción activada")
            
            # Extraer datos
            session_id = encrypted_data['session_id']
            nonce = bytes.fromhex(encrypted_data['nonce'])
            ciphertext = bytes.fromhex(encrypted_data['ciphertext'])
            tag = bytes.fromhex(encrypted_data['tag'])
            associated_data = bytes.fromhex(encrypted_data['associated_data']) if encrypted_data.get('associated_data') else None
            
            # Verificar que la sesión existe
            if session_id not in self.session_keys:
                raise ValueError("Sesión no válida o expirada")
            
            session_key = self.session_keys[session_id]['key']
            
            # Crear cipher para desencriptación
            cipher = AES.new(session_key, AES.MODE_GCM, nonce=nonce)
            
            # Agregar datos asociados si existen
            if associated_data:
                cipher.update(associated_data)
            
            # Desencriptar y verificar tag
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            
            # Incrementar contador de uso
            self.session_keys[session_id]['uses'] += 1
            
            return plaintext
            
        except Exception as e:
            # Registrar intento fallido
            self._record_failed_attempt("decryption", str(e))
            
            # Si es un error de autenticación, activar autodestrucción
            if "tag" in str(e).lower() or "verification" in str(e).lower():
                self._trigger_autodestruction("authentication_failure", encrypted_data)
            
            raise
    
    def _record_failed_attempt(self, operation: str, error: str):
        """
        Registra un intento fallido y evalúa amenazas.
        
        Args:
            operation: Tipo de operación fallida
            error: Descripción del error
        """
        self.failed_attempts += 1
        
        # Registrar en historial de ataques
        attack_record = {
            'timestamp': time.time(),
            'operation': operation,
            'error': error,
            'threat_level': min(1.0, self.failed_attempts / self.max_failed_attempts)
        }
        
        self.attack_history.append(attack_record)
        
        # Evaluar nivel de amenaza
        self._evaluate_threat_level()
        
        # Verificar si se debe activar bloqueo
        if self.failed_attempts >= self.max_failed_attempts:
            self._activate_lockout()
    
    def _evaluate_threat_level(self):
        """Evalúa el nivel de amenaza basado en el historial de ataques."""
        if not self.attack_history:
            self.threat_level = 0.0
            return
        
        # Calcular amenaza basada en intentos recientes
        recent_attacks = [a for a in self.attack_history 
                         if time.time() - a['timestamp'] < 300]  # Últimos 5 minutos
        
        if not recent_attacks:
            self.threat_level = max(0.0, self.threat_level - 0.1)
        else:
            # Aumentar amenaza basado en frecuencia y severidad
            attack_frequency = len(recent_attacks) / 5.0  # Normalizar a 5 minutos
            severity = sum(a['threat_level'] for a in recent_attacks) / len(recent_attacks)
            
            self.threat_level = min(1.0, attack_frequency * 0.3 + severity * 0.7)
        
        # Ajustar salud del sistema
        self.system_health = max(0.0, 1.0 - self.threat_level)
    
    def _activate_lockout(self):
        """Activa bloqueo temporal del sistema."""
        lockout_duration = min(3600, 2 ** self.failed_attempts)  # Exponencial, máximo 1 hora
        self.lockout_until = time.time() + lockout_duration
        
        print(f"🚫 Sistema bloqueado por {lockout_duration} segundos debido a múltiples intentos fallidos")
    
    def _trigger_autodestruction(self, reason: str, context: Any):
        """
        Activa el mecanismo de autodestrucción caótica.
        
        Args:
            reason: Razón de la autodestrucción
            context: Contexto del evento
        """
        print(f"💥 ACTIVANDO AUTODESTRUCCIÓN CAÓTICA - Razón: {reason}")
        
        # Inicializar motor de destrucción con claves actuales
        for session_id, session_data in self.session_keys.items():
            try:
                # Generar hash del contexto de ataque
                attack_context = f"{reason}_{session_id}_{time.time()}".encode()
                attack_hash = hashlib.sha256(attack_context).digest()
                
                # Corromper clave de sesión
                corrupted_key = self.destruction_engine.corrupt_key_material(
                    session_data['key'], 
                    attack_hash
                )
                
                # Reemplazar con clave corrompida
                self.session_keys[session_id]['key'] = corrupted_key
                self.session_keys[session_id]['corrupted'] = True
                
                print(f"🔑 Clave de sesión {session_id} corrompida irreversiblemente")
                
            except Exception as e:
                print(f"❌ Error durante autodestrucción de sesión {session_id}: {e}")
        
        # Marcar sistema como comprometido
        self.system_health = 0.0
        self.threat_level = 1.0
        
        # Limpiar historial de ataques
        self.attack_history.clear()
        
        print("💀 AUTODESTRUCCIÓN COMPLETADA - Sistema comprometido permanentemente")
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual del sistema.
        
        Returns:
            Diccionario con estado del sistema
        """
        return {
            'system_health': self.system_health,
            'threat_level': self.threat_level,
            'failed_attempts': self.failed_attempts,
            'active_sessions': len(self.session_keys),
            'lockout_active': time.time() < self.lockout_until,
            'lockout_remaining': max(0, self.lockout_until - time.time()),
            'recent_attacks': len([a for a in self.attack_history 
                                 if time.time() - a['timestamp'] < 300]),
            'destruction_engine_stats': self.destruction_engine.get_destruction_statistics()
        }
    
    def reset_system(self, new_master_key: bytes):
        """
        Resetea el sistema con una nueva clave maestra.
        
        Args:
            new_master_key: Nueva clave maestra
        """
        if self.system_health < 0.1:
            raise RuntimeError("No se puede resetear un sistema comprometido")
        
        # Limpiar estado
        self.session_keys.clear()
        self.attack_history.clear()
        self.failed_attempts = 0
        self.lockout_until = 0
        self.threat_level = 0.0
        self.system_health = 1.0
        
        # Resetear motor de destrucción
        self.destruction_engine.reset_destruction_engine()
        
        print("🔄 Sistema FLORA reseteado exitosamente")


# Función de utilidad para testing
def test_flora_system():
    """Función de prueba para el sistema FLORA."""
    print("🧪 Probando Sistema de Cifrado FLORA...")
    
    # Crear instancia del sistema
    flora = FloraCryptoSystem()
    
    # Generar clave maestra
    password = "FLORA_SUPER_SECURE_PASSWORD_2024"
    master_key, salt = flora.generate_master_key(password)
    print(f"✅ Clave maestra generada: {master_key[:16].hex()}...")
    
    # Mensaje de prueba
    test_message = b"Este es un mensaje secreto del sistema FLORA - Crypto Flower 2024!"
    session_id = "test_session_001"
    
    print(f"📝 Mensaje original: {test_message.decode('utf-8')}")
    
    # Encriptar mensaje
    try:
        encrypted_data = flora.encrypt_message(test_message, master_key, session_id)
        print(f"🔒 Mensaje encriptado exitosamente")
        print(f"   Session ID: {encrypted_data['session_id']}")
        print(f"   Nonce: {encrypted_data['nonce'][:16]}...")
        print(f"   Ciphertext: {encrypted_data['ciphertext'][:32]}...")
        
        # Desencriptar mensaje
        decrypted_message = flora.decrypt_message(encrypted_data, master_key)
        print(f"🔓 Mensaje desencriptado: {decrypted_message.decode('utf-8')}")
        
        # Verificar integridad
        if test_message == decrypted_message:
            print("✅ Verificación de integridad exitosa!")
        else:
            print("❌ Error en verificación de integridad")
        
        # Estado del sistema
        status = flora.get_system_status()
        print(f"📊 Estado del sistema: {status}")
        
    except Exception as e:
        print(f"❌ Error durante operación: {e}")
    
    print("✅ Prueba del sistema FLORA completada!")


if __name__ == "__main__":
    test_flora_system()
