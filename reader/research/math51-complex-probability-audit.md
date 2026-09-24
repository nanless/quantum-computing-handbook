# 数学工具章第 51 轮只读审稿：复数与概率

范围：`handbook/01-math.md` 第 1–29、108–118、276–327、369–378 行；参照 `handbook/appendices/prerequisites.md` 的先修自测与 `handbook/appendices/exercises.md` 的第 1 章答案。对象是高中数学多年未用、需要重新建立操作感的读者。本轮未编辑正文、`reader/` 或 `sources/`。

## 判定

没有发现现有公式的确定性数学错误；问题主要是**顺序过快**和**只有结论没有带数字的演算**。现稿对已经记得复数和平面概率的人是提要，对用户指定的读者不是可独立学习的数学工具章。P0：无。P1：3 项。P2：6 项。P3：2 项。

## P1：必须补足的学习断层

1. **复数的入门操作被跳过（第 9–17 行）。** 第一段同时给 `i²=-1`、共轭、模、极坐标、Euler，未说实部和虚部是什么、为何出现 `i`、如何加减乘除，也没有将 `z^*z` 展开为 `a²+b²`。读者会照抄第 21–27 行，却不能独立处理 `(1+i)/(1-i)`。建议顺序：`i²=-1` → `a+bi` 的两个实数坐标 → 加减按同类项、乘法用分配律和 `i²=-1` → 共轭及 `zz*=a²+b²` → 分母有复数时乘共轭 → 模。每一步保留一个两行以内的手算，例如 `(1+2i)+(3-i)=4+i`、`(1+i)(1-i)=2`、`1/(1+i)=(1-i)/2`。之后再接相位。OpenStax 的预备数学教材也先处理四则和共轭，再单列极坐标形式。[依据：OpenStax §3.1](https://openstax.org/books/precalculus-2e/pages/3-1-complex-numbers)、[§8.5](https://openstax.org/books/precalculus-2e/pages/8-5-polar-form-of-complex-numbers)。

2. **几何相位从公式直接跳到抽象句（第 11–17 行；第 108–118 行）。** 未给复平面坐标图或文字坐标表，未解释 `r=|z|` 是从原点到 `(a,b)` 的距离、`θ` 从正实轴量起、`a=r cos θ` 与 `b=r sin θ`，故 `e^{iθ}` 看来像凭空引入的新符号。建议以 `z=1+i` 完整走一遍：点 `(1,1)`、`r=√2`、`θ=π/4`、`z=√2(cos π/4+i sin π/4)=√2e^{iπ/4}`；附四象限小图，说明 `θ` 与 `θ+2πk` 等价、`z=0` 没有唯一相位。再用 `e^{iφ}z` 的例子呈现“模不变、角度加 `φ`”，最后接量子态的全局/相对相位，以免把平面旋转与物理可测性混淆。[依据：OpenStax §8.5](https://openstax.org/books/precalculus-2e/pages/8-5-polar-form-of-complex-numbers)。

3. **概率段落没有一条从样本空间到 Bayes 的手算主线（第 278–296 行）。** 第一式是 `E[f(X)]`，可读作“期望”，但 `X`、`x`、`p(x)`、`f` 均未先落到具体表格；随后 `A∩B` 也未解释，且 Bayes 分母 `Pr(B)` 需要分情况求和。第 375 行才有筛查题，答案在另一页，不足以支撑独学。建议先做一张 100 人计数表：20 人属 `A`，其中 16 人阳性；80 人不属 `A`，其中 8 人阳性。边读表边得到 `Pr(A∩+)=16/100`、`Pr(+)=24/100`、`Pr(A|+)=16/24=2/3`，再写 `Pr(+|A)Pr(A)/[Pr(+|A)Pr(A)+Pr(+|¬A)Pr(¬A)]`。刻意并排 `Pr(A|+)` 和 `Pr(+|A)`，不能把二者倒置。再做现有第 375 行低基率练习。OpenStax 明确从样本空间、事件和缩小分母解释条件概率；其公式回顾也列出联合概率的两种分解。[依据：OpenStax 概率术语](https://openstax.org/books/introductory-statistics-2e/pages/3-1-terminology)、[公式回顾](https://openstax.org/books/introductory-statistics-2e/pages/3-formula-review)、[列联表](https://openstax.org/books/introductory-statistics-2e/pages/3-4-contingency-tables)。

## P2：局部跳步、边界和可教学性

4. **第 5 行“100 次平均 25 次”易被读成“每一批的经验平均”。** 现句最后已说明不能保证，数学上正确，但建议先定义单次成功指示量 `Y=1/0`，再区分理论期望 `E[S]=25` 和一次实验的实际计数 `S`；暂不必在导语里写符号，可改为“若反复做很多批，每批成功次数的平均会接近 25”。后续第 8 节再正式推导。

5. **第 21–29 行只展示模平方，没有同时展示归一化和不同相位可对应同一概率。** 现例 `(1+i)/2` 模平方 `1/2` 正确。可补另一振幅 `(1-i)/2`，同样给 `1/2`；给两个结果的振幅 `((1+i)/2,(1-i)/2)`，验证 `1/2+1/2=1`，将“单个非负数”连到“完整概率分布”，但须写明量子测量规则是在后章引入的物理规则，不能由复数代数独自推出。

6. **第 108–118 行全局相位虽然证明正确，但相对相位只靠交叉引用。** 给零基础读者一个两行的可观测对照：`|+⟩=(1,1)^T/√2` 和 `|−⟩=(1,-1)^T/√2` 的计算基概率都为各半；再按本章已有 `H` 算 `H|+⟩=|0⟩`、`H|−⟩=|1⟩`。将共同乘 `i` 与只改第二项符号并列。此处若跨到第 4 节的 `H`，可注明“学完矩阵一节回看”。

7. **第 278–280 行先给 `E[f(X)]`，再一直没有一个 `f(X)` 的数值例子。** 应先定义随机变量：把每次试验的结果编号成数字；给一个二结果表 `X∈{0,1}`、概率 `{3/4,1/4}`，逐项算 `E[X]=0×3/4+1×1/4=1/4`；再说明若 `f(X)=X²`，这里 `E[X²]=1/4`。等熟悉后才抽象成求和式。可以直接连接第 319–327 行的 `Z∈{+1,-1}` 例子，显式指出“`E[Z]` 是加权平均，不要求等于某次可能的读数”。[依据：OpenStax 期望与标准差](https://openstax.org/books/introductory-statistics-2e/pages/4-2-mean-or-expected-value-and-standard-deviation)。

8. **第 298–313 行方差恒等式与样本频率方差均无中间步骤。** 建议先对一个 `X∈{0,1}`、`p=1/4` 手算 `E[X]=1/4`、`E[X²]=1/4`、`Var(X)=1/4-(1/4)²=3/16`。下一行写 `\hat p=(X_1+⋯+X_N)/N`，说明“独立”时 `Var(X_1+⋯+X_N)=ΣVar(X_j)`，再逐步得 `Var(\hat p)=N p(1-p)/N²=p(1-p)/N`。给 `p=1/4,N=100`，标准差 `√(3/1600)=√3/40≈0.0433`（成功次数标准差 `≈4.33`）；避免把 0.0433 误读为计数单位。[依据：OpenStax 样本比例](https://openstax.org/books/introductory-business-statistics-2e/pages/7-3-the-central-limit-theorem-for-proportions)。

9. **第 305–310 行“Bernoulli”“sd”首次出现未释义。** 说明 Bernoulli 试验是每次仅成功/失败两个结果、成功率固定 `p`；`sd` 是标准差 `√Var`；不同轮次独立是该公式的前提。单次 `X²=X` 导出 `Var(X)=p(1-p)` 是最短的手算桥梁。已在先修自测中提醒漂移/相关会破坏公式，可把提醒在正文就地放一次。

## P3：低成本体验改善

10. **第 9–17 行建议图形与文字互补。** 一个简单复平面（水平“实部”、竖直“虚部”、`1+i` 的坐标、半径 `√2`、角 `π/4`）比单独 Euler 公式更适合断档读者；图注还应写出该图只解释单个复数，不直接解释量子比特的 Bloch 球。

11. **第 369–378 行自检缺中间台阶。** 当前第 5 题直接是低基率筛查；在此之前可添两道各 20 秒的题：算 `(2+i)(2-i)`，以及“100 人中 30 人有 `A`，其中 12 人又有 `B`，求 `Pr(B|A)`”；答案写出分母选 30 而非 100。现有筛查题保留为进阶。

## 建议正文重排（不扩大后续章节负担）

- §1 分成“`i` 与复数的两分量”→“四则/共轭/模”→“复平面的长度与角度”→“Euler 记号”→“振幅模平方”五个短层次；每层一个数字算例，至少一张坐标小图。
- §8 分成“事件和随机变量”→“列概率表及期望”→“条件概率先缩小样本空间”→“联合概率和 Bayes 的人数表”→“方差/标准差”→“独立重复和样本频率”→“量子测量的期望”。先具体再符号化，不必为初学者删去公式。
- 可在两节开头各放一句“学完你能手算什么”，各结尾给两道即时核对题，完整答案留在习题附录。

## 权威资料核对记录

对照 OpenStax 官方《Precalculus 2e》[§3.1](https://openstax.org/books/precalculus-2e/pages/3-1-complex-numbers) 与 [§8.5](https://openstax.org/books/precalculus-2e/pages/8-5-polar-form-of-complex-numbers)，现稿复数共轭、模、极坐标式正确；[MIT OpenCourseWare 复数与指数讲义](https://ocw.mit.edu/courses/es-1803-differential-equations-spring-2024/mites_1803_s24_topic4.pdf)确认 Euler 式。它缺的是教材先行铺垫的运算与几何坐标。对照 OpenStax 官方《Introductory Statistics 2e》[概率公式](https://openstax.org/books/introductory-statistics-2e/pages/3-formula-review)、[期望与方差](https://openstax.org/books/introductory-statistics-2e/pages/4-2-mean-or-expected-value-and-standard-deviation)及《Introductory Business Statistics 2e》[样本比例](https://openstax.org/books/introductory-business-statistics-2e/pages/7-3-the-central-limit-theorem-for-proportions)，现稿条件概率、Bayes、方差和独立 Bernoulli 样本比例方差公式正确。后者是**独立且同概率**二值观测的精确方差式，而不是所有计数数据的通用误差式。资料用于逐式核查和教学顺序参照，未复制教材行文。
