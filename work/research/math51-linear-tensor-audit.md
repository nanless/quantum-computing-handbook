# 第 51 轮：数学工具章（向量至张量积）只读审稿

范围：`handbook/01-math.md` 第 2–7 节及对应的第 1 章练习答案。定位读者为“很久没有系统学数学”，故以下优先级以**能否跟着纸笔复算**为主，而不以研究生教材常见的简洁度为主。本轮不改正文。2026-09-23。

## 结论与优先级

未发现已写出的向量、内积、Hadamard 或张量积算式存在错号、错维度或位序计算错误。存在一处明确的定义遗漏，以及多处使初学者无法从定义独立算到结论的跳步。特别是现有参考书 Watrous 明言其预备章节**假定读者已了解基、维数等基础概念，且不提供证明**，因此不能靠末尾引用替代本章的逐步教学。[Watrous, Mathematical preliminaries, pp.1–5](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)。

### P1｜定义与推导顺序

1. **本征向量必须非零，现行定义遗漏条件。** 第 194–198 行写“若 $A|v\rangle=\lambda|v\rangle$，则 $|v\rangle$ 是本征向量”，零向量对任意 $\lambda$ 都满足这个等式，照字面会把所有数误判为本征值。改为“存在**非零**向量 $|v\rangle$ ……”，随即用 $X[x,y]^T=[y,x]^T=\lambda[x,y]^T$，推出 $y=\lambda x, x=\lambda y$、$\lambda^2=1$，再归一化得到 $|\pm\rangle$；不要只写“解得”。[MIT OCW 18.06, Lecture 21: Eigenvalues and eigenvectors](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-21-eigenvalues-and-eigenvectors/)。
2. **外积在谱分解中先用后定义。** 第 200、210 行已经出现 $|v\rangle\langle v|$，第 212 行才介绍外积，而且只说“是矩阵”。建议把外积移至谱分解前，先计算 $|0\rangle\langle0|=\left[\begin{smallmatrix}1&0\\0&0\end{smallmatrix}\right]$，再计算 $|+\rangle\langle+|=\tfrac12\left[\begin{smallmatrix}1&1\\1&1\end{smallmatrix}\right]$，点明外积的尺寸为“列数 × 行数”，用 $P^2=P$ 展示为何是投影。之后才讲 $X=|+\rangle\langle+|-|-\rangle\langle-|$，并把两矩阵完整相减验算为 $X$。[Watrous, 谱定理及迹](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)。
3. **“基”“线性组合”“张成”“完备”均未解释，正交归一公式缺桥梁。** 第 122–139 行直接从 $\langle e_j|e_k\rangle=\delta_{jk}$ 跳到“任何向量都可展开”。先用二维坐标 $[a,b]^T=a[1,0]^T+b[0,1]^T$ 解释一组基须能表示空间中**每个**向量；$\delta_{jk}$ 要解释“$j=k$ 为 1，否则为 0”。再在 $|+\rangle,|-\rangle$ 上逐项算 $\langle+|-\rangle=0$、两范数为 1、任意 $[a,b]^T$ 的新坐标 $(a+b)/\sqrt2,(a-b)/\sqrt2$。由对展开式左乘 $\langle e_k|$ 推出 $c_k=\langle e_k|\psi\rangle$，而非把公式直接宣告。提醒“正交归一”不自动“完备”：三维空间中两个正交单位向量仍非一组基。[Watrous, pp.3–5](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)；[MIT OCW 18.06 资源索引：基与维数](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/resource-index/)。
4. **矩阵的最基本运算尚不足以支撑表中的性质。** 第 143–158 行先给出厄米、酉、投影、正半定以及 POVM，读者只在后面的第 160–177 行看到一次矩阵乘列向量；尚无 $2\times2$ 矩阵乘矩阵、复共轭转置、$I$ 的具体形式或乘法次序示例。建议先给 $A=\left[\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right]$、$B=\left[\begin{smallmatrix}e&f\\g&h\end{smallmatrix}\right]$ 的行乘列规则，算一个有数字的 $AB$ 与 $BA$，再以 $H^\dagger H=H^2=I$ 的四格手算介绍酉。复矩阵 $\left[\begin{smallmatrix}1&i\\0&2\end{smallmatrix}\right]^\dagger=\left[\begin{smallmatrix}1&0\\-i&2\end{smallmatrix}\right]$ 可清楚区分 $T,* ,\dagger$。把 POVM/正半定放在这些基础之后作“往后会用到”的延伸阅读。[MIT OCW 18.06，矩阵乘法、逆矩阵与转置的课程顺序](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/readings/)；[Watrous, pp.6–15](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)。
5. **两比特矩阵缺完整 $4\times4$ 算例。** 第 262–274 行给了 $(H\otimes I)|01\rangle$ 的抽象规则，却未展示 $H\otimes I$ 的块矩阵如何来，也未按四维列乘算一次。写出 $H\otimes I=\tfrac1{\sqrt2}\left[\begin{smallmatrix}1&0&1&0\\0&1&0&1\\1&0&-1&0\\0&1&0&-1\end{smallmatrix}\right]$；第二列作用于 $|01\rangle=[0,1,0,0]^T$ 得 $[0,1,0,1]^T/\sqrt2$。并列 $I\otimes H$ 的四维形式，比较作用在哪个比特。这同时落实“维度相乘”和本书 $00,01,10,11$ 的位序。[MIT 8.05 Lecture 8, pp.1–3](https://ocw.mit.edu/courses/8-05-quantum-physics-ii-fall-2013/ffe665c0cba2eae19a83e88dec42925c_MIT8_05F13_Chap_08.pdf)。

### P2｜针对“数学生疏”需要的逐步桥梁

6. **bra–ket 里的符号变换太快。** 第 33–48 行应先标注 $2\times1$ 列、$1\times2$ 行、$1\times1$ 标量三种尺寸；把“转置 $T$”和“逐项复共轭 $*$”分别做，再得到 $\dagger$。用 $|u\rangle=[1,i]^T$ 算 $\langle u|=[1,-i]$、$\langle u|u\rangle=2$，并说明 $\langle\phi|\psi\rangle$ 与 $\langle\psi|\phi\rangle$ 互为共轭，不必相等。现有例子只给一对正交向量，对非零复内积的感觉不足。[Watrous, pp.3–4](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)。
7. **Cauchy–Schwarz 证明仅写“展开得”，而当前读者可能不会展开复内积。** 第 82–106 行建议设 $c=\langle u|v\rangle/\langle u|u\rangle$，逐项写出 $\langle v-cu|v-cu\rangle=\langle v|v\rangle-c\langle v|u\rangle-c^*\langle u|v\rangle+|c|^2\langle u|u\rangle$，再合并；配一对 $u=[1,0]^T,v=[1,1]^T$ 的直角图示或计算。若篇幅受限，把这段标为“进阶推导”，不要放在基和矩阵乘法之前形成主线阻塞。[Watrous, Cauchy–Schwarz](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)。
8. **酉矩阵只证明保持一个态的总范数，缺从定义到可逆/保内积的演算。** 第 179–190 行可以用两任意态写 $\langle U\phi|U\psi\rangle=\langle\phi|U^\dagger U|\psi\rangle=\langle\phi|\psi\rangle$，再把 $U^{-1}=U^\dagger$ 以 $2\times2$ 的 $H$ 验算。避免“酉 = 每个概率分量不变”的误读：$H|0\rangle=|+\rangle$ 改变了计算基中各结果的概率，守恒的是总和。[Watrous, unitary operators](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)。
9. **外积、迹和密度矩阵完全没有数值算例。** 第 212–221 行建议 $|\psi\rangle=(|0\rangle+i|1\rangle)/\sqrt2$：算出 $\rho=\tfrac12\left[\begin{smallmatrix}1&-i\\i&1\end{smallmatrix}\right]$，然后逐行核对 $\rho^\dagger=\rho$、$\operatorname{Tr}\rho=1$、$\rho^2=\rho$；再用 $A=|0\rangle\langle0|$ 算 $\operatorname{Tr}(A\rho)=1/2$，与概率对应。迹的循环性可取两个简单数值矩阵各算 $AB,BA$ 的对角线，提醒循环换位不是任意调序。[Watrous, trace identities](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)。
10. **张量积只有一个含 $|+\rangle$ 的因式例子，没说明线性与“不是所有双系统态都可拆开”。** 第 223–259 行先用两组普通分量 $[a_0,a_1]^T$、$[b_0,b_1]^T$ 手排四项，逐行解释 $|a\rangle\otimes|b\rangle$ 为何按 $00,01,10,11$；再用复数算 $([1,i]^T/\sqrt2)\otimes([1,1]^T/\sqrt2)=[1,1,i,i]^T/2$ 和范数平方。最后指出 $|00\rangle+|11\rangle$ 不能写为单个 $|a\rangle\otimes|b\rangle$（因若两端项非零则中间两项至少无法同时为零），否则容易把“张量积空间中的向量”误以为“必然是乘积态”。[MIT 8.05 Lecture 8, pp.1–2](https://ocw.mit.edu/courses/8-05-quantum-physics-ii-fall-2013/ffe665c0cba2eae19a83e88dec42925c_MIT8_05F13_Chap_08.pdf)。
11. **正半定示例紧挨定义却不给为何特征值是 $0,2$ 的可算路径。** 第 152–158 行既然保留例子，可写 $\det(A-\lambda I)=\lambda(\lambda-2)$，或者待本征值一节后按 $A=|v\rangle\langle v|$ 直接构造更直观的正半定例子；把“含复非对角元仍可正半定”保留为进阶例，而不是读者第一次接触矩阵的第一例。[Watrous, spectral theorem and positive semidefinite operators](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)。
12. **基变换的“同一态不同坐标”没有双向核算。** 第 135–139 行目前只给 $|0\rangle=(|+\rangle+|-\rangle)/\sqrt2$。建议选 $|\psi\rangle=(|0\rangle+i|1\rangle)/\sqrt2$，用内积算新坐标 $c_+=(1+i)/2,c_-=(1-i)/2$，再带回并验算两个基中的概率各自和为 1；这样为后文“相对相位可测”搭桥。[Watrous, orthonormal bases and measurement basis](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)。

### P3｜编排、图与练习

13. 第 74 行 $[1,1+i]^T$ 的 $T$ 直到第 10 节才间接出现；第一次出现时明确“上标 $T$ 把横排写法转为列”，并与 $\dagger$ 区分。
14. 设计一张统一的“对象尺寸与运算”图：$|v\rangle$ 为 $2\times1$，$\langle v|$ 为 $1\times2$，$\langle v|v\rangle$ 为数，$|v\rangle\langle v|$ 为 $2\times2$，两个量子比特的态为 $4\times1$，单比特算符的张量积为 $4\times4$。这比只画抽象箭头更能帮助初学者自查维度。
15. 第 1 章仅有 6 道自检，其中“基变换、复共轭转置、$2\times2$ 矩阵乘法、本征解、外积迹、$4\times4$ 张量算符”没有独立练习。每个新增台阶配一道**带完整答案**的小题；先填空式分步练习，再整题。当前第 3 题的 $H^\dagger H$ 只在答案中展示，核心教学应进入正文。错解示范可选“把 $[1,i]^T$ 的 bra 误写为 $[1,i]$”和“交换两比特但不交换矩阵行列”。

## 推荐修订顺序与验收线

建议按“二维列向量与复数内积 → 归一化 → 基与新坐标 → 矩阵乘法/伴随 → 外积/投影 → 本征解/谱分解 → 迹/密度矩阵 → 向量与矩阵的张量积”重排。Cauchy–Schwarz 和正半定的完整证明可做二层阅读，不阻断主线。验收时让没有预习的读者只凭正文独立完成以下四件事：求一个复向量的 bra 与范数；将 $[a,b]^T$ 改写成 $|\pm\rangle$ 基坐标；把 $X$ 的两个外积逐格相减还原矩阵；写出并乘一次 $H\otimes I$ 的 $4\times4$ 矩阵。四件中任一仍需翻别章或猜步骤，则本轮不算“讲细”。

## 核查边界

上述材料是对第 2–7 节的编辑性和数学审稿，不等于审完第 1 章的概率、复杂度部分。网页资料均来自作者教材、MIT 开放课程或官方量子教学页；未使用二手博客替代数学结论。[IBM Quantum Learning：多系统与张量积](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/multiple-systems/quantum-information)。
