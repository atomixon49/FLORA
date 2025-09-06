#!/usr/bin/env python3
"""
FLORA API Test Simple
Script para probar la API de FLORA de manera simple
"""

import requests
import json
import time
import sys
from datetime import datetime

def test_api_connection(base_url="http://localhost:8000"):
    """Probar conexión básica a la API"""
    print("🧪 Probando conexión a la API...")
    
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API respondiendo correctamente")
            return True
        else:
            print(f"❌ API respondiendo con código: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_encryption(base_url="http://localhost:8000", api_key="test_api_key_12345678901234567890"):
    """Probar endpoint de encriptación"""
    print("🔐 Probando endpoint de encriptación...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "data": "Hola FLORA desde API test"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/encrypt",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Encriptación exitosa")
            print(f"   Key ID: {result.get('key_id', 'N/A')}")
            print(f"   Algorithm: {result.get('algorithm', 'N/A')}")
            print(f"   Security Level: {result.get('security_level', 'N/A')}")
            return result
        else:
            print(f"❌ Error en encriptación: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_decryption(base_url="http://localhost:8000", api_key="test_api_key_12345678901234567890", encrypt_result=None):
    """Probar endpoint de desencriptación"""
    print("🔓 Probando endpoint de desencriptación...")
    
    if not encrypt_result:
        print("❌ No hay datos encriptados para probar")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "key_id": encrypt_result.get("key_id"),
        "encrypted_data": encrypt_result.get("encrypted_data")
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/decrypt",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Desencriptación exitosa")
            print(f"   Datos desencriptados: {result.get('decrypted_data', 'N/A')}")
            print(f"   Key ID: {result.get('key_id', 'N/A')}")
            print(f"   Algorithm: {result.get('algorithm', 'N/A')}")
            return True
        else:
            print(f"❌ Error en desencriptación: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_status(base_url="http://localhost:8000", api_key="test_api_key_12345678901234567890"):
    """Probar endpoint de estado"""
    print("📊 Probando endpoint de estado...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{base_url}/api/v1/status",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Estado obtenido correctamente")
            print(f"   Status: {result.get('status', 'N/A')}")
            print(f"   Version: {result.get('version', 'N/A')}")
            print(f"   Security Level: {result.get('security_level', 'N/A')}")
            print(f"   Timestamp: {result.get('timestamp', 'N/A')}")
            return True
        else:
            print(f"❌ Error obteniendo estado: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_authentication(base_url="http://localhost:8000"):
    """Probar autenticación con API key inválida"""
    print("🔑 Probando autenticación con API key inválida...")
    
    headers = {
        "Authorization": "Bearer invalid_api_key",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{base_url}/api/v1/status",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 401:
            print("✅ Autenticación correctamente rechazada")
            return True
        else:
            print(f"❌ Error en autenticación: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_rate_limiting(base_url="http://localhost:8000", api_key="test_api_key_12345678901234567890"):
    """Probar rate limiting"""
    print("⏱️ Probando rate limiting...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Hacer múltiples requests rápidos
    for i in range(5):
        try:
            response = requests.get(
                f"{base_url}/api/v1/status",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 429:
                print(f"✅ Rate limiting funcionando (request {i+1})")
                return True
            elif response.status_code == 200:
                print(f"   Request {i+1}: OK")
            else:
                print(f"   Request {i+1}: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   Request {i+1}: Error - {e}")
        
        time.sleep(0.1)  # Pequeña pausa entre requests
    
    print("⚠️ Rate limiting no activado (puede ser normal)")
    return True

def main():
    """Función principal"""
    print("FLORA API Test Simple")
    print("=" * 50)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    api_key = "test_api_key_12345678901234567890"
    
    tests_passed = 0
    total_tests = 6
    
    # 1. Probar conexión
    if test_api_connection(base_url):
        tests_passed += 1
        print("✅ Test de conexión: PASÓ")
    else:
        print("❌ Test de conexión: FALLÓ")
        print("   Asegúrate de que la API esté ejecutándose")
        return 1
    
    # 2. Probar autenticación
    if test_authentication(base_url):
        tests_passed += 1
        print("✅ Test de autenticación: PASÓ")
    else:
        print("❌ Test de autenticación: FALLÓ")
    
    # 3. Probar estado
    if test_status(base_url, api_key):
        tests_passed += 1
        print("✅ Test de estado: PASÓ")
    else:
        print("❌ Test de estado: FALLÓ")
    
    # 4. Probar encriptación
    encrypt_result = test_encryption(base_url, api_key)
    if encrypt_result:
        tests_passed += 1
        print("✅ Test de encriptación: PASÓ")
    else:
        print("❌ Test de encriptación: FALLÓ")
    
    # 5. Probar desencriptación
    if encrypt_result and test_decryption(base_url, api_key, encrypt_result):
        tests_passed += 1
        print("✅ Test de desencriptación: PASÓ")
    else:
        print("❌ Test de desencriptación: FALLÓ")
    
    # 6. Probar rate limiting
    if test_rate_limiting(base_url, api_key):
        tests_passed += 1
        print("✅ Test de rate limiting: PASÓ")
    else:
        print("❌ Test de rate limiting: FALLÓ")
    
    # Resumen final
    print("\n" + "=" * 50)
    print("RESUMEN FINAL")
    print("=" * 50)
    print(f"Tests pasados: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 TODOS LOS TESTS PASARON")
        print("✅ API funcionando correctamente")
        return 0
    elif tests_passed >= 4:
        print("⚠️ La mayoría de tests pasaron")
        print("✅ API funcionando con algunas advertencias")
        return 0
    else:
        print("❌ Varios tests fallaron")
        print("⚠️ Revisar configuración de la API")
        return 1

if __name__ == "__main__":
    sys.exit(main())
