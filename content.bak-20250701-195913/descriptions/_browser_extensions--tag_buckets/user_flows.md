# User Flows - URL Tagger Extension

## 🧭 Primary Flows

### 1. Add Tags to URL

* Trigger: User opens extension on active tab
* If tags exist → display them
* Else → show empty tag list
* User enters new tag in input box
* User clicks "Add" or presses Enter
* Tag is appended to list (deduplicated)
* Tag list saved under key = full URL

### 2. View Existing Tags

* Trigger: Popup loads on current tab
* Query `chrome.storage.local` for URL
* If tags exist → display as bubble tags
* Else → show placeholder "No tags yet"

### 3. Remove Tags

* Trigger: User clicks a tag (optional behavior: click to remove)
* Remove tag from in-memory list
* Save updated tag list to `chrome.storage.local`

### 4. Export Tags to JSON

* Trigger: User clicks "Export" in popup menu
* Retrieve all entries from `chrome.storage.local`
* Show File Picker (via File System Access API)
* Write JSON structure to file (e.g. `tags.json`)

### 5. Import Tags from JSON

* Trigger: User clicks "Import" in popup menu
* Show File Picker (read mode)
* Parse JSON file
* Merge with existing entries in `chrome.storage.local`
* Prevent overwriting unless URL already exists

### 6. Visual Feedback for Current Page

* On tab switch or navigation:

  * Query storage for current URL
  * If tags exist → green badge with ✓
  * Else → red badge with !

### 7. In-Page Banner (Optional)

* Inject `content.js` when page loads
* Send message to background with current URL
* Display banner at top of page with tag info
* Color: Green = tagged, Red = untagged

## 🧑‍💻 Edge Cases

* Add duplicate tag → ignore
* Remove last tag → entry may remain empty
* Visit same URL with/without query string → treated as different
* Tags stored against full `URL.href`, not just hostname or path

## 🔐 Permissions Required

* `tabs` – get current URL
* `storage` – store tags
* `scripting` – inject banner (if used)
* `activeTab` – needed for popup tab context

