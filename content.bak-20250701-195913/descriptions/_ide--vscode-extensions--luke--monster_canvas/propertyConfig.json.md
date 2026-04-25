# propertyConfig.json

This configuration file defines the required and optional documentation properties for code in the Monster Canvas extension. It establishes a schema for code documentation, with specified severity levels for missing properties.

The file contains two main sections:

1. **properties**: Defines the documentation properties and their requirements:
   - `masterFormula`: Required property for the core algorithm/formula of the code (error if missing)
   - `author`: Required property for code authorship (error if missing)
   - `description`: Required property describing the code's purpose (error if missing)
   - `params`: Optional property documenting function parameters (warning if missing)
   - `returns`: Optional property documenting return values (warning if missing)
   - `example`: Optional property showing usage examples (info if missing)

2. **scopes**: Defines which properties apply to different code scopes:
   - `file`: Properties required at the file level (masterFormula, author, description)
   - `function`: Properties required at the function level (masterFormula, description, params, returns, example)

This configuration is likely used by the extension to validate code documentation, provide warnings for incomplete documentation, and enforce documentation standards within projects.
