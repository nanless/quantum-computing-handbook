# 第 72 轮系统组：八篇逐章审读与完整 SDK 证据

日期：2026-10-13。负责人：systems72。范围：09、10、11、12、14、15、19、量子力学 Q3 八篇原稿及对应原题答、系统/实践实验入口、round71 系统报告。先读 AGENTS.md 与 STYLE.md，按章分段完整阅读；被工具截断处用较小窗口补读。只编辑分配的八篇正文、自己的代码/图/研究报告，不改共享目录、同步 sources、附录题号、AGENTS 或构建，不执行 Git 提交。

“逐页”指 Markdown 篇章，不称固定 PDF 页码；本组只人工查看两张新科学图的实际 PNG，没有宣称全文逐屏人工验收。没有新增章：现有器件→编译控制→纠错→资源→网络→运维/实践链能容纳这些缺口。数学工具入口前移由主审处理，本组引用既有第 01 章作为先修。

## 1. 逐篇覆盖及本轮修订

### 09｜从物理量子比特到控制栈

全文覆盖共同系统层、DiVincenzo、六平台存/控/读/基础设施、T1/T2/SPAM/泄漏与丢失、热复位、告警贝叶斯、有限标定、路由反馈和截至 2026-09-24 的里程碑。核对 11 道原自检与答案，没有改动题号或原 101=49+48+4 资源口径。

发现实现断点：硬件/平均门不保真度到 SDK 电路噪声尚无具体换算，容易把所有 0.1% 都当同一量。S72-09 给完整 DEPOLARIZE1 Pauli 映射、Bloch 缩放 1-4p/3、纯态平均重叠 1-2p/3，以及两比特 r=4p/5 和反向 p=5r/4；说明 p 全区间 Pauli CP 及高 p 的负缩放。标准库六输入算术与 SDK 数据分开，未把 T1 或 RB 单数直接当整个设备模型。

来源：真实打开 Stim v1.16.0 gates.md，访问 2026-10-13。旧硬件里程碑未整体重核，不刷新旧日期。未补无证据的新厂商纪录。

### 10｜量子错误校正与容错计算

完整覆盖编码非复制、辅助奇偶、Shor/相干逻辑残差、KL、稳定子/擦除、Steane、检测事件首末边界、加权译码、阈值、容错/T与资源、玻色和码距预算；核对原 10 道自检/答案与实验 S10。

缺口：原三位加权穷举与当前源码入口之间没有真正的电路级完整 SDK。S72-10 实跑 Stim 1.16.0 + PyMatching 2.4.0：rotated_memory_x、d=3/5/7、rounds=d、每点 20,000 shots、四种 p=.001；电路生成→DEM→全部检测事件/逻辑数据→匹配→残余逻辑判错。失败数 13/2/0，保存所有 bitpacked NPZ、文本电路、DEM、种子、哈希、统计与计时；零噪声1000对照全零。不是 import smoke test。

明确 decompose_errors 的 graphlike 部分不抹去相关原机制，普通 MWPM不等价所有码最佳逻辑解码。检测数组与实际逻辑 bit 分开，避免答案泄露。新增框架 qubit index span 26/64/118 不等实际物理参与17/49/97 的实证，后者从flattened指令独立数出。

来源：真实打开 Stim 原论文2103.02202、Sparse Blossom2303.15933及官方PyMatching stable；论文2021/2025，访问2026-10-13。stable网页标题2.1.0与安装2.4.0记录不同。未运行阈值参数网格、两种存储基、相关匹配、流式控制器、泄漏或真机。

### 11｜资源估算与基准

逐节覆盖任务/资源五元组、RB根/平方约定、QV/XEB/CLOPS、后选择、逻辑指标/奇偶、工厂调度、墙钟/能量、相关shots/统计与审稿；核对9道原题/答和S11。

S72-11 从实跑 0/20,000 的完整七轮存储反解双侧95%精确上界 .00018442696、单侧95% .00014977540；不除以7冒称每周期实测。中间计数精确区间使用Beta检验反演，不混作贝叶斯先验；标准库以二项CDF递推/二分独立核对全部四case。解释逐点区间不是三点同时95%，新增错误预算练习。批处理耗时/shot不等实时响应，含完整未来轮次，不能照搬工业微秒基准。

来源：NIST binomial guide、PyMatching官方文档真实访问2026-10-13。本次没有跑论文百万级规模或用单个桌面时间排名。

### 12｜密码、量子网络与前沿

全文覆盖PQC/QKD/Shor/Grover区分、NIST状态与勘误、KEM/认证、BB84有限统计与安全条件、损耗/PLOB、网络层、等待/不同速率/cutoff、交换/噪声卷积、指标/部署、分布式门、退火/传感与事实核查；核对17道原自检/答案和S12。旧2026-09-24部署事实未刷新。

S72-12A 完整 liboqs C 项目锁 tag0.15.0/commit97f6b86b1b6d109cfd43cf276ae39c2e776aed80，限制ML-KEM三参数、关闭OpenSSL；所有库内哈希/算法依赖完整构建。实际clean-first编译，官方example_kem及三个test_kem通过；自编C每算法10合法往返、10等长篡改后返回成功但不同secret，全部通过。输出公/私钥/密文/共享秘密长度、原始材料2272B的限定。解释implicit rejection不是API失败或身份认证，秘密不打印并安全清理。不称TLS集成或FIPS认证；签名/所有算法测试仍未跑。

S72-12B 完整SeQUeNCe0.8.5发布包及其全部声明依赖安装；真实Timeline/Event/Process/Node/QuantumChannel/ClassicalChannel/Photon，1000光子发射/624接收与确认/2248事件。10km/.2dB每km，透过期望.630957、观察.624；量子50us、经典默认60us（额外10us）、返回确认110us。全部时间戳/序号归档，窗口2000us；不是Bell成功先兆、中继或QKD安全。master README python3.12和发布包>=3.11,<3.15具体差异保存，3.11.15实际运行。

来源：实际打开liboqs官方仓库/KEM例子、FIPS203、SeQUeNCe论文2009.12000及固定通道源码。文档站404记录，使用官方仓库与已安装发布包的精确源码，不伪称网页可访问。访问2026-10-13。liboqs MIT仅顶层，third-party许可仍独立；SeQUeNCe wheel缺license字段，不推断可任意重分发。

### 14｜编译、调度与控制

完整覆盖表示层、SX共同/受控相位、虚拟Z、映射、流水线、共享调度、Hamiltonian/失谐、Rabi/校准、历史Pulse移除、GST/RB、读出、动态/实时、批处理、manifest；核对8道原自检与答案/S14。

S72-14 补完整 GRAPE 算法链，不仅链接库名：160控制变量/80槽/.5ns/40ns，H/hbar用rad/ns，计算Z失谐5MHz，每通道±.12；目标-iX。写时间序产品和非对易指数Fréchet导数，前/后向复用，g=|Tr(Utar†U)|/2、g²、Favg与态转移各分开。实际qutip-qtrl0.2.0+QuTiP5.2.3受界L-BFGS-B 5迭代达g目标，独立SciPy整矩阵差3.81e-15；gradient Fréchet vs centered diff6.09e-12，错误可交换近似差.00211155。

保存初始、矩形、优化、1ns sampled one-pole滤后、3—7MHz敏感性与波形CSV。两级g误差6.63e-12，滤后Favg.999259，最大槽间跳变.191631；强调独立盒约束不限制合成幅度/带宽，没有校准设备。首轮generic L-BFGS-B出现maxfev warning，改专用FMIN_L_BFGS_B并真实重跑，无警告同结果。未隐藏这个修复。

来源：qutip-qtrl官方控制指南/0.2.0源码、Khaneja原GRAPE论文，访问2026-10-13。控制指南0.2.1.dev与发布0.2.0分别标识。

### 15｜实践路线与论文复核

逐节覆盖四级验证、单/双比特/端序、计数/Wilson/漂移/停止、Bell witness、弛豫诊断、编译/缓解/七个labs、论文阅读、图表/研究/报告/版本；核对8原题/答及P15-A至G的题答结构。

S72-15 补可执行证据阶梯：读片段/完整安装/示例/目标实验，三种存档独立重建练习。verify_saved_results不重采样、不优化：NPZ解包/hashes/全shot重计及重新decode归档detector，从CSV独立expm全门+3D泄漏，逐条网络通知时差。额外标准库round72_checks不importSDK：字节解析、二项反演、Pauli闭式和3D Taylor路径。记录跨SIMD/versionseed限制与C系统随机源，不为一致输出替换密钥随机数。

### 19｜可维护量子系统工程

完整覆盖五平台控制、仪器POVM/后态、复位、分温区热、封装、良率/自动校准事务、模块化LO/LOCC/真链路、QA/TTS/模拟、CV/玻色、擦除/架构、标准/供应链、服务日志/能耗/manifest；核对12道原自检/答案和S19。

S72-19 补实时反馈队列具体算例：每us一个任务，19个.8us/1个4us，平均.96<1，但最大响应4us，2usdeadline失败10/20。用Fraction算所有时序避免2us边界浮点误判；第11任务latency2.2，第12恰2。公式start=max(arrival,previousfinish)，response=wait+service。多服务台不缩短本身4us服务。未用离线batch均值充当反馈，旧器件/工业论文数字不整体刷新。

### Q3｜从能级到物理量子比特

完整覆盖能隙单位、子空间与泄漏、热占据、谐振子/transmon相对vs绝对非谐、弱谱零点、自旋磁矩、RWA因子/驱动相位、环境偏迹、各平台编码及不可辨识诊断；核对8原题/答案。

S72-Q3 把第14同一真实优化CSV投入具体三维RWA，给a矩阵/√2、n、完整H/hbar与计算Z失谐对齐。最低两级-Δn去共同能量=ΔZ/2，Y控制方向一致；α=-200MHz。本次L0=.0132565731/L1=.0236287002，远大于两级gerror，独立SciPy与标准库49项Taylor重复，全三维酉性误差<1e-12。解释投影2D一般不酉/后选择分母改变；没有把该反例叫工业transmon门或完整DRAG/鲁棒优化。

## 2. 实际运行与文件证据

- 完整安装环境 `/tmp/quantum-round72-systems-sdk`，顶层锁Stim1.16.0/PyMatching2.4.0/QuTiP5.2.3/qutip-qtrl.2.0/sequence.8.5；实际 `pip check` 无broken requirements，pipfreeze保存全部依赖。
- 六个Python入口（stim_matching、grape_control、sequence_timeline、systems_calculations、verify_saved_results、plot_results）实际退出0；日志与JSON在 `codes/systems/sdk/`。
- 完整C liboqs配置/clean-first构建/example/tests/本书C均退出0，所有命令/退出码/完整日志记录 `liboqs-build-run.json`；源码hash独立由git读取，未把test_kem打印unknown误当hash。
- `python3 codes/systems/round72_checks.py --case all` 标准库八case全部过。验证NPZ全部逻辑记录、二项CDF、80槽Pauli闭式、三维Taylor、624事件和有理数queue。
- 八个主验证/绘图入口已实际用`-O`运行，各退出1并明确拒绝关闭断言；结果见assertion-guard-results.json。
- 两幅科学图以原始归档生成，PNG实际查看无遮挡；修复首次不存在PingFang路径为配置字体STHeiti并重新生成，SVG转字形路径。原图归档不承诺Linux无字体自动生成。
- 本轮旧系统入口round71已按八case重跑，历史JSON不覆盖；全书build/links/公式与desktop/mobile由主审整合。

## 3. 仍未完成的边界

完整安装和目标工作流已运行，不代表上述SDK所有功能、所有上游测试或真机工业系统都已验证。未跑中继/存储/网络安全、标准所有算法和完整KAT/侧信道、真机脉冲/所有设备约束、QEC阈值/泄漏/双基/相关与流式译码。上述未实现项与共享工业代码覆盖表应继续分开列出，不能合并成“所有算法齐全”。

算法组交换复核已完成，独立从全部80CSV、全部NPZ、624网络事件、二项尾反演及C日志确认本组关键新增；报告为round72-cross-algorithms-systems.md，无待修项。本组已经完成root OBP/MPF/cutting实际重执行及独立公式对照，A72/F72原样本/相位/矩阵独立复算；对应代码和报告见 `round72-systems-crossreview.md`。重点新增公式未发现待修项；root先发现的OBP0.3.0真实缺陷保留复现与guard，未倒记成库无问题。最终add/commit/push由主审统一执行，本组没有提交。
