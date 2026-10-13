# Round 72：完整 SDK 实验册与集成工作流的第二次独立复核

负责人foundations72_resume，日期2026-10-13。按主审要求完整阅读 handbook/labs/sdk-validation.md 和 codes/sdk/workflows/validate_workflows.py；先协调独占再小修，未重装依赖、未调用云或账号。此复核针对实验册全部条目及集成九case的代码，重点IAE资源、GST gauge和设置、MPF真实分解、OBP退回、防护与cutting方差；未冒充复跑26项目的全部上游功能。

## 已发现问题与修复

1. **IAE自适应批次整数重种子：真实统计风险。** 固定Qiskit2.5.2的StatevectorSampler._run_pub每个pub调用final_state.seed(self._seed)；QuantumState.seed收到整数会创建新default_rng，故原RecordingSampler(seed=72)每批重用底层随机流。后批电路又由前批结果选定，这不能支持独立新样本的区间假设。官方StatevectorSampler接口允许Generator。改为只初始化一次numpy.random.default_rng(72)，保持跨自适应批次推进；保存策略和seed。最小反例用H测64次、两次run：整数seed两份逐bit相同；持续Generator两份不同，结果及安装源码哈希见round72-cross-sdk-results.json。这个反例检测重流，没有宣称两份不同就证明所有伪随机数统计独立或量子随机性。
2. **IAE资源计数缺少直接机器核对。** 原算术62976/30720在原重种子轨迹上没有算错，但只由正文计算。新记录器以每pub真实各寄存器计数和metadata互查，只把同一次shot算一次，剔除powers初始占位；实际幂、总shots、Q、A和A逆调用均保存并断言。持续流改变了实际轨迹，已同步正文新数字，旧JSON另存before-independent-review-results.json，不把旧结果伪刷新。
3. **GST训练重合尚未逐条标记。** 原正文承认部分短电路重合，但代码字段统一称holdouts、scope却称held-out，可能误当全部12条独立留出。现在每条保存is_in_training_set；实际1–7在训练集，8–12不在。92个生成条目、set、数据集、计数字典同时断言唯一数，逐设置16384分母与总数1507328保存。字段lgst_holdouts保留旧JSON兼容，但scope和正文明确长度检查的训练重合。
4. **MPF独立近似路径补实。** 原已正确显式decompose避免精确高层PauliEvolutionGate矩阵，但只用最终精确答案比较偏差。新增断言分解后均为u门，无高层演化门；独立手写Strang半X/全Z/半X矩阵k次乘积，与SDK每项期望逐项核验。解析线性解、固定系数和CLARABEL解也互查。
5. **cutting的N分母可能误读为两侧执行总数。** 数学Γ²/N界在明确独立、有界估计样本模型下正确；正文现在定义N为成对样本数，每对至少一次A和一次B子线路执行。九倍是同估计样本口径的保守方差上界，不是已测总设备调用恰九倍。共享样本、分组读出和设备时长另计，精确概率任务没有有限shots实测方差。
6. **Qualtran表格用词收紧。** “实际分解矩阵”容易让人以为ModExp整个分解量子矩阵已收缩；已改为指数0–7模算术/bloq分解经典语义，另明确Toffoli完整张量。对应作者算法脚本确实执行的是这两条不同路径。

7. **结果入口映射修复。** 算法作者另指出“前十行”包含Qiskit/Algorithms，而算法JSON实际只有Cirq至dimod八项；已改为八项算法记录和前两项集成记录分别链接。作者同时提出的Qualtran边界已在第6项修复。

## 重点独立复算与实际重跑

命令：`/tmp/quantum-round72-workflow-sdk/bin/python -u codes/sdk/workflows/validate_workflows.py --case all`。修复后实际退出0，九case全passed，完整实际输出保存codes/sdk/workflows/results-all.json与independent-review-run.log；没有将安装成功当算法通过。

- IAE：实际幂[0,4,46]，每批512，成功95/379/298，总shots1536。SDK口径Q=512×50=25600；A=512×(1+5+47)=27136，A逆=25600，总52736。点估计.19996175923826892，区间[.19943445308410365,.20048906539243422]。区间含.2且半宽符合目标，是固定伪随机流本地回归，不证明95%重复覆盖率或实机SPAM正确。
- GST：92唯一设置×16384=1507328。手写非平凡可逆S=diag(1,1.2,.8,1.1)，同时变换r/e/G，在长度1–12的dense预测上最大概率差1.11e-16；正文代数S逆S抵消正确。S为表示变换，不把它称物理信道，也未据矩阵逐格差解释物理误差。LGST本身用target_model作为默认gauge参考；实际probability残差保留，未说真实门等于理想目标。LGST不是长序列MLE、线性估计不保证CP。
- MPF：独立Strang期望.35368081646218225/.3141599796425098，与SDK .35368081646218247/.3141599796425099差≤2.23e-16；实际u门6/12。系数(-1/3,4/3)，重构.30098636736928575，精确.3011069005521366，偏差.0001205331828508519；Gamma=5/3，未调用动态张量MPF。
- OBP：已查固定0.3.0源码初始observables_out=observables_tmp别名与slices[:-accepted]。正常接受2片与U†ZU完整矩阵一致；拒绝0片却剩0片且候选2项的上游缺陷继续真实复现。防护恢复原始Z副本和两段电路副本，新增n−accepted片数/算符矩阵断言再查原期望.7976622192414451。这个防护只修本例调用路径，未声称上游已修复或覆盖任意中途截断。
- Cutting：完整partition→6项QPD→每侧12子实验→精确分布→reconstruct，XX/ZZ/IZ为1/1/0。Gamma=3，独立成对有界估计器保守方差≤9/N正确；没有执行有限shot抽样，不给实測方差或运行优势结论。
- 其他case：Qiskit布局校正等价、SQD完整谱/残差与限制子空间上界、Mitiq独立退极化公式、Pauli Rust传播与可达L1偏差界均重跑通过。各自范围仍按原结果保存。

## 来源、检查与闭环

2026-10-13实际浏览官方StatevectorSampler、Qiskit Algorithms0.4.0 IAE、cutting0.10.0教程、MPF0.3.0首页、OBP0.3.0固定源码及pyGSTi v0.10.2 LGST源码；同时定位已安装对应版本源码，包括create_lgst_circuits去重、run_lgst默认gauge、IAE每批num_oracle_queries增量。源码哈希及最小重种子反例另存round72-cross-sdk-results.json。

实验册新增后74个公式KaTeX实际渲染0错，marked无未解析粗体，git diff --check通过；这不替代主审网页截图与全书链接检查。已将IAE新数值、GST训练重合和独立修改通知主审。旧原始失败、旧复核前结果均保留，不把发现记成零问题。主审可接续reader构建、共享报告同步与最终提交。
