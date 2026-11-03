import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const base = process.argv[2];
assert(base, 'Usage: npm test -- http://127.0.0.1:4321');
const origin = new URL(base).origin;
const work = await (await fetch(new URL('/work.json', base))).json();
assert.equal(work.scenes.length, 30, 'Acceptance work must contain 30 scenes');
const browser = await chromium.launch({headless: true});
const errors = [];
try {
  const page = await browser.newPage();
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
  await page.goto(base);
  const theme = await page.locator('html').getAttribute('data-theme');
  await page.getByRole('button', {name: 'Switch day or night theme'}).click();
  const changedTheme = await page.locator('html').getAttribute('data-theme');
  assert.notEqual(changedTheme, theme);
  await page.reload();
  assert.equal(await page.locator('html').getAttribute('data-theme'), changedTheme);

  const routes = ['/', ...work.scenes.map(item => `/scenes/${item.scene_id}/`),
    ...work.endings.map(item => `/endings/${item.ending_id}/`),
    ...work.artifacts.map(item => `/artifacts/${item.artifact_id}/`)];
  const checked = new Set();
  for (const route of routes) {
    const response = await page.goto(new URL(route, base).href);
    assert(response.ok(), `Missing page ${route}`);
    assert(await page.locator('h1').textContent(), `Missing title ${route}`);
    if (route.startsWith('/artifacts/')) assert(await page.locator('.artifact-body').textContent());
    for (const href of await page.locator('a[href]').evaluateAll(items => items.map(item => item.href))) {
      const url = new URL(href);
      if (url.origin !== origin || checked.has(url.href)) continue;
      checked.add(url.href);
      assert((await page.request.get(url.href)).ok(), `Broken internal link ${url.href}`);
    }
  }

  // Explore visible choices using the product's state effects and saved reader state.
  await page.evaluate(() => localStorage.clear());
  const queue = [{url: new URL(`/scenes/${work.entry_content_id}/`, base).href, storage: {}}];
  const visited = new Set();
  let path = null;
  for (let count = 0; queue.length && count < 2000; count++) {
    const task = queue.shift();
    await page.goto(base);
    await page.evaluate(storage => { localStorage.clear(); for (const [key, value] of Object.entries(storage)) localStorage.setItem(key, value); }, task.storage);
    await page.goto(task.url);
    const snapshot = await page.evaluate(() => Object.fromEntries(Object.entries(localStorage)));
    const stateKey = Object.keys(snapshot).find(key => key.endsWith(':reader-state:v1'));
    assert(stateKey, 'Reader state was not persisted');
    const state = JSON.parse(snapshot[stateKey]);
    const identity = `${new URL(task.url).pathname}:${JSON.stringify(state.values)}`;
    if (visited.has(identity)) continue;
    visited.add(identity);
    await page.reload();
    assert.deepEqual(JSON.parse(await page.evaluate(key => localStorage.getItem(key), stateKey)), state, 'Reload changed reader state');
    if (new URL(task.url).pathname.startsWith('/endings/')) { path = state.path; break; }
    const links = await page.locator('.choice:visible').evaluateAll(items => items.map(item => item.href));
    for (const href of links) {
      await page.evaluate(storage => { for (const [key, value] of Object.entries(storage)) localStorage.setItem(key, value); }, snapshot);
      await page.goto(task.url);
      const locator = page.locator('.choice:visible');
      const index = (await locator.evaluateAll(items => items.map(item => item.href))).indexOf(href);
      if (index < 0) continue;
      await locator.nth(index).click();
      await page.waitForLoadState();
      queue.push({url: page.url(), storage: await page.evaluate(() => Object.fromEntries(Object.entries(localStorage)))});
    }
  }
  assert(path, 'No condition-valid opening-to-ending playthrough within 2,000 distinct states');
  assert.deepEqual(errors, [], 'Browser errors');
  console.log(JSON.stringify({scenes: work.scenes.length, endings: work.endings.length, artifacts: work.artifacts.length,
    pages: routes.length, internal_links: checked.size, theme_persisted: true, state_persisted: true, ending_path: path, browser_errors: errors}, null, 2));
} finally {
  await browser.close();
}
