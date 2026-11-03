# Browser acceptance

Test-only Playwright and Chromium; neither is a generated reader dependency.

```sh
npm ci
PLAYWRIGHT_BROWSERS_PATH=/tmp/cathedrals-playwright-browsers npx playwright install chromium
PLAYWRIGHT_BROWSERS_PATH=/tmp/cathedrals-playwright-browsers npm test -- http://127.0.0.1:4327
```

Serve a complete 30-scene publication first. The check visits all scene, ending and evidence pages, verifies internal links, persists theme and reader state across reloads, follows visible choices to an ending and rejects console errors. It explores at most 2,000 distinct content/state combinations and fails explicitly if it cannot establish a valid path within that bound.
