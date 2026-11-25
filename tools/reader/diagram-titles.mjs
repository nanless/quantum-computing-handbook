// Single source of truth for Mermaid flowchart captions shared by Web, PDF, and EPUB builders.
// Any Mermaid block may also override its own caption via a leading `%% title: ...` comment.

export const diagramTitles = {
  'README.md': ['主篇 00—21 与物理篇 Q1—Q4 共 26 章的学习路线'],
  '00-overview.md': [
    '一次量子计算从输入到验证的五个环节',
    '相同测量概率的两态经 H 门干涉后的分流对照',
  ],
  '01-math.md': ['从厄米算符出发的测量与酉演化两条路径'],
  '02-single-qubit.md': ['单量子比特测量模型的三层结构：投影测量、POVM 与量子仪器'],
  '06-algorithmic-primitives.md': ['量子算法核心原语之间的依赖关系与拼装路径'],
  '07-algorithms.md': ['经典与量子核心复杂度类的包含关系与代表性问题定位'],
  '08-applications.md': ['变分算法中量子测量与经典参数更新的循环'],
  '09-hardware.md': ['量子计算机从程序到控制、读出和反馈的系统链'],
  '10-error-correction.md': ['魔法态培育五步流程与互补间隙后选择路径'],
  '11-resources-benchmarks.md': ['从应用目标逐层估算逻辑与物理资源'],
  '12-security-network-frontiers.md': [
    '机内互连、远距离网络与量子互联网的范围区别',
    '量子网络从物理链路到应用服务的分层',
  ],
  '13-quantum-information.md': ['以数据处理不等式为总枢纽的量子信息核心不等式关系图'],
  '14-compilation-control.md': [
    '算法线路到物理执行的九层表示与编译控制流程',
    '门校准的依赖顺序与漂移回归路径',
    '实时纠错从模拟读出到流式解码与条件反馈的路径',
  ],
  '15-practice-research.md': ['从纸笔小例到硬件实验的四级验证阶梯与排错回退路径'],
  '16-advanced-algorithms-verification.md': [
    '隐藏子群算法从查询到经典恢复的共同骨架',
    '大型量子模拟结果的四类交叉证据',
  ],
  '17-computation-models.md': ['七大计算模型之间的理论模拟联系与不能直接等同的边界'],
  '18-channels-capacities-complexity.md': [
    '量子态纯化、信道表示、钻石范数与通信容量之间的逻辑脉络',
    '混态纠缠资源理论中的免费操作、蒸馏稀释与度量层级',
    '交互式量子证明中验证者与证明者的消息往返与判决流程',
    '同时消息模型中双方发送量子指纹并由裁判执行交换测试的流程',
  ],
  '19-engineering-architecture.md': ['校准参数依赖有向无环图与快照原子晋级流程'],
  '20-quantum-sensing-metrology.md': ['量子传感从物理信号编码、噪声滤波到参数估计极限的决策路径'],
  'quantum-mechanics/01-experiments-states.md': ['延迟选择量子擦除的因果顺序与经典符合分组流程'],
  'quantum-mechanics/02-observables-dynamics.md': ['量子系统时间演化的五条计算路径选择'],
  'quantum-mechanics/03-levels-control.md': ['Ramsey 干涉与 Hahn 自旋回波的脉冲时序及测量目标对照'],
  'quantum-mechanics/04-wavefunctions-models.md': ['连续量子模型在计算机上的两条离散化路径与收敛核验'],
};

export function resolveDiagramTitle(relSource, zeroBasedIndex, mermaidCode = '') {
  const inline = mermaidCode.match(/^%%\s*title:\s*(.+)$/m)?.[1]?.trim();
  if (inline) return inline;
  const title = diagramTitles[relSource]?.[zeroBasedIndex];
  if (!title) {
    throw new Error(`missing descriptive diagram title for ${relSource} #${zeroBasedIndex + 1}`);
  }
  return title;
}
