# 数学工具章第 52 轮：复数与概率补写

范围：只修改 `handbook/01-math.md` 的 §1 与 §8。未改导语、§2–7、§9、章末题、附录、`reader/` 或 `sources/`。依据第 51 轮只读审稿 `math51-complex-probability-audit.md`，将“先给抽象公式”改为“先有对象和手算，后抽象公式”。

## §1 的调整

- 先定义 `i²=-1` 与复数的实、虚两个实数分量；给复数加减法、乘法以及共轭相乘的逐行算例。
- 用 `1/(1+i)` 示范分子、分母同乘共轭，说明分母转为实数的理由。
- 从复平面的点 `(a,b)` 和勾股关系定义模，再用 `1+i` 给出 `√2` 与 `π/4`；说明弧度、象限、相位模 `2π`，以及零复数没有唯一相位。
- 将 `r(cosθ+i sinθ)` 接到 Euler 写法 `re^{iθ}`；以 `(1+i)(1-i)=2` 核验乘法时长度相乘、角度相加。复数指数暂作可计算记号，不预设微积分。
- 用一对归一化复振幅 `(1±i)/2` 分别算模平方与总概率，并明确 Born 规则是量子测量公设，不是复数代数定理；末尾给即时自测和答案。

## §8 的调整

- 从样本空间与事件开始，区分等可能个数法和一般概率相加；用完整的 100 人 `A/非 A`、`阳性/阴性` 四格计数表让条件概率的分母可见。
- 并列算 `Pr(A|+)=16/24=2/3` 与 `Pr(+|A)=16/20=4/5`，再由同一联合事件两种拆法推 Bayes 公式，使用互斥两组求阳性总概率 `24/100`。保留“经典记录更新”与“量子测量物理作用”的区别。
- 定义 `0/1` 随机变量、概率表、期望、`f(X)` 与求和记号；使用 `p=1/4` 的例子逐项算 `E[X]`、`E[X²]`。
- 从平方偏差引入方差和标准差，逐项展开 `Var(X)=E[X²]-(E[X])²`，再推出单次 Bernoulli 方差 `p(1-p)`。
- 令成功频率 `\hat p=(X_1+⋯+X_N)/N`，解释独立性如何令交叉项的期望为零，推得 `Var(\hat p)=p(1-p)/N`；用 `p=1/4,N=100` 区分计数标准差约 4.33 次与频率标准差约 4.33 个百分点。明确标准差不是绝对界，相关、漂移或选择样本会使公式不适用。
- 将原有 `Z` 测量期望例子补上“两个读数加权平均”和矩阵式交叉核对；末尾给条件概率与频率标准差即时自测。

## 逐式核验

人工展开了复数乘法、共轭和除法；计算了 Bayes 四格表各边际和；用独立数值计算核查 `Pr(+)=0.24`、`Pr(A|+)=2/3`、`sd(S)=4.3301270189`、`sd(\hat p)=0.0433012702`。引用 [OpenStax《Precalculus 2e》复数四则](https://openstax.org/books/precalculus-2e/pages/3-1-complex-numbers)、[极坐标](https://openstax.org/books/precalculus-2e/pages/8-5-polar-form-of-complex-numbers)、[MIT OpenCourseWare 复数指数](https://ocw.mit.edu/courses/es-1803-differential-equations-spring-2024/mites_1803_s24_topic4.pdf)、[OpenStax 概率公式](https://openstax.org/books/introductory-statistics-2e/pages/3-formula-review)、[期望与标准差](https://openstax.org/books/introductory-statistics-2e/pages/4-2-mean-or-expected-value-and-standard-deviation)、[样本比例方差](https://openstax.org/books/introductory-business-statistics-2e/pages/7-3-the-central-limit-theorem-for-proportions)核对通式与边界。

§1 的复平面图由并行作图代理处理；本轮没有加入一个尚不存在的图像链接。整页公式渲染、移动端检查与通篇交叉复核由总审统一执行；本报告不预称这些步骤已完成。

第 53 轮交叉审指出方差恒等式从展开到分项期望时，最好让久未学习数学的读者看到“加权平均可先逐项算再相加”的理由；已在 §8 对应公式前补上一句，不改变结果。
