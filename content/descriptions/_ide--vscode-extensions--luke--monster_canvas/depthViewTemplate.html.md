# depthViewTemplate.html

This file serves as the HTML template for the Depth View feature in the Monster Canvas extension. It provides a specialized interface for exploring file and folder hierarchies with enhanced visualization options.

## Key Components:

### Document Structure
- Complete HTML5 document with embedded CSS styles and JavaScript
- Uses VSCode theme variables for consistent styling with the editor

### Header Section
- File name display with prominent styling
- File path display for context
- File details section showing metadata (type, size, creation date, modification date)

### Depth Container
- Main content area that displays files and folders in a specialized format
- Each item shows:
  - Type indicator (Folder, JS, TS, HTML, etc.)
  - File/folder name
  - Cover image area (with option to set a custom cover)
  - Stickers section (with option to add custom stickers)

### Interactive Features
- Expandable folder structure with accordion behavior
- Click handlers for files to open them in the editor
- Click handlers for folders to expand/collapse their contents
- Special handlers for cover images and stickers to customize the view
- Error message display system
- "No workspace" fallback view with browse button

### JavaScript Functionality
- Bidirectional communication with the extension via the VS Code API
- Dynamic rendering of file and folder information
- Formatting utilities for file sizes and dates
- Event handlers for user interactions
- Message processing for extension commands

This template provides a rich, interactive interface for exploring and visualizing the file structure with additional metadata and customization options, enhancing the standard file explorer experience.
