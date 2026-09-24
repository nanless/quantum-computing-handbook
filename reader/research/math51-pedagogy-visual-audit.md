# 第 51 轮｜数学工具章的初学者路径与图解审稿（只读）

范围：`handbook/01-math.md`、`handbook/appendices/prerequisites.md`、`handbook/appendices/exercises.md` 第 1 章、`handbook/02-single-qubit.md` 前六节，以及 `reader/01-math.html` 的现有结构。此轮只提出修改建议，未改正文、读本或附录。优先级 P1 表示会直接阻碍“多年未系统看数学”的读者顺畅走到第 02 章；P2 表示显著降低可学性；P3 是精修建议。抽查的公式未发现需要作为 P0/P1 数学错误处理的问题。

## P1：承诺的“高中数学起步”与真实学习台阶不一致

章首让高中基础读者学完第 1–4、7–8 节再读 Q1，但第 2 节在第一次出现复数内积后立即给出 Cauchy–Schwarz 的抽象正交分解证明；第 4 节在一次矩阵乘法之前集中给出厄米、酉、投影、正半定四个定义及复矩阵本征值反例。对目标读者，最急需的是“复数模平方—两个振幅—行乘列—两种测量基”，而非先证明内积不等式或判定正半定。这不是内容不该有，而是主线和加深层混在一起。IBM 的基础课以基本线性代数和复数为推荐背景，并先用单系统态向量、矩阵、测量建立计算，再在更一般的课程讲密度矩阵；这支持分层讲解，不能据此声称本书必须照搬 IBM 的目录。[IBM 基础课概览](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information)、[IBM 单系统量子信息](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/quantum-information)、[IBM 密度矩阵导论](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/introduction)。

建议在章首增加明确的两层阅读路线，标出“直达第 02 章的必读小节”和“第 05 章/量子力学 Q2 用到时回看”的小节。Cauchy–Schwarz、复矩阵正半定与谱分解可保留完整证明，但移入带标题的“进阶回看”小节，或在主线前给出一句“暂可跳过”。不宜删去严格性；应降低第一次经过时的门槛。

## P1：符号转换过快，缺少最小的“逐格”演算链

第 1 节从 $a+bi$ 直接跳到 $re^{i\theta}$ 与 Euler 公式，没有讲 $r=\sqrt{a^2+b^2}$、$\cos\theta=a/r$、$\sin\theta=b/r$ 在象限中的含义，也没有拿 $1+i$ 走完直角坐标、极坐标、共轭、模平方四步。第 2 节虽展示 bra/ket 和归一化，但没有先用一个实二维向量解释行乘列、长度平方、为什么左边要先变成行；随后 $\langle u|v\rangle$ 的含 $i$ 计算对久未看数学者仍跨度大。第 3 节给出 $c_j=\langle e_j|\psi\rangle$ 和 $|0\rangle=(|+\rangle+|-\rangle)/\sqrt2$，没有把具体态的两套坐标和两套测量概率逐项并排算出。第 6 节外积与迹只有定义和恒等式，没有任何 $2\times2$ 数字演算；第 5 节“解 $X|v\rangle=\lambda|v\rangle$ 得”跳过了求解过程。

建议贯穿同一个简单态（例如 $(|0\rangle+i|1\rangle)/\sqrt2$），从复数乘法、列向量转 bra、$\langle\psi|\psi\rangle$、矩阵乘向量、$|+\rangle$ 基投影、外积矩阵到迹，按“写出每个分量→代数运算→检验物理含义”走完；另以 $X$ 手算 $\det(X-\lambda I)=0$、解两个线性方程、归一化本征向量，并把 $|+\rangle\langle+|$ 写成具体 $2\times2$ 矩阵。IBM 单系统课程确实并列展示列向量、Dirac 记号、振幅模平方的数值例子，MIT 18.06 的本征值课明确以矩阵如何改变向量为入口。[IBM 单系统例题](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/quantum-information)、[MIT 18.06 本征值课](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-21-eigenvalues-and-eigenvectors/)。

## P2：概率节公式正确，但初学者缺少“分母、样本、条件”的手算场景

第 8 节写出条件概率、Bayes、期望、方差及二项频率标准差，却只有 $Z$ 期望值算例；没有在本章逐步手算“100 人筛选→真阳性/假阳性→阳性中有病比例”，也未拆开 $\hat p=(X_1+\cdots+X_N)/N$ 为何带来 $p(1-p)/N$。第 1 章自检有 Bayes 题，答案附录给出结果；先修页也有条件频率及有限采样题，但数学正文读者必须离开此页才能看到完整场景。建议正文增加一个人数表或树状流程，逐行固定分母；统计误差公式至少说明 $X_i\in\{0,1\}$、独立同分布、$\operatorname{Var}(X_i)=p(1-p)$ 与相加除以 $N^2$，并明确“标准差不是一次运行的确定误差上界”。MIT 的概率课程把条件概率/Bayes 作为单独讲次，配有例题和练习，说明这一概念需要独立练习空间。[MIT 6.041SC 资源索引](https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/pages/resource-index/)。

## P2：矩阵、外积、张量积有“结果”，欠缺可以照着重算的形状检查

第 4 节 Hadamard 乘 $|0\rangle$ 的说明好，但没有先给 $2\times2$ 乘 $2\times1$ 的一般形状、两矩阵连乘为何最右先作用，以及 $A^T$、$A^*$、$A^\dagger$ 的逐格对照。第 7 节给出两个向量的张量积和 $(H\otimes I)|01\rangle$ 的分配律，未列 $H\otimes I$ 的 $4\times4$ 分块矩阵供核查；第 1 章练习 3 直接要求证明 $H$ 酉，答案跳过 $H^2$ 的四个格子。建议加一个“形状检查”窄表（输入、操作、输出尺寸）、一个 $H\otimes I$ 的分块矩阵，并补“从右向左”两门例子。IBM 多系统课程用元素顺序和矩阵张量积的具体式子验证 $(M\otimes N)(|\phi\rangle\otimes|\psi\rangle)$，与此建议的逐格校验一致。[IBM 多系统：经典信息](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/multiple-systems/classical-information)。

## P2：视觉解释明显少于符号密度

生成的 `reader/01-math.html` 中没有任何 `<figure>` 或 `<img>`；仅有两张表。第 01 章是全书后续公式的入口，读者反复面对纯文本公式而没有“代数对象怎样变形”的静态辅助图。建议至少做两幅**与正文步骤逐项对应**、不依赖颜色的 SVG：① 一张 2×2 行列格展示“共轭→行乘列→模平方→概率”，每条箭头标上实际数字；② 一张两比特基位序与张量积四行位置图（左列 $|a\rangle$ 的两个分量，右列 $|b\rangle$ 的两个分量，输出 $00,01,10,11$）。图应有文字说明且手机横向可读，而不只是装饰。若版面只能容纳一张，优先第一张，因为它连接本章最多概念。可以另用概率树解释条件概率，但请勿把“图”替代旁边的分母计算。

## P2：练习缺少中途检查和难度阶梯

第 1 章的 6 道自检全在末尾，覆盖归一化、张量积、酉矩阵、期望、Bayes、复杂度，却没有共轭转置、两基坐标展开、外积/迹、本征向量的低门槛题；也没有每两节即可核对的 10–30 秒小题。对“多年没看数学”的用户，建议每节后放一题“自己暂停算一格”，下行给折叠或附录答案；章末按“会算→会解释→会迁移”三级列题，保留现有综合题。尤其增加 $(1+i)^*$、$(1+i)(1-i)$、$\langle+|\psi\rangle$、$|0\rangle\langle1|$ 与 $H|1\rangle$ 的最短题。先修页 7 题已经是好的分流工具，不必复制；数学章应补**学习过程中的即时反馈**。

## P3：概念边界与术语表联动

- 第 4 节“投影 $P=P^\dagger=P^2$”可在第一次出现时加一句“它把向量留在某个方向或子空间，并丢掉与之垂直的部分”，避免把“投影测量”当作与日常投影完全相同的操作。
- 第 5 节“本征值/特征值”双称谓处理得好；可在术语表与符号表补对应索引，标明 $\dagger$ 是“先共轭再转置”，不同于单独的 $*$ 或 $T$。数学章中的 “bra/ket”“厄米”“正半定”目前解释偏操作定义，缺一句白话作用。
- 第 9 节的 $O,\Omega,\Theta,o$、oracle、一致电路族、承诺问题等信息很重要，但对只想去第 02 章的读者是高认知负荷。应明显标为“到算法篇再读”，或拆成附页，保留本章目录跳转。

## 建议的验收方式

1. 请一个只会高中复数和基本概率的读者不翻附录，完成“给 $(1+i,1-i)^T$ 求归一化、$H$ 作用、在 $|+\rangle$ 基算概率”；每一步所需规则都应在本章此前由一组数字示范。
2. 请读者指出 $A^T,A^*,A^\dagger$ 的区别，写出 $|0\rangle\langle1|$ 的四格以及 $H\otimes I$ 的四行；若不会，应能回到正文对应的逐格例题，而非只找到定义。
3. 在 390px 阅读宽度核对新 SVG 的图题、箭头、公式和顺序，不出现整图压缩成 5px 字或页面全局横向滚动。
4. 对改后的第 01 章做一次交叉审稿：是否把本章从“数学课本”变成清楚的**学习路线**，并确保严格性仍可按需逐步找回。
