# 第 38 轮：算法新增内容独立交叉审

日期：2026-09-23。性质：只读交叉审，未修改 `handbook/06-algorithmic-primitives.md`、`07-algorithms.md`、`16-advanced-algorithms-verification.md` 或 `17-computation-models.md`。

## 结论

本轮检查了第 37 轮新增的 Grover 二维矩阵、QPE 等比和及最近网格点界、Shor 模乘本征态和完整寄存器扩展、QSVT 分叉图与 $T_2$ 算例、MBQC 测量角和伴随算符、qDRIFT 平均信道条件，以及第 17 章八位搜索数值。发现 **1 个 P2 表述缺口**；已即时告知算法作者和主审。其余所列等式与来源边界在本轮核查范围内未见待修问题。

| 等级 | 位置 | 问题与建议 |
|---|---|---|
| P2 | 第 07 章 §3.2 | 先说模乘 $U_a$ 只定义在与 $N$ 互素的剩余类子空间；后面为完整量子寄存器扩展只举 $y\ge N$ 固定，却没有交代 $0\le y<N$ 且 $\gcd(y,N)>1$ 的基态。因为 $\gcd(a,N)=1$，映射 $y\mapsto ay\bmod N$ 实际置换**所有** $0\le y<N$ 的剩余类，包括非单位元素。例如 $N=35,a=2$ 时，非单位 $5\mapsto10$ 仍可逆。建议直接在全部合法剩余类上定义模乘，并让 $y\ge N$ 固定，从而明确整个 $2^n$ 维寄存器上的置换酉。参考 [IBM Quantum Learning 的 Shor 讲义](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/shor-algorithm)。 |

## 逐项复算

1. **Grover 反射符号**：在 $(|G\rangle,|B\rangle)$ 顺序下，$D=2(s,c)^T(s,c)-I$、$S_G=\operatorname{diag}(-1,1)$，故 $DS_G=\left(\begin{smallmatrix}\cos2\theta&\sin2\theta\\-\sin2\theta&\cos2\theta\end{smallmatrix}\right)$。作用在 $(\sin\theta,\cos\theta)^T$ 上确为 $(\sin3\theta,\cos3\theta)^T$；第 06 章矩阵和乘法次序一致。[Boyer 等原论文](https://arxiv.org/abs/quant-ph/9605034)也给任意迭代次数的正弦平方成功率。
2. **QPE 振幅与下界**：对 $\delta=\phi-y/M$，$M^{-1}\sum_{k=0}^{M-1}e^{2\pi ik\delta}=e^{\pi i(M-1)\delta}\sin(\pi M\delta)/(M\sin\pi\delta)$，相位因子符号正确。圆周最近点可取 $|\delta|\le1/(2M)$ 的整数代表，利用 $\sin z\ge2z/\pi$ 与 $|\sin z|\le|z|$ 得概率至少 $4/\pi^2$。直接复数求和在 $M=4,\phi=1/3$ 得概率 $(0.0625,0.6997595264,0.1875,0.0502404736)$，和为 1；第 06 章表正确。[IBM 官方相位估计教程](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/phase-estimation-procedure)给同一傅里叶分析。
3. **Shor 本征态**：系数 $e^{-2\pi ikj/r}$ 在 $j\mapsto j+1$ 后得到本征值 $e^{+2\pi ik/r}$；对 $k$ 作 Fourier 和还原 $|1\rangle$，各本征相位权重为 $1/r$。第 07 章这两处推导正确；缺口只在完整寄存器上那些非单位基态的定义说明。
4. **QSVT 图与两次信号调用**：第 16 章图从 block encoding 分别进入“$U,U^\dagger$ 与投影反射”及 Hermitian 特例的 qubitization/QSP，未把后者列为一般 QSVT 的必经前置。取 $W=xI+i\sqrt{1-x^2}X$，直接平方得左上元 $x^2-(1-x^2)=2x^2-1$，$x=1/2$ 时为 $-1/2$。对一般非 Hermitian 矩阵须分别处理左右奇异向量，正文已限定。[Gilyén 等 QSVT 原论文](https://arxiv.org/abs/1806.01838)的 projected unitary encoding 框架支持这一路线区分。
5. **MBQC 角度符号**：$\langle+_\alpha|=(\langle0|+e^{-i\alpha}\langle1|)/\sqrt2$，投影后输出为 $e^{-i\alpha/2}HR_z(-\alpha)|\psi\rangle/\sqrt2$；负号结果在前面加 $X$。$R_z(\alpha)X=XR_z(-\alpha)$、$HX=ZH$，故 $J(-\alpha)X=ZJ(\alpha)$。两个结果概率各 $1/2$，第 17 章的前馈角度变号与全局相位正确。[Raussendorf 等原论文](https://arxiv.org/abs/quant-ph/0108118)是测量角适应性的一手来源。
6. **qDRIFT 条件**：第 07 章 $\lambda=\sum|h_j|$、$p_j=|h_j|/\lambda$、时间片 $\lambda t/N$ 一阶平均给 $H$；对 $0.6X+0.8Z$，$p_X=3/7,p_Z=4/7$。正文把标准 $O(\lambda^2t^2/\epsilon)$ 界限定到**平均信道**，并说明固定一条随机线路反复测量不能直接套用。与 [Campbell 原论文](https://arxiv.org/abs/1811.08017)的平均随机电路通道口径一致。
7. **八位搜索数值**：$\theta=\arcsin(1/16)$，独立计算得 $p_{12}=0.9999470421$、$p_{13}=0.9861862401$，与第 17 章一致；它仍只是 oracle 查询数演示，正文已经计入可逆加密、比较、反计算与扩散反射的额外工作。

## 审查边界

本轮只复核上述新增区域及列出的原始论文/官方课程对应事实，没有重新审查四章的所有旧段落、阅读版全页布局、共享答案或全部量子算法。第 07 章的 P2 在本报告写入时仍待算法作者修订；修订后应再读该段，确认“完整寄存器置换酉”的对象与示例一致。
