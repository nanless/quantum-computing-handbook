// Pedagogical ordering shared by rendering and browser verification.
// Source filenames and chapter numbers remain stable across V3 (26 chapters: 00–21 + Q1–Q4).
export const readingGroups = [
  ['第一篇 · 数学、量子态与电路', ['00', '01', '02', '03', '04', '05']],
  ['第二篇 · 实验、动力学与器件物理', ['Q1', 'Q2', 'Q3', 'Q4']],
  ['第三篇 · 核心算法、应用与实验方法', ['06', '07', '08', '15']],
  ['第四篇 · 量子硬件、纠错与执行', ['09', '10', '11', '14', '19']],
  ['第五篇 · 量子信息、通信与传感', ['13', '12', '18', '20']],
  ['第六篇 · 高级算法、计算模型与经典模拟', ['16', '17', '21']],
];

export function readingPlan(entries) {
  const byId = new Map();
  for (const file of entries) {
    const parts = file.replaceAll('\\', '/').split('/');
    const prefix = parts.at(-1).match(/^(\d\d)-/)?.[1];
    if (!prefix) throw new Error(`Reading order cannot identify chapter: ${file}`);
    const id = parts.at(-2) === 'quantum-mechanics' ? `Q${Number(prefix)}` : prefix;
    if (byId.has(id)) throw new Error(`Reading order has two files for ${id}`);
    byId.set(id, file);
  }
  const groups = readingGroups.map(([label, ids], index) => {
    const [tag, title] = label.split(' · ');
    const files = ids.map(id => {
      if (!byId.has(id)) throw new Error(`Reading order needs chapter ${id}`);
      return byId.get(id);
    });
    return { label, ids, files, tag, title, number: index + 1 };
  });
  const sequence = groups.flatMap(group => group.files);
  if (sequence.length !== entries.length || new Set(sequence).size !== entries.length) {
    throw new Error('Reading order omitted or duplicated a chapter');
  }
  return { groups, sequence };
}
