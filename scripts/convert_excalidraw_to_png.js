const puppeteer = require('puppeteer');

async function findGlobal() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  try {
    await page.goto('about:blank');
    const initialGlobals = await page.evaluate(() => Object.keys(window));
    await page.addScriptTag({ url: 'https://unpkg.com/@excalidraw/excalidraw@0.17.3/dist/excalidraw.production.min.js' });
    const finalGlobals = await page.evaluate(() => Object.keys(window));
    const newGlobals = finalGlobals.filter(key => !initialGlobals.includes(key));
    console.log('New global variables found:', newGlobals);
  } finally {
    await browser.close();
  }
}

findGlobal().catch(console.error);