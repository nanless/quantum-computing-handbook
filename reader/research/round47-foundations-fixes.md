# 第 47 轮：基础篇缺口修订与核验

依据 [第 46 轮审校](round46-foundations-audit.md)，仅改动基础组独占的四个 Markdown 文件；`sources/`、共享练习附录、构建产物和审校总日志均未编辑。

| 文件 | 修订 | 手算或边界核验 |
|---|---|---|
| `handbook/quantum-mechanics/01-experiments-states.md` | 从记录态重叠推出相位扫描式、极值和可见度 $\mathcal V=|\gamma|$，明示平衡、无损条件。 | $\gamma=0.6$ 时 $P_{0,\min}=0.2$、$P_{0,\max}=0.8$，可见度 $0.6$；$\gamma=0,1$ 两端极限与原文一致。 |
| `handbook/03-multiple-qubits.md` | 把单配性从一句断言扩为 Bell 纯约化态的支持空间论证，并与 GHZ 三方态的 $AB$ 经典关联对照；明确一般定量关系需选纠缠量，避免把安全直觉当安全证明。 | $\operatorname{Tr}_C(|\mathrm{GHZ}\rangle\langle\mathrm{GHZ}|)=\tfrac12(|00\rangle\langle00|+|11\rangle\langle11|)$，不是 Bell 纯态。 |
| `handbook/04-circuits-protocols.md` | 补不可删除的输入/输出内积计算 $c^2=c\langle A_\phi|A_\psi\rangle$，用 $|0\rangle,|+\rangle$ 检查非正交情形。 | $c=1/\sqrt2$，两个复制输入内积 $c^2=1/2$；若输出辅助态固定，内积会错误地变成 $c$。SWAP 可把信息转移到辅助系统，无矛盾。 |
| `handbook/05-noise-channels.md` | 从振幅阻尼 Kraus 算子与随机 $Z$ 退相位推导 $1/T_2=1/(2T_1)+1/T_\phi$，另加 $T_1=T_\phi=60\,\mu s$ 的数值例。 | $T_2=40\,\mu s$；$|+\rangle$ 等待 $40\,\mu s$ 后 $\rho_{11}\approx0.257$、$\rho_{01}\approx0.184$。限定为零温、指数弛豫与 Markov 模型。 |

资料： [Englert 1996 原始论文](https://doi.org/10.1103/PhysRevLett.77.2154)、[Coffman–Kundu–Wootters 2000 原始论文](https://doi.org/10.1103/PhysRevA.61.052306)、[Pati–Braunstein 2000 原始论文](https://doi.org/10.1038/35004532)、[Preskill 量子信道课程讲义](https://www.preskill.caltech.edu/ph219/Ph-CS-219A-Slides-2020/Ph-CS-219A-Lecture-5-Qubit-Channels.pdf) 与 [IBM Quantum Learning 的 Kraus 讲义](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/representations-of-channels)。

验证：`node tools/reader/check-qm-examples.mjs` 通过；`node tools/reader/check-qm-review.mjs` 通过，181 题与 181 答仍匹配；新增数值用独立 Node 计算复核。尚未由本组重建或检查 HTML，交由主审汇总构建。全局完整性不是本次有限审校可证明的命题；本组未发现新的 P0/P1 事实错误。
