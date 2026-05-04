// Ejemplo de uso de OpenClaw Browser con Puppeteer
const puppeteer = require('puppeteer');

async function testOpenClawBrowser() {
  console.log('🚀 Probando OpenClaw Browser...');
  
  let browser;
  try {
    // Conectar a OpenClaw Browser (WebSocket)
    console.log('🔗 Conectando a ws://localhost:3000...');
    browser = await puppeteer.connect({
      browserWSEndpoint: 'ws://localhost:3000',
      defaultViewport: { width: 1280, height: 800 }
    });
    
    console.log('✅ Conectado exitosamente!');
    
    const page = await browser.newPage();
    
    // Test 1: Navegar a Google
    console.log('🌐 Navegando a Google...');
    await page.goto('https://www.google.com', { waitUntil: 'networkidle2' });
    
    const title = await page.title();
    console.log(`📄 Título: ${title}`);
    
    // Test 2: Tomar screenshot
    console.log('📸 Tomando screenshot...');
    await page.screenshot({ path: 'google-screenshot.png' });
    console.log('✅ Screenshot guardado: google-screenshot.png');
    
    // Test 3: Buscar algo
    console.log('🔍 Buscando "OpenClaw"...');
    await page.type('textarea[name="q"]', 'OpenClaw');
    await page.keyboard.press('Enter');
    await page.waitForNavigation({ waitUntil: 'networkidle2' });
    
    // Test 4: Ver resultados
    const results = await page.$$('h3');
    console.log(`📊 Resultados encontrados: ${results.length}`);
    
    // Test 5: Navegar a GitHub de OpenClaw
    console.log('🐙 Navegando a GitHub OpenClaw...');
    await page.goto('https://github.com/openclaw/openclaw', { waitUntil: 'networkidle2' });
    
    const stars = await page.$eval('.social-count[aria-label*="star"]', el => el.textContent.trim());
    console.log(`⭐ Stars en GitHub: ${stars}`);
    
    console.log('\n🎉 ¡Todos los tests pasaron!');
    console.log('OpenClaw Browser está funcionando correctamente.');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    
    // Intentar con Chrome local como fallback
    console.log('🔄 Intentando con Chrome local...');
    try {
      browser = await puppeteer.launch({ headless: 'new' });
      const page = await browser.newPage();
      await page.goto('https://www.google.com');
      console.log('✅ Chrome local funciona, pero OpenClaw Browser no está disponible');
      console.log('💡 Asegúrate de que:');
      console.log('   1. Docker esté corriendo');
      console.log('   2. La imagen se haya descargado: docker pull coollabsio/openclaw-browser:latest');
      console.log('   3. El contenedor esté corriendo: docker run -p 3000:3000 openclaw-browser');
    } catch (fallbackError) {
      console.error('❌ Fallback también falló:', fallbackError.message);
    }
  } finally {
    if (browser) {
      await browser.close();
      console.log('🔒 Navegador cerrado');
    }
  }
}

// Instrucciones de instalación si falta puppeteer
if (!require('puppeteer')) {
  console.log('📦 Instalando Puppeteer...');
  console.log('Ejecuta: npm install puppeteer');
  process.exit(1);
}

// Ejecutar test
testOpenClawBrowser();