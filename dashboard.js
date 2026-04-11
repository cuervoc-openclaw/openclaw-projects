/**
 * Cliente JavaScript para el Dashboard de Credenciales
 * Se comunica con el servidor Python en localhost:8081
 */

class CredentialsClient {
    constructor(serverUrl = 'http://localhost:8081') {
        this.serverUrl = serverUrl;
        this.connected = false;
        this.checkConnection();
    }
    
    async checkConnection() {
        try {
            const response = await fetch(`${this.serverUrl}/status`);
            if (response.ok) {
                this.connected = true;
                console.log('✅ Conectado al servidor de credenciales');
                return true;
            }
        } catch (error) {
            console.warn('⚠️ Servidor de credenciales no disponible');
            this.connected = false;
        }
        return false;
    }
    
    async storeCredentials(credentials) {
        if (!this.connected) {
            throw new Error('Servidor no disponible');
        }
        
        try {
            const response = await fetch(this.serverUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(credentials)
            });
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error almacenando credenciales:', error);
            throw error;
        }
    }
    
    async getCredentials() {
        if (!this.connected) {
            throw new Error('Servidor no disponible');
        }
        
        try {
            const response = await fetch(`${this.serverUrl}/get`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error obteniendo credenciales:', error);
            throw error;
        }
    }
    
    async clearCredentials() {
        if (!this.connected) {
            throw new Error('Servidor no disponible');
        }
        
        try {
            const response = await fetch(`${this.serverUrl}/clear`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error limpiando credenciales:', error);
            throw error;
        }
    }
}

// Exportar para uso en navegador
if (typeof window !== 'undefined') {
    window.CredentialsClient = CredentialsClient;
    
    // Inicializar automáticamente cuando se carga la página
    document.addEventListener('DOMContentLoaded', function() {
        window.credentialsClient = new CredentialsClient();
        
        // Actualizar estado de conexión en UI
        setTimeout(() => {
            const statusIndicator = document.getElementById('serverStatus');
            if (statusIndicator) {
                statusIndicator.textContent = window.credentialsClient.connected 
                    ? '✅ Conectado al servidor seguro' 
                    : '⚠️ Servidor no disponible - Usando almacenamiento local';
                statusIndicator.className = window.credentialsClient.connected 
                    ? 'status valid' 
                    : 'status invalid';
            }
        }, 1000);
    });
}

// Para uso en Node.js/OpenClaw
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CredentialsClient;
}