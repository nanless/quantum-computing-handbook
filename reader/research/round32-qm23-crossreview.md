# 第 32 轮：Q2/Q3 数学与先修边界只读交叉审查

日期：2026-09-23  
范围：

- `handbook/quantum-mechanics/02-observables-dynamics.md`
- `handbook/quantum-mechanics/03-levels-control.md`
- `work/research/round31-qm2-answers.md`
- `work/research/round31-qm3-answers.md`

性质：只读；未修改 Q2、Q3 或答案草稿。

## 结论

| 等级 | 数量 | 结论 |
|---|---:|---|
| P0 | 0 | 未发现使全章主结论失效的问题。 |
| P1 | 0 | 未发现错误概率、错误旋转方向或会系统性误导读者的问题。 |
| P2 | 3 | Q3 有一处表格源文件的通用 Markdown 兼容性风险、一处先修术语跳步，以及一组首次出现术语/文字清理问题。 |

Q2 的有限维测量、Robertson 关系、时不变与时变演化均复算通过；Q3 的 $2\pi$、能隙、热占据、旋转坐标系、RWA、Rabi 振荡和退相干矩阵均复算通过。下面先列需要修复的三项，再给通过证据。

## 需要修复的问题

### P2-1｜Q3 平台表中的 ket 裸竖线有通用 Markdown 兼容性风险

位置：`03-levels-control.md` 第 8 节“同样是量子比特，不同平台选的‘两个态’不同”，当前约第 444、447、448 行。

三列表格的表头和正常数据行各有 4 个 Markdown 分隔竖线，但以下三行分别有 6、6、8 个裸竖线：

- transmon 行中的 `$|2\rangle,|3\rangle,\ldots$`；
- 光子偏振行中的 `$|H\rangle,|V\rangle$`；
- 光子双轨行中的 `$|10\rangle_{ab},|01\rangle_{ab}$`、`$|00\rangle$`、`$|11\rangle$`。

本项目当前的 `build.mjs` 会先保护数学片段再交给 marked，所以第 32 轮首轮离线构建验证中没有观察到拆列，表格校验为 0 错误。这里的问题是源文件的可移植性：其他常见 Markdown 渲染器可能在数学渲染前把这些 ket 竖线当作额外列分隔符；同时它也不符合 `STYLE.md` 要求在表格内使用 `\lvert` 的源文件规范。因此本项保留为通用 Markdown 兼容性风险，不把它表述为当前离线 HTML 已经拆坏。

建议把表格内所有 ket 左竖线改为 `\lvert`，例如

```text
$\lvert10\rangle_{ab},\lvert01\rangle_{ab}$
```

正文段落和展示公式中的普通 ket 不受此问题影响，不需机械替换全章。

### P2-2｜Q3 首次使用“偏迹”时缺少定义或明确先修回链

位置：`03-levels-control.md` 第 7 节，当前约第 424 行；同时涉及本篇 `README.md` 中只把 Q2 写为 Q3 直接先修的表述。

正文从联合纯态直接跳到“把环境偏迹掉后得到”二维矩阵。矩阵本身正确，但 Q2 没有定义偏迹；直接按 Q2 → Q3 路线阅读的初学者无法从本章文字独立检查交叉项为什么恰好乘上 $\langle E_1|E_0\rangle$。

建议二选一：

1. 在式前补一句最小定义

   $$
   \rho_S=\operatorname{Tr}_E(|\Psi\rangle\langle\Psi|)
   =\sum_j{}_E\langle e_j|\Psi\rangle\langle\Psi|e_j\rangle_E,
   $$

   并用一行说明对环境基求和产生环境态内积；或
2. 明确把主篇第 03 章列为本节先修并链接其偏迹定义，同时仍用一句白话说明“偏迹保留系统自身全部测量统计、忽略环境记录”。

目前只在结果之后回链第 05 章噪声模型，不能替代首次出现处的概念定义。

### P2-3｜Q3 有未作白话消歧的首次术语和一个可见重复字

位置：

- 第 6.1 节约第 345 行：“Bloch–Siegert 位移”；
- 第 8 节平台表：“Zeeman 态”“Rydberg 辅助态”；
- 第 9 节：“平衡 Gibbs 分布”；
- 第 3 节约第 131 行：“处处处于”。

这些不改变数学，但不符合 `STYLE.md` 的“术语首次出现处给出白话解释”。建议作最短补充即可：

- Bloch–Siegert 位移：被 RWA 丢弃的反向旋转项造成的共振频率偏移；
- Zeeman 态：由磁场分裂并按磁量子数区分的能级；
- Rydberg 态：主量子数很高、相互作用强的高激发原子态；
- “Gibbs 分布”改成“第 3 节使用的热平衡 Boltzmann（Gibbs）分布”，避免突然换名；
- “处处处于”删去一个“处”。

DRAG 虽未展开英文全称，但正文已经用“正交通道加入主包络导数分量以抑制泄漏”说明操作含义，本轮不另计问题。

## Q2 独立复算

### 1. 谱测量、期望值与方差

- 简并本征值用整个本征子空间投影 $P_a$，条件态 $P_a|\psi\rangle/\sqrt{p(a)}$ 是当前明确声明的理想投影（Lüders 型）模型，正文没有把厄米性单独当成后态定律。
- $Z$ 算例中 $p_+=3/4,p_-=1/4$，故 $\langle Z\rangle=1/2$、$(\Delta Z)^2=3/4$、$\Delta Z=\sqrt3/2$。
- $N=300$ 时样本平均标准差为

  $$
  \frac{\sqrt3/2}{\sqrt{300}}=0.05,
  $$

  与正文一致。

### 2. 对易与 Robertson 关系

直接矩阵乘法给出

$$
[X,Z]=-2iY,
\qquad
[Z,X]=2iY.
$$

正文从中心化算符定义、Cauchy–Schwarz、$z-z^*$ 的虚部依次得到

$$
(\Delta A)^2(\Delta B)^2
\ge|\langle\widetilde A\widetilde B\rangle|^2
\ge\frac14|\langle[A,B]\rangle|^2.
$$

步骤、复共轭顺序和 $1/2$ 因子均正确。

- 在 $|{+i}\rangle$ 上，$\langle Y\rangle=1$，$\Delta X=\Delta Z=1$，左右两端都为 1。
- 在 $\cos(\pi/8)|0\rangle+\sin(\pi/8)|1\rangle$ 上，Bloch 向量为 $(1/\sqrt2,0,1/\sqrt2)$，两个标准差均为 $1/\sqrt2$，乘积为 $1/2$，但对易子期望为 0。正文正确说明“下界为零”不等于方差为零，也不把制备不确定关系误写成普遍测量扰动关系。

### 3. 时间演化、守恒量和旋转

- $U(t)=e^{-i\mathcal Ht/\hbar}$ 的求导、初值和酉性检查均正确。
- 对不显含时间的 $A$，

  $$
  \frac{d}{dt}\langle A\rangle
  =\frac{i}{\hbar}\langle[\mathcal H,A]\rangle
  $$

  的符号正确；正文也补充了 $A(t)$ 显含时间时的偏导项。
- $\mathcal H_Z=\hbar\omega Z/2$ 给 $R_z(\omega t)$，对 $|+\rangle$ 的 $X$ 基概率为 $(1\pm\cos\omega t)/2$。
- $\mathcal H_X=\hbar\Omega X/2$ 给

  $$
  p_1(t)=\sin^2(\Omega t/2),
  \qquad
  t_\pi=\pi/|\Omega|.
  $$

  若 $\Omega/(2\pi)=25\ \mathrm{MHz}$，答案草稿的 $20\ \mathrm{ns}$ 正确。
- 两段操作复算得

  $$
  R_z(\pi/2)R_x(\pi/2)|0\rangle=e^{-i\pi/4}|+\rangle,
  $$

  $$
  R_x(\pi/2)R_z(\pi/2)|0\rangle=e^{-i\pi/4}|{-i}\rangle.
  $$

  两者末态测 $X$ 的正结果概率分别为 1 与 $1/2$。正文当前已经把两时刻对易写成“常用充分条件”，并注明特殊不对易情形可能化简；没有再错误声称该条件逻辑上必要。

### 4. Q2 教学边界

章节开头明确限定有限维、纯态和理想投影测量；简并、单次读数与期望值、状态不确定度与仪器扰动、Hamiltonian 与 Hadamard、Hz 与 rad/s 都在首次关键使用处消歧。当前转义字符均为合法 `\qquad`；先前已修复的转义问题不计入未解决项。

Q2 正文和 8 题答案草稿在题意、符号、数值和结论上对应，未发现 P0/P1/P2。

## Q3 独立复算

### 1. 能隙、热占据与非谐性

用精确 SI 常数复算：

$$
h(5\ \mathrm{GHz})=3.313035075\times10^{-24}\ \mathrm J
=20.6767\ \mu\mathrm{eV},
$$

$$
\frac{hf}{k_{\rm B}}=0.239962\ \mathrm K.
$$

相应二能级热模型数值为：

| 条件 | $\Delta E/(k_{\rm B}T)$ | $p_1/p_0$ | $p_1$ |
|---|---:|---:|---:|
| 5 GHz，20 mK | $11.9981$ | $6.15585\times10^{-6}$ | $6.15581\times10^{-6}$ |
| 5 GHz，300 K | $7.99874\times10^{-4}$ | $0.99920045$ | $0.49980003$ |
| 4 GHz，50 mK（答案题） | $3.83939$ | $0.0215066$ | $0.0210538$ |

正文和答案的舍入均正确，且已经声明非简并、平衡、二能级假设。$T_{\rm eff}=0.23996/\ln99\approx52.2\ \mathrm{mK}$ 也正确。

$f_{01}=5.0$ GHz、$f_{12}=4.8$ GHz 给 $\alpha/(2\pi)=-200$ MHz；$20$ ns 与 $5$ ns 脉冲的 $1/\tau$ 量级分别为 50 MHz 与 200 MHz。正文把它限定为频宽量级而非泄漏概率，边界正确。

### 2. 自旋符号与能量基

由

$$
H=-\frac{\gamma\hbar B}{2}\sigma_z
$$

可得 $\Delta E=|\gamma|\hbar B$。$\gamma>0$ 时 $\sigma_z=+1$ 较低，$\gamma<0$ 时 $\sigma_z=-1$ 较低；答案草稿与正文一致。

把低能态命名为逻辑 $|0\rangle$ 后，全书 $Z|0\rangle=|0\rangle$ 的约定给

$$
H_0=-\frac{\hbar\omega_0}{2}Z.
$$

第 6 节另定义 $Z_E=|1\rangle\langle1|-|0\rangle\langle0|=-Z$，所以 $H_0=+\hbar\omega_0Z_E/2$。两节符号完全相容。

### 3. 旋转坐标系、RWA 与 Rabi 频率

在

$$
R=e^{-i\omega_dtZ_E/2},
\qquad
|\psi_{\rm lab}\rangle=R|\psi_{\rm rot}\rangle
$$

的约定下，

$$
-i\hbar R^\dagger\dot R=-\frac{\hbar\omega_d}{2}Z_E,
$$

所以残余自由项是 $\hbar(\omega_0-\omega_d)Z_E/2$，正文的 $\Delta=\omega_0-\omega_d$ 符号正确。

又有

$$
R^\dagger\sigma_+R=e^{i\omega_dt}\sigma_+,
\qquad
R^\dagger\sigma_-R=e^{-i\omega_dt}\sigma_-,
$$

余弦展开后，慢项确为

$$
\frac{\hbar\Omega}{2}
(e^{-i\phi}\sigma_++e^{i\phi}\sigma_-)
=\frac{\hbar\Omega}{2}
(\cos\phi X+\sin\phi Y_E).
$$

因此正文的

$$
H_{\rm RWA}=\frac\hbar2
[\Delta Z_E+\Omega(\cos\phi X+\sin\phi Y_E)]
$$

没有漏掉或多出二分之一。由于三个 Pauli 方向两两反对易，$K^2=(\Delta^2+\Omega^2)I$；激发振幅中的 $e^{-i\phi}$ 和概率

$$
P_1(t)=\frac{\Omega^2}{\Omega^2+\Delta^2}
\sin^2\!\left(\frac{\sqrt{\Omega^2+\Delta^2}\,t}{2}\right)
$$

均正确。

对 $\Omega/(2\pi)=10$ MHz、$\Delta/(2\pi)=6$ MHz，独立复算得

$$
\Omega_R/(2\pi)=11.6619\ \mathrm{MHz},
\quad
t_{\rm peak}=42.8746\ \mathrm{ns},
\quad
P_1^{\max}=0.735294.
$$

正文舍入正确。答案题的 4–3–5 算例给 $5$ MHz、$100$ ns、$0.64$，也正确。

### 4. 系统—环境矩阵和答案

从

$$
\alpha|0\rangle|E_0\rangle+\beta|1\rangle|E_1\rangle
$$

对环境取约化态，$01$ 元为 $\alpha\beta^*\langle E_1|E_0\rangle$，$10$ 元为其共轭，对角占据不变。正文与答案第 7 题正确；问题只在首次使用“偏迹”时没有给初学者定义，不在矩阵本身。

Q3 的 8 题答案草稿与题目逐题对应；除上述三个局部呈现/先修问题外，未发现公式、单位或数值错误。

## 最终判定

本轮计数为 **P0 = 0，P1 = 0，P2 = 3**。修复三项 P2 后，Q2/Q3 的核心数学与教学主线可进入下一轮回归。
