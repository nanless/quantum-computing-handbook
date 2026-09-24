# 第 47 轮：算法组修订与定向复核

日期：2026-09-23。只修改第 08、16 章的两处 P2，以及第 16 章同段的相干更新措辞；没有改动共享练习、术语表、阅读版或 sources/。问题起点见[第 46 轮审校](round46-algorithms-audit.md)。

## 已修订

1. **三顶点路径的 QAOA。** 在 handbook/08-applications.md 第 3 节增补 $U_B^\dagger Z_1Z_2U_B$ 的四项展开、各项经代价层共轭后的 $|+++\rangle$ 期望表、从 $Z_1Y_2$ 得到相邻边 $\cos\gamma$ 的解释，以及最优角度 $\beta=\pi/8,\gamma=\pi/3$ 的一阶导数检验。由此求得 $p=1$ 的最大期望割值 $1+3\sqrt3/8\approx1.64952$，并明确它只属于这条路径与本书符号约定。独立用三比特状态向量作矩阵数值核算，得到 $1.6495190528383281$；解析式给 $1.649519052838329$。

2. **element distinctness 的查询指数。** 在 handbook/16-advanced-algorithms-verification.md 第 4.3 节由唯一相等数对逐步算出子集标记比例 $r(r-1)/[N(N-1)]$，再代 Johnson 图经典链谱隙 $\Theta(1/r)$、相干缓存的 $S=O(r),U=O(1),C=0$，得 $O(r+N/\sqrt r)$；平衡两项给 $r=\Theta(N^{2/3})$。另说明 $O(r)$ 个数值槽并非免费量子内存，$C=0$ 只指不再调用数值 oracle，经典/量子门的重复值检查仍需计费。第 4.2 节将 $U$ 明确写成可相干执行且可逆的更新，而非经典邻居抽样。

## 来源与复核边界

- [Wang 等原论文的修订版](https://arxiv.org/html/1706.02998v2)给出一般图 $p=1$ 的解析式；其修订历史注明补过式 (14) 的因子 2，本次按修订版和本书的 $e^{-i\gamma C},e^{-i\beta B}$ 符号约定逐项复算。
- [Ambainis 原论文](https://arxiv.org/html/quant-ph/0311001v9)给出子集缓存与 $O(N^{2/3})$ 查询结果；[Magniez、Nayak、Roland、Santha 原论文](https://arxiv.org/html/quant-ph/0608026v4)给出 $S+(U/\sqrt\delta+C)/\sqrt\varepsilon$ 搜索框架及 Johnson 图 $\delta=\Theta(1/r)$ 的条件。
- 第二轮定向回读了新增文字与相邻上下文，检查符号、维度、概率、$O(\cdot)$ 使用和查询/门成本分离。仅在上述修订范围内，未留下新的 P0–P2；这不代表全书知识已穷尽。阅读版的公式与手机表格渲染须由主审在最终构建中验收。
