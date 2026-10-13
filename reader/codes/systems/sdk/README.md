# 第 72 轮：完整系统 SDK 的实际本地实验

本目录自编程序与保存数据独立于 `codes/vendor/` 的第三方源码摘录。实际运行日期与官方访问日期为 2026-10-13，Python 3.11.15、macOS ARM64。所有实验只调用本地 CPU；没有设备账号、云作业或付费请求。安装成功不等于实验成功；每个入口都有断言和实际输出。

## 1. 独立环境与版本

```sh
python3.11 -m venv /tmp/quantum-round72-systems-sdk
/tmp/quantum-round72-systems-sdk/bin/python -m pip install -r codes/systems/sdk/requirements-lock.txt
/tmp/quantum-round72-systems-sdk/bin/python -m pip check
```

完整顶层包为 Stim 1.16.0、PyMatching 2.4.0、QuTiP 5.2.3、qutip-qtrl 0.2.0、SeQUeNCe（发布包名 `sequence`）0.8.5。`requirements-lock.txt` 是实际安装后导出的全部依赖，含 SeQUeNCe 声明的界面/笔记本依赖；没有将它们全部跑过测试。锁文件固定版本，仍需目标操作系统有相应 wheel 或可构建依赖，不保证所有平台逐 bit 相同。

`installed-package-evidence.json` 保存发布包元数据、Python 条件和可取得的随包许可哈希。Stim/PyMatching 为 Apache-2.0，QuTiP/qutip-qtrl 为 BSD-3-Clause。SeQUeNCe wheel 未带许可文件或许可字段，因此不依据缺失字段推断可任意再分发；上游 [LICENSE](https://github.com/sequence-toolbox/SeQUeNCe/blob/v0.8.5/LICENSE) 和仓库既有 vendor 许可材料是源码再分发核对入口。这里不重新分发第三方安装包或二进制。

开发文档与固定发布版可能不同：PyMatching stable 网页标题为 2.1.0，本机实际 2.4.0；SeQUeNCe 当前 master README 要求 Python 3.12，0.8.5 元数据为 `>=3.11,<3.15`，本轮 3.11.15 完整安装并执行。qutip-qtrl 当前文档为 0.2.1.dev，本轮使用发布版 0.2.0；不把网页标题改成安装版本。

## 2. 电路级纠错：两个完整 SDK 接成一条证据链

```sh
/tmp/quantum-round72-systems-sdk/bin/python codes/systems/sdk/stim_matching.py
```

旋转 X 存储，码距与轮数均为 3、5、7。每个噪声点 20,000 shots，四类独立模型参数各为 0.001：Clifford 门后去极化、轮前数据去极化、测量前翻转、复位后翻转。零噪声距离 3 对照额外 1000 shots。固定种子分别为 720100/720103/720105/720107；具体电路决定每项机制的位置，不能把四个数简单相加成一个物理错误率。

保存 `.stim` 全电路、`.dem` 完整探测错误模型和每条 shot 的压缩 `.npz`。NPZ 中 `detectors`、`actual`、`prediction` 使用小端 `np.packbits(...,bitorder='little')`，行对应 shot；`detector_count` 给出有效列数，末字节填充位须截去；`failures` 是每行任一逻辑 observable 不同。读取用 `allow_pickle=False`。

本次失败数 13、2、0，分别为完整 3、5、7 轮存储。双侧 95% Clopper–Pearson 区间保存于 `stim-matching-results.json`。零失败仍有正上界 0.000184427。逐点区间不是三点同时置信保证；没有拟合阈值或运行相关匹配。匹配的批处理耗时不含逐轮采集、运输、控制反馈和尾延迟。

`circuit.num_qubits` 是编号跨度，实际参与的器件数另在独立验证结果里计为 17/49/97。

## 3. GRAPE：受界优化、独立传播与模型失配

```sh
/tmp/quantum-round72-systems-sdk/bin/python codes/systems/sdk/grape_control.py
/tmp/quantum-round72-systems-sdk/bin/python codes/systems/sdk/systems_calculations.py
```

基为 `|0>,|1>`，时间 ns，Hamiltonian 输入为 H/hbar，角频率 rad/ns。漂移 Δ=2π·0.005，两个控制 X/2、Y/2，目标 -iX。80 个 0.5 ns 槽，共 40 ns；每通道独立界 ±0.12 rad/ns，种子 72014。调用完整 qutip-qtrl `FMIN_L_BFGS_B`（受界 L-BFGS-B 专用接口），最多 500 迭代、60 秒，预定目标 `1-g <= 1e-10`。本轮 5 迭代达标，不证明全局最优。

`grape-amplitudes.csv` 每行是该槽起点、原始两个控制、采样一阶滤后控制。滤波时常 1 ns，初值为零，按槽更新并按槽保持；只传播原 40 ns，没有尾部补偿。`grape-results.json` 保存初始、矩形、优化、滤后、失谐敏感性和三能级复验。SDK 与独立 SciPy 指数传播矩阵差 3.81e-15。

归一化迹重叠 g、过程重叠 g²、平均门保真度 (2g²+1)/3、基态转移概率分别保存，不能混用。三能级采用 a 的矩阵元 1、sqrt(2)，α=-2π·0.2 rad/ns，H/hbar=-Δn+αn(n-I)/2+ux(a+a†)/2-iu_y(a-a†)/2。保留同一波形得到基输入泄漏 0.0132566/0.0236287，暴露两级目标没有覆盖的通路。

`systems_calculations.py` 用 Fréchet 导数与中心差分核对非对易槽梯度，另有独立 Pauli 参数平均重叠和 20 项反馈队列时序。队列数据是教学输入，不是解码器实测。

## 4. SeQUeNCe：实际时间轴、两端点和通道

```sh
/tmp/quantum-round72-systems-sdk/bin/python codes/systems/sdk/sequence_timeline.py
```

使用 SDK Timeline/Event/Process/Node/QuantumChannel/ClassicalChannel/Photon。本书仅自定义端点发送、接收、确认。10 km、0.2 dB/km、量子通道传播 50 μs；发布包经典默认另加 10 μs，回信 60 μs，发射到返回共 110 μs。1000 个偏振光子间隔 100 ns，节点种子 72012/72013，时间窗 2000 μs。

实际收到 624 个，发出并收到 624 条确认，执行 2248 事件。`sequence-results.json` 保留每个发射、到达和确认的序号及 ps 时间。先预约发送时间，再初始化/运行真实 SDK 的事件队列；此确认不称为 Bell 对先兆。未包括纠缠生成、QKD 后处理、暗计数、存储、死时间、中继或协议安全。

## 5. liboqs：完整 C 依赖的构建和功能验证

先显式获取官方源码并核对标签；脚本不会暗中下载和执行别的仓库。

```sh
git clone --branch 0.15.0 --depth 1 https://github.com/open-quantum-safe/liboqs.git /tmp/quantum-round72-liboqs
/tmp/quantum-round72-systems-sdk/bin/python codes/systems/sdk/run_liboqs.py --source /tmp/quantum-round72-liboqs --cmake cmake
```

脚本拒绝非预定提交，固定 HEAD `97f6b86b1b6d109cfd43cf276ae39c2e776aed80`。完整构建仅启用标准 ML-KEM-512/768/1024，`OQS_USE_OPENSSL=OFF`，Release；用 `--clean-first` 保存一次实际完整编译日志。运行上游 `example_kem` 和三个 `test_kem`，再编译本书 `liboqs_roundtrip.c`，每算法 10 次合法往返及单 bit 篡改密文检查。均退出 0；日志及配置在 `liboqs-build-run.json`，摘要在 `liboqs-run.log`。

本轮 AppleClang 21 与 ARM64 构建，不能视为所有 CPU/算法均验证；未运行所有上游测试、KAT 全套、TLS、签名算法、侧信道或标准认证。系统随机源用于生成测试密钥；不输出秘密，使用库的安全清理函数释放私钥与共享秘密。篡改密文解封装返回成功但给出不同秘密，属于隐式拒绝，不能因此认为得到已认证会话。

liboqs 顶层 MIT，内含第三方依赖有独立许可；构建和引用须保留原源码目录的许可，不能把顶层 MIT 套给全库。完整源码在显式官方获取步骤中，本目录保留作者写的集成代码与精确重建条件。

## 6. 从归档重新计算，以及可再生科学图

```sh
/tmp/quantum-round72-systems-sdk/bin/python codes/systems/sdk/verify_saved_results.py
/tmp/quantum-round72-systems-sdk/bin/python codes/systems/sdk/plot_results.py
```

第一程序不再采样或优化：验证原样本哈希和逻辑计数、重新译码已保存检测事件、从 CSV 独立传播 2/3 维矩阵、逐条复算网络通知时差。输出 `saved-results-verification.json`；均通过。

第二程序由归档数据生成 `handbook/assets/round72-systems-qec.svg` 与 `round72-systems-control.svg`，另存 PNG 预览。SVG 将文字转路径，保证离线显示字形。macOS 默认 STHeiti；别的平台设置 `HANDBOOK_CJK_FONT` 为已安装 CJK 字体路径。两幅 PNG 已实际人工查看，标题、单位、图例、区间和箭头无重叠；正式 reader 的桌面/手机检查由主审整合执行。

所有验证入口拒绝 `python -O`；不要关闭断言后把程序退出成功当验收通过。SDK本地运行证据、工业实验论文证据、生产服务指标分别表述，尚未实现的目标仍在本轮逐章报告列出。
