<p align="center">
  <picture>
    <source media="(prefers-reduced-motion: reduce)" srcset="handbook/assets/cover-banner-static.svg">
    <img src="handbook/assets/cover-banner.svg" alt="量子计算手册封面横幅：从直觉、数学与物理到纠错、传感与模拟边界" width="100%">
  </picture>
</p>

# 量子计算：从直觉到研究入口

一套面向零基础自学者、工程研发人员与入门研究生的中文量子计算系统教材。全书以二维和四维草稿纸手算为起点，贯通数学语言、量子物理、算法原语、硬件控制、容错纠错、密码网络、精密传感与经典模拟边界，全部公式、图表、题答与验证脚本均可完全离线核对。

---

## 核心阅读与多格式直达

| 交付形态 | 入口路径 | 内容与适用场景 |
| :--- | :--- | :--- |
| **离线展厅阅读版（HTML）** | [`reader/index.html`](reader/index.html) | 整目录离线打开即可阅读（请保留完整 `reader/` 文件夹，勿只下载单个 HTML），内置预渲染 KaTeX 公式、双主题矢量图、目录检索与分章翻页 |
| **零安装离线交互量子实验台** | [`reader/lab/quantum-lab.html`](reader/lab/quantum-lab.html) | 单页离线浏览器实验台（源码位于 [`tools/reader/quantum-lab.html`](tools/reader/quantum-lab.html)）：Mach–Zehnder 干涉仪、3D Bloch 球门沙箱、Ramsey $\sqrt{P_0}$ 与 $V(t)$ 误区实时 WAV 音频合成 |
| **出版级 A4 合订本 PDF** | [`dist/quantum-computing-handbook.pdf`](dist/quantum-computing-handbook.pdf) | 适合打印精读与平板批注的完整合订本，含封面、分级目录书签、真字体公式与全矢量插图 |
| **原生 MathML 3 EPUB 3 电子书** | [`dist/quantum-computing-handbook.epub`](dist/quantum-computing-handbook.epub) | 适合电子书阅读器与手机流式阅读的标准 EPUB 3（现代阅读器支持原生 MathML 3 公式与矢量 SVG） |
| **Markdown 原稿与阅读路线** | [`handbook/README.md`](handbook/README.md) | 26 章全书总览、统一符号契约、手算算例索引与快速核查清单 |
| **271 题零跳步题答汇编** | [`handbook/appendices/exercises.md`](handbook/appendices/exercises.md) | 全书 26 章自检题完整解答（题意拆解 → 分步演算 → 数值回验 → 易错提醒），与正文和脚本参数严格同步 |

> GitHub 网页直接预览仓库中的 `.html` 文件会显示源码，不会渲染为网站；请克隆或下载本仓库后在本地打开 `reader/index.html`。

---

## 规模与可信度一览

| 维度 | 量化指标 | 核验口径与约束 |
| :--- | :--- | :--- |
| **课程体量** | **26 章**（22 主章 `00`–`21` + 4 篇物理基础 `Q1`–`Q4`） | 覆盖“计算—通信—传感”量子科技三大支柱及经典模拟生死线，配套 7 份附录与 7 份动手实验册 |
| **数学公式** | **46,000+ 条** KaTeX 构建期预渲染公式 | 统一 `$...$` / `$$...$$` 定界符、左共轭内积、大端序基序、$\log_2/\ln$ 底数与根保真度契约 |
| **科学插图** | **80+ 张** 亮暗双主题公式生成矢量图 + 全套 Mermaid 流程图 | 由脚本按公式或精确数据生成，轴标、单位与正文一致；支持原尺寸查看与 `prefers-color-scheme` 适配 |
| **习题体系** | **271 道** 零跳步 4 步题答 + 章内独立标签就地进阶练习 | 覆盖全部 26 章 `## 自检题`，保持题号连续并经自动化脚本对账 |
| **本地验算** | **36 个** 零外网纯 Python 标准库验证脚本 + **5 段**确定性合成 WAV | `python3 codes/run_all.py` 一键执行并核验断言、源码哈希与音频 PCM 元数据，不消耗云额度 |
| **开源对照** | **31 个** 代表性开源项目 / **122 份** 第三方源码摘录 | 40 位 Git 提交哈希与 SHA-256 锁定于 [`codes/vendor/manifest.json`](codes/vendor/manifest.json)，另附隔离环境实跑记录 |
| **离线交付** | **100% 离线**，零外部网络请求 | 字体、样式、脚本、音频与交互实验台全部打包在本地，由 Playwright 浏览器双宽度自动门禁核验 |

---

## 问题驱动选读矩阵

如果你带着具体困惑翻开本书，可以直接按问题直达对应章节与实验：

| 你最想弄清的问题 | 直达正文章节 | 配套手算与本地实验 |
| :--- | :--- | :--- |
| 复振幅凭什么能“相消”？一次测量能读出所有叠加答案吗？ | [第 00 章](handbook/00-overview.md) → [第 01 章](handbook/01-math.md) → [Q1](handbook/quantum-mechanics/01-experiments-states.md) | [先修 7 题自测](handbook/appendices/prerequisites.md) · [基础实验册](handbook/labs/foundations.md) · 交互实验台 MZI / Bloch 沙箱 |
| 纠缠比经典相关强在哪儿？为什么局域测量藏不住贝尔违背？ | [第 03 章](handbook/03-multiple-qubits.md) → [第 04 章](handbook/04-circuits-protocols.md) | CHSH 合作博弈 $75\%$ vs $85.36\%$ 手算 · [第 15 章 Bell 见证计数](handbook/15-practice-research.md) |
| Grover、QPE、Shor 与 HHL 到底加速了什么，账本常漏算什么？ | [第 06 章](handbook/06-algorithmic-primitives.md) → [第 07 章](handbook/07-algorithms.md) → [第 08 章](handbook/08-applications.md) | [算法实验册](handbook/labs/algorithms.md) · $N=15,35$ 连分数手算 · QRAM 瓶颈与去量子化边界 |
| 如何自己写模拟器、算准置信区间、避开论文与 SDK 里的隐蔽坑？ | [第 15 章](handbook/15-practice-research.md) | [统计实践实验册](handbook/labs/practice.md) · [开源实践对照](handbook/appendices/software-practice.md) · [完整 SDK 实验册](handbook/labs/sdk-validation.md) |
| 真实芯片为什么放进 20 mK 冰箱？脉冲、读出、纠错和制冷怎样串成整机？ | [Q3](handbook/quantum-mechanics/03-levels-control.md) → [第 09 章](handbook/09-hardware.md) → [第 14 章](handbook/14-compilation-control.md) → [第 10 章](handbook/10-error-correction.md) → [第 11 章](handbook/11-resources-benchmarks.md) → [第 19 章](handbook/19-engineering-architecture.md) | [系统与传感实验册](handbook/labs/systems.md) · [声音教学样本](handbook/labs/audio.md) |
| 后量子密码（PQC）与 QKD 是什么关系？光纤为什么有 PLOB 界？ | [第 12 章](handbook/12-security-network-frontiers.md) | 双链等待与存储截止实验 · NIST FIPS 203–205 / HQC / IR 8547 对照 |
| 量子传感器怎样突破散粒噪声？退相位下为什么 GHZ 态会输给独立比特？ | [第 20 章](handbook/20-quantum-sensing-metrology.md) | [`codes/systems/sensing_lab.py`](codes/systems/sensing_lab.py)（SQL / HL / Huelga 1997 / 压缩态 / HNLS） |
| 存不下 $2^n$ 振幅为何仍能被经典算穿？量子优势的四道铁壁在哪里？ | [第 21 章](handbook/21-stabilizer-classical-simulation.md) → [第 16 章](handbook/16-advanced-algorithms-verification.md) | [`codes/algorithms/simulation_engines_lab.py`](codes/algorithms/simulation_engines_lab.py)（稳定子表 + MPS + Pauli 传播） |
| 信道容量、GKP 网格码、拓扑任意子与连续变量波函数怎么严格入门？ | [第 13 章](handbook/13-quantum-information.md) → [第 17 章](handbook/17-computation-models.md) → [Q4](handbook/quantum-mechanics/04-wavefunctions-models.md) → [第 18 章](handbook/18-channels-capacities-complexity.md) | 擦除信道四容量手算 · GKP $4\pi$ 晶胞与 Wigner 负性检验 |

---

## 五篇 26 章全书路线图

离线阅读版侧栏与上下章翻页统一按下列五篇教学顺序编排（全部源文件保留稳定的 `00`–`21` 与 `Q1`–`Q4` 编号）：

### 第一篇｜入门、数学与量子态基础

| 序号 | 章节标题 | 核心问题与收获 |
| :---: | :--- | :--- |
| `00` | [00｜全景：量子计算是什么，又不是什么](handbook/00-overview.md) | 量子科技三大支柱、复振幅相消、最小随机比特实验与 2025–2026 现实边界 |
| `01` | [01｜零基础数学工具：看懂量子计算的最小数学语言](handbook/01-math.md) | 复数旋转、左共轭内积、酉阵与厄米阵、谱分解、条件数与张量积印章分块 |
| `Q1` | [Q1｜从实验认识量子态](handbook/quantum-mechanics/01-experiments-states.md) | 双缝干涉、MZI、Elitzur–Vaidman 炸弹测试、Stern–Gerlach 级联、马吕斯定律与量子擦除 |
| `02` | [02｜单量子比特：状态、相位、旋转与测量](handbook/02-single-qubit.md) | 相对相位、Bloch 球、$S/T$ 门与欧拉旋转、投影测量、POVM 与量子仪器 |
| `Q2` | [Q2｜可观测量与量子态的时间演化](handbook/quantum-mechanics/02-observables-dynamics.md) | 谱分解与 CSCO、Robertson/Schrödinger 不确定关系、三绘景、Ehrenfest 定理、Magnus 展开与 Lindblad 主方程 |
| `03` | [03｜多量子比特、量子纠缠与非局域性](handbook/03-multiple-qubits.md) | Bell 态、偏迹、Schmidt 分解、PPT 判据、CHSH 合作博弈与纠缠单配性 |
| `04` | [04｜量子门、电路与基础协议](handbook/04-circuits-protocols.md) | 电路矩阵翻译、Toffoli 可逆反计算、不可克隆、隐形传态、超密编码与延迟测量 |
| `05` | [05｜混态、噪声与量子信道](handbook/05-noise-channels.md) | 密度矩阵、CPTP 信道五种表示、五大噪声几何、广义振幅阻尼与 Landauer 擦除下限 |

### 第二篇｜核心算法、应用与实验实践

| 序号 | 章节标题 | 核心问题与收获 |
| :---: | :--- | :--- |
| `06` | [06｜量子算法的共同骨架](handbook/06-algorithmic-primitives.md) | 预言机、相位回踢、振幅放大、QFT、QPE、Trotter 分片、Hadamard/SWAP 测试与 QRAM 瓶颈 |
| `07` | [07｜代表性量子算法：从隐藏周期到量子模拟](handbook/07-algorithms.md) | Simon、Grover、Shor、哈密顿量模拟、HHL 线性系统、去量子化边界与复杂度类 |
| `08` | [08｜应用、变分算法与证据边界](handbook/08-applications.md) | 量子化学映射、VQE、QAOA、参数移位法则、贫瘠高原、误差缓解、SQD 与量子优势四类证据 |
| `15` | [15｜实践路线：从手算、模拟到真机实验与论文复核](handbook/15-practice-research.md) | $O(2^n)$ 态矢量引擎、Wilson/Clopper–Pearson 统计箱、论文十大红旗、四大现代 SDK 范式对照 |

### 第三篇｜物理硬件、编译、纠错与系统工程

| 序号 | 章节标题 | 核心问题与收获 |
| :---: | :--- | :--- |
| `Q3` | [Q3｜从能级到物理量子比特](handbook/quantum-mechanics/03-levels-control.md) | 热占据与制冷、约瑟夫森结非谐性、Rabi/Ramsey/Hahn 回波、三能级泄漏与 cQED 色散读出 |
| `09` | [09｜主流硬件平台与物理噪声特性](handbook/09-hardware.md) | 超导、离子阱、中性原子、光子、硅自旋与拓扑六大平台物理机制、SPAM 不确定度传播与最新进展 |
| `14` | [14｜从算法电路到物理执行：编译、调度与控制](handbook/14-compilation-control.md) | OpenQASM 3/QIR/MLIR、KAK 与 Weyl 室、ZX 演算、Virtual-Z、SABRE、DRAG/DD/GRAPE、M3/TREX、线路切割与 Litinski 容错编译 |
| `10` | [10｜量子纠错与容错计算](handbook/10-error-correction.md) | Knill–Laflamme 条件、五比特码、Toric Code 任意子、旋转表面码、晶格手术、qLDPC 与魔法态培育 |
| `11` | [11｜基准测试与容错资源估算](handbook/11-resources-benchmarks.md) | RB/IRB/GST、层保真度与 EPLG、实时解码尾延迟、九步容错资源流水线与 RSA-2048 估算演进 |
| `19` | [19｜可维护量子系统工程](handbook/19-engineering-architecture.md) | 稀释制冷热预算、3D 封装、校准依赖 DAG、玻色猫比特实证、FIFO 排队 SLA 与整机可用率 |

### 第四篇｜密码、网络与精密测量

| 序号 | 章节标题 | 核心问题与收获 |
| :---: | :--- | :--- |
| `12` | [12｜量子密码、后量子安全与量子网络](handbook/12-security-network-frontiers.md) | 格密码与 NIST PQC 标准（FIPS 203–205、HQC、IR 8547）、BB84/E91/TF-QKD/百公里 DI-QKD、PLOB 界与三代量子中继 |
| `20` | [20｜量子传感与量子精密测量：从 Fisher 信息到海森堡极限](handbook/20-quantum-sensing-metrology.md) | CFI/QFI 与 QCRB、SQL vs HL、Huelga 退相位坍塌、自旋与光学压缩（LIGO O4）、AC 锁相谱学与 HNLS 纠错传感 |

### 第五篇｜信息理论、高级算法、模拟边界与计算模型

| 序号 | 章节标题 | 核心问题与收获 |
| :---: | :--- | :--- |
| `13` | [13｜量子信息量度：熵、距离与可提取信息](handbook/13-quantum-information.md) | 熵与负条件熵、数据处理不等式、迹距离、根保真度、Helstrom 判别、无歧义判别与 Holevo 界 |
| `16` | [16｜高级算法与验证：从查询下界、统一框架到可信输出](handbook/16-advanced-algorithms-verification.md) | 多项式/对手下界、连续与离散量子行走、LCU→QSVT→GQSP 统一框架、经典阴影与可扩展验证 |
| `21` | [21｜稳定子形式、经典模拟引擎与量子优势边界](handbook/21-stabilizer-classical-simulation.md) | Aaronson–Gottesman 稳定子表、魔术度与稳定子秩、匹配门、MPS 逐键 SVD、含噪 Pauli 传播与四维量子优势铁壁 |
| `17` | [17｜量子计算模型：门、测量、绝热、退火、拓扑与模拟](handbook/17-computation-models.md) | 门模型、MBQC/gflow、FBQC、绝热计算与 Landau–Zener、量子退火端到端 TTS、拓扑任意子编织与模拟模拟器 |
| `Q4` | [Q4｜波函数、势阱、谐振子、隧穿与原子能级](handbook/quantum-mechanics/04-wavefunctions-models.md) | 连续波函数与高斯波包展宽、方势阱、谐振子升降算符、WKB 双势阱劈裂、原子超精细钟态与 Fock 截断陷阱 |
| `18` | [18｜量子信道、通信容量、复杂度与连续变量](handbook/18-channels-capacities-complexity.md) | Choi 同构、钻石范数、四类通信容量、纠缠负性、`QIP`/`MIP*=RE`、连续变量 Wigner 函数与 GKP 网格码 |

**附录与实验入口**：[先修自测](handbook/appendices/prerequisites.md) · [符号表与速查](handbook/appendices/notation.md) · [术语表](handbook/appendices/glossary.md) · [练习答案](handbook/appendices/exercises.md) · [开源实践对照](handbook/appendices/software-practice.md) · [参考资料](handbook/appendices/references.md) · [审校记录](handbook/appendices/audit-log.md) · [逐章实验总览](handbook/labs/README.md) · [声音实验](handbook/labs/audio.md) · [完整 SDK 实验册](handbook/labs/sdk-validation.md)

---

## 本地零付费复现

所有自编验证脚本仅依赖 Python 3 标准库，默认不联网、不调用云量子设备；阅读版与电子书构建依赖 Node.js 与 Playwright/Chromium，阅读已生成的 `reader/` 或 `dist/` 无需安装构建依赖。

```sh
# 1. 运行全部 36 个纯 Python 标准库教学与核验脚本（含 vendor SHA-256 与 5 段 WAV 校验）
python3 codes/run_all.py

# 2. 安装阅读版构建依赖并重新生成离线 HTML 阅读版
npm ci --prefix tools/reader --ignore-scripts --no-audit --no-fund
npm exec --prefix tools/reader -- playwright install chromium
node tools/reader/build.mjs

# 3. 执行离线阅读版全量浏览器验收（1440px / 390px、公式、链接、SVG 文字边界）及算例/题答复核
node tools/reader/verify.mjs
node tools/reader/check-network-examples.mjs
node tools/reader/check-qm-examples.mjs
node tools/reader/check-qm-review.mjs

# 4. 生成出版级 A4 PDF 与原生 MathML 3 EPUB 3 电子书
node tools/reader/build-pdf.mjs
node tools/reader/build-epub.mjs
```

详细依赖说明、环境变量（`HANDBOOK_CHROMIUM`、`HANDBOOK_NODE_MODULES`）与脚本边界见 [`tools/reader/README.md`](tools/reader/README.md) 与 [`codes/README.md`](codes/README.md)。

---

## 仓库目录与许可边界

- `handbook/`：全书 26 章、7 份附录、7 份实验册与矢量图的 Markdown 原稿；
- `reader/`：由 `tools/reader/build.mjs` 编译生成的完整离线阅读版（含本地 KaTeX 字体、流程图、合成音频、交互实验台与代码副本）；
- `dist/`：出版级 A4 PDF 与 EPUB 3 电子书发布产物；
- `codes/`：自编标准库教学程序与 [`codes/vendor/`](codes/vendor/README.md) 第三方固定提交源码摘录；
- `tools/reader/`：静态构建、PDF/EPUB 导出、浏览器渲染与算例自动验收工具；
- `work/research/`：与正文相互引用的审校记录、构建报告与固定核验数据。

**时效性与许可声明**：文中涉及的硬件指标、纠错里程碑、后量子标准与开源软件版本均标明了核验日期与证据层级，对外引用前建议对照所列一手论文或官方页面复核。本仓库目前未对原创教材正文、插图与自编教学代码附带开放许可证；公开可读不代表授予转载、改编、商用或再授权许可。`codes/vendor/` 中的第三方源码摘录各自保留原版权头、许可证与 `NOTICE` 文件，遵循其原有许可证条款，不因归档于同一仓库而改变，亦不套用于全书原创内容；第三方摘录仅用于源码对照学习，不自动执行。
