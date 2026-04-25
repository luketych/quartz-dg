# Sprint 3: Historical Data Collection for Event Simulation

**Overall Objective:** Collect a sufficient volume of historical financial news and 5-minute intraday price data for key tickers. This data will enable future simulation of market events by allowing a chronological "walk-forward" through 5-minute intervals, correlating price changes with influential news events.

---

- [x] ## Milestone 11: Define Data Collection Scope and Strategy
    *   **Objective:** Specify the tickers, historical time range, data granularity, storage methods, and error handling for the data collection process.
    *   **Status: COMPLETED**
    *   **Plan Details:**
        1.  **Ticker Selection:**
            *   **Primary (5-min Intraday OHLCV & News):** `AAPL.US` (Utilizing EODHD `DEMO` key's specific support).
            *   **Secondary (News & potentially EOD historical prices):** `TSLA.US`, `VTI.US`, `AMZN.US`, `BTC-USD.CC`, `EURUSD.FOREX`.
                *   *Note: 5-min intraday for secondary tickers, especially crypto, might be limited with EODHD `DEMO` key. Shrimpy API may be revisited for crypto if needed.*
        2.  **Time Period Definition:**
            *   **Target Range:** Last ~90-120 days to maximize data via EODHD `DEMO` key.
            *   **Specific Dates (approx., assuming current date June 2, 2025):** March 4, 2025 – June 1, 2025.
            *   Applies to `AAPL.US` intraday and news for all selected tickers.
        3.  **Storage Strategy:**
            *   **Format:** JSON.
            *   **Root Data Directory:** `data/` (at project root `/Users/luketych/Dev/_playground/n8n/mock_data-events/`)
            *   **Intraday Prices:** `data/prices/eodhd/5_minute/{TICKER_CLEAN}/{YYYY-MM-DD}.json` (e.g., `AAPL_US/2025-05-20.json`). Each file = 1 day's 5-min candles.
            *   **News:** `data/news/eodhd/{TICKER_CLEAN}/{YYYY-MM}.json` (e.g., `AAPL_US/2025-05.json`). Each file = 1 month's news items for the ticker.
        4.  **API Interaction Plan (EODHD API & `DEMO` key):**
            *   **Critical Constraint:** EODHD `DEMO` key limit: **20 API calls/day**.
            *   **Intraday Prices (`AAPL.US`, 5-min interval):**
                *   Attempt to fetch the entire ~120-day available range in a **single API call** (`from` = ~120 days ago, `to` = yesterday).
                *   Data then split and saved into daily files locally.
            *   **Financial News (All 6 selected tickers):**
                *   For each ticker: Attempt to fetch news for the entire 90-day period in a **single API call** (`from`, `to` date parameters, `limit=1000`).
                *   Handle pagination (using `offset`) if results equal `limit` (risk for 20 calls/day limit).
            *   **General Parameters:** `api_token=DEMO`, `fmt=json`.
            *   Implement robust error handling (retries, 429 handling) and meticulous logging.
    *   **Verification:**
        *   This documented plan serves as the primary verification for this milestone.
        *   Choices justified by `DEMO` key limits and project goals.
        *   Main challenge: Strict 20 API calls/day limit; collection may span multiple days.

---

- [x] ## Milestone 12: Implement and Execute Intraday Price Data Collection
    *   **Objective:** Develop, test, and run the necessary scripts or server logic to systematically fetch and store 5-minute intraday historical price data for the selected primary ticker(s).
    *   **Status: COMPLETED**
    *   **Summary of Actions:**
        1.  Created a new script `viscera/scripts/collectIntraday_AAPL.js`.
        2.  The script defines `AAPL.US` as the target ticker and the period March 4, 2025 – June 1, 2025.
        3.  It utilizes the existing `getIntradayHistoricalData` function from `viscera/services/eodhdService.js` to fetch 5-minute interval data for the entire period in a single API call (leveraging `DEMO` key's capability for `AAPL.US`).
        4.  Fetched data is processed and grouped by day.
        5.  Each day's 5-minute candle data is saved into a separate JSON file in `data/prices/eodhd/5_minute/AAPL_US/{YYYY-MM-DD}.json`.
        6.  The script includes logging for API calls, data processing, and file saving operations.
        7.  Successfully ran the script, and data for `AAPL.US` from March 4, 2025, to May 30, 2025 (as per API availability) has been collected and stored.
    *   **Verification:**
        *   Confirmed 5-minute intraday price data for `AAPL.US` (approx. March 4 - May 30, 2025) is successfully fetched and stored in daily JSON files under `data/prices/eodhd/5_minute/AAPL_US/`.
        *   Verified stored data format (JSON array of 5-min candles with OHLCV, timestamp, datetime) and basic integrity by inspecting a sample file (`2025-05-20.json`).
        *   The collection script (`collectIntraday_AAPL.js`) is suitable for this specific task, handling a single large data fetch and subsequent local processing.

---

- [x] ## Milestone 13: Implement and Execute Financial News Data Collection
    *   **Objective:** Develop, test, and run scripts/logic to fetch and store historical financial news data for all selected tickers.
    *   **Status: COMPLETED**
    *   **Summary of Actions:**
        1.  **Modified `eodhdService.js`:** The `getFinancialNews` function was updated to accept an `options` object, allowing `limit`, `from`, `to`, and `offset` parameters to be passed, removing the hardcoded `limit: 10`.
        2.  **Created `viscera/scripts/collectNews.js`:**
            *   This script targets `AAPL.US`, `TSLA.US`, `VTI.US`, `AMZN.US`, `BTC-USD.CC`, and `EURUSD.FOREX`.
            *   It aims to fetch news for the period March 4, 2025 – June 1, 2025.
            *   It calls `getFinancialNews` with `limit: 1000`, `from`, and `to` dates for each ticker.
            *   Due to the 20 API calls/day limit with the `DEMO` key, full pagination for >1000 items per ticker was not implemented; instead, a warning is logged if 1000 items are returned.
            *   Fetched news items are grouped by month (e.g., `2025-05`) and saved into `data/news/eodhd/{TICKER_CLEAN}/{YYYY-MM}.json`.
        3.  **Executed `collectNews.js`:**
            *   The script ran successfully, making one API call per ticker.
            *   For `AAPL.US`, `TSLA.US`, `AMZN.US`, `BTC-USD.CC`, and `EURUSD.FOREX`, 1000 news items were returned, triggering the warning about potential further data.
            *   For `VTI.US`, 8 news items were returned.
            *   Data was saved in the specified monthly JSON files.
    *   **Verification:**
        *   Financial news data for the target period and all selected tickers has been fetched and stored in the `data/news/eodhd/` directory, organized by ticker and then by month (e.g., `AAPL_US/2025-06.json`).
        *   Verified stored data format (JSON array of news items with `date`, `title`, `content`, `link`, `symbols`) by inspecting a sample file (`AAPL_US/2025-06.json`).
        *   Acknowledged that for high-volume tickers, the collection might be incomplete due to API limitations (1000 items per call, 20 calls/day for `DEMO` key).

---

- [x] ## Milestone 14: Validate and Prepare Collected Data for Simulation
    *   **Objective:** Perform final checks on the collected historical data to ensure its integrity, completeness (within known limits), and suitability for the event simulation engine.
    *   **Status: COMPLETED**
    *   **Summary of Validation Findings & Pre-processing Considerations:**
        1.  **Price Data (`AAPL.US` - 5-minute intraday):
            *   **Integrity & Completeness:** Daily JSON files exist for all expected trading days from March 4, 2025, to May 30, 2025. Sampled files show correct 5-minute candle format (OHLCV, timestamp, datetime), sequential timestamps covering standard market hours (9:30 AM - 4:00 PM ET), and reasonable data values. No obvious corruption or major errors found.
            *   **Format:** Consistent JSON structure observed.
        2.  **News Data (All Selected Tickers - `AAPL.US`, `TSLA.US`, `VTI.US`, `AMZN.US`, `BTC-USD.CC`, `EURUSD.FOREX`):
            *   **Integrity & Completeness:**
                *   Monthly JSON files created as expected. However, March 2025 news data appears to be missing for `TSLA.US` and `AMZN.US` (files not generated), possibly due to no news items for March being present in the top 1000 items fetched for the entire March-June period for these tickers.
                *   For tickers where the API returned 1000 news items (`AAPL.US`, `TSLA.US`, `AMZN.US`, `BTC-USD.CC`, `EURUSD.FOREX`), the collection for the period might be incomplete due to the API's `limit` per call. This is a known constraint of using the `DEMO` key.
            *   **Format:** Sampled files show correct JSON structure with essential fields (`date`, `title`, `content`, `link`, `symbols`).
            *   **Potential Duplicates:** Observed instances of news items with identical titles and dates but different source links (e.g., Yahoo Finance vs. Nasdaq.com for the same story). This indicates a need for a deduplication strategy during pre-processing.
        3.  **Overall Data Readiness:**
            *   The collected data is considered sufficient for initial development of the event simulation engine.
        4.  **Key Pre-processing Considerations for Simulation Engine Development:**
            *   **News Deduplication:** Implement a strategy to identify and handle (e.g., merge or select one) duplicate or near-duplicate news articles. This might involve comparing normalized titles, URLs, or content similarity.
            *   **Timestamp Alignment:** Ensure consistent timestamp handling (e.g., all UTC) between price and news data for accurate correlation.
            *   **Data Loading Strategy:** The simulation engine will need to efficiently load daily price data and corresponding news data.
    *   **Verification:**
        *   Data validation performed by listing files, sampling content, and checking against expected formats and ranges.
        *   Key findings (missing March news for some tickers, news duplication) and pre-processing needs documented above.
        *   The dataset is deemed ready for initial use in the simulation, with the above pre-processing considerations to be addressed as part of the simulation engine's data ingestion/preparation phase.
