# 第72轮：算法、信息与连续变量逐篇复读和完整SDK验证

日期2026-10-13，范围为06、07、08、13、16、17、18、Q4八篇Markdown原稿。先读仓库AGENTS与STYLE、round71计划/实施报告，再分段完整复读八篇（包括现有练习、误区和来源）、本组原题答案、算法实验册和既有round70/71代码说明。逐篇指Markdown文档，不冒充固定PDF逐页或全HTML逐屏人工审看。共享附录、AGENTS、vendor、构建器和最终提交由主agent整合。

## 逐篇结论与实质修订

| 篇 | 逐节复读范围与保留 | 本轮发现、修订、运行证据 | 仍未覆盖 |
|---|---|---|---|
|06|oracle/相位回踢、DJ/BV、振幅放大、QFT/QPE、模拟、垃圾位、成功率、查询下界及原自检逐项复读；原归一化/模型提醒保留|A72-06补显式可逆oracle、四位寄存器及完整Cirq门链，DJ常值/平衡、BV101输出全分布断言|任意真值表的廉价可扩展oracle综合没有实现|
|07|Simon样本/秩、Grover重试、Shor模乘/连分数、模拟/qDRIFT、HHL/QAE、复杂度类及原答案复读；旧解析演算保留|最明确缺口是HHL只有解析解没有全链电路。A72-07补非对角A、本征基、受控正相位U、两位QPE、倒数角、反计算、成功分支、Z/X读出、C缩小练习；Cirq真正20000×2 shots。另完整六位Simon oracle/边缘概率/64样本经典恢复|HHL一般稀疏输入、负谱、非网格、容错旋转和真机未实现；此组未重做大型Shor或QAE，主agent另集成|
|08|变分原理、测量/协方差、单边/路径QAOA、训练、QML装载/核、QUBO/金融、化学/SQD、优势/缓解逐项复读；原证据边界保留|A72-08补费米双轨道完整映射、粒子数块、全空间真空反例，OpenFermion真实映射与反对易核对；PennyLane100步参数偏移VQE真实优化|玩具跳跃模型没有真实分子积分；有限shot工业优化与强全尺寸化学基线未运行|
|13|经典/量子熵、联合/条件/纠缠熵、相对熵、Helstrom/USD、根保真度、Holevo、广播/SSA、后选择诊断及原题复读|A72-13补负谱阴影并非密度矩阵、纯度插件偏差1+1/N、独立快照U统计量及单批仍不物理反例；标准库二项式穷举与独立二快照均值核查|一般非线性熵置信界、SPAM/相关样本下无偏性没有证明|
|16|查询下界/HSP、coin/MNRS/element distinctness、LCU/encoding/qubitization、QSP/QSVT、预算/验证/阴影等全部复读，round71修过的信号条件保留|A72-16a任意加权小图CTQW接口与三路径解析；b实际pyqsp sym_qsp相位综合、Chebyshev/幂系数、虚部/完整矩阵元区别；c实际30000两位阴影、9倍权重和方差8、原始样本。quimb/pyqsp/PennyLane全部实际运行，独立重建；新增三联科学图|CTQW不是MNRS完整搜索；有限网格不是连续误差证书；本例未实现任意A的容错QSVT、通用陷阱或密码委托协议|
|17|门/MBQC、绝热谱隙、退火TTS/两层概率、数字-模拟echo、可信外推、密码资源、嵌入/链及原题复读|A72-17补dimod真实BQM→精确求解→Ising全配置等能；SDK s=2x−1与Pauli z=1−2x符号转换及常数偏移|经典ExactSolver不是退火动力学；未运行QPU、真实嵌入或工业TTS|
|18|纯化/Uhlmann、Choi CP/TP、Stein、四容量完整上下界、混态PPT、验证类、通信/指纹、CV物理性/压缩/有限码及原答复读|A72-18补真实Walrus covariance→Fock概率；压缩真空组合数、4层/20层漏质量、平均光子数、hbar默认拒绝和两模排序；清楚区别Gaussian描述与非Gaussian photon counting|有限一二阶矩不重构非Gaussian态；未大规模GBS、有限能量GKP或工业通信仿真|
|Q4|位置/微分方程/硬壁、定态叠加、升降谱/零点、隧穿/势垒各能区、二态近似、Fock边界诊断全部复读；旧顶点/共振推导保留|A72-Q4补相干态递推→Poisson→遗漏质量→归一化投影→根保真度与sqrt尾迹距离；d4/8/12详细表、无界N不适用简单2T界。标准库概率与振幅两路径|只比较已知无限态投影，未证明截断Hamiltonian动力学；网格误差与Fock截止仍分别核算|

不建议另增算法章：本轮缺口都能接回现有对象、先修与练习。数学工具的整体前置由主agent改阅读顺序；本组新增计算保持引用第01章数学和第13章根保真度，不改原编号或造成先修循环。

## 新文件与实际命令

- `codes/algorithms/sdk/round72_sdk.py`：8正式包真实对象/算法链，允许`all`或包名单项；`README.md`给完整依赖、运行范围、API和原始计数。`requirements-lock.txt`冻结全部依赖，`install.log`真实正常完整安装，`run.log`增强全任务输出。
- `round72-results.json`保存逐任务版本/CPU/墙钟/结果，`hhl-circuit.txt`保存实际四位电路，`pyqsp-solver.log`保存真正相位求解日志，`shadow-samples.npz`保存30000×2 bits/recipes及seed。全部本地理想模拟，非硬件实验。
- `python3 codes/algorithms/round72_checks.py all`：标准库13/Q4解析验证；可选`13`或`q4`。新结果`codes/algorithms/round72-results.json`，没有修改旧报告。
- `/tmp/quantum-round72-algorithms-sdk/bin/python codes/algorithms/sdk/round72_sdk.py all`：八任务增强重跑实际全部passed。
- `/tmp/quantum-round72-algorithms-sdk/bin/python -m pip check`：No broken requirements found。
- `/tmp/quantum-round72-algorithms-sdk/bin/python codes/algorithms/round72_figures.py`：重建三联公式图`handbook/assets/round72-algorithms.svg`、预览`work/rendered/round72-algorithms.png`。已用view_image实际看PNG，标题/轴/图例无遮挡，各类别线型/标记区分，不只靠颜色。手机与完整HTML由主agent集成验收。
- `git diff --check`实际通过。代码不请求账户、不下载数据、不运行vendor摘录。

## 实际版本与时长

本轮Python实际3.11.15、macOS arm64；初始口头版本3.11.11预判已被真实sys.version纠正。正式包与上轮vendor固定源码不自动同版本；没有刷新或自动执行vendor。增强重跑单项函数的秒数如下（含进入函数后的import/对象，受共享缓存影响，非性能排行榜）：

|包|版本|CPU秒|墙钟秒|
|---|---|---:|---:|
|Cirq|1.7.0|0.607|0.773|
|PennyLane|0.45.1|0.588|0.635|
|OpenFermion|1.8.1|0.013|0.013|
|Qualtran|0.7.0|0.237|0.237|
|pyqsp|0.2.0|0.015|0.015|
|quimb|1.15.0|0.014|0.014|
|The Walrus|0.22.0|0.165|0.166|
|dimod|0.12.22|0.043|0.043|

首次科学库import较慢；对Cirq -X importtime诊断表明正常导入约25.7秒，并非云调用卡死。正式安装成功，没有依赖冲突，没有以自编程序代替SDK来报告运行成功。开发期一次HHL独立残差断言误写因子2/√10，捕获后改为正确4/√10；实际电路态与成功率原本正确。MIT旧猜测URL404后改为实际可访问的lecture14官方页。所有修复后增强重跑通过，不把开发阶段发现倒记成零问题。

## 关键数值与证据边界

HHL p=.625、x=(.94868329805,.31622776602)、Z=.8、X=.6；Z批成功12461/20000、条件11252/1209；X批成功12488/20000、条件10022/2466。两个批次单独重新制备。Simon64次最终计数{'6': 12, '7': 18, '0': 16, '1': 18}（整数键对应000/001/110/111，增强重跑因加X批后随机序列改变），恢复110；固定种子结果不等于保证任何固定预算都满秩。

PennyLane阴影XX1.0128/YY−1.0158/ZZ.9912/ZI−.0019，匹配3376/3386/3304；方差解析8。VQE末能量−.728010988928，精确−√.53。OpenFermion一粒子最低(3−√2)/2=.792893218813；不限粒子真空0。Qualtran0…7模幂输出1/2/4/8/1/2/4/8，分解同值、完整Toffoli置换同矩阵。

pyqsp真正合成相位(.10328832343,.15851106437,.15851106437,.10328832343)，虚部目标.3T1+.2T3；1001网格独立误差1.8e−16、酉性8.9e−16；不能据此发连续认证。quimb三路径t=π/√2完美转移；五图完整概率见JSON，能量约−2.5e−16。Walrus20层质量.9999999999467017、漏5.3298e−11、光子数.1249999989214对.125。dimod四目标值0/−2/−3/−1与原题及Ising全部一致。

13纯度插件N6期望7/6，真值1；二快照独立积期望1。Q4 μ1: d4尾.01898816/T.13779752；d8尾1.0249197e−5/T.003201437；d12尾8.3161074e−10/T2.8837662e−5。有限截断态的平均光子数不是自动真值。

## 官方研究与工业实践覆盖

本轮实际浏览的主来源为Cirq官方入门/示例、PennyLane阴影API、OpenFermion官方教程、Qualtran模幂及tensor/classical simulation、pyqsp官方README、quimb Evolution、Walrus quick guide/physicality及dimod文档（均2026-10-13）。原理论接口HHL2009、Huang2020、Farhi–Gutmann1997/1998与MIT8.05相干态讲义均在正文和SDK说明给一手链接。pyqsp官方基/虚部规则用独立二维连乘确认；Walrus hbar/排序用物理矩阵反例确认。

工业整理对应的是实际研究接口：费米映射/粒子数、参数训练、随机测量数据复用、模算术和部件资源、QSP经典相位、图/张量演化、Gaussian数值、QUBO经典基线。未宣称生产部署或商业优势，也未宣称穷尽所有算法。源码可见、完整包可运行、具体小例正确和大型端到端优势四层证据保持区分；完整上游源码由原vendor与官方包入口保留许可来源，仓库交付自编调用和锁定依赖，不将包环境拷贝为不明许可源文件。

交换复核及共享整合待主agent协调；本组不commit。新增10组就地练习：A72-06、07、08、13、16a/16b/16c、17、18、Q4，旧251编号不改。附录/实验目录须链接这些新增标签及SDK入口。

## 交换复核闭环

基础复核者完整读本组八篇新增及SDK，独立用显式DFT重建HHL、重建QSP、读取全部30000阴影原样本、核查有限N的U统计，数学与固定结果通过。发现Q4把至59的有限尾和当无限尾时仍需可检查的剩余上界，作者同意由复核者补脚本/正文/JSON并实际重跑，剩余上界为4.4947884202e−83。具体闭环见 `round72-cross-foundations-algorithms.md`，复核代码 `codes/foundations/round72_cross_algorithms.py`；不能把这一发现写成零问题。
