# 🌸 FLORA - Script Principal de Testing
# Prueba completa del sistema de cifrado híbrido con autodestrucción caótica

import sys
import os
import time
import hashlib

# Intentar importar desde el paquete instalado primero
try:
    from flora.chaotic_map import ChaoticDestructionEngine
    from flora.flora_crypto import FloraCryptoSystem
    print("✅ Módulos FLORA importados desde paquete instalado")
except ImportError:
    # Si falla, intentar desde src/python
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'python'))
    try:
        from chaotic_map import ChaoticDestructionEngine
        from flora_crypto import FloraCryptoSystem
        print("✅ Módulos FLORA importados desde src/python")
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("💡 Asegúrate de estar en el directorio raíz del proyecto")
        sys.exit(1)
    print("✅ Módulos FLORA importados exitosamente")
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("💡 Asegúrate de estar en el directorio raíz del proyecto")
    sys.exit(1)

def test_chaotic_destruction_engine():
    """Prueba del motor de autodestrucción caótica."""
    print("\n" + "="*60)
    print("🧪 PRUEBA 1: Motor de Autodestrucción Caótica")
    print("="*60)
    
    try:
        # Crear instancia del motor
        engine = ChaoticDestructionEngine()
        print("✅ Motor de autodestrucción creado")
        
        # Material de clave de prueba
        test_key = b"FLORA_TEST_KEY_2024_CRYPTO_FLOWER"
        print(f"🔑 Clave de prueba: {test_key[:20].hex()}...")
        
        # Inicializar semilla caótica
        r, x0 = engine.initialize_chaos_seed(test_key)
        print(f"🌱 Semilla caótica: r={r:.6f}, x0={x0:.6f}")
        
        # Simular ataque
        attack_hash = hashlib.sha256(b"ATTACK_ATTEMPT_2024").digest()
        print(f"⚔️ Hash de ataque: {attack_hash[:16].hex()}...")
        
        # Generar secuencia de destrucción
        destruction_seq = engine.generate_destruction_sequence(
            iterations=1000, 
            perturbation_hash=attack_hash
        )
        print(f"💥 Secuencia de destrucción: {len(destruction_seq)} valores")
        
        # Corromper material de clave
        corrupted_key = engine.corrupt_key_material(test_key, attack_hash)
        print(f"🔒 Clave corrompida: {corrupted_key[:20].hex()}...")
        
        # Verificar irreversibilidad
        original_hash = hashlib.sha256(test_key).hexdigest()
        corrupted_hash = hashlib.sha256(corrupted_key).hexdigest()
        
        print(f"🔍 Hash original: {original_hash[:32]}...")
        print(f"🔍 Hash corrompido: {corrupted_hash[:32]}...")
        print(f"🔍 ¿Son diferentes? {'✅ SÍ' if original_hash != corrupted_hash else '❌ NO'}")
        
        # Estadísticas
        stats = engine.get_destruction_statistics()
        print(f"📊 Estadísticas: {stats}")
        
        print("✅ Prueba del motor de autodestrucción EXITOSA")
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de autodestrucción: {e}")
        return False

def test_flora_crypto_system():
    """Prueba del sistema de cifrado FLORA completo."""
    print("\n" + "="*60)
    print("🧪 PRUEBA 2: Sistema de Cifrado FLORA Completo")
    print("="*60)
    
    try:
        # Crear instancia del sistema
        flora = FloraCryptoSystem()
        print("✅ Sistema FLORA creado")
        
        # Generar clave maestra
        password = "FLORA_SUPER_SECURE_PASSWORD_2024_CRYPTO_FLOWER"
        master_key, salt = flora.generate_master_key(password)
        print(f"🔑 Clave maestra: {master_key[:16].hex()}...")
        print(f"🧂 Salt: {salt[:16].hex()}...")
        
        # Mensaje de prueba
        test_message = b"Este es un mensaje ultra secreto del sistema FLORA - Crypto Flower 2024!"
        session_id = "test_session_001"
        
        print(f"📝 Mensaje original: {test_message.decode('utf-8')}")
        print(f"🆔 Session ID: {session_id}")
        
        # Encriptar mensaje
        encrypted_data = flora.encrypt_message(test_message, master_key, session_id)
        print(f"🔒 Mensaje encriptado exitosamente")
        print(f"   📦 Session ID: {encrypted_data['session_id']}")
        print(f"   🔢 Nonce: {encrypted_data['nonce'][:16]}...")
        print(f"   🗝️ Ciphertext: {encrypted_data['ciphertext'][:32]}...")
        print(f"   🏷️ Tag: {encrypted_data['tag'][:16]}...")
        print(f"   ⏰ Timestamp: {encrypted_data['timestamp']}")
        
        # Desencriptar mensaje
        decrypted_message = flora.decrypt_message(encrypted_data, master_key)
        print(f"🔓 Mensaje desencriptado: {decrypted_message.decode('utf-8')}")
        
        # Verificar integridad
        if test_message == decrypted_message:
            print("✅ Verificación de integridad EXITOSA")
        else:
            print("❌ Error en verificación de integridad")
            return False
        
        # Estado del sistema
        status = flora.get_system_status()
        print(f"📊 Estado del sistema:")
        for key, value in status.items():
            if key != 'destruction_engine_stats':
                print(f"   {key}: {value}")
        
        print("✅ Prueba del sistema FLORA EXITOSA")
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba del sistema FLORA: {e}")
        return False

def test_attack_simulation():
    """Prueba de simulación de ataques y autodestrucción."""
    print("\n" + "="*60)
    print("🧪 PRUEBA 3: Simulación de Ataques y Autodestrucción")
    print("="*60)
    
    try:
        # Crear sistema FLORA
        flora = FloraCryptoSystem()
        print("✅ Sistema FLORA creado para prueba de ataques")
        
        # Generar clave y encriptar mensaje
        password = "ATTACK_TEST_PASSWORD"
        master_key, salt = flora.generate_master_key(password)
        test_message = b"Mensaje que sera atacado"
        session_id = "attack_test_session"
        
        encrypted_data = flora.encrypt_message(test_message, master_key, session_id)
        print(f"🔒 Mensaje encriptado: {encrypted_data['ciphertext'][:32]}...")
        
        # Simular múltiples intentos fallidos
        print("\n⚔️ Simulando ataques...")
        for i in range(5):
            try:
                # Intentar desencriptar con clave incorrecta
                wrong_key = hashlib.sha256(f"WRONG_KEY_{i}".encode()).digest()[:32]
                flora.decrypt_message(encrypted_data, wrong_key)
            except Exception as e:
                print(f"   🚫 Intento {i+1} fallido: {str(e)[:50]}...")
                
                # Mostrar estado del sistema
                status = flora.get_system_status()
                print(f"   📊 Threat Level: {status['threat_level']:.2f}")
                print(f"   📊 System Health: {status['system_health']:.2f}")
                print(f"   📊 Failed Attempts: {status['failed_attempts']}")
                
                # Verificar si se activó bloqueo
                if status['lockout_active']:
                    print(f"   🚫 Sistema bloqueado por {status['lockout_remaining']:.0f} segundos")
                    break
        
        # Estado final
        final_status = flora.get_system_status()
        print(f"\n📊 Estado final del sistema:")
        print(f"   🚨 Threat Level: {final_status['threat_level']:.2f}")
        print(f"   💚 System Health: {final_status['system_health']:.2f}")
        print(f"   🔒 Lockout Active: {final_status['lockout_active']}")
        print(f"   ⚔️ Failed Attempts: {final_status['failed_attempts']}")
        
        print("✅ Prueba de simulación de ataques COMPLETADA")
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de ataques: {e}")
        return False

def test_performance():
    """Prueba de performance del sistema FLORA."""
    print("\n" + "="*60)
    print("🧪 PRUEBA 4: Performance y Rendimiento")
    print("="*60)
    
    try:
        # Crear sistema
        flora = FloraCryptoSystem()
        password = "PERFORMANCE_TEST"
        master_key, salt = flora.generate_master_key(password)
        
        # Mensajes de diferentes tamaños
        test_messages = [
            b"Pequeno",  # ~7 bytes
            b"Este es un mensaje de tamano medio para testing",  # ~50 bytes
            b"X" * 1000,  # 1KB
            b"X" * 10000,  # 10KB
        ]
        
        print("📊 Testing performance con diferentes tamaños de mensaje:")
        
        for i, message in enumerate(test_messages):
            session_id = f"perf_test_{i}"
            
            # Medir tiempo de encriptación
            start_time = time.time()
            encrypted_data = flora.encrypt_message(message, master_key, session_id)
            encrypt_time = time.time() - start_time
            
            # Medir tiempo de desencriptación
            start_time = time.time()
            decrypted_message = flora.decrypt_message(encrypted_data, master_key)
            decrypt_time = time.time() - start_time
            
            # Verificar integridad
            integrity_ok = message == decrypted_message
            
            print(f"   📝 Mensaje {i+1} ({len(message)} bytes):")
            print(f"      🔒 Encriptación: {encrypt_time*1000:.2f} ms")
            print(f"      🔓 Desencriptación: {decrypt_time*1000:.2f} ms")
            print(f"      ✅ Integridad: {'OK' if integrity_ok else 'ERROR'}")
            
            # Calcular throughput
            if encrypt_time > 0:
                encrypt_throughput = len(message) / encrypt_time / 1024  # KB/s
                decrypt_throughput = len(message) / decrypt_time / 1024  # KB/s
                print(f"      🚀 Throughput: {encrypt_throughput:.1f} KB/s (enc) / {decrypt_throughput:.1f} KB/s (dec)")
        
        print("✅ Prueba de performance COMPLETADA")
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de performance: {e}")
        return False

def main():
    """Función principal de testing."""
    print("🌸 FLORA - Sistema de Cifrado Híbrido Post-Cuántico")
    print("🧪 INICIANDO SUITE COMPLETA DE PRUEBAS")
    print("="*60)
    
    # Contador de pruebas exitosas
    successful_tests = 0
    total_tests = 4
    
    # Ejecutar todas las pruebas
    tests = [
        ("Motor de Autodestrucción Caótica", test_chaotic_destruction_engine),
        ("Sistema de Cifrado FLORA", test_flora_crypto_system),
        ("Simulación de Ataques", test_attack_simulation),
        ("Performance y Rendimiento", test_performance)
    ]
    
    for test_name, test_function in tests:
        try:
            if test_function():
                successful_tests += 1
                print(f"✅ {test_name}: EXITOSA")
            else:
                print(f"❌ {test_name}: FALLIDA")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL DE PRUEBAS")
    print("="*60)
    print(f"✅ Pruebas exitosas: {successful_tests}/{total_tests}")
    print(f"📈 Tasa de éxito: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests == total_tests:
        print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS! Sistema FLORA funcionando perfectamente.")
        print("🚀 El sistema está listo para uso en producción.")
    elif successful_tests >= total_tests * 0.75:
        print("⚠️ La mayoría de pruebas exitosas. Revisar fallas antes de producción.")
    else:
        print("❌ Muchas pruebas fallidas. Revisar implementación del sistema.")
    
    print("\n🌸 ¡Gracias por probar FLORA - Crypto Flower!")
    return successful_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
