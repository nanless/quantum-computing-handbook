import fs from 'node:fs/promises';
import fsSync from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
import { readingPlan } from './reading-order.mjs';
import { closeBrowser } from './browser-cleanup.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.HANDBOOK_NODE_MODULES
  ? path.join(process.env.HANDBOOK_NODE_MODULES, 'playwright')
  : 'playwright');

const CHROME_FALLBACKS = [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
];
const browserOptions = { headless: true };
if (process.env.HANDBOOK_CHROMIUM) {
  browserOptions.executablePath = process.env.HANDBOOK_CHROMIUM;
} else {
  let pwChromium = '';
  try { pwChromium = chromium.executablePath(); } catch {}
  if (pwChromium && fsSync.existsSync(pwChromium)) {
    browserOptions.executablePath = pwChromium;
  } else {
    const sysChrome = CHROME_FALLBACKS.find(p => fsSync.existsSync(p));
    if (sysChrome) browserOptions.executablePath = sysChrome;
  }
}

// Decode an 8-bit RGB/RGBA non-interlaced Playwright screenshot PNG and compute average luminance (0..255).
function measurePngAvgLum(buf) {
  let pos = 8;
  let width = 0, height = 0, colorType = 6;
  const idatParts = [];
  while (pos + 8 <= buf.length) {
    const len = buf.readUInt32BE(pos);
    const type = buf.toString('ascii', pos + 4, pos + 8);
    const dataStart = pos + 8;
    if (type === 'IHDR') {
      width = buf.readUInt32BE(dataStart);
      height = buf.readUInt32BE(dataStart + 4);
      colorType = buf[dataStart + 9];
    } else if (type === 'IDAT') {
      idatParts.push(buf.subarray(dataStart, dataStart + len));
    } else if (type === 'IEND') {
      break;
    }
    pos = dataStart + len + 4;
  }
  const bpp = colorType === 6 ? 4 : colorType === 2 ? 3 : 4;
  const stride = width * bpp;
  const raw = zlib.inflateSync(Buffer.concat(idatParts));
  const prev = new Uint8Array(stride);
  const curr = new Uint8Array(stride);
  let lumSum = 0;
  let count = 0;
  const paeth = (a, b, c) => {
    const p = a + b - c;
    const pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c);
    return pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
  };
  for (let y = 0; y < height; y++) {
    const rowOff = y * (stride + 1);
    const filter = raw[rowOff];
    for (let x = 0; x < stride; x++) {
      const v = raw[rowOff + 1 + x];
      const a = x >= bpp ? curr[x - bpp] : 0;
      const b = prev[x];
      const c = x >= bpp ? prev[x - bpp] : 0;
      if (filter === 0) curr[x] = v;
      else if (filter === 1) curr[x] = (v + a) & 255;
      else if (filter === 2) curr[x] = (v + b) & 255;
      else if (filter === 3) curr[x] = (v + ((a + b) >> 1)) & 255;
      else curr[x] = (v + paeth(a, b, c)) & 255;
    }
    if (y % 2 === 0) {
      for (let x = 0; x < stride; x += bpp * 2) {
        const r = curr[x], g = curr[x + 1], bl = curr[x + 2];
        lumSum += 0.2126 * r + 0.7152 * g + 0.0722 * bl;
        count++;
      }
    }
    prev.set(curr);
  }
  return count ? lumSum / count : 255;
}

const report = {
  generatedAt: new Date().toISOString(),
  pages: [],
  labChecks: [],
  darkSvgChecks: [],
  searchChecks: [],
  searchIndexGate: null,
  flowNodeGate: null,
  errors: [],
  externalRequests: [],
  screenshots: [],
};
const build = JSON.parse(await fs.readFile(path.join(root, 'work/research/reader-build-report.json'), 'utf8'));
const expectedReading = readingPlan(build.pages.filter(p => /^reader\/(?:quantum-mechanics\/)?\d\d-/.test(p.output)).map(p => p.output)).sequence;
if (JSON.stringify(build.readingOrder) !== JSON.stringify(expectedReading)) {
  throw new Error('Build reading order differs from the pedagogical plan');
}
const edition = (await fs.readFile(path.join(root, 'handbook/README.md'), 'utf8')).match(/^>\s*版本：(\d{4}-\d{2}-\d{2})/m)?.[1];
if (!edition || Number.isNaN(Date.parse(edition + 'T00:00:00Z')) || new Date(edition + 'T00:00:00Z').toISOString().slice(0, 10) !== edition) {
  throw new Error('handbook/README.md must declare a valid YYYY-MM-DD edition');
}
const digest = value => crypto.createHash('sha256').update(value).digest('hex');

// Scheme C static hygiene gates: no STYLE.html, no reader/research, only .woff2 KaTeX fonts.
if (fsSync.existsSync(path.join(root, 'reader/STYLE.html'))) {
  report.errors.push({ file: 'reader/STYLE.html', message: 'internal STYLE.html must be excluded from reader/' });
}
if (fsSync.existsSync(path.join(root, 'reader/research'))) {
  report.errors.push({ file: 'reader/research', message: 'work/research archive must not be copied into reader/' });
}
const katexFontsDir = path.join(root, 'reader/assets/katex/fonts');
if (fsSync.existsSync(katexFontsDir)) {
  const nonWoff2 = (await fs.readdir(katexFontsDir)).filter(f => !f.endsWith('.woff2'));
  if (nonWoff2.length) {
    report.errors.push({ file: 'reader/assets/katex/fonts', message: 'legacy non-woff2 fonts present', nonWoff2 });
  }
} else {
  report.errors.push({ file: 'reader/assets/katex/fonts', message: 'missing KaTeX woff2 fonts directory' });
}

// Permanent Gate: 100% of reader/assets/search-index.js URLs & #anchors must exist in generated HTML.
{
  const searchIndexPath = path.join(root, 'reader/assets/search-index.js');
  const readerRoot = path.join(root, 'reader');
  const htmlCache = new Map();
  let broken = 0;
  let total = 0;
  if (!fsSync.existsSync(searchIndexPath)) {
    report.errors.push({ file: 'reader/assets/search-index.js', message: 'missing search-index.js' });
  } else {
    const rawIdx = await fs.readFile(searchIndexPath, 'utf8');
    const jsonPayload = rawIdx.replace(/^\s*window\.__QCH_SEARCH_INDEX__\s*=\s*/, '').replace(/;\s*$/, '');
    const entries = JSON.parse(jsonPayload);
    if (!Array.isArray(entries) || entries.length === 0) {
      report.errors.push({ file: 'reader/assets/search-index.js', message: 'search-index.js is empty or invalid' });
    } else {
      total = entries.length;
      const sampleBroken = [];
      for (const item of entries) {
        const rawUrl = String(item.u || item.url || '').trim();
        const [relFile, rawHash = ''] = rawUrl.split('#');
        const absTarget = path.resolve(readerRoot, relFile);
        if (!relFile || !absTarget.startsWith(readerRoot + path.sep) || !fsSync.existsSync(absTarget)) {
          broken++;
          if (sampleBroken.length < 20) sampleBroken.push({ u: rawUrl, reason: 'missing file' });
          continue;
        }
        if (rawHash) {
          let anchor;
          try { anchor = decodeURIComponent(rawHash); } catch { anchor = rawHash; }
          let htmlText = htmlCache.get(absTarget);
          if (htmlText === undefined) {
            htmlText = await fs.readFile(absTarget, 'utf8');
            htmlCache.set(absTarget, htmlText);
          }
          if (!htmlText.includes(`id="${anchor}"`) && !htmlText.includes(`id='${anchor}'`)) {
            broken++;
            if (sampleBroken.length < 20) sampleBroken.push({ u: rawUrl, title: item.t, reason: `missing anchor #${anchor}` });
          }
        }
      }
      if (broken > 0) {
        report.errors.push({
          file: 'reader/assets/search-index.js',
          message: `search-index gate failed: ${broken}/${total} entries have broken URL or #anchor`,
          samples: sampleBroken,
        });
      }
    }
  }
  report.searchIndexGate = { total, broken };
}

for (const [file, expected] of Object.entries(build.inputHashes || {})) {
  if (digest(await fs.readFile(path.join(root, file))) !== expected) {
    report.errors.push({ file, message: 'build input changed; rebuild required' });
  }
}
for (const entry of build.pages) {
  for (const [key, hash] of [['source', 'sourceSha256'], ['output', 'outputSha256']]) {
    if (digest(await fs.readFile(path.join(root, entry[key]))) !== entry[hash]) {
      report.errors.push({ file: entry[key], message: 'source/output hash differs from build' });
    }
  }
}
for (const entry of build.codeCopies || []) {
  if (digest(await fs.readFile(path.join(root, entry.output))) !== entry.outputSha256) {
    report.errors.push({ file: entry.output, message: 'copied code differs from build' });
  }
}

const shots = path.join(root, 'work/rendered');
await fs.mkdir(shots, { recursive: true });
const browser = await chromium.launch(browserOptions);

const screenshotTargets = new Set([
  'reader/index.html',
  'reader/02-single-qubit.html',
  'reader/03-multiple-qubits.html',
  'reader/04-circuits-protocols.html',
  'reader/07-algorithms.html',
  'reader/08-applications.html',
  'reader/09-hardware.html',
  'reader/12-security-network-frontiers.html',
  'reader/16-advanced-algorithms-verification.html',
  'reader/18-channels-capacities-complexity.html',
  'reader/20-quantum-sensing-metrology.html',
  'reader/21-stabilizer-classical-simulation.html',
  'reader/appendices/notation.html',
  'reader/appendices/prerequisites.html',
  'reader/appendices/software-practice.html',
]);

try {
  for (const width of [1440, 390]) {
    const page = await browser.newPage({ viewport: { width, height: 1000 }, deviceScaleFactor: 1 });
    page.on('pageerror', e => report.errors.push({ width, type: 'javascript', message: e.message }));
    page.on('console', msg => {
      if (msg.type() === 'error') {
        report.errors.push({ width, type: 'console', message: msg.text(), url: page.url() });
      }
    });
    page.on('requestfailed', req => {
      const errText = req.failure()?.errorText || '';
      if (req.url().startsWith('blob:') && errText === 'net::ERR_ABORTED') return;
      report.errors.push({ width, type: 'requestfailed', url: req.url(), failure: errText });
    });
    page.on('request', req => { if (/^https?:/.test(req.url())) report.externalRequests.push(req.url()); });

    for (const entry of build.pages) {
      await page.goto(pathToFileURL(path.join(root, entry.output)).href);
      await page.evaluate(async () => {
        await document.fonts.ready;
        for (const img of document.images) {
          img.loading = 'eager';
          await img.decode().catch(() => {});
        }
      });

      if (width === 1440) {
        const isFoundation = /^reader\/quantum-mechanics\/\d/.test(entry.output);
        const isMain = /^reader\/\d/.test(entry.output);
        if (isFoundation || isMain) {
          const sequence = expectedReading;
          const at = sequence.indexOf(entry.output);
          const expected = [sequence[at - 1], sequence[at + 1]].filter(Boolean).map(p => pathToFileURL(path.join(root, p)).href);
          const actual = await page.locator('.page-turn a').evaluateAll(links => links.map(a => a.href));
          if (JSON.stringify(actual) !== JSON.stringify(expected)) {
            report.errors.push({ file: entry.output, message: 'pedagogical previous/next navigation differs', expected, actual });
          }
        }
        if (await page.locator('.chapters nav a[href$="quantum-mechanics/index.html"]').count() !== 1) {
          report.errors.push({ file: entry.output, message: 'foundation guide missing from navigation' });
        }
        const sidebar = await page.locator('.chapters nav a').evaluateAll(links =>
          links.map(a => a.href).filter(href => /\/(?:quantum-mechanics\/)?\d\d-[^/]+\.html$/.test(href)),
        );
        const expectedSidebar = expectedReading.map(file => pathToFileURL(path.join(root, file)).href);
        if (JSON.stringify(sidebar) !== JSON.stringify(expectedSidebar)) {
          report.errors.push({ file: entry.output, message: 'sidebar order differs; mathematics must precede dependent chapters' });
        }
      }

      const result = await page.evaluate(() => {
        const failures = [];
        const mainArticle = document.querySelector('main > article');
        const prose = document.createTreeWalker(mainArticle, NodeFilter.SHOW_TEXT);
        for (let text = prose.nextNode(); text; text = prose.nextNode()) {
          if (!text.parentElement.closest('pre,code,.katex') && text.textContent.includes('**')) {
            failures.push('unrendered emphasis in prose: ' + text.textContent.slice(0, 120));
          }
        }
        if (document.documentElement.scrollWidth > innerWidth + 2) {
          const offenders = [...document.querySelectorAll('main > article *')].filter(e => {
            if (e.getBoundingClientRect().right <= innerWidth + 2) return false;
            for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) {
              if (['auto', 'scroll', 'hidden'].includes(getComputedStyle(p).overflowX)) return false;
            }
            return true;
          }).slice(0, 5).map(e => ({ tag: e.tagName, class: e.className?.baseVal ?? e.className, text: e.textContent.slice(0, 100), right: e.getBoundingClientRect().right }));
          const wide = [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > innerWidth + 2)
            .sort((a, b) => b.getBoundingClientRect().right - a.getBoundingClientRect().right)
            .slice(0, 4)
            .map(e => ({ tag: e.tagName, class: e.className?.baseVal ?? e.className, right: e.getBoundingClientRect().right }));
          failures.push('page horizontally overflows: ' + JSON.stringify({ width: document.documentElement.scrollWidth, offenders, wide }));
        }
        for (const img of document.images) if (!img.complete || !img.naturalWidth) failures.push('broken image: ' + img.getAttribute('src'));
        if (document.querySelector('.math-error,.katex-error,pre code.language-mermaid,[data-handbook-math]')) failures.push('unrendered math/diagram');
        if (document.querySelector('.katex-mathml')) failures.push('unexpected .katex-mathml under Scheme C output:html');
        if (document.styleSheets.length < 2 || getComputedStyle(document.querySelector('header')).position !== 'sticky') failures.push('reader CSS not loaded');
        const katexStrut = document.querySelector('.katex .strut');
        if (katexStrut && getComputedStyle(katexStrut).display !== 'inline-block') failures.push('KaTeX CSS not loaded');
        const katexNodes = [...document.querySelectorAll('main > article .katex')];
        if (katexNodes.some(el => !el.querySelector('.katex-html'))) failures.push('KaTeX node missing .katex-html');
        const displayNodes = [...document.querySelectorAll('main > article .katex-display')];
        const displayTex = displayNodes.map(e => e.getAttribute('data-tex') || '');
        if (displayTex.some(t => !t)) failures.push('display math missing data-tex attribute');
        const navsWithoutLabel = [...document.querySelectorAll('.chapters nav, .contents nav')].filter(n => !n.getAttribute('aria-label'));
        if (navsWithoutLabel.length) failures.push('sidebar/toc nav missing aria-label');
        const ids = [...document.querySelectorAll('[id]')].map(e => e.id);
        if (new Set(ids).size !== ids.length) failures.push('duplicate HTML id');
        for (const t of document.querySelectorAll('table')) {
          const expected = t.rows[0]?.cells.length;
          for (const r of t.rows) if (r.cells.length !== expected) failures.push('table row width mismatch');
        }
        const headings = [...document.querySelectorAll('main > article h1,main > article h2,main > article h3,main > article h4,main > article h5,main > article h6')].map(e => ({ text: e.textContent, id: e.id }));
        const expectedSections = [...document.querySelectorAll('main > article h2,main > article h3')].map(e => '#' + e.id);
        for (const nav of document.querySelectorAll('.contents nav,.inline-contents nav')) {
          if (JSON.stringify([...nav.querySelectorAll('a')].map(a => a.getAttribute('href'))) !== JSON.stringify(expectedSections)) {
            failures.push('section navigation differs from H2/H3 sequence');
          }
        }
        for (const a of document.querySelectorAll('.image-open')) {
          if (a.href !== a.querySelector('img')?.src) failures.push('original-size image link differs from image');
        }
        for (const figure of document.querySelectorAll('figure.flowchart')) {
          const alt = figure.querySelector('img')?.getAttribute('alt') || '';
          if (!alt || /流程关系图\s*\d/.test(alt) || !figure.querySelector('figcaption')?.textContent.includes(alt)) {
            failures.push('flowchart needs a specific matching title and text alternative');
          }
        }
        for (const e of document.querySelectorAll('.table-scroll,.katex-display,.flowchart,.flowchart-scroll,.math-inline,.scientific-svg')) {
          if (e.scrollWidth > e.clientWidth + 2) {
            const before = e.scrollLeft;
            e.scrollLeft = e.scrollWidth;
            if (Math.abs(e.scrollLeft - (e.scrollWidth - e.clientWidth)) > 2) failures.push('scroll area cannot reach right edge');
            e.scrollLeft = before;
          }
        }
        return {
          failures,
          displayTex,
          formulas: katexNodes.length,
          images: document.images.length,
          headings,
          links: [...document.querySelectorAll('a[href]')].map(a => a.href),
          footer: document.querySelector('main footer')?.textContent || '',
        };
      });

      report.pages.push({ file: entry.output, width, formulas: result.formulas, images: result.images });
      for (const message of result.failures) report.errors.push({ file: entry.output, width, message });
      if (!result.footer.includes(`${edition} 版`)) report.errors.push({ file: entry.output, width, message: 'reader footer edition differs from handbook README' });
      if (result.formulas !== entry.formulas) report.errors.push({ file: entry.output, width, message: 'formula count mismatch', expected: entry.formulas, actual: result.formulas });
      if (result.displayTex.length !== entry.displayFormulas) report.errors.push({ file: entry.output, width, message: 'display formula count mismatch', expected: entry.displayFormulas, actual: result.displayTex.length });
      if (digest(JSON.stringify(result.displayTex)) !== entry.displayMathDigest) report.errors.push({ file: entry.output, width, message: 'display formula content or order mismatch' });
      if (JSON.stringify(result.headings.map(h => h.id)) !== JSON.stringify(entry.headingIds)) report.errors.push({ file: entry.output, width, message: 'heading sequence mismatch' });

      if (width === 1440) {
        for (const href of new Set(result.links)) {
          if (!href.startsWith('file:')) continue;
          const u = new URL(href);
          const fragment = decodeURIComponent(u.hash.slice(1));
          u.hash = '';
          const target = fileURLToPath(u);
          try {
            if (!target.startsWith(path.join(root, 'reader') + path.sep)) {
              report.errors.push({ file: entry.output, message: 'local link is not portable: ' + href });
            }
            await fs.access(target);
            if (fragment && target.endsWith('.html')) {
              const html = await fs.readFile(target, 'utf8');
              if (!html.includes(`id="${fragment}"`)) report.errors.push({ file: entry.output, message: 'broken anchor: ' + href });
            }
          } catch {
            report.errors.push({ file: entry.output, message: 'broken file: ' + href });
          }
        }
      }

      if (screenshotTargets.has(entry.output) || entry.output.startsWith('reader/quantum-mechanics/') || entry.output.startsWith('reader/labs/')) {
        if (width === 390) await page.locator('.chapters details').evaluate(e => { e.open = false; });
        const name = (entry.output.startsWith('reader/quantum-mechanics/') ? 'qm-' : entry.output.startsWith('reader/labs/') ? 'lab-' : '') + path.basename(entry.output, '.html') + '-' + width + '.png';
        await page.screenshot({ path: path.join(shots, name) });
        report.screenshots.push('work/rendered/' + name);
      }
    }

    // Check flagship course home, Cmd+K global search, sidebar search, dark mode, and hero workbench.
    await page.goto(pathToFileURL(path.join(root, 'reader/index.html')).href);
    if (width === 1440) {
      await page.evaluate(async () => {
        await document.fonts.ready;
        await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      });
      // Verify 4-mode flagship hero workbench interaction (phi180, decohere, phi0).
      await page.locator('#qch-hero-sim [data-phase="180"]').click();
      let heroCheck = await page.evaluate(() => ({
        p0: document.getElementById('qch-hero-p0')?.textContent,
        p1: document.getElementById('qch-hero-p1')?.textContent,
        mode: document.getElementById('qch-hero-sim')?.dataset.mode,
      }));
      if (heroCheck.p0 !== '0%' || heroCheck.p1 !== '100%') {
        report.errors.push({ width, file: 'reader/index.html', message: 'hero workbench phi180 failed', heroCheck });
      }
      await page.locator('#qch-hero-sim [data-phase="decohere"]').click();
      heroCheck = await page.evaluate(() => ({
        p0: document.getElementById('qch-hero-p0')?.textContent,
        p1: document.getElementById('qch-hero-p1')?.textContent,
        mode: document.getElementById('qch-hero-sim')?.dataset.mode,
      }));
      if (heroCheck.p0 !== '50%' || heroCheck.p1 !== '50%' || heroCheck.mode !== 'decohere') {
        report.errors.push({ width, file: 'reader/index.html', message: 'hero workbench decohere failed', heroCheck });
      }
      await page.locator('#qch-hero-sim [data-phase="0"]').click();

      // Verify CHSH and d=3 Surface Code home interactive preview cards.
      await page.locator('.course-chsh-widget [data-course-chsh="classic"]').click();
      if ((await page.locator('.course-chsh-widget').getAttribute('data-chsh')) !== 'classic') {
        report.errors.push({ width, file: 'reader/index.html', message: 'course-home CHSH preview toggle failed' });
      }
      await page.locator('.course-chsh-widget [data-course-chsh="quantum"]').click();
      await page.locator('.course-qec-widget [data-course-qec="double"]').click();
      if ((await page.locator('.course-qec-widget').getAttribute('data-qec')) !== 'double') {
        report.errors.push({ width, file: 'reader/index.html', message: 'course-home QEC preview toggle failed' });
      }
      await page.locator('.course-qec-widget [data-course-qec="single"]').click();

      // Verify offline Cmd/Ctrl+K full-book search modal across representative terms.
      await page.locator('[data-open-search]').first().click();
      const searchOpen = await page.locator('#qch-search-dialog').evaluate(d => d.open);
      if (!searchOpen) {
        report.errors.push({ width, file: 'reader/index.html', message: 'global search modal did not open' });
      } else {
        for (const query of ['表面码', 'Barren Plateau', 'Weyl 室', 'Grover', 'CHSH']) {
          await page.locator('#qch-global-search-input').fill(query);
          const hitCount = await page.locator('#qch-search-results .search-item').count();
          report.searchChecks.push({ query, hitCount });
          if (hitCount < 1) {
            report.errors.push({ width, file: 'reader/index.html', message: `global search returned 0 hits for "${query}"` });
          }
        }
        await page.locator('#qch-search-dialog [data-search-close]').click();
      }

      // Switch to dark mode via #theme-toggle and capture 1440px dark screenshot.
      await page.locator('#theme-toggle').click();
      const darkTheme = await page.evaluate(async () => {
        await document.fonts.ready;
        await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
        return document.documentElement.getAttribute('data-theme');
      });
      if (darkTheme !== 'dark') {
        report.errors.push({ width, file: 'reader/index.html', message: 'theme toggle did not activate dark mode', actual: darkTheme });
      }
      await page.screenshot({ path: path.join(shots, 'index-1440-dark.png') });
      report.screenshots.push('work/rendered/index-1440-dark.png');
      // Restore light mode so subsequent checks stay clean.
      await page.locator('#theme-toggle').click();
      await page.evaluate(() => {
        try {
          localStorage.removeItem('qch-theme');
          localStorage.removeItem('qch-lab-theme');
        } catch {}
      });
    }
    if (width === 390) {
      // Mobile sidebar details must default to collapsed (recovers first viewport height).
      const mobileOpenByDefault = await page.locator('.chapters > details').evaluate(e => e.open);
      if (mobileOpenByDefault) {
        report.errors.push({ width, file: 'reader/index.html', message: 'mobile .chapters details must be collapsed by default' });
      }
      await page.locator('.chapters > details > summary').click();
      const name = 'index-390-navigation-open.png';
      await page.screenshot({ path: path.join(shots, name) });
      report.screenshots.push('work/rendered/' + name);
    }

    await page.locator('#nav-search').fill('__NO_MATCH_QCH__');
    const visibleEmptyLabels = await page.locator('.chapters nav .nav-label:visible').count();
    if (visibleEmptyLabels !== 0) {
      report.errors.push({ width, message: 'empty .nav-label headings should be hidden when #nav-search has 0 hits', visibleEmptyLabels });
    }
    await page.locator('#nav-search').fill('单量子比特');
    if (await page.locator('.chapters nav a:visible').count() !== 1) report.errors.push({ width, message: 'chapter search should identify chapter 02' });
    await page.locator('#nav-search').fill('入门先修');
    if (await page.locator('.chapters nav a:visible').count() !== 1) report.errors.push({ width, message: 'chapter search should identify prerequisite guide' });
    await page.locator('#nav-search').fill('');
    await page.locator('.chapters a[href="02-single-qubit.html"]').click();
    if (!page.url().endsWith('02-single-qubit.html')) report.errors.push({ width, message: 'chapter navigation failed' });

    if (width === 390) {
      await page.goto(pathToFileURL(path.join(root, 'reader/12-security-network-frontiers.html')).href);
      await page.locator('.inline-contents summary').click();
      await page.screenshot({ path: path.join(shots, '12-mobile-section-menu.png') });
      report.screenshots.push('work/rendered/12-mobile-section-menu.png');
      const section = page.locator('.inline-contents .toc-level-3').first();
      const destination = await section.getAttribute('href');
      await section.click();
      await page.waitForFunction(id => { const y = document.getElementById(id.slice(1)).getBoundingClientRect().top; return y >= 56 && y <= 150; }, destination, { timeout: 5000 }).catch(() => report.errors.push({ width, message: 'mobile heading did not settle below fixed header' }));
      const reached = await page.evaluate(id => ({ hash: decodeURIComponent(location.hash), open: document.querySelector('.inline-contents').open, top: document.getElementById(id.slice(1)).getBoundingClientRect().top }), destination);
      if (reached.hash !== destination || reached.open) report.errors.push({ width, message: 'mobile section navigation failed', reached });
      await page.screenshot({ path: path.join(shots, '12-mobile-section-arrival.png') });
      report.screenshots.push('work/rendered/12-mobile-section-arrival.png');
    }

    // Verify 6-module offline interactive quantum lab at both 1440px and 390px.
    const labPath = path.join(root, 'reader/lab/quantum-lab.html');
    const labErrorsBefore = report.errors.length;
    const labExternalBefore = report.externalRequests.length;
    await page.goto(pathToFileURL(labPath).href);
    const labState = await page.evaluate(async () => {
      await document.fonts.ready;
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      return {
        title: document.title,
        scrollWidth: document.documentElement.scrollWidth,
        innerWidth: window.innerWidth,
        svgCount: document.querySelectorAll('svg').length,
        controlsCount: document.querySelectorAll('button, input').length,
        tabCount: document.querySelectorAll('[role="tab"]').length,
      };
    });
    const labOverflow = labState.scrollWidth > labState.innerWidth + 2;
    if (labOverflow) {
      report.errors.push({ file: 'reader/lab/quantum-lab.html', width, message: 'interactive lab horizontally overflows', labState });
    }
    if (labState.svgCount < 1 || labState.controlsCount < 1 || labState.tabCount !== 6) {
      report.errors.push({ file: 'reader/lab/quantum-lab.html', width, message: 'interactive lab missing 6 modules/SVG/controls', labState });
    }
    if (width === 1440) {
      // Pure math kernel exactness verification for all 6 modules.
      const kernelFailures = await page.evaluate(() => {
        const errs = [];
        const M = window.QuantumLabModel;
        if (!M) return ['QuantumLabModel missing on window'];
        const approx = (a, b, tol, msg) => { if (Math.abs(a - b) > tol) errs.push(`${msg}: got ${a}, expected ${b}`); };
        // 1. MZI
        const mzi120 = M.mziMetrics((2 * Math.PI) / 3, 1);
        approx(mzi120.p0, 0.25, 1e-12, 'MZI 120deg p0');
        const mziMix = M.mziMetrics(Math.PI, 0);
        approx(mziMix.p0, 0.5, 1e-12, 'MZI V=0 p0');
        if (!mziMix.isMixed) errs.push('MZI V=0 should report isMixed=true');
        // 2. Bloch H -> S -> T & no negative zero
        let st = M.stateFromAngles(0, 0);
        st = M.applyGate(st, 'H');
        st = M.applyGate(st, 'S');
        st = M.applyGate(st, 'T');
        const bv = M.blochVector(st);
        approx(bv.rx, -Math.SQRT1_2, 1e-12, 'Bloch H->S->T rx');
        approx(bv.ry, Math.SQRT1_2, 1e-12, 'Bloch H->S->T ry');
        approx(bv.rz, 0, 1e-12, 'Bloch H->S->T rz');
        approx(bv.norm, 1, 1e-12, 'Bloch norm');
        if (M.fmtFixed(-1e-12, 3) !== '0.000') errs.push('fmtFixed produced negative zero');
        // 3. Ramsey
        const rp = M.ramseyPoint(1.5, 1.0, 1.5);
        approx(rp.vis, Math.exp(-1), 1e-12, 'Ramsey visibility at T2');
        approx(rp.pDecay, (1 - Math.exp(-1)) / 2, 1e-12, 'Ramsey pDecay at 1.5s');
        if (!(rp.envCorrect > rp.envPitfall)) errs.push('Ramsey correct envelope should exceed pitfall at 1.5s');
        // 4. Bell & CHSH
        const bm = M.bellWernerMetrics(Math.PI / 4, 1);
        approx(bm.entropyA, 1, 1e-12, 'Bell entropyA');
        approx(bm.concurrence, 1, 1e-12, 'Bell concurrence');
        approx(bm.rA.r, 0, 1e-12, 'Bell reduced Bloch length');
        const ch = M.chshCorrelations(Math.PI / 4, 1, 0, 90, 45, -45);
        approx(ch.S, 2 * Math.SQRT2, 1e-12, 'CHSH Tsirelson S');
        approx(ch.pWin, 0.5 + Math.SQRT2 / 4, 1e-12, 'CHSH win prob');
        const sim = M.simulateChshRounds(Math.PI / 4, 1, 0, 90, 45, -45, 1000, 20261125);
        if (!sim.beatsClassicCI) errs.push('CHSH 1000-round Wilson CI should beat 75%');
        // 5. Grover
        let g2 = M.groverStep(M.groverInit(2, [3]));
        approx(M.groverMetrics(g2).pGood, 1, 1e-12, 'Grover n=2 1-step pGood');
        let g3 = M.groverInit(3, [5]);
        g3 = M.groverStep(g3);
        g3 = M.groverStep(g3);
        approx(M.groverMetrics(g3).pGood, 0.9453125, 1e-12, 'Grover n=3 2-step pGood');
        g3 = M.groverStep(g3);
        const g3m = M.groverMetrics(g3);
        approx(g3m.pGood, 0.330078125, 1e-12, 'Grover n=3 3-step overshoot pGood');
        if (!g3m.isOvershot) errs.push('Grover n=3 step 3 must flag isOvershot');
        // 6. d=3 Surface Code: all 27 single-qubit errors corrected/degenerate, X4X5 & Z3Z6 logical flip
        for (let q = 0; q < 9; q++) {
          for (const p of ['X', 'Y', 'Z']) {
            const arr = new Array(9).fill('I');
            arr[q] = p;
            const res = M.surfaceAnalyze(arr);
            if (res.logicalXFlip || res.logicalZFlip || !res.residualZeroSyndrome) {
              errs.push(`Surface d=3 single error ${p}${q + 1} caused logical/syndrome error: ${res.verdict}`);
            }
          }
        }
        const x4x5 = ['I', 'I', 'I', 'X', 'X', 'I', 'I', 'I', 'I'];
        const rx = M.surfaceAnalyze(x4x5);
        if (rx.verdict !== 'logical_error' || !rx.logicalXFlip) errs.push('Surface X4X5 should trigger logical X flip');
        const z3z6 = ['I', 'I', 'Z', 'I', 'I', 'Z', 'I', 'I', 'I'];
        const rz = M.surfaceAnalyze(z3z6);
        if (rz.verdict !== 'logical_error' || !rz.logicalZFlip) errs.push('Surface Z3Z6 should trigger logical Z flip');
        return errs;
      });
      for (const kf of kernelFailures) {
        report.errors.push({ file: 'reader/lab/quantum-lab.html', width, message: 'lab math kernel failed: ' + kf });
      }

      // Interactive UI verification across all 6 tabs + WAI-ARIA ArrowRight + theme sync.
      await page.locator('[data-mzi-phi="180"]').click();
      if ((await page.locator('#mzi-p0-out').textContent())?.trim() !== '0.0%') {
        report.errors.push({ file: 'reader/lab/quantum-lab.html', message: 'MZI UI 180deg button did not update P(0)' });
      }
      await page.locator('#tab-mzi').focus();
      await page.keyboard.press('ArrowRight');
      if ((await page.locator('#tab-bloch').getAttribute('aria-selected')) !== 'true') {
        report.errors.push({ file: 'reader/lab/quantum-lab.html', message: 'WAI-ARIA ArrowRight did not switch from MZI to Bloch tab' });
      }
      await page.locator('[data-gate="H"]').click();
      await page.locator('[data-gate="S"]').click();
      await page.locator('[data-gate="T"]').click();
      const blochVecTxt = (await page.locator('#bloch-vec').textContent()) || '';
      if (blochVecTxt.includes('-0.000')) {
        report.errors.push({ file: 'reader/lab/quantum-lab.html', message: 'Bloch UI displayed -0.000', blochVecTxt });
      }
      await page.locator('#bloch-sample-1000').click();
      await page.locator('#tab-ramsey').click();
      await page.locator('[data-ramsey-jump="1.5"]').click();
      await page.locator('#tab-chsh').click();
      await page.locator('#chsh-sim-btn').click();
      if (!((await page.locator('#chsh-sim-out').textContent()) || '').includes('Wilson')) {
        report.errors.push({ file: 'reader/lab/quantum-lab.html', message: 'CHSH UI 1000-round simulation did not render Wilson CI' });
      }
      await page.locator('#tab-grover').click();
      await page.locator('#grover-oracle-btn').click();
      await page.locator('#grover-diff-btn').click();
      await page.locator('#grover-step-btn').click();
      await page.locator('#grover-step-btn').click();
      if (!((await page.locator('#grover-pgood-val').textContent()) || '').includes('33.01')) {
        report.errors.push({ file: 'reader/lab/quantum-lab.html', message: 'Grover UI step 3 overshoot did not reach 33.01%' });
      }
      await page.locator('#tab-surface').click();
      await page.locator('[data-surface-preset="x4x5"]').click();
      await page.locator('#surface-decode-btn').click();
      if (!((await page.locator('#surface-verdict-val').textContent()) || '').includes('翻转')) {
        report.errors.push({ file: 'reader/lab/quantum-lab.html', message: 'Surface Code UI X4X5 did not report logical flip' });
      }
      // Verify lab theme toggle syncs both qch-theme and qch-lab-theme.
      await page.locator('#theme-toggle').click();
      const labThemes = await page.evaluate(() => ({
        t1: localStorage.getItem('qch-theme'),
        t2: localStorage.getItem('qch-lab-theme'),
      }));
      if (labThemes.t1 !== 'dark' || labThemes.t2 !== 'dark') {
        report.errors.push({ file: 'reader/lab/quantum-lab.html', message: 'lab theme toggle failed to sync qch-theme and qch-lab-theme', labThemes });
      }
      await page.locator('#theme-toggle').click();
      await page.evaluate(() => { try { localStorage.removeItem('qch-theme'); localStorage.removeItem('qch-lab-theme'); } catch {} });
      await page.locator('#tab-mzi').click();
    }
    const labShotName = `quantum-lab-${width}.png`;
    await page.screenshot({ path: path.join(shots, labShotName) });
    report.screenshots.push('work/rendered/' + labShotName);
    report.labChecks.push({
      file: 'reader/lab/quantum-lab.html',
      width,
      overflow: labOverflow,
      jsErrors: report.errors.length - labErrorsBefore,
      externalRequests: report.externalRequests.length - labExternalBefore,
      ...labState,
    });

    await page.close();
  }

  // Verify teaching WAV metadata, unique aria-labels, and Ramsey cue buttons.
  const audioPage = await browser.newPage();
  await audioPage.goto(pathToFileURL(path.join(root, 'reader/labs/audio.html')).href);
  report.audioChecks = await audioPage.locator('audio').evaluateAll(async elements => {
    return Promise.all(elements.map(e => new Promise(resolve => {
      const done = () => resolve({
        src: e.getAttribute('src'),
        ariaLabel: e.getAttribute('aria-label') || '',
        duration: e.duration,
        readyState: e.readyState,
        error: e.error?.message || null,
        autoplay: e.autoplay,
        controls: e.controls,
      });
      e.addEventListener('loadedmetadata', done, { once: true });
      e.addEventListener('error', done, { once: true });
      setTimeout(done, 5000);
      e.load();
    })));
  });
  const audioLabels = report.audioChecks.map(a => a.ariaLabel.trim());
  if (report.audioChecks.length !== 5 || report.audioChecks.some(a => a.error || a.duration !== 4 || a.autoplay || !a.controls)) {
    report.errors.push({ message: 'teaching WAV metadata/controls failed', audio: report.audioChecks });
  }
  if (audioLabels.some(l => !l) || new Set(audioLabels).size !== audioLabels.length) {
    report.errors.push({ file: 'reader/labs/audio.html', message: 'audio elements must have non-empty unique aria-label attributes', audioLabels });
  }
  const ramseyBarCount = await audioPage.locator('.ramsey-cue-bar').count();
  if (ramseyBarCount !== 2) {
    report.errors.push({ file: 'reader/labs/audio.html', message: 'expected 2 Ramsey cue jump bars on labs/audio.html', actual: ramseyBarCount });
  }
  await audioPage.close();

  // Verify mobile right-edge scroll samples and revised explanations.
  const sample = await browser.newPage({ viewport: { width: 390, height: 1000 } });
  for (const [file, selector, label] of [
    ['labs/audio.html', '.table-scroll', 'audio-controls'],
    ['labs/practice.html', '.katex-display', 'statistics-formula'],
    ['appendices/notation.html', '.table-scroll', 'table'],
    ['appendices/prerequisites.html', '.table-scroll', 'prerequisites-table'],
    ['10-error-correction.html', '.table-scroll', 'syndrome-table'],
    ['06-algorithmic-primitives.html', '.katex-display', 'formula'],
    ['08-applications.html', '.flowchart-scroll', 'flowchart'],
    ['19-engineering-architecture.html', '.scientific-svg[href$="hardware-control-lanes.svg"]', 'hardware-figure'],
    ['10-error-correction.html', '.scientific-svg[href$="surface-code-events.svg"]', 'surface-code-figure'],
    ['15-practice-research.html', '.scientific-svg[href$="bell-witness-sampling.svg"]', 'bell-witness-figure'],
  ]) {
    await sample.goto(pathToFileURL(path.join(root, 'reader', file)).href);
    await sample.evaluate(() => document.fonts.ready);
    await sample.locator(selector).evaluateAll(elements => {
      const e = elements.find(el => el.scrollWidth > el.clientWidth + 2) || elements[0];
      if (e) e.setAttribute('data-scroll-sample', 'true');
    });
    const region = sample.locator('[data-scroll-sample="true"]');
    await region.scrollIntoViewIfNeeded();
    await region.evaluate(e => { e.scrollLeft = e.scrollWidth; });
    const name = label + '-390-right-edge.png';
    await region.screenshot({ path: path.join(shots, name) });
    report.screenshots.push('work/rendered/' + name);
  }
  for (const [file, needle, label] of [
    ['03-multiple-qubits.html', '代入', 'chsh-table'],
    ['04-circuits-protocols.html', 'Bob 的归一化条件态', 'teleportation-table'],
    ['19-engineering-architecture.html', '仅局域操作的线路切割', 'modularity-table'],
    ['15-practice-research.html', '乘积为', 'bell-witness-counts-table'],
  ]) {
    await sample.goto(pathToFileURL(path.join(root, 'reader', file)).href);
    const region = sample.locator('.table-scroll').filter({ hasText: needle }).first();
    if (await region.count() !== 1) { report.errors.push({ file, message: 'new teaching table not found: ' + label }); continue; }
    await region.scrollIntoViewIfNeeded();
    await region.evaluate(e => { e.scrollLeft = e.scrollWidth; });
    const name = label + '-390-right-edge.png';
    await region.screenshot({ path: path.join(shots, name) });
    report.screenshots.push('work/rendered/' + name);
  }
  for (const [file, needle, label] of [
    ['03-multiple-qubits.html', '漏检不一定是因为关联落在别的轴上', 'entanglement-witness'],
    ['08-applications.html', '有限样本的加权估计不能代替精确期望值', 'vqe-sampling'],
    ['17-computation-models.html', '重复实验的成功概率目标', 'tts-probability'],
    ['17-computation-models.html', '都要做的链修复', 'tts-postprocessing'],
  ]) {
    await sample.goto(pathToFileURL(path.join(root, 'reader', file)).href);
    const region = sample.locator('main > article p').filter({ hasText: needle }).first();
    if (await region.count() !== 1) { report.errors.push({ file, message: 'revised explanation not found: ' + label }); continue; }
    await region.scrollIntoViewIfNeeded();
    const name = label + '-390.png';
    await region.screenshot({ path: path.join(shots, name) });
    report.screenshots.push('work/rendered/' + name);
  }
  await sample.goto(pathToFileURL(path.join(root, 'reader/04-circuits-protocols.html')).href);
  await sample.screenshot({ path: path.join(shots, '04-circuits-protocols-390-full.png'), fullPage: true });
  report.screenshots.push('work/rendered/04-circuits-protocols-390-full.png');
  await sample.goto(pathToFileURL(path.join(root, 'reader/16-advanced-algorithms-verification.html')).href);
  await sample.locator('.flowchart').nth(1).locator('img').evaluate(async e => { e.loading = 'eager'; await e.decode(); });
  await sample.locator('.flowchart').nth(1).screenshot({ path: path.join(shots, '16-qsvt-flowchart-390.png') });
  report.screenshots.push('work/rendered/16-qsvt-flowchart-390.png');
  const qsvtSvg = await sample.locator('.flowchart').nth(1).locator('img').getAttribute('src');
  await sample.goto(pathToFileURL(path.join(root, 'reader', qsvtSvg)).href);
  await sample.locator('svg').screenshot({ path: path.join(shots, '16-qsvt-flowchart-full.png') });
  report.screenshots.push('work/rendered/16-qsvt-flowchart-full.png');
  await sample.close();

  // Manual Dark Mode Gate: System Light + click #theme-toggle -> chapter <img> average luminance must be <= 120.
  // Also verifies reverse direction (System Dark + click #theme-toggle -> Light >= 170), exercises.html chips, & beginner mode.
  const darkGatePage = await browser.newPage({ viewport: { width: 1440, height: 1000 }, colorScheme: 'light' });
  darkGatePage.on('pageerror', e => report.errors.push({ type: 'javascript', context: 'darkGate', message: e.message }));
  for (const [relHtml, selector, label] of [
    ['reader/02-single-qubit.html', 'img[data-dark-src$="bloch-sphere.svg"]', '02-bloch-svg-manual-dark'],
    ['reader/02-single-qubit.html', 'figure.flowchart img', '02-flowchart-manual-dark'],
    ['reader/14-compilation-control.html', 'img[data-dark-src$="v3-14-weyl-chamber-zx.svg"]', '14-weyl-svg-manual-dark'],
    ['reader/labs/algorithms.html', 'img[data-dark-src$="algorithm-lab-checks.svg"]', 'lab-mpl-svg-manual-dark'],
  ]) {
    await darkGatePage.goto(pathToFileURL(path.join(root, relHtml)).href);
    await darkGatePage.evaluate(() => { try { localStorage.removeItem('qch-theme'); localStorage.removeItem('qch-lab-theme'); } catch {} });
    await darkGatePage.reload();
    await darkGatePage.locator('#theme-toggle').click();
    const imgLoc = darkGatePage.locator(selector).first();
    await imgLoc.scrollIntoViewIfNeeded();
    await imgLoc.evaluate(async img => {
      img.loading = 'eager';
      if (!img.complete) await new Promise(r => { img.onload = r; img.onerror = r; });
      await img.decode().catch(() => {});
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    });
    const pngBuf = await imgLoc.screenshot();
    const avgLum = Number(measurePngAvgLum(pngBuf).toFixed(1));
    report.darkSvgChecks.push({ file: relHtml, label, mode: 'os-light-manual-dark', avgLum });
    if (avgLum > 120) {
      report.errors.push({ file: relHtml, label, message: `manual dark mode SVG too bright (avgLum=${avgLum} > 120)` });
    }
    if (label === '02-bloch-svg-manual-dark') {
      await darkGatePage.screenshot({ path: path.join(shots, '02-single-qubit-1440-dark.png') });
      report.screenshots.push('work/rendered/02-single-qubit-1440-dark.png');
    }
  }
  // Reverse direction check: OS Dark -> manual Light must render bright SVG (avgLum >= 170).
  await darkGatePage.emulateMedia({ colorScheme: 'dark' });
  await darkGatePage.goto(pathToFileURL(path.join(root, 'reader/02-single-qubit.html')).href);
  await darkGatePage.evaluate(() => { try { localStorage.removeItem('qch-theme'); localStorage.removeItem('qch-lab-theme'); } catch {} });
  await darkGatePage.reload();
  await darkGatePage.locator('#theme-toggle').click();
  const lightImgLoc = darkGatePage.locator('img[data-light-src$="bloch-sphere.svg"]').first();
  await lightImgLoc.scrollIntoViewIfNeeded();
  await lightImgLoc.evaluate(async img => {
    img.loading = 'eager';
    if (!img.complete) await new Promise(r => { img.onload = r; img.onerror = r; });
    await img.decode().catch(() => {});
  });
  const revAvgLum = Number(measurePngAvgLum(await lightImgLoc.screenshot()).toFixed(1));
  report.darkSvgChecks.push({ file: 'reader/02-single-qubit.html', label: '02-bloch-svg-manual-light-in-os-dark', mode: 'os-dark-manual-light', avgLum: revAvgLum });
  if (revAvgLum < 170) {
    report.errors.push({ file: 'reader/02-single-qubit.html', message: `manual light mode in OS dark rendered dark SVG (avgLum=${revAvgLum} < 170)` });
  }
  await darkGatePage.emulateMedia({ colorScheme: 'light' });
  await darkGatePage.evaluate(() => { try { localStorage.removeItem('qch-theme'); localStorage.removeItem('qch-lab-theme'); } catch {} });

  // Verify exercises.html sticky chapter chip filtering, collapsible chapters & permanent >=271 two-level hint gate.
  await darkGatePage.goto(pathToFileURL(path.join(root, 'reader/appendices/exercises.html')).href);
  const exChapterCount = await darkGatePage.locator('details.ex-chapter').count();
  if (exChapterCount !== 26) {
    report.errors.push({ file: 'reader/appendices/exercises.html', message: `expected 26 collapsible ex-chapters, found ${exChapterCount}` });
  }
  const exHintCount = await darkGatePage.locator('details.ex-hint-box').count();
  if (exHintCount < 271) {
    report.errors.push({ file: 'reader/appendices/exercises.html', message: `two-level anti-spoiler gate failed: expected >= 271 details.ex-hint-box, found ${exHintCount}` });
  }
  const exAnswerCount = await darkGatePage.locator('details.ex-answer-box').count();
  if (exAnswerCount < 271) {
    report.errors.push({ file: 'reader/appendices/exercises.html', message: `two-level anti-spoiler gate failed: expected >= 271 details.ex-answer-box, found ${exAnswerCount}` });
  }
  await darkGatePage.locator('#ex-toolbar [data-ex-filter="10"]').click();
  const visibleExAfter10 = await darkGatePage.locator('details.ex-chapter:not([hidden])').count();
  if (visibleExAfter10 !== 1) {
    report.errors.push({ file: 'reader/appendices/exercises.html', message: `chip filter "10" should show 1 chapter, showed ${visibleExAfter10}` });
  }
  await darkGatePage.locator('#ex-toolbar [data-ex-filter="all"]').click();

  // Verify Beginner Core-Track Mode collapses data-advanced="true" sections.
  await darkGatePage.goto(pathToFileURL(path.join(root, 'reader/16-advanced-algorithms-verification.html')).href);
  const advCount = await darkGatePage.locator('section.advanced-section[data-advanced="true"]').count();
  if (advCount < 1) {
    report.errors.push({ file: 'reader/16-advanced-algorithms-verification.html', message: 'missing data-advanced="true" sections' });
  } else {
    await darkGatePage.locator('#beginner-toggle').click();
    const begAttr = await darkGatePage.evaluate(() => document.documentElement.getAttribute('data-beginner-mode'));
    if (begAttr !== 'on') {
      report.errors.push({ file: 'reader/16-advanced-algorithms-verification.html', message: 'beginner-toggle did not enable data-beginner-mode="on"' });
    }
    await darkGatePage.locator('#beginner-toggle').click();
  }
  await darkGatePage.close();

  // Verify all handbook/assets/*.svg text bounding boxes & capture light/dark renders.
  const svgPage = await browser.newPage({ viewport: { width: 1000, height: 1000 } });
  report.svgChecks = [];
  for (const file of (await fs.readdir(path.join(root, 'handbook/assets'))).filter(f => f.endsWith('.svg'))) {
    await svgPage.goto(pathToFileURL(path.join(root, 'handbook/assets', file)).href);
    await svgPage.evaluate(() => document.fonts.ready);
    await svgPage.evaluate(() => {
      const s = document.querySelector('svg'), v = s.viewBox.baseVal;
      s.setAttribute('width', v.width);
      s.setAttribute('height', v.height);
    });
    const bounds = await svgPage.evaluate(() => {
      const svg = document.querySelector('svg'), v = svg.viewBox.baseVal;
      return [...svg.querySelectorAll('text')].flatMap(e => {
        const local = e.getBBox(), matrix = svg.getCTM().inverse().multiply(e.getCTM());
        const points = [
          [local.x, local.y],
          [local.x + local.width, local.y],
          [local.x, local.y + local.height],
          [local.x + local.width, local.y + local.height],
        ].map(([x, y]) => new DOMPoint(x, y).matrixTransform(matrix));
        const xs = points.map(p => p.x), ys = points.map(p => p.y);
        const b = { x: Math.min(...xs), y: Math.min(...ys), width: Math.max(...xs) - Math.min(...xs), height: Math.max(...ys) - Math.min(...ys) };
        return b.x < v.x - 1 || b.x + b.width > v.x + v.width + 1 || b.y < v.y - 1 || b.y + b.height > v.y + v.height + 1
          ? [{ text: e.textContent, x: b.x, y: b.y, width: b.width, height: b.height }]
          : [];
      });
    });
    report.svgChecks.push({ file, textOutsideViewBox: bounds });
    if (bounds.length) report.errors.push({ file, message: 'SVG text extends beyond viewBox', bounds });
    await svgPage.locator('svg').screenshot({ path: path.join(shots, file.replace('.svg', '-light.png')) });
    await svgPage.emulateMedia({ colorScheme: 'dark' });
    await svgPage.locator('svg').screenshot({ path: path.join(shots, file.replace('.svg', '-dark.png')) });
    await svgPage.emulateMedia({ colorScheme: 'light' });
  }

  // Permanent Gate: all generated flow-*.svg (light + dark) must have zero blank .node elements.
  {
    const flowDirs = [
      { dir: path.join(root, 'reader/assets'), prefix: 'reader/assets' },
      { dir: path.join(root, 'reader/assets/dark'), prefix: 'reader/assets/dark' },
    ];
    let checkedFiles = 0;
    let totalNodes = 0;
    let emptyNodes = 0;
    const sampleEmpty = [];
    for (const { dir, prefix } of flowDirs) {
      if (!fsSync.existsSync(dir)) continue;
      const flowFiles = (await fs.readdir(dir)).filter(f => /^flow-.*\.svg$/.test(f)).sort();
      for (const file of flowFiles) {
        checkedFiles++;
        await svgPage.goto(pathToFileURL(path.join(dir, file)).href);
        const res = await svgPage.evaluate(() => {
          const svg = document.querySelector('svg');
          const nodes = [...document.querySelectorAll('.node')];
          const empties = nodes
            .filter(n => n.textContent.trim().length === 0)
            .map((n, idx) => n.id || `node#${idx}`);
          return {
            hasText: Boolean(svg && svg.textContent.trim().length > 0),
            nodeCount: nodes.length,
            empties,
          };
        });
        totalNodes += res.nodeCount;
        if (!res.hasText) {
          emptyNodes++;
          if (sampleEmpty.length < 20) sampleEmpty.push({ file: `${prefix}/${file}`, reason: 'SVG has no text content' });
        }
        if (res.empties.length > 0) {
          emptyNodes += res.empties.length;
          if (sampleEmpty.length < 20) sampleEmpty.push({ file: `${prefix}/${file}`, emptyNodeIds: res.empties });
        }
      }
    }
    if (checkedFiles === 0 || emptyNodes > 0) {
      report.errors.push({
        file: 'reader/assets/flow-*.svg',
        message: checkedFiles === 0
          ? 'flow-*.svg gate failed: no flow-*.svg files found'
          : `flow-*.svg gate failed: ${emptyNodes} empty .node element(s) across ${checkedFiles} files`,
        samples: sampleEmpty,
      });
    }
    report.flowNodeGate = { checkedFiles, totalNodes, emptyNodes };
  }
  await svgPage.close();

  const reportJson = JSON.stringify(report, null, 2);
  await fs.mkdir(path.join(root, 'work/research'), { recursive: true });
  await fs.writeFile(path.join(root, 'work/research/reader-verification.json'), reportJson);
  console.log(JSON.stringify({
    pagesAtTwoWidths: report.pages.length,
    labChecks: report.labChecks.length,
    darkSvgChecks: report.darkSvgChecks,
    searchChecks: report.searchChecks.length,
    searchIndexGate: report.searchIndexGate,
    flowNodeGate: report.flowNodeGate,
    screenshots: report.screenshots.length,
    externalRequests: report.externalRequests.length,
    errors: report.errors,
  }, null, 2));
  if (report.errors.length || report.externalRequests.length) process.exitCode = 1;
} catch (error) {
  process.exitCode = 1;
  throw error;
} finally {
  await closeBrowser(browser);
}
