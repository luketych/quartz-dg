# events.js

This file implements the event handling system for the Monster Canvas extension, managing all user interactions with the canvas and its elements.

## Key Functionality:

### Mouse Event Handlers
- `handleCanvasMouseDown`: Processes mouse button press events for shape resizing, character/shape dragging, and element creation
- `handleCanvasMouseMove`: Tracks mouse movement for dragging operations, hover effects, and cursor style updates
- `handleCanvasMouseUp`: Finalizes drag and resize operations, saving the updated state
- `handleCanvasMouseLeave`: Handles cases when the mouse leaves the canvas during an operation
- `handleCanvasClick`: Processes click events for element selection, deletion, and placement

### Drag and Drop Support
- `handleCanvasDragOver`: Manages drag-over events for file/folder dragging from the file explorer
- `handleCanvasDrop`: Processes drop events, creating visual representations of files/folders on the canvas
- Tracks which files are already represented on the canvas to prevent duplicates

### Interaction Modes
- Supports different interaction modes (drag mode, delete mode, carrying mode)
- Provides visual feedback through cursor changes based on the current mode
- Implements "carrying mode" where elements follow the cursor until placed

### State Management
- Tracks dragged and resized elements with offset calculations for precise positioning
- Maintains the state of used files to prevent duplicate representations
- Updates the file explorer UI to reflect which files are already on the canvas
- Provides debugging capabilities for troubleshooting state inconsistencies

### Visual Feedback
- Updates cursor styles based on the current interaction context
- Highlights elements on hover to show they can be interacted with
- Implements a flashing effect to locate elements on the canvas

This module forms the interactive foundation of the Monster Canvas extension, enabling users to manipulate visual elements through intuitive mouse operations and drag-and-drop functionality.
