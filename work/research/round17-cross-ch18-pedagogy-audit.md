# 第 17 轮交叉审稿：第 18 章教学与一致性审计

## 1. 范围与结论

本轮只读审查了：

- `handbook/18-channels-capacities-complexity.md`；
- `handbook/05-noise-channels.md`、`handbook/13-quantum-information.md` 中新增的第 18 章回链；
- `handbook/appendices/exercises.md` 的“第 18 章”十道答案；
- `handbook/appendices/notation.md`、`glossary.md`、`references.md` 对第 18 章的支撑情况。

没有修改任何 handbook 文件。

结论计数：

| 级别 | 数量 | 结论 |
|---|---:|---|
| P0 | 0 | 未发现会导致整章主线失效、严重安全问题或大面积错误的问题 |
| P1 | 1 | 量子指纹只给“最小相对距离”，不足以推出正文与答案使用的重叠绝对值上界 |
| P2 | 7 | 主要是定理适用条件、容量等式的最优性说明、资源模型、CV 边界、术语与引用入口 |

除 P1 所列的第 9 题外，其余九道答案与题目语义对应，复算无误。

## 2. P1：必须修复

### P1-1 量子指纹的码距前提不足，导致第 9 题的上界并非由现有条件推出

**位置**

- 正文第 7.1 节，约第 696–713 行；
- 自检第 9 题，约第 857 行；
- `appendices/exercises.md` 第 18 章答案 9，约第 733–758 行。

**现有表述**

正文只假设二元码的相对距离“至少为 $\delta$”，随后对相位指纹

$$
|\phi_x\rangle=\frac1{\sqrt m}\sum_i(-1)^{E(x)_i}|i\rangle
$$

使用

$$
|\langle\phi_x|\phi_y\rangle|\le 1-2\delta.
$$

**问题**

设两码字的相对 Hamming 距离为 $\Delta$，则精确地有

$$
\langle\phi_x|\phi_y\rangle=1-2\Delta.
$$

条件 $\Delta\ge\delta$ 只能推出 $1-2\Delta\le1-2\delta$，不能推出绝对值上界。若两个码字互补，$\Delta=1$，则内积为 $-1$、绝对值为 1，swap test 会始终把它们判为“相同”。因此，当前第 9 题所给 $5/8$ 与 $(5/8)^{10}$ 虽然算术正确，却不由题设推出。

原始量子指纹论文明确要求用于相位指纹的码字两两距离集中在 $m/2$ 附近，从而使内积的**绝对值**很小；参见 Buhrman–Cleve–Watrous–de Wolf 原文第 2 页：距离位于 $\frac12(1-\eta)m$ 与 $\frac12(1+\eta)m$ 之间时，才有 $|\langle h_x|h_y\rangle|\le\eta$。

**精确修法（保留现有数值答案）**

1. 把正文“相对距离至少为 $\delta$”改为：对任意 $x\ne y$，

   $$
   \delta\le \Delta(E(x),E(y))\le1-\delta,
   \qquad 0<\delta<\frac12.
   $$

   或直接假设该码具有“成对偏差”

   $$
   |1-2\Delta(E(x),E(y))|\le\eta.
   $$

2. 在内积推导中显式写出

   $$
   |\langle\phi_x|\phi_y\rangle|
   =|1-2\Delta(E(x),E(y))|
   \le1-2\delta.
   $$

3. 把自检第 9 题改为“任意不同码字的相对距离均落在 $[1/4,3/4]$”，答案才可继续使用

   $$
   p_{\rm same}\le\frac{1+(1/2)^2}{2}=\frac58,
   \qquad
   (5/8)^{10}\approx0.00909495.
   $$

4. 若只想保留“最小距离至少 $1/4$”这一普通纠错码条件，则应改用原论文较早的带码位寄存器指纹

   $$
   |h_x\rangle=\frac1{\sqrt m}\sum_i|i\rangle|E_i(x)\rangle,
   $$

   此时重叠是码位相同的比例；但数值上界会改变，不能继续沿用 $5/8$。

**一手证据**

- H. Buhrman, R. Cleve, J. Watrous, R. de Wolf, *Quantum Fingerprinting*: <https://arxiv.org/abs/quant-ph/0102001>
- 作者托管的论文 PDF：<https://jhwatrous.github.io/BuhrmanCleveWatrousdeWolf2001.pdf>

## 3. P2：应修复以提高严谨性与初学者可读性

### P2-1 Uhlmann 定理缺少“共同参考系统足够大”的限定

**位置**：第 1.2 节，约第 116–122 行。

当前写成“固定 $\rho$ 的一个纯化，在同一参考空间上优化 $\sigma$ 的纯化”。若固定的是最小纯化，而 $\operatorname{rank}\sigma>\dim R$，则 $\sigma$ 根本无法在该 $R$ 上纯化。

**精确修法**：改为“先选择满足 $\dim R\ge\max\{\operatorname{rank}\rho,\operatorname{rank}\sigma\}$ 的共同参考系统，并把固定的 $\rho$ 纯化嵌入其中；再对 $\sigma$ 在该空间上的所有纯化取最大值”。随后保留当前根保真度公式。也可补一句：在等维充分大的参考空间中，所有纯化可用参考端酉变换参数化；维数不同时需使用等距变换。

正文采用根保真度而非平方保真度，公式本身正确。

**权威入口**：Watrous, *The Theory of Quantum Information*, purifications and fidelity: <https://cs.uwaterloo.ca/~watrous/TQI/>

### P2-2 Stein 引理后的“约等于”应改成明确的指数阶陈述

**位置**：第 3 节，约第 273–281 行。

当前

$$
\beta_n\approx2^{-nD(\rho\|\sigma)}
$$

容易被初学者理解为有限 $n$ 的数值近似或逐项相等。Stein 引理只固定一阶渐近指数。

**精确修法**：定义

$$
\beta_n^*(\epsilon)=
\min_{T_n:\alpha(T_n)\le\epsilon}\beta(T_n),
$$

并写成

$$
\lim_{n\to\infty}-\frac1n\log_2\beta_n^*(\epsilon)
=D(\rho\|\sigma),
$$

或等价地

$$
\beta_n^*(\epsilon)=2^{-nD(\rho\|\sigma)+o(n)}.
$$

这也会使答案 4 中“$0.2781$ bit 是错误指数”的单位更清楚：它是以 2 为底时的“每副本 bit 指数”。

**一手证据**：T. Ogawa, H. Nagaoka, *Strong Converse and Stein's Lemma in Quantum Hypothesis Testing*: <https://arxiv.org/abs/quant-ph/9906090>

### P2-3 擦除信道小节多处从“构造可达方案”直接跳到容量等式，欠缺最优性桥梁

**位置**：第 4.5 节，特别是经典容量约第 417–423 行、纠缠辅助容量约第 471–484 行。

正交编码只证明 $C\ge1-\varepsilon$，最大混合输入的互信息计算只证明 $C_E\ge2(1-\varepsilon)$。现文直接写等号，对初学者隐藏了“可达率”和“容量上界”的差别。$Q$、$P$ 段已经用可降解/反降解说明最优性，结构反而更完整。

**精确修法**：

- 经典容量补一行 converse：已知擦除位置后，一次使用至多在未擦除分支贡献 $\log_2d$ bit，因此 $C\le(1-\varepsilon)\log_2d$；qubit 时与正交编码下界合并得到 $C=1-\varepsilon$。
- 纠缠辅助容量对任意输入 $\rho$ 写出

  $$
  I(R:B)=2(1-\varepsilon)S(\rho)
  \le2(1-\varepsilon)\log_2d,
  $$

  最大混合输入取等；这才推出 qubit 的 $C_E=2(1-\varepsilon)$。
- 可在 $Q$ 段把“严格证明可用……”改得再明确一点：$\varepsilon\le1/2$ 时可降解性使单次相干信息可加；$\varepsilon\ge1/2$ 时反降解性给出零容量。

答案 5 的四个数值均正确，无需改数值。

**一手证据**：

- Bennett–DiVincenzo–Smolin, *Capacities of Quantum Erasure Channels*: <https://arxiv.org/abs/quant-ph/9701015>
- Bennett–Shor–Smolin–Thapliyal, *Entanglement-assisted capacity of a quantum channel and the reverse Shannon theorem*: <https://arxiv.org/abs/quant-ph/0106052>
- Devetak, *The private classical capacity and quantum capacity of a quantum channel*: <https://arxiv.org/abs/quant-ph/0304127>

### P2-4 私密容量的免费资源口径仍有一句含混

**位置**：容量表与第 4.3 节，约第 316–319、391–394 行。

“必须声明公共通信等模型”和“无反向或双向辅助通信”会让读者不确定本节究竟允许不允许免费前向公共通信。标准无辅助私密经典通信公式不需要额外公共信道；对相应密钥生成任务，免费的前向公共通信不提高 Devetak 所给容量，但反向/双向辅助会定义不同任务。

**精确修法**：直接写清本章的口径，例如：“下式首先定义不带额外辅助信道的私密经典容量；若改写为密钥生成，允许免费前向公共通信仍得到同一容量，而反向或双向公共通信对应另一种辅助容量。”容量表的“免费辅助资源”一栏相应写“无；等价密钥生成模型可允许不增益的前向公共通信”。

### P2-5 连续变量段的压缩方向与高效模拟条件说得过于省略

**位置**：第 8 节，约第 770–817 行。

两个公式的数值约定正确，但有三处可更精确：

1. $V(r)=\frac12\operatorname{diag}(e^{-2r},e^{2r})$ 默认压缩轴已经与 $q$ 对齐且 $r>0$；一般相位下协方差矩阵还需旋转。
2. 前面定义了 $\hat R$，随后写 $d_i=\langle R_i\rangle$，帽号不一致。
3. “在常见条件下”是隐藏条件。高效经典模拟需说明输入与演化有有效的 Gaussian 描述，模式数、步骤数、所需数值精度与能量/截断资源按问题规模受控；结论不是对任意无限能量或指数精度描述的无条件算法。

**精确修法**：在压缩矩阵前加“选择压缩相位使 $q$ 为压缩轴，并取 $r>0$”；统一写 $d_i=\langle\hat R_i\rangle$；把模拟边界改成具体的多项式资源条件。答案 10 的 $1/4,1,1/4$ 均正确。

**一手证据**：

- Bartlett–Sanders–Braunstein–Nemoto, *Efficient Classical Simulation of Continuous Variable Quantum Information Processes*: <https://arxiv.org/abs/quant-ph/0109047>
- Weedbrook et al., *Gaussian Quantum Information*: <https://arxiv.org/abs/1110.3234>

### P2-6 初学者入口仍残留未解释的英文与高级术语，符号表和术语表没有承接第 18 章

**位置**：正文多处；`notation.md` 目前止于 $\chi$；`glossary.md` 未覆盖第 18 章核心术语。

正文首次出现或只靠语境解释的词包括 `ensemble`、`i.i.d.`、`SPAM`、`shots`、可降解/反降解信道、互补信道、相干信息、Gaussian/非 Gaussian、同相/外差探测。尤其第 665 行“SPAM、漂移、有限 shots”与全书要求的平实中文不一致。

**精确修法**：

- 首次出现时写“态系综（ensemble）”“独立同分布（i.i.d.）”“状态制备与测量误差（SPAM）”“有限次采样（shots）”。
- 在第 4.2–4.3 节用一句式定义互补信道、可降解与反降解，而不是只在擦除例中报名称。
- `notation.md` 至少加入 $J_{\mathcal E}$、$D(\rho\|\sigma)$、$D_H^\epsilon$、$I_c$、$C/Q/P/C_E$、$\mathcal N(\rho)$、$\hat q,\hat p,V$，并注明 $\mathcal N$ 在本章也用于“负性”，避免与信道 $\mathcal N$ 的上下文冲突。
- `glossary.md` 至少加入纯化、Choi 矩阵、相干信息、互补信道、负性、QCMA/QMA/QIP、通信复杂度、Gaussian 态。

这不是要求把术语表变成另一章，只需给出一到两句可回查定义。

### P2-7 参考入口缺少两组直接支撑正文定理的原始来源，且纠缠辅助容量条目元数据不完整

**位置**：第 18 章“参考起点”和 `appendices/references.md`。

第 18 章直接使用负性定义以及 $2\times2$ 的 PPT 充要判据，却只列资源理论综述，没有列负性与 PPT 判据的原始论文。纠缠辅助容量条目只给 arXiv 和“2001/2002”，适合作为链接但书目信息不完整。全书精选参考页目前也没有能代表第 18 章新增通信复杂度、信道容量与 CV 的条目。

**精确修法**：

- 第 18 章参考起点加入：
  - G. Vidal, R. F. Werner, *A computable measure of entanglement*: <https://arxiv.org/abs/quant-ph/0102117>
  - A. Peres, *Separability Criterion for Density Matrices*: <https://arxiv.org/abs/quant-ph/9604005>
  - M. Horodecki, P. Horodecki, R. Horodecki, *Separability of Mixed States: Necessary and Sufficient Conditions*: <https://arxiv.org/abs/quant-ph/9605038>
- 把 Bennett–Shor–Smolin–Thapliyal 补全为 *IEEE Transactions on Information Theory* 48, 2637–2655 (2002)，并优先补 DOI `10.1109/TIT.2002.802612`；arXiv 可保留为开放版本。
- `appendices/references.md` 的“精选入口”至少增补一条量子信道容量（Watrous 已有，可指到第 8 章）、一条量子指纹/QIP、一条 Gaussian 信息；若坚持精选原则，可不把所有原始论文重复收入。

## 4. 已核对为正确的部分

### 4.1 数学与计算

- 纯化 $\sqrt{0.8}|00\rangle+\sqrt{0.2}|11\rangle$ 的偏迹推导正确。
- 根保真度约定与第 05、13 章一致；$F(I/2,|0\rangle)=1/\sqrt2$ 正确。
- 未归一化 Choi 约定、重构公式中的转置、CP 判据和 TP 偏迹方向均正确。
- 复位信道 $J_{\mathcal R}=\operatorname{diag}(1,0,1,0)$ 正确。
- $D(\operatorname{diag}(0.8,0.2)\|I/2)=0.278071905\ldots$ bit，迹距离 $0.3$，Helstrom 成功率 $0.65$，均正确。
- qubit 擦除信道在 $\varepsilon=1/4$ 时：

  $$
  C=0.75,
  \quad Q=0.50,
  \quad P=0.50,
  \quad C_E=1.50
  $$

  数值和单位正确。
- $\rho_p=p|\Phi^+\rangle\langle\Phi^+|+(1-p)I/4$ 在 $p=0.6$ 时，部分转置谱为 $(-0.2,0.4,0.4,0.4)$，负性为 $0.2$，正确。
- QCMA/QMA 的 yes/no 量词与见证类型区分正确；“QCMA 的验证者仍是量子验证者”表述正确。
- $\mathrm{QIP}=\mathrm{PSPACE}$ 没有被误写为 $\mathrm{BQP}=\mathrm{PSPACE}$。
- $[q,p]=i$、真空方差 $1/2$ 的约定内部一致；$r=(\ln2)/2$ 时两个方差为 $1/4$ 与 $1$，乘积 $1/4$，正确。

### 4.2 结构、回链与答案对应

- 第 05 章第 127 行到第 18 章的回链路径有效，CPTP 与根保真度口径一致。
- 第 13 章第 156、178、334 行的三个回链路径有效，分别正确指向混态纠缠、Stein 引理和信道容量的后续展开。
- 第 18 章到练习答案的锚点有效。
- 本轮检查的三个正文文件没有失效的本地 Markdown 链接。
- 第 18 章 1–10 题与答案 1–10 编号齐全；除第 9 题前提不足外，题答语义一一对应。

## 5. 建议修订顺序

1. 先同步修正文 7.1、自检 9、答案 9 的码距条件，消除唯一 P1。
2. 补 Uhlmann 辅助维数和 Stein 指数的严格限定。
3. 给擦除信道的 $C$、$C_E$ 增加两行 converse/最优化推导，并澄清 $P$ 的公共通信口径。
4. 明确 CV 压缩轴与 Gaussian 模拟条件，统一帽号。
5. 最后补术语、符号与精选参考入口。

按以上顺序修复后，第 18 章的主线无需重写；现有结构、绝大多数推导和图表可以保留。
