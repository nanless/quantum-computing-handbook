# 第 71 轮：算法、信息和波函数组逐章规划

日期：2026-10-13。负责人范围：06、07、08、13、16、17、18、Q4；不改共享附录、构建器、目录或 vendor。逐篇指 Markdown 正文，非固定页码 PDF。本报告不代表整书逐屏人工验收。

## 阅读范围与增章结论

分段完整读取八篇正文，随后读取算法实验册、原题答案中本组八章、基础实验册中 13/Q4 相关实现入口，以及 round16、55–58、70 的既有研究与运行说明。原有信息链条从算法骨架到完整算法、应用、量度、现代算法、计算模型与容量已经覆盖本组主线；Q4 的连续空间桥梁亦在。**本组不建议独立增章**。测量协方差放 08、块编码的信号条件放 16、协方差物理性放 18、势垒顶极限放 Q4，能直接接到现有对象。把每个知识点拆成新章会制造符号重复和前置知识循环。

## 各章逐节覆盖与计划

| 章 | 已读主线与已有正确内容 | 实际缺口/修改任务 | 保留边界与跨章接口 |
|---|---|---|---|
| 06 | 九类骨架、相位回踢、DJ/BV、振幅放大、QFT、有限 QPE、非网格条件态、乘积公式、反计算、成功率、多项式/hybrid 下界、Hadamard 测试 | §8 已有极端正交垃圾例，但未算部分泄漏的连续量；补 rho 的非对角元乘垃圾内积，区别复位工作位与反计算 | 查询不等于门；QPE 圆周误差、精确前缀限制保持；连接 05 偏迹与 14 控制 |
| 07 | Simon 余集和 GF(2) 消元、满秩期望；Grover 未知 M；Shor 模乘、连分数与三类失败；模拟误差、qDRIFT 平均信道；HHL 后选择；QAE 混叠；复杂度类与 local Hamiltonian | Simon 只给平均次数，缺固定失败预算；补满秩乘积概率及并合上界，题答和枚举同步 | 非零 s 承诺保持；有限样本保证以 i.i.d. 为前提；不改算法复杂度类别 |
| 08 | VQE 原理/测量分配、QAOA 单边/三顶点细算、梯度/参数偏移、QML 装载摊销与核集中、QUBO/金融/化学预算、SQD、优势证据/缓解 | §2 说协方差影响却未给一组可算共测例；补 Bell 态 Z1±Z2 的协方差，统一总态制备预算、配对原始计数和分组方差 | 共测减少基设置不直接推出端到端优势；不把人为计数称实测；重新访问 2026 三篇预印本记录版本 |
| 13 | 熵、负条件熵/互信息、纯态纠缠率、相对熵/DPI、Helstrom 不等先验、USD、根保真度、Holevo 可访问信息间隙、无广播、熵不等式、滤波后选择 | §11 强次可加性只给公式表；补条件互信息定义，经典 Markov 链和 XOR 对照并逐项求边缘熵 | 使用 S 量子熵、H 经典熵；零条件 MI 不等于无条件独立；不声称经典例证明量子 SSA |
| 16 | 查询下界、HSP、MNRS/element distinctness 查询模型、LCU、block encoding、QSP/QSVT、精度/容错资源、阴影/DFE/能量证书/委托验证、后选择放大误差 | **P1 缺条件**：任意 Hermitian 左上块并不保证简单 RU 有 arccos 相位。重写 §5.4，明确 Hermitian involution 信号酉、二维不变子空间、通用编码的厄米化及反例 | 与 §5.5 非 Hermitian 奇异值区别保持；不把数学二维例当完整合成器；标明编码调用及 U†/受控成本 |
| 17 | 门/MBQC 前馈、绝热路径与谱隙、退火 TTS 两层概率、echo、模型证据、密码查询/门口径、链强度 | echo 理想等时条件有文字无预算；补 t1≠t2 的精确残余耦合、态概率与谱范数误差，区分瞬时脉冲与真实控制 | 与 14 编译控制对应但不重复硬件脉冲推导；J 为角频率，JΔt 无量纲 |
| 18 | 纯化/Uhlmann、Choi CP/TP/转置、Stein/单副本检验、容量正则化/擦除完整证明、混态纠缠/PPT、QCMA/QMA/QIP、相位指纹、CV/压缩/能量约束、短擦除码 | CV 协方差定义后未判断物理性；补 V+iΩ/2≽0、单模行列式及相关项、无效正矩阵反例、正规 Gaussian 软件约定 | 区别经典 covariance 正性与 quantum uncertainty；不从非 Gaussian 一二阶矩恢复整个态；与 Q4 hbar 统一 |
| Q4 | 位置波函数/单位/定义域、硬壁能谱、叠加密度、谐振子代数/零点能、半无限衰减/有限势垒边界流、Fock 截断 | 势垒仅 0<E<V0，缺顶点 E=V0 与 E>V0；补线性内部解、连续极限、超势垒反射/共振，保存科学图和生成器 | 固定质量、同外侧势、平稳散射前提不变；不称实际器件模型；网格/Fock 截断不混写 |

## 一手核查与证据记录

真实浏览日期均为 2026-10-13。主要链接：

- IBM [经典计算与反计算](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/quantum-algorithmic-foundations/simulating-classical-computations)；[Simon 教程](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/quantum-query-algorithms/simon-algorithm)。教学定义与后处理，非生产优势。
- Crawford 等 [Pauli 有限采样测量优化](https://arxiv.org/abs/1908.06942)（2019 预印本、2021 Quantum 期刊版）；覆盖方差/分组，不用“组数少”代替测量成本。
- Watrous [TQI 作者手稿](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf)（2018），第 5 章、定理 5.36 的 SSA。教材熵定义与判据。
- Low–Chuang [Qubitization 期刊版](https://quantum-journal.org/papers/q-2019-07-12-163/)（2019-07-12）、[v3 全文](https://arxiv.org/html/1610.06546v3)，第 4 节/Lemma 8/10 与 Theorem 2 的信号条件和厄米化；本轮反例另由矩阵乘法独立证明。
- Weedbrook 等 [Gaussian Quantum Information](https://arxiv.org/html/1110.3234v1)（2011 预印本、RMP 2012），采用 [q,p]=2i，要换算到本书 [q,p]=i。正文的 V+iΩ 不直接抄入本书。
- [MIT 8.04 2013 Problem Set 7 Solution](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2013/40efdf7cc15a643eeade11c4178e5cf7_MIT8_04S13_ps7_sol.pdf)，式 32–34、PDF 页 6–7 的势垒顶极限与两侧统一式。
- [Qualtran 信号 walk 源码](https://github.com/quantumlib/Qualtran/blob/main/qualtran/bloqs/qubitization/qubitization_walk_operator.py)；[The Walrus Gaussian checks](https://github.com/XanaduAI/thewalrus/blob/master/thewalrus/quantum/gaussian_checks.py)。官方可检查软件，不代表已复现大型计算。固定提交/许可交主 agent 存档。
- 原章三篇 2026 预印本已重新访问：2607.24937 v1（7月27日）、2607.25941 v3（9月2日）、2607.25998。摘要支持原章的特定任务与证据限制，未见新增期刊出版记录；不据此断言其他渠道绝无后续出版。

检索异常：2111.05176v3 的 experimental HTML 返回无关 specimen 文本，未用于技术结论；不把它的内容当成 VQE 正文。其它错误入口未纳入引用。理论计算仍以定义/原始论文和独立小反例为准。

## 实施与验收规划

新增题目就地编号 A71-06、07、08、13、16、17、18、Q4，各含分步答案；不变更附录原题编号。代码 `codes/algorithms/round71_checks.py` 固定输入、标准库、独立解析式/矩阵与枚举对比；结果另存 round71-results.json，不改旧结果。图只为 Q4 连续极限与共振关系生成，并保留生成器。主 agent 统一构建 reader、附录入口、完整运行及提交推送；本组不单独 commit。

未承诺：所有量子算法/工业生产部署穷尽；所有第三方源码实际运行；全部书页逐屏人工验证；连续 QSP 合成最坏误差证明；真实退火/量子化学/硬件实验。
