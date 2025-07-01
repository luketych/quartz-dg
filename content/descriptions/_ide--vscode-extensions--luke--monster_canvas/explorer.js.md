# explorer.js

This file implements the file explorer functionality for the Monster Canvas extension, providing a tree view of workspace files and folders that can be dragged onto the canvas.

## Key Functionality:

### File Explorer UI
- Creates and manages a hierarchical tree view of workspace files and folders
- Implements collapsible folder structure with toggle controls
- Displays appropriate icons for different file types
- Provides visual feedback for files that are already represented on the canvas

### Drag and Drop Integration
- Makes file and folder items draggable for placement on the canvas
- Configures drag events with appropriate metadata for the canvas to process
- Prevents dragging of files that are already represented on the canvas
- Maintains a set of used files to track which items are already on the canvas

### Interactive Features
- Allows clicking on used files to highlight their location on the canvas
- Implements folder expansion/collapse with intuitive toggle controls
- Provides visual feedback during drag operations
- Handles both file and folder items with appropriate behaviors

### State Management
- Tracks visibility state of the file explorer panel
- Maintains references to workspace files loaded from the extension
- Coordinates with the canvas to track which files are already in use
- Updates the UI to reflect the current state of file usage

This module enhances the Monster Canvas extension by providing a direct interface to the workspace file structure, allowing users to visually represent their project files on the canvas through an intuitive drag-and-drop mechanism.
