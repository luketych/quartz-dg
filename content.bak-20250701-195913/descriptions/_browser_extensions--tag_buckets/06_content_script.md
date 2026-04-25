# Content Script Logic - URL Tagger Extension

## 📋 Purpose
- Provide an **in-page visual cue** indicating whether the current page is tagged
- Inject a **color-coded banner** at the top of the webpage
- Banner displays tag status and current tags

## 📥 Injection Trigger
- Content script is injected on all pages (via manifest or scripting)
- Runs when DOM is ready

## 🔁 Message Flow
1. `content.js` sends message to background with `location.href`
2. Background script retrieves tags from `chrome.storage.local`
3. Background sends back tag list (or empty array)
4. `content.js` injects banner based on tag presence

```js
chrome.runtime.sendMessage({ action: "getTags", url: location.href }, (tags) => {
  injectBanner(tags);
});
```

## 🎨 Banner UI
### Styles
```css
position: fixed;
top: 0;
left: 0;
width: 100%;
padding: 8px;
font-size: 14px;
text-align: center;
z-index: 9999;
color: white;
background-color: (green if tagged, red if untagged);
```

### Logic
```js
function injectBanner(tags) {
  const banner = document.createElement('div');
  banner.textContent = tags.length
    ? `Tagged: ${tags.join(', ')}`
    : '⚠️ No tags for this page';
  banner.style.backgroundColor = tags.length ? '#4CAF50' : '#F44336';
  banner.style = commonStyles;
  document.body.appendChild(banner);
}
```

## 🧼 Cleanup
- Only one banner is injected per page
- Optionally remove banner on navigation or reinject on SPA changes

## ⚠️ Considerations
- May conflict with site styles or headers
- Consider user setting to enable/disable content script injection
- Respect `z-index` stacking contexts of target site
- Avoid interfering with form inputs or fixed navs

## 🔐 Permissions Needed
```json
"content_scripts": [
  {
    "matches": ["<all_urls>"],
    "js": ["content.js"]
  }
]
```

## ✅ Optional Enhancements
- Add close button to banner
- Allow inline tag editing from banner (future feature)
- Auto-hide after delay (e.g. 10 seconds)
- Move to corner or bottom bar instead of top
