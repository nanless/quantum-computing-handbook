# 系统实验：从噪声标签到长期吞吐

本目录的数值实验脚本均为本手册原创教学程序，只用 Python 标准库；原有六个脚本在 Python 3.9.6 实际运行通过。绘图生成器另需 Matplotlib，见下文。脚本不会连接量子设备，也不需要账户或密钥。数据全部为模型参数、合成日志或伪随机模拟，不是真机测量。

在项目根目录分别运行：

```sh
python3 codes/systems/hardware_flags.py
python3 codes/systems/weighted_decoder.py
python3 codes/systems/factory_schedule.py
python3 codes/systems/network_wait.py
python3 codes/systems/routing_mapping.py
python3 codes/systems/service_timeline.py
```

| 程序 | 对应章节 | 核心断言 | 参考输出 |
|---|---|---|---|
| `hardware_flags.py` | 09 硬件 | 四类计数守恒，条件概率分母为零时返回 `None` | 精确率 0.3290799194；漏检 20 |
| `weighted_decoder.py` | 10 纠错 | 八错误概率归一化，残余仅为恒等或逻辑 X | 加权失败 0.01；最少翻转失败 0.0432 |
| `factory_schedule.py` | 11 资源 | 每次消费前供应足够，上一层已结束 | 一厂 16 周期；两厂 10 周期 |
| `network_wait.py` | 12 网络 | 解析值与固定种子样本均值在六标准误内 | 解析等待 11.428571；模拟 11.44125 |
| `routing_mapping.py` | 14 编译 | 八基向量和一个复态等价；不解释映射有反例 | 最大振幅误差 0；4 门或恢复后的 7 门 |
| `service_timeline.py` | 19 运维 | 重叠/嵌套/相接区间只算一次 | 在线 20 h；合格 18 h；75000 合格 shots/s |

完整实际运行输出保存在 [expected-results.json](expected-results.json)，其中同时记录 Python 版本。有随机性的程序明确设置 `69012` 或 `69014`；其余程序是完全确定性的精确枚举或算术，不需要随机种子。`assert` 是教学不变量检查，请不要用 Python 的 `-O` 选项关闭它们。浮点输出最后几位可能随环境变化，应按文档精度或误差容限比较。

手算过程、后续练习与开源研究路线见[系统实验册](../../labs/systems.html)。第三方源码位于上级 `vendor`，有各自许可证；这里的六个标准库脚本不依赖第三方源码快照。

## 第 70 轮新增：六个条件边界实验

以下实验均无随机采样，无须随机种子，数据和参数直接写在脚本及对应章节。执行命令为 `python3 codes/systems/文件名.py`；请勿加 `-O` 关闭断言。完整实际输出见 [round70-expected-results.json](round70-expected-results.json)。

| 文件名 | 章节 | 独立复核方式 | 主要输出与限制 |
|---|---|---|---|
| `calibration_uncertainty` | 09 §5.4 | 三项方差与连续最优分配比较；拒绝奇异模型与全零一阶方差的退化分配 | 标准误 0.017814；一阶传播不是精确区间 |
| `coherent_repetition` | 10 §3.1 | 八维振幅按综合征恢复，对照四个逻辑 Kraus；四输入四角度 | $P_1=0.000296026$，$Y=-0.00392069$；理想综合征，无阈值结论 |
| `correlated_shots` | 11 §10.1 | 两种二项分布显式枚举，对照协方差公式 | 方差放大 4.96，等效样本 2016.13；仅合成批模型 |
| `network_cutoff` | 12 §6.4 | 瞬态状态概率传播，对照更新过程闭式解 | $K=1$ 等待 42.143 轮；无通信、交换失败 |
| `resource_schedule` | 14 §5.1 | 检查所有共享资源区间互斥与前驱完成 | 不含/含共享通道 1100/1300 ns；贪心不普遍最优 |
| `calibration_dependencies` | 19 §6.2 | 闭包、失败回归、通过回归、旧版本及额外未验证参数拒绝 | 失败保留版本7，通过晋级8；不连接硬件 |

科学图生成器 `plot_round70_cutoff.py` 另需 `matplotlib>=3.6`。运行 `python3 codes/systems/plot_round70_cutoff.py` 生成 `handbook/assets/round70-systems-cutoff.svg`；可用 `--preview /绝对路径/preview.png` 输出检查图。坐标来自解析模型，时间单位为毫秒，保存的 SVG 可脱离绘图库直接阅读。代码来源、公式推导和限制均在对应章节就地说明。

## 第 71 轮：八篇正文的模型边界核查

运行 `python3 codes/systems/round71_checks.py --case all`（默认也运行全部）；单题用 `--case 09`、`10`、`11`、`12`、`14`、`15`、`19` 或 `q3`。Python 3.9 以上，全部只用标准库。输入确定、无需随机种子、均为合成数据，不联网、不调用设备。实际输出保存于 [round71-expected-results.json](round71-expected-results.json)，不要使用 `-O` 关闭断言。

| 题号 | 输入与独立核查 | 参考输出及限制 |
|---|---|---|
| S71-09 | 向上/向下率100/9900每秒；500微秒；解析与分步速率方程 | 激发占据0.01667057；到2%需459.512微秒；没有相干或泄漏 |
| S71-10 | 本章Steane生成元；穷举4^7 Pauli与全部两位擦除支撑 | 距离3；336支撑检查；理想综合征与标签 |
| S71-11 | 独立每周期X概率0.01，100周期；二项奇数项与递推 | 最终0.433690；至少一次0.633968；非一般逻辑信道 |
| S71-12 | 独立对称Bell混合重叠0.9；四比特条件投影与卷积 | 两段0.813333；非对称同重叠反例0.82；不算链路速率 |
| S71-14 | Z帧和赤道旋转各π/2；逐矩阵元相等 | 正确/错误相位的P0为1/0；非仪器波形 |
| S71-15 | 累计100/400/1600次与70/280/1120成功；alpha预算 | 下界0.564190/0.622641/0.658615；预定查看点、稳定独立样本 |
| S71-19 | 两套同POVM Kraus，输入0/1/+；两次分支范数 | 输入1两次同值为1/0；未模拟真实测量噪声 |
| S71-Q3 | 200MHz失谐、弱面积0.1rad；复积分与精确孤立两态式 | 2.5ns一阶0.00101321；5ns谱零点仍有高阶项；非完整三态泄漏 |

`plot_round71_spectrum.py` 从 S71-Q3 公式生成 `handbook/assets/round71-systems-spectrum.svg`，只用标准库；时长单位ns、纵轴无量纲概率，图上明确合成模型与近似边界。运行 `python3 codes/systems/plot_round71_spectrum.py` 可重建，无需安装绘图库。

## 第 20 章量子传感与精密测量验算（`sensing_lab.py`）

运行 `python3 codes/systems/sensing_lab.py`（纯 Python 3 标准库、零外网、确定性计算；请勿使用 `-O` 关闭断言，已纳入统一入口 `python3 codes/run_all.py`）。对应[第 20 章](../../20-quantum-sensing-metrology.html)，包含 6 大核心断言模块（断言容差均不宽松于 `1e-12`）：

| 模块 | 对应内容 | 核心验算与边界 |
|---|---|---|
| Ramsey CFI/QFI 与 Bures 极限 | 第 20 章 §2–§3 | 理想 $V=1$ 恒满足 $F_C(\phi)=1$；含噪 $V=0.9,0.8$ 峰值 $V^2$ 与 $\phi=0$ 盲点；与根保真度 Bures 二阶极限逐点对照 |
| 多比特 GHZ 宇称测量与丢失坍塌 | 第 20 章 §3–§4 | $N=2,3,4$ 下 $\langle X^{\otimes N}\rangle=\cos(N\phi)$ 与 $F_C=F_Q=N^2$；丢弃任一比特求偏迹后 $F_Q=0$ 归零 |
| Huelga (1997) 马尔可夫退相位标度 | 第 20 章 §4 | 零死时间 $t_d=0$ 时 GHZ 与独立探针最优精度严格打平、常数因子 $e$；有限死时间 $t_d>0$ 下 GHZ 严格劣于独立方案 |
| 自旋压缩与光学损耗压缩 | 第 20 章 §5 | $N=2$ 精确 $3\times 3$ 单轴扭转（OAT）与 Kitagawa–Ueda 一般 $N$ Wineland 压缩参数 $\xi_R^2$；光学损耗正交压缩与 LIGO dB 换算 |
| CPMG-$n$ 交流锁相滤波器 | 第 20 章 §6 | 验证 $2/\pi$ 整流因子与带通滤波器主峰 $|Y(\omega_0)|^2 = 4/\pi^2$ |
| HNLS 判据与 2 比特纠错传感 | 第 20 章 §7 | 检验退相位、比特翻转与振幅阻尼信道下的 HNLS 子空间条件，并核对 2 比特纠错传感编码保护逻辑相位 |

## 跨库独立复算与隔离交叉复核入口

- **纯标准库独立复算**（均已纳入 `python3 codes/run_all.py`）：`python3 codes/systems/round72_checks.py --case all`（说明见 [round72-README.md](round72-README.md)，复算 [sdk/](sdk/README.md) 归档样本与 `liboqs-build-run.json`）与 `python3 codes/systems/round73_checks.py --case all`（说明见 [sdk73/README.md](sdk73/README.md)，零依赖解包 NPY/ZIP 复算双基解码、三维 GRAPE 传播与先兆网络重叠）。
- **隔离环境交叉复核**（需在独立虚拟环境中安装 `numpy`/`scipy`/`stim`，不由默认标准库入口执行）：`codes/systems/crossreview72.py` 与 `codes/systems/sdk73/crossreview_algorithms.py`。
