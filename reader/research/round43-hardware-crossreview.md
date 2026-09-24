# 第 43 轮：硬件组第 42 轮修订交叉审查（只读）

范围：`handbook/09-hardware.md`、`handbook/19-engineering-architecture.md`、`handbook/assets/hardware-control-lanes.svg`，以及 `work/rendered/hardware-control-lanes-round42-{light,dark}-{1440,390}.png` 四张截图。另查阅读器中普通 SVG 的样式，以判断 390 px 图像能否在正文中阅读。本轮未改正文、样式、图或 `sources/`。

## 待处理

1. **P1｜五平台 SVG 在旧手机截图中几乎不可读；阅读版已修，待截图签收。** `hardware-control-lanes.svg` 的原始 `viewBox` 为 1400×820，浅色/深色 1440 px 截图中文字清楚、箭头和格子没有明显重叠；先前两张 390 px 截图把整张图缩到约 350 px，主格文字相当于约 4–6 px。审查期间，阅读版新增了科学 SVG 的局部横向滚动、手机最小 880 px 图宽和“图可左右滑动”提示（`tools/reader/reader.css`、`tools/reader/build.mjs`）；源 SVG 未变。这正对准了问题，但这些旧截图不能证明新阅读版的效果。仍需在真正阅读页复查 390 px 浅/深两种主题：没有全页横向溢出，图内可左右滑至最右列，字和格线在局部窗口能辨读。此项原先是实际可见的版式缺陷，而非源 SVG 本身越界。

2. **P2｜GKP 增益的“分母”还可更精确。** `19-engineering-architecture.md:359` 已正确限定为“对应维数的物理腔 Fock 态”且非通用门保真度，优于笼统的“量子比特寿命”。但“一样实验条件下、使用对应维数的物理腔 Fock 态存储的信息”容易被理解为直接并行测得完整物理 qudit 存储曲线。Brock 等人的[原论文](https://www.nature.com/articles/s41586-025-08899-y)明确用同装置实测腔 $T_{1,c}$ 和 Ramsey $T_{2R,c}$ 计算/外推物理 Fock qudit 的有效衰减率 $\Gamma_d^{\rm Fock}$，再与测得的逻辑 GKP 有效衰减率比 $G_d=\Gamma_d^{\rm Fock}/\Gamma_d^{\rm GKP}$；qutrit 为 $1.82\pm0.03$，ququart 为 $1.87\pm0.03$（论文正文“Characterizing quantum memories”“Logical qutrit”“Logical ququart”段）。建议将分母一句写为“基于同设备测得的腔弛豫和 Ramsey 退相干参数，外推相同维数的物理腔 Fock 编码短时有效衰减率”；再称这个倒数比为有效寿命增益。这样可防止把实验定义扩大为任意裸量子比特或直接测得的长时寿命倍数。

3. **P3｜LO/LOCC 总结句略可消除误读。** `19-engineering-architecture.md:285–291` 的表已清楚说 LO 不要求实时跨芯片反馈、LOCC 使用该链路，分类实质正确。紧随表的“两个各有 127 比特的处理器通过实时经典链路，分别实验了……”单读可能暗示 LO 那组也使用链路。建议改为“两处理器具备实时经典链路；其中 LO 实验只在经典端重构，LOCC 实验使用跨芯片前馈”。[2024 年原论文](https://www.nature.com/articles/s41586-024-08178-2)第 73–77、102–116 段明确两者区别；LO 可在单一设备上顺序运行子线路，LOCC 才验证实时跨设备条件门。原文的 142 qubit 是摘要所说的最高跨 QPU 线路规模，主要图态例子另是 134 qubit；本章“最多 142”没有把两者混同。

4. **P3｜超导读出格可标注 HEMT 所处温级。** SVG 第 34 行写“JPA/TWPA → HEMT”，下方写“室温放大、ADC、判决”；`19-engineering-architecture.md:53` 则明确顺序为量子受限前置放大、**4 K HEMT**、室温放大、ADC。图在一格里没有把 4 K 写出来，容易让第一次看图的读者把 HEMT 与“室温放大”混成同一级。若格内宽度允许，建议写“JPA/TWPA → 4 K HEMT”，下行保留室温后端。[超导量子器件一手实验方法](https://www.nature.com/articles/s41467-024-47857-6)也明确把 HEMT 安在 4 K 级，随后才是室温链路。图已有空间，但仍需手机可读性先得到修复。

## 核对无误的重点

- **2024 LO/LOCC 实验口径。** [Carrera Vazquez 等原论文](https://www.nature.com/articles/s41586-024-08178-2)明确有 LO-only 准概率线路切割、LOCC 消耗切割所得“虚拟 Bell 对”并跨芯片前馈；没有可保存的实体远程 Bell 对。`19-engineering-architecture.md:285–291` 的表和“不是相干量子链路”判断正确。
- **Google 论文与更正。** [原论文](https://doi.org/10.1038/s41586-024-08449-y)给距离 7 存储占 49 数据 + 48 测量 + 4 泄漏清除 = 101 个物理比特，位于 105 比特 Willow 处理器；$0.143\%\pm0.003\%$ 每轮与 $2.14\pm0.02$ 抑制因子无误。[2026 作者更正的官方 PDF](https://www.nature.com/articles/s41586-026-10559-8.pdf)只改图 3a 中重复码横轴标签和两条图例，不是距离 7 数据。`09-hardware.md:169` 准确保持存储实验与通用容错计算的界限。
- **Ramsey 单位。** `09-hardware.md:120–127` 以 $\cos(\Delta t+\phi)$ 写角频率失谐 $\Delta$（rad/s），并明示 $\Delta=2\pi\Delta f$；与第 15 章 $\cos(2\pi\Delta f t+\phi)$ 等价，指数 $t/T_2^*$ 无量纲。
- **离子阱图格与回环。** SVG 离子阱泳道保留了独立的“电极搬运/激光寻址”“内态+运动模”“荧光→PMT/相机”“光抽运/淬灭、再冷却与复用”；四段箭头从左至右对齐，1440 px 浅/深色格内文字无可见碰撞。图首说明横箭头代表**本轮**处理顺序，末句说各平台完成复位后进入各自下一轮；并未用右列箭头误画成同一轮持续闭环。因此内容与方向正确，真正问题是手机缩放。

本审查未发现上述内容中的硬性数值错误。P1 可读性问题已有阅读版修复、仍待真实页面的移动端浅/深截图签收；GKP 比较基线的 P2 精确化仍待硬件组修订，另有 2 项 P3 措辞/标注建议。
