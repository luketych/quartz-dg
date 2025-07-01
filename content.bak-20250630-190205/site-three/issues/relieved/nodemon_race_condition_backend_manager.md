# Report: Resolving EADDRINUSE Race Condition in Development Environment

## 1. Executive Summary

This report details a persistent `EADDRINUSE` (Error: Address Already in Use) issue that occurred when running the backend server (`dev:server`) concurrently with the Svelte client development server (`dev:client:svelte`), particularly when initiated via VS Code's `launch.json` compound configurations. The root cause was a race condition involving `nodemon` (managing the backend server) restarting due to client-side file changes, and the client-side test setup (`backendManager.js`) attempting to launch its own backend instance.

The solution involved two main strategies:
1.  Modifying `backendManager.js` to detect and use an existing backend server instance.
2.  Refining `nodemon`'s configuration (`nodemon.json`) to strictly limit its watched files and ignore client-side activity, preventing unnecessary restarts.

These changes have stabilized the development environment, allowing both server and client development processes to run concurrently without port conflicts.

## 2. Problem Description

Developers encountered frequent `EADDRINUSE` errors on the designated backend port (initially 4500, later changed to 4501 for testing) when:
*   Starting the `dev:server` (backend) and `dev:client:svelte` (client) scripts in close succession.
*   Using VS Code `launch.json` configurations designed to run both processes as a compound task.

The primary symptom was the backend server crashing shortly after startup or when the client server was initiated, with logs indicating the port was already in use. This significantly hindered development workflow.

## 3. Analysis of Contributing Factors & Race Condition

The `EADDRINUSE` error stemmed from multiple processes attempting to bind to the same port, driven by the following interacting factors:

*   **`nodemon` Restarts**: The main backend server, launched via `npm run dev:server`, uses `nodemon` to monitor file changes and automatically restart. Initially, `nodemon` was configured to watch a broad set of files across the project.
*   **Client-Side File Activity**: When `npm run dev:client:svelte` was executed:
    *   The Vite build process and Svelte dev server would create/modify files (e.g., build artifacts in `dist/`, cache files in `.vite/`).
    *   The client-side Mocha test setup script, `viscera/client/svelte-app/test-setup-mocha/backendManager.js`, was sometimes triggered. This script, designed for test environments, would attempt to manage a backend server instance, including creating a `.backend.ready` file.
*   **Race Condition - `nodemon` vs. Port Release**: If any client-side file activity (including `.backend.ready` creation) triggered `nodemon` to restart the main backend server *before* the previous instance had fully shut down and released the port, the new instance would fail with `EADDRINUSE`.
*   **`backendManager.js` Behavior**: Independently, `backendManager.js` itself was designed to start a backend server. If a main backend server was already running (manually or via `dev:server`), `backendManager.js` would attempt to start another one on the same port, leading to a direct `EADDRINUSE` conflict.
*   **VS Code `launch.json`**: Launching both server and client via a compound `launch.json` configuration in VS Code exacerbated the issue by starting both processes almost simultaneously, maximizing the probability of these race conditions occurring.

## 4. Solution Implementation

Addressing the issue required a multi-pronged approach:

### 4.1. Modifying `backendManager.js`

The script `viscera/client/svelte-app/test-setup-mocha/backendManager.js` was updated to prevent it from starting a duplicate server:
*   **`isPortInUse` Function**: An asynchronous function `isPortInUse(port)` was added, utilizing `lsof -i :<port> -t -sTCP:LISTEN` to check if the target backend port was already occupied.
*   **Conditional Server Start**: The `startBackendServer` function within `backendManager.js` was modified to first call `isPortInUse`. 
    *   If the port is found to be in use, `backendManager.js` now logs this, ensures the `.backend.ready` file is created (to satisfy any polling logic expecting it), and then resolves its promise, effectively using the existing server instance instead of trying to start a new one.
    *   If the port is free, it proceeds with its original logic of starting a managed server instance (primarily for isolated test runs).

### 4.2. Refining `nodemon` Configuration

To prevent `nodemon` from restarting the main backend server due to irrelevant client-side file changes, its configuration was made more robust:
*   **Initial Attempts**: Inline `--ignore` flags in the `package.json` script for `dev:server` were tried but proved inconsistent in how they were applied by `nodemon` through `npm`.
*   **`nodemon.json` Implementation**: A dedicated `viscera/nodemon.json` file was created to serve as the single source of truth for `nodemon`'s configuration. This file includes:
    *   `"verbose": true`: Enables detailed logging from `nodemon`, indicating the specific file(s) or reason for any restart, aiding in debugging.
    *   **Comprehensive `ignore` List**: An extensive list of patterns to ignore was added, including:
        *   Standard ignores: `.git`, `node_modules/**/node_modules`
        *   Test and coverage outputs: `test/**`, `coverage/**`, `.nyc_output/**`
        *   Log files: `logs/**`, `*.log`
        *   OS-specific files: `.DS_Store`
        *   Client-side directories and artifacts: `client/`, `client/**/*`, and more specific paths like `viscera/client/svelte-app/dist/*`, `viscera/client/svelte-app/.vite/*`.
        *   The `.backend.ready` file, to prevent its creation/modification by `backendManager.js` from triggering restarts.
    *   **Explicit `watch` Directories**: Crucially, a `"watch": ["server/", "config/"]` directive was added. This explicitly tells `nodemon` to *only* monitor changes within the `server/` and `config/` directories. This is a more effective strategy than relying solely on ignore patterns, as it defines a positive set of paths that *should* trigger a backend restart.
    *   `"ext": "js,mjs,json,yaml,ts"`: Specifies the file extensions `nodemon` should monitor within the watched directories.

## 5. Outcome & Verification

After implementing these changes:
*   The main backend server, managed by `nodemon` via `npm run dev:server`, no longer restarts due to file system changes originating from the client-side development server or its associated scripts.
*   The `backendManager.js` script correctly detects if a backend server is already running on the designated port and refrains from starting a duplicate instance.
*   Running `npm run dev:server` and `npm run dev:client:svelte` concurrently (either manually in sequence or via VS Code's `launch.json`) now works reliably without `EADDRINUSE` errors.
*   The development environment is stable, allowing developers to focus on feature development rather than wrestling with port conflicts.

This resolution ensures a smoother and more predictable development experience.
