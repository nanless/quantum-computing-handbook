# 离线阅读版与多格式出版工具链（V3）

正文源文件位于 `handbook/`，离线网页阅读版输出位于 `reader/`，合订本 PDF 与 EPUB 3 出版产物输出位于 `dist/`。整个 `reader/` 文件夹完整自包含（含本地 KaTeX 字体、预渲染公式、矢量图表、教学音频、配套代码与离线交互实验台），复制整目录后直接打开 `reader/index.html` 即可零依赖离线阅读，无需服务器或联网；不要只复制单个 HTML 文件。

## 快速构建与全套验收命令

在项目根目录运行：

```sh
# 1. 安装锁定依赖与 Chromium（首次或依赖变更时）
npm ci --prefix tools/reader --ignore-scripts --no-audit --no-fund
npm exec --prefix tools/reader -- playwright install chromium

# 2. 构建 V3 离线阅读版（含 5 篇 26 章路线、展厅首页、可折叠本章解答与离线实验台）
node tools/reader/build.mjs

# 3. 浏览器双宽全量验收（1440px / 390px、暗色模式、交互实验台、音频与 SVG 边界）
node tools/reader/verify.mjs

# 4. V3 全书质量与完整性门禁（公式定界符、术语统一、SVG 文本节点、26 章 271 题对齐）
node tools/reader/check-v3-quality.mjs

# 5. 专项算例与题答复核（或直接在仓库根目录运行 make check-all / make lint）
node tools/reader/check-network-examples.mjs
node tools/reader/check-qm-examples.mjs
node tools/reader/check-qm-review.mjs
```

仓库根目录已提供统一 `Makefile`（支持 `make test`、`make lint`、`make build`、`make verify`、`make pdf`、`make epub`、`make release`、`make check-all`），`tools/reader/package.json` 亦提供对应的 `npm run --prefix tools/reader <script>` 入口。PDF 后处理依赖锁定于 [`tools/reader/requirements-pdf.txt`](requirements-pdf.txt)（`PyMuPDF`、`pypdf`，可用 `make install-pdf` 安装）。

如需指定本机已安装的共享 Playwright 依赖或 Chromium 可执行文件，可传入环境变量 `HANDBOOK_NODE_MODULES` 与 `HANDBOOK_CHROMIUM`（切勿将本机绝对路径写入教材或仓库配置）。Mermaid 流程图在构建阶段通过仅绑定 `127.0.0.1` 的临时服务预渲染并缓存于 `work/render-cache/`，成品不依赖任何在线服务。

## V3 阅读版核心特性与五篇 26 章路线

- **五篇 26 章统一阅读序（`reading-order.mjs`）**：保持原章号 `00–21` 与物理基础篇 `Q1–Q4` 稳定不变，按教学依赖编排为五篇：
  1. **第一篇 · 入门、数学与量子态基础**：`00 → 01 → Q1 → 02 → Q2 → 03 → 04 → 05`
  2. **第二篇 · 核心算法、应用与实验实践**：`06 → 07 → 08 → 15`
  3. **第三篇 · 物理硬件、编译、纠错与系统工程**：`Q3 → 09 → 14 → 10 → 11 → 19`
  4. **第四篇 · 密码、网络与精密测量**：`12 → 20`
  5. **第五篇 · 信息理论、高级算法、模拟边界与计算模型**：`13 → 16 → 21 → 17 → Q4 → 18`
- **纸感制图桌双主题阅读体验（`reader.css` & `reader.js`）**：支持亮/暗模式手动切换（`#theme-toggle` + `localStorage` 持久化）与系统偏好自适应、顶部 2px 阅读进度条、右侧目录 ScrollSpy、四色语义 Callout 提示框、算例/练习标题微标、科学矢量图可见图注与原生 `<dialog>` 放大灯箱、代码块与行间公式（原始 TeX）一键复制、以及行内公式与后随标点防拆行胶水。
- **展厅级课程首页与零安装交互实验台**：`reader/index.html` 顶部集成三态量子干涉交互演示、四条读者路径与可验证科研闭环概览；构建同步发布离线交互实验台 `reader/lab/quantum-lab.html`。
- **可折叠本章参考解答**：构建期从 `handbook/appendices/exercises.md` 自动解析对应章节的零跳步推导，以默认折叠的 `<details>` 卡片注入每章末尾（打印时自动全部展开），不改变正文 `<article>` 的公式计数与哈希校验。
- **听觉实验增强**：每段 `.wav` 音频均配唯一无障碍 `aria-label`，全页互斥播放，并为 `labs/audio.html` 中的 Ramsey 双轨自动提供 `0.0s / 0.5s / 1.5s / 3.5s` 时刻快速跳转按钮。

## 多格式电子书出版（A4 PDF 与 EPUB 3）

在完成原稿更新后，可在项目根目录生成离线合订本 PDF 与原生 MathML EPUB 3：

```sh
# 构建带封面、页眉页码与 3 级 Unicode 书签的 A4 合订本 PDF -> dist/quantum-computing-handbook.pdf
node tools/reader/build-pdf.mjs

# 如需独立运行 PDF 后处理与 10 项出版质量门禁（元数据、3 级书签、内链、字形与体积检查）
python3 tools/reader/postprocess-pdf.py

# 构建原生 MathML 3 电子书 -> dist/quantum-computing-handbook.epub
node tools/reader/build-epub.mjs
```

- **A4 合订本 PDF 流水线（`build-pdf.mjs` + `postprocess-pdf.py`）**：零外网本地 KaTeX 预渲染与按块并行 Chrome 排版（`tagged: false`），经两遍构建探测精确正文页码并生成带右对齐页码的两栏目录，再由 PyMuPDF 原生合订、写入 `/PageLabels`（封面 `Cover` / 目录罗马页码 `i` 起 / 正文 `1` 起零偏移连续编号）与页眉页脚，生成 **3 级 Unicode 书签**与 **2,000+ 条精确内部跳转链接**，并执行 `/ToUnicode` CMap **康熙部首归一化**、字体子集化与流/SMask 去重无损压缩（成品稳定控制在 **`< 50 MiB`**，0 xref 损坏）。V4 后处理主动清空半残 `/StructTreeRoot` 与 `/MarkInfo`（避免误导屏幕阅读器，并在 `work/research/pdf-build-report.json` 通过 `noMisleadingPartialTagTree` 如实记录 `structTreeRoot: false`、`structParentsPages: 0`）；无障碍屏幕朗读请优先使用配套原生 MathML 3 EPUB 3 版本。
- **EPUB 3 电子书流水线（`build-epub.mjs`）**：输出原生 MathML 3 公式与矢量 SVG（完整收录 26 章正文、7 篇附录含附录 G 审校记录及 7 篇实验册），内置 EPUB Accessibility 1.1（`dcterms:conformsTo` 与 `schema.org`）元数据及 EPUB 2 NCX 兼容导航，由 Python 标准库打包为首条目无压缩 `mimetype` 的标准归档，并对全包 XML/XHTML/OPF/SVG 良构性及全部内部链接/锚点执行零报错门禁（报告写入 `work/research/epub-build-report.json`）。

> 浏览器“打印本章”仅作为单章便捷打印功能；正式合订本交付以 `build-pdf.mjs` + `postprocess-pdf.py` 及 `build-epub.mjs` 验收通过的 `dist/` 产物为准。

## GitHub Actions CI、Pages 与 Release 工作流

- `.github/workflows/ci.yml`：在 `push` 与 `pull_request` 时运行全套离线验收门禁（`python3 codes/run_all.py`、质量与隐私门禁、算例/题答复核、`build.mjs` 与 `verify.mjs`），显式安装 `fonts-noto-cjk` 与 `fonts-wqy-zenhei` 并缓存 Playwright 浏览器。
- `.github/workflows/pages.yml`：在主分支更新或手动触发时执行完整离线门禁与构建验证，收紧 `build` job 至只读权限，将 `reader/` 与带 GitHub Releases 入口的 `_pages/dist/index.html` 发布至 GitHub Pages。
- `.github/workflows/release-ebooks.yml`：在推送 `v*` 标签或手动触发时，统一调用 `tools/reader/build-release.mjs` 打包并校验全套 5 项发行产物（A4 PDF、EPUB 3、整站离线包 `*-web.zip`、自编离线代码复算包 `*-codes.zip` 与 `SHA256SUMS.txt`）并上传至 GitHub Releases。

## 验收报告、代码与历史检查说明

- **构建与浏览器验证报告**：仅写入 `work/research/reader-build-report.json` 与 `work/research/reader-verification.json`；V4 已停止向 `reader/research/` 复制内部日志与审校归档（`build.mjs` 构建前自动清理旧目录，`verify.mjs` 与 `build-release.mjs` 强制门禁校验 `reader/` 零 `research/` 与零 `STYLE.html`）。桌面/手机双宽页面、暗色模式、交互实验台与科学图截图保存于 `work/rendered/`。
- **验证覆盖范围**：包括全书所有生成页的 1440px / 390px 布局与溢出检查、源/输出与 `inputHashes`（含 `reader.js` 与 `quantum-lab.html`）SHA-256 核验、公式计数与 `mathSourceDigest`、标题序列与锚点、目录搜索与翻页顺序、`reader/lab/quantum-lab.html` 离线交互零报错、5 段 WAV 元数据与唯一 `aria-label`，以及全部 `handbook/assets/*.svg` 的 `getBBox()` 边界与亮/暗双色渲染检查。
- **质量与隐私门禁（`check-v3-quality.mjs`）**：校验全书面向读者的 Markdown（含 `audit-log.md`，不再豁免）零 `\(...\)` / `\[...\]`、零禁用旧术语（`参数偏移` / `玩具模型` / `左线性`）、统一采用“解码”（仅放行 `亦称译码`、`旧称译码`、`vendor` 原文）、全部科学 SVG 含真实 `<text>` 节点、26 章自检题数与 `exercises.md` 精确对齐（总计 271 题），以及 `handbook/`、`codes/`（排除 `vendor/`）与 `tools/reader/` 零本机绝对隐私路径泄露。
- **离线教学代码与音频**：运行 `python3 codes/run_all.py` 执行标准库数值脚本、第三方快照哈希核对与 5 段 WAV 格式检验，结果写入 `work/research/code-validation.json`。构建会复制 `codes/` 并仅改写本书自编说明中的教材相对链接，第三方 `vendor/` 字节原样保留。
- **浏览器收尾保护**：`browser-cleanup.mjs` 在保存报告后为浏览器退出设置 10 秒上限，防止部分 Chrome 版本的残留传输句柄阻塞进程，且不会改变检查失败状态。
- **历史轮次脚本退役说明**：早期已失效且会覆写历史归档 JSON 的 `check-round71/72/73.mjs` 与 `verify-round71/72/73-visuals.mjs` 已于 V4 清理下线；原始历史运行证据文件仍完整保留于 `work/research/round7*-*.json` 供追溯。自动截图不代替人工目视验收，实际人工抽查范围另行记录于审校报告。
