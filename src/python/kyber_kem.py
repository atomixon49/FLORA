# 🌸 FLORA - Kyber KEM (Integración Opcional)
# Encapsulamiento/decapsulamiento de claves usando CRYSTALS-Kyber si está disponible.

from typing import Optional, Tuple

class KyberNotAvailable(Exception):
	"""Excepción cuando Kyber no está disponible en el entorno."""
	pass


def _import_kyber_impl():
	"""Intenta importar una implementación de Kyber disponible en Python.
	Devuelve (modulo, variant) o (None, None) si no hay implementación.
	"""
	# Intento 1: pykyber (hipotético)
	try:
		import pykyber as kyb  # type: ignore
		return kyb, "pykyber"
	except Exception:
		pass

	# Intento 2: pqcrypto (algunas distros exponen pqcrypto.kem.kyber*
	try:
		from pqcrypto.kem import kyber512 as kyb  # type: ignore
		return kyb, "pqcrypto-kyber512"
	except Exception:
		pass

	# Sin implementación
	return None, None


class KyberKEM:
	"""Wrapper simple para KEM Kyber con detección dinámica.

	Uso:
		kem = KyberKEM()
		if kem.available:
			pk, sk = kem.keygen()
			c, ss = kem.encaps(pk)
			ss2 = kem.decaps(sk, c)
	"""

	def __init__(self, prefer_variant: str = "kyber512") -> None:
		self.prefer_variant = prefer_variant
		self.impl, self.variant = _import_kyber_impl()
		self.available = self.impl is not None

	def keygen(self) -> Tuple[bytes, bytes]:
		if not self.available:
			raise KyberNotAvailable("Kyber no disponible en este entorno")
		# pqcrypto y similares devuelven (pk, sk)
		try:
			pk, sk = self.impl.generate_keypair()  # type: ignore[attr-defined]
		except Exception:
			# Fallback a API estilo pqcrypto
			kp = self.impl.generate_keypair  # type: ignore[attr-defined]
			res = kp()
			pk, sk = res.public_key, res.secret_key  # type: ignore[attr-defined]
		return bytes(pk), bytes(sk)

	def encaps(self, public_key: bytes) -> Tuple[bytes, bytes]:
		if not self.available:
			raise KyberNotAvailable("Kyber no disponible en este entorno")
		try:
			ciphertext, shared_secret = self.impl.encrypt(public_key)  # type: ignore[attr-defined]
		except Exception:
			# API estilo pqcrypto
			enc = self.impl.encrypt  # type: ignore[attr-defined]
			res = enc(public_key)
			ciphertext, shared_secret = res.ciphertext, res.shared_key  # type: ignore[attr-defined]
		return bytes(ciphertext), bytes(shared_secret)

	def decaps(self, secret_key: bytes, ciphertext: bytes) -> bytes:
		if not self.available:
			raise KyberNotAvailable("Kyber no disponible en este entorno")
		try:
			shared_secret = self.impl.decrypt(secret_key, ciphertext)  # type: ignore[attr-defined]
		except Exception:
			# API estilo pqcrypto
			dec = self.impl.decrypt  # type: ignore[attr-defined]
			res = dec(ciphertext, secret_key)
			shared_secret = res  # type: ignore[assignment]
		return bytes(shared_secret)


def try_create_kyber() -> Optional[KyberKEM]:
	"""Crea instancia si hay backend disponible; de lo contrario, None."""
	kem = KyberKEM()
	return kem if kem.available else None



