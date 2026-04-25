# Export / Import Logic - URL Tagger Extension

## 🎯 Purpose
- Allow users to export all tagged URL data to a `tags.json` file
- Allow users to import `tags.json` to restore or merge tags
- Enable external tool integration (e.g. Obsidian, scripts)

---

## 📤 Export Flow
### Trigger
- User clicks "Export" button in popup

### Steps
1. Use `chrome.storage.local.get(null)` to get all tag entries
2. Prompt user with `showSaveFilePicker()`
3. Write data to JSON file (pretty printed)
4. Save file as `tags.json`

### Example
```js
const data = await new Promise(resolve => chrome.storage.local.get(null, resolve));
const handle = await window.showSaveFilePicker({
  suggestedName: 'tags.json',
  types: [{ description: 'JSON', accept: { 'application/json': ['.json'] } }]
});
const writable = await handle.createWritable();
await writable.write(JSON.stringify(data, null, 2));
await writable.close();
```

### File Format
See `03_storage_schema.json` for exact format.

---

## 📥 Import Flow
### Trigger
- User clicks "Import" button in popup

### Steps
1. Prompt user with `showOpenFilePicker()`
2. Read selected file as text
3. Parse contents as JSON
4. For each entry:
   - If key (URL) exists in `chrome.storage.local`:
     - Merge `tags` arrays using Set (deduplicate)
     - Retain original `title`, `createdAt`, `notes`
   - If key does not exist:
     - Add entry as-is
5. Save merged object back to `chrome.storage.local`

### Example
```js
const [handle] = await window.showOpenFilePicker();
const file = await handle.getFile();
const text = await file.text();
const imported = JSON.parse(text);

chrome.storage.local.get(null, (existing) => {
  for (const url in imported) {
    const current = existing[url] || { tags: [], title: '', createdAt: '', notes: '' };
    const newTags = new Set([...(current.tags || []), ...(imported[url].tags || [])]);
    existing[url] = {
      ...current,
      tags: [...newTags],
      title: current.title || imported[url].title,
      createdAt: current.createdAt || imported[url].createdAt,
      notes: current.notes || imported[url].notes
    };
  }
  chrome.storage.local.set(existing);
});
```

---

## ⚠️ Import Safeguards
- Validate JSON structure
- Catch parse errors
- Limit size or number of entries
- Confirm with user before overwriting large batches

---

## ✅ Compatibility
- Output is compatible with:
  - Obsidian (convert to Markdown or YAML frontmatter)
  - CLI tools / scripts
  - Other extensions with same format
