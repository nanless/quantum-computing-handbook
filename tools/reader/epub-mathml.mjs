import katex from 'katex';

const SCRIPT_ARITY = new Map([['msub', 2], ['msup', 2], ['msubsup', 3], ['mover', 2], ['munder', 2], ['munderover', 3]]);

function normalizeMathNode(node) {
  if (!node.children) return node;
  node.children = node.children.map(normalizeMathNode);

  // Operators such as \min and \deg expand to an identifier and an apply-
  // function marker. KaTeX can splice the marker into fixed-arity scripts or
  // accents. Remove the extra child and leave markers in expression rows alone.
  const arity = SCRIPT_ARITY.get(node.type);
  if (arity) {
    // KaTeX's untyped DocumentFragment serializes its children directly.
    const serializedChildren = node.children.flatMap(child =>
      !child.type && child.children ? child.children : [child]
    );
    if (serializedChildren.length === arity + 1) {
      const marker = serializedChildren.findIndex((child, i) =>
        i > 0 && serializedChildren[i - 1].type === 'mi' &&
        child.type === 'mo' && child.children.length === 1 && child.children[0].text === '\u2061'
      );
      if (marker !== -1) {
        serializedChildren.splice(marker, 1);
        node.children = serializedChildren;
      }
    }
  }

  if (node.type !== 'mo' || node.children.length !== 1) return node;
  const [child] = node.children;
  if (child.type === 'mrow' && child.children.length === 3 && child.children.every((letter, i) =>
    letter.type === 'mi' && letter.attributes.mathvariant === 'normal' &&
    letter.children.length === 1 && letter.children[0].text === 'mod'[i]
  )) {
    // The operator is a single token. Retain KaTeX's explicit operator spacing.
    const letter = child.children[0].children[0];
    letter.text = 'mod';
    node.children = [letter];
  } else if (Object.keys(node.attributes).length === 0 &&
    (child.type === 'mover' || (child.type === 'mo' && child.children.length === 1 && child.children[0].text === '='))) {
    // \overset{?}{=} generates two redundant wrappers. Its mover and scripts remain intact.
    return child;
  }
  return node;
}

export function renderEpubMathMl(latex, displayMode) {
  // The MathML tree shape comes from the locked KaTeX version. Normalize it
  // before serialization so nested scripts do not require regex reparsing.
  const root = katex.__renderToDomTree(latex, {
    displayMode, throwOnError: true, strict: 'ignore', trust: false, output: 'mathml',
  });
  const [math] = root.children;
  const [semantics] = math.children;
  if (math.type !== 'math' || semantics.type !== 'semantics') {
    throw new Error('Unexpected KaTeX MathML wrapper');
  }
  const [presentation] = semantics.children;
  math.children = [normalizeMathNode(presentation)];
  math.attributes.display = displayMode ? 'block' : 'inline';
  return math.toMarkup();
}

export function renderWebMath(latex, displayMode) {
  const tree = katex.__renderToDomTree(latex, {
    displayMode, throwOnError: true, strict: 'ignore', trust: false, output: 'htmlAndMathml',
  });
  function visit(node) {
    if (node.type === 'math') {
      const [semantics] = node.children;
      semantics.children[0] = normalizeMathNode(semantics.children[0]);
    } else if (node.children) {
      node.children.forEach(visit);
    }
  }
  visit(tree);
  return tree.toMarkup();
}
