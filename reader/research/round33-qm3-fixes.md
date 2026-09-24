# 第 33 轮：Q3 交叉审查修订记录

日期：2026-09-23

依据：`work/research/round32-qm23-crossreview.md`。本轮只修改 `handbook/quantum-mechanics/03-levels-control.md`；8 道答案草稿未改，主审可继续使用已经编号的版本。

## 修订

1. **源文档的通用 Markdown 兼容性风险。** 把平台表单元格中的 ket 左竖线改成 `\lvert`。本项目阅读器会先保护数学片段再交给 Markdown 解析器，所以首轮生成的 HTML 实际没有拆列；修改是为了符合 `STYLE.md`，并避免其他先解析表格、后解析数学的渲染器把 ket 竖线误认成列边界。当前用 `marked.lexer` 复核，表头和六条数据行都恰为三个单元格；正文展示公式不做无关的机械替换。
2. **偏迹先修。** 在系统—环境联合态首次约化处补上

   $$
   \rho_S=\operatorname{Tr}_E(|\Psi\rangle\langle\Psi|)
   =\sum_j{}_E\langle e_j|\Psi\rangle\langle\Psi|e_j\rangle_E,
   $$

   并说明偏迹“忽略环境记录，但保留所有只作用于系统的测量统计”，再回链主篇第 03 章第 4 节的完整定义与 Bell 态算例。这样正文中的环境态内积不再凭空出现。
3. **首次术语和文字。** 用一句白话分别解释 Rydberg 态、Bloch–Siegert 位移和 Zeeman 态；把突然出现的 “Gibbs 分布”改为“第 3 节所用的热平衡 Boltzmann（Gibbs）分布”；删除“处处处于”的重复字。

## 复核结论

- RWA 的算符推导、热占据和答案数值没有改变。
- 平台表每条数据行仍是三列；数学 ket 中不再含可能被通用 Markdown 渲染器当作列边界的裸 `|`。当前阅读器原先已有数学占位保护，因此不把这一项记成已发生的阅读版显示故障。
- 新增偏迹公式只展开原文已有结果，没有改变密度矩阵的共轭次序。
- 本轮没有新增或删减自检题，也没有修改共享附录。
