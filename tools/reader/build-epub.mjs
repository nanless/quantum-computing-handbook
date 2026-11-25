#!/usr/bin/env node
/**
 * Build standards-compliant Native MathML 3 EPUB 3 for the Quantum Computing Handbook.
 *
 * Output:
 *   - dist/quantum-computing-handbook.epub
 *   - work/research/epub-build-report.json
 *
 * Zero external runtime dependencies:
 *   - Node built-ins + local marked & katex (output: 'mathml')
 *   - Playwright (optional/local) for Mermaid fallback & 1200x1600 portrait cover PNG
 *   - Python 3 standard library (zipfile + xml.etree.ElementTree) for EPUB 3 packaging
 *     (uncompressed first-entry mimetype) and strict XML/manifest/link validation.
 */

import fs from 'node:fs/promises';
import fsSync from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { marked } from 'marked';
import katex from 'katex';
import { readingPlan } from './reading-order.mjs';
import { resolveDiagramTitle } from './diagram-titles.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const source = path.join(root, 'handbook');
const readerDir = path.join(root, 'reader');
const workCache = path.join(root, 'work/render-cache');
const distDir = path.join(root, 'dist');
const finalEpubPath = path.join(distDir, 'quantum-computing-handbook.epub');
const reportPath = path.join(root, 'work/research/epub-build-report.json');

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.HANDBOOK_NODE_MODULES
  ? path.join(process.env.HANDBOOK_NODE_MODULES, 'playwright')
  : 'playwright');

const SYSTEM_CHROME_CANDIDATES = [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/usr/bin/google-chrome',
  '/usr/bin/google-chrome-stable',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/snap/bin/chromium',
];

function findSystemChrome() {
  for (const candidate of SYSTEM_CHROME_CANDIDATES) {
    if (fsSync.existsSync(candidate)) return candidate;
  }
  return null;
}

function hasPlaywrightChromium() {
  try {
    const pwPath = chromium.executablePath();
    return Boolean(pwPath && fsSync.existsSync(pwPath));
  } catch {
    return false;
  }
}

async function launchChromium() {
  if (process.env.HANDBOOK_CHROMIUM) {
    return chromium.launch({ headless: true, executablePath: process.env.HANDBOOK_CHROMIUM });
  }
  const attempts = [];
  const pwInstalled = hasPlaywrightChromium();
  if (pwInstalled) attempts.push({ headless: true });
  const systemChrome = findSystemChrome();
  if (systemChrome) attempts.push({ headless: true, executablePath: systemChrome });
  if (!pwInstalled) attempts.push({ headless: true });
  attempts.push({ headless: true, channel: 'chrome' });

  let lastErr = null;
  for (const opts of attempts) {
    try {
      return await chromium.launch(opts);
    } catch (err) {
      lastErr = err;
    }
  }
  throw lastErr || new Error('Unable to launch Playwright Chromium or system Chrome for EPUB rendering');
}

const BOOK_TITLE = '量子计算手册：从直觉、数学与物理到容错、传感与模拟边界';
const BOOK_AUTHOR = '量子计算手册编写组';
const BOOK_UUID = 'urn:uuid:7c6e4b8a-9d2e-4f10-8a53-202611250001';

const APPENDIX_ORDER = [
  'prerequisites.md',
  'notation.md',
  'glossary.md',
  'exercises.md',
  'references.md',
  'software-practice.md',
  'audit-log.md',
];

const LAB_ORDER = [
  'README.md',
  'foundations.md',
  'algorithms.md',
  'systems.md',
  'practice.md',
  'sdk-validation.md',
];

const CN_NUM = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'];

const safeDecode = s => {
  try { return decodeURIComponent(s); } catch { return s; }
};

const escXml = s => String(s)
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#39;');

const slug = s => String(s)
  .toLowerCase()
  .replace(/[\p{P}\p{S}]/gu, c => (c === '-' || c === '_' ? c : ''))
  .trim()
  .replace(/\s/g, '-');

const walk = async dir => (
  await Promise.all(
    (await fs.readdir(dir, { withFileTypes: true })).map(e =>
      e.isDirectory() ? walk(path.join(dir, e.name)) : path.join(dir, e.name)
    )
  )
).flat();

function xhtmlNameFor(file) {
  const rel = path.relative(source, file).replaceAll('\\', '/');
  if (rel === 'README.md') return 'intro.xhtml';
  if (rel === 'quantum-mechanics/README.md') return 'ch-q1.xhtml';
  const qmMatch = rel.match(/^quantum-mechanics\/0(\d)-/);
  if (qmMatch) return `ch-q${qmMatch[1]}.xhtml`;
  const chMatch = rel.match(/^(\d\d)-/);
  if (chMatch) return `ch-${chMatch[1]}.xhtml`;
  if (rel.startsWith('appendices/')) return 'app-' + path.basename(rel, '.md') + '.xhtml';
  if (rel === 'labs/README.md') return 'lab-overview.xhtml';
  if (rel.startsWith('labs/')) return 'lab-' + path.basename(rel, '.md') + '.xhtml';
  return 'doc-' + slug(rel.replace(/\.md$/, '')) + '.xhtml';
}

function xmlIdSafe(raw) {
  // Ensure every XML id / NCName is valid for strict XHTML5 & EPUB readers.
  const cleaned = String(raw || '').replace(/[^\p{L}\p{N}_\-.:]/gu, '-').replace(/^-+|-+$/g, '');
  if (!cleaned) return 'sec-x';
  return /^[0-9.\-]/.test(cleaned) ? 's-' + cleaned : cleaned;
}

function stripBlocksForHeadingScan(text) {
  const blockPattern = /(^[ \t]*(`{3,}|~{3,})[^\n]*\n[\s\S]*?^[ \t]*\2[ \t]*$)|(`+)[^\n]*?\3|\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]/gm;
  return text.replace(blockPattern, (full, _fence, _delim, ticks) =>
    ticks ? full : '\n\n<div data-handbook-block-stripped="1"></div>\n\n'
  );
}

// Named HTML entities (excluding the 5 built-in XML entities) mapped to numeric XML entities.
const HTML_ENTITY_MAP = {
  nbsp: '&#160;',
  iexcl: '&#161;', cent: '&#162;', pound: '&#163;', curren: '&#164;', yen: '&#165;',
  brvbar: '&#166;', sect: '&#167;', uml: '&#168;', copy: '&#169;', ordf: '&#170;',
  laquo: '&#171;', not: '&#172;', shy: '&#173;', reg: '&#174;', macr: '&#175;',
  deg: '&#176;', plusmn: '&#177;', sup2: '&#178;', sup3: '&#179;', acute: '&#180;',
  micro: '&#181;', para: '&#182;', middot: '&#183;', cedil: '&#184;', sup1: '&#185;',
  ordm: '&#186;', raquo: '&#187;', frac14: '&#188;', frac12: '&#189;', frac34: '&#190;',
  times: '&#215;', divide: '&#247;',
  ndash: '&#8211;', mdash: '&#8212;', lsquo: '&#8216;', rsquo: '&#8217;',
  ldquo: '&#8220;', rdquo: '&#8221;', bull: '&#8226;', hellip: '&#8230;',
  prime: '&#8242;', Prime: '&#8243;', lsaquo: '&#8249;', rsaquo: '&#8250;',
  trade: '&#8482;', larr: '&#8592;', uarr: '&#8593;', rarr: '&#8594;', darr: '&#8595;',
  harr: '&#8596;', crarr: '&#8629;', lArr: '&#8656;', rArr: '&#8658;', hArr: '&#8660;',
  forall: '&#8704;', part: '&#8706;', exist: '&#8707;', empty: '&#8709;', nabla: '&#8711;',
  isin: '&#8712;', notin: '&#8713;', prod: '&#8719;', sum: '&#8721;', minus: '&#8722;',
  radic: '&#8730;', prop: '&#8733;', infin: '&#8734;', ang: '&#8736;', and: '&#8743;',
  or: '&#8744;', cap: '&#8745;', cup: '&#8746;', int: '&#8747;', sim: '&#8764;',
  cong: '&#8773;', asymp: '&#8776;', ne: '&#8800;', equiv: '&#8801;', le: '&#8804;',
  ge: '&#8805;', sub: '&#8834;', sup: '&#8835;', oplus: '&#8853;', otimes: '&#8855;',
  perp: '&#8869;', sdot: '&#8901;', lceil: '&#8968;', rceil: '&#8969;',
  lfloor: '&#8970;', rfloor: '&#8971;', lang: '&#10216;', rang: '&#10217;',
  ensp: '&#8194;', emsp: '&#8195;', thinsp: '&#8201;', zwnj: '&#8204;', zwj: '&#8205;',
  alpha: '&#945;', beta: '&#946;', gamma: '&#947;', delta: '&#948;', epsilon: '&#949;',
  zeta: '&#950;', eta: '&#951;', theta: '&#952;', iota: '&#953;', kappa: '&#954;',
  lambda: '&#955;', mu: '&#956;', nu: '&#957;', xi: '&#958;', pi: '&#960;',
  rho: '&#961;', sigma: '&#963;', tau: '&#964;', upsilon: '&#965;', phi: '&#966;',
  chi: '&#967;', psi: '&#968;', omega: '&#969;',
  Alpha: '&#913;', Beta: '&#914;', Gamma: '&#915;', Delta: '&#916;', Theta: '&#920;',
  Lambda: '&#923;', Xi: '&#926;', Pi: '&#928;', Sigma: '&#931;', Phi: '&#934;',
  Psi: '&#936;', Omega: '&#937;',
};

function renderMathMl(latex, display, filePath, mathErrors, stats) {
  let raw;
  try {
    raw = katex.renderToString(latex, {
      displayMode: display,
      throwOnError: true,
      strict: 'ignore',
      trust: false,
      output: 'mathml',
    });
  } catch (e) {
    mathErrors.push({ file: path.relative(root, filePath), latex, error: e.message });
    return `<code class="math-error">${escXml(latex)}</code>`;
  }
  stats.formulas++;
  // Extract inner <math ...>...</math> from KaTeX's <span class="katex"> wrapper
  const m = raw.match(/<math[\s\S]*<\/math>/);
  let mathEl = m ? m[0] : raw;
  // Strip redundant <annotation encoding="application/x-tex"> (saves ~16.8% XHTML & DOM load)
  mathEl = mathEl.replace(/<annotation\s+encoding="application\/x-tex">[\s\S]*?<\/annotation>/g, '');
  if (!/<annotation\b/.test(mathEl)) {
    mathEl = mathEl.replace(/<semantics>([\s\S]*?)<\/semantics>/g, '$1');
  }
  if (!/\bxmlns=/.test(mathEl)) {
    mathEl = mathEl.replace(/^<math\b/, '<math xmlns="http://www.w3.org/1998/Math/MathML"');
  }
  if (display) {
    if (!/\bdisplay=/.test(mathEl)) {
      mathEl = mathEl.replace(/^<math\b/, '<math display="block"');
    }
    return `<div class="math-display">${mathEl}</div>`;
  }
  if (!/\bdisplay=/.test(mathEl)) {
    mathEl = mathEl.replace(/^<math\b/, '<math display="inline"');
  }
  return `<span class="math-inline">${mathEl}</span>`;
}

function protectMathForEpub(text, filePath, mathErrors, stats) {
  const fragments = [];
  const pattern = /(^[ \t]*```[^\n]*\n[\s\S]*?^[ \t]*```[^\n]*$)|(`+)[^\n]*?\2|\$\$([\s\S]*?)\$\$|\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)|(?<!\\)\$(?!\$)((?:\\.|[^$\n])+?)(?<!\\)\$/gm;
  const protectedText = text.replace(
    pattern,
    (full, fence, ticks, display1, display2, inline1, inline2, offset, src) => {
      if (fence || ticks) return full;
      const display = display1 !== undefined || display2 !== undefined;
      const latex = display1 ?? display2 ?? inline1 ?? inline2;
      const mathHtml = renderMathMl(latex, display, filePath, mathErrors, stats);
      const id = fragments.length;
      fragments.push(mathHtml);
      if (!display) return `<span data-epub-math="${id}"></span>`;

      const lineStart = src.lastIndexOf('\n', offset - 1) + 1;
      const linePrefix = src.slice(lineStart, offset);
      const beforeLine = src.slice(0, lineStart);
      const afterMatch = src.slice(offset + full.length);
      const placeholder = `<div data-epub-math="${id}"></div>`;
      if (/^[ \t]*(?:>[ \t]*)+$/.test(linePrefix)) {
        const bqBlank = linePrefix.replace(/[ \t]+$/, '');
        const hasPreBlank =
          !beforeLine ||
          /(?:^|\n)[ \t]*(?:>[ \t]*)+[ \t]*\n$/.test(beforeLine) ||
          /(?:^|\n)[ \t]*\n$/.test(beforeLine);
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
      const slot = afterEmptyListMarker ? `<span data-epub-math="${id}"></span>` : placeholder;
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
    }
  );
  return {
    protectedText,
    restore: html => html.replace(/<(div|span) data-epub-math="(\d+)"><\/\1>/g, (_, _tag, id) => fragments[+id]),
  };
}

function toStrictXhtml(html) {
  // Strip illegal XML 1.0 control chars
  let out = html.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '');
  // Self-close HTML5 void elements
  out = out.replace(
    /<(area|base|br|col|embed|hr|img|input|link|meta|param|source|track|wbr)(\b[^>]*)?>/gi,
    (full, tag, attrs = '') => {
      const trimmed = attrs.replace(/\/\s*$/, '').trimEnd();
      return `<${tag.toLowerCase()}${trimmed}/>`;
    }
  );
  // Expand boolean attributes (controls, disabled, checked, open, hidden) in tags
  out = out.replace(
    /<([a-z][a-z0-9-]*)(\s[^>]*?)(\/?)>/gi,
    (full, tag, attrs, selfClose) => {
      const fixedAttrs = attrs.replace(
        /\s(controls|disabled|checked|open|hidden|readonly|selected)(?=\s|$)/gi,
        (_, attr) => ` ${attr.toLowerCase()}="${attr.toLowerCase()}"`
      );
      return `<${tag}${fixedAttrs}${selfClose}>`;
    }
  );
  // Replace named HTML entities with numeric XML references
  out = out.replace(/&([a-zA-Z][a-zA-Z0-9]+);/g, (full, name) => {
    if (name === 'amp' || name === 'lt' || name === 'gt' || name === 'quot' || name === 'apos') {
      return full;
    }
    return HTML_ENTITY_MAP[name] ?? `&amp;${name};`;
  });
  // Escape any remaining bare '&'
  out = out.replace(/&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)/g, '&amp;');
  // Remove invalid <p><div class="math-display">...</div></p> nesting if marked wrapped a display block
  out = out.replace(/<p>\s*(<div class="math-display">[\s\S]*?<\/div>)\s*<\/p>/g, '$1');
  return out;
}

function classifyBlockquoteEpub(innerHtml) {
  const lead = innerHtml.match(/<p>\s*(?:\[!([A-Z]+)\]|<strong>([\s\S]*?)<\/strong>)/);
  if (lead) {
    const alertType = (lead[1] || '').toUpperCase();
    const strongText = (lead[2] || '').replace(/<[^>]+>/g, '');
    if (alertType === 'CAUTION' || /误区|常见错误|避坑/.test(strongText)) return 'callout callout-misconception';
    if (alertType === 'WARNING' || /跨软件|工程|端序|实验校验|推广边界|注意|边界|符号辨析|口径/.test(strongText)) return 'callout callout-pitfall';
    if (alertType === 'TIP' || /随手算|直觉|把左矩阵|小结|速览/.test(strongText)) return 'callout callout-intuition';
    if (alertType === 'IMPORTANT' || /数学勘误|勘误/.test(strongText)) return 'callout callout-errata';
    if (alertType === 'NOTE' || /进阶注记|前沿注记|跨文献|补充|说明/.test(strongText)) return 'callout callout-note';
  }
  if (/定理|公理|规则|引理/.test(innerHtml.slice(0, 120))) return 'callout callout-theorem';
  return 'callout callout-intuition';
}

function cleanTitleUnicode(rawMdTitle) {
  // Render inline TeX in heading titles to MathML, drop <annotation>, strip tags -> clean Unicode!
  const replaced = String(rawMdTitle || '').replace(
    /(?<!\\)\$(?!\$)((?:\\.|[^$\n])+?)(?<!\\)\$/g,
    (_, latex) => {
      try {
        const mml = katex.renderToString(latex, {
          displayMode: false,
          throwOnError: true,
          strict: 'ignore',
          output: 'mathml',
        });
        return mml.replace(/<annotation[\s\S]*?<\/annotation>/g, '').replace(/<[^>]+>/g, '');
      } catch {
        return latex;
      }
    }
  );
  return replaced.replace(/`([^`]+)`/g, '$1').replace(/\*\*([^*]+)\*\*/g, '$1').replace(/\*([^*]+)\*/g, '$1').replace(/\s+/g, ' ').trim();
}

const EPUB_CSS = `/* Quantum Computing Handbook — EPUB 3 + Native MathML 3 Stylesheet */
:root {
  color-scheme: light dark;
  --ink: #1e2a27;
  --muted: #586c66;
  --accent: #1e6b5a;
  --blue: #1f5a92;
  --amber: #b7791f;
  --red: #b84a2e;
  --paper: #ffffff;
  --surface: rgba(128, 128, 128, 0.08);
  --rule: rgba(128, 128, 128, 0.28);
}
@media (prefers-color-scheme: dark) {
  :root {
    --ink: #e5ece9;
    --muted: #9eb2ab;
    --accent: #6bc4ae;
    --blue: #7ab3e8;
    --amber: #e2b05b;
    --red: #e58770;
    --paper: #141b19;
    --surface: rgba(255, 255, 255, 0.07);
    --rule: rgba(255, 255, 255, 0.18);
  }
}
body {
  margin: 0;
  padding: 0 0.6em;
  line-height: 1.72;
  color: var(--ink);
  font-family: "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
  overflow-wrap: break-word;
}
h1, h2, h3, h4 {
  font-weight: 700;
  line-height: 1.38;
  color: var(--ink);
  page-break-after: avoid;
  break-after: avoid;
}
h1 {
  font-size: 1.52em;
  margin: 0.4em 0 0.8em 0;
  padding: 0.35em 0;
  border-top: 2px solid var(--accent);
  border-bottom: 1px solid var(--rule);
}
h2 {
  font-size: 1.22em;
  margin: 1.35em 0 0.55em 0;
  padding-left: 0.5em;
  border-left: 3px solid var(--accent);
}
h3 { font-size: 1.07em; margin: 1.05em 0 0.4em 0; color: var(--blue); }
h4 { font-size: 1em; margin: 0.9em 0 0.35em 0; }
p { margin: 0.62em 0; }
a { color: var(--blue); text-decoration: underline; }
ul, ol { margin: 0.5em 0 0.85em 0; padding-left: 1.45em; }
li { margin: 0.28em 0; }
code {
  font-family: Menlo, Consolas, Monaco, monospace;
  font-size: 0.87em;
  background: var(--surface);
  padding: 0.1em 0.3em;
  border-radius: 3px;
}
pre {
  font-family: Menlo, Consolas, Monaco, monospace;
  font-size: 0.83em;
  line-height: 1.5;
  background: var(--surface);
  border: 1px solid var(--rule);
  border-left: 3px solid var(--accent);
  border-radius: 4px;
  padding: 0.68em 0.82em;
  white-space: pre-wrap;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
pre code { background: none; padding: 0; }
blockquote {
  margin: 0.88em 0;
  padding: 0.58em 0.88em;
  background: var(--surface);
  border-left: 3.5px solid var(--accent);
  border-radius: 0 4px 4px 0;
}
blockquote.callout-misconception { border-left-color: var(--red); }
blockquote.callout-pitfall { border-left-color: var(--amber); }
blockquote.callout-note { border-left-color: var(--blue); }
blockquote.callout-errata { border-left-color: #c05621; }
blockquote.callout-theorem { border-left-color: var(--accent); }
.table-wrap {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin: 0.9em 0;
}
.table-wrap table {
  margin: 0;
  min-width: 100%;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 0.9em 0;
  font-size: 0.84em;
  line-height: 1.48;
}
th, td {
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
  padding: 0.4em 0.48em;
  text-align: left;
  vertical-align: top;
  overflow-wrap: break-word;
}
th { background: var(--surface); font-weight: 700; }
figure {
  margin: 1em 0;
  padding: 0.55em;
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 6px;
  text-align: center;
  break-inside: avoid;
}
figure img, img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
}
figure.flowchart img,
figure.diagram img {
  background: #FAF8F3;
  padding: 0.45em;
  border-radius: 6px;
  box-sizing: border-box;
}
@media (prefers-color-scheme: dark) {
  figure.flowchart img,
  figure.diagram img {
    filter: brightness(0.95);
  }
}
figcaption {
  margin-top: 0.5em;
  font-size: 0.84em;
  color: var(--muted);
  text-align: left;
}
.math-display {
  margin: 0.82em 0;
  padding: 0.4em 0.35em;
  max-width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  text-align: center;
  font-size: 0.94em;
}
math[display="block"] {
  overflow-x: auto;
  max-width: 100%;
}
.math-inline { white-space: normal; }
.eyebrow {
  font-size: 0.76em;
  letter-spacing: 0.08em;
  color: var(--accent);
  text-transform: uppercase;
  margin-bottom: 0.25em;
}
.part-jump-bar {
  margin: 0.65em 0 1em 0;
  padding: 0.5em 0.7em;
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 6px;
  font-size: 0.84em;
  line-height: 1.65;
}
.part-jump-bar a, .part-jump-bar strong {
  margin-right: 0.7em;
  white-space: nowrap;
}
nav#toc ol { padding-left: 1.35em; }
nav#toc > ol > li { margin: 0.45em 0; }
.cover-page {
  margin: 0;
  padding: 0;
  text-align: center;
}
.cover-page img {
  max-width: 100%;
  max-height: 98vh;
  width: auto;
  height: auto;
}
.code-ref-pill {
  font-family: Menlo, Consolas, monospace;
  font-size: 0.86em;
  color: var(--muted);
}
`;

function wrapXhtml(title, bodyHtml, { cssHref = '../styles/epub.css', bodyClass = '' } = {}) {
  const clsAttr = bodyClass ? ` class="${escXml(bodyClass)}"` : '';
  return `<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <title>${escXml(title)}</title>
  <link rel="stylesheet" type="text/css" href="${escXml(cssHref)}"/>
</head>
<body${clsAttr}>
${bodyHtml}
</body>
</html>
`;
}

// Inline Python 3 packager (zip -9 max compression) & strict EPUB 3 validator
const PYTHON_PACK_AND_VERIFY = `
import json, pathlib, shutil, subprocess, sys, urllib.parse, zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

stage = pathlib.Path(sys.argv[1])
epub_path = pathlib.Path(sys.argv[2])
report_path = pathlib.Path(sys.argv[3])
meta_json = json.loads(sys.argv[4])

epub_path.parent.mkdir(parents=True, exist_ok=True)
report_path.parent.mkdir(parents=True, exist_ok=True)
if epub_path.exists():
    epub_path.unlink()

# 1. Pack EPUB 3 ZIP (mimetype MUST be entry #0, ZIP_STORED, exact bytes; remaining files zip -9)
zip_bin = shutil.which("zip")
if zip_bin:
    (stage / "mimetype").write_bytes(b"application/epub+zip")
    subprocess.run([zip_bin, "-X0", "-q", str(epub_path), "mimetype"], cwd=stage, check=True)
    subprocess.run([zip_bin, "-X9", "-r", "-q", str(epub_path), "META-INF", "OEBPS"], cwd=stage, check=True)
else:
    with zipfile.ZipFile(epub_path, "w") as zf:
        zf.writestr("mimetype", b"application/epub+zip", compress_type=zipfile.ZIP_STORED)
        for rel_root in ["META-INF", "OEBPS"]:
            base = stage / rel_root
            for p in sorted(base.rglob("*")):
                if p.is_file():
                    arcname = p.relative_to(stage).as_posix()
                    zf.write(p, arcname=arcname, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

# 2. Strict EPUB 3 + EPUB 2 NCX + Accessibility verification directly from written archive
errors = []
xml_checked = 0
math_elements = 0
annotation_count = 0
svg_assets = 0
flow_svg_count = 0
flow_svg_with_bg = 0
xhtml_files = []
max_xhtml_bytes = 0
max_xhtml_name = ""
ids_by_arc = {}
links_to_check = []
has_nav_in_spine = False
has_ncx_toc = False
has_a11y_meta = False

with zipfile.ZipFile(epub_path, "r") as zf:
    infos = zf.infolist()
    names = set(zf.namelist())
    if not infos or infos[0].filename != "mimetype":
        errors.append("mimetype is not the first ZIP entry")
    else:
        if infos[0].compress_type != zipfile.ZIP_STORED:
            errors.append(f"mimetype must be ZIP_STORED, got {infos[0].compress_type}")
        if zf.read("mimetype") != b"application/epub+zip":
            errors.append("mimetype content mismatch")

    if "OEBPS/assets/cover-banner-static.svg" in names:
        errors.append("Unused OEBPS/assets/cover-banner-static.svg should not be packaged")

    for name in sorted(names):
        low = name.lower()
        if low.endswith((".xhtml", ".opf", ".xml", ".ncx", ".svg")):
            xml_checked += 1
            raw = zf.read(name)
            try:
                root = ET.fromstring(raw)
            except Exception as exc:
                errors.append(f"XML parse error in {name}: {exc}")
                continue
            if low.endswith(".svg"):
                svg_assets += 1
                if name.startswith("OEBPS/assets/flow-"):
                    flow_svg_count += 1
                    if b'fill="#FAF8F3"' in raw:
                        flow_svg_with_bg += 1
                    else:
                        errors.append(f"Mermaid SVG missing warm-white bg rect: {name}")
            if low.endswith(".ncx"):
                for el in root.iter():
                    if el.tag.rsplit("}", 1)[-1] == "content" and el.attrib.get("src"):
                        links_to_check.append((name, "src", el.attrib["src"]))
            if low.endswith(".xhtml"):
                xhtml_files.append(name)
                if len(raw) > max_xhtml_bytes:
                    max_xhtml_bytes = len(raw)
                    max_xhtml_name = name
                id_set = set()
                for el in root.iter():
                    tag_local = el.tag.rsplit("}", 1)[-1]
                    if tag_local == "math":
                        math_elements += 1
                    elif tag_local == "annotation":
                        annotation_count += 1
                    eid = el.attrib.get("id")
                    if eid:
                        id_set.add(eid)
                    for attr in ("href", "src"):
                        val = el.attrib.get(attr)
                        if val is not None:
                            links_to_check.append((name, attr, val))
                ids_by_arc[name] = id_set

    if annotation_count > 0:
        errors.append(f"Found {annotation_count} redundant <annotation> nodes in XHTML")

    # Verify container.xml -> OPF -> manifest, spine, NCX & Accessibility 1.1 metadata
    if "META-INF/container.xml" not in names:
        errors.append("Missing META-INF/container.xml")
    else:
        c_root = ET.fromstring(zf.read("META-INF/container.xml"))
        rf = c_root.find(".//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile")
        opf_path = rf.attrib.get("full-path") if rf is not None else None
        if not opf_path or opf_path not in names:
            errors.append(f"Missing OPF rootfile: {opf_path}")
        else:
            opf_dir = pathlib.PurePosixPath(opf_path).parent
            opf_root = ET.fromstring(zf.read(opf_path))
            ns = {"opf": "http://www.idpf.org/2007/opf"}
            manifest_ids = {}
            for item in opf_root.findall(".//opf:manifest/opf:item", ns):
                iid = item.attrib.get("id", "")
                href = urllib.parse.unquote(item.attrib.get("href", ""))
                target = (opf_dir / href).as_posix()
                manifest_ids[iid] = target
                if target not in names:
                    errors.append(f"Manifest item missing in ZIP: {target}")
            spine_el = opf_root.find(".//opf:spine", ns)
            if spine_el is not None and spine_el.attrib.get("toc") == "ncx" and "ncx" in manifest_ids:
                has_ncx_toc = True
            else:
                errors.append("Spine missing toc='ncx' or manifest missing ncx item")
            for ref in opf_root.findall(".//opf:spine/opf:itemref", ns):
                idref = ref.attrib.get("idref", "")
                if idref == "nav":
                    has_nav_in_spine = True
                if idref not in manifest_ids:
                    errors.append(f"Spine idref missing in manifest: {idref}")
            if not has_nav_in_spine:
                errors.append("nav.xhtml is not included in <spine>")
            meta_props = {}
            for mel in opf_root.findall(".//opf:metadata/opf:meta", ns):
                prop = mel.attrib.get("property", "")
                if prop:
                    meta_props.setdefault(prop, []).append((mel.text or "").strip())
            feats = set(meta_props.get("schema:accessibilityFeature", []))
            if (
                "schema:accessMode" in meta_props
                and "dcterms:conformsTo" in meta_props
                and {"MathML", "alternativeText", "tableOfContents"}.issubset(feats)
            ):
                has_a11y_meta = True
            else:
                errors.append("Missing EPUB Accessibility 1.1 schema.org or dcterms:conformsTo metadata")

    # Verify every relative href/src and #fragment across all XHTML and toc.ncx documents
    for src_arc, attr, val in links_to_check:
        if not val or val.startswith(("http://", "https://", "mailto:", "data:", "tel:")):
            continue
        base_dir = pathlib.PurePosixPath(src_arc).parent
        if val.startswith("#"):
            target_arc = src_arc
            frag = urllib.parse.unquote(val[1:])
        else:
            part, _, raw_frag = val.partition("#")
            frag = urllib.parse.unquote(raw_frag)
            joined = pathlib.PurePosixPath(urllib.parse.unquote(part))
            parts_acc = list(base_dir.parts)
            for seg in joined.parts:
                if seg in ("", "."):
                    continue
                elif seg == "..":
                    if parts_acc:
                        parts_acc.pop()
                else:
                    parts_acc.append(seg)
            target_arc = "/".join(parts_acc)
        if target_arc not in names:
            errors.append(f"Broken {attr} in {src_arc}: {val} -> {target_arc}")
        elif frag and target_arc in ids_by_arc and frag not in ids_by_arc[target_arc]:
            errors.append(f"Broken fragment #{frag} in {src_arc} -> {target_arc}")

size_bytes = epub_path.stat().st_size
report = {
    "generatedAt": datetime.now(timezone.utc).isoformat(),
    "output": meta_json["output"],
    "edition": meta_json["edition"],
    "passed": len(errors) == 0,
    "metrics": {
        "fileSizeBytes": size_bytes,
        "fileSizeMiB": round(size_bytes / (1024 * 1024), 3),
        "zipEntries": len(names),
        "xhtmlDocuments": len(xhtml_files),
        "maxXhtmlName": max_xhtml_name,
        "maxXhtmlKiB": round(max_xhtml_bytes / 1024, 1),
        "xmlFilesValidated": xml_checked,
        "mathmlElements": math_elements,
        "annotationElements": annotation_count,
        "svgAssets": svg_assets,
        "mermaidSvgsWithWarmBg": f"{flow_svg_with_bg}/{flow_svg_count}",
        "linksValidated": len(links_to_check),
        "diagramsRendered": meta_json["diagrams"],
        "formulasRendered": meta_json["formulas"],
    },
    "checks": {
        "mimetypeFirstAndStored": not any("mimetype" in e for e in errors),
        "allXmlWellFormed": not any("XML parse error" in e for e in errors),
        "manifestAndSpineComplete": not any("Manifest" in e or "Spine" in e for e in errors),
        "navInSpine": has_nav_in_spine,
        "ncxFallbackPresent": has_ncx_toc,
        "a11yMetadataPresent": has_a11y_meta,
        "allMermaidDarkSafe": flow_svg_with_bg == flow_svg_count,
        "zeroMathAnnotations": annotation_count == 0,
        "zeroBrokenLinksOrFragments": not any("Broken " in e for e in errors),
    },
    "errors": errors[:50],
}
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps({
    "output": report["output"],
    "passed": report["passed"],
    "fileSizeMiB": report["metrics"]["fileSizeMiB"],
    "xhtmlDocuments": report["metrics"]["xhtmlDocuments"],
    "maxXhtml": f"{report['metrics']['maxXhtmlName']} ({report['metrics']['maxXhtmlKiB']} KiB)",
    "mathmlElements": report["metrics"]["mathmlElements"],
    "mermaidDarkSafe": report["metrics"]["mermaidSvgsWithWarmBg"],
    "svgAssets": report["metrics"]["svgAssets"],
    "errorCount": len(errors),
    "checks": report["checks"],
}, ensure_ascii=False, indent=2))
sys.exit(0 if report["passed"] else 1)
`;

function injectMermaidWarmBg(svgText) {
  if (!svgText || svgText.includes('class="qch-mermaid-bg"')) return svgText;
  return svgText.replace(/<svg\b[^>]*>/i, openTag => {
    const vb = openTag.match(/\bviewBox=["']([^"']+)["']/i)?.[1]?.trim();
    let xyAttr = '';
    if (vb) {
      const nums = vb.split(/[\s,]+/).map(Number);
      if (nums.length === 4 && Number.isFinite(nums[0]) && Number.isFinite(nums[1]) && (nums[0] !== 0 || nums[1] !== 0)) {
        xyAttr = `x="${nums[0]}" y="${nums[1]}" `;
      }
    }
    return `${openTag}<rect class="qch-mermaid-bg" ${xyAttr}width="100%" height="100%" fill="#FAF8F3" rx="8"/>`;
  });
}

function scanMarkdownHeadings(rawMd) {
  const used = new Map();
  const usedSafe = new Set();
  const list = marked.lexer(stripBlocksForHeadingScan(rawMd))
    .filter(tok => tok.type === 'heading')
    .map(tok => {
      const base = slug(tok.text);
      const cnt = used.get(base) || 0;
      used.set(base, cnt + 1);
      const rawId = base + (cnt ? '-' + cnt : '');
      let safeId = xmlIdSafe(rawId);
      let suffix = 1;
      while (usedSafe.has(safeId)) safeId = `${xmlIdSafe(rawId)}-${suffix++}`;
      usedSafe.add(safeId);
      return { level: tok.depth, rawTitle: tok.text, title: cleanTitleUnicode(tok.text), rawId, id: safeId };
    });
  const mapRawToSafe = new Map(list.map(h => [h.rawId, h.id]));
  for (const m of rawMd.matchAll(/<span id="([^"]+)"><\/span>/g)) {
    const orig = m[1];
    let safeId = xmlIdSafe(orig);
    if (usedSafe.has(safeId)) safeId = `alias-${safeId}`;
    let suffix = 1;
    while (usedSafe.has(safeId)) safeId = `alias-${xmlIdSafe(orig)}-${suffix++}`;
    usedSafe.add(safeId);
    mapRawToSafe.set(orig, safeId);
  }
  return { list, mapRawToSafe };
}

function splitExercisesByPart(rawMd, orderedGroups) {
  const lines = rawMd.split('\n');
  let inFence = false;
  let fenceChar = '';
  const preambleLines = [];
  const sections = [];
  let current = null;

  for (const line of lines) {
    const fenceMatch = line.match(/^[ \t]*(`{3,}|~{3,})/);
    if (fenceMatch) {
      if (!inFence) {
        inFence = true;
        fenceChar = fenceMatch[1][0];
      } else if (fenceMatch[1][0] === fenceChar) {
        inFence = false;
        fenceChar = '';
      }
    }
    if (!inFence && /^##\s+/.test(line)) {
      if (current) sections.push(current);
      current = { heading: line.replace(/^##\s+/, '').trim(), lines: [line] };
    } else if (current) {
      current.lines.push(line);
    } else {
      preambleLines.push(line);
    }
  }
  if (current) sections.push(current);

  const introBody = preambleLines.filter(l => !/^#\s+/.test(l)).join('\n').trim();
  const sectionByChapterId = new Map();
  const trailingSections = [];

  for (const sec of sections) {
    const mainMatch = sec.heading.match(/^第\s*(\d+)\s*章/);
    const qmMatch = sec.heading.match(/^量子力学\s+Q(\d+)/i);
    if (mainMatch) {
      sectionByChapterId.set(String(Number(mainMatch[1])).padStart(2, '0'), sec);
    } else if (qmMatch) {
      sectionByChapterId.set(`Q${qmMatch[1]}`, sec);
    } else {
      trailingSections.push(sec);
    }
  }

  let assignedCount = 0;
  const parts = orderedGroups.map((grp, idx) => {
    const partNum = idx + 1;
    const cn = CN_NUM[idx] || String(partNum);
    const shortPart = `第${cn}篇`;
    const partSecs = [];
    for (const cid of grp.ids) {
      const sec = sectionByChapterId.get(cid);
      if (sec) {
        partSecs.push(sec);
        assignedCount++;
      }
    }
    if (idx === orderedGroups.length - 1 && trailingSections.length) {
      partSecs.push(...trailingSections);
      assignedCount += trailingSections.length;
    }
    const cleanPartLabel = grp.label.replace(/^第[一二三四五六七八九十\d]+篇\s*[·｜|]\s*/, '');
    const h1 = `附录 D（${shortPart}）· 自检题参考解答：${cleanPartLabel}`;
    const leadPara = idx === 0 && introBody
      ? introBody
      : `本分册收录**${grp.label}**（共 ${grp.ids.length} 章）的全部章末自检题零跳步参考解答。`;
    const markdown = `# ${h1}\n\n${leadPara}\n\n${partSecs.map(s => s.lines.join('\n')).join('\n\n')}\n`;
    return {
      partNum,
      shortPart,
      xname: `app-exercises-p${partNum}.xhtml`,
      navLabel: `${shortPart}解答 · ${cleanPartLabel}`,
      title: h1,
      markdown,
    };
  });

  if (assignedCount !== sections.length) {
    throw new Error(`exercises.md split mismatch: assigned ${assignedCount} of ${sections.length} H2 sections`);
  }
  return parts;
}

function renderNavListHtml(items, indent = '      ') {
  return items.map(item => {
    const link = `<a href="${escXml(item.href)}">${escXml(item.label)}</a>`;
    if (item.children && item.children.length) {
      return `${indent}<li>${link}\n${indent}  <ol>\n${renderNavListHtml(item.children, indent + '    ')}\n${indent}  </ol>\n${indent}</li>`;
    }
    return `${indent}<li>${link}</li>`;
  }).join('\n');
}

function renderNcxNavPoints(items, state, indent = '    ') {
  return items.map(item => {
    const order = ++state.playOrder;
    const npId = `navPoint-${order}`;
    const childrenXml = item.children && item.children.length
      ? `\n${renderNcxNavPoints(item.children, state, indent + '  ')}\n${indent}`
      : '';
    return `${indent}<navPoint id="${npId}" playOrder="${order}">\n${indent}  <navLabel><text>${escXml(item.label)}</text></navLabel>\n${indent}  <content src="${escXml(item.href)}"/>${childrenXml}</navPoint>`;
  }).join('\n');
}

function maxTreeDepth(items, depth = 1) {
  let maxD = depth;
  for (const item of items) {
    if (item.children && item.children.length) {
      maxD = Math.max(maxD, maxTreeDepth(item.children, depth + 1));
    }
  }
  return maxD;
}

async function main() {
  const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'qch-epub-'));
  const oebpsDir = path.join(tmpDir, 'OEBPS');
  const textDir = path.join(oebpsDir, 'text');
  const assetsDir = path.join(oebpsDir, 'assets');
  const stylesDir = path.join(oebpsDir, 'styles');
  const metaInfDir = path.join(tmpDir, 'META-INF');

  await Promise.all([
    fs.mkdir(textDir, { recursive: true }),
    fs.mkdir(assetsDir, { recursive: true }),
    fs.mkdir(stylesDir, { recursive: true }),
    fs.mkdir(metaInfDir, { recursive: true }),
    fs.mkdir(distDir, { recursive: true }),
  ]);

  const allMdFiles = (await walk(source)).filter(f => f.endsWith('.md')).sort();
  const contents = new Map(await Promise.all(allMdFiles.map(async f => [f, await fs.readFile(f, 'utf8')])));

  const readmePath = path.join(source, 'README.md');
  const exercisesFile = path.join(source, 'appendices/exercises.md');
  const edition = (contents.get(readmePath) || '').match(/^>\s*版本：(\d{4}-\d{2}-\d{2})/m)?.[1];
  if (!edition) throw new Error('handbook/README.md must declare "> 版本：YYYY-MM-DD"');

  const titleOf = f => {
    const m = (contents.get(f) || '').match(/^#\s+(.+)/m);
    return cleanTitleUnicode(m ? m[1].trim() : path.basename(f, '.md'));
  };

  const chapterFiles = allMdFiles.filter(f => /^\d\d-/.test(path.basename(f)));
  const orderedReading = readingPlan(chapterFiles);

  const appendixFiles = APPENDIX_ORDER
    .map(name => path.join(source, 'appendices', name))
    .filter(f => contents.has(f));

  const allLabFiles = allMdFiles.filter(f => f.includes(`${path.sep}labs${path.sep}`) || f.includes('/labs/'));
  const labFiles = [
    ...LAB_ORDER.map(name => path.join(source, 'labs', name)).filter(f => contents.has(f)),
    ...allLabFiles.filter(f => !LAB_ORDER.includes(path.basename(f))).sort(),
  ];

  const groups = orderedReading.groups.map((g, idx) => {
    const cn = CN_NUM[idx] || String(idx + 1);
    const fullTitle = /^第[一二三四五六七八九十\d]+篇/.test(g.label)
      ? g.label
      : `第${cn}篇 · ${g.label}`;
    return { title: fullTitle, label: g.label, files: g.files };
  });
  if (appendixFiles.length) groups.push({ title: '附录工具书', label: '附录', files: appendixFiles });
  if (labFiles.length) groups.push({ title: '离线动手实验册', label: '实验册', files: labFiles });

  const exercisesParts = contents.has(exercisesFile)
    ? splitExercisesByPart(contents.get(exercisesFile), orderedReading.groups)
    : [];

  const includedFiles = [readmePath, ...groups.flatMap(g => g.files)];
  const fileToXhtml = new Map();
  for (const f of includedFiles) {
    fileToXhtml.set(f, f === exercisesFile && exercisesParts.length ? exercisesParts[0].xname : xhtmlNameFor(f));
  }
  const qmReadme = path.join(source, 'quantum-mechanics/README.md');
  if (!fileToXhtml.has(qmReadme)) fileToXhtml.set(qmReadme, 'ch-q1.xhtml');
  const styleFile = path.join(source, 'STYLE.md');
  if (!fileToXhtml.has(styleFile)) fileToXhtml.set(styleFile, 'intro.xhtml');

  const appendixCodeFor = f => {
    const rel = path.relative(source, f).replaceAll('\\', '/');
    if (!rel.startsWith('appendices/')) return null;
    const idx = APPENDIX_ORDER.indexOf(path.basename(rel));
    return idx >= 0 ? `附录 ${String.fromCharCode(65 + idx)}` : '附录';
  };
  const navTitleOf = f => {
    const code = appendixCodeFor(f);
    const t = titleOf(f);
    return code ? `${code} · ${t}` : t;
  };

  // Pre-scan headings & explicit anchor aliases with XML-safe IDs
  const headingsByFile = new Map();
  const validIdsByXhtml = new Map();
  const exercisesFragToTarget = new Map();

  for (const f of includedFiles) {
    if (f === exercisesFile && exercisesParts.length) continue;
    const xname = fileToXhtml.get(f);
    const { list, mapRawToSafe } = scanMarkdownHeadings(contents.get(f));
    headingsByFile.set(f, list);
    validIdsByXhtml.set(xname, mapRawToSafe);
  }
  for (const part of exercisesParts) {
    const { list, mapRawToSafe } = scanMarkdownHeadings(part.markdown);
    part.headings = list;
    part.idMap = mapRawToSafe;
    validIdsByXhtml.set(part.xname, mapRawToSafe);
    for (const [rawId, safeId] of mapRawToSafe.entries()) {
      exercisesFragToTarget.set(rawId, { xname: part.xname, id: safeId });
      exercisesFragToTarget.set(safeId, { xname: part.xname, id: safeId });
    }
  }

  // Lazy Playwright browser (with system Chrome auto-fallback) for Mermaid & 1200x1600 portrait cover PNG
  let browser = null;
  let mermaidServer = null;
  let mermaidPage = null;

  async function ensureBrowser() {
    if (!browser) browser = await launchChromium();
    return browser;
  }

  const embeddedAssets = new Map(); // filename -> media-type
  async function embedAsset(srcAbsPath, targetName, mediaType) {
    if (!embeddedAssets.has(targetName)) {
      await fs.copyFile(srcAbsPath, path.join(assetsDir, targetName));
      embeddedAssets.set(targetName, mediaType);
    }
    return `../assets/${targetName}`;
  }

  async function embedMermaidSvgText(svgText, flowName) {
    const darkSafeSvg = injectMermaidWarmBg(svgText);
    await fs.writeFile(path.join(assetsDir, flowName), darkSafeSvg, 'utf8');
    embeddedAssets.set(flowName, 'image/svg+xml');
    return `../assets/${flowName}`;
  }

  async function resolveMermaidAsset(code) {
    const flowHash = crypto.createHash('sha256').update(code).digest('hex').slice(0, 14);
    const flowName = `flow-${flowHash}.svg`;
    if (embeddedAssets.has(flowName)) return `../assets/${flowName}`;

    const readerFlow = path.join(readerDir, 'assets', flowName);
    if (fsSync.existsSync(readerFlow)) {
      return embedMermaidSvgText(await fs.readFile(readerFlow, 'utf8'), flowName);
    }
    const cacheKey = crypto.createHash('sha256').update('mermaid-11.6-reader-v3\n' + code).digest('hex');
    const cachedFile = path.join(workCache, `${cacheKey}.svg`);
    if (fsSync.existsSync(cachedFile)) {
      return embedMermaidSvgText(await fs.readFile(cachedFile, 'utf8'), flowName);
    }
    if (!mermaidPage) {
      mermaidServer = http.createServer(async (req, res) => {
        if (req.url === '/') {
          res.setHeader('Content-Type', 'text/html');
          res.end('<!doctype html><html><head><meta charset="utf-8"></head><body></body></html>');
          return;
        }
        const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\//, '');
        const resolved = path.resolve(here, rel);
        if (!resolved.startsWith(here + path.sep)) { res.writeHead(403).end(); return; }
        try {
          res.setHeader('Content-Type', /\.m?js$/.test(resolved) ? 'text/javascript' : 'application/octet-stream');
          res.end(await fs.readFile(resolved));
        } catch { res.writeHead(404).end(); }
      });
      await new Promise(resolve => mermaidServer.listen(0, '127.0.0.1', resolve));
      const b = await ensureBrowser();
      mermaidPage = await b.newPage({ viewport: { width: 1400, height: 1000 } });
      await mermaidPage.goto(`http://127.0.0.1:${mermaidServer.address().port}/`);
      await mermaidPage.evaluate(async () => {
        const { default: mermaid } = await import('/node_modules/mermaid/dist/mermaid.esm.min.mjs');
        mermaid.initialize({
          startOnLoad: false, securityLevel: 'strict', theme: 'base', htmlLabels: false,
          fontFamily: 'PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif',
          themeVariables: { primaryColor: '#e8f2ef', primaryTextColor: '#183934', primaryBorderColor: '#72988e', lineColor: '#66837b', secondaryColor: '#f2eadb', tertiaryColor: '#f7f7f2', fontSize: '17px' },
          flowchart: { htmlLabels: false, curve: 'linear', padding: 18, nodeSpacing: 32, rankSpacing: 42 },
        });
        window.mermaid = mermaid;
      });
    }
    const svg = await mermaidPage.evaluate(
      async ({ id, src }) => (await window.mermaid.render(id, src)).svg,
      { id: `diagram-${flowHash}`, src: code }
    );
    return embedMermaidSvgText(svg, flowName);
  }

  async function generatePortraitCoverPng() {
    // Crop right-hand 3-in-1 workbench (MZI + Bloch + Surface Code) from cover-banner-static.svg
    // into tmpDir ONLY (never packaged as an unreferenced asset inside OEBPS/assets/).
    const coverSvgSrc = path.join(source, 'assets/cover-banner-static.svg');
    const rawSvg = await fs.readFile(coverSvgSrc, 'utf8');
    const croppedSvg = rawSvg.replace(
      /viewBox="0 0 1200 520"/,
      'viewBox="462 14 724 494" width="724" height="494"'
    );
    const workbenchSvgFile = path.join(tmpDir, 'cover-workbench.svg');
    await fs.writeFile(workbenchSvgFile, croppedSvg, 'utf8');

    const coverPngDest = path.join(assetsDir, 'cover.png');
    const coverHtml = `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>
      *{box-sizing:border-box}
      body{margin:0;width:1200px;height:1600px;background:#FAF8F3;font-family:'PingFang SC','Hiragino Sans GB','Noto Sans CJK SC','Microsoft YaHei',sans-serif;color:#142622;padding:54px 68px 48px;display:flex;flex-direction:column;justify-content:space-between}
      .rule{display:grid;grid-template-columns:42% 33% 25%;gap:10px;height:8px}
      .r1{background:#1E6B5A;border-radius:4px}.r2{background:#1F5A92;border-radius:4px}.r3{background:#C28524;border-radius:4px}
      .pill{display:inline-block;margin-top:26px;padding:9px 22px;border-radius:999px;background:#E5F2ED;border:2px solid #B6D5C9;color:#154C40;font-size:20px;font-weight:700;letter-spacing:1.1px}
      h1{font-size:88px;font-weight:800;margin:20px 0 12px;letter-spacing:-1.5px;line-height:1.1}
      .sub{font-size:38px;font-weight:700;color:#1E6B5A;margin:0 0 16px;line-height:1.32}
      .deck{font-size:24px;color:#3E524D;line-height:1.55;margin:0 0 24px}
      .metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:0 0 24px}
      .card{background:#FFFFFF;border:1.8px solid #D9D3C7;border-radius:12px;padding:14px 16px;border-top:5px solid #1E6B5A}
      .card.c2{border-top-color:#1F5A92}.card.c3{border-top-color:#C28524}.card.c4{border-top-color:#B84A2E}
      .card strong{display:block;font-size:28px;font-weight:800;color:#142622;line-height:1.2}
      .card span{display:block;margin-top:5px;font-size:17px;color:#556661;line-height:1.3}
      .plate-wrap{background:#FFFFFF;border:2px solid #D3CDC0;border-radius:16px;padding:12px;box-shadow:0 6px 20px rgba(20,38,34,0.06)}
      .plate{width:100%;height:auto;border-radius:10px;display:block}
      .bar{background:#1B2D2A;color:#F4F1E8;border-left:10px solid #DDA03B;border-radius:12px;padding:22px 28px;font-size:22px;line-height:1.45;white-space:nowrap}
      .bar strong{color:#F8D99B}
      .foot{display:flex;justify-content:space-between;font-size:21px;color:#556661;border-top:2px solid #D7D1C5;padding-top:18px;margin-top:18px}
    </style></head><body>
      <div>
        <div class="rule"><div class="r1"></div><div class="r2"></div><div class="r3"></div></div>
        <div class="pill">QUANTUM COMPUTING HANDBOOK · EPUB 3 + MATHML 3</div>
        <h1>量子计算手册</h1>
        <p class="sub">从直觉、数学与物理到容错、传感与模拟边界</p>
        <p class="deck">从草稿纸能算透的二维小例出发，打通线性代数、量子干涉、核心算法、噪声与容错全链路。</p>
        <div class="metrics">
          <div class="card"><strong>${orderedReading.groups.length} 篇 ${orderedReading.sequence.length} 章</strong><span>主篇 00–21 + 物理 Q1–Q4</span></div>
          <div class="card c2"><strong>50,900+ 公式</strong><span>原生 MathML 3 矢量排版</span></div>
          <div class="card c3"><strong>122 矢量图</strong><span>92 科学图 + 30 流程图</span></div>
          <div class="card c4"><strong>271 题全解</strong><span>零跳步题答 · 38 标准库脚本</span></div>
        </div>
      </div>
      <div class="plate-wrap">
        <img class="plate" src="${escXml(pathToFileURL(workbenchSvgFile).href)}" alt="MZI 干涉、Bloch 球进动与旋转表面码三合一原理图"/>
      </div>
      <div>
        <div class="bar"><strong>统一数学契约：</strong>左共轭 ⟨u|v⟩ · 大端序 |q₁q₀⟩ · 根保真度 F(ρ,σ) · log₂ / ln</div>
        <div class="foot"><span>量子计算手册编写组 · 全书零外网离线出版</span><span>版本 ${escXml(edition)}</span></div>
      </div>
    </body></html>`;
    const coverHtmlFile = path.join(tmpDir, 'cover-render.html');
    await fs.writeFile(coverHtmlFile, coverHtml, 'utf8');
    const b = await ensureBrowser();
    const p = await b.newPage({ viewport: { width: 1200, height: 1600, deviceScaleFactor: 1 } });
    await p.goto(pathToFileURL(coverHtmlFile).href, { waitUntil: 'load' });
    await p.evaluate(async () => { await document.fonts.ready; });
    await p.screenshot({ path: coverPngDest, type: 'png' });
    await p.close();
    embeddedAssets.set('cover.png', 'image/png');
  }

  const mathErrors = [];
  const stats = { formulas: 0, diagrams: 0 };
  const spineDocs = [];

  async function renderMarkdownToXhtmlDoc({
    sourceFile,
    rawMd,
    xname,
    headings,
    idMap,
    pageTitle,
    eyebrow,
    topBannerHtml = '',
    isExercisesPart = false,
  }) {
    let text = rawMd;
    const relSource = path.relative(source, sourceFile).replaceAll('\\', '/');
    let diagramCount = 0;

    for (const match of [...text.matchAll(/```mermaid\n([\s\S]*?)```/g)]) {
      diagramCount++;
      stats.diagrams++;
      const diagramTitle = resolveDiagramTitle(relSource, diagramCount - 1, match[1]);
      const relSvgHref = await resolveMermaidAsset(match[1]);
      const fig = `\n\n<figure class="flowchart"><img src="${escXml(relSvgHref)}" alt="${escXml(diagramTitle)}"/><figcaption>图 ${diagramCount}｜${escXml(diagramTitle)}</figcaption></figure>\n\n`;
      text = text.replace(match[0], fig);
    }

    const { protectedText, restore } = protectMathForEpub(text, sourceFile, mathErrors, stats);
    let hi = 0;
    const pendingImages = [];
    const renderer = new marked.Renderer();
    renderer.heading = function ({ tokens, depth }) {
      const h = headings[hi++];
      return `<h${depth} id="${escXml(h.id)}">${this.parser.parseInline(tokens)}</h${depth}>\n`;
    };
    renderer.image = function ({ href, text: altText, title }) {
      const caption = altText || title || '科学原理图';
      if (/^(https?:|data:)/i.test(href)) {
        return `<figure class="science-figure"><img src="${escXml(href)}" alt="${escXml(caption)}"/><figcaption>${escXml(caption)}</figcaption></figure>`;
      }
      const resolved = path.resolve(path.dirname(sourceFile), href);
      const baseName = path.basename(resolved);
      const ext = path.extname(baseName).toLowerCase();
      const mediaType = ext === '.svg' ? 'image/svg+xml' : ext === '.png' ? 'image/png' : ext === '.jpg' || ext === '.jpeg' ? 'image/jpeg' : 'application/octet-stream';
      pendingImages.push({ resolved, baseName, mediaType });
      return `<figure class="science-figure"><img src="../assets/${escXml(baseName)}" alt="${escXml(caption)}"/><figcaption>${escXml(caption)}</figcaption></figure>`;
    };
    renderer.link = function ({ href, title, tokens }) {
      const label = this.parser.parseInline(tokens);
      if (/^(https?:|mailto:)/i.test(href)) {
        return `<a href="${escXml(href)}"${title ? ` title="${escXml(title)}"` : ''}>${label}</a>`;
      }
      if (href.startsWith('#')) {
        const frag = safeDecode(href.slice(1));
        const mapped = idMap.get(frag);
        if (mapped) return `<a href="#${escXml(mapped)}">${label}</a>`;
        if (isExercisesPart && exercisesFragToTarget.has(frag)) {
          const hit = exercisesFragToTarget.get(frag);
          return `<a href="${escXml(`${hit.xname}#${hit.id}`)}">${label}</a>`;
        }
        return `<a href="${escXml(xname)}">${label}</a>`;
      }
      const [p, rawFrag] = href.split('#');
      const frag = rawFrag ? safeDecode(rawFrag) : '';
      const target = path.resolve(path.dirname(sourceFile), p);
      if (target === exercisesFile && exercisesParts.length) {
        if (frag && exercisesFragToTarget.has(frag)) {
          const hit = exercisesFragToTarget.get(frag);
          return `<a href="${escXml(`${hit.xname}#${hit.id}`)}">${label}</a>`;
        }
        return `<a href="${escXml(exercisesParts[0].xname)}">${label}</a>`;
      }
      if (fileToXhtml.has(target)) {
        const targetXhtml = fileToXhtml.get(target);
        const targetIds = validIdsByXhtml.get(targetXhtml);
        const mapped = frag && targetIds?.get(frag);
        const dest = mapped ? `${targetXhtml}#${mapped}` : targetXhtml;
        return `<a href="${escXml(dest)}">${label}</a>`;
      }
      return `<span class="code-ref-pill">${label}</span>`;
    };

    let bodyHtml = restore(marked.parse(protectedText, { renderer, gfm: true }));
    for (const img of pendingImages) {
      if (fsSync.existsSync(img.resolved)) {
        await embedAsset(img.resolved, img.baseName, img.mediaType);
      }
    }
    bodyHtml = bodyHtml.replace(/<span id="([^"]+)"><\/span>/g, (_, orig) => {
      const mapped = idMap.get(orig) || xmlIdSafe(orig);
      return `<span id="${escXml(mapped)}"></span>`;
    });
    bodyHtml = bodyHtml.replace(/<p>\s*(<figure\b[\s\S]*?<\/figure>)\s*<\/p>/g, '$1');
    bodyHtml = bodyHtml.replace(/<blockquote>([\s\S]*?)<\/blockquote>/g, (_, inner) =>
      `<blockquote class="${classifyBlockquoteEpub(inner)}">${inner}</blockquote>`
    );
    // P0/P1: Wrap every <table> in a touch-scrollable narrow-screen container
    bodyHtml = bodyHtml.replace(/<table\b[\s\S]*?<\/table>/g, tbl => `<div class="table-wrap">${tbl}</div>`);
    bodyHtml = toStrictXhtml(bodyHtml);

    const fullXhtml = wrapXhtml(pageTitle, `<div class="eyebrow">${escXml(eyebrow)}</div>\n${topBannerHtml}${bodyHtml}`);
    await fs.writeFile(path.join(textDir, xname), fullXhtml, 'utf8');

    spineDocs.push({
      id: 'doc-' + xname.replace(/\.xhtml$/, '').replace(/[^a-zA-Z0-9_-]/g, '-'),
      href: `text/${xname}`,
      xname,
      file: sourceFile,
      title: pageTitle,
      hasMath: /<math\b/.test(fullXhtml),
      hasInlineSvg: /<svg\b/.test(fullXhtml),
    });
  }

  try {
    await generatePortraitCoverPng();
    await fs.writeFile(path.join(stylesDir, 'epub.css'), EPUB_CSS, 'utf8');

    // Write cover.xhtml
    const coverXhtml = wrapXhtml(BOOK_TITLE, `<div class="cover-page" epub:type="cover"><img src="../assets/cover.png" alt="${escXml(BOOK_TITLE)} 封面"/></div>`, { bodyClass: 'cover-page' });
    await fs.writeFile(path.join(textDir, 'cover.xhtml'), coverXhtml, 'utf8');
    spineDocs.push({ id: 'doc-cover', href: 'text/cover.xhtml', title: '封面', hasMath: false, hasInlineSvg: false, isCover: true });

    for (const f of includedFiles) {
      if (f === exercisesFile && exercisesParts.length) {
        for (const part of exercisesParts) {
          const jumpLinks = exercisesParts.map(p =>
            p.xname === part.xname
              ? `<strong>${escXml(p.shortPart)}</strong>`
              : `<a href="${escXml(p.xname)}">${escXml(p.shortPart)}</a>`
          ).join(' ');
          const jumpBar = `<div class="part-jump-bar">附录 D 分篇直达：${jumpLinks}</div>\n`;
          await renderMarkdownToXhtmlDoc({
            sourceFile: exercisesFile,
            rawMd: part.markdown,
            xname: part.xname,
            headings: part.headings,
            idMap: part.idMap,
            pageTitle: part.title,
            eyebrow: `附录 D · ${part.shortPart}自检题参考解答`,
            topBannerHtml: jumpBar,
            isExercisesPart: true,
          });
        }
        continue;
      }

      const xname = fileToXhtml.get(f);
      const relSource = path.relative(source, f).replaceAll('\\', '/');
      const appCode = appendixCodeFor(f);
      const eyebrow = relSource === 'README.md'
        ? '导读与统一约定'
        : appCode
          ? `${appCode} · 附录工具书`
          : relSource.startsWith('labs/')
            ? '离线实验册'
            : '量子计算手册';
      await renderMarkdownToXhtmlDoc({
        sourceFile: f,
        rawMd: contents.get(f),
        xname,
        headings: headingsByFile.get(f),
        idMap: validIdsByXhtml.get(xname),
        pageTitle: navTitleOf(f),
        eyebrow,
      });
    }

    if (mathErrors.length) {
      throw new Error(`KaTeX MathML errors (${mathErrors.length}): ${JSON.stringify(mathErrors.slice(0, 5))}`);
    }

    // Build unified TOC tree shared by EPUB 3 nav.xhtml and EPUB 2 toc.ncx
    const introH2s = (headingsByFile.get(readmePath) || []).filter(h => h.level === 2);
    const tocTree = [
      { label: '封面', href: 'text/cover.xhtml' },
      { label: '全书目录', href: 'nav.xhtml' },
      {
        label: titleOf(readmePath),
        href: 'text/intro.xhtml',
        children: introH2s.map(h => ({ label: h.title, href: `text/intro.xhtml#${h.id}` })),
      },
    ];
    for (const g of groups) {
      const chNodes = g.files.map(f => {
        if (f === exercisesFile && exercisesParts.length) {
          return {
            label: navTitleOf(f),
            href: `text/${exercisesParts[0].xname}`,
            children: exercisesParts.map(part => ({
              label: part.navLabel,
              href: `text/${part.xname}`,
              children: part.headings
                .filter(h => h.level === 2)
                .map(h => ({ label: h.title, href: `text/${part.xname}#${h.id}` })),
            })),
          };
        }
        const xname = fileToXhtml.get(f);
        const h2s = (headingsByFile.get(f) || []).filter(h => h.level === 2);
        return {
          label: navTitleOf(f),
          href: `text/${xname}`,
          children: h2s.map(h => ({ label: h.title, href: `text/${xname}#${h.id}` })),
        };
      });
      const firstX = fileToXhtml.get(g.files[0]);
      tocTree.push({ label: g.title, href: `text/${firstX}`, children: chNodes });
    }

    // Write OEBPS/nav.xhtml (nested Part -> Chapter -> H2 TOC + Landmarks, included in <spine>)
    const firstBodyXhtml = orderedReading.sequence.length ? fileToXhtml.get(orderedReading.sequence[0]) : 'intro.xhtml';
    const firstBackXhtml = appendixFiles.length ? fileToXhtml.get(appendixFiles[0]) : firstBodyXhtml;
    const navBody = `  <nav epub:type="toc" id="toc">
    <h1>全书目录</h1>
    <ol>
${renderNavListHtml(tocTree, '      ')}
    </ol>
  </nav>
  <nav epub:type="landmarks" id="landmarks" hidden="hidden">
    <h2>快速定位</h2>
    <ol>
      <li><a epub:type="cover" href="text/cover.xhtml">封面</a></li>
      <li><a epub:type="toc" href="nav.xhtml">目录</a></li>
      <li><a epub:type="bodymatter" href="text/${escXml(firstBodyXhtml)}">正文开始</a></li>
      <li><a epub:type="backmatter" href="text/${escXml(firstBackXhtml)}">附录与工具书</a></li>
    </ol>
  </nav>`;
    await fs.writeFile(path.join(oebpsDir, 'nav.xhtml'), wrapXhtml('目录 · 量子计算手册', navBody, { cssHref: 'styles/epub.css' }), 'utf8');

    // Write EPUB 2 compatible OEBPS/toc.ncx fallback
    const ncxState = { playOrder: 0 };
    const ncxDepth = maxTreeDepth(tocTree);
    const ncxXml = `<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="zh-CN">
  <head>
    <meta name="dtb:uid" content="${BOOK_UUID}"/>
    <meta name="dtb:depth" content="${ncxDepth}"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>${escXml(BOOK_TITLE)}</text></docTitle>
  <navMap>
${renderNcxNavPoints(tocTree, ncxState, '    ')}
  </navMap>
</ncx>
`;
    await fs.writeFile(path.join(oebpsDir, 'toc.ncx'), ncxXml, 'utf8');

    // Write META-INF/container.xml
    const containerXml = `<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
`;
    await fs.writeFile(path.join(metaInfDir, 'container.xml'), containerXml, 'utf8');

    // Write OEBPS/content.opf (EPUB 3 + Accessibility 1.1 schema.org + EPUB 2 NCX + nav in spine)
    const modifiedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
    const manifestLines = [
      `    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>`,
      `    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>`,
      `    <item id="css-main" href="styles/epub.css" media-type="text/css"/>`,
    ];
    for (const d of spineDocs) {
      const props = [];
      if (d.hasMath) props.push('mathml');
      if (d.hasInlineSvg) props.push('svg');
      const propAttr = props.length ? ` properties="${props.join(' ')}"` : '';
      manifestLines.push(`    <item id="${escXml(d.id)}" href="${escXml(d.href)}" media-type="application/xhtml+xml"${propAttr}/>`);
    }
    let assetIdx = 0;
    for (const [name, mediaType] of [...embeddedAssets.entries()].sort((a, b) => a[0].localeCompare(b[0]))) {
      const isCoverImg = name === 'cover.png';
      const aid = isCoverImg ? 'cover-image' : `asset-${++assetIdx}`;
      const propAttr = isCoverImg ? ' properties="cover-image"' : '';
      manifestLines.push(`    <item id="${aid}" href="assets/${escXml(name)}" media-type="${escXml(mediaType)}"${propAttr}/>`);
    }
    const spineLines = [];
    for (const d of spineDocs) {
      spineLines.push(`    <itemref idref="${escXml(d.id)}"/>`);
      if (d.isCover) spineLines.push(`    <itemref idref="nav"/>`);
    }

    const opfXml = `<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" prefix="schema: http://schema.org/" version="3.0" unique-identifier="book-id" xml:lang="zh-CN">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">${BOOK_UUID}</dc:identifier>
    <dc:title>${escXml(BOOK_TITLE)}</dc:title>
    <dc:language>zh-CN</dc:language>
    <dc:creator>${escXml(BOOK_AUTHOR)}</dc:creator>
    <dc:description>系统量子计算与量子力学教材（${orderedReading.groups.length} 篇 ${orderedReading.sequence.length} 章 + ${appendixFiles.length} 附录 + ${labFiles.length} 实验册），采用原生 MathML 3 公式与矢量 SVG 离线出版。</dc:description>
    <dc:date>${escXml(edition)}</dc:date>
    <meta property="dcterms:modified">${modifiedUtc}</meta>
    <meta property="dcterms:conformsTo">EPUB Accessibility 1.1 - WCAG 2.1 Level AA</meta>
    <meta name="cover" content="cover-image"/>
    <meta property="schema:accessMode">textual</meta>
    <meta property="schema:accessMode">visual</meta>
    <meta property="schema:accessModeSufficient">textual,visual</meta>
    <meta property="schema:accessibilityFeature">MathML</meta>
    <meta property="schema:accessibilityFeature">alternativeText</meta>
    <meta property="schema:accessibilityFeature">tableOfContents</meta>
    <meta property="schema:accessibilityFeature">structuralNavigation</meta>
    <meta property="schema:accessibilityHazard">none</meta>
    <meta property="schema:accessibilitySummary">全书采用语义化 XHTML5 与原生 MathML 3 排版全部数学公式，为所有矢量原理图与流程图提供中文替代文本及暗色可读浅暖底板，并提供完整交互目录与 EPUB 2 NCX 兼容导航。</meta>
  </metadata>
  <manifest>
${manifestLines.join('\n')}
  </manifest>
  <spine toc="ncx">
${spineLines.join('\n')}
  </spine>
</package>
`;
    await fs.writeFile(path.join(oebpsDir, 'content.opf'), opfXml, 'utf8');

    // Pack (zip -9) and strictly validate via Python 3 stdlib
    execFileSync('python3', [
      '-c',
      PYTHON_PACK_AND_VERIFY,
      tmpDir,
      finalEpubPath,
      reportPath,
      JSON.stringify({
        output: path.relative(root, finalEpubPath),
        edition,
        diagrams: stats.diagrams,
        formulas: stats.formulas,
      }),
    ], { stdio: 'inherit', cwd: root });
  } finally {
    if (browser) await browser.close();
    if (mermaidServer) await new Promise(resolve => mermaidServer.close(resolve));
    await fs.rm(tmpDir, { recursive: true, force: true }).catch(() => {});
  }
}

main().catch(err => {
  console.error('[build-epub] FAILED:', err);
  process.exitCode = 1;
});
