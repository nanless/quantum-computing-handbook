# 全书 24 章重塑与三轮独立交叉审校验收报告（v2，2026-11-25）

本报告记录本轮对《量子计算手册》全书 **24 章主篇**（`handbook/00-overview.md` 至 `19-engineering-architecture.md` 与 `handbook/quantum-mechanics/01..04`）、**配套附录与实验册**、**19 张全新公式驱动科学图（`v2-*.svg`）与 3 张升级旧图**、**校验代码与离线阅读版构建工具** 的完整重写、缺陷闭环与实际执行验证结果。所有历史 `work/research/roundNN-*` 归档报告与 `codes/vendor/`（31 个第三方项目 / 122 个归档源码文件）均保持原样未改动。

---

## 1. 重写范围与核心提升

- **全书 24 章深度重写**：基于 12 份覆盖 2024–2026 一手同行评审文献与官方标准（含 NIST FIPS 203/204/205、HQC、NIST IR 8547 Final、IETF RFC 10024、Google Willow & Quantum Echoes、IBM Gross qLDPC、Gidney 2025 RSA-2048、魔法态培育 *Science* 2026、Quantinuum Helios *Nature* 2026、Harvard/QuEra 中性原子系列、AWS Ocelot、AlphaQubit、DLA 贫瘠高原理论、Tindall *Science* 2026 与 Manabe–Gu–Pan 2026 经典模拟等）的专题研究档案，对全部 24 章彻底重写：
  - **24 章总篇幅**：由原约 20,967 行扩展至 **30,375 行**（全书 41 篇 Markdown 共含 **28,969 条 KaTeX 公式**与 **33 张 Mermaid 流程图**）；
  - **消除 AI 黑话与防御腔**：按 `handbook/STYLE.md` 全量清除套话、中英硬拼、机翻硬伤与内部审校补丁痕迹，改用朴实平和、面向初学者的“问题—直觉—定义与条件—零跳步手算—边界反例”叙事；
  - **补齐零跳步推导与勘误**：补全复数/内积/SVD/Euler ZYZ/Stinespring/Choi→Kraus/Grover 几何/QPE/Shor/HHL/QSVT/QAOA/表面码/晶格手术/PLOB/纠缠交换/DEJMPS/绝热误差界/连续变量 Wigner 与 TMSV 等完整推导，并修复 `codes/foundations/round73_checks.py`（Delta 法偏导互换）、`codes/algorithms/round73_checks.py`（$d=12$ 迹距离浮点灾难性抵消）与 `codes/review/cross_systems.py`（`__debug__` 断言前置）三处真实代码缺陷。
- **科学插图与离线阅读器升级**：
  - 新增 **19 张**纯 Python 标准库公式驱动、自适应亮/暗双主题矢量科学图（`handbook/assets/v2-*.svg`，生成脚本存档于 `codes/practice/generate_v2_figures_part{1a,1b,2a,2b}.py`）；
  - 按标准右手 3D 正交投影重绘 `handbook/assets/bloch-sphere.svg`，升级 `handbook/assets/partial-trace-grid.svg`（补齐 `①/②` 单元格角标），清除 `handbook/assets/round73-algorithms.svg`（及 `codes/algorithms/round73_figures.py`）顶栏的内部 `Round 73:` 前缀；
  - 加固 `tools/reader/build.mjs`：新增 `stripBlocksForHeadingScan`（彻底杜绝公式内独立 `=`/`---` 被 `marked.lexer` 误判为 Setext 标题）与展示公式占位符空行/空首行列表项防呆，自动清理孤儿 `flow-*.svg`。
- **附录、题答与实验册同步**：对齐 `handbook/appendices/{exercises,notation,glossary,prerequisites,references,software-practice}.md`、`handbook/README.md`、`handbook/quantum-mechanics/README.md`、`handbook/STYLE.md` 及全部 7 份 `handbook/labs/*.md`，严格保持 24 章 251 道自检题与参考答案一一对应。

---

## 2. 三轮独立交叉审校闭环记录

按“独立审查 → 闭环修复 → 换组复核 → 最终门禁”执行三轮交叉审校，真实保留每轮发现的缺陷及修复记录：

### 第一轮交叉审校（12 个独立只读审校代理，按 12 组邻近章配对）
覆盖全部 24 章、附录、代码与 SVG，检出并由 14 个互不重叠的修复代理（`Fix-01`..`Fix-14`）全部修复的关键缺陷包括：
- **数学与物理修正**：`01-math.md` 与 `Q1` 内积“左反线性”；`Q1` Tonomura 1989 数量级（5 个数量级而非 8）；`Q2` 厄米充要条件补全完备正交归一本征基；`03` 复系数态熵中间项；`05` 两处 `$|{+i}\rangle\langle{+i}|$` 与 Ramsey 失谐 $\Delta=\omega_{\mathrm{ref}}-\omega_0$；`07` 厄米条件数绝对值与 Grover 开区间 $(0,\pi/2)$；`08` 三节点 QAOA 反向传播符号 `-`；`11` XEB 积分多余 $2^{-n}$、LGST $A$ 多余 $^T$、20 mK 冷量、Litinski 快速/中间数据块公式；`12` $(I\otimes XZ)|\Phi^+\rangle = +|\Psi^-\rangle$；`14` Euler ZYZ 零分支割线提取公式（Haar 随机 1000 组失败率从 480/1000 降至 0/1000）与虚拟 Z $\varphi=-\phi$ 跨章对齐；`15` Wald 覆盖率 `87.75%/80.22%` 与 SeQUeNCe 后态 vs 比对目标矩阵区分；`17` 绝热界左端 $\|(I-P_0(1))|\psi(T)\rangle\|$；`18` Choi→Kraus 按列重排、单光子 Wigner 峰 `0.1420`、TMSV 两单重辛本征值与 `v2-18` 图注核齐；`Q4` $d=12$ 迹距离 `7.71005e-6`。
- **事实、术语与排版修复**：补齐 Helios *Nature* 2026-06、维也纳 TES vs NIST SNSPD、Chevignard CRYPTO 2025、Ragavan–Vaikuntanathan $O(L\log_2 L)$、King 2025 Advantage2/Advantage、Tindall *Science* 2026-05、Rudolph *PRX Quantum* 2026、Kuperberg 2023 逆封闭假设、单 CNOT LOCC $\gamma=3$；清除 Ch19 三处机翻（协同冷却、多节点、非对称磁通穿入）与全书术语统一（二元双循环码、量子仪器、共生度 $C_{\mathrm{conc}}$、魔法态、纠错症状、钻石范数、误差缓解）；根除 Ch04 Setext H1 错位、全书 CommonMark 中文标点粗体闭合陷阱（裸 `**` 与静默嵌套 `<strong>`）及 `$$` 后缺空行吞行；修复全部 12 张 SVG 并经 Playwright `getBBox()` 零越界/零重叠核验。

### 第二轮独立换组交叉审校（12 个全新审校代理，全书换组跨缝配对）
重新组合为 12 个跨依赖缝配对（`00+15`、`01+06`、`Q1+13`、`02+05`、`Q2+Q3`、`03+12`、`04+17`、`07+16`、`08+18`、`09+19`、`10+11`、`14+Q4`），逐行核验原稿、编译 HTML 与独立 Python/50 位 `mpmath` 复算：
- **8 组直接通过（ZERO P0/P1）**：`CR2-03`（Q1+13）、`CR2-04`（02+05）、`CR2-05`（Q2+Q3）、`CR2-06`（03+12）、`CR2-07`（04+17）、`CR2-09`（08+18）、`CR2-10`（09+19+glossary）、`CR2-11`（10+11+references）。
- **4 组新捕获真实 P0/P1 并全部闭环修复**（同步结合实图目检发现）：
  1. `CR2-12`（P0）：`exercises.md:236` 第 5 章第 1 题空首行 `1.\n   \[...\]` 触发 `<ol>` 崩塌导致第 5 章 8 题脱离列表（243/251）→ 修复 `exercises.md` 全部 3 处空首行（L107/L236/L289）并加固 `build.mjs` `afterEmptyListMarker` 槽位逻辑，恢复 **251/251** 顶层 `<li>`；
  2. `CR2-02`（P0）：`01-math.md` 4 张表格共 21 处 ket/bra 误写 `\|` 在 KaTeX 下渲染为双竖线 `∥` → 全部改为 `\lvert/\rvert/\vert` 并修复 L137 `$|z|^2$` 表格裸竖线（全书 41 文件同步扫描清零）；
  3. `CR2-02` + 实图目检（P0）：`06-algorithmic-primitives.md`（L7/232/1174）、`07-algorithms.md`（L9）、`16-advanced-algorithms-verification.md`（L17）共 5 处“左线性” → 全部修正为“左反线性”；
  4. `CR2-02`（P1）：`06-algorithmic-primitives.md` L1221–1233 采样次数 `$S$` 改 `$R$`（避开相位门 `$S$`）、L1343 迁至 IBM 新域名 `quantum.cloud.ibm.com/learning/...`；
  5. `CR2-08`（P1）：`round73-algorithms.svg`（及 `codes/algorithms/round73_figures.py:28`）清除顶栏 `Round 73:` 标签；
  6. `CR2-01`（P1×3）：`15-practice-research.md` L36 厘清 $X$ 基测得 `+`（经 $H$ 读出 `0`）、L613 定义 $k$ 与 $\Gamma=\gamma^k$/$\Gamma^2=\gamma^{2k}$ 衔接、L638 改为“混淆五层技术成熟度”；
  7. 顺带落实跨章链接标题对齐、Ch08“参数移位法则”、Ch09“12Q carbon 码”与 `exercises.md` Ch19 #9“离线重译码”。

### 第三轮最终零问题门禁复核（6 个独立只读代理 `CR3-01`..`CR3-06`）
对二轮后全部改动章节、附录、`build.mjs`、SVG 及全书 41 份编译 `reader/**/*.html` 执行最终门禁审查：
- **`CR3-01`（01+06）**：`PASS — ZERO P0/P1 ISSUES`
- **`CR3-02`（07+16+`round73-algorithms.svg`）**：`PASS — ZERO P0/P1 ISSUES`
- **`CR3-03`（15+00）**：`PASS — ZERO P0/P1 ISSUES`
- **`CR3-04`（08+18）**：`PASS — ZERO P0/P1 ISSUES`
- **`CR3-05`（09+13+Q2）**：`PASS — ZERO P0/P1 ISSUES`
- **`CR3-06`（`exercises.html` 251/251 + `build.mjs` 双重单测 + 全书 41 份 HTML 巡检）**：`PASS — ZERO P0/P1 ISSUES`

至此，全书 24 章、全部附录与 41 份离线 HTML 页面均在未经后续改动的定稿状态下通过独立交叉审校，**P0 = 0，P1 = 0**。

---

## 3. 自动化构建与验收实跑结果（全部来自实际执行）

| 验证命令 | 执行范围与关键指标 | 退出码 / 状态 |
| :--- | :--- | :---: |
| `python3 codes/run_all.py` | 全部 34 组本地标准库、交叉检查与快照脚本 + 5 份 WAV 音频核验 | `0` / **PASS (34/34)** |
| `node tools/reader/build.mjs`（System Chrome） | 41 篇 HTML、28,969 条 KaTeX 公式、33 张 Mermaid 流程图、`mathErrors: []`、`diagramErrors: []` | `0` / **PASS** |
| `node tools/reader/verify.mjs`（System Chrome） | 41 页 × 2 视口（1440px / 390px = **82 组**）自动浏览器检测、74 张截图、`externalRequests: 0`、`errors: []` | `0` / **PASS** |
| `node tools/reader/check-network-examples.mjs` | 纠缠交换 4 分支（含 $ZX$ 精确 $+1$ 重叠）、双链存储退相干、BB84 边界 | `0` / **PASS** |
| `node tools/reader/check-qm-examples.mjs` | MZI 干涉、部分路径记录、不确定度、势阱、谐振子、势垒、热占据、拉比振荡 | `0` / **PASS** |
| `node tools/reader/check-qm-review.mjs` | 24 章、251 题 / 251 答对齐、4 篇物理档案、4 组数学检查、21 组全局相位检查 | `0` / **PASS** |
| 全书 41 份编译 HTML 结构体检（`CR3-06`） | 6,199 条本地链接/锚点、182 条媒体引用、60 张同名非 flow SVG SHA-256 同步、251/251 习题顶层 `<li>`、0 `.katex-error`、0 裸 `**`、0 嵌套 `<strong>`、0 双竖线 ket/bra | `0` / **PASS** |

---

## 4. 视觉渲染抽检范围说明（诚实区分自动检查与人工目检）

- **全书自动浏览器检查**：由 `verify.mjs` 在真实 Chrome 中覆盖全部 **41 个生成 HTML 页面 × 桌面（1440px）与手机（390px）= 82 个视口组合**，自动检测横向溢出、字体/公式渲染、音频控件、本地资源与全部 SVG `<text>` 边界，结果均为 **0 报错**。
- **人工抽检实图目检（共 17 张最新渲染 PNG，不冒充整书 82 屏逐屏人工审看）**：
  - **页面桌面/手机截图（7 张）**：`work/rendered/index-{1440,390}.png`、`02-single-qubit-1440.png`、`04-circuits-protocols-390.png`、`07-algorithms-1440.png`、`16-advanced-algorithms-verification-1440.png`、`18-channels-capacities-complexity-390.png`；
  - **科学图明/暗主题截图（10 张）**：`work/rendered/bloch-sphere-{light,dark}.png`、`work/rendered/partial-trace-grid-light.png`、`work/rendered/round73-algorithms-light.png`，以及 `v2-07-shor-hhl-pipeline_light.png`、`v2-06-grover-geometry_dark.png`、`v2-14-drag-dd-pulses_light.png`、`v2-10-surface-lattice-surgery_light.png`、`v2-12-bb84-plob_light.png`、`v2-q1-double-slit-mzi_light.png`（其余 12 张修复 SVG 另由 `Fix-13` 在 Playwright Chrome 亮/暗主题下完成 `getBBox()` 0 越界 0 重叠验证与逐张目检）。

---

## 5. 仓库卫生核查

- `codes/vendor/`：**0 修改、0 新增、0 删除**；
- 历史 `work/research/roundNN-*` 报告与数据：**0 修改**；
- 未执行 `git add` / `git commit` / `git push`（保留完整工作区改动供用户审阅后决定是否提交）。
