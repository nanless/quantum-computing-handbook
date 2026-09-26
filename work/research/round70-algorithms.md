# Round 70：算法、应用、模型与容量逐章研究及修改

日期：2026-09-26。范围：06、07、08、16、17、18 章；本组教学代码和两幅独立命名科学图。不修改同步 sources、不操作共享附录、不执行云任务、不自行提交。

## 实际读审范围

已读仓库 AGENTS.md、handbook/STYLE.md。六章均完整阅读，长输出被截断处另以行范围补读：06 原 608 行；07 原 941 行；08 原 721 行；16 原 881 行；17 原 478 行；18 原 1119 行。没有把标题检索当作全文审读。

另全文读 exercises.md 中第 6、7、8、16、17、18 章现有题答，逐项对应各章自检题。未修改原自检编号，新题使用独立 06-B/07-B/08-B/16-B/17-B/18-B 编号，题目和解答就地成段，避免同一答案散落两个位置。本轮未发现原题答需随新 B 题重算的参数变更。

读审深度是完整 Markdown 源稿及关键推导，不是每一历史外链原论文都全文重读，也不是逐页纸质校样已人工验收。reader 构建、宽窄屏截图由主 agent 统一完成。

## 逐章发现与落地

| 章 | 缺口或问题 | 本轮修改 | 独立验算 |
|---|---|---|---|
| 06 | Hadamard 测试未展开；**原文错误称交换两个反射次序不改成功概率** | 从四维联合态推实/虚部测量，明确 S† 符号、受控 U 与联合失败预算；修正 DS_G 与 S_GD 次序，a=1/4 一轮分别 1 和 1/4 | 联合振幅与内积公式；二维反射直接计算 |
| 07 | “无 QFT”入口缺乏统计不可辨识反例 | 同一 k=1 对 a=1/4 与 1 都给概率 1；加入 k=0 计数消歧；似然端点和 400 次制备调用账 | 三倍角多项式与三角表达式；固定连续论证 + 网格复查 |
| 08 | 只说参数偏移，没有共享参数的适用条件 | 单门生成元与三角展开；两门共参错误导数 0 对正确 -sqrt(2)；方差预算；四类工业研究工作流证据表 | 旋转矩阵与链式求导；方差上界 |
| 16 | 块编码误差未连到后选择条件态误差 | 逐步证明 2 epsilon/sqrt(p) 范数界；概率区间；p=10^-4 的二维块例与根/平方保真度 | 归一化向量距离与概率/保真度 |
| 17 | 链强度取舍没有四状态阈值算例 | 精确四状态表；严格 J>2，J=2 简并边界；统一范围缩放示例及后选择样本口径 | 全四配置枚举与系数缩放 |
| 18 | 容量已定义，但缺实际短码可靠性例 | 经典重复码与 (3,2) 奇偶码；全码字/擦除模式、显式失败与量子不可复制边界 | 全消息×八掩码候选译码 + 二项式公式 |

所有新增实验说明输入、输出、适用条件、成本、成功/失败含义；不能由代码反推未证明的算法保证。段落按问题、推导、样例、边界、题、解拆开，公式与表格前后保留空行。

## 网络检索与一手证据

以下均实际打开或检索到官方/原作者来源，访问日 2026-09-26。只使用原始论文、官方代码和官方文档形成正文主张。

| 来源 | 年代/阶段 | 核验用途及边界 |
|---|---|---|
| https://arxiv.org/abs/quant-ph/0511096 及 https://arxiv.org/html/quant-ph/0511096v2 | 2005 预印本，STOC 2006；v2 更正与更新于 2006-04-10 | §2.2 完整说明 Hadamard 测试实部、虚部；本节不展开 Jones 算法 |
| https://arxiv.org/abs/1904.10246 | 2019 预印本，2020 期刊 | 最大似然式幅度估计组合不同 Grover 幂测量；不能只重复一个混叠深度 |
| https://qiskit-community.github.io/qiskit-algorithms/stubs/qiskit_algorithms.MaximumLikelihoodAmplitudeEstimation.html | 官方 0.4.0 文档入口 | 接口明确不需额外相位评估比特；软件入口不等于低噪深度保证 |
| https://arxiv.org/abs/1811.11184 | 2018 预印本，2019 期刊 | 参数偏移生成元条件，单门导数与经典链式法则需区分 |
| https://github.com/PennyLaneAI/pennylane/blob/main/pennylane/gradients/parameter_shift.py | 官方代码，动态 main | 参数偏移工程入口；固定版本摘录由 root 统一存档 |
| https://arxiv.org/abs/1806.01838 | 2018 预印本，STOC 2019 | QSVT 算法上下文；新后选择范数界为本节显式推导 |
| https://github.com/quantumlib/Qualtran 和 https://arxiv.org/abs/2409.04643 | 官方资源软件与 2024 论文 | 逻辑算法分解和资源模型，不能改写成实机工业性能 |
| https://qualtran.readthedocs.io/en/latest/bloqs/chemistry/resource_estimation.html | 官方教程 | 化学 QPE 资源分解、误差模型输入 |
| https://github.com/Qiskit/qiskit-addon-sqd | 官方研究软件 | 从量子样本到经典子空间；未声称生产部署或一般优势 |
| https://qiskit-community.github.io/qiskit-finance/tutorials/00_amplitude_estimation.html | 官方教程 | 金融概率估计接口；分布准备和经典基线仍需另外计 |
| https://docs.dwavequantum.com/en/latest/quantum_research/embedding_guidance.html | 官方工程文档 | 链强度过大/过小的取舍 |
| https://docs.dwavequantum.com/en/latest/quantum_research/basic_config.html | 官方工程文档 | 链强度与自动缩放；正文统一 [-1,1] 是教学模型，不冒充产品范围 |
| https://doi.org/10.1103/PhysRevLett.78.3217 | 1997 原始容量论文 | 擦除信道容量背景；有限码可靠性在正文自行枚举证明 |

对既有时效段落另外复核 https://arxiv.org/abs/2607.24937、https://arxiv.org/abs/2607.25941、https://arxiv.org/abs/2607.25998 以及 https://www.ibm.com/quantum/blog/quantum-advantage。来源存在且与第 08 章的特定任务、预印本、不能推广 VQE/QAOA 一般优势的表述一致，因此没有删除该段；没有把作者主张提升为普遍独立验证。

检索中的 GitHub qiskit-algorithms/mlae.py 页面一度 cache miss，改用官方接口文档；未伪称逐行读完那个源码文件。系统 Python 和捆绑 Python 都缺 matplotlib，随后用主 agent 已准备的隔离依赖 matplotlib 3.9.4、NumPy 2.0.2 成功生成图，不写本机临时路径到教程。

## 代码、固定样本与实际运行

- `codes/algorithms/round70_checks.py`：六组标准库程序；无随机数、无网络调用。
- `codes/algorithms/round70-results.json`：本轮实际全量输出。
- `codes/algorithms/round70_figures.py`：可选绘图；引用同一概率函数并由公式生成能量曲线。
- `codes/algorithms/README.md`：输入、命令、依赖、样本性质、断言及限制。
- 两张交付 SVG：`round70-amplitude-aliasing.svg`、`round70-chain-strength.svg`，均有生成程序和正文原尺寸链接。

实际运行 `python3 codes/algorithms/round70_checks.py all --write-results` 成功，所有断言通过；生成结果 JSON 禁止 NaN/Infinity。具体数值：

- 06：U=diag(1,i) 两组 p0=0.75；改 -i 时虚部组 p0=0.25；DS_G/SG_D 为 1 与 0.25。
- 07：指定计数的网格最大点 0.25，A/A† 调用 400，好态反射 100。
- 08：错误共同平移约 0，正确梯度 -1.414213562373095；单门标准差界 0.02236068 与 2.236068。
- 16：epsilon=0.001 时条件向量差 0.09962740376031952，界 0.2，平方保真度 100/101。
- 17：J=1 唯一最低态断链；J=2 三重简并含断链；J=3 两合法最低态；归一化场幅 2/3 与 1/4。
- 18：epsilon=1/4 的块失败率 1/64 与 5/32；epsilon=1/2 时为 1/8 与 1/2。

`git diff --check` 对本组六章和代码目录通过。绘图生成成功；已用图像工具打开两幅 PNG 检查标题、轴标、曲线和标注。第一稿幅度图图例遮住近原点数据，已移出绘图区后重新生成并再次打开。原尺寸图检查不能替代 reader 手机上真实显示检查，后者待主 agent 合并运行。

## 交叉复核

systems agent 完整读六章新增 B 段及 round70_checks.py，重新运行 all，并独立抽查 100 组复输入的 Hadamard 测试、100 个共享参数角度，最大概率误差 6.66e-16。数学未发现问题；其建议将 08-B 题目明确为“符合单门规则的两点估计器”已落实，避免被误读成四线路共享梯度总方差。

Grover 次序修正发生在该审查之后，已追加二维反射断言并通知 systems 再核对；若追加审查完成，以交叉报告为准。

## 给共享目录整合的精确建议

1. 现有附录六章题答均已读，无参数需同步改写。可在练习索引增加“各章实操扩展 B（就地含答案）”，不要把六段完整答案再复制一遍。
2. 新增代码与图须随离线 reader 打包；尤其第 08 章新增源码清单链接 `../codes/vendor/manifest.json` 要经过构建规则改写/验证。
3. root 已统一收集 PennyLane parameter_shift、Qualtran block_encoding/linear_combination 与 qubitization walk、pyqsp 等固定版本源码；本组不改 vendor manifest，避免并行冲突。建议在映射表把这些分别接到 08-B、16 章算法栈；MLAE 官方入口保留为入口，未下载则写明。
4. AGENTS.md 可补一条：参数共享与自动微分须按门生成元和链式法则核对；成功分支的范数误差须在归一化后重新分配预算。这是本组建议，不要求无限增加流程。

## 未完成及覆盖边界

没有宣称算法、工业部署或开源生态已穷尽。新覆盖为六个明确缺口；完整 MLAE 置信区间/噪声模型、一般 QSP 相位合成、动态退火、多体有限温度、长块码构造和真实化学基准不在本组代码实现范围。没有下载不明许可证材料，也没有执行第三方源或量子云 API。共享导航、题库索引、reader 自动构建/截图、全库许可/大文件检查、add/commit/push 均由主 agent 完成。

## 补充：原算法实验册完整检查

按主 agent 补充要求完整阅读 `handbook/labs/algorithms.md` 六组 A 实验、题解、图释及工业入口表。原实验均与新增 B 题兼容：A 组参数偏移已经限定单次 Pauli 旋转，B 组专门展示共享参数为什么不能沿用；A 组 Grover 顺序明确先标记再扩散，与本轮次序修复一致；A 组相干信息仅网格核查并把容量标为 theorem，B 组另算有限短码，没有改动原容量结论。原实验册无本轮必须修改的参数或断言，也未重复加入 B 组全文。建议 root 仅添加 B 组索引链接以便发现。
