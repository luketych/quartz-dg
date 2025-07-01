# main.js

This JavaScript file serves as the main entry point and initialization module for the Monster Canvas extension's webview frontend. It provides:

1. **Global State Management**: 
   - Defines and manages global variables for the entire frontend application:
     - characters: Array of character objects (emojis with position data)
     - shapes: Array of shape objects
     - shapeTypes: Available geometric shape types
     - unicodeCharacters: Categories of Unicode/emoji characters
     - Default data for reset functionality
     - ID counters for creating new elements

2. **Initialization Function (`init`)**:
   - Accepts parameters passed from the backend:
     - Initial character and shape data
     - Shape types configuration
     - Unicode character collections
     - Default data for reset operations
     - Workspace file structure
   - Sets up the application state with provided data
   - Calculates next available IDs for new elements
   - Initializes all UI components by calling other modules:
     - Canvas initialization
     - UI initialization
     - Sidebar initialization
     - File explorer population

3. **Event Handling**:
   - Sets up message event listeners for communication with the extension backend
   - Handles workspace file updates from VSCode
   - Sets up keyboard event listeners (e.g., for Escape key)

4. **Animation Loop**:
   - Establishes the canvas drawing interval (10 frames per second)

The file acts as the coordinating center for the frontend application, bringing together the various JavaScript modules and connecting them to the data provided by the VSCode extension. It exposes the `init` function globally, which is called by the script injected by `webviewContent.js` when the DOM is loaded.
