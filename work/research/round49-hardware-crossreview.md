# 第 49 轮：纠错、基准、QKD 与控制算例只读交叉审

日期：2026-09-23。只读检查硬件组第 47 轮新增的第 10、11、12、14 章四处算例；未修改对方正文、SVG、共享附录、阅读版或 sources/。本结论不延伸到这些章的其他段落。

| 章节 | 独立核查 | 结论 |
|---|---|---|
| 第 10 章 Shor 九比特码 | 六个组内 $ZZ$ 与两项跨组 $X_1\cdots X_6$、$X_4\cdots X_9$ 与 [IBM Quantum 原始课程](https://quantum.cloud.ibm.com/learning/en/courses/foundations-of-quantum-error-correction/stabilizer-formalism/stabilizer-codes)相符。$X_2$ 与前两项 $ZZ$ 反对易，$Z_1$ 与第一项跨组 $X$ 反对易，$Y_2$ 同时表现两者；表中四行符号正确。$Z_1,Z_2,Z_3$ 在码空间上由 $ZZ$ 稳定子联系，退化性解释正确。 | 无 P0–P2 |
| 第 11 章 RB 换算 | [Magesan、Gambetta、Emerson 原论文](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.106.180504/fulltext)把衰减参数与 twirled 去极化通道的平均不保真度相连。教材所设 $\mathcal D_\alpha(\rho)=\alpha\rho+(1-\alpha)I/d$ 给 $F_{\rm avg}=\alpha+(1-\alpha)/d$；$d=2,\alpha=0.998$ 时 $r=0.001$，不是 $0.002$。只称“每被抽样 Clifford”、不称每原生脉冲错误率，口径正确。 | 无 P0–P2 |
| 第 12 章 dB 与 QKD | $0.2\,\mathrm{dB/km}\times100\,\mathrm{km}=20$ dB，对应 $\eta=10^{-2}$；$50$ km 对应 $10^{-1}$。一百万枚理想单光子平均一万枚送达，等概率双基筛选再留约五千，算术正确；正文明确这不是最终安全密钥位数。[Tang 等原论文](https://www.nature.com/articles/s41534-022-00630-3)的 Methods 确写 100 km 光纤为 $0.235$ dB/km，同时摘要写的是**含其他器件损耗的总链路** $31.5$ dB；正文只引用前者作光纤对比，没有把两种口径混同。 | 无 P0–P2 |
| 第 14 章失谐 Rabi | $H_{\rm rot}=\hbar(\Delta Z+\Omega_xX)/2$ 的平方是 $\hbar^2(\Delta^2+\Omega_x^2)I/4$，故从 $|0\rangle$ 到 $|1\rangle$ 的振幅为 $-i(\Omega_x/\Omega_{\rm eff})\sin(\Omega_{\rm eff}T/2)$。在 $\Delta/\Omega_x=0.1,T=\pi/\Omega_x=50$ ns 时，概率 $[1/1.01]\sin^2(\pi\sqrt{1.01}/2)=0.99003824\ldots$，与正文 $0.99004$ 一致；$1-P_1=0.9961759\ldots\%$，正文约 $0.996\%$ 也正确。已限定为初态转移概率而非平均门不保真度。 | 无 P0–P2 |

四个例子都提供了模型、算式和不能外推的边界；本轮未发现必须回改的数学或初学者层次问题。真实阅读版的表格与公式外观仍由主审的最终构建和截屏验收。
