# 第 50 轮：第 08 章角度范围补充后的只读终审

复读第 08 章三顶点路径 QAOA 的最优性段落。第 48 轮指出的唯一 P2 是：原文只在 $0\le\gamma\le\pi$ 求极值，却宣称对所有角度最大。现已补 $2\pi$ 周期及映射 $\gamma'=2\pi-\gamma$、$\beta'=\beta+\pi/4$。核算：$\cos\gamma'=\cos\gamma$、$\sin\gamma'=-\sin\gamma$、$\sin(4\beta')=-\sin(4\beta)$，所以期望式中唯一随角度变化的乘积保持不变；后一半周期映到已分析的前一半周期，端点额外项为零。因此全域最大期望 $1+3\sqrt3/8$ 的论证已闭合。

第 16 章 element distinctness 的独立复算见[第 48 轮报告](round48-algorithms-crossreview.md)，没有待修 P0–P2。此次只读终审未编辑算法组文件、阅读版或 `sources/`。在第 08、16 章此次**指定修订范围**内，未发现遗留 P0–P2；这不是对全书或全部量子计算知识的穷尽性证明。
