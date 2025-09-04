// FLORA Browser Extension - Popup Script

class FloraPopup {
    constructor() {
        this.flora = null;
        this.isActive = false;
        this.sessionStart = Date.now();
        this.encryptedCount = 0;
        
        this.init();
    }
    
    async init() {
        console.log('🌸 FLORA Popup initialized');
        
        // Cargar configuración guardada
        await this.loadSettings();
        
        // Configurar event listeners
        this.setupEventListeners();
        
        // Inicializar WebAssembly
        await this.initWasm();
        
        // Actualizar UI
        this.updateUI();
        
        // Iniciar timer de sesión
        this.startSessionTimer();
    }
    
    async loadSettings() {
        try {
            const result = await chrome.storage.sync.get([
                'masterKey',
                'autoProtect',
                'autoDestroy',
                'encryptedCount'
            ]);
            
            if (result.masterKey) {
                document.getElementById('masterKey').value = result.masterKey;
            }
            
            if (result.autoProtect !== undefined) {
                document.getElementById('autoProtect').checked = result.autoProtect;
            }
            
            if (result.autoDestroy !== undefined) {
                document.getElementById('autoDestroy').checked = result.autoDestroy;
            }
            
            if (result.encryptedCount) {
                this.encryptedCount = result.encryptedCount;
            }
            
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    }
    
    async saveSettings() {
        try {
            const settings = {
                masterKey: document.getElementById('masterKey').value,
                autoProtect: document.getElementById('autoProtect').checked,
                autoDestroy: document.getElementById('autoDestroy').checked,
                encryptedCount: this.encryptedCount
            };
            
            await chrome.storage.sync.set(settings);
            console.log('Settings saved');
        } catch (error) {
            console.error('Error saving settings:', error);
        }
    }
    
    setupEventListeners() {
        // Generar clave
        document.getElementById('generateKey').addEventListener('click', () => {
            this.generateKey();
        });
        
        // Cambios en la clave
        document.getElementById('masterKey').addEventListener('input', () => {
            this.updateKeyStatus();
            this.saveSettings();
        });
        
        // Botones de cifrado
        document.getElementById('encryptPage').addEventListener('click', () => {
            this.encryptCurrentPage();
        });
        
        document.getElementById('decryptPage').addEventListener('click', () => {
            this.decryptCurrentPage();
        });
        
        // Toggles
        document.getElementById('autoProtect').addEventListener('change', () => {
            this.saveSettings();
            this.updateStatus();
        });
        
        document.getElementById('autoDestroy').addEventListener('change', () => {
            this.saveSettings();
        });
        
        // Enlaces
        document.getElementById('settings').addEventListener('click', (e) => {
            e.preventDefault();
            this.openSettings();
        });
        
        document.getElementById('help').addEventListener('click', (e) => {
            e.preventDefault();
            this.openHelp();
        });
    }
    
    async initWasm() {
        try {
            // En un entorno real, esto cargaría el módulo WASM
            // const wasmModule = await import('./flora-wasm.js');
            // this.flora = new wasmModule.FloraWasm();
            
            // Por ahora, simulamos la funcionalidad
            console.log('WASM module loaded (simulated)');
            this.isActive = true;
            this.updateStatus();
            
        } catch (error) {
            console.error('Error loading WASM:', error);
            this.showError('Error al cargar el módulo de cifrado');
        }
    }
    
    generateKey() {
        // Generar clave aleatoria de 32 bytes
        const key = new Uint8Array(32);
        crypto.getRandomValues(key);
        
        // Convertir a string hexadecimal
        const keyHex = Array.from(key)
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
        
        document.getElementById('masterKey').value = keyHex;
        this.updateKeyStatus();
        this.saveSettings();
        
        this.showNotification('Clave generada correctamente');
    }
    
    updateKeyStatus() {
        const key = document.getElementById('masterKey').value;
        const keyStatus = document.getElementById('keyStatus');
        
        if (key.length === 64) { // 32 bytes en hex
            keyStatus.textContent = 'Clave válida (32 bytes)';
            keyStatus.style.color = '#2ed573';
        } else if (key.length > 0) {
            keyStatus.textContent = `Clave inválida (${key.length/2} bytes)`;
            keyStatus.style.color = '#ff4757';
        } else {
            keyStatus.textContent = 'Sin clave configurada';
            keyStatus.style.color = '#7f8c8d';
        }
    }
    
    async encryptCurrentPage() {
        if (!this.isActive) {
            this.showError('FLORA no está activo');
            return;
        }
        
        const key = document.getElementById('masterKey').value;
        if (key.length !== 64) {
            this.showError('Clave inválida. Debe tener 32 bytes (64 caracteres hex)');
            return;
        }
        
        try {
            // Obtener pestaña activa
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            
            // Enviar comando de cifrado al content script
            await chrome.tabs.sendMessage(tab.id, {
                action: 'encrypt',
                key: key
            });
            
            this.encryptedCount++;
            this.updateStats();
            this.saveSettings();
            
            this.showNotification('Página cifrada correctamente');
            
        } catch (error) {
            console.error('Error encrypting page:', error);
            this.showError('Error al cifrar la página');
        }
    }
    
    async decryptCurrentPage() {
        if (!this.isActive) {
            this.showError('FLORA no está activo');
            return;
        }
        
        const key = document.getElementById('masterKey').value;
        if (key.length !== 64) {
            this.showError('Clave inválida. Debe tener 32 bytes (64 caracteres hex)');
            return;
        }
        
        try {
            // Obtener pestaña activa
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            
            // Enviar comando de desifrado al content script
            await chrome.tabs.sendMessage(tab.id, {
                action: 'decrypt',
                key: key
            });
            
            this.showNotification('Página desifrada correctamente');
            
        } catch (error) {
            console.error('Error decrypting page:', error);
            this.showError('Error al desifrar la página');
        }
    }
    
    updateStatus() {
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.status-text');
        
        if (this.isActive) {
            statusDot.classList.add('active');
            statusText.textContent = 'Activo';
        } else {
            statusDot.classList.remove('active');
            statusText.textContent = 'Inactivo';
        }
    }
    
    updateStats() {
        document.getElementById('encryptedCount').textContent = this.encryptedCount;
    }
    
    startSessionTimer() {
        setInterval(() => {
            const elapsed = Date.now() - this.sessionStart;
            const minutes = Math.floor(elapsed / 60000);
            const seconds = Math.floor((elapsed % 60000) / 1000);
            
            document.getElementById('sessionTime').textContent = 
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);
    }
    
    showNotification(message) {
        // Crear notificación temporal
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #2ed573;
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
    
    showError(message) {
        // Crear notificación de error
        const notification = document.createElement('div');
        notification.className = 'notification error';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ff4757;
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
    
    openSettings() {
        // Abrir página de configuración
        chrome.tabs.create({ url: chrome.runtime.getURL('settings.html') });
    }
    
    openHelp() {
        // Abrir página de ayuda
        chrome.tabs.create({ url: 'https://github.com/atomixon49/CRYPTO-FLOWER' });
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new FloraPopup();
});

// Agregar estilos para notificaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
