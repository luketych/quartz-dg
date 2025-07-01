# Sprint 2: Realistic Historical Event Simulation

This sprint focuses on integrating real historical stock data to generate more realistic mock chart events.

- [x] ## Milestone 8: Select and Document Primary Data Source for News and Historical Market Data
*   **Objective:** Decide on the primary API(s) for fetching both financial news (for influencer events) and historical market data (for chart events/backtesting). Document API endpoints, key parameters, data formats, and any limitations (especially with free/demo keys).
*   **Tasks:**
    1.  Research and select a suitable API provider.
        *   **Decision: EODHD API (eodhd.com) selected.**
    2.  Identify specific endpoints for:
        *   Financial News.
            *   **Endpoint: `https://eodhd.com/api/news`**
        *   Historical Market Data (OHLCV – aiming for 5-minute intervals if possible, otherwise daily).
            *   **Endpoint (Intraday, 5-min for AAPL.US with DEMO key): `https://eodhd.com/api/intraday/{TICKER_SYMBOL}`**
            *   **Endpoint (End-of-Day, daily for all demo tickers): `https://eodhd.com/api/eod/{TICKER_SYMBOL}`**
        *   (Optional) Sentiment Data.
            *   **Endpoint: `https://eodhd.com/api/sentiments` (DEMO key support TBD)**
    3.  Document API key requirements and usage (e.g., `DEMO` key for EODHD).
    4.  Note supported tickers for the demo key: `AAPL.US, TSLA.US, VTI.US, AMZN.US, BTC-USD.CC, EURUSD.FOREX`.
    5.  Create/update `eod_hd-api_info.md` with all findings.
*   **Verification:**
    *   `eod_hd-api_info.md` is comprehensive and accurately reflects the capabilities of the EODHD API with the `DEMO` key for both news and historical stock data.
    *   Clear understanding of what data can be fetched for the initial demo stock tickers.

- [x] ## Milestone 9: Test EODHD APIs and Setup Historical Stock Data Fetching
*   **Objective:** Thoroughly test the EODHD News, EOD Historical, and Intraday Historical (for AAPL.US) APIs. Implement logic in the Node.js server to fetch and store/log sample historical stock data (5-minute for AAPL.US, daily for other demo stocks) to prepare for event generation.
*   **Tasks:**
    1.  Systematically test EODHD News API for all demo tickers (`AAPL.US, TSLA.US, VTI.US, AMZN.US, BTC-USD.CC, EURUSD.FOREX`) using the `DEMO` key.
    2.  Systematically test EODHD EOD Historical API (daily data) for all demo tickers using the `DEMO` key.
    3.  Systematically test EODHD Intraday API (5-minute data) for `AAPL.US` using the `DEMO` key.
    4.  Clarify and test date filtering capabilities for the News API.
    5.  (Optional) Test the EODHD Sentiment API, particularly with the `DEMO` key for `AAPL.US`, to confirm accessibility and data format.
    6.  Begin implementing basic functions in the Node.js server (e.g., in a `services/eodhdService.js` module) to make requests to these EODHD API endpoints.
    7.  Fetch and log/store sample data (news articles, daily OHLCV for several tickers, 5-min OHLCV for AAPL.US).
    8.  Ensure the `DEMO` API key is handled appropriately (e.g., as a constant or environment variable placeholder for future real keys).
*   **Verification:**
    *   Server logs demonstrate successful API calls and data retrieval for News, EOD Historical (daily), and Intraday Historical (5-min for AAPL.US) APIs for the specified demo stock tickers.
    *   Sample fetched stock data (news content, OHLCV data) is available and its structure is understood.
    *   Basic API fetching functions are integrated into the Node.js server structure.

- [x] ## Milestone 10: Project Cleanup, Refactoring, and ES Modules Migration
*   **Objective:** Review recent project structure changes, update to ES module syntax (`import`/`export`), configure `package.json` for ES modules and add run scripts, and set up basic Mocha testing. (All tasks completed)
*   **Tasks:** (All tasks completed)
    1.  **Project Structure Review:** (Completed)
        *   Documented current structure (e.g., `viscera/server/index.js` as main, `viscera/services/eodhdService.js`).
        *   Identified and updated paths/configurations (e.g., in `.vscode/launch.json`).
    2.  **ES Modules Migration:** (Completed)
        *   Updated root `package.json` by adding `"type": "module"`.
        *   Converted `viscera/server/index.js` and `viscera/services/eodhdService.js` to ES Modules.
        *   Ensured imports use correct relative paths and file extensions (e.g., `import ... from '../services/eodhdService.js';`).
        *   Updated `viscera/package.json` to `{"type": "module"}` to resolve Node.js module type warnings.
    3.  **Update `launch.json`:** (Completed)
        *   Verified program path in `launch.json` points to `viscera/server/index.js`.
        *   Confirmed compatibility with ES module execution.
    4.  **Add `package.json` Scripts:** (Completed)
        *   Created `"start": "node viscera/server/index.js"` script.
        *   Created `"test": "mocha"` script.
    5.  **Mocha Test Setup:** (Completed)
        *   Installed Mocha and Chai.
        *   Created `test/` directory and `test/eodhdService.test.js`.
        *   Wrote tests for `getFinancialNews` (valid/invalid tickers) and structural checks for other service functions.
*   **Verification:**
    *   [x] The application runs correctly using `npm start`.
    *   [x] `import`/`export` syntax is used throughout the JavaScript files.
    *   [x] VS Code debugger launches the correct server file.
    *   [x] A basic Mocha test runs successfully via `npm test`.
*   **Notes & Changes from Expectations:**
    *   The main server file path was confirmed as `viscera/server/index.js`. The `start` script in `package.json` was updated accordingly.
    *   An existing `package.json` file in the `viscera/` subdirectory, which appeared to be an outdated duplicate, was updated to solely contain `{"type": "module"}`. This resolved Node.js module type detection warnings that occurred during test runs.
    *   The initial Mocha test for `eodhdService.getFinancialNews` required an assertion update: the EODHD API returns a `date` field for news items, not `pubDate` as initially assumed.
    *   The EODHD API responds with a 403 (Forbidden) error for news requests involving completely invalid or non-existent tickers. The test for invalid tickers was confirmed to correctly anticipate an error being thrown.
