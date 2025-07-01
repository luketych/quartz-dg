# Refactoring Plan: Phases and Priorities

This document outlines a prioritized plan to refactor the application, ensuring that foundational changes are made first to minimize disruption.

---

### Phase 1: Foundational Cleanup & Restructuring (Highest Priority)

These are large-scale changes that affect the entire directory structure. They should be done first to create the new foundation for the application.

1.  **Remove `tradeSignals`:** Delete the unused model, service, and any related files to simplify the codebase.
2.  **Create New Core Directories:**
    *   `viscera/util/`
    *   `viscera/server/errors/`
    *   `viscera/server/hooks/utilFunctions/`
3.  **Move Core Files & Folders:**
    *   Move `server/util.js` to `viscera/util/index.js`.
    *   Move error-related functions into `viscera/server/errors/`.
    *   Move `server/app.hooks.js` into `viscera/server/hooks/`.
    *   Move [services/ratings/hooks.js](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/services/ratings/hooks.js:0:0-0:0) to `viscera/server/hooks/ratings.hooks.js`.
4.  **Update All Import Paths:** Meticulously search the entire project and update all `import` and `require` statements to point to the new file locations.

**Checkpoint:** Run the full test suite after this phase to ensure all paths are resolved correctly.

---

### Phase 2: Consolidating Hook Logic (Medium Priority)

With the new structure in place, move individual hook and utility functions into their new homes.

5.  **Move Hook Utility Functions:**
    *   Move functions from [server/hooks/index.js](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/hooks/index.js:0:0-0:0) ([generateHash](cci:1://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/hooks/index.js:8:0-76:2), [_getFlags](cci:1://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/hooks/index.js:169:0-202:1), etc.) into individual files within `viscera/server/hooks/utilFunctions/`.
    *   Move [findExistingRatings()](cci:1://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/services/ratings/hooks.js:159:0-210:3) into this directory.
6.  **Isolate [conditionallyFetchAndCreateRatings](cci:1://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/services/ratings/hooks.js:17:0-138:2):**
    *   Move this hook and its private helpers into its own file: `viscera/server/hooks/utilFunctions/conditionallyFetchAndCreateRatings.js`.
7.  **Isolate [fetchRatings](cci:1://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/hooks/fetchRatings.js:53:0-159:1):**
    *   Move [fetchRatings.js](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/hooks/fetchRatings.js:0:0-0:0) into `viscera/server/hooks/utilFunctions/`.
8.  **Update Imports Again:** Update all necessary import paths, especially within `ratings.hooks.js`.

**Suggestion:** Create an [index.js](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/hooks/index.js:0:0-0:0) file in `server/hooks/utilFunctions/` to export all functions from that directory for cleaner imports.

---

### Phase 3: Refinements & Documentation (Lower Priority)

These are smaller, less disruptive changes that are best saved for last.

9.  **Rename Functions:**
    *   Rename [_getFlags](cci:1://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/hooks/index.js:169:0-202:1) to [getFlags](cci:1://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/hooks/index.js:169:0-202:1).
    *   Rename [_setHardFlags](cci:1://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/hooks/index.js:205:0-212:1) to [setHardFlags](cci:1://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/hooks/index.js:205:0-212:1).
    *   Rename [getDateRange](cci:1://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/hooks/fetchRatings.js:23:0-51:1) in [fetchRatings.js](cci:7://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/hooks/fetchRatings.js:0:0-0:0) to `_getDateRange`.
10. **Delete [isQueryEmpty()](cci:1://file:///Users/luketych/Dev/_endeavors/srt-playground/ratings_api/viscera/server/services/ratings/hooks.js:151:0-156:1):** This function is no longer used and can be safely removed.
11. **Write Docstrings:** Add documentation for all functions in the `utilFunctions` directory.