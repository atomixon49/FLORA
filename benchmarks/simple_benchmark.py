"""
Benchmark simple: C++ vs Rust (sin FLORA completo)
"""
import time
import statistics
import sys
import os

# Agregar el directorio src/python al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'python'))

try:
    from ffi_cpp import cpp_encrypt, cpp_decrypt
    from ffi_rust import rust_encrypt, rust_decrypt
    print("✅ Backends C++ y Rust importados correctamente")
except ImportError as e:
    print(f"❌ Error importando backends: {e}")
    sys.exit(1)

def benchmark_backend(encrypt_func, decrypt_func, name: str, data: bytes, iterations: int = 100):
    """Benchmark genérico para cualquier backend"""
    times = []
    key = b'benchmark_key_32_bytes_for_testing'[:32]
    
    for _ in range(iterations):
        start = time.perf_counter()
        
        # Encriptar
        nonce, ciphertext = encrypt_func(key, data, b'AD')
        
        # Desencriptar
        decrypted = decrypt_func(key, nonce, ciphertext, b'AD')
        
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        'name': name,
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'std': statistics.stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times)
    }

def main():
    """Función principal"""
    print("🚀 FLORA Simple Benchmark: C++ vs Rust")
    print("=" * 50)
    
    # Datos de prueba
    test_cases = {
        'small': b'Hello FLORA',
        'medium': b'FLORA is a revolutionary encryption system' * 10,
        'large': b'FLORA combines multiple cryptographic approaches' * 100,
    }
    
    iterations = 50
    
    for size_name, data in test_cases.items():
        print(f"\n📊 Tamaño: {size_name} ({len(data)} bytes)")
        print("-" * 30)
        
        # Benchmark C++
        print("⚡ Probando C++...")
        try:
            cpp_result = benchmark_backend(cpp_encrypt, cpp_decrypt, "C++", data, iterations)
            print(f"   Media: {cpp_result['mean']:.6f}s")
            print(f"   Mediana: {cpp_result['median']:.6f}s")
        except Exception as e:
            print(f"   ❌ Error C++: {e}")
            cpp_result = None
        
        # Benchmark Rust
        print("🦀 Probando Rust...")
        try:
            rust_result = benchmark_backend(rust_encrypt, rust_decrypt, "Rust", data, iterations)
            print(f"   Media: {rust_result['mean']:.6f}s")
            print(f"   Mediana: {rust_result['median']:.6f}s")
        except Exception as e:
            print(f"   ❌ Error Rust: {e}")
            rust_result = None
        
        # Comparación
        if cpp_result and rust_result:
            cpp_time = cpp_result['mean']
            rust_time = rust_result['mean']
            
            if cpp_time > 0 and rust_time > 0:
                ratio = cpp_time / rust_time
                if ratio > 1:
                    print(f"   🏆 Rust es {ratio:.2f}x más rápido que C++")
                else:
                    print(f"   🏆 C++ es {1/ratio:.2f}x más rápido que Rust")
    
    print("\n" + "=" * 50)
    print("✅ Benchmark completado")

if __name__ == "__main__":
    main()
