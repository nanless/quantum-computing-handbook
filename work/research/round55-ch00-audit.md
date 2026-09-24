# 第 55 轮：第 00 章初学者审查

范围：`handbook/00-overview.md` 与 `handbook/appendices/exercises.md` 第 0 章。目标是让多年未复习数学的读者先建立可检查的整体图，再进入第 01 章。参考 IBM Quantum Learning 的单系统课程、Watrous 的量子信息框架、Preskill 的 NISQ 原文与 NIST 的后量子密码说明。只用这些一手资料核对定义和限制，不照搬原文。

## 主要发现

1. P1：第 2 节直接给态矢量和“同概率不同态”，却只报 `H|+⟩=|0⟩`，未展示一个读者能照着重算的干涉步骤。需给出矩阵逐行运算、两条路径振幅如何相加和模平方。
2. P2：开篇表格同时出现 Shor、Grover、HHL、VQE、QAOA、oracle 和复杂度记号，初读负荷过高。需要分层阅读提示：首次先理解计算链和一比特例子，表格留作地图。另须说明查询次数只是一种成本单位。
3. P2：第 5 节首次出现 NP、BQP 却没有定义。概览页不宜让读者在第一遍误把未经介绍的复杂度类当作先修条件，应改成普通语言并指出这仍是开放边界。
4. P2：最小算法只展示门的输出，未把测量概率逐步从两个分量的模平方算出；1000 次采样也须明确均值 500 并非每组保证。
5. P2：第 0 章原四题多为文字理解，没有检查最基础的振幅模平方和“相同任务、同样误差”的比较条件。增补低门槛自检和分步答案。

## 事实边界

- IBM Quantum Learning 的[单系统导论](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/introduction)以复振幅向量、酉操作和测量组织基础概念；[量子信息小节](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/quantum-information)也以 `|+⟩` 与 `|−⟩` 说明同一基的统计不足以确定态。
- Preskill, [Quantum Computing in the NISQ era and beyond](https://doi.org/10.22331/q-2018-08-06-79) 提供“噪声中等规模”一词的来源；它不是按比特数硬划的正式等级。
- NIST 的[后量子密码 FAQ](https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/faqs)区分量子算法对公钥与对称密码的影响；概览不应写成“所有密码立即失效”。

P0：未见确定性数值错误。此轮问题是解释顺序、抽象术语和自检台阶；修订后还须与其他章节交叉核查。
