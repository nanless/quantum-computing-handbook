// Pedagogical ordering shared by rendering and browser verification.
// Source filenames and chapter numbers remain stable.
export const readingGroups = [
  ['入门与数学', ['00', '01']],
  ['量子态、测量与电路', ['Q1', '02', 'Q2', '03', '04', '05']],
  ['算法与应用', ['06', '07', '08']],
  ['硬件、容错与网络', ['Q3', '09', '10', '11', '12']],
  ['信息、控制与实践', ['13', '14', '15']],
  ['高级算法与系统工程', ['16', '17', '18', '19']],
  ['波函数与模型 · 进阶选读', ['Q4']],
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
  const groups = readingGroups.map(([label, ids]) => ({label, ids, files: ids.map(find)}));
  const sequence = groups.flatMap(group => group.files);
  if (sequence.length !== entries.length || new Set(sequence).size !== entries.length) throw new Error('Reading order omitted or duplicated a chapter');
  return {groups, sequence};
}
