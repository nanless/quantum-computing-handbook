# Round 70 基础篇逐章读审与诊断实验

日期：2026-09-26。执行者：foundations 子 agent。工作仓库：`quantum-computing-handbook`。读过仓库 `AGENTS.md`、`handbook/STYLE.md`，初始 `git status --short` 为空；未修改上层同步材料、共享附录、构建工具或阅读版，未提交。

## 实际阅读范围

完整阅读 Markdown 原稿：00（187 行）、01（825）、02（511）、03（521）、04（389）、05（447）、13（607）、Q1（534）、Q2（653）、Q3（528）、Q4（424）、QM README（39），合计 12 篇 5665 行，行数为编辑前版本。对早期合并读取出现的截断，另按区段补读。完整阅读 `codes/foundations/README.md`；对旧代码阅读矩阵助手及运行接口，未声称逐行审计整个旧脚本。

主 agent 后续要求的共享答案已全文读审：`handbook/appendices/exercises.md` 的第 0–5 章（第 5–235 行）、第 13 章（438–465）、Q1–Q4（1109–1606），行号为此次读取版本。对照原章自检的题目参数、基序与结果，未发现本轮必须修改的题答错位；新增诊断题有就地详解，不插入原编号，因此无同步改号建议。原有 Q2 第 6 题给正的 25 MHz，答案使用 Ω 而非 |Ω| 是在其参数条件下成立的，勿为形式统一而误报错误。

这是一轮原稿逐篇阅读、重点推导复算与代码运行；不是所有引用全文阅读，不是每张阅读版页面的人工验收，更不是全书正确性保证。

## 逐章发现与实质修改

| 文件 | 本轮发现的解释/实验缺口 | 修改及对应诊断 |
|---|---|---|
| 00 | 已提独立性，但没量化重复日志的错误置信感 | 10 个独立块各复制 100 次；穷举 1024 历史，标准差相差 10 倍 |
| 01 | 已证明酉性保持长度，但缺“基态都通过仍不够”的反例 | 两列相同矩阵；基态长度正常，叠加态输出长度平方 2/0，区分振幅相加与复位分支相加 |
| 02 | 已有 Bloch 定义，缺有限数据拼出非物理态的现实诊断 | X/Y 各 9/1、Z 5/5 的 30 次合成计数；负本征值、欧氏投影与似然/置信证据边界；新增公式生成 SVG |
| 03 | 已有实符号见证漏检，缺复相位的轴旋转例子 | (00+i11)/√2 的 ZZ=1、XX=0、XY=1；证明 ZZ+XY 可分界，不混淆选轴与无纠缠 |
| 04 | 提到受控分支相位，但缺完整可验证编译反例 | C(I) 与 C(-I) 四维矩阵、H 读出；一般相位因子怎样转成控制相位门 |
| 05 | 零温阻尼与热态边界已有文字，缺有限温度完整映射 | 四个 Kraus 的广义振幅阻尼，完备性、布居更新、固定点、γ=0 边界；核查上游接口文字冲突 |
| 13 | 先验与判别已有完整材料，缺后选时定理为何不能直接套用 | 同一工具成功/失败标记；0.8→条件0.936329、全部标记0.706476；后选先验25/98；显式加权矩阵。另修“下表”误指上表 |
| Q1 | 等权模型边界写明但无不等权定量反例 | 推导 V=2√p(1-p)|γ|，同可见度0.6对应纯度1或0.68；避免由可见度唯一反推退相干 |
| Q2 | 简并谱已有文字，未展示 Lüders 与细分后遗忘的区别 | 三维 diag(0,0,1) 工具，两者同 POVM 后态不同；原文条件后态明确限定 Lüders 工具 |
| Q3 | Rabi 失谐有正向预测，缺逆向参数不可辨识性 | ±6 MHz 全时域布居相同；独立声明 Ramsey δZ/2 与 ZE 符号换算，再用 Y 读出符号 |
| Q4 | 网格离散已讲，Fock 截断未讲对易边界 | [a,a†]=I-d|d−1><d−1|，四维及最高层3%例子；追踪无限维与有限矩阵区别 |
| QM README | 学习路径及边界与上述增补兼容 | 阅读但不改；新增题均在所属章可发现 |

所有新增内容均置于“新增诊断练习”节，题目、分步答案、限制、代码链接就地出现；保留原自检编号与原 11 章实验册，不以堆叠同义解释扩充。新增小节不宣称完整囊括对应主题的全部实验或算法。

## 外部资料与证据分级

所有访问日期为 2026-09-26。只把原始研究、作者教材、项目官方文档用于技术依据；搜索结果中的百科、论坛未用作结论来源。

| 一手来源 | 日期/版本 | 核查到的内容与证据类型 | 使用边界 |
|---|---|---|---|
| [Qiskit Experiments 状态层析](https://qiskit-community.github.io/qiskit-experiments/manuals/verification/state_tomography) | 页面显示 0.14.2；无独立发布日期 | 官方软件行为文档：线性反演、raw_eigvals、PSD修正与可选受约束拟合 | 未安装运行该版本；自编径向投影不声称复现所有 fitter |
| [Smolin/Gambetta/Smith, Maximum Likelihood, Minimum Effort](https://arxiv.org/abs/1106.5458) | 2011 首版 | 作者论文入口及摘要；作为层析修正研究线索 | 未全文审计，此轮未据其标题把任何投影都叫二项最大似然 |
| [Qiskit Aer amplitude_damping_error](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.amplitude_damping_error.html) | 0.17.1，页面更新 2025-06-04 | 官方软件文档，读取四 Kraus、固定点、参数文字 | 参数表把 excited_state_population 写为 |0> 占据，与同页公式矛盾；记录冲突并按矩阵和固定点定义 r=|1>占据 |
| [IBM 噪声模型指南](https://quantum.cloud.ibm.com/docs/en/guides/build-noise-models) | 动态页面 | 官方工程接口：thermal relaxation 含 T1/T2/t/激发热占据 | 说明建模接口，不证明任何实机满足该模型 |
| [Khatri/Sharma/Wilde, generalized amplitude damping](https://arxiv.org/abs/1903.07747) | 2019 首版 | 作者原始研究入口与摘要，广义阻尼的量子信息研究 | 未用该摘要主张应用优势或最新容量结果 |
| [QuTiP 状态与算符](https://qutip.readthedocs.io/en/stable/guide/guide-states.html) | stable 页面显示 5.3 | 官方文档：destroy(5) 的5维矩阵与归一化 | 截断对易式由本轮独立推导，未执行 QuTiP |
| [Qiskit ControlledGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.ControlledGate) | latest动态文档 | 官方受控门对象和定义入口 | C(I)/C(-I)结论由本轮矩阵直接推导，不依赖某次编译实测 |
| [Englert, Fringe Visibility and Which-Way Information](https://doi.org/10.1103/PhysRevLett.77.2154) | 1996-09-09 | 同行评审原始论文元数据与摘要，路径信息/可见度取舍 | 正文付费范围未突破；本轮不声称完整读过论文，新不等权公式由本章模型独立推导 |
| [Preskill 讲义第3章](https://www.preskill.caltech.edu/ph229/notes/chap3.pdf) | PDF未在本轮核实修订日期 | 作者官方测量/演化讲义，正交与一般测量框架 | 仅定位相关测量部分，不声称62页全文审读 |
| [Watrous TQI](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf) | 作者书稿；2018书籍 | 作者官方教材，仪器、判别与信道收缩定义 | 未声称598页全文阅读；后选数字是自编例子，非摘录教材习题 |

工业/工程迁移覆盖的是测量数据拟合、门语义验证、热噪声仿真、驱动标定和 Fock 截断检查。这些属于可复用工程方法与开源接口，不是生产量子优势证据。官方源码快照由主 agent 统一管理 `codes/vendor/`；本组新增代码全部独立编写，仅复用仓库已有自编矩阵助手，未拷贝第三方源码。

## 实际运行与产物

- `python3 codes/foundations/diagnostic_lab.py --case all --output codes/foundations/diagnostic-results.json`：11组通过，结果入库。参数全部固定、无随机种子；统计00用全枚举而非抽一批随机结果。
- `python3 codes/foundations/foundations_lab.py --case all --output /tmp/round70-foundations-original-results.json`：旧11组通过。旧种子20260926未变。
- 新诊断全量再次运行至 `/tmp/round70-foundations-diagnostic-results.json` 通过；不使用 `-O`，断言保留。
- `python3 codes/foundations/generate_diagnostic_figure.py`：生成 `handbook/assets/round70-foundations-tomography.svg`，坐标等比例、无量纲轴、原估计方形和修正圆形，颜色不是唯一编码。
- `git diff --check`：通过。
- 开发时两次实际失败已修复：默认Python3.9不支持 `int.bit_count`，改为 `bin(mask).count('1')`；Q4实值复类型不能直接JSON编码，检查后输出`.real`。没有隐瞒失败，也不以这些调试失败证明最终结果不成立。
- Quick Look 光栅化调用失败：`sandbox initialization failed: invalid data type of path filter; expected pattern, got boolean`。没有产生截图，也没有声称看过渲染图。已通知主 agent 在最终浏览器验收检查该图。

## 未完成与交叉复核建议

1. 主 agent 尚需重新构建阅读版、运行链接/题号/公式/数值检查，并实际查看新图及新增宽矩阵在桌面、窄屏的显示。原尺寸SVG不是实际视觉验收证明。
2. 本轮搜索不能代表“所有基础算法、所有工业使用、所有开源项目已穷尽”；上述具体来源/接口之外仍有大量范围未展开。
3. 请求另一 agent 优先复核：13章后选加权矩阵与全部标记迹距离、05章四 Kraus 与上游热占据参数、Q3两种 Z 约定的换算、Q4对易关系边界。数值程序与正文都在共享仓库。
4. 原附录对应题答暂无强制同步改动。若主 agent 希望提高可发现性，可在附录新增实验入口处增加“新增诊断练习答案就地给出”的导航，不要把新题硬插入原编号。
5. 不将自编小规模矩阵计算称作一般定理证明；章节中一般结论要么显式手推，要么明确转交标准定理。

## 补充读审与他人交叉核对

按主 agent 补充要求，全文阅读 `handbook/labs/foundations.md`，包含 F00–FQ4 十一组题答、索引与工程说明。未发现与新增诊断冲突：FQ1 明确等权边界，FQ2 的子系统统一能量平移与第04章受控分支相位是不同操作，F13 的不等先验与第13章后选更新先验一致。旧实验册无需改题号或公式。

algorithms 子 agent 已独立读完新增11节、诊断脚本与图生成逻辑，重跑全部案例；其100随机混态广义阻尼及组合核对最大误差2.22e-16，Fock维数2–12检查通过，后选择全部标记判别成功率0.853238低于原0.9。该复核未提出阻塞修订。case02的重构矩阵当前固定r_z=0，未来如扩展成任意计数接口必须补入r_z项；当前算例不是任意输入层析工具。
