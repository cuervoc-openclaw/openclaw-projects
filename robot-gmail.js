// 🤖 ROBOT GMAIL TEST
// Archivo: robot-gmail.js
// Ejecutar: node robot-gmail.js

const puppeteer = require('puppeteer');

console.log('🚀 Iniciando robot Gmail test...');
console.log('📝 Este es un EJEMPLO - NO usar credenciales reales!');
console.log('⚠️  ADVERTENCIA: No pongas passwords reales en código!');

async function robotGmailTest() {
  let browser;
  
  try {
    console.log('🔗 Conectando al robot navegador...');
    
    // OPCIÓN A: Usar OpenClaw Browser (recomendado)
    browser = await puppeteer.connect({
      browserWSEndpoint: 'ws://localhost:3000',
      defaultViewport: { width: 1280, height: 800 }
    });
    console.log('✅ Conectado a OpenClaw Browser');
    
  } catch (error) {
    console.log('⚠️  OpenClaw Browser no disponible, usando Chrome local...');
    
    // OPCIÓN B: Chrome local (fallback)
    browser = await puppeteer.launch({ 
      headless: false,  // true = sin pantalla, false = ver navegador
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    console.log('✅ Chrome local iniciado');
  }
  
  const page = await browser.newPage();
  
  try {
    // PASO 1: Ir a Gmail
    console.log('📧 Paso 1: Yendo a Gmail...');
    await page.goto('https://gmail.com', { 
      waitUntil: 'networkidle2',
      timeout: 30000 
    });
    
    // Verificar que cargó
    const title = await page.title();
    console.log(`📄 Título página: "${title}"`);
    
    // PASO 2: Buscar campo email (EJEMPLO - NO ESCRIBIR)
    console.log('🔍 Paso 2: Buscando campo email...');
    const emailField = await page.$('input[type="email"]');
    
    if (emailField) {
      console.log('✅ Campo email encontrado');
      console.log('💡 EJEMPLO: Aquí el robot escribiría tu email');
      console.log('💡 EJEMPLO: await page.type(\'input[type="email"]\', "tu@email.com")');
    } else {
      console.log('⚠️  Campo email no encontrado');
    }
    
    // PASO 3: Tomar screenshot
    console.log('📸 Paso 3: Tomando screenshot...');
    await page.screenshot({ 
      path: 'gmail-screenshot.png',
      fullPage: true 
    });
    console.log('✅ Screenshot guardado: gmail-screenshot.png');
    
    // PASO 4: Ver elementos de la página
    console.log('🔎 Paso 4: Analizando página...');
    
    const elements = {
      'input[type="email"]': 'Campo email',
      'input[type="password"]': 'Campo password',
      'button:contains("Siguiente")': 'Botón siguiente',
      'a:contains("Crear cuenta")': 'Enlace crear cuenta'
    };
    
    for (const [selector, description] of Object.entries(elements)) {
      const count = (await page.$$(selector)).length;
      if (count > 0) {
        console.log(`✅ ${description}: ${count} encontrado(s)`);
      }
    }
    
    console.log('\n🎉 ¡Demo completada!');
    console.log('📋 Resumen:');
    console.log('  - Robot navegó a Gmail');
    console.log('  - Encontró campos de login');
    console.log('  - Tomó screenshot');
    console.log('  - Listo para automatización REAL');
    
    console.log('\n🚀 Para automatización REAL necesitarías:');
    console.log('  1. Credenciales en variables de entorno');
    console.log('  2. Manejo seguro de passwords');
    console.log('  3. Lógica para captchas (si hay)');
    console.log('  4. Manejo de errores robusto');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    console.log('💡 Posibles soluciones:');
    console.log('  - Internet funciona?');
    console.log('  - Gmail está online?');
    console.log('  - OpenClaw Browser corriendo? (ws://localhost:3000)');
    
    // Tomar screenshot del error
    await page.screenshot({ path: 'error-screenshot.png' });
    console.log('📸 Screenshot del error: error-screenshot.png');
    
  } finally {
    // Cerrar navegador
    if (browser) {
      await browser.close();
      console.log('🔒 Navegador cerrado');
    }
  }
}

// Instrucciones si falta puppeteer
if (!require('puppeteer')) {
  console.log('📦 Instalando dependencias...');
  console.log('Ejecuta: npm install puppeteer');
  console.log('Luego: node robot-gmail.js');
  process.exit(1);
}

// Ejecutar el robot
robotGmailTest();