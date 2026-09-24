# 第 18 章自检答案草稿

> 对应 `handbook/18-channels-capacities-complexity.md` 的 10 道自检题。此稿供练习附录下一次统一编排使用；本轮不修改共享附录。

## 1. 构造纯化并做偏迹

取

$$
|\psi\rangle_{AR}=\sqrt{0.8}|00\rangle+\sqrt{0.2}|11\rangle.
$$

它的密度矩阵为

$$
\begin{aligned}
|\psi\rangle\langle\psi|
={}&0.8|00\rangle\langle00|
+\sqrt{0.16}|00\rangle\langle11|\\
&+\sqrt{0.16}|11\rangle\langle00|
+0.2|11\rangle\langle11|.
\end{aligned}
$$

使用

$$
\operatorname{Tr}_R
(|a\rangle|i\rangle\langle b|\langle j|)
=|a\rangle\langle b|\,\langle j|i\rangle,
$$

两个交叉项分别带有 $\langle1|0\rangle$ 和 $\langle0|1\rangle$，因而为零；两个对角项保留。于是

$$
\operatorname{Tr}_R(|\psi\rangle\langle\psi|)
=0.8|0\rangle\langle0|+0.2|1\rangle\langle1|=\rho.
$$

这只是一个纯化。还可以只在 $R$ 上做任意酉变换，得到同一 $\rho$ 的其他纯化。

## 2. qubit 复位信道的 Choi 矩阵

本章采用未归一化向量

$$
|\Omega\rangle=|00\rangle+|11\rangle.
$$

复位信道满足

$$
\mathcal R(|i\rangle\langle j|)
=\delta_{ij}|0\rangle\langle0|.
$$

所以

$$
\begin{aligned}
J_{\mathcal R}
&=\sum_{i,j=0}^1|i\rangle\langle j|
\otimes\mathcal R(|i\rangle\langle j|)\\
&=\sum_{i=0}^1|i\rangle\langle i|\otimes|0\rangle\langle0|\\
&=I\otimes|0\rangle\langle0|.
\end{aligned}
$$

在 $|00\rangle,|01\rangle,|10\rangle,|11\rangle$ 顺序下，

$$
J_{\mathcal R}=\operatorname{diag}(1,0,1,0).
$$

它的本征值全非负，故 $J_{\mathcal R}\succeq0$，由 Choi 判据可知 $\mathcal R$ 完全正。对输出系统 $B$ 做偏迹，

$$
\operatorname{Tr}_B J_{\mathcal R}
=I\operatorname{Tr}(|0\rangle\langle0|)=I,
$$

故 $\mathcal R$ 保迹。两项合起来说明它是 CPTP 信道。

## 3. 改用归一化最大纠缠态

若

$$
|\Phi\rangle=\frac{|\Omega\rangle}{\sqrt d},
$$

则新的 Choi 态为

$$
\tau_{\mathcal E}
=(I\otimes\mathcal E)(|\Phi\rangle\langle\Phi|)
=\frac{J_{\mathcal E}}d.
$$

对保迹映射，未归一化约定给出 $\operatorname{Tr}J_{\mathcal E}=d$，所以

$$
\operatorname{Tr}\tau_{\mathcal E}=1.
$$

保迹的偏迹条件则变为

$$
\operatorname{Tr}_B\tau_{\mathcal E}=\frac{I_{A'}}d.
$$

因此两种约定描述同一个映射，只是整体差一个输入维数 $d$。

## 4. 相对熵与 Helstrom 任务的区别

直接计算

$$
\begin{aligned}
D(\rho\|\sigma)
&=0.8\log_2\frac{0.8}{0.5}
+0.2\log_2\frac{0.2}{0.5}\\
&=0.8\log_2 1.6+0.2\log_2 0.4\\
&\approx0.278071905\text{ bit}.
\end{aligned}
$$

这个数是 Stein 非对称多副本检验中的最优第二类错误指数，不是概率。作为对照，若只有一个副本、两种先验各为 $1/2$，则

$$
\rho-\sigma=\operatorname{diag}(0.3,-0.3),
$$

$$
T(\rho,\sigma)=\frac12(0.3+0.3)=0.3,
$$

Helstrom 最优成功率为

$$
p_{\rm guess}=\frac{1+T}{2}=0.65.
$$

$0.2781$ bit 与 $0.65$ 回答的是不同问题，单位和操作含义也不同。

## 5. 擦除概率为 $1/4$ 时的四种容量

对 qubit 擦除信道，

$$
C=1-\varepsilon,
\qquad
Q=\max\{0,1-2\varepsilon\},
\qquad
P=\max\{0,1-2\varepsilon\},
\qquad
C_E=2(1-\varepsilon).
$$

代入 $\varepsilon=1/4$：

$$
C=\frac34=0.75\text{ bit/use},
$$

$$
Q=1-\frac12=0.50\text{ qubit/use},
$$

$$
P=1-\frac12=0.50\text{ secret bit/use},
$$

$$
C_E=2\times\frac34=1.50\text{ bit/use}.
$$

它们不同并不矛盾：$C$ 传普通经典消息，$Q$ 传未知量子态，$P$ 传不向环境泄露的经典消息，$C_E$ 则允许无限预共享纠缠后再传经典消息。$P=Q$ 是擦除信道的特殊结果，不是一般定律。任务与免费资源不同，容量定义就不同。

## 6. 加白噪声 Bell 态的负性

部分转置的四个本征值为三个

$$
\frac{1+p}{4}
$$

以及一个

$$
\frac{1-3p}{4}.
$$

取 $p=0.6$，唯一负本征值是

$$
\frac{1-1.8}{4}=-0.2.
$$

迹范数比 1 多出负本征值绝对值的两倍，因此

$$
\mathcal N(\rho_{0.6})
=\frac{\|\rho_{0.6}^{T_B}\|_1-1}{2}
=0.2.
$$

等价地，直接代入 $\max\{0,(3p-1)/4\}$ 也得到 $0.2$。

## 7. QCMA 与 QMA 的量词

设 $V_x$ 是多项式时间量子验证电路，$c-s\ge1/\operatorname{poly}(|x|)$。两类都满足

$$
\begin{aligned}
x\in L_{\rm yes}&:\quad
\exists w,\ \Pr[V_x(w)=1]\ge c,\\
x\in L_{\rm no}&:\quad
\forall w,\ \Pr[V_x(w)=1]\le s.
\end{aligned}
$$

区别在 $w$ 的类型：QCMA 的 $w$ 是多项式长度的经典串；QMA 的 $w$ 是多项式量子比特的量子态。二者的验证者都是量子多项式时间，不能把 QCMA 的字母 C 误解成“经典验证者”。

## 8. 为什么 QIP = PSPACE 不等于 BQP = PSPACE

QIP 协议包含两个角色：多项式时间量子验证者，以及计算能力不受限制但可能作弊的证明者。验证者借助交互，在 yes 实例上应能被某个证明策略说服，在 no 实例上则不能被任何策略高概率骗过。

$\mathrm{QIP}=\mathrm{PSPACE}$ 说的是“带有这种强大证明者的交互验证协议”恰好能验证 PSPACE 中的承诺问题。BQP 模型没有额外的全能证明者，因此该等式没有给出普通量子计算机独立求解 PSPACE 问题的高效算法。

## 9. 量子指纹的误报概率

相对距离 $\delta=1/4$ 时，不同输入的指纹重叠满足

$$
|\langle\phi_x|\phi_y\rangle|
\le1-2\delta=\frac12.
$$

一次 swap test 输出“相同”的概率至多

$$
p_{\rm same}
\le\frac{1+(1/2)^2}{2}
=\frac58=0.625.
$$

若 10 次独立重复且只在每次都通过时才接受，误报概率至多

$$
\left(\frac58\right)^{10}
=\frac{9\,765\,625}{1\,073\,741\,824}
\approx0.00909495.
$$

这里独立重复使用的是 10 对独立制备的指纹，不是反复测量同一对测后态。

## 10. 压缩真空的两个方差

由 $r=(\ln2)/2$ 得

$$
e^{-2r}=e^{-\ln2}=\frac12,
\qquad
e^{2r}=2.
$$

代入

$$
\operatorname{Var}(q)=\frac12e^{-2r},
\qquad
\operatorname{Var}(p)=\frac12e^{2r},
$$

得到

$$
\operatorname{Var}(q)=\frac14,
\qquad
\operatorname{Var}(p)=1,
$$

以及

$$
\operatorname{Var}(q)\operatorname{Var}(p)=\frac14.
$$

在 $[q,p]=i$ 约定下，不确定性关系要求乘积至少为 $1/4$。此态恰好饱和下界：$q$ 方向更窄，但 $p$ 方向按相反倍数变宽，所以没有同时提高两个共轭量的精度。
