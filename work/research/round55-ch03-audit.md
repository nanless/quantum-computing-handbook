# 第 3 章修订前审查（2026-09-24）

范围：`handbook/03-multiple-qubits.md` 与练习附录第 3 章；只核对基础原理和教学表达，不把本轮视为全书完成审校。

## 核对来源

- [IBM Quantum Learning：多个系统的量子信息](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/multiple-systems/quantum-information)：张量积、联合态和局部测量。
- [IBM Quantum Learning：多系统与约化态](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/multiple-systems)：偏迹公式、Bell 态的局部混态。
- [IBM Quantum Learning：纠缠作为资源](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/introduction)：纠缠与共享随机数不是一回事。
- [Watrous, *The Theory of Quantum Information*, §1.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf)：Schmidt 分解的数学表述。
- [IBM Quantum Learning：局部测量的形式](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/general-measurements/formulations-of-measurements)：局部测量结果与条件态。

## 发现

| 优先级 | 位置 | 问题 | 拟改法 |
|---|---|---|---|
| 高 | 第 1 节 | 由 `n` 比特直接跳到 $2^n$ 维和指数振幅；缺少两比特四种基序、Kronecker 积、索引顺序的手算。 | 从两比特乘积的四格展开起步，再推广。 |
| 高 | 第 2 节 | $ad-bc$ 测试前没有真正演练四系数如何来自乘积；反方向一句“秩为一”对长期没看数学的读者太陡。 | 给至少两个逐项算例，并分情形证明逆向，秩术语移进阶注。 |
| 高 | 第 3、6 节 | Bell 态与经典混合的关键差别主要是文字；缺少在 $X$ 基逐项展开、四种概率表。 | 完整展开两个态，解释相位正负为何在改变测量基后可见。 |
| 高 | 第 4 节 | 偏迹定义虽正确，但没有由矩阵分块演示；“删掉 B”这一错误容易重现。 | 添加四乘四密度矩阵、索引相加规则与逐格算例，说明局部态的统计意义。 |
| 高 | 第 4 节 | 局部测量的概率、保留结果后的态、丢弃结果后的态放在大段文字中，容易混淆。 | 分为三个明确步骤，对 Bell 态和部分纠缠态都算。 |
| 中 | 第 5 节 | Schmidt 分解突然出现，对不会奇异值分解者难以理解。 | 先用例子说明它是“双边各换一组基”的形式，再把一般定理和证明范围说明白。 |
| 中 | 第 7 节 | CHSH 的技术证明长且抽象，挤占主线；初学者不易区分实验含义与数学补充。 | 主线保留可核对的四项相关值，范数证明标明进阶回看。 |
| 中 | 第 8 节 | 单配性是更高级主题，与本章起步路径衔接弱。 | 保留正确的纯态特殊例子，标明进阶回看，避免口号化。 |
| 中 | 自检 | 四题不足以检验张量积、X 基比较、偏迹逐格与条件态。 | 增至覆盖每个核心计算的题组，答案写步骤。 |
| 中 | 视觉 | 本章没有直接解释“联合四格、偏迹取对角块”的图。 | 新增可黑白阅读的静态 SVG 或相应清晰表格。 |

现有章节在抽样核对中未发现需要紧急纠正的基础公式错误。这里的主要缺陷是推导密度不足与知识顺序不适合数学久未使用的读者。
