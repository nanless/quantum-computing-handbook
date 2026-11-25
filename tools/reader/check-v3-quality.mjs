import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import { readingGroups, readingPlan } from './reading-order.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const handbookDir = path.join(root, 'handbook');
const assetsDir = path.join(handbookDir, 'assets');
const exercisesPath = path.join(handbookDir, 'appendices/exercises.md');

const EXPECTED_TOTAL_EXERCISES = 271;
const HISTORICAL_TERMINOLOGY_EXEMPT = new Set(['handbook/appendices/audit-log.md']);

async function walk(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const nested = await Promise.all(
    entries.map(e => (e.isDirectory() ? walk(path.join(dir, e.name)) : path.join(dir, e.name))),
  );
  return nested.flat();
}

// Replace fenced code blocks and inline code with same-line-count spaces so line numbers stay exact.
function maskCodePreserveLines(text) {
  const pattern = /(^[ \t]*(`{3,}|~{3,})[^\n]*\n[\s\S]*?^[ \t]*\2[ \t]*$)|(`+)[^\n]*?\3/gm;
  return text.replace(pattern, full => full.replace(/[^\n]/g, ' '));
}

function lineNumberAt(text, index) {
  let line = 1;
  for (let i = 0; i < index; i++) if (text.charCodeAt(i) === 10) line++;
  return line;
}

function excerptAround(text, index, len = 48) {
  const lineStart = text.lastIndexOf('\n', index) + 1;
  let lineEnd = text.indexOf('\n', index);
  if (lineEnd === -1) lineEnd = text.length;
  const line = text.slice(lineStart, lineEnd).trim();
  return line.length > len * 2 ? line.slice(Math.max(0, index - lineStart - len), index - lineStart + len) : line;
}

function chapterIdFromFile(filePath) {
  const rel = path.relative(handbookDir, filePath).replaceAll('\\', '/');
  const qm = rel.match(/^quantum-mechanics\/0(\d)-/);
  if (qm) return `Q${qm[1]}`;
  const main = rel.match(/^(\d\d)-/);
  if (main) return main[1];
  return null;
}

function countOrderedListItems(markdownSlice) {
  if (!markdownSlice || !markdownSlice.trim()) return 0;
  // Shield display math blocks so `---` or blank lines inside math never split tokens.
  const shielded = markdownSlice.replace(/\$\$[\s\S]*?\$\$/g, ' MATHBLOCK ');
  const tokens = marked.lexer(shielded, { gfm: true });
  let total = 0;
  for (const token of tokens) {
    if (token.type === 'list' && token.ordered) {
      total += token.items.length;
    }
  }
  return total;
}

function extractSelfCheckSlice(chapterText) {
  const match = chapterText.match(/^##\s*自检题[^\n]*(?:\r?\n|$)/m);
  if (!match) return null;
  const start = match.index + match[0].length;
  const rest = chapterText.slice(start);
  const nextH2 = rest.search(/^##\s/m);
  return nextH2 === -1 ? rest : rest.slice(0, nextH2);
}

function parseExercisesByChapter(exercisesText) {
  const map = new Map();
  const sections = exercisesText.split(/^(?=##\s)/m);
  for (const sec of sections) {
    const firstNewline = sec.indexOf('\n');
    const heading = (firstNewline === -1 ? sec : sec.slice(0, firstNewline)).trim();
    const body = firstNewline === -1 ? '' : sec.slice(firstNewline + 1);
    let key = null;
    const mMain = heading.match(/^##\s*第\s*(\d+)\s*章(?:\s*[｜|].*)?$/);
    const mQm = heading.match(/^##\s*(?:量子力学|物理篇)\s*Q(\d+)(?:\s*[｜|].*)?$/);
    if (mMain) key = String(Number(mMain[1])).padStart(2, '0');
    else if (mQm) key = `Q${Number(mQm[1])}`;
    if (key) {
      map.set(key, {
        heading,
        count: countOrderedListItems(body),
      });
    }
  }
  return map;
}

async function main() {
  const allMd = (await walk(handbookDir)).filter(f => f.endsWith('.md')).sort();
  const chapterFiles = allMd.filter(f => /^\d\d-/.test(path.basename(f)));
  const plan = readingPlan(chapterFiles);
  const orderedIds = readingGroups.flatMap(([, ids]) => ids);

  // Target prose files: 26 chapters + READMEs + appendices/ + labs/
  const scanFiles = allMd.filter(f => {
    const rel = path.relative(handbookDir, f).replaceAll('\\', '/');
    return rel !== 'STYLE.md';
  });

  const gate1LatexDelims = [];
  const gate2BannedTerms = [];
  const gate3DecodeTerm = [];
  const historicalTerminologyNotes = [];

  const bannedPattern = /参数偏移|玩具模型|左线性/g;
  const decodePattern = /译码/g;
  // Match single-backslash \(, \), \[, \] (not double-backslash \\[4pt] matrix linebreaks).
  const latexDelimPattern = /(?<!\\)\\(?:[()[\]])/g;

  for (const file of scanFiles) {
    const rel = path.relative(root, file).replaceAll('\\', '/');
    const raw = await fs.readFile(file, 'utf8');
    const masked = maskCodePreserveLines(raw);
    const isHistorical = HISTORICAL_TERMINOLOGY_EXEMPT.has(rel);

    // Gate 1: Zero \(...\) or \[...\] in prose (code excluded).
    for (const m of masked.matchAll(latexDelimPattern)) {
      const idx = m.index;
      // Ignore Markdown escaped brackets like \[1\] only if not part of math? No, standard prose shouldn't use \[ or \(.
      gate1LatexDelims.push({
        file: rel,
        line: lineNumberAt(raw, idx),
        token: m[0],
        excerpt: excerptAround(raw, idx),
      });
    }

    // Gate 2: Zero 参数偏移 / 玩具模型 / 左线性
    for (const m of masked.matchAll(bannedPattern)) {
      const hit = {
        file: rel,
        line: lineNumberAt(raw, m.index),
        term: m[0],
        excerpt: excerptAround(raw, m.index),
      };
      if (isHistorical) historicalTerminologyNotes.push({ gate: 'bannedTerms', ...hit });
      else gate2BannedTerms.push(hit);
    }

    // Gate 3: Zero 译码 (allow only 亦称译码 / 旧称译码 / vendor 原始引用)
    for (const m of masked.matchAll(decodePattern)) {
      const idx = m.index;
      const before = raw.slice(Math.max(0, idx - 6), idx);
      const lineStart = raw.lastIndexOf('\n', idx) + 1;
      let lineEnd = raw.indexOf('\n', idx);
      if (lineEnd === -1) lineEnd = raw.length;
      const fullLine = raw.slice(lineStart, lineEnd);

      const allowedAlias = /(?:亦称|旧称)[“"「（(]?$/.test(before);
      const allowedVendor = /\bvendor\b|codes\/vendor/i.test(fullLine);
      if (allowedAlias || allowedVendor) continue;

      const hit = {
        file: rel,
        line: lineNumberAt(raw, idx),
        excerpt: excerptAround(raw, idx),
      };
      if (isHistorical) historicalTerminologyNotes.push({ gate: 'decodeTerm', ...hit });
      else gate3DecodeTerm.push(hit);
    }
  }

  // Gate 4: Every handbook/assets/*.svg must contain at least one <text> node.
  const svgFiles = (await fs.readdir(assetsDir)).filter(f => f.endsWith('.svg')).sort();
  const svgFailures = [];
  for (const name of svgFiles) {
    const svgText = await fs.readFile(path.join(assetsDir, name), 'utf8');
    const textCount = (svgText.match(/<text\b/g) || []).length;
    if (textCount === 0) {
      svgFailures.push({ file: `handbook/assets/${name}`, textCount });
    }
  }

  // Gate 5: All 26 chapters' ## 自检题 item counts match exercises.md top-level <li> counts.
  const exercisesRaw = await fs.readFile(exercisesPath, 'utf8');
  const exercisesMap = parseExercisesByChapter(exercisesRaw);
  const exerciseChecks = [];
  const exerciseMismatches = [];
  let totalChapterQuestions = 0;
  let totalExerciseAnswers = 0;

  const fileById = new Map(plan.sequence.map(f => [chapterIdFromFile(f), f]));
  for (const id of orderedIds) {
    const file = fileById.get(id);
    const rel = file ? path.relative(root, file).replaceAll('\\', '/') : null;
    const raw = file ? await fs.readFile(file, 'utf8') : '';
    const slice = extractSelfCheckSlice(raw);
    const chapterCount = slice === null ? 0 : countOrderedListItems(slice);
    const exEntry = exercisesMap.get(id);
    const exerciseCount = exEntry ? exEntry.count : 0;

    totalChapterQuestions += chapterCount;
    totalExerciseAnswers += exerciseCount;

    const ok = slice !== null && chapterCount > 0 && chapterCount === exerciseCount;
    const row = {
      chapter: id,
      file: rel,
      hasSelfCheckHeading: slice !== null,
      chapterQuestions: chapterCount,
      exerciseAnswers: exerciseCount,
      ok,
    };
    exerciseChecks.push(row);
    if (!ok) exerciseMismatches.push(row);
  }

  const totalMatchesExpected =
    totalChapterQuestions === EXPECTED_TOTAL_EXERCISES &&
    totalExerciseAnswers === EXPECTED_TOTAL_EXERCISES;

  const summary = {
    generatedAt: new Date().toISOString(),
    scannedMarkdownFiles: scanFiles.length,
    scannedSvgFiles: svgFiles.length,
    excludedHistoricalForTerminology: [...HISTORICAL_TERMINOLOGY_EXEMPT],
    gates: {
      gate1LatexDelimiters: {
        passed: gate1LatexDelims.length === 0,
        count: gate1LatexDelims.length,
        violations: gate1LatexDelims.slice(0, 50),
      },
      gate2BannedTerms: {
        passed: gate2BannedTerms.length === 0,
        count: gate2BannedTerms.length,
        violations: gate2BannedTerms.slice(0, 50),
      },
      gate3DecodeTerminology: {
        passed: gate3DecodeTerm.length === 0,
        count: gate3DecodeTerm.length,
        violations: gate3DecodeTerm.slice(0, 50),
      },
      gate4SvgTextNodes: {
        passed: svgFailures.length === 0,
        totalSvgs: svgFiles.length,
        zeroTextCount: svgFailures.length,
        failures: svgFailures,
      },
      gate5ExerciseAlignment: {
        passed: exerciseMismatches.length === 0 && totalMatchesExpected,
        chapterCount: orderedIds.length,
        expectedTotal: EXPECTED_TOTAL_EXERCISES,
        totalChapterQuestions,
        totalExerciseAnswers,
        totalMatchesExpected,
        mismatchCount: exerciseMismatches.length,
        mismatches: exerciseMismatches,
        perChapter: exerciseChecks,
      },
    },
    historicalTerminologyNotesCount: historicalTerminologyNotes.length,
  };

  const allPassed = Object.values(summary.gates).every(g => g.passed);
  summary.passed = allPassed;

  console.log(JSON.stringify(summary, null, 2));
  if (!allPassed) process.exitCode = 1;
}

await main();
