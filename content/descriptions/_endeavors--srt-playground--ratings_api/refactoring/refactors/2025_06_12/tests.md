# Refactoring Test Strategy

To ensure the refactoring process is successful and does not introduce regressions, we will use a combination of existing end-to-end (E2E) tests and new, focused unit tests.

### Guiding Principles

1.  **Test Before You Change:** Always ensure the current test suite is passing before starting a refactoring step.
2.  **Test After You Change:** After every significant file move, rename, or structural change, run the full E2E test suite. A passing suite is the green light to proceed.
3.  **Create Unit Tests for Utilities:** As functions are moved into isolated files (especially within `hooks/utilFunctions/`), create corresponding unit tests for them. This verifies their logic independently and makes future changes safer.

---

### Phase-by-Phase Testing Plan

#### Pre-Refactor

*   Run `npm run mocha` and confirm all 12 tests are passing.

#### During Phase 1 (Restructuring)

*   **After each major file move (steps 1-4):** Run the full E2E test suite (`npm run mocha`).
*   **Goal:** The tests will fail due to incorrect import paths. The objective is to fix all import statements until the entire suite passes again. This validates that the new structure is correctly wired.

#### During Phase 2 (Consolidating Hooks)

*   **As you move utility functions:** Create new unit test files for them.
    *   `test/hooks/util/generateHash.test.js`
    *   `test/hooks/util/getFlags.test.js`
    *   `test/hooks/util/setHardFlags.test.js`
    *   etc.
*   **After moving a function:** Run its new unit test *and* the full E2E test suite.
*   **Goal:** This ensures the function works in isolation and that its integration into the application remains correct.

#### During Phase 3 (Refinements)

*   **After renaming functions:** Run the full E2E test suite to catch any places where the old name was still being used.
*   **After deleting [isQueryEmpty()](cci:1://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/services/ratings/hooks.js:151:0-156:1):** Run the full E2E test suite to confirm it had no undiscovered dependencies.

---

This systematic approach will help us catch errors early and refactor with confidence.