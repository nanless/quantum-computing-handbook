# 第六轮扩展研究：硬件、控制、编译、实验与 2025—2026 进展缺口审计

> 审计截止日：2026-09-22（Asia/Shanghai）  
> 审读范围：`handbook/00-overview.md` 至 `handbook/12-security-network-frontiers.md` 的当前文本，重点复核 09、10、11、12 章与全书中“抽象线路怎样落到实验系统”的接口。  
> 资料原则：优先同行评审论文、RFC/ISO 等标准组织资料和开放语言规范；厂商文档只用于说明其接口与可复现字段，不用于证明平台优越性。  
> 本轮约束：只做缺口审计，不修改正文，也不修改 `sources/`。

## 0. 结论先行

当前教材已经把量子态、线路、算法、纠错、六条硬件路线、主要基准和前沿证据边界讲清楚了。最明显的剩余缺口不是再增加一种量子比特，而是缺少一条连续的工程主线：

```text
目标酉操作
  → 控制 Hamiltonian 与旋转坐标系
  → 可生成、可采样的脉冲/激光/电压波形
  → 校准、状态判别与表征
  → 目标机编译、布局、路由与调度
  → 中途测量、复位、反馈和译码
  → 封装、制冷、光学、电子学与运维
  → 可复现的云端实验记录
```

09 章现有系统栈图已经给出这些名词，但没有解释它们怎样互相约束。11 章能判断指标是否公平，却尚不能指导读者把“单门指标”连接到“持续运行的系统指标”。12 章已经有网络物理和性能指标，但缺少“应用请求如何经过链路层、交换、经典控制再交付 Bell 对”的协议栈。建议新增一个“系统实现”主节，另用 10、11、12 章的小型交叉框补足译码、运维、网络与复现。

本轮没有发现需要立即更正的基础物理 P0 错误；发现 **36 项可执行改进**，其中 P1 27 项、P2 9 项。另有 6 项时敏结论需要建立定期复核机制。

### 优先级约定

- **P1**：缺失会让初学者形成错误的系统直觉，或使研究生无法据此读懂实验/架构论文。
- **P2**：内容方向正确但工程深度不足；加入后能显著提升完整性和研究入口价值。
- **易变性**：低＝物理原理稳定；中＝接口或工程最佳实践会演进；高＝纪录、产品、标准项目状态和厂商接口会变化。

---

## 1. Hamiltonian 到脉冲：当前最重要的断层

### 1.1 [P1，低] 增加“从目标门到实验波形”的四层推导

**现状与风险**：02 章定义旋转门，09 章说“微波脉冲/激光/电压做门”，中间没有桥梁。学生容易把 `RX(θ)` 当成硬件固有按钮。

**可执行改进**：在 09 章系统栈后增加一个统一模型：

\[
H(t)=H_0+\sum_k u_k(t)H_k,
\qquad
U(T)=\mathcal T\exp\!\left[-\frac{i}{\hbar}\int_0^T H(t)\,dt\right].
\]

随后用受驱动两能级系统说明：实验室坐标系中的载波乘包络，经旋转坐标系与旋波近似后，包络的两个正交分量决定 Bloch 球赤道上的旋转轴；脉冲面积决定旋转角。明确四层不是一一等价的：目标酉矩阵、有效 Hamiltonian、控制波形、DAC/AWG 输出到器件后的实际波形。

**新增图**：图 A“门到波形的翻译链”，同时画出软件门、旋转坐标系、I/Q 包络、数模转换、混频/光调制、传输线或光路、量子比特。

**权威入口**：[OpenQASM 脉冲层说明](https://openqasm.com/language/pulses.html)；[OpenPulse 3.1 规范](https://openqasm.com/versions/3.1/language/openpulse.html)。规范明确把 `defcal` 绑定到具体物理量子比特，并用 port、frame、waveform、play、capture 表示硬件控制；OpenPulse 仍在积极开发，语法不是所有平台的统一物理模型。

### 1.2 [P1，低] 增加 Rabi 标定手算，解释幅度、时长、失谐各自做什么

**可执行改进**：给出旋转坐标系中的最小 Hamiltonian

\[
H_{\rm rot}=\frac{\hbar}{2}\left(\Delta Z+\Omega_x X+\Omega_y Y\right).
\]

先令 \(\Delta=0,\Omega_y=0\)，推得矩形脉冲满足 \(\theta=\Omega_x T\)；再取 \(\Omega_x/2\pi=10\,\mathrm{MHz}\)，算出 \(X_\pi\) 理想时长 50 ns、\(X_{\pi/2}\) 为 25 ns。最后让 \(\Delta\ne0\)，说明旋转轴倾斜且角速度变为 \(\sqrt{\Omega_x^2+\Delta^2}\)，这同时造成角度和轴误差。必须注明真实系统会用成形脉冲、有限带宽和多能级模型，矩形脉冲只用于建立直觉。

**新增例题**：根据一次 Rabi 扫描找到 \(\pi\) 脉冲，再用 Ramsey 扫描找失谐；让学生说明只校准幅度为何不能消除频率漂移。

### 1.3 [P1，低] 用 DRAG 说明“更快”与“更少泄漏”的权衡

**现状与风险**：09 章已正确指出 transmon 的 \(|2\rangle\) 泄漏，但没有展示波形工程怎样抑制它。

**可执行改进**：介绍弱非谐振荡器中短脉冲频谱更宽，容易驱动 \(|1\rangle\leftrightarrow|2\rangle\)。说明 DRAG 在正交通道加入与主包络导数成比例的分量，并配合失谐修正；不要把它写成“万能消泄漏”，参数仍须按器件校准，也不能消除所有两比特门或串扰泄漏。

**权威来源**：F. Motzoi et al., [Simple Pulses for Elimination of Leakage in Weakly Nonlinear Qubits](https://doi.org/10.1103/PhysRevLett.103.110501), *PRL* 103, 110501 (2009)。

### 1.4 [P2，中] 区分开环最优控制、闭环标定和 Hamiltonian 学习

**可执行改进**：加入一个三列表：

| 方法 | 输入与目标 | 不能自动保证 |
|---|---|---|
| 模型驱动最优控制 | 已知/拟合 Hamiltonian、带宽与约束，搜索波形 | 模型外漂移和串扰下仍最优 |
| 闭环实验标定 | 反复执行实验，以测得代价更新幅度、频率、相位 | 找到物理可解释的噪声来源 |
| Hamiltonian/噪声谱学习 | 从时域或频域数据估计模型参数 | 直接给出大规模最佳编译 |

这能避免把“机器学习校准”“脉冲优化”“系统辨识”混成同一件事。

---

## 2. 校准、层析与验证：把“调好”与“测好”分开

### 2.1 [P1，低] 增加校准依赖图和最小闭环

**现状与风险**：09 章把校准数据库画在系统旁边，却没有说明校准存在依赖顺序和回归测试。

**可执行改进**：新增图 B“校准依赖 DAG”：

```text
时钟/线性响应/电延迟
   → 比特与读出频率
   → 读出幅度、积分核、判别阈值
   → 单比特幅度与相位
   → 两比特门参数
   → 同时门、串扰、泄漏
   → 层级基准与应用回归
                ↺ 漂移触发局部或全局重标定
```

强调某一层改变可能使下游参数失效；校准不是每天生成一张“真值表”，而是带时间戳、不确定度和依赖关系的系统状态。

**规范证据**：[OpenQASM calibrations in practice](https://openqasm.com/language/pulses.html#calibrations-in-practice) 明确说明校准随时间变化、按目标系统唯一，并常由周期性自动程序从旧标定自举。

### 2.2 [P1，低] 明确 calibration、characterization、verification、benchmarking 的不同目的

**可执行改进**：在 11 章元件指标表前增加定义框：

- 校准：改变控制参数，让操作更接近目标。
- 表征：估计某个模型或过程参数，帮助解释误差。
- 验证：检验实现是否满足预先规定的性质或误差界。
- 基准：用约定工作负载比较能力、吞吐或质量。

同一 RB 数据可用于调参，但 RB 的平均衰减率并不等于完整噪声模型，也不自动给出最坏情形阈值保证。

### 2.3 [P1，低] 增加 RB、同步 RB、循环/层基准、GST、过程层析的选择树

**现状与风险**：11 章已有方法表，但缺少“遇到什么问题该用什么”的操作性。

**可执行改进**：新增图 C：

1. 想快速追踪平均门层退化 → RB/直接 RB/循环基准；
2. 怀疑并行串扰 → 同步 RB 或上下文相关的层基准；
3. 想找相干轴误差和门间自洽模型 → GST；
4. 已有可信制备与测量且只需一个过程矩阵 → 过程层析；
5. 想预测目标算法 → 镜像线路或应用工作负载，而不是只看一个门。

说明 GST 同时拟合门、制备和测量，存在 gauge 自由度，并通常假设平稳、马尔可夫、固定维数；违背这些假设时需要模型失配诊断。过程层析会把自身制备/测量误差带入估计。

**权威来源**：[GST 的实验验证与假设](https://www.nature.com/articles/ncomms14485)；T. Proctor et al., [Direct Randomized Benchmarking for Multiqubit Devices](https://doi.org/10.1103/PhysRevLett.123.030503)；关于平均误差和最坏情形阈值不可直接等同，见 [Comparing Experiments to the Fault-Tolerance Threshold](https://doi.org/10.1103/PhysRevLett.117.170502)。

### 2.4 [P2，中] 增加“测量也是量子仪器”的动态线路表征

**可执行改进**：指出中途测量不是终止测量的简单复制：它同时有分类错误、对未测量邻居的串扰、回馈等待期间的退相干，以及条件分支错误。补充 quantum-instrument randomized benchmarking 作为研究入口，不必展开推导。

**同行评审来源**：[Measuring error rates of mid-circuit measurements](https://www.nature.com/articles/s41467-025-60923-x), *Nature Communications* (2025)。

---

## 3. 连接、封装与控制基础设施

### 3.1 [P1，低] 超导封装不应只写“布线多”

**可执行改进**：在超导小节补一张截面图，至少标出量子比特裸片、读出/控制层、倒装焊凸点、中介层、超导 TSV、封装地、冷台和室温链路。正文解释四个相互冲突的目标：更多垂直 I/O、更好接地/抑制槽模、低损耗材料、充分热化。普通 CMOS 中可接受的介质和铜互连可能引入介质损耗、发热或准粒子。

**同行评审来源**：[3D integrated superconducting qubits](https://www.nature.com/articles/s41534-017-0044-0)；[Solid-state qubits integrated with superconducting through-silicon vias](https://www.nature.com/articles/s41534-020-00289-8)。后者专门讨论 TSV、多层堆叠、寄生模式和热化路径。

### 3.2 [P1，中] 增加低温电子学的热预算，而不是只说 cryo-CMOS 能减少线缆

**可执行改进**：用分层功耗表区分室温、3–4 K、约 100 mK、约 10–20 mK；解释“把电子学移近量子比特”会缩短信号路径和减少线缆，却把开关功耗、噪声和热流带到冷端。给出热预算式：

\[
P_{\rm stage}=P_{\rm static}+N_{\rm ch} f E_{\rm pulse}+P_{\rm IO},
\qquad P_{\rm stage}<P_{\rm cool}(T),
\]

但明确这只是工程账本，不是通用缩放定律。

**2025 实证**：mK cryo-CMOS 芯片含超过 10 万晶体管，论文报告数字模块固定开销为数十微瓦、模拟单元在特定 100 mV 脉冲条件下约 \(20\,\mathrm{nW\,MHz^{-1}}\)，并观察到寄生加热风险；这些数值仅适用于该芯片、封装和工作点。[Spin-qubit control with a milli-kelvin CMOS chip](https://www.nature.com/articles/s41586-025-09157-x)，2025。

### 3.3 [P1，低] 离子 QCCD 必须把搬运原语计入门图

**可执行改进**：增加分区阱图：存储区、纠缠区、读出区、结点；把 split、shuttle、merge、swap/reorder、recool 画成编译器可调度的原语。明确“链内全连接”与“QCCD 中任意两离子可经搬运相遇”都不等于零成本全并行。

**新增例题**：同一 6 比特线路在单链和两个门区 QCCD 上排程，比较纠缠门数不变但搬运关键路径不同。

**同行评审来源**：[Demonstration of the trapped-ion quantum CCD computer architecture](https://www.nature.com/articles/s41586-021-03318-4)；[Closed-loop optimization of fast trapped-ion shuttling with sub-quanta excitation](https://www.nature.com/articles/s41534-022-00579-3)。

### 3.4 [P1，低] 中性原子加入“装载—成像—重排—计算—补原子”的循环

**可执行改进**：09 章已经解释可重排，但还应画一次完整实验循环，并把原子数拆成站点数、平均装载数、无缺陷计算区、参与两比特门数、读出后可复用数。这样读者能理解“6,100 原子阵列”和“448 原子容错原语”回答不同问题。

**2025 证据**：6,100 原子论文在约 12,000 站点上平均装入约 6,100 原子，使用约 130 W 光源、到物镜约 35–40 W，成像时长和重排也是系统资源；不能只取阵列数。[Nature 2025](https://www.nature.com/articles/s41586-025-09641-4)。连续运行路线另见 [Continuous operation of a coherent 3,000-qubit system](https://www.nature.com/articles/s41586-025-09596-6)，其贡献是补充与持续维护，不是 3,000 比特全部完成通用门。

### 3.5 [P1，低] 光子平台加入端到端损耗预算和时钟预算

**可执行改进**：把源亮度、herald、耦合、波导、开关、延迟线、芯片间接口、探测效率、死时间、暗计数、前馈延迟列成乘法/时序链。延续 09 章 \(\eta^n\) 例子，再给一个“条件保真度高、事件率仍低”的数值例：若 4 个必须到达的光子各自总生存率 0.7、源尝试率 100 MHz，则仅损耗造成的理想上界约 \(100\,\mathrm{MHz}\times0.7^4\approx24\,\mathrm{MHz}\)，随后还要乘源成功、融合成功和接受率。

**证据边界**：2025 硅光子论文的 SPAM 99.98%、芯片间通道 99.72%、融合 99.22% 均有条件性；表 1 明写“不计损耗”，论文也报告约 3 dB 光栅耦合损耗和约 26% 最大 Klyshko 效率。[Nature 2025](https://www.nature.com/articles/s41586-025-08820-7)。

### 3.6 [P1，低] 半导体自旋加入“自动调谐—谷态—交换脉冲—读出复用”的工程链

**可执行改进**：在 09 章自旋小节补充四个不是普通晶体管问题的量：量子点占据数和隧穿率自动调谐、谷分裂相对热能/驱动带宽、交换耦合对栅压噪声的敏感度、RF 反射读出复用。说明晶圆工艺一致性是必要条件，不能替代大阵列的自动调参和低温互连。

**2025 证据**：[Industrial 300 mm wafer processed spin qubits](https://www.nature.com/articles/s41534-025-01016-x) 和 [Industry-compatible silicon spin-qubit unit cells exceeding 99% fidelity](https://www.nature.com/articles/s41586-025-09531-9) 都是制造与小单元里程碑；后者仍明确说需在全局微波、较高温度和更可扩展条件下继续研究。

### 3.7 [P2，高] 拓扑路线增加“替代解释—读出—保护—门”的证据账本

**可执行改进**：保留现有五级证据阶梯，另加每项实验的四列账本：观测量、最直接结论、仍可能的平庸解释、下一项排除实验。不要将“奇偶寿命”“零偏压峰”“topological gap protocol”“poor man's Majorana”汇总成一个“拓扑比特指标”。

**时敏核查**：2025 InAs–Al 论文正文明确说测量本身不能无歧义区分拓扑 MZM 与精细调谐的平庸 Andreev 束缚态；页面记录 2026-06-24 已发表 Matters Arising，DOI [10.1038/s41586-026-10567-8](https://doi.org/10.1038/s41586-026-10567-8)。2026 最小 Kitaev 链论文称其为保护有限的 poor man's Majoranas。[原论文](https://www.nature.com/articles/s41586-024-08445-2)；[两站链奇偶读出](https://www.nature.com/articles/s41586-025-09927-7)。任何更强结论都应重新核查争论和后续数据。

---

## 4. 编译、路由、调度与动态线路

### 4.1 [P1，中] 把当前一段编译说明扩成“七级目标机编译”图

**可执行改进**：在 09 章软件节新增图 D：

```text
算法/高层程序
 → 规范化与逻辑优化
 → 门分解/酉综合
 → 初始布局（逻辑比特映射到物理比特）
 → 路由（SWAP、搬运或远程纠缠）
 → 本征门翻译
 → 受资源和串扰约束的调度
 → defcal/脉冲绑定与控制器执行
```

指出不同平台的“路由”含义不同：超导/自旋常插 SWAP，中性原子可移动原子，离子 QCCD 可搬运离子，模块化架构可能消耗 Bell 对。抽象连接图不能表达全部并发和方向约束。

**规范/官方入口**：[IBM 的目标机编译阶段说明](https://quantum.cloud.ibm.com/docs/en/guides/transpile) 可作为一个具体实现例子；它不是通用标准。QIR 的前端、通用 IR 变换、目标后端 lowering 三阶段见 [QIR 规范](https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md)。

### 4.2 [P1，低] 增加一个可手算的布局与 SWAP 路由例题

**例题设计**：物理连接为线形 \(0-1-2-3\)，逻辑线路依次需要 \(\mathrm{CNOT}(a,b)\)、\(\mathrm{CNOT}(a,d)\)、\(\mathrm{CNOT}(c,d)\)。先给布局 \(a,b,c,d\mapsto0,1,2,3\)，让学生插 SWAP；再比较另一初始布局。要求同时数：额外双比特门、深度、最终逻辑—物理置换。最后问“若 CNOT 只有单向本征实现、相邻门不能同时驱动，答案怎样变”。

**教学目标**：让读者看到最少 SWAP、最低深度、最高预计成功率并不总是同一解。

### 4.3 [P1，中] 增加调度约束与串扰冲突图

**可执行改进**：用资源冲突图表示同一 coupler、读出总线、控制 port、离子门区或共用激光束不能同时使用；用“逻辑上作用于不同量子比特”不代表物理上可并行。介绍 ASAP/ALAP 调度和等待期间 dynamical decoupling 的基本权衡，不必展开算法细节。

**规范证据**：[OpenPulse](https://openqasm.com/versions/3.1/language/openpulse.html) 对 frame 的时钟、barrier 和碰撞给出明确语义；[IBM transpiler 配置](https://quantum.cloud.ibm.com/docs/en/guides/defaults-and-configuration-options) 展示目标、定时约束和 ASAP/ALAP 是后端相关设置。

### 4.4 [P1，中] 解释 OpenQASM、OpenPulse、QIR“可移植”的边界

**可执行改进**：扩写 09 章表格：

- OpenQASM 3 是源/交换语言，可表达经典控制、定时和校准入口；单独通过语法检查不等于语义正确或任何后端都能运行。
- `defcal` 把门绑定到特定物理比特和暂态标定；一旦进入脉冲层，物理量子比特不可互换。
- OpenPulse 是可选校准语法，仍在积极开发，后端可只实现子集。
- QIR 是 LLVM 基础的中间表示；后端声明支持的 profile/指令，规范不要求共同物理门集。

**权威来源**：[OpenQASM live specification](https://openqasm.com/language/)；[pulse-level descriptions](https://openqasm.com/language/pulses.html)；[QIR specification](https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md)；[QIR instruction set](https://github.com/qir-alliance/qir-spec/blob/main/specification/Instruction_Set.md)。

### 4.5 [P1，低] 动态线路增加一条完整延迟式

**可执行改进**：将“经典分支必须在相干预算内完成”展开为

\[
t_{\rm fb}=t_{\rm meas}+t_{\rm classify}+t_{\rm transport}
+t_{\rm classical}+t_{\rm dispatch}+t_{\rm pulse}.
\]

分别解释读出积分、状态判别、控制器/机箱传输、条件计算、指令下发和最终脉冲。指出云 API 往返时延通常不属于硬件实时路径；动态线路必须在靠近设备的控制层执行。测量期间旁观量子比特还会退相干或受串扰，需计入误差而不只是时间。

**新增例题**：若测量 800 ns、判别 150 ns、传输 300 ns、条件逻辑 200 ns、下发与脉冲 150 ns，则反馈路径 1.6 μs；让学生比较 \(T_1=100\,\mu s\) 下仅由等待造成的振幅阻尼概率 \(1-e^{-1.6/100}\approx1.59\%\)，并说明这不是动态线路的全部错误。

**实验来源**：[Combining quantum processors with real-time classical communication](https://www.nature.com/articles/s41586-024-08178-2) 对动态线路与模块化的边界有清晰说明；动态 QFT 的系统演示入口为 [Quantum Fourier Transform Using Dynamic Circuits](https://research.ibm.com/publications/quantum-fourier-transform-using-dynamic-circuits)，*PRL* (2024)。

### 4.6 [P2，中] 主动重置与被动重置要成为独立资源

**可执行改进**：增加比较：等待数个 \(T_1\) 的被动重置、测量后条件 \(X\)、耗散/泵浦重置、丢弃并换入新原子。对每种方式报告时间、残余激发/错误、邻居扰动和是否需要反馈。把 reset 从“一个门符号”改写为带延迟和误差的硬件动作。

---

## 5. 译码实时性、可靠性与能耗

### 5.1 [P1，低] 译码器必须同时报告吞吐和响应时延

**现状与风险**：10、11 章已要求“解码时间短于反馈预算”，但没有区分两个不同约束。

**可执行改进**：在 10 章容错节加框：

- **吞吐**：平均处理综合征的速度必须高于数据产生率，否则形成不断增长的 backlog；可以通过并行化提高。
- **响应时延**：从最后一轮测量到条件逻辑门可执行的总时间；包括数据搬运、译码、控制通信，不能只报算法内核时间。
- **准确率**：离线、利用未来数据的译码器可很准，却不一定可在线使用。
- **可扩展性**：小码距查找表的低延迟不能外推到大码距。

**2026 实验例**：8 比特稳定性实验报告 9 轮后的完整响应 9.6 μs，其中译码 6.5 μs、通信和控制 3.1 μs；每轮平均译码低于 1 μs，但论文也讨论随噪声与轮数增长的缩放。[Demonstrating real-time and low-latency QEC](https://www.nature.com/articles/s41467-026-73331-6)，2026。该结果证明一个小规模集成路径，不是所有表面码规模都已满足实时性。

### 5.2 [P1，中] 增加“综合征到 Pauli frame”的数据路径图

**可执行改进**：新增图 E：ADC/相机 → 分类结果 → detector events → 时空窗口/边界条件 → decoder → Pauli frame/逻辑分支 → 控制器。标出哪些错误只需更新 Pauli frame，哪些非 Clifford/传送步骤真的要求及时条件操作。这样可纠正“译码后每次都立即打一个物理纠正脉冲”的常见误解。

**研究入口**：[Willow 表面码论文](https://www.nature.com/articles/s41586-024-08449-y) 同时报告离线和实时译码，并明确大码距综合征数按面积增长；[AlphaQubit](https://www.nature.com/articles/s41586-024-08148-8) 主要证明准确率和模拟扩展性，不应自动表述为已部署、低延迟、大规模在线控制器。

### 5.3 [P1，低] 将“可用率”拆成可靠性与维护指标

**可执行改进**：11 章资源表加入：

| 指标 | 建议定义 |
|---|---|
| 可用率 | 计划运行窗口中可接受作业的比例 |
| calibration duty cycle | 用于校准而非用户线路的时间比例 |
| MTBF / MTTR | 失效间平均时间 / 平均修复时间，须定义何为失效 |
| yield | 制造站点、可寻址比特、可用耦合边、合格模块各自的良率 |
| sustained quality | 连续小时/天内达到阈值的分位数，而非最好一批 |
| job success | 含排队、编译、运行、上传在内的端到端成功率 |

强调这些指标目前未形成跨厂商统一口径，教材应教“怎样定义和保存”，不发布伪精确排行榜。

### 5.4 [P1，中] 能耗必须先规定系统边界，再谈量子优势

**可执行改进**：把 11 章“能耗”一行扩成四个边界：器件内控制能量、冷端热负载、整机墙插功率、完成目标任务的总能量。建议统一写为

\[
E_{\rm solution}=\frac{(P_{\rm cryo}+P_{\rm laser}+P_{\rm control}+P_{\rm classical}+P_{\rm facility})\,t_{\rm wall}}{P_{\rm success}},
\]

这是核算框架，不是物理定律；还要列排队、校准、失败重试和经典前后处理是否计入。不能用单脉冲的阿焦耳级能量代表整台稀释制冷机，也不能用整栋实验楼功率与经典芯片 TDP 直接比较。

**同行评审来源**：A. Auffèves, [Quantum Technologies Need a Quantum Energy Initiative](https://doi.org/10.1103/PRXQuantum.3.020101), *PRX Quantum* 3, 020101 (2022)；[Optimizing resource efficiencies for scalable full-stack quantum computers](https://doi.org/10.1103/PRXQuantum.4.040319), *PRX Quantum* 4, 040319 (2023)；理论上的能耗优势标准见 [Energy-Consumption Advantage of Quantum Computation](https://doi.org/10.1103/PRXEnergy.4.023008), *PRX Energy* 4, 023008 (2025)，不能把理论查询模型直接当成现有机器实测节能。

### 5.5 [P2，高] 标准状态必须写成“已发布/在研/撤项”，不能只写项目编号

**可执行改进**：保留 ISO/IEC 4879:2024，但明确它是已发布的**词汇**标准，不是性能基准或互操作认证。不要把 IEEE P7131 写成已完成标准：IEEE-SA 2024-12 会议记录将它列为行政撤项。若介绍新的能效或架构标准项目，要写“项目状态与访问日期”，不暗示已有共识规范。

**官方来源**：[ISO/IEC 4879:2024](https://www.iso.org/standard/80432.html)；[ISO/IEC JTC 3 项目目录](https://www.iso.org/cms/live/live/en/sites/isoorg/contents/data/committee/10/13/10138914/x/catalogue/)；[IEEE-SA 2024-12 会议记录，P7131 administrative withdrawal](https://standards.ieee.org/wp-content/uploads/2025/02/1224sasbmin.pdf)。

---

## 6. 平台专属错误：从“名单”升级为“对控制和纠错有什么后果”

### 6.1 [P1，低] 增加统一的“错误—可见信号—系统后果—对策”表

**可执行改进**：在 09 章路线表后增加下表，而不是继续堆最好保真度：

| 平台错误 | 实验上怎样看到 | 为什么系统级危险 | 典型处理 |
|---|---|---|---|
| 超导频率碰撞/残余耦合 | 同时门退化、谱线/层基准异常 | 路由和调度上下文相关 | 频率规划、可调耦合、校准感知调度 |
| transmon 泄漏 | \(|2\rangle\) 人口、非二态读出 | 可跨纠错轮持续并污染邻居 | DRAG、泄漏复位/交换、泄漏感知译码 |
| 离子模加热/谱拥挤 | 边带热占据、门随链长退化 | 搬运和并行门改变误差 | 冷却、脉冲整形、分区 QCCD |
| 中性原子丢失/Rydberg 衰变 | 成像空位或状态外人口 | 丢失时间未知会传播成相关错误 | 无损/中途检测、擦除译码、补原子 |
| 光子损耗/不可区分性 | coincidence、HOM、herald 统计 | 成功率与误差同时影响时空资源 | 复用、低损耗开关、擦除型码与前馈 |
| 自旋电荷噪声/谷态 | 交换频率漂移、泄漏、调谐失败 | 同一波形无法跨器件复用 | sweet spot、自动调谐、材料/同位素工程 |
| Majorana 候选的准粒子中毒 | 奇偶随机跳变与 dwell time | 破坏编码奇偶，且信号不证明拓扑 | 奇偶监测、材料与能隙工程、替代解释检验 |

表格脚注必须说明：可标记的擦除通常比未知 Pauli 错误更易解码，但“可标记”依赖探测误报、漏报和发生时间分辨率。

### 6.2 [P2，低] 区分随机误差、相干误差、相关突发和漂移

**可执行改进**：05 章已说明非独立同分布；09/11 章应把它落到硬件：同样的平均 infidelity，随机 Pauli 误差随深度近似累积，相干小角误差可有方向地积累，慢漂移造成批次差异，高能粒子或共用控制可产生多比特突发。要求基准报告时间块、同时运行条件和空间相关性，而不只报平均。

---

## 7. 量子网络协议栈：从物理链路到可调用服务

### 7.1 [P1，低] 增加混合经典—量子协议栈图

**现状与风险**：12 章已经讲了链路、交换和指标，但“链路层/传输层/应用层”只有一句，初学者仍可能把 Bell 对当成携带 payload 的数据包。

**可执行改进**：新增图 F：

```text
应用：传态 / 分布式门 / 传感 / QKD
  ↓ 请求：端点、数量、最低保真度、截止时间
端到端服务：选择路径、交换、纯化、超时、交付
  ↓
链路层：邻居间尝试、herald、pair ID、保真度估计、重试
  ↓
物理层：发光、传输、干涉、探测、量子存储

并行经典平面：认证、时钟同步、预约、路由、herald/交换结果、资源回收
```

强调 Bell 对不是带首部的经典包；两端必须通过 pair ID 和经典消息关联存储位置，且 Bell 对会随等待变旧。

**权威来源**：[RFC 9340: Architectural Principles for a Quantum Internet](https://www.rfc-editor.org/rfc/rfc9340.html)，2023。它是 IRTF informational RFC，不是 Internet Standards Track 规范；其核心观点是纠缠分发是网络服务，保真度是服务的一部分，经典与量子数据面必须关联。

### 7.2 [P1，低] 用两链路等待算例解释存储寿命和调度

**例题设计**：A–B、B–C 两链路每 1 ms 各独立成功概率 \(p=0.1\)。

1. 单链路几何分布平均等待 10 ms。
2. 两段并行且都成功后交换，不能简单写成 20 ms；应计算最大值的期望，或用模拟比较串行/并行策略。
3. 若先成功的 Bell 对保真度随等待 \(t\) 按 \(F(t)=\tfrac14+(F_0-\tfrac14)e^{-t/T_m}\) 衰减，讨论 \(T_m=5\) ms 与 100 ms 时是否值得保留或重试。

不要求在正文推导闭式解，但应让学生看到“生成率、存储寿命、保真度、重试策略”不可分开。

### 7.3 [P1，中] 增加服务对象与元数据：不是只返回一个“成功”

**可执行改进**：定义最小纠缠交付记录：pair ID、两端存储槽、创建/最后操作时间、目标/估计保真度、生成路径、herald 状态、交换/纯化历史、过期时间、所需经典校正。解释应用请求可能指定 pair 数量、最低保真度、最大等待、连续速率或同步窗口。

**实验证据**：[Experimental demonstration of entanglement delivery using a quantum network stack](https://www.nature.com/articles/s41534-022-00631-2), *npj Quantum Information* 8, 121 (2022)，展示物理层和链路层把反复纠缠尝试抽象成平台无关交付服务；论文本身也指出多节点还需网络层和可选传输层。

### 7.4 [P2，高] RFC 9583 的“六阶段”只作能力分类，不作预测时间表

**可执行改进**：将 trusted repeater、prepare-and-measure、entanglement distribution、quantum memory、fault-tolerant few-qubit network、quantum computing network 列成能力阶梯，并逐项写“这一级新增什么”。不要把阶段号写成全球统一标准或完成日期。

**官方来源**：[RFC 9583: Application Scenarios for the Quantum Internet](https://www.rfc-editor.org/rfc/rfc9583.html)，2024，同样是 informational RFC；其文字明确说技术仍在形成，时间线难以预测。

### 7.5 [P2，中] 区分 QKD 网络与纠缠网络的协议和信任边界

**可执行改进**：12 章已区分 PQC/QKD/量子互联网，但网络栈图应再注明：可信节点 QKD 可以转发经典密钥，却不是保持端到端量子态的量子中继；prepare-and-measure 网络也不等于按需 Bell 对服务。避免把已有 QKD 城域网当成通用量子互联网的部署证据。

---

## 8. 云端实验可复现：从“保存参数”升级为可重放包

### 8.1 [P1，中] 增加一份机器可读实验清单

**可执行改进**：把 09、11 章已有保存项扩成可重放 manifest，至少包括：

```yaml
provider: ...
backend_id: ...
job_id: ...
submit_time_utc: ...
execution_time_utc: ...
sdk_and_plugin_versions: ...
source_circuit_hash: ...
target_or_isa_snapshot: ...
basis_and_connectivity: ...
calibration_snapshot_or_retrieval_time: ...
compiler_pipeline_and_optimization_level: ...
layout_routing_scheduling_methods: ...
random_seeds: ...
compiled_circuit: ...
shots_and_batching: ...
dynamic_circuit_options: ...
mitigation_and_postselection: ...
raw_results_and_schema_version: ...
analysis_code_hash: ...
```

注明校准快照未必由云平台长期提供，所以用户应在执行时保存可合法获取的目标机属性；作业提交时间与真正执行时间必须分开。

### 8.2 [P1，中] 解释编译可复现不等于物理结果可复现

**可执行改进**：给出三层复现：

1. 同一源线路和种子得到相同编译线路；
2. 同一编译线路在目标机 ISA 上仍被接受；
3. 不同日期采样得到统计相容结果。

前两层可通过版本、Target/ISA 和随机种子改善；第三层受漂移、再校准、固件和器件维护影响，不能由 seed 保证。

**官方示例**：[IBM Target/Backend 说明](https://quantum.cloud.ibm.com/docs/en/guides/represent-quantum-computers) 说明 Target 含指令、连接和脉冲/定时约束；[transpiler reproducibility](https://quantum.cloud.ibm.com/docs/en/api/qiskit/2.2/transpiler) 明确启发式编译需保存 `seed_transpiler`，但这只解决编译随机性。IBM 是案例，不是全行业规范。

### 8.3 [P2，高] 云平台表格只比较能力字段，不维护设备排行榜

**可执行改进**：若补 AWS Braket、Azure Quantum、IBM Quantum 表，只列：作业 ID/元数据、目标选择、结果保存、设备属性、动态线路/脉冲可见性、数据保留政策链接。不要永久写设备数量、价格、排队时间或“最强后端”。

**官方入口**：[Azure Quantum job properties](https://learn.microsoft.com/en-us/azure/quantum/how-to-work-with-jobs) 明确 provider、target、job ID 与运行历史；[Amazon Braket Developer Guide](https://docs.aws.amazon.com/braket/latest/developerguide/braket-developer-guide.pdf) 说明任务/混合作业结果和存储位置。所有接口、版本和数据保留规则均标为高易变，引用时记录访问日期。

---

## 9. 2025—2026 时敏结论复核

| 现有结论 | 本轮核验结果 | 教材应保留的限定 | 下次复核触发器 |
|---|---|---|---|
| Willow 距离 7 表面码低于阈值缩放 | **成立**。101 物理比特、每周期逻辑错误 \(0.143\%\pm0.003\%\)、码距每增 2 抑制 \(2.14\pm0.02\) | 是量子存储实验，不是通用 FTQC；论文有 2026-04-28 作者更正 | 新勘误、独立重复、逻辑门/算法结果 |
| 2026 更正改变核心逻辑错误数字 | **不成立**。更正只改 Fig. 3a 的横轴和图例标签 | 仍应链接更正，但不要暗示核心结论被撤回 | 论文 change history |
| 6,100 中性原子等于 6,100 门型处理器 | **不成立** | 是装载、成像、相干与搬运系统里程碑；全阵列通用高保真门未在该论文中证明 | 同一规模的并行两比特门、QEC、连续运行 |
| 2025 光子高保真指标可与确定性门直接比较 | **不成立** | SPAM/通道/融合指标条件于探测且表 1 不计损耗；必须同时给效率、事件率、接受率 | 后续论文是否报告端到端损耗与逻辑层 |
| 2026 离子逻辑改善 11×–800× 代表任意算法普遍加速 | **不成立** | 依赖具体 carbon/tesseract code、物理基线、错误检测和后选择；数据和线路仅按请求提供也影响复查 | 接受率细分、重复 QEC、无后选择逻辑门 |
| 2025 Majorana 论文证明拓扑量子比特 | **不成立** | 论文只证明单次奇偶读出原语，并明说不能排除平庸解释；2026 已有 Matters Arising | 对应回复、独立材料系统、编织/融合、保护缩放 |

### 可加入但必须谨慎限定的三项新里程碑

1. **中性原子容错架构组合实验**：2025-11-10 在线的论文用最多 448 原子组合四轮/五轮表面码实验、逻辑纠缠、传送式通用逻辑和中途复用；它展示“关键原语在一个架构中的组合”，不是已运行任意长的实用容错算法。论文有 2026-01-19 出版更正。[Nature](https://www.nature.com/articles/s41586-025-09848-5)。
2. **离子 98 比特系统**：2026-06-17 的 Nature 论文报告 98 比特 QCCD 与全连接能力，但“全连接”应连同运输、并行度、门层和 2026-07-07 出版更正一起解释。[Nature](https://www.nature.com/articles/s41586-026-10676-4)。
3. **实时译码集成**：2026 的 8 比特稳定性实验给出完整 9.6 μs 反馈响应，是把译码器接入控制器的工程证据；码距、线路类型和缩放模拟必须保留。[Nature Communications](https://www.nature.com/articles/s41467-026-73331-6)。

---

## 10. 建议新增的图表与例题清单

### 图（优先按 A–F 实施）

1. **图 A：门—Hamiltonian—波形—控制链**（P1）：贯穿 02、05、09 章。
2. **图 B：校准依赖 DAG 与漂移闭环**（P1）：说明为什么一个参数变化会使下游失效。
3. **图 C：校准、层析、RB、GST、系统基准选择树**（P1）。
4. **图 D：七级目标机编译管线**（P1）：标出平台相关的路由原语。
5. **图 E：综合征采集—实时译码—Pauli frame—逻辑分支**（P1）：区分吞吐与响应时延。
6. **图 F：量子网络混合协议栈**（P1）：量子物理/链路/端到端/应用与并行经典控制平面。
7. **超导三维封装截面图**（P1）：TSV、凸点、中介层、冷台、放大链和热流。
8. **中性原子实验循环图**（P1）：装载、拍照、重排、分区、读出、补原子。

### 表

1. **平台专属错误—可见信号—系统后果—处理方法**（P1）。
2. **表征方法选择与假设**（P1）：RB/GST/QPT/层基准/应用基准。
3. **动态线路延迟预算**（P1）：每一段时间和误差来源。
4. **可靠性与运维指标**（P1）：可用率、校准占空、MTBF/MTTR、良率、持续质量。
5. **云端可重放 manifest**（P1）：字段、为什么保存、是否易变。
6. **标准状态表**（P2）：已发布标准、informational RFC、在研项目、已撤项项目分栏。

### 例题

1. **Rabi/Ramsey 双标定**：从 \(\Omega\)、\(T\)、\(\Delta\) 算旋转角和轴。
2. **4 节点线形连接的布局与 SWAP**：比较两种初始布局、方向约束和深度。
3. **动态线路 1.6 μs 延迟预算**：估计等待期间振幅阻尼，并指出遗漏的测量串扰。
4. **两条概率量子链路并行等待**：比较生成率、存储衰减、超时和重试。
5. **光子条件保真度与事件率**：把 \(F_{\rm cond}\)、总生存率、融合成功率、时钟率合成每秒可接受事件。
6. **能量到解**：给制冷、激光/微波、控制、经典后处理和成功率，比较只算 QPU 与全系统的差异。

---

## 11. 建议的实施顺序

### 第一批：补上系统主线

先在 09 章加入图 A、B、D，Rabi/Ramsey 例题、编译路由例题和动态线路延迟式。这四项能把全书从“会读抽象线路”推进到“知道线路怎样在设备上发生”。

### 第二批：让指标能预测持续运行

在 10 章加入译码吞吐/响应时延框和图 E；在 11 章加入校准/表征/验证/基准选择树、可靠性表、系统能耗边界和可重放 manifest。

### 第三批：补平台工程和网络

在 09 章补超导封装、离子搬运、中性原子循环、光子损耗时钟、自旋调谐；在 12 章加入图 F、两链路例题和 informational RFC 限定。

### 第四批：最后更新里程碑

里程碑必须最后写，逐项保存截止日、论文版本、勘误/Matters Arising、数据/代码可得性和“没有证明什么”。这能避免结构修改期间反复追逐厂商新闻。

---

## 12. 事实核查与维护清单

1. Hamiltonian 是否标明坐标系、近似和控制约束？
2. 脉冲面积例题是否明确只适用于理想两能级、共振和给定包络？
3. 校准结果是否有时间戳、依赖关系和回归测试？
4. 门保真度是独立门、同时门、门层还是应用线路？
5. GST/层析结果是否说明 SPAM、gauge、平稳性和马尔可夫假设？
6. 连接图是否同时给出方向、并发、共享资源和搬运/SWAP 成本？
7. 动态线路时延是否包含测量、判别、传输、逻辑和下发？
8. 译码是否分别报告吞吐、响应时延、准确率和缩放条件？
9. “实时”是否真的在实验运行中闭环，而不是事后按时间模拟？
10. 能耗是否给出系统边界、墙钟时间、失败重试和经典部分？
11. “可用率”“稳定运行”是否有观察窗口和失效定义？
12. 光子保真度是否条件于探测，损耗和事件率是否同报？
13. 原子/离子数量是否等于参与门、参与 QEC 或可复用的数量？
14. 拓扑主张是否给出替代解释、争议、Matters Arising 与回复？
15. RFC 是 Standards Track 还是 informational？ISO/IEEE 文件是已发布还是项目？
16. 云端复现是否保存编译后线路、Target/ISA、种子、执行时间和原始结果？
17. 文档中的产品、后端、价格、量子比特数和“纪录”是否标截止日？
18. 论文是否有 change history、Publisher/Author Correction 或数据重分析？

---

## 13. 核心资料索引

### 控制与编译

- OpenQASM, [Live language specification](https://openqasm.com/language/) 与 [pulse-level descriptions](https://openqasm.com/language/pulses.html)，访问 2026-09-22。
- OpenQASM, [OpenPulse 3.1 grammar](https://openqasm.com/versions/3.1/language/openpulse.html)，访问 2026-09-22；页面明确标注仍在积极开发。
- QIR Alliance, [QIR specification](https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md) 与 [Instruction Set](https://github.com/qir-alliance/qir-spec/blob/main/specification/Instruction_Set.md)，访问 2026-09-22。
- F. Motzoi et al., [Simple Pulses for Elimination of Leakage in Weakly Nonlinear Qubits](https://doi.org/10.1103/PhysRevLett.103.110501), *PRL* 103, 110501 (2009)。

### 表征、系统与封装

- R. Blume-Kohout et al., [Demonstration of qubit operations below a rigorous fault tolerance threshold with gate set tomography](https://www.nature.com/articles/ncomms14485), *Nature Communications* 8, 14485 (2017)。
- T. Proctor et al., [Direct Randomized Benchmarking for Multiqubit Devices](https://doi.org/10.1103/PhysRevLett.123.030503), *PRL* 123, 030503 (2019)。
- M. Vahidpour et al., [Superconducting through-silicon vias](https://www.nature.com/articles/s41534-020-00289-8), *npj Quantum Information* 6, 59 (2020)。
- J. P. G. van Dijk et al., [CMOS-based cryogenic control of silicon quantum circuits](https://www.nature.com/articles/s41586-021-03469-4), *Nature* 592, 369–373 (2021)。
- [Spin-qubit control with a milli-kelvin CMOS chip](https://www.nature.com/articles/s41586-025-09157-x), *Nature* (2025)。

### 实时译码、里程碑与争议

- Google Quantum AI and Collaborators, [Quantum error correction below the surface code threshold](https://www.nature.com/articles/s41586-024-08449-y), online 2024-12-09 / *Nature* 638 (2025)；[Author Correction](https://doi.org/10.1038/s41586-026-10559-8)，2026-04-28。
- [Demonstrating real-time and low-latency quantum error correction with superconducting qubits](https://www.nature.com/articles/s41467-026-73331-6), *Nature Communications* (2026)。
- J. Bausch et al., [Learning high-accuracy error decoding for quantum processors](https://www.nature.com/articles/s41586-024-08148-8), *Nature* 635, 834–840 (2024)。
- H. J. Manetsch et al., [A tweezer array with 6,100 highly coherent atomic qubits](https://www.nature.com/articles/s41586-025-09641-4), *Nature* 647, 60–67 (2025)。
- D. Bluvstein et al., [A fault-tolerant neutral-atom architecture for universal quantum computation](https://www.nature.com/articles/s41586-025-09848-5), online 2025-11-10 / *Nature* 649 (2026)。
- M. A. Guidry et al., [A manufacturable platform for photonic quantum computing](https://www.nature.com/articles/s41586-025-08820-7), *Nature* (2025)。
- A. Paetznick et al., [Improved quantum processor logical error rates via correction and detection](https://www.nature.com/articles/s41586-026-10628-y), *Nature* 654, 349–355 (2026)。
- Microsoft Azure Quantum et al., [Interferometric single-shot parity measurement in InAs–Al hybrid devices](https://www.nature.com/articles/s41586-024-08445-2), *Nature* 638, 651–655 (2025)；页面链接 2026-06-24 Matters Arising。

### 网络、能耗与标准

- W. Kozlowski et al., [RFC 9340: Architectural Principles for a Quantum Internet](https://www.rfc-editor.org/rfc/rfc9340.html), IRTF informational RFC, March 2023。
- M. Caleffi et al., [RFC 9583: Application Scenarios for the Quantum Internet](https://www.rfc-editor.org/rfc/rfc9583.html), informational RFC, June 2024。
- M. Pompili et al., [Experimental demonstration of entanglement delivery using a quantum network stack](https://www.nature.com/articles/s41534-022-00631-2), *npj Quantum Information* 8, 121 (2022)。
- A. Auffèves, [Quantum Technologies Need a Quantum Energy Initiative](https://doi.org/10.1103/PRXQuantum.3.020101), *PRX Quantum* 3, 020101 (2022)。
- ISO/IEC, [ISO/IEC 4879:2024 — Quantum computing vocabulary](https://www.iso.org/standard/80432.html)，发布 2024-05。

## 14. 最终审计判断

当前硬件章节没有原则性错误，证据边界总体谨慎。它的剩余问题是“系统名词齐全、相互作用不够”：读者知道有脉冲、编译、反馈、封装和云，却还不能从一个目标门一路追到可复现实验，也不能把连接、时延、热、译码和运维放进同一预算。

以上 36 项中，优先完成 1.1、1.2、2.1、2.3、4.1、4.2、4.5、5.1、5.2、7.1、7.2、8.1，即可补齐最关键的“从 Hamiltonian 到系统”主线；其余内容可作为平台专栏和研究入口逐批加入。时敏里程碑不应继续扩张数量，而应转为带版本、勘误、条件和下一复核触发器的维护表。
