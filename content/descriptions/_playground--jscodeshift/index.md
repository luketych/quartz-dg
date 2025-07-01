## Objective: Auto-Inject and Remove Log Statements in a Codebase

We want a codemod system that automatically injects and removes logging statements in a clean, centralized, and maintainable way.

---

### Primary Goals

1. Inject logging at:

   * Top of every file
   * Start and end of every function

2. Logs should be inserted with a clear comment marker (e.g., `// @auto-log`) so they can be easily removed later.

3. Use a centralized logging module so the logging mechanism can be changed easily without modifying the codemod.

4. Be able to remove all injected logs automatically.

---

## Logging Design

Create a central logger module:

```js
// logger.js
export const log = {
  file: (filename) => console.log(`[LOG][FILE] ${filename}`),
  enter: (fn) => console.log(`[LOG][ENTER] ${fn}`),
  exit: (fn) => console.log(`[LOG][EXIT] ${fn}`),
};
```

All codemod-injected logs will use this `log` object. This makes future swapping (e.g., to `pino`, `debug`, etc.) easy.

---

## File: `inject-logs.js` (jscodeshift transformer)

### Features

* Adds `import { log } from './logger'` if missing.
* Inserts `log.file(__filename)` at the top of each file.
* Inserts `log.enter('funcName')` at the start of each function body.
* Inserts `log.exit('funcName')` at the end of each function body.
* Marks all injected lines with a `// @auto-log` comment.

### Run with:

```bash
jscodeshift -t inject-logs.js src/
```

---

## File: `remove-logs.js` (jscodeshift transformer)

### Features

* Removes all lines containing the comment `@auto-log`

### Run with:

```bash
jscodeshift -t remove-logs.js src/
```

---

## File: `inject-logs.js` (full script)

(See code snippet in ChatGPT conversation. This script uses jscodeshift to locate function declarations/expressions/arrow functions and injects logging.)

---

## File: `remove-logs.js` (full script)

(See code snippet in ChatGPT conversation. This script scans for `@auto-log` comment markers and removes those statements.)

---

## Next Steps for Implementation

1. Copy the provided code into the respective files.
2. Test on a small JS/TS codebase first.
3. Adjust file paths, function name extraction, or logger structure as needed.
4. Commit changes before running codemods in case of bugs.

---

Let the next developer or LLM read this file and implement the full toolchain.

