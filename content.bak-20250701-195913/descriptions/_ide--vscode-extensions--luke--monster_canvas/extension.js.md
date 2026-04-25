# extension.js

The primary entry point for the Monster Canvas VSCode extension. This file is responsible for:

1. Activating the extension and initializing all providers
2. Creating necessary cache directories for storing images and other data
3. Registering all tree view and webview providers
4. Setting up command handlers for the extension
5. Managing the interaction between different views and components

Key components initialized:
- FileExplorerProvider: Provides the sidebar tree view of files
- DrawingViewProvider: Handles the canvas for viewing and drawing on images
- FileDetailsViewProvider: Shows detailed information about files and directories
- DepthViewProvider: Provides a depth/hierarchy view of file structures

The file also sets up event listeners to synchronize the different views, ensuring that when a user selects a file in the explorer, all views are updated accordingly.
