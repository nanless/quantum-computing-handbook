# V3 全书深度重构、多轮独立交叉审校与多格式出版呈现验收报告

- **版本日期**：2026-11-25
- **仓库名称**：`quantum-computing-handbook`
- **审校与归档规范**：保留全部历史 `work/research/roundNN-*` 与 `rewrite-v2-verification-report.md` 原字节不动，本报告作为 V3 独立归档；所有数据与通过状态均来自本轮最终落盘后的实际命令执行与浏览器/出版器实测。

---

## 1. 任务总览与架构跃迁（V2 → V3）

本轮围绕两大目标实施了全仓库级重构：

1. **全书知识补缺、勘误清零与架构重组（V3 内容深化）**：
   - **新增两大全套专题章 + 独立离线实验脚本**：
     - [第 20 章｜量子传感与量子精密测量：从 Fisher 信息到海森堡极限](../../handbook/20-quantum-sensing-metrology.md) + 纯标准库脚本 [sensing_lab.py](../../codes/systems/sensing_lab.py)（7 项断言模块全通过）
     - [第 21 章｜稳定子形式、经典模拟引擎与量子优势边界](../../handbook/21-stabilizer-classical-simulation.md) + 纯标准库脚本 [simulation_engines_lab.py](../../codes/algorithms/simulation_engines_lab.py)（Tableau / MPS / Pauli 传播三引擎对照态矢量最大误差 $\le 2.22\times 10^{-15}$）
   - **全书五篇 26 章逻辑重排**：保持所有源文件命名 `00`–`21` 与 `Q1`–`Q4` 稳定不变，统一调整阅读顺序为：
     - 第一篇 入门、数学与量子态基础：`00, 01, Q1, 02, Q2, 03, 04, 05`
     - 第二篇 核心算法、应用与实验实践：`06, 07, 08, 15`
     - 第三篇 物理硬件、编译、纠错与系统工程：`Q3, 09, 14, 10, 11, 19`
     - 第四篇 密码、网络与精密测量：`12, 20`
     - 第五篇 信息理论、高级算法、模拟边界与计算模型：`13, 16, 21, 17, Q4, 18`
   - **重名与定位升级（6 章）**：Ch03（多量子比特、量子纠缠与非局域性）、Ch09（主流硬件平台与物理噪声特性）、Ch11（基准测试与容错资源估算）、Ch12（量子密码、后量子安全与量子网络）、Ch17（新增全书唯一拓扑量子计算 TQC 与 Ising/Fibonacci 任意子编织推导，吸收 Ch19 退火 TTS 账本）、Ch18（量子信道、通信容量、复杂度与连续变量）、Q4（补齐波包展宽、WKB 双势阱劈裂与原子态记号）。
   - **全书 26 章 271 道自检题零跳步题答重铸**：[handbook/appendices/exercises.md](../../handbook/appendices/exercises.md) 保留原 24 章 251 道题编号不变，新增第 20/21 章各 10 题，全部 **271 / 271** 题统一为「`题意与约定` → `完整分步演算` → `结论与边界回验` → `易错坑提醒`」四步零跳步格式（全文件 7,570+ 条公式零报错）。
   - **全库 83 张亮/暗双主题矢量图升级**：新增 21 张公式/数据驱动的 `v3-*.svg`、2 张封面横幅（动/静双态），修复 19 张 `v2-*.svg` 与 3 张手写 SVG，并将 15 张遗留 Matplotlib 轮廓路径旧图全部重铸为带真实 `<text>` 节点与 `@media (prefers-color-scheme: dark)` 的轻量矢量图（全库 **83/83 SVG 零 0-text 残留**）。

2. **多格式呈现体系升级（参考 `microphone-array-signal-processing`，只读借鉴、零外网自包含）**：
   - **产品化科研首页** [README.md](../../README.md)：`<picture>` 双态封面横幅（支持 `prefers-reduced-motion: reduce` 自动降级静态版）、零外部徽章、多格式直达导航、问题驱动选读矩阵与 5 篇 26 章路线图。
   - **展厅级离线 Web 阅读版** [reader/index.html](../../reader/index.html)（工具链 [tools/reader/](../../tools/reader/)）：纸感制图桌亮/暗双主题切换、2×2 规模指标卡（`26` 篇章 / `46,000+` 公式 / `80+` 矢量图 / `271` 题答）、三态交互式单比特量子干涉 SVG、四色 Callout 自动升维、可见 `<figcaption>`、行内公式防拆行标点胶水、右栏 ScrollSpy、顶部阅读进度条、原生 `<dialog>` 图像灯箱、代码块与 TeX 公式一键复制、每章末自动注入可折叠 271 题参考解答、音频互斥播放与 Ramsey 时刻跳转条，以及 [.github/workflows/pages.yml](../../.github/workflows/pages.yml)。
   - **零安装离线交互量子实验台** [reader/lab/quantum-lab.html](../../reader/lab/quantum-lab.html)（源 [tools/reader/quantum-lab.html](../../tools/reader/quantum-lab.html)）：Mach–Zehnder 干涉仪、3D 右手 Bloch 球单比特门沙箱、Ramsey 退相干 `√P₀(t)` vs `V(t)` 误区实时 22050 Hz 16-bit PCM WAV 声化，100% 离线零外部请求。
   - **A4 出版级离线 PDF** [dist/quantum-computing-handbook.pdf](../../dist/quantum-computing-handbook.pdf)：按块 6 路并发 Chrome 打印 + `pypdf`/`PyMuPDF` 合并、连续页眉页码、3 级 Unicode 书签、1,581 条内部可点击链接、SVG 康熙部首 `/ToUnicode` CMap 自动归一化与 $O(N)$ 流去重压缩。
   - **原生 MathML 3 EPUB 3 电子书** [dist/quantum-computing-handbook.epub](../../dist/quantum-computing-handbook.epub)：零外部依赖构建，46,770 条原生 MathML 3 公式与 114 项内嵌矢量资源，全包严格 XML 良构。

---

## 2. 三轮独立交叉审校闭环记录（直至 0 P0 / 0 P1）

| 轮次 | 并行审校路数 | 覆盖范围 | 检出 P0 | 检出 P1 | 闭环修复与验证动作 |
| :--- | :---: | :--- | :---: | :---: | :--- |
| **第一轮（`V3-CR1-01`..`12`）** | 12 路独立只读 | 全部 26 章、271 题答、7 实验册、6 附录、83 SVG、2 新脚本 | **29** | **91** | 11 路并行修复代理（`V3-Fix-01`..`11`）+ 2 项目检视觉优化（首页 2×2 卡片、封面 `解码` 与胶囊边距），100% 落实后重编 Web/PDF/EPUB |
| **第二轮（`V3-CR2-01`..`07`）** | 7 路轮换独立只读 | 逐条核验 R1 闭环率 + 专项体检 Web / 交互台 / PDF xref / EPUB / 仓库红线 | **0** | **11** | `V3-CR2-01/04/05` 率先达成 0 P0 / 0 P1；剩余 11 项 P1（含 `v2-05` `‖r′‖`、Ch03/05 `\mathrm`、Ch04 链接、Ch20 引 Ch13 节号、271 题四步小标统一、恢复历史 `round71` JSON、PDF 封面与 `/StructParents` 诚实度量化）由 `V3-Polish-A/B` 两路彻底清零，并统一将 `audit-log.md` 收录为 PDF/EPUB `附录 G` |
| **第三轮（`V3-CR3-A` & `B`）** | 2 路终审独立只读 | 全部终版改动文件 + 终版 PDF/EPUB/Web + 全站 44 HTML 嵌套标签扫查 | **0** | **0** | 全部达到 **0 P0 / 0 P1 — PASS**；另将 `V3-CR3-A` 顺带检出的范围外 4 篇正文最后 7 处嵌套 `<strong>` 与 `exercises.md` 8 处 `\mathrm{甲/乙}` 一并清零并完成终版全量重建与验收 |

> **关键硬错（P0）修复范例**（完整明细留存于各轮审校报告）：
> - 第 04 章：Solovay–Kitaev 补齐 $-i$ 与无迹生成元 $K$；Lowenthal 定理限定锐夹角 $\psi=\arccos|\hat n\cdot\hat m|\in(0,\pi/2]$；
> - 第 05 章：纯准静态高斯退相干 $e^{-(t/T_2^*)^2}$ 精准区分“打破时间齐次半群律”与“单时间映射仍严格 CP-可分”；`v3-05` 修正 Pauli Twirling 为 `¼∑ R_P R R_P`；
> - 第 06/07 章：Bucket-Brigade QRAM 区分激活开关 $O(\log_2 N)$、路由门交互 $\Theta(\log_2^2 N)$ 与 FTQC 总门数 $\Theta(N)$；Shor 位宽精确为 $t=\lfloor 2\log_2 N\rfloor+1$；题答补齐 HHL 半角 $\sin(\theta_j/2)$ 与 Ch06 Q12 精确值 `0.3166`；
> - 第 08/17 章：修正双电子物理学家记号 $\langle pq|sr\rangle$、Fibonacci 五边形方程组 $F_{11}+F_{\tau\tau}^2=1$ 与 DAQC 残余符号 $(t_1-t_2)J Z_1 Z_2$；
> - 第 09/11 章：修正 `v3-09` 面板 (5) 硅自旋双量子点势阱在 SVG $y$ 向下坐标中的上下倒置；删除交错 RB 对相干噪声失效的 `min{b_1,b_2}` 界并引入经 2,934 组随机 CPTP 信道压测零违例的 Magesan 保守界 + Carignan-Dugas–Wallman–Emerson (*NJP* 2019) 界；
> - 第 12/13 章：奇数模 $q=17$ LWE 容错界精确收紧至对称充分界 $|w|\le 3$（正文/题答/`v3-12` 三方一致）；将 Lu 等 (*Science* 2026) 11 km DI-QKD 实测值修正为 $S=2.612\pm 0.031, Q=0.0285\pm 0.0002$ 并与 Hensen (2015) 严格区分；补齐 Jaeger–Shimony USD 分界平方 $s^2\le \eta_1/\eta_0\le 1/s^2$；
> - 第 14/16/18 章：修正 $\sqrt{\mathrm{SWAP}}$ 最少 $\mathrm{iSWAP}$ 数为 `3` 并补 Makhlin $g_1$ 证明；修正 Litinski $\pi/8$ 注入 $m_1=-1$ 需非 Pauli Clifford $\pi/4$ 修正；补全 Mahadev TCF 校验方程 $c=d\cdot(x_0\oplus x_1)\pmod 2$；修正恒定退极化噪声摧毁的是 Porter–Thomas 涨落与 `#P` 难干涉信号而非“打破反集中”；
> - 第 20/21 章与 Q2：对齐 Ch20 §7.3 双边谱因子 2（与 Ch14 §6.2 一致）；修复 `v3-20` 全部曲线在低 $N$ 严格满足 $\ge$ 无噪 HL 且 $N=1$ 重合于 $2\sqrt{e}$；将 `v3-21` 匹配门/高斯代数口袋移至右侧高 $t$/高 $\chi$ 区；修正 `v3-q2-lindblad-trajectories.svg` 速率符号 `γ→κ` 与 Q2 高斯脉冲初态 $|{+i}\rangle$。

---

## 3. 终版自动化门禁与实测指标（全部退出码 0）

| 验收项目 | 执行命令 | 实测结果 |
| :--- | :--- | :--- |
| 离线 Python 数值与音频校验 | `python3 codes/run_all.py` | **36 / 36 脚本 PASS**，5 段确定性合成 WAV 验真通过，`codes/vendor/` 31 项目 / 122 文件 SHA-256 全部通过 |
| V3 质量与完整性门禁 | `node tools/reader/check-v3-quality.mjs` | **5 / 5 门禁 PASS**（42 份 MD 零 `\(...\)`/`\[...\]`、零禁词、零违规 `译码`、83/83 SVG 含 `<text>`、26 章 271/271 题答对齐） |
| 物理篇与网络数值核验 | `node tools/reader/check-qm-review.mjs` / `check-network-examples.mjs` / `check-qm-examples.mjs` | **全部 PASS**（26 章、271 题/271 答、4 份物理篇存档对齐、Q1 `\theta_{\rm g}` 字节锁与 0 `\chi`、21 项全局相位断言通过） |
| Web 阅读版离线构建 | `node tools/reader/build.mjs` | **43 篇离线 HTML + `reader/lab/quantum-lab.html`**、**46,827 条 KaTeX 公式**、**35 张 Mermaid 流程图**、`mathErrors: []`、`diagramErrors: []` |
| Web 双宽浏览器全站验收 | `node tools/reader/verify.mjs` | **86 组页面×视口（1440px / 390px）** + 2 组交互台双宽验收 + 81 张渲染截图 + 83/83 SVG `getBBox()` 零越界 + 5/5 WAV（4.0s） + **0 外部网络请求** + **0 错误** |
| 全站 HTML 嵌套粗体扫描 | Python 扫描全部 44 份 `reader/**/*.html` | **0 处嵌套 `<strong>`** |
| A4 出版级 PDF 构建与 QA | `node tools/reader/build-pdf.mjs` | **1,292 页**（1 封面 + 1,291 正文，含附录 G）、**37.626 MiB**（`< 50 MiB`）、**516 条 3 级 Unicode 书签**（514/514 命中 Named Destinations）、**1,581 条内部 GoTo 链接**（47/47 目录链接）、**0 康熙部首**（自动归一化 1,333 处 CMap）、**0 空白页**、**0 损坏 xref**（C 级 stderr 0 字节）、总耗时 `37.43s`、**10 / 10 门禁 PASS**（注：分块合并如实记录 `structParentsPages: 8 / 1292`） |
| 原生 MathML 3 EPUB 3 构建与 QA | `node tools/reader/build-epub.mjs` | **3.639 MiB**、**43 篇 XHTML**（含 `app-audit-log.xhtml`）、**46,770 条原生 MathML 3 公式**、**114 项 SVG 资产**、**159 / 159 XML 严格良构**、**2,483 条链接 0 断链**、**4 / 4 门禁 PASS** |
| 仓库红线与工作区卫生 | `git status` + `find` | `codes/vendor/` **0 改动**、历史 `work/research/roundNN-*` **0 改动**、`__pycache__` **0 残留** |

---

## 4. 自动检测与人工目视抽检范围（诚实区分）

- **全量自动检查范围**：全部 42 篇源 Markdown、43 篇生成的 `reader/` HTML（双宽 86 屏）+ `reader/lab/quantum-lab.html`（双宽 2 屏）、全部 83 张 `handbook/assets/*.svg`（Chrome `getBBox()` 越界检测）、全部 1,292 页 PDF 文本/康熙部首/空白页/书签/链接/xref 校验，以及全部 159 份 EPUB XML 文件解析校验。
- **主代理人工目视查看的渲染截图（抽检，非整书 1,292 页逐屏人工翻阅）**：
  - Web 阅读版与交互实验台：`work/rendered/index-1440.png`（初版与 2×2 终版）、`index-1440-dark.png`、`index-390.png`、`quantum-lab-1440.png`、`quantum-lab-390.png`、`20-quantum-sensing-metrology-1440.png`、`21-stabilizer-classical-simulation-1440.png`；
  - 封面横幅与重点矢量图：`cover-banner-light.png`（初版与终版）、`cover-banner-dark.png`、`v3-09-entangling-gates-six-platforms-light.png`、`v3-20-sensing-limits-light.png`、`v3-21-classical-sim-boundaries-light.png`、`v2-05-bloch-noise-channels-light.png`；
  - PDF 150 DPI 出版样张：`pdf-preview-cover.png`（初版与终版）、`pdf-preview-toc.png`（初版与含附录 G 终版）、`pdf-preview-sample1.png`、`pdf-preview-sample2.png`。
  - （此外，各图组与交叉审校子代理分别在其专项审查中逐张查看了全部新增与重铸 SVG 的亮/暗双主题 PNG 截图。）
