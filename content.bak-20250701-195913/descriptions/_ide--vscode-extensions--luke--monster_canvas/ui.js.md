# ui.js

This file implements the user interface functionality for the Monster Canvas extension, managing the sidebar, palettes, and various UI controls.

## Key Functionality:

### UI Initialization
- Sets up event listeners for all UI buttons and controls
- Initializes the character and shape palettes with available options
- Configures the collapsible sidebar with toggle functionality
- Establishes the initial UI state for the application

### Mode Management
- Implements different interaction modes (drag mode, delete mode)
- Provides visual feedback for the active mode through button styling
- Updates cursor styles to reflect the current interaction mode
- Handles mode transitions when users switch between different operations

### Palette Management
- Populates the character palette with Unicode emoji characters organized by category
- Creates the shape palette with buttons for different geometric shapes
- Implements selection logic for characters and shapes
- Handles visibility toggling for different palette sections

### File Explorer Integration
- Manages the workspace file explorer visibility and population
- Implements the canvas file explorer showing files currently on the canvas
- Creates file tree items with appropriate icons and metadata
- Provides interactive elements to locate files on the canvas

### Event Handlers
- Processes button clicks for saving, resetting, and mode switching
- Handles palette item selection and deselection
- Manages sidebar expansion and collapse
- Coordinates with the canvas to highlight selected elements

This module forms the interactive control layer of the Monster Canvas extension, providing users with intuitive access to the application's features through a well-organized sidebar interface with palettes, buttons, and file explorers.
