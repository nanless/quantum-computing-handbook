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
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const slug = s => s.toLowerCase().replace(/[\p{P}\p{S}]/gu, c => c === '-' || c === '_' ? c : '').trim().replace(/\s/g, '-');
const walk = async dir => (await Promise.all((await fs.readdir(dir, { withFileTypes: true })).map(e => e.isDirectory() ? walk(path.join(dir, e.name)) : path.join(dir, e.name)))).flat();
await fs.mkdir(output, { recursive: true });
await fs.mkdir(cache, { recursive: true });
const files = (await walk(source)).filter(f => f.endsWith('.md')).sort();
const contents = new Map(await Promise.all(files.map(async f => [f, await fs.readFile(f, 'utf8')])));
const edition = contents.get(path.join(source, 'README.md')).match(/^>\s*版本：(\d{4}-\d{2}-\d{2})/m)?.[1];
if (!edition || Number.isNaN(Date.parse(edition + 'T00:00:00Z')) || new Date(edition + 'T00:00:00Z').toISOString().slice(0, 10) !== edition) throw new Error('handbook/README.md must declare a valid YYYY-MM-DD edition');
const titleOf = f => contents.get(f).match(/^# (.+)/m)[1];
const outputName = f => path.relative(source, f).replace(/README\.md$/, 'index.html').replace(/\.md$/, '.html');
const chapters = files.filter(f => /^\d\d-/.test(path.basename(f)));
const foundations = chapters.filter(f => path.dirname(f) === path.join(source, 'quantum-mechanics'));
const mainChapters = chapters.filter(f => path.dirname(f) === source);
const orderedReading = readingPlan(chapters);
const appendixOrder = ['prerequisites.md','notation.md','glossary.md','exercises.md','references.md','software-practice.md','audit-log.md'];
const labs = files.filter(f => f.includes('/labs/'));
const appendices = files.filter(f => f.includes('/appendices/')).sort((a,b) => appendixOrder.indexOf(path.basename(a)) - appendixOrder.indexOf(path.basename(b)));
// Keep diagram titles specific to the relationship shown, rather than generating
// "flowchart 1" captions that tell readers nothing about the figure.
const diagramTitles = {
  'README.md': ['主篇 00—19 章的主题分组与推荐衔接'],
  '00-overview.md': ['一次量子计算从输入到验证的五个环节'],
  '08-applications.md': ['变分算法中量子测量与经典参数更新的循环'],
  '09-hardware.md': ['量子计算机从程序到控制、读出和反馈的系统链'],
  '11-resources-benchmarks.md': ['从应用目标逐层估算逻辑与物理资源'],
  '12-security-network-frontiers.md': ['机内互连、远距离网络与量子互联网的范围区别', '量子网络从物理链路到应用服务的分层'],
  '14-compilation-control.md': ['算法线路到物理执行的编译与控制步骤', '门校准的依赖顺序与漂移回归', '实时纠错从读出到译码和反馈的路径'],
  '16-advanced-algorithms-verification.md': ['隐藏子群算法从查询到经典恢复的共同骨架', '从矩阵编码到奇异值变换的两条构造路径', '大型量子模拟结果的四类交叉证据'],
  '17-computation-models.md': ['量子计算模型之间的联系与不能直接等同之处', '模拟量子模拟器结论的四类核查', '核对一种计算模型性能声明的七个问题'],
  '18-channels-capacities-complexity.md': ['量子态、信道与容量概念之间的关系', '纠缠资源的制备、蒸馏与度量', '交互证明中验证者与证明者交换消息的顺序', '量子指纹在同时消息模型中的通信方式'],
};
const report = { generatedAt: new Date().toISOString(), pages: [], mathErrors: [], diagramErrors: [], diagrams: 0, formulas: 0 };
const reportCopies = new Map();
const digest = value => crypto.createHash('sha256').update(value).digest('hex');
let browser, server, page;
async function diagram(code) {
  const key = crypto.createHash('sha256').update('mermaid-11.6-reader-v3\n' + code).digest('hex');
  const file = path.join(cache, key + '.svg');
  try { return await fs.readFile(file, 'utf8'); } catch {}
  if (!page) {
    server = http.createServer(async (req, res) => {
      if (req.url === '/') { res.setHeader('Content-Type', 'text/html'); res.end('<!doctype html><html><head><meta charset="utf-8"></head><body></body></html>'); return; }
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\//, '');
      const file = path.resolve(here, rel);
      if (!file.startsWith(here + path.sep)) { res.writeHead(403).end(); return; }
      try { res.setHeader('Content-Type', /\.m?js$/.test(file) ? 'text/javascript' : 'application/octet-stream'); res.end(await fs.readFile(file)); } catch { res.writeHead(404).end(); }
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
function protectMath(text, f) {
  const fragments = [], latexSources = [];
  const pattern = /(^[ \t]*```[^\n]*\n[\s\S]*?^[ \t]*```[^\n]*$)|(`+)[^\n]*?\2|\$\$([\s\S]*?)\$\$|\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)|(?<!\\)\$(?!\$)((?:\\.|[^$\n])+?)(?<!\\)\$/gm;
  const protectedText = text.replace(pattern, (full, fence, ticks, display1, display2, inline1, inline2) => {
    if (fence || ticks) return full;
    const display = display1 !== undefined || display2 !== undefined;
    const latex = display1 ?? display2 ?? inline1 ?? inline2;
    latexSources.push(latex);
    let html;
    try { html = katex.renderToString(latex, { displayMode: display, throwOnError: true, strict: 'ignore', trust: false, output: 'htmlAndMathml' }); }
    catch (e) { report.mathErrors.push({ file: path.relative(root, f), latex, error: e.message }); html = '<code class="math-error">' + esc(latex) + '</code>'; }
    report.formulas++;
    const id = fragments.length; fragments.push(display ? html : '<span class="math-inline">' + html + '</span>');
    return display ? `<div data-handbook-math="${id}"></div>` : `<span data-handbook-math="${id}"></span>`;
  });
  return { protectedText, mathSourceDigest: digest(JSON.stringify(latexSources)), restore: html => html.replace(/<(div|span) data-handbook-math="(\d+)"><\/\1>/g, (_, tag, id) => fragments[+id]) };
}
const headingsByFile = new Map();
for (const [f, text] of contents) {
  const used = new Map();
  headingsByFile.set(f, marked.lexer(text).filter(token => token.type === 'heading').map(token => {
    const base = slug(token.text), count = used.get(base) || 0; used.set(base, count + 1);
    return { level: token.depth, title: token.text, id: base + (count ? '-' + count : '') };
  }));
}
try {
  for (const [f, raw] of contents) {
    let text = raw, diagramCount = 0;
    for (const match of [...text.matchAll(/```mermaid\n([\s\S]*?)```/g)]) {
      diagramCount++; report.diagrams++;
      try {
        const diagramTitle = diagramTitles[path.relative(source, f)]?.[diagramCount - 1];
        if (!diagramTitle) throw new Error('missing descriptive diagram title');
        const svg = await diagram(match[1]);
        const rel = 'assets/flow-' + crypto.createHash('sha256').update(match[1]).digest('hex').slice(0, 14) + '.svg';
        await fs.mkdir(path.join(output, 'assets'), { recursive: true });
        await fs.writeFile(path.join(output, rel), svg);
        const prefix = path.dirname(outputName(f)) === '.' ? '' : '../';
        const intrinsicWidth = Number(svg.match(/viewBox="[^" ]+ [^" ]+ ([^" ]+)/)?.[1]) || 650;
        text = text.replace(match[0], `<figure class="flowchart"><img src="${prefix + rel}" style="width:${intrinsicWidth}px" alt="${esc(diagramTitle)}" loading="lazy"><figcaption>图 ${diagramCount}｜${esc(diagramTitle)} · 横向较长时可在图内滚动 · <a href="${prefix + rel}">打开完整图</a></figcaption></figure>`);
      } catch (e) { report.diagramErrors.push({ file: path.relative(root, f), diagram: diagramCount, error: e.message }); }
    }
    const formulasBefore = report.formulas;
    const { protectedText, mathSourceDigest, restore } = protectMath(text, f);
    const headings = headingsByFile.get(f); let hi = 0;
    const renderer = new marked.Renderer();
    renderer.image = function ({ href, text, title }) { const svgClass = /\.svg(?:$|[?#])/.test(href) ? ' scientific-svg' : ''; return `<a class="image-open${svgClass}" href="${esc(href)}" aria-label="打开原尺寸图：${esc(text)}"><img src="${esc(href)}" alt="${esc(text)}"${title ? ` title="${esc(title)}"` : ''} loading="lazy"><span>打开原尺寸图 ↗</span></a>`; };
    renderer.heading = function ({ tokens, depth }) { const h = headings[hi++]; return `<h${depth} id="${esc(h.id)}">${this.parser.parseInline(tokens)}</h${depth}>\n`; };
    renderer.link = function ({ href, title, tokens }) {
      if (!/^(https?:|mailto:|#)/.test(href)) {
        const [p, anchor] = href.split('#'), target = path.resolve(path.dirname(f), p);
        if (contents.has(target)) href = path.relative(path.dirname(path.join(output, outputName(f))), path.join(output, outputName(target))) + (anchor ? '#' + anchor : '');
        else if (target.startsWith(path.join(root, 'codes') + path.sep)) {
          const local = path.join(output, 'codes', path.relative(path.join(root, 'codes'), target));
          href = path.relative(path.dirname(path.join(output, outputName(f))), local) + (anchor ? '#' + anchor : '');
        } else if (target.startsWith(path.join(root, 'work/research') + path.sep)) {
          const local = path.join(output, 'research', path.basename(target));
          reportCopies.set(target, local);
          href = path.relative(path.dirname(path.join(output, outputName(f))), local) + (anchor ? '#' + anchor : '');
        } else if (target.startsWith(output + path.sep)) {
          href = path.relative(path.dirname(path.join(output, outputName(f))), target) + (anchor ? '#' + anchor : '');
        }
      }
      const link = `<a href="${esc(href)}"${title ? ` title="${esc(title)}"` : ''}>${this.parser.parseInline(tokens)}</a>`;
      return /\.wav$/.test(href) ? `${link}<audio controls preload="none" src="${esc(href)}" aria-label="教学合成音频"></audio>` : link;
    };
    let body = restore(marked.parse(protectedText, { renderer, gfm: true }));
    body = body.replace(/<table>/g, '<div class="table-scroll" tabindex="0"><table>').replace(/<\/table>/g, '</table></div>');
    const prefix = outputName(f).includes('/') ? '../' : '';
    const chapterLinks = list => list.map(c => `<a ${c === f ? 'aria-current="page" ' : ''}href="${prefix + outputName(c)}">${esc(titleOf(c))}</a>`).join('');
    const nav = orderedReading.groups.map((group, i) => `<div class="nav-label">${esc(group.label)}</div>${i === 1 ? `<a href="${prefix}quantum-mechanics/index.html">物理篇导读与先修说明</a>` : ''}${chapterLinks(group.files)}`).join('') + `<div class="nav-label">实验、代码与音频</div>${chapterLinks(labs)}`;
    const appNav = appendices.map(c => `<a ${c === f ? 'aria-current="page" ' : ''}href="${prefix + outputName(c)}">${esc(titleOf(c))}</a>`).join('');
    const renderedHeadings = new Map([...body.matchAll(/<h[23] id="([^"]+)">([\s\S]*?)<\/h[23]>/g)].map(m => [m[1], m[2]]));
    const toc = headings.filter(h => h.level === 2 || h.level === 3).map(h => `<a class="toc-level-${h.level}" href="#${esc(h.id)}">${renderedHeadings.get(esc(h.id)) || esc(h.title)}</a>`).join('');
    const mobileToc = toc ? `<details class="inline-contents"><summary>本页导航 · 展开查找小节</summary><nav aria-label="本页章节">${toc}</nav></details>` : '';
    const sequence = orderedReading.sequence;
    const index = sequence.indexOf(f);
    const prev = index > 0 ? `<a href="${prefix + outputName(sequence[index - 1])}">← ${esc(titleOf(sequence[index - 1]))}</a>` : '';
    const next = index >= 0 && index < sequence.length - 1 ? `<a href="${prefix + outputName(sequence[index + 1])}">${esc(titleOf(sequence[index + 1]))} →</a>` : '';
    const html = `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(titleOf(f))} · 量子计算手册</title><link rel="stylesheet" href="${prefix}assets/katex/katex.min.css"><link rel="stylesheet" href="${prefix}assets/reader.css"></head><body><a class="skip" href="#content">跳到正文</a><header><a class="brand" href="${prefix}index.html"><span class="mark">ψ</span>量子计算手册</a><span class="edition">从直觉到研究入口</span><button type="button" onclick="window.print()">打印本章</button></header><div class="layout"><aside class="chapters"><details open><summary>全书目录</summary><input type="search" id="nav-search" aria-label="查找章节" placeholder="查找章节…"><nav>${nav}<div class="nav-label">附录</div>${appNav}</nav></details></aside><main id="content"><div class="eyebrow">QUANTUM COMPUTING · 学习手册</div>${mobileToc}<article>${body}</article><div class="page-turn">${prev}${next}</div><footer>${edition} 版 · 公式、图表和字体均保存在本地<br>配套 Markdown 为可编辑原稿；事实更新与审校范围见审校记录。</footer></main><aside class="contents"><strong>本页内容</strong><nav>${toc}</nav><a class="top" href="#content">↑ 返回顶部</a></aside></div><script>document.getElementById('nav-search').addEventListener('input',function(){const q=this.value.toLowerCase();document.querySelectorAll('.chapters nav a').forEach(a=>a.hidden=!a.textContent.toLowerCase().includes(q))});document.querySelectorAll('.inline-contents a').forEach(a=>a.addEventListener('click',()=>{document.querySelector('.inline-contents').open=false}));</script></body></html>`;
    const target = path.join(output, outputName(f)); await fs.mkdir(path.dirname(target), { recursive: true }); await fs.writeFile(target, html);
    report.pages.push({ source: path.relative(root, f), output: path.relative(root, target), sourceSha256: digest(raw), outputSha256: digest(html), mathSourceDigest, headingIds: headings.map(h=>h.id), diagrams: diagramCount, headings: hi, formulas: report.formulas - formulasBefore });
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
    report.codeCopies.push({source: path.relative(root, from), output: path.relative(root, to), outputSha256: digest(await fs.readFile(to))});
  }
  await fs.cp(path.join(source, 'assets'), path.join(output, 'assets'), { recursive: true });
  await fs.cp(path.join(here, 'node_modules/katex/dist'), path.join(output, 'assets/katex'), { recursive: true });
  await fs.copyFile(path.join(here, 'reader.css'), path.join(output, 'assets/reader.css'));
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
          // Historical reports also contain quoted Markdown patches, not only links.
          try { await fs.access(target); reportCopies.set(target, path.join(output, 'research', path.basename(target))); } catch {}
        }
      }
    }
  }
  await fs.mkdir(path.join(output, 'assets/licenses'), { recursive: true });
  for (const [pkg, license] of [['katex', 'LICENSE'], ['mermaid', 'LICENSE'], ['marked', 'LICENSE.md']]) await fs.copyFile(path.join(here, 'node_modules', pkg, license), path.join(output, 'assets/licenses', pkg + '.txt'));
  report.inputHashes = {};
  report.readingOrder = orderedReading.sequence.map(file => path.relative(root, path.join(output, outputName(file))));
  for (const file of [fileURLToPath(import.meta.url), path.join(here,'reading-order.mjs'), path.join(here,'reader.css'), ...(await walk(path.join(source,'assets'))), ...(await walk(path.join(root,'codes'))).filter(f => !f.includes('__pycache__') && !f.endsWith('.pyc'))]) report.inputHashes[path.relative(root,file)] = digest(await fs.readFile(file));
  await fs.writeFile(path.join(root, 'work/research/reader-build-report.json'), JSON.stringify(report, null, 2));
  await fs.writeFile(path.join(output, 'research/reader-build-report.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ pages: report.pages.length, formulas: report.formulas, diagrams: report.diagrams, mathErrors: report.mathErrors, diagramErrors: report.diagramErrors }, null, 2));
  if (report.mathErrors.length || report.diagramErrors.length) process.exitCode = 1;
} finally { if (browser) await browser.close(); if (server) await new Promise(resolve => server.close(resolve)); }
