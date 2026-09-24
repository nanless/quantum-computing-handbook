# 第 22 轮：基础数学、测量与约化态调研修订

审阅与修订日期：2026-09-22

## 1. 范围与方法

本轮先完整阅读 `handbook/STYLE.md`，再逐段复核第 01–05 章，重点检查：

- 术语首次出现时是否先给直观含义，再给数学定义；
- 一般测量是否被误缩成“每个结果一个 Kraus 算子”；
- Born 概率、条件后态与非选择后态是否写明各自条件；
- 旋转门的矩阵指数是否跳过关键代数；
- 偏迹是否只给形式计算，却没有说明其局域统计意义；
- 抽象定义后是否有初学者可独立复算的二维或四维例子。

按任务边界，本轮只修改了：

- `handbook/02-single-qubit.md`
- `handbook/03-multiple-qubits.md`
- `handbook/05-noise-channels.md`

`handbook/01-math.md` 已完整复核但未修改：其中条件概率已经明确写出 $\Pr(B)>0$，也已区分“知道经典记录后的概率更新”和“测量造成的物理反作用”。为避免无意义扩篇，本轮保留原文。

## 2. 权威来源与支持范围

以下来源均在 2026-09-22 访问。

| 来源 | 发布信息 | 本轮用于核对的范围 |
|---|---|---|
| John Watrous, [*The Theory of Quantum Information*](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf) | 作者官网公开的 2018 年稿，Cambridge University Press 出版前版本 | §2.1.3 对约化态和偏迹的定义；§2.2 的完全正映射与 Kraus 表示；§2.3，尤其书中第 112–113 页对 quantum instrument 的定义：每个结果对应完全正映射，所有结果之和为信道，概率是该分支输出的迹，条件态需除以正概率。 |
| E. B. Davies and J. T. Lewis, [“An operational approach to quantum probability”](https://doi.org/10.1007/BF01647093) | *Communications in Mathematical Physics* 17, 239–260，1970-09 | 原始论文中 instrument 同时概括 observable 与 operation，支持“POVM 统计”与“包含后态的完整测量过程”必须分开。 |
| K. Kraus, [“General state changes in quantum theory”](https://doi.org/10.1016/0003-4916(71)90108-4) | *Annals of Physics* 64(2), 311–335，1971-06 | 一般量子状态变化和操作和表示的原始来源；用于核对多 Kraus 分支、完全正操作以及确定性过程的完备关系。 |
| IBM Quantum Learning, [Mathematical formulations of measurements](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/general-measurements/formulations-of-measurements) | 官方在线课程，访问版本无独立发布日期 | 明确区分只输出经典结果的 POVM 描述与还保留测后量子系统的非破坏测量；用于核对教学顺序和 Born 概率表述。 |
| IBM Quantum Learning, [Data encoding：Angle encoding](https://quantum.cloud.ibm.com/learning/en/courses/quantum-machine-learning/data-encoding) | 官方在线课程，访问版本无独立发布日期 | 明确给出 $R_y(\theta)|0\rangle=\cos(\theta/2)|0\rangle+\sin(\theta/2)|1\rangle$；用于交叉核对半角和 $R_y(\pi/2)|0\rangle=|+\rangle$。 |
| John Preskill, [Ph/CS 219 Quantum Computation, Fall 2021](https://www.preskill.caltech.edu/ph219/ph219_2021-22.html) | Caltech 官方课程页；所列密度矩阵、广义测量和信道讲义为 2020 年课程材料 | 用于核对适合研究生入门的知识顺序：密度算符 → 广义测量 → 量子信道，而不是在 POVM 处暗中假定唯一的测后状态。 |

## 3. 真实问题、修复与复算证据

### 3.1 [P1，已修复] 一般测量被单 Kraus 特例遮住

**发现**

第 02 章原文先说“更一般的结果概率”，随后用 $E_k=M_k^\dagger M_k$ 和 $M_k\rho M_k^\dagger$ 描述后态，最后才用一句话说明“更一般时一个结果可对应多个 Kraus 算子”。第 05 章又把“一般测量算子 $M_k$”写成每个结果一个算子。公式本身是合法特例，但标题和叙述容易让初学者把特例误当完整定义，也无法直接表达同一实验记录下存在未分辨微观分支的情形。

**修复**

在第 02 章把一般有限维测量直接定义成量子测量工具：

$$
\mathcal I_k(\rho)=\sum_\alpha M_{k\alpha}\rho M_{k\alpha}^\dagger,
\qquad
\sum_{k,\alpha}M_{k\alpha}^\dagger M_{k\alpha}=I.
$$

并逐步推出

$$
E_k=\sum_\alpha M_{k\alpha}^\dagger M_{k\alpha},
\qquad
p(k)=\operatorname{Tr}[\mathcal I_k(\rho)]
=\operatorname{Tr}(E_k\rho).
$$

条件后态只在 $p(k)>0$ 时写成 $\rho_k=\mathcal I_k(\rho)/p(k)$；丢弃结果时写成 $\rho'=\sum_k\mathcal I_k(\rho)$。第 05 章同步改成完全正、迹不增加的分支映射，明确只有分支总和才是 CPTP 的确定性过程。

**新增可复算例证**

对同一个计算基 POVM，比较：

$$
M_0=|0\rangle\langle0|,\quad M_1=|1\rangle\langle1|
$$

与

$$
N_0=|0\rangle\langle0|,\quad N_1=|0\rangle\langle1|.
$$

逐项有 $M_k^\dagger M_k=N_k^\dagger N_k=E_k$，所以输入 $|+\rangle$ 时两种装置都以 $1/2$、$1/2$ 报告 0、1。第一种装置丢弃记录后输出 $I/2$；第二种装置的两个分支都输出 $|0\rangle$，故丢弃记录后输出 $|0\rangle\langle0|$。这直接证明“相同 POVM 不决定相同测量反作用”。

### 3.2 [P2，已修复] 旋转指数公式跳过了最关键的一步

**发现**

第 02 章原来直接写

$$e^{-i\theta\sigma_j/2}
=\cos(\theta/2)I-i\sin(\theta/2)\sigma_j,$$

没有解释矩阵指数为何会化成三角函数，也没有一个数值角度例子。初学者容易把它当作需背诵的特殊公式，或误把 Bloch 球转角 $\theta$ 写成态振幅中的 $\theta$ 而非 $\theta/2$。

**修复**

利用 $\sigma_j^2=I$，把指数级数拆成偶数项与奇数项，分别认出余弦级数和正弦级数。随后显式写出

$$
R_y(\theta)=
\begin{bmatrix}
\cos(\theta/2)&-\sin(\theta/2)\\
\sin(\theta/2)&\cos(\theta/2)
\end{bmatrix}
$$

以及

$$
R_y(\pi/2)|0\rangle
=\frac1{\sqrt2}(1,1)^T=|+\rangle.
$$

复算时 $\cos(\pi/4)=\sin(\pi/4)=1/\sqrt2$，输出范数为 $1/2+1/2=1$；这也把“Bloch 向量转 $\pi/2$”与“振幅使用 $\pi/4$ 半角”明确接上。

### 3.3 [P2，已修复] 偏迹只有 Bell 极端例，缺少局域统计含义

**发现**

第 03 章原文已经正确逐项计算 Bell 态的偏迹，但只有 $I/2$ 这一极端结果。读者可能形成两个误解：偏迹只是某种删矩阵元的技巧；或任何纠缠纯态的单边约化态都是最大混态。

**修复**

加入偏迹的操作意义：对任意局域可观察量 $O_A$，

$$
\operatorname{Tr}[(O_A\otimes I_B)\rho_{AB}]
=\operatorname{Tr}(O_A\rho_A),
\qquad \rho_A=\operatorname{Tr}_B\rho_{AB}.
$$

它说明 $\rho_A$ 保存 Alice 单独可测到的全部统计，而不是任意删去信息。

新增部分纠缠例子

$$
|\psi\rangle=\frac{\sqrt3}{2}|00\rangle+\frac12|11\rangle,
\qquad
\rho_A=\operatorname{diag}(3/4,1/4).
$$

两种路径都给出局域 $Z$ 期望 $1/2$：

$$
\langle\psi|(Z\otimes I)|\psi\rangle
=\frac34-\frac14=\frac12,
$$

$$
\operatorname{Tr}(Z\rho_A)
=\frac34-\frac14=\frac12.
$$

同时 $\operatorname{Tr}(\rho_A^2)=9/16+1/16=5/8<1$，故局部态确为混态；但它不等于 $I/2$，排除了“纠缠必然使局部最大混合”的错误泛化。后文原来的 Bell 态结论也改成“回到前面的 Bell 态”，避免指代到新增例子。

## 4. Born 条件与一致性检查

- 第 01 章条件概率保留了 $\Pr(B)>0$。
- 第 02 章投影条件态明确说明 $p(k)=0$ 时结果不发生、无需定义后态。
- 第 02 与第 05 章的一般量子测量工具都只在 $p(k)>0$ 时定义条件后态。
- 对丢弃测量结果的情况，两章统一写成所有分支之和，不再把某个条件分支误当非选择输出。
- 一般定义、单 Kraus 特例和投影测量特例的包含关系已显式写出。

## 5. 未完成项与边界

本轮没有遗留的 P0、P1 或 P2 问题。以下内容是有意不做，而非遗漏：

- 未新增或改写自检题，四章现有题数不变；因此共享练习答案无需同步变更。
- 未在第 01 章重复添加 Born 规则，因为第 01 章负责经典条件概率，第 02 章负责量子测量，当前顺序更清楚。
- 未扩展到连续结果 POVM、无限维测量、Naimark 扩张或测量模型的实验辨识；这些超出本轮的入门基础边界。
- 未修改 README、共享附录、术语表、审校日志或其他章节。

## 6. 结论

本轮完成了 3 项有实质教学价值的修订：一般量子测量从单 Kraus 特例提升到完整 instrument 定义；旋转指数从结论补成可逐项核算的推导；偏迹从 Bell 态形式计算补成局域统计定理和部分纠缠数值例。新增公式与算例均可在二维或四维内手算，自检题数和原有学习路线未改变。
