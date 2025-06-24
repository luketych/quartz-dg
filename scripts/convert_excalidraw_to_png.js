const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const { createCanvas, loadImage, Image, Path2D } = require('canvas');

// Setup DOM simulation for Node.js
const { window } = new JSDOM('<!DOCTYPE html><html><body></body></html>', {
  pretendToBeVisual: true,
});

// Attach canvas-related properties to the window
window.Image = Image;
window.Path2D = Path2D;
window.HTMLCanvasElement.prototype.getContext = (contextId) => {
    if (contextId === '2d') {
        // The canvas returned here can be a dummy one; excalidraw creates its own
        return createCanvas(0, 0).getContext('2d');
    }
    return null;
};

// Set up all the globals that excalidraw might need
global.window = window;
global.document = window.document;
global.navigator = window.navigator;
global.devicePixelRatio = window.devicePixelRatio || 1;
global.self = window;
global.Blob = window.Blob;
global.HTMLCanvasElement = window.HTMLCanvasElement;
global.Image = window.Image;
global.DOMParser = window.DOMParser;
global.Path2D = window.Path2D;

// Now, require excalidraw
const { exportToBlob } = require('@excalidraw/excalidraw');

// ---- Main Logic ----

const excalidrawPath = process.argv[2];
if (!excalidrawPath) {
  console.error('Usage: node export-excalidraw-to-png.js path/to/file.excalidraw');
  process.exit(1);
}

(async () => {
  const jsonData = fs.readFileSync(excalidrawPath, 'utf-8');
  const { elements, appState } = JSON.parse(jsonData);

  const blob = await exportToBlob({
    elements,
    appState,
    files: {}, // if your drawing has embedded files
    mimeType: 'image/png',
  });

  const arrayBuffer = await blob.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);

  const outputPath = path.basename(excalidrawPath, '.excalidraw') + '.png';
  fs.writeFileSync(outputPath, buffer);
  console.log(`✅ Exported to ${outputPath}`);
})();