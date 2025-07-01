# Tagging Logic - URL Tagger Extension

## 🧠 Tag Association
- Tags are associated with the full `URL.href`
  - Includes protocol, domain, path, query string
- Each URL maps to an object containing:
  - `tags` (array of strings)
  - `title` (string, optional)
  - `createdAt` (ISO 8601 string)
  - `notes` (string, optional)

## ➕ Adding Tags
1. Get current tab’s full URL
2. Retrieve current tag array from `chrome.storage.local`
3. Input tag → trim + lowercase (optional normalization)
4. If tag not in list → add
5. Save back to storage

```js
const tags = new Set(existingTags);
tags.add(newTag);
const updated = [...tags];
```

## ➖ Removing Tags
- On user action (e.g. click “×” on tag bubble)
- Remove tag from array
- If array becomes empty → leave entry or optionally delete
- Save updated array to storage

## 🔁 Deduplication
- Tags treated as case-sensitive strings
- Set-based approach ensures no duplicates
- On import: merge tags from file + existing storage
  - Use Set to eliminate duplicates

## 🧼 Normalization (Optional Enhancements)
- Lowercase all tags
- Strip leading/trailing whitespace
- Disallow special characters
- Replace spaces with hyphens or underscores

## 🟢 Tagged vs 🔴 Untagged State
### Definition
- Tagged = URL has non-empty `tags` array in `chrome.storage.local`
- Untagged = URL missing or has empty `tags` array

### Visual Indicators
- Extension badge:
  - ✅ Tagged: Green background, text: ✓
  - ⚠️ Untagged: Red background, text: !
- Content script (optional):
  - Injects banner div
  - Color-coded based on tag presence

## 📅 Metadata
- `createdAt`: stored on first tag creation for a URL
- `title`: auto-fetched from `tab.title`
- `notes`: user-editable field (optional future addition)

## 🔄 Merge Logic for Import
- For each URL in imported JSON:
  - If URL exists:
    - Merge tag arrays (deduplicated)
    - Do not overwrite `title`, `createdAt`, or `notes` unless explicitly allowed
  - If URL does not exist:
    - Add full entry as-is
