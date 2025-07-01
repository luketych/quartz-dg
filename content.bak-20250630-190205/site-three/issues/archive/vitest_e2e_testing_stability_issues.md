Vitest E2E Testing Environment Stability Plan

Purpose

This document outlines the issues we’re facing with the Vitest end-to-end (E2E) testing environment and provides a comprehensive plan for resolving them. The goal is to ensure that our E2E tests run reliably and consistently by addressing global setup, server initialization, port management, and test execution issues.

High-Level Overview of Issues

Our E2E tests are currently unstable due to:
	1.	Global Variable Access: Tests cannot reliably access globals set in globalSetup.
	2.	Undefined Vite Dev Server Port: Dynamic ports sometimes aren’t resolved or passed correctly.
	3.	Incorrect Server Initialization: Backend server doesn’t always launch as expected.
	4.	Hanging Tests: Tests stall waiting for services that haven’t started or can’t be reached.
	5.	Incompatible Vitest Versions: Upgrades or mismatches between v1.x and v3.x cause inconsistencies.

What We’ve Tried So Far

Attempted Fixes
	1.	Global Setup Rewrite
	•	Replaced minimal setup with a comprehensive launcher.
	•	Sequential backend → frontend → Puppeteer boot process.
	•	Port cleanup and async control.
	2.	Backend Initialization
	•	Standalone script to load app.js and call setupApp().
	•	ES module compatibility fixes.
	3.	Frontend Server Adjustments
	•	Vite dev server port fix attempts.
	•	Excluded client deps from optimization.
	•	Updated path/alias resolution.
	4.	Environment Variable Handling
	•	Used process.env, global, globalThis, and return values from setup.
	5.	Dependency Standardization
	•	Unified to Vitest 3.2.3.
	•	Updated related plugins.

Theories and Hypotheses
	1.	Global Variable Inconsistency
	•	Different Vitest versions treat globalSetup return values and globalThis differently.
	2.	Vite Port Handling
	•	Dynamic allocation is unstable; needs to be explicitly defined.
	3.	Startup Race Conditions
	•	Startup isn’t fully awaited; services are half-available when tests start.
	4.	Test Discovery Problems
	•	Misconfigured include/exclude patterns in config.
	5.	Puppeteer Timeout Issues
	•	Connections can hang indefinitely without error reporting.

Solution Strategy

1. Diagnostic Phase
	• [x] Add minimal test to log available globals:

import { test } from 'vitest';
test('debug', () => {
  console.log('GLOBALS:', Object.keys(global));
  console.log('ENV:', process.env);
});


	• [x] Run with:

DEBUG=vitest:* npx vitest run debug-test.js --no-threads


	•	Add timing metrics to globalSetup.js:

const time = (label) => {
  const start = Date.now();
  return () => console.log(`${label}: ${Date.now() - start}ms`);
};



2. Global Setup Fixes
	•	Rewrite globalSetup.js:
	•	Log timing and lifecycle events.
	•	Use fixed port (5173) with fallback via get-port.
	•	Set globals via:
	•	global[key]
	•	globalThis[key]
	•	process.env[key]
	•	return object { PUPPETEER_WS_ENDPOINT: ... }
	•	Add error handling + timeouts to Puppeteer connection logic.

3. Backend and Frontend Startup
	•	Use async function for setupApp() from app.js.
	•	Validate port binding and listening manually.
	•	Start Vite server with defined port and no auto-open.

4. Test File Revisions
	• [x] Add access fallback utility:

// test/utils/globals.js
export const getGlobal = (key) =>
  globalThis?.[key] ?? global?.[key] ?? process.env?.[key];


	•	Update all tests to:
	•	Use timeouts on async ops.
	•	Use getGlobal().
	•	Log major checkpoints.

5. Vitest Config Updates
	•	Use clear file match patterns:

test: {
  include: ["test/**/*.e2e.test.js"],
  globals: true,
  testTimeout: 30000,
  environment: 'node',
}


	•	Add/verify vitest.setup.js.

6. Implementation Plan

Stage 1: Global Setup
	• [x] Fix startup sequence and global propagation.

Stage 2: Test File Refactor
	•	Rewrite tests to use fallback global strategy and log connection attempts.

Stage 3: Configuration Cleanup
	•	Standardize Vitest config, file paths, and port logic.

Stage 4: Incremental Validation
	•	Run one test at a time.
	•	Confirm Puppeteer connection and console logs.

Stage 5: CI Compatibility
	•	Add support for headless, fixed-port CI.
	•	Validate behavior using --no-threads.

Expected Outcomes
	•	Global variables accessible in every test context.
	•	Backend and frontend servers launch reliably.
	•	Puppeteer consistently connects.
	•	E2E tests either pass or fail quickly with actionable logs.
	•	CI and local environments behave identically.

Optional Enhancements
	•	test:debug script in package.json
	•	Fail-fast E2E reporter or summary output
	•	Parallel vs serial test toggling
	•	Health check endpoint on backend to avoid fixed delays

⸻

This document is the living source of truth for fixing Vitest E2E reliability. Updates to tooling, test setup, or startup scripts should be reflected here.