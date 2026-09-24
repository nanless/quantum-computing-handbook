# 第 65 轮｜基础九篇独立正确性深审

范围：`handbook/00-overview.md`、`01-math.md`、`02-single-qubit.md`、`03-multiple-qubits.md`、`04-circuits-protocols.md`，以及 `handbook/quantum-mechanics/01–04`。本轮检查定义、符号和位序、关键推导、具体数值、图示标签、自检题与答案的对应；并单独复算了容易藏符号或单位错误的例子。`sources/` 和共享答案附录未改。

## 逐篇核查

| 篇章 | 独立核对的关键点 | 结果与本轮处理 |
|---|---|---|
| 00 全景 | $H|+\rangle=|0\rangle$、$H|-\rangle=|1\rangle$；Grover 查询次数与墙钟时间的区分；随机数例的频率和安全性边界 | 未发现确定错误。公式和参考对象一致；保留“问题地图而非现实优势承诺”的限定。 |
| 01 数学 | 复数共轭、Cauchy–Schwarz 展开、$H^\dagger H=I$、$X$ 谱分解、迹循环、张量积位序、Bayes 表格、Bernoulli 方差、$n$ 与 $N=2^n$ | 逐格复算正确。特别核对 $M[1,i]^T=[0,2i]^T$ 与 100 次 $p=1/4$ 的频率标准差 $\sqrt3/40\approx0.0433$；答案一致。 |
| 02 单量子比特 | $Y=iXZ$ 的符号、Bloch 的 $r_y=2\operatorname{Im}(\alpha^*\beta)$、$R_y/R_z$ 半角与全局相位、投影测量及 POVM/测量工具区别 | 与所定 Pauli 约定一致；$|{+i}\rangle$ 的 $Y=+1$、$R_z(\pi/2)|+\rangle\sim|{+i}\rangle$ 均正确。POVM 相同但后态不同的两个工具也满足 $M_k^\dagger M_k=N_k^\dagger N_k=E_k$。 |
| 03 双比特 | $ad-bc$ 可分判据含零边界、Bell 基换基、偏迹四格规则、Schmidt 权重、$XX+ZZ$ 可分上界、CHSH 量子上界和单配性 | 独立按 $00,01,10,11$ 基序核对，式与图一致。$q=0.8$ 白噪声模型两组相关值均为 $0.8$，1000 次每组期望计数 $450,450,50,50$ 正确。绝对值版见证仍只是充分条件，正文已有此限定。 |
| 04 电路协议 | CNOT 四列、不可克隆/不可删除的内积论证、传态四分支及门序、超密编码解码、受控本征相位回踢 | 传态位序固定为 $Q,A,B$；`11` 分支为 $XZ|\psi\rangle$，Bob 用 $ZX$ 校正，乘积为 $I$；超密编码 `11` 也给 $|\Psi^-\rangle$。正文与答案一致。 |
| Q1 实验与状态 | $B U_\phi B|0\rangle$ 的两输出、部分路径记录的 $\gamma=\langle d_1|d_0\rangle$ 与可见度、$z+\to x+\to z$ 的条件计数 | 公式正确。修订 §4.2：原句“两个 $SG_x$ 结果都被探测并保留”容易误作吸收式探测后还把同一原子送往下一台仪器；现在明确为理想非破坏式路径记录，两束继续传播，吸收式末端计数不适用。 |
| Q2 可观测量与动力学 | 谱投影的简并处理、Robertson 推导与 $[X,Z]=-2iY$、$U=e^{-i\mathcal Ht/\hbar}$、$Z/X$ Hamiltonian 和时序反例 | 公式与基序一致。$f=10\,\mathrm{MHz}$ 时 $t_\pi=50\,\mathrm{ns}$；先 $X$ 后 $Z$ 的 $\pi/2$ 脉冲把 $|0\rangle$ 送到 $e^{-i\pi/4}|+\rangle$，交换顺序送到 $e^{-i\pi/4}|{-i}\rangle$，分别测 $X$ 得 1 和 $1/2$。 |
| Q3 能级与控制 | $\Delta E=hf=\hbar\omega$、热平衡占据、transmon 绝对/相对非谐性、旋转框架与 RWA 相位及二倍因子、失谐 Rabi | 独立复算：5 GHz 为 $3.313035075\times10^{-24}$ J、$20.6783\,\mu\mathrm{eV}$、$\Delta E/k_B=0.239962$ K；20 mK 的 $p_1=6.1558\times10^{-6}$，300 K 的 $p_1=0.499800$；$\Omega/2\pi=10$ MHz、$\Delta/2\pi=6$ MHz 时首峰 $42.8746$ ns、峰值 $100/136=0.735294$。文中四舍五入正确。 |
| Q4 波函数模型 | 势阱正交归一与 $E_n\propto n^2/L^2$、左半井干涉积分、$a^\dagger a$ 的常数项、基态不确定度、方势垒边界匹配及厚势垒近似 | 复算 $P_{\rm middle}=1/2+1/\pi=0.81831$、$P_{\rm left}(0)=0.924413$、$T(\kappa L=1,E=V_0/2)=0.419974$、$T(3)=0.00986604$，与正文和答案一致。修订 §5：$\|a|\nu\rangle\|^2=\nu$ 只在 $|\nu\rangle$ 归一化时成立，现写出前提及非归一化时的公式。 |

## 图与自检题

逐项对照本组相关 SVG 中的图名、标签及正文约定：复平面图把复数而非 Bloch 球标清；Bloch 球六轴态的 $\pm Y$ 符号正确；Bell 电路与传态图的高位、控制目标、校正门序一致；偏迹图中 $4\times4\to2\times2$ 的两格求和正确；干涉图使用明确的 Hadamard 相位约定；能级图的相等/不等相邻差正确；势阱图画的是 $\sqrt L\phi_n$ 与 $L|\phi_n|^2$，曲线节点与归一化面积正确。抽查并逐题对应阅读 00–04 与 Q1–Q4 的现有答案，没有发现必须改动共享答案或 `round31-qm*-answers.md` 的确定错误。

## 一手核对来源

- John Watrous, *The Theory of Quantum Information*，作者提供的完整讲义和章节目录：https://cs.uwaterloo.ca/~watrous/TQI/ 。用于谱分解、测量工具、偏迹、纠缠与量子信息基本定义。
- IBM Quantum Learning，传态的四类经典消息与 Pauli 校正：https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/teleportation 。其资料按自身比特显示约定陈列；本书明确使用 $Q,A,B$，不能直接复制位串顺序。
- IBM Quantum Learning，CHSH 游戏与 Tsirelson 上界：https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/chsh-game 。与本书的 $2$、$2\sqrt2$ 结论一致。
- MIT OpenCourseWare 8.321，第 8 讲时变 Hamiltonian 与时间顺序：https://ocw.mit.edu/courses/8-321-quantum-theory-i-fall-2017/579cb61c4eaa494b9adb90830d921099_MIT8_321F17_lec8.pdf 。支持 Q2 对不对易分段操作顺序的限定。
- Koch 等人，transmon 原始论文，*Physical Review A* 76, 042319 (2007)：https://doi.org/10.1103/PhysRevA.76.042319 。摘要明确区分电荷色散指数下降和非谐性较慢变化；本书进一步按固定参数区分绝对/相对非谐性。
- MIT OpenCourseWare 8.04，课程大纲和势阱/谐振子教学范围：https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/pages/syllabus/ ；MIT 6.772 单势垒系数：https://ocw.mit.edu/courses/6-772-compound-semiconductor-devices-spring-2003/cf610e766603218f5e15fe998daf18d4_Lecture6v2.pdf 。后者用于独立核对 Q4 的双边同质量方势垒透射率；正文还列明了波函数/导数连续的适用条件。
- Pati 与 Braunstein，不可删除原始论文预印本：https://arxiv.org/abs/quant-ph/9911090 。核对“擦除系统”和“连同辅助系统无痕删除副本”是不同任务。
- Englert，路径信息与条纹可见度原始论文：https://doi.org/10.1103/PhysRevLett.77.2154 。本书的 $\mathcal V=|\gamma|$ 仅在等权、理想无损模型使用，未外推至任意干涉仪。

## 范围边界

本轮不是对量子计算全部文献的穷尽证明。计算和模型均按正文写明的理想条件核对：纯态或标出的混态、有限维门电路、等权无损干涉、二能级热平衡、RWA、同质量矩形势垒等。真实器件的漂移、读出反作用、泄漏和实验漏洞不能由这些理想算式单独保证。参考论文的 DOI/摘要或开放讲义可核对的内容已核对；受订阅限制的论文正文没有假装逐页阅读。剩余硬件性能和标准时效由其他分组负责。
