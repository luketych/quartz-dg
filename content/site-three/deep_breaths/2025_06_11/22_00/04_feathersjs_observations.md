# FeathersJS Specific Observations

**Date:** 2025-06-11

This document notes specific behaviors and characteristics of FeathersJS encountered during this debugging process.

## 1. Handling of `$`-Prefixed Query Parameters

- FeathersJS (v5) appears to treat query parameters that start with a `$` symbol (e.g., `$limit`, `$skip`, `$sort`, `$select`) as special or reserved.
- Custom query parameters also starting with `$` (like our initial `$fetch`) are stripped from `context.params.query` before they reach service-level hooks if they are not recognized Feathers operators.
- **Resolution:** To pass custom operational flags via query parameters that should be directly accessible in `context.params.query` within hooks, avoid prefixing them with `$`. We changed `$fetch` to `perform_fetch`.

## 2. Hook Context (`context`) Object

- The `context` object is fundamental and is passed through the chain of hooks and to the service method.
- Properties can be added to `context` in one hook and read by subsequent hooks (e.g., `context.didRunConditionalFetch`). This is a standard way to pass state between hooks.
- `context.params.query` is the object representing the query from the client. It can be mutated by hooks.
  - Our `_getFlags` utility explicitly mutates `context.params.query` by deleting flag-like properties.
  - Our `conditionallyFetchAndCreateRatings` hook also mutates `context.params.query` by deleting the `perform_fetch` parameter after processing it.

## 3. Hook Execution Order

- `before` hooks run in the order they are registered for a given method.
- In our case, for `find`: `conditionallyFetchAndCreateRatings()` runs, then `findExistingRatings()`.
- If a `before` hook returns `context`, the chain continues. If it throws an error, or returns something other than `context` (like a direct result), it can short-circuit the chain.

## 4. Error Handling

- If a hook throws an error, FeathersJS typically wraps it in a FeathersError object and propagates it.
- `context.error` can be set by a hook if an error occurs. Subsequent hooks can check `context.error` to alter their behavior (e.g., skip processing).
- Our `conditionallyFetchAndCreateRatings` re-throws errors from API calls to allow Feathers to handle them and set `context.error`. `findExistingRatings` checks for `context.error` at its entry.

## 5. Service Method Execution

- After all `before` hooks have run (and none have short-circuited the process), the actual service method (e.g., the adapter's `find` method) is executed.
- This method uses the `context.params` (including the potentially modified `context.params.query`) to perform its database operation.

## 6. `_getFlags` Utility

- The custom `_getFlags(ctx, rmFlags=true)` function in `server/hooks/index.js` plays a crucial role.
- When `rmFlags` is `true`:
  - It identifies properties in `ctx.params.query` starting with `$`.
  - It removes these `$`-prefixed properties from `ctx.params.query`.
  - It also removes `ctx.params.query.flags` if present.
  - It collects all these flags (from `ctx.params.flags`, `ctx.params.query.flags`, and `$`-prefixed query params) into a new object, assigns this object to `ctx.params.flags`, and returns it.
- This means that if `ctx.params.query` initially contained *only* `$`-prefixed properties or a `flags` property, it would become an empty object `{}` after `_getFlags` runs.