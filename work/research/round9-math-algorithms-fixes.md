# 第 9 轮：算法数学问题修订与复算记录

日期：2026-09-22

## 1. 范围与结论

本轮依据 `work/research/round8-cross-math-algorithms-audit.md`，只修改以下五个正文文件：

- `handbook/06-algorithmic-primitives.md`
- `handbook/07-algorithms.md`
- `handbook/08-applications.md`
- `handbook/10-error-correction.md`
- `handbook/16-advanced-algorithms-verification.md`

没有修改 `handbook/appendices/exercises.md`、`handbook/appendices/audit-log.md`、共享附录或 `sources/`。第 8 轮列出的正文 P0=2、P1=2、P2=7 均已落实；附录中需要总编同步的两处答案列在第 6 节。

## 2. P0 修订

### P0-1｜block encoding 定义恢复归一化因子

文件：`handbook/16-advanced-algorithms-verification.md`，5.3 节。

把损坏的

```tex
A-alpha(\langle0^a|\otimes I)U(|0^a\rangle\otimes I)
```

改成

```tex
A-\alpha(\langle0^a|\otimes I)U(|0^a\rangle\otimes I).
```

复核：这与本节采用的 $(\alpha,a,\epsilon)$ block encoding 约定一致，也与后文的 $\alpha t$、$\alpha/\Delta$、$\alpha\kappa$ 复杂度依赖一致。全文搜索已无 `A-alpha` 残留。

依据：A. Gilyén et al., [Quantum Singular Value Transformation and Beyond](https://arxiv.org/abs/1806.01838)（2018）；G. H. Low and I. L. Chuang, [Hamiltonian Simulation by Qubitization](https://quantum-journal.org/papers/q-2019-07-12-163/)（2019）。访问日期：2026-09-22。

### P0-2｜统一平方重叠与根保真度

文件：`handbook/16-advanced-algorithms-verification.md`，7.4、7.5 与自检第 10 题。

修改如下：

1. 用 $f=\langle\psi|\rho|\psi\rangle$ 表示纯目标态的平方重叠。
2. 明写本书根保真度约定 $F(\rho,|\psi\rangle)=\sqrt f$。
3. 能量—能隙界统一改成基态占据 $f_0$：
   $$
   f_0\ge1-\frac{E-E_0}{\Delta}.
   $$
4. 说明非简并纯基态下 $F_0=\sqrt{f_0}$；若基态简并，该式约束的是整个基态子空间占据，不能直接解释为与某个指定纯基态的保真度。
5. 手算例改为 $f_0\ge0.75$，根保真度 $F_0\ge\sqrt{0.75}\approx0.866$。
6. 自检题明确分别询问“占据下界”和“根保真度下界”。

独立复算：$\sqrt{0.75}=0.8660254\ldots$；自检数据将给出 $f_0\ge1-0.03/0.20=0.85$ 与 $F_0\ge\sqrt{0.85}=0.9219544\ldots$。

依据：Flammia–Liu 的直接保真度估计使用平方约定，正文已提醒读者转换到本书的根保真度约定。S. T. Flammia and Y.-K. Liu, [Direct Fidelity Estimation from Few Pauli Measurements](https://arxiv.org/abs/1104.4695), *Physical Review Letters* 106, 230501 (2011)。访问日期：2026-09-22。

## 3. P1 修订

### P1-1｜区分 HSP 的条件纯态与非选择混态

文件：`handbook/16-advanced-algorithms-verification.md`，3.1 节及流程图。

正文现在分别写出：

- 测量输出并按结果条件化：得到纯陪集态 $|gH\rangle$；
- 丢弃输出寄存器：得到
  $$
  \rho_H=\frac1{|G/H|}\sum_{gH\in G/H}|gH\rangle\langle gH|.
  $$

同时说明二者在只测输入寄存器时具有相同的 Fourier 采样统计。流程图的节点也由含混的“随机陪集态”改成“条件纯陪集态或非选择陪集混态”。

复核：$|G|$ 个均匀群元素按 $|G/H|$ 个陪集、每个 $|H|$ 个元素分组，故每个正交陪集态的混合权重是 $|H|/|G|=1/|G/H|$，归一化正确。

### P1-2｜明确 Eastin–Knill 不只排除连续门集

文件：`handbook/10-error-correction.md`，9 节。

在准确的原正文后补充：定理也排除离散但通用的纯横向逻辑门集；它限制的是固定编码上完全依赖横向门实现通用性，不否定单个横向门和魔法态、码切换、规范固定等非横向容错机制。

依据：B. Eastin and E. Knill, [Restrictions on Transversal Encoded Quantum Gate Sets](https://doi.org/10.1103/PhysRevLett.102.110502), *Physical Review Letters* 102, 110502 (2009)。

## 4. P2 修订

### P2-1｜相位 oracle 的寄存器数消歧

文件：`handbook/06-algorithmic-primitives.md`，1 节。

标题改为“两个输入比特的手算”，结果标注为

$$
|-\rangle_{x_1}|-\rangle_{x_2}|-\rangle_y,
$$

并说明线路共三个量子比特：两个输入位与一个 oracle 目标位。

### P2-2｜补 QPE 非精确相位的概率公式与数值例

文件：`handbook/06-algorithmic-primitives.md`，6 节。

新增 $M=2^t$ 时的测量概率

$$
\Pr(y)=\left[
\frac{\sin(\pi M(\phi-y/M))}
{M\sin(\pi(\phi-y/M))}
\right]^2,
$$

最近网格点的标准下界 $4/\pi^2\approx0.405$，以及 $\phi=1/3,t=2$ 的手算：最近输出 $y=1$，

$$
\Pr(1)=\left[\frac{\sin(\pi/3)}{4\sin(\pi/12)}\right]^2
=0.6997595\ldots\approx0.700.
$$

标题同步改为“三个手算例子”。正文还说明增加置信位与舍去多余低位的作用，避免把“$t$ 位寄存器”误读成“必定输出 $t$ 位精确相位”。

依据：IBM Quantum Learning, [Phase estimation and factoring](https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring)。访问日期：2026-09-22。

### P2-3｜增加 Shor 成功概率账本

文件：`handbook/07-algorithms.md`，新增 3.4 节，原复杂度节顺延为 3.5。

新增表格依次列出：随机 $a$ 的 gcd 分支、偶数阶与非平凡平方根条件、Fourier 峰、$\gcd(k,r)>1$ 导致约分、候选模幂验证与重试。明确指出：

- 对含至少两个不同素因子的奇合数，随机互素 $a$ 通过经典约化中“偶数阶且非平凡平方根”检查的概率至少为 $1/2$；
- 完整单轮成功率还依赖相位精度以及 $k$ 与 $r$ 的互素性，不能写成脱离输入结构的固定百分比；
- 每个失败分支都可检测，重复后的期望轮数仍为位长的多项式，结果可经典验证。

补入成功概率的直接参考：G. Leander, [Improving the Success Probability for Shor's Factoring Algorithm](https://arxiv.org/abs/quant-ph/0208183)（2002）；原始算法引用仍为 P. W. Shor, [SIAM J. Comput. 26, 1484–1509](https://doi.org/10.1137/S0097539795293172)（1997）。

### P2-4｜量子幅度估计术语与资源参数

文件：`handbook/07-algorithms.md`，6 节。

把“经典幅度估计定理”改成“标准 QPE 型量子幅度估计定理”，并定义 $M$ 是相位网格大小/受控 Grover 幂覆盖的资源尺度，总 $Q$ 调用数为 $O(M)$。保留原来正确的 $8/\pi^2$ 成功概率和误差界。

依据：G. Brassard et al., [Quantum Amplitude Amplification and Estimation](https://arxiv.org/abs/quant-ph/0005055)（提交于 2000-05-15）。

### P2-5｜补全单边 QAOA 的中间代数

文件：`handbook/08-applications.md`，3 节。

新增代价层状态、$e^{-i\beta X}=\cos\beta I-i\sin\beta X$、奇宇称振幅

$$
A_{01}=A_{10}
=\frac12\left[-i\sin(2\beta)+e^{-i\gamma}\cos(2\beta)\right],
$$

并由 $|A_{01}|^2+|A_{10}|^2$ 逐步得到

$$
\langle C\rangle
=\frac12[1+\sin(4\beta)\sin\gamma].
$$

复核：$\beta=\pi/8,\gamma=\pi/2$ 时 $\sin(4\beta)=\sin\gamma=1$，故 $\langle C\rangle=1$；两个奇宇称串总概率为 1。推导中的正号与本节 $e^{-i\beta B}e^{-i\gamma C}$ 的符号约定一致。

### P2-6｜补 element distinctness 匹配下界来源

文件：`handbook/16-advanced-algorithms-verification.md`，4.3 节与参考起点。

正文明确标注 Shi 的 $\Omega(N^{2/3})$ 查询下界，并新增原始论文：Y. Shi, [Quantum lower bounds for the collision and the element distinctness problems](https://arxiv.org/abs/quant-ph/0112086)（提交于 2001-12-15；FOCS 2002）。这与 Ambainis 的 $O(N^{2/3})$ 上界配成匹配界。

### P2-7｜补 Trotter 条件、范数与 no-fast-forwarding 来源

文件：`handbook/07-algorithms.md`，4 节与参考起点。

公式前明确 $A,B$ 是有限维空间上的有界 Hermitian 算符，$\|\cdot\|$ 是谱范数；补充 no-fast-forwarding 是 oracle 模型的一般下界，不排除有特殊结构的快速模拟。新增两条直接来源：

- A. M. Childs et al., [Theory of Trotter Error with Commutator Scaling](https://doi.org/10.1103/PhysRevX.11.011020), *Physical Review X* 11, 011020 (2021)；
- D. W. Berry, G. Ahokas, R. Cleve, B. C. Sanders, [Efficient Quantum Algorithms for Simulating Sparse Hamiltonians](https://arxiv.org/abs/quant-ph/0508139), *Communications in Mathematical Physics* 270, 359–371 (2007)。

复算：对 $A=X,B=Z$，$[X,Z]=-2iY$，故 $\|[X,Z]\|=2$；$t=0.2,r=4$ 时上界为

$$
\frac{t^2}{2r}\|[X,Z]\|=\frac{0.04}{8}\times2=0.01.
$$

若要求不超过 $2\times10^{-3}$，则 $0.04/r\le0.002$，得到 $r\ge20$，与现有自检答案应有的数值一致。

## 5. 总体一致性复核

完成修改后进行全文定向搜索与独立数值复算：

- `A-alpha`：0 处；
- “经典幅度估计”：0 处；
- 原“两比特手算”标题：0 处；
- 把 $\langle\psi|\rho|\psi\rangle$ 直接记作根保真度 $F$：0 处；
- HSP 流程图的含混“随机陪集态”：0 处；
- Shor 小节编号连续为 3.1–3.5；
- QPE 数值概率、QAOA 振幅、Trotter 上界与根保真度平方根均重新计算通过。

## 6. 需由总编同步的附录答案

本轮按任务边界没有修改练习附录。为避免正文与答案错位，总编还需统一以下两处：

1. `handbook/appendices/exercises.md` 第 10 章答案 6：删除把 Eastin–Knill 限制为“连续的”门集的措辞，改成不存在通用的纯横向编码门集；离散通用门集也不能绕过。
2. 同文件第 16 章答案 10：同时给出基态占据 $f_0\ge0.85$ 与本书根保真度 $F_0\ge\sqrt{0.85}\approx0.922$，并列出能隙、可靠能量上界和非简并假设；简并时只界定基态子空间总占据。

第 8 章答案 2 的最终公式仍正确；若总编希望答案与正文的“完整手算”同等详细，可同步加入 $A_{01}=A_{10}$ 的中间式，但这不是数值纠错。

## 7. 本轮剩余风险

正文范围内，第 8 轮列出的 P0/P1/P2 已全部处理，未发现新的数学冲突。剩余风险仅是上述附录答案尚待总编同步；该项不在本轮授权修改范围内。
