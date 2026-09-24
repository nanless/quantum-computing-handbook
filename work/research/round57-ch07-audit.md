# 第 7 章逐篇审查：代表性量子算法（2026-09-24）

## 审查范围与来源

本轮只检查 `handbook/07-algorithms.md` 与练习附录第 7 章。核心事实以原论文和官方教学资料核对：Simon [原论文](https://doi.org/10.1137/S0097539796298637)及 [IBM Simon 教程](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/quantum-query-algorithms/simon-algorithm)；Grover [原论文](https://doi.org/10.1145/237814.237866)、[Boyer 等人的多解分析](https://arxiv.org/abs/quant-ph/9605034)及 [IBM 迭代数教程](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/grover-algorithm/number-of-iterations)；Shor [原论文](https://doi.org/10.1137/S0097539795293172)及 [IBM Shor 教程](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/shor-algorithm)；QFT [IBM 定义](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/phase-estimation-procedure)；HHL [原论文](https://arxiv.org/abs/0811.3171)。其余模拟、幅度估计与复杂度类主要沿用现有章末一手文献。

## 第一轮：关键缺口

| 优先级 | 段落 | 观察 | 修订方向 |
|---|---|---|---|
| P1 | 章首 | 全章已有大量正确推导，但从 Simon 直接进入黑盒承诺，对久未接触数学的读者缺学习路线；主线、进阶细节与资源口径挤在一起。 | 加“先读什么、用到时回看什么”，每算法先列输入、承诺、输出、成本、失败情形。 |
| P1 | §1 Simon | `\oplus`、`\cdot` 的二进制模 2 规则未在本章现身；初学者难复算 `s=110`；未强调本章特意排除 `s=0` 的一一映射变体。 | 加 3 位 XOR/点积具体算例，解释每个采样结果怎样约束而不是直接给出 `s`，给重复样本未增秩的实例。 |
| P1 | §2 Grover | 正弦公式和 N=16 表格准确，但没有一轮“oracle 改符号—扩散做均值反射”的四分量手算，读者只能背几何结论。 | 加 `N=4,M=1` 的精确振幅表与最终概率；区分一次迭代的查询和门实现。 |
| P1 | §3 Shor / QFT | 第 06 章讲过 QFT，但在此最重要的“周期为何变峰”未显式演示；`Q=256` 的峰位像凭空给出的结论。§3.5 失败表顺序把经典约化列在 Fourier 采样前，实际流程不是这样。 | 加 `Q=16,r=4` 的几何和小例子，接到 `N=15` 的四峰；按真实处理次序重排失败表；给 `a^{r/2}=+1` 不可能（若 r 真为阶）的解释。 |
| P1 | §5 HHL | 说了“受控旋转编码 `1/λ`”但没有写出 ancilla 测量与失败概率；二维例子恰可把成功概率 `5/8` 算出来。 | 写旋转幅度 `C/λ`、`0<C≤min|λ|`、成功概率 `C²||A^{-1}b||²`，在 `diag(1,2)` 上算 `5/8`；把态输出与经典解分清。 |
| P2 | §3.1/§3.4 | 模乘例子细，但“余数/模同余、gcd、阶”仍过于压缩；35 的连分数演示较高阶。 | 在 15 的例子中用一行算术解释“mod”与阶，再把 35 例标作进阶回看；增加一个 `r` 偶数但 `a^{r/2}=-1` 的失败支。 |
| P2 | §4/6/7 | 模拟误差、幅度估计与复杂度类包含关系为研究生层级，现有推导总体准确，但读者容易把 `H`（Hadamard vs Hamiltonian）和 `N`（候选数 vs qDRIFT 步数）混用。 | 在各节首次声明局部符号含义，并在章首路线中标出基础/进阶层。 |
| P2 | §10/答案 | 现有十题大多问结论和数量级；缺 Simon 方程、Grover 一轮、QFT 四峰、HHL 后选择手算。 | 增加对应题目与细解，检查和正文基序/记号一致。 |

## 已核对且保留的结论

- Simon 的三位 `s=110` 例子及满秩期望 `10/3` 次成立。
- Grover `N=16` 表格与 `sin²((2k+1)θ)` 一致；其最优性应继续限定无结构黑盒查询模型。
- `N=35,a=2` 的模幂序列、阶 12、读数 171、误差 `1/6144`、连分数 `[0;11,1,41,1,3]`、最终因子 5 和 7 均待本轮独立数值回归；此前没有发现明显相互矛盾。
- HHL 二维例子的解态 `(2|0>+|1>)/√5` 与 `⟨Z⟩=3/5` 正确，但缺后选择概率。

本报告只是第一轮缺口清单，修订完成后另写独立核算和仍待交叉审的记录。
