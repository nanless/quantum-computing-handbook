# Round 71 基础八篇：修改与实际验证

日期：2026-10-13。读审规划见 [round71-foundations-plan.md](round71-foundations-plan.md)。本 agent 完整阅读分工八篇 Markdown 原稿、对应旧自检答案、基础实验册与历史报告；不把正文完整阅读说成每份外部文献全文阅读，也不把语法渲染说成人工逐屏验收。未改同步 sources、共享附录、构建工具、vendor 或提交。

## 架构结论

保留现有章节数。八篇已有主线足以承载新增内容，全部 F71 节直接置于对应主题中，保留旧自检和诊断编号。没有重复新增概率、Bell、CPTP或动力学章节。00仍为概览，01复基例明确学过矩阵后回看，04参考系统例明确进阶；Q1擦除紧接部分路径记录，Q2加强界紧接已有松界反例。

主篇矩阵维度、左因子高位、门右侧先执行、已知条件态与非选择态、根保真度原约定保持。新增局部记号C/W、m/n、p/γ均就地定义；Q2 Hamiltonian仍写花体H，Hadamard仍为H/H_Had。统一练习标签F71-*，每篇新题有答案与程序入口。

## 00：模拟内存

在§3.3后新增F71-00。逐个复振幅16byte→2^n态数组→4^n密度数组，20/30比特准确区分MiB/GiB/TiB/EiB；追加22比特倍率练习。代码使用整数计算，未巨量分配。说明该成本不含临时数组，只是稠密方法；稳定子/MPS入口不等于一切态都高效压缩，稠密模拟困难不等于实用优势。

无需修改既有oracle成本、NISQ含义、随机性、独立性与后量子密码解释。来源为Aer官方0.17.1 API，实际读取模拟方法与max_memory_mb段。

## 01：换基与主动门

在§3末新增F71-01。复Y本征基W、坐标W†ψ、同时变换测量W†ZW=X；同态Z均值1，两种表示一致。主动W†后仍测固定Z均值0；附Wᵀ误认Y方向的反例。新题说明共轭转置的必要，不把改坐标当改变历史制备。

无需修改复数四则、Cauchy–Schwarz、张量基顺序或原14题答案。Watrous数学预备为作者教材入口，公式在本轮独立逐格算出。

## 02：非投影仪器

在§7末新增F71-02，回到原有E0/E1实例，显式额外指定M_k=√E_k，完整分支长度、条件ket、非选择密度、纯度7/8、X正概率0.933013、重测0给5/8。明确平方根是选择的一种工具，非唯一测后态。

无需改已有层析有限样本诊断与原11题。独立标准库代码执行Kraus分支，检查完备性与正性。Preskill2015版测量讲义§3.1.2的sqrt POVM构造实际网页定位读取，未声称全文65页逐页阅读。

## 03：复Schmidt构造

在§5中插入F71-03：C=[[1,i],[0,1]]/√3，ρA=CC†、ρB=CᵀC*；准确区分C†C与B态坐标。用迹1、行列式1/9求两权重(3±√5)/6，再给A本征向量、B配对共轭、正交性和四格重构。熵0.550048bit，有就地练习答案。新增推导独立检验复振幅，不仅检验测量概率或本征值。

差异复审发现最初标题“四项态”易误解为四项非零，已改“含复系数的态”；配对向量的内积表达补上复共轭，公式与代码一致。原纠缠见证/CHSH前提、单配性、11题答案无需修改。Watrous原书第31页Schmidt/SVD相关段已定位读取。

## 04：参考系统传态

把§6最后“留到以后”一句接成进阶F71-04：RQAB基序，16复振幅，m/n对应Q/A结果；全部四分支各1/4，Bob Z^mX^n校正使RB回到Bell。未获记录时RB=I4/4。对比测量重制备保持同样局部I/2和ZZ却使XX=0，揭露仅测边缘概率的验收不足。

代码另检验复不等权纠缠与乘积RQ输入，未拿三个输入冒充一般定理证明。原传态符号、11校正顺序、不可删除条件、超密编码答案保持。IBM官方传态课程“reference system”部分已读取，其一般结论与本书自算基序区分。

## 05：顺序与无信号

§4新增一般局域CPTP无信号证明，用联合迹循环与Kraus完备对所有Alice POVM元素证明约化态保持，明确选择单支不保迹、经典标签可改变条件描述。接上03原先留下的证明接口。

§5末新增F71-05：随机X翻转p=1/4与零温阻尼γ=.36交换次序给激发.16/.25，任意复输入差pγZ；说明本组的相干项恰可交换而布居不交换，不把§6可交换那对模型推广。移植Qiskit组合方法时使用最小反例验证顺序。

原广义阻尼四Kraus与上游文档冲突保留历史核查日期，未把旧日期刷新成新审查。Qiskit最新Kraus API的compose/dot/front段本轮实际读取；第三方源码由主agent固定提交收录。

## Q1：条件擦除条纹

§2.3末新增F71-Q1：路径P、记录D的正交记录联合态，D的±基展开、各支1/2、条件(1±cosφ)/2、四个联合概率、边缘恒1/2。φ0的400输入期望四格200/0/0/200，φπ/3的条件3/4与1/4，明确期待计数与实际频率差别。

新增公式生成SVG与129点生成程序，三条曲线使用实/虚/点线及方形/圆形，标rad/无量纲。图为理想公式，不是实测。模型要求能访问记录相干性，不能把删日志、环境不可控、超光速或逆因果混入结论。Scully/Drühl 1982原始论文页面与Preskill旧版量子擦除相关段实际读取，但未读取付费完整论文。

## Q2：对称协方差

§4.2后新增F71-Q2：保留原z的实部，定义对称协方差和单位，推到Schrödinger平方不等式。原π/8实态Cov=-1/2，方差乘积1/4，完整下界1/4；准确区分标准差乘积1/2。说明不对易量不能从两个顺序读数的未扰动乘积估计协方差；另列斜轴C/D校验。

原Robertson关系没有错误，本轮是补更紧界，动力学、时间顺序和单位原题答案不改。Schrödinger原文1930、英译v3为2008-05-23；实际打开PDF定位协方差与公式，没有把译注日期当原论文日期。

## 一手来源与工程边界

全部本轮访问日期为2026-10-13：

1. [AerSimulator](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html)：页面标0.17.1，软件接口证据。
2. [Watrous数学预备](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)：作者教材，定位Schmidt/SVD段；只链接，不再分发。
3. [Preskill测量讲义](https://www.preskill.caltech.edu/ph219/chap3_15.pdf)：作者讲义，定位POVM平方根段。
4. [IBM传态](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/quantum-teleportation)：官方课程，定位参考系统一般论证。
5. [Qiskit Kraus](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Kraus)：latest动态API，定位compose/dot/front，未声称固定版本调用已执行。
6. [Qiskit Experiments ProcessTomography](https://qiskit-community.github.io/qiskit-experiments/stubs/qiskit_experiments.library.tomography.ProcessTomography.html)：0.14.2官方页面，默认4^n3^n设置与条件经典位；工程说明加入代码README，未安装拟合器。
7. [Scully/Drühl](https://doi.org/10.1103/PhysRevA.25.2208)：1982原始研究页面/摘要，完整文受访问限制。
8. [Schrödinger英译](https://arxiv.org/abs/quant-ph/9903100)：PDF v3 2008，原文1930，原始论证译文及注释。

不宣称所有基础算法、工业使用、开源代码已穷尽。已核验范围是上述接口、定义及本书新增自编例子；实机校准、生产验证、上游拟合器执行与大规模资源预测不在这八组程序覆盖中。

## 实际执行与结果

- `python3 codes/foundations/round71_checks.py --case all --output codes/foundations/round71-results.json`：八组全部通过，实际结果存档；调整本征方程断言后重新执行通过。
- 八个编号各自独立命令实际运行通过，不依赖前一案例状态。
- `foundations_lab.py --case all` 与 `diagnostic_lab.py --case all`：原两套各11组回归通过，结果存/tmp/round71-foundations-original.json和diagnostic.json，未覆盖原历史证据。
- `generate_round71_eraser.py`实际执行生成SVG；Python系统缺cairosvg，未安装，未声称已经得到PNG或人工查看渲染截图。
- 使用仓库KaTeX 0.16.22对八篇3043个公式片段实际renderToString，错误0；报告 `round71-foundations-math-check.json`。这是公式语法验证，不是数学正确性或视觉完美证明。
- `git diff --check`通过。复审发现一次字符串转义产生控制字符，已修正并检查八篇全部无非换行/制表控制字符。

主agent需最终构建阅读版、检查全部链接锚点与宽窄屏，并实际查看新图和长推导；本组不执行或改写共享构建。跨组复核另存独立报告。AGENTS已有逐章读审、证据分级、分支检查、版权与逐页验收规则足够，建议主agent只追加新轮产物入口/验收范围，不为格式偏好反复扩写同一规范。

## 后续独立复核反馈

algorithms组完整阅读本组八篇4574行并独立复算复Schmidt、参考系统传态、信道顺序、擦除和协方差，未提出尚未解决的数学错误。其代码建议已落实：round71主入口检测`__debug__`，`python3 -O`实际以错误码2拒绝运行；00的22/20倍率4/16加入计算、断言和保存结果，重新运行八组通过。对应独立报告由作者保存为 `round71-cross-algorithms-foundations.md`。

本组对systems八篇与软件实践新增§11–16的独立复核另见 [round71-cross-foundations-systems.md](round71-cross-foundations-systems.md)。这些复核记录不替代主agent阅读版视觉验收。

## 手机实际截图发现的强调标记修复

主agent在手机实际截图中发现01的F71开头“只改写坐标时…”与Q1的F71开头“在能保持记录相干…”两段原样显示`**`。原因是粗体内句末标点后，闭标记紧接中文，CommonMark未识别强调。两处已拆为介绍、独立强调句、下一说明三个段落；没有改数学或实验条件。

进一步用仓库marked实际解析这两篇全文，排除代码块后查HTML中的残留`**`，还发现Q1既有§2.2“关键不是实验者眼睛有没有看记录…”同类问题。它也改为独立段落，文字保持原样。再次解析两篇，残留数均为0；`git diff --check`通过。主agent负责重建阅读版并重拍实际页面，本组只记录原截图反馈及源稿修复，没有把静态解析检查冒充重新截图。
