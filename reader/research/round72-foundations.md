# Round 72 基础八篇：逐章再审与完整 SDK 实跑

日期2026-10-13。负责人为 foundations72_resume，接替因服务容量中断的前任；前任留下安装与初版验证脚本，但 `run.log` 为0、无运行进程，本报告不把前任安装视为算法通过。已读实际仓库AGENTS/STYLE，独占00–05/Q1/Q2、codes/foundations和独有图；未操作上层sources，未修改共享README/附录/vendor/构建/AGENTS，也未commit。

## 完整阅读与结构判断

八篇当前Markdown完整分段重读：00 223行、01 885、02 567、03 617、04 433、05 532、Q1 625、Q2 708，共4590行。完整读对应第0–5与Q1/Q2原自检答案，以及基础实验册238行。第一次合并输出01尾/02头出现截断，已另读01尾和02头；其他较长输出逐段控制返回量。读round71基础计划/完成报告，不重复上一轮主题。代码只审本轮完整验证器与新连接脚本，不冒充所有既有基础程序逐行审计。

八篇已有主线够承载这些断点，未增章。01在正文已前置，但侧栏曾先列Q1–Q4；导航由主审统一，本组只补01的矩阵指数数学桥接。保留原自检编号，F72题答均就地放到概念上下文。旧来源访问日期不刷新；新来源各自标2026-10-13。

## 00：全景

覆盖：§1–9、内存估算F71、随机记录诊断、原六题及实验册F00全文。
发现：稠密成本已清楚，但“存在稳定子表示”缺可运行的同任务对照，也容易把相同种子误当跨实现应逐格相等。
改动：§3.3后F72-00，在Bell电路推导理想分布，再给2048计数的标准差22.63与两方法实际计数，明确比较分布而非随机流。
来源：[AerSimulator](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html)，网页0.17.1，固定包0.17.2另实跑。
结果：statevector 1027/1021，stabilizer1008/1040，均只有00/11。
限制：仅Clifford两比特，无性能外推、真机或随机源认证。

## 01：数学工具

覆盖：§1–11、复数/内积证明/换基F71/张量积/概率/复杂度/原14题与F01完整读。
发现：02先引矩阵指数并用幂级数，01未预先解释“方阵指数非逐格指数”；这是学习顺序断点，非已发现原公式错误。
改动：§6末F72-01给矩阵幂级数与谱定义，e^(-iπX/4)两独立路径、错误逐格指数的列长平方2，前置于旋转及时间演化。
来源：[QuTiP主方程文档](https://qutip.readthedocs.io/en/v5.3.1/guide/dynamics/dynamics-master.html)的矩阵演化；推导本轮独立。
结果：SciPy expm、QuTiP Qobj.expm、Qiskit RXGate三上游矩阵与(I-iX)/sqrt2误差<1e-12。
限制：有限维可谱分解案例，不用指数加法省略不对易时序。

## 02：单比特

覆盖：§1–10、仪器与F71非投影分支、有限计数诊断、原11题与F02完整读。
发现：原层析诊断虽已解释球外估计，SDK仍停在文档入口；缺完整电路生成→运行→原计数→拟合→独立复算。
改动：§8后F72-02，真实X/Y/Z三组8192计数，差除分母、矩阵、谱与径向PSD公式，保留负原谱。
来源：[Experiments QST](https://qiskit-community.github.io/qiskit-experiments/manuals/verification/state_tomography.html)，0.14.2及固定安装源码 `_make_positive`。
结果：原Bloch=(.003662109375,.875244140625,.51611328125)，长度1.01608987586；负谱-.00804493793，PSD独立对照6.11e-16，精确目标差.00397029。
限制：两维径向等价不泛化高维；理想可信测量基，无SPAM校准。
修复闭环：首次验收脚本把raw与PSD用.003比较而失败，存initial-failure日志/JSON；修为同一PSD公式对照后完整重跑通过，不任意放宽容差。

## 03：多比特

覆盖：§1–10、Schmidt F71、见证/CHSH/单配性、诊断复相位、原11题与F03。
发现：原无信号讨论正确，但容易把远端边缘保持误读为联合纠缠完全保持；混态噪声之后已有纯态熵不能继续直接套。
改动：§6末F72-03，局部广义阻尼Bell的完整4×4矩阵、两侧偏迹、部分转置2×2谱，并由可分凸混合直接证明负谱的充分性。
来源：[Peres 1996](https://arxiv.org/abs/quant-ph/9604005)一手原论文入口、固定Aer。
结果：A=I/2，B=diag(.644,.356)，PPT最小谱-.31642834547，与独立公式一致。
限制：不声称任意维度PPT充分可分，也不以局部混态熵作纠缠量。

## 04：电路与协议

覆盖：§1–11、不可克隆/删除、传态与F71参考关联、超密编码/受控相位诊断、原9题/F04。
发现：已有每支手算正确，但上游真实动态反馈未执行；只有计算基验收会漏掉一条经典校正。
改动：§6末F72-04，从忽略m而保留n的公式推导(ρ+ZρZ)/2，输入复相干，计算基仍3/4/1/4但Y相干消失；软件c1c0映射明确。
来源：Aer官方接口，行为由固定包实际验证；一般传态恒等式沿已有正文逐支推导。
结果：完整校正六种输入各4096次误差<1e-11且四支出现。遗漏Z的8192次四计数2066/2094/2020/2012，样本相干残差.0010571599，与理想零相干区分。
限制：合成理想反馈，无真机通信、延迟或反馈门噪声复现。

## 05：信道

覆盖：§1–10、CPTP/系统环境/无信号证明/F71门序/广义阻尼诊断、原8题/F05。
发现：过程表征表缺完整上游过程层析实跑；“修为正且总迹正确”不能替代TP验收。
改动：§8末F72-05，四输入×三基12设置，显式未归一化J、输入输出顺序、广义阻尼四块、输出偏迹I；独立J*=2|00><00|反例。保留高shot拟合恰TP的事实，增加32-shot压力实际不TP结果。
来源：[ProcessTomography](https://qiskit-community.github.io/qiskit-experiments/stubs/qiskit_experiments.library.tomography.ProcessTomography.html)、[TomographyAnalysis](https://qiskit-community.github.io/qiskit-experiments/stubs/qiskit_experiments.library.tomography.TomographyAnalysis.html)，0.14.2；固定Aer源码也保留r参数文字错写0态的冲突。
结果：高shot每设置16384，Frobenius误差.02793801084，TP偏迹差1.11e-15；32shot正性修正后CP真、TP假，偏迹差.04658983839。完整Aer54例最大阻尼矩阵差1.33e-15，Choi谱/偏迹/KrausCP-TP均查。
限制：linear_inversion+事后PSD/trace修正不叫约束MLE；不宣称真实测量模型正确。

## Q1：实验与态

覆盖：§1–8、部分记录/F71擦除/不等权诊断、原7题/FQ1。
发现：已有“挡路是另一实验”的文字，但没有从入射分母到探测条件分母的完整数例与可执行失败标志。
改动：§2末F72-Q1，效率η0/η1与三结果概率，8000期望计数4000/1000/3000，s=5/8、条件4/5；单支Mdet与失败分支补齐完备性，真实合成SDK计数另列。
来源：现有一般工具定义与固定Aer本地扩充；推导不依赖第三方探测器主张。
结果：8192入射，4077/1013/3102，条件.80098231827、吞吐.621337890625，完整flag-port计数保存。
限制：无暗计数模型，失败两维标签是数学扩充，不把被吸收粒子说成可控；不认证探测器或Bell漏洞。

## Q2：可观测量与动力学

覆盖：§1–11、Robertson/Schrödinger F71/简并工具诊断、原8题/FQ2。
发现：封闭动力学完整，但开放模型仍只有另章公式/QuTiP入口；随机轨迹SD与平均SE需分开。一手官方stable指南把未定义errors写1/n，与独立均值标准误定义不一致。
改动：§9末F72-Q2，h=-ωZ/2、L显式外积、逐格推出b与c，us/rad-us/rate单位，mesolve/MC真运行、Bernoulli跃迁率与SE；文档冲突按5.3.1安装源码 `_create_e_data` 和 `_target_tolerance_end` 加独立统计核查，不暗自择一。
来源：[QuTiP MC指南](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-monte.html)、[固定版本主方程文档](https://qutip.readthedocs.io/en/v5.3.1/guide/dynamics/dynamics-master.html)、[源码入口](https://qutip.readthedocs.io/en/stable/_modules/qutip/solver/multitrajresult.html)。
结果：41时间点mesolve误差6.341e-11，4096 MC平均矩阵误差.003053538；965跃迁、观测.235595703125、解析.234797484344、SE.006623002826。std_expect与原runs总体SD独立核对，通过；标准误按sqrt(N)除。
限制：Markov零温模型/普通独立轨迹，回归六SE不是同时覆盖证明，不泛化加权采样；各时间点相关。
图：真实JSON生成 `round72-foundations-trajectories.svg/png`，已实际查看PNG，主/残差双面板、轴/单位/图例/误差线无遮挡；主审仍需网页宽窄屏核对。

## 本轮执行与交付边界

- `validate_sdks.py --case all`实际退出0、aer/tomography/qutip全通过；完整版本/锁/日志/输出在codes/foundations/sdk。初次失败保留。未执行vendor源码碎片。
- `round72_checks.py --case all`实际退出0、八篇通过；00/02/05/q2显式复用完整SDK JSON并记录其哈希，其余案例直接调用完整上游包。不是把保存结果冒充再次独立拟合。
- `generate_round72_figure.py`实际生成SVG/PNG，已看PNG。
- 原foundations_lab、diagnostic_lab、round71_checks全部实际回归退出0，结果存/tmp/round72-foundations-*，历史JSON未覆盖。
- 八篇共3212个公式片段KaTeX实渲染0错，marked无残留**，所有本地目标文件存在；保存 `round72-foundations-math-check.json`。未声称这一语法检验替代数学或网页视觉验收。
- `git diff --check`通过。主审最终构建reader、全书锚点/题号/宽窄屏/离线包/共享附录映射与add/commit/push；本组不作这些共享变更。

不声称全书算法/工业软件已穷尽；本报告仅八篇基础与上述固定包的本地完整路径。跨组独立复核另存报告，发现按实际修复记录追加。
