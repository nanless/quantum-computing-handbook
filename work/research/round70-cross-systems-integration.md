# 系统组对第70轮共享整合的独立复核

日期：2026-09-26。复核范围：仓库AGENTS.md本轮差异、软件实践附录§8–10全文、vendor README与机器清单、`snapshot_sources.py`的PROJECTS/固定恢复逻辑、`run_all.py`完整文件及新增入口。只读取第三方代码，未导入或执行vendor，未运行云服务。

## 源码与许可记录

用AST读取本书下载器的PROJECTS字面量，独立对照manifest；没有执行下载器的网络模式。结果：19个项目、64个源码/许可证/声明文件，全部项目名、官方repo路径、请求源码路径、完整commit、原始URL、字节数和SHA-256一致；没有`missing_requested_paths`。以Git HEAD中的旧manifest作基准，15个旧项目的commit均保持原值。

重新实际执行 `python3 codes/snapshot_sources.py --verify`，输出19项目、64文件通过。另独立逐文件算哈希，而非只引用工具的成功信息。当前reader副本也包含这64份文件，全部字节与源manifest哈希一致，没有缺失文件。

检查19个项目均有归档的根许可证，并核对README所列许可类型；重点读完整pyqsp MIT、qutip-qtrl BSD三条款、SeQUeNCe三条款文本，及Mitiq源码GPL-v3头、liboqs示例MIT SPDX和根多许可说明。README没有把Mitiq写成宽松许可，也没有把liboqs全部组件说成MIT。已有NOTICE/AUTHORS在清单中保留。这里是所收摘录与许可文本的对应检查，不是对整个上游仓库全部依赖的法律意见或执行验证。

## 软件实践附录的源码对照与数学核验

| 段落 | 实际阅读位置或独立推导 | 结论 |
|---|---|---|
| §8.1 | pyqsp `QuantumSignalProcessingPhases` 的Chebyshev转换、`ComputeQSPResponse`的`U[0,0]`分支 | 列表的基约定、复响应不是概率的提醒与固定代码一致 |
| §8.2 | Qualtran `LinearCombination.alpha`为`sum(abs(l)*be.alpha)` | 0.3X−0.4Z的系数界0.7、算符范数0.5及反对易推导一致 |
| §8.3 | PennyLane `bits/recipes`的`(T,len(wires))`说明与构造输入 | 单阴影矩阵本征值2和−1正确；非物理单快照不等于估计错误 |
| §8.4 | 参数偏移模块入口与本轮共享参数反例 | 链式法则和逐门偏移的边界一致 |
| §8.5 | mesolve/mcsolve文件的接口类别与数值误差说明 | 轨迹抽样、积分容差、Hilbert截断三种误差未混用；没有虚构完整包运行 |
| §8.6 | qutip-qtrl `pulseoptim`的GRAPE/CRAB入口、`grape_unitary`的Experimental docstring | 教材描述与源码一致，未把实验性函数当生产保证 |
| §8.7 | cutting `WeightType.EXACT/SAMPLED`与重构函数要求的顺序 | 1.5×0.4−0.5×(−0.2)=0.7，错序−0.5正确 |
| §8.8 | Aer广义阻尼矩阵、平衡态与占据参数位置 | 指向基础组的逐式核查且不篡改vendor的处理恰当 |

独立运行 `python3 codes/practice/source_reading_checks.py`，S04/S05/S06/S08断言全部通过；该脚本只用标准库，不导入vendor。S07本来是工程判断题，没有把数值断言冒充设备认证。

§9明确将厂商参考架构与四类addons入口写为公开技术路线，没有把它们等同商业优势，也明确后四类未保存和运行。§10的覆盖状态与实际归档一致：代表性源码不等于完整包、外部入口不等于已经本地实现、公开文档不等于生产日志。此次复核不重新声称已经全文复现这些外部项目。

## 链接、统一入口与工作约定

对AGENTS.md、codes/README.md、vendor/README.md及软件实践附录的110条相对文件链接逐项检查，零缺失；此项只检查目标文件存在，不代替全书HTML锚点/浏览器检查。64个vendor文件在reader中的字节也全部一致，离线引用有实际副本。

`run_all.py`共有21个命令入口，文件均存在，没有一个入口位于vendor。新增基础、算法、六个系统、源码阅读、研究实验入口均已加入；下载器只使用`--verify`。最新报告写入`work/research/code-validation.json`，没有再覆盖round69存档。此轮只单独重跑上述源码与数学检查，没有另跑整个统一入口去覆盖root正在整合的最新报告。

AGENTS新增条款明确了附录负责人、保留历史证据、文档/源码冲突记录，以及Markdown、HTML、PDF和人工抽查的范围，未与只读同步文件规则或用户授权冲突。

唯一发送root的小项是代码总README绘图段仍仅列原有两个生成器；新增`algorithms/round70_figures.py`和`systems/plot_round70_cutoff.py`应列入，或显式指向分组README。这是入口完整性问题，不影响当前数学或文件链接有效性。本组未直接修改共享文件。

截至本报告，未发现需阻断交付的新增数学错误、清单/源码矛盾或缺失本地链接。结论只覆盖上列文件与实际执行，最终阅读版全局检查、Git提交与推送仍由主agent完成。
