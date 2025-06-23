# Feature Implementation Proposal

**Date:** 2025-06-12

The new features primarily focus on enhancing the frontend capabilities for fetching, displaying, and organizing ratings data. We'll need to make changes to both the frontend UI and potentially the backend API to support these features.

**Assumptions:**
*   The project uses a FeathersJS backend and will be implementing a Svelte-based frontend.
*   Ratings data is stored in a database that the API interacts with.

---

### Proposed Implementation Plan

**Milestone 1: Backend API Enhancements**

*   **Objective:** Update API endpoints to support new querying capabilities (date ranges, sorting) and potentially a new mode for fetching data.
*   **Tasks:**
    1.  **Date Range Support:**
        *   Modify the relevant API endpoint (e.g., `/ratings`) to accept `start_date` and `end_date` query parameters.
        *   Update the database query logic to filter ratings within the specified date range.
    2.  **Sorting Support:**
        *   Modify the API endpoint to accept `sort_by` (e.g., `dtISO`, `analyst`) and `sort_order` (`asc`, `desc`) query parameters.
        *   Update database query logic to order results based on these parameters.
    3.  **"Display Ratings" (Database Only) Endpoint/Mode:**
        *   Decide on an approach:
            *   **Option A (Modify Existing Endpoint):** Add a query parameter (e.g., `source=db_only`) to the existing "Fetch and Display Ratings" endpoint to instruct it not to call the external source and only return data from the local database.
            *   **Option B (New Endpoint):** Create a new, simpler endpoint (e.g., `/ratings/local`) that only queries the local database.
        *   Implement the chosen approach.

**Milestone 2: Frontend UI Enhancements for Date Range Selection (with Svelte Setup)**

*   **Objective:** Set up Svelte and implement the UI for date range selection.
*   **Tasks:**
    1.  **Svelte Setup:** Integrate Svelte into the frontend, including necessary build tools and project structure for Svelte components.
    2.  **Date Input UI:** Add input fields (e.g., two date pickers or text inputs) for selecting start and end dates.
    3.  **UI Component:** Replace or augment the current single date picker with a date range picker component. This component should also allow selecting a single date (where start and end dates are the same).
    4.  **API Integration:** Modify the API call logic for "Fetch and Display Ratings" to pass the selected date(s) or range to the backend.

**Milestone 3: Frontend - "Display Ratings" Button & Logic**

*   **Objective:** Implement the new "Display Ratings" button.
*   **Tasks:**
    1.  **Add Button:** Add the "Display Ratings" button to the UI.
    2.  **API Call:** Wire up the button to call the appropriate backend API (from Milestone 1, Task 3) to fetch ratings only from the local database, using the currently selected date/range and other filters.
    3.  **Data Handling:** Ensure the frontend correctly processes and displays the data returned for this action.

**Milestone 4: Frontend - "All" Action Type**

*   **Objective:** Implement the "All" action type in the frontend filter.
*   **Tasks:**
    1.  **UI Update:** Add "All" as an option to the action type filter (e.g., in a dropdown menu).
    2.  **Filtering Logic:**
        *   If "All" is selected, the frontend should either omit the `action_type` filter when calling the API, or the API needs to be updated to understand "All" as a special value.
        *   Ensure this interacts correctly with other filters (date range, etc.).

**Milestone 5: Frontend - Sorting Results**

*   **Objective:** Implement UI controls for sorting the displayed ratings.
*   **Tasks:**
    1.  **UI Controls:** Add UI elements for sorting (e.g., dropdowns for sort field and order, or clickable table headers).
        *   Sortable fields: `dtISO`, `analyst`, `analystName`, `tickerSymbol`, `actionPT`, `type`, `exchange`.
    2.  **API Integration/Client-Side Logic:**
        *   **Server-Side Sorting (Recommended):** When a sort option is selected, re-fetch the data from the API with the new `sort_by` and `sort_order` parameters.
        *   **Client-Side Sorting (Alternative):** If the dataset displayed is typically small, sorting could be implemented purely on the client-side after data is fetched. However, server-side sorting is generally more robust and performant for larger datasets or paginated results.
    3.  **State Management:** Update frontend state to reflect the current sort order and re-render the data accordingly.

**Milestone 6: Testing and Refinement**

*   **Objective:** Ensure all new features work correctly and the user experience is good.
*   **Tasks:**
    1.  **Unit & Integration Tests:** Write tests for new backend API logic and frontend components/logic.
    2.  **End-to-End Testing:** Test all feature flows:
        *   Selecting single dates and date ranges.
        *   Using "Fetch and Display Ratings" and "Display Ratings" buttons.
        *   Filtering by "All" action type and other action types.
        *   Sorting results by all available fields and in both ascending/descending order.
        *   Verify interactions between different filters and sorting.
    3.  **UI/UX Review:** Review the usability and appearance of the new UI elements. Make adjustments as needed.
    4.  **Documentation:** Update any relevant user or developer documentation.

---

**Proposed Way to Implement (General Approach):**

1.  **Backend First:** Start with Milestone 1 to ensure the API can support the new frontend requirements. This provides a stable foundation for frontend development.
2.  **Iterative Frontend Development:** Tackle frontend milestones (2-5) one by one. For each feature:
    *   Implement the UI changes.
    *   Integrate with the backend API.
    *   Test thoroughly.
3.  **Continuous Testing:** Integrate testing throughout the development process (Milestone 6) rather than leaving it all to the end.
