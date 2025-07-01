# Proposal for Refining Mock Data Generation

While the current mock data server sends varied data using Faker.js, we can enhance it to be more realistic and suitable for specific testing scenarios. This document outlines potential refinements.

## 1. More Specific Data Types & Formats

This involves tailoring the generated data to better match real-world formats and constraints.

### Influencer Endpoint (`/send-influencer`)

*   **`tickers` Field:**
    *   **Current:** `[faker.finance.currencyCode() + faker.finance.currencyCode()]` (e.g., "CADUSD")
    *   **Proposed Refinement:**
        *   Use a predefined list of common stock symbols (e.g., "AAPL", "MSFT", "TSLA") or crypto tickers (e.g., "BTC", "ETH", "SOL").
        *   Alternatively, use `faker.finance.stockSymbol()` for a stock-like format, or `faker.finance.bitcoinAddress()` / `faker.finance.ethereumAddress()` if relevant.
        *   For crypto pairs, consider `[faker.helpers.arrayElement(['BTC', 'ETH', 'SOL']), faker.helpers.arrayElement(['USD', 'EUR', 'CAD'])].join('/')` to get "BTC/USD".
    *   **Example:** `tickers: [faker.helpers.arrayElement(['AAPL', 'GOOG', 'TSLA', 'BTC', 'ETH'])]`

*   **`content` Field:**
    *   **Current:** `faker.lorem.sentence()`
    *   **Proposed Refinement:**
        *   Adjust content length or style based on the `platform`.
        *   If `platform` is 'twitter', use `faker.lorem.words(faker.number.int({ min: 5, max: 20 }))` to simulate tweet length.
        *   If `platform` is 'youtube', content could be `faker.lorem.sentence({ min: 5, max: 10 })` to mimic a video title.

### Chart Endpoint (`/send-chart`)

*   **`ticker` Field:**
    *   **Current:** `faker.finance.currencyCode()` (e.g., "USD", "EUR")
    *   **Proposed Refinement:**
        *   Use `faker.finance.stockSymbol()` for a more appropriate stock ticker format.
        *   Alternatively, use a predefined list of relevant tickers for your specific domain.
    *   **Example:** `ticker: faker.finance.stockSymbol()`

## 2. Relationships Between Fields (Contextual Data)

This focuses on making the generated data internally consistent and logical.

### Chart Endpoint (`/send-chart`)

*   **`event_type` and `rsi` Fields:**
    *   **Current:** `event_type` is random, and `rsi` is a random float (10-90), with no direct correlation.
    *   **Proposed Refinement:**
        *   If `event_type` is `'rsi_oversold'`, generate `rsi` in a low range (e.g., `faker.number.float({ min: 10, max: 30 })`).
        *   If `event_type` is `'rsi_overbought'`, generate `rsi` in a high range (e.g., `faker.number.float({ min: 70, max: 90 })`).
        *   For other `event_type` values, `rsi` can be in a neutral or broader range.
    *   **Example Implementation Snippet:**
        ```javascript
        const eventType = faker.helpers.arrayElement(['rsi_oversold', 'rsi_overbought', 'golden_cross']);
        let rsiValue;
        if (eventType === 'rsi_oversold') {
          rsiValue = faker.number.float({ min: 10, max: 30, precision: 2 });
        } else if (eventType === 'rsi_overbought') {
          rsiValue = faker.number.float({ min: 70, max: 90, precision: 2 });
        } else {
          rsiValue = faker.number.float({ min: 30, max: 70, precision: 2 });
        }
        // ... then use eventType and rsiValue in chartData
        ```

### Influencer Endpoint (`/send-influencer`)

*   **`content` and `tickers` Fields:**
    *   **Current:** `content` and `tickers` are generated independently.
    *   **Proposed Refinement:**
        *   First, generate a `selectedTicker`.
        *   Then, incorporate `selectedTicker` into the `content` string.
        *   Ensure the `tickers` array includes `selectedTicker`.
    *   **Example Implementation Snippet:**
        ```javascript
        const selectedTicker = faker.finance.stockSymbol();
        const content = `Great news about ${selectedTicker}! ${faker.lorem.sentence()}`;
        const tickers = [selectedTicker, faker.finance.stockSymbol()]; // Could add more random tickers
        // ... then use content and tickers in influencerData
        ```

## Benefits of These Refinements

*   **Increased Realism:** Mock data will more closely resemble actual data, improving the quality of tests.
*   **Targeted Scenario Testing:** Enables the creation of specific data patterns to test edge cases or particular behaviors in n8n workflows.
*   **Improved Clarity:** More coherent and logical mock data is easier to understand during demonstrations or debugging.

Let me know if you'd like to proceed with implementing any of these specific refinements!
