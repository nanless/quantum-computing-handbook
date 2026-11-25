import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import test from 'node:test';
import { marked } from 'marked';
import { splitExercisesByPart } from './exercise-ebook.mjs';
import { exerciseChapterId } from './exercise-identity.mjs';
import { readingPlan } from './reading-order.mjs';

const handbook = new URL('../../handbook/', import.meta.url);
const relativeChapters = async directory => (await readdir(new URL(directory || '.', handbook)))
  .filter(file => /^\d\d-.+\.md$/.test(file))
  .map(file => directory + file);
const entries = [...await relativeChapters(''), ...await relativeChapters('quantum-mechanics/')];
const plan = readingPlan(entries.toReversed());
const appendix = await readFile(new URL('appendices/exercises.md', handbook), 'utf8');
const order = plan.groups.flatMap(group => group.ids);
const chapterRow = /\]\((?:\.\.\/)?((?:quantum-mechanics\/)?\d\d-[^\s)]+\.md)\)/;
const answerIds = markdown => marked.lexer(markdown, { gfm: true })
  .filter(token => token.type === 'heading' && token.depth === 2)
  .map(token => exerciseChapterId(token.text))
  .filter(Boolean);

test('六篇 26 章的编排不受输入顺序影响，拒绝缺章或互相覆盖', () => {
  assert.deepEqual(plan.groups.map(group => group.ids.join(' ')), [
    '00 01 02 03 04 05', 'Q1 Q2 Q3 Q4', '06 07 08 15', '09 10 11 14 19', '13 12 18 20', '16 17 21',
  ]);
  assert.deepEqual(readingPlan(entries).sequence, plan.sequence);
  assert.deepEqual(readingPlan(entries.map(file => file.replace('/', '\\'))).sequence.map(file => file.replace('\\', '/')), plan.sequence);
  assert.throws(() => readingPlan(entries.slice(1)), /needs chapter 00/);
  assert.throws(() => readingPlan([...entries, entries[0]]), /two files for 00/);
});

test('Markdown 主目录中的篇名、章节路径与每章阅读位置完全一致', async () => {
  const handbookReadme = await readFile(new URL('README.md', handbook), 'utf8');
  const actual = [];
  let current;
  for (const line of handbookReadme.split('\n')) {
    if (line.startsWith('### ')) {
      current = /^### 第.+篇\s+·\s+(.+)$/.test(line) ? { label: line.slice(4), files: [], positions: [] } : null;
      if (current) actual.push(current);
    }
    const chapter = line.startsWith('|') && line.match(chapterRow);
    if (current && chapter) {
      current.files.push(chapter[1]);
      current.positions.push(Number(line.split('|')[1].trim()));
    }
  }
  let position = 0;
  assert.deepEqual(actual, plan.groups.map(group => ({
    label: group.label, files: group.files, positions: group.files.map(() => ++position),
  })));
});

test('题答速查表与解答正文按同一章序，保留所有原章号', () => {
  const quickIndex = appendix.split('\n').filter(line => line.startsWith('|'))
    .map(line => line.match(chapterRow)?.[1]).filter(Boolean);
  assert.deepEqual(quickIndex, plan.sequence);
  assert.deepEqual(answerIds(appendix), order);
});

test('EPUB 题答按六篇分组并保留首册速查与末册扩展索引', () => {
  const parts = splitExercisesByPart(appendix, plan.groups);
  assert.deepEqual(parts.map(part => part.xname), plan.groups.map(group => `app-exercises-p${group.number}.xhtml`));
  assert.deepEqual(parts.map(part => answerIds(part.markdown)), plan.groups.map(group => group.ids));
  assert.match(parts[0].markdown, /^## .+自检题速查与难度分布目录$/m);
  assert.match(parts.at(-1).markdown, /^## 配套实验册与进阶练习索引$/m);
  assert.ok(parts.slice(1).every(part => !/^## .+自检题速查与难度分布目录$/m.test(part.markdown)));
});
