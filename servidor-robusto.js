// Servidor HTTP robusto para TDAH Dashboard
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8082;
const HOST = '0.0.0.0'; // Escuchar en todas las interfaces
const DIR = '/home/cuervoc/.openclaw/workspace/TDAH-DASHBOARD/dist';

console.log('🚀 SERVIDOR TDAH DASHBOARD - ROBUSTO');
console.log('====================================');
console.log(`📁 Directorio: ${DIR}`);
console.log(`🌐 Host: ${HOST}`);
console.log(`🔢 Puerto: ${PORT}`);
console.log(`🔗 URL local: http://localhost:${PORT}`);
console.log(`🔗 URL red: http://192.168.100.170:${PORT}`);

// Verificar directorio
if (!fs.existsSync(DIR)) {
    console.error(`❌ Error: Directorio no existe: ${DIR}`);
    process.exit(1);
}

if (!fs.existsSync(path.join(DIR, 'index.html'))) {
    console.error('❌ Error: index.html no encontrado');
    process.exit(1);
}

// Crear servidor
const server = http.createServer((req, res) => {
    console.log(`📥 ${new Date().toISOString()} - ${req.method} ${req.url}`);
    
    let filePath = path.join(DIR, req.url === '/' ? 'index.html' : req.url);
    
    // Seguridad: prevenir directory traversal
    if (!filePath.startsWith(DIR)) {
        filePath = path.join(DIR, 'index.html');
    }
    
    // Extensiones y content-types
    const extname = path.extname(filePath);
    let contentType = 'text/html';
    
    switch (extname) {
        case '.js': contentType = 'text/javascript'; break;
        case '.css': contentType = 'text/css'; break;
        case '.json': contentType = 'application/json'; break;
        case '.png': contentType = 'image/png'; break;
        case '.jpg': contentType = 'image/jpg'; break;
        case '.svg': contentType = 'image/svg+xml'; break;
        case '.ico': contentType = 'image/x-icon'; break;
        case '.webmanifest': contentType = 'application/manifest+json'; break;
    }
    
    // Leer archivo
    fs.readFile(filePath, (error, content) => {
        if (error) {
            if (error.code === 'ENOENT') {
                // Archivo no encontrado, servir index.html
                fs.readFile(path.join(DIR, 'index.html'), (err, content) => {
                    if (err) {
                        res.writeHead(500);
                        res.end('Error interno');
                    } else {
                        res.writeHead(200, { 'Content-Type': 'text/html' });
                        res.end(content, 'utf-8');
                    }
                });
            } else {
                res.writeHead(500);
                res.end(`Error del servidor: ${error.code}`);
            }
        } else {
            res.writeHead(200, { 
                'Content-Type': contentType,
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'no-cache'
            });
            res.end(content, 'utf-8');
        }
    });
});

// Iniciar servidor
server.listen(PORT, HOST, () => {
    console.log('\n✅ SERVIDOR INICIADO CORRECTAMENTE');
    console.log('================================');
    console.log(`🔗 URLs de acceso:`);
    console.log(`   1. Desde ESTE notebook: http://localhost:${PORT}`);
    console.log(`   2. Desde TU PC (via SSH Tunnel): http://localhost:${PORT}`);
    console.log(`   3. Directo desde red: http://192.168.100.170:${PORT}`);
    console.log('\n📱 El TDAH Dashboard debería cargar en tu navegador');
    console.log('🛑 Para detener: Ctrl+C');
});

// Manejar cierre
process.on('SIGINT', () => {
    console.log('\n🛑 Servidor detenido');
    process.exit(0);
});