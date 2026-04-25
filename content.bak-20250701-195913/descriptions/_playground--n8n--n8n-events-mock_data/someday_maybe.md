# Someday/Maybe: Future Enhancements

This file lists optional features or milestones that could be considered for future development of the mock data server.

## Public Accessibility (Previously Milestone 7)

*   **Objective:** Make the local server accessible from the internet if required for broader testing or integration (e.g., if an external service needs to call *into* this mock server, or if you want to trigger it from outside your local network).
*   **Context:** Not currently necessary as the server only makes outbound calls to publicly accessible n8n webhooks.
*   **Tasks (If needed):**
    1.  **Option 1 (Temporary):** Use a tool like `ngrok` to create a secure tunnel to your `localhost`.
        *   Install ngrok.
        *   Run `ngrok http 3000` (or your server's port).
        *   Use the provided ngrok URL.
    2.  **Option 2 (More Permanent):** Deploy the Node.js server as a lightweight cloud function or service (e.g., AWS Lambda + API Gateway, Google Cloud Functions, Vercel Serverless Functions, Heroku). This would involve adapting the server code for the chosen platform.

- [ ] ## Milestone 10: Generate Realistic Chart Events from Historical Stock Data
*   **Objective:** Adapt the `/send-chart` endpoint (or create a new one, e.g., `/send-historical-stock-chart`) to generate events based on the fetched historical stock data.
*   **Tasks:**
    1.  Decide on a strategy for using historical stock data:
        *   **Option A (Replay):** Fetch a chunk of historical stock data and "replay" it, sending events sequentially as if time is progressing.
        *   **Option B (Event Trigger):** Analyze a chunk of historical stock data to identify significant patterns (e.g., large price swing, RSI crossing a threshold based on historical closes, volume spike) and generate a single event based on that pattern.
    2.  Modify the event generation logic:
        *   Instead of purely `faker` for `rsi`, `event_type`, and `context`, derive these from the historical stock data.
        *   For example, calculate RSI from historical stock closing prices.
        *   Set `event_type` based on identified patterns or RSI values.
        *   Populate `context` with information about the historical stock data point that triggered the event.
        *   The `ticker` should be the stock symbol for which data was fetched (e.g., `AAPL.US`).
        *   `timestamp` should reflect the historical stock data point's time.
*   **Verification:**
    *   The `/send-chart` (or new) endpoint sends events to n8n where the data (ticker, RSI, event_type, context, timestamp) is clearly derived from actual historical stock data.
    *   Events for stocks appear more realistic and less random.

- [ ] ## Milestone 11: Testing and Refinement of Historical Stock Event Generation
*   **Objective:** Thoroughly test the new historical stock event generation and refine as needed.
*   **Tasks:**
    1.  Send multiple stock events and verify data consistency and realism in n8n.
    2.  Test with different stock symbols available via the DEMO key (e.g., `AAPL.US`, `TSLA.US` for daily if 5-min is limited).
    3.  Refine event detection logic (if using Option B from Milestone 10) to capture interesting scenarios in stock data.
    4.  Ensure error handling for API data issues (e.g., missing data points) is robust.
*   **Verification:**
    *   The system reliably generates a stream of realistic stock chart events based on historical data.
