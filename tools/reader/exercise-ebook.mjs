import { marked } from 'marked';
import { exerciseChapterId } from './exercise-identity.mjs';

export function splitExercisesByPart(markdown, groups) {
  const front = [];
  const tail = [];
  const sections = new Map();
  let current = front;
  for (const token of marked.lexer(markdown, { gfm: true })) {
    if (token.type === 'heading' && token.depth === 1 && current === front) continue;
    if (token.type === 'heading' && token.depth === 2) {
      const chapter = exerciseChapterId(token.text);
      if (chapter) {
        if (sections.has(chapter)) throw new Error(`Duplicate answer section ${chapter}`);
        current = [];
        sections.set(chapter, current);
      } else {
        current = sections.size > 0 ? tail : front;
      }
    }
    current.push(token.raw);
  }

  return groups.map((group, index) => {
    const isFirst = index === 0;
    const isLast = index === groups.length - 1;
    const title = `附录 D（${group.tag}）· 自检题参考解答：${group.title}`;
    const intro = `本分册收录**${group.label}**（共 ${group.ids.length} 章）的全部章末自检题零跳步参考解答。`;
    const chapters = group.ids.map(chapter => {
      if (!sections.has(chapter)) throw new Error(`Missing answer section ${chapter}`);
      return sections.get(chapter).join('').trim();
    });
    const content = [
      `# ${title}`,
      isFirst ? front.join('').trim() : intro,
      ...chapters,
      isLast ? tail.join('').trim() : '',
    ].filter(Boolean).join('\n\n');
    return {
      partNum: group.number,
      shortPart: group.tag,
      xname: `app-exercises-p${group.number}.xhtml`,
      navLabel: `${group.tag}解答 · ${group.title}`,
      title,
      markdown: `${content}\n`,
    };
  });
}
