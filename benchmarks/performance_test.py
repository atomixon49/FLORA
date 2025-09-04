"""
Benchmarks comparativos para FLORA: Python vs C++ vs Rust
"""
import time
import statistics
import sys
import os
from typing import List, Dict, Any

# Agregar el directorio src/python al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'python'))

try:
    from flora_crypto import FloraCryptoSystem
    from ffi_cpp import cpp_encrypt, cpp_decrypt
    from ffi_rust import rust_encrypt, rust_decrypt
    print("✅ Todos los backends importados correctamente")
except ImportError as e:
    print(f"❌ Error importando backends: {e}")
    sys.exit(1)

class PerformanceBenchmark:
    def __init__(self):
        self.results = {}
        self.test_data = {
            'small': b'Hello FLORA',
            'medium': b'FLORA is a revolutionary encryption system' * 10,
            'large': b'FLORA combines multiple cryptographic approaches' * 100,
            'xlarge': b'This is a very large message for performance testing' * 1000
        }
        
        # Configurar FLORA
        self.flora = FloraCryptoSystem()
        self.flora.generate_master_key('benchmark_password')
        self.flora.create_session_key('bench_session', 'bench_session')
        
        # Clave fija para C++ y Rust
        self.key = b'benchmark_key_32_bytes_for_testing'
    
    def benchmark_python_flora(self, data: bytes, iterations: int = 100) -> Dict[str, float]:
        """Benchmark del sistema FLORA Python"""
        times = []
        
        for _ in range(iterations):
            start = time.perf_counter()
            
            # Encriptar
            encrypted = self.flora.encrypt_message(data, 'bench_session', 'bench_session')
            
            # Desencriptar
            decrypted = self.flora.decrypt_message(encrypted, 'bench_session', 'bench_session')
            
            end = time.perf_counter()
            times.append(end - start)
        
        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'std': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times)
        }
    
    def benchmark_cpp(self, data: bytes, iterations: int = 100) -> Dict[str, float]:
        """Benchmark del backend C++"""
        times = []
        
        for _ in range(iterations):
            start = time.perf_counter()
            
            # Encriptar
            nonce, ciphertext = cpp_encrypt(self.key, data, b'AD')
            
            # Desencriptar
            decrypted = cpp_decrypt(self.key, nonce, ciphertext, b'AD')
            
            end = time.perf_counter()
            times.append(end - start)
        
        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'std': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times)
        }
    
    def benchmark_rust(self, data: bytes, iterations: int = 100) -> Dict[str, float]:
        """Benchmark del backend Rust"""
        times = []
        
        for _ in range(iterations):
            start = time.perf_counter()
            
            # Encriptar
            nonce, ciphertext = rust_encrypt(self.key, data, b'AD')
            
            # Desencriptar
            decrypted = rust_decrypt(self.key, nonce, ciphertext, b'AD')
            
            end = time.perf_counter()
            times.append(end - start)
        
        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'std': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times)
        }
    
    def run_benchmarks(self, iterations: int = 100):
        """Ejecutar todos los benchmarks"""
        print(f"🚀 Iniciando benchmarks con {iterations} iteraciones por prueba...")
        print("=" * 80)
        
        for size_name, data in self.test_data.items():
            print(f"\n📊 Tamaño de datos: {size_name} ({len(data)} bytes)")
            print("-" * 50)
            
            # Python FLORA
            print("🐍 Probando Python FLORA...")
            try:
                python_results = self.benchmark_python_flora(data, iterations)
                self.results[f'{size_name}_python'] = python_results
                print(f"   Media: {python_results['mean']:.6f}s")
                print(f"   Mediana: {python_results['median']:.6f}s")
            except Exception as e:
                print(f"   ❌ Error: {e}")
                self.results[f'{size_name}_python'] = None
            
            # C++
            print("⚡ Probando C++...")
            try:
                cpp_results = self.benchmark_cpp(data, iterations)
                self.results[f'{size_name}_cpp'] = cpp_results
                print(f"   Media: {cpp_results['mean']:.6f}s")
                print(f"   Mediana: {cpp_results['median']:.6f}s")
            except Exception as e:
                print(f"   ❌ Error: {e}")
                self.results[f'{size_name}_cpp'] = None
            
            # Rust
            print("🦀 Probando Rust...")
            try:
                rust_results = self.benchmark_rust(data, iterations)
                self.results[f'{size_name}_rust'] = rust_results
                print(f"   Media: {rust_results['mean']:.6f}s")
                print(f"   Mediana: {rust_results['median']:.6f}s")
            except Exception as e:
                print(f"   ❌ Error: {e}")
                self.results[f'{size_name}_rust'] = None
    
    def print_summary(self):
        """Imprimir resumen de resultados"""
        print("\n" + "=" * 80)
        print("📈 RESUMEN DE RESULTADOS")
        print("=" * 80)
        
        for size_name in self.test_data.keys():
            print(f"\n🔍 {size_name.upper()}:")
            
            python_result = self.results.get(f'{size_name}_python')
            cpp_result = self.results.get(f'{size_name}_cpp')
            rust_result = self.results.get(f'{size_name}_rust')
            
            if python_result and cpp_result and rust_result:
                # Calcular ratios de rendimiento
                python_time = python_result['mean']
                cpp_time = cpp_result['mean']
                rust_time = rust_result['mean']
                
                print(f"   Python FLORA: {python_time:.6f}s")
                print(f"   C++:          {cpp_time:.6f}s")
                print(f"   Rust:         {rust_time:.6f}s")
                
                if cpp_time > 0:
                    print(f"   C++ vs Python: {python_time/cpp_time:.2f}x más rápido")
                if rust_time > 0:
                    print(f"   Rust vs Python: {python_time/rust_time:.2f}x más rápido")
                if rust_time > 0 and cpp_time > 0:
                    print(f"   Rust vs C++: {cpp_time/rust_time:.2f}x más rápido")
            else:
                print("   ❌ Algunos resultados no disponibles")

def main():
    """Función principal"""
    print("🌸 FLORA Performance Benchmarks")
    print("Comparando Python vs C++ vs Rust")
    print("=" * 80)
    
    # Verificar que los backends estén disponibles
    print("🔍 Verificando backends...")
    
    try:
        # Test rápido de cada backend
        flora = FloraCryptoSystem()
        flora.generate_master_key('test')
        flora.create_session_key('test', 'test')
        
        test_data = b'Test message'
        
        # Python FLORA
        encrypted = flora.encrypt_message(test_data, 'test', 'test')
        decrypted = flora.decrypt_message(encrypted, 'test', 'test')
        assert decrypted == test_data
        print("✅ Python FLORA: OK")
        
        # C++
        key = b'test_key_32_bytes_for_testing_123'
        nonce, ciphertext = cpp_encrypt(key, test_data, b'AD')
        decrypted = cpp_decrypt(key, nonce, ciphertext, b'AD')
        assert decrypted == test_data
        print("✅ C++: OK")
        
        # Rust
        nonce, ciphertext = rust_encrypt(key, test_data, b'AD')
        decrypted = rust_decrypt(key, nonce, ciphertext, b'AD')
        assert decrypted == test_data
        print("✅ Rust: OK")
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return
    
    # Ejecutar benchmarks
    benchmark = PerformanceBenchmark()
    benchmark.run_benchmarks(iterations=50)  # Reducido para demo
    benchmark.print_summary()

if __name__ == "__main__":
    main()
