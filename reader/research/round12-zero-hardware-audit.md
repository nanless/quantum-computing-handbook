# 第 12 轮硬件、系统与网络零问题验收

审查日期：2026-09-22  
审查方式：只读复核；除本报告外，未修改 `handbook/`、`README.md` 或任何图表。

## 结论

**本轮未发现问题。**

| 等级 | 数量 | 结论 |
|---|---:|---|
| P0 | 0 | 无阻断发布的事实、公式或结构错误 |
| P1 | 0 | 无需要本轮修正的实质性误导、证据越界或缺漏 |
| P2 | 0 | 无需要继续润色、补链接或调整图表的明确问题 |

## 复核范围

- 硬件、资源基准、网络安全与系统控制：`09-hardware.md`、`11-resources-benchmarks.md`、`12-security-network-frontiers.md`、`14-compilation-control.md`。
- 第 10 章中与硬件闭环有关的 Pauli 帧表述。
- 全部附录、根目录与手册 README、`STYLE.md`。
- `bloch-sphere.svg`、`evidence-ladder.svg`、`qec-syndrome.svg` 及其正文引用。
- 第 10 轮遗留项、时效事实、例题、114 道题答案、本地链接、外链语法、代码围栏和控制字符。

## 第 10 轮问题回归验证

以下修复均仍然存在，且正文与集中参考页一致：

1. H. F. Legg 条目已使用正式题名 **“On the robustness of topological gap detection via transport”**，DOI `10.1038/s41586-026-10567-8`，卷页为 *Nature* 654, E22–E26 (2026)。Crossmark 记录的正式题名与 2026-06-24 在线日期一致：<https://crossmark.crossref.org/dialog/?doi=10.1038%2Fs41586-026-10567-8>。
2. 作者回复已使用正式题名 **“Reply to: On the robustness of topological gap detection via transport”**，DOI `10.1038/s41586-026-10568-7`，卷页为 *Nature* 654, E27–E28 (2026)。Nature 的 Matters Arising 列表与 PubMed 元数据一致：<https://www.nature.com/nature/articles?type=matters-arising>、<https://pubmed.ncbi.nlm.nih.gov/42342876/>。
3. N. van Loo et al. 条目已写为 **“Single-shot parity readout of a minimal Kitaev chain”**，*Nature* 650, 334–339 (2026)，DOI `10.1038/s41586-025-09927-7`，并准确标出 2026-02-11 在线：<https://www.nature.com/articles/s41586-025-09927-7>。
4. `10-error-correction.md` 的首次相关用法已写为“Pauli 帧（Pauli frame）”；术语表也有同一定义。第 12、14 章的简短定义与之没有冲突。
5. 网络正文、术语表和第 12 章第 6 题答案统一使用“成功先兆（herald）”，并明确它是概率性操作成功的经典标志，不读取未知量子信息。

## 时效事实抽查

抽查均以一手论文、官方标准页或正式元数据为准；教材的日期、限定词和证据边界与来源相符。

| 抽查项 | 来源复核 | 教材结论 |
|---|---|---|
| Willow 表面码 | Nature 论文列出 2024-12-09 在线、2025 卷期、2026-04-28 作者更正；101 比特距离 7、每周期逻辑错误 `0.143% ± 0.003%`、距离加 2 的抑制因子 `2.14 ± 0.02` | 数字、日期及“特定存储实验而非通用容错机”的限定准确。<https://www.nature.com/articles/s41586-024-08449-y> |
| 6100 原子光镊阵列 | Nature 论文报告 6100 个原子、`12.6(1) s` 相干时间和 `22.9(1) min` 真空寿命，在线日期 2025-09-24 | 教材没有把阵列规模误写成 6100 个同时执行通用高保真门的逻辑处理器。<https://www.nature.com/articles/s41586-025-09641-4> |
| 光子条件指标 | 论文明确写明所报 SPAM、融合和互连指标“conditional on photon detection and not accounting for loss”，在线日期 2025-02-26 | 教材明确保留条件化、损耗与接受率边界。<https://www.nature.com/articles/s41586-025-08820-7> |
| 离子逻辑改进 | Nature 论文在线日期 2026-06-10；11×–800× 相对所选物理线路基线，结合错误检测与后选择 | 教材没有把范围外推为任意算法、任意深度的普遍改进。<https://www.nature.com/articles/s41586-026-10628-y> |
| Majorana 证据边界 | 原论文明确说宇称测量本身不能无歧义地区分拓扑 MZM 与精细调节的普通 Andreev 态；2026 年 Matters Arising 与回复并存；van Loo 论文明确是保护有限的两站点“poor man's Majoranas” | 教材使用“器件与宇称测量进展，但不能声称已无争议实现受拓扑保护通用量子比特”的谨慎表述。<https://www.nature.com/articles/s41586-024-08445-2>、<https://www.nature.com/articles/s41586-025-09927-7> |
| NIST PQC / HQC | NIST 当前项目页仍表述 HQC 标准化正在进行；Selected Algorithms 页面未把它列成已经发布的最终 FIPS | 教材准确区分 2025-03-11“选中”、草案/制定流程与最终 FIPS。<https://csrc.nist.gov/projects/post-quantum-cryptography>、<https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization/selected-algorithms> |
| 量子网络里程碑 | Knaut et al. 论文为两个多比特 SiV 节点、40 km 盘纤和 35 km 波士顿部署光纤回路；Kucera et al. 为 14.4 km 城市暗纤上的纠缠与离子到电信光子传态 | 距离、链路类型、节点数与“不是多跳容错互联网”的限定准确。<https://www.nature.com/articles/s41586-024-07252-z>、<https://www.nature.com/articles/s41534-024-00886-x> |
| 网络协议栈地位 | RFC 9340 明确为 Informational，且不是 Internet Standards Track 规范 | 教材将分层图称为分析框架，没有误称统一部署标准。<https://www.rfc-editor.org/rfc/rfc9340> |

## 例题复算

| 项目 | 独立复算 | 结论 |
|---|---:|---|
| 两条 `p=0.1` 链路并行等待 | `2/p - 1/[1-(1-p)^2] = 14.736842...` 轮；每轮 1 ms 即 14.74 ms | 正确 |
| 系统能耗 | `20 kW × 30 s / 0.25 = 2400 kJ = 2.4 MJ = 0.6667 kWh` | 正确，单位换算与系统边界说明完整 |
| Rabi 门时长 | `Ω/2π=10 MHz` 时 `Tπ=π/Ω=50 ns`，`Tπ/2=25 ns` | 正确 |
| 动态反馈等待弛豫 | 六项时延合计 `1.6 μs`；`1-exp(-1.6/100)=1.5873%` | 正确；退相干被正确表述为等待后果而非第七项时延 |
| SWAP 路由 | 两次 SWAP、每次 3 个 CNOT，共 6 个额外 CNOT | 正确 |
| 关键路径 | `20+200+800=1020 ns` | 正确；独立单比特门与并行测量没有重复相加 |

## 结构、图表与练习检查

- 17 章自检题数量依次为 `4, 6, 4, 4, 5, 6, 8, 10, 8, 5, 9, 7, 7, 6, 8, 7, 10`，合计 **114**；附录各章答案数量逐章完全一致。
- 所有章节“答案见”锚点都指向实际存在的附录章节。
- 三张 SVG 均通过 `xmllint --noout`；XML 结构有效。图中文字、符号和正文一致：Bloch 球的 `±X/±Y/±Z` 标签正确；证据阶梯与正文的四级层次一致；三比特重复码图的 `X₂` 综合征 `(-1,-1)` 与正文一致。
- 三张 SVG 均已在正确章节引用：Bloch 球在第 2 章，证据阶梯在第 9 章，纠错综合征图在第 10 章；替代文字清楚。
- 全部本地 Markdown 目标存在；183 个 HTTP(S) 引用（126 个唯一 URL）均通过 URI 语法解析，关键时效外链已实际打开抽查。
- `README.md` 与全部 Markdown 文件的三反引号围栏数量均为偶数，未发现未闭合围栏。
- `README.md` 与 `handbook/` 未发现 `U+0000–U+0008`、`U+000B`、`U+000C`、`U+000E–U+001F` 或 `U+007F` 控制字符。

## 残余风险

P0/P1/P2 均为 0。唯一持续性维护事项不是当前缺陷：设备纪录、云平台接口、NIST 标准状态和前沿论文可能在截止日后变化；教材已经对这些条目标注截至日期、证据边界和复核入口。
