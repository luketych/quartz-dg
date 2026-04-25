# 📡 Test Server Setup: Sending Mock Influencer & Chart Data to n8n

## ✅ Goal

Set up a lightweight HTTP server that sends **mock influencer** and **chart event** data to an n8n **Webhook Trigger**. This document is designed for developers or AI agents to implement directly.

---

## 🔗 n8n Webhook Configuration

### Step 1: Create Webhook in n8n

1. Open n8n.
2. Create a new workflow.
3. Add a **Webhook node**.
4. Configure it as follows:

   * **HTTP Method**: `POST`
   * **Path**: `external-events`
   * Save and **activate** the workflow.

### Example Webhook URL (Local)

```
http://localhost:5678/webhook/external-events
```

---

## 🧪 JSON Data Structure

This is the structure of the data that will be POSTed to the webhook.

### Influencer Event

```json
{
  "type": "influencer",
  "influencer": "elonmusk",
  "platform": "twitter",
  "content": "Tesla announces major breakthrough in battery tech",
  "timestamp": "2024-05-27T15:32:00Z",
  "engagement": {
    "likes": 120000,
    "retweets": 23000
  },
  "sentiment": 0.92,
  "tickers": ["TSLA"]
}
```

### Chart Event

```json
{
  "type": "chart",
  "ticker": "TSLA",
  "event_type": "rsi_oversold",
  "rsi": 28.5,
  "timestamp": "2024-05-27T15:45:00Z",
  "context": "RSI dropped below 30"
}
```

---

## 🧰 Server Implementation (Node.js + Express)

### Install dependencies:

```bash
npm init -y
npm install express axios
```

### `server.js`

```javascript
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

const N8N_WEBHOOK_URL = 'http://localhost:5678/webhook/external-events';

app.post('/send-influencer', async (req, res) => {
  const data = {
    type: 'influencer',
    influencer: 'elonmusk',
    platform: 'twitter',
    content: 'Tesla announces major breakthrough in battery tech',
    timestamp: new Date().toISOString(),
    engagement: {
      likes: 120000,
      retweets: 23000
    },
    sentiment: 0.92,
    tickers: ['TSLA']
  };

  try {
    await axios.post(N8N_WEBHOOK_URL, data);
    res.send('Influencer event sent');
  } catch (error) {
    console.error(error);
    res.status(500).send('Error sending to n8n');
  }
});

app.post('/send-chart', async (req, res) => {
  const data = {
    type: 'chart',
    ticker: 'TSLA',
    event_type: 'rsi_oversold',
    rsi: 28.5,
    timestamp: new Date().toISOString(),
    context: 'RSI dropped below 30'
  };

  try {
    await axios.post(N8N_WEBHOOK_URL, data);
    res.send('Chart event sent');
  } catch (error) {
    console.error(error);
    res.status(500).send('Error sending to n8n');
  }
});

app.listen(3000, () => {
  console.log('Test server running on http://localhost:3000');
  console.log('POST to /send-influencer or /send-chart to trigger');
});
```

### Run the Server

```bash
node server.js
```

---

## 🧪 Trigger Event

To simulate data being sent to n8n:

```bash
curl -X POST http://localhost:3000/send-influencer
curl -X POST http://localhost:3000/send-chart
```

You should see the data appear in n8n under the Webhook node.

---

## 🧼 Notes

* You can run this server locally or deploy it as a lightweight cloud function.
* Make sure n8n is running and the workflow is activated.
* For public access, use `ngrok` or a reverse proxy to expose your localhost.

---

Let the dev team or agent modify the mock data to include more variations over time.

