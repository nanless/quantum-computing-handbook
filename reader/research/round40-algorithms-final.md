# 第 40 轮：第 07 章模乘酉扩展终审

日期：2026-09-23。性质：只读复核第 38 轮发现的第 07 章 §3.2 缺口及其阅读版；未修改算法正文。

## 复核结果

| 等级 | 数量 | 范围内结论 |
|---|---:|---|
| P0 | 0 | 未发现模乘定义错误或不酉的映射。 |
| P1 | 0 | 未发现妨碍读者理解阶寻找的缺段。 |
| P2 | 0 | 第 38 轮的非单位剩余类缺口已修复；未发现该修订段的新问题。 |

修订段现在先要求 $\gcd(a,N)=1$，在全部 $0\le y<N$ 的剩余类上定义 $U_a|y\rangle=|ay\bmod N\rangle$。它明确说明逆元 $a^{-1}$ 存在：若 $ay_1\equiv ay_2\pmod N$，两边乘逆元即 $y_1\equiv y_2\pmod N$，所以这是全部 $N$ 个剩余类的置换，非单位元素也包括在内。再规定寄存器中 $y\ge N$ 的计算基态固定，便得到整个 $2^{\lceil\log_2N\rceil}$ 维空间的置换酉。原有从 $|1\rangle$ 出发的阶 $r$ 轨道与 Fourier 本征态推导保持一致。

独立用 $N=35,a=2$ 核查：寄存器有 64 个基态；映射 $0\le y<35$ 时按 $2y\bmod35$，其余 35 至 63 固定，64 个输出互不重复。非单位例子为 $5\mapsto10$、$7\mapsto14$，零映到零；从 1 出发的轨道为 $1,2,4,8,16,32,29,23,11,22,9,18$，长度仍为 12。[IBM Quantum Learning 的 Shor 课程](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/shor-algorithm)也明确把模乘定义为整个 $\mathbb Z_N$ 基上的置换。

阅读版 `reader/07-algorithms.html` 已含修订句，构建报告记录的该章源文件 SHA-256 与当前 Markdown 实测哈希一致；MathML 注释中的 $0\le y<N$ 和模乘公式存在。因此正文与生成版对应。

**终审判定：在上述修订段、其数学例子和对应阅读版范围内，P0=0、P1=0、P2=0。**本简报不把这个局部结论扩展成四章全量或整个算法领域无缺陷。
