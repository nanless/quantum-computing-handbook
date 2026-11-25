import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { marked } from 'marked';

export const expectedExerciseCount = 271;
const marker = /<!-- exercise-id: (\d{2}-\d{2}|Q[1-4]-\d{2}) -->/g;
const answerSteps = ['题意与约定', '核心提示', '完整分步演算', '结论与边界回验', '易错坑提醒'];
const answerStepPattern = /^(?:\*\*|__)?([^：:\n*]+?)(?:\*\*|__)?[ \t]*[：:]/;
const fingerprintParts = ['标题', '核心提示', '解题正文'];

export function exerciseChapterId(title) {
  const main = title.match(/^第\s*(\d+)\s*章(?:\s*[｜|：:].*)?$/);
  if (main) return String(Number(main[1])).padStart(2, '0');
  const qm = title.match(/^(?:量子力学(?:基础)?|物理(?:基础)?篇?)\s*Q(\d+)(?:\s*[｜|：:].*)?$/);
  return qm ? `Q${Number(qm[1])}` : null;
}

export function exerciseIdOf(item) {
  const matches = [...item.text.matchAll(marker)];
  const firstLine = item.text.split('\n', 1)[0];
  return matches.length === 1 && firstLine.endsWith(matches[0][0]) ? matches[0][1] : null;
}

function sourceSections(text) {
  return marked.lexer(text, { gfm: true }).reduce((sections, token) => {
    if (token.type === 'heading' && token.depth === 2) {
      sections.push({ title: token.text, items: [], text: '' });
    } else if (sections.length) {
      const section = sections.at(-1);
      section.text += token.raw;
      if (token.type === 'list' && token.ordered) section.items.push(...token.items);
    }
    return sections;
  }, []);
}

function answerParts(item) {
  const steps = item.tokens.flatMap(token => token.type === 'list' && !token.ordered ? token.items : []);
  const titles = steps.map(step => step.text.match(answerStepPattern)?.[1]);
  const title = item.text.split('\n', 1)[0].replace(marker, '').trim();
  return {
    valid: /^\*\*【(?:基础|计算|进阶)】.+\*\*$/.test(title)
      && steps.length === answerSteps.length
      && answerSteps.every((step, index) => step === titles[index]),
    content: [title, steps[1]?.text, steps.filter((_, index) => index !== 1).map(step => step.text).join('\n')],
  };
}

function fingerprint(value) {
  return createHash('sha256').update((value || '').replace(/\s+/gu, ' ').trim()).digest('hex').slice(0, 24);
}

function buildFingerprintIndex(baseline) {
  const index = fingerprintParts.map(() => new Map());
  for (const [id, parts] of Object.entries(baseline)) {
    for (const [part, digest] of parts.entries()) {
      const owners = index[part].get(digest) || new Set();
      owners.add(id);
      index[part].set(digest, owners);
    }
  }
  return index;
}

// The audited original is used as a cross-check, not a content lock. An ordinary revision may add new wording.
// A known title, hint or body copied to the wrong identity still fails if the author left the comment in place.
export function verifyExerciseAlignment(chapters, appendixText, {
  expectedTotal = expectedExerciseCount,
  baseline = JSON.parse(readFileSync(new URL('./exercise-answer-fingerprints.json', import.meta.url), 'utf8')),
} = {}) {
  const sections = new Map();
  const errors = [];
  for (const section of sourceSections(appendixText)) {
    const id = exerciseChapterId(section.title);
    if (!id) continue;
    if (sections.has(id)) errors.push({ chapter: id, message: '附录章节重复' });
    sections.set(id, section);
  }

  const baselineOwners = buildFingerprintIndex(baseline);
  const fingerprints = {};
  const perChapter = [];
  const knownChapters = new Set();
  let totalChapterQuestions = 0;
  let totalExerciseAnswers = 0;
  for (const { id, file, text } of chapters) {
    knownChapters.add(id);
    const section = sourceSections(text).find(({ title }) => /^自检题(?:\s|$)/.test(title));
    const questions = section?.items || [];
    const answers = sections.get(id)?.items || [];
    totalChapterQuestions += questions.length;
    totalExerciseAnswers += answers.length;
    const before = errors.length;
    if (!questions.length || questions.length !== answers.length) {
      errors.push({ chapter: id, message: `题面 ${questions.length} 与解答 ${answers.length} 未能逐题对应` });
    }

    const [questionIds, answerIds] = [questions, answers].map((items, side) => items.map((item, index) => {
      const number = index + 1;
      const expectedId = `${id}-${String(number).padStart(2, '0')}`;
      const actualNumber = Number(item.raw.match(/^[ \t]*(\d+)[.)][ \t]+/)?.[1]);
      const actualId = exerciseIdOf(item);
      const location = side === 0 ? '题面' : '附录答案';
      if (actualNumber !== number || actualId !== expectedId) {
        errors.push({ chapter: id, question: number, message: `${location}需使用原题号 ${number} 和身份 ${expectedId}，读到 ${Number.isFinite(actualNumber) ? actualNumber : '无题号'} / ${actualId || '无有效身份'}` });
      }
      if (side !== 0) {
        const { valid, content } = answerParts(item);
        if (!valid) errors.push({ chapter: id, question: number, message: '答案缺少难度、核心提示或原有四步结构' });
        const digests = content.map(fingerprint);
        fingerprints[expectedId] = digests;
        for (const [part, digest] of digests.entries()) {
          const owners = baselineOwners[part].get(digest);
          if (owners && !owners.has(expectedId)) {
            errors.push({ chapter: id, question: number, message: `${fingerprintParts[part]}与其他题的已核对内容一致，原身份 ${[...owners].join('、')}` });
          }
        }
      }
      return actualId;
    }));
    perChapter.push({
      chapter: id,
      file,
      hasSelfCheckHeading: Boolean(section),
      chapterQuestions: questions.length,
      exerciseAnswers: answers.length,
      questionIds,
      answerIds,
      ok: before === errors.length,
    });
  }

  for (const id of sections.keys()) {
    if (!knownChapters.has(id)) errors.push({ chapter: id, message: '附录有无对应题面的章节' });
  }
  for (const id of Object.keys(baseline)) {
    if (!(id in fingerprints)) errors.push({ chapter: id, message: '原有题号或解答缺失' });
  }
  const totalMatchesExpected = totalChapterQuestions === expectedTotal && totalExerciseAnswers === expectedTotal;
  return {
    passed: errors.length === 0 && totalMatchesExpected,
    chapterCount: chapters.length,
    expectedTotal,
    totalChapterQuestions,
    totalExerciseAnswers,
    totalMatchesExpected,
    mismatchCount: errors.length,
    mismatches: errors,
    perChapter,
    appendixByChapter: new Map([...sections].map(([id, section]) => [id, section.text])),
    fingerprints,
  };
}

export function requireExerciseAlignment(result) {
  if (!result.passed) {
    const details = result.mismatches.slice(0, 6)
      .map(({ chapter, question, message }) => `${chapter}${question ? ` 第 ${question} 题` : ''} ${message}`);
    throw new Error(`题答核对失败（题面 ${result.totalChapterQuestions}、答案 ${result.totalExerciseAnswers}、预期 ${result.expectedTotal}）\n${details.join('\n')}`);
  }
}
