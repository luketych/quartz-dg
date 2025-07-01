# template.html

This file serves as the main HTML template for the Monster Canvas extension's webview interface. It defines the structure and layout of the interactive drawing canvas environment. The template includes:

1. **Basic HTML structure** with appropriate meta tags and a responsive viewport setting
2. **Sidebar section** containing:
   - Toggle button for expanding/collapsing the sidebar
   - Header with title and basic instructions
   - Character palette for selecting Unicode characters/emojis
   - Shape palette for selecting geometric shapes
   - File explorer panels (hidden by default)
   - Control buttons for various canvas operations:
     - Saving and resetting positions
     - Toggling between drag and delete modes
     - Showing/hiding different palettes and explorers

3. **Main content area** containing the canvas element where drawing and interaction occurs

4. **Placeholder tokens**:
   - `{{styles}}`: Replaced at runtime with CSS styles
   - `{{scripts}}`: Replaced at runtime with JavaScript code

This template provides the foundation for the visual interface of the extension, enabling users to interact with various elements, drag and place characters/shapes on the canvas, and manage their creations. The actual functionality is implemented through JavaScript that's injected into the template at runtime.
