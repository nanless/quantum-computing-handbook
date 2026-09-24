# 第 41 轮：先修、数学基础与量子力学只读审稿

审稿范围：`handbook/appendices/prerequisites.md`、`01-math.md`、`02-single-qubit.md` 至 `05-noise-channels.md`、量子力学 Q1–Q4 及这些章节在 `appendices/exercises.md` 中的答案。为核对“动手”先修衔接，另只读查看第 15 章的代码开头；为核对算法入口，另只读查看第 06 章的可逆 oracle 开头。没有修改正文或 `sources/`。本文的“未发现”仅限上述逐段阅读与抽样复算，不代表全领域穷尽。

## 需要修的教学缺口

1. **P2｜动手路线缺少编程准备的明确信号。** `appendices/prerequisites.md:9–17` 的路线表有读基础、算法、硬件、波函数、实验数据五条，但第 15 章从第 28–73 行马上使用 Python/NumPy 的数组、矩阵乘法 `@`、`np.vdot`、`np.kron`，随后又用随机采样。先修页第 17 行只说“编程不是理解前五章的前提”，读者可能错误地以为做第 15 章也完全无需编程准备。建议在路线表增一条可选的“亲手运行与改写实验代码”：基本 Python 表达式、列表/数组与索引、函数/循环、安装/导入 NumPy；明确这不是阅读前五章或理解量子理论的强制先修。可用 2×2 矩阵乘向量代码与第 01 章的手算对应，而不必变成完整 Python 课程。[NumPy 官方初学者教程](https://numpy.org/doc/stable/user/absolute_beginners)从安装、导入、数组入门；[IBM 量子信息入门](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information)把数学而非 Python 列为理论课的建议准备。这也支持区分“读懂理论”与“运行代码”。

2. **P2｜进入第 06 章前没有直观的二进制异或例子。** `appendices/prerequisites.md:12,56–62` 的算法准备和自测只覆盖模 15 周期与查询/门数。`06-algorithmic-primitives.md:15–23` 第一次以 $y\oplus f(x)$ 解释可逆 oracle，但此前正文没有二元异或真值表；仅 `appendices/notation.md:27` 给一句“模 2 加法”。建议在先修页算法路线或自测中加四行真值表（`0⊕0=0,0⊕1=1,1⊕0=1,1⊕1=0`），再给一个非单射函数 $f(0)=f(1)=0$，比较“只输出 $f(x)$”丢失输入与“保留 $x$ 并写入 $y\oplus f(x)$”可逆，列出输入 `(x,y)` 的两个不同样本。第 06 章首次出现符号时仍宜就地定义。IBM 官方课程在讲量子线路前先列出 [XOR 真值表](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/quantum-circuits/circuits)，并另讲[经典运算的可逆模拟](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/quantum-algorithmic-foundations/simulating-classical-computations)。

3. **P2｜Bloch 球的坐标映射直接给结论，首次读者难以复算。** `02-single-qubit.md:39–71` 从 $\cos(\theta/2)|0\rangle+e^{i\varphi}\sin(\theta/2)|1\rangle$ 直接给 $\vec r=(\sin\theta\cos\varphi,\sin\theta\sin\varphi,\cos\theta)$；第 03 章和 Q2 又直接由 Bloch 向量读取 Pauli 期望，缺少从矩阵到坐标的桥。建议加入 $r_j=\langle\psi|\sigma_j|\psi\rangle$ 的三次 2×2 乘法，并用非轴点的具体态 $\sqrt3|0\rangle/2+i|1\rangle/2$ 核对 $(r_x,r_y,r_z)=(0,\sqrt3/2,1/2)$，再求至少一个测量概率。图旁可标注“坐标是三个 Pauli 期望，不是粒子在三维空间的真实位置”。[IBM 官方 Bloch 球讲解](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/bloch-sphere)从密度矩阵与 Pauli 系数解释坐标。`02-single-qubit.md:135` 的 “SU(2) 二维表示”未定义，对入门读者可改为括注选读，不宜当半角的唯一解释。

4. **P2｜Q4 的核心对易关系在从微积分过渡到谐振子时跳步。** `quantum-mechanics/04-wavefunctions-models.md:35–61` 已定义 $\hat x\psi=x\psi$、$\hat p\psi=-i\hbar\psi'$，但第 198 行直接用 $[\hat x,\hat p]=i\hbar I$ 推导升降算符；第 200–221 行的零点能正靠此关系。建议在第 2 节或第 5 节前对光滑试探函数 $f$ 算一次 $\hat x\hat p f=-i\hbar x f'$ 与 $\hat p\hat x f=-i\hbar(f+xf')$，相减得 $i\hbar f$；再补一句共同定义域条件，避免把无界算符恒等式当作任意函数上的等式。MIT 8.04 的[波函数、算符与谐振子课程序列](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/pages/lecture-notes/)把位置/动量表示先于升降算符，符合这样的衔接。

5. **P2｜CHSH 的 $2$ 与 $2\sqrt2$ 目前是未计算的宣告。** `03-multiple-qubits.md:194–208` 正确地注明测量设置独立与 Bell 局域性，也给出 $S$ 和两个界，但没有哪怕一组具体设置、四个相关值的表，也没有章节自检让读者算出界。建议先用 $A_0=Z,A_1=X,B_0=(Z+X)/\sqrt2,B_1=(Z-X)/\sqrt2$、$|\Phi^+\rangle$，逐项算 $\langle Z\otimes Z\rangle=\langle X\otimes X\rangle=1$ 和交叉期望为 0，得到四个 $\pm1/\sqrt2$ 与 $S=2\sqrt2$；再以确定取值 $a_0,a_1,b_0,b_1\in\{\pm1\}$ 展示经典 $a_0(b_0+b_1)+a_1(b_0-b_1)=\pm2$，说明概率混合仍不超 2。配一张四行“设置—相关值”表即可，比增加抽象段落更适合初学者。[IBM 官方 CHSH 教学](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/chsh-game)逐组计算量子策略；[CHSH 原始论文](https://doi.org/10.1103/PhysRevLett.23.880)用于边界核对。

6. **P2｜隐形传态恰在关键恒等式处略去展开。** `04-circuits-protocols.md:101–124` 从初态与两步门直接跳到四个 $QA$ 分支，随后仅说“按结果校正”；当前练习第 4 章也没有要求重建分支。建议至少写出初态的四项，再列 $\mathrm{CNOT}_{Q\to A}$ 后四项以及 Hadamard 后按 `00,01,10,11` 分组的中间表，并列 Bob 的校正 $I,X,Z,ZX$（明确采用统一门序）。这会让“2 位经典消息为何足够”可以手算，而非只需相信结果。[Bennett 等人的原始方案](https://doi.org/10.1103/PhysRevLett.70.1895)与 [IBM 基础课程纠缠应用](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/introduction)可作一手核对。当前分支公式本身未见错。

## 可选扩展，暂不算硬错误

- **P3｜Schmidt 与熵可多给一个非最大纠缠算例。** `03-multiple-qubits.md:113–172` 已有 $\sqrt3|00\rangle/2+|11\rangle/2$ 的约化态，紧接着却仅对 Bell 态算熵。顺手计算 $-\tfrac34\log_2\tfrac34-\tfrac14\log_2\tfrac14\approx0.811$ bit，并说明 0、1 bit 两端的意义，有助于入门研究生区分“是否纠缠”与“纠缠多少”。[IBM 官方 Schmidt 分解教程](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)可核对权重定义。矩阵奇异值分解的完整证明可放选读框，不宜强塞到先修页。
- **P3｜Q1 的三种路径记录情形已有表，但图只画无记录情形。** `quantum-mechanics/01-experiments-states.md:204–296` 给 $\gamma=0,0.6,1$ 的分析；`assets/qm-interference.svg` 明确只画无记录。若加一张简洁的 $P_0(\phi)$ 三条曲线（共同中心 $1/2$、起伏幅度分别 0、0.3、0.5），可让“部分记录只是减弱可见度”的中间情形立即看见。若画出具体可区分度界，须注明等权路径与纯记录态等条件；[Englert 原始论文](https://doi.org/10.1103/PhysRevLett.77.2154)是边界核查来源。

## 核对结果与边界

已手工复算：先修页 7 题与第 1–5 章练习答案的主要数字；Q1 的 $\gamma$ 非对角元与输出概率；Q2 的 Robertson 两例、$X/Z$ 操作顺序及 Hz/rad/s；Q3 的 5 GHz 能隙、20 mK 热占据、旋转坐标系相位与 Rabi 频率；Q4 的势阱中间区概率、左半井概率、升降算符常数项与有限方势垒的透射率及近似。**未确认出需要勘误的硬性公式错误**。上面 P2 主要是阅读门槛与推导连续性缺口；P3 是有价值但非必需的扩展。基础物理模型、原始实验和课程门槛已分别与 MIT/IBM/NIST/原论文的一手资料交叉核对；器件当前性能不在本轮范围内。
