# 第 65 轮：硬件、纠错、安全与系统工程正确性深审

核查日期：2026-09-24。范围：`handbook/09-hardware.md`、`10-error-correction.md`、`11-resources-benchmarks.md`、`12-security-network-frontiers.md`、`14-compilation-control.md`、`15-practice-research.md`、`17-computation-models.md`、`19-engineering-architecture.md`。本报告只记录这些章节的独立复核；其他章节和共享练习答案由主代理或其他组处理。`sources/` 未改动。

## 逐篇结论

| 章 | 重点复核 | 结果 |
|---|---|---|
| 09 硬件 | 六平台编码、控制与读出；物理/逻辑比特；T1/T2*；101/105 比特、原子阵列、光子条件指标、离子后选择 | 所查定义与里程碑口径未见须改之处。101=49 数据+48 测量+4 额外泄漏清除；阵列 12.6 s 是 XY16 动态解耦 T2，14.0 ms 是自由 Ramsey T2*，不能混用。 |
| 10 纠错 | 三比特码、Shor 码和 Steane 综合征；Knill–Laflamme；距离与擦除；表面码计数和时空事件；阈值与 T 资源 | 逐行核算综合征与 `d=17`、`2d²−1=577`，无确认错误。原始论文支持 101 比特实测补丁不同于裸布局 97 比特。 |
| 11 基准 | RB 去极化换算、QV 重输出判据、条件保真度/接受率、能量和逻辑资源账 | `r=(d−1)(1−α)/d`；`d=2, α=.998 → r=.001`，`100×577=57,700`，`20 kW×30 s/.25=2.4 MJ≈.667 kWh` 均复算一致；未发现须改的数值。 |
| 12 安全与网络 | NIST FIPS 阶段、BB84、QKD 损耗、PLOB、两链路等待、纠缠交换、网络实验 | 修正一处“光纤本体衰减/整条实验链路损耗”混用风险，见下。HQC/Falcon 仍非最终 FIPS；IR 8547 仍为草案，均以 NIST 当日项目页复核。 |
| 14 编译控制 | SX 与 Rx 的全局相位、Rabi 失谐、路由计数、读出矩阵、反馈时延 | `7` 个 CNOT、`2220 ns`、`P1≈.990038`、`1.65 μs` 与原论文 9.6/6.5/3.1 μs 分解均复核一致；无须改。 |
| 15 实践 | 程序的门序、Wilson 区间、Bell 投影见证、三组 Hoeffding 并合界、Ramsey 与过程层析边界 | 态矢量、统计和见证的不等式经独立代数复核；确认 `f>1/2` 是充分纠缠见证而非必要条件；无须改。 |
| 17 计算模型 | MBQC 两结果的幅度/全局相位、绝热二能级谱隙、退火 TTS、echo、Grover 迭代 | `Δmin=√2`、`R=21`、Grover 12 次 `p≈.999947`，均独立复验；未见须改。 |
| 19 系统工程 | 判决矩阵、热预算、良率置信下限、退火总时间、GKP 基线、cat+重复码、标准成熟度 | 补明 CMOS 活动功耗条件和 cat 实验指标/渐近阈值边界；其余复算一致。 |

## 确认问题与正文改动

1. **第 12 章，100 km QKD 的损耗分母。** 原文把实验的 `0.235 dB/km` 称为“链路损耗”，可能让读者按 100 km 得到 `23.5 dB`，误以为这就是论文所报整链路损耗。原论文分别写：100 km 光纤本体 `0.235 dB/km`，系统**总损耗 31.5 dB**。现改为并列说明 `23.5 dB` 光纤段与 `31.5 dB` 整链路，防止把教学模型的透过率当成该实验实际点击率。原始来源：[Tang 等，2022](https://www.nature.com/articles/s41534-022-00630-3)，正文摘要和实验装置段；核查 2026-09-24。
2. **第 19 章，低温 CMOS 的活动功耗条件。** 原文虽说“特定工作点”，却未写 `20 nW MHz⁻¹` 是产生约 **100 mV 幅度脉冲**时每模拟单元的活动功耗，容易被误用为恒定每比特功率。已补条件、需乘实际更新频率、另有数十微瓦数字固定功耗。原始来源：[Spin-qubit control with a milli-kelvin CMOS chip，2025](https://www.nature.com/articles/s41586-025-09157-x)，Discussion；核查 2026-09-24。
3. **第 19 章，cat+重复码最低 `1.65%` 的指标。** 数值原来正确，但应明确是论文所定义的**整体逻辑存储每周期错误**，并非 CX 门错误。其重复码层无法纠正物理位翻转，因此作者明确说明**没有完整的渐近阈值**；现补进正文，避免“距离 5 低于阈值”被误读为完整容错阈值。原始来源：[Putterman 等，2025](https://www.nature.com/articles/s41586-025-08642-7)，Fig. 5 附近正文；核查 2026-09-24。

这些改动未改任何自检题号或答案。共享 `handbook/appendices/exercises.md` 无需按本组修改。

## 独立复算清单

- 硬件：`0.99^100=.366032`，`0.999^100=.904792`；`exp(−1/100)=.9900498`。
- BB84：理想截获再发送 `Q=(1/2)(1/2)=1/4`；1000 发送的期望同基约 500，错误约 125；无错抽检 20 位 `(.75)^20=.003171`。这些仅属文中独立理想模型。
- 两并行概率链路：`E[max(X,Y)]=20−1/.19=14.73684` 时隙，`E|X−Y|=20−2/.19=9.47368` 时隙；`p=.1, τ=1 ms, Tmem=20 ms` 时平均相干因子 `.678904`，而对平均等待直接取指数 `.622704`，不可交换次序。
- 控制：`P1=[1/1.01]sin²(π√1.01/2)=.99003824`；这只是失谐态转移概率，正文未把它叫平均门保真度。
- 退火：`ceil(ln .01/ln .8)=21`；另一例 `ceil(ln .01/ln .98)=228`，`1 s+228×140 μs=1.03192 s`。
- 良率：四次全成功的双侧 95% Clopper–Pearson 下限 `(.025)^(1/4)=.397635`；要使下限至少 `.99`，`n≥ln .025/ln .99=367.0404`，故最小整数 368。
- Grover：8 位唯一目标、`θ=asin(1/16)` 时 `p12=.9999470`、`p13=.9861862`。

## 原始与官方证据入口（均于 2026-09-24 核查）

- [Google 表面码原论文](https://www.nature.com/articles/s41586-024-08449-y)：49+48+4、每周期 0.143%±0.003%、增长 2 码距的抑制因子 2.14±0.02，且不同解码器有不同数字。
- [6100 中性原子阵列原论文](https://www.nature.com/articles/s41586-025-09641-4)：11,998 站点、约 23 分钟真空寿命、XY16 下 12.6 s 与自由 Ramsey 14.0 ms。
- [离子编码实验原论文](https://www.nature.com/articles/s41586-026-10628-y)：11–800 倍是相对所选物理线路基线、结合错误检测与后选择。
- [光子平台原论文](https://www.nature.com/articles/s41586-025-08820-7)：所报高保真指标条件于光子探测，未计损耗。
- [NIST PQC 标准化页](https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post_Quantum_Cryptography-Standardization)、[已选算法页](https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization/selected-algorithms)、[出版物列表](https://csrc.nist.gov/Projects/post-quantum-cryptography/publications)：FIPS 203/204/205 final，HQC/Falcon `FIPS coming soon`，IR 8547 draft，SP 800-227 final；状态具有时间敏感性。
- [实时译码原论文](https://www.nature.com/articles/s41467-026-73331-6)：8 比特稳定性实验，9 轮后响应 9.6 μs，含译码 6.5 μs、通信/控制 3.1 μs。
- [QV 原始协议](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.100.032328)、[Eastin–Knill 原始论文的 NIST 页面](https://www.nist.gov/publications/restrictions-transversal-encoded-quantum-gate-sets)、[量子退火公平基准原论文](https://arxiv.org/abs/1401.2910)：用于核对三类理论/基准表述。
- [GKP qudit 存储原论文](https://www.nature.com/articles/s41586-025-08899-y)、[cat+重复码原论文](https://www.nature.com/articles/s41586-025-08642-7)、[mK CMOS 原论文](https://www.nature.com/articles/s41586-025-09157-x)、[4 K 硅控制器原论文](https://www.nature.com/articles/s41586-026-10754-7)、[ISO 词汇标准](https://www.iso.org/standard/80432.html)：用于核对平台和工程口径。

## 复核边界

八篇合计约 3300 行；本轮逐篇通读、针对公式/数值独立复算、对时效和高风险实验声明取原论文或官方机构资料交叉查证。它不是所有引用的全文逐句同行评审，也没有把任何设备性能外推到未来日期。统计示例依赖各自写明的独立、稳定与测量模型；真实设备若存在相关噪声、漂移、泄漏、后选择或不可见损耗，不应机械代入玩具式。截止 2026-09-24，本组未发现其他可证实且须立即改动的错误。
