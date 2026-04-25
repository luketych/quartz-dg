# drawingViewProvider.js

This file implements the DrawingViewProvider class which manages a webview for viewing and interacting with images associated with files in the VSCode workspace. The provider offers the following capabilities:

1. Displaying images associated with files
2. Uploading and saving new images for files
3. Managing a cache of images stored in the 'monster-cache' directory
4. Providing file management operations:
   - Opening images in the system file explorer
   - Copying image paths to clipboard

The provider uses a hash-based system to associate images with specific files in the workspace, enabling persistent storage and retrieval of these associations. When a file is selected in the explorer, the drawing view automatically checks if there's an associated image and displays it.

The implementation leverages VSCode's Webview API to create an interactive canvas interface, and uses template HTML, CSS, and JavaScript files to build the webview. It also handles cross-platform concerns for operations like opening files in the system explorer.
