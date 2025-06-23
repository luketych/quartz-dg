# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Quartz is a modern static site generator for publishing digital gardens and notes as websites. Built with TypeScript, it transforms Markdown content into fully functional websites with features like Obsidian compatibility, full-text search, graph views, and wikilinks.

## Development Commands

### Core Commands

- `npx quartz build` - Build the site
- `npx quartz build --serve` - Build and serve locally with hot reload
- `npx quartz build --serve -d docs` - Build and serve the docs
- `npm run docs` - Shortcut to build and serve docs
- `npm run check` - Type check and format check
- `npm run format` - Format code with Prettier
- `npm run test` - Run tests with Node.js test runner
- `npm run profile` - Profile build performance

### Development Server

- Local server runs on http://localhost:8080
- WebSocket server on port 3001 for hot reload
- File watching with chokidar for incremental rebuilds

## Architecture

### Three-Stage Processing Pipeline

```
Content → Transformers → Filters → Emitters → Output
```

1. **Transformers** - Parse and transform Markdown content (frontmatter, LaTeX, syntax highlighting)
2. **Filters** - Determine which content to publish (remove drafts, etc.)
3. **Emitters** - Generate output files (HTML pages, RSS feeds, assets)

### Key Directories

- `/quartz/` - Core framework code
- `/content/` - User content (Markdown files)
- `/docs/` - Documentation
- `/public/` - Generated output
- `/quartz/components/` - UI components (Preact/JSX)
- `/quartz/plugins/` - Content processing plugins
- `/quartz/util/` - Utility functions

### Build System

- **Runtime**: Node.js v22+ with npm v10.9.2+
- **Language**: TypeScript with JSX/TSX
- **Frontend**: Preact for components
- **Bundler**: esbuild for transpilation
- **Styling**: SCSS with Lightning CSS
- **Content**: Unified ecosystem (remark/rehype) for Markdown

## Component System

### Component Architecture

Components are functions that return JSX-rendering functions with this pattern:

```typescript
export default (() => {
  function ComponentName(props: QuartzComponentProps) {
    return <div>...</div>
  }

  ComponentName.css = "styles.scss"
  ComponentName.beforeDOMLoaded = "script.inline.ts"
  return ComponentName
}) satisfies QuartzComponentConstructor
```

### Component Props

All components receive `QuartzComponentProps`:

- `fileData` - Current file metadata
- `cfg` - Site configuration
- `tree` - Content tree structure
- `allFiles` - All site files

### Layout System

- **Shared Layout** (`quartz.layout.ts`) - Components used across all pages
- **Content Pages** - Layout for individual content pages
- **List Pages** - Layout for tag/folder listing pages
- **Responsive** - MobileOnly/DesktopOnly wrapper components

## Plugin Development

### Plugin Types

- **QuartzTransformerPlugin** - Transform content during processing
- **QuartzFilterPlugin** - Filter which content gets published
- **QuartzEmitterPlugin** - Generate output files

### Plugin Configuration

Plugins are configured in `quartz.config.ts` in order of execution:

```typescript
plugins: {
  transformers: [Plugin.FrontMatter(), Plugin.SyntaxHighlighting(), ...],
  filters: [Plugin.RemoveDrafts()],
  emitters: [Plugin.ComponentResources(), Plugin.ContentPage(), ...]
}
```

## Configuration Files

### Primary Configuration

- **`quartz.config.ts`** - Main site configuration (theme, plugins, analytics)
- **`quartz.layout.ts`** - Component layout configuration
- **`package.json`** - Dependencies and npm scripts
- **`tsconfig.json`** - TypeScript configuration

### Configuration Features

- Theme customization (fonts, colors, typography)
- Analytics integration (Google, Plausible, Umami, etc.)
- Plugin configuration and ordering
- SPA routing and popover previews
- Internationalization support

## Testing

### Test Structure

- **Test Runner**: Node.js built-in test runner with `tsx --test`
- **Location**: Tests are co-located with source files (`.test.ts` suffix)
- **Type Safety**: TypeScript compiler validates types with `tsc --noEmit`
- **Code Style**: Prettier ensures consistent formatting

### Current Test Coverage

- Path utilities (`/quartz/util/path.test.ts`)
- File tree operations (`/quartz/util/fileTrie.test.ts`)

## Key Patterns

### Functional Architecture

- Immutable content transformations
- Pure functions for content processing
- Plugin-based extensibility
- Type-safe configuration

### Performance Optimizations

- Incremental builds with change detection
- Worker threads for parallel processing (>128 files)
- Static resource bundling and optimization
- Client-side SPA routing with `micromorph`

### Development Experience

- Hot reload via WebSocket
- TypeScript-first development
- Comprehensive error handling
- Extensive documentation

## Content Processing

### Supported Features

- Wikilinks and transclusions
- LaTeX math rendering (KaTeX/MathJax)
- Syntax highlighting (Shiki)
- Citations and bibliographies
- Mermaid diagrams
- Callouts and admonitions
- Obsidian compatibility

### File Processing

Content files support:

- Frontmatter (YAML/TOML)
- Multiple date formats
- Custom metadata
- Draft status
- Tag systems
