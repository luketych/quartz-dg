# Key Hooks and Intended Flow for `ratings` Service `find` Method

**Date:** 2025-06-12

## Overview

The `find` method of the `ratings` service has a `before` hook chain designed to implement conditional data fetching and creation, followed by querying existing data. The two primary custom hooks involved are:
1.  `conditionallyFetchAndCreateRatings()`
2.  `findExistingRatings()`

They are registered in `viscera/server/services/ratings/hooks.js` as follows:
```javascript
// ...
  before: {
    // ...
    find: [ conditionallyFetchAndCreateRatings(), findExistingRatings() ],
    // ...
  },
// ...
```

## 1. `conditionallyFetchAndCreateRatings` (conditionallyFetchAndCreateRatings)

*   **Purpose:** To fetch new ratings data from an external API (Benzinga) and create them in the local database, but only if specific conditions are met.
*   **Trigger Condition:** Runs its main fetching logic if `context.params.query.perform_fetch === 'true'`.
*   **Key Actions if Triggered:**
    *   Sets `context.didRunConditionalFetch = true`.
    *   Calls the `fetchRatings` hook (an external utility) to get data from Benzinga.
    *   Processes the fetched data, checks for existing entries by hash to prevent duplicates.
    *   Creates new, non-duplicate ratings in the database via `context.service.create()`.
    *   Removes the `perform_fetch` parameter from `context.params.query` to prevent it from interfering with subsequent database queries or the `findExistingRatings` hook's interpretation of the query.
*   **If Not Triggered:**
    *   `context.didRunConditionalFetch` remains `false` (its initialized value).
    *   The hook does minimal work and passes the context to the next hook.

## 2. `findExistingRatings` (FER)

*   **Purpose:** To query the local database for existing ratings based on the client's query parameters, after potentially being modified by conditionallyFetchAndCreateRatings and after internal flag processing.
*   **Coordination with conditionallyFetchAndCreateRatings:**
    *   Checks `context.didRunConditionalFetch` at its entry.
    *   If `context.didRunConditionalFetch === true`, this hook is expected to **skip its main logic entirely**. The assumption is that conditionallyFetchAndCreateRatings has handled data fetching/creation, and the original service method (after all `before` hooks) will use the (potentially modified by conditionallyFetchAndCreateRatings) query to retrieve all relevant records (newly created and pre-existing).
*   **Main Logic (if `didRunConditionalFetch` is `false`):
    *   Calls `_getFlags(context, true)`: This utility function extracts special parameters (like `$limit`, `$skip`, and any other `$`-prefixed params) from `context.params.query`. Critically, `_getFlags` with `rmFlags=true` **modifies `context.params.query` by removing these extracted flags**.
    *   Checks if `context.params.query` is empty after `_getFlags` has processed it using `isQueryEmpty()`.
    *   **If the query is now empty, it throws the `Error: Empty query.`** This is the error currently plaguing the tests.
    *   If the query is not empty, it allows the original service method to proceed with this (now cleaned) query to fetch data from the database.
    *   It also contains logic for `SEND_MOCK_RATINGS` which is not active during tests.

## Intended Flow Summary

1.  Client calls `app.service('ratings').find({ query: { ...params... } })`.
2.  `conditionallyFetchAndCreateRatings` runs:
    *   If `query.perform_fetch === 'true'`: Fetches, creates, sets `didRunConditionalFetch = true`, removes `perform_fetch` from query.
    *   Else: `didRunConditionalFetch = false`, query is largely untouched.
3.  `findExistingRatings` runs:
    *   If `didRunConditionalFetch === true`: Skips all further logic in this hook.
    *   Else (`didRunConditionalFetch === false`): Processes `query` with `_getFlags`. If `query` becomes empty, throws error. Otherwise, allows flow to continue.
4.  The actual Feathers service `find` method executes using the `context.params.query` as it stands after these hooks. This query is then translated by the adapter (e.g., Sequelize) into a database query.
