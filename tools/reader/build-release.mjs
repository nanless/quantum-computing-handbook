#!/usr/bin/env node
/**
 * Build and verify the full GitHub Release artifact suite for the Quantum Computing Handbook.
 *
 * Usage:
 *   node tools/reader/build-release.mjs [--version v1.0.0]
 *
 * Outputs (in dist/release/, gitignored):
 *   1. quantum-computing-handbook.pdf
 *   2. quantum-computing-handbook.epub
 *   3. quantum-computing-handbook-<ver>-web.zip   (complete self-contained offline flagship site)
 *   4. quantum-computing-handbook-<ver>-codes.zip (self-authored stdlib suite + WAV audio, excl. vendor/)
 *   5. SHA256SUMS.txt                             (sorted SHA-256 manifest for the 4 release artifacts)
 */

import fs from 'node:fs/promises';
import fsSync from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const handbookDir = path.join(root, 'handbook');
const readerDir = path.join(root, 'reader');
const codesDir = path.join(root, 'codes');
const audioDir = path.join(handbookDir, 'assets/audio');
const distDir = path.join(root, 'dist');
const releaseDir = path.join(distDir, 'release');

const TEXT_EXTENSIONS = new Set([
  '.html', '.htm', '.xhtml', '.xml', '.svg', '.css', '.js', '.mjs', '.cjs',
  '.json', '.md', '.txt', '.py', '.csv', '.log', '.sh', '.yml', '.yaml', '.toml',
]);

function parseVersionArg(argv) {
  let version = 'v1.0.0';
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--version' && argv[i + 1]) {
      version = argv[++i];
    } else if (arg.startsWith('--version=')) {
      version = arg.slice('--version='.length);
    } else if (arg === '-h' || arg === '--help') {
      console.log('Usage: node tools/reader/build-release.mjs [--version v1.0.0]');
      process.exit(0);
    }
  }
  if (!/^v?[0-9A-Za-z._-]+$/.test(version) || version.includes('..')) {
    throw new Error(`Invalid --version value: ${version}`);
  }
  return version;
}

async function assertFileNonEmpty(absPath, hint = '') {
  let stat;
  try {
    stat = await fs.stat(absPath);
  } catch {
    throw new Error(`Required release input missing: ${path.relative(root, absPath)}${hint ? ` (${hint})` : ''}`);
  }
  if (!stat.isFile() || stat.size <= 0) {
    throw new Error(`Required release input is empty: ${path.relative(root, absPath)}${hint ? ` (${hint})` : ''}`);
  }
  return stat.size;
}

async function sha256File(absPath) {
  const buf = await fs.readFile(absPath);
  return crypto.createHash('sha256').update(buf).digest('hex');
}

function fmtMiB(bytes) {
  return `${(bytes / (1024 * 1024)).toFixed(2)} MiB`;
}

function escHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

async function copyTreeFiltered(srcDir, dstDir, shouldSkip) {
  await fs.mkdir(dstDir, { recursive: true });
  const entries = await fs.readdir(srcDir, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(srcDir, entry.name);
    const dstPath = path.join(dstDir, entry.name);
    if (shouldSkip(srcPath, entry)) continue;
    if (entry.isDirectory()) {
      await copyTreeFiltered(srcPath, dstPath, shouldSkip);
    } else if (entry.isFile()) {
      await fs.copyFile(srcPath, dstPath);
    }
  }
}

async function walkFiles(dir) {
  const out = [];
  const entries = await fs.readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      out.push(...(await walkFiles(full)));
    } else if (entry.isFile()) {
      out.push(full);
    }
  }
  return out.sort();
}

async function readEditionDate() {
  try {
    const readme = await fs.readFile(path.join(handbookDir, 'README.md'), 'utf8');
    return readme.match(/^>\s*版本：(\d{4}-\d{2}-\d{2})/m)?.[1] || 'unknown';
  } catch {
    return 'unknown';
  }
}

async function buildThirdPartySourcesText(version, edition) {
  const manifestPath = path.join(codesDir, 'vendor/manifest.json');
  const vendorReadmePath = path.join(codesDir, 'vendor/README.md');
  const licenseByProject = new Map();

  if (fsSync.existsSync(vendorReadmePath)) {
    const readmeTxt = await fs.readFile(vendorReadmePath, 'utf8');
    for (const line of readmeTxt.split('\n')) {
      const m = line.match(/^\|\s*\[([^\]]+)\]\([^)]+\)\s*\|[^|]+\|\s*([^|]+?)\s*\|/);
      if (m) licenseByProject.set(m[1].trim(), m[2].trim());
    }
  }

  let projects = [];
  let retrievedAt = 'unknown';
  if (fsSync.existsSync(manifestPath)) {
    const data = JSON.parse(await fs.readFile(manifestPath, 'utf8'));
    projects = Array.isArray(data.projects) ? data.projects : [];
    retrievedAt = data.extended_at_utc || data.retrieved_at_utc || 'unknown';
  }

  const lines = [
    `Quantum Computing Handbook (${version} / Edition ${edition})`,
    'THIRD-PARTY OPEN-SOURCE REFERENCES & ACQUISITION GUIDE',
    '========================================================================',
    '',
    'LICENSE BOUNDARY NOTICE (per repository AGENTS.md):',
    '  1. This standalone codes release archive intentionally EXCLUDES codes/vendor/',
    '     so third-party source excerpts are never redistributed outside their',
    '     original upstream license contexts or misapplied to this handbook.',
    '  2. Each upstream project below remains governed solely by its own license,',
    '     copyright headers, and NOTICE/AUTHORS files in its official repository.',
    '  3. Do NOT treat source excerpts as installable packages. For real SDK runs,',
    '     install official pinned releases or exact upstream commits in an isolated',
    '     Python/C++/Rust virtual environment following upstream documentation.',
    '',
    `Catalogued Upstream Projects: ${projects.length} (snapshot metadata: ${retrievedAt})`,
    'How to restore the full pinned vendor snapshot in a Git repository clone:',
    '  python3 codes/snapshot_sources.py --fetch',
    '  python3 codes/snapshot_sources.py --verify',
    '',
    '------------------------------------------------------------------------',
    'PROJECT INDEX (31 UPSTREAM REPOSITORIES)',
    '------------------------------------------------------------------------',
  ];

  projects.forEach((proj, idx) => {
    const num = String(idx + 1).padStart(2, '0');
    const lic = licenseByProject.get(proj.name) || 'See upstream LICENSE/NOTICE';
    const fileCount = Array.isArray(proj.files) ? proj.files.length : 0;
    lines.push(`${num}. ${proj.name}`);
    lines.push(`    Repository : ${proj.repository || 'N/A'}`);
    lines.push(`    Commit SHA : ${proj.commit || 'N/A'}`);
    lines.push(`    License    : ${lic}`);
    lines.push(`    Excerpts   : ${fileCount} pinned file(s) listed in codes/vendor/manifest.json`);
  });

  lines.push('');
  return lines.join('\n');
}

function buildOfflineDistGuideHtml({ version, edition, pdfBytes, pdfSha, epubBytes, epubSha }) {
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>离线电子书下载与本地打开指引 · 量子计算手册 ${escHtml(version)}</title>
  <style>
    :root { --bg: #FAF8F3; --card: #FFFFFF; --ink: #142622; --muted: #556661; --accent: #1E6B5A; --blue: #1F5A92; --rule: #D8D2C5; }
    * { box-sizing: border-box; }
    body { margin: 0; padding: 36px 20px; background: var(--bg); color: var(--ink); font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; line-height: 1.7; }
    main { max-width: 820px; margin: 0 auto; }
    .card { background: var(--card); border: 1px solid var(--rule); border-radius: 14px; padding: 24px 28px; margin-bottom: 18px; }
    h1 { margin: 0 0 8px; font-size: 1.7rem; }
    h2 { margin: 0 0 10px; font-size: 1.15rem; color: var(--accent); }
    .meta { color: var(--muted); font-size: 0.92rem; margin: 0 0 16px; }
    .links { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin-top: 12px; }
    a.btn { display: block; text-decoration: none; padding: 14px 16px; border-radius: 10px; border: 1.5px solid var(--rule); color: var(--ink); background: #FAF8F3; }
    a.btn:hover { border-color: var(--accent); }
    a.btn strong { display: block; font-size: 1rem; color: var(--blue); margin-bottom: 4px; }
    a.btn span { display: block; font-size: 0.85rem; color: var(--muted); }
    code { font-family: Menlo, Consolas, monospace; font-size: 0.84rem; background: #F1EDE4; padding: 2px 6px; border-radius: 4px; word-break: break-all; }
    ol { margin: 8px 0 0; padding-left: 1.35rem; }
    li { margin: 6px 0; }
  </style>
</head>
<body>
  <main>
    <div class="card">
      <h1>离线电子书与阅读版快捷入口</h1>
      <p class="meta">量子计算手册 · 发布版本 ${escHtml(version)} · 内容版本 ${escHtml(edition)} · 全包 100% 离线可用</p>
      <div class="links">
        <a class="btn" href="../index.html">
          <strong>打开离线旗舰阅读首页</strong>
          <span>26 章 + 7 附录 + 7 实验册 + 全文离线搜索 + 5 段声化音频</span>
        </a>
        <a class="btn" href="../lab/quantum-lab.html">
          <strong>打开六模块量子互动实验台</strong>
          <span>纯前端零外网交互仿真（Bloch / 干涉 / 门线路 / 纠错等）</span>
        </a>
        <a class="btn" href="quantum-computing-handbook.pdf">
          <strong>A4 印刷级 PDF 快捷入口</strong>
          <span>quantum-computing-handbook.pdf · ${escHtml(fmtMiB(pdfBytes))}</span>
        </a>
        <a class="btn" href="quantum-computing-handbook.epub">
          <strong>原生 MathML 3 EPUB 3 快捷入口</strong>
          <span>quantum-computing-handbook.epub · ${escHtml(fmtMiB(epubBytes))}</span>
        </a>
      </div>
    </div>
    <div class="card">
      <h2>离线电子书本地放置与校验说明</h2>
      <ol>
        <li>本压缩包为完整自包含离线网站版，无需联网，解压后直接双击根目录 <code>index.html</code> 即可完整阅读、检索、听音频并运行交互实验台。</li>
        <li>为避免重复占用下载流量，PDF 与 EPUB 电子书作为同版本 GitHub Release 的独立文件发布。下载后将 <code>quantum-computing-handbook.pdf</code> 与 <code>quantum-computing-handbook.epub</code> 放入本 <code>dist/</code> 目录，上方快捷入口即可直接离线打开。</li>
        <li>官方 SHA-256 校验摘要：
          <br/>PDF：<code>${escHtml(pdfSha)}</code>
          <br/>EPUB：<code>${escHtml(epubSha)}</code>
        </li>
      </ol>
    </div>
  </main>
</body>
</html>
`;
}

async function auditStagedTree(stageRoot, label, { forbidVendor = false } = {}) {
  const files = await walkFiles(stageRoot);
  const violations = [];

  for (const abs of files) {
    const rel = path.relative(stageRoot, abs).replaceAll('\\', '/');
    const base = path.basename(abs);
    if (base === 'STYLE.html' || /(^|\/)STYLE\.html$/i.test(rel)) {
      violations.push(`[${label}] Forbidden STYLE.html present: ${rel}`);
    }
    if (/(^|\/)research(\/|$)/.test(rel)) {
      violations.push(`[${label}] Forbidden research/ artifact present: ${rel}`);
    }
    if (/(^|\/)__pycache__(\/|$)/.test(rel) || base.endsWith('.pyc')) {
      violations.push(`[${label}] Forbidden Python cache present: ${rel}`);
    }
    if (forbidVendor && /(^|\/)codes\/vendor(\/|$)/.test(rel)) {
      violations.push(`[${label}] Forbidden codes/vendor/ present: ${rel}`);
    }

    const ext = path.extname(abs).toLowerCase();
    if (TEXT_EXTENSIONS.has(ext)) {
      const content = await fs.readFile(abs, 'utf8');
      if (content.includes('/Users/')) {
        violations.push(`[${label}] Local /Users/ path leak in: ${rel}`);
      }
      if (label === 'web' && (ext === '.html' || ext === '.htm')) {
        if (/href=["'][^"']*STYLE\.html/i.test(content)) {
          violations.push(`[${label}] Broken link to STYLE.html in: ${rel}`);
        }
        if (/href=["'](?:\.\.\/)*research\//i.test(content)) {
          violations.push(`[${label}] Link to excluded research/ in: ${rel}`);
        }
      }
    }
  }

  if (violations.length) {
    throw new Error(
      `Release staging audit FAILED (${violations.length} violation(s)):\n  - ` +
      violations.slice(0, 25).join('\n  - ')
    );
  }
  return files.length;
}

function zipMaxCompression(cwd, folderName, outZipPath) {
  execFileSync('zip', ['-9', '-r', '-q', outZipPath, folderName], { cwd, stdio: 'inherit' });
}

function verifyZipIntegrity(zipPath, { forbidVendor = false } = {}) {
  execFileSync('unzip', ['-t', '-qq', zipPath], { stdio: 'inherit' });
  const entries = execFileSync('unzip', ['-Z1', zipPath], { encoding: 'utf8' })
    .split('\n')
    .map(s => s.trim())
    .filter(Boolean);
  for (const entry of entries) {
    if (/(^|\/)STYLE\.html$/i.test(entry)) {
      throw new Error(`ZIP ${path.basename(zipPath)} contains forbidden STYLE.html: ${entry}`);
    }
    if (/(^|\/)research(\/|$)/.test(entry)) {
      throw new Error(`ZIP ${path.basename(zipPath)} contains forbidden research/: ${entry}`);
    }
    if (/(^|\/)__pycache__(\/|$)/.test(entry)) {
      throw new Error(`ZIP ${path.basename(zipPath)} contains forbidden __pycache__/: ${entry}`);
    }
    if (forbidVendor && /(^|\/)codes\/vendor(\/|$)/.test(entry)) {
      throw new Error(`ZIP ${path.basename(zipPath)} contains forbidden codes/vendor/: ${entry}`);
    }
  }
  return entries.length;
}

async function main() {
  const version = parseVersionArg(process.argv.slice(2));
  const edition = await readEditionDate();

  // 1. Precondition assertions (all required inputs must exist and be non-empty)
  const pdfSrc = path.join(distDir, 'quantum-computing-handbook.pdf');
  const epubSrc = path.join(distDir, 'quantum-computing-handbook.epub');
  await assertFileNonEmpty(path.join(readerDir, 'index.html'), 'run make build');
  await assertFileNonEmpty(path.join(readerDir, 'lab/quantum-lab.html'), 'run make build');
  await assertFileNonEmpty(path.join(readerDir, 'assets/search-index.js'), 'run make build');
  const pdfSrcBytes = await assertFileNonEmpty(pdfSrc, 'run make pdf');
  const epubSrcBytes = await assertFileNonEmpty(epubSrc, 'run make epub');
  await assertFileNonEmpty(path.join(codesDir, 'run_all.py'));
  await assertFileNonEmpty(path.join(codesDir, 'README.md'));
  await assertFileNonEmpty(path.join(audioDir, 'manifest.json'));

  const [pdfSrcSha, epubSrcSha] = await Promise.all([sha256File(pdfSrc), sha256File(epubSrc)]);

  await fs.rm(releaseDir, { recursive: true, force: true });
  await fs.mkdir(releaseDir, { recursive: true });

  const stageDir = await fs.mkdtemp(path.join(os.tmpdir(), 'qch-release-'));
  try {
    // 2. Artifact 1 & 2: Copy PDF and EPUB and verify exact byte count + SHA-256
    const pdfName = 'quantum-computing-handbook.pdf';
    const epubName = 'quantum-computing-handbook.epub';
    const pdfDst = path.join(releaseDir, pdfName);
    const epubDst = path.join(releaseDir, epubName);
    await Promise.all([fs.copyFile(pdfSrc, pdfDst), fs.copyFile(epubSrc, epubDst)]);

    const [pdfDstBytes, epubDstBytes, pdfDstSha, epubDstSha] = await Promise.all([
      assertFileNonEmpty(pdfDst),
      assertFileNonEmpty(epubDst),
      sha256File(pdfDst),
      sha256File(epubDst),
    ]);
    if (pdfDstBytes !== pdfSrcBytes || pdfDstSha !== pdfSrcSha) {
      throw new Error('Copied PDF byte/SHA-256 verification failed');
    }
    if (epubDstBytes !== epubSrcBytes || epubDstSha !== epubSrcSha) {
      throw new Error('Copied EPUB byte/SHA-256 verification failed');
    }

    // 3. Artifact 3: Complete self-contained offline flagship website ZIP
    const webFolder = `quantum-computing-handbook-${version}-web`;
    const webZipName = `${webFolder}.zip`;
    const webStage = path.join(stageDir, webFolder);
    await copyTreeFiltered(readerDir, webStage, (_srcPath, entry) => {
      if (entry.name === '.DS_Store' || entry.name === '__pycache__' || entry.name.endsWith('.pyc')) return true;
      if (entry.isDirectory() && entry.name === 'work') return true;
      return false;
    });

    const webDistDir = path.join(webStage, 'dist');
    await fs.mkdir(webDistDir, { recursive: true });
    await fs.writeFile(
      path.join(webDistDir, 'index.html'),
      buildOfflineDistGuideHtml({
        version,
        edition,
        pdfBytes: pdfSrcBytes,
        pdfSha: pdfSrcSha,
        epubBytes: epubSrcBytes,
        epubSha: epubSrcSha,
      }),
      'utf8'
    );
    await fs.writeFile(
      path.join(webDistDir, 'README.txt'),
      [
        `Quantum Computing Handbook ${version} (Edition ${edition}) — Offline eBook Quick Guide`,
        '',
        '1. Double-click ../index.html to browse the full offline flagship site immediately.',
        '2. Double-click ../lab/quantum-lab.html to open the 6-module interactive lab offline.',
        '3. Download quantum-computing-handbook.pdf and quantum-computing-handbook.epub from',
        `   GitHub Release ${version} into this dist/ directory for 1-click offline opening.`,
        '',
        `SHA-256 (PDF) : ${pdfSrcSha}  quantum-computing-handbook.pdf`,
        `SHA-256 (EPUB): ${epubSrcSha}  quantum-computing-handbook.epub`,
        '',
      ].join('\n'),
      'utf8'
    );

    const webFileCount = await auditStagedTree(webStage, 'web');
    const webZipPath = path.join(releaseDir, webZipName);
    zipMaxCompression(stageDir, webFolder, webZipPath);
    const webZipEntries = verifyZipIntegrity(webZipPath);

    // 4. Artifact 4: Complete self-authored offline Python verification suite ZIP (excl. codes/vendor & __pycache__)
    const codesFolder = `quantum-computing-handbook-${version}-codes`;
    const codesZipName = `${codesFolder}.zip`;
    const codesStage = path.join(stageDir, codesFolder);
    const vendorAbs = path.join(codesDir, 'vendor');

    await copyTreeFiltered(codesDir, path.join(codesStage, 'codes'), (srcPath, entry) => {
      if (srcPath === vendorAbs || srcPath.startsWith(vendorAbs + path.sep)) return true;
      if (entry.name === '.DS_Store' || entry.name === '__pycache__' || entry.name.endsWith('.pyc') || entry.name.endsWith('.pyo')) return true;
      return false;
    });
    await copyTreeFiltered(audioDir, path.join(codesStage, 'handbook/assets/audio'), (_srcPath, entry) => entry.name === '.DS_Store');

    const rootLicense = path.join(root, 'LICENSE');
    if (fsSync.existsSync(rootLicense)) {
      await fs.copyFile(rootLicense, path.join(codesStage, 'LICENSE'));
    }

    const thirdPartyText = await buildThirdPartySourcesText(version, edition);
    await fs.writeFile(path.join(codesStage, 'THIRD-PARTY-SOURCES.txt'), thirdPartyText, 'utf8');
    await fs.writeFile(
      path.join(codesStage, 'README-RELEASE.txt'),
      [
        `Quantum Computing Handbook ${version} (Edition ${edition}) — Offline Self-Authored Codes Suite`,
        '',
        'Included:',
        '  - codes/                  All self-authored Python stdlib verification scripts, JSON baselines & docs',
        '  - handbook/assets/audio/  All 5 synthesized WAV audio demonstrations + manifest.json',
        '  - THIRD-PARTY-SOURCES.txt Index of all 31 upstream open-source repositories, commits & license notices',
        '',
        'Excluded intentionally (license boundary):',
        '  - codes/vendor/           Excluded from standalone release zips; see THIRD-PARTY-SOURCES.txt.',
        '  - __pycache__/            Excluded build caches.',
        '',
        'Quick start (Python 3.9+, stdlib only, zero paid APIs):',
        '  python3 codes/foundations/foundations_lab.py --case all',
        '  python3 codes/algorithms/experiments.py all',
        '  python3 codes/systems/sensing_lab.py',
        '  python3 codes/algorithms/v4_algorithms_lab.py all',
        '  python3 codes/practice/v4_practice_lab.py',
        '',
      ].join('\n'),
      'utf8'
    );

    const codesFileCount = await auditStagedTree(codesStage, 'codes', { forbidVendor: true });
    const codesZipPath = path.join(releaseDir, codesZipName);
    zipMaxCompression(stageDir, codesFolder, codesZipPath);
    const codesZipEntries = verifyZipIntegrity(codesZipPath, { forbidVendor: true });

    // 5. Artifact 5: SHA256SUMS.txt (sorted by filename)
    const artifactNames = [pdfName, epubName, webZipName, codesZipName].sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
    const records = [];
    for (const name of artifactNames) {
      const fullPath = path.join(releaseDir, name);
      const bytes = await assertFileNonEmpty(fullPath);
      const sha256 = await sha256File(fullPath);
      records.push({ name, bytes, sha256 });
    }
    const sumsContent = records.map(r => `${r.sha256}  ${r.name}`).join('\n') + '\n';
    const sumsPath = path.join(releaseDir, 'SHA256SUMS.txt');
    await fs.writeFile(sumsPath, sumsContent, 'utf8');

    // Final cross-check of SHA256SUMS.txt
    const parsedSums = (await fs.readFile(sumsPath, 'utf8')).trim().split('\n');
    if (parsedSums.length !== records.length) {
      throw new Error('SHA256SUMS.txt line count mismatch');
    }

    console.log(`\n[build-release] PASS — Quantum Computing Handbook ${version} (edition ${edition})`);
    console.log(`[build-release] Audited: web (${webFileCount} files, ${webZipEntries} ZIP entries) | codes (${codesFileCount} files, ${codesZipEntries} ZIP entries)`);
    console.log('[build-release] Checks : 0 /Users/ leaks · 0 STYLE.html · 0 reader/research/ · 0 vendor/ in codes.zip · unzip -t PASS\n');
    console.log('Release Artifacts (dist/release/):');
    for (const r of records) {
      console.log(`  ${r.name.padEnd(48)} ${fmtMiB(r.bytes).padStart(10)}  ${r.sha256}`);
    }
    const sumsBytes = await assertFileNonEmpty(sumsPath);
    console.log(`  ${'SHA256SUMS.txt'.padEnd(48)} ${(sumsBytes + ' B').padStart(10)}  (${records.length} entries)\n`);
  } finally {
    await fs.rm(stageDir, { recursive: true, force: true }).catch(() => {});
  }
}

main().catch(err => {
  console.error('[build-release] FAILED:', err.message || err);
  process.exitCode = 1;
});
