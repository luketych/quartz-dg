const fs = require('fs').promises;
const path = require('path');
const puppeteer = require('puppeteer');
const lz = require('lz-string');

async function main() {
  const excalidrawPath = process.argv[2];
  if (!excalidrawPath) {
    console.error('Usage: node convert_excalidraw_to_png.js path/to/file.excalidraw.md');
    process.exit(1);
  }

  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  try {
    // Load React and ReactDOM, which are peer dependencies of Excalidraw.
    await page.addScriptTag({ url: 'https://unpkg.com/react@18.2.0/umd/react.production.min.js' });
    await page.addScriptTag({ url: 'https://unpkg.com/react-dom@18.2.0/umd/react-dom.production.min.js' });

    // Now, load the UMD build of the Excalidraw library.
    await page.addScriptTag({ url: 'https://unpkg.com/@excalidraw/excalidraw@0.17.3/dist/excalidraw.production.min.js' });

    // Wait for the library to be fully initialized and expose its global
    await page.waitForFunction('window.ExcalidrawLib');

    const fileContent = await fs.readFile(excalidrawPath, 'utf-8');
    const regex = /```compressed-json\n([\s\S]*?)\n```/;
    const match = fileContent.match(regex);
    if (!match || !match[1]) {
      throw new Error('Could not find compressed JSON data in the file.');
    }
    const compressedData = match[1].replace(/\s/g, '');
    const decompressedData = lz.decompressFromBase64(compressedData);
    if (!decompressedData) {
        throw new Error('Failed to decompress data.');
    }
    const { elements, appState } = JSON.parse(decompressedData);

    // Use page.evaluate to run code within the browser's context
    const base64Data = await page.evaluate(async ({ elements, appState }) => {
      const blob = await window.ExcalidrawLib.exportToBlob({
        elements,
        appState,
        files: {},
        mimeType: 'image/png',
      });

      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
      });
    }, { elements, appState });

    const buffer = Buffer.from(base64Data.split(',')[1], 'base64');
    const outputFileName = path.basename(excalidrawPath, '.excalidraw.md') + '.png';
    const outputPath = path.join(path.dirname(excalidrawPath), outputFileName);
    await fs.writeFile(outputPath, buffer);

    console.log(`✅ Exported to ${outputPath}`);
  } finally {
    await browser.close();
  }
}

main().catch(console.error);