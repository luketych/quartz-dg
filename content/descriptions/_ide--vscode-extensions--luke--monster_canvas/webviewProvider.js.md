# webviewProvider.js

This file implements the `monsterCanvasWebviewProvider` class which is responsible for creating and managing the main webview panel for the Monster Canvas extension. The provider handles:

1. **Panel Creation and Lifecycle**:
   - Creating the webview panel with appropriate options
   - Handling panel disposal and state preservation
   - Managing panel visibility and focus

2. **Data Management**:
   - Loading saved character and shape data from extension storage
   - Persisting changes to character positions and shapes
   - Providing mechanisms for resetting to default states

3. **Communication**:
   - Setting up bidirectional messaging between the extension and webview
   - Processing commands from the webview (save, reset, workspace file requests)
   - Sending updates back to the webview

4. **Workspace Integration**:
   - Reading the workspace file structure recursively
   - Filtering out specific directories (node_modules, .git)
   - Providing file metadata to the webview for the file explorer

The provider works closely with other utility modules like `webviewContent.js` (for generating HTML), `storage.js` (for data persistence), and `constants.js` (for default values). It acts as the central controller that coordinates between the VSCode extension API and the user-facing webview interface, ensuring that user interactions are properly processed and state is maintained across sessions.
