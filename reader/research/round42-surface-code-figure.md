# 第 42 轮：表面码空间／时间检测事件图

日期：2026-09-23。对应第 41 轮硬件报告第 3 项 P2。只改 `handbook/10-error-correction.md` 第 7 节，并新增自主绘制的 `handbook/assets/surface-code-events.svg`；不复制论文图片，也不修改 `sources/`。

旧字符框只写“错误链、端点、修正链”，无法直观看出数据错误沿空间连接两个检查位置，或一次读出错误在相邻轮次形成一对时间事件。新双面板分别画同一对空间端点的实际错误链与候选修正链，以及单检查读数 `(0,1,0)` 在两次相邻比较中形成 `δ₂=δ₃=1`。说明图中只画用于发现 X 数据错误的 Z 型检查，X 型检查交错放置但未逐格画出；网格不是特定芯片布线。图文同时说明只有在所画简单拓扑中可收缩的闭环才可当作稳定子，含孔或边界连接须另判。

原理按 [Fowler 等，*Surface codes: Towards practical large-scale quantum computation*](https://doi.org/10.1103/PhysRevA.86.032324) 与 [Acharya 等，*Suppressing quantum errors by scaling a surface code logical qubit*](https://www.nature.com/articles/s41586-022-05434-1) 核对：后者明确区分数据错误的空间检测事件对与测量错误的时间检测事件对。图为教学概念图，未把这两种典型模式宣称为所有电路故障的穷尽；正文随后列出门故障、泄漏、相关噪声与初末边界的限制。

SVG 用实线／虚线及文字区分实际错误链和候选修正链，不只靠红蓝颜色。已用 Chromium 检查浅色与深色实际截图；面板标签、箭头、圆点、路径没有遮挡，文字处于视窗内。手机宽度仍需在最终阅读版检查图像原尺寸链接和页面级溢出。
