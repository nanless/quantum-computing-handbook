# 第 37 轮：算法、复杂度与计算模型研究记录

日期：2026-09-23。范围仅限 `06-algorithmic-primitives.md`、`07-algorithms.md`、`16-advanced-algorithms-verification.md`、`17-computation-models.md`。本轮核查的是这些章节中可识别的概念、推导、算例和模型边界；不能由此声称量子算法领域已无其他可补充内容。

## 资料核查

1. [IBM Quantum Learning：相位估计步骤](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/phase-estimation-procedure) 给出逆 QFT 后的有限等比和、最近网格点概率和重复估计的条件。第 6 章新补的 $A_y=M^{-1}\sum_k e^{2\pi ik\delta}$、正弦商和 $4/\pi^2$ 下界与其相符；下界也在正文中独立推得。
2. [Boyer 等：Grover 精确成功率](https://arxiv.org/abs/quant-ph/9605034) 分析任意迭代次数、多解与未知解数。第 6 章的二维反射矩阵直接推出 $\sin^2[(2k+1)\theta]$；第 17 章八位搜索的数值已单独核算。
3. [Shor 原论文](https://arxiv.org/abs/quant-ph/9508027) 与 [IBM Quantum Learning：Shor 算法](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/shor-algorithm) 支持阶寻找、受控模乘、连分数与分母约分的区分。第 7 章补全本征态的指标平移验证、$|1\rangle$ 的等权展开，并明确模乘先置换全部 $0\le y<N$ 的剩余类，再对 $y\ge N$ 固定完成寄存器上的可逆扩展。
4. [Beals 等：量子查询的多项式下界](https://arxiv.org/abs/quant-ph/9802049) 明确区分 partial 与 total Boolean function；原文给出 $O(T^6)$ 经典确定性查询上界。第 6、16 章现有“至多多项式相差”的表述准确，未把查询结论误移到端到端时间。
5. [Campbell：qDRIFT 原论文](https://arxiv.org/pdf/1811.08017) 第 3–6 页明确区分随机线路的平均信道、单个随机酉和金刚石距离；附录给出平均信道误差随 $\lambda^2t^2/N$ 缩放。第 7 章增补“每次运行独立重新抽样”这一使用条件。
6. [Gilyén、Su、Low、Wiebe：QSVT 原论文](https://arxiv.org/pdf/1806.01838) 第 3 页将一般构造写成 projected unitary encoding $\widetilde\Pi U\Pi$ 与多项式奇异值变换；其 qubitization 章节提供相关构造视角。第 16 章旧流程图把 qubitization 画成一切 QSVT 的必经步骤，现已改成并列的构造／分析路线，且说明一般非 Hermitian 情形不能随意写 $P(A)$。
7. [Raussendorf、Browne、Briegel：单向量子计算原论文](https://arxiv.org/pdf/quant-ph/0108118) 第 2–3 页使用赤道测量基与基于先前结果调整测量角的规则。第 17 章补出二比特 $J(\alpha)=HR_z(-\alpha)$ 算例，明确定义角度与 $R_z$ 的符号约定，并推导 $J(-\alpha)X=ZJ(\alpha)$。
8. [Aharonov 等：绝热与门模型等价](https://arxiv.org/abs/quant-ph/0405098) 是第 17 章已有“多项式等价”结论的原始依据。本轮保留其对理想模型、谱隙和物理设备的边界描述。
9. [Brassard 等：幅度估计](https://arxiv.org/abs/quant-ph/0005055) 支持第 7 章的 $O(1/\epsilon)$ 理想查询标度；正文继续明确 $A,A^\dagger$ 与好态反射成本。

## 本轮发现与修复

| 位置 | 发现 | 修复 |
|---|---|---|
| 第 6 章振幅放大 | 只给旋转结果，初学者看不到反射为何生成 $2\theta$ 旋转 | 写出好态／坏态坐标、两次反射的 $2\times2$ 矩阵和一次迭代的三角变换 |
| 第 6 章相位估计 | 从逆 QFT 直接跳到概率正弦商，缺少振幅与模平方步骤 | 从有限等比和推到带整体相位的振幅，再推概率与最近点下界 |
| 第 7 章 Shor | 本征向量和 $|1\rangle$ 等权叠加缺少核算；模乘门的完整可逆作用容易被忽略 | 补指标平移、正交 Fourier 和；证明 $\gcd(a,N)=1$ 时模乘置换全部 $N$ 个剩余类，并固定 $y\ge N$ 的态完成可逆扩展 |
| 第 7、16、17 章模拟公式 | $e^{-iHt}$ 没有统一说明 $\hbar=1$，且第 7 章未在公式处声明 $H$ 与时间无关 | 写出物理单位版本 $e^{-iH_{\rm energy}t/\hbar}$、时间依赖时的时间排序，以及 $\alpha t$ 的无量纲条件 |
| 第 7 章 qDRIFT | 误差界限定为平均信道，但读者可能固定一条线路重复测量 | 明确每次独立重新抽样的条件，并加原论文直接链接 |
| 第 16 章 QSVT 图 | 串联图暗示 qubitization 是一般 QSVT 的必经前置电路 | 改图与文字，区分一般酉编码／投影反射路线和 Hermitian 的 qubitization 视角 |
| 第 17 章 MBQC | 只说前馈会改测量角，没有算出改多少 | 推广至 $|\pm_\alpha\rangle$ 测量，推得角度变号与已知 $X^mZ$ 伴随算符 |
| 第 7、16、17 章文字 | 少数总括句和口语化表述过于绝对 | 换成明确的范围和自然叙述 |

## 独立核算与二次检查

- 用独立求和式核算 $M=4,\phi=1/3,y=1$ 的概率为 $0.6997595264$；$M=2048,\phi=1/12,y=171$ 的概率为 $0.6839180492$，与第 6、7 章小数吻合。
- 用直接三角函数核算 $N=256,M=1$ 搜索在 $r=12,13$ 次后成功率分别为 $0.9999470421,0.9861862401$，与第 17 章吻合。
- 第 17 章新测量公式按 $R_z(\beta)=e^{-i\beta Z/2}$ 逐项展开；测量两个结果的范数平方均为 $1/2$，$J(-\alpha)X=ZJ(\alpha)$ 的矩阵恒等式成立。
- 重读四章中的查询复杂度、门复杂度、输入输出和成功率表述；本轮未发现其他需立即更正的数学错误。此结论限于本轮检查范围与所列资料。

## 供全书整合的建议

- 若共享术语表还没有收录“时间排序”“QSVT 中的奇异值变换”“Pauli 帧”，可增短定义并指向本章算例；此项不在本代理的编辑权限内。
- 第 6 章练习答案若提到 $4/\pi^2$，可引用新推导中的两条正弦不等式；第 17 章答案涉及 MBQC 前馈时，可补 $J(-\alpha)X=ZJ(\alpha)$。现有题目和答案无需改变编号。
- 阅读版应特别复核第 16 章新 Mermaid 分叉图，以及第 17 章角度公式在窄屏的显示。
