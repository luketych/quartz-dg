# canvas.js

This JavaScript file provides the core canvas drawing and interaction functionality for the Monster Canvas extension. It manages the HTML5 Canvas element used to render and interact with characters (emojis) and shapes. The module provides:

1. **Canvas Initialization and Sizing**:
   - Setting up the canvas element and 2D rendering context
   - Configuring event listeners for mouse and drag interactions
   - Implementing responsive canvas resizing to fit its container
   - Creating the animation/rendering loop

2. **Drawing Functions**:
   - Drawing characters (emojis) with their size, color, and position
   - Rendering various shape types (circle, square, triangle)
   - Displaying tooltips for file/folder information when hovering over elements
   - Highlighting selected or dragged elements with visual indicators
   - Drawing resize handles for shapes

3. **Interaction Utilities**:
   - Collision detection functions for determining if a point is within a shape
   - Helper functions for resize handle detection
   - Visual feedback functions (like flashing characters to highlight them)
   - Cursor style management based on the current mode (e.g., delete mode)

4. **State Management**:
   - Tracking currently dragged or resized elements
   - Managing canvas rendering state

5. **Advanced Features**:
   - Auto-scrolling to center highlighted elements
   - Shape-specific hit detection algorithms (different for circles, squares, triangles)
   - Visual feedback through color changes and animations

The canvas module is designed to work with other components like events.js (which handles the event callbacks referenced in this file) and provides a public interface through the global window.canvas object, allowing other modules to access its functionality.
