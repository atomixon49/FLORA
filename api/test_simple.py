"""
FLORA API - Test Simple
Script para probar la API simplificada
"""

import requests
import json
from datetime import datetime

# Configuración
API_BASE_URL = "http://localhost:8000"
API_KEY = "test_api_key_12345678901234567890"

def test_health_check():
    """Probar health check"""
    print("🔍 Probando health check...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_encryption():
    """Probar cifrado"""
    print("🔐 Probando cifrado...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "data": "Este es un mensaje secreto para cifrar"
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/encrypt",
        headers=headers,
        json=data
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Encrypted Data: {result.get('encrypted_data', 'N/A')}")
    print(f"Key ID: {result.get('key_id', 'N/A')}")
    print()
    
    return result.get('encrypted_data'), result.get('key_id')

def test_decryption(encrypted_data, key_id):
    """Probar desifrado"""
    print("🔓 Probando desifrado...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "encrypted_data": encrypted_data,
        "key_id": key_id
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/decrypt",
        headers=headers,
        json=data
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Decrypted Data: {result.get('decrypted_data', 'N/A')}")
    print()

def test_statistics():
    """Probar estadísticas"""
    print("📈 Probando estadísticas...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"{API_BASE_URL}/api/v1/stats",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total Operations: {result.get('total_operations', 0)}")
    print(f"Encrypt Operations: {result.get('encrypt_operations', 0)}")
    print(f"Decrypt Operations: {result.get('decrypt_operations', 0)}")
    print()

def test_audit_logs():
    """Probar logs de auditoría"""
    print("📊 Probando logs de auditoría...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"{API_BASE_URL}/api/v1/audit",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total Logs: {result.get('total', 0)}")
    for log in result.get('logs', [])[:3]:
        print(f"  - {log['action']} at {log['timestamp']}")
    print()

def main():
    """Función principal"""
    print("🌸 FLORA API Simple - Test Suite")
    print("=" * 50)
    print()
    
    try:
        # Probar endpoints básicos
        test_health_check()
        
        # Probar cifrado y desifrado
        encrypted_data, key_id = test_encryption()
        if encrypted_data and key_id:
            test_decryption(encrypted_data, key_id)
        
        # Probar estadísticas y auditoría
        test_statistics()
        test_audit_logs()
        
        print("✅ Todas las pruebas completadas exitosamente!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor API")
        print("Asegúrate de que el servidor esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error durante las pruebas: {str(e)}")

if __name__ == "__main__":
    main()

