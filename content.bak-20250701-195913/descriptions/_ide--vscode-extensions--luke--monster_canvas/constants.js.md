# constants.js

This file defines a set of constant values and default data used throughout the Monster Canvas extension. It includes:

1. **defaultCharacterData**: An array of preset characters (emojis) with their positions, sizes, and colors that are used as default content for the drawing canvas if no saved data exists. Each character has:
   - Unique ID
   - Unicode character (emoji)
   - Position (x, y coordinates)
   - Size
   - Color (in hex format)

2. **defaultShapes**: An array of preset geometric shapes with their properties, used as default content for the drawing canvas if no saved data exists. Each shape includes:
   - Unique ID
   - Type (circle, square, triangle)
   - Position (x, y coordinates)
   - Dimensions (width, height)
   - Color (in hex format)

3. **shapeTypes**: A list of available geometric shape types that users can select when creating shapes on the canvas.

4. **unicodeCharacters**: A categorized collection of Unicode characters (primarily emojis) organized into themed groups that users can select from:
   - monsters: Fantasy creatures and monster-like characters
   - animals: Various animal emojis across different species
   - fantasy: Mythical and fantasy-themed character emojis
   - faces: Facial expressions and emotion emojis
   - symbols: Various symbolic and decorative characters

These constants provide the default visual elements and character options available in the drawing canvas, giving users a starting point for creating visual content.
