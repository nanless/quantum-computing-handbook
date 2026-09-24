# 第 37 轮：硬件、信息、纠错与系统工程独立研究和修订

日期：2026-09-23  
范围：`handbook/09-hardware.md`、`10-error-correction.md`、`13-quantum-information.md`、`14-compilation-control.md`、`19-engineering-architecture.md`。已通读这五章和 `AGENTS.md`、`handbook/STYLE.md`。没有修改同步的 `sources/`、共享附录、构建程序或其他章节。

## 本轮发现与处理

| 等级 | 发现 | 处理 |
|---|---|---|
| P1 | 第 09 章把中性原子阵列的 12.6 秒相干时间列为里程碑，却没有写明该数值是 XY16 动态解耦后的 $T_2$。读者可能把它当成未经控制的自然空闲时间；原论文同时给出阵列平均 $T_2^*=14.0(1)$ 毫秒。 | 在里程碑中补全约 12,000 站点、超过 6,100 原子、动态解耦 $T_2$ 与自由演化 $T_2^*$ 的实验条件，并保留“阵列不等于通用逻辑处理器”的边界。 |
| P2 | 第 10 章有综合征表，却没有展示辅助比特怎样只测奇偶而保留未知逻辑振幅，初学者容易把“测 $Z_1Z_2$”理解成分别测两个数据比特。 | 加入两次数据到辅助的 CNOT 线路、小态矢量计算和相干错误分支。明确指出实际校验线路故障仍需容错设计。 |
| P2 | 第 10 章的示意逻辑错误缩放与第 13 节的 $10^8$ 层预算彼此分离。 | 在同一组假设下反算 $p_L(d)=10^{-(d+3)/2}$，得奇数码距至少 17、裸旋转补丁约 577 个物理比特；明确它是教学下界，不是设备资源预测。 |
| P2 | 第 10 章原预算句说每层错误率应“远低于”$10^{-10}$，后续新算例却按并合上界的等号 $p_L\le10^{-10}$ 取 $d=17$。 | 改为同一层错误概率上界至多 $10^{-10}$，若预留其他错误预算则需更低；与 $d=17$ 示意推导对齐。 |
| P2 | 第 13 章直接给 Bell 态约化熵，读者需自行补偏迹步骤。 | 写出四项密度矩阵、偏迹规则、交叉项消失及 $\rho_A=I/2$。 |
| P2 | 第 14 章有 SWAP 增加六个 CNOT 的计数，却没有同一例子的时间与错误成本。 | 用七个 CNOT、20 ns 单比特门和 800 ns 并行读出算得 2220 ns，并把 $0.99^7\approx0.932$ 明确定义为独立故障模型中的“全程无故障”概率，而非 Bell 态保真度。 |
| P2 | 第 14 章旧反馈例把条件脉冲也合在等待时间中，随后对整个路径套空闲 $T_1$ 指数衰减。 | 把下发与脉冲拆成 150 ns 与 50 ns：完整路径 1.65 μs，脉冲开始前空闲 1.60 μs；仅对空闲段计算 $1-e^{-0.016}\approx1.59\%$。 |
| P2 | 第 19 章 TTS 重复次数公式没有列出独立、同设置、恒定单次命中概率假设，也未定义“命中”标准。 | 从 $(1-p_{\rm hit})^N$ 推导公式，要求预先固定目标值/后处理规则，并注明漂移与相关 shots 时需要重估。 |
| P2 | 第 19 章直接使用 `minor embedding`、`gauge` 和高斯资源，没有为初学者解释对象。 | 在原段落给 QUBO/Ising、次图嵌入、链强度、自旋反转变换和高斯态/操作/测量下短定义。 |
| P2 | 第 09 章的 Majorana 零模与“非阿贝尔”对初学者首次出现偏突然。 | 增加近零能量边界模式、多个模式共同编码、交换顺序不可互换的白话定义；仍区分信号与已证实的保护。 |

## 来源与核查边界

1. [Manetsch 等，*Nature* 2025](https://www.nature.com/articles/s41586-025-09641-4)：正文给超过 6,100 原子/约 12,000 站点；方法和图注明确 $T_2=12.6(1)$ 秒来自 XY16 动态解耦，阵列平均 $T_2^*=14.0(1)$ 毫秒，约 23 分钟为真空限制寿命。两种相干时间的实验序列不同。本轮修正依据正文，不按新闻标题外推。
2. [Google Quantum AI，*Nature* 2025，2026 年作者更正](https://www.nature.com/articles/s41586-024-08449-y)：正文明确距离 7 记忆实验 49 数据、48 测量、4 额外泄漏清除比特，$0.143\%\pm0.003\%$ 每周期和距离增 2 的抑制因子 $2.14\pm0.02$。核对后原里程碑数字和“记忆实验”口径保留。
3. [Paetznick 等，*Nature* 2026](https://www.nature.com/articles/s41586-026-10628-y)：论文摘要支持“11 至 800 倍，取决于所选物理线路基线，含错误检测与后选择”，原文限制语保留。
4. [Guidry 等，*Nature* 2025](https://www.nature.com/articles/s41586-025-08820-7)：论文明确光子指标条件于探测、不计损耗；原文限制语保留。
5. [IBM Quantum Learning，Repetition codes](https://quantum.cloud.ibm.com/learning/en/courses/foundations-of-quantum-error-correction/correcting-quantum-errors/repetition-codes)：教材用辅助比特 CNOT 奇偶测量说明三比特重复码；本轮新推导按同一线路约定。
6. [IBM Quantum Documentation，Represent quantum computers for the transpiler](https://quantum.cloud.ibm.com/docs/en/guides/represent-quantum-computers)：官方目标连接图说明 SWAP 路由和常见三 CNOT 分解；本轮数值例子另行清楚标注简化假设。
7. [Preskill，Ph/CS 219A Lecture 2](https://www.preskill.caltech.edu/ph219/Ph-CS-219A-Slides-2020/Ph-CS-219A-Lecture-2-Density-Operators.pdf)：偏迹的算符规则。新例子由规则直接计算，并没有把局部混合误认成全态混合。
8. [Kitaev，*Unpaired Majorana fermions in quantum wires*](https://arxiv.org/abs/cond-mat/0010440)：边界零模、有限尺寸劈裂与候选编码的原始模型；第 09 章仍遵循其后实验论文的争议边界。
9. [Albash 等，*npj Quantum Information* 2019](https://www.nature.com/articles/s41534-019-0210-7)：固定单次命中概率下的 TTS 定义。本轮补足重复试验公式适用前提。
10. [OpenQASM 3.1 OpenPulse 语法](https://openqasm.com/versions/3.1/language/openpulse.html)：官方文档明确仍在开发且可能变化；第 14 章目前“仍在发展”的说法成立。
11. [Bartlett 等，*Physical Review Letters* 2002](https://doi.org/10.1103/PhysRevLett.88.097904)：高斯初态、二次 Hamiltonian、正交分量测量和相应条件操作组成的连续变量过程可高效经典模拟；为第 19 章的高斯资源边界提供原始来源。
12. [D-Wave 官方嵌入文档](https://docs.dwavequantum.com/en/latest/quantum_research/embedding_guidance.html)与[控制设置文档](https://docs.dwavequantum.com/en/latest/quantum_research/solver_configuration.html)：定义次图嵌入、链强度和自旋反转；后者给出 $h_i\mapsto g_i h_i$、$J_{ij}\mapsto g_i g_jJ_{ij}$ 以及数学等价但硬件采样分布可变的理由。

## 独立计算检查

- $e^{-0.01}=0.9900498337$，故 1 μs / 100 μs 空闲弛豫概率 $0.9950166\%$。
- 七次独立 CNOT 均无所建模故障：$0.99^7=0.93206535$；时间 $20+7\times200+800=2220$ ns。
- 反馈例完整路径 $800+150+300+200+150+50=1650$ ns；脉冲前 1600 ns；$1-e^{-0.016}=0.01587268$。
- 码距 17：$p_L=10^{-10}$，$2\times17^2-1=577$。公式只沿用原章节的示意 $A=0.1,p/p_{\rm th}=0.1$，且额外假设一层一周期。
- 退火例 $\lceil\ln(0.01)/\ln(0.98)\rceil=228$，$1+228\times140\,\mu\mathrm s=1.03192$ 秒，原算例保留。

## 留给整合与下一轮审校

- 新增的正文均嵌入已有章节与原练习范围，未增加自检题，所以共享练习答案无需同步编号。若主审决定增加对应题，再同时扩充共享答案。
- 第 10 章的辅助比特校验步骤改为按时间顺序的四列表格，避免等宽字符线路在窄屏误对齐。请在最终阅读版查看表格容器是否局部横向滚动、数学片段是否仍在正确单元格。
- 已有 `assets/hardware-control-lanes.svg`、`cryo-control-stack.svg`、`evidence-ladder.svg` 等图本轮未重绘；其图意从文本看未发现与本轮修订冲突，明暗主题、窄屏实际视觉由阅读版审查统一确认。
- 当前报告只覆盖这五章和上述来源/算例，不宣称全书或该领域的所有知识已经穷尽。没有在这次研究中发现需要扩展到新硬件纪录清单的可靠教学理由。
