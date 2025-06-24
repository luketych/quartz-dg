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
    // We need to load the library using an ES module import.
    // We can do this by setting the page content to an HTML
    // with a <script type="module"> tag.
    const html = `
      <!DOCTYPE html>
      <html>
        <body>
          <script type="module">
            import { exportToBlob } from 'https://unpkg.com/@excalidraw/excalidraw@0.17.3/dist/index.modern.js';
            window.ExcalidrawUtils = { exportToBlob };
          </script>
        </body>
      </html>
    `;
    await page.setContent(html, { waitUntil: 'load' });

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
      const blob = await window.ExcalidrawUtils.exportToBlob({
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