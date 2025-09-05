"""
FLORA API - Test Script
Script para probar las APIs de FLORA
"""

import requests
import json
import time
from datetime import datetime

# Configuración
API_BASE_URL = "http://localhost:8000"
API_KEY = "test_api_key_12345678901234567890"

def test_health_check():
    """Probar endpoint de salud"""
    print("🔍 Probando health check...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_encryption():
    """Probar cifrado de datos"""
    print("🔐 Probando cifrado...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "data": "Este es un mensaje secreto para cifrar",
        "algorithm": "hybrid_post_quantum",
        "metadata": {
            "source": "test_script",
            "timestamp": datetime.now().isoformat()
        }
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
    """Probar desifrado de datos"""
    print("🔓 Probando desifrado...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "encrypted_data": encrypted_data,
        "key_id": key_id,
        "metadata": {
            "source": "test_script",
            "timestamp": datetime.now().isoformat()
        }
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

def test_create_api_key():
    """Probar creación de API key"""
    print("🔑 Probando creación de API key...")
    
    data = {
        "name": "API Key de Prueba",
        "permissions": ["encrypt", "decrypt", "read"],
        "expires_in_days": 30
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/keys",
        json=data
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"New API Key: {result.get('api_key', 'N/A')}")
    print(f"Key ID: {result.get('key_id', 'N/A')}")
    print()

def test_list_api_keys():
    """Probar listado de API keys"""
    print("📋 Probando listado de API keys...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"{API_BASE_URL}/api/v1/keys",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"API Keys: {len(result.get('api_keys', []))}")
    for key in result.get('api_keys', []):
        print(f"  - {key['name']} ({key['key_id']})")
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
    for log in result.get('logs', [])[:3]:  # Mostrar solo los primeros 3
        print(f"  - {log['action']} at {log['timestamp']}")
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

def test_webhook():
    """Probar creación de webhook"""
    print("🔗 Probando creación de webhook...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "url": "https://webhook.site/your-webhook-url",
        "events": ["encrypt", "decrypt", "error"]
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/webhooks",
        headers=headers,
        json=data
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Webhook ID: {result.get('webhook_id', 'N/A')}")
    print(f"URL: {result.get('url', 'N/A')}")
    print()

def main():
    """Función principal de pruebas"""
    print("🌸 FLORA API - Test Suite")
    print("=" * 50)
    print()
    
    try:
        # Probar endpoints básicos
        test_health_check()
        
        # Probar cifrado y desifrado
        encrypted_data, key_id = test_encryption()
        if encrypted_data and key_id:
            test_decryption(encrypted_data, key_id)
        
        # Probar gestión de API keys
        test_create_api_key()
        test_list_api_keys()
        
        # Probar auditoría y estadísticas
        test_audit_logs()
        test_statistics()
        
        # Probar webhooks
        test_webhook()
        
        print("✅ Todas las pruebas completadas exitosamente!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor API")
        print("Asegúrate de que el servidor esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error durante las pruebas: {str(e)}")

if __name__ == "__main__":
    main()

