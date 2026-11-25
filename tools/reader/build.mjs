import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import katex from 'katex';
import { readingPlan } from './reading-order.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const source = path.join(root, 'handbook');
const output = path.join(root, 'reader');
const cache = path.join(root, 'work/render-cache');
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.HANDBOOK_NODE_MODULES
  ? path.join(process.env.HANDBOOK_NODE_MODULES, 'playwright')
  : 'playwright');
const browserOptions = { headless: true };
if (process.env.HANDBOOK_CHROMIUM) browserOptions.executablePath = process.env.HANDBOOK_CHROMIUM;

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const slug = s => s.toLowerCase().replace(/[\p{P}\p{S}]/gu, c => (c === '-' || c === '_' ? c : '')).trim().replace(/\s/g, '-');
const walk = async dir => (await Promise.all((await fs.readdir(dir, { withFileTypes: true })).map(e => (e.isDirectory() ? walk(path.join(dir, e.name)) : path.join(dir, e.name))))).flat();
const digest = value => crypto.createHash('sha256').update(value).digest('hex');

await fs.mkdir(output, { recursive: true });
await fs.mkdir(cache, { recursive: true });

const files = (await walk(source)).filter(f => f.endsWith('.md')).sort();
const contents = new Map(await Promise.all(files.map(async f => [f, await fs.readFile(f, 'utf8')])));
const edition = contents.get(path.join(source, 'README.md')).match(/^>\s*版本：(\d{4}-\d{2}-\d{2})/m)?.[1];
if (!edition || Number.isNaN(Date.parse(edition + 'T00:00:00Z')) || new Date(edition + 'T00:00:00Z').toISOString().slice(0, 10) !== edition) {
  throw new Error('handbook/README.md must declare a valid YYYY-MM-DD edition');
}
const titleOf = f => contents.get(f).match(/^# (.+)/m)[1];
const outputName = f => path.relative(source, f).replace(/README\.md$/, 'index.html').replace(/\.md$/, '.html');
const chapters = files.filter(f => /^\d\d-/.test(path.basename(f)));
const orderedReading = readingPlan(chapters);
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

// Keep diagram titles specific to the relationship shown, rather than generating
// "flowchart 1" captions that tell readers nothing about the figure.
const diagramTitles = {
  'README.md': ['主篇 00—21 与物理篇 Q1—Q4 共 26 章的五篇学习路线'],
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
  '14-compilation-control.md': ['算法线路到物理执行的九层表示与编译控制流程', '门校准的依赖顺序与漂移回归路径', '实时纠错从模拟读出到流式解码与条件反馈的路径'],
  '15-practice-research.md': ['从纸笔小例到硬件实验的四级验证阶梯与排错回退路径'],
  '16-advanced-algorithms-verification.md': ['隐藏子群算法从查询到经典恢复的共同骨架', '从矩阵编码到奇异值变换的两条构造路径', '大型量子模拟结果的四类交叉证据'],
  '17-computation-models.md': ['七大计算模型之间的理论模拟联系与不能直接等同的边界', '模拟量子模拟器从可算区外推的四类互补核查', '审读计算模型性能声明的七步核查流程'],
  '18-channels-capacities-complexity.md': ['量子态纯化、信道表示、钻石范数与通信容量之间的逻辑脉络', '混态纠缠资源理论中的免费操作、蒸馏稀释与度量层级', '交互式量子证明中验证者与证明者的消息往返与判决流程', '同时消息模型中双方发送量子指纹并由裁判执行交换测试的流程'],
  '19-engineering-architecture.md': ['校准参数依赖有向无环图与快照原子晋级流程'],
  '20-quantum-sensing-metrology.md': ['量子传感从物理信号编码、噪声滤波到参数估计极限的决策路径'],
  '21-stabilizer-classical-simulation.md': ['按比特数、非 Clifford 门、纠缠拓扑与噪声率四关判定经典模拟引擎边界的决策树'],
  'quantum-mechanics/01-experiments-states.md': ['延迟选择量子擦除的因果顺序与经典符合分组流程'],
  'quantum-mechanics/02-observables-dynamics.md': ['量子系统时间演化的五条计算路径选择'],
  'quantum-mechanics/03-levels-control.md': ['Ramsey 干涉与 Hahn 自旋回波的脉冲时序及测量目标对照'],
  'quantum-mechanics/04-wavefunctions-models.md': ['连续量子模型在计算机上的两条离散化路径与收敛核验'],
};

const report = { generatedAt: new Date().toISOString(), pages: [], mathErrors: [], diagramErrors: [], diagrams: 0, formulas: 0 };
const reportCopies = new Map();
const usedFlowSvgs = new Set();

let browser, server, page;
async function diagram(code) {
  const key = crypto.createHash('sha256').update('mermaid-11.6-reader-v3\n' + code).digest('hex');
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
      mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'base', htmlLabels: false, fontFamily: 'PingFang SC, Microsoft YaHei, sans-serif', themeVariables: { primaryColor: '#e8f2ef', primaryTextColor: '#183934', primaryBorderColor: '#72988e', lineColor: '#66837b', secondaryColor: '#f2eadb', tertiaryColor: '#f7f7f2', fontSize: '17px' }, flowchart: { htmlLabels: false, curve: 'linear', padding: 18, nodeSpacing: 32, rankSpacing: 42 } });
      window.mermaid = mermaid;
    });
  }
  const id = 'diagram-' + key.slice(0, 14);
  const svg = await page.evaluate(async ({ id, code }) => (await window.mermaid.render(id, code)).svg, { id, code });
  await fs.writeFile(file, svg);
  return svg;
}

// Protect math before Markdown tokenization, including bars inside table cells.
// When `trackInReport` is false (e.g. collapsible chapter solutions), KaTeX renders
// identically without mutating `report.formulas` or `mathSourceDigest`.
function protectMath(text, f, { trackInReport = true } = {}) {
  const fragments = [];
  const meta = [];
  const latexSources = [];
  const pattern = /(^[ \t]*```[^\n]*\n[\s\S]*?^[ \t]*```[^\n]*$)|(`+)[^\n]*?\2|\$\$([\s\S]*?)\$\$|\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)|(?<!\\)\$(?!\$)((?:\\.|[^$\n])+?)(?<!\\)\$/gm;
  const protectedText = text.replace(pattern, (full, fence, ticks, display1, display2, inline1, inline2, offset, src) => {
    if (fence || ticks) return full;
    const display = display1 !== undefined || display2 !== undefined;
    const latex = display1 ?? display2 ?? inline1 ?? inline2;
    latexSources.push(latex);
    let html;
    try {
      html = katex.renderToString(latex, { displayMode: display, throwOnError: true, strict: 'ignore', trust: false, output: 'htmlAndMathml' });
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

function enhanceBodySemantics(html) {
  let out = html.replace(/<p>\s*(<figure class="scientific-figure">[\s\S]*?<\/figure>)\s*<\/p>/g, '$1');
  out = classifyBlockquotes(out);
  out = enhanceTables(out);
  return out;
}

function createLinkRewriter(sourceFile, targetOutputFile) {
  return function rewriteHref(href) {
    if (/^(https?:|mailto:|#)/.test(href)) return href;
    const [p, anchor] = href.split('#');
    const target = path.resolve(path.dirname(sourceFile), p);
    if (contents.has(target)) {
      return path.relative(path.dirname(targetOutputFile), path.join(output, outputName(target))) + (anchor ? '#' + anchor : '');
    }
    if (target.startsWith(path.join(root, 'codes') + path.sep)) {
      const local = path.join(output, 'codes', path.relative(path.join(root, 'codes'), target));
      return path.relative(path.dirname(targetOutputFile), local) + (anchor ? '#' + anchor : '');
    }
    if (target.startsWith(path.join(root, 'work/research') + path.sep)) {
      const local = path.join(output, 'research', path.basename(target));
      reportCopies.set(target, local);
      return path.relative(path.dirname(targetOutputFile), local) + (anchor ? '#' + anchor : '');
    }
    if (target.startsWith(output + path.sep)) {
      return path.relative(path.dirname(targetOutputFile), target) + (anchor ? '#' + anchor : '');
    }
    return href;
  };
}

function parseExercisesByChapter(exercisesRaw) {
  const map = new Map();
  if (!exercisesRaw) return map;
  const sections = exercisesRaw.split(/^(?=##\s)/m);
  for (const sec of sections) {
    const nl = sec.indexOf('\n');
    const heading = (nl === -1 ? sec : sec.slice(0, nl)).trim();
    const body = nl === -1 ? '' : sec.slice(nl + 1);
    let key = null;
    const mMain = heading.match(/^##\s*第\s*(\d+)\s*章(?:\s*[｜|].*)?$/);
    const mQm = heading.match(/^##\s*(?:量子力学|物理篇)\s*Q(\d+)(?:\s*[｜|].*)?$/);
    if (mMain) key = String(Number(mMain[1])).padStart(2, '0');
    else if (mQm) key = `Q${Number(mQm[1])}`;
    if (key) map.set(key, body);
  }
  return map;
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
    const resolved = rewriteHref(href);
    const linkHtml = this.parser.parseInline(inlineTokens);
    const plainLabel = linkHtml.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim() || path.basename(resolved);
    const link = `<a href="${esc(resolved)}"${title ? ` title="${esc(title)}"` : ''}>${linkHtml}</a>`;
    return /\.wav$/i.test(resolved)
      ? `${link}<audio controls preload="none" src="${esc(resolved)}" aria-label="教学合成音频：${esc(plainLabel)}"></audio>`
      : link;
  };

  const renderedItems = [];
  let qIndex = 0;
  for (const token of tokens) {
    if (token.type !== 'list' || !token.ordered) continue;
    for (const item of token.items) {
      qIndex++;
      const itemHtml = enhanceTables(restore(marked.parser(item.tokens, { renderer: solRenderer, gfm: true })));
      renderedItems.push(
        `<details class="solution-item">` +
          `<summary><span class="sol-num">第 ${qIndex} 题参考解答</span><span class="sol-hint">展开零跳步推导</span></summary>` +
          `<div class="solution-body">${itemHtml}</div>` +
        `</details>`,
      );
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

function buildLandingShell() {
  return (
    `<section class="landing-shell" aria-label="课程展厅导览与快速入口">` +
      `<div class="landing-hero">` +
        `<div class="landing-intro">` +
          `<span class="landing-kicker">OPEN MONOGRAPH · 100% 离线自包含</span>` +
          `<div class="landing-title">量子计算手册</div>` +
          `<p class="landing-subtitle">从零基础直觉、完整公式推导到容错系统、精密测量与经典模拟边界</p>` +
          `<div class="landing-metrics">` +
            `<div class="metric-tile"><span class="metric-num">26</span><span class="metric-label">完整篇章（00–21 + Q1–Q4）</span></div>` +
            `<div class="metric-tile"><span class="metric-num">46,000+</span><span class="metric-label">本地预渲染公式</span></div>` +
            `<div class="metric-tile"><span class="metric-num">80+</span><span class="metric-label">矢量科学图与流程图</span></div>` +
            `<div class="metric-tile"><span class="metric-num">271</span><span class="metric-label">零跳步自检题答</span></div>` +
          `</div>` +
          `<div class="landing-ctas">` +
            `<a class="cta-primary" href="00-overview.html">从第 00 章开始阅读 →</a>` +
            `<a class="cta-accent" href="lab/quantum-lab.html">⚡ 打开离线交互实验台</a>` +
            `<a class="cta-ghost" href="labs/audio.html">🔊 听觉实验与声波对比</a>` +
            `<a class="cta-ghost" href="appendices/exercises.html">📝 271 题零跳步题答</a>` +
          `</div>` +
        `</div>` +
        `<div class="hero-interference-card" id="qch-hero-sim">` +
          `<div class="hero-card-head">` +
            `<span class="hero-card-title">单比特量子干涉实时预览</span>` +
            `<span class="hero-card-formula">H · P(φ) · H |0⟩</span>` +
          `</div>` +
          `<div class="phase-switcher" role="group" aria-label="切换相对相位">` +
            `<button type="button" class="phase-btn is-active" data-phase="0" aria-pressed="true"><strong>φ = 0</strong><span>相长 · D0 100%</span></button>` +
            `<button type="button" class="phase-btn" data-phase="90" aria-pressed="false"><strong>φ = π/2</strong><span>均衡 · 50%/50%</span></button>` +
            `<button type="button" class="phase-btn" data-phase="180" aria-pressed="false"><strong>φ = π</strong><span>相消 · D1 100%</span></button>` +
          `</div>` +
          `<div class="hero-svg-wrap">` +
            `<svg viewBox="0 0 420 184" role="img" aria-label="单量子比特干涉线路 H-P(φ)-H 及探测器 D0 与 D1 概率分布图">` +
              `<text x="16" y="96" font-size="13" font-weight="700" fill="var(--heading)">|0⟩</text>` +
              `<line x1="42" y1="92" x2="72" y2="92" stroke="var(--svg-wire)" stroke-width="2"/>` +
              `<rect x="72" y="72" width="38" height="40" rx="6" fill="var(--svg-box-fill)" stroke="var(--svg-box-stroke)" stroke-width="2"/>` +
              `<text x="91" y="97" text-anchor="middle" font-size="14" font-weight="700" fill="var(--heading)">H</text>` +
              `<path d="M 110 82 L 138 52 L 242 52 L 266 82" fill="none" stroke="var(--svg-wire)" stroke-width="2"/>` +
              `<path d="M 110 102 L 138 132 L 182 132 M 238 132 L 242 132 L 266 102" fill="none" stroke="var(--amber)" stroke-width="2.2"/>` +
              `<text x="190" y="42" text-anchor="middle" font-size="11" fill="var(--muted)">上支路 |0⟩ · 相位 0</text>` +
              `<circle cx="210" cy="132" r="24" fill="var(--svg-box-fill)" stroke="var(--amber)" stroke-width="2"/>` +
              `<circle cx="210" cy="132" r="12" fill="none" stroke="var(--line)" stroke-width="1.5" stroke-dasharray="3 2"/>` +
              `<path id="qch-svg-phase-arc" d="M 210 132 L 222 132" fill="none" stroke="var(--amber)" stroke-width="2.8" stroke-linecap="round"/>` +
              `<text id="qch-svg-phase-text" x="210" y="170" text-anchor="middle" font-size="12" font-weight="700" fill="var(--amber)">φ = 0</text>` +
              `<rect x="266" y="72" width="38" height="40" rx="6" fill="var(--svg-box-fill)" stroke="var(--svg-box-stroke)" stroke-width="2"/>` +
              `<text x="285" y="97" text-anchor="middle" font-size="14" font-weight="700" fill="var(--heading)">H</text>` +
              `<line x1="304" y1="80" x2="326" y2="62" stroke="var(--svg-bar-d0)" stroke-width="2"/>` +
              `<line x1="304" y1="104" x2="326" y2="122" stroke="var(--svg-bar-d1)" stroke-width="2"/>` +
              `<text x="330" y="50" font-size="11.5" font-weight="700" fill="var(--heading)">D0 (|0⟩)</text>` +
              `<rect x="330" y="56" width="72" height="14" rx="4" fill="var(--svg-bar-track)"/>` +
              `<rect id="qch-svg-bar0" x="330" y="56" width="72" height="14" rx="4" fill="var(--svg-bar-d0)"/>` +
              `<text id="qch-svg-val0" x="402" y="84" text-anchor="end" font-size="11.5" font-weight="700" fill="var(--svg-bar-d0)">100%</text>` +
              `<text x="330" y="110" font-size="11.5" font-weight="700" fill="var(--heading)">D1 (|1⟩)</text>` +
              `<rect x="330" y="116" width="72" height="14" rx="4" fill="var(--svg-bar-track)"/>` +
              `<rect id="qch-svg-bar1" x="330" y="116" width="2" height="14" rx="4" fill="var(--svg-bar-d1)"/>` +
              `<text id="qch-svg-val1" x="402" y="144" text-anchor="end" font-size="11.5" font-weight="700" fill="var(--svg-bar-d1)">0%</text>` +
            `</svg>` +
          `</div>` +
          `<div class="hero-readout">` +
            `<div class="hero-readout-probs">P(D0) = cos²(φ/2) = <strong id="qch-hero-p0">100%</strong> · P(D1) = sin²(φ/2) = <strong id="qch-hero-p1">0%</strong></div>` +
            `<span id="qch-hero-note">两支路同相相加（1 + 1），全部概率汇入 D0，D1 严格相消归零。</span>` +
          `</div>` +
          `<a class="hero-lab-jump" href="lab/quantum-lab.html">进入连续调相、Bloch 球与 Ramsey 退相干完整实验台 →</a>` +
        `</div>` +
      `</div>` +
      `<div class="path-grid">` +
        `<div class="path-card"><span class="path-badge">路径 01 · 零基础全景入门</span><div class="path-card-title">数学先修 → 量子态、测量与基础线路</div><p>先用 10 分钟自测查漏补缺，再沿 00 → 01 → Q1 → 02 → Q2 → 03–05 拿草稿纸算透叠加、干涉、纠缠与噪声信道。</p><div class="path-links"><a href="00-overview.html">第 00 章全景 →</a><a href="appendices/prerequisites.html">七道先修自测 →</a></div></div>` +
        `<div class="path-card"><span class="path-badge">路径 02 · 算法与软件工程</span><div class="path-card-title">核心原语 → 变分应用与可复算实验</div><p>掌握 QFT、QPE、振幅放大与 HHL 骨架，落地 VQE/QAOA 采样统计，并用纯标准库手写模拟器验证论文结论。</p><div class="path-links"><a href="06-algorithmic-primitives.html">第 06 章算法原语 →</a><a href="15-practice-research.html">第 15 章动手实践 →</a></div></div>` +
        `<div class="path-card"><span class="path-badge">路径 03 · 物理硬件与容错系统</span><div class="path-card-title">能级控制 → 编译、表面码纠错与工程运维</div><p>打通超导/离子阱/中性原子物理载体、九层编译控制、表面码解码与资源账本，读懂容错系统工程全景。</p><div class="path-links"><a href="quantum-mechanics/03-levels-control.html">物理篇 Q3 控制 →</a><a href="09-hardware.html">第 09 章物理硬件 →</a></div></div>` +
        `<div class="path-card"><span class="path-badge">路径 04 · 科研前沿与模拟边界</span><div class="path-card-title">精密测量 → QSVT、经典模拟边界与七大模型</div><p>深入量子传感与 Fisher 信息极限、QSVT 统一框架、稳定子/张量网络经典模拟四关判据及七大计算模型对比。</p><div class="path-links"><a href="20-quantum-sensing-metrology.html">第 20 章量子传感 →</a><a href="21-stabilizer-classical-simulation.html">第 21 章模拟边界 →</a></div></div>` +
      `</div>` +
      `<div class="verify-strip">` +
        `<div class="verify-strip-title">可验证科研闭环 · 零黑盒离线交付</div>` +
        `<div class="verify-steps">` +
          `<span class="verify-step">零跳步推导</span><span class="verify-arrow">→</span>` +
          `<span class="verify-step">36 个离线脚本验算</span><span class="verify-arrow">→</span>` +
          `<span class="verify-step">浏览器双宽门禁</span><span class="verify-arrow">→</span>` +
          `<span class="verify-step">交互实验台直观验证</span>` +
        `</div>` +
        `<p class="verify-dist-note">支持本地离线构建合订本 A4 PDF（<code>dist/quantum-computing-handbook.pdf</code>）与原生 MathML 电子书（<code>dist/quantum-computing-handbook.epub</code>）：在仓库根目录运行 <code>node tools/reader/build-pdf.mjs</code> 与 <code>node tools/reader/build-epub.mjs</code> 即可同源生成。</p>` +
      `</div>` +
    `</section>`
  );
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

const exercisesFile = path.join(source, 'appendices/exercises.md');
const exercisesMap = parseExercisesByChapter(contents.get(exercisesFile));

try {
  for (const [f, raw] of contents) {
    let text = raw;
    let diagramCount = 0;
    const relSource = path.relative(source, f).replaceAll('\\', '/');
    const outRel = outputName(f);
    const target = path.join(output, outRel);
    const prefix = path.dirname(outRel) === '.' ? '' : '../';

    for (const match of [...text.matchAll(/```mermaid\n([\s\S]*?)```/g)]) {
      diagramCount++;
      report.diagrams++;
      try {
        const diagramTitle = diagramTitles[relSource]?.[diagramCount - 1];
        if (!diagramTitle) throw new Error('missing descriptive diagram title');
        const flowFile = 'flow-' + crypto.createHash('sha256').update(match[1]).digest('hex').slice(0, 14) + '.svg';
        usedFlowSvgs.add(flowFile);
        const svg = await diagram(match[1]);
        const rel = 'assets/' + flowFile;
        await fs.mkdir(path.join(output, 'assets'), { recursive: true });
        await fs.writeFile(path.join(output, rel), svg);
        const intrinsicWidth = Number(svg.match(/viewBox="[^" ]+ [^" ]+ ([^" ]+)/)?.[1]) || 650;
        text = text.replace(
          match[0],
          `<figure class="flowchart"><img src="${prefix + rel}" style="width:${intrinsicWidth}px" alt="${esc(diagramTitle)}" loading="lazy"><figcaption>图 ${diagramCount}｜${esc(diagramTitle)} · 横向较长时可在图内滚动 · <a href="${prefix + rel}">打开完整图</a></figcaption></figure>`,
        );
      } catch (e) {
        report.diagramErrors.push({ file: path.relative(root, f), diagram: diagramCount, error: e.message });
      }
    }

    const configuredTitles = diagramTitles[relSource]?.length || 0;
    if (configuredTitles > diagramCount) {
      report.diagramErrors.push({
        file: path.relative(root, f),
        diagram: diagramCount,
        error: `unused descriptive diagram title(s): configured ${configuredTitles}, rendered ${diagramCount}`,
      });
    }

    const formulasBefore = report.formulas;
    const { protectedText, mathSourceDigest, restore } = protectMath(text, f, { trackInReport: true });
    const headings = headingsByFile.get(f);
    let hi = 0;
    const rewriteHref = createLinkRewriter(f, target);
    const renderer = new marked.Renderer();

    renderer.image = function ({ href, text: altText, title }) {
      const safeHref = esc(href);
      const safeAlt = esc(altText || '');
      const titleAttr = title ? ` title="${esc(title)}"` : '';
      if (/\.svg(?:$|[?#])/i.test(href)) {
        return (
          `<figure class="scientific-figure">` +
            `<a class="image-open scientific-svg" href="${safeHref}" aria-label="打开原尺寸图：${safeAlt}">` +
              `<img src="${safeHref}" alt="${safeAlt}"${titleAttr} loading="lazy">` +
              `<span>放大查看 ↗</span>` +
            `</a>` +
            (safeAlt ? `<figcaption class="scientific-caption">${safeAlt}</figcaption>` : '') +
          `</figure>`
        );
      }
      return (
        `<a class="image-open" href="${safeHref}" aria-label="打开原尺寸图：${safeAlt}">` +
          `<img src="${safeHref}" alt="${safeAlt}"${titleAttr} loading="lazy">` +
          `<span>放大查看 ↗</span>` +
        `</a>`
      );
    };

    renderer.heading = function ({ tokens, depth }) {
      const h = headings[hi++];
      const cls = classifyHeadingClass(depth, h.title);
      return `<h${depth} id="${esc(h.id)}"${cls}>${this.parser.parseInline(tokens)}</h${depth}>\n`;
    };

    renderer.link = function ({ href, title, tokens }) {
      const resolved = rewriteHref(href);
      const linkHtml = this.parser.parseInline(tokens);
      const plainLabel = linkHtml.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim() || path.basename(resolved);
      const link = `<a href="${esc(resolved)}"${title ? ` title="${esc(title)}"` : ''}>${linkHtml}</a>`;
      return /\.wav$/i.test(resolved)
        ? `${link}<audio controls preload="none" src="${esc(resolved)}" aria-label="教学合成音频：${esc(plainLabel)}"></audio>`
        : link;
    };

    const body = enhanceBodySemantics(restore(marked.parse(protectedText, { renderer, gfm: true })));
    const chapterLinks = list => list.map(c => `<a ${c === f ? 'aria-current="page" ' : ''}href="${prefix + outputName(c)}">${esc(titleOf(c))}</a>`).join('');
    const qmGuideCurrent = outRel === 'quantum-mechanics/index.html' ? 'aria-current="page" ' : '';
    const nav =
      orderedReading.groups
        .map(
          group =>
            `<div class="nav-label">${esc(group.label)}</div>` +
            `${group.ids.includes('Q1') ? `<a ${qmGuideCurrent}href="${prefix}quantum-mechanics/index.html">物理篇导读与先修说明</a>` : ''}` +
            `${chapterLinks(group.files)}`,
        )
        .join('') +
      `<div class="nav-label">实验、代码与音频</div>` +
      `<a class="nav-lab-featured" href="${prefix}lab/quantum-lab.html">⚡ 交互式量子实验台（离线）</a>` +
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
    const prev = index > 0 ? `<a href="${prefix + outputName(sequence[index - 1])}">← ${esc(titleOf(sequence[index - 1]))}</a>` : '';
    const next = index >= 0 && index < sequence.length - 1 ? `<a href="${prefix + outputName(sequence[index + 1])}">${esc(titleOf(sequence[index + 1]))} →</a>` : '';

    const landingHtml = outRel === 'index.html' ? buildLandingShell() : '';
    const solutionsHtml = buildChapterSolutionsHtml(chapterIdOf(f), target, prefix, exercisesFile, exercisesMap);
    const themeInitScript = `<script>(function(){try{var t=localStorage.getItem('qch-theme')||localStorage.getItem('qch-lab-theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}catch(e){}})();</script>`;

    const html =
      `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">` +
      `<title>${esc(titleOf(f))} · 量子计算手册</title>${themeInitScript}` +
      `<link rel="stylesheet" href="${prefix}assets/katex/katex.min.css">` +
      `<link rel="stylesheet" href="${prefix}assets/reader.css"></head><body>` +
      `<div class="read-progress" id="qch-read-progress" aria-hidden="true"></div>` +
      `<a class="skip" href="#content">跳到正文</a>` +
      `<header>` +
        `<a class="brand" href="${prefix}index.html"><span class="mark">ψ</span>量子计算手册</a>` +
        `<span class="edition">V3 · 离线阅读版</span>` +
        `<div class="header-actions">` +
          `<button type="button" id="theme-toggle" aria-pressed="false" aria-label="切换为暗色模式" title="切换为暗色模式"><span class="theme-icon" aria-hidden="true">☾</span><span class="theme-label">暗色</span></button>` +
          `<a class="header-btn header-lab-link" href="${prefix}lab/quantum-lab.html">⚡ 实验台</a>` +
          `<button type="button" class="header-print-btn" onclick="window.print()">打印<span class="header-print-label-long">本章</span></button>` +
        `</div>` +
      `</header>` +
      `<div class="layout">` +
        `<aside class="chapters"><details open><summary>全书目录</summary><input type="search" id="nav-search" aria-label="查找章节" placeholder="查找章节…（按 / 聚焦）"><nav>${nav}<div class="nav-label">附录</div>${appNav}</nav></details></aside>` +
        `<main id="content"><div class="eyebrow">QUANTUM COMPUTING · V3 离线学习手册</div>${landingHtml}${mobileToc}<article>${body}</article>${solutionsHtml}<div class="page-turn">${prev}${next}</div><footer>${edition} 版 · 公式、图表、字体与交互实验台均保存在本地<br>配套 Markdown 为可编辑原稿；事实更新与审校范围见审校记录。</footer></main>` +
        `<aside class="contents"><strong>本页内容</strong><nav>${toc}</nav><a class="top" href="#content">↑ 返回顶部</a></aside>` +
      `</div>` +
      `<script src="${prefix}assets/reader.js" defer></script>` +
      `</body></html>`;

    await fs.mkdir(path.dirname(target), { recursive: true });
    await fs.writeFile(target, html);
    report.pages.push({
      source: path.relative(root, f),
      output: path.relative(root, target),
      sourceSha256: digest(raw),
      outputSha256: digest(html),
      mathSourceDigest,
      headingIds: headings.map(h => h.id),
      diagrams: diagramCount,
      headings: hi,
      formulas: report.formulas - formulasBefore,
    });
  }

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

  await fs.cp(path.join(source, 'assets'), path.join(output, 'assets'), { recursive: true });
  if (!report.diagramErrors.length) {
    const sourceAssets = new Set(await fs.readdir(path.join(source, 'assets')));
    const outputAssetsDir = path.join(output, 'assets');
    for (const name of await fs.readdir(outputAssetsDir)) {
      if (name.startsWith('flow-') && name.endsWith('.svg') && !usedFlowSvgs.has(name) && !sourceAssets.has(name)) {
        await fs.unlink(path.join(outputAssetsDir, name));
      }
    }
  }

  await fs.cp(path.join(here, 'node_modules/katex/dist'), path.join(output, 'assets/katex'), { recursive: true });
  await fs.copyFile(path.join(here, 'reader.css'), path.join(output, 'assets/reader.css'));
  await fs.copyFile(path.join(here, 'reader.js'), path.join(output, 'assets/reader.js'));

  const quantumLabSrc = path.join(here, 'quantum-lab.html');
  await fs.mkdir(path.join(output, 'lab'), { recursive: true });
  await fs.copyFile(quantumLabSrc, path.join(output, 'lab/quantum-lab.html'));

  await fs.mkdir(path.join(output, 'research'), { recursive: true });
  // Follow research-report links so a portable audit record retains its evidence.
  for (const [from, to] of reportCopies) {
    await fs.copyFile(from, to);
    if (from.endsWith('.md')) {
      const raw = await fs.readFile(from, 'utf8');
      for (const match of raw.matchAll(/\]\(([^)]+)\)/g)) {
        if (/^(https?:|#|mailto:)/.test(match[1])) continue;
        const target = path.resolve(path.dirname(from), match[1].split('#')[0]);
        if (target.startsWith(path.join(root, 'work/research') + path.sep) && !reportCopies.has(target)) {
          try { await fs.access(target); reportCopies.set(target, path.join(output, 'research', path.basename(target))); } catch {}
        }
      }
    }
  }

  await fs.mkdir(path.join(output, 'assets/licenses'), { recursive: true });
  for (const [pkg, license] of [['katex', 'LICENSE'], ['mermaid', 'LICENSE'], ['marked', 'LICENSE.md']]) {
    await fs.copyFile(path.join(here, 'node_modules', pkg, license), path.join(output, 'assets/licenses', pkg + '.txt'));
  }

  report.inputHashes = {};
  report.readingOrder = orderedReading.sequence.map(file => path.relative(root, path.join(output, outputName(file))));
  const inputFiles = [
    fileURLToPath(import.meta.url),
    path.join(here, 'reading-order.mjs'),
    path.join(here, 'reader.css'),
    path.join(here, 'reader.js'),
    quantumLabSrc,
    ...(await walk(path.join(source, 'assets'))),
    ...(await walk(path.join(root, 'codes'))).filter(f => !f.includes('__pycache__') && !f.endsWith('.pyc')),
  ];
  for (const file of inputFiles) {
    report.inputHashes[path.relative(root, file)] = digest(await fs.readFile(file));
  }

  await fs.writeFile(path.join(root, 'work/research/reader-build-report.json'), JSON.stringify(report, null, 2));
  await fs.writeFile(path.join(output, 'research/reader-build-report.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify({
    pages: report.pages.length,
    formulas: report.formulas,
    diagrams: report.diagrams,
    mathErrors: report.mathErrors,
    diagramErrors: report.diagramErrors,
  }, null, 2));
  if (report.mathErrors.length || report.diagramErrors.length) process.exitCode = 1;
} finally {
  if (browser) await browser.close();
  if (server) await new Promise(resolve => server.close(resolve));
}
