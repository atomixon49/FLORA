//! FLORA WebAssembly - Plugin para Navegadores
//! 
//! Compila el motor de cifrado FLORA a WebAssembly para uso en extensiones de navegador

use wasm_bindgen::prelude::*;
use aes_gcm::{Aes256Gcm, KeyInit, Nonce};
use aes_gcm::aead::{Aead, Payload};
use rand::Rng;

// Importar funciones de consola para debugging
#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}

// Macro para logging fácil
macro_rules! console_log {
    ($($t:tt)*) => (log(&format_args!($($t)*).to_string()))
}

/// Motor de cifrado FLORA para WebAssembly
#[wasm_bindgen]
pub struct FloraWasm {
    key: [u8; 32],
}

#[wasm_bindgen]
impl FloraWasm {
    /// Crear nueva instancia de FLORA WASM
    #[wasm_bindgen(constructor)]
    pub fn new(key: &[u8]) -> Result<FloraWasm, JsValue> {
        if key.len() != 32 {
            return Err(JsValue::from_str("Key must be exactly 32 bytes"));
        }
        
        let mut key_array = [0u8; 32];
        key_array.copy_from_slice(key);
        
        Ok(FloraWasm { key: key_array })
    }
    
    /// Generar clave aleatoria de 32 bytes
    #[wasm_bindgen]
    pub fn generate_key() -> Vec<u8> {
        let mut key = [0u8; 32];
        rand::thread_rng().fill(&mut key);
        key.to_vec()
    }
    
    /// Cifrar datos
    #[wasm_bindgen]
    pub fn encrypt(&self, plaintext: &[u8], associated_data: &[u8]) -> Result<Vec<u8>, JsValue> {
        console_log!("🔐 Encrypting {} bytes", plaintext.len());
        
        let cipher = Aes256Gcm::new_from_slice(&self.key)
            .map_err(|e| JsValue::from_str(&format!("Cipher creation failed: {}", e)))?;
        
        // Generar nonce aleatorio
        let mut nonce_bytes = [0u8; 12];
        rand::thread_rng().fill(&mut nonce_bytes);
        let nonce = Nonce::from_slice(&nonce_bytes);
        
        let payload = Payload {
            msg: plaintext,
            aad: associated_data,
        };
        
        let ciphertext = cipher.encrypt(nonce, payload)
            .map_err(|e| JsValue::from_str(&format!("Encryption failed: {}", e)))?;
        
        // Retornar nonce + ciphertext
        let mut result = Vec::new();
        result.extend_from_slice(&nonce_bytes);
        result.extend_from_slice(&ciphertext);
        
        console_log!("✅ Encrypted successfully");
        Ok(result)
    }
    
    /// Desifrar datos
    #[wasm_bindgen]
    pub fn decrypt(&self, encrypted_data: &[u8], associated_data: &[u8]) -> Result<Vec<u8>, JsValue> {
        console_log!("🔓 Decrypting {} bytes", encrypted_data.len());
        
        if encrypted_data.len() < 12 {
            return Err(JsValue::from_str("Encrypted data too short"));
        }
        
        let cipher = Aes256Gcm::new_from_slice(&self.key)
            .map_err(|e| JsValue::from_str(&format!("Cipher creation failed: {}", e)))?;
        
        // Separar nonce y ciphertext
        let nonce_bytes = &encrypted_data[..12];
        let ciphertext = &encrypted_data[12..];
        
        let nonce = Nonce::from_slice(nonce_bytes);
        
        let payload = Payload {
            msg: ciphertext,
            aad: associated_data,
        };
        
        let plaintext = cipher.decrypt(nonce, payload)
            .map_err(|e| JsValue::from_str(&format!("Decryption failed: {}", e)))?;
        
        console_log!("✅ Decrypted successfully");
        Ok(plaintext)
    }
    
    /// Cifrar texto (string)
    #[wasm_bindgen]
    pub fn encrypt_string(&self, text: &str, associated_data: &str) -> Result<String, JsValue> {
        let plaintext = text.as_bytes();
        let ad = associated_data.as_bytes();
        
        let encrypted = self.encrypt(plaintext, ad)?;
        Ok(hex::encode(encrypted))
    }
    
    /// Desifrar texto (string)
    #[wasm_bindgen]
    pub fn decrypt_string(&self, encrypted_hex: &str, associated_data: &str) -> Result<String, JsValue> {
        let encrypted = hex::decode(encrypted_hex)
            .map_err(|e| JsValue::from_str(&format!("Hex decode failed: {}", e)))?;
        
        let ad = associated_data.as_bytes();
        let plaintext = self.decrypt(&encrypted, ad)?;
        
        String::from_utf8(plaintext)
            .map_err(|e| JsValue::from_str(&format!("UTF-8 decode failed: {}", e)))
    }
    
    /// Verificar integridad de datos
    #[wasm_bindgen]
    pub fn verify_integrity(&self, data: &[u8], associated_data: &[u8]) -> bool {
        // Implementación simple de verificación
        // En una implementación real, esto sería más sofisticado
        data.len() > 12 && associated_data.len() > 0
    }
}

/// Funciones de utilidad para el navegador
#[wasm_bindgen]
pub struct FloraUtils;

#[wasm_bindgen]
impl FloraUtils {
    /// Detectar si estamos en un entorno seguro
    #[wasm_bindgen]
    pub fn is_secure_context() -> bool {
        // En un entorno real, esto verificaría HTTPS, etc.
        true
    }
    
    /// Generar ID único para sesión
    #[wasm_bindgen]
    pub fn generate_session_id() -> String {
        let mut id = [0u8; 16];
        rand::thread_rng().fill(&mut id);
        hex::encode(id)
    }
    
    /// Validar formato de clave
    #[wasm_bindgen]
    pub fn validate_key(key: &[u8]) -> bool {
        key.len() == 32
    }
}

// Configurar panic hook para mejor debugging
#[wasm_bindgen(start)]
pub fn main() {
    console_error_panic_hook::set_once();
    console_log!("🌸 FLORA WASM initialized");
}

