# EODHD API Information

## General
-   **Provider**: EODHD (eodhd.com)
-   **API Key for Testing**: `DEMO`
-   **Test Tickers for DEMO Key**: AAPL.US, TSLA.US, VTI.US, AMZN.US, BTC-USD.CC, EURUSD.FOREX.
    -   Note: Intraday data with the `DEMO` key is confirmed to work only for `AAPL.US`.

## 1. Financial News API
-   **Documentation**: [https://eodhd.com/financial-apis/stock-market-financial-news-api](https://eodhd.com/financial-apis/stock-market-financial-news-api)
-   **Base Endpoint**: `https://eodhd.com/api/news`
-   **Description**: Returns latest financial news headlines and full articles for a given ticker or topic tag. Supports filtering by date and pagination.
-   **Key Parameters**:
    -   `api_token`: Your API key (e.g., `DEMO`).
    -   `s`: Ticker symbol (e.g., `AAPL.US`).
    -   `t`: Topic tag (e.g., `earnings report`). *Must provide `s` or `t`.*
    -   `offset`: For pagination (e.g., `0`).
    -   `limit`: Number of results per page (e.g., `10`).
    -   `fmt`: Output format (e.g., `json`).
-   **Example (JSON for AAPL.US)**:
    ```
    [https://eodhd.com/api/news?s=AAPL.US&offset=0&limit=10&api_token=demo&fmt=json](https://eodhd.com/api/news?s=AAPL.US&offset=0&limit=10&api_token=demo&fmt=json)
    ```

## 2. Intraday Historical Data API
-   **Documentation**: [https://eodhd.com/financial-apis/intraday-historical-data-api](https://eodhd.com/financial-apis/intraday-historical-data-api)
-   **Base Endpoint**: `https://eodhd.com/api/intraday/{SYMBOL_NAME}.{EXCHANGE_ID}`
-   **Description**: Provides intraday (1-minute, 5-minute, 1-hour) historical stock data.
-   **Key Parameters**:
    -   `api_token`: Your API key (e.g., `DEMO`).
    -   `interval`: Data interval (`1m`, `5m`, `1h`).
    -   `fmt`: Output format (`json` or `csv`).
    -   `from`, `to`: UNIX timestamps (UTC) for date/time range.
        -   Max period for 5-min data: 600 days.
        -   Without `from`/`to`, defaults to last 120 days.
-   **Example (JSON, 5-min for AAPL.US)**:
    ```
    [https://eodhd.com/api/intraday/AAPL.US?interval=5m&api_token=demo&fmt=json](https://eodhd.com/api/intraday/AAPL.US?interval=5m&api_token=demo&fmt=json)
    ```
-   **Example (CSV, 5-min for AAPL.US)**:
    ```
    [https://eodhd.com/api/intraday/AAPL.US?interval=5m&api_token=demo&fmt=csv](https://eodhd.com/api/intraday/AAPL.US?interval=5m&api_token=demo&fmt=csv)
    ```
-   **Output (JSON)**: Array of objects, each with `timestamp`, `gmtoffset`, `datetime`, `open`, `high`, `low`, `close`, `volume`.

## 3. End-of-Day (EOD) Historical Data API
-   **Documentation**: [https://eodhd.com/financial-apis/api-for-historical-data-and-volumes](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)
-   **Base Endpoint**: `https://eodhd.com/api/eod/{SYMBOL_NAME}.{EXCHANGE_ID}`
-   **Description**: Provides daily, weekly, or monthly historical stock data.
-   **Key Parameters**:
    -   `api_token`: Your API key (e.g., `DEMO`).
    -   `from`, `to`: Date range in `YYYY-MM-DD` format.
    -   `period`: Data period (`d` for daily, `w` for weekly, `m` for monthly).
    -   `fmt`: Output format (`json` or `csv`).
-   **Example (JSON, Daily for MCD.US - from docs, adapt ticker)**:
    ```
    [https://eodhd.com/api/eod/MCD.US?from=2020-01-05&to=2020-02-10&period=d&api_token=demo&fmt=json](https://eodhd.com/api/eod/MCD.US?from=2020-01-05&to=2020-02-10&period=d&api_token=demo&fmt=json)
    ```
-   **Output (JSON)**: Array of objects, each with `date`, `open`, `high`, `low`, `close`, `adjusted_close`, `volume`.

## Additional API Details and Considerations (Re-evaluation)

### General
- **Ticker Naming Convention**: For APIs requiring a ticker (Intraday, EOD Historicals, News, Sentiments), the format is generally `{SYMBOL_NAME}.{EXCHANGE_ID}` (e.g., `AAPL.US` for NASDAQ). A list of supported exchanges can be found at [https://eodhistoricaldata.com/financial-apis/list-supported-exchanges/](https://eodhistoricaldata.com/financial-apis/list-supported-exchanges/).

### Intraday Historical Data API (Further Notes)
- **Date Filtering (`from`, `to`)**:
    - Parameters must be UNIX timestamps (UTC).
    - Maximum data period retrievable per request:
        - 1-minute interval: 120 days
        - 5-minute interval: 600 days
        - 1-hour interval: 7200 days (theoretical maximum)
    - If `from` and `to` are not specified, the API returns data for the last 120 days.
- **Output Format**: Default is CSV. Ensure `fmt=json` is used for JSON.

### Financial News API (Further Notes)
- **Date Filtering**: The documentation states the API supports filtering by date, but the provided examples do not demonstrate date parameters (`from`, `to`). **The exact format and usage for date filtering need to be confirmed (e.g., `YYYY-MM-DD` or UNIX timestamps).**
- **Output Data**: News articles in the JSON output should have dates in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
- **Topic Tags (parameter `t`)**: A comprehensive list of over 50 tags is available for fetching news by topic, including:
    - `'balance sheet', 'capital employed', 'class action', 'company announcement', 'consensus eps estimate', 'earnings report', 'financial results', 'initial public offering', 'insider transactions', 'institutional ownership', 'price target', 'quarterly earnings', 'revenue estimates', 'shareholder rights', 'total revenue', etc.` (Full list in documentation).

### Sentiment Data API (New Section)
- **Endpoint**: `GET https://eodhd.com/api/sentiments`
- **Description**: Provides sentiment scores for financial instruments (stocks, ETFs, crypto), calculated from news and social media. Scores are normalized from -1 (very negative) to +1 (very positive).
- **Key Parameters**:
    - `s`: One or multiple ticker symbols, comma-separated (e.g., `AAPL.US,BTC-USD.CC`).
    - `from`, `to`: Date range for sentiment data (e.g., `from=2022-01-01&to=2022-04-22`).
    - `api_token`: Your API key. 
    - `fmt=json`: For JSON output.
- **Output Format (JSON)**: Data is grouped by ticker. 
- **Potential Use**: Could be valuable for "influencer events" by associating news or market periods with a sentiment score.