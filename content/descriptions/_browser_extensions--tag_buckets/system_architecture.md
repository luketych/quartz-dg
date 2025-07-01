# System Architecture - URL Tagger Extension

## 📁 File Structure

```
url-tagger-extension/
├── manifest.json
├── popup.html
├── popup.js
├── popup.css
├── background.js
├── content.js
├── utils.js (optional)
├── icons/
│   └── icon_*.png
```

## 🧱 Components

### Popup

* Triggered by browser action icon
* Renders UI to view/add tags
* Calls `chrome.storage.local` for tag retrieval/storage
* Triggers export/import logic

### Background Script

* Runs continuously as service worker
* Listens to:

  * `chrome.tabs.onActivated`
  * `chrome.tabs.onUpdated`
* Determines current tab's URL → checks for tags
* Sets badge text and color based on tag state
* Listens for messages from `content.js`

### Content Script

* Injected into matching pages (optional)
* On page load:

  * Sends message to background to fetch tags for `window.location.href`
  * Injects banner (green/red) showing tag presence and content

### Storage

* Uses `chrome.storage.local` to persist tag data
* JSON structure: `{ URL.href: { tags: [...], title, createdAt, notes } }`

### Export/Import

* Uses File System Access API
* Triggered via popup
* Export: Saves `chrome.storage.local` contents as `tags.json`
* Import: Loads file and merges data into `chrome.storage.local`

## 🔄 Message Passing

* `popup.js ↔ background.js`
* `content.js ↔ background.js`
* Messages include `{ action, url }`, e.g., `getTags`, `setBadge`, `showBanner`

## 📦 Data Keys

* URLs stored as `key = full URL (string)`
* Values:

```json
{
  "tags": ["string"],
  "title": "string",
  "createdAt": "ISO 8601 string",
  "notes": "string"
}
```

## 🔐 Permissions (in manifest)

```json
"permissions": [
  "storage",
  "tabs",
  "activeTab",
  "scripting"
]
```

## 🛠 Manifest (v3)

* Uses background service worker
* `"action"` defines popup HTML
* `"content_scripts"` injected into `<all_urls>`

## ⚙️ Optional Utilities

* `utils.js` for:

  * URL normalization
  * Tag deduplication
  * Export/import helpers

