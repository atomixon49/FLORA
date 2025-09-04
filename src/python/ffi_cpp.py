# 🌸 FLORA - Wrapper ctypes para C++ (flora_c)
# Carga flora_c.dll/.so y expone AES-GCM encrypt/decrypt

import os
import sys
import ctypes
from ctypes import c_uint8, c_size_t, c_int, POINTER
from typing import Tuple, Optional

# Ruta de la DLL/SO
# 1) Variable de entorno FLORA_CPP_DLL
# 2) build por defecto en Windows
# 3) LD_LIBRARY_PATH / PATH

def _default_library_path() -> str:
	cand = [
		os.environ.get("FLORA_CPP_DLL", ""),
		os.path.join(os.path.dirname(__file__), "..", "..", "cpp", "build", "Release", "flora_c.dll"),
		os.path.join(os.path.dirname(__file__), "..", "..", "cpp", "build", "flora_c.so"),
	]
	for p in cand:
		if p and os.path.exists(p):
			return os.path.abspath(p)
	return "flora_c.dll"  # confiar en PATH

_lib_path = _default_library_path()
_lib = ctypes.CDLL(_lib_path)

# firmas
_lib.flora_aes_gcm_encrypt.argtypes = [
	POINTER(c_uint8), c_size_t,
	POINTER(c_uint8), c_size_t,
	POINTER(c_uint8), c_size_t,
	POINTER(c_uint8), c_size_t,
	POINTER(c_uint8), POINTER(c_size_t),
	POINTER(c_uint8), c_size_t
]
_lib.flora_aes_gcm_encrypt.restype = c_int

_lib.flora_aes_gcm_decrypt.argtypes = [
	POINTER(c_uint8), c_size_t,
	POINTER(c_uint8), c_size_t,
	POINTER(c_uint8), c_size_t,
	POINTER(c_uint8), c_size_t,
	POINTER(c_uint8), c_size_t,
	POINTER(c_uint8), POINTER(c_size_t)
]
_lib.flora_aes_gcm_decrypt.restype = c_int


def _to_ptr(buf: Optional[bytes]):
	if not buf:
		return None
	arr = (c_uint8 * len(buf)).from_buffer_copy(buf)
	return ctypes.cast(arr, POINTER(c_uint8))


def aes_gcm_encrypt(key: bytes, nonce: bytes, plaintext: bytes, associated_data: bytes = b"") -> Tuple[bytes, bytes]:
	if len(nonce) != 12:
		raise ValueError("nonce debe ser 12 bytes")
	if len(key) not in (16, 24, 32):
		raise ValueError("key debe ser 16/24/32 bytes")
	ct_buf = (c_uint8 * (len(plaintext) + 16))()
	ct_len = c_size_t(len(plaintext) + 16)
	tag_buf = (c_uint8 * 16)()
	res = _lib.flora_aes_gcm_encrypt(
		_to_ptr(key), len(key),
		_to_ptr(nonce), len(nonce),
		_to_ptr(associated_data), len(associated_data),
		_to_ptr(plaintext), len(plaintext),
		ct_buf, ctypes.byref(ct_len),
		tag_buf, 16
	)
	if res != 0:
		raise RuntimeError(f"flora_aes_gcm_encrypt error={res}")
	ciphertext = bytes(ct_buf)[: ct_len.value]
	tag = bytes(tag_buf)
	return ciphertext, tag


def aes_gcm_decrypt(key: bytes, nonce: bytes, ciphertext: bytes, tag: bytes, associated_data: bytes = b"") -> bytes:
	if len(nonce) != 12:
		raise ValueError("nonce debe ser 12 bytes")
	if len(tag) != 16:
		raise ValueError("tag debe ser 16 bytes")
	pt_buf = (c_uint8 * (len(ciphertext)))()
	pt_len = c_size_t(len(ciphertext))
	res = _lib.flora_aes_gcm_decrypt(
		_to_ptr(key), len(key),
		_to_ptr(nonce), len(nonce),
		_to_ptr(associated_data), len(associated_data),
		_to_ptr(ciphertext), len(ciphertext),
		_to_ptr(tag), len(tag),
		pt_buf, ctypes.byref(pt_len)
	)
	if res != 0:
		raise RuntimeError(f"flora_aes_gcm_decrypt error={res}")
	return bytes(pt_buf)[: pt_len.value]


if __name__ == "__main__":
	k = b"\x11" * 32
	n = b"\x22" * 12
	ad = b"ABC"
	msg = "Hola FLORA desde C++ via ctypes".encode("utf-8")
	ct, tg = aes_gcm_encrypt(k, n, msg, ad)
	pt = aes_gcm_decrypt(k, n, ct, tg, ad)
	print(pt.decode("utf-8"))
