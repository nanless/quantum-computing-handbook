# 第 4 章逐篇审查：量子门、电路与基础协议（2026-09-24）

## 范围和约定

- 核对 `handbook/04-circuits-protocols.md` 及 `handbook/appendices/exercises.md` 的第 4 章题答；不改动 `sources/`。
- 全章统一以 `|00>, |01>, |10>, |11>` 排列两比特计算基，左位为第一个张量因子；三比特传态按 Q、A、B 排列。
- 查证来源：IBM Quantum Learning 的 [Circuits](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/quantum-circuits/circuits)、[Quantum teleportation](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/quantum-teleportation)、[Superdense coding](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/superdense-coding)、[The phase-estimation procedure](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/phase-estimation-procedure)，以及 Bennett 等人的[传态原论文](https://doi.org/10.1103/PhysRevLett.70.1895)、Pati–Braunstein 的[不可删除原论文](https://arxiv.org/abs/quant-ph/9911090)、Brylinski 等人的[通用门结果](https://arxiv.org/abs/quant-ph/0108062)。

## 第一轮：发现的问题

| 优先级 | 位置 | 发现 | 拟修订 |
|---|---|---|---|
| P1 | §1–2 | 从“线从左到右”直接跳到酉性、门表。忘了矩阵乘法的读者难以把图上的时间次序和 `U_3U_2U_1` 对上；门表许多作用没有最小算例。 | 从一比特 `|0>→H→Z` 写出每步列向量，明确右乘先执行与软件位序的区别；常用门加具体输入/输出。 |
| P1 | §3 | Bell 态例子只演示了两个非零振幅，未讲清 CNOT 对一般四分量列向量的置换，也没有反例说明 CNOT 不总产生纠缠。 | 先列四条基态规则，再算 `(a,b,c,d)^T→(a,b,d,c)^T`，附四分量数字例子与乘积态反例。 |
| P1 | §6 | 传态表正确，但展开过于拥挤；没有让初学者看清 `1/2` 的分支振幅、`1/4` 的结果概率、按结果归一化、Bob 未收消息时 `I/2` 之间的关系。 | 分开“门操作”“测量”“两位经典消息”“校正”；选一个具体输入走完四分支，并用矩阵说明 `I/2`。 |
| P1 | §7 | 超密编码只有对照表，没有给 Bell 测量的具体解码电路，读者不能验证 `00/01/10/11`；`ZX` 的门序易混淆。 | 推出四态，逐态计算 `CNOT→H` 后的基态结果；注明 `ZX` 表示先 X 后 Z。 |
| P2 | §8 | 相位回踢只有抽象 `U|u>=e^{iθ}|u>`，没有“如何看见相位”的测量例子；初学者可能以为控比特直接量出 θ。 | 加受控 `Z`、目标 `|1>` 的逐步算例，再对控制比特施加 `H` 与测量；说明目标非本征态时通常不分离。 |
| P2 | §4–5 | 不可克隆/不可删除的证明虽基本正确，但缺“把 `|+>` 输入 CNOT 得 Bell 态”的直观核对，以及整体酉复位与局部非酉复位的区别。 | 加可手算反例，限定不可删除命题的封闭系统与环境信息保留范围。 |
| P2 | §9 | “任意单比特门 + 任意纠缠两比特门”是真但未解释“任意”与“有限离散门集可近似”，Clifford/T 与高成本术语突然出现。 | 先解释通用性是逼近目标酉运算，不意味着一门一步完成；把较进阶的容错成本移到回看段。 |
| P2 | §11/答案 | 只有 5 题，多数是概念问答，没有四振幅乘法、传态具体分支、超密解码或相位读出题。 | 扩充阶梯习题和逐步答案，所有题与正文约定一致。 |

## 核对结论

原文传态的 `11` 分支 `XZ|ψ>`、Bob 用 `ZX` 校正，与当前 QAB 位序一致；`ZX(XZ|ψ>)=|ψ>`。原文没有发现会导致协议输出错误的公式，但“概念—例子—计算—测量解释”的台阶不足。本轮不改动第 4 章以外内容。
