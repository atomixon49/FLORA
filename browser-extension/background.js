// FLORA Browser Extension - Background Script (Service Worker)

class FloraBackground {
    constructor() {
        this.init();
    }
    
    init() {
        console.log('🌸 FLORA Background Script initialized');
        
        // Configurar event listeners
        this.setupEventListeners();
        
        // Inicializar configuración por defecto
        this.initializeDefaultSettings();
    }
    
    setupEventListeners() {
        // Instalación de la extensión
        chrome.runtime.onInstalled.addListener((details) => {
            this.handleInstallation(details);
        });
        
        // Actualización de la extensión
        chrome.runtime.onStartup.addListener(() => {
            this.handleStartup();
        });
        
        // Mensajes del content script
        chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
            this.handleMessage(request, sender, sendResponse);
            return true;
        });
        
        // Cambios en las pestañas
        chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
            this.handleTabUpdate(tabId, changeInfo, tab);
        });
        
        // Cierre de pestañas
        chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
            this.handleTabRemoved(tabId, removeInfo);
        });
    }
    
    async handleInstallation(details) {
        console.log('FLORA extension installed:', details.reason);
        
        if (details.reason === 'install') {
            // Configuración inicial
            await this.initializeDefaultSettings();
            
            // Abrir página de bienvenida
            chrome.tabs.create({
                url: chrome.runtime.getURL('welcome.html')
            });
        } else if (details.reason === 'update') {
            // Manejar actualizaciones
            await this.handleUpdate(details.previousVersion);
        }
    }
    
    async handleStartup() {
        console.log('FLORA extension started');
        
        // Verificar configuración
        await this.validateSettings();
        
        // Inicializar monitoreo de seguridad
        this.startSecurityMonitoring();
    }
    
    async initializeDefaultSettings() {
        const defaultSettings = {
            masterKey: '',
            autoProtect: false,
            autoDestroy: false,
            encryptedCount: 0,
            sessionStart: Date.now(),
            securityLevel: 'medium',
            whitelist: [],
            blacklist: []
        };
        
        try {
            const existing = await chrome.storage.sync.get(Object.keys(defaultSettings));
            const settings = { ...defaultSettings, ...existing };
            await chrome.storage.sync.set(settings);
            
            console.log('Default settings initialized');
        } catch (error) {
            console.error('Error initializing settings:', error);
        }
    }
    
    async validateSettings() {
        try {
            const settings = await chrome.storage.sync.get(['masterKey', 'securityLevel']);
            
            if (!settings.masterKey) {
                console.log('No master key configured');
                return;
            }
            
            if (settings.masterKey.length !== 64) {
                console.warn('Invalid master key length');
                await chrome.storage.sync.remove(['masterKey']);
            }
            
        } catch (error) {
            console.error('Error validating settings:', error);
        }
    }
    
    async handleUpdate(previousVersion) {
        console.log(`Updating from version ${previousVersion}`);
        
        // Migrar configuración si es necesario
        await this.migrateSettings(previousVersion);
        
        // Notificar al usuario sobre la actualización
        this.showUpdateNotification();
    }
    
    async migrateSettings(previousVersion) {
        // Lógica de migración de configuración
        // Esto se ejecutaría cuando se actualiza la extensión
        console.log('Migrating settings from version:', previousVersion);
    }
    
    showUpdateNotification() {
        chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icons/icon48.png',
            title: 'FLORA Actualizado',
            message: 'La extensión se ha actualizado con nuevas características de seguridad.'
        });
    }
    
    async handleMessage(request, sender, sendResponse) {
        try {
            switch (request.action) {
                case 'getSettings':
                    const settings = await chrome.storage.sync.get();
                    sendResponse({ success: true, settings });
                    break;
                    
                case 'updateSettings':
                    await chrome.storage.sync.set(request.settings);
                    sendResponse({ success: true });
                    break;
                    
                case 'logEvent':
                    this.logSecurityEvent(request.event);
                    sendResponse({ success: true });
                    break;
                    
                case 'checkSecurity':
                    const securityStatus = await this.checkSecurityStatus();
                    sendResponse({ success: true, security: securityStatus });
                    break;
                    
                default:
                    sendResponse({ success: false, message: 'Unknown action' });
            }
        } catch (error) {
            console.error('Error handling message:', error);
            sendResponse({ success: false, message: error.message });
        }
    }
    
    async handleTabUpdate(tabId, changeInfo, tab) {
        if (changeInfo.status === 'complete' && tab.url) {
            // Verificar si la página está en la lista negra
            const isBlacklisted = await this.isUrlBlacklisted(tab.url);
            if (isBlacklisted) {
                this.handleBlacklistedSite(tabId, tab.url);
            }
            
            // Verificar si la protección automática está activa
            const settings = await chrome.storage.sync.get(['autoProtect']);
            if (settings.autoProtect) {
                this.enableAutoProtectionForTab(tabId);
            }
        }
    }
    
    async handleTabRemoved(tabId, removeInfo) {
        // Limpiar datos de la pestaña
        console.log(`Tab ${tabId} removed`);
    }
    
    async isUrlBlacklisted(url) {
        try {
            const settings = await chrome.storage.sync.get(['blacklist']);
            const blacklist = settings.blacklist || [];
            
            return blacklist.some(pattern => {
                try {
                    const regex = new RegExp(pattern);
                    return regex.test(url);
                } catch (e) {
                    return url.includes(pattern);
                }
            });
        } catch (error) {
            console.error('Error checking blacklist:', error);
            return false;
        }
    }
    
    handleBlacklistedSite(tabId, url) {
        console.log(`Blacklisted site detected: ${url}`);
        
        // Mostrar advertencia
        chrome.tabs.sendMessage(tabId, {
            action: 'showWarning',
            message: 'Este sitio está en la lista negra de FLORA'
        });
    }
    
    async enableAutoProtectionForTab(tabId) {
        try {
            await chrome.tabs.sendMessage(tabId, {
                action: 'enableAutoProtection'
            });
        } catch (error) {
            // El content script podría no estar listo aún
            console.log('Content script not ready for tab:', tabId);
        }
    }
    
    startSecurityMonitoring() {
        // Monitorear eventos de seguridad
        setInterval(() => {
            this.performSecurityCheck();
        }, 30000); // Cada 30 segundos
    }
    
    async performSecurityCheck() {
        try {
            const settings = await chrome.storage.sync.get(['autoDestroy', 'securityLevel']);
            
            if (settings.autoDestroy) {
                // Verificar si hay actividad sospechosa
                const suspiciousActivity = await this.detectSuspiciousActivity();
                
                if (suspiciousActivity) {
                    await this.triggerAutoDestruction();
                }
            }
        } catch (error) {
            console.error('Error in security check:', error);
        }
    }
    
    async detectSuspiciousActivity() {
        // Implementar detección de actividad sospechosa
        // Por ahora, simulación
        return false;
    }
    
    async triggerAutoDestruction() {
        console.log('🚨 Auto-destruction triggered');
        
        // Limpiar todas las claves
        await chrome.storage.sync.clear();
        
        // Notificar a todas las pestañas
        const tabs = await chrome.tabs.query({});
        for (const tab of tabs) {
            try {
                await chrome.tabs.sendMessage(tab.id, {
                    action: 'autoDestruction'
                });
            } catch (error) {
                // Ignorar errores de pestañas sin content script
            }
        }
        
        // Mostrar notificación
        chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icons/icon48.png',
            title: 'FLORA Auto-Destrucción',
            message: 'Sistema comprometido. Todas las claves han sido destruidas.'
        });
    }
    
    async checkSecurityStatus() {
        try {
            const settings = await chrome.storage.sync.get([
                'masterKey', 'autoProtect', 'autoDestroy', 'securityLevel'
            ]);
            
            return {
                hasKey: !!settings.masterKey,
                autoProtect: settings.autoProtect,
                autoDestroy: settings.autoDestroy,
                securityLevel: settings.securityLevel || 'medium',
                lastCheck: Date.now()
            };
        } catch (error) {
            console.error('Error checking security status:', error);
            return { error: error.message };
        }
    }
    
    logSecurityEvent(event) {
        console.log('Security event:', event);
        
        // En un entorno real, esto enviaría logs a un servidor
        // Por ahora, solo log local
    }
}

// Inicializar background script
new FloraBackground();
