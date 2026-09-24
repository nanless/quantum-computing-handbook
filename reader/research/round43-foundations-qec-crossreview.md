# 第 43 轮只读交叉审：先修、单/多比特、波函数与表面码事件

范围：第 42 轮基础组新增区域 `handbook/appendices/prerequisites.md`、`02-single-qubit.md`、`03-multiple-qubits.md`、`04-circuits-protocols.md`、`quantum-mechanics/04-wavefunctions-models.md`，以及第 10 章第 7 节和 `handbook/assets/surface-code-events.svg`。核对相关练习答案、原始/官方资料。未改正文或 `sources/`。

## 结论

- **P0：未发现。**
- **P1：未发现。** Bloch 坐标、传态四分支、对易子、CHSH 具体相关值和表面码时空检测事件的算式、符号均可复算；新 SVG 与第 10 章文字一致。
- **P2：1 项。** 第 3 章在例子里展示量子值 `2√2` 可达到，但“它是所有量子策略的上界”仍只作为结论出现。该缺口不改变本节数值结论，但“可达到值”和“上界”是不同命题。
- **可选扩展：无。** 此次新增区域其余部分在限定审查范围内无新增问题。网页窄屏布局仍须随总站构建复核；本轮只对 SVG 自身做了实际渲染查看。

## P2：CHSH 的 `2√2` 目前只算到“可达到”，没有说明为什么不能更高

位置：`handbook/03-multiple-qubits.md` 第 7 节，从“量子理论可达到 $2\sqrt2$，称 Tsirelson 界”到四行 `E_{ij}` 表格。现有推导完整证明局域隐藏变量值满足 `|S|≤2`，并以指定 Bell 态和测量设置算出 `S=2√2`；这一步给出量子**下界/可达到值**，而 Tsirelson 的“界”还需要对所有合法二值量子可观测量给出上界。

最小修法：在量子表格后明确加一句“这个例子只证明能达到 `2√2`；它是普适上界还需另一步证明”，并指向研究生层的证明位置。若希望就地补上，可把以下算符范数推导放在可选进阶段，先说明 `A_i²=B_j²=I`、不同方的算符可对易：

```
𝓑 = A₀⊗(B₀+B₁)+A₁⊗(B₀−B₁),
𝓑² = 4I−[A₀,A₁]⊗[B₀,B₁].
```

由 `∥A_i∥=∥B_j∥=1` 得每个交换子范数不超过 2，于是 `∥𝓑²∥≤4+2×2=8`、`|⟨𝓑⟩|≤∥𝓑∥≤2√2`；前文 Bell 态例恰好取到等号。若顾及初学者，此段可以移到注解/练习，不必在首次讲纠缠时要求读者掌握算符范数。

来源：[CHSH 原始论文](https://doi.org/10.1103/PhysRevLett.23.880)给经典 Bell 不等式；[Tsirelson 1980 原论文](https://doi.org/10.1007/BF00417500)给量子上界；[IBM Quantum Learning 的 CHSH 教学](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/chsh-game)可供核对初学者路线。

## 逐项核对及无问题范围

1. **先修路线**：`prerequisites.md` 新增 Python/NumPy 是可选动手路线，没有把编程错列为前五章理论先修；第 15 章 `@` 和 `np.vdot` 的本地解释准确。七题的条件频率、归一化、矩阵乘法、张量积、模周期、二项标准误差和势阱积分均可复算。题 5 明确把 `√N=1024` 次当教学假设，不误称精确 Grover 迭代数。[NumPy 官方入门教程](https://numpy.org/doc/stable/user/absolute_beginners)与路线使用场景相符。
2. **Bloch 算例**：从 `Y=[[0,−i],[i,0]]` 得 `r_y=2 Im(α*β)`；对 `α=√3/2,β=i/2`，`r=(0,√3/2,1/2)`、`|r|²=1`，`P(Y=+1)=(2+√3)/4≈0.9330`。从 `R_y(θ)|0⟩` 得 `(sinθ,0,cosθ)`，半角与球面转角一致。[IBM Bloch 球教学](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/bloch-sphere)使用相同矩阵约定。
3. **Schmidt/CHSH**：`−(3/4)log₂(3/4)−(1/4)log₂(1/4)≈0.811278` bit；CHSH 四值 `(+,+,+,−)/√2`，代入 `+,+,+,−` 得 `2√2`。正文已说明四种不相容设置要用多轮制备，且没有把确定性隐藏变量当作物理必要假设。[IBM CHSH 教学](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/chsh-game)作独立对照。
4. **传态四分支**：固定 `Q,A,B` 顺序，CNOT 后四项与 H 后 `00,01,10,11` 表格吻合。最后一支为 `XZ|ψ⟩=−β|0⟩+α|1⟩`，表中校正 `ZX` 精确复原；四支各有概率 `1/4`，忽略 Alice 两位记录时 Bob 为 `I/2`。[Bennett 等传态原论文](https://doi.org/10.1103/PhysRevLett.70.1895)支持资源与条件修正结构。
5. **Q4 对易子**：在共同作用域内，`x(−iℏf′)−[−iℏ(xf)′]=iℏf`；符号和乘积法则正确。正文明确在整条实线、足够光滑试探函数上算，并警告无界算符/有限区间边界，深浅平衡合理。[MIT 8.04 讲义](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/pages/lecture-notes/)提供相同位置表示背景。
6. **表面码时间事件**：`(s₁,s₂,s₃)=(0,1,0)` 给 `(δ₂,δ₃)=(1,1)`，代表一次读出反转的两个相邻时间事件；`(0,1,1)` 给 `(1,0)`，代表持续数据错误导致一次时间变化。正文还说明单稳定子表不能单独定罪、数据错误通常产生空间事件对，并正确处理首次/末次检测边界。[Fowler 等表面码原始综述](https://doi.org/10.1103/PhysRevA.86.032324)和[Acharya 等实际检测事件实验](https://www.nature.com/articles/s41586-022-05434-1)作交叉核对。
7. **表面码 SVG**：实际用本机浏览器渲染成 1200×670 截图查看，标题、图例、事件圆点和时间下箭头无遮挡。左图红、蓝路径从 `(132,330)` 到 `(332,420)`，中间形成不触发额外检查的可收缩闭环；右图橙点在第 1/2 和 2/3 轮之间，正对应 `δ₂=δ₃=1`。虚线边界和图下提醒已避免把概念图误称具体芯片布线。手机中的整页缩放仍由总站渲染检查。

本轮的“限定范围无新问题”只覆盖上面第 1、2、4、5、6、7 项及第 3 项的已列数值；CHSH 上界与可达到值的推导区分仍待最小补注。
