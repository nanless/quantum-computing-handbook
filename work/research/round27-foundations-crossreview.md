# 第 27 轮：00、01、13 章基础内容交叉审阅

## 范围与方法

本轮只读审阅当前文本：

- `handbook/00-overview.md`
- `handbook/01-math.md`
- `handbook/13-quantum-information.md`
- `work/research/round27-foundations-parent-review.md`

重点检查初学者定义顺序、正半定的厄米前提、分数 ebit 的资源含义、无歧义态判别（USD）的最优成功率与可构造测量，以及 Holevo 上界、实际测量和经典互信息的区别。先读主代理报告，再读当前正文，避免重复报告已经修复的第 01 章问题。

结论：P0 = 0，P1 = 0，P2 = 3。三项都在第 13 章；第 00、01 章当前未发现新的 P0/P1/P2。

## 已验证关闭的问题

### 第 01 章正半定前提：已关闭

当前 `handbook/01-math.md:97-110` 已把正半定定义写成

$$
A=A^\dagger,
\qquad
\langle v|A|v\rangle\ge0,
$$

并把“本征值全非负”的等价明确限定为有限维厄米矩阵。复厄米例子

$$
\begin{bmatrix}1&i\\-i&1\end{bmatrix}
$$

本征值为 $0,2$；“对角元非负仍可能非正半定”的反例本征值为 $3,-1$。定义、前提和例子一致，不重复上报主代理已经修复的 P1。

### 第 01 章全局相位顺序：已关闭

当前 `handbook/01-math.md:60-70` 只用前文已经定义的复振幅和模平方证明

$$
|e^{i\gamma}c|^2=|c|^2,
$$

不再提前调用尚未定义的投影算符或 Born 公式；$|+\rangle,|-\rangle$ 明确说明在下一节定义。初学者顺序已经自洽，不重复上报主代理已经修复的 P2。

## P2-1｜分数 ebit 段首次使用 LOCC 却未定义，渐近近似条件未说完

### 定位

`handbook/13-quantum-information.md:148-156`

### 现状与问题

正文正确算出

$$
h_2(0.1)=0.4689955936\ldots\text{ ebit},
$$

也正确提醒“单份态不是 0.469 个 Bell 对”。但 `LOCC` 在第 13 章首次出现时没有展开；全书搜索显示“局域操作与经典通信（LOCC）”直到第 18 章才定义。对按章顺序阅读的初学者，这是前置术语缺口。

另外，“渐近浓缩出约 $0.469n$ 个 Bell 对”没有说明渐近陈述允许近似，并要求当 $n\to\infty$ 时误差趋零。原句数值没有错，但操作含义还差这两个限定。

### 精确修法

首次出现时改成“局域操作与经典通信（LOCC）”，并补一句：在大块长极限中，输出 Bell 对数与 $n$ 的比率趋于 $h_2(0.1)$，同时输出态与理想 Bell 对的误差趋于零；这不是有限 $n$ 下的精确等式或确定性分割。

### 证据

Bennett、Bernstein、Popescu、Schumacher 的原始纠缠浓缩论文明确给出：大量相同部分纠缠纯态经局域操作可浓缩为最大纠缠对，且当 $n$ 很大时每份产率趋于约化态的二进制 von Neumann 熵：

- C. H. Bennett et al., [Concentrating partial entanglement by local operations](https://doi.org/10.1103/PhysRevA.53.2046), *Physical Review A* 53, 2046–2052 (1996)。

## P2-2｜USD 只报最优数值，没有给能达到它的三结果 POVM，也没有说明为何最优

### 定位

`handbook/13-quantum-information.md:211-219`

### 现状与问题

正文对等先验 $|0\rangle,|+\rangle$ 正确写出最优无歧义成功率

$$
1-|\langle0|+\rangle|=1-\frac1{\sqrt2}=0.292893\ldots,
$$

但读者无法据此构造测量，也无法检查“成功时零错误”和“最优”分别来自哪里。这个段落位于“迹距离：最优区分能力”，恰好需要把二结果最小错误与三结果零错误测量并排展示；只报一个定理数值会让操作含义断裂。

### 可直接采用的构造

令

$$
s=\frac1{\sqrt2},
\qquad
c=\frac1{1+s}=2-\sqrt2.
$$

三结果 POVM 可取

$$
E_0=c|-\rangle\langle-|,
\qquad
E_+=c|1\rangle\langle1|,
\qquad
E_?=I-E_0-E_+.
$$

$E_0$ 的结果只认定输入为 $|0\rangle$，因为 $\langle+|E_0|+\rangle=0$；$E_+$ 只认定输入为 $|+\rangle$，因为 $\langle0|E_+|0\rangle=0$。在计算基中

$$
E_?=
\begin{bmatrix}
1-c/2 & c/2\\
c/2 & 1-3c/2
\end{bmatrix},
$$

其本征值为

$$
0,\qquad2(\sqrt2-1),
$$

所以 $E_?\succeq0$，确实是合法 POVM。两个输入的正确识别概率都为

$$
\frac c2=1-\frac1{\sqrt2}.
$$

### 最优性短证

对任意零误判三结果 POVM，记两个输入的失败概率为

$$
f_0=\langle0|E_?|0\rangle,
\qquad
f_+=\langle+|E_?|+\rangle.
$$

零误判条件使

$$
\langle0|E_?|+\rangle=\langle0|+\rangle=s.
$$

在 $E_?\succeq0$ 诱导的半内积中用 Cauchy–Schwarz，再用算术—几何平均不等式：

$$
f_0f_+\ge s^2,
\qquad
\frac{f_0+f_+}{2}\ge\sqrt{f_0f_+}\ge s.
$$

因此平均失败概率至少为 $s$，成功率至多为 $1-s$；上述对称构造达到上界。这个证明足以让“最优”不再只是背诵结果。

### 证据

- I. D. Ivanovic, [How to differentiate between non-orthogonal states](https://doi.org/10.1016/0375-9601(87)90222-2), *Physics Letters A* 123, 257–259 (1987)。原始工作明确使用广义测量在部分轮次无错误识别非正交态。
- A. Peres, [How to differentiate between non-orthogonal states](https://doi.org/10.1016/0375-9601(88)91034-1), *Physics Letters A* 128, 19 (1988)。
- D. Dieks, [Overlap and distinguishability of quantum states](https://doi.org/10.1016/0375-9601(88)90840-7), *Physics Letters A* 126, 303–306 (1988)。

## P2-3｜$I_{\rm acc}$ 未显式定义，0.399 bit 没有实际测量基与条件概率表

### 定位

`handbook/13-quantum-information.md:289-344`

### 现状与问题

正文从“任意测量有 $I(X:Y)\le\chi$”直接写

$$
I_{\rm acc}\le\chi\le\log_2d,
$$

但首次出现 $I_{\rm acc}$ 时没有把它定义为对 POVM 测量优化后的互信息。随后非正交例子正确给出

$$
\chi=0.600876\ldots\text{ bit},
\qquad
I_{\rm acc}=0.399124\ldots\text{ bit},
$$

却只说“Helstrom 测量”，没有写测量基、条件概率或 $H(Y)-H(Y|X)$。因此“Holevo 是上界、某个实际测量取得较小互信息”仍停留在数字陈述，读者不能复算。

### 精确修法

先定义

$$
I_{\rm acc}(\{p_x,\rho_x\})
=\max_{\{M_y\}} I(X:Y).
$$

对等先验 $|0\rangle,|+\rangle$，给出正交测量基

$$
|m_0\rangle=cos\frac\pi8|0\rangle-sin\frac\pi8|1\rangle,
$$

$$
|m_+\rangle=sin\frac\pi8|0\rangle+cos\frac\pi8|1\rangle.
$$

条件概率表应为

| 输入 $X$ | $Y=0$ | $Y=+$ |
|---|---:|---:|
| $0$ | $q$ | $p_e$ |
| $+$ | $p_e$ | $q$ |

其中

$$
q=\cos^2\frac\pi8=\frac12\left(1+\frac1{\sqrt2}\right),
\qquad
p_e=\sin^2\frac\pi8=\frac12\left(1-\frac1{\sqrt2}\right).
$$

等先验使输出也均匀，因此

$$
H(Y)=1,
\qquad
H(Y|X)=h_2(p_e),
$$

$$
I(X:Y)=1-h_2(p_e)=0.3991239633\ldots\text{ bit}.
$$

随后再引用二元纯态集合的最优性定理，说明这个实际测量值就是 $I_{\rm acc}$。不必在入门章证明所有 POVM 中的全局最优性，但要把“可直接复算的示例”与“引用的最优性定理”分开。

### 证据

- A. S. Holevo, [Bounds for the quantity of information transmitted by a quantum communication channel](https://doi.org/10.1007/BF01007469), *Problems of Information Transmission* 9, 177–183 (1973)：$I_{\rm acc}\le\chi$ 的原始来源。
- L. B. Levitin, “Optimal Quantum Measurements for Two Pure and Mixed States,” in [*Quantum Communications and Measurement*](https://doi.org/10.1007/978-1-4899-1391-3), pp. 439–448, Plenum Press (1995)：给出二元纯态集合的最大信息量与最优测量基。
- C. A. Fuchs, C. M. Caves, [Ensemble-Dependent Bounds for Accessible Information in Quantum Mechanics](https://doi.org/10.1103/PhysRevLett.73.3047), *Physical Review Letters* 73, 3047–3050 (1994)：区分 Holevo 上界与依赖具体集合的可访问互信息界。

## 第 00 章结论

第 00 章当前结构遵循“态与测量—叠加/纠缠/干涉—任务与资源—反例—最小完整流程”。Hadamard 虽在概览前半首次出现，但同节给出输入输出作用，第 7 节再给矩阵；作为概览没有构成需要改写的跳步。oracle、SPAM、break-even 等首次出现均有中文解释或限定。本轮未发现新的 P0/P1/P2。

## 第 01 章结论

除主代理已经修复并在本报告验证关闭的两项外，定义次序、复共轭、基、算符、谱分解、张量积、概率和复杂度的先后关系自洽。正半定例子、本征值和厄米性复算正确。本轮未发现新的 P0/P1/P2。

## 数值复算

独立矩阵计算得到：

```text
USD c = 0.585786437626905
eig(E?) = [0, 0.828427124746190]
USD conditional rows:
state |0>: [0.2928932188, 0, 0.7071067812]
state |+>: [0, 0.2928932188, 0.7071067812]

Helstrom conditional rows:
state |0>: [0.8535533906, 0.1464466094]
state |+>: [0.1464466094, 0.8535533906]
I = 0.39912396330714384 bit
chi = 0.6008760366928562 bit
```

这些结果分别核对了 POVM 正半定、零误判、最优 USD 成功率，以及实际测量互信息与 Holevo 上界的严格间隙。
