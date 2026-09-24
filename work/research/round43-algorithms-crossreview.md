# 第 43 轮算法组交叉复核（只读）

日期：2026-09-23。范围限定为第 42 轮在 `handbook/06-algorithmic-primitives.md`、`07-algorithms.md`、`16-advanced-algorithms-verification.md`、`18-channels-capacities-complexity.md` 和 `handbook/appendices/exercises.md` 第 7、18 章答案中的新增内容。本轮未改正文，也未改 `sources/`。复核依据为原论文、作者论文正文与独立算术重算；结论不代表全书其余区域无误。

## P0 / P1

未发现。以下重点结论中的数学式、适用条件与示例数字均能复现。

## P2：随机码存在性证明可补最后一步常数

- 位置：`handbook/18-channels-capacities-complexity.md` 第 7.1 节，“由二项分布的集中界……并合界”一段。
- 发现：当前已正确给出单对坏事件概率 `2e^{-m/8}` 和不同输入对数 `<2^{2n-1}`，也正确说 `m=O(n)` 足够。但对希望自己核算的初学者，仍少了把两数相乘、解出一个明确线性长度的最后一步。这不是错误，而是本轮指定的“随机码概率界”算例还可更完整。
- 建议：在“并合界”后接 `\Pr(\exists\text{ 坏对})<2^{2n}e^{-m/8}`；取整数 `m>16n\ln 2` 即使右边小于 1，因此存在满足所有配对双侧距离的码。可点明合界不要求各配对事件互相独立。随后保留“存在性不等于高效编码”的现有提醒。
- 来源：[Buhrman 等原论文第 3 节](https://arxiv.org/html/quant-ph/0102001v1)直接给出随机 `\{\pm1\}` 指纹向量、Chernoff 界和配对合界；现稿用二元码字相位表示，令 `\delta=1/2` 后与论文构造等价。

## 可选的初学者微调（不构成缺陷）

- `handbook/06-algorithmic-primitives.md` 首次出现 `\oplus` 时，定义紧跟显示公式之后；可将“异或是模 2 加法”前置到公式之前。但现稿紧接真值表和常值函数反例，已足以独立理解，不必为了顺序单独重写。
- `handbook/16-advanced-algorithms-verification.md` 第 4.2 节可把 `U` 说明为“相干实现转移及逆操作的更新成本”，以免初学者把它理解成只随机抽取一个经典邻居的成本。现稿已有“可逆 Markov 链上的量子行走”和具体定理条件警告，因此不是错误。[Magniez 等原论文第 1.3 节](https://arxiv.org/html/quant-ph/0608026v4)明确按酉操作及其逆定义 `U`。

## 逐项核对记录

| 项目与位置 | 独立核对 | 结论 |
|---|---|---|
| 第 6 章第 1 节 XOR oracle | 固定 `x` 时 `y\mapsto y\oplus f(x)` 是二元集合置换，施加两次恢复 `y`；保留 `x` 后常值函数仍映成正交输出。 | 正确。 |
| 第 7 章第 3.3 节及第 7 章习题答案，`N=15,a=2` | 真阶 4；相位 `2/4=1/2` 给候选 2，`2^2\bmod15=4`，小倍数 `2\times2=4` 可经模幂验证；现稿明确没有把无界枚举误称多项式算法。 | 正确。 |
| 第 7 章第 3.4 节，`N=35,a=2` | 真阶 12；`2048/6=341.333…`，最近读数 341；`2^6\bmod35=29`、`2^{12}\bmod35=1`。`k` 与 12 互素的集合 `{1,5,7,11}` 也正确。第一个相位分支的显示概率重算为 `0.683918049…`，符合约 `0.684`。 | 正确。 |
| 第 16 章第 4.2 节量子行走 | 标准框架为 `S+O((U/\sqrt{\delta_{walk}}+C)/\sqrt\varepsilon)`，前提是相应 Markov 链及相干数据操作。代 `\varepsilon=1/16,\delta=1/4,S=10,C=3`，`U=2` 得 38，`U=20` 得 182；现稿限定为“成本尺度”，未宣称精确门数。 | 正确。[Magniez 等](https://arxiv.org/html/quant-ph/0608026v4) |
| 第 16 章第 5.5 节 QSP 相位桥 | `W(x)=xI+i\sqrt{1-x^2}X` 的本征值为 `e^{\pm i\arccos x}`；`W^2` 左上元为 `2x^2-1=T_2(x)`，`x=1/2` 得 `-1/2`。现稿已限定这是二维原型，未把特定反射次序的 qubitization 符号约定混为一谈。 | 正确。[Low–Chuang 原论文](https://quantum-journal.org/papers/q-2019-07-12-163/) |
| 第 18 章第 4.5 节 qubit 擦除信道 | 对任意输入 `\rho`，`S(B)=h_2(\varepsilon)+(1-\varepsilon)S(\rho)`、`S(RB)=h_2(\varepsilon)+\varepsilon S(\rho)`，故 `I_c=(1-2\varepsilon)S(\rho)`。可降解区 `\varepsilon\le1/2` 最大为 `1-2\varepsilon`；反降解区量子及私密容量为 0。正交位私密信息 `I(X:B)-I(X:E)=1-2\varepsilon`。第 18 章练习代 `\varepsilon=1/4` 得 `C=.75,Q=.5,P=.5,C_E=1.5`，单位和辅助资源说明均正确。 | 正确。[Bennett–DiVincenzo–Smolin](https://arxiv.org/abs/quant-ph/9701015)、[Devetak](https://arxiv.org/abs/quant-ph/0304127) |
| 第 18 章第 7.1 节相位指纹 | 相位指纹内积 `1-2\Delta`，双侧距离 `[1/4,3/4]` 推出模不超过 `1/2`；swap test 误报率至多 `5/8`，十次为 `0.009094947…`。单对坏事件 `2e^{-m/8}` 是 Hoeffding/Chernoff 界；与 `<2^{2n-1}` 对合并得到线性长度存在性。原论文第 2 节的码位值指纹只需单侧距离；其第 3 节另给与现稿相位指纹等价的随机符号向量构造，所以来源吻合。 | 正确；证明最后一步见上方 P2。[Buhrman 等第 2–3 节](https://arxiv.org/html/quant-ph/0102001v1) |

本轮没有发现要求立即修改的事实性或公式性错误。若后续选择处理唯一 P2，建议只补合界数值一步，不改当前双侧距离、模型前提或结论。
