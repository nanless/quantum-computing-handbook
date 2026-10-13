# 审校记录

## 2026-09-22：从零建立与多轮审校

工作区初始状态只有 `AGENTS.md`，`sources/` 为空，因此不存在可逐页修订的原稿。本轮创建新手册，并保留以下审校轨迹：

1. 数学与量子信息基础专项：知识树、公式、噪声与限制性定理。
2. 算法、复杂度与错误校正专项：查询模型、手算例题、阈值和容错。
3. 硬件与产业专项：六类路线、指标、基准、时间敏感里程碑和营销边界。
4. 第二轮由各专项审稿人直接复算公式、核对边界条件并修订对应成稿。
5. 第三轮交叉检查附录、术语、位序、目录、练习答案和参考文献元数据。

详细研究报告位于 `work/research/`。它们是编辑过程材料，正文以 `handbook/` 为准。

## 2026-09-22：附录交叉检查

- 将练习附录按各章现行自检逐题对应，并补上中间计算、假设与结论边界。旧版“68 道题”和实施中期的“104 道题”都是加入新章或增补题目之前的快照，不再作为固定总数；截至第七轮全部合并后，按每个正文文件的“自检”区间重新统计为 114 题，发布前仍应以同一规则自动重算。
- 修正第 9–12 章旧答案错位，补齐第 4–12 章新增题；重点复算 Grover、QFT、Shor、QAOA、Steane 综合征与距离 5 的纠错能力。
- 符号表明确左高位约定、向量分量、模 2 内积和 T 门定义；术语表补上 phase kickback 的两种常见译名及 QFT、稳定子、阈值、Clifford、魔法态和错误缓解。
- 修正 Steane 论文标题和多项算法/纠错文献的卷页、会议名及作者信息；补入正文直接依赖的模拟、变分算法和容错原始资料。
- 自动检查本级 README 与全部附录中的本地 Markdown 链接，未发现失效目标；调整阅读路线图，使箭头与章节表中的先修关系一致。
- 以 NIST 官方页面复核：FIPS 203/204/205 已于 2024 年发布；HQC 仍处于标准制定过程，不能称为已经发布的最终 FIPS。

本轮详细记录见 [`work/research/round3-appendices-cross-review.md`](../../work/research/round3-appendices-cross-review.md)。

## 2026-09-22：第四轮与第五轮终局验收

第四轮按 P0/P1/P2 门槛分域复核，仍发现并修复：Simon 承诺条件遗漏 $y=x$ 的自反分支、练习措辞与正文不一致、一条参考文献题名不对应，以及 Bloch 球深色模式箭头对比度不足。任何“已修复”都不视为零问题轮次。

修复完成后重新执行第五轮，结果如下：

| 验收范围 | P0 | P1 | P2 | 正文是否需再改 |
|---|---:|---:|---:|---|
| 00–05 与三张 SVG | 0 | 0 | 0 | 否 |
| 06–08、10 | 0 | 0 | 0 | 否 |
| 09、11–12、README 与附录 | 0 | 0 | 0 | 否 |

第五轮当时同时通过了当时版本的题答对应、本地 Markdown 链接解析、数学与代码围栏配对、SVG XML 语法、一级标题唯一性和异常 Unicode 控制字符检查。后续新增章节与题目后，题目总数改为按各章“自检”区间动态重算；截至第七轮全部合并后为 114 题，不再沿用旧版“68 道题”或实施中期“104 道题”的断言。

对应记录：

- [`round5-foundations-zero-issues.md`](../../work/research/round5-foundations-zero-issues.md)
- [`round5-algorithms-qec-zero-issues.md`](../../work/research/round5-algorithms-qec-zero-issues.md)
- [`round5-hardware-appendices-zero-issues.md`](../../work/research/round5-hardware-appendices-zero-issues.md)

## 2026-09-22：第六至第九轮扩展与交叉修订

第六轮重新以“初学者到入门研究生”的目标审查知识缺口，分别形成教学、理论算法和硬件系统三份差距报告。第七轮据此新增量子信息量度、编译与控制、实践复核、高级算法与验证四章，并扩写概率、查询模型、动态反馈、实时译码、能源边界和量子网络等主线。

第八轮由不同专项审稿人交换范围，只审不改。该轮发现并记录了 2 项 P0、11 项 P1 和 19 项 P2；其中包括损坏的 block-encoding 归一化因子、根保真度与平方重叠混用、条件陪集纯态与非选择混态混写、不可克隆证明的全局相位处理、实验诊断误称完整过程层析，以及若干时效、署名、术语、引用和推导跳步问题。因为仍有实质问题，第八轮不计为通过。

第九轮逐项修复上述问题，并同步练习答案。新增的两张示意图已接入错误校正和硬件事实核查章节；NIST HQC 状态、Majorana 争议来源、网络实验署名与实时系统术语也已按截至日期的一手来源更新。合并后仍为 17 个正文文件、114 道自检题与 114 条对应答案。

对应记录：

- [`round6-pedagogy-gap-audit.md`](../../work/research/round6-pedagogy-gap-audit.md)
- [`round6-theory-algorithms-gap-audit.md`](../../work/research/round6-theory-algorithms-gap-audit.md)
- [`round6-hardware-systems-gap-audit.md`](../../work/research/round6-hardware-systems-gap-audit.md)
- [`round8-cross-foundations-information-audit.md`](../../work/research/round8-cross-foundations-information-audit.md)
- [`round8-cross-math-algorithms-audit.md`](../../work/research/round8-cross-math-algorithms-audit.md)
- [`round8-cross-hardware-system-audit.md`](../../work/research/round8-cross-hardware-system-audit.md)
- [`round9-foundations-information-fixes.md`](../../work/research/round9-foundations-information-fixes.md)
- [`round9-math-algorithms-fixes.md`](../../work/research/round9-math-algorithms-fixes.md)
- [`round9-hardware-system-fixes.md`](../../work/research/round9-hardware-system-fixes.md)

## 2026-09-22：第十轮终审与第十一轮定点修订

第十轮再次只读交叉验收，仍发现 3 项 P1 和 7 项 P2，因此没有把该轮记作“零问题”。最重要的遗漏是第 6 章第 1 道自检题与答案语义错配；其余问题涉及 QPE 的模 1 环绕、Shor 对素数与完美幂的经典预处理、block encoding 参数域、首次术语、章内答案导航，以及两条 Majorana 正式论文书目信息。

第十一轮完成定点修订：重写错配答案；补齐 QPE、Shor 和 block encoding 边界；统一高级章术语与符号表；为 00–16 章自检加入对应答案锚点；修正正式 Matters Arising、作者回复和 minimal Kitaev chain 论文信息。第十轮问题清单与第十一轮修订记录见：

- [`round10-final-math-audit.md`](../../work/research/round10-final-math-audit.md)
- [`round10-final-pedagogy-audit.md`](../../work/research/round10-final-pedagogy-audit.md)
- [`round10-final-hardware-audit.md`](../../work/research/round10-final-hardware-audit.md)
- [`round11-math-terminology-fixes.md`](../../work/research/round11-math-terminology-fixes.md)
- [`round11-hardware-reference-fixes.md`](../../work/research/round11-hardware-reference-fixes.md)

## 2026-09-22：第十二至第十四轮最终验收

第十二轮再次分三路只读验收。数学与硬件两路均为 P0=0、P1=0、P2=0；教学一路发现 1 项 P2：量子纠错专用的“探测事件（detector event）”与量子网络中的成功先兆用词发生碰撞。随后将网络语境改为“协议指定的探测器点击、Bell 测量结果或其他测量记录”，不再复用纠错译码术语。

第十三轮复核确认正文、公式、题答、术语、引用、图表和静态结构均无回归；教学审稿仅指出审校记录尚未写入第十二、十三轮，内容本身没有新问题。本节补齐了该审计链。第十四轮在此日志更新后再次进行只读终验，三路报告均为 P0=0、P1=0、P2=0，结论为“本轮未发现问题”。

对应记录：

- [`round12-zero-math-audit.md`](../../work/research/round12-zero-math-audit.md)
- [`round12-zero-pedagogy-audit.md`](../../work/research/round12-zero-pedagogy-audit.md)
- [`round12-zero-hardware-audit.md`](../../work/research/round12-zero-hardware-audit.md)
- [`round13-zero-math-regression.md`](../../work/research/round13-zero-math-regression.md)
- [`round13-zero-pedagogy-audit.md`](../../work/research/round13-zero-pedagogy-audit.md)
- [`round13-zero-hardware-regression.md`](../../work/research/round13-zero-hardware-regression.md)
- [`round14-zero-math-final.md`](../../work/research/round14-zero-math-final.md)
- [`round14-zero-pedagogy-final.md`](../../work/research/round14-zero-pedagogy-final.md)
- [`round14-zero-hardware-final.md`](../../work/research/round14-zero-hardware-final.md)

## 2026-09-22：第十五至第十八轮再次扩展

第十四轮的“零问题”只针对当时的 17 章版本，不代表知识覆盖已经封顶。第十五轮重新从理论信息、计算模型和系统工程三个方向查找结构性空白；现有内容没有发现新的硬性错误，但审稿指出纯化与 Choi 表示、信道容量、不同计算模型、Hamiltonian 复杂度、读出复位、控制链、低温热预算、良率、模块化、qLDPC 和可维护性等研究入口仍过于简略。

第十六轮新增第 17–19 章，并在原章节加入必要回链；新增两张硬件控制 SVG。第十七轮交换审稿范围，只审不改，发现量子指纹码距前提不足，以及 qDRIFT、退火 TTS、绝热等价、Grover 整数轮数、Uhlmann、Stein、容量资源模型、QND、热预算和图中方向等边界仍需补齐。第十八轮逐项完成上述修改。合并后全书为 20 个正文文件、146 道自检题与 146 条对应答案。

对应记录：

- [`round15-theory-information-gap-audit.md`](../../work/research/round15-theory-information-gap-audit.md)
- [`round15-models-algorithms-gap-audit.md`](../../work/research/round15-models-algorithms-gap-audit.md)
- [`round15-hardware-engineering-gap-audit.md`](../../work/research/round15-hardware-engineering-gap-audit.md)
- [`round16-theory-information-implementation.md`](../../work/research/round16-theory-information-implementation.md)
- [`round16-models-algorithms-implementation.md`](../../work/research/round16-models-algorithms-implementation.md)
- [`round16-hardware-engineering-implementation.md`](../../work/research/round16-hardware-engineering-implementation.md)
- [`round16-shared-integration.md`](../../work/research/round16-shared-integration.md)
- [`round17-cross-ch17-math-audit.md`](../../work/research/round17-cross-ch17-math-audit.md)
- [`round17-cross-ch18-pedagogy-audit.md`](../../work/research/round17-cross-ch18-pedagogy-audit.md)
- [`round17-cross-ch19-hardware-audit.md`](../../work/research/round17-cross-ch19-hardware-audit.md)
- [`round18-ch17-fixes.md`](../../work/research/round18-ch17-fixes.md)
- [`round18-ch18-fixes.md`](../../work/research/round18-ch18-fixes.md)
- [`round18-ch19-fixes.md`](../../work/research/round18-ch19-fixes.md)

## 2026-09-22：第十九至第二十一轮扩展版终验

第十九轮对 20 章版本执行三路只读验收。正文公式、时效事实、五张 SVG 和 146 组题答均通过；审稿仍发现 3 项 P2：第十七、十八轮的职责在日志中写反，两处连续变量算符漏写帽号，以及答案中残留未解释的 `canary` 术语。三处均已修正。

第二十轮在修正后再次只读验收，仍发现轻微术语衔接问题：`shots`、Hamiltonian 及现代模拟方法的解释或回链偏晚；第 19 章的 `circuit cutting` 和 `supercheck` 没有在练习答案中同步中文化；本日志还曾在三份报告完成前提前写入“三路全 0”。上述问题均已修正，因此第二十轮不记为零问题轮。

第二十一轮对修正后的完整文档再做数学、教学与硬件三路只读回归。三份报告全部落盘后，三路实际结论均为 P0=0、P1=0、P2=0，即“本轮未发现问题”。这是本次扩展和修订的停止条件。

对应记录：

- [`round19-zero-math-audit.md`](../../work/research/round19-zero-math-audit.md)
- [`round19-zero-pedagogy-audit.md`](../../work/research/round19-zero-pedagogy-audit.md)
- [`round19-zero-hardware-audit.md`](../../work/research/round19-zero-hardware-audit.md)
- [`round20-zero-math-final.md`](../../work/research/round20-zero-math-final.md)
- [`round20-zero-pedagogy-final.md`](../../work/research/round20-zero-pedagogy-final.md)
- [`round20-zero-hardware-final.md`](../../work/research/round20-zero-hardware-final.md)
- [`round21-zero-math-final.md`](../../work/research/round21-zero-math-final.md)
- [`round21-zero-pedagogy-final.md`](../../work/research/round21-zero-pedagogy-final.md)
- [`round21-zero-hardware-final.md`](../../work/research/round21-zero-hardware-final.md)

## 2026-09-22：第二十二至第二十四轮深化与实际排版

用户要求继续改进后，再次由三位审稿代理分别查阅原始论文与官方课程，检查基础、算法、硬件，并交换范围复核。第 21 轮的未发现问题结论保留为历史记录，不作为后续免检依据。

第 22 轮补齐一般测量的多 Kraus 分支、旋转门指数推导、偏迹的局域统计意义、有限精度 QPE 完整分布、Simon 秩增长、Grover 过度旋转、VQE 测量预算、重复纠错记录、读出反演和码距资源算例。第 23 轮仍发现条件与教学问题，包括有限精度 QPE 被过强地说成投影、有限维系统与离散结果混淆、旋转半角解释、无信号条件、纠错首末边界和读出方差传播。第 24 轮逐项修正并复算。

本次还新增离线 HTML 阅读版与 Bell 态制备图。实际渲染发现三处流程图语法错误、字面换行符及科学 SVG 标签/箭头遮挡，已修正。阅读版交叉审查又指出三项自动验证覆盖不足，随后补入源/输出哈希、公式内容与顺序摘要、标题 ID 比对、局部滚动末端和整页抽样检查。这几轮均不记作零问题轮。

对应记录：

- [基础调研与修订](../../work/research/round22-foundations-research-fixes.md)
- [算法调研与修订](../../work/research/round22-algorithms-research-fixes.md)
- [硬件调研与修订](../../work/research/round22-hardware-research-fixes.md)
- [基础交叉审查](../../work/research/round23-foundations-crossreview.md)
- [算法交叉审查](../../work/research/round23-algorithms-crossreview.md)
- [硬件交叉审查](../../work/research/round23-hardware-crossreview.md)
- [阅读版交叉审查](../../work/research/round23-reader-crossreview.md)
- [基础定点修订](../../work/research/round24-foundations-fixes.md)
- [硬件定点修订](../../work/research/round24-hardware-fixes.md)
- [阅读版与视觉修订](../../work/research/round24-reader-visual-fixes.md)

## 2026-09-22：第二十五轮独立终验

在第 22–24 轮修订完成后，三位审稿代理再次只读复核。三份报告全部完成并读取后，实际结论均为 P0=0、P1=0、P2=0，因此本轮记为“在声明的检查范围内未发现待修问题”。

- [数学与算法终验](../../work/research/round25-math-final.md)：复核第 01–08、16–18 章及对应题答，独立复算测量、QPE、Simon、Grover、VQE 和高级章节关键算例。
- [硬件与科学图终验](../../work/research/round25-hardware-final.md)：复核第 09–11、19 章及对应题答，复算纠错与资源链，实际查看六张科学 SVG 和 Bell 图暗色版本。
- [离线阅读版终验](../../work/research/round25-reader-final.md)：核对 27 页源/输出一致性、2855 个公式的内容与顺序、20 张流程图、标题、表格、链接及宽窄屏阅读表现。

全书维持 20 章、146 道自检题和 146 条对应答案。浏览器验证覆盖 54 个页面/宽度组合，另保存 15 张代表页面或局部截图及科学图截图；生成与验证均未发现错误，页面运行无外部网络请求。最新机器报告见[构建结果](../../work/research/reader-build-report.json)与[阅读验证](../../work/research/reader-verification.json)。此结论不是对全部量子计算知识的完备性证明，也不是未经抽样限制的逐像素排版保证；未来新增内容或资料变化仍须重新审校。

## 2026-09-22：第二十六轮重新调研与深化

用户再次要求继续改进后，重新审阅基础、量子信息、算法、实践、硬件控制和网络内容，而非把上一轮通过当作免检依据。此次纠正总览的环节计数、未知优势与不可能性的区别、纠错与实验里程碑的混用；补出正半定反例、分数 ebit 的资源含义，以及 Holevo 上界与实际可访问信息的差别。

算法方面新增分解 35 的非整齐相位读数、连分数候选和重试，补齐 Hamiltonian 模拟误差与操作数的换算；实践章增加 Wilson 区间和分批漂移例子，五段代码均实际运行。硬件方面解释距离 7 实验为何用了 101 而不是裸旋转码的 97 个物理比特，并修正固定角旋转门通用性的条件。

第 12 章新增 BB84 条件概率、渐近密钥比例的适用条件、两段链路的额外存储时间与平均相干因子、纠缠交换的四个条件分支，配一张新 SVG 及四道题答。手机阅读增加小节导航和原尺寸图入口；首页增加按问题查找算例的表格。正文中的“人口振荡”等生硬翻译及部分反复使用的隐喻也已改成直接表述。

第 26 轮为发现并实施修订的轮次，不记为零问题。具体来源与验证见：

- [基础数学与量子信息调研](../../work/research/round26-foundations-research-fixes.md)
- [算法与实践调研](../../work/research/round26-algorithms-research-fixes.md)
- [硬件与编译控制调研](../../work/research/round26-hardware-research-fixes.md)
- [量子网络与阅读体验修订](../../work/research/round26-network-reader-fixes.md)
- [网络例子的独立数值检查](../../work/research/network-example-checks.json)

## 2026-09-22：第二十七至第二十八轮交叉复核与修订

交叉复核继续发现具体问题，因此没有把第 26 轮的内容增加直接当作终验通过。基础部分补上正半定判据的 Hermitian 前提，改写提前使用未定义投影算符的全局相位说明；第 13 章补齐 LOCC 定义、误差趋零的渐近条件、无歧义判别的三结果 POVM 与最优性证明，以及可访问互信息的测量基、条件概率表和计算。

算法部分明确酉门近似下的误差累积条件，展开观测量误差的两项估计，修正 Wilson 区间的覆盖率表述与漂移检验的零假设，并说明 Shor 后处理除重新采样外还可检查候选分母的倍数。硬件控制部分明确 $SX=e^{i\pi/4}R_x(\pi/2)$，不能把只差全局相位的门在受控使用时无条件视为相同。

阅读版实际检查发现：代码围栏中的 Python 注释曾被误识别成标题，导致实践章目录错位。构建已改为按 Markdown 标题结构提取，而不是扫描行首井号；重建后目录顺序、链接与公式检查通过。来源复核还把一条不能核实的 Holevo 论文链接换为期刊原文记录，并把 Levitin 整本书链接细化到原始章节。

对应记录：

- [基础数学的主审复核](../../work/research/round27-foundations-parent-review.md)
- [量子信息的独立交叉复核](../../work/research/round27-foundations-crossreview.md)
- [量子信息的逐项修订与复算](../../work/research/round28-foundations-fixes.md)
- [算法与统计的主审复核](../../work/research/round27-algorithms-parent-review.md)
- [算法与实践的独立复算](../../work/research/round27-algorithms-crossreview.md)
- [网络数学与新增题答的独立复算](../../work/research/round27-network-crossreview.md)
- [控制门相位的复核与修订](../../work/research/round27-hardware-parent-review.md)
- [阅读版标题转换的回归修复](../../work/research/round27-reader-regression.md)
- [阅读版独立交叉复核](../../work/research/round28-reader-crossreview.md)
- [参考链接核查与修订](../../work/research/round28-reference-link-fixes.md)

本阶段的阅读检查包括 27 页在宽屏和手机宽度下的 54 个组合，以及新图的明暗渲染；独立数值脚本检查纠缠交换的四个分支和无条件态、链路存储平均值及 BB84 数值。审稿报告中的阶段性构建数量对应各自快照；最终交付数量应以终验后的最新构建报告为准。

## 2026-09-22：第二十九轮内容复核与记录修正

三路独立复核均未在各自正文范围内发现待修问题：基础组复算判别测量、信息量、渐近纠缠率、门相位和正半定前提；教学组复算网络与 Shor 后处理，并逐章核对 150 道题和 150 条答案；硬件与阅读组核对实验口径，并实际查看新增量子信息内容在桌面、手机上的渲染及新图明暗版本。

主审随后检查审稿记录本身，仍发现两处 P2：等待时间展示式把随机变量定义和均值等式混排，另一处把指标清单修改误记为题目修改。两处仅在报告中，正文原式和题答无误；已由报告作者修正并保留修订记录。因此第 29 轮整体不记为零问题轮，仍需下一轮核验。

- [基础数学与量子信息定点复核](../../work/research/round29-foundations-final-review.md)
- [网络教学与 150 组题答复核](../../work/research/round29-network-teaching-final-review.md)
- [硬件事实与最终图文复核](../../work/research/round29-reader-hardware-final-review.md)
- [主审发现的记录问题与修正要求](../../work/research/round29-report-clarity-fixes.md)

## 2026-09-22：第三十轮修正后终验

第 29 轮的记录问题修正后，三路再次进行有限只读复核。三份报告全部落盘并经主审读取后，实际结果均为 P0=0、P1=0、P2=0。主审还统一了报告中“复核”等用词，并明确各报告的范围可以重叠而结论相容。本轮检查范围内未发现待修问题；这不改写第 29 轮曾发现问题的历史，也不构成对全领域知识绝对完备、永远无错的保证。

- [基础与网络记录终验](../../work/research/round30-foundations-final-review.md)
- [教学记录与题答范围终验](../../work/research/round30-teaching-final-review.md)
- [硬件与阅读版有限回归终验](../../work/research/round30-reader-hardware-final-review.md)

第 30 轮交付版本为 20 章、150 道自检题与 150 条对应答案，配 7 张科学 SVG 和 20 张流程图。主审独立逐章检查题号连续性与题答数量，全部对应。当时离线阅读版包含 27 个 HTML 页面、3116 个数学片段；宽屏和手机宽度共 54 个页面组合的验证覆盖源/输出一致性、公式内容与顺序、标题、表格、链接、导航交互及图片，另有 17 张代表性阅读截图和科学图渲染。这些是该轮历史数量；持续更新的实测结果见[构建报告](../../work/research/reader-build-report.json)、[阅读验证](../../work/research/reader-verification.json)和[网络数值检查](../../work/research/network-example-checks.json)。

正式交付是可离线打开的 HTML 阅读版，不把尚未逐页验收的浏览器打印结果当作 PDF 成品。视觉检查包含实际截图审阅与自动边界检查，但不是每种字体、浏览器与缩放比例的逐像素保证；外部论文仍需联网访问，时敏事实也需在后续使用时重查。

## 2026-09-22—23：第三十一轮新增量子力学基础篇

新增独立的 Q1–Q4 四章，分别解释实验与量子态、可观测量与时间演化、真实器件的能级与驱动、波函数与典型模型。保留主篇 00–19 的编号，把 Q1/Q2 插入零基础路线，Q3 放在硬件前，Q4 标为需要一元微积分的进阶选读。

三个子审稿分组与主审分工查阅大学官方课程、原始理论及实验论文，逐步推导算例；增加 31 道自检题及答案、3 张科学 SVG，并整合符号表、术语表和目录。这一轮是研究与初稿阶段，不宣称没有缺陷。

- [Q1 调研与初稿记录](../../work/research/round31-qm1-research.md)
- [Q2 测量与演化研究](../../work/research/round31-qm2-research.md)
- [Q3 能级与控制研究](../../work/research/round31-qm3-research.md)
- [Q4 模型、插图与复算记录](../../work/research/round31-qm4-research.md)

## 2026-09-23：第三十二轮交叉审查

本轮确实发现了问题：路径记录的“可区分”与“完全可区分”不能混写；密度矩阵和偏迹在首次出现处解释不足；个别术语缺少白话说明；一份个人课堂笔记的证据性质需要明确；Q3 表格中的裸 ket 竖线存在拆列风险。主审还检查了时间演化的适用条件、驱动推导跳步、来源适用范围和新旧章节的符号衔接。

已复算的 Q2/Q3 核心数学和 Q4 势阱、谐振子、势垒公式未发现计算错误；这不能抵消上述条件与教学问题。本轮不是零问题轮。首次 32 页阅读版的 64 个宽窄屏组合检查通过，但作者修订后仍须重新构建。

- [Q2/Q3 数学与先修交叉审](../../work/research/round32-qm23-crossreview.md)
- [Q1/Q4 条件与推导交叉审](../../work/research/round32-qm14-crossreview.md)
- [主审发现与整合检查](../../work/research/round32-qm-integration-review.md)
- [新图与阅读版交叉审](../../work/research/round32-qm-reader-crossreview.md)

## 2026-09-23：第三十三轮修订与回归

Q1 已用记录态重叠解释完整、部分和消失的干涉，明确等权路径与正交记录的条件，并增加 $\gamma=0.6$ 时输出 $0.8/0.2$ 的例子；正文、自检题和共享答案同步修订。密度矩阵先给最小定义，再使用；原先的学生课堂笔记替换为 MIT 官方讲义。第 31 轮研究记录保留初稿历史，并在开头注明后续勘误。

Q3 已补偏迹定义、首次术语解释，以及从旋转坐标系 Hamiltonian 到 Rabi 概率的中间步骤；收窄非线性表述，并补核与逻辑编码对应的实验来源。表格使用安全的数学竖线记法。须说明：当前构建器已保护数学片段，初次 HTML 并未实际拆列；修复的是普通 Markdown 渲染兼容性风险，审稿记录也已据此澄清。

回归检查另外发现 Q1 新增的偏迹回链使用了不存在的锚点，已按主篇真实标题修复。修复后候选版的 64 个宽窄屏组合检查为 0 错误；仍由下一轮独立复核决定是否可以结束本次修订。

- [Q1 条件、来源与答案修复](../../work/research/round33-qm1-fixes.md)
- [Q3 先修、术语与表格修复](../../work/research/round33-qm3-fixes.md)
- [量子力学独立数值检查](../../work/research/qm-example-checks.json)
- [24 章题答编号与数量核对](../../work/research/qm-question-inventory.json)

## 2026-09-23：第三十四轮独立终审与新发现

教学组和图文组在各自范围内未发现新的问题，数学组则发现 1 项 P2：Q1 为避免局部重名而换用的全局相位符号，与全书的 Holevo 量符号相同。局部计算没有错误，但共享符号仍需统一。因此第 34 轮整体不记为零问题轮。

- [教学、31 组题答与阅读路线终审](../../work/research/round34-qm-teaching-final.md)
- [数学与共享符号终审：发现 1 项 P2](../../work/research/round34-qm-math-final.md)
- [插图、Q3 修复区域与阅读版终审](../../work/research/round34-qm-reader-final.md)

## 2026-09-23：第三十五轮统一相位记号

Q1 的全局相位统一改为实数角 θ_g，正文、自检题、共享答案和答案草稿同步；第 33 轮报告补明修订历史，不覆盖当时事实。主审复算 21 个相位与投影测量组合，概率均保持不变；31 条新增答案与原草稿逐字符一致，全书题答编号与数量为 181/181。

两位子审稿在接续任务时触及服务用量限制，未完成计划中的第 36 轮报告。剩余定点复核由主审接续，不将受限任务列为已完成的独立审稿。

- [相位记号修订与验证](../../work/research/round35-qm-symbol-fix.md)

## 2026-09-23：第三十六轮主审定点终验

主审读取修订后的正文、题目、答案及前轮报告，复算相位不变性，核对路径记录条件和章节回链，重新运行题答与数值检查。上述范围内 P0=0、P1=0、P2=0，未发现新的待修问题。本轮明确是主审接续终验，不冒称受用量限制未完成的子审稿已经完成。

当前交付为主篇 20 章与基础篇 4 章，共 181 道自检题及对应答案；配 10 张科学 SVG、20 张流程图，离线阅读版共 32 个 HTML 页面。64 个宽窄屏组合的公式、表格、链接、导航、图片和源码一致性检查通过，另实际查看了最终相位修订的桌面与手机局部截图。此前 20 章、150 题和 27 页的统计属于旧版，不应当成当前数量。

- [主审定点终验及其边界](../../work/research/round36-qm-primary-final.md)
- [最新构建](../../work/research/reader-build-report.json) · [最新阅读验证](../../work/research/reader-verification.json)
- [量子力学算例](../../work/research/qm-example-checks.json) · [题答核对](../../work/research/qm-question-inventory.json)

本次修订止于这一轮已经完成的有限检查。未将没有终点的“所有知识”写成已穷尽，也不将未经逐页验收的打印结果列为 PDF 成品。

## 2026-09-23：第三十七至第三十九轮再研究与交叉修订

三路分别重读先修与数学、算法与计算模型、硬件与系统工程，并查一手课程资料、论文与官方技术文档。新增[入门先修自测与补习路线](prerequisites.md)：按学习目标给出路径，用七道题逐步检查条件概率、复振幅、矩阵作用顺序、张量积、模周期、算法成本、有限采样和波函数归一化。数学章补上柯西－施瓦茨不等式的推导、矩阵和张量积算例；算法章补 Grover 旋转、相位估计读数界、Shor 模乘算符的完整定义、MBQC 自适应角度等缺失步骤。硬件与工程章节区分动态解耦相干时间与自由演化时间，补奇偶综合征的辅助比特计算、偏迹、码距预算、路由时间及独立故障概率，并说明 TTS 公式的统计前提。

第三十八轮交换范围只读复核，仍发现 Shor 模乘定义漏述非互素剩余类，先修路径有跳步；另在主审整合时发现量子力学 Q1 与数学 01 的全局相位角符号需要统一。第三十九轮已修正文、路径和例题，并把窄屏容易错位的字符电路改为按时间排列的表格。上述发现说明第三十八轮不是零问题轮。

- [先修与数学研究](../../work/research/round37-prerequisites-research.md) · [先修缺口与新页](../../work/research/round37-prerequisite-map.md)
- [算法研究](../../work/research/round37-algorithms-research.md) · [硬件与工程研究](../../work/research/round37-hardware-info-research.md)
- [先修路径交叉审](../../work/research/round38-prerequisites-crossreview.md) · [算法交叉审](../../work/research/round38-algorithms-crossreview.md) · [硬件算例交叉审](../../work/research/round38-hardware-crossreview.md)
- [先修路径修订](../../work/research/round39-prerequisites-fixes.md)

## 2026-09-23：第四十轮有限终验

先修路线和第 5 题成本小问由算法组独立重读；第 07 章模乘算符修订段由硬件组交叉复核。两份报告在各自限定范围内均为 P0=0、P1=0、P2=0。模乘复核用 $N=35,a=2$ 实测完整 64 个计算基态的像互不重复，并检查非互素余数。先修复核核对五条路径、31 个源文档本地链接及阅读版链接，且再次确认查询次数不等于端到端门数。

主审复算新增算例，运行量子力学、网络与题答回归检查；24 章共 181 道自检题与 181 条对应答案。最新离线阅读版有 33 页、10 张科学 SVG 和 20 张流程图。66 个宽窄屏页面组合检查无错误、无外部请求，并抽取 33 张截图查看页面、表格两侧与关键图。主审实际查看了先修页的桌面和手机布局、奇偶校验表格窄屏右侧，以及 QSVT 分叉图；长表和长图允许在各自容器中横向滚动。正式数量以随版附带的最新报告为准。

这是一轮**指定增修区域及可自动验证项目**的零问题终验，不是“量子计算全部知识已经没有问题”的断言。此前第三十八、三十九轮发现并修过的问题仍保留在记录中。

- [先修页终审](../../work/research/round40-prerequisites-final.md) · [模乘定义终审](../../work/research/round40-algorithms-final.md)
- [最新构建](../../work/research/reader-build-report.json) · [宽窄屏验证](../../work/research/reader-verification.json)
- [量子力学算例](../../work/research/qm-example-checks.json) · [题答核对](../../work/research/qm-question-inventory.json) · [网络算例](../../work/research/network-example-checks.json)

## 2026-09-23：第四十一至第四十五轮研究、修订与交叉审查

三路分别复查先修与量子力学、算法与信息、硬件与系统，并以原始论文、官方课程和技术文档复核算式与适用范围。第四十一轮还逐图检查阅读版流程图，发现原来只有“流程关系图 1/2”的泛称，难以独立识别图意。第四十二轮据此补足 Bloch 坐标与对易子的逐步推导、CHSH 四相关值、传态四分支、量子行走成本与擦除信道熵的手算、随机指纹码的概率论证，以及 Python/NumPy 可选动手路线；修正离子阱电极搬运与光学寻址的图示，区分 LO 线路切割与需要实时经典前馈的 LOCC 虚拟门。表面码字符示意改成配文字说明的时空检测事件图，科学 SVG 增至 11 张。20 张流程图均有具体图题与相同的替代文字。

第四十三轮交换审查没有把“没有硬性数值错误”当作终点，又指出 CHSH 的例子只证明 $2\sqrt2$ 可达到、随机码缺并合界最后一步、GKP 增益的物理比较基线需精确界定，以及宽科学图在手机上被压得过小。第四十四轮分别补上算符范数上界、$m>16n\ln2$ 的存在性充分条件、由实测腔参数外推的同维 Fock 基线；手机阅读版让宽科学图在自身区域横向滑动，并保持原尺寸图链接。第四十五轮继续逐图逐式检查，修正首页主篇主题图原先过宽的“全书”图题，把 CHSH 长算式分行显示，并移除曾妨碍从图内向上滑动整页的触控限制。每轮缺陷和改动保留在下列记录中，不能把前几轮写成零问题。

- [基础审稿](../../work/research/round41-foundations-audit.md) · [算法审稿](../../work/research/round41-algorithms-audit.md) · [硬件审稿](../../work/research/round41-hardware-audit.md) · [流程图审稿](../../work/research/round41-reader-figures-audit.md)
- [基础修订](../../work/research/round42-foundations-fixes.md) · [算法修订](../../work/research/round42-algorithms-fixes.md) · [硬件修订](../../work/research/round42-hardware-fixes.md) · [表面码图](../../work/research/round42-surface-code-figure.md)
- [基础与纠错交叉审](../../work/research/round43-foundations-qec-crossreview.md) · [算法交叉审](../../work/research/round43-algorithms-crossreview.md) · [硬件交叉审](../../work/research/round43-hardware-crossreview.md)
- [CHSH 上界补证](../../work/research/round44-chsh-bound-fix.md) · [随机码补证](../../work/research/round44-fingerprint-fix.md) · [GKP 基线修订](../../work/research/round44-gkp-fix.md) · [手机科学图与图题](../../work/research/round44-mobile-figures-fix.md)
- [第 45 轮 CHSH 与表面码终审](../../work/research/round45-chsh-qec-final.md) · [随机码与图题终审](../../work/research/round45-fingerprint-figures-final.md) · [硬件与手机科学图终审](../../work/research/round45-hardware-visual-final.md)
- [最新构建](../../work/research/reader-build-report.json) · [宽窄屏验证](../../work/research/reader-verification.json)

三份第四十五轮终审在各自限定范围内均没有待修 P0、P1、P2。最新阅读版是 33 页、181 道自检题及对应答案、11 张科学 SVG、20 张流程图；共 4580 处数学片段，构建错误为零。浏览器对 66 个宽窄屏页面组合复核，留存 38 张截图，未检测到页面验证错误或运行时外部请求；另实际测试科学图的触屏横滑与页面纵滑。这里的零问题只针对这一轮指定区域和已编码检查项，不等同于全学科已被穷尽，也不保证未测试浏览器的表现。

## 2026-09-23：第四十六至第五十轮扩查、补证与有限终验

三路重新从基础、算法、硬件审查初学者是否能复算关键结论；主审另外检查第 15 章的有限样本实验。第四十六轮共记录十一处 P2 教学缺口：路径记录的可见度与条件、纠缠单配性的推导、不可删除的内积约束、$T_1/T_2/T_\phi$ 的矩阵来源；三顶点 QAOA 与元素去重查询指数的推导；Shor 九比特码综合征、随机基准错误率换算、光纤损耗及失谐 Rabi 数字例；Bell 见证的有限样本判定。前三路分别以原始论文和公开课程材料核对，主审为最后一项复算概率界。此轮并非零问题轮。

第四十七轮分组补上逐步算例和边界；Bell 见证新增原始计数表、可分离态阈值证明、三组并合界、练习及说明估计值与保守区间关系的科学 SVG。第四十八轮交换只读复核，Bell 见证的数字和图上坐标、基础新推导均通过，但发现 QAOA 的“全参数域最大值”只证明了半个角度周期，且第 05 章 Ramsey 式的角频率、对比度和初始相位缺明确定义。第四十九轮补了 QAOA 的周期与角度映射证明、Ramsey 的单位和符号，并核对硬件四处新算例。第五十轮对这两处后续修订作限定终审；其结论和整站机器验收见下方报告，不把某一组无问题误写成全部知识无遗漏。

- [基础审稿](../../work/research/round46-foundations-audit.md) · [算法审稿](../../work/research/round46-algorithms-audit.md) · [硬件审稿](../../work/research/round46-hardware-audit.md) · [实践与统计审稿](../../work/research/round46-practice-audit.md)
- [基础修订](../../work/research/round47-foundations-fixes.md) · [算法修订](../../work/research/round47-algorithms-fixes.md) · [硬件修订](../../work/research/round47-hardware-fixes.md) · [Bell 见证与图](../../work/research/round47-practice-fixes.md)
- [算法交叉审](../../work/research/round48-algorithms-crossreview.md) · [基础交叉审](../../work/research/round48-foundations-crossreview.md) · [实践与图交叉审](../../work/research/round48-practice-crossreview.md)
- [QAOA 全域补证](../../work/research/round49-algorithms-followup.md) · [Ramsey 符号修订](../../work/research/round49-foundations-fix.md) · [硬件算例交叉审](../../work/research/round49-hardware-crossreview.md)
- [算法后续终审](../../work/research/round50-algorithms-final-crossreview.md) · [QAOA、Ramsey 与新图终审](../../work/research/round50-final-crossreview.md) · [最新构建](../../work/research/reader-build-report.json) · [宽窄屏验证](../../work/research/reader-verification.json)

在三路终审各自指定区域内，第四十九轮修订后未留下 P0、P1、P2。最终阅读版为 33 页、182 道自检题和 182 条答案、12 张科学 SVG 及 20 张流程图；含 4840 处数学片段。66 个桌面/手机页面组合通过浏览器验证，保存 40 张截图；公式与流程图构建、页面宽度、资源加载和本地链接未报错，运行时没有外部网络请求。另实际查看新图明暗主题和手机上表格、图的右侧。这是明确范围内的有限终验，不能证明学科内容或所有屏幕尺寸永远没有问题。

## 2026-09-23：第五十一至第五十四轮数学工具章细化

本次集中处理“多年没看数学”的读者能否独立复算第 01 章。三路子审分别检查复数与概率、向量矩阵与张量积、教学顺序与插图；主审逐节核对式子并整合。第五十一轮发现的主要不是原公式算错，而是复数四则、共轭和几何相位、行乘列、外积、条件概率与方差在旧稿里跳步过大，原六道自检题也缺少入门台阶。各组以 OpenStax、MIT、Watrous 和量子信息教材的原始材料核对定义与前提。

第五十二轮将第 01 章改为可分段阅读的路线，加入复数四则与相位图、bra/ket 尺寸图、矩阵逐格乘法、$X$ 的本征向量与谱分解、迹和密度矩阵、双比特 $4\times4$ 运算、100 人条件概率表、Bayes 推导、独立重复的频率波动，以及 $n$ 与 $N=2^n$ 的区别。原有进阶证明保留，但注明可回看。第 01 章自检扩为 14 题，答案逐题写出中间步骤，不再把 Bloch 球或 $Y$ 算符当作本章答题捷径。

第五十三轮交换范围只读复核仍发现数处问题：酉矩阵证明漏写初态归一化的前提；同一字母反复指代不同向量；迹的算例未列出矩阵乘积，循环迹的解释漏说数值乘法可交换；一致电路族的硬编码描述过宽；首遍路线与后文章节依赖不完全匹配。这些已在正文修正，因此第五十三轮不记为零问题轮。两张科学 SVG 还分别检查了明暗主题。第五十四轮独立逐题对照 14 道题与 14 条答案，复算归一化、Bayes 后验、频率标准差和复杂度界；指定范围未发现遗留 P0–P2。阅读版有 33 页，数学公式片段 5390 处；66 个桌面/手机页面组合验证无报错、无外部请求。手机 390px 下两张新图可局部横滑，页面本身未横向溢出。该结论只针对本轮指定章节和工具可检查的项目，不代表所有数学或量子计算知识再无可改处。

- [复数与概率审稿](../../work/research/math51-complex-probability-audit.md) · [线性代数与张量积审稿](../../work/research/math51-linear-tensor-audit.md) · [教学及插图审稿](../../work/research/math51-pedagogy-visual-audit.md) · [主审记录](../../work/research/math51-root-audit.md)
- [复数与概率修订](../../work/research/math52-complex-probability-fixes.md) · [张量积修订](../../work/research/math52-tensor-fixes.md) · [科学插图及视觉验收](../../work/research/math52-visual-fixes.md)
- [线性代数交叉审](../../work/research/math53-linear-algebra-crossreview.md) · [复数、概率与复杂度交叉审](../../work/research/math53-complex-probability-crossreview.md) · [教学与手机图文交叉审](../../work/research/math53-pedagogy-visual-crossreview.md)
- [第 54 轮独立数学终审](../../work/research/math54-final-math-review.md)
- [最新构建](../../work/research/reader-build-report.json) · [宽窄屏验证](../../work/research/reader-verification.json) · [题答对应检查](../../work/research/qm-question-inventory.json)

## 2026-09-24：第五十五至第五十九轮全书逐篇改写与交叉审查

这次以细讲的数学工具章为参照，三路子审分别负责单比特、应用、信道；多比特、算法原语、硬件、密码网络；电路协议、代表算法、高级算法。主审负责概览、量子力学 Q1–Q4、噪声、纠错、资源、信息、编译、实践、计算模型和系统工程。各篇先列教学缺口，再查原始论文、课程讲义与官方资料，逐节补概念的前提、小规模手算、误区、练习和逐步答案。20 章主篇与 4 章量子力学基础篇均已进入本轮修订范围；第 01 章沿用前四轮的细讲成果，并参与全书检查。

第一轮改写后仍发现跨章问题：应用章把实证问题按四类并列，旧图却画成可逐级推出结论的阶梯；相位估计曾把高成功率的舍入结果误写成必定正确的二进制前缀；偏迹、传态、Grover 和隐藏子群缺少足够直观的独立插图。这些已分别改成并列证据图、带反例的误差说明和可逐格核对的科学图。第 59 轮三路交换只读审稿又指出若干教学和记号细节，包括无信号性的双向条件、LCU 的 PREPARE 酉矩阵、Trotter 步长的矩阵差、平均门保真度与态保真度的约定，以及图中 H 的双重含义；正文、题答与图注已同步修订。因此前面各轮不能记为零问题轮。

- [全书逐篇进度和范围](../../work/research/round55-fullbook-tracker.md) · [主审跨章核算与来源](../../work/research/round58-root-crossreview.md)
- [单比特审改](../../work/research/round55-ch02-fixes.md) · [多比特审改](../../work/research/round55-ch03-fixes.md) · [电路协议审改](../../work/research/round55-ch04-fixes.md)
- [算法原语](../../work/research/round57-ch06-fixes.md) · [代表算法](../../work/research/round57-ch07-fixes.md) · [应用证据](../../work/research/round57-ch08-fixes.md)
- [硬件](../../work/research/round58-ch09-fixes.md) · [密码网络](../../work/research/round58-ch12-fixes.md) · [高级算法](../../work/research/round58-ch16-fixes.md) · [信道容量](../../work/research/round58-ch18-fixes.md)
- [第 59 轮交叉审 A](../../work/research/round59-crossreview-a.md) · [交叉审 B](../../work/research/round59-crossreview-b.md) · [交叉审 C](../../work/research/round59-crossreview-c.md)

## 2026-09-24：第六十轮整站回归与视觉复核

前一轮审稿修订后重新生成离线阅读版：33 页、7873 处数学片段、20 张流程图，数学与流程图构建错误均为零。24 章的 251 道自检题和 251 条答案编号对应；量子力学与量子网络的数值检查通过。浏览器对 66 个桌面／手机页面组合检查公式、资源、链接、导航和横向溢出，保存 52 张截图，检测到 0 个运行时外部请求和 0 项页面错误。

主审另目视检查新增偏迹、传态、Grover、隐藏子群以及实证类型图的明暗主题，并查看算法、硬件、安全、高级算法、信道等章的手机首屏。视觉检查发现偏迹图末行说明与矩阵边框距离过小，已扩大底部留白并重跑整站回归；未把发现前的版本当成交付版。上述指定范围在修订后未发现待处理的 P0–P2。它是有限验收，不代表所有量子计算知识已穷尽，也不保证不断变化的标准与设备数据今后不需更新。

- [第 60 轮验收摘要](../../work/research/round60-final-integration.md)
- [最终构建数据](../../work/research/reader-build-report.json) · [宽窄屏浏览器检查](../../work/research/reader-verification.json) · [题答对应](../../work/research/qm-question-inventory.json)
- [量子力学算例](../../work/research/qm-example-checks.json) · [量子网络算例](../../work/research/network-example-checks.json)

## 2026-09-24：第六十一至第六十三轮全书再审

第 61 轮让三组子审重新分篇通读全书 24 章，范围互不重叠：一组看概览、数学、单／多比特、电路和量子力学；一组看噪声、算法、应用与信息论；一组看硬件、纠错、基准、安全、控制、实践和系统工程。主审独立检查先修、术语、符号、共用答案与阅读版。此次没有把旧版“已验收”当作新一轮的正确性证明。

确实发现并修正了多处问题：CHSH 中平方等于恒等算符的是两结果的读数算符，不是单个投影；transmon 的绝对／相对非谐性必须说明固定哪些参数；同一 POVM 可以有不同的测后态；二阶 Trotter 的单片公式要写成总时间的重复线路；有限次测量的 VQE 报告值可能低于精确基态能量而不违反变分原理；$T_1$ 弛豫也会压低非对角相干；Choi 矩阵作用于纠缠态的外积而不是 ket。另补了纠缠见证、量子相对熵、能隙证书、随机数安全边界、基准统计和第 13 章逐步答案。

第 62 轮三组交换范围，只读复算彼此的新段落；仍发现纠缠见证对同轴异号 Bell 态的漏检解释过窄，以及退火两处成功概率／统计置信度和逐次后处理成本的口径问题。第 63 轮按这些精确位置复核主审修订后的证明和算例，指定范围未再发现 P0–P2。最后统一“正半定”术语并让阅读版页脚从首页读取实际版本日期；浏览器检查还发现导论改标题后先修页的一处旧锚点，已修复并重验。前两轮发现过问题，不能倒写成零问题轮。

- [基础组第 61 轮](../../work/research/round61-foundations-review.md) · [算法组第 61 轮](../../work/research/round61-algorithms-review.md) · [系统组第 61 轮](../../work/research/round61-systems-review.md) · [附录与术语](../../work/research/round61-appendices-review.md)
- [基础组交叉审](../../work/research/round62-foundations-crossreview.md) · [算法组交叉审](../../work/research/round62-algorithms-crossreview.md) · [系统组交叉审](../../work/research/round62-systems-crossreview.md)
- [基础组定点复核](../../work/research/round63-foundations-final.md) · [算法组定点复核](../../work/research/round63-algorithms-final.md) · [系统组定点复核](../../work/research/round63-systems-final.md)

第 64 轮整站回归数字及其边界见[最终整合报告](../../work/research/round64-final-integration.md)。

## 2026-09-24：第六十五至第六十七轮全书正确性复核

第 65 轮重新把 24 篇正文分给三组，逐篇核对定义、适用条件、符号、主要证明、例题数值、图文关系和自检答案；主审另核先修、符号表、术语表、共用答案与参考资料。时效性硬件及标准结论追溯到原论文或官方页面，数值例另作独立计算。此轮确实发现并处理了数处容易形成错误理解的缺口：Stern–Gerlach 顺序实验必须区分非破坏式路径记录与吸收计数；谐振子降阶范数公式要先假定原态归一化；退极化信道两种参数约定及其共同范围要写出推导；擦除信道经典容量的上界要覆盖跨多次使用的联合编码，不能只靠“每个未擦除比特一位”的直觉；QKD 的光纤本体与整链路损耗、低温 CMOS 活动功耗的脉冲条件、cat 加重复码的每周期逻辑存储指标也已明确。NIST 三项最终后量子标准改为分别链接官方标准页，并记下待处理勘误与正式版状态的区别。

第 66 轮交换范围只读复核，仍找出了此前审稿未见的 P2：8 位 Grover 示例的 12 次只对应**首个**成功峰，不能叫所有整数迭代次数中的全局最佳；码距“可检测”不保证低权重稳定子产生异常综合征；Eastin–Knill 的有限维前提正文漏写；路径记录在统计中不用不等于物理抹除；降阶公式在 $n=0$ 时不能写未定义的 $|-1\rangle$；cat 实验的 $1.65\%$ 要给出论文实际采用的位/相位错误平均定义，不能称作“任一种错误的总概率”。主审依原论文和逐项计算修了这些位置，并同步第 17 章题干与答案。另把 QKD 的两个 dB 口径分别换算成透过率，以便读者看到系统边界的数量级差异。前两轮发现过实质缺口，不能倒写成“零问题”。

第 67 轮三组对上述新修段落再作定点只读复核：第 05、18 章的新推导、第 10、17 章与答案、量子力学 Q1/Q4 及第 19 章的适用条件都在各自指定范围内未发现残留 P0–P2。这个“零待修”仅指明确列出的复核点，不表示所有量子计算知识已被穷尽或任何新实验数据今后都不会改变。

- [第 65 轮基础九篇](../../work/research/round65-foundations-correctness.md) · [算法、噪声与信息七篇](../../work/research/round65-algorithms-correctness.md) · [硬件系统八篇](../../work/research/round65-systems-correctness.md) · [附录与跨章约定](../../work/research/round65-appendices-correctness.md)
- [第 66 轮算法组交叉审](../../work/research/round66-algorithms-crossreview-systems.md) · [基础组交叉审](../../work/research/round66-foundations-crossreview-systems.md) · [系统组交叉审](../../work/research/round66-systems-crossreview-foundations.md)
- [第 67 轮算法与纠错定点终审](../../work/research/round67-algorithms-targeted-final.md) · [噪声与容量定点终审](../../work/research/round67-foundations-targeted-final.md) · [量子力学与实验口径定点终审](../../work/research/round67-systems-targeted-final.md)
- [题答对应和相位样例](../../work/research/qm-question-inventory.json) · [量子力学算例](../../work/research/qm-example-checks.json) · [网络算例](../../work/research/network-example-checks.json)

第 68 轮阅读版构建、浏览器与视觉验收的实测结果另见[整合报告](../../work/research/round68-final-integration.md)。

## 已明确的非目标

- “所有量子计算知识”没有有限终点；本书提供完整入门骨架与研究入口，不替代量子复杂性、量子信息论、凝聚态或器件物理的专著。
- 不维护厂商排行榜。硬件数据变化快，应按正文事实核查框架实时更新。
- 不把小规模教学线路的成功运行写成实用优势。

## 发布门槛

- P0：归一化、维度、矩阵、基序、复杂度类别或事实结论错误。必须修复。
- P1：会让初学者形成错误模型的类比、缺失条件或含混术语。必须修复。
- P2：缺例题、图注不清、跳步或章节衔接弱。尽量在本轮修复。
- P3：扩展阅读、风格优化、非核心新进展。记录后按价值加入。

## 第 69 轮：逐章实验、源码与声音整合（2026-09-26）

三组 subagent 分别完整审查基础11篇、算法6篇、系统6篇，交换复核新增推导；主 agent 审查第15章、整合共享附录与交付。新增六页实验材料、24篇正文实验映射、4张科学图、5个教学合成音频，以及15个开源项目46份固定源码/许可文件。原251道自检题答保持编号，新增实验单独命名。

关键纠正包括子系统能量零点的全局相位、热预算严格边界、综合征定位的错误模型条件、可用率相乘的独立假设、寄存器编号与基顺序区别。进一步补充QPE圆周误差、Grover重试、有限样本预算、QSVT非厄米反例、工程调度和故障区间计算。

[详细整合与验收记录](../../work/research/round69-final-integration.md)列出逐组审稿、交叉检查、运行结果、源码许可和未覆盖范围。离线版扩展到40页；数学/流程图构建、数值实验、原题答编号、80个页面宽度组合及音频加载经过实际检查。浏览器首轮发现的新图顶部越界及代码打包问题已修复，再次验证通过；人工目视是抽查，不能表述成所有长页逐屏人工验收。

## 第70轮：逐章诊断、算法源码与工业研究扩充（2026-09-26）

主审与三个子agent按24篇正文分工全文读审，随后交换核算新增数学和代码。新增32组练习与逐步答案、固定样本及可运行实验，6张由公式生成的科学图；源码阅读摘录扩充至19项目64文件。原251道自检题答编号保留，实验目录补回第19章。工业资料按原论文、官方架构和实际复现状态标记；开源摘录保留提交、哈希、许可和原路径。

本轮纠正了Grover反射换序、综合征后的残余相干、Jeffreys区间口径、固定版本源码与说明冲突等问题。交叉审又发现校准退化分配除零及未验证参数发布边界，均已修复并独立复测；因此不记作零问题轮。新增图完整图像及代表性图文经过目视检查，40页桌面/手机自动验收与人工抽查分别记录。

[本轮详细整合报告](../../work/research/round70-final-integration.md)汇总逐章报告、交换复核、源代码范围、AGENTS修改、实际运行记录和未覆盖边界；[执行计划](../../work/research/round70-plan.md)记录分工与完成口径。最新代码结果写入独立报告，历史第69轮证据保持原样。

## 第71轮：逐章展开与全书和谐性复核（2026-10-13）

三个子代理逐篇完整阅读并实施24篇正文，判断已有架构足够容纳本轮缺口，未另起重复章节。新增24组就地细算题解、6组工业工作流/源码题、固定样本和独立标准库核算；4张公式数据生成图保留生成器。原251道自检编号保留。固定源码扩至26项目97文件，旧19项目版本不换。

实质修正包括qubitization信号条件、虚拟Z与能量基相位约定；补清测量工具、复数Schmidt、参考系统传态、噪声顺序、有限预算、联合错误擦除、协方差物理性和势垒顶连续极限。四阶段末三组交换全文阅读，独立复算并修复代码断言模式、脉冲数学极限、序贯预算与QSP角色衔接问题。实际排版检查发现强调标记和答案续行问题，修复后重新核对公式内容与题号。

[详细整合报告](../../work/research/round71-final-integration.md)列出逐章规划/来源、两轮完整阅读的实际范围、发现与闭环、运行证据、AGENTS调整、图文检查与未复现部分。[执行计划](../../work/research/round71-plan.md)和[新题目录检查](../../work/research/round71-inventory.json)记录章级责任与完整入口。27个代码入口、97文件字节校验及40文档×两宽度检查实际运行；生成截图与人工看图范围分别记录，没有将源码摘录或小模型说成整套工业系统复现。

## 第72轮：24篇再审、完整SDK实跑与数学前置（2026-10-13）

三组作者分别完整阅读基础、算法与系统八篇及旧题答，研究一手文档，随后交换复核新增推导、SDK与原始样本。现有章节足够承载本轮缺口；新增完整SDK实验册，24篇就地练习包含算法组10项细题，另有六组集成练习。旧251道自检编号保留，新增四张科学SVG及生成器。

数学01原本已在主篇前面，离线侧栏却曾先列Q1–Q4。现统一侧栏与翻页为00→01→Q1→02→Q2→03–08→Q3→09–19→Q4，Q4为进阶选读；编号和路径保留。数学章另补矩阵指数，符号表补齐失谐、噪声、根保真度、平均门保真度与QSP响应约定。

26项目完整发行包或完整C/C++提交均实际执行明示CPU任务，补齐HHL、QSP、阴影、化学映射、图行走、CV、IAE、SQD、MPF、OBP、切割、缓解、LGST、层析、纠错、控制与网络。SQD-HPC另有49测试/36652断言；liboqs完整构建三种ML-KEM并检查合法与篡改密文。SDK与标准库默认入口分开，AGENTS补充按明确授权隔离实跑的规则。

真正发现并处理Q4无限尾部缺剩余界、QST验收错配、IAE分批重种子及标题跳级。OBP0.3.0的零接受段上游缺陷保留复现和防护，不倒写为SDK已修复。GRAPE两级小误差对应三能级百分比泄漏、低shot QPT正但不TP等反例保留在正文。

[整合与实际验收](../../work/research/round72-final-integration.md)列出逐章报告、交叉复算、30个标准库入口、26完整项目、四张新图及尚未运行的上层工业流程；[证据索引](../../work/research/round72-inventory.json)与[完整SDK实验册](../labs/sdk-validation.md)给具体入口。自动宽窄屏检查与人工图文抽查分别记录，不冒称所有长页逐屏或全部工业算法完成。
