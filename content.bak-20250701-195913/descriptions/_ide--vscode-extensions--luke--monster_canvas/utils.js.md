# utils.js

This file provides utility functions used throughout the Monster Canvas extension's webview, offering common operations and helper methods that support the application's functionality.

## Key Functionality:

### Color Management
- `getRandomColor`: Generates random colors from a predefined palette for new characters and shapes
- Provides a consistent set of visually distinct colors for visual elements

### Geometric Calculations
- `isPointInShape`: Implements hit detection algorithms for different shape types:
  - Circle: Uses distance calculation from center
  - Square: Uses boundary checking
  - Triangle: Uses barycentric coordinate calculation
- `isPointNearResizeHandle`: Determines if a point is close enough to a shape's resize handle

### File Type Utilities
- `getFileIcon`: Maps file extensions to appropriate icon representations
- Provides visual differentiation between different file types in the explorer

### Export Mechanism
- Exposes utility functions through a global `window.utils` object
- Makes functions available to other modules without requiring explicit imports

This module serves as a shared library of helper functions that are used across multiple components of the Monster Canvas extension. By centralizing these common operations, it promotes code reuse and maintains consistency throughout the application.
