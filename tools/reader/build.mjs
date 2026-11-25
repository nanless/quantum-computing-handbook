import fs from 'node:fs/promises';
import fsSync from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import { renderWebMath } from './epub-mathml.mjs';
import { readingPlan } from './reading-order.mjs';
import { exerciseChapterId, exerciseIdOf, requireExerciseAlignment, verifyExerciseAlignment } from './exercise-identity.mjs';
import { resolveDiagramTitle } from './diagram-titles.mjs';
import { recordDeliveryBuild, snapshotDeliverySource } from './build-provenance.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const source = path.join(root, 'handbook');
const output = path.join(root, 'reader');
const cache = path.join(root, 'work/render-cache');
const courseHomeDir = path.join(here, 'course-home');
const labSrcDir = path.join(here, 'lab');
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

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const slug = s => s.toLowerCase().replace(/[\p{P}\p{S}]/gu, c => (c === '-' || c === '_' ? c : '')).trim().replace(/\s/g, '-');
const walk = async dir => (await Promise.all((await fs.readdir(dir, { withFileTypes: true })).map(e => (e.isDirectory() ? walk(path.join(dir, e.name)) : path.join(dir, e.name))))).flat();
const digest = value => crypto.createHash('sha256').update(value).digest('hex');

const files = (await walk(source))
  .filter(f => f.endsWith('.md') && path.basename(f) !== 'STYLE.md')
  .sort();
const contents = new Map(await Promise.all(files.map(async f => [f, await fs.readFile(f, 'utf8')])));
const edition = contents.get(path.join(source, 'README.md')).match(/^>\s*版本：(\d{4}-\d{2}-\d{2})/m)?.[1];
if (!edition || Number.isNaN(Date.parse(edition + 'T00:00:00Z')) || new Date(edition + 'T00:00:00Z').toISOString().slice(0, 10) !== edition) {
  throw new Error('handbook/README.md must declare a valid YYYY-MM-DD edition');
}
const titleOf = f => contents.get(f).match(/^# (.+)/m)[1];
const outputName = f => path.relative(source, f).replace(/README\.md$/, 'index.html').replace(/\.md$/, '.html');
const chapters = files.filter(f => /^\d\d-/.test(path.basename(f)));
const orderedReading = readingPlan(chapters);
const readingPositions = new Map(orderedReading.sequence.map((file, index) => [file, index + 1]));
const readingPosition = file => `阅读顺序 ${readingPositions.get(file)} / ${orderedReading.sequence.length}`;
const exercisesFile = path.join(source, 'appendices/exercises.md');
const exerciseAlignment = verifyExerciseAlignment(chapters.map(file => ({
  id: chapterIdOf(file),
  file: path.relative(root, file),
  text: contents.get(file),
})), contents.get(exercisesFile));
requireExerciseAlignment(exerciseAlignment);
const exercisesMap = exerciseAlignment.appendixByChapter;
const exerciseIdsByChapter = new Map(exerciseAlignment.perChapter.map(chapter => [chapter.chapter, chapter]));

await fs.mkdir(output, { recursive: true });
await fs.mkdir(cache, { recursive: true });
// Clean legacy / orphan output directories before build (Scheme C: no reader/research, no STYLE.html).
await fs.rm(path.join(output, 'research'), { recursive: true, force: true });
await fs.rm(path.join(output, 'STYLE.html'), { force: true });
await fs.rm(path.join(output, 'assets'), { recursive: true, force: true });
await fs.rm(path.join(output, 'lab'), { recursive: true, force: true });

const appendixOrder = ['prerequisites.md', 'notation.md', 'glossary.md', 'exercises.md', 'references.md', 'software-practice.md', 'audit-log.md'];
const labs = files.filter(f => f.includes('/labs/'));
const appendices = files.filter(f => f.includes('/appendices/')).sort((a, b) => appendixOrder.indexOf(path.basename(a)) - appendixOrder.indexOf(path.basename(b)));

function chapterIdOf(f) {
  const rel = path.relative(source, f).replaceAll('\\', '/');
  const qm = rel.match(/^quantum-mechanics\/0(\d)-/);
  if (qm) return `Q${qm[1]}`;
  const main = rel.match(/^(\d\d)-/);
  if (main) return main[1];
  return null;
}

// Split a dual-theme scientific SVG with @media (prefers-color-scheme: dark) into
// pure-light (no dark media query) and pure-dark (unwrapped dark rules) variants so
// manual theme switching works identically in both Light OS and Dark OS environments.
function splitSvgLightDark(svgText) {
  const re = /@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)/g;
  const blocks = [];
  let m;
  while ((m = re.exec(svgText)) !== null) {
    const braceStart = svgText.indexOf('{', m.index + m[0].length);
    if (braceStart === -1) continue;
    let depth = 0;
    let braceEnd = -1;
    for (let i = braceStart; i < svgText.length; i++) {
      if (svgText[i] === '{') depth++;
      else if (svgText[i] === '}') {
        depth--;
        if (depth === 0) {
          braceEnd = i;
          break;
        }
      }
    }
    if (braceEnd !== -1) {
      blocks.push({ start: m.index, end: braceEnd + 1, inner: svgText.slice(braceStart + 1, braceEnd) });
      re.lastIndex = braceEnd + 1;
    }
  }
  if (!blocks.length) return { hasDark: false, lightSvg: svgText, darkSvg: null };

  let lightSvg = '';
  let darkSvg = '';
  let cursor = 0;
  for (const b of blocks) {
    lightSvg += svgText.slice(cursor, b.start);
    darkSvg += svgText.slice(cursor, b.start) + '\n' + b.inner.trim() + '\n';
    cursor = b.end;
  }
  lightSvg += svgText.slice(cursor);
  darkSvg += svgText.slice(cursor);
  lightSvg = lightSvg.replace(/color-scheme\s*:\s*light\s+dark/gi, 'color-scheme:light');
  darkSvg = darkSvg.replace(/color-scheme\s*:\s*light\s+dark/gi, 'color-scheme:dark');
  return { hasDark: true, lightSvg, darkSvg };
}

// Pre-scan handbook/assets/*.svg to know which SVGs have native dark variants.
const sourceAssetsDir = path.join(source, 'assets');
const svgDarkAvailable = new Set();
for (const entry of await fs.readdir(sourceAssetsDir, { withFileTypes: true })) {
  if (entry.isFile() && entry.name.endsWith('.svg')) {
    const rawSvg = await fs.readFile(path.join(sourceAssetsDir, entry.name), 'utf8');
    if (/@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)/.test(rawSvg)) {
      svgDarkAvailable.add(entry.name);
    }
  }
}

const report = { generatedAt: new Date().toISOString(), pages: [], mathErrors: [], diagramErrors: [], diagrams: 0, formulas: 0 };
const usedFlowSvgs = new Set();
const usedAssets = new Set();

let browser, server, page, currentMermaidTheme = null;
const MERMAID_THEMES = {
  light: {
    cachePrefix: 'mermaid-11.6-reader-v3\n',
    themeVariables: {
      primaryColor: '#e8f2ef',
      primaryTextColor: '#183934',
      primaryBorderColor: '#72988e',
      lineColor: '#66837b',
      secondaryColor: '#f2eadb',
      tertiaryColor: '#f7f7f2',
      fontSize: '17px',
    },
  },
  dark: {
    cachePrefix: 'mermaid-11.6-reader-v4-dark\n',
    themeVariables: {
      darkMode: true,
      background: '#141d1b',
      primaryColor: '#1b302b',
      primaryTextColor: '#e6f0ec',
      primaryBorderColor: '#5ec4aa',
      lineColor: '#8eb2a7',
      secondaryColor: '#292218',
      secondaryTextColor: '#f2e6d5',
      secondaryBorderColor: '#d99a4e',
      tertiaryColor: '#182422',
      tertiaryTextColor: '#e6f0ec',
      tertiaryBorderColor: '#4d7369',
      clusterBkg: '#162220',
      clusterBorder: '#3b574f',
      edgeLabelBackground: '#182422',
      textColor: '#e6f0ec',
      nodeTextColor: '#e6f0ec',
      fontSize: '17px',
    },
  },
};

async function diagram(code, themeMode = 'light') {
  const cfg = MERMAID_THEMES[themeMode] || MERMAID_THEMES.light;
  const key = crypto.createHash('sha256').update(cfg.cachePrefix + code).digest('hex');
  const file = path.join(cache, key + '.svg');
  try { return await fs.readFile(file, 'utf8'); } catch {}
  if (!page) {
    server = http.createServer(async (req, res) => {
      if (req.url === '/') { res.setHeader('Content-Type', 'text/html'); res.end('<!doctype html><html><head><meta charset="utf-8"></head><body></body></html>'); return; }
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\//, '');
      const filePath = path.resolve(here, rel);
      if (!filePath.startsWith(here + path.sep)) { res.writeHead(403).end(); return; }
      try { res.setHeader('Content-Type', /\.m?js$/.test(filePath) ? 'text/javascript' : 'application/octet-stream'); res.end(await fs.readFile(filePath)); } catch { res.writeHead(404).end(); }
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    browser = await chromium.launch(browserOptions);
    page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
    await page.goto('http://127.0.0.1:' + server.address().port);
    await page.evaluate(async () => {
      const { default: mermaid } = await import('/node_modules/mermaid/dist/mermaid.esm.min.mjs');
      window.mermaid = mermaid;
    });
  }
  if (currentMermaidTheme !== themeMode) {
    await page.evaluate(themeVariables => {
      window.mermaid.initialize({
        startOnLoad: false,
        securityLevel: 'strict',
        theme: 'base',
        htmlLabels: false,
        fontFamily: 'PingFang SC, Microsoft YaHei, sans-serif',
        themeVariables,
        flowchart: { htmlLabels: false, curve: 'linear', padding: 18, nodeSpacing: 32, rankSpacing: 42 },
      });
    }, cfg.themeVariables);
    currentMermaidTheme = themeMode;
  }
  const id = 'diagram-' + themeMode[0] + '-' + key.slice(0, 13);
  let svg = await page.evaluate(async ({ id, code }) => (await window.mermaid.render(id, code)).svg, { id, code });
  if (themeMode === 'dark') {
    svg = svg.replace(/<svg\b([^>]*)>/, '<svg$1><style>:root{color-scheme:dark}svg{background:#141d1b}</style>');
  }
  await fs.writeFile(file, svg);
  return svg;
}

// Protect math before Markdown tokenization, including bars inside table cells.
// Keep visual HTML and MathML semantics together. Display formulas also keep exact TeX for copying.
function protectMath(text, f, { trackInReport = true } = {}) {
  const fragments = [];
  const meta = [];
  const latexSources = [];
  const displaySources = [];
  const pattern = /(^[ \t]*```[^\n]*\n[\s\S]*?^[ \t]*```[^\n]*$)|(`+)[^\n]*?\2|\$\$([\s\S]*?)\$\$|\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)|(?<!\\)\$(?!\$)((?:\\.|[^$\n])+?)(?<!\\)\$/gm;
  const protectedText = text.replace(pattern, (full, fence, ticks, display1, display2, inline1, inline2, offset, src) => {
    if (fence || ticks) return full;
    const display = display1 !== undefined || display2 !== undefined;
    const latex = display1 ?? display2 ?? inline1 ?? inline2;
    latexSources.push(latex);
    let html;
    try {
      html = renderWebMath(latex, display);
      if (display) {
        const trimmed = latex.trim();
        displaySources.push(trimmed);
        const safeTex = esc(trimmed);
        html = html.includes('class="katex-display"')
          ? html.replace('<span class="katex-display"', `<span class="katex-display" data-tex="${safeTex}"`)
          : `<span class="katex-display" data-tex="${safeTex}">${html}</span>`;
      }
    } catch (e) {
      if (trackInReport) report.mathErrors.push({ file: path.relative(root, f), latex, error: e.message });
      html = '<code class="math-error">' + esc(latex) + '</code>';
    }
    if (trackInReport) report.formulas++;
    const id = fragments.length;
    fragments.push(display ? html : '<span class="math-inline">' + html + '</span>');
    meta.push({ display, latex });
    if (!display) return `<span data-handbook-math="${id}"></span>`;
    const lineStart = src.lastIndexOf('\n', offset - 1) + 1;
    const linePrefix = src.slice(lineStart, offset);
    const beforeLine = src.slice(0, lineStart);
    const afterMatch = src.slice(offset + full.length);
    const placeholder = `<div data-handbook-math="${id}"></div>`;
    if (/^[ \t]*(?:>[ \t]*)+$/.test(linePrefix)) {
      const bqBlank = linePrefix.replace(/[ \t]+$/, '');
      const hasPreBlank = !beforeLine || /(?:^|\n)[ \t]*(?:>[ \t]*)+[ \t]*\n$/.test(beforeLine) || /(?:^|\n)[ \t]*\n$/.test(beforeLine);
      const pre = hasPreBlank ? '' : `\n${bqBlank}\n${linePrefix}`;
      let post = '';
      if (/^[ \t]*\n/.test(afterMatch)) {
        const afterFirstNl = afterMatch.replace(/^[ \t]*\n/, '');
        const hasPostBlank = !afterFirstNl || /^[ \t]*(?:(?:>[ \t]*)+)?[ \t]*(?:\n|$)/.test(afterFirstNl);
        if (!hasPostBlank) post = `\n${bqBlank}`;
      } else if (afterMatch.trim()) {
        post = `\n${bqBlank}\n${linePrefix}`;
      }
      return `${pre}${placeholder}${post}`;
    }
    const indent = /^[ \t]*$/.test(linePrefix) ? linePrefix : linePrefix.match(/^[ \t]*/)[0];
    const prevLine = beforeLine.slice(beforeLine.lastIndexOf('\n', beforeLine.length - 2) + 1);
    const afterEmptyListMarker = /^[ \t]*(?:[-*+]|\d+[.)])[ \t]*\n$/.test(prevLine);
    const slot = afterEmptyListMarker ? `<span data-handbook-math="${id}"></span>` : placeholder;
    let pre = '';
    if (linePrefix.trim() !== '') pre = `\n\n${indent}`;
    else if (beforeLine && !afterEmptyListMarker && !/(?:^|\n)[ \t]*\n$/.test(beforeLine)) pre = `\n${indent}`;
    let post = '';
    if (/^[ \t]*\n/.test(afterMatch)) {
      const afterFirstNl = afterMatch.replace(/^[ \t]*\n/, '');
      const hasPostBlank = !afterFirstNl || /^[ \t]*(?:\n|$)/.test(afterFirstNl);
      if (!hasPostBlank) post = '\n';
    } else if (afterMatch.trim()) {
      post = `\n\n${indent}`;
    }
    return `${pre}${slot}${post}`;
  });
  return {
    protectedText,
    mathSourceDigest: digest(JSON.stringify(latexSources)),
    displayMathDigest: digest(JSON.stringify(displaySources)),
    displayFormulas: displaySources.length,
    restore: html => {
      // Glue short inline formulas to immediately following punctuation so orphan punctuation never wraps alone.
      const glued = html.replace(
        /<span data-handbook-math="(\d+)"><\/span>([，。；：、！？）》」』,.!?;:])/g,
        (full, idStr, punct) => {
          const idx = +idStr;
          const m = meta[idx];
          if (!m || m.display || m.latex.length > 48 || m.latex.includes('\\begin{')) {
            return fragments[idx] + punct;
          }
          return `<span class="math-glue">${fragments[idx]}${punct}</span>`;
        },
      );
      return glued.replace(/<(div|span) data-handbook-math="(\d+)"><\/\1>/g, (_, _tag, id) => fragments[+id]);
    },
  };
}

// Strip fenced code blocks and display math blocks before heading tokenization so
// standalone '=' or '---' lines inside formulas/code can never be misparsed as Setext H1/H2.
function stripBlocksForHeadingScan(text) {
  const blockPattern = /(^[ \t]*(`{3,}|~{3,})[^\n]*\n[\s\S]*?^[ \t]*\2[ \t]*$)|(`+)[^\n]*?\3|\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]/gm;
  return text.replace(blockPattern, (full, _fence, _fenceDelim, ticks) => (ticks ? full : '\n\n<div data-handbook-block-stripped></div>\n\n'));
}

function classifyHeadingClass(depth, rawTitle) {
  if (depth !== 3 && depth !== 4) return '';
  const plain = rawTitle.replace(/[*_`~]/g, '').trim();
  if (/^(?:例(?:\s|\d|[A-Za-z])|算例)/.test(plain)) return ' class="heading-example"';
  if (/^练(?:\s|\d|[A-Za-z])/.test(plain)) return ' class="heading-practice"';
  return '';
}

function classifyBlockquotes(html) {
  const tagRe = /<\/?blockquote(?:\s[^>]*)?>/gi;
  let out = '';
  let last = 0;
  let depth = 0;
  let openStart = -1;
  let openEnd = -1;
  let openTag = '';

  for (const m of html.matchAll(tagRe)) {
    const tag = m[0];
    const isClose = tag.startsWith('</');
    if (!isClose) {
      if (depth === 0) {
        openStart = m.index;
        openEnd = m.index + tag.length;
        openTag = tag;
      }
      depth++;
    } else if (depth > 0) {
      depth--;
      if (depth === 0) {
        out += html.slice(last, openStart);
        const inner = html.slice(openEnd, m.index);
        if (/\bclass=/i.test(openTag)) {
          out += openTag + inner + tag;
        } else {
          const plain = inner
            .replace(/<[^>]+>/g, ' ')
            .replace(/&nbsp;/g, ' ')
            .replace(/&amp;/g, '&')
            .replace(/&lt;/g, '<')
            .replace(/&gt;/g, '>')
            .replace(/\s+/g, ' ')
            .trim();
          const head24 = plain.slice(0, 24);
          let cls = 'callout-note';
          let label = '要点 · 批注';
          if (/(?:误区|注意|警示|陷阱|反例|勘误|常见错误|千万别)/.test(head24)) {
            cls = 'callout-warn';
            label = '警示 · 常见误区';
          } else if (/(?:工程|边界|限制|现实|硬件|实验条件|代价)/.test(head24)) {
            cls = 'callout-eng';
            label = '工程 · 物理边界';
          } else if (/(?:直觉|白话|类比|几何|生活|一句话)/.test(head24)) {
            cls = 'callout-intuition';
            label = '直觉 · 物理画面';
          } else if (/(?:进阶|定理|证明|延伸|严格|小结|总结|核心结论)/.test(head24)) {
            cls = 'callout-deep';
            label = '核心 · 定理与小结';
          }
          out += `<blockquote class="callout ${cls}" data-callout-label="${label}">${inner}${tag}`;
        }
        last = m.index + tag.length;
      }
    }
  }
  return out + html.slice(last);
}

function enhanceTables(html) {
  return html
    .replace(/<table>/g, '<div class="table-scroll" role="region" aria-label="可横向滚动的数据表" tabindex="0"><table>')
    .replace(/<\/table>/g, '</table></div>')
    .replace(/<th(?=\s|>)(?![^>]*\bscope=)/g, '<th scope="col"');
}

// Wrap H2/H3/H4 sections containing 进阶选读 / 进阶回看 / 进阶深潜 in <section data-advanced="true">
// while preserving the exact heading tags, IDs, and sequence inside main > article.
function wrapAdvancedSections(html) {
  const re = /<h([234])\s+id="([^"]+)"[^>]*>([\s\S]*?)<\/h\1>/g;
  const headings = [...html.matchAll(re)].map(m => ({
    level: Number(m[1]),
    id: m[2],
    text: m[3].replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim(),
    index: m.index,
  }));
  const ranges = [];
  for (let i = 0; i < headings.length; i++) {
    const h = headings[i];
    if (!/(?:进阶选读|进阶回看|进阶深潜)/.test(h.text)) continue;
    // Skip if already inside an enclosing wrapped range.
    if (ranges.some(r => h.index >= r.start && h.index < r.end)) continue;
    let end = html.length;
    for (let j = i + 1; j < headings.length; j++) {
      if (headings[j].level <= h.level) {
        end = headings[j].index;
        break;
      }
    }
    ranges.push({ start: h.index, end, title: h.text });
  }
  if (!ranges.length) return html;
  let out = '';
  let cursor = 0;
  for (const r of ranges) {
    out += html.slice(cursor, r.start);
    out += `<section class="advanced-section" data-advanced="true" data-advanced-title="${esc(r.title)}">${html.slice(r.start, r.end)}</section>`;
    cursor = r.end;
  }
  return out + html.slice(cursor);
}

// Assign deterministic id="term-N" anchors to glossary term paragraphs for direct search jump.
function annotateGlossaryTerms(html) {
  let idx = 0;
  return html.replace(/<p><strong>((?:(?!<\/strong>|<\/p>)[\s\S])+)<\/strong>([：:])/g, (full, term, colon) => {
    idx++;
    return `<p id="term-${idx}" class="glossary-entry"><strong>${term}</strong>${colon}`;
  });
}

function enhanceBodySemantics(html, relSource = '') {
  let out = html.replace(/<p>\s*(<figure class="scientific-figure">[\s\S]*?<\/figure>)\s*<\/p>/g, '$1');
  out = classifyBlockquotes(out);
  out = enhanceTables(out);
  if (relSource === 'appendices/glossary.md') out = annotateGlossaryTerms(out);
  out = wrapAdvancedSections(out);
  return out;
}

function recordAssetTarget(target) {
  if (target.startsWith(sourceAssetsDir + path.sep) && fsSync.existsSync(target)) {
    usedAssets.add(path.relative(sourceAssetsDir, target).replaceAll('\\', '/'));
  }
}

function createLinkRewriter(sourceFile, targetOutputFile) {
  return function rewriteHref(href) {
    if (/^(https?:|mailto:|#)/.test(href)) return href;
    const [p, anchor] = href.split('#');
    const target = path.resolve(path.dirname(sourceFile), p);
    if (contents.has(target)) {
      return path.relative(path.dirname(targetOutputFile), path.join(output, outputName(target))) + (anchor ? '#' + anchor : '');
    }
    if (target === path.join(source, 'STYLE.md')) {
      return path.relative(path.dirname(targetOutputFile), path.join(output, 'appendices/notation.html')) + (anchor ? '#' + anchor : '');
    }
    if (target.startsWith(sourceAssetsDir + path.sep)) {
      recordAssetTarget(target);
      const local = path.join(output, 'assets', path.relative(sourceAssetsDir, target));
      return path.relative(path.dirname(targetOutputFile), local) + (anchor ? '#' + anchor : '');
    }
    if (target.startsWith(path.join(root, 'codes') + path.sep)) {
      const local = path.join(output, 'codes', path.relative(path.join(root, 'codes'), target));
      return path.relative(path.dirname(targetOutputFile), local) + (anchor ? '#' + anchor : '');
    }
    if (target.startsWith(output + path.sep)) {
      return path.relative(path.dirname(targetOutputFile), target) + (anchor ? '#' + anchor : '');
    }
    return href;
  };
}

// Split an exercise ordered-list item into { stemHtml, hintHtml, answerHtml }.
// Scans all bullets in the item's unordered list for `- 核心提示：` or `- **核心提示**：`
// so two-level anti-spoiler folding works regardless of bullet ordering (e.g. after 题意与约定).
function renderExerciseItemParts(itemTokens, renderer, restore) {
  let stemTokens = [];
  let bodyTokens = itemTokens;
  if (itemTokens.length > 1 && (itemTokens[0].type === 'paragraph' || itemTokens[0].type === 'text')) {
    stemTokens = [itemTokens[0]];
    bodyTokens = itemTokens.slice(1);
  }
  let hintHtml = '';
  const remainingBody = [];
  const hintRe = /^(?:\*\*|__)?核心提示(?:\*\*|__)?\s*[：:]/;
  for (const tok of bodyTokens) {
    if (!hintHtml && tok.type === 'list' && !tok.ordered && tok.items.length) {
      const hintIdx = tok.items.findIndex(it => {
        const itemText = (it.text || (it.raw || '').replace(/^\s*[-*+]\s+/, '')).trim();
        return hintRe.test(itemText);
      });
      if (hintIdx !== -1) {
        hintHtml = enhanceTables(restore(marked.parser(tok.items[hintIdx].tokens, { renderer, gfm: true })));
        const restItems = tok.items.filter((_, idx) => idx !== hintIdx);
        if (restItems.length) {
          remainingBody.push({ ...tok, items: restItems });
        }
        continue;
      }
    }
    remainingBody.push(tok);
  }
  const stemHtml = stemTokens.length
    ? restore(marked.parser(stemTokens, { renderer, gfm: true })).replace(/^<p>([\s\S]*)<\/p>\s*$/, '$1')
    : '';
  const answerHtml = enhanceTables(restore(marked.parser(remainingBody.length ? remainingBody : itemTokens, { renderer, gfm: true })));
  return { stemHtml, hintHtml, answerHtml };
}

function buildChapterSolutionsHtml(chId, targetOutputFile, prefix, exercisesFile, exercisesMap) {
  if (!chId || !exercisesMap.has(chId)) return '';
  const sliceRaw = exercisesMap.get(chId);
  if (!sliceRaw || !sliceRaw.trim()) return '';
  const { protectedText, restore } = protectMath(sliceRaw, exercisesFile, { trackInReport: false });
  const tokens = marked.lexer(protectedText, { gfm: true });
  const rewriteHref = createLinkRewriter(exercisesFile, targetOutputFile);
  const solRenderer = new marked.Renderer();
  solRenderer.heading = function ({ tokens: inlineTokens }) {
    return `<p><strong>${this.parser.parseInline(inlineTokens)}</strong></p>\n`;
  };
  solRenderer.link = function ({ href, title, tokens: inlineTokens }) {
    const resolved = href && href.startsWith('#') ? `${prefix}appendices/exercises.html${href}` : rewriteHref(href);
    const linkHtml = this.parser.parseInline(inlineTokens);
    return `<a href="${esc(resolved)}"${title ? ` title="${esc(title)}"` : ''}>${linkHtml}</a>`;
  };

  const renderedItems = [];
  for (const token of tokens) {
    if (token.type !== 'list' || !token.ordered) continue;
    for (const item of token.items) {
      const exerciseId = exerciseIdOf(item);
      const qIndex = Number(exerciseId.split('-')[1]);
      const { stemHtml, hintHtml, answerHtml } = renderExerciseItemParts(item.tokens, solRenderer, restore);
      if (hintHtml) {
        renderedItems.push(
          `<div class="solution-item solution-two-level" data-exercise-id="${exerciseId}">` +
            `<div class="solution-item-head"><span class="sol-num">第 ${qIndex} 题</span><span class="sol-stem">${stemHtml}</span></div>` +
            `<div class="solution-two-level-body">` +
              `<details class="ex-hint-box"><summary>💡 查看核心提示</summary><div class="ex-hint-body">${hintHtml}</div></details>` +
              `<details class="ex-answer-box"><summary>📖 查看完整四步解答</summary><div class="ex-answer-body">${answerHtml}</div></details>` +
            `</div>` +
          `</div>`,
        );
      } else {
        const fullHtml = stemHtml ? `<p>${stemHtml}</p>${answerHtml}` : answerHtml;
        renderedItems.push(
          `<details class="solution-item" data-exercise-id="${exerciseId}">` +
            `<summary><span class="sol-num">第 ${qIndex} 题参考解答</span><span class="sol-hint">展开零跳步推导</span></summary>` +
            `<div class="solution-body">${fullHtml}</div>` +
          `</details>`,
        );
      }
    }
  }
  if (!renderedItems.length) return '';

  return (
    `<section class="chapter-solutions" id="chapter-solutions" aria-labelledby="chapter-solutions-title">` +
      `<div class="solutions-head">` +
        `<div>` +
          `<h2 class="solutions-title" id="chapter-solutions-title">本章自检题参考解答（共 ${renderedItems.length} 题）</h2>` +
          `<p class="solutions-note">默认折叠，便于先独立推演再逐题核对；打印时自动展开。完整汇总见 <a href="${prefix}appendices/exercises.html">附录：练习答案与推导提示</a>。</p>` +
        `</div>` +
        `<button type="button" class="solutions-toggle-all" data-solutions-toggle aria-expanded="false">展开全部解答</button>` +
      `</div>` +
      `<div class="solutions-list">${renderedItems.join('')}</div>` +
    `</section>`
  );
}

// Restructure appendices/exercises.html into sticky chip filter bar + collapsible <details class="ex-chapter">
// + two-level anti-spoiler question cards while preserving every H2 heading/id & KaTeX formula order.
function buildExercisesPageBody(protectedText, headings, renderer, restore) {
  const tokens = marked.lexer(protectedText, { gfm: true });
  let hi = 0;
  const introParts = [];
  const chapterBlocks = [];
  const tailParts = [];
  let currentChapter = null;
  let seenChapter = false;

  for (const tok of tokens) {
    if (tok.type === 'heading') {
      const h = headings[hi++];
      const innerHtml = restore(marked.parser([{ ...tok, type: 'paragraph' }], { renderer, gfm: true }).replace(/^<p>([\s\S]*)<\/p>\s*$/, '$1'));
      if (tok.depth === 2) {
        const key = exerciseChapterId(h.title);
        if (key) {
          seenChapter = true;
          currentChapter = { key, chip: key, id: h.id, title: h.title, titleHtml: innerHtml, qCount: 0, htmlParts: [] };
          chapterBlocks.push(currentChapter);
          continue;
        }
        currentChapter = null;
      }
      const hHtml = `<h${tok.depth} id="${esc(h.id)}">${innerHtml}</h${tok.depth}>\n`;
      if (currentChapter) currentChapter.htmlParts.push(hHtml);
      else if (seenChapter) tailParts.push(hHtml);
      else introParts.push(hHtml);
      continue;
    }

    if (currentChapter && tok.type === 'list' && tok.ordered) {
      for (const item of tok.items) {
        const exerciseId = exerciseIdOf(item);
        const qIdx = Number(exerciseId.split('-')[1]);
        const { stemHtml, hintHtml, answerHtml } = renderExerciseItemParts(item.tokens, renderer, restore);
        const searchKey = `${currentChapter.chip} ${qIdx} ${stemHtml.replace(/<[^>]+>/g, ' ')}`.replace(/\s+/g, ' ').trim();
        currentChapter.htmlParts.push(
          `<div class="ex-question-card" data-ex-q="${qIdx}" data-exercise-id="${exerciseId}" data-ex-search="${esc(searchKey.toLowerCase())}">` +
            `<div class="ex-question-head"><span class="ex-q-badge">第 ${qIdx} 题</span><div class="ex-q-stem">${stemHtml || `第 ${qIdx} 题`}</div></div>` +
            (hintHtml ? `<details class="ex-hint-box"><summary>💡 查看核心提示</summary><div class="ex-hint-body">${hintHtml}</div></details>` : '') +
            `<details class="ex-answer-box"><summary>📖 查看完整四步解答</summary><div class="ex-answer-body">${answerHtml}</div></details>` +
          `</div>`,
        );
      }
      currentChapter.qCount += tok.items.length;
      continue;
    }

    const chunkHtml = enhanceBodySemantics(restore(marked.parser([tok], { renderer, gfm: true })));
    if (currentChapter) currentChapter.htmlParts.push(chunkHtml);
    else if (seenChapter) tailParts.push(chunkHtml);
    else introParts.push(chunkHtml);
  }

  const chipsHtml =
    `<button type="button" class="ex-chip is-active" data-ex-filter="all" aria-pressed="true">全部 (${chapterBlocks.length} 章)</button>` +
    chapterBlocks
      .map(c => `<button type="button" class="ex-chip" data-ex-filter="${esc(c.key)}" aria-pressed="false">${esc(c.chip)}</button>`)
      .join('');

  const toolbarHtml =
    `<div class="ex-toolbar" id="ex-toolbar" role="region" aria-label="自检题章节筛选与折叠控制">` +
      `<div class="ex-toolbar-row">` +
        `<input type="search" id="ex-search" class="ex-search-input" aria-label="按关键词或题号筛选习题" placeholder="筛选题目标题或关键词（如：Bell、Grover、表面码）…">` +
        `<div class="ex-toolbar-btns">` +
          `<button type="button" class="ex-ctrl-btn" data-ex-toggle-chapters aria-expanded="false">展开全部章</button>` +
          `<button type="button" class="ex-ctrl-btn" data-ex-toggle-answers aria-expanded="false">展开当前解答</button>` +
        `</div>` +
      `</div>` +
      `<div class="ex-chip-bar" role="group" aria-label="按章节快速筛选">${chipsHtml}</div>` +
      `<div class="ex-toolbar-status" id="ex-toolbar-status" aria-live="polite">当前显示全部 ${chapterBlocks.length} 章（默认仅展开第 00 章，点击上方芯片秒切任意章）</div>` +
    `</div>`;

  const chaptersHtml = chapterBlocks
    .map((c, idx) =>
      `<details class="ex-chapter" data-ex-ch="${esc(c.key)}"${idx === 0 ? ' open' : ''}>` +
        `<summary class="ex-chapter-summary">` +
          `<h2 id="${esc(c.id)}" class="ex-chapter-heading">${c.titleHtml}</h2>` +
          `<span class="ex-chapter-meta">共 ${c.qCount} 题</span>` +
        `</summary>` +
        `<div class="ex-chapter-body">${c.htmlParts.join('')}</div>` +
      `</details>`,
    )
    .join('\n');

  return {
    bodyHtml: introParts.join('') + toolbarHtml + `<div class="ex-chapters-wrap">${chaptersHtml}</div>` + tailParts.join(''),
    headingCount: hi,
  };
}

function cleanInlineLatex(expr) {
  let s = expr;
  for (let i = 0; i < 2; i++) {
    s = s.replace(/\\[dt]?frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}/g, '($1)/($2)');
    s = s.replace(/\\sqrt\s*\{([^{}]+)\}/g, '√($1)');
    s = s.replace(/\\(?:vec|hat|bar|tilde|overline|underline)\s*\{([^{}]+)\}/g, '$1');
  }
  const symMap = {
    '\\to': '→', '\\rightarrow': '→', '\\leftarrow': '←', '\\leftrightarrow': '↔',
    '\\mapsto': '↦', '\\Rightarrow': '⇒', '\\Leftarrow': '⇐', '\\Leftrightarrow': '⇔',
    '\\langle': '⟨', '\\rangle': '⟩', '\\lvert': '|', '\\rvert': '|',
    '\\lVert': '‖', '\\rVert': '‖', '\\Vert': '‖', '\\vert': '|', '\\mid': '|',
    '\\succeq': '⪰', '\\preceq': '⪯', '\\ge': '≥', '\\geq': '≥', '\\le': '≤', '\\leq': '≤',
    '\\ne': '≠', '\\neq': '≠', '\\approx': '≈', '\\equiv': '≡', '\\sim': '∼', '\\propto': '∝',
    '\\ll': '≪', '\\gg': '≫', '\\pm': '±', '\\mp': '∓', '\\times': '×', '\\cdot': '·',
    '\\otimes': '⊗', '\\oplus': '⊕', '\\dagger': '†', '\\infty': '∞', '\\partial': '∂',
    '\\in': '∈', '\\notin': '∉', '\\subseteq': '⊆', '\\subset': '⊂', '\\cup': '∪', '\\cap': '∩',
    '\\sum': '∑', '\\prod': '∏', '\\int': '∫', '\\dots': '…', '\\ldots': '…', '\\cdots': '⋯',
    '\\lfloor': '⌊', '\\rfloor': '⌋', '\\lceil': '⌈', '\\rceil': '⌉',
    '\\alpha': 'α', '\\beta': 'β', '\\gamma': 'γ', '\\delta': 'δ', '\\epsilon': 'ε', '\\varepsilon': 'ε',
    '\\zeta': 'ζ', '\\eta': 'η', '\\theta': 'θ', '\\kappa': 'κ', '\\lambda': 'λ', '\\mu': 'μ',
    '\\nu': 'ν', '\\xi': 'ξ', '\\pi': 'π', '\\rho': 'ρ', '\\sigma': 'σ', '\\tau': 'τ',
    '\\phi': 'φ', '\\varphi': 'φ', '\\chi': 'χ', '\\psi': 'ψ', '\\omega': 'ω',
    '\\Gamma': 'Γ', '\\Delta': 'Δ', '\\Theta': 'Θ', '\\Lambda': 'Λ', '\\Pi': 'Π',
    '\\Sigma': 'Σ', '\\Phi': 'Φ', '\\Psi': 'Ψ', '\\Omega': 'Ω', '\\ell': 'ℓ', '\\hbar': 'ℏ',
    '\\diamond': '◇', '\\perp': '⊥', '\\star': '★', '\\forall': '∀', '\\exists': '∃',
  };
  s = s.replace(/\\[A-Za-z]+/g, cmd => {
    if (Object.prototype.hasOwnProperty.call(symMap, cmd)) return symMap[cmd];
    if (/^\\(?:mathrm|mathbf|mathit|mathcal|mathbb|mathfrak|mathsf|text|textrm|textbf|operatorname|left|right|bigl|bigr|Bigl|Bigr|biggl|biggr|displaystyle|scriptstyle|limits|nolimits|not)$/.test(cmd)) {
      return '';
    }
    return cmd.slice(1);
  });
  return s
    .replace(/\\[,;!:\s]/g, ' ')
    .replace(/\\([{}%$&_#])/g, '$1')
    .replace(/[{}]/g, '');
}

function markdownToPlainSnippet(mdSlice, maxLen = 110) {
  const cleaned = mdSlice
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/\$\$[\s\S]*?\$\$/g, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/`([^`\n]+)`/g, '$1')
    .replace(/\$([^$\n]+)\$/g, (_, m) => cleanInlineLatex(m))
    .replace(/(?:^|\s)[>#]+(?=\s)/g, ' ')
    .replace(/\*\*|__|~~/g, '')
    .replace(/\s+\|\s+/g, ' · ')
    .replace(/\s+/g, ' ')
    .trim();
  return cleaned.length > maxLen ? cleaned.slice(0, maxLen - 1).trimEnd() + '…' : cleaned;
}

const headingsByFile = new Map();
for (const [f, text] of contents) {
  const used = new Map();
  headingsByFile.set(
    f,
    marked.lexer(stripBlocksForHeadingScan(text))
      .filter(token => token.type === 'heading')
      .map(token => {
        const base = slug(token.text);
        const count = used.get(base) || 0;
        used.set(base, count + 1);
        return { level: token.depth, title: token.text, id: base + (count ? '-' + count : '') };
      }),
  );
}

const courseReadingGroups = orderedReading.groups.map(group =>
  `<li data-reading-part="${group.number}"><span>${esc(group.tag)}</span><h3>${esc(group.title)}</h3><div>` +
    group.files.map((file, index) =>
      `<a data-reading-chapter="${group.ids[index]}" href="${esc(outputName(file))}">${esc(titleOf(file))}</a>`,
    ).join('') +
  `</div></li>`,
).join('\n');
const courseHomeHtml = (await fs.readFile(path.join(courseHomeDir, 'index.html'), 'utf8'))
  .replaceAll('{{reading-chapters}}', String(orderedReading.sequence.length))
  .replaceAll('{{reading-parts}}', String(orderedReading.groups.length))
  .replace('<!-- READING GROUPS -->', courseReadingGroups)
  .replace(/href="([^"]*\/)?README\.html(#[^"]*)?"/g, 'href="$1index.html$2"');
// Register all local assets referenced in course-home/index.html.
for (const m of courseHomeHtml.matchAll(/(?:src|href)="(assets\/[^"#?]+)"/g)) {
  recordAssetTarget(path.join(source, m[1]));
}

const searchIndex = [];
const generatedHtmlRel = new Set();

function collectPageSearchEntries(f, raw, outRel, headings) {
  const pageTitle = titleOf(f);
  const relSource = path.relative(source, f).replaceAll('\\', '/');
  const isLab = relSource.startsWith('labs/');
  const isAppendix = relSource.startsWith('appendices/');
  const firstPara = markdownToPlainSnippet(raw.replace(/^# .+\n/, '').slice(0, 500), 110);
  searchIndex.push({
    t: pageTitle,
    p: isLab ? '动手实验册' : isAppendix ? '全书附录' : '全书章节',
    u: outRel,
    k: isLab ? 'lab' : 'ch',
    s: firstPara,
  });

  if (relSource === 'appendices/glossary.md') {
    let tIdx = 0;
    for (const line of raw.split('\n')) {
      const m = line.match(/^\*\*((?:(?!\*\*)[^\n]){1,120})\*\*([：:])\s*(.+)$/);
      if (!m) continue;
      tIdx++;
      searchIndex.push({
        t: markdownToPlainSnippet(m[1].trim(), 120),
        p: '术语表',
        u: `${outRel}#term-${tIdx}`,
        k: 'term',
        s: markdownToPlainSnippet(m[3], 115),
      });
    }
    return;
  }

  // Extract H2/H3 section entries with a concise plain-text first-paragraph snippet.
  const lines = raw.split('\n');
  let inFence = false;
  const hPos = [];
  for (let i = 0; i < lines.length; i++) {
    const ln = lines[i];
    if (/^[ \t]*(?:`{3,}|~{3,})/.test(ln)) { inFence = !inFence; continue; }
    if (inFence) continue;
    const hm = ln.match(/^(#{1,6})\s+(.+)$/);
    if (hm) hPos.push({ line: i, depth: hm[1].length });
  }
  for (let i = 0; i < headings.length && i < hPos.length; i++) {
    const h = headings[i];
    if (h.level !== 2 && h.level !== 3) continue;
    const startLine = hPos[i].line + 1;
    const endLine = i + 1 < hPos.length ? hPos[i + 1].line : lines.length;
    const slice = lines.slice(startLine, Math.min(endLine, startLine + 14)).join('\n');
    const cleanTitle = markdownToPlainSnippet(h.title, 90);
    searchIndex.push({
      t: cleanTitle,
      p: pageTitle,
      u: `${outRel}#${h.id}`,
      k: isLab ? 'lab' : 'sec',
      s: markdownToPlainSnippet(slice, 105),
    });
  }
}

try {
  const originalDigest = await snapshotDeliverySource(root);
  await fs.mkdir(path.join(output, 'assets/dark'), { recursive: true });

  for (const [f, raw] of contents) {
    let text = raw;
    let diagramCount = 0;
    const relSource = path.relative(source, f).replaceAll('\\', '/');
    const outRel = outputName(f);
    generatedHtmlRel.add(outRel.replaceAll('\\', '/'));
    const target = path.join(output, outRel);
    const prefix = path.dirname(outRel) === '.' ? '' : '../';
    const isHomePage = outRel === 'index.html';
    const chId = chapterIdOf(f);

    for (const match of [...text.matchAll(/```mermaid\n([\s\S]*?)```/g)]) {
      diagramCount++;
      report.diagrams++;
      try {
        const diagramTitle = resolveDiagramTitle(relSource, diagramCount - 1, match[1]);
        const flowFile = 'flow-' + crypto.createHash('sha256').update(match[1]).digest('hex').slice(0, 14) + '.svg';
        usedFlowSvgs.add(flowFile);
        const [lightSvg, darkSvg] = [await diagram(match[1], 'light'), await diagram(match[1], 'dark')];
        const lightRel = 'assets/' + flowFile;
        const darkRel = 'assets/dark/' + flowFile;
        await fs.writeFile(path.join(output, lightRel), lightSvg);
        await fs.writeFile(path.join(output, darkRel), darkSvg);
        const intrinsicWidth = Number(lightSvg.match(/viewBox="[^" ]+ [^" ]+ ([^" ]+)/)?.[1]) || 650;
        text = text.replace(
          match[0],
          `<figure class="flowchart"><div class="flowchart-scroll"><img src="${prefix + lightRel}" data-light-src="${prefix + lightRel}" data-dark-src="${prefix + darkRel}" style="width:${intrinsicWidth}px" alt="${esc(diagramTitle)}" loading="lazy"></div><figcaption>图 ${diagramCount}｜${esc(diagramTitle)} · 横向较长时可在图内滚动 · <a href="${prefix + lightRel}" data-light-href="${prefix + lightRel}" data-dark-href="${prefix + darkRel}">打开完整图</a></figcaption></figure>`,
        );
      } catch (e) {
        report.diagramErrors.push({ file: path.relative(root, f), diagram: diagramCount, error: e.message });
      }
    }

    const formulasBefore = report.formulas;
    const { protectedText, mathSourceDigest, displayMathDigest, displayFormulas, restore } = protectMath(text, f, { trackInReport: true });
    const headings = headingsByFile.get(f);
    collectPageSearchEntries(f, raw, outRel, headings);
    let hi = 0;
    const rewriteHref = createLinkRewriter(f, target);
    const renderer = new marked.Renderer();

    renderer.image = function ({ href, text: altText, title }) {
      const resolvedHref = rewriteHref(href);
      const safeHref = esc(resolvedHref);
      const safeAlt = esc(altText || '');
      const titleAttr = title ? ` title="${esc(title)}"` : '';
      let darkAttrsImg = '';
      let darkAttrsLink = '';
      const rawPath = href.split('#')[0].split('?')[0];
      const absTarget = path.resolve(path.dirname(f), rawPath);
      recordAssetTarget(absTarget);
      if (absTarget.startsWith(sourceAssetsDir + path.sep) && rawPath.endsWith('.svg')) {
        const assetRel = path.relative(sourceAssetsDir, absTarget).replaceAll('\\', '/');
        if (svgDarkAvailable.has(assetRel)) {
          const darkHref = esc(prefix + 'assets/dark/' + assetRel);
          darkAttrsImg = ` data-light-src="${safeHref}" data-dark-src="${darkHref}"`;
          darkAttrsLink = ` data-light-href="${safeHref}" data-dark-href="${darkHref}"`;
        }
      }
      if (/\.svg(?:$|[?#])/i.test(resolvedHref)) {
        const svgFile = /^(?:https?:|data:)/i.test(href) ? '' : path.resolve(path.dirname(f), href.split(/[?#]/)[0]);
        let widthAttr = '';
        if (svgFile && fsSync.existsSync(svgFile)) {
          const svg = fsSync.readFileSync(svgFile, 'utf8');
          const box = svg.match(/<svg\b[^>]*\bviewBox=["']([^"']+)["']/i)?.[1];
          const width = box?.trim().split(/[\s,]+/).map(Number)[2];
          if (Number.isFinite(width) && width > 0) widthAttr = ` data-original-width="${width}"`;
        }
        return (
          `<figure class="scientific-figure">` +
            `<a class="image-open scientific-svg" href="${safeHref}"${darkAttrsLink} aria-label="打开原尺寸图：${safeAlt}">` +
              `<img src="${safeHref}"${darkAttrsImg}${widthAttr} alt="${safeAlt}"${titleAttr} loading="lazy">` +
              `<span>放大查看 ↗</span>` +
            `</a>` +
            (safeAlt ? `<figcaption class="scientific-caption">${safeAlt}</figcaption>` : '') +
          `</figure>`
        );
      }
      return (
        `<a class="image-open" href="${safeHref}"${darkAttrsLink} aria-label="打开原尺寸图：${safeAlt}">` +
          `<img src="${safeHref}"${darkAttrsImg} alt="${safeAlt}"${titleAttr} loading="lazy">` +
          `<span>放大查看 ↗</span>` +
        `</a>`
      );
    };

    renderer.listitem = function (item) {
      const html = marked.Renderer.prototype.listitem.call(this, item);
      const exerciseId = exerciseIdOf(item);
      return exerciseId ? html.replace('<li>', `<li data-exercise-id="${exerciseId}">`) : html;
    };

    renderer.heading = function ({ tokens, depth }) {
      const h = headings[hi++];
      const cls = classifyHeadingClass(depth, h.title);
      return `<h${depth} id="${esc(h.id)}"${cls}>${this.parser.parseInline(tokens)}</h${depth}>\n`;
    };

    renderer.link = function ({ href, title, tokens }) {
      const resolved = rewriteHref(href);
      const linkHtml = this.parser.parseInline(tokens);
      return `<a href="${esc(resolved)}"${title ? ` title="${esc(title)}"` : ''}>${linkHtml}</a>`;
    };

    let body;
    if (relSource === 'appendices/exercises.md') {
      const builtEx = buildExercisesPageBody(protectedText, headings, renderer, restore);
      body = builtEx.bodyHtml;
      hi = builtEx.headingCount;
    } else {
      body = enhanceBodySemantics(restore(marked.parse(protectedText, { renderer, gfm: true })), relSource);
    }

    const chapterLinks = list => list.map(c => {
      const cid = chapterIdOf(c);
      const title = esc(titleOf(c));
      const caption = cid ? `<span>${title}<small class="nav-reading-position">${readingPosition(c)}</small></span>` : title;
      return `<a ${c === f ? 'aria-current="page" ' : ''}${cid ? `data-ch-id="${cid}" ` : ''}href="${prefix + outputName(c)}">${caption}</a>`;
    }).join('');
    const qmGuideCurrent = outRel === 'quantum-mechanics/index.html' ? 'aria-current="page" ' : '';
    const nav =
      orderedReading.groups
        .map(
          group =>
            `<div class="nav-label" data-reading-part="${group.number}">${esc(group.label)}</div>` +
            `${group.ids.includes('Q1') ? `<a ${qmGuideCurrent}href="${prefix}quantum-mechanics/index.html">物理篇导读与先修说明</a>` : ''}` +
            `${chapterLinks(group.files)}`,
        )
        .join('') +
      `<div class="nav-label">实验与代码</div>` +
      `<a class="nav-lab-featured" href="${prefix}lab/quantum-lab.html">⚡ 6 模块交互量子实验台（离线）</a>` +
      `${chapterLinks(labs)}`;

    const appNav = appendices.map(c => `<a ${c === f ? 'aria-current="page" ' : ''}href="${prefix + outputName(c)}">${esc(titleOf(c))}</a>`).join('');
    const renderedHeadings = new Map([...body.matchAll(/<h[23]\s+id="([^"]+)"[^>]*>([\s\S]*?)<\/h[23]>/g)].map(m => [m[1], m[2]]));
    const toc = headings
      .filter(h => h.level === 2 || h.level === 3)
      .map(h => `<a class="toc-level-${h.level}" href="#${esc(h.id)}">${renderedHeadings.get(esc(h.id)) || esc(h.title)}</a>`)
      .join('');
    const mobileToc = toc ? `<details class="inline-contents"><summary>本页导航 · 展开查找小节</summary><nav aria-label="本页章节">${toc}</nav></details>` : '';

    const sequence = orderedReading.sequence;
    const index = sequence.indexOf(f);
    const chapterPosition = index >= 0 ? `<p class="chapter-reading-position">${readingPosition(f)}</p>` : '';
    const prev = index > 0 ? `<a data-nav-prev href="${prefix + outputName(sequence[index - 1])}">← ${esc(titleOf(sequence[index - 1]))}</a>` : '';
    const next = index >= 0 && index < sequence.length - 1 ? `<a data-nav-next href="${prefix + outputName(sequence[index + 1])}">${esc(titleOf(sequence[index + 1]))} →</a>` : '';

    const solutionsHtml = buildChapterSolutionsHtml(chId, target, prefix, exercisesFile, exercisesMap);
    const checkinHtml = chId
      ? `<div class="chapter-checkin" data-chapter-id="${chId}" data-chapter-url="${outRel}" data-chapter-title="${esc(titleOf(f))}">` +
          `<div class="checkin-info">` +
            `<strong class="checkin-title">学习进度打卡（仅存本地浏览器）</strong>` +
            `<span class="checkin-sub" id="qch-checkin-status">学完本章并核对自检题后，可标记为已掌握。</span>` +
          `</div>` +
          `<button type="button" class="checkin-btn" id="qch-checkin-btn" aria-pressed="false">✓ 标记本章已掌握</button>` +
        `</div>`
      : '';
    const bootScript =
      `<script>(function(){try{` +
      `var t=localStorage.getItem('qch-theme')||localStorage.getItem('qch-lab-theme');` +
      `if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);` +
      `if(localStorage.getItem('qch-beginner-mode')==='on')document.documentElement.setAttribute('data-beginner-mode','on');` +
      `}catch(e){}})();</script>`;

    const topSectionHtml = isHomePage
      ? courseHomeHtml
      : `<header class="reader-header">` +
          `<a class="brand" href="${prefix}index.html"><span class="mark">ψ</span>量子计算手册</a>` +
          `<span class="edition">V4 · 离线阅读版</span>` +
          `<div class="header-actions">` +
            `<button type="button" class="header-btn header-search-btn" data-open-search aria-label="全书离线检索 (Cmd+K)" title="全书离线检索 (Cmd/Ctrl+K 或 /)">` +
              `<span aria-hidden="true">🔍</span><span class="header-search-label">检索</span><kbd class="header-kbd">⌘K</kbd>` +
            `</button>` +
            `<button type="button" id="beginner-toggle" class="header-btn header-beginner-btn" aria-pressed="false" aria-label="切换初学主线模式" title="初学主线模式：一键折叠进阶选读小节">` +
              `<span aria-hidden="true">🎯</span><span class="beginner-label">主线</span>` +
            `</button>` +
            `<button type="button" id="theme-toggle" aria-pressed="false" aria-label="切换为暗色模式" title="切换为暗色模式 (t)">` +
              `<span class="theme-icon" aria-hidden="true">☾</span><span class="theme-label">暗色</span>` +
            `</button>` +
            `<a class="header-btn header-lab-link" href="${prefix}lab/quantum-lab.html" aria-label="实验台"><span aria-hidden="true">⚡</span><span class="header-lab-label">实验台</span></a>` +
            `<button type="button" class="header-print-btn" onclick="window.print()">打印<span class="header-print-label-long">本章</span></button>` +
          `</div>` +
        `</header>`;

    const bodyAttrs = isHomePage
      ? ` class="course-page course-home-page" data-page-url="${outRel}" data-page-title="${esc(titleOf(f))}"`
      : ` data-page-url="${outRel}" data-page-title="${esc(titleOf(f))}"`;

    const faviconLink =
      `<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%2314453d'/%3E%3Ctext x='32' y='45' text-anchor='middle' font-family='Georgia,serif' font-size='38' font-weight='700' fill='%23fbfaf6'%3E%CF%88%3C/text%3E%3C/svg%3E">`;
    const html =
      `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">` +
      `${faviconLink}` +
      `<title>${esc(titleOf(f))} · 量子计算手册</title>${bootScript}` +
      `<link rel="stylesheet" href="${prefix}assets/katex/katex.min.css">` +
      `<link rel="stylesheet" href="${prefix}assets/reader.css">` +
      `${isHomePage ? `<link rel="stylesheet" href="${prefix}assets/home.css">` : ''}</head><body${bodyAttrs}>` +
      `<div class="read-progress" id="qch-read-progress" aria-hidden="true"></div>` +
      `<a class="skip" href="#content">跳到正文</a>` +
      `${topSectionHtml}` +
      `<div class="layout" id="main-content">` +
        `<aside class="chapters"><details open><summary>全书目录</summary>` +
          `<input type="search" id="nav-search" aria-label="筛选目录章节" placeholder="筛选目录…（全书按 ⌘K）">` +
          `<div class="sidebar-progress" id="qch-sidebar-progress" hidden><div class="sidebar-progress-head"><span>已掌握进度</span><strong id="qch-progress-count">0 / ${sequence.length} 章</strong></div><div class="sidebar-progress-track"><span id="qch-progress-fill" style="width:0%"></span></div></div>` +
          `<nav aria-label="全书章节目录">${nav}<div class="nav-label">附录</div>${appNav}</nav>` +
        `</details></aside>` +
        `<main id="content"><div class="eyebrow">QUANTUM COMPUTING · V4 离线学习手册</div>${chapterPosition}${mobileToc}<article>${body}</article>${solutionsHtml}${checkinHtml}<div class="page-turn">${prev}${next}</div><footer>${edition} 版 · 公式、双主题矢量图、字体与 6 模块交互实验台均保存在本地<br>配套 Markdown 为可编辑原稿；事实更新与审校范围见审校记录。</footer></main>` +
        `<aside class="contents"><strong>本页内容</strong><nav aria-label="本页小节目录">${toc}</nav><a class="top" href="#content">↑ 返回顶部</a></aside>` +
      `</div>` +
      `<script src="${prefix}assets/search-index.js" defer></script>` +
      `<script src="${prefix}assets/reader.js" defer></script>` +
      `${isHomePage ? `<script src="${prefix}assets/home.js" defer></script>` : ''}` +
      `</body></html>`;

    await fs.mkdir(path.dirname(target), { recursive: true });
    await fs.writeFile(target, html);
    report.pages.push({
      source: path.relative(root, f),
      output: path.relative(root, target),
      sourceSha256: digest(raw),
      outputSha256: digest(html),
      exerciseIds: relSource === 'appendices/exercises.md'
        ? { questionIds: [], answerIds: [...exercisesMap.keys()].flatMap(id => exerciseIdsByChapter.get(id).answerIds) }
        : {
            questionIds: exerciseIdsByChapter.get(chId)?.questionIds || [],
            answerIds: exerciseIdsByChapter.get(chId)?.answerIds || [],
          },
      mathSourceDigest,
      displayMathDigest,
      displayFormulas,
      headingIds: headings.map(h => h.id),
      diagrams: diagramCount,
      headings: hi,
      formulas: report.formulas - formulasBefore,
    });
  }

  // Add the 6 interactive Quantum Lab modules to the offline search index.
  searchIndex.push(
    { t: '01 · MZI 干涉与密度矩阵实验台', p: '6 模块离线交互实验台', u: 'lab/quantum-lab.html#tab-mzi', k: 'lab', s: 'Mach-Zehnder 单比特干涉仪、复振幅相量、可见度 V、混态密度矩阵与 Englert 对偶。' },
    { t: '02 · Bloch 球真弧旋转与千次采样沙盒', p: '6 模块离线交互实验台', u: 'lab/quantum-lab.html#tab-bloch', k: 'lab', s: '右手三维 Bloch 球、球面真弧单比特门（H/X/Y/Z/S/T/Rx/Ry/Rz）与 Z/X/Y 基采样坍缩。' },
    { t: '03 · Ramsey 退相干稳态与 Fisher 灵敏度实验台', p: '6 模块离线交互实验台', u: 'lab/quantum-lab.html#tab-ramsey', k: 'lab', s: '对比真实纯退相位 P₀(t)→0.50 稳态与衰减至 0 误区，实时观测经典 Fisher 信息 F_C(φ; V)。' },
    { t: '04 · Bell 偏迹坍缩与 CHSH 博弈台', p: '6 模块离线交互实验台', u: 'lab/quantum-lab.html#tab-chsh', k: 'lab', s: '双 Bloch 球约化态缩向球心、并发度、CHSH 测量角调节与 1000 局 95% Wilson 置信检验。' },
    { t: '05 · Grover 振幅放大半拍拆解与过冲陷阱', p: '6 模块离线交互实验台', u: 'lab/quantum-lab.html#tab-grover', k: 'lab', s: '拆分 Oracle 反相与绕均值扩散两半拍，观察 n=3 M=1 第 2 步 94.53% 与第 3 步过冲 33.01%。' },
    { t: '06 · d=3 旋转表面码注错与症状解码沙箱', p: '6 模块离线交互实验台', u: 'lab/quantum-lab.html#tab-surface', k: 'lab', s: '[[9,1,3]] 表面码点击注错（X/Z/Y）、稳定子亮灯、最小权重解码与单错纠回 vs 双错逻辑翻转。' },
  );
  await fs.writeFile(path.join(output, 'assets/search-index.js'), `window.__QCH_SEARCH_INDEX__=${JSON.stringify(searchIndex)};\n`);

  // Clean any orphan HTML files from previous builds outside codes/, lab/, assets/, and dist/.
  for (const existing of await walk(output)) {
    const rel = path.relative(output, existing).replaceAll('\\', '/');
    if (rel.startsWith('codes/') || rel.startsWith('lab/') || rel.startsWith('assets/') || rel.startsWith('dist/')) continue;
    if (rel.endsWith('.html') && !generatedHtmlRel.has(rel)) {
      await fs.unlink(existing);
    }
  }

  // Generate local offline dist/index.html landing page so ./dist/index.html works in local reader/,
  // GitHub Pages (_pages/dist/index.html overwrites it with embedded PDF/EPUB links), and release ZIPs.
  await fs.mkdir(path.join(output, 'dist'), { recursive: true });
  const distLandingHtml =
    `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">` +
    `<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%2314453d'/%3E%3Ctext x='32' y='45' text-anchor='middle' font-family='Georgia,serif' font-size='38' font-weight='700' fill='%23fbfaf6'%3E%CF%88%3C/text%3E%3C/svg%3E">` +
    `<title>电子书与离线包下载 · 量子计算手册</title>` +
    `<style>` +
    `body{font-family:"PingFang SC","Noto Sans CJK SC","Microsoft YaHei",system-ui,-apple-system,sans-serif;max-width:780px;margin:44px auto;padding:0 20px;line-height:1.75;color:#1b2b27;background:#fbfaf6}` +
    `a{color:#14453d;font-weight:650}h1{margin:0 0 8px;font-size:1.65rem;color:#102420}` +
    `.meta{margin:0 0 20px;color:#565f5b;font-size:.92rem}` +
    `.card{margin:18px 0;padding:18px 22px;border:1px solid #d7d1c5;border-radius:10px;background:#f3efe6}` +
    `.card h2{margin:0 0 8px;font-size:1.12rem;color:#14453d}ul{margin:8px 0 0;padding-left:1.3rem}li{margin:8px 0}` +
    `code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86rem;background:#e8e3d8;padding:2px 6px;border-radius:4px}` +
    `</style></head><body>` +
    `<h1>量子计算手册 · 全介质电子书与离线包下载</h1>` +
    `<p class="meta">当前内容版本：${esc(edition)} 版 · 同源零失真构建（PDF / EPUB / 完整离线网站 ZIP / 自编代码 ZIP / SHA256SUMS.txt）</p>` +
    `<section class="card"><h2>GitHub Releases 官方最新版下载</h2>` +
    `<p>包含 A4 印刷级 PDF、原生 MathML 3 EPUB 3、完整离线网站 ZIP、自编标准库代码 ZIP 与 <code>SHA256SUMS.txt</code> 完整性校验清单：</p>` +
    `<ul>` +
    `<li><a href="https://github.com/nanless/quantum-computing-handbook/releases/latest" target="_blank" rel="noopener">前往 GitHub Releases 最新版（全部 5 类发布产物）↗</a></li>` +
    `<li><a href="https://github.com/nanless/quantum-computing-handbook/releases/latest/download/quantum-computing-handbook.pdf" target="_blank" rel="noopener">直接下载 A4 印刷级 PDF ↗</a></li>` +
    `<li><a href="https://github.com/nanless/quantum-computing-handbook/releases/latest/download/quantum-computing-handbook.epub" target="_blank" rel="noopener">直接下载原生公式 EPUB 3 ↗</a></li>` +
    `<li><a href="https://github.com/nanless/quantum-computing-handbook/releases/latest/download/SHA256SUMS.txt" target="_blank" rel="noopener">下载 SHA256SUMS.txt 校验清单 ↗</a></li>` +
    `</ul></section>` +
    `<section class="card"><h2>本地仓库构建产物路径</h2>` +
    `<p>如果你已克隆本仓库并本地构建了电子书，PDF 与 EPUB 位于仓库根目录 <code>dist/quantum-computing-handbook.pdf</code> 与 <code>dist/quantum-computing-handbook.epub</code>；GitHub Pages 部署时会自动同步至本站 <code>./dist/</code> 目录。</p>` +
    `</section>` +
    `<p><a href="../index.html">← 返回离线阅读版首页</a> · <a href="../lab/quantum-lab.html">打开 6 模块交互实验台 →</a></p>` +
    `</body></html>\n`;
  await fs.writeFile(path.join(output, 'dist/index.html'), distLandingHtml);

  // Copy codes/ cleanly.
  await fs.rm(path.join(output, 'codes'), { recursive: true, force: true });
  await fs.cp(path.join(root, 'codes'), path.join(output, 'codes'), { recursive: true, filter: f => !f.includes('__pycache__') && !f.endsWith('.pyc') });
  // Only rewrite our own Markdown guides; third-party bytes remain untouched.
  report.codeCopies = [];
  for (const from of (await walk(path.join(root, 'codes'))).filter(f => !f.includes('__pycache__') && !f.endsWith('.pyc'))) {
    const rel = path.relative(path.join(root, 'codes'), from);
    const to = path.join(output, 'codes', rel);
    if (from.endsWith('.md') && !rel.startsWith('vendor' + path.sep)) {
      const raw = await fs.readFile(from, 'utf8');
      const rewritten = raw.replace(/\]\(([^)]+)\)/g, (full, href) => {
        if (/^(https?:|#|mailto:)/.test(href)) return full;
        const [p, anchor] = href.split('#');
        const target = path.resolve(path.dirname(from), p);
        if (!contents.has(target)) return full;
        return '](' + path.relative(path.dirname(to), path.join(output, outputName(target))) + (anchor ? '#' + anchor : '') + ')';
      });
      await fs.writeFile(to, rewritten);
    }
    report.codeCopies.push({ source: path.relative(root, from), output: path.relative(root, to), outputSha256: digest(await fs.readFile(to)) });
  }

  // Copy ONLY referenced assets (auto-drops unreferenced orphans & cover banners);
  // split dual-theme scientific SVGs into pure-light + pure-dark variants.
  for (const assetRel of [...usedAssets].sort()) {
    const srcPath = path.join(sourceAssetsDir, assetRel);
    const dstPath = path.join(output, 'assets', assetRel);
    await fs.mkdir(path.dirname(dstPath), { recursive: true });
    if (assetRel.endsWith('.svg')) {
      const rawSvg = await fs.readFile(srcPath, 'utf8');
      const { hasDark, lightSvg, darkSvg } = splitSvgLightDark(rawSvg);
      await fs.writeFile(dstPath, lightSvg);
      if (hasDark && darkSvg) {
        const darkDst = path.join(output, 'assets/dark', assetRel);
        await fs.mkdir(path.dirname(darkDst), { recursive: true });
        await fs.writeFile(darkDst, darkSvg);
      }
    } else {
      await fs.copyFile(srcPath, dstPath);
    }
  }

  // Scheme C KaTeX slimming: copy ONLY katex.min.css (stripped of .woff/.ttf URLs) + fonts/*.woff2.
  const katexDist = path.join(here, 'node_modules/katex/dist');
  const katexFontsOut = path.join(output, 'assets/katex/fonts');
  await fs.mkdir(katexFontsOut, { recursive: true });
  const rawKatexCss = await fs.readFile(path.join(katexDist, 'katex.min.css'), 'utf8');
  const slimKatexCss = rawKatexCss.replace(/,\s*url\([^)]+\.(?:woff|ttf)\)\s*format\(["'][^"']+["']\)/g, '');
  await fs.writeFile(path.join(output, 'assets/katex/katex.min.css'), slimKatexCss);
  for (const fontFile of await fs.readdir(path.join(katexDist, 'fonts'))) {
    if (fontFile.endsWith('.woff2')) {
      await fs.copyFile(path.join(katexDist, 'fonts', fontFile), path.join(katexFontsOut, fontFile));
    }
  }

  await fs.copyFile(path.join(here, 'reader.css'), path.join(output, 'assets/reader.css'));
  await fs.copyFile(path.join(here, 'reader.js'), path.join(output, 'assets/reader.js'));
  await fs.copyFile(path.join(courseHomeDir, 'home.css'), path.join(output, 'assets/home.css'));
  await fs.copyFile(path.join(courseHomeDir, 'home.js'), path.join(output, 'assets/home.js'));

  // Copy 6-module offline Quantum Lab (quantum-lab.html + lab/*.js).
  const quantumLabSrc = path.join(here, 'quantum-lab.html');
  await fs.mkdir(path.join(output, 'lab'), { recursive: true });
  await fs.copyFile(quantumLabSrc, path.join(output, 'lab/quantum-lab.html'));
  const labJsFiles = (await fs.readdir(labSrcDir)).filter(f => f.endsWith('.js')).sort();
  for (const lf of labJsFiles) {
    await fs.copyFile(path.join(labSrcDir, lf), path.join(output, 'lab', lf));
  }

  await fs.mkdir(path.join(output, 'assets/licenses'), { recursive: true });
  for (const [pkg, license] of [['katex', 'LICENSE'], ['mermaid', 'LICENSE'], ['marked', 'LICENSE.md']]) {
    await fs.copyFile(path.join(here, 'node_modules', pkg, license), path.join(output, 'assets/licenses', pkg + '.txt'));
  }

  report.inputHashes = {};
  report.searchEntries = searchIndex.length;
  report.usedAssetsCount = usedAssets.size;
  report.readingOrder = orderedReading.sequence.map(file => path.relative(root, path.join(output, outputName(file))));
  const inputFiles = [
    fileURLToPath(import.meta.url),
    path.join(here, 'reading-order.mjs'),
    path.join(here, 'exercise-identity.mjs'),
    path.join(here, 'exercise-answer-fingerprints.json'),
    path.join(here, 'epub-mathml.mjs'),
    path.join(here, 'build-provenance.mjs'),
    path.join(here, 'diagram-titles.mjs'),
    path.join(here, 'reader.css'),
    path.join(here, 'reader.js'),
    path.join(courseHomeDir, 'index.html'),
    path.join(courseHomeDir, 'home.css'),
    path.join(courseHomeDir, 'home.js'),
    quantumLabSrc,
    ...labJsFiles.map(lf => path.join(labSrcDir, lf)),
    ...[...usedAssets].sort().map(rel => path.join(sourceAssetsDir, rel)),
    ...(await walk(path.join(root, 'codes'))).filter(f => !f.includes('__pycache__') && !f.endsWith('.pyc')),
  ];
  for (const file of inputFiles) {
    report.inputHashes[path.relative(root, file)] = digest(await fs.readFile(file));
  }

  await fs.mkdir(path.join(root, 'work/research'), { recursive: true });
  await fs.writeFile(path.join(root, 'work/research/reader-build-report.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify({
    pages: report.pages.length,
    formulas: report.formulas,
    diagrams: report.diagrams,
    searchEntries: report.searchEntries,
    usedAssets: report.usedAssetsCount,
    mathErrors: report.mathErrors,
    diagramErrors: report.diagramErrors,
  }, null, 2));
  if (report.mathErrors.length || report.diagramErrors.length) {
    process.exitCode = 1;
  } else {
    await recordDeliveryBuild(root, 'web', output, originalDigest);
  }
} finally {
  if (browser) await browser.close();
  if (server) await new Promise(resolve => server.close(resolve));
}
