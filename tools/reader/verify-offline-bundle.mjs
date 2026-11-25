import fs from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
import { closeBrowser } from './browser-cleanup.mjs';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.HANDBOOK_NODE_MODULES
  ? path.join(process.env.HANDBOOK_NODE_MODULES, 'playwright')
  : 'playwright');
const root = path.resolve(process.argv[2]);
const chrome = process.env.HANDBOOK_CHROMIUM || [
  chromium.executablePath(), '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome', '/usr/bin/chromium',
].find(file => file && existsSync(file));

async function followLocal(page, selector, navigate = true) {
  const href = await page.locator(selector).first().evaluate(link => link.href);
  const url = new URL(href);
  const file = fileURLToPath(url);
  const relative = path.relative(root, file);
  if (relative.startsWith('..' + path.sep) || relative === '..' || path.isAbsolute(relative)) {
    throw new Error(`Offline link goes outside the bundle: ${href}`);
  }
  if (!(await fs.stat(file)).isFile()) throw new Error(`Offline link is not a file: ${href}`);
  if (navigate) await page.goto(href);
}

const browser = await chromium.launch({ headless: true, executablePath: chrome });
try {
  const page = await browser.newPage({ offline: true, viewport: { width: 390, height: 844 } });
  page.setDefaultTimeout(7500);
  const errors = [];
  const network = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('request', request => {
    if (/^https?:/.test(request.url())) network.push(request.url());
  });
  await page.goto(pathToFileURL(path.join(root, 'index.html')).href);
  await followLocal(page, 'a[href$="00-overview.html"]');
  await page.keyboard.press('/');
  await page.locator('#qch-global-search-input').fill('表面码');
  await followLocal(page, '#qch-search-results .search-item', false);
  await page.keyboard.press('Escape');
  await followLocal(page, 'a[href$="labs/foundations.html"]');
  await followLocal(page, 'a[href$="codes/foundations/diagnostic_lab.py"]', false);
  await page.goto(pathToFileURL(path.join(root, 'lab/quantum-lab.html')).href);
  await page.locator('#tab-grover').click();
  await page.locator('#panel-grover').waitFor({ state: 'visible' });
  if (errors.length || network.length) {
    throw new Error(`Offline browser validation failed: ${JSON.stringify({ errors, network })}`);
  }
  console.log('Extracted Web ZIP passed: chapter, search, code link, and Grover, no network requests.');
} catch (error) {
  process.exitCode = 1;
  throw error;
} finally {
  await closeBrowser(browser);
}
