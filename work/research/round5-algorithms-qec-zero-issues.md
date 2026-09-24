# 第五轮终局复核：算法与量子纠错零问题记录

复核日期：2026-09-22

复核范围：

- `handbook/06-algorithmic-primitives.md`
- `handbook/07-algorithms.md`
- `handbook/08-applications.md`
- `handbook/10-error-correction.md`

本轮只重新读取当前最终文本，验证第四轮 Simon 修复及相关上下文，不扩展、不润色正文。

## 结论

**本轮未发现问题。**

| 等级 | 数量 |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 0 |

未修改任何 handbook 正文。

## Simon 修复回归检查

当前承诺为

$$
f(x)=f(y)\quad\Longleftrightarrow\quad
y=x\ \text{或}\ y=x\oplus s,
$$

等价于 $x\oplus y\in\{0^n,s\}$，其中 $s\ne0^n$。逐项检查结果：

1. 令 $y=x$ 时承诺成立，不再与 $f(x)=f(x)$ 矛盾。
2. 对每个 $x$，另一个不同原像是 $x\oplus s$；因为 $s\ne0^n$，两者确实不同。
3. 承诺排除了第三个原像，因此正文“每个函数值恰有两个原像”成立。
4. 测量第二寄存器后，第一寄存器为

   $$
   \frac{|x_0\rangle+|x_0\oplus s\rangle}{\sqrt2},
   $$

   后续 Hadamard 干涉仍只保留 $z\cdot s=0$ 的结果。
5. $s=110$ 的三比特例子、$n-1$ 条独立方程和 $O(n)$ 次量子查询结论未受修复影响。

## 其余章节复核

### `06-algorithmic-primitives.md`

可逆 oracle、相位回踢、Deutsch–Jozsa/Bernstein–Vazirani、振幅放大、QFT、相位估计、反计算和成功概率的公式及成本边界保持一致。未发现 P0/P1/P2。

### `07-algorithms.md`

除已验证的 Simon 修复外，Grover、Shor、Trotter 模拟、HHL、幅度估计及复杂度类表述没有回归；查询模型、输入输出和容错成本限定仍完整。未发现 P0/P1/P2。

### `08-applications.md`

VQE 变分界、单比特算例、单边 MaxCut QAOA 公式、shots 成本、数据装载和实用优势证据等级均保持正确。未发现 P0/P1/P2。

### `10-error-correction.md`

三比特码与 Steane 综合征、码距能力、表面码计数限定、阈值依赖、Eastin–Knill 边界、魔法态和逻辑错误预算均保持正确。未发现 P0/P1/P2。

## 结构检查

- 四章 Markdown 代码围栏与展示公式分隔符保持成对闭合。
- 本轮未改 06、07、08、10，也未改其他章节、附录、assets 或 `sources/`。
