# Project Milestones (Detailed Runway)

- [x] ## Milestone 1: n8n Webhook Setup & Verification

*   **Objective:** Configure and activate the n8n webhooks to receive data.
*   **Tasks:**
    1.  Open n8n.
    2.  Create two new workflows (or use sub-workflows).
    3.  Add a **Webhook node** to each.
    4.  Configure the Webhook nodes:
        *   **Chart Events Webhook:**
            *   **HTTP Method**: `POST`
            *   **Path**: `chart_events` (or as per n8n setup)
            *   **URL**: `https://auto.codis.ca/webhook-test/chart_events`
        *   **Influencer Events Webhook:**
            *   **HTTP Method**: `POST`
            *   **Path**: `influential_events` (or as per n8n setup)
            *   **URL**: `https://auto.codis.ca/webhook-test/influential_events`
    5.  Save and **activate** the workflows.
*   **Verification:**
    *   Webhook URLs confirmed: `https://auto.codis.ca/webhook-test/chart_events` and `https://auto.codis.ca/webhook-test/influential_events`.
    *   Confirm the webhooks are active and listening for test events.

- [x] ## Milestone 2: Node.js Project & Server Initialization

*   **Objective:** Set up the basic Node.js project structure and Express server.
*   **Tasks:**
    1.  Create a new project directory (e.g., `mock-data-server`). (Completed: `/Users/luketych/Dev/_playground/n8n/mock_data-events/viscera/`)
    2.  Navigate into the directory and initialize a Node.js project: `npm init -y`. (Completed: `package.json` exists)
    3.  Install required dependencies: `npm install express axios`. (Completed: Dependencies listed in `package.json`)
    4.  Create the main server file: `server.js`. (Completed: `/Users/luketych/Dev/_playground/n8n/mock_data-events/viscera/server.js`)
    5.  In `server.js`:
        *   Require `express` and `axios`. (Completed)
        *   Initialize the Express app: `const app = express();`. (Completed)
        *   Enable JSON body parsing: `app.use(express.json());`. (Completed)
        *   Define constants for the two n8n webhook URLs: (Completed)
            *   `N8N_CHART_EVENTS_URL = 'https://auto.codis.ca/webhook-test/chart_events'`
            *   `N8N_INFLUENCER_EVENTS_URL = 'https://auto.codis.ca/webhook-test/influential_events'`

- [x] ## Milestone 3: Implement Influencer Event Endpoint

*   **Objective:** Create the server endpoint to send mock influencer data.
*   **Tasks:**
    1.  In `server.js`, define a `POST` route for `/send-influencer`. (Completed)
    2.  Inside the route handler:
        *   Construct the mock influencer JSON data object as specified in `start.md`. (Completed)
        *   Use `async/await` with `axios.post(N8N_INFLUENCER_EVENTS_URL, influencerData)` to send the data. (Completed)
        *   Send a success response: `res.send('Influencer event sent successfully');`. (Completed)
        *   Implement error handling: (Completed)
            *   Log errors to the console (`console.error(error);`).
            *   Send a 500 status code with an error message: `res.status(500).send('Error sending influencer event to n8n');`.

- [x] ## Milestone 4: Implement Chart Event Endpoint

*   **Objective:** Create the server endpoint to send mock chart event data.
*   **Tasks:**
    1.  In `server.js`, define a `POST` route for `/send-chart`. (Completed)
    2.  Inside the route handler:
        *   Construct the mock chart event JSON data object as specified in `start.md`. (Completed)
        *   Use `async/await` with `axios.post(N8N_CHART_EVENTS_URL, chartData)` to send the data. (Completed)
        *   Send a success response: `res.send('Chart event sent successfully');`. (Completed)
        *   Implement error handling (similar to the influencer endpoint). (Completed)

- [x] ## Milestone 5: Server Launch & Testing

*   **Objective:** Start the server and test its functionality by sending data to n8n.
*   **Tasks:**
    1.  In `server.js`, add the code to start the Express server: (Completed)
        ```javascript
        const PORT = process.env.PORT || 3000; // Or the current port being used, e.g., 3003
        app.listen(PORT, () => {
          console.log(`Mock data server running on http://localhost:${PORT}`);
          console.log(`POST to /send-influencer or /send-chart to trigger n8n events.`);
        });
        ```
    2.  Run the server from the terminal: `node server.js`. (Completed)
    3.  Use `curl` (or an API client like Postman) to send test requests: (Completed)
        *   `curl -X POST http://localhost:3000/send-influencer` (Adjust port as needed)
        *   `curl -X POST http://localhost:3000/send-chart` (Adjust port as needed)
*   **Verification:**
    *   Check the server console for startup messages and any error logs. (Completed)
    *   Verify that data appears in the n8n webhook executions. (Completed)
    *   Confirm that the server handles errors gracefully (e.g., if n8n webhook URL is wrong). (Completed)

- [x] ## Milestone 6: Implement Data Variation and Randomization

*   **Objective:** Enhance the server to send varied and randomized data for more realistic testing.
*   **Tasks:**
    1.  Add a data generation library like Faker.js: `npm install @faker-js/faker --save`. (Completed)
    2.  In `server.js`, import `faker` and modify the `/send-influencer` endpoint: (Completed)
        *   Use `faker` to generate random values for `influencer`, `platform`, `content`, `engagement` numbers, `sentiment`, and `tickers`.
    3.  Modify the `/send-chart` endpoint: (Completed)
        *   Use `faker` to generate random values for `ticker`, `event_type`, `rsi`, and `context`.
    4.  Test both endpoints to ensure varied data is sent and received by n8n. (Completed)
    5.  Consider and implement further refinements (optional, based on the [Data Refinement Proposal](./mock_data_refinements.md)):
        *   More specific data types (e.g., realistic stock tickers). (Completed)
        *   Contextual relationships between fields (e.g., RSI value matches `rsi_oversold` type). (Completed)
*   **Verification:**
    *   Observe varied data in n8n executions. (Completed)

## Project Completion Notes

*   All core objectives for creating a mock data server that sends varied, realistic influencer and chart events to n8n webhooks have been met.
*   The server is configurable, uses Faker.js for dynamic data, and includes basic error handling.
*   Further enhancements or optional features are now tracked in `someday_maybe.md`.
