# Browser Extension API Usage - URL Tagger

## 🔌 Permissions (Manifest v3)

```json
"permissions": [
  "storage",
  "tabs",
  "activeTab",
  "scripting"
],
"host_permissions": [
  "<all_urls>"
]
```

## 🔧 Core APIs Used

### `chrome.storage.local`

* Store and retrieve tag data
* Key = full URL (string)
* Value = `{ tags: [...], title, createdAt, notes }`
* Used by: `popup.js`, `background.js`

```js
chrome.storage.local.get([url], (result) => { ... });
chrome.storage.local.set({ [url]: value }, () => { ... });
```

---

### `chrome.tabs`

* Get the current tab and its URL
* Used to initialize the popup context

```js
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const tab = tabs[0];
  const url = new URL(tab.url).href;
});
```

---

### `chrome.action`

* Sets popup HTML
* Controls badge text and color
* Used by `background.js`

```js
chrome.action.setBadgeText({ tabId, text: "✓" });
chrome.action.setBadgeBackgroundColor({ tabId, color: "#4CAF50" });
```

---

### `chrome.runtime.sendMessage / onMessage`

* Communication between popup, content, and background
* Used to request tags, update badges, trigger in-page banners

```js
// content.js
chrome.runtime.sendMessage({ action: "getTags", url: location.href }, (tags) => { ... });

// background.js
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "getTags") {
    chrome.storage.local.get([msg.url], (result) => {
      sendResponse(result[msg.url] || []);
    });
    return true; // Keep channel open
  }
});
```

---

### `chrome.scripting.executeScript`

* Inject content script dynamically (optional setup)
* Used to show in-page tag banners

```js
chrome.scripting.executeScript({
  target: { tabId },
  files: ["content.js"]
});
```

---

### `window.showSaveFilePicker()` (File System Access API)

* Used for manual export of all tag data

```js
const handle = await window.showSaveFilePicker({ ... });
const writable = await handle.createWritable();
await writable.write(JSON.stringify(data, null, 2));
await writable.close();
```

---

### `window.showOpenFilePicker()`

* Used for importing JSON file containing tagged URLs

```js
const [fileHandle] = await window.showOpenFilePicker();
const file = await fileHandle.getFile();
const text = await file.text();
const importedData = JSON.parse(text);
```

## 🧠 Summary Table

| API                              | Purpose                 | Used In                   |
| -------------------------------- | ----------------------- | ------------------------- |
| `chrome.storage.local`           | Store/retrieve tag data | popup.js, background.js   |
| `chrome.tabs`                    | Get active tab          | popup.js                  |
| `chrome.action`                  | Set badge icon/text     | background.js             |
| `chrome.runtime.sendMessage`     | Message passing         | content.js, background.js |
| `chrome.scripting.executeScript` | Inject scripts          | background.js             |
| `showSaveFilePicker`             | Export tags             | popup.js                  |
| `showOpenFilePicker`             | Import tags             | popup.js                  |

