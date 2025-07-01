# storage.js

This utility file provides functions for managing data persistence within the Monster Canvas extension. It handles saving and loading data to/from the extension's global state storage, ensuring that user-created content persists between VSCode sessions. The file includes the following functions:

1. **loadCharacterData**: Retrieves saved character (emoji) data from the extension's storage. If no saved data exists, it returns the provided default data.

2. **loadShapeData**: Retrieves saved shape data from the extension's storage. If no saved data exists, it returns the provided default shapes.

3. **saveCharacterData**: Persists character data to the extension's global state and optionally displays a notification to the user.

4. **saveShapeData**: Persists shape data to the extension's global state and optionally displays a notification to the user.

5. **resetShapes**: Reverts the saved shapes back to their default values, updating the storage and notifying the user.

6. **resetCharacterPositions**: Reverts the saved character positions back to their default values, updating the storage and notifying the user.

All functions are designed to work with the VSCode extension context's globalState API for persistent storage. The module supports the canvas drawing functionality by ensuring that user-created or modified visual elements (characters and shapes) are preserved across sessions.
