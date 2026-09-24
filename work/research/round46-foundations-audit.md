# 第 46 轮：基础、量子力学与噪声篇审校

范围：`handbook/quantum-mechanics/README.md` 与 Q1–Q4、`appendices/prerequisites.md`、主篇 01–05。先通读各章结构、关键推导、已给算例与题答衔接，再以原始论文和大学/研究机构公开讲义核对以下问题。这里的 P2 指本轮应修的教学或论证缺口，并不表示原文结论必定错误。

| 级别 | 位置 | 具体发现与修法 | 核查依据 |
|---|---|---|---|
| P2 | Q1 §2.2，部分路径记录 | 已从记录态重叠 $\gamma$ 推到 $P_0=[1+\operatorname{Re}(\gamma e^{-i\phi})]/2$，但读者尚看不出“干涉减弱多少”与可观测明暗度的直接关系。补 $\gamma=|\gamma|e^{i\delta}$、最大/最小概率和在等权无损模型下的可见度 $\mathcal V=|\gamma|$，同时写清它不能无条件移植到不平衡或有损装置。 | [Englert, *PRL* 77, 2154 (1996)](https://doi.org/10.1103/PhysRevLett.77.2154) 是路径信息与干涉可见度的原始工作；本章等权纯记录模型的数值式可由现有矩阵直接推出。 |
| P2 | 主篇 03 §8，单配性 | 仅有一句“AB 最大纠缠纯态则与 C 无关联”和安全直觉，缺少为何必然如此的解释，也可能让初学者误会“任何纠缠都不能与第三方共享”。补纯 AB 的 Schmidt 秩为 1 所导致的 $\rho_{ABC}=\rho_{AB}\otimes\rho_C$，并用 GHZ 态说明三方相关与 AB 最大纠缠不是一回事；一般定量单配关系需说明依赖纠缠量。 | [Coffman–Kundu–Wootters, *PRA* 61, 052306 (2000)](https://doi.org/10.1103/PhysRevA.61.052306) 给出三比特定量取舍；本轮只给初学者能核查的特殊情形。 |
| P2 | 主篇 04 §5，不可删除 | 现有公式带 $|A_\psi\rangle$，但直接说“信息必然转移”而没有展示内积怎样约束辅助态。补对两种非正交输入的内积等式 $|c|^2=c\langle A_\phi|A_\psi\rangle$，解释若辅助态固定就矛盾，SWAP 则把态转移到辅助系统。 | [Pati–Braunstein, *Nature* 404, 164–165 (2000)](https://doi.org/10.1038/35004532) 为原始不可删除定理。 |
| P2 | 主篇 05 §5.3 与 §6，$T_1/T_2$ 衔接 | 振幅阻尼的 $\gamma$ 和后一节的 $T_1,T_2,T_\phi$ 各自正确，却没有推导为何 $1/T_2=1/(2T_1)+1/T_\phi$。补任意 $2\times2$ 输入经阻尼和纯退相位的矩阵元素计算、时间参数化与一组可手算数值；明确零温、Markov、指数衰减条件。 | [Preskill, Ph/CS 219A Lecture 5, Qubit Channels](https://www.preskill.caltech.edu/ph219/Ph-CS-219A-Slides-2020/Ph-CS-219A-Lecture-5-Qubit-Channels.pdf) 直接列出阻尼信道与 $T_2=2T_1$ 极限；[IBM Quantum Learning, Kraus representations](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/representations-of-channels) 核对信道表示。 |

其余已核对的高风险点：Q3 旋转坐标系与 RWA 的相位/二倍因子；Q4 谐振子交叉项、势垒边界匹配与厚势垒系数；主篇 02 的 $Y$ 符号、Bloch 坐标和 POVM/测量工具之别；主篇 03 的 CHSH 四相关量与上界；主篇 04 的传态四分支及 $XZ/ZX$ 全局相位；主篇 05 的退极化两种参数约定。未发现须立即阻断发布的 P0/P1 数学错误。

本轮仅修上述明确缺口，不把不同硬件平台的经验结论塞进基础篇，也不声称对所有未来知识或实验报告完成穷尽审查。
