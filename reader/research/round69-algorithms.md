# 第 69 轮：算法、应用、计算模型与容量审查

审查日期：2026-09-26。实际编辑位置为 `quantum-computing-handbook/`；只读上层 AGENTS，按仓库新增 AGENTS 和 `handbook/STYLE.md` 核对。未修改上层同步源、共享附录、构建工具或提交 Git。

## 范围与方法

逐章分段完整阅读 06、07、08、16、17、18 原稿，共 4562 行，包括公式、表格、自检与参考文献；六章已有丰富算例，本轮避免重复重写，主要补“读完理论仍不会独立执行的步骤”。没有把本轮称为全部理论穷尽或全部页面人工验收。阅读版统一构建和浏览器截图验收由主 agent 完成。

## 逐章发现与实际改动

| 章 | 发现或解释断点 | 实际修改与代码映射 |
|---|---|---|
| 06 | 非网格 QPE 已有推导，但接近 1 的圆周误差尚缺可执行例；原文称 16 章有“完整证明”，实际只有框架 | 增 $63/64,t=4$ 输出 0 的 0.8112208 概率例；普通平均失败解释；15 次基本受控 U 的口径；修正完整证明承诺；实验 06 |
| 07 | 迭代数按成功峰选择，尚未区分有验证重试时的平均成本 | 增 $(k+1)/p_k$ 四策略表，揭示 k=2 平均查询优于 k=3；17 次重启覆盖 99% 的边界；逐振幅实验 07 |
| 08 | 正态近似 shot 规划容易被引用成严格保证；期望割值与最优串概率仍需完整数值；现代应用缺 SQD 入口 | 增加加权 Hoeffding 从每项区间宽度推导，14940 shots；选择偏差与独立最终验证样本；冗余参数例区分模型容量与训练；SQD 投影小例及工业成本；实验 08 给八项 QAOA 分布 |
| 16 | QSVT 非 Hermitian 边界只定性提醒；“完整下界证明”过度承诺；hybrid 文段将单轮 Cauchy 界放在“必须”后语义断裂 | 加 $A^2=0$ 而 $A^\dagger A\ne0$ 反例，奇偶/左右空间与实部块提取条件；补相位合成后逐层核验；修正证明承诺及段落关系；实验 16 |
| 17 | TTS 现有 0.2 当已知，虽提置信下界但未算完整统计预算；嵌入实践缺入口 | 加 20/100 校准的 95% 下界 0.0776127，后续 58 次、6.96 ms、校准额外 12 ms、两阶段失败并合≤0.06；补 minor embedding 和断链记录；实验 17 |
| 18 | 擦除可降解性已有定理引用，但如何真正构造降解映射未展示；数值优化与正则化容量证明边界易混 | 显式保留概率 ε/(1−ε)，反向映射；输出三元谱熵的 101 点核对；ε=.75 负相干信息与零容量区别；实验 18 |

新增 `handbook/labs/algorithms.md` 含六组主问题、详细答案、扩展题及运行映射；新增 `codes/algorithms/experiments.py`、README、expected-results.json、绘图程序。六组实验均为自行编写参考计算，不是完整量子SDK或生产求解器。

## 网络检索与原始证据

本轮实际使用网页检索/打开下列原始论文和官方文档；没有用二手新闻作为技术结论证据：

- Gilyén 等 QSVT 原论文：<https://arxiv.org/abs/1806.01838>。用于限定奇异值变换、访问假设和算法统一框架。
- PennyLane QSVT 电路接口：<https://docs.pennylane.ai/en/stable/code/api/pennylane.QSVT.html>，高层接口 <https://docs.pennylane.ai/en/stable/code/api/pennylane.qsvt.html>。核对 U/U† 交替、投影相位及某接口目标实部的约定。
- Hoeffding 原始论文 DOI：<https://doi.org/10.1080/01621459.1963.10500830>。新预算由其独立有界变量尾界逐步推导，不直接搬用正态近似。
- Sim 等参数化线路表达能力原论文：<https://arxiv.org/abs/1905.10876>。
- Caro 等泛化原论文：<https://www.nature.com/articles/s41467-022-32550-3>、<https://arxiv.org/abs/2111.05292>。正文只引用条件化研究方向，没有把摘要缩放律无条件套成数值保证。
- SQD 原始化学研究：<https://arxiv.org/abs/2405.05068>；IBM 氮分子官方教程：<https://quantum.cloud.ibm.com/docs/en/tutorials/sample-based-quantum-diagonalization>；官方包文档：<https://quantum.cloud.ibm.com/docs/en/addons/qiskit-addon-sqd>。区分新方法工作分配与端到端优势。
- D-Wave 嵌入：<https://docs.dwavequantum.com/en/latest/quantum_research/embedding_intro.html>，最佳实践 <https://docs.dwavequantum.com/en/latest/quantum_research/embedding_guidance.html>。用于工业复现需保留的参数和断链边界。
- Bennett 等纠缠辅助容量原论文：<https://arxiv.org/abs/quant-ph/0106052>。擦除容量定理沿用原稿 PRL 78,3217 原始引用，本轮新增的是显式降解构造与计算核对。

检索发现旧 `github.com/Qiskit/qiskit-algorithms` 页面返回404；已采用真实社区仓库 `qiskit-community/qiskit-algorithms`，避免继续传播过时路径。

## 开源存档及版本核对

网络沙箱未允许本子 agent 使用 Python 直接 API 下载；改用网页核查，提交哈希和源文件由主 agent 统一从上游取得。已读取 `codes/vendor/manifest.json` 和许可证原文核对本组相关项目，均为 Apache-2.0：

| 项目 | 固定 commit | 本轮实际保存的主要代码 |
|---|---|---|
| qiskit-algorithms | bcb7ded3594dac02e14acce7f59f05976916d39d | grover.py、iae.py、vqe.py、phase_estimation.py |
| pennylane | 45f1df84938b3bcbab9e20b284e90010d5f839aa | qaoa/cost.py、templates/subroutines/qsvt.py |
| qualtran | 8db02b8b3fb39d69d2900dcc7b52d9d6a36834c3 | arithmetic/addition.py、qft/qft_text_book.py |
| qiskit-addon-sqd | 99ef7544aac30280bcee76737b1faedce06d197f | configuration_recovery.py、fermion.py |
| dimod | 7eadc49df61fdf01848d882636b719548d30b142 | reference/samplers/exact_solver.py |

这些只是未修改源代码摘录，不是完整依赖环境。本组未安装或执行它们，不宣称复现了其真机、化学大规模或商业实验。manifest 记录原路径、完整 commit、URL、字节数与 SHA-256；教学代码 README 与 lab 页均链接该清单。

## 实际执行记录

- `python3 codes/algorithms/experiments.py all`：六组全断言通过；输出保存 expected-results.json。
- 重跑至 `/tmp/algorithm-results.json` 并与 expected-results.json 逐字比较：一致，退出码0。
- 初次开发 QAOA 最优概率解析常数有误，断言实际检出；在发布前通过全振幅概率修正为 $(11+6\sqrt3)/32$，之后六组通过。未把失败初稿写成成功验证。
- `generate_figure.py` 使用 matplotlib 3.9.4/NumPy 2.0.2 生成 SVG 和临时 PNG；已实际查看 PNG，双面板轴标、图例、标记形状、箭头均可读且无遮挡。截图不是手机阅读版验收，后者留主线。
- 绘图脚本固定 SVG hashsalt 并不写生成日期，便于复现。实际生成时有字体缓存不可写提示，但图形正常完成并已查看，不影响图像结果。
- 系统 agent 已独立检查六组与 MBQC 四维投影，详见 `round69-cross-systems-algorithms.md`，没有要求再修正的数学问题。

## 未完成/边界

没有声称逐个链接审完六章所有历史原始论文全文，也没有把原稿所有时效结论当作本轮重新验证。新增研究入口经过实际检索，新增数值全部有执行或推导证据。完整浏览器构建、全书练习编号、本地代码链接打包和最终提交推送由主 agent 验收。音频由主 agent 的统一教学音频工作流完成，本组未伪造硬件声音。
