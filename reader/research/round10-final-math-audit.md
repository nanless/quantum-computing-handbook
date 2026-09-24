# 第 10 轮：全书数学终验

日期：2026-09-22

## 1. 范围、方法与结论

本轮只读复核全书正文、符号附录和练习答案，没有修改任何 `handbook/` 文件。重点逐式检查第 9 轮改动：

- QPE 非精确相位的概率分布与常数成功率；
- Shor 经典约化、成功概率账本和连分数恢复；
- 单边 MaxCut 的 QAOA 振幅展开；
- block encoding 定义；
- HSP 的条件纯陪集态与偏迹混态；
- 平方重叠 $f$、根保真度 $F$ 和能量—能隙证书；
- Eastin–Knill 定理边界与练习答案同步。

同时抽查第 01–05、10、13–16 章的线性代数、测量、密度矩阵、信道、纠错、熵与信息量、控制和验证公式，并逐题核对练习附录中的主要数值题。

终验计数：

| 等级 | 数量 | 结论 |
|---|---:|---|
| P0 | 0 | 未发现会使核心公式失效或答案相反的问题 |
| P1 | 0 | 未发现会形成错误物理/算法模型的实质问题 |
| P2 | 3 | 三处定义域或边界条件仍需补全 |

因此本轮**不能**写“本轮未发现问题”。三项均不改变现有手算结果，但会影响定义完整性或边界输入下的准确表述。

## 2. P2 问题

### P2-1｜QPE 的“最近整数”没有说明相位按模 1 环绕

**位置**：`handbook/06-algorithmic-primitives.md:245-259`。

正文的精确概率公式

$$
\Pr(y)=\left[
\frac{\sin(\pi M(\phi-y/M))}
{M\sin(\pi(\phi-y/M))}
\right]^2
$$

正确，$\phi=1/3,M=4,y=1$ 的例子也正确。但“输出最接近 $M\phi$ 的整数的概率至少为 $4/\pi^2$”在 $\phi$ 靠近 1 时需要按模 $M$ 理解。QPE 的相位在圆周 $\mathbb R/\mathbb Z$ 上：例如 $M=4,\phi=0.99$，普通意义下最接近 $M\phi=3.96$ 的整数是 4，却不在输出集合 $\{0,1,2,3\}$ 中；实际高概率输出是 $y=0$，因为 0 与 1 表示同一个模 1 边界。

独立代入现有公式得到

$$
\Pr(y=0)\approx0.9951,
\qquad
\Pr(y=3)\approx0.0021.
$$

**可执行修改**：把相关两句改为“输出圆周距离下最接近 $\phi$ 的网格点 $y/M$，等价于最接近 $M\phi$ 的模 $M$ 整数”；或明确误差用

$$
\min_{k\in\mathbb Z}|\phi-y/M-k|
$$

度量。这样 $4/\pi^2$ 下界才覆盖 $\phi\approx1$ 的环绕边界。

来源：IBM Quantum Learning, [Phase estimation and factoring](https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring)。访问日期：2026-09-22。

### P2-2｜Shor 成功账本缺少“完美幂预处理”这一输入分支

**位置**：`handbook/07-algorithms.md:132-155,222-234`。

表格已经正确限定：当奇合数含至少两个不同素因子时，随机互素 $a$ 产生可用偶数阶和非平凡平方根的概率至少为 $1/2$。但本节开头把输入写成任意奇合数，随后第 234 行概括“重复次数的期望仍为输入位长的多项式”，却没有说明完美幂 $N=p^m$ 要先用经典多项式时间方法识别并约化。

这不是装饰条件。对素数幂，模 $N$ 的平方根结构与“至少两个不同素因子”的计数论证不同，不能直接套用表中 $1/2$ 下界。标准 Shor 约化先排除偶数、素数和完美幂，再对至少含两个不同素因子的奇合数使用阶寻找。

**可执行修改**：在 3.1 的步骤 1 前加入：“先用经典算法检查 $N$ 是否为素数或完美幂；素数直接结束，若 $N=b^m$ 则递归分解底数 $b$。”在 3.4 总结中把多项式期望重复的结论明确绑定到这个预处理后的输入。

来源：P. W. Shor, [Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer](https://doi.org/10.1137/S0097539795293172), *SIAM Journal on Computing* 26, 1484–1509 (1997)，原分析明确把非素数幂情形交给阶寻找，并指出素数幂可经典高效处理；G. Leander, [Improving the Success Probability for Shor's Factoring Algorithm](https://arxiv.org/abs/quant-ph/0208183)（2002）。访问日期：2026-09-22。

### P2-3｜block encoding 定义未给参数域和范数类型

**位置**：`handbook/16-advanced-algorithms-verification.md:325-335`。

第 9 轮已经把主公式修正为

$$
\left\|A-\alpha
(\langle0^a|\otimes I)U(|0^a\rangle\otimes I)
\right\|\le\epsilon,
$$

公式本身正确。但定义没有说明：

- $\alpha>0$；
- $a\in\mathbb Z_{\ge0}$ 是辅助量子比特数；
- $\epsilon\ge0$；
- $\|\cdot\|$ 是谱范数，即算符 $2$-范数。

第 07 章的 Trotter 界已经显式声明谱范数，因此这里省略会造成同一本书对相似范数符号的解释不一致。初学者也无法仅从公式判断这是谱范数、Frobenius 范数还是迹范数。

**可执行修改**：在“若酉矩阵 $U$ 满足”前补一句：“取 $\alpha>0$、$a\in\mathbb Z_{\ge0}$、$\epsilon\ge0$，下式的范数为谱范数（算符 $2$-范数）。”若要进一步完整，可说明 $U$ 作用于 $a$ 个辅助量子比特与承载 $A$ 的系统空间。

来源：A. Gilyén et al., [Quantum Singular Value Transformation and Beyond](https://arxiv.org/abs/1806.01838)（2018），block encoding 定义。访问日期：2026-09-22。

## 3. 第 9 轮重点复核结果

### 3.1 QPE 非精确概率

- 概率公式由有限几何级数的模平方得到，归一化因子 $M^{-2}$ 正确。
- 对 $\phi=1/3,M=4,y=1$：
  $$
  \left[\frac{\sin(\pi/3)}{4\sin(\pi/12)}\right]^2
  =0.6997595\ldots,
  $$
  与正文的 $0.700$ 一致。
- 最近网格点的 $4/\pi^2$ 常数下界正确；仅需补 P2-1 的模 1 边界说明。

### 3.2 Shor 与连分数

- 本征态符号正确：正文的 $e^{-2\pi ikj/r}$ 给出 $U_a|u_k\rangle=e^{2\pi ik/r}|u_k\rangle$。
- 连分数充分条件 $|y/Q-k/r|<1/(2r^2)$ 正确。
- $N=15,a=2,r=4$ 的峰位置和 gcd 计算正确；$1/2$ 样本只给分母 2，必须验证或继续采样。
- 成功账本正确区分随机 $a$、阶条件、Fourier 样本、互素性和候选验证；除 P2-2 的完美幂预处理外未发现问题。

### 3.3 单边 QAOA

正文中

$$
A_{01}=A_{10}
=\frac12[-i\sin(2\beta)+e^{-i\gamma}\cos(2\beta)]
$$

由四个计算基分量逐项展开可得。再计算

$$
2|A_{01}|^2
=\frac12[1+\sin(4\beta)\sin\gamma]
$$

正确。$\beta=\pi/8,\gamma=\pi/2$ 时期望为 1。`handbook/appendices/exercises.md` 第 8 章答案的 Heisenberg 图像结果与正文一致。

### 3.4 HSP 条件态与混态

测量输出并条件化时得到纯态

$$
|gH\rangle=|H|^{-1/2}\sum_{h\in H}|gh\rangle.
$$

丢弃输出寄存器时得到

$$
\rho_H=\frac1{|G/H|}\sum_{gH}|gH\rangle\langle gH|.
$$

权重正确，因为每个陪集含 $|H|$ 个群元素，$|H|/|G|=1/|G/H|$。正文也正确说明后续 Fourier 统计是各条件纯态分布的平均。

### 3.5 根保真度与能隙证书

- 全书第 05、13、15、16 章和符号附录统一采用根保真度。
- 第 16 章正确用 $f=\langle\psi|\rho|\psi\rangle$ 表示平方重叠，并写 $F=\sqrt f$。
- 能量界
  $$
  f_0\ge1-\frac{E-E_0}{\Delta}
  $$
  方向正确；正文例给 $f_0\ge0.75$、$F_0\ge\sqrt{0.75}\approx0.866$。
- 自检答案已同步为 $f_0\ge0.85$、$F_0\ge\sqrt{0.85}=0.9219544\ldots\approx0.922$，并正确写出非简并与系统误差前提。

### 3.6 Eastin–Knill 与答案

正文和练习答案均不再加入错误的“连续门集”限定。当前表述正确排除固定非平凡有限维纠错码上的通用纯横向编码门集，同时保留魔法态、码切换、规范固定和格码手术等非纯横向容错路径。

依据：B. Eastin and E. Knill, [Restrictions on Transversal Encoded Quantum Gate Sets](https://doi.org/10.1103/PhysRevLett.102.110502), *Physical Review Letters* 102, 110502 (2009)。

## 4. 其余章节抽查

以下项目复核后未发现 P0/P1/P2：

- **第 01–03 章**：复数模平方、bra/ket、张量积端序、Born 概率、Bloch 参数化、投影/POVM 条件态与非选择态、两比特可分判据、偏迹、Schmidt 权重、纠缠熵和 CHSH 界。
- **第 04–05 章**：不可克隆的全局相位边界、不可删除与环境转移、隐形传态分支、Kraus 完备性、正与完全正、复位信道、振幅阻尼、退极化两种参数约定、$T_1/T_2/T_\phi$ 和根保真度。
- **第 07 章其余公式**：Simon 约束、Grover 旋转、Trotter 交换子界、HHL 输出形式、幅度估计误差界和复杂度类包含关系。
- **第 10 章**：三比特码综合征、Shor 码字、Knill–Laflamme 条件、Steane 列综合征、距离与擦除数、示意阈值缩放、Ross–Selinger 主项和 T count 增量。
- **第 12–15 章**：双链路几何等待时间、Shannon/von Neumann 熵、量子互信息、相对熵数据处理、Helstrom 界、Fuchs–van de Graaf 不等式、Holevo 量、读出矩阵、Rabi 门时长、反馈弛豫和 Bell 重叠见证。
- **第 16 章其余公式**：多项式方法次数、coined walk、element distinctness 上下界、LCU 权重、Chebyshev 矩阵多项式、误差预算和单比特 Pauli 阴影均值/方差。

练习答案的主要数值复算均通过，包括：Bayes 例 $0.1538$、振幅阻尼输出行列式 $0.0576$、退极化 $p=0.20\leftrightarrow q=0.15$、Grover 约 785 次、Trotter $r\ge20$、核差缩小四倍导致 shots 增加十六倍、双链路等待 $14.74$ 轮和根保真度 $\sqrt{0.85}\approx0.922$。

## 5. 最终判定

本轮未发现 P0 或 P1。第 9 轮的核心数学修复和练习答案同步均正确，但仍有 3 项 P2：QPE 环绕边界、Shor 完美幂预处理、block encoding 参数域与范数。修复后应再做一次只读定向复核，届时才能据实判定是否达到零问题。
