# 🧪 Vitest Hanging After E2E Tests — Vite Dev Server Teardown Leak

**Date:** June 17, 2025  
**Environment:** Vitest + Vite + FeathersJS + Puppeteer + macOS

---

## ⚙️ High-Level Overview

Vitest fails to exit cleanly after end-to-end tests, hanging until it hits its internal timeout. Investigation shows that the Vite dev server—started programmatically via `createServer()`—does not fully release system resources, particularly file handles in `rollup/dist/native.js`. This leak persists despite manual teardown logic completing successfully for the FeathersJS API and Puppeteer.

The problem appears to stem from Vite or Rollup not fully cleaning up native watchers or other internals, even after calling `.close()` and `.ws.close()`.

---

## 🧩 Root Problem

- Vitest hangs after tests complete, despite teardown finishing.
- Hanging-process reporter points to retained `FILEHANDLE`s in `rollup/dist/native.js`.
- Manual calls to `viteDevServer.ws.close()` and `viteDevServer.close()` do not fully release resources.
- Adding `process.exit(0)` at the end of `globalSetup.js` resolves the hang—but only by forcefully exiting.

---

## 🔍 Troubleshooting Summary

### ✅ Working

- **FeathersJS Teardown:** Uses SIGTERM + fallback SIGKILL; shuts down reliably now.
- **Puppeteer Close:** Completes without issue.
- **`hanging-process` Reporter:** Identified lingering handles in `rollup/dist/native.js`.
- **`viteDevServer.ws.close()` + `viteDevServer.close()`:** Executed manually, improves shutdown clarity.
- **Temporary `process.exit(0)`:** Confirms problem is after user teardown logic.

### ❌ Not Working

- `execa.terminate()` failed to cleanly stop Feathers in SSR/Vitest.
- Setting `server.watch: null` or `server.hmr: false` didn’t prevent the hang.
- Using `configFile: false` caused new errors and still leaked handles.
- Re-enabling default Vite options had no positive effect.

---

## 🧭 Current Status

Despite proper teardown in test code, **Vite's internal watchers or Rollup’s native bindings** appear to retain file handles after `close()`, especially on macOS. The issue likely resides in:

- Vite’s interaction with Rollup (native watchers)
- Incomplete cleanup when Vite is run programmatically (via `createServer()`)

---

## ✅ Recommended Next Steps (Prioritized)

### 1. 🧪 Create a Minimal Reproduction Script

**Why:** To confirm whether the leak is in Vite itself or tied to Vitest’s test harness.

**How:**

```js
import { createServer } from 'vite';

const server = await createServer({ root: '.', logLevel: 'silent' });
await server.listen();

// Optional: wait 2s, then cleanup
setTimeout(async () => {
  await server.ws?.close?.();
  await server.close();
}, 2000);

process.on('beforeExit', () => {
  console.log('Process beforeExit - did it hang?');
});
```

> ✅ Run this standalone. If it hangs, the issue is with Vite or Node, not Vitest.

---

### 2. 🔍 Search Vite/Rollup GitHub Issues

Check for open or closed issues mentioning:

- `hanging`, `teardown`, `process exit`
- `rollup/dist/native.js`, `file handle leak`, `createServer close`

Look especially for:

- OS-specific bugs (e.g., macOS file watcher behavior)
- Regressions or fixes in recent Rollup/Vite releases

---

### 3. 🧪 Test Different Node.js Versions

Native module behavior (especially file system watchers) can vary.

- Try latest **Node.js LTS**
- Try **previous LTS**
- Use `nvm` to quickly switch

---

### 4. 📦 Audit and Update Dependencies

Ensure these are on the latest compatible versions:

- `vite`, `rollup`, `vitest`, `svelte`
- Any plugins related to dev servers or HMR

Also:

- Clear `node_modules` and reinstall
- Check for peer dependency warnings

---

### 5. 🔍 Re-check Teardown Config

Double-check async teardown logic:

- Are all `await server.close()` and `await ws.close()` used properly?
- Is anything still running in the background (like file listeners or sockets)?
- Is Vitest’s `forceExit` disabled (which could hide real leaks)?
- Review `vitest.config.js` and shared `vite.config.js` for:
  - `pool`, `poolOptions`
  - HMR/watch overrides
  - Plugins that may extend the dev server

---

### 6. 🛑 Use `process.exit(0)` as a Temporary Fallback

If this is blocking workflow, you can add `process.exit(0)` at the end of teardown—but clearly mark it as a **temporary measure**.

```js
// FIXME: Forcibly exit due to Vite server hang
process.exit(0);
```

> 🛠️ Don't rely on this permanently—it masks real teardown bugs.

---

## 🧠 Final Thoughts

All signs point to **an internal resource cleanup issue in Vite/Rollup**, likely tied to native watchers not shutting down completely. Since Vitest teardown runs cleanly, the next best move is a minimal script outside the test context to isolate whether Vite alone is at fault.

Once confirmed, this could be upstreamed as a bug report or issue with a reproducible test case.

---

Would you like help drafting that reproduction script as a GitHub issue or test case template?
