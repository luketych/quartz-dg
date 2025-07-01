# URL Tagger Extension - 50,000 ft Overview

## 🧭 Purpose
Enable users to attach, view, and manage tags on any URL via a browser extension. Tags are stored locally in a structured, exportable format (JSON), with a focus on integration with personal knowledge management systems (e.g. Obsidian).

## 🎯 Core Features
- Add/remove custom tags to the current URL via popup UI
- Visual indication if current page has tags or not (e.g. icon badge or in-page banner)
- Store tags persistently using browser storage (local or file-based JSON)
- Export/import all tagged URLs to/from JSON format
- Option to annotate each URL with title, timestamp, and custom notes

## 🔄 Flow Summary
1. User opens extension while visiting a webpage
2. User views current tags (if any) and can add/remove tags
3. Extension shows visual cue if page is tagged (green) or not (red)
4. Tags are stored locally in JSON (key = URL, value = tag list + metadata)
5. User can export/import data as `tags.json`
6. JSON format is compatible with markdown/YAML for Obsidian

## 📦 Data Format (tags.json)
```json
{
  "https://example.com": {
    "tags": ["design", "research"],
    "title": "Example Site",
    "createdAt": "2025-05-23T12:00:00Z",
    "notes": "Optional user notes"
  },
  ...
}
```

## 🔌 Tech Stack
- **Browser**: Chrome (Manifest v3)
- **Storage**: `chrome.storage.local` + FileSystem API for export/import
- **UI**: HTML/CSS/JS (Popup + optional injected banner)
- **APIs**: Chrome Extensions API, Tab API, Storage API

## 🔗 Obsidian Integration
- Exported `tags.json` can be:
  - Converted to markdown files per URL
  - Parsed into YAML frontmatter
  - Used to cluster URLs by tag within Obsidian graph view

## 🚦 Visual Tag Presence Indicator
- ✅ Tagged: Green badge (✓)
- ⚠️ Untagged: Red badge (!)
- Optional: On-page banner indicating tag state

## 🧱 Design Goals
- Speed: Minimal interaction needed to tag
- Visibility: Tag state must be immediately obvious
- Portability: Data must be easy to export, analyze, transform
- Extensibility: Support future annotation types and integrations
