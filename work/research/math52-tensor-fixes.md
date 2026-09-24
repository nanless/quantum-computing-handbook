# 第 52 轮：数学工具章 §7 张量积修订

2026-09-23。仅修改 `handbook/01-math.md` 的第 7 节，未碰其他节、附录、读本生成物或 `sources/`。

## 对照一手资料

- [MIT OCW 8.05 Quantum Physics II, Lecture Notes 8](https://ocw.mit.edu/courses/8-05-quantum-physics-ii-fall-2013/ffe665c0cba2eae19a83e88dec42925c_MIT8_05F13_Chap_08.pdf)，第 1–3 页：张量积的分配律、维度相乘、$(T\otimes S)(v\otimes w)=Tv\otimes Sw$；据此核对正文按分量展开与算符作用顺序。
- [Watrous, *The Theory of Quantum Information*, Mathematical preliminaries](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)，第 2–3 页：复向量张量积的分量定义以及 $00,01,10,11$ 顺序；第 4–8 页：算符的张量积及其矩阵表示。
- [IBM Quantum Learning, Multiple Systems: Classical Information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/multiple-systems/classical-information) 与 [Quantum Information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/multiple-systems/quantum-information)：基串次序、不同软件编号约定、复合系统的态及张量算符。正文明确沿用本书左边为第一个比特的约定，不照搬某一软件的字符串习惯。

## 修改点

1. 从 $(a_0|0\rangle+a_1|1\rangle)\otimes(b_0|0\rangle+b_1|1\rangle)$ 的分配律逐项得到四个振幅，解释 $2\times2=4$ 的维度与每个位置的标签。
2. 在原 $|+\rangle\otimes|1\rangle$ 例子之后加复数乘积态 $([1,i]^T/\sqrt2)\otimes([1,1]^T/\sqrt2)=[1,1,i,i]^T/2$，把四个模平方加回 1；加一条即时核对 $|1\rangle\otimes|+\rangle$，避免以为次序可交换。
3. 把 $H\otimes I$ 展成 $\tfrac1{\sqrt2}\left[\begin{smallmatrix}I&I\\I&-I\end{smallmatrix}\right]$，再逐格展成 $4\times4$ 矩阵；列出四列各自对应的基输入与输出。保留原有抽象规则，再用第二列和 $|01\rangle$ 复核结果。
4. 并列 $I\otimes H$ 的 $4\times4$ 矩阵，解释零矩阵块，计算同一个输入 $|01\rangle$ 的不同输出。再加 $|10\rangle$ 的即时核对，强化“左/右比特”与列序。
5. 用 $|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2$ 的四系数乘法关系，给出“在张量积空间里”不等于“本身是乘积态”的最短反例，并把术语留给下一章。

## 校验

用独立的 2×2 Kronecker 乘法短程序逐项核验两个 4×4 矩阵和第 2、3 列：

| 输入 | $H\otimes I$ | $I\otimes H$ |
|---|---|---|
| $|01\rangle$ | $(0,1,0,1)^T/\sqrt2$ | $(1,-1,0,0)^T/\sqrt2$ |
| $|10\rangle$ | $(1,0,-1,0)^T/\sqrt2$ | $(0,0,1,1)^T/\sqrt2$ |

复数乘积态的范数平方为 $4\cdot(1/4)=1$。Bell 态的四系数为 $(1/\sqrt2,0,0,1/\sqrt2)$，乘积态必要条件 $c_{00}c_{11}=c_{01}c_{10}$ 变为 $1/2=0$，不成立。此必要条件只是乘积态的分量恒等式，没有将“非乘积”错误等同于“所有双系统态都不可拆”。

待总编校验：读本构建后的移动端四列表格和 4×4 公式布局需截图复核；本代理没有在其他代理同时改正文时重建共享读本。
