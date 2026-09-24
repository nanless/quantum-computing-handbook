# 第 8 轮交叉审稿：硬件、系统、网络与附录

审稿日期：2026-09-22  
审稿范围：`handbook/09-hardware.md`、`11-resources-benchmarks.md`、`12-security-network-frontiers.md`、`14-compilation-control.md`、根目录与 handbook 的 README、`STYLE.md`、`handbook/appendices/` 全部文件、`handbook/assets/` 全部 SVG。  
约束：本轮只审不改正文；本文件是唯一新增文件。

## 1. 结论与分级

| 等级 | 数量 | 结论 |
|---|---:|---|
| P0 | **0** | 未发现会使核心理论、实验结论或计算结果整体错误的问题。 |
| P1 | **6** | 1 项时效状态需要补齐，2 项一手来源署名错误，1 项争议来源类型表述不准，1 项网络术语未定义，1 项答案与正文公式不一致。 |
| P2 | **5** | 数学排版、能耗模型适用条件、术语首次解释、孤立 SVG、集中参考资料的覆盖范围可改进。 |

总体判断：四章的主要物理边界、系统指标和实验限定词可靠；所有新增可复算例均算对；目录、本地链接、自检题与答案数量一致。当前不宜宣称“零问题”，但没有 P0。

## 2. P1：应在下一轮修复

### P1-1｜HQC 状态只复述 2025 年计划，未明确 2026-09-22 的实际状态

- 位置：`handbook/12-security-network-frontiers.md:21-31`，尤其第 29 行。
- 现状：标题写“截至 2026-09-22”，正文却只说 2025-03-11 公告中“约 2026 年形成标准草案、2027 年定稿”的计划。
- 核验：NIST 当前项目页仍把 HQC 列为正在标准化的额外 KEM；Selected Algorithms 页面仍写作“FIPS coming soon”，没有把 HQC 列为已经发布的最终 FIPS。2024 年正式发布的仍是 FIPS 203、204、205。
- 精确修改：在第 29 行后补一句：**“截至 2026-09-22，NIST 当前项目页仍将 HQC 列为正在标准化的额外 KEM，Selected Algorithms 页面标注为 ‘FIPS coming soon’；本书不把 2025 年公布的计划日期写成已经完成的草案或最终标准。”** 同时给当前页面加访问日期。
- 一手来源：[NIST PQC Standardization](https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post_Quantum_Cryptography-Standardization)、[NIST Selected Algorithms](https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization/selected-algorithms)、[2025-03-11 HQC 选择公告](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption)。

### P1-2｜Majorana 争议来源不应写成笼统的“期刊随文编辑说明”

- 位置：`handbook/09-hardware.md` 的拓扑路线参考资料，现用语为“并见期刊随文编辑说明”。
- 问题：截至本轮日期，Nature 已发表正式的 **Matters Arising** 和作者回复。这是同行评议的科学争论，不只是编辑提示。笼统写法会模糊证据类型，也不便读者追溯具体质疑与回应。
- 精确修改：保留正文现有的谨慎结论，但把来源改成：
  1. 原论文：[M. Aghaee et al., *Nature* 638, 651–655 (2025)](https://www.nature.com/articles/s41586-024-08445-2)；
  2. [H. F. Legg, Matters Arising, *Nature* 654, E22–E26 (2026)](https://www.nature.com/articles/s41586-026-10567-8)；
  3. 作者回复 DOI：[10.1038/s41586-026-10568-7](https://doi.org/10.1038/s41586-026-10568-7)。
- 证据边界：原论文自己也明确说，奇偶读出不能无歧义地区分拓扑 Majorana 零模与精细调节的平庸 Andreev 态；因此不能把论文改写成“拓扑量子比特已证实”。

### P1-3｜40/35 km 硅空位网络论文的第一作者写错

- 位置：`handbook/12-security-network-frontiers.md:210`。
- 现状：写成 “M. K. Bhaskar et al.”；Bhaskar 是合作者，不是第一作者。
- 精确修改：改为 **“C. M. Knaut et al., *Nature* 629, 573–578 (2024)”**，标题和链接保持不变。
- 一手来源：[Nature 论文页](https://www.nature.com/articles/s41586-024-07252-z)。论文支持正文的限定：40 km 盘纤、35 km 波士顿地区部署光纤回路、1350 nm 转换、两个含多量子比特寄存器的 SiV 节点；正文没有把它夸大成多跳容错互联网。

### P1-4｜RFC 9583 的第一作者写错

- 位置：`handbook/12-security-network-frontiers.md:214`。
- 现状：写成 “A. Dahlberg et al.”。
- 精确修改：改为 **“C. Wang, A. Rahman, R. Li, M. Aelmans and K. Chakraborty, RFC 9583 (2024)”**。继续保留“信息性文档，不是互联网标准”的限定。
- 一手来源：[RFC Editor：RFC 9583](https://www.rfc-editor.org/rfc/rfc9583.html)。

### P1-5｜`herald` 对初学者未作首次定义

- 位置：`handbook/12-security-network-frontiers.md:84` 首次出现，随后见第 94、114、136、186、190 行；答案又见 `appendices/exercises.md:258`。
- 问题：这是理解概率性纠缠链路的关键术语，却一直只写英文；与本书“首次出现给中文解释”的风格不一致。读者还可能误解为读取了未知量子态。
- 精确修改：首次改为 **“先兆成功信号（herald：某个探测事件宣布本次纠缠生成成功，但不读取纠缠所承载的未知量子信息）”**；后文统一用“先兆信号”或“先兆条件”。同步在术语表加入一项。
- 依据：[RFC 9340](https://www.rfc-editor.org/rfc/rfc9340.html) 将 Bell 对视为网络服务资源，并强调经典控制消息、质量与交付条件；正文的分层思想与之相容。

### P1-6｜动态电路第 6 题答案与正文六项延迟公式不一致

- 位置：正文 `handbook/14-compilation-control.md:227-234`；答案 `handbook/appendices/exercises.md:294`。
- 正文公式：
  `t_fb = t_meas + t_classify + t_transport + t_classical + t_dispatch + t_pulse`，对应测量积分、状态判别、控制系统内传输、条件计算、指令下发、条件脉冲。
- 现答案：列出“模拟信号传输、滤波/积分与分类”等，但漏掉最终条件脉冲，把“等待期间退相干”放进六项之一。退相干是等待造成的错误后果，不是该式中的延迟分量。
- 精确修改：答案严格按公式列六项；另起一句说明“反馈总延迟会在等待期间引入退相干和其他时间相关误差，但退相干不是第七个时延项”。

## 3. P2：不影响核心正确性，但应改善

### P2-1｜两个答案中的 LaTeX 单位没有进入数学模式

- 位置：`handbook/appendices/exercises.md:249,266`。
- 现状：使用 `(20\,\mathrm{kW})`、`(30\,\mathrm{s})`、`(1\,\mathrm{ms})` 等普通括号，常见 Markdown 渲染器会直接显示反斜杠。
- 精确修改：改成 `$20\,\mathrm{kW}$`、`$30\,\mathrm{s}$`、`$0.25$`、`$2.4\,\mathrm{MJ}$、`$1\,\mathrm{ms}$`、`$14.74\,\mathrm{ms}$`；或全段统一用 `\(...\)`。

### P2-2｜每成功答案能耗公式应再写明平稳、等成本重试假设

- 位置：`handbook/11-resources-benchmarks.md:155-171`。
- 现状：公式与示例均正确，正文也说它只是审计框架；但一般式把一次尝试的功率和时长除以单次成功率，隐含了重试近似独立、每次尝试平均成本相同、成功判据固定等条件。
- 精确修改：在第 163 行后补一句：**“该简式适用于成功概率和平均尝试成本近似稳定的重试模型；若不同尝试成本不同、失败相关或存在批处理，应直接报告总实测能量除以最终接受答案数，并给出分布而不只给均值。”**

### P2-3｜编译/实时系统中的几个英文术语首次解释仍不够统一

- 位置：`handbook/14-compilation-control.md:254-267` 的 `detector events`、`Pauli frame`、`backlog`；`handbook/11-resources-benchmarks.md:189` 的 `manifest`。
- 精确修改：首次分别写成“探测事件（detector events）”“Pauli 帧（经典跟踪待施加 Pauli 修正的记录）”“未处理数据积压（backlog）”“可复现实验清单（manifest）”。Pauli 帧也可交叉链接 `10-error-correction.md` 已有定义。术语表至少补“Pauli 帧”和“先兆信号”；其余可只做行内定义。

### P2-4｜两张制作良好的 SVG 是孤立资产，证据阶梯还与正文分类数不一致

- 位置：`handbook/assets/evidence-ladder.svg`、`handbook/assets/qec-syndrome.svg`。
- 核验：三张 SVG 均通过 XML 解析和人工渲染检查，标签清楚、对比度良好、无裁切；`bloch-sphere.svg` 已在第 02 章引用，但另外两张未被任何 Markdown 引用。
- 精确修改：
  - 把 `qec-syndrome.svg` 放到第 10 章三比特重复码/综合征第一次完整解释之后，并补图注和正文引用；
  - `evidence-ladder.svg` 当前有五级，而第 08 章正文使用四层证据结构。先统一层级名称与数量，再嵌入第 08 章；若不准备维护，删除或明确标记为未使用草图。
- 美观性结论：图本身 **0 个 P0/P1**；问题仅是内容集成和分类一致性。

### P2-5｜集中参考资料页并非完整索引，却未声明“选择性”

- 位置：`handbook/appendices/references.md:47-76`。
- 现状：章节本地参考资料已含多数新来源，但集中页的“硬件与基准”“密码与网络”“编译、控制与实验”没有收入本轮文本实际依赖的重要一手资料，例如 Knaut/Kucera 网络实验、RFC 9340/9583、2026 实时译码实验和当前 NIST 状态页。读者可能把该页误认为全书完整书目。
- 精确修改：二选一：
  1. 标题下声明“本页为精选入口，各章末尾书目才是完整来源”；或
  2. 补入上述来源及日期/版本，形成真正的集中索引。

## 4. 时效事实逐项核验

下表中的“0”表示本轮未发现正文事实或限定词问题；上节已单列的问题除外。

| 主题 | 核验结论 | 一手来源 |
|---|---|---|
| Google Willow 表面码存储 | **0**。论文为 101 物理量子比特、距离 7、每循环逻辑错误约 0.143%±0.003%、抑制因子 $\Lambda=2.14\pm0.02$；正文正确限定为逻辑存储进展，不是通用 FTQC。2026-04-28 有勘误，应在维护时连同原文查看。 | [Nature 原论文](https://www.nature.com/articles/s41586-024-08449-y)、[2026 correction](https://www.nature.com/articles/s41586-026-10559-8) |
| 中性原子阵列 | **0**。2025-09-24 在线发表；11,998 个光镊位点、超过 6,100 个原子；正文没有把原子数写成通用逻辑量子比特数。 | [Nature 论文](https://www.nature.com/articles/s41586-025-09641-4) |
| 光子容错实验 | **0**。原文明确其指标条件于光子探测，且不把光子丢失计入；正文准确保留了“条件保真度/未计损失”限定。 | [Nature 论文](https://www.nature.com/articles/s41586-025-08820-7) |
| 离子阱 QCCD 逻辑改善 | **0**。2026-06-10 论文报告 12 物理比特/2 逻辑比特与 16 物理比特/4 逻辑比特实例，并在其基线、检测和后选择条件下报告 11–800 倍改善；正文没有把倍率外推为任意算法。 | [Nature 论文](https://www.nature.com/articles/s41586-026-10628-y) |
| Majorana / 拓扑路线 | 核心结论 **0**：正文保持未定论，并区分“poor man's Majoranas”与受拓扑保护量子比特。来源类型需按 P1-2 修正。 | [原论文](https://www.nature.com/articles/s41586-024-08445-2)、[Matters Arising](https://www.nature.com/articles/s41586-026-10567-8)、[minimal Kitaev chain](https://www.nature.com/articles/s41586-025-09927-7) |
| 实时译码 | **0**。2026-06-01 论文确为 8 比特稳定性实验、最多 25 轮；9 轮后的完整响应 9.6 μs，其中译码 6.5 μs、通信与控制 3.1 μs。正文明确说不能外推到任意码距。 | [Nature Communications](https://www.nature.com/articles/s41467-026-73331-6) |
| 网络分层与 Bell 对服务 | **0**。正文说明 RFC 是信息性研究文档、Bell 对不是经典数据包、经典控制面不可省略，均符合原文边界。署名问题见 P1-4。 | [RFC 9340](https://www.rfc-editor.org/rfc/rfc9340.html)、[RFC 9583](https://www.rfc-editor.org/rfc/rfc9583.html) |
| 14.4 km 城市暗纤实验 | **0**。光子—光子、离子—光子纠缠和离子到远端电信光子的状态传送限定正确。 | [npj Quantum Information](https://www.nature.com/articles/s41534-024-00886-x) |
| OpenPulse | **0**。端口、帧、波形及持续演进的规范边界表述正确。 | [OpenQASM 3.1 OpenPulse](https://openqasm.com/versions/3.1/language/openpulse.html) |
| ISO/IEC 4879:2024 | **0**。它是量子技术术语与定义标准，正文没有把它说成性能认证标准。 | [ISO 官方页面](https://committee.iso.org/cms/live/live/en/sites/isoorg/contents/data/standard/08/04/80432.html) |
| GRAPE 参考文献 | **0**。作者、标题、卷页与 DOI 已正确：N. Khaneja et al., *JMR* 172, 296–305 (2005)。 | [DOI](https://doi.org/10.1016/j.jmr.2004.11.004) |

## 5. 新例题复算

| 例题 | 复算 | 结论 |
|---|---|---|
| Rabi 脉冲 | $\Omega/2\pi=10\,\mathrm{MHz}$，故 $t_\pi=\pi/\Omega=50\,\mathrm{ns}$，$t_{\pi/2}=25\,\mathrm{ns}$；$\Delta/\Omega=0.1$。 | **正确，P0/P1/P2=0** |
| 动态反馈 | $800+150+300+200+150\,\mathrm{ns}=1.6\,\mu\mathrm{s}$；若 $T_1=100\,\mu\mathrm{s}$，等待弛豫概率 $1-e^{-1.6/100}=1.587\%\approx1.59\%$。 | **正确，P0/P1/P2=0** |
| 能耗 | $20\,\mathrm{kW}\times30\,\mathrm{s}/0.25=2400\,\mathrm{kJ}=2.4\,\mathrm{MJ}=0.6667\,\mathrm{kWh}$。 | **数值正确**；一般式适用条件见 P2-2，答案排版见 P2-1。 |
| 两链路几何等待 | 对支撑集 $\{1,2,\ldots\}$ 的独立几何变量，$E[\max(X,Y)]=2/p-1/[1-(1-p)^2]$；$p=0.1$ 得 $14.7368$ 轮，即 $14.74\,\mathrm{ms}$。顺序等待为 $20\,\mathrm{ms}$。 | **正确**；答案排版见 P2-1。 |
| 路由与关键路径 | 两次 SWAP、每次 3 CNOT，额外 6 CNOT；示例关键路径 $20+200+800=1020\,\mathrm{ns}$。 | **正确，P0/P1/P2=0** |

## 6. 结构、链接、术语和图表验收

- **目录与本地链接：0 个问题。** 根 README 到 handbook 的入口有效；handbook README 的 00–16 章节链接、5 个附录链接均有目标。09/11 对 14 章 `#13-可复现实验记录模板`、11 对 `#10-动态电路` 的锚点与实际标题一致。
- **自检与答案数量：** 逐章题数与附录答案条目完全一致，共 **114** 题；仅 P1-6 是内容不一致，不是缺题/错号。
- **符号与约定：0 个 P0/P1。** 能量、时延、几何分布、保真度与 Pauli 帧的用法没有发现互相矛盾；根保真度约定在术语表和相关答案中一致。
- **STYLE 本身：0 个问题。** 发现的是正文少量偏离首次定义/数学排版规则，已列为 P1-5、P2-1、P2-3。
- **SVG 技术质量：0 个 P0/P1。** 三图 XML 均可解析，渲染后没有裁切、重叠或低对比文字；集成问题见 P2-4。
- **README：0 个问题。** 版本日期、适用读者、阅读路线和章节表一致；根 README 简洁且没有失效入口。
- **其他附录：0 个 P0/P1。** `notation.md`、`glossary.md`、`audit-log.md` 未发现错误条目；术语扩充建议见 P1-5/P2-3，参考资料范围问题见 P2-5。

## 7. 易过时内容与维护动作

这些项目即使本轮核验通过，也不应被当成永久事实：

1. **NIST PQC/HQC 阶段**：每次发布前查 NIST 项目页、FIPS 页面与勘误；区分选择、草案、最终 FIPS。
2. **2024–2026 硬件纪录**：复核论文在线日期与期刊卷期；保留物理/逻辑规模、是否后选择、是否条件于探测、误差定义和实验任务。
3. **Majorana 路线**：成对追踪原论文、Matters Arising、Reply 与后续独立复现；不要只引用厂商新闻稿。
4. **实时译码**：规模、码距、轮数、吞吐、平均/高分位响应和接口时延必须同时报告，小规模集成结果不能外推。
5. **量子网络**：距离必须标盘纤/部署光纤、节点数、存储器、生成率、保真度定义、成功先兆条件、长时间可用率和多跳能力。
6. **OpenQASM/OpenPulse 与云接口**：记录规范版本、后端/ISA/校准快照和访问日期；不要把某一平台当前接口写成永久通用标准。

## 8. 验收判定

- P0：**0**
- P1：**6**
- P2：**5**
- 本轮没有修改 handbook、README、STYLE、appendices 或 assets。
- 完成上述 P1 后，核心内容可进入下一次“零 P0/P1”验收；P2 可在不改变科学结论的编辑轮集中处理。
