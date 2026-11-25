import assert from 'node:assert/strict';
import test from 'node:test';
import { requireExerciseAlignment, verifyExerciseAlignment } from './exercise-identity.mjs';

const chapters = [{
  id: '00',
  file: '00-overview.md',
  text: '## 自检题\n\n1. 题甲 <!-- exercise-id: 00-01 -->\n2. 题乙 <!-- exercise-id: 00-02 -->\n',
}];

const answer = (number, tag, example) => `${number}. **【基础】标题${example}** <!-- exercise-id: ${tag} -->

   - **题意与约定**：假设${example}
   - **核心提示**：提示${example}
   - **完整分步演算**：演算${example}
   - **结论与边界回验**：结论${example}
   - **易错坑提醒**：核对${example}

`;
const original = '## 第 0 章\n\n' + answer(1, '00-01', '甲') + answer(2, '00-02', '乙');
const options = {
  expectedTotal: 2,
  baseline: verifyExerciseAlignment(chapters, original, { expectedTotal: 2, baseline: {} }).fingerprints,
};

test('原题保留身份且正常修改答案可通过', () => {
  requireExerciseAlignment(verifyExerciseAlignment(chapters, original, options));
  requireExerciseAlignment(verifyExerciseAlignment(chapters, original.replace('演算甲', '补充演算步骤甲'), options));
});

test('原序号未变时拒绝两个答案身份的错配', () => {
  const swapped = '## 第 0 章\n\n' + answer(1, '00-02', '乙') + answer(2, '00-01', '甲');
  const check = verifyExerciseAlignment(chapters, swapped, options);
  assert.equal(check.totalExerciseAnswers, 2);
  assert.throws(() => requireExerciseAlignment(check), /00 第 1 题 附录答案需使用原题号 1 和身份 00-01/);
});

test('身份标记留在原位时拒绝把已核对正文移到另一题', () => {
  const content = (tag) => answer(1, '00-01', tag)
    .replace(`标题${tag}`, '标题甲')
    .replace(`提示${tag}`, '提示甲');
  const swapped = '## 第 0 章\n\n' + content('乙') + answer(2, '00-02', '甲');
  const check = verifyExerciseAlignment(chapters, swapped, options);
  assert.throws(() => requireExerciseAlignment(check), /00 第 1 题 解题正文与其他题的已核对内容一致，原身份 00-02/);
});

test('拒绝丢失、重复身份、重复章节和缺少核心提示', () => {
  const variants = [
    [original.replace(' <!-- exercise-id: 00-01 -->', ''), /无有效身份/],
    [original.replace('exercise-id: 00-02', 'exercise-id: 00-01'), /原题号 2 和身份 00-02/],
    [original + '\n## 第 0 章\n\n', /附录章节重复/],
    [original.replace('   - **核心提示**：提示甲\n', ''), /缺少难度、核心提示或原有四步结构/],
  ];
  for (const [input, message] of variants) {
    assert.throws(() => requireExerciseAlignment(verifyExerciseAlignment(chapters, input, options)), message);
  }
});
