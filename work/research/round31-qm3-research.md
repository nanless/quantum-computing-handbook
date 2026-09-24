# 第 31 轮：Q3 从能级到物理量子比特——研究与实施记录

日期：2026-09-22

## 交付

- 新增正文：`handbook/quantum-mechanics/03-levels-control.md`
- 新增 8 道自检题完整答案草稿：`work/research/round31-qm3-answers.md`
- 图位预留：`../assets/qm-energy-levels.svg`，图注已明确“非等比例”；静态 SVG 由主审另行绘制。

没有修改共享附录、既有章节或 `sources/`。

## 1. 原始缺口与写作选择

现有第 02 章从抽象单量子比特态、Pauli 门和测量出发，第 09 章直接比较硬件路线。二者之间缺少一层实验桥梁：

1. $\Delta E=hf=\hbar\omega$ 中 Hz 与 rad/s 的区别；
2. 为什么实际多能级器件可以在受限条件下近似为量子比特；
3. 温度、非谐性、脉冲带宽、失谐和泄漏怎样共同限制控制；
4. 自旋磁矩符号怎样影响高低能态，计算基标签又怎样保持自洽；
5. 从实验室驱动到旋转坐标系/RWA 的系数约定，尤其是常见二倍因子错误；
6. 光子偏振/双轨编码为何不等于真空—单光子编码；
7. 系统—环境联合酉演化怎样在约化系统上表现为退相干。

正文按“能隙—热占据—多能级—自旋—驱动—环境—平台”推进，避免先堆平台名词。每个主要公式后都给操作含义或可复算数值。失谐 Rabi 概率不是直接列结果：正文先定义 $K=\Delta Z_E+\Omega(\cos\phi X+\sin\phi Y_E)$，由 $K^2=\Omega_R^2I$ 展开 $U_{\rm RWA}$，再显式取 $\langle1|U_{\rm RWA}|0\rangle$ 和模平方。

## 2. 一手或大学官方资料核查

### 常数与热算例

NIST 给出新 SI 中的精确值：

- $h=6.62607015\times10^{-34}\ \mathrm{J\,s}$；
- $k_{\rm B}=1.380649\times10^{-23}\ \mathrm{J/K}$。

来源：<https://www.nist.gov/si-redefinition/meet-constants>

据此重新计算 5 GHz：

$$
hf=3.313035075\times10^{-24}\ \mathrm J,
\qquad
hf/k_{\rm B}=0.239962\ \mathrm K.
$$

平衡非简并二能级模型中：

- 20 mK：$p_1/p_0=e^{-11.9981}=6.16\times10^{-6}$，$p_1$ 与之在所示精度内相同；
- 300 K：$p_1/p_0=e^{-0.00079987}=0.999200$，$p_1=0.499800$。

正文明确限制：这不是厂商指标；300 K 下对弱非谐振荡器截成两级不可靠；冷台温度也不保证器件有效温度。

### 两能级驱动、旋转坐标系和自旋

MIT 6.728 两态系统讲义给出失谐下的 Rabi 概率、广义 Rabi 频率与共振 $\pi$ 脉冲条件；MIT 22.51 课程讲义从 $\boldsymbol\mu=\gamma\mathbf S$ 讨论自旋在磁场中的演化。它们共同支持正文的推导结构，同时也显示不同讲义会把驱动矩阵元命名为 $V$、$\omega_1$ 或 $\Omega$，所以必须从完整 Hamiltonian 核对二倍因子。

- <https://ocw.mit.edu/courses/6-728-applied-quantum-and-statistical-physics-fall-2006/resources/twolevel04/>
- <https://ocw.mit.edu/courses/22-51-quantum-theory-of-radiation-interactions-fall-2012/resources/mit22_51f12_ch5/>
- 辅助核对 RWA：<https://www.ocw.mit.edu/courses/5-61-physical-chemistry-fall-2017/resources/mit5_61f17_lec36/>

正文固定的约定是

$$
H_{\rm lab}
=\frac{\hbar\omega_0}{2}Z_E
+\hbar\Omega\cos(\omega_dt+\phi)X,
$$

其中 $Z_E=|1\rangle\langle1|-|0\rangle\langle0|$，以免与全书 $Z|0\rangle=|0\rangle$ 的计算基约定混淆。在

$$
R(t)=e^{-i\omega_dtZ_E/2}
$$

约定下，RWA 给出

$$
H_{\rm RWA}
=\frac\hbar2[\Delta Z_E+\Omega(\cos\phi X+\sin\phi Y_E)],
\quad \Delta=\omega_0-\omega_d.
$$

所以本章的共振结果是 $P_1=\sin^2(\Omega t/2)$。这一步显式保留了余弦展开带来的 $1/2$，避免把实验室振幅、有效 Hamiltonian 系数和概率振荡角频率混成一个名字。

### transmon、非谐性与泄漏

Koch 等的 transmon 原始论文说明：随 $E_J/E_C$ 增大，电荷色散指数下降，而非谐性按较弱的幂律下降，因此能在降低电荷噪声敏感性的同时保留选择性控制所需的非谐性：

<https://doi.org/10.1103/PhysRevA.76.042319>

Motzoi 等的 DRAG 原始论文明确把问题表述为“从弱非谐振荡器的多能级中选出两级”，并指出短时标简单控制会耦合泄漏能级；其解析方案使用与主包络导数相关的第二控制：

<https://doi.org/10.1103/PhysRevLett.103.110501>

正文中的 $f_{01}=5.0\ \mathrm{GHz}$、$f_{12}=4.8\ \mathrm{GHz}$ 仅是教学假设。$1/\tau$ 也只作为频谱宽度量级，未被写成通用泄漏阈值或厂商性能。

### 光子与中性原子编码边界

Nature Communications 的实验论文直接说明：常见离散变量双轨光子量子比特是一颗光子占据两个正交模式之一，模式可取水平/垂直偏振；同文另行区分“单轨”真空/单光子编码：

<https://doi.org/10.1038/s41467-018-06055-x>

Evered 等的中性原子纠缠门实验明确使用超精细基态量子比特，并通过 ground–Rydberg 驱动与 Rydberg 相互作用实现并行纠缠门，直接支持正文把“计算态”和“门的辅助态”分开：

- <https://doi.org/10.1038/s41586-023-06481-y>

早先采用全 Rydberg 两态的模拟器工作不能单独证明“长寿命超精细计算态加 Rydberg 辅助态”这一具体控制链，因此没有再把 Ebadi 2021 作为该句的直接证据。

## 3. 独立复算

### 热占据

使用精确 SI 常数复算了正文 5 GHz 的 20 mK、300 K 两组数，以及答案草稿中 4 GHz、50 mK 的结果：

$$
\frac{hf}{k_{\rm B}T}\approx3.839,
\quad
p_1/p_0\approx0.0215,
\quad
p_1\approx0.0211.
$$

### 失谐 Rabi

正文算例 $\Omega/2\pi=10\ \mathrm{MHz}$、$\Delta/2\pi=6\ \mathrm{MHz}$：

$$
\Omega_R/2\pi=\sqrt{136}\ \mathrm{MHz}\approx11.66\ \mathrm{MHz},
$$

$$
t_{\rm peak}=1/[2(11.66\ \mathrm{MHz})]\approx42.9\ \mathrm{ns},
\qquad
P_1^{\max}=100/136\approx0.7353.
$$

自检题 $4$–$3$–$5$ 三角形给出 $\Omega_R/2\pi=5\ \mathrm{MHz}$、$P_1^{\max}=16/25=0.64$、$t_{\rm peak}=100\ \mathrm{ns}$。

### 退相干矩阵

从

$$
\alpha|0\rangle|E_0\rangle+\beta|1\rangle|E_1\rangle
$$

对环境偏迹，$01$ 元确为 $\alpha\beta^*\langle E_1|E_0\rangle$，对角元不变。正文只把它称为纯退相位直觉，并把能量交换导致的弛豫回链到第 05 章，未拿一个模型代替全部开放系统动力学。

## 4. 保留的限制与后续事项

- 图文件 `handbook/assets/qm-energy-levels.svg` 已由主审制作；正文给出正确相对路径，并明确图意和“非等比例”要求。图形本身留待下一轮阅读版交叉审查。
- Q2 已落盘，本章开头链接 `02-observables-dynamics.md`；谐振子的升降阶推导回链 Q4，避免在本章重复。
- 练习答案先放在独立草稿，未改共享 `appendices/exercises.md`；正文按要求预留 `#量子力学-q3` 链接。
- 没有使用任何 2025–2026 厂商排行榜或会快速过时的设备数字。唯一具体 GHz/MHz 参数均标为教学假设。
