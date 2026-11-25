# 量子计算手册 V4 升级、旗舰网站建设与全介质发布验收报告

- **日期**：2026-11-25
- **基准提交**：基于 `71e43ba` 实施 V4 全面升级、对标 MASP 旗舰课程网站重构、方案 C 极致轻量化与 GitHub Pages / Release `v1.0.0` 全产物发布
- **红线核查**：`codes/vendor/`（31 项目 / 122 文件）零修改；历史 `work/research/roundNN-*` 归档报告零修改；全仓对外路径零本机绝对路径泄露；全部 26 章编号与 271 道既有自检题原题号 100% 保持稳定。

---

## 一、全链路自动化与独立交叉复核实测指标

| 验收维度 | 执行命令 / 方式 | 实测结果 |
| :--- | :--- | :--- |
| **纯标准库复算套件** | `PYTHONDONTWRITEBYTECODE=1 python3 codes/run_all.py` | **38 / 38 PASS**（新增 `v4_algorithms_lab.py` 与 `v4_practice_lab.py`）+ 122 份 vendor SHA-256 + 5 段 WAV 校验通过 |
| **6 道质量与隐私门禁** | `node tools/reader/check-v3-quality.mjs` | **6 / 6 PASS**（42 份面向读者 MD、92 张 SVG 均含文本、26 章 271 题精确对齐、520 文件隐私路径 0 泄露、0 禁用词、0 旧定界符） |
| **物理篇与网络算例核验** | `check-qm-examples.mjs` / `check-qm-review.mjs` / `check-network-examples.mjs` | **全部 PASS**（`\theta_{\mathrm{g}}` 统一、21 组全局相位检验、0 `\theta_{\rm g}`） |
| **旗舰官网构建与双宽度验收** | `make build && make verify` | **42 页、50,937 公式、30 幅亮/暗双变体流程图（60/60 零空节点）、1,494 条离线检索索引（151/151 术语锚点精确对齐）、271/271 两级提示解答、84 视口 0 溢出、双向暗色像素亮度达标（37–46 / 241.9）、6 模块实验台全核验、0 外部请求、0 报错** |
| **出版级 A4 PDF** | `make pdf`（`dist/quantum-computing-handbook.pdf`） | **1,045 页 / 27.58 MiB**（较 V3 1,292 页 / 37.63 MiB 瘦身 247 页、减重 10.05 MiB）、目录印刷页码 48/48（100%）0 偏移、527 条 3 级书签、2,007 条内链 0 断链、避头点由 859 处降至 7 处（-99.2%）、0 康熙部首、0 空白页、13/13 QA 门禁 PASS |
| **原生 MathML 3 EPUB 3** | `make epub`（`dist/quantum-computing-handbook.epub`） | **3.35 MiB**、47 XHTML（附录 D 拆为 5 篇，单章 ≤ 1.0 MiB）、50,925 原生 MathML 3（0 冗余 `<annotation>`）、30/30 暗色安全暖底 Mermaid、367/367 横向可滚表格、`nav` + `toc.ncx` + Accessibility 1.1（`dcterms:conformsTo`）、9/9 门禁 PASS |
| **全产物 Release `v1.0.0`** | `make release VERSION=v1.0.0`（`dist/release/`） | PDF（27.58 MiB）+ EPUB（3.35 MiB）+ 完整离线网站 ZIP（12.52 MiB / 846 文件）+ 自编代码 ZIP（4.41 MiB / 402 文件，0 `vendor/`）+ `SHA256SUMS.txt` 4/4 OK、`unzip -t PASS`、脱离原仓实跑核心脚本与离线双击 Chrome 全通 |

---

## 二、两轮独立只读交叉复核闭环摘要

1. **Round 1（4 路独立只读对抗复核：`V4-XRev-01`～`04`）**：
   - 覆盖全书新增数学推导独立 Python 复算、72 张真实 Chrome 官网与 6 模块实验台截屏目检、18 帧 A4 PDF 与 EPUB 封面样页目检、Release ZIP 脱离原仓解压实跑，以及 21 张新/修 SVG 与 3 份 GitHub Actions 工作流核查。
   - 检出并随后全部清零的关键问题：
     - **P0**：3 幅 Mermaid v11 因 `"1. ..."` 列表语法输出空白框（Ch10/11/14，修复并增设永久 `verify.mjs` 门禁）；`Cmd+K` 术语 `#term-100..151` 锚点漂移（放宽正则并对齐至 151/151）；`练 14-C` $\sqrt{\mathrm{SWAP}}$ 的 Cartan $k_z$ 符号修正为 $-\pi/8$；统一 `release-ebooks.yml`、`Makefile`、`course-home` 下载链调用 `build-release.mjs`；两张 Matplotlib SVG 外扩 `12pt` 安全边距防止 Ubuntu `DejaVu Sans` 越界。
     - **P1**：修复 `renderExerciseItemParts()` 使 271/271 题两级「💡 核心提示 → 📖 完整四步解答」100% 生效；消除官网与实验台内置 SVG（Hero、CHSH、Grover、Ramsey）及 `v3-21`/`v3-14`/`v4-21` 穿线/撞字；左侧目录改为纯容器 `scrollTop` 不再拖偏主页面 `<h1>`；手机端 `#ex-toolbar` 改为非吸顶单行横滑、桌面芯片跳转精确扣减吸顶高度；修复 4 处闭合粗体空格、2 处小节号、`audit-log` 14 道题数与 `exercises.md` 6 处残余“铁壁”。
2. **Round 2（2 路独立只读视觉与出版复验：`V4-XRev2-Web` & `V4-XRev2-Pub`）**：
   - `V4-XRev2-Pub` 正式裁决 **`0 P0 / 0 P1 PASS`**；
   - `V4-XRev2-Web` 确认此前全部 P0/P1 清零并捕获 1 项残余 P1（`glossary.html#term-*` 缺少 `scroll-margin-top`），当即在 `reader.css` 补齐 `scroll-margin-top: 92px` + `:target` 高亮、同步 `glossary.md` 导语 `106→151`，重建并在真实 Chrome 实测 `Cmd+K` 跳转 `#term-102` 稳定落点 `rectTop = 92.3px`（高于 68px 顶栏 `+24.3px`），达成全维度 **`0 P0 / 0 P1 PASS`**。
