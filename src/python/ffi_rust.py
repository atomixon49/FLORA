"""
Wrapper Python para el módulo Rust flora_rs
"""
import flora_rs
from typing import Tuple, Union

def rust_encrypt(key: bytes, plaintext: bytes, associated_data: bytes = b'') -> Tuple[bytes, bytes]:
    """
    Encripta datos usando el backend Rust
    
    Args:
        key: Clave de 32 bytes
        plaintext: Datos a encriptar
        associated_data: Datos asociados (opcional)
    
    Returns:
        Tuple[bytes, bytes]: (nonce, ciphertext)
    """
    if len(key) != 32:
        raise ValueError("La clave debe tener exactamente 32 bytes")
    
    nonce, ciphertext = flora_rs.py_encrypt(key, plaintext, associated_data)
    
    # Convertir listas a bytes si es necesario
    if isinstance(nonce, list):
        nonce = bytes(nonce)
    if isinstance(ciphertext, list):
        ciphertext = bytes(ciphertext)
    
    return nonce, ciphertext

def rust_decrypt(key: bytes, nonce: bytes, ciphertext: bytes, associated_data: bytes = b'') -> bytes:
    """
    Desencripta datos usando el backend Rust
    
    Args:
        key: Clave de 32 bytes
        nonce: Nonce usado en la encriptación
        ciphertext: Datos encriptados
        associated_data: Datos asociados (opcional)
    
    Returns:
        bytes: Datos desencriptados
    """
    if len(key) != 32:
        raise ValueError("La clave debe tener exactamente 32 bytes")
    
    plaintext = flora_rs.py_decrypt(key, nonce, ciphertext, associated_data)
    
    # Convertir lista a bytes si es necesario
    if isinstance(plaintext, list):
        plaintext = bytes(plaintext)
    
    return plaintext

def test_rust_backend():
    """Prueba el backend Rust"""
    print("🧪 Probando backend Rust...")
    
    key = b'key12345678901234567890123456789012'[:32]  # 32 bytes
    plaintext = b'Hola FLORA desde Rust'
    associated_data = b'AD'
    
    print(f"Clave: {key.hex()}")
    print(f"Texto: {plaintext}")
    print(f"AD: {associated_data}")
    
    # Encriptar
    nonce, ciphertext = rust_encrypt(key, plaintext, associated_data)
    print(f"Nonce: {nonce.hex()}")
    print(f"Ciphertext: {ciphertext.hex()}")
    
    # Desencriptar
    decrypted = rust_decrypt(key, nonce, ciphertext, associated_data)
    print(f"Desencriptado: {decrypted}")
    
    # Verificar
    if decrypted == plaintext:
        print("✅ Backend Rust funciona correctamente")
        return True
    else:
        print("❌ Error en el backend Rust")
        return False

if __name__ == "__main__":
    test_rust_backend()
