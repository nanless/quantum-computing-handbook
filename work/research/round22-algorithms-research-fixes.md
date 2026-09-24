# 第 22 轮：算法教学调研与实施记录

日期：2026-09-22  
范围：`handbook/06-algorithmic-primitives.md`、`07-algorithms.md`、`08-applications.md`、`16-advanced-algorithms-verification.md`  
约束：未修改共享附录、README、其他章节；未增加自检题；未修改 Mermaid 图块。

## 1. 调研依据

本轮先完整阅读 `handbook/STYLE.md`，再以“读者能否从定义独立复算到数值结论”为标准逐段检查。主要核对的一手论文与官方材料如下。

1. R. Cleve, A. Ekert, C. Macchiavello, M. Mosca, [Quantum Algorithms Revisited](https://arxiv.org/abs/quant-ph/9708016), *Proceedings of the Royal Society A* 454, 339–354 (1998)。论文把一批算法统一到相位估计框架，并明确讨论有限精度；据此核查第 6 章的有限网格输出与概率解释。
2. M. Boyer, G. Brassard, P. Høyer, A. Tapp, [Tight bounds on quantum searching](https://arxiv.org/abs/quant-ph/9605034), *Fortschritte der Physik* 46, 493–505 (1998)。论文给出任意迭代次数的精确成功率，并处理多解和未知解数；据此核查第 7 章的过度旋转和随机迭代策略。
3. D. R. Simon, [On the Power of Quantum Computation](https://doi.org/10.1137/S0097539796298637), *SIAM Journal on Computing* 26, 1474–1483 (1997)。据此核查承诺、Fourier 采样所得线性方程及查询复杂度口径。
4. A. Peruzzo et al., [A variational eigenvalue solver on a photonic quantum processor](https://doi.org/10.1038/ncomms5213), *Nature Communications* 5, 4213 (2014)。原论文把 Hamiltonian 拆为可测项并以重复态制备估计期望值；据此核查第 8 章 VQE 流程和测量成本。本文新增的两项 shots 分配则由方差式直接推导，不把原论文当成该数值预算的来源。
5. IBM Quantum Learning, [Phase estimation procedure](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/phase-estimation-procedure) 与 [Grover algorithm: number of iterations](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/grover-algorithm/number-of-iterations)。作为官方课程交叉核对有限精度输出和未知解数处理；正文结论仍优先追溯到上述原论文。

## 2. 已修复的四处实质缺口

### 2.1 第 6 章：有限精度 QPE 只有单个概率，没有完整输出分布

**原问题。** 原文对 $\phi=1/3,t=2$ 只算了最近网格点 $y=1$ 的概率约 0.700。读者看不见其余概率去了哪里，也容易把“分辨率更高”和“单次成功置信度更高”混为一谈。

**新增内容。** 补出 $y=0,1,2,3$ 的完整分布：

$$
\left(\frac1{16},\frac{6+3\sqrt3}{16},\frac3{16},\frac{6-3\sqrt3}{16}\right)
\approx(0.0625,0.6998,0.1875,0.0502),
$$

并显式核对总和为 1。进一步区分：控制位数决定网格分辨率；重复实验只在能重复制备相同本征态、噪声近似独立时提高统计置信度。

**复算。** 逐项代入

$$
\Pr(y)=\left[\frac{\sin(4\pi(1/3-y/4))}{4\sin(\pi(1/3-y/4))}\right]^2
$$

得到上述精确值，小数和为 1.0000。

**局限。** 未在本章推导任意目标精度、任意失败概率所需的附加控制位公式，以免把入门主线变成尾界证明；正文已经说明可以增加控制位并舍弃低位。也没有把独立重复公式套到存在漂移或相关噪声的设备。

### 2.2 第 7 章：Grover “过度旋转”和未知 $M$ 只有口头提醒

**原问题。** 原文给出 $p_k=\sin^2((2k+1)\theta)$，但“未知解数会错过峰值”没有数值例，读者无法判断错用唯一解迭代数究竟会损失多少。

**新增内容。** 对 $N=16$ 同时列出 $M=1$ 与 $M=4$、$k=0,\ldots,4$ 的成功率。关键对比是：

- $M=1,k=3$ 时 $p_3\approx0.9613$；
- 实际 $M=4$ 却仍取 $k=3$ 时，$p_3=0.25$；
- $M=4,k=1$ 时反而有 $p_1=1$。

正文又补出 Boyer–Brassard–Høyer–Tapp 的可执行轮廓：逐步增大上限、在 $0$ 至 $m-1$ 中随机选迭代次数、测量后经典验证。在 $M>0$ 时期望查询量为 $O(\sqrt{N/M})$；$M=0$ 时必须设停止规则，并把“未找到”与数学上的不存在证明区分开。

**复算。** $M=1$ 时 $\theta=\arcsin(1/4)$，表中五项为 $0.0625,0.47265625,0.90844727,0.96131897,0.58170414$；$M=4$ 时 $\theta=\pi/6$，五项为 $0.25,1,0.25,0.25,1$。

**局限。** 没有展开未知解数算法的常数因子证明，也没有把固定点搜索误写成与标准 Grover 完全相同的资源曲线。这里的保证仍是 oracle 查询复杂度，不是数据库端到端墙钟时间。

### 2.3 第 7 章：Simon 的 $O(n)$ 样本数缺少由来

**原问题。** 原文从三比特例直接跳到“约 $O(n)$ 个样本”，没有说明重复样本和零向量为何不会改变渐近阶，也没有说明 $n-1$ 次抽样不等于必然得到 $n-1$ 条独立方程。

**新增内容。** 对 $s=110$，明确写出

$$
s^\perp=\{000,001,110,111\}.
$$

从秩 0 到秩 1 的成功概率为 $3/4$，期望等待 $4/3$ 次；从秩 1 到秩 2 的成功概率为 $1/2$，期望等待 2 次，所以满秩平均需要 $10/3$ 次。一般 $d=n-1$ 维时，当前秩为 $r$ 的升秩概率是 $1-2^{r-d}$，故

$$
\mathbb E[T]=\sum_{r=0}^{d-1}\frac1{1-2^{r-d}}=d+O(1)=O(n).
$$

并明确查询后仍有 $\mathbb F_2$ 高斯消元的经典成本。

**局限。** 这里给的是期望样本数，不是高概率尾界；若要把失败概率压到指定 $\delta$，还需额外样本和相应尾界。该指数查询分离仍依赖 Simon 承诺和黑盒模型。

### 2.4 第 8 章：VQE 只有 $1/\sqrt S$ 量级，没有可执行 shots 预算

**原问题。** 原文虽说明每项标准差至多 $1/\sqrt S$，但没有把 Hamiltonian 系数、不同测量组的 shots 分配和置信区间合在一次数值计算里。

**新增内容。** 沿用 $H=0.7Z+0.2X$，推得独立测量组的最坏情形方差界

$$
\operatorname{Var}(\widehat E)\le\frac{0.49}{S_Z}+\frac{0.04}{S_X}.
$$

固定 $S_Z+S_X=S$ 时，最优分配为 $S_Z:S_X=7:2$，因此方差界为 $0.81/S$。用明确标注为“实验规划”的正态近似，使 95% 区间半宽不超过 0.02，需要

$$
S\ge\left(\frac{1.96\times0.9}{0.02}\right)^2=7779.24,
$$

故示例取 7780 次，约分配为 $S_Z=6051,S_X=1729$。代回得到标准差上界约 0.010204，乘 1.96 后约 0.019999。

**局限。** 这是最坏方差界加正态近似的规划数，不是严格有限样本保证，更不是完整 VQE 成本。它未计入状态相关的真实方差、偏差、漂移、协方差、缓解倍率和优化器访问的多个参数点；正文已逐项注明。

## 3. 第 16 章审查结论

第 16 章现有内容已包含：查询下界与模型边界、HSP 骨架、量子行走、LCU/block encoding/qubitization/QSP/QSVT 的关系与最小 QSP 算例、算法级精度预算、层析/classical shadows/验证信任模型。其相位、搜索和测量前提也分别回链到第 6–8 章。本轮没有发现能在不重复既有材料的情况下达到同等优先级的真实跳步，因此未为追求改动数量而增写。

## 4. 一致性与回归检查

- 四处新增公式均已独立数值复算；QPE 概率和为 1，Grover 表由同一 $p_k$ 公式生成，VQE 分配代回满足目标半宽。
- 第 6、7、8 章自检题数仍分别为 8、10、8；未修改题号或答案锚点。
- 未修改任何 Mermaid 块，避免与离线 HTML 渲染修复并发冲突。
- 未修改 `handbook/16-advanced-algorithms-verification.md`，原因见上一节；不是漏审。
- 新增两条章内参考起点：Cleve 等相位估计论文、Boyer 等量子搜索论文。Simon 和 Peruzzo 原始论文已存在于对应章节参考起点，未重复添加。

## 5. 本轮结论

本轮修复 4 个可复算性缺口，没有发现需要更正的 P0 事实错误。改动集中在“有限精度输出是什么”“错误迭代数会怎样”“$O(n)$ 从哪里来”“统计精度要付多少 shots”四个初学者最容易只记结论、无法跟算的位置。保留的限制均已在正文紧邻公式处说明，没有把查询复杂度、正态近似或理想独立采样外推为设备端到端保证。
