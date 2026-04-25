# Migration Plan: Vitest to Mocha + Puppeteer for E2E Tests

## 1. Rationale

Persistent issues with Vitest failing to execute test files after `globalSetup` completion, despite extensive debugging, necessitate a move to a more stable and well-understood E2E testing stack. Mocha, Chai, and direct Puppeteer integration offer a robust alternative.

## 2. New Dependencies

Install the following dependencies:

```bash
npm install --save-dev mocha chai puppeteer
npm install --save-dev @types/mocha @types/chai
# Consider cross-env if not already used for setting NODE_ENV
# npm install --save-dev cross-env
```

Ensure Puppeteer version is compatible with your needs (current is ~24.x).

## 3. Directory Structure

Maintain a similar structure for clarity:

-   `client/svelte-app/test-setup-mocha/` (for Mocha-specific setup files)
    -   `globalHooks.js` (or `mocha.global.js` - for global hooks)
    -   `testHooks.js` (for `beforeEach`, `afterEach` page setup)
-   `test/client/e2e-mocha/` (for new Mocha spec files)

## 4. Setup/Teardown Logic Migration

### 4.1. Global Setup (Backend, Frontend, Puppeteer Browser)

-   The logic currently in `client/svelte-app/test-setup/globalSetup.js` (starting backend, frontend dev server, and Puppeteer browser instance) needs to be adapted.
-   Mocha supports global setup via programmatic usage or root-level hooks. A common approach is to have a dedicated setup file specified with Mocha's `--file` option or in `.mocharc.js`.
-   This global setup file can export `mochaHooks` which can define `beforeAll` and `afterAll` root hooks.
    -   `beforeAll`: Start backend, frontend, Puppeteer browser. Store `browser.wsEndpoint()` and the Vite dev server port (e.g., as environment variables or in a global object).
    -   `afterAll`: Close backend, frontend, Puppeteer browser.

**Example `client/svelte-app/test-setup-mocha/globalHooks.js`:**

```javascript
// client/svelte-app/test-setup-mocha/globalHooks.js
const { startBackendServer, stopBackendServer } = require('./backendManager'); // Adapt from globalSetup.js
const { startFrontendServer, stopFrontendServer } = require('./frontendManager'); // Adapt from globalSetup.js
const puppeteer = require('puppeteer');

let browser;
let backendProcess;
let frontendDevServer;

exports.mochaHooks = {
  async beforeAll() {
    console.log('MOCHA GLOBAL: Starting all services...');
    // Start Backend
    backendProcess = await startBackendServer(); // Needs to return the process
    process.env.BACKEND_READY = 'true'; // Or use a file flag

    // Start Frontend
    frontendDevServer = await startFrontendServer(); // Needs to return the server instance
    process.env.VITE_DEV_SERVER_PORT = frontendDevServer.port; // Assuming it has a port property

    // Start Puppeteer
    browser = await puppeteer.launch({
      headless: process.env.CI ? true : 'new', // Or your preferred config
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    process.env.PUPPETEER_WS_ENDPOINT = browser.wsEndpoint();
    console.log('MOCHA GLOBAL: All services started.');
  },
  async afterAll() {
    console.log('MOCHA GLOBAL: Stopping all services...');
    if (browser) await browser.close();
    if (frontendDevServer) await stopFrontendServer(frontendDevServer);
    if (backendProcess) await stopBackendServer(backendProcess);
    console.log('MOCHA GLOBAL: All services stopped.');
  }
};
```

### 4.2. Per-Test Setup (Puppeteer Page)

-   The logic in `client/svelte-app/test-setup/vitest.setup.js` (connecting to browser, creating new page, providing `goto` utility) will be handled by Mocha's `beforeEach` and `afterEach` hooks. These can be defined in a common file required by Mocha (e.g., via `--file`) or at the top of each spec file/suite.
-   Store `page` and `browser` (connected instance) on Mocha's `this` context within hooks and tests.

**Example `client/svelte-app/test-setup-mocha/testHooks.js` (to be required by Mocha):**

```javascript
// client/svelte-app/test-setup-mocha/testHooks.js
const puppeteer = require('puppeteer');
const { beforeEach, afterEach } = require('mocha');

beforeEach(async function() {
  // `this` is Mocha's context
  if (!process.env.PUPPETEER_WS_ENDPOINT) {
    throw new Error('PUPPETEER_WS_ENDPOINT not set. Global setup might have failed.');
  }
  this.browser = await puppeteer.connect({ browserWSEndpoint: process.env.PUPPETEER_WS_ENDPOINT });
  this.page = await this.browser.newPage();
  
  const vitePort = process.env.VITE_DEV_SERVER_PORT;
  if (!vitePort) {
    throw new Error('VITE_DEV_SERVER_PORT not set.');
  }
  this.baseUrl = `http://localhost:${vitePort}`;
  this.goto = async (path, options) => {
    const url = new URL(path, this.baseUrl).toString();
    return this.page.goto(url, options);
  };
});

afterEach(async function() {
  if (this.page && !this.page.isClosed()) {
    await this.page.close();
  }
  if (this.browser) {
    await this.browser.disconnect(); // Disconnect from the browser instance per test
  }
});
```

## 5. Test File Conversion

-   **Syntax**:
    -   Replace Vitest's `describe`, `it`, `beforeAll`, `beforeEach`, `afterEach`, `afterAll` with Mocha's equivalents (they are mostly the same).
    -   Replace Vitest's `expect` with Chai's `expect` or `should`.
        ```javascript
        // Vitest: import { expect, it } from 'vitest';
        // Mocha/Chai:
        const { expect } = require('chai');
        // or: const chai = require('chai'); const expect = chai.expect;
        ```
-   **Accessing Page/Browser**:
    -   Use `this.page` and `this.goto` within `it` blocks if using the `testHooks.js` approach above. Ensure test functions are *not* arrow functions to preserve Mocha's `this` context.
        ```javascript
        it('should display the dashboard title', async function() { // Note: `function` not `=>`
          await this.goto('/');
          const h1 = await this.page.$('h1');
          const text = await this.page.evaluate(el => el.textContent, h1);
          expect(text).to.include('Ratings Dashboard');
        });
        ```

## 6. Configuration

-   Create a Mocha configuration file, e.g., `.mocharc.js` or `.mocharc.json` in the `client/svelte-app/` directory (or project root).
    ```javascript
    // .mocharc.js (example)
    module.exports = {
      require: [
        './test-setup-mocha/globalHooks.js', // For global setup/teardown of services
        './test-setup-mocha/testHooks.js'    // For per-test page setup
      ],
      spec: ['../../test/client/e2e-mocha/**/*.spec.js'], // Path from where mocha is run
      timeout: 90000, // ms
      reporter: 'spec', // Or your preferred reporter
      ui: 'bdd',
      // parallel: false, // E2E tests with shared resources often run serially
      // jobs: 1,         // If parallel is true, how many parallel jobs
      // exit: true,      // Force Mocha to exit after tests complete
    };
    ```
-   Adjust paths in `spec` and `require` based on where you run `mocha` from and where `.mocharc.js` is located.

## 7. Scripts (`package.json`)

Update or add scripts in `client/svelte-app/package.json` (or the root `package.json` if Mocha is run from there):

```json
{
  "scripts": {
    "test:e2e": "cross-env NODE_ENV=test mocha", // Assumes .mocharc.js is in CWD
    // Or more explicitly:
    // "test:e2e": "cross-env NODE_ENV=test mocha --config client/svelte-app/.mocharc.js" 
  }
}
```
Run Mocha from `client/svelte-app/` if `.mocharc.js` and setup paths are relative to it.

## 8. Environment Variables

-   `PUPPETEER_WS_ENDPOINT` and `VITE_DEV_SERVER_PORT` will be set by the new `globalHooks.js` and consumed by `testHooks.js` and potentially tests.
-   `NODE_ENV=test` should be set for test runs (e.g., via `cross-env`).

## 9. Cleanup

Once Mocha tests are stable:
-   Remove Vitest dependencies (`vitest`, `@vitest/ui`, etc.).
-   Delete `vite.config.js`'s `test` block or Vitest-specific configurations.
-   Delete old Vitest setup files (`client/svelte-app/test-setup/`).
-   Delete old Vitest spec files (`test/client/e2e/`).
-   Remove Vitest-related scripts from `package.json`.

## 10. Step-by-Step Migration Approach

1.  **Install Dependencies**: Add Mocha, Chai, and their types.
2.  **Basic Mocha Config**: Create an initial `.mocharc.js`.
3.  **Global Hooks**: Create `client/svelte-app/test-setup-mocha/globalHooks.js`. Adapt logic from the existing `globalSetup.js` to start/stop backend, frontend, and the main Puppeteer browser instance. Test this part by running Mocha with a dummy test file to see if services start and stop.
4.  **Test Hooks**: Create `client/svelte-app/test-setup-mocha/testHooks.js`. Adapt logic from `vitest.setup.js` to connect to the browser, create pages, and provide utilities like `goto`.
5.  **Convert One Test**:
    -   Copy one simple spec file (e.g., `ratings_dashboard.spec.js`) to `test/client/e2e-mocha/`.
    -   Change Vitest syntax to Mocha/Chai.
    -   Update how `page` and `goto` are accessed (e.g., `this.page`).
6.  **Run and Debug**: Run Mocha against this single test file. Debug issues in setup, hooks, and test logic.
    ```bash
    # From client/svelte-app directory
    npx mocha ../../test/client/e2e-mocha/ratings_dashboard.spec.js 
    ```
7.  **Iterate**: Refine setup and test files until the first test passes reliably.
8.  **Convert Remaining Tests**: Once the pattern is established, convert other E2E test files.
9.  **Full Test Suite Run**: Run all Mocha E2E tests.
10. **CI/CD**: Update any CI/CD pipeline configurations to use the new Mocha test command.
11. **Cleanup**: Remove old Vitest files, configurations, and dependencies.

This plan provides a structured approach to migrating your E2E tests from Vitest to Mocha + Puppeteer.

