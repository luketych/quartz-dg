# Monster Canvas VSCode Extension File Descriptions

This document provides descriptions for all files in the `src` directory of the Monster Canvas VSCode extension.

## Table of Contents

1. [Main Files](#main-files)
2. [Sidebar](#sidebar)
3. [Utils](#utils)
4. [Webview](#webview)
   - [HTML Templates](#html-templates)
   - [JavaScript](#javascript)
   - [Styles](#styles)

## Main Files

- [extension.js](extension.js.md) - The main entry point for the extension that handles activation and registration of commands and providers.
- [propertyConfig.json](propertyConfig.json.md) - Configuration file defining properties and validation rules for code documentation.

## Sidebar

- [fileExplorerProvider.js](fileExplorerProvider.js.md) - Provider for the file explorer tree view in the sidebar.

## Utils

- [constants.js](constants.js.md) - Contains default data and constants used throughout the extension.
- [storage.js](storage.js.md) - Utility functions for handling storage operations.

## Webview

- [webviewContent.js](webviewContent.js.md) - Generates the HTML content for webviews.
- [webviewProvider.js](webviewProvider.js.md) - Manages the webview panel for the Monster Canvas.
- [depthViewProvider.js](depthViewProvider.js.md) - Provider for the depth viewer webview.
- [drawingViewProvider.js](drawingViewProvider.js.md) - Provider for the image viewer webview.
- [fileDetailsViewProvider.js](fileDetailsViewProvider.js.md) - Provider for the file details view webview.

### HTML Templates

- [template.html](template.html.md) - Base HTML template for webviews.
- [depthViewTemplate.html](depthViewTemplate.html.md) - HTML template for the depth viewer.
- [drawingViewTemplate.html](drawingViewTemplate.html.md) - HTML template for the drawing canvas.
- [fileDetailsTemplate.html](fileDetailsTemplate.html.md) - HTML template for the file details view.
- [fileDetailsViewTemplate.html](fileDetailsViewTemplate.html.md) - HTML template for the file details view.

### JavaScript

- [canvas.js](canvas.js.md) - Handles canvas drawing and rendering.
- [events.js](events.js.md) - Manages event handling for the webview.
- [explorer.js](explorer.js.md) - Implements file explorer functionality in the webview.
- [fileDetails.js](fileDetails.js.md) - JavaScript for the file details view.
- [main.js](main.js.md) - Main JavaScript file that initializes the webview.
- [ui.js](ui.js.md) - Handles UI components and interactions.
- [utils.js](utils.js.md) - Utility functions for the webview.

### Styles

- [styles.css](styles.css.md) - CSS styles for the webview.
- [fileDetailsStyles.css](fileDetailsStyles.css.md) - CSS styles for the file details view.
