# Vitest Version Standardization Report

**Date:** 2025-06-16
**Project:** ratings_api

## 1. Issue Identified

A significant discrepancy was observed in the Vitest versions being used for test execution, leading to inconsistent behavior, configuration difficulties, and failing tests. Specifically:

*   When `npx vitest run` was executed from the project root ([/Users/luketych/Dev/_endeavors/srt-playground/ratings_api/](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api:0:0-0:0)), **Vitest v3.2.3** was invoked. This version was likely a globally installed package or resolved from a `node_modules` directory outside the Svelte application's specific dependencies.
*   When `npx vitest run` was executed from the Svelte application's directory (`.../viscera/client/svelte-app/`), **Vitest v1.6.1** was invoked. This version corresponds to the `vitest: "^1.6.0"` dependency specified in `.../viscera/client/svelte-app/package.json`.

This version mismatch made it difficult to diagnose configuration issues, as the behavior of Vitest (e.g., path resolution, `globalSetup` execution, `root` directory handling) can differ between major versions.

## 2. Symptoms Observed

The version inconsistency manifested in several ways:

*   **[globalSetup.js](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/client/svelte-app/test-setup/globalSetup.js:0:0-0:0) Not Executing:** Console logs from the [globalSetup.js](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/client/svelte-app/test-setup/globalSetup.js:0:0-0:0) script were not appearing in test outputs, indicating the script wasn't being run, which prevented essential E2E setup (like Puppeteer and server initialization).
*   **"No test files found" Errors:** Despite various adjustments to `include` paths in [vite.config.js](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/node_modules/psl/vite.config.js:0:0-0:0) (relative, absolute, different base directories), Vitest often failed to locate any test files.
*   **Inconsistent Configuration Interpretation:** Attempts to use the `--config` flag to point to the nested [vite.config.js](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/node_modules/psl/vite.config.js:0:0-0:0) from the project root led to different errors (e.g., Svelte config path issues, test file discovery issues) than when running Vitest directly from the Svelte app directory.

## 3. Root Cause

The primary root cause was the `npx vitest` command resolving to different Vitest installations based on the Current Working Directory (CWD) and the `node_modules` resolution hierarchy. The Svelte app had its own local Vitest dependency (v1.6.0), while a different, newer version (v3.2.3) was accessible from the project root.

## 4. Resolution and Standardization

To ensure consistent and predictable test execution, the following standardization approach was adopted:

1.  **Acknowledge Local Dependency:** The `vitest: "^1.6.0"` dependency in `.../viscera/client/svelte-app/package.json` is considered the authoritative version for the Svelte application's tests.
2.  **Standardize Execution Context:** All Vitest commands for the Svelte app's tests should be executed from within the `.../viscera/client/svelte-app/` directory. This ensures that `npm run test` (or direct `npx vitest` calls from this directory) will always use the locally installed Vitest v1.6.x.
3.  **Configuration Alignment:** The [vite.config.js](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/node_modules/psl/vite.config.js:0:0-0:0) located in `.../viscera/client/svelte-app/` will be configured with the assumption that Vitest v1.6.x is running and that its CWD is `.../viscera/client/svelte-app/`.

This approach eliminates the ambiguity of which Vitest version is running and provides a stable baseline for further debugging of test configurations and execution. While a global Vitest (v3.2.3) might exist, project-specific testing will rely on the version pinned in the local [package.json](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/package.json:0:0-0:0).

## 5. Next Steps

With a standardized Vitest version and execution context:
*   Continue debugging the "No test files found" error under Vitest v1.6.x.
*   Verify that [globalSetup.js](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/client/svelte-app/test-setup/globalSetup.js:0:0-0:0) is correctly invoked by Vitest v1.6.x.
*   Ensure all paths in [vite.config.js](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/node_modules/psl/vite.config.js:0:0-0:0) (for `include`, `globalSetup`, `setupFiles`, etc.) are correctly resolved relative to the `viscera/client/svelte-app/` directory.
