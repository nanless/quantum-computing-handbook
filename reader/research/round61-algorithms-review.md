# 第 61 轮独立复审：噪声、算法、应用与信息论七章

范围：`05`、`06`、`07`、`08`、`13`、`16`、`18`。逐篇通读定义、公式、手算、前后章术语、教学梯度与出处；只修改这七个章节，不修改 `sources/`、`reader/` 或共享练习答案。

## 逐篇发现与处理

| 章 | 独立复审的主要核对点 | 发现的问题与本轮处理 |
|---|---|---|
| 05 混态与信道 | 密度矩阵正性、测量工具、Kraus、完全正、四类噪声、退极化参数、$T_1/T_2$ | 原文指出“同一 POVM 可有不同测后态”，却没有手算实例。加入计算基投影与“测后复位”的两种工具：二者 $M_k^\dagger M_k$ 相同，但对 $|+\rangle$ 的条件与非选择后态不同。这也防止初学者误认为 POVM 元已定义了全部测量过程。 |
| 06 算法骨架 | oracle 可逆性、相位回踢、DJ/BV、QFT、有限精度 QPE、重复成本 | 原有相位回踢推导正确，但没有把“经典可查询接口”与“相干 oracle”在同一算例中对照。加入先测量输入位的反例：相位符号在 $I/2$ 中不可见，末尾 Hadamard 仍各半。 |
| 07 代表算法 | Simon、Grover、Shor 连分数、Trotter 数值界、qDRIFT、HHL、幅度估计、复杂度 | 二阶对称乘积公式只写了单片，却直接谈固定总时间的 $O(t^3/r^2)$，初学者易误把单片当完整模拟。改成 $[e^{-iA\Delta/2}e^{-iB\Delta}e^{-iA\Delta/2}]^r$、$\Delta=t/r$，并算出相邻半片合并后的 $2r+1$ 个指数操作。 |
| 08 应用 | VQE 变分界与采样误差、QAOA 符号与单边/路径算例、数据装载、金融采样、2026 年实验主张 | “有限采样可低于真基态”原先只作文字提醒。用本章 $0.7Z+0.2X$ 的**精确基态**算出各测一份、都得 $-1$ 时 $\hat E=-0.9<E_0\approx-0.728$，该事件概率约 $0.6251$。突出物理期望与有限样本估计不是同一量。 |
| 13 信息量度 | 熵、迹距离、根保真度、无歧义判别、Holevo 例子、相对熵数据处理 | 相对熵只有通式，缺一个能从定义算到底的初级例子。加入 $\rho=\operatorname{diag}(3/4,1/4)$、$\sigma=I/2$，算得 $D=1-h_2(1/4)\approx0.18872$ bit；共同复位后为 0，并明确单例不能代替普遍定理。 |
| 16 高级算法与验证 | HSP、量子行走、LCU/块编码/QSVT、阴影、能隙证书 | 原能隙证书从定义直接跳到不等式。补能量本征态展开、激发子空间总占据 $1-f_0$，并用两能级混态构造 $E-E_0=0.10,\Delta=0.40,f_0=0.75$ 的取等号例，说明证书何时紧。 |
| 18 容量与复杂度 | 纯化/Choi、Stein 引理、四类擦除信道容量、PPT、量子指纹、连续变量 | “相干信息可负而容量非负”虽正确，但缺简单逻辑桥。补充任一纯输入令参考系一维即 $S(B)=S(RB)$，所以单次最大相干信息至少为零；负值只属于某些特定输入。 |

## 独立核验

- $0.7Z+0.2X$ 的本征值为 $\pm\sqrt{0.53}$。精确基态两组独立单次测量都得到 $-1$ 的概率经数值复算为 `0.6250990047336068`；其一次能量估计是 `-0.9`，确低于真实最低能量 `-0.7280109889280518`。
- $D(\operatorname{diag}(3/4,1/4)\|I/2)=0.18872187554086717$ bit。
- 05 的两组测量算子分别满足 $\sum_kM_k^\dagger M_k=\sum_kN_k^\dagger N_k=I$，且两个结果的效应同为 $P_0,P_1$；结果为 1 时后态分别为 $|1\rangle$、$|0\rangle$。
- 07 对称公式总指数因子数：未合并为 $3r$；$r-1$ 个片间相邻 $A$ 半步各合并一次，故 $3r-(r-1)=2r+1$。此数是指数操作数，不是原生门数。
- 16 两能级证书例中 $E=0.25\times0.40=0.10$，$f_0=0.75=1-E/\Delta$，取等号。
- 18 对纯输入作一维参考纯化，$I_c=0$，故最大化后的单次值不可能为负。

## 一手资料核对

- IBM Quantum Learning, [Mathematical formulations of measurements](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/general-measurements/formulations-of-measurements)：区分只报告结果的测量与需要规定量子后态的过程；05 已增列出处。
- Cleve 等，[Quantum Algorithms Revisited](https://arxiv.org/abs/quant-ph/9708016)：以相干干涉为算法共同机制；06 已有该出处。
- Childs 等，[A Theory of Trotter Error](https://arxiv.org/abs/1912.08854)：一阶和高阶乘积公式及误差；07 已有期刊版出处。
- Peruzzo 等，[VQE 原始论文](https://doi.org/10.1038/ncomms5213) 与 Farhi 等，[QAOA 原始论文](https://arxiv.org/abs/1411.4028)：08 已有出处。此轮增加的有限样本概率是直接从该章的本征态与 Born 规则计算，不借用实验性能声明。
- Petz，[Monotonicity of quantum relative entropy revisited](https://arxiv.org/abs/quant-ph/0209053)：数据处理定理；13 已增列出处。
- Gilyén 等，[Quantum singular value transformation and beyond](https://arxiv.org/abs/1806.01838)：16 原有出处，用于复核块编码与多项式变换的边界。
- Watrous，[The Theory of Quantum Information](https://cs.uwaterloo.ca/~watrous/TQI/) 与 Bennett、DiVincenzo、Smolin，[Capacities of Quantum Erasure Channels](https://doi.org/10.1103/PhysRevLett.78.3217)：18 原有出处；本轮没有改写容量定理的范围。
- 2026 年的三篇 IBM 相关预印本页面已再次核对：[Floquet 观测量](https://arxiv.org/abs/2607.24937)、[困难线路采样](https://arxiv.org/abs/2607.25941)、[无经典真值时的观测量估计](https://arxiv.org/abs/2607.25998)。08 的“预印本、特定任务、待后续检验”限定仍适当，本轮不改动该结论。

## 给共享练习文件维护者的建议

本轮**没有新增、删除或改写**七章中任何一章的自检题；尤其第 13 章现有 1–6 题及题号均未动。共享 `appendices/exercises.md` 未由本代理修改，以避免并行编辑冲突。

下一轮可考虑补 05 “两套相同 POVM 的测后态”、08 “为何 $-0.9$ 不违反变分原理”、13 “$1-h_2(1/4)$ 数据处理”、16 “两能级证书取等号”各一小题及答案；这些只是未实施的建议，不影响本轮现有题答。

## 留待统一集成检查

由主代理统一构建阅读版并核查新公式渲染、移动端宽度、链接与跨章题答。本文只报告本代理负责章节的有证据改进；未发现的错误仍可能存在，不能把此次抽查称为全书“绝对零缺陷”。
