// FLORA Browser Extension - Content Script

class FloraContentScript {
    constructor() {
        this.isEncrypted = false;
        this.originalValues = new Map();
        this.encryptedElements = new Set();
        
        this.init();
    }
    
    init() {
        console.log('🌸 FLORA Content Script loaded');
        
        // Escuchar mensajes del popup
        chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
            this.handleMessage(request, sender, sendResponse);
            return true; // Mantener el canal abierto para respuestas asíncronas
        });
        
        // Detectar formularios automáticamente si la protección automática está activa
        this.checkAutoProtection();
        
        // Observar cambios en el DOM
        this.observeDOM();
    }
    
    async handleMessage(request, sender, sendResponse) {
        try {
            switch (request.action) {
                case 'encrypt':
                    await this.encryptPage(request.key);
                    sendResponse({ success: true, message: 'Página cifrada' });
                    break;
                    
                case 'decrypt':
                    await this.decryptPage(request.key);
                    sendResponse({ success: true, message: 'Página desifrada' });
                    break;
                    
                case 'getStatus':
                    sendResponse({ 
                        success: true, 
                        isEncrypted: this.isEncrypted,
                        encryptedCount: this.encryptedElements.size
                    });
                    break;
                    
                default:
                    sendResponse({ success: false, message: 'Acción no reconocida' });
            }
        } catch (error) {
            console.error('Error handling message:', error);
            sendResponse({ success: false, message: error.message });
        }
    }
    
    async checkAutoProtection() {
        try {
            const result = await chrome.storage.sync.get(['autoProtect']);
            if (result.autoProtect) {
                this.enableAutoProtection();
            }
        } catch (error) {
            console.error('Error checking auto protection:', error);
        }
    }
    
    enableAutoProtection() {
        // Detectar campos sensibles automáticamente
        const sensitiveSelectors = [
            'input[type="password"]',
            'input[name*="password"]',
            'input[name*="secret"]',
            'input[name*="key"]',
            'textarea[name*="private"]',
            'input[name*="credit"]',
            'input[name*="card"]',
            'input[name*="ssn"]'
        ];
        
        sensitiveSelectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                this.addEncryptionIndicator(element);
            });
        });
        
        console.log('🛡️ Auto-protection enabled');
    }
    
    addEncryptionIndicator(element) {
        // Agregar indicador visual de que el campo puede ser cifrado
        const indicator = document.createElement('span');
        indicator.className = 'flora-indicator';
        indicator.innerHTML = '🌸';
        indicator.style.cssText = `
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 12px;
            opacity: 0.7;
            cursor: pointer;
            z-index: 1000;
        `;
        
        // Hacer el contenedor relativo si no lo es
        const computedStyle = window.getComputedStyle(element);
        if (computedStyle.position === 'static') {
            element.style.position = 'relative';
        }
        
        element.parentNode.insertBefore(indicator, element.nextSibling);
        
        // Agregar evento de clic para cifrar
        indicator.addEventListener('click', (e) => {
            e.preventDefault();
            this.encryptElement(element);
        });
    }
    
    async encryptPage(key) {
        if (this.isEncrypted) {
            console.log('Página ya está cifrada');
            return;
        }
        
        try {
            // Convertir clave hex a bytes
            const keyBytes = this.hexToBytes(key);
            
            // Encontrar todos los campos de entrada
            const inputs = document.querySelectorAll('input, textarea');
            
            for (const input of inputs) {
                if (input.type === 'password' || this.isSensitiveField(input)) {
                    await this.encryptElement(input, keyBytes);
                }
            }
            
            this.isEncrypted = true;
            this.showEncryptionBanner();
            console.log('✅ Página cifrada correctamente');
            
        } catch (error) {
            console.error('Error encrypting page:', error);
            throw error;
        }
    }
    
    async decryptPage(key) {
        if (!this.isEncrypted) {
            console.log('Página no está cifrada');
            return;
        }
        
        try {
            // Convertir clave hex a bytes
            const keyBytes = this.hexToBytes(key);
            
            // Desifrar todos los elementos cifrados
            for (const element of this.encryptedElements) {
                await this.decryptElement(element, keyBytes);
            }
            
            this.isEncrypted = false;
            this.hideEncryptionBanner();
            console.log('✅ Página desifrada correctamente');
            
        } catch (error) {
            console.error('Error decrypting page:', error);
            throw error;
        }
    }
    
    async encryptElement(element, keyBytes = null) {
        if (!keyBytes) {
            // Obtener clave del storage
            const result = await chrome.storage.sync.get(['masterKey']);
            if (!result.masterKey) {
                throw new Error('No hay clave maestra configurada');
            }
            keyBytes = this.hexToBytes(result.masterKey);
        }
        
        const originalValue = element.value;
        if (!originalValue.trim()) {
            return; // No cifrar valores vacíos
        }
        
        try {
            // Simular cifrado (en un entorno real, usaría WebAssembly)
            const encrypted = await this.simulateEncryption(originalValue, keyBytes);
            
            // Guardar valor original
            this.originalValues.set(element, originalValue);
            
            // Actualizar elemento
            element.value = encrypted;
            element.setAttribute('data-flora-encrypted', 'true');
            element.style.backgroundColor = '#fff3cd';
            element.style.borderColor = '#ffc107';
            
            // Agregar a la lista de elementos cifrados
            this.encryptedElements.add(element);
            
            console.log(`🔐 Elemento cifrado: ${element.name || element.id || 'unknown'}`);
            
        } catch (error) {
            console.error('Error encrypting element:', error);
            throw error;
        }
    }
    
    async decryptElement(element, keyBytes) {
        if (!element.hasAttribute('data-flora-encrypted')) {
            return; // No está cifrado
        }
        
        try {
            // Obtener valor original
            const originalValue = this.originalValues.get(element);
            if (!originalValue) {
                console.warn('No se encontró valor original para el elemento');
                return;
            }
            
            // Restaurar valor original
            element.value = originalValue;
            element.removeAttribute('data-flora-encrypted');
            element.style.backgroundColor = '';
            element.style.borderColor = '';
            
            // Remover de la lista de elementos cifrados
            this.encryptedElements.delete(element);
            this.originalValues.delete(element);
            
            console.log(`🔓 Elemento desifrado: ${element.name || element.id || 'unknown'}`);
            
        } catch (error) {
            console.error('Error decrypting element:', error);
            throw error;
        }
    }
    
    async simulateEncryption(text, keyBytes) {
        // Simulación de cifrado (en un entorno real, usaría WebAssembly)
        const textBytes = new TextEncoder().encode(text);
        const encrypted = new Uint8Array(textBytes.length);
        
        for (let i = 0; i < textBytes.length; i++) {
            encrypted[i] = textBytes[i] ^ keyBytes[i % keyBytes.length];
        }
        
        return 'FLORA:' + Array.from(encrypted)
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }
    
    isSensitiveField(element) {
        const sensitiveNames = [
            'password', 'secret', 'key', 'private', 'credit', 'card', 'ssn',
            'social', 'security', 'pin', 'code', 'token'
        ];
        
        const name = (element.name || '').toLowerCase();
        const id = (element.id || '').toLowerCase();
        const placeholder = (element.placeholder || '').toLowerCase();
        
        return sensitiveNames.some(sensitive => 
            name.includes(sensitive) || 
            id.includes(sensitive) || 
            placeholder.includes(sensitive)
        );
    }
    
    hexToBytes(hex) {
        const bytes = new Uint8Array(hex.length / 2);
        for (let i = 0; i < hex.length; i += 2) {
            bytes[i / 2] = parseInt(hex.substr(i, 2), 16);
        }
        return bytes;
    }
    
    showEncryptionBanner() {
        // Crear banner de cifrado
        const banner = document.createElement('div');
        banner.id = 'flora-encryption-banner';
        banner.innerHTML = `
            <div style="
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 8px 16px;
                text-align: center;
                font-size: 14px;
                font-weight: 600;
                z-index: 10000;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            ">
                🌸 FLORA: Página cifrada - ${this.encryptedElements.size} elementos protegidos
            </div>
        `;
        
        document.body.appendChild(banner);
        
        // Ajustar el contenido para el banner
        document.body.style.paddingTop = '40px';
    }
    
    hideEncryptionBanner() {
        const banner = document.getElementById('flora-encryption-banner');
        if (banner) {
            banner.remove();
            document.body.style.paddingTop = '';
        }
    }
    
    observeDOM() {
        // Observar cambios en el DOM para detectar nuevos campos
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            // Buscar campos sensibles en el nuevo nodo
                            const inputs = node.querySelectorAll ? 
                                node.querySelectorAll('input, textarea') : [];
                            
                            inputs.forEach(input => {
                                if (this.isSensitiveField(input)) {
                                    this.addEncryptionIndicator(input);
                                }
                            });
                        }
                    });
                }
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
}

// Inicializar content script
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new FloraContentScript();
    });
} else {
    new FloraContentScript();
}

