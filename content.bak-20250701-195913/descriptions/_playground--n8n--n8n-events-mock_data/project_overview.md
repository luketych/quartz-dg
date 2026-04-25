# Project Overview: Mock Data Server for n8n

## 🎯 Goal

To set up a lightweight HTTP server that sends mock "influencer" and "chart event" data to an n8n Webhook Trigger. This server will facilitate testing and development of n8n workflows that consume external event data.

## 🛠️ Core Technologies

*   **Runtime/Framework:** Node.js with Express.js
*   **HTTP Client:** `axios`
*   **Target System:** n8n (for receiving webhook data)

## 📝 Description

The server will expose two main POST endpoints:
*   `/send-influencer`: Sends mock data representing an event from a social media influencer.
*   `/send-chart`: Sends mock data representing a technical analysis event from a financial chart.

The data structures for these events are predefined. The server will initially send hardcoded mock data, with potential for future enhancements to include more dynamic and varied data.
