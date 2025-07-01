# webviewContent.js

This utility file is responsible for generating the HTML content for the Monster Canvas extension's webviews. It combines HTML templates, CSS styles, and JavaScript files to create complete, interactive webview pages. The file provides:

1. **readFile function**: A helper function that reads file contents from the provided path.

2. **getWebviewContent function**: The main function that:
   - Loads the HTML template from `template.html`
   - Injects CSS styles from `styles.css`
   - Combines and injects JavaScript from multiple source files:
     - utils.js (utility functions)
     - canvas.js (canvas drawing functionality)
     - events.js (event handling)
     - ui.js (user interface interactions)
     - explorer.js (file explorer functionality)
     - main.js (main application logic)
   - Passes initialization data to the JavaScript, including:
     - Character data (emojis/unicode characters and their positions)
     - Shape data (geometric shapes and their properties)
     - Available shape types
     - Unicode character collections
     - Default data for reset functionality
     - Workspace file structure

The file acts as a bridge between the extension's backend (Node.js/VSCode API) and the frontend webview (HTML/CSS/JavaScript), ensuring that all necessary resources are properly combined and that runtime data is correctly passed to the webview interface. By using this approach, the extension can maintain separation of concerns while still providing a rich, interactive user experience.
