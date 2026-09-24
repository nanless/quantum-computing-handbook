# 第 9 轮修订：硬件、系统、网络与附录

日期：2026-09-22  
依据：`work/research/round8-cross-hardware-system-audit.md`

## 1. 本轮结果

第 8 轮的 6 项 P1、5 项 P2 中，本轮完成了 **5 项 P1、4 项 P2**。另有 **1 项 P1、1 项 P2** 位于 `handbook/appendices/exercises.md`；本轮任务明确禁止修改该文件，因此没有越界处理，见第 4 节。

没有修改 `handbook/08-applications.md`、`handbook/appendices/exercises.md` 或 `handbook/appendices/audit-log.md`。

## 2. 已修改文件

| 文件 | 修改 |
|---|---|
| `handbook/09-hardware.md` | 把 Majorana 争议来源从笼统“编辑说明”改为原论文、正式 Matters Arising 与作者回复；正文明确原论文的判别边界；接入与第 08 章四级分类一致的证据阶梯图；核查清单改为追踪更正、Matters Arising 与回复。 |
| `handbook/10-error-correction.md` | 在三比特重复码的 $X_2$ 综合征例子后接入 `qec-syndrome.svg`，补充图中流程、适用假设和相位错误局限。 |
| `handbook/11-resources-benchmarks.md` | 为每成功答案能耗公式补上稳定成功概率、近似等成本重试的适用条件；说明相关或变成本重试应直接用总实测能量除以接受答案数；把 manifest 首次写成“可复现实验清单”。 |
| `handbook/12-security-network-frontiers.md` | 补齐 HQC 截至 2026-09-22 的实际状态；定义“成功先兆”；统一相关用语；行内解释 Pauli 帧；修正 Knaut 论文和 RFC 9583 的作者署名；补当前 NIST 状态页。 |
| `handbook/14-compilation-control.md` | 首次解释探测事件、Pauli 帧和未处理数据积压；Mermaid 图改用中文标签。 |
| `handbook/appendices/glossary.md` | 新增 Pauli 帧、探测事件、成功先兆、可复现实验清单四项定义。 |
| `handbook/appendices/references.md` | 明确本页是精选入口而非完整书目；补硬件里程碑、Majorana 争议、NIST 当前状态、网络论文与 RFC、2026 实时译码等一手来源。 |
| `handbook/assets/evidence-ladder.svg` | 从五级改为与第 08 章完全一致的四级：可运行性、正确性、算法优势、实用优势；同步改标题、说明、配色与文字。 |

`handbook/assets/qec-syndrome.svg` 本身无须改图，只新增正文引用和解释。

## 3. 第 8 轮问题逐项状态

### P1

1. **HQC 当前状态：已修复。** 明确截至 2026-09-22 仍在标准化，NIST Selected Algorithms 标为 “FIPS coming soon”，没有把 2025 计划写成已发布 FIPS。
2. **Majorana 争议来源：已修复。** 使用 H. F. Legg 的正式 Matters Arising 和作者回复，保留中立证据边界。
3. **Knaut 论文作者：已修复。** `M. K. Bhaskar et al.` 改为 `C. M. Knaut et al.`，并补卷页。
4. **RFC 9583 作者：已修复。** 改为 C. Wang、A. Rahman、R. Li、M. Aelmans、K. Chakraborty。
5. **herald 未定义：已修复。** 统一为“成功先兆（herald）”，正文和术语表说明它宣布概率事件成功但不读取未知量子信息。
6. **动态电路第 6 题答案与公式不一致：未修改。** 原因见第 4 节。

### P2

1. **练习答案的数学定界符：未修改。** 原因见第 4 节。
2. **能耗模型条件：已修复。** 补平稳、等平均成本重试假设和实测替代口径。
3. **英文术语首次解释：已修复。** `detector events`、`Pauli frame`、`backlog`、`manifest` 均有中文解释；主要概念进入术语表。
4. **孤立 SVG：已修复。** 两张 SVG 分别接入第 09、10 章；证据阶梯先对齐第 08 章四级定义，未修改第 08 章。
5. **集中参考页范围不明：已修复。** 声明其为精选入口，并补本轮关键一手来源。

## 4. 受任务边界限制的残余项

以下两项只能通过修改 `handbook/appendices/exercises.md` 完成，但本轮明确禁止修改该文件：

1. **残余 P1：第 14 章第 6 题答案。** `exercises.md:294` 仍漏列最终条件脉冲，把等待退相干混入六项时延。后续允许编辑时，应严格列出 $t_{\rm meas}$、$t_{\rm classify}$、$t_{\rm transport}$、$t_{\rm classical}$、$t_{\rm dispatch}$、$t_{\rm pulse}$；再单独说明退相干是时延造成的误差后果。
2. **残余 P2：练习答案单位排版。** `exercises.md:249,266` 的 `(20\,\mathrm{kW})`、`(1\,\mathrm{ms})` 等仍在数学模式之外；后续应改为 `$20\,\mathrm{kW}$`、`$1\,\mathrm{ms}$` 等。

本轮没有通过改写正文公式来迁就错误答案，因为那会降低技术正确性。

## 5. 验证

- 三张 SVG 均通过 XML 解析；证据阶梯不再含旧五级标签或 `s5` 样式。
- `evidence-ladder.svg` 已被第 09 章引用；`qec-syndrome.svg` 已被第 10 章引用；不再是孤立资产。
- 证据阶梯的四个名称逐字对应第 08 章第 9 节；第 08 章未修改。
- 全书指定范围内已无错误署名 `M. K. Bhaskar et al.`、`A. Dahlberg et al.`，也无“期刊随文编辑说明”旧表述。
- `herald` 只保留在首次中文定义与术语表英文对照中，其余正文统一为“成功先兆”。
- HQC 状态保留截止日期与官方动态页面，未把未来计划当成已完成事实。

## 6. 本轮验收

- 已处理：P1 **5**，P2 **4**。
- 因禁止修改练习答案而保留：P1 **1**，P2 **1**。
- 新增 P0：**0**。
- 未发现本轮修改引入的公式、链接、SVG XML 或术语冲突。
