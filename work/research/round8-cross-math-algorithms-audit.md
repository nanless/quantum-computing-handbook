# 第 8 轮交叉审稿：算法、纠错与验证的数学审计

日期：2026-09-22

## 1. 审稿范围与结论

按更正后的实际文件名，本轮只读审阅：

- `handbook/06-algorithmic-primitives.md`
- `handbook/07-algorithms.md`
- `handbook/08-applications.md`
- `handbook/10-error-correction.md`
- `handbook/16-advanced-algorithms-verification.md`
- `handbook/appendices/exercises.md` 的第 6、7、8、10、16 章答案

未修改任何 `handbook/` 文件。

本轮发现：

| 等级 | 数量 | 结论 |
|---|---:|---|
| P0 | 2 | 必须修复：block encoding 定义损坏；根保真度约定冲突并导致练习数值口径错误 |
| P1 | 2 | 必须修复：忽略输出寄存器与条件陪集态混写；Eastin–Knill 答案缩窄定理范围 |
| P2 | 7 | 推导跳步、成功概率铺垫、术语和引用精度问题 |

指定答案条目数与正文自检题数一致：第 6、7、8、10、16 章分别为 8、10、8、9、10 题，共 45 题。除下述根保真度答案与 Eastin–Knill 措辞外，数值题复算一致。

## 2. P0：必须修复的数学或约定错误

### P0-1｜block encoding 定义中的 `\alpha` 丢失

**位置**：`handbook/16-advanced-algorithms-verification.md`，5.3 节，约第 319–327 行。

当前公式为

```tex
\left\|A-alpha
(\langle0^a|\otimes I)U(|0^a\rangle\otimes I)
\right\|\le\epsilon.
```

`alpha` 既没有反斜杠，也会被渲染成一串变量乘积，因而该定义在数学上和版面上都损坏。建议改为

```tex
\left\|A-\alpha
(\langle0^a|\otimes I)U(|0^a\rangle\otimes I)
\right\|\le\epsilon.
```

等价地也可写左上块与 $A/\alpha$ 的距离不超过 $\epsilon/\alpha$，但必须与本节采用的 $(\alpha,a,\epsilon)$ 约定一致。Gilyén 等人的 QSVT 原论文和 Low–Chuang 的 qubitization 框架均要求明确归一化因子；本节后文关于 $\alpha t$、$\alpha/\Delta$、$\alpha\kappa$ 的讨论也依赖这个定义。

**证据**：A. Gilyén et al., *Quantum Singular Value Transformation and Beyond*, 2018，[arXiv:1806.01838](https://arxiv.org/abs/1806.01838)；G. H. Low and I. L. Chuang, *Hamiltonian Simulation by Qubitization*, 2019，[Quantum 3, 163](https://quantum-journal.org/papers/q-2019-07-12-163/)。访问日期：2026-09-22。

### P0-2｜第 16 章把平方重叠写成根保真度，练习答案随之错用数值

**位置**：

- `handbook/16-advanced-algorithms-verification.md` 7.4 节，约第 523–531 行；
- 同文件 7.5 节，约第 533–556 行；
- 同文件自检第 10 题，约第 591 行；
- `handbook/appendices/exercises.md` 第 16 章答案 10，约第 332–334 行。

全书第 13 章明确采用根保真度

$$
F(\rho,\sigma)=\operatorname{Tr}\sqrt{\sqrt\rho\,\sigma\sqrt\rho}.
$$

当目标为纯态时，根保真度是

$$
F(\rho,|\psi\rangle\langle\psi|)
=\sqrt{\langle\psi|\rho|\psi\rangle}.
$$

但第 16 章 7.4 直接写成

$$F=\langle\psi|\rho|\psi\rangle,$$

这是根保真度的平方。7.5 的能量—能隙推导实际下界也是**基态占据/平方重叠**，不是根保真度本身。于是练习答案把

$$1-0.03/0.20=0.85$$

称为“根保真度至少 0.85”。按全书约定，正确区分应是：

$$
f_0:=\langle E_0|\rho|E_0\rangle\ge0.85,
\qquad
F(\rho,|E_0\rangle\langle E_0|)\ge\sqrt{0.85}\approx0.922.
$$

若基态简并，则 $f_0=\operatorname{Tr}(P_0\rho)$ 是整个基态子空间占据；此时应避免把它直接写成与某一个纯态的根保真度。

**可执行修改**：全节把平方重叠统一记为 $f$ 或 $f_0$；在 7.4 明写“按本书约定，根保真度为 $F=\sqrt f$”；自检题明确问“基态占据（平方保真度）”还是“根保真度”，答案同时给出 $0.85$ 与 $\sqrt{0.85}$。

**证据**：Flammia–Liu 的直接保真度估计论文采用平方约定，并在纯目标态下写 $F=\operatorname{Tr}(\rho\sigma)$；这正说明引用该论文时必须翻译到本书的根保真度约定。S. T. Flammia and Y.-K. Liu, *Direct Fidelity Estimation from Few Pauli Measurements*, published 2011-06-08，[APS](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.106.230501)，[arXiv:1104.4695](https://arxiv.org/abs/1104.4695)。访问日期：2026-09-22。

## 3. P1：会形成错误模型的表述

### P1-1｜“测量或忽略输出寄存器”没有区分纯条件态与混合非选择态

**位置**：`handbook/16-advanced-algorithms-verification.md` 3.1 节，约第 118–125 行；流程图约第 163–170 行。

当前写“测量或忽略输出寄存器，可得到随机陪集态 $|gH\rangle$”。两种操作的后续 Fourier 测量统计可以相同，但状态描述不同：

- 测量输出并条件于某个结果：第一寄存器是一个纯陪集态 $|gH\rangle$；
- 不读结果并对输出寄存器做偏迹：第一寄存器是陪集态的经典混合
  $$
  \rho_H=\frac1{|G/H|}\sum_{gH}|gH\rangle\langle gH|.
  $$

建议正文明确写出这两个分支，再说明二者做群 Fourier 变换后对 $H^\perp$ 的采样分布相同。这样与第 02、03、05 章已经建立的“条件态/非选择态”约定一致。

Ettinger–Høyer–Knill 的结论本身被正确转述：任意有限群 HSP 的查询数是 $\operatorname{poly}(\log|G|)$，但已知实现可耗指数时间。[原论文](https://arxiv.org/abs/quant-ph/0401083)，提交于 2004-01-14；访问日期：2026-09-22。

### P1-2｜练习答案把 Eastin–Knill 缩成“连续的、普适的”横向门集

**位置**：

- `handbook/10-error-correction.md` 9 节约第 279–283 行；
- `handbook/appendices/exercises.md` 第 10 章答案 6，约第 229 行。

正文“不能拥有一个通用的横向逻辑门集”准确；答案却改成排除“连续的、普适的横向逻辑门集合”。“连续的”这一额外限定会让初学者误以为某个离散但稠密的通用横向门集可能绕过定理。

建议答案与正文和原论文统一为：对能检测任意单物理子系统错误的非平凡有限维量子码，不存在通用的横向编码门集；定理不否认通过魔法态、码切换、规范固定等非纯横向机制实现通用容错计算。

**证据**：Eastin–Knill 原论文摘要明确写的是“incompatible with the existence of a universal, transversal encoded gate set”，没有把结论限制为连续门集。论文 2009-03-18 发表；[NIST 论文页与全文](https://www.nist.gov/publications/restrictions-transversal-encoded-quantum-gate-sets)。访问日期：2026-09-22。

## 4. P2：可执行的教学、推导与引用改进

### P2-1｜相位 oracle 的“两比特手算”实际含两个输入位和一个目标位

**位置**：`handbook/06-algorithmic-primitives.md` 1 节“两比特手算”，约第 51–60 行。

标题容易让初学者以为总共只有两个量子比特，而等式右侧实际有三个 ket：两个输入位加一个目标位。建议改成“两个输入比特的手算”，并标注

$$|-angle_{x_1}|-\rangle_{x_2}|-\rangle_y.$$

同时点明前两个 $| -\rangle$ 是符号模式的因式分解，最后一个是保持分离的 oracle 目标位。

### P2-2｜QPE 只说“概率集中”，没有给初学者可核查的成功概率

**位置**：`handbook/06-algorithmic-primitives.md` 6 节，约第 241–258 行。

精确二进制例子正确，但非精确相位只给定性描述。建议补一个 $t=2$ 的非精确例子，逐项计算逆 QFT 后的概率，或至少给出“测得最近整数”的标准常数下界及增加若干控制位如何把失败率降到目标值。必须说明所采用的输出舍入规则和“精度位/置信位”分工，避免读者以为 $t$ 位总能以高概率给出 $t$ 位精度。

### P2-3｜Shor 的失败分支列出了，但没有形成完整成功概率账本

**位置**：`handbook/07-algorithms.md` 3.1–3.4 节，约第 132–233 行。

正文正确列出 $r$ 为奇数、$a^{r/2}\equiv-1$、$\gcd(k,r)>1$ 和有限精度恢复失败，但没有把它们组织为“单轮成功概率—重复次数—验证”的资源账本。建议增加一个框：

1. 随机选择 $a$ 可能直接通过 gcd 得因子；
2. 对合适复合数，随机 $a$ 产生可用偶数阶的概率有常数下界；
3. Fourier 样本恢复真阶还受 $k$ 与 $r$ 互素及近似精度影响；
4. 每个候选都用模幂验证，失败则独立重试，因此整体期望轮数仍为多项式。

不要给脱离 $N$ 类型和具体阶结构的单一“固定成功率”。Shor 原始分析和后续成功率研究都强调这些条件；例如 [Shor 1997](https://doi.org/10.1137/S0097539795293172) 与 [Leander 2002](https://arxiv.org/abs/quant-ph/0208183)。访问日期：2026-09-22。

### P2-4｜“经典幅度估计定理”措辞可能被理解为 classical

**位置**：`handbook/07-algorithms.md` 6 节，约第 349–357 行。

这里引用的是 Brassard 等人的标准/原始量子幅度估计定理，不是“经典算法的幅度估计”。建议把“经典幅度估计定理的一种写法”改成“标准 QPE 型量子幅度估计定理的一种写法”，并在 $M$ 首次出现时说明它对应的相位网格大小或 Grover 算符调用规模。

现有误差界和至少 $8/\pi^2$ 的常数成功概率与原始结果一致。[Brassard et al., arXiv:quant-ph/0005055](https://arxiv.org/abs/quant-ph/0005055)，提交于 2000-05-15；访问日期：2026-09-22。

### P2-5｜QAOA 小节名为“完整手算”，正文和答案却跳过核心代数

**位置**：

- `handbook/08-applications.md` 3 节，约第 142–172 行；
- `handbook/appendices/exercises.md` 第 8 章答案 2，约第 200–206 行。

公式

$$
\langle C\rangle=\frac12[1+\sin(4\beta)\sin\gamma]
$$

复算正确，$\beta=\pi/8,\gamma=\pi/2$ 时确得 1。但正文用“逐项展开，可得”，答案用“反向共轭并只保留非零项，可得”，都没有展示中间一步，不足以完成题目要求的“用矩阵或逐振幅方法验证”。

建议至少补出：

$$
e^{-i\gamma C}|++\rangle
=\frac12(|00\rangle+|11\rangle
+e^{-i\gamma}|01\rangle+e^{-i\gamma}|10\rangle),
$$

再写 $e^{-i\beta X}=\cos\beta I-i\sin\beta X$，展开两个比特的 mixer，最后由 $P_{01}+P_{10}$ 得到期望值。这样初学者能检查符号约定，而不是只能相信结果。

原始 QAOA 定义与符号来源：[Farhi–Goldstone–Gutmann, arXiv:1411.4028](https://arxiv.org/abs/1411.4028)，2014；访问日期：2026-09-22。

### P2-6｜element distinctness 的“匹配下界”没有对应原始引用

**位置**：`handbook/16-advanced-algorithms-verification.md` 4.3 节约第 231–239 行及参考起点。

Ambainis 引用支持 $O(N^{2/3})$ 量子行走上界，但“匹配已知查询下界”需要另引下界论文。建议加入 Yaoyun Shi 的原始下界：其论文明确推出 element distinctness 的 $\Omega(N^{2/3})$ 查询下界。

**证据**：Y. Shi, *Quantum lower bounds for the collision and the element distinctness problems*, submitted 2001-12-15，[arXiv:quant-ph/0112086](https://arxiv.org/abs/quant-ph/0112086)。访问日期：2026-09-22。

### P2-7｜具体 Trotter 界与 no-fast-forwarding 结论缺少直接支撑来源

**位置**：`handbook/07-algorithms.md` 4 节约第 245–295 行。

本轮复算：$[X,Z]=-2iY$、单步 BCH 的领先项 $it^2Y$、例题上界 $0.04/r$ 和答案 $r\ge20$ 均正确。但参考起点中的 Lloyd 1996 与截断 Taylor 论文不是本节所写“交换子范数乘积公式误差界”的最直接来源；no-fast-forwarding 也没有单独标出原始定理来源。

建议为具体不等式补入现代乘积公式误差论文，并为 no-fast-forwarding 单列原始来源；同时在公式前明确 $A,B$ 为有界 Hermitian 算符、范数为算符范数。可用：A. Childs et al., *Theory of Trotter Error with Commutator Scaling*, [Physical Review X 11, 011020 (2021)](https://doi.org/10.1103/PhysRevX.11.011020)。访问日期：2026-09-22。

## 5. 分域核验结果

### 第 06 章

- P0：0
- P1：0
- P2：2（寄存器标注；非精确 QPE 成功概率缺手算）
- 已复算通过：相位回踢、Deutsch–Jozsa 的 $A(0^n)$、BV 因式分解、四项 Grover、QFT$_4$、QPE 精确相位、Deutsch XOR 二次多项式、hybrid 的 $\Omega(\sqrt N)$ 量级。

### 第 07 章

- P0：0
- P1：0
- P2：3（Shor 成功概率账本；幅度估计措辞；Trotter/no-fast-forwarding 引用）
- 已复算通过：Simon 三比特例、Grover 迭代角、Shor 的 $N=15$ 与练习 $N=21$、一阶 Trotter 示例、HHL 输出形式、幅度估计 $a=1/2$ 双峰、复杂度类包含关系。

### 第 08 章

- P0：0
- P1：0
- P2：1（QAOA 标称完整手算但跳步）
- 已复算通过：$0.7Z+0.2X$ 的 VQE 最小值 $-\sqrt{0.53}$、单边 QAOA 公式、Pauli 估计标准差、核差异缩小四倍导致朴素 shots 增加十六倍。

### 第 10 章

- P0：0
- P1：1（练习答案缩窄 Eastin–Knill）
- P2：0
- 已复算通过：三比特码综合征、Shor 码字、Knill–Laflamme 条件、Steane 列综合征、$2d^2-1$ 旋转补丁计数的适用说明、示意阈值表、Ross–Selinger 主项和练习中约 60 个 T 门的增量。

### 第 16 章

- P0：2（block encoding 公式；根保真度/平方重叠）
- P1：1（纯条件陪集态与非选择混合态）
- P2：1（element distinctness 下界引用）
- 已复算通过：查询多项式次数、Deutsch XOR、Simon annihilator、四环 coined walk、LCU 权重、$T_2(A)$、误差预算、Pauli 阴影均值/方差、能量—能隙对**占据概率**的下界。

## 6. 引用支持度总评

现有主要引用整体可靠，并真正覆盖了核心陈述：Beals 等支持多项式方法；Ettinger–Høyer–Knill 支持“一般有限群 HSP 查询高效但时间可指数”；Ambainis 支持 element distinctness 上界；Low–Chuang 与 Gilyén 等支持 qubitization/QSVT；Huang–Kueng–Preskill 支持经典阴影；Haah 等支持一般态层析的 $d^2$ 级副本需求；Ross–Selinger 支持典型 $3\log_2(1/\epsilon)$ 主项；Eastin–Knill 支持无通用横向门集。

需要补强的只有三类：element distinctness 匹配下界、具体 Trotter 交换子界、no-fast-forwarding 原始定理。另有一类不是引用错误而是**约定翻译错误**：Flammia–Liu 使用平方保真度，本书采用根保真度，必须显式换算。

## 7. 建议修复顺序

1. 先修 P0-1 block encoding 公式。
2. 统一第 16 章正文与练习中的 $f$（平方重叠/占据）和 $F$（根保真度）。
3. 修正陪集态的条件/非选择描述和 Eastin–Knill 答案。
4. 补 QAOA 中间推导及 QPE/Shor 成功概率账本。
5. 最后补三条精确引用和术语润色。

