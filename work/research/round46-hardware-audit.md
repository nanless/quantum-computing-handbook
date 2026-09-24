# 第 46 轮：硬件、纠错、资源与安全章节审校

审校范围：第 09、10、11、12、14、19 章及这些章节引用的现有科学图。2026-09-23 逐节检查概念、算例、工程口径与图文对应，并以原始论文、官方标准或研究机构教材复核易错事实。本轮不是声称穷尽整个领域，只记录可定位、可修复的问题。

| 级别 | 位置 | 发现与证据 | 修法 |
|---|---|---|---|
| P2 | 第 10 章 §3 | 给出九比特 Shor 码编码态和 `[[9,1,3]]` 结论，却没有真的算一次位翻转、相位翻转的不同综合征。初学者难以从“三组 GHZ”过渡到稳定子测量。IBM 官方 [Stabilizer codes](https://quantum.cloud.ibm.com/learning/en/courses/foundations-of-quantum-error-correction/stabilizer-formalism/stabilizer-codes) 列出六个组内 $ZZ$ 与两个跨组 $XXXXXX$ 检查。 | 增加 $X_2$、$Z_1$、$Y_2$ 三种单点错误的反对易表，写清跨组检查如何定位相位所在组、为何组内任一 $Z$ 可作同效修正。 |
| P2 | 第 11 章 §3 | RB 给出衰减模型 $A\alpha^m+B$ 后，只说换算为“每门错误”依赖假设，没有一个可复算的一量子比特数值例子，容易把 $1-\alpha$ 直接当平均门不保真度。原始 [Magesan 等 2011](https://doi.org/10.1103/PhysRevLett.106.180504) 将 RB 衰减与所用维数下的平均错误联系起来。 | 在门依赖小、噪声稳定且有效去极化的限定下推导 $r=(d-1)(1-\alpha)/d$，给 $d=2,\alpha=0.998$ 的数值，并强调对象是每个 Clifford 而非每个原生脉冲。 |
| P2 | 第 12 章 §4 | “光纤衰减使直接链路成功概率随距离指数下降”完全正确，但没有给 dB 到透过率的计算。没有这一步，读者难以理解为何 100 km 很难以及“距离纪录”不等于秘密密钥率。原始 [量子密钥分发实验](https://www.nature.com/articles/s41534-022-00630-3) 给出 100 km 链路实测 0.235 dB/km；另一个 [芯片 QKD 实验](https://www.nature.com/articles/ncomms13984) 用 0.2 dB/km 作电信波段示意。 | 用明确标为示意的 $0.2\,\mathrm{dB/km}$ 推出 $\eta(L)=10^{-0.2L/10}$，算 50/100 km，并注明探测、耦合、暗计数和有限密钥成本未算；不把它当现实密钥率。 |
| P2 | 第 14 章 §6 | 已推导共振脉冲面积和失谐后旋转轴倾斜，但 1 MHz 对 10 MHz 的算例只报轴比 0.1，没有算读出概率或量化这一系统误差。两能级受驱 Hamiltonian 足以直接对角化，给出初态 $|0\rangle$ 到 $|1\rangle$ 的概率。 | 推出 $P_1(T)=\Omega_x^2/(\Omega_x^2+\Delta^2)\sin^2(\sqrt{\Omega_x^2+\Delta^2}T/2)$；代入原算例的 50 ns，区分理想模型的失谐误差与真实门错误。 |

复核没有发现可立刻认定的 P0/P1 事实错误。已核对：NIST 官方 [Selected Algorithms](https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization/selected-algorithms) 在本轮仍把 HQC 标成尚未发布的 FIPS；[Paetznick 等 2026](https://www.nature.com/articles/s41586-026-10628-y) 摘要支持 11—800 倍、12/16 物理比特以及检测与后选择的限定；[实时译码原文](https://www.nature.com/articles/s41467-026-73331-6) 支持 8 比特、9 轮、6.5+3.1=9.6 μs；[GKP 多能级原文](https://www.nature.com/articles/s41586-025-08899-y) 支持 1.82/1.87 寿命增益及 Fock 比较基线。第 19 章控制链图与第 10 章表面码图的标签、箭头和相邻正文一致，暂不需要编辑 SVG。
