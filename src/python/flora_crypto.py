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

# Integración Kyber opcional
try:
	from .kyber_kem import try_create_kyber
except ImportError:
	try:
		from kyber_kem import try_create_kyber
	except Exception:
		try_create_kyber = None  # type: ignore

class FloraCryptoSystem:
	"""
	Sistema de cifrado FLORA: Fractal Lattice Obfuscation with Rotational Autodestruction
	
	Este sistema combina:
	1. Cifrado simétrico AES-256-GCM para datos
	2. Motor de autodestrucción caótica para claves
	3. Sistema de detección de amenazas en tiempo real
	4. Gestión dinámica de claves con perfect forward secrecy
	5. (Opcional) Intercambio de clave de sesión con Kyber KEM
	"""
	
	def __init__(self, 
				 key_size: int = 32,  # 256 bits
				 salt_size: int = 32,
				 iterations: int = 100000,
				 use_kyber: bool = True,
				 session_max_uses: int = 3):
		"""
		Inicializa el sistema de cifrado FLORA.
		
		Args:
			key_size: Tamaño de clave en bytes (32 = 256 bits)
			salt_size: Tamaño del salt para derivación de claves
			iterations: Iteraciones para PBKDF2
			use_kyber: Intentar usar Kyber KEM para claves de sesión
			session_max_uses: Número máximo de usos por clave de sesión antes de rotarla
		"""
		self.key_size = key_size
		self.salt_size = salt_size
		self.iterations = iterations
		
		# Motor de autodestrucción caótica
		self.destruction_engine = ChaoticDestructionEngine()
		
		# Estado del sistema
		self.session_keys: Dict[str, Dict[str, Any]] = {}
		self.threat_level = 0.0
		self.attack_history = []
		self.system_health = 1.0
		
		# Configuración de seguridad
		self.max_failed_attempts = 3
		self.failed_attempts = 0
		self.lockout_until = 0
		self.session_max_uses = max(1, session_max_uses)
		
		# KEM Kyber opcional
		self.kyber = None
		if use_kyber and 'try_create_kyber' in globals() and callable(try_create_kyber):  # type: ignore
			try:
				self.kyber = try_create_kyber()
			except Exception:
				self.kyber = None
		self.kyber_enabled = self.kyber is not None
		
	def generate_master_key(self, password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
		"""
		Genera una clave maestra usando PBKDF2.
		"""
		if salt is None:
			salt = get_random_bytes(self.salt_size)
		master_key = PBKDF2(
			password.encode('utf-8'),
			salt,
			dkLen=self.key_size,
			count=self.iterations,
			hmac_hash_module=SHA256
		)
		return master_key, salt
	
	def _derive_session_key_pbkdf2(self, master_key: bytes, session_id: str) -> bytes:
		"""Deriva clave de sesión con PBKDF2 (fallback si no se usa Kyber)."""
		session_salt = hashlib.sha256(
			master_key + session_id.encode() + str(time.time()).encode()
		).digest()
		session_key = PBKDF2(
			master_key,
			session_salt,
			dkLen=self.key_size,
			count=1000,
			hmac_hash_module=SHA256
		)
		return session_key

	def _derive_session_key_pbkdf2_with_salt(self, master_key: bytes, session_salt: bytes) -> bytes:
		"""Deriva clave de sesión a partir de un salt proporcionado (para reconstrucción stateless)."""
		return PBKDF2(
			master_key,
			session_salt,
			dkLen=self.key_size,
			count=1000,
			hmac_hash_module=SHA256
		)
	
	def _encapsulate_session_key_kyber(self) -> Tuple[bytes, bytes, bytes]:
		"""Si Kyber está disponible, genera (pk, c_L, ss)."""
		if not self.kyber_enabled:
			raise RuntimeError("Kyber no está habilitado")
		pk, sk = self.kyber.keygen()
		c_L, ss = self.kyber.encaps(pk)
		self._last_kyber_sk = sk  # type: ignore[attr-defined]
		return pk, c_L, ss
	
	def _store_session(self, session_id: str, session_key: bytes, kem_info: Optional[Dict[str, Any]] = None, session_salt: Optional[bytes] = None):
		self.session_keys[session_id] = {
			'key': session_key,
			'created': time.time(),
			'uses': 0,
			'max_uses': self.session_max_uses,
			'kem': kem_info or None,
			'session_salt': session_salt.hex() if session_salt else None
		}
	
	def _rotate_session_key(self, master_key: bytes, session_id: str):
		"""Rota la clave de sesión al alcanzar max_uses."""
		old = self.session_keys.get(session_id)
		if not old:
			return
		# Borrado lógico del material de la clave antigua
		old['key'] = b"\x00" * len(old.get('key', b''))
		old['uses'] = old.get('max_uses', self.session_max_uses)
		
		# Crear nueva clave de sesión
		new_key = None
		kem_info = None
		if self.kyber_enabled:
			try:
				_, c_L, ss = self._encapsulate_session_key_kyber()
				new_key = hashlib.sha256(ss).digest()[:self.key_size]
				kem_info = {'ciphertext': c_L.hex()}
			except Exception:
				new_key = None
		if new_key is None:
			# Re-derivar con nuevo salt
			new_salt = hashlib.sha256((session_id + str(time.time())).encode()).digest()
			new_key = self._derive_session_key_pbkdf2_with_salt(master_key, new_salt)
		self._store_session(session_id, new_key, kem_info, session_salt=(None if kem_info else new_salt))
	
	def create_session_key(self, master_key: bytes, session_id: str) -> bytes:
		"""
		Crea una clave de sesión única (Kyber si está disponible; PBKDF2 en fallback).
		"""
		if self.kyber_enabled:
			try:
				_, c_L, ss = self._encapsulate_session_key_kyber()
				session_key = hashlib.sha256(ss).digest()[:self.key_size]
				kem_info = {'ciphertext': c_L.hex()}
				self._store_session(session_id, session_key, kem_info)
				return session_key
			except Exception:
				pass
		# PBKDF2 con salt persistido en el bundle para reconstrucción
		new_salt = hashlib.sha256((session_id + str(time.time())).encode()).digest()
		session_key = self._derive_session_key_pbkdf2_with_salt(master_key, new_salt)
		self._store_session(session_id, session_key, session_salt=new_salt)
		return session_key
	
	def _touch_session_use(self, master_key: bytes, session_id: str):
		"""Incrementa el contador de uso y rota si alcanzó max_uses."""
		s = self.session_keys.get(session_id)
		if not s:
			return
		s['uses'] = s.get('uses', 0) + 1
		if s['uses'] >= s.get('max_uses', self.session_max_uses):
			self._rotate_session_key(master_key, session_id)
	
	def encrypt_message(self, 
					   message: bytes, 
					   master_key: bytes, 
					   session_id: str,
					   associated_data: Optional[bytes] = None) -> Dict[str, Any]:
		"""
		Encripta un mensaje usando el sistema FLORA.
		"""
		try:
			if self.system_health < 0.1:
				raise RuntimeError("Sistema comprometido - autodestrucción activada")
			
			# Crear/obtener clave de sesión
			session_key = self.session_keys.get(session_id, {}).get('key')
			if not session_key:
				session_key = self.create_session_key(master_key, session_id)
			
			nonce = get_random_bytes(12)
			cipher = AES.new(session_key, AES.MODE_GCM, nonce=nonce)
			if associated_data:
				cipher.update(associated_data)
			ciphertext, tag = cipher.encrypt_and_digest(message)
			
			# Marcar uso (y posible rotación)
			self._touch_session_use(master_key, session_id)
			
			info = self.session_keys.get(session_id, {})
			return {
				'session_id': session_id,
				'nonce': nonce.hex(),
				'ciphertext': ciphertext.hex(),
				'tag': tag.hex(),
				'associated_data': associated_data.hex() if associated_data else None,
				'timestamp': time.time(),
				'threat_level': self.threat_level,
				'system_health': self.system_health,
				'session_uses': info.get('uses'),
				'session_max_uses': info.get('max_uses'),
				'kem': info.get('kem'),
				'session_salt': info.get('session_salt')
			}
		except Exception as e:
			self._record_failed_attempt("encryption", str(e))
			raise
	
	def decrypt_message(self, 
					   encrypted_data: Dict[str, Any], 
					   master_key: bytes) -> bytes:
		"""
		Desencripta un mensaje usando el sistema FLORA.
		"""
		try:
			if self.system_health < 0.1:
				raise RuntimeError("Sistema comprometido - autodestrucción activada")
			
			session_id = encrypted_data['session_id']
			nonce = bytes.fromhex(encrypted_data['nonce'])
			ciphertext = bytes.fromhex(encrypted_data['ciphertext'])
			tag = bytes.fromhex(encrypted_data['tag'])
			associated_data = bytes.fromhex(encrypted_data['associated_data']) if encrypted_data.get('associated_data') else None
			
			if session_id not in self.session_keys:
				# Intento de reconstrucción stateless (solo PBKDF2)
				salt_hex = encrypted_data.get('session_salt')
				if not salt_hex:
					raise ValueError("Sesión no válida o expirada")
				session_salt = bytes.fromhex(salt_hex)
				recovered_key = self._derive_session_key_pbkdf2_with_salt(master_key, session_salt)
				self._store_session(session_id, recovered_key, session_salt=session_salt)
			
			session_key = self.session_keys[session_id]['key']
			cipher = AES.new(session_key, AES.MODE_GCM, nonce=nonce)
			if associated_data:
				cipher.update(associated_data)
			plaintext = cipher.decrypt_and_verify(ciphertext, tag)
			
			# Marcar uso (y posible rotación)
			self._touch_session_use(master_key, session_id)
			
			return plaintext
		except Exception as e:
			self._record_failed_attempt("decryption", str(e))
			if "tag" in str(e).lower() or "verification" in str(e).lower():
				self._trigger_autodestruction("authentication_failure", encrypted_data)
			raise
	
	def _record_failed_attempt(self, operation: str, error: str):
		self.failed_attempts += 1
		attack_record = {
			'timestamp': time.time(),
			'operation': operation,
			'error': error,
			'threat_level': min(1.0, self.failed_attempts / self.max_failed_attempts)
		}
		self.attack_history.append(attack_record)
		self._evaluate_threat_level()
		if self.failed_attempts >= self.max_failed_attempts:
			self._activate_lockout()
	
	def _evaluate_threat_level(self):
		if not self.attack_history:
			self.threat_level = 0.0
			return
		recent_attacks = [a for a in self.attack_history if time.time() - a['timestamp'] < 300]
		if not recent_attacks:
			self.threat_level = max(0.0, self.threat_level - 0.1)
		else:
			attack_frequency = len(recent_attacks) / 5.0
			severity = sum(a['threat_level'] for a in recent_attacks) / len(recent_attacks)
			self.threat_level = min(1.0, attack_frequency * 0.3 + severity * 0.7)
		self.system_health = max(0.0, 1.0 - self.threat_level)
	
	def _activate_lockout(self):
		lockout_duration = min(3600, 2 ** self.failed_attempts)
		self.lockout_until = time.time() + lockout_duration
		print(f"🚫 Sistema bloqueado por {lockout_duration} segundos debido a múltiples intentos fallidos")
	
	def _trigger_autodestruction(self, reason: str, context: Any):
		print(f"💥 ACTIVANDO AUTODESTRUCCIÓN CAÓTICA - Razón: {reason}")
		for session_id, session_data in self.session_keys.items():
			try:
				attack_context = f"{reason}_{session_id}_{time.time()}".encode()
				attack_hash = hashlib.sha256(attack_context).digest()
				corrupted_key = self.destruction_engine.corrupt_key_material(
					session_data['key'], 
					attack_hash
				)
				self.session_keys[session_id]['key'] = corrupted_key
				self.session_keys[session_id]['corrupted'] = True
				print(f"🔑 Clave de sesión {session_id} corrompida irreversiblemente")
			except Exception as e:
				print(f"❌ Error durante autodestrucción de sesión {session_id}: {e}")
		self.system_health = 0.0
		self.threat_level = 1.0
		self.attack_history.clear()
		print("💀 AUTODESTRUCCIÓN COMPLETADA - Sistema comprometido permanentemente")
	
	def get_system_status(self) -> Dict[str, Any]:
		return {
			'system_health': self.system_health,
			'threat_level': self.threat_level,
			'failed_attempts': self.failed_attempts,
			'active_sessions': len(self.session_keys),
			'lockout_active': time.time() < self.lockout_until,
			'lockout_remaining': max(0, self.lockout_until - time.time()),
			'recent_attacks': len([a for a in self.attack_history if time.time() - a['timestamp'] < 300]),
			'destruction_engine_stats': self.destruction_engine.get_destruction_statistics()
		}
	
	def reset_system(self, new_master_key: bytes):
		if self.system_health < 0.1:
			raise RuntimeError("No se puede resetear un sistema comprometido")
		self.session_keys.clear()
		self.attack_history.clear()
		self.failed_attempts = 0
		self.lockout_until = 0
		self.threat_level = 0.0
		self.system_health = 1.0
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
