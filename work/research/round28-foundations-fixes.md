# 第 28 轮：第 13 章基础信息论教学修订

## 范围

根据 `work/research/round27-foundations-crossreview.md` 的 3 项 P2，只修改：

- `handbook/13-quantum-information.md`

没有修改第 00、01 章、共享附录、README、审校日志、图片或构建工具，也没有新增自检题。

## 修复 1｜定义 LOCC，并补全分数 ebit 的渐近条件

### 原缺口

第 13 章首次使用 `LOCC` 时没有展开，定义直到第 18 章才出现；“$0.469n$ 个 Bell 对”虽明确是渐近资源率，却没有说明近似误差也要在大块长极限中趋零。

### 实施

正文现在先定义局域操作与经典通信（LOCC）：两地参与者各自只操作手中子系统，可交换普通经典消息，但不直接传送量子系统。对

$$
|\psi\rangle=\sqrt{0.9}|00\rangle+\sqrt{0.1}|11\rangle
$$

明确写成：

$$
\lim_{n\to\infty}
\frac{\text{输出 Bell 对数}}{n}
=h_2(0.1)
=0.4689955936\ldots,
$$

同时输出态与理想 Bell 对的误差（例如迹距离）趋于零。正文继续保留“有限 $n$ 不是精确等式，单份态不是分数个 Bell 对”的提醒。

### 来源

C. H. Bennett et al., [Concentrating partial entanglement by local operations](https://doi.org/10.1103/PhysRevA.53.2046), *Physical Review A* 53, 2046–2052 (1996)。原始论文给出大量相同部分纠缠纯态的最大纠缠对产率趋于约化态熵。

## 修复 2｜给出 USD 的合法 POVM、成功率与最优性短证

### 原缺口

原文正确给出等先验 $|0\rangle,|+\rangle$ 的最优无歧义成功率

$$
1-\frac1{\sqrt2}\approx0.2929,
$$

但没有读者可构造的测量，也没有解释“最优”而不仅是“这个构造能达到”。

### 实施

令

$$
s=\frac1{\sqrt2},
\qquad
c=\frac1{1+s}=2-\sqrt2.
$$

正文新增三结果 POVM

$$
E_0=c|-\rangle\langle-|,
\qquad
E_+=c|1\rangle\langle1|,
\qquad
E_?=I-E_0-E_+.
$$

并逐项验证：

1. 零误判：

   $$
   \langle+|E_0|+\rangle=0,
   \qquad
   \langle0|E_+|0\rangle=0.
   $$

2. 合法性：

   $$
   E_?=
   \begin{bmatrix}
   1-c/2&c/2\\
   c/2&1-3c/2
   \end{bmatrix}
   $$

   的本征值为

   $$
   0,\qquad2(\sqrt2-1),
   $$

   所以 $E_?\succeq0$；三个元素之和为 $I$。

3. 达到的成功率：

   $$
   \langle0|E_0|0\rangle
   =\langle+|E_+|+\rangle
   =\frac c2
   =1-\frac1{\sqrt2}.
   $$

4. 最优性：对任意零误判 POVM，记两态的失败概率为 $f_0,f_+$。零误判使

   $$
   \langle0|E_?|+\rangle=\langle0|+\rangle=s.
   $$

   柯西—施瓦茨与算术—几何平均给出

   $$
   f_0f_+\ge s^2,
   \qquad
   \frac{f_0+f_+}{2}\ge s.
   $$

   因而平均成功率至多为 $1-s$；上述构造达到上界。

### 来源

- I. D. Ivanovic, [How to differentiate between non-orthogonal states](https://doi.org/10.1016/0375-9601(87)90222-2), *Physics Letters A* 123, 257–259 (1987)。
- D. Dieks, [Overlap and distinguishability of quantum states](https://doi.org/10.1016/0375-9601(88)90840-7), *Physics Letters A* 126, 303–306 (1988)。
- A. Peres, [How to differentiate between non-orthogonal states](https://doi.org/10.1016/0375-9601(88)91034-1), *Physics Letters A* 128, 19 (1988)。

## 修复 3｜定义可访问互信息，并实际算出 Helstrom 测量的 0.399 bit

### 原缺口

$I_{\rm acc}$ 首次出现时没有定义；非正交编码虽给出 $0.399<0.601$ bit，却没有测量基、条件概率表或互信息计算。读者不能从“Holevo 是上界”走到“一个测量实际得到多少”。

### 实施

正文先定义

$$
I_{\rm acc}(\{p_x,\rho_x\})
=\max_{\{M_y\}}I(X:Y).
$$

对等先验 $|0\rangle,|+\rangle$，新增正交测量基

$$
|m_0\rangle=
\cos\frac\pi8|0\rangle-
\sin\frac\pi8|1\rangle,
$$

$$
|m_+\rangle=
\sin\frac\pi8|0\rangle+
\cos\frac\pi8|1\rangle.
$$

令

$$
q=\cos^2\frac\pi8
=\frac12\left(1+\frac1{\sqrt2}\right),
$$

$$
p_e=\sin^2\frac\pi8
=\frac12\left(1-\frac1{\sqrt2}\right).
$$

正文加入条件概率表：

| 输入 $X$ | $Y=0$ | $Y=+$ |
|---|---:|---:|
| $0$ | $q$ | $p_e$ |
| $+$ | $p_e$ | $q$ |

等先验与对称性给 $H(Y)=1$、$H(Y|X)=h_2(p_e)$，因此这个实际测量取得

$$
I(X:Y)=1-h_2(p_e)=0.3991239633\ldots\text{ bit}.
$$

原有 Holevo 量复算为

$$
\chi=h_2(q)=0.6008760367\ldots\text{ bit}.
$$

正文把两层结论分开：条件概率表直接证明这组测量取得 0.399 bit；“它对等先验二元纯态集合达到最大互信息”则明确归于 Levitin 的最优测量结果，不在入门段落假装已经证明所有 POVM 的全局最优性。

### 来源

- A. S. Holevo, [Bounds for the quantity of information transmitted by a quantum communication channel](https://www.mathnet.ru/eng/ppi903), *Problems of Information Transmission* 9, 177–183 (1973)。
- L. B. Levitin, “Optimal Quantum Measurements for Two Pure and Mixed States,” in [*Quantum Communications and Measurement*](https://doi.org/10.1007/978-1-4899-1391-3), pp. 439–448, Plenum Press (1995)。

## 独立数值复算

用矩阵直接验证新增公式，结果如下：

```text
round28 formulas: PASS
eig(E?) [7.0e-17, 0.828427124746190]
USD rows
  |0>: [0.2928932188, 0,            0.7071067812]
  |+>: [0,            0.2928932188, 0.7071067812]
Helstrom rows
  |0>: [0.8535533906, 0.1464466094]
  |+>: [0.1464466094, 0.8535533906]
I     = 0.39912396330714384 bit
chi   = 0.6008760366928562 bit
```

$E_?$ 的首个数值本征值是浮点舍入下的 $7\times10^{-17}$，解析值为 0。POVM 和条件概率的各行均归一化为 1。

## 静态检查与残余边界

- 第 13 章展示公式分隔符共 118 个，成对；没有代码围栏或新增 Mermaid。
- 没有修改第 13 章自检题，因此共享答案数量与编号不变。
- 新增参考资料均为原始论文或原始学术章节；没有把 Holevo 上界写成可达率。
- USD 最优性短证只针对本节的等先验二元纯态；正文没有推广到不等先验、混态或三个以上候选态。
- Helstrom 测量与最大互信息测量重合只限定在本节的对称二元纯态集合；正文继续保留“不能一般化”的提醒。
