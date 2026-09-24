# 第 29 轮：基础数学与量子信息定点终审

日期：2026-09-22  
范围：`handbook/13-quantum-information.md` 的无歧义态判别、二元纯态可访问信息和纯态纠缠渐近率；`handbook/14-compilation-control.md` 的 SX 与旋转门相位关系；`handbook/01-math.md` 的正半定定义及全局相位说明。  
性质：只读复核；本轮未修改 handbook。

## 结论

| 等级 | 数量 | 结论 |
|---|---:|---|
| P0 | 0 | 未发现导致数学结论失效的问题。 |
| P1 | 0 | 未发现会系统性误导初学者的问题。 |
| P2 | 0 | 在本轮指定范围内未发现仍需修订的问题。 |

本结论只适用于上述定点检查范围，不外推为对全书或领域知识的绝对无错声明。

## 1. 三结果无歧义判别（USD）

正文令

$$
s=|\langle0|+\rangle|=\frac1{\sqrt2},
\qquad
c=\frac1{1+s}=2-\sqrt2,
$$

并取

$$
E_0=c|-\rangle\langle-|,
\qquad
E_+=c|1\rangle\langle1|,
\qquad
E_?=I-E_0-E_+.
$$

独立展开得到

$$
E_0=\frac c2
\begin{bmatrix}1&-1\\-1&1\end{bmatrix},
\qquad
E_+=c
\begin{bmatrix}0&0\\0&1\end{bmatrix},
$$

从而

$$
E_?=
\begin{bmatrix}
1-c/2&c/2\\
c/2&1-3c/2
\end{bmatrix}.
$$

该矩阵行列式为零，迹为 $2-2c=2(\sqrt2-1)>0$，故本征值确为

$$
0,\qquad2(\sqrt2-1)\approx0.8284271247.
$$

因此三个元素都正半定且和为 $I$，POVM 合法。又因 $\langle+|-\rangle=0$、$\langle0|1\rangle=0$，两个确定结果不会误判。两种输入的成功概率均为

$$
\frac c2=1-\frac1{\sqrt2}\approx0.2928932188.
$$

最优性证明也闭合：零误判和正半定性给出 $E_0|+\rangle=0$、$E_+|0\rangle=0$，所以 $\langle0|E_?|+\rangle=s$。对 $E_?$ 的半内积应用柯西—施瓦茨，得 $f_0f_+\ge s^2$；等先验时再由算术—几何平均不等式得到平均失败率至少为 $s$。上述构造达到这一界，因此成功率 $1-s$ 最优。正文没有把“允许不确定结果”误写成确定性区分。

## 2. Helstrom 测量、条件概率表与可访问信息

对等先验 $|0\rangle,|+\rangle$，正文所用测量基给出

$$
q=\cos^2\frac\pi8
=\frac12\left(1+\frac1{\sqrt2}\right),
\qquad
p_e=\sin^2\frac\pi8
=\frac12\left(1-\frac1{\sqrt2}\right)
\approx0.1464466094.
$$

逐项计算振幅，条件概率表确为对称二元信道：输入 $0$ 时为 $(q,p_e)$，输入 $+$ 时为 $(p_e,q)$。等先验使两个输出也均匀，故

$$
I(X:Y)=1-h_2(p_e)\approx0.3991239633\text{ bit}.
$$

平均态

$$
\bar\rho=
\begin{bmatrix}3/4&1/4\\1/4&1/4\end{bmatrix}
$$

的本征值为 $(1\pm1/\sqrt2)/2$，所以

$$
\chi=S(\bar\rho)
=h_2\!\left(\frac12\left(1+\frac1{\sqrt2}\right)\right)
\approx0.6008760367\text{ bit}.
$$

正文据 Levitin 的等先验二元纯态结果，把前述测量取得的 $0.3991239633$ bit 认定为本例的 $I_{\rm acc}$，同时明确指出最小错误与最大互信息一般不是同一优化问题；边界表述准确。Holevo 上界与本例可访问信息之和数值上恰为 1，但正文没有把这一特殊数值关系推广。

来源可追溯性已经由第 28 轮定点修正：

- Holevo 原始论文的期刊记录：[Math-Net](https://www.mathnet.ru/eng/ppi903)。
- 二元纯态最大信息测量结果：[Levitin 原始章节入口](https://link.springer.com/chapter/10.1007/978-1-4899-1391-3_43)。

## 3. LOCC 与纯态纠缠的渐近资源率

对

$$
|\psi\rangle=\sqrt{0.9}|00\rangle+\sqrt{0.1}|11\rangle,
$$

Schmidt 概率为 $0.9,0.1$，纯态纠缠熵为

$$
E=h_2(0.1)\approx0.469\text{ ebit}.
$$

正文已把这一定量结论限制为许多份相同纯态在 LOCC 下的渐近纠缠浓缩率，并同时写明 $n\to\infty$、输出 Bell 对数与 $n$ 的比率趋近该值、输出误差趋零。它没有把 $0.469$ ebit 解释成单副本可确定获得的“分数个 Bell 对”，也没有把纯态约化熵公式误用于一般混态。所需操作类、极限和误差条件均已给出。

## 4. SX 与 $R_x(\pi/2)$ 的全局相位

从

$$
R_x(\pi/2)=\frac1{\sqrt2}
\begin{bmatrix}1&-i\\-i&1\end{bmatrix}
$$

直接乘以 $e^{i\pi/4}=(1+i)/\sqrt2$，得到

$$
e^{i\pi/4}R_x(\pi/2)
=\frac12
\begin{bmatrix}1+i&1-i\\1-i&1+i\end{bmatrix}
=\mathrm{SX}.
$$

继续平方可得 $\mathrm{SX}^2=X$，而 $R_x(\pi/2)^2=R_x(\pi)=-iX$。正文正确区分：无条件单比特门的共同相位不影响测量统计，但受控分支中该因子可成为相对相位，因而不能把两个受控门直接视为同一矩阵。

## 5. 正半定前提与全局相位的教学顺序

第 01 章现将正半定定义写为

$$
A=A^\dagger,
\qquad
\langle v|A|v\rangle\ge0\quad\text{对所有 }|v\rangle,
$$

并明确限定：只对有限维**厄米矩阵**，正半定才等价于全部本征值非负；不能把该判据直接套到任意非厄米矩阵。这排除了仅看非厄米矩阵本征值的误用。两个随文例子的本征值分别为 $0,2$ 和 $3,-1$，复算正确。

全局相位段在尚未定义投影算符时，只用振幅模平方

$$
|e^{i\gamma}c|^2=|c|^2
$$

说明概率不变，并把相对相位的可观测效应推迟到后续 Hadamard 实验，教学顺序和术语均无前置依赖。

## 6. 静态检查

- `01-math.md`、`13-quantum-information.md`、`14-compilation-control.md` 的独立展示公式定界符计数分别为 22、90、26，均成对。
- 本轮未改正文、练习、术语表、导航或审校日志。

## 最终判定

本轮指定范围内未发现 P0、P1 或 P2 问题；计数为 **P0 = 0，P1 = 0，P2 = 0**。
