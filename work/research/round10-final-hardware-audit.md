# 第 10 轮零问题验收：硬件、系统、网络与附录

验收日期：2026-09-22  
范围：`handbook/09-hardware.md`、`11-resources-benchmarks.md`、`12-security-network-frontiers.md`、`14-compilation-control.md`、全部附录、两个 README、`STYLE.md`、三张 SVG，并交叉检查 08、10 等章节中的硬件事实与术语引用。  
约束：本轮只读，不修改 handbook、附录、README、STYLE 或 assets。

## 1. 验收结论

| 等级 | 数量 | 结论 |
|---|---:|---|
| P0 | **0** | 未发现公式、物理结论、安全边界、实验规模或示例计算错误。 |
| P1 | **2** | Majorana 的一条正式论文题名仍沿用预印本题名；另一个 2026 年实验事实缺少对应一手论文条目。 |
| P2 | **1** | 两处跨章节术语没有采用术语表的统一中文名称。 |

因此本轮**不能写“零问题”**。除下列 3 项外，指定范围均通过。

## 2. P1：必须修复

### P1-1｜正式 Matters Arising 的题名写成了预印本题名

- 位置：
  - `handbook/09-hardware.md:208`
  - `handbook/appendices/references.md:57`
- 当前写法：H. F. Legg, “Comment on ‘Interferometric single-shot parity measurement in InAs–Al hybrid devices’”, DOI `10.1038/s41586-026-10567-8`。
- 问题：该 DOI 的正式同行评议版本题名是 **“On the robustness of topological gap detection via transport”**。当前链接、作者、卷页和年份正确，但显示题名仍是 arXiv 评论稿题名，造成书目元数据不一致。
- 精确修改：两处统一改为：

  > H. F. Legg, [On the robustness of topological gap detection via transport](https://doi.org/10.1038/s41586-026-10567-8), *Nature* 654, E22–E26 (2026)；Microsoft Quantum et al., [Reply to: On the robustness of topological gap detection via transport](https://doi.org/10.1038/s41586-026-10568-7), *Nature* 654, E27–E28 (2026)。

- 一手/权威元数据：[Crossmark 记录](https://crossmark.crossref.org/dialog/?doi=10.1038%2Fs41586-026-10567-8)给出正式题名、作者和 2026-06-24 在线日期；[原论文 Nature 页面](https://www.nature.com/articles/s41586-024-08445-2)也明确链接到 2026-06-24 的 Matters Arising。回复的正式题名、卷页与 DOI 可由[出版记录](https://pubmed.ncbi.nlm.nih.gov/42342876/)交叉核对。

### P1-2｜2026 年 minimal Kitaev chain 的时效事实没有对应来源条目

- 位置：`handbook/09-hardware.md:165` 的“2026 年两站点 Kitaev 链工作实现了长于 1 ms 的宇称读出”。
- 问题：该句事实与限定词正确，但本章参考资料没有列出支撑它的论文；现有 Aghaee 论文与 Legg Matters Arising 支撑的是另一套 InAs–Al 器件及其争议，不能代替这条独立实验来源。对于带年份、寿命数字和平台限定的快速变化事实，STYLE 要求给一手来源。
- 精确修改：在第 09 章参考资料加入：

  > N. van Loo et al., [Single-shot parity readout of a minimal Kitaev chain](https://www.nature.com/articles/s41586-025-09927-7), *Nature* 650, 334–339 (2026；2026-02-11 在线)。

  集中参考资料页是“精选入口”，可选同步加入，但本章本地书目必须加入。
- 一手来源：[Nature 论文页](https://www.nature.com/articles/s41586-025-09927-7)明确写出两站点 minimal chain、poor man's Majoranas、保护有限，以及随机电报切换寿命超过 1 ms；这些限定与正文一致。

## 3. P2：术语统一

### P2-1｜“成功先兆”和“Pauli 帧”尚未在全书完全统一

- 术语表的规范名称：`成功先兆（herald）`、`Pauli 帧（Pauli frame）`。
- 不一致位置：
  - `handbook/appendices/exercises.md:258` 写“先兆信号（herald）结果”；
  - `handbook/10-error-correction.md:280` 写“Pauli frame（……）”。
- 精确修改：分别改为“成功先兆（herald）结果”和“Pauli 帧（Pauli frame，在经典控制器中记录待施加的 Pauli 修正）”。技术含义目前没有错，本项只影响全书术语一致性和初学者检索。

## 4. 时效事实重新核验

以下项目均以本轮日期重新打开一手或标准组织页面。除第 2 节的书目问题外，事实、日期和限定词通过：

| 项目 | 验收结果 | 核验来源 |
|---|---|---|
| HQC | **通过。** NIST 页面更新于 2026-08-05，仍写 HQC 于 2025-03-11 selected for standardization；Selected Algorithms 仍为 “FIPS coming soon”，正文没有把它写成最终 FIPS。 | [NIST Standardization](https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post_Quantum_Cryptography-Standardization)、[Selected Algorithms](https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization/selected-algorithms) |
| Willow 表面码存储 | **通过。** 101 物理量子比特、距离 7、每循环 $0.143\%\pm0.003\%$、$\Lambda=2.14\pm0.02$；Nature 页面列出 2026-04-28 作者更正。正文正确限定为存储实验。 | [Nature 原论文](https://www.nature.com/articles/s41586-024-08449-y) |
| 中性原子 6,100 阵列 | **通过。** 日期、规模、12.6 s 相干与约 23 min 寿命没有被外推为 6,100 个通用逻辑比特。 | [Nature 论文](https://www.nature.com/articles/s41586-025-09641-4) |
| 光子条件指标 | **通过。** 原文明确为 conditional on photon detection and not accounting for loss；正文同时写出这一条件。 | [Nature 论文](https://www.nature.com/articles/s41586-025-08820-7) |
| 离子逻辑改进 | **通过。** 12→2、16→4 与 11–800 倍均保留特定基线、错误检测、后选择和线路族限定。 | [Nature 论文](https://www.nature.com/articles/s41586-026-10628-y) |
| Majorana 原论文结论 | **通过。** 原文明确说宇称测量不能无歧义地区分拓扑 MZM 与精细调节的普通 Andreev 态；正文没有宣称已证明拓扑量子比特。 | [Nature 原论文](https://www.nature.com/articles/s41586-024-08445-2) |
| Majorana 争议 | **正文通过，书目见 P1-1。** Matters Arising 与回复均为 2026-06-24 正式发表，正文保持中立。 | [Crossmark](https://crossmark.crossref.org/dialog/?doi=10.1038%2Fs41586-026-10567-8)、[回复 DOI](https://doi.org/10.1038/s41586-026-10568-7) |
| Minimal Kitaev chain | **正文通过，缺来源见 P1-2。** 论文为 2026-02-11，Nature 650, 334–339；摘要明确“limited protection”和寿命超过 1 ms。 | [Nature 论文](https://www.nature.com/articles/s41586-025-09927-7) |
| 实时译码 | **通过。** 8 比特 stability experiment、最多 25 轮；9 轮完整响应 9.6 μs=6.5 μs 译码+3.1 μs 控制通信。正文没有外推到大码距。 | [Nature Communications](https://www.nature.com/articles/s41467-026-73331-6) |
| 网络作者与类型 | **通过。** Knaut 是 40/35 km 论文第一作者；RFC 9583 作者为 C. Wang 等且是 informational，不是互联网标准。 | [Knaut et al.](https://www.nature.com/articles/s41586-024-07252-z)、[RFC 9583](https://www.rfc-editor.org/rfc/rfc9583.html)、[RFC 9340](https://www.rfc-editor.org/rfc/rfc9340.html) |
| OpenPulse、ISO、GRAPE | **通过。** 规范范围和 Khaneja 元数据无误，没有把术语标准写成性能认证。 | [OpenPulse 3.1](https://openqasm.com/versions/3.1/language/openpulse.html)、[ISO/IEC 4879:2024](https://www.iso.org/standard/80432.html)、[Khaneja DOI](https://doi.org/10.1016/j.jmr.2004.11.004) |

## 5. 例题与指标复算

| 项目 | 独立复算 | 结论 |
|---|---|---|
| 能耗 | $20\,\mathrm{kW}\times30\,\mathrm{s}/0.25=2400\,\mathrm{kJ}=2.4\,\mathrm{MJ}=0.6667\,\mathrm{kWh}$。正文已补稳定成功概率、近似等平均成本的适用条件。 | **0 个问题** |
| 反馈时延 | $800+150+300+200+150=1600\,\mathrm{ns}=1.6\,\mu\mathrm{s}$；$1-e^{-1.6/100}=1.5873\%\approx1.59\%$。答案现已列全六个分量，并把退相干写成后果。 | **0 个问题** |
| 几何等待 | 对独立 $X,Y\sim\mathrm{Geom}(p)$、支撑集 $1,2,\ldots$，$E[\max(X,Y)]=2/p-1/[1-(1-p)^2]$；$p=0.1$ 得 14.7368 轮，即 14.74 ms。 | **0 个问题** |
| Rabi | $\Omega/2\pi=10\,\mathrm{MHz}$ 给 $t_\pi=\pi/\Omega=50\,\mathrm{ns}$、$t_{\pi/2}=25\,\mathrm{ns}$；$\Delta/\Omega=0.1$。 | **0 个问题** |
| 路由/关键路径 | 两次 SWAP 各 3 CNOT，共 6 CNOT；关键路径 $20+200+800=1020\,\mathrm{ns}$。 | **0 个问题** |

## 6. 结构与资产检查

- **114 题答：通过。** 17 章自检题逐章为 `4,6,4,4,5,6,8,10,8,5,9,7,7,6,8,7,10`，总计 114；附录 17 个答案区逐章数量完全相同。
- **练习残余：已解决。** 第 11 章能量单位已进入数学模式；第 12 章 ms 单位已进入数学模式；第 14 章第 6 题已与六项反馈公式一致。
- **本地链接：通过。** 两个 README、正文与附录的全部本地 Markdown 文件目标存在；09→08、09/11→14 的标题锚点仍存在。
- **围栏：通过。** 全部 Markdown 三反引号围栏成对。
- **控制字符：通过。** README、handbook 和本报告创建前的检查范围未发现 NUL、C0 异常控制字符或 DEL。
- **SVG：通过。** 三张 SVG 均通过 XML 解析；Bloch 球在第 02 章、证据阶梯在第 09 章、综合征流程在第 10 章，各有正文引用。证据阶梯四级名称逐字对应第 08 章；综合征图的 $X_2$、$S_1,S_2=(-1,-1)$ 与正文表一致。
- **README/STYLE：通过。** 章节数、章节名、先修关系、版本日期和附录入口一致；STYLE 中事实日期、图表和初次定义要求与正文总体执行一致。
- **符号与答案：通过，除 P2-1 的中文名称统一。** 根保真度、基序、Pauli 帧含义、动态时延和几何分布支撑集没有冲突。
- **审校记录：通过。** 第五轮的“0 问题”表明确是历史快照，第八、九轮扩展记录没有把后续新增内容误说成已经由第五轮覆盖。

## 7. 最终判定

- P0：**0**
- P1：**2**
- P2：**1**
- 本轮未修改任何 handbook 文件。
- 修复两条 Majorana 书目问题并统一两处中文术语后，可再执行一次针对这 3 处的短验收；其余指定范围本轮为 0。
