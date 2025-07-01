**Sprint 4: n8n Data Integration**

*   **Goal:** To reliably send the collected historical price and news data to the designated n8n webhook endpoints, enabling further processing and utilization within n8n workflows.

---

*   [ ] ## Milestone 15: Design and Implement n8n Data Sender Script
    *   **Objective:** Create a Node.js script capable of reading locally stored historical data, transforming it into the required payload format, and sending it to n8n webhooks.
    *   **Tasks:**
        1.  **Finalize Payload Structures:**
            *   Confirm JSON structure for price data (to `chart_events`).
            *   Confirm JSON structure for news data (to `influential_events`), including handling of content snippets and sentiment.
        2.  **Create Script File:**
            *   Create `viscera/scripts/sendDataToN8N.js`.
        3.  **Implement Core Logic:**
            *   Add functions to read daily price JSON files and monthly news JSON files.
            *   Implement data transformation logic for both price candles and news items.
            *   Use `axios` (or a similar HTTP client) to send `POST` requests to n8n webhook URLs.
        4.  **Add Configuration:**
            *   Allow specification of:
                *   Target ticker(s).
                *   Date range (for prices) or month range (for news).
                *   Data type to send (`price`, `news`, or `all`).
                *   Delay between individual POST requests (to manage n8n load).
        5.  **Implement Logging:**
            *   Log script progress (e.g., file being processed, number of items sent).
            *   Log successful transmissions and any errors encountered (e.g., API errors from n8n).
    *   **Verification:**
        *   The script `sendDataToN8N.js` is created with the outlined functionalities.
        *   Code review confirms logic for reading, transforming, and sending data.
        *   Configuration options are implemented.

---

*   [x] ## Milestone 16: Test n8n Data Sending - Price Data (`chart_events`)
- **Objective**: Send a sample of 5-minute intraday price data for one ticker/day to the n8n `chart_events` webhook and verify receipt and basic data integrity in n8n.
- **Key Tasks**:
    - Run `sendDataToN8N.js` with `price` type, a specific ticker (e.g., `AAPL_US`), and a specific date (e.g., `2025-03-05`).
    - Monitor the n8n `chart_events` workflow for incoming data.
    - Check that data items are received and the payload structure matches the design.
- **Acceptance Criteria**: At least one day's worth of 5-minute price data (e.g., ~79 candles for a full trading day) is successfully received by the n8n workflow, with each candle potentially triggering a separate workflow execution. Data in n8n matches sent data.
- **Status**: `[[COMPLETED]]`
- **Summary**: Successfully tested sending 5-minute intraday price data for `AAPL.US` (file: `2025-03-05.json`, 79 candles) to the n8n `chart_events` webhook (`https://auto.codis.ca/webhook/chart_events`). Each candle was sent as an individual POST request with a 50ms delay. The n8n server responded with `Status: 200` and `{"message": "Workflow was started"}` for each request. The n8n workflow for `chart_events` correctly triggered a separate execution for each of the 79 candles, and the data payload was verified as correct within n8n. This confirms the script's ability to send individual price events and n8n's ability to receive and process them as separate workflow executions.

---

*   [x] ## Milestone 17: Test n8n Data Sending - News Data (`influential_events`)
- **Objective**: Send a sample of financial news data for one ticker/month to the n8n `influential_events` webhook and verify receipt and basic data integrity in n8n.
- **Key Tasks**:
    - Run `sendDataToN8N.js` with `news` type, a specific ticker (e.g., `AAPL_US`), and a specific month (e.g., `2025-05`).
    - Monitor the n8n `influential_events` workflow for incoming data.
    - Check that data items are received and the payload structure matches the design.
- **Acceptance Criteria**: At least one month's worth of news data is successfully received by the n8n workflow, with each news item potentially triggering a separate workflow execution. Data in n8n matches sent data.
- **Status**: `[[COMPLETED]]`
- **Summary**: Successfully tested sending financial news data for `AAPL.US` (file: `2025-05.json`, 987 news items) to the n8n `influential_events` webhook (`https://auto.codis.ca/webhook/influential_events`). Each news item was sent as an individual POST request with a 100ms delay. The n8n server acknowledged each request, and the n8n workflow for `influential_events` correctly triggered a separate execution for each news item. The data payload was verified as correct within n8n. This confirms the script's ability to send individual news events and n8n's ability to receive and process them.
    *   **Tasks:**
        1.  Configure `sendDataToN8N.js` to send `AAPL.US` news data for a single month (e.g., `2025-05.json`).
        2.  Run the script.
        3.  Monitor the n8n `influential_events` workflow for incoming data.
        4.  Verify that the received data in n8n matches the structure and content of the source data and the defined payload.
        5.  Consider how news deduplication (identified in Sprint 3) will be handled – either by pre-filtering in the script or noting how n8n might manage it.
        6.  Troubleshoot and resolve any connectivity or data format issues.
    *   **Verification:**
        *   News data for the test month is successfully received and validated in the n8n `influential_events` workflow.
        *   Script logs confirm successful transmission.

---

*   [ ] ## Milestone 18: (Optional) Bulk Data Sending & Refinement
    *   **Objective:** If initial tests are successful, attempt to send a larger volume of data and refine the sending script for stability and performance.
    *   **Tasks:**
        1.  Plan a strategy for sending a larger dataset (e.g., all `AAPL.US` price data, or all news for multiple tickers).
        2.  Execute the bulk sending process, monitoring script performance and n8n instance load.
        3.  Refine `sendDataToN8N.js` based on observations (e.g., adjust default delay, improve error handling for sustained runs, implement batching if necessary).
    *   **Verification:**
        *   A larger dataset is successfully transmitted to n8n.
        *   The sending script is robust enough for potentially longer-running tasks.
