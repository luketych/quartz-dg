# drawingViewTemplate.html

This file provides the HTML template for the Drawing View feature in the Monster Canvas extension. It defines the structure and styling for the image viewer interface that allows users to view and upload images associated with files in the workspace.

## Key Components:

### Document Structure
- Complete HTML5 document with embedded CSS styles and JavaScript
- Uses VSCode theme variables for consistent styling with the editor

### UI Layout
- Header section displaying the current file name
- Main image container for displaying uploaded images
- Toolbar with buttons for image operations and view mode options
- Message area for displaying status information when no image is available

### Interactive Features
- Upload button for adding new images to files
- Open in Finder button to locate images in the file system
- Copy Path button to copy the image file path to clipboard
- View mode options for displaying images at exact size or fit to width

### JavaScript Functionality
- Bidirectional communication with the extension via the VS Code API
- Image upload handling with file selection and data transfer
- Dynamic image display with size information
- View mode switching with visual updates
- Message handling for various states (loading, no image, etc.)

This template provides a clean, functional interface for the Drawing View feature, allowing users to associate images with their files and view them within VSCode. The separation of this HTML into its own file improves code organization and maintainability.
