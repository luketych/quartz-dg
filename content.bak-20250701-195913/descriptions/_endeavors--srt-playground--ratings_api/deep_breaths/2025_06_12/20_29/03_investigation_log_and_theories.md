# Investigation Log and Theories

**Date:** 2025-06-12

This document tracks the debugging steps and evolving theories regarding the `"Empty query."` error.

---

## Initial State & Problem

- Multiple tests in `ratings.test.js` fail with `"Empty query."` from the `findExistingRatings` (FER) hook.
- `conditionallyFetchAndCreateRatings` (conditionallyFetchAndCreateRatings) runs **before** `findExistingRatings`.
- conditionallyFetchAndCreateRatings uses `context.didRunConditionalFetch` to signal FER to skip its main logic.

---

## Phase 1: Understanding `$fetch` and Context Propagation

- **Observation:** `$fetch: 'true'` parameter in test queries was disappearing before reaching conditionallyFetchAndCreateRatings.

- **Theory 1:** A hook between the client call and conditionallyFetchAndCreateRatings was stripping `$fetch`.
  - **Investigation:** Checked `ratings/hooks.js`. No such hook found.

- **Theory 2:** FeathersJS itself treats `$`-prefixed query params specially and removes them.
  - **Investigation:** Logged `context.params` in conditionallyFetchAndCreateRatings. Confirmed `$fetch` was missing from `context.params.query` upon entry to the hook.
  - **Action:** Renamed `$fetch` to `perform_fetch` (no `$` prefix).
  - **Result:** 
    - `perform_fetch` now correctly reaches conditionallyFetchAndCreateRatings.
    - conditionallyFetchAndCreateRatings's logic for `perform_fetch: 'true'` executes:
      - Sets `didRunConditionalFetch = true`
      - Removes `perform_fetch` from the query
    - FER logs show it *skipping* its main logic when `didRunConditionalFetch` is true.

- **Problem Persists:** `"Empty query."` error still occurs in the same tests.

---

## Phase 2: The Contradiction and `_getFlags`

- **Contradiction:** If FER skips its main logic (where the error is thrown) for `perform_fetch: 'true'` tests, why do these tests still show the error originating from that exact line in FER?

- **Theory 3:** 

  - The error is not from the *initial* `find` call (with `perform_fetch: 'true'`) in the tests, but from *subsequent* `find` calls within the same test methods.
  - These subsequent calls are often used to verify results, count totals, or check for duplicates, and might use queries like `{ $limit: 0 }` or `{}`.

- **Investigation (`_getFlags` from `server/hooks/index.js`):**

  - `_getFlags(ctx, true)` is called by FER (when `didRunConditionalFetch` is false).
  - This function **mutates** `ctx.params.query` by removing:
    - Any property starting with `$` (e.g., `$limit`, `$skip`)
    - The `flags` property itself (`ctx.params.query.flags`)
  - `perform_fetch` (no `$`) is *not* removed by this function.

- **Hypothesis:** If a test includes:

  ```js
  app.service('ratings').find({ query: { $limit: 0 } })
  ```

  Then the flow is:

  1. conditionallyFetchAndCreateRatings runs. `perform_fetch` is undefined → `didRunConditionalFetch = false`.
  2. FER runs its main logic.
  3. `_getFlags(context, true)` removes `$limit`, making `ctx.params.query = {}`.
  4. `isQueryEmpty(ctx.params.query)` returns `true`.
  5. FER throws `Error: Empty query.`.

- **Supporting Evidence:**

  - Stack trace consistently points to `throw new Error('Empty query.')` inside FER.
  - Logs for `perform_fetch: 'true'` show FER skipping its main logic.
  - Strongly suggests another call path is hitting the error.

---

## Current Leading Theory

The `"Empty query."` errors are primarily caused by **subsequent `find` calls** within the tests (e.g., `find({ query: { $limit: 0 } })` or `find({ query: {} })`) where `_getFlags` correctly strips all parameters, leaving an empty query object that `findExistingRatings` then rejects.

The initial `perform_fetch` calls seem to be handled correctly by the hook logic, with FER skipping its main processing as intended.
