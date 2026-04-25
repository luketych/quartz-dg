# fileDetailsTemplate.html

This file serves as the HTML template for the File Details View feature in the Monster Canvas extension. It provides a comprehensive interface for viewing and interacting with file and folder information with multiple visualization options.

## Key Components:

### Document Structure
- Complete HTML5 document with embedded CSS styles and JavaScript
- Uses VSCode theme variables for consistent styling with the editor

### Header Section
- File name display with prominent styling
- File path display for context
- File details section showing metadata (type, size, creation date, modification date)

### View Controls
- Toggle buttons for different view modes:
  - List View: Detailed rows with file information
  - Icons View: Grid of icons with file names
  - Columns View: Hierarchical column-based navigation
  - Gallery View: Visual grid with cover images
- Each view mode has specialized CSS styling and layout

### Content Display
- Flexible container that adapts based on the selected view mode
- Support for displaying file hierarchies with expandable folders
- Special handling for code file comments
- Cover image and sticker support for visual customization

### Interactive Features
- Click handlers for files to open them in the editor
- Click handlers for folders to expand/collapse their contents
- Special handlers for cover images and stickers to customize the view
- View mode persistence through extension storage
- Error message display system
- "No workspace" fallback view with browse button

### JavaScript Functionality
- Bidirectional communication with the extension via the VS Code API
- Dynamic rendering of file and folder information
- Formatting utilities for file sizes and dates
- View mode switching with UI updates
- Event handlers for user interactions
- Message processing for extension commands

This template provides a feature-rich interface for exploring and interacting with files and folders, with multiple visualization options and customization capabilities that enhance the standard file explorer experience.
