import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.HANDBOOK_NODE_MODULES
  ? path.join(process.env.HANDBOOK_NODE_MODULES, 'playwright')
  : 'playwright');
const browserOptions = { headless: true };
if (process.env.HANDBOOK_CHROMIUM) browserOptions.executablePath = process.env.HANDBOOK_CHROMIUM;
const report = { generatedAt: new Date().toISOString(), pages: [], errors: [], externalRequests: [], screenshots: [] };
const build = JSON.parse(await fs.readFile(path.join(root, 'work/research/reader-build-report.json'), 'utf8'));
const edition = (await fs.readFile(path.join(root, 'handbook/README.md'), 'utf8')).match(/^>\s*版本：(\d{4}-\d{2}-\d{2})/m)?.[1];
if (!edition || Number.isNaN(Date.parse(edition + 'T00:00:00Z')) || new Date(edition + 'T00:00:00Z').toISOString().slice(0, 10) !== edition) throw new Error('handbook/README.md must declare a valid YYYY-MM-DD edition');
const digest = value => crypto.createHash('sha256').update(value).digest('hex');
for (const [file, expected] of Object.entries(build.inputHashes || {})) if (digest(await fs.readFile(path.join(root,file))) !== expected) report.errors.push({file,message:'build input changed; rebuild required'});
for (const entry of build.pages) for (const [key,hash] of [['source','sourceSha256'],['output','outputSha256']]) if (digest(await fs.readFile(path.join(root,entry[key]))) !== entry[hash]) report.errors.push({file:entry[key],message:'source/output hash differs from build'});
for (const entry of build.codeCopies || []) if (digest(await fs.readFile(path.join(root, entry.output))) !== entry.outputSha256) report.errors.push({file:entry.output,message:'copied code differs from build'});
const shots = path.join(root, 'work/rendered');
await fs.mkdir(shots, { recursive: true });
const browser = await chromium.launch(browserOptions);
try {
  for (const width of [1440, 390]) {
    const page = await browser.newPage({ viewport: { width, height: 1000 }, deviceScaleFactor: 1 });
    page.on('pageerror', e => report.errors.push({ width, type: 'javascript', message: e.message }));
    page.on('request', req => { if (/^https?:/.test(req.url())) report.externalRequests.push(req.url()); });
    for (const entry of build.pages) {
      await page.goto(pathToFileURL(path.join(root, entry.output)).href);
      await page.evaluate(async () => { await document.fonts.ready; for (const img of document.images) { img.loading = 'eager'; await img.decode().catch(() => {}); } });
      if (width === 1440) {
        const isFoundation = /^reader\/quantum-mechanics\/\d/.test(entry.output);
        const isMain = /^reader\/\d/.test(entry.output);
        if (isFoundation || isMain) {
          const sequence = build.pages.filter(p => isFoundation ? /^reader\/quantum-mechanics\/\d/.test(p.output) : /^reader\/\d/.test(p.output)).map(p=>p.output).sort();
          const at = sequence.indexOf(entry.output);
          const expected = [sequence[at-1],sequence[at+1]].filter(Boolean).map(p=>pathToFileURL(path.join(root,p)).href);
          const actual = await page.locator('.page-turn a').evaluateAll(links=>links.map(a=>a.href));
          if (JSON.stringify(actual) !== JSON.stringify(expected)) report.errors.push({file:entry.output,message:'part-local previous/next navigation differs',expected,actual});
        }
        if (await page.locator('.chapters nav a[href$="quantum-mechanics/index.html"]').count() !== 1) report.errors.push({file:entry.output,message:'foundation guide missing from navigation'});
      }
      const result = await page.evaluate(() => {
        const failures = [];
        if (document.documentElement.scrollWidth > innerWidth + 2) {
          const offenders = [...document.querySelectorAll('article *')].filter(e => {
            if (e.getBoundingClientRect().right <= innerWidth + 2) return false;
            for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) if (['auto','scroll','hidden'].includes(getComputedStyle(p).overflowX)) return false;
            return true;
          }).slice(0, 5).map(e => ({tag: e.tagName, class: e.className?.baseVal ?? e.className, text: e.textContent.slice(0,100), right:e.getBoundingClientRect().right}));
          const wide = [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > innerWidth + 2).sort((a,b)=>b.getBoundingClientRect().right-a.getBoundingClientRect().right).slice(0,4).map(e=>({tag:e.tagName,class:e.className?.baseVal ?? e.className,right:e.getBoundingClientRect().right}));
          failures.push('page horizontally overflows: ' + JSON.stringify({width:document.documentElement.scrollWidth,offenders,wide}));
        }
        for (const img of document.images) if (!img.complete || !img.naturalWidth) failures.push('broken image: ' + img.getAttribute('src'));
        if (document.querySelector('.math-error,.katex-error,pre code.language-mermaid,[data-handbook-math]')) failures.push('unrendered math/diagram');
        if (document.styleSheets.length < 2 || getComputedStyle(document.querySelector('header')).position !== 'sticky') failures.push('reader CSS not loaded');
        const mathml = document.querySelector('.katex-mathml');
        if (mathml && getComputedStyle(mathml).position !== 'absolute') failures.push('KaTeX CSS not loaded');
        const ids = [...document.querySelectorAll('[id]')].map(e => e.id);
        if (new Set(ids).size !== ids.length) failures.push('duplicate HTML id');
        for (const t of document.querySelectorAll('table')) { const expected = t.rows[0]?.cells.length; for (const r of t.rows) if (r.cells.length !== expected) failures.push('table row width mismatch'); }
        const headings = [...document.querySelectorAll('article h1,article h2,article h3,article h4,article h5,article h6')].map(e => ({ text: e.textContent, id: e.id }));
        const latex = [...document.querySelectorAll('article annotation[encoding="application/x-tex"]')].map(e=>e.textContent);
        const expectedSections = [...document.querySelectorAll('article h2,article h3')].map(e=>'#'+e.id);
        for (const nav of document.querySelectorAll('.contents nav,.inline-contents nav')) if (JSON.stringify([...nav.querySelectorAll('a')].map(a=>a.getAttribute('href'))) !== JSON.stringify(expectedSections)) failures.push('section navigation differs from H2/H3 sequence');
        for (const a of document.querySelectorAll('.image-open')) if (a.href !== a.querySelector('img')?.src) failures.push('original-size image link differs from image');
        for (const figure of document.querySelectorAll('figure.flowchart')) {
          const alt = figure.querySelector('img')?.getAttribute('alt') || '';
          if (!alt || /流程关系图\s*\d/.test(alt) || !figure.querySelector('figcaption')?.textContent.includes(alt)) failures.push('flowchart needs a specific matching title and text alternative');
        }
        for (const e of document.querySelectorAll('.table-scroll,.katex-display,.flowchart,.math-inline,.scientific-svg')) if (e.scrollWidth > e.clientWidth + 2) {
          const before = e.scrollLeft; e.scrollLeft = e.scrollWidth;
          if (Math.abs(e.scrollLeft - (e.scrollWidth-e.clientWidth)) > 2) failures.push('scroll area cannot reach right edge');
          e.scrollLeft = before;
        }
        return { failures, latex, formulas: document.querySelectorAll('article .katex').length, images: document.images.length, headings, links: [...document.querySelectorAll('a[href]')].map(a => a.href), footer: document.querySelector('main footer')?.textContent || '' };
      });
      report.pages.push({ file: entry.output, width, formulas: result.formulas, images: result.images });
      for (const message of result.failures) report.errors.push({ file: entry.output, width, message });
      if (!result.footer.includes(`${edition} 版`)) report.errors.push({ file: entry.output, width, message: 'reader footer edition differs from handbook README' });
      if (result.formulas !== entry.formulas) report.errors.push({ file: entry.output, width, message:'formula count mismatch', expected:entry.formulas, actual:result.formulas });
      if (digest(JSON.stringify(result.latex)) !== entry.mathSourceDigest) report.errors.push({file:entry.output,width,message:'formula content or order mismatch'});
      if (JSON.stringify(result.headings.map(h=>h.id)) !== JSON.stringify(entry.headingIds)) report.errors.push({file:entry.output,width,message:'heading sequence mismatch'});
      if (width === 1440) for (const href of new Set(result.links)) {
        if (!href.startsWith('file:')) continue;
        const u = new URL(href), fragment = decodeURIComponent(u.hash.slice(1)); u.hash = '';
        const target = fileURLToPath(u);
        try {
          if (!target.startsWith(path.join(root, 'reader') + path.sep)) report.errors.push({file:entry.output,message:'local link is not portable: '+href});
          await fs.access(target);
          if (fragment && target.endsWith('.html')) {
            const html = await fs.readFile(target, 'utf8');
            if (!html.includes(`id="${fragment}"`)) report.errors.push({ file: entry.output, message: 'broken anchor: ' + href });
          }
        } catch { report.errors.push({ file: entry.output, message: 'broken file: ' + href }); }
      }
      if (['reader/index.html','reader/02-single-qubit.html','reader/03-multiple-qubits.html','reader/04-circuits-protocols.html','reader/07-algorithms.html','reader/08-applications.html','reader/09-hardware.html','reader/12-security-network-frontiers.html','reader/16-advanced-algorithms-verification.html','reader/18-channels-capacities-complexity.html','reader/appendices/notation.html','reader/appendices/prerequisites.html'].includes(entry.output) || entry.output.startsWith('reader/quantum-mechanics/') || entry.output.startsWith('reader/labs/') || entry.output === 'reader/appendices/software-practice.html') {
        if (width === 390) await page.locator('.chapters details').evaluate(e => e.open = false);
        const name = (entry.output.startsWith('reader/quantum-mechanics/') ? 'qm-' : entry.output.startsWith('reader/labs/') ? 'lab-' : '') + path.basename(entry.output, '.html') + '-' + width + '.png';
        await page.screenshot({ path: path.join(shots, name) }); report.screenshots.push('work/rendered/' + name);
      }
    }
    // Check the search and chapter navigation as a reader would use them.
    await page.goto(pathToFileURL(path.join(root, 'reader/index.html')).href);
    if (width === 390) {
      const name = 'index-390-navigation-open.png';
      await page.screenshot({ path: path.join(shots, name) });
      report.screenshots.push('work/rendered/' + name);
    }
    await page.locator('#nav-search').fill('单量子比特');
    if (await page.locator('.chapters nav a:visible').count() !== 1) report.errors.push({ width, message: 'chapter search should identify chapter 02' });
    await page.locator('#nav-search').fill('入门先修');
    if (await page.locator('.chapters nav a:visible').count() !== 1) report.errors.push({ width, message: 'chapter search should identify prerequisite guide' });
    await page.locator('#nav-search').fill('');
    await page.locator('.chapters a[href="02-single-qubit.html"]').click();
    if (!page.url().endsWith('02-single-qubit.html')) report.errors.push({ width, message: 'chapter navigation failed' });
    if (width === 390) {
      await page.goto(pathToFileURL(path.join(root,'reader/12-security-network-frontiers.html')).href);
      await page.locator('.inline-contents summary').click();
      await page.screenshot({path:path.join(shots,'12-mobile-section-menu.png')});
      report.screenshots.push('work/rendered/12-mobile-section-menu.png');
      const section = page.locator('.inline-contents .toc-level-3').first();
      const destination = await section.getAttribute('href');
      await section.click();
      await page.waitForFunction(id=>{const y=document.getElementById(id.slice(1)).getBoundingClientRect().top;return y>=62&&y<=150},destination,{timeout:5000}).catch(()=>report.errors.push({width,message:'mobile heading did not settle below fixed header'}));
      const reached = await page.evaluate(id=>({hash:decodeURIComponent(location.hash),open:document.querySelector('.inline-contents').open,top:document.getElementById(id.slice(1)).getBoundingClientRect().top}),destination);
      if (reached.hash !== destination || reached.open) report.errors.push({width,message:'mobile section navigation failed',reached});
      await page.screenshot({path:path.join(shots,'12-mobile-section-arrival.png')});
      report.screenshots.push('work/rendered/12-mobile-section-arrival.png');
    }
    await page.close();
  }
  const audioPage = await browser.newPage();
  await audioPage.goto(pathToFileURL(path.join(root, 'reader/labs/audio.html')).href);
  report.audioChecks = await audioPage.locator('audio').evaluateAll(async elements => {
    return Promise.all(elements.map(e => new Promise(resolve => {
      const done = () => resolve({src:e.getAttribute('src'), duration:e.duration, readyState:e.readyState, error:e.error?.message || null, autoplay:e.autoplay, controls:e.controls});
      e.addEventListener('loadedmetadata', done, {once:true});
      e.addEventListener('error', done, {once:true});
      setTimeout(done, 5000); e.load();
    })));
  });
  if (report.audioChecks.length !== 5 || report.audioChecks.some(a => a.error || a.duration !== 4 || a.autoplay || !a.controls)) report.errors.push({message:'teaching WAV metadata/controls failed', audio:report.audioChecks});
  await audioPage.close();
  const sample = await browser.newPage({viewport:{width:390,height:1000}});
  for (const [file,selector,label] of [['labs/audio.html','.table-scroll','audio-controls'],['labs/practice.html','.katex-display','statistics-formula'],['appendices/notation.html','.table-scroll','table'],['appendices/prerequisites.html','.table-scroll','prerequisites-table'],['10-error-correction.html','.table-scroll','syndrome-table'],['06-algorithmic-primitives.html','.katex-display','formula'],['08-applications.html','.flowchart','flowchart'],['19-engineering-architecture.html','.scientific-svg[href$="hardware-control-lanes.svg"]','hardware-figure'],['10-error-correction.html','.scientific-svg[href$="surface-code-events.svg"]','surface-code-figure'],['15-practice-research.html','.scientific-svg[href$="bell-witness-sampling.svg"]','bell-witness-figure']]) {
    await sample.goto(pathToFileURL(path.join(root,'reader',file)).href);
    await sample.evaluate(()=>document.fonts.ready);
    await sample.locator(selector).evaluateAll(elements => { const e=elements.find(e=>e.scrollWidth>e.clientWidth+2)||elements[0]; if(e)e.setAttribute('data-scroll-sample','true'); });
    const region = sample.locator('[data-scroll-sample="true"]');
    await region.scrollIntoViewIfNeeded();
    await region.evaluate(e=>e.scrollLeft=e.scrollWidth);
    const name = label+'-390-right-edge.png';
    await region.screenshot({path:path.join(shots,name)}); report.screenshots.push('work/rendered/'+name);
  }
  for (const [file,needle,label] of [['03-multiple-qubits.html','代入','chsh-table'],['04-circuits-protocols.html','Bob 的归一化条件态','teleportation-table'],['19-engineering-architecture.html','仅局域操作的线路切割','modularity-table'],['15-practice-research.html','乘积为','bell-witness-counts-table']]) {
    await sample.goto(pathToFileURL(path.join(root,'reader',file)).href);
    const region = sample.locator('.table-scroll').filter({hasText:needle}).first();
    if (await region.count() !== 1) { report.errors.push({file,message:'new teaching table not found: '+label}); continue; }
    await region.scrollIntoViewIfNeeded();
    await region.evaluate(e=>e.scrollLeft=e.scrollWidth);
    const name = label+'-390-right-edge.png';
    await region.screenshot({path:path.join(shots,name)}); report.screenshots.push('work/rendered/'+name);
  }
  for (const [file,needle,label] of [['03-multiple-qubits.html','漏检不一定是因为关联落在别的轴上','entanglement-witness'],['08-applications.html','有限样本的加权估计不能代替精确期望值','vqe-sampling'],['17-computation-models.html','重复实验的成功概率目标','tts-probability'],['19-engineering-architecture.html','都要做的链修复','tts-postprocessing']]) {
    await sample.goto(pathToFileURL(path.join(root,'reader',file)).href);
    const region = sample.locator('article p').filter({hasText:needle}).first();
    if (await region.count() !== 1) { report.errors.push({file,message:'revised explanation not found: '+label}); continue; }
    await region.scrollIntoViewIfNeeded();
    const name = label+'-390.png';
    await region.screenshot({path:path.join(shots,name)}); report.screenshots.push('work/rendered/'+name);
  }
  await sample.goto(pathToFileURL(path.join(root,'reader/04-circuits-protocols.html')).href);
  await sample.screenshot({path:path.join(shots,'04-circuits-protocols-390-full.png'),fullPage:true});
  report.screenshots.push('work/rendered/04-circuits-protocols-390-full.png');
  await sample.goto(pathToFileURL(path.join(root,'reader/16-advanced-algorithms-verification.html')).href);
  await sample.locator('.flowchart').nth(1).locator('img').evaluate(async e => { e.loading = 'eager'; await e.decode(); });
  await sample.locator('.flowchart').nth(1).screenshot({path:path.join(shots,'16-qsvt-flowchart-390.png')});
  report.screenshots.push('work/rendered/16-qsvt-flowchart-390.png');
  const qsvtSvg = await sample.locator('.flowchart').nth(1).locator('img').getAttribute('src');
  await sample.goto(pathToFileURL(path.join(root,'reader',qsvtSvg)).href);
  await sample.locator('svg').screenshot({path:path.join(shots,'16-qsvt-flowchart-full.png')});
  report.screenshots.push('work/rendered/16-qsvt-flowchart-full.png');
  await sample.close();
  const svgPage = await browser.newPage({ viewport: { width: 1000, height: 1000 } });
  report.svgChecks = [];
  for (const file of (await fs.readdir(path.join(root, 'handbook/assets'))).filter(f => f.endsWith('.svg'))) {
    await svgPage.goto(pathToFileURL(path.join(root, 'handbook/assets', file)).href);
    await svgPage.evaluate(() => document.fonts.ready);
    await svgPage.evaluate(() => { const s = document.querySelector('svg'), v = s.viewBox.baseVal; s.setAttribute('width', v.width); s.setAttribute('height', v.height); });
    const bounds = await svgPage.evaluate(() => {
      const svg = document.querySelector('svg'), v = svg.viewBox.baseVal;
      return [...svg.querySelectorAll('text')].flatMap(e => {
        const local = e.getBBox(), matrix = svg.getCTM().inverse().multiply(e.getCTM());
        const points = [[local.x,local.y],[local.x+local.width,local.y],[local.x,local.y+local.height],[local.x+local.width,local.y+local.height]].map(([x,y]) => new DOMPoint(x,y).matrixTransform(matrix));
        const xs = points.map(p=>p.x), ys = points.map(p=>p.y);
        const b = {x:Math.min(...xs),y:Math.min(...ys),width:Math.max(...xs)-Math.min(...xs),height:Math.max(...ys)-Math.min(...ys)};
        return b.x < v.x - 1 || b.x + b.width > v.x + v.width + 1 || b.y < v.y - 1 || b.y + b.height > v.y + v.height + 1 ? [{text:e.textContent, x:b.x,y:b.y,width:b.width,height:b.height}] : [];
      });
    });
    report.svgChecks.push({ file, textOutsideViewBox: bounds });
    if (bounds.length) report.errors.push({ file, message:'SVG text extends beyond viewBox', bounds });
    await svgPage.locator('svg').screenshot({path:path.join(shots,file.replace('.svg','-light.png'))});
    await svgPage.emulateMedia({colorScheme:'dark'});
    await svgPage.locator('svg').screenshot({path:path.join(shots,file.replace('.svg','-dark.png'))});
    await svgPage.emulateMedia({colorScheme:'light'});
  }
  await svgPage.close();
  const reportJson = JSON.stringify(report, null, 2);
  await fs.writeFile(path.join(root, 'work/research/reader-verification.json'), reportJson);
  await fs.mkdir(path.join(root, 'reader/research'), { recursive: true });
  await fs.writeFile(path.join(root, 'reader/research/reader-verification.json'), reportJson);
  console.log(JSON.stringify({ pagesAtTwoWidths: report.pages.length, screenshots: report.screenshots.length, externalRequests: report.externalRequests.length, errors: report.errors }, null, 2));
  if (report.errors.length || report.externalRequests.length) process.exitCode = 1;
} finally { await browser.close(); }
