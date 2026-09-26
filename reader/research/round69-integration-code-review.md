# 第 69 轮集成代码交叉审查

日期：2026-09-26。只读审查主 agent 的 `tools/reader/build.mjs`、`codes/run_all.py`、`codes/snapshot_sources.py` 及新增实验文档链接；没有修改这些共享文件。只在 `/tmp` 对快照失败路径做无网络、无真实上游写入的模拟。另按主 agent 请求修复了本组图生成器的 SVG 顶部留白。

## 实际执行与通过项

- 新增 `handbook/labs/*.md` 与 `handbook/appendices/software-practice.md` 的 Markdown 本地目标检查：87 个链接目标，缺失 0。
- 当前阅读版 40 个 HTML 页面，以独立 HTMLParser 解析 a/img/audio/link：3933 个本地链接实例，文件和 HTML 锚点缺失均为 0。这个检查不等于检查网络URL或所有CSS内部字体URL。
- 阅读版 `reader/codes/vendor/` 的 46 个文件逐一计算 SHA-256，与正式 manifest 全部相同。复制未改第三方源码。
- build 对正文中的 codes 路径映射到 reader/codes，对已知 Markdown 页映射为相应 HTML；导航包含 labs，当前所有目录层级均为一层，相对前缀与生成布局一致。
- `.wav` 普通本地链接同时生成 audio 控件；原音频文件随 assets 一并复制。当前链接没有查询字符串，不受仅匹配结尾 `.wav` 的限制。
- run_all 仅运行自行编写的教学程序和 vendor 校验，不自动执行第三方源码；父进程明确拒绝 `-O`。子进程失败会在普通非零退出时累计到报告并最终返回失败。

## 发现 1：复制的自编 README 内部链接未重写

`reader/codes/algorithms/README.md`、`foundations/README.md`、`systems/README.md` 中仍有 `../../handbook/labs/*.md`。构建只处理 handbook 正文链接，而 codes 文件按字节复制，离线目录并不存在 reader/handbook，造成三个内部目标悬空。

这些不是正文 HTML 检查可以发现的链接，因此单独检查原始 README 很有必要。已向主 agent 报告；主 agent确认负责修复构建后的自编 Markdown 链接，保留 vendor 摘录不改。最终闭环应重新检查三个 README 实际目标，并保留第三方46文件哈希不变。

## 发现 2：离线副本统一运行入口的音频位置假设不成立

源码 `run_all.py` 由自身位置求 ROOT，然后固定读取 `ROOT/handbook/assets/audio/manifest.json`。复制到 reader/codes 后，实际音频在 `reader/assets/audio`，原路径不存在。静态路径存在性检查已实际核实。没有在主 agent 构建期间运行会写结果的 reader 副本，以免争用生成目录。

代码总 README 已说明主要运行入口是仓库根目录，故这不影响源码仓库的正确运行，但离线完整目录中的统一入口仍会在跑完程序后因音频路径失败，便携性不足。已向主 agent 报告；其确认负责兼容两种布局。最终闭环应从独立临时目录复制完整 reader 后运行统一入口，确保没有依赖仓库兄弟目录。

## 发现 3：未来刷新失败会使现有快照与 manifest 不一致

`--refresh` 在并行任务中直接向正式 vendor 目录写新许可证和源码；所有项目完成后才写新 manifest。虽然不会发布声称成功的新 manifest，但中途某项目失败时，已经覆盖的正式文件不会回滚，旧 manifest 将与现有字节不符。

在 `/tmp` 将 BASE 指向独立临时目录，准备旧 LICENSE 与其记录，mock git 返回固定40位提交、mock下载只返回新LICENSE而全部源码路径不存在。`refresh_project` 如预期报 `demo: no source paths found`；实际观察：旧 manifest 未变，LICENSE 字节已变。因此这是可复现的未来失败路径，不是对网络波动的猜测。

当前正式46文件哈希均正确，不影响本轮已取得的存档。已向主 agent 报告；建议将刷新写到同一文件系统上的临时快照目录，全部校验通过后再发布目录/manifest，或至少明确失败后应按旧 manifest 重新 --fetch 恢复。未再次下载任何上游仓库。

## 图形修复协作

主 agent 的浏览器 SVG 检查指出算法双面板总标题的字体边界越过 viewBox 顶部约2.08px，PNG肉眼检查未显现这一字体度量差异。本组已在 `codes/algorithms/generate_figure.py` 两个 savefig 添加 `bbox_inches='tight', pad_inches=0.22` 并实际重生成 SVG/PNG。已通知主 agent重新复制并执行浏览器边界检查；不能用首次 PNG 检查替代这次 SVG 实际字体边界验收。

## 边界

未修改共享构建/运行/存档脚本，未运行外部SDK，未下载额外代码。上述三个集成发现都已实时通知主 agent；修复后的最终构建与便携运行结果应以主线实际执行报告为准，不能把本报告的修复建议当成已通过的测试。

## 修复后复核闭环（同日追加）

主 agent 已修复以上三项；本段用实际执行结果替代前文的待验收状态。独立结果保存于 `round69-integration-fix-check.json`。

### 1. 离线原创 Markdown 链接

重读新构建逻辑：复制 codes 后，仅对不在 vendor 下的原创 `.md` 将可识别的 handbook 文档目标改写为相应阅读版 HTML。重新扫描全部原创代码 Markdown，7 个本地链接均存在；此前三个 `../../handbook/labs/*.md` 已指向可用的 labs HTML。同时再次逐一验证46份第三方代码的 SHA-256，全部符合 manifest，证明重写没有修改 vendor 摘录。

### 2. 独立目录内统一运行

`run_all.py` 优先使用仓库的 handbook/assets/audio，不存在时回退 assets/audio。为避免仅在当前仓库兄弟目录存在时偶然成功，另在 `/tmp` 创建独立目录，只复制最终 reader/codes 与 reader/assets/audio，没有复制 handbook 或仓库其他目录。在该目录实际运行 `python3 codes/run_all.py`，10个子程序入口全部 PASS，5份WAV校验通过，退出码0。独立目录内确实没有 handbook 子目录。这比仅检查回退路径更直接地验证便携运行。

### 3. 快照发布、失败保护与异常回滚

重新读取新实现：refresh/fetch 先在 BASE 下同文件系统的临时 next 目录准备文件，哈希验证和 manifest/README 写完后才发布；现有 vendor 先移到 previous，若第二次发布 rename 抛异常则移回。注释明确不能与构建并发；这里验证的是异常回滚，不声称两步rename是面对并发读者或断电的单步原子事务。

使用真实新脚本的 `main()`，仅 mock git输出、下载函数及指定的一次 rename 失败，所有状态放在 `/tmp`。共六种场景实际执行并断言：

| 场景 | 观察结果 | 验收 |
|---|---|---|
| 许可证成功、源码全部缺失 | 抛缺少源码异常，未调用rename | 旧目录全部文件及旧manifest逐文件哈希不变 |
| 下载函数中途抛异常 | 未调用rename | 旧目录及清单不变 |
| 全部成功 | 两次rename，提交更新为固定测试SHA，新文件和新清单通过verify | 旧哨兵文件消失，新源码出现；临时目录清理 |
| 第一次移走旧vendor失败 | 抛预设异常 | 旧目录及清单不变 |
| 第二次发布next失败 | 第三次rename将previous恢复为vendor | 旧目录所有字节及清单精确恢复 |
| --fetch下载字节与旧清单哈希不符 | 断言失败，未调用rename | 旧目录及清单不变 |

六种场景均通过；每种结束后都检查没有遗留 `.snapshot-*` 临时目录。没有请求任何网络或写正式 vendor。

**最终结论。** 三个报告问题已由主 agent 修复，并由本 agent 独立复核闭环；本次检查范围内没有未解决的链接、统一运行路径或上述异常回滚缺口。SVG顶部修复后的实际浏览器边界检查仍以主线图形报告为准。

## 可重复运行的离线回归测试

上述六场景现已整理为正式标准库 unittest 文件 `codes/tests/test_snapshot_sources.py`，不再只保留临时脚本与结果 JSON。运行命令：

```sh
python3 codes/tests/test_snapshot_sources.py
```

2026-09-26 实际执行：6 tests，全部 OK，退出码0；另外从 `/tmp` 用绝对脚本路径再次运行，六项仍全部通过，证明它不依赖仓库当前工作目录。

每项测试导入一份新的存档模块，将 BASE、MANIFEST、项目表定向到独立 TemporaryDirectory；下载函数和 git 查询被 mock，额外禁止真实 subprocess.check_output。文件写入与rename使用真实文件系统，但限定在该临时根下。失败保护通过比较包括 LICENSE、源码、README、manifest 和旧哨兵在内的完整文件树哈希验证；成功发布检查新提交、新内容、新清单和旧哨兵移除；回滚场景还验证第三次rename确实从previous恢复vendor。临时目录结束时清理，不触碰正式上游存档。

本次新增仅涉及该测试文件和本审查报告；统一 run_all 接入由主 agent 负责。
