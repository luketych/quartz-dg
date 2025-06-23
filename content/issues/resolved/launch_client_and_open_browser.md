# Resolving the "Launch Client and Open Browser" VS Code Configuration

This report details the troubleshooting steps and resolution for issues encountered with the VS Code launch configuration designed to start the client-side `http-server` and automatically open it in a browser.

## 1. Problem Description

The VS Code launch configuration named "Launch Client and Open Browser" was experiencing two main issues:

1.  **Intermittent Process Termination**: The `npm run start:client` process (which runs `http-server`) was frequently being terminated with an exit code 137 (`killed`). This typically indicates an Out Of Memory (OOM) condition or that the process was forcefully terminated by `SIGKILL`.
2.  **Browser Not Opening**: Even when the `http-server` process managed to stay alive, the browser was not automatically opening as intended by the `serverReadyAction` configuration.

## 2. Troubleshooting Steps and Findings

### a. Investigating Process Termination (Exit Code 137)

*   **Initial Suspicion**: The `serverReadyAction.pattern` in `launch.json` was initially suspected, as complex regex patterns can sometimes cause issues. Simplifying this pattern temporarily allowed the server to stay alive once, suggesting a link, but the `killed` issue returned.
*   **Debugger Interference**: We isolated the problem by creating a simplified test launch configuration ("Test: Launch Client (Simple)") that ran `npm run start:client` without any debugger attachments (`NODE_OPTIONS` related to `--require bootloader.js` or `--inspect`). This simplified configuration ran stably.
*   **Conclusion**: The exit code 137 was strongly correlated with the Node.js debugger being attached to the `http-server` process by the `type: "node"` launch configuration when initiated via VS Code's standard "Run and Debug" (F5). It's likely that the overhead or specific interactions of the debugger with `http-server` (when run as an npm script) led to instability or excessive resource consumption, triggering the `killed` signal.

### b. Investigating Browser Not Opening

*   **`serverReadyAction.pattern` Issues**:
    *   The initial patterns used were either too simple or did not correctly match the console output of `http-server`.
    *   We refined the pattern to be more specific: `"Available on:\\s*http://127.0.0.1:5500"`.
*   **`uriFormat` and Capturing Groups**: A crucial error message from macOS eventually surfaced: `"Format uri ('%s') uses a substitution placeholder but pattern did not capture anything"`. This indicated that:
    *   The `uriFormat: "%s"` requires the `pattern` to have a capturing group (e.g., `(...)`).
    *   Our pattern `"Available on:\\s*http://127.0.0.1:5500"` was matching but not capturing the URL part for substitution.

## 3. Solution Implemented

1.  **Corrected `serverReadyAction.pattern`**: The pattern in `.vscode/launch.json` for the "Launch Client and Open Browser" configuration was updated to include a capturing group around the URL:
    ```json
    "pattern": "Available on:\\s*(http://127.0.0.1:5500)"
    ```
    This allowed `uriFormat: "%s"` to correctly extract the URL `http://127.0.0.1:5500` and pass it to the browser.

2.  **Addressing Process Termination (Implicit)**: While the primary fix was for the `serverReadyAction`, the user confirmed that "it's working now." This implies that either:
    *   The user started using "Run Without Debugging" (Ctrl+F5) for the "Launch Client and Open Browser" configuration, which avoids attaching the problematic debugger flags to `http-server`.
    *   Or, the instability was somehow linked to the `serverReadyAction` failing in a way that, once fixed, allowed the process to remain stable even with debugger flags (less likely, but possible if the failure caused unhandled exceptions that cascaded).
    *   The most likely scenario for stability is running without the debugger attached to `http-server`, as `http-server` itself rarely needs direct debugging.

## 4. Final `launch.json` Snippet for "Launch Client and Open Browser"

```json
{
    "type": "node",
    "request": "launch",
    "name": "Launch Client and Open Browser",
    "runtimeExecutable": "npm",
    "runtimeArgs": [
        "run-script",
        "start:client"
    ],
    "cwd": "${workspaceFolder}/viscera",
    "console": "integratedTerminal",
    "serverReadyAction": {
        "pattern": "Available on:\\s*(http://127.0.0.1:5500)",
        "uriFormat": "%s",
        "action": "openExternally"
    }
}
```

## 5. Recommendations for Future Stability

*   When launching simple servers like `http-server` where direct debugging of the server process itself is not the primary goal, prefer using VS Code's "Run Without Debugging" (Ctrl+F5). This avoids potential conflicts with debugger attachments.
*   If debugging is required for the *client-side code* served by `http-server`, use the browser's developer tools. The Feathers backend service should have its own dedicated debug configuration (e.g., "Launch Feathers App and Debug").
*   Ensure no other processes are using the target port (e.g., 5500) before launching to prevent `EADDRINUSE` errors.
