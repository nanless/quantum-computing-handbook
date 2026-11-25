// Pedagogical ordering shared by rendering and browser verification.
// Source filenames and chapter numbers remain stable across V3 (26 chapters: 00–21 + Q1–Q4).
export const readingGroups = [
  ['第一篇 · 入门、数学与量子态基础', ['00', '01', 'Q1', '02', 'Q2', '03', '04', '05']],
  ['第二篇 · 核心算法、应用与实验实践', ['06', '07', '08', '15']],
  ['第三篇 · 物理硬件、编译、纠错与系统工程', ['Q3', '09', '14', '10', '11', '19']],
  ['第四篇 · 密码、网络与精密测量', ['12', '20']],
  ['第五篇 · 信息理论、高级算法、模拟边界与计算模型', ['13', '16', '21', '17', 'Q4', '18']],
];

export function readingPlan(entries) {
  const normalized = entries.map(file => file.replaceAll('\\', '/'));
  const find = id => {
    const isQM = id.startsWith('Q');
    const prefix = isQM ? `0${id.slice(1)}-` : `${id}-`;
    const matches = entries.filter((file, i) => {
      const parts = normalized[i].split('/');
      return parts.at(-1).startsWith(prefix) && normalized[i].includes('/quantum-mechanics/') === isQM;
    });
    if (matches.length !== 1) throw new Error(`Reading order needs exactly one ${id}, found ${matches.length}`);
    return matches[0];
  };
  const groups = readingGroups.map(([label, ids]) => ({ label, ids, files: ids.map(find) }));
  const sequence = groups.flatMap(group => group.files);
  if (sequence.length !== entries.length || new Set(sequence).size !== entries.length) {
    throw new Error('Reading order omitted or duplicated a chapter');
  }
  return { groups, sequence };
}
