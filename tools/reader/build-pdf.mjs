#!/usr/bin/env node
/**
 * Build publication-grade A4 PDF for the Quantum Computing Handbook.
 *
 * High-speed chunked rendering pipeline:
 * 1. Dynamically reads handbook/README.md edition & reading-order.mjs part/chapter plan
 *    plus all 7 appendices (A–G) and 7 labs (100% offline, zero external network requests).
 * 2. Resolves Mermaid diagrams from reader/assets/flow-<sha14>.svg (exact build.mjs hash),
 *    falling back to work/render-cache or headless Playwright Mermaid rendering into /tmp.
 * 3. Pre-renders all LaTeX formulas via local KaTeX (output: 'html' — ~65% smaller DOM)
 *    using build.mjs protectMath, and extracts clean Unicode outline titles directly from
 *    Markdown headings (no MathML dependency).
 * 4. Splits the book into lightweight HTML chunks (< ~5 MB each) preserving exact chapter
 *    page breaks, intra-chunk Named Destinations, and cross-chunk link sentinels
 *    (https://qch.local/#<anchor>), then prints cover.pdf + all chunk-*.pdf in parallel
 *    via Chrome with tagged: true, displayHeaderFooter: false, preferCSSPageSize: true.
 * 5. Writes /tmp/qch-pdf-build/outline-manifest.json and invokes postprocess-pdf.py to
 *    merge chunks (retaining catalog /StructTreeRoot from front chunk while honestly auditing
 *    per-page /StructParents coverage), stamp continuous running headers & page numbers,
 *    rewrite TOC + cross-chunk internal GoTo links, write 3-level Unicode bookmarks,
 *    normalize Kangxi /ToUnicode CMaps, losslessly deduplicate & compress (<50 MiB),
 *    run all 10 publishing QA gates, and render 4 150-DPI previews.
 */

import fs from 'node:fs/promises';
import fsSync from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { marked } from 'marked';
import katex from 'katex';
import { readingPlan } from './reading-order.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const source = path.join(root, 'handbook');
const readerDir = path.join(root, 'reader');
const workCache = path.join(root, 'work/render-cache');
const tmpDir = '/tmp/qch-pdf-build';
const tmpAssetsDir = path.join(tmpDir, 'assets');
const distDir = path.join(root, 'dist');
const finalPdfPath = path.join(distDir, 'quantum-computing-handbook.pdf');

const skipPostprocess = process.argv.includes('--skip-postprocess');
const CROSS_LINK_PREFIX = 'https://qch.local/#';
const TARGET_CHUNK_BYTES = 4.8 * 1024 * 1024;
const EXERCISES_CHUNK_BYTES = 4.2 * 1024 * 1024;
const PRINT_CONCURRENCY = Math.max(1, Math.min(6, Number(process.env.PDF_PRINT_CONCURRENCY || 6)));

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.HANDBOOK_NODE_MODULES
  ? path.join(process.env.HANDBOOK_NODE_MODULES, 'playwright')
  : 'playwright');

const CHROME_DEFAULT = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const browserOptions = { headless: true };
if (process.env.HANDBOOK_CHROMIUM) {
  browserOptions.executablePath = process.env.HANDBOOK_CHROMIUM;
} else if (fsSync.existsSync(CHROME_DEFAULT)) {
  browserOptions.executablePath = CHROME_DEFAULT;
}

const safeDecode = s => {
  try { return decodeURIComponent(s); } catch { return s; }
};

const esc = s => String(s)
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

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

const SUP_MAP = {
  '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
  '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
  '+': '⁺', '-': '⁻', 'n': 'ⁿ', 'i': 'ⁱ',
};

const SUB_MAP = {
  '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
  '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
  '+': '₊', '-': '₋',
};

const GREEK_MAP = {
  alpha: 'α', beta: 'β', gamma: 'γ', delta: 'δ', epsilon: 'ε', varepsilon: 'ε',
  zeta: 'ζ', eta: 'η', theta: 'θ', vartheta: 'θ', iota: 'ι', kappa: 'κ',
  lambda: 'λ', mu: 'μ', nu: 'ν', xi: 'ξ', pi: 'π', varpi: 'π',
  rho: 'ρ', varrho: 'ρ', sigma: 'σ', varsigma: 'ς', tau: 'τ', upsilon: 'υ',
  phi: 'φ', varphi: 'φ', chi: 'χ', psi: 'ψ', omega: 'ω',
  Gamma: 'Γ', Delta: 'Δ', Theta: 'Θ', Lambda: 'Λ', Xi: 'Ξ', Pi: 'Π',
  Sigma: 'Σ', Upsilon: 'Υ', Phi: 'Φ', Psi: 'Ψ', Omega: 'Ω',
};

function latexToUnicode(expr) {
  let s = String(expr || '');
  // Strip sizing & spacing macros
  s = s.replace(/\\(?:left|right|bigl|bigr|Bigl|Bigr|biggl|biggr|big|Big|bigg|Bigg|displaystyle|textstyle)\b/g, '');
  s = s.replace(/\\[,;:! ]/g, ' ');
  s = s.replace(/\\quad\b|\\qquad\b/g, ' ');

  // Convert common multi-arg macros
  for (let i = 0; i < 4; i++) {
    const prev = s;
    s = s.replace(/\\(?:text|mathrm|mathbf|mathit|mathsf|mathtt|mathcal|mathbb|operatorname|boldsymbol|bm|hat|tilde|bar|vec|overline|underline)\{([^{}]*)\}/g, '$1');
    s = s.replace(/\\ket\{([^{}]*)\}/g, '|$1⟩');
    s = s.replace(/\\bra\{([^{}]*)\}/g, '⟨$1|');
    s = s.replace(/\\braket\{([^{}]*)\}/g, '⟨$1⟩');
    s = s.replace(/\\(?:d|t)?frac\{([^{}]*)\}\{([^{}]*)\}/g, '$1/$2');
    s = s.replace(/\\sqrt\{([^{}]*)\}/g, '√($1)');
    if (s === prev) break;
  }

  // Replace standard math operators & arrows
  const symbols = [
    [/\\langle\b/g, '⟨'], [/\\rangle\b/g, '⟩'],
    [/\\times\b/g, '×'], [/\\cdot\b/g, '·'], [/\\otimes\b/g, '⊗'], [/\\oplus\b/g, '⊕'],
    [/\\pm\b/g, '±'], [/\\mp\b/g, '∓'], [/\\approx\b/g, '≈'], [/\\neq?\b/g, '≠'],
    [/\\leq?\b/g, '≤'], [/\\geq?\b/g, '≥'], [/\\equiv\b/g, '≡'], [/\\sim\b/g, '∼'],
    [/\\propto\b/g, '∝'], [/\\infty\b/g, '∞'], [/\\hbar\b/g, 'ℏ'], [/\\ell\b/g, 'ℓ'],
    [/\\partial\b/g, '∂'], [/\\nabla\b/g, '∇'], [/\\dagger\b/g, '†'], [/\\star\b/g, '⋆'],
    [/\\to\b|\\rightarrow\b/g, '→'], [/\\leftarrow\b/g, '←'], [/\\leftrightarrow\b/g, '↔'],
    [/\\Rightarrow\b/g, '⇒'], [/\\Leftarrow\b/g, '⇐'], [/\\Leftrightarrow\b/g, '⇔'], [/\\mapsto\b/g, '↦'],
    [/\\in\b/g, '∈'], [/\\notin\b/g, '∉'], [/\\subset\b/g, '⊂'], [/\\subseteq\b/g, '⊆'],
    [/\\cup\b/g, '∪'], [/\\cap\b/g, '∩'], [/\\forall\b/g, '∀'], [/\\exists\b/g, '∃'],
    [/\\ldots\b|\\cdots\b|\\dots\b/g, '…'],
  ];
  for (const [re, rep] of symbols) s = s.replace(re, rep);

  // Greek letters
  s = s.replace(/\\([A-Za-z]+)\b/g, (full, name) => {
    if (name === 'circ') return '°';
    if (GREEK_MAP[name]) return GREEK_MAP[name];
    return name;
  });

  // Superscripts: degrees, stars, digits/n
  s = s.replace(/\^\{?°\}?/g, '°');
  s = s.replace(/\^\{?\*\}?/g, '*');
  s = s.replace(/\^\{([0-9+\-ni]+)\}/g, (_, g) => [...g].map(c => SUP_MAP[c] || c).join(''));
  s = s.replace(/\^([0-9n])/g, (_, c) => SUP_MAP[c] || c);

  // Subscripts: digits -> Unicode subscript; single Greek/letter -> clean inline
  s = s.replace(/_\{([0-9+\-]+)\}/g, (_, g) => [...g].map(c => SUB_MAP[c] || c).join(''));
  s = s.replace(/_([0-9])/g, (_, c) => SUB_MAP[c] || c);
  s = s.replace(/_\{([^{}]+)\}/g, '_$1');

  // Remove residual braces, backslashes, dollar signs
  s = s.replace(/[{}]/g, '');
  s = s.replace(/\\/g, '');
  s = s.replace(/\$/g, '');
  return s.replace(/\s+/g, ' ').trim();
}

function cleanMarkdownHeading(raw) {
  let s = String(raw || '');
  // Unwrap Markdown links [label](href) -> label
  s = s.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
  // Strip inline HTML tags
  s = s.replace(/<[^>]+>/g, '');
  // Convert display/inline LaTeX to clean Unicode
  s = s.replace(/\$\$([\s\S]*?)\$\$/g, (_, m) => latexToUnicode(m));
  s = s.replace(/\\\(([\s\S]*?)\\\)/g, (_, m) => latexToUnicode(m));
  s = s.replace(/(?<!\\)\$(?!\$)((?:\\.|[^$\n])+?)(?<!\\)\$/g, (_, m) => latexToUnicode(m));
  // Strip inline code backticks & emphasis markers
  s = s.replace(/`([^`]+)`/g, '$1');
  s = s.replace(/\*\*([^*]+)\*\*/g, '$1');
  s = s.replace(/__([^_]+)__/g, '$1');
  s = s.replace(/\\([\\`*_{}\[\]()#+\-.!])/g, '$1');
  s = s.replace(/\$/g, '');
  return s.replace(/\s+/g, ' ').trim();
}

const diagramTitles = {
  'README.md': ['主篇的主题分组与推荐衔接'],
  '00-overview.md': ['一次量子计算从输入到验证的五个环节', '相同测量概率的两态经 H 门干涉后的分流对照'],
  '01-math.md': ['从厄米算符出发的测量与酉演化两条路径'],
  '02-single-qubit.md': ['单量子比特测量模型的三层结构：投影测量、POVM 与量子仪器'],
  '05-noise-channels.md': ['CPTP 量子信道的三种等价表示：Stinespring 扩张、Kraus 算符和与 Choi 矩阵'],
  '06-algorithmic-primitives.md': ['量子算法核心原语之间的依赖关系与拼装路径'],
  '07-algorithms.md': ['经典与量子核心复杂度类的包含关系与代表性问题定位'],
  '08-applications.md': ['变分算法中量子测量与经典参数更新的循环'],
  '09-hardware.md': ['量子计算机从程序到控制、读出和反馈的系统链'],
  '11-resources-benchmarks.md': ['从应用目标逐层估算逻辑与物理资源'],
  '12-security-network-frontiers.md': ['机内互连、远距离网络与量子互联网的范围区别', '量子网络从物理链路到应用服务的分层'],
  '13-quantum-information.md': ['以数据处理不等式为总枢纽的量子信息核心不等式关系图'],
  '14-compilation-control.md': ['算法线路到物理执行的九层表示与编译控制流程', '门校准的依赖顺序与漂移回归路径', '实时纠错从模拟读出到流式译码与条件反馈的路径'],
  '15-practice-research.md': ['从纸笔小例到硬件实验的四级验证阶梯与排错回退路径'],
  '16-advanced-algorithms-verification.md': ['隐藏子群算法从查询到经典恢复的共同骨架', '从矩阵编码到奇异值变换的两条构造路径', '大型量子模拟结果的四类交叉证据'],
  '17-computation-models.md': ['六大计算模型之间的理论模拟联系与不能直接等同的边界', '模拟量子模拟器从可算区外推的四类互补核查', '审读计算模型性能声明的七步核查流程'],
  '18-channels-capacities-complexity.md': ['量子态纯化、信道表示、钻石范数与通信容量之间的逻辑脉络', '混态纠缠资源理论中的免费操作、蒸馏稀释与度量层级', '交互式量子证明中验证者与证明者的消息往返与判决流程', '同时消息模型中双方发送量子指纹并由裁判执行交换测试的流程'],
  '19-engineering-architecture.md': ['校准参数依赖有向无环图与快照原子晋级流程'],
  '20-quantum-sensing-metrology.md': ['量子传感协议从信号特征到纠缠极限与退相干策略的选型路径'],
  '21-stabilizer-classical-simulation.md': ['评估量子线路能否突破全部经典模拟引擎的四关判别流程'],
  'quantum-mechanics/01-experiments-states.md': ['延迟选择量子擦除的因果顺序与经典符合分组流程'],
  'quantum-mechanics/02-observables-dynamics.md': ['量子系统时间演化的五条计算路径选择'],
  'quantum-mechanics/03-levels-control.md': ['Ramsey 干涉与 Hahn 自旋回波的脉冲时序及测量目标对照'],
  'quantum-mechanics/04-wavefunctions-models.md': ['连续量子模型在计算机上的两条离散化路径与收敛核验'],
};

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
  'audio.md',
  'sdk-validation.md',
];

const CN_NUM = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'];

function docIdFor(file) {
  const rel = path.relative(source, file).replaceAll('\\', '/');
  if (rel === 'README.md') return 'front-readme';
  if (rel === 'quantum-mechanics/README.md') return 'ch-q1';
  const qmMatch = rel.match(/^quantum-mechanics\/0(\d)-/);
  if (qmMatch) return `ch-q${qmMatch[1]}`;
  const chMatch = rel.match(/^(\d\d)-/);
  if (chMatch) return `ch-${chMatch[1]}`;
  if (rel.startsWith('appendices/')) return 'app-' + path.basename(rel, '.md');
  if (rel === 'labs/README.md') return 'lab-overview';
  if (rel.startsWith('labs/')) return 'lab-' + path.basename(rel, '.md');
  return 'doc-' + slug(rel.replace(/\.md$/, ''));
}

function badgeCodeFor(file) {
  const rel = path.relative(source, file).replaceAll('\\', '/');
  const qmMatch = rel.match(/^quantum-mechanics\/0(\d)-/);
  if (qmMatch) return `Q${qmMatch[1]}`;
  const chMatch = rel.match(/^(\d\d)-/);
  if (chMatch) return chMatch[1];
  if (rel.startsWith('appendices/')) {
    const idx = APPENDIX_ORDER.indexOf(path.basename(rel));
    return idx >= 0 ? `附录 ${String.fromCharCode(65 + idx)}` : '附录';
  }
  if (rel.startsWith('labs/')) {
    const idx = LAB_ORDER.indexOf(path.basename(rel));
    return idx === 0 ? '实验总览' : `实验 ${idx > 0 ? idx : ''}`.trim();
  }
  return '导读';
}

function stripBlocksForHeadingScan(text) {
  const blockPattern = /(^[ \t]*(`{3,}|~{3,})[^\n]*\n[\s\S]*?^[ \t]*\2[ \t]*$)|(`+)[^\n]*?\3|\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]/gm;
  return text.replace(blockPattern, (full, _fence, _delim, ticks) =>
    ticks ? full : '\n\n<div data-handbook-block-stripped></div>\n\n'
  );
}

function protectMath(text, filePath, mathErrors, stats) {
  const fragments = [];
  const pattern = /(^[ \t]*```[^\n]*\n[\s\S]*?^[ \t]*```[^\n]*$)|(`+)[^\n]*?\2|\$\$([\s\S]*?)\$\$|\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)|(?<!\\)\$(?!\$)((?:\\.|[^$\n])+?)(?<!\\)\$/gm;
  const protectedText = text.replace(
    pattern,
    (full, fence, ticks, display1, display2, inline1, inline2, offset, src) => {
      if (fence || ticks) return full;
      const display = display1 !== undefined || display2 !== undefined;
      const latex = display1 ?? display2 ?? inline1 ?? inline2;
      let html;
      try {
        html = katex.renderToString(latex, {
          displayMode: display,
          throwOnError: true,
          strict: 'ignore',
          trust: false,
          output: 'html',
        });
      } catch (e) {
        mathErrors.push({ file: path.relative(root, filePath), latex, error: e.message });
        html = '<code class="math-error">' + esc(latex) + '</code>';
      }
      stats.formulas++;
      const id = fragments.length;
      fragments.push(display ? html : `<span class="math-inline">${html}</span>`);
      if (!display) return `<span data-handbook-math="${id}"></span>`;

      const lineStart = src.lastIndexOf('\n', offset - 1) + 1;
      const linePrefix = src.slice(lineStart, offset);
      const beforeLine = src.slice(0, lineStart);
      const afterMatch = src.slice(offset + full.length);
      const placeholder = `<div data-handbook-math="${id}"></div>`;
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
    }
  );
  return {
    protectedText,
    restore: html => html.replace(/<(div|span) data-handbook-math="(\d+)"><\/\1>/g, (_, _tag, id) => fragments[+id]),
  };
}

function classifyBlockquote(innerHtml) {
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

function enrichSemanticHtml(html, docId, inlineAnchorMap) {
  // Scope explicit inline anchor aliases (<span id="..."></span>) to short ASCII IDs so Skia never truncates PDF Named Destinations
  let out = html.replace(/<span id="([^"]+)"><\/span>/g, (_, origId) => {
    const shortId = inlineAnchorMap?.get(origId) || `${docId}--${origId}`;
    return `<span id="${esc(shortId)}"></span>`;
  });
  // Classify blockquotes into four-color drafting workbench callouts
  out = out.replace(/<blockquote>([\s\S]*?)<\/blockquote>/g, (_, inner) => {
    const cls = classifyBlockquote(inner);
    return `<blockquote class="${cls}">${inner}</blockquote>`;
  });
  // Highlight worked-example headings
  out = out.replace(/<(h[34]) id="([^"]+)">([\s\S]*?)<\/\1>/g, (full, tag, id, inner) => {
    const plain = inner.replace(/<[^>]+>/g, '').trim();
    if (/^(?:\d+(?:\.\d+)*\s*)?(?:算例|手算例|例\s*[0-9A-Za-z一二三四五])|算例[：:]/.test(plain)) {
      return `<${tag} id="${id}" class="worked-heading">${inner}</${tag}>`;
    }
    if (/进阶回看/.test(plain)) {
      return `<${tag} id="${id}">${inner} <span class="advanced-badge">选读</span></${tag}>`;
    }
    return full;
  });
  out = out.replace(/<(h2) id="([^"]+)">([\s\S]*?)<\/h2>/g, (full, _tag, id, inner) => {
    const plain = inner.replace(/<[^>]+>/g, '').trim();
    if (/进阶回看/.test(plain)) {
      return `<h2 id="${id}">${inner} <span class="advanced-badge">选读</span></h2>`;
    }
    return full;
  });
  // Highlight worked-example lead paragraphs
  out = out.replace(/<p><strong>(算例|反例|手算)([^<]*)<\/strong>/g, '<p class="worked-lead"><strong>$1$2</strong>');
  // Wrap standalone tables in table-scroll
  out = out.replace(/<table>/g, '<div class="table-scroll"><table>').replace(/<\/table>/g, '</table></div>');
  return out;
}

function collectElementIds(html) {
  const ids = new Set();
  for (const m of html.matchAll(/\bid="([^"]+)"/g)) {
    ids.add(m[1]);
  }
  return ids;
}

function splitLargeChapterByH2(ch, partKicker, partId, maxBytes) {
  const fullHtml = `
<section class="chapter-section" id="${esc(ch.docId)}" data-chapter-id="${esc(ch.docId)}" data-part-ref="${esc(partId)}">
  <div class="chapter-eyebrow">${esc(partKicker)} · ${esc(ch.code)}</div>
  ${ch.bodyHtml}
</section>`;
  if (Buffer.byteLength(fullHtml) <= maxBytes) {
    return [fullHtml];
  }
  // Split at top-level <h2 id="..."> boundaries (safe for exercises.md where each chapter's solutions begin with <h2>)
  const blocks = ch.bodyHtml.split(/(?=<h2\s+id=")/);
  if (blocks.length <= 1) return [fullHtml];

  const groups = [];
  let cur = [];
  let curBytes = 0;
  for (const blk of blocks) {
    const bLen = Buffer.byteLength(blk);
    if (cur.length > 0 && curBytes + bLen > maxBytes) {
      groups.push(cur.join(''));
      cur = [blk];
      curBytes = bLen;
    } else {
      cur.push(blk);
      curBytes += bLen;
    }
  }
  if (cur.length > 0) groups.push(cur.join(''));

  return groups.map((groupHtml, idx) => {
    if (idx === 0) {
      return `
<section class="chapter-section" id="${esc(ch.docId)}" data-chapter-id="${esc(ch.docId)}" data-part-ref="${esc(partId)}">
  <div class="chapter-eyebrow">${esc(partKicker)} · ${esc(ch.code)}</div>
  ${groupHtml}
</section>`;
    }
    return `
<section class="chapter-section chapter-continuation" data-chapter-id="${esc(ch.docId)}" data-part-ref="${esc(partId)}">
  ${groupHtml}
</section>`;
  });
}

function wrapChunkDocument({ title, katexCssUrl, pdfCssUrl, innerHtml, hiddenAnchorHtml }) {
  // Inject hidden outline/cross-link anchor triggers inside the first section so they never cause a blank page 1
  let bodyContent = innerHtml;
  if (hiddenAnchorHtml) {
    const anchorDiv = `\n  <div class="pdf-outline-anchor-refs" aria-hidden="true">${hiddenAnchorHtml}</div>\n`;
    const firstClose = bodyContent.indexOf('</section>');
    if (firstClose >= 0) {
      bodyContent = bodyContent.slice(0, firstClose) + anchorDiv + bodyContent.slice(firstClose);
    } else {
      bodyContent = bodyContent + anchorDiv;
    }
  }
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>${esc(title)}</title>
  <link rel="stylesheet" href="${esc(katexCssUrl)}">
  <link rel="stylesheet" href="${esc(pdfCssUrl)}">
  <style>
    :root {
      --font-sans: "STHeiti", "Heiti SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
      --font-body: "STHeiti", "Heiti SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
    }
    .pdf-body-root > :first-child { break-before: auto !important; page-break-before: auto !important; }
    .pdf-outline-anchor-refs { top: 0; left: 0; }
  </style>
</head>
<body class="pdf-body-doc">
  <div class="pdf-body-root">
${bodyContent}
  </div>
</body>
</html>`;
}

async function main() {
  const buildStartMs = Date.now();
  await fs.rm(tmpDir, { recursive: true, force: true });
  await fs.mkdir(tmpAssetsDir, { recursive: true });
  await fs.mkdir(distDir, { recursive: true });

  const allMdFiles = (await walk(source)).filter(f => f.endsWith('.md')).sort();
  const contents = new Map(await Promise.all(allMdFiles.map(async f => [f, await fs.readFile(f, 'utf8')])));

  const readmePath = path.join(source, 'README.md');
  const readmeText = contents.get(readmePath) || '';
  const edition = readmeText.match(/^>\s*版本：(\d{4}-\d{2}-\d{2})/m)?.[1];
  if (!edition) {
    throw new Error('handbook/README.md must declare "> 版本：YYYY-MM-DD"');
  }

  const titleOf = f => {
    const m = (contents.get(f) || '').match(/^#\s+(.+)/m);
    return m ? cleanMarkdownHeading(m[1].trim()) : path.basename(f, '.md');
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

  const stripPartPrefix = s => String(s || '').replace(/^第[一二三四五六七八九十\d]+篇\s*[·:：\-—]*\s*/, '').trim();

  const parts = orderedReading.groups.map((group, idx) => {
    const cn = CN_NUM[idx] || String(idx + 1);
    const shortLabel = stripPartPrefix(group.label) || group.label;
    const fullTitle = /^第[一二三四五六七八九十\d]+篇/.test(group.label)
      ? group.label
      : `第${cn}篇 · ${group.label}`;
    return {
      id: `part-${idx + 1}`,
      kicker: `PART ${String(idx + 1).padStart(2, '0')} · 第${cn}篇`,
      title: fullTitle,
      label: shortLabel,
      files: group.files,
      isAppendix: false,
    };
  });

  if (appendixFiles.length) {
    parts.push({
      id: 'part-appendices',
      kicker: 'APPENDICES · 附录工具书',
      title: '附录：先修自测、符号表、术语、题答与开源对照',
      label: '附录工具书',
      files: appendixFiles,
      isAppendix: true,
    });
  }

  if (labFiles.length) {
    parts.push({
      id: 'part-labs',
      kicker: 'OFFLINE LABS · 离线动手实验册',
      title: '动手实验、合成声音与开源 SDK 核验',
      label: '离线动手实验册',
      files: labFiles,
      isAppendix: true,
    });
  }

  const includedFiles = [readmePath, ...parts.flatMap(p => p.files)];
  const fileToDocId = new Map();
  for (const f of includedFiles) fileToDocId.set(f, docIdFor(f));
  const qmReadme = path.join(source, 'quantum-mechanics/README.md');
  if (!fileToDocId.has(qmReadme)) fileToDocId.set(qmReadme, 'ch-q1');
  const styleFile = path.join(source, 'STYLE.md');
  if (!fileToDocId.has(styleFile)) fileToDocId.set(styleFile, 'front-readme');

  // Pre-scan headings & explicit anchor aliases for every included document.
  // Assign short pure-ASCII PDF destination IDs (<= 28 bytes) so Chrome/Skia never
  // percent-encodes and truncates Chinese heading IDs at the PDF 1.7 127-byte Name limit.
  const headingsByFile = new Map();
  const anchorMapByDocId = new Map();
  for (const f of includedFiles) {
    const raw = contents.get(f);
    const docId = fileToDocId.get(f);
    const used = new Map();
    const anchorMap = new Map();
    let hSeq = 0;
    const list = marked.lexer(stripBlocksForHeadingScan(raw))
      .filter(tok => tok.type === 'heading')
      .map(tok => {
        const base = slug(tok.text);
        const cnt = used.get(base) || 0;
        used.set(base, cnt + 1);
        const origId = base + (cnt ? '-' + cnt : '');
        hSeq++;
        const shortId = `${docId}--s${hSeq}`;
        anchorMap.set(origId, shortId);
        return {
          level: tok.depth,
          rawText: tok.text,
          title: cleanMarkdownHeading(tok.text),
          id: origId,
          shortId,
        };
      });
    headingsByFile.set(f, list);
    let aSeq = 0;
    for (const m of raw.matchAll(/<span id="([^"]+)"><\/span>/g)) {
      if (!anchorMap.has(m[1])) {
        aSeq++;
        anchorMap.set(m[1], `${docId}--a${aSeq}`);
      }
    }
    anchorMapByDocId.set(docId, anchorMap);
  }

  // Lazy browser + Mermaid fallback renderer (reused for PDF printing)
  let browser = null;
  let mermaidServer = null;
  let mermaidPage = null;

  async function ensureBrowser() {
    if (!browser) browser = await chromium.launch(browserOptions);
    return browser;
  }

  async function resolveMermaidSvgUrl(code) {
    const flowHash = crypto.createHash('sha256').update(code).digest('hex').slice(0, 14);
    const flowName = `flow-${flowHash}.svg`;
    const readerFlow = path.join(readerDir, 'assets', flowName);
    if (fsSync.existsSync(readerFlow)) {
      return pathToFileURL(readerFlow).href;
    }
    const cacheKey = crypto.createHash('sha256').update('mermaid-11.6-reader-v3\n' + code).digest('hex');
    const cachedFile = path.join(workCache, `${cacheKey}.svg`);
    const tmpFlow = path.join(tmpAssetsDir, flowName);
    if (fsSync.existsSync(cachedFile)) {
      await fs.copyFile(cachedFile, tmpFlow);
      return pathToFileURL(tmpFlow).href;
    }
    if (fsSync.existsSync(tmpFlow)) {
      return pathToFileURL(tmpFlow).href;
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
        if (!resolved.startsWith(here + path.sep)) {
          res.writeHead(403).end();
          return;
        }
        try {
          res.setHeader('Content-Type', /\.m?js$/.test(resolved) ? 'text/javascript' : 'application/octet-stream');
          res.end(await fs.readFile(resolved));
        } catch {
          res.writeHead(404).end();
        }
      });
      await new Promise(resolve => mermaidServer.listen(0, '127.0.0.1', resolve));
      const b = await ensureBrowser();
      mermaidPage = await b.newPage({ viewport: { width: 1400, height: 1000 } });
      await mermaidPage.goto(`http://127.0.0.1:${mermaidServer.address().port}/`);
      await mermaidPage.evaluate(async () => {
        const { default: mermaid } = await import('/node_modules/mermaid/dist/mermaid.esm.min.mjs');
        mermaid.initialize({
          startOnLoad: false,
          securityLevel: 'strict',
          theme: 'base',
          htmlLabels: false,
          fontFamily: 'PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif',
          themeVariables: {
            primaryColor: '#e8f2ef',
            primaryTextColor: '#183934',
            primaryBorderColor: '#72988e',
            lineColor: '#66837b',
            secondaryColor: '#f2eadb',
            tertiaryColor: '#f7f7f2',
            fontSize: '17px',
          },
          flowchart: { htmlLabels: false, curve: 'linear', padding: 18, nodeSpacing: 32, rankSpacing: 42 },
        });
        window.mermaid = mermaid;
      });
    }
    const svg = await mermaidPage.evaluate(
      async ({ id, src }) => (await window.mermaid.render(id, src)).svg,
      { id: `diagram-${flowHash}`, src: code }
    );
    await fs.writeFile(tmpFlow, svg, 'utf8');
    return pathToFileURL(tmpFlow).href;
  }

  const mathErrors = [];
  const stats = { formulas: 0, diagrams: 0, images: 0, docs: 0 };

  async function renderMarkdownDoc(filePath) {
    let text = contents.get(filePath);
    const docId = fileToDocId.get(filePath);
    const relSource = path.relative(source, filePath).replaceAll('\\', '/');
    let diagramCount = 0;

    for (const match of [...text.matchAll(/```mermaid\n([\s\S]*?)```/g)]) {
      diagramCount++;
      stats.diagrams++;
      const diagramTitle = diagramTitles[relSource]?.[diagramCount - 1] || `结构与逻辑流程图 ${diagramCount}`;
      const svgUrl = await resolveMermaidSvgUrl(match[1]);
      const figureHtml = `\n\n<figure class="flowchart"><img src="${esc(svgUrl)}" alt="${esc(diagramTitle)}"><figcaption><span class="fig-badge">图 ${diagramCount}</span>${esc(diagramTitle)}</figcaption></figure>\n\n`;
      text = text.replace(match[0], figureHtml);
    }

    const { protectedText, restore } = protectMath(text, filePath, mathErrors, stats);
    const headings = headingsByFile.get(filePath);
    let hi = 0;

    const renderer = new marked.Renderer();
    renderer.heading = function ({ tokens, depth }) {
      const h = headings[hi++];
      const inner = this.parser.parseInline(tokens);
      if (depth === 1) {
        return `<h1 id="${esc(docId + '--h1')}" data-doc-h1="${esc(docId)}">${inner}</h1>\n`;
      }
      const scopedId = h.shortId;
      const outlineAttr = depth === 2 ? ` data-outline-h2="${esc(docId)}"` : '';
      return `<h${depth} id="${esc(scopedId)}"${outlineAttr}>${inner}</h${depth}>\n`;
    };

    renderer.image = function ({ href, text: altText, title }) {
      stats.images++;
      let imgSrc = href;
      if (!/^(https?:|file:|data:)/i.test(href)) {
        const resolved = path.resolve(path.dirname(filePath), href);
        imgSrc = pathToFileURL(resolved).href;
      }
      const caption = altText || title || '科学原理图';
      return `<figure class="science-figure"><img src="${esc(imgSrc)}" alt="${esc(caption)}"><figcaption><span class="fig-badge">科学图解</span>${esc(caption)}</figcaption></figure>`;
    };

    renderer.link = function ({ href, title, tokens }) {
      const labelHtml = this.parser.parseInline(tokens);
      if (/^(https?:|mailto:)/i.test(href)) {
        return `<a href="${esc(href)}"${title ? ` title="${esc(title)}"` : ''}>${labelHtml}</a>`;
      }
      if (href.startsWith('#')) {
        const rawAnchor = safeDecode(href.slice(1));
        const anchorMap = anchorMapByDocId.get(docId);
        const mapped = anchorMap?.get(rawAnchor);
        const dest = mapped ? `#${mapped}` : `#${docId}`;
        return `<a href="${esc(dest)}">${labelHtml}</a>`;
      }
      const [p, rawFrag] = href.split('#');
      const frag = rawFrag ? safeDecode(rawFrag) : '';
      if (/\.wav$/i.test(p)) {
        return `<span class="audio-print-note">${labelHtml} · 合成音频见离线阅读版</span>`;
      }
      const target = path.resolve(path.dirname(filePath), p);
      if (fileToDocId.has(target)) {
        const targetDocId = fileToDocId.get(target);
        const anchorMap = anchorMapByDocId.get(targetDocId);
        const mapped = frag ? anchorMap?.get(frag) : null;
        const dest = mapped ? `#${mapped}` : `#${targetDocId}`;
        return `<a href="${esc(dest)}">${labelHtml}</a>`;
      }
      return `<span class="code-ref-pill">${labelHtml}</span>`;
    };

    let html = restore(marked.parse(protectedText, { renderer, gfm: true }));
    html = html.replace(/<p>\s*(<figure\b[\s\S]*?<\/figure>)\s*<\/p>/g, '$1');
    html = enrichSemanticHtml(html, docId, anchorMapByDocId.get(docId));
    stats.docs++;
    return html;
  }

  try {
    const katexCssPath = fsSync.existsSync(path.join(readerDir, 'assets/katex/katex.min.css'))
      ? path.join(readerDir, 'assets/katex/katex.min.css')
      : path.join(here, 'node_modules/katex/dist/katex.min.css');
    const katexCssUrl = pathToFileURL(katexCssPath).href;
    const pdfCssUrl = pathToFileURL(path.join(here, 'pdf.css')).href;
    const coverSvgUrl = pathToFileURL(path.join(source, 'assets/cover-banner-static.svg')).href;

    // 1. Render all Markdown documents (KaTeX output: 'html')
    const mdStartMs = Date.now();
    const frontHtml = await renderMarkdownDoc(readmePath);
    const frontTitle = titleOf(readmePath) || '导读与统一约定';

    const renderedParts = [];
    for (const part of parts) {
      const renderedChapters = [];
      for (const f of part.files) {
        const bodyHtml = await renderMarkdownDoc(f);
        renderedChapters.push({
          file: f,
          docId: fileToDocId.get(f),
          code: badgeCodeFor(f),
          rawTitle: titleOf(f),
          bodyHtml,
          h2s: headingsByFile.get(f).filter(h => h.level === 2),
        });
      }
      renderedParts.push({ ...part, chapters: renderedChapters });
    }

    if (mathErrors.length) {
      throw new Error(`KaTeX math rendering failed on ${mathErrors.length} expression(s): ${JSON.stringify(mathErrors.slice(0, 5))}`);
    }
    const mdElapsedMs = Date.now() - mdStartMs;

    const mainPartCount = orderedReading.groups.length;
    const mainChapterCount = orderedReading.sequence.length;

    // 2. Build Cover HTML (standalone cover.pdf, zero header/footer)
    const coverRowsHtml = orderedReading.groups.map((g, idx) => {
      const cn = CN_NUM[idx] || String(idx + 1);
      const shortLabel = stripPartPrefix(g.label) || g.label;
      const chCodes = g.ids.join(' · ');
      return `<tr><td class="cover-part-tag">第${cn}篇</td><td class="cover-part-name">${esc(shortLabel)}</td><td class="cover-part-chapters">${esc(chCodes)}（共 ${g.files.length} 章）</td></tr>`;
    }).join('\n');

    const coverHtml = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>量子计算手册 · 封面</title>
  <link rel="stylesheet" href="${esc(pdfCssUrl)}">
  <style>
    :root {
      --font-sans: "STHeiti", "Heiti SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
      --font-body: "STHeiti", "Heiti SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
    }
  </style>
</head>
<body class="pdf-cover-doc">
  <section class="pdf-cover-page">
    <div>
      <div class="cover-top-rule"><div class="seg-teal"></div><div class="seg-blue"></div><div class="seg-amber"></div></div>
      <div class="cover-header-row">
        <span class="cover-eyebrow">QUANTUM COMPUTING HANDBOOK · A4 出版级精排本</span>
        <span class="cover-edition-pill">版本 ${esc(edition)}</span>
      </div>
      <div class="cover-title-block">
        <h1 class="cover-main-title">量子计算手册</h1>
        <p class="cover-sub-title">从直觉、数学与物理到容错、传感与模拟边界</p>
        <p class="cover-deck">从草稿纸能算透的二维小例出发，贯通线性代数、量子力学基础、干涉算法骨架、噪声信道、表面码容错、量子精密测量与现代经典模拟引擎全链路。</p>
      </div>
      <div class="cover-banner-wrap">
        <img class="cover-banner-img" src="${esc(coverSvgUrl)}" alt="量子计算手册主视觉原理图">
      </div>
      <div class="cover-structure-box">
        <div class="cover-structure-heading">全书体系结构总览 <span>${mainPartCount} 篇 ${mainChapterCount} 章 + ${appendixFiles.length} 附录 + ${labFiles.length} 实验册</span></div>
        <table class="cover-structure-table">
          <tbody>
            ${coverRowsHtml}
            <tr><td class="cover-part-tag">附录与实验</td><td class="cover-part-name">工具书与离线验证</td><td class="cover-part-chapters">先修自测 · 符号与术语表 · 全书逐步题答 · 开源对照 · 离线实验与声音样本</td></tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="cover-footer-stack">
      <div class="cover-contract-strip">
        <strong>全书统一契约：</strong>
        <code>左共轭 ⟨u|v⟩</code> · <code>高位在左大端序 |q₁q₀⟩</code> · <code>算符从右向左作用 VU|ψ⟩</code> · <code>根保真度 F(ρ,σ)</code> · <code>显式底数 log₂ / ln</code>
      </div>
      <div class="cover-colophon">
        <div>量子计算手册编写组 · 零外网本地排版（KaTeX + 矢量 SVG + 3 级 Unicode 书签）<br>全书原稿、离线阅读版与 Python 验算脚本均可本地离线复算</div>
        <div style="text-align:right">出版日期：${esc(edition)}<br>格式：ISO A4 Portrait</div>
      </div>
    </div>
  </section>
</body>
</html>`;

    // 3. Build 3-level clean Unicode outline manifest structure + Chunk plan
    const allOutlineAnchorIds = new Set(['toc-page', 'front-readme']);
    const manifestParts = renderedParts.map(part => {
      allOutlineAnchorIds.add(part.id);
      return {
        id: part.id,
        title: cleanMarkdownHeading(part.title),
        chapters: part.chapters.map(ch => {
          allOutlineAnchorIds.add(ch.docId);
          const sections = ch.h2s.map(h2 => {
            const secId = h2.shortId;
            allOutlineAnchorIds.add(secId);
            return { id: secId, title: h2.title };
          });
          return {
            id: ch.docId,
            title: ch.rawTitle,
            sections,
          };
        }),
      };
    });

    const tocGroupsHtml = renderedParts.map(part => {
      const itemsHtml = part.chapters.map(ch =>
        `<li class="toc-item"><a href="#${esc(ch.docId)}"><span class="toc-code">${esc(ch.code)}</span><span class="toc-name">${esc(ch.rawTitle)}</span></a></li>`
      ).join('\n');
      return `<div class="toc-group"><a class="toc-part-title" href="#${esc(part.id)}">${esc(part.title)}</a><ul class="toc-list">${itemsHtml}</ul></div>`;
    }).join('\n');

    const colophonHtml = `
    <div class="book-colophon">
      <strong>全书完 · 量子计算手册</strong><br>
      版本 ${esc(edition)} · 全书共收录 ${mainChapterCount} 章正文、${appendixFiles.length} 篇附录与 ${labFiles.length} 篇实验册，共预渲染 ${stats.formulas.toLocaleString('en-US')} 个公式与 ${stats.diagrams + stats.images} 幅矢量图表。<br>
      本电子版采用零外网离线流水线构建；配套可运行 Python 教学脚本与第三方开源源码摘录见仓库 <code>codes/</code> 目录。
    </div>`;

    const buildPartDividerHtml = part => {
      const partListHtml = part.chapters.map(ch =>
        `<li><a href="#${esc(ch.docId)}"><span class="part-ch-num">${esc(ch.code)}</span><span>${esc(ch.rawTitle)}</span></a></li>`
      ).join('\n');
      return `
<section class="part-divider" id="${esc(part.id)}" data-part-id="${esc(part.id)}" data-part-title="${esc(part.title)}">
  <div class="part-kicker">${esc(part.kicker)}</div>
  <h1 class="part-title">${esc(part.title)}</h1>
  <div class="part-rule"><span class="r1"></span><span class="r2"></span><span class="r3"></span></div>
  <p class="part-subtitle">本篇共收录 ${part.chapters.length} 节完整内容；每章独立成页，公式与图表均按统一符号契约核验。</p>
  <ul class="part-chapter-list">${partListHtml}</ul>
</section>`;
    };

    const buildChapterSectionHtml = (part, ch) => `
<section class="chapter-section" id="${esc(ch.docId)}" data-chapter-id="${esc(ch.docId)}" data-part-ref="${esc(part.id)}">
  <div class="chapter-eyebrow">${esc(part.kicker)} · ${esc(ch.code)}</div>
  ${ch.bodyHtml}
</section>`;

    // Helper: pack an ordered list of HTML sections into lightweight chunks <= targetBytes
    const rawChunks = [];
    const pushPackedChunks = (baseId, baseTitle, sectionItems, targetBytes = TARGET_CHUNK_BYTES) => {
      const groups = [];
      let cur = [];
      let curBytes = 0;
      for (const secHtml of sectionItems) {
        const bLen = Buffer.byteLength(secHtml);
        if (cur.length > 0 && curBytes + bLen > targetBytes) {
          groups.push(cur.join('\n'));
          cur = [secHtml];
          curBytes = bLen;
        } else {
          cur.push(secHtml);
          curBytes += bLen;
        }
      }
      if (cur.length > 0) groups.push(cur.join('\n'));
      groups.forEach((html, idx) => {
        const suffix = groups.length > 1 ? `-${String.fromCharCode(97 + idx)}` : '';
        rawChunks.push({
          id: `${baseId}${suffix}`,
          title: `${baseTitle}${groups.length > 1 ? ` (${idx + 1}/${groups.length})` : ''}`,
          contentHtml: html,
        });
      });
    };

    // Chunk 00: 2-column TOC + Frontmatter (handbook/README.md)
    rawChunks.push({
      id: 'chunk-00-toc-front',
      title: '量子计算手册 · 目录与导读',
      contentHtml: `
<section class="pdf-toc-page" id="toc-page">
  <div class="toc-header">
    <h1>全书目录</h1>
    <span class="toc-meta">${mainPartCount} 篇 ${mainChapterCount} 章 · ${appendixFiles.length} 附录 · ${labFiles.length} 实验册 · ${esc(edition)} 版</span>
  </div>
  <div class="toc-grid">${tocGroupsHtml}</div>
</section>

<section class="frontmatter-section" id="front-readme" data-frontmatter="front-readme">
  <div class="chapter-eyebrow">FRONT MATTER · 导读、阅读路线与统一约定</div>
  ${frontHtml}
</section>`,
    });

    // Chunks 01..05: Parts 1..5 (auto-subchunked at chapter boundaries to stay <= ~5 MB each)
    for (let pIdx = 0; pIdx < renderedParts.length; pIdx++) {
      const part = renderedParts[pIdx];
      if (!part.isAppendix) {
        const num = String(pIdx + 1).padStart(2, '0');
        const items = [
          buildPartDividerHtml(part),
          ...part.chapters.map(ch => buildChapterSectionHtml(part, ch)),
        ];
        pushPackedChunks(`chunk-${num}-${part.id}`, `量子计算手册 · ${part.title}`, items, TARGET_CHUNK_BYTES);
      } else if (part.id === 'part-appendices') {
        const dividerHtml = buildPartDividerHtml(part);
        const preItems = [dividerHtml];
        const postItems = [];
        let exercisesCh = null;
        for (const ch of part.chapters) {
          if (ch.docId === 'app-exercises') {
            exercisesCh = ch;
          } else if (!exercisesCh) {
            preItems.push(buildChapterSectionHtml(part, ch));
          } else {
            postItems.push(buildChapterSectionHtml(part, ch));
          }
        }
        // Chunk 06: Appendices A-C (prerequisites, notation, glossary)
        pushPackedChunks('chunk-06-appendices-pre', '量子计算手册 · 附录（先修、符号、术语）', preItems, TARGET_CHUNK_BYTES);
        // Chunk 07: Appendix D (exercises.md — split cleanly at H2 boundaries <= 4.2 MB each)
        if (exercisesCh) {
          const exParts = splitLargeChapterByH2(exercisesCh, part.kicker, part.id, EXERCISES_CHUNK_BYTES);
          exParts.forEach((exHtml, idx) => {
            const suffix = exParts.length > 1 ? `-${String.fromCharCode(97 + idx)}` : '';
            rawChunks.push({
              id: `chunk-07-exercises${suffix}`,
              title: `量子计算手册 · 附录 D 题答${exParts.length > 1 ? ` (${idx + 1}/${exParts.length})` : ''}`,
              contentHtml: exHtml,
            });
          });
        }
        // Chunk 08: Appendices E-G (references, software-practice, audit-log)
        if (postItems.length) {
          pushPackedChunks('chunk-08-appendices-post', '量子计算手册 · 附录（参考文献、软件实践、审校记录）', postItems, TARGET_CHUNK_BYTES);
        }
      } else if (part.id === 'part-labs') {
        const labItems = [
          buildPartDividerHtml(part),
          ...part.chapters.map((ch, idx) => {
            const sec = buildChapterSectionHtml(part, ch);
            // Append final colophon right inside the last lab section so it never causes a trailing blank page
            if (idx === part.chapters.length - 1) {
              const closeIdx = sec.lastIndexOf('</section>');
              return closeIdx >= 0 ? sec.slice(0, closeIdx) + colophonHtml + '\n</section>' : sec + colophonHtml;
            }
            return sec;
          }),
        ];
        pushPackedChunks('chunk-09-labs', '量子计算手册 · 离线动手实验册', labItems, TARGET_CHUNK_BYTES);
      }
    }

    // Pass 1: Collect every element ID residing in each chunk
    for (const chunk of rawChunks) {
      chunk.localAnchorIds = collectElementIds(chunk.contentHtml);
    }

    // Pass 2: Rewrite ALL visible internal href="#target" links (TOC, intra-chunk, and cross-chunk)
    // to sentinel URI https://qch.local/#<target> so Chrome emits exact PDF link rectangles that
    // postprocess-pdf.py converts to true internal GoTo links pointing to exact merged (page, y) targets.
    const globalLinkTargets = new Set();
    let internalLinkCount = 0;
    for (const chunk of rawChunks) {
      chunk.contentHtml = chunk.contentHtml.replace(/href="#([^"]+)"/g, (_full, rawTarget) => {
        const target = safeDecode(rawTarget);
        globalLinkTargets.add(target);
        internalLinkCount++;
        return `href="${CROSS_LINK_PREFIX}${encodeURIComponent(target)}"`;
      });
    }

    // Pass 3: Build per-chunk hidden anchor list (all outline targets + all internal link targets in this chunk)
    // and write standalone HTML files to /tmp/qch-pdf-build/
    const chunksMeta = [];
    for (const chunk of rawChunks) {
      const chunkAnchors = [];
      for (const aid of chunk.localAnchorIds) {
        if (allOutlineAnchorIds.has(aid) || globalLinkTargets.has(aid)) {
          chunkAnchors.push(aid);
        }
      }
      const hiddenAnchorHtml = chunkAnchors.map(aid => `<a href="#${esc(aid)}">a</a>`).join('');
      const fullDocHtml = wrapChunkDocument({
        title: chunk.title,
        katexCssUrl,
        pdfCssUrl,
        innerHtml: chunk.contentHtml,
        hiddenAnchorHtml,
      });
      const htmlPath = path.join(tmpDir, `${chunk.id}.html`);
      const pdfPath = path.join(tmpDir, `${chunk.id}.pdf`);
      await fs.writeFile(htmlPath, fullDocHtml, 'utf8');
      chunksMeta.push({
        id: chunk.id,
        title: chunk.title,
        htmlPath,
        pdfPath,
        htmlBytes: Buffer.byteLength(fullDocHtml),
        anchorCount: chunkAnchors.length,
      });
    }

    const coverHtmlPath = path.join(tmpDir, 'cover.html');
    const coverPdfPath = path.join(tmpDir, 'cover.pdf');
    const manifestPath = path.join(tmpDir, 'outline-manifest.json');
    await fs.writeFile(coverHtmlPath, coverHtml, 'utf8');

    // 4. Print cover.pdf + all chunk-*.pdf via Playwright Chrome (parallel worker pool, 0 external requests)
    const printStartMs = Date.now();
    const b = await ensureBrowser();
    const externalRequests = [];
    const pageErrors = [];
    const brokenImagesAll = [];
    let totalScaledEquations = 0;
    let totalCompactedTables = 0;

    async function printCover() {
      const ctx = await b.newContext();
      const page = await ctx.newPage();
      page.setDefaultTimeout(120000);
      await page.route(/^https?:\/\//i, route => {
        externalRequests.push(route.request().url());
        route.abort();
      });
      page.on('pageerror', err => pageErrors.push(`cover: ${err.message}`));
      await page.goto(pathToFileURL(coverHtmlPath).href, { waitUntil: 'load', timeout: 120000 });
      await page.evaluate(async () => {
        await document.fonts.ready;
        await Promise.all([...document.images].map(img => (
          img.complete ? Promise.resolve() : new Promise(r => { img.onload = r; img.onerror = r; })
        )));
        await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      });
      await page.pdf({
        path: coverPdfPath,
        format: 'A4',
        printBackground: true,
        displayHeaderFooter: false,
        preferCSSPageSize: true,
        tagged: true,
      });
      await ctx.close();
    }

    async function printChunk(chunk) {
      const t0 = Date.now();
      const ctx = await b.newContext();
      const page = await ctx.newPage();
      page.setDefaultTimeout(180000);
      await page.route(/^https?:\/\//i, route => {
        externalRequests.push(`${chunk.id}: ${route.request().url()}`);
        route.abort();
      });
      page.on('pageerror', err => pageErrors.push(`${chunk.id}: ${err.message}`));

      await page.goto(pathToFileURL(chunk.htmlPath).href, { waitUntil: 'load', timeout: 180000 });
      const audit = await page.evaluate(async () => {
        await document.fonts.ready;
        await Promise.all([...document.images].map(img => (
          img.complete ? Promise.resolve() : new Promise(r => { img.onload = r; img.onerror = r; })
        )));
        const brokenImages = [...document.images]
          .filter(img => !img.complete || img.naturalWidth === 0)
          .map(img => img.getAttribute('src') || img.alt);

        const rootEl = document.querySelector('.pdf-body-root');
        const maxW = rootEl ? rootEl.clientWidth : 665;
        let scaledEquations = 0;
        let compactedTables = 0;

        for (const box of document.querySelectorAll('.katex-display')) {
          const inner = box.querySelector('.katex');
          if (!inner) continue;
          const avail = Math.max(120, box.clientWidth - 16);
          const needed = inner.scrollWidth;
          if (needed > avail + 2) {
            const ratio = Math.max(0.56, (avail - 2) / needed);
            box.style.fontSize = `${(ratio * 100).toFixed(1)}%`;
            scaledEquations++;
          }
        }

        for (const tbl of document.querySelectorAll('table')) {
          if (tbl.scrollWidth > maxW + 3) {
            tbl.classList.add('table-compact');
            compactedTables++;
            if (tbl.scrollWidth > maxW + 3) {
              tbl.classList.add('table-ultra-compact');
            }
          }
        }

        await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
        return { brokenImages, scaledEquations, compactedTables };
      });

      await page.pdf({
        path: chunk.pdfPath,
        format: 'A4',
        printBackground: true,
        displayHeaderFooter: false,
        preferCSSPageSize: true,
        tagged: true,
        margin: { top: '20mm', right: '17mm', bottom: '20mm', left: '17mm' },
      });
      await ctx.close();

      chunk.elapsedMs = Date.now() - t0;
      chunk.pdfBytes = (await fs.stat(chunk.pdfPath)).size;
      totalScaledEquations += audit.scaledEquations;
      totalCompactedTables += audit.compactedTables;
      for (const bi of audit.brokenImages) brokenImagesAll.push(`${chunk.id}: ${bi}`);
    }

    // Run cover + chunk workers in parallel (bounded concurrency)
    const queue = [...chunksMeta];
    const workers = [printCover()];
    for (let w = 0; w < PRINT_CONCURRENCY; w++) {
      workers.push((async () => {
        while (queue.length > 0) {
          const next = queue.shift();
          if (next) await printChunk(next);
        }
      })());
    }
    await Promise.all(workers);

    if (externalRequests.length > 0) {
      throw new Error(`Zero-external-request policy violated (${externalRequests.length}): ${externalRequests.slice(0, 5).join(', ')}`);
    }
    if (pageErrors.length > 0) {
      throw new Error(`Page JS errors during PDF render: ${pageErrors.join(' | ')}`);
    }
    if (brokenImagesAll.length > 0) {
      throw new Error(`Broken images during PDF render (${brokenImagesAll.length}): ${brokenImagesAll.slice(0, 5).join(', ')}`);
    }

    const printElapsedMs = Date.now() - printStartMs;

    // 5. Write chunked outline-manifest.json
    const manifest = {
      edition,
      generatedAt: new Date().toISOString(),
      mode: 'chunked',
      crossLinkPrefix: CROSS_LINK_PREFIX,
      cover: coverPdfPath,
      stats: {
        ...stats,
        scaledEquations: totalScaledEquations,
        compactedTables: totalCompactedTables,
        internalLinks: internalLinkCount,
        chunkCount: chunksMeta.length,
        markdownRenderMs: mdElapsedMs,
        chromePrintMs: printElapsedMs,
      },
      chunks: chunksMeta.map(c => ({
        id: c.id,
        title: c.title,
        path: c.pdfPath,
        htmlBytes: c.htmlBytes,
        pdfBytes: c.pdfBytes,
        anchorCount: c.anchorCount,
        elapsedMs: c.elapsedMs,
      })),
      frontmatter: { id: 'front-readme', title: frontTitle },
      parts: manifestParts,
    };
    await fs.writeFile(manifestPath, JSON.stringify(manifest, null, 2), 'utf8');

    console.log(JSON.stringify({
      stage: 'chrome-chunks-rendered',
      edition,
      docs: stats.docs,
      formulas: stats.formulas,
      diagrams: stats.diagrams,
      images: stats.images,
      chunkCount: chunksMeta.length,
      concurrency: PRINT_CONCURRENCY,
      markdownRenderSec: +(mdElapsedMs / 1000).toFixed(2),
      chromePrintSec: +(printElapsedMs / 1000).toFixed(2),
      scaledEquations: totalScaledEquations,
      compactedTables: totalCompactedTables,
      internalLinks: internalLinkCount,
      externalRequests: externalRequests.length,
      pageErrors: pageErrors.length,
      chunks: chunksMeta.map(c => ({
        id: c.id,
        htmlMiB: +(c.htmlBytes / 1048576).toFixed(2),
        pdfMiB: +(c.pdfBytes / 1048576).toFixed(2),
        sec: +(c.elapsedMs / 1000).toFixed(2),
      })),
    }, null, 2));

    // Close Chrome before Python postprocess to free RAM immediately
    if (browser) {
      await browser.close();
      browser = null;
    }

    if (!skipPostprocess) {
      const pyStartMs = Date.now();
      const pyScript = path.join(here, 'postprocess-pdf.py');
      execFileSync('python3', [
        pyScript,
        '--cover', coverPdfPath,
        '--chunks-manifest', manifestPath,
        '--output', finalPdfPath,
      ], { stdio: 'inherit', cwd: root });
      const pyElapsedMs = Date.now() - pyStartMs;
      const totalElapsedMs = Date.now() - buildStartMs;
      console.log(JSON.stringify({
        stage: 'pdf-build-complete',
        postprocessSec: +(pyElapsedMs / 1000).toFixed(2),
        totalBuildSec: +(totalElapsedMs / 1000).toFixed(2),
      }, null, 2));
    }
  } finally {
    if (browser) await browser.close();
    if (mermaidServer) await new Promise(resolve => mermaidServer.close(resolve));
  }
}

main().catch(err => {
  console.error('[build-pdf] FAILED:', err);
  process.exitCode = 1;
});
