# Issue: Infinite Loop on "Fetch Ratings"

**Reported:** 2025-06-21

## 1. Problem Description

When the "Fetch Ratings" button is clicked in the frontend, the backend enters an infinite loop of requests. This continues until the `nodemon` process crashes, likely due to an out-of-memory error. The logs show repeated calls to the Benzinga API, indicating the loop is occurring within the server-side fetching logic.

## 2. Diagnostic Plan: Measure & Log

Our primary goal is to trace a single user request through the entire backend process to pinpoint where the loop begins. 

### Hypothesis

The loop is likely caused by the `conditionallyFetchAndCreateRatings` hook being re-triggered inappropriately. This could be due to one of the following:

1.  **State Management:** The `perform_fetch` query parameter is not being correctly removed after the initial fetch, causing subsequent or concurrent operations to re-initiate the entire process.
2.  **Faulty Loop Condition:** The `while` loop inside the pagination logic of `_getRatingsForDateRange` or `_fetchBenzingaRatingsByDay` has a condition that never evaluates to `false`.
3.  **Unintended Recursion:** A function is calling itself without a proper base case, leading to a stack overflow.

### Action Items:

1.  **Add Granular, Request-Specific Logging:**
    *   Introduce a unique `requestId` at the very beginning of the `conditionallyFetchAndCreateRatings` hook.
    *   Log this `requestId` at the entry and exit points of all related hooks and utility functions: `conditionallyFetchAndCreateRatings`, `_getRatingsForDateRange`, and `_fetchBenzingaRatingsByDay`.
    *   For each log entry, include the full `context.params.query` to track how it changes through the process.

2.  **Implement a "Circuit Breaker":**
    *   Introduce a depth counter or iteration limit to the main fetching loop in `_getRatingsForDateRange`.
    *   If the number of iterations exceeds a safe threshold (e.g., 100 days or 50 pages), the loop should terminate and throw a specific error. This will prevent the server from crashing and provide a clear signal that the loop was aborted.

## 3. Solution Strategy

Once the logs allow us to identify the root cause, the solution will likely involve one of the following:

*   **Fixing State Handling:** Ensure that the `perform_fetch` parameter is definitively removed from the `context` immediately after the fetch is initiated. 
*   **Correcting Loop Logic:** Adjust the `while` loop conditions to correctly handle all possible API responses, including empty data sets or unexpected formats that might be preventing the loop from terminating.
*   **Refactoring for Clarity:** If the logic proves to be too complex and prone to errors, refactor it into smaller, more predictable functions with clear responsibilities and exit conditions.

By following this structured approach, we can systematically identify the bug, implement a robust fix, and add safeguards to prevent it from happening again.
