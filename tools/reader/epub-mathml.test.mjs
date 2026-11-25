import assert from 'node:assert/strict';
import test from 'node:test';
import katex from 'katex';
import { renderEpubMathMl } from './epub-mathml.mjs';

const rawMathMl = latex => katex.renderToString(latex, { output: 'mathml' });

test('fixed-arity scripts keep their subscript and superscript', () => {
  const examples = [
    [String.raw`\sigma_{\max}`, '<msub><mi>σ</mi><mi>max</mi></msub>'],
    [String.raw`H_{\min}^{\varepsilon}`, '<msubsup><mi>H</mi><mi>min</mi><mi>ε</mi></msubsup>'],
    [String.raw`p_{\mathrm{guess}}^{\max}`, '<mi>max</mi></msubsup>'],
    [String.raw`\widetilde{\deg}_{1/3}(f)`, '<mover accent="true"><mi>deg</mi><mo stretchy="true">~</mo></mover>'],
  ];
  for (const [latex, wanted] of examples) {
    assert.ok(rawMathMl(latex).includes('<mo>\u2061</mo>'));
    const repaired = renderEpubMathMl(latex, false);
    assert.ok(repaired.includes(wanted), repaired);
    assert.ok(!repaired.includes('<mo>\u2061</mo>'), repaired);
    assert.ok(repaired.includes('display="inline"'));
  }
});

test('genuine function application is preserved', () => {
  const math = renderEpubMathMl(String.raw`\sin x + x^2`, true);
  assert.ok(math.includes('<mi>sin</mi><mo>\u2061</mo><mi>x</mi>'));
  assert.ok(math.includes('<msup><mi>x</mi><mn>2</mn></msup>'));
  assert.ok(math.includes('display="block"'));
});

test('binary mod is one operator token with KaTeX spacing', () => {
  const latex = String.raw`x\bmod y`;
  assert.match(rawMathMl(latex), /<mo[^>]*><mrow>/);
  assert.ok(renderEpubMathMl(latex, false).includes('<mo lspace="0.22em" rspace="0.22em">mod</mo>'));
});

test('an overset relation preserves its raised symbol and base relation', () => {
  const latex = String.raw`A\overset{?}{=}B`;
  assert.ok(rawMathMl(latex).includes('<mo><mover><mo><mo>='));
  const repaired = renderEpubMathMl(latex, false);
  assert.ok(repaired.includes('<mover><mo>=</mo><mo stretchy="false" lspace="0em" rspace="0em">?</mo></mover>'));
});
