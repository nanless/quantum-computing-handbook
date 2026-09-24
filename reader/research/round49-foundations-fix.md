# 第 49 轮：Ramsey 拟合符号补全

算法组交叉审指出 `handbook/05-noise-channels.md` §6 的 $\cos(\Delta t+\phi)$ 未逐一定义 $\Delta,C,\phi$，容易把普通频率 Hz 直接代入角频率位置。已在本组独占文件紧接公式补上：$\Delta=\omega_0-\omega_{\rm ref}$，单位 rad/s；若 $\Delta f$ 用 Hz，则 $\Delta=2\pi\Delta f$；$C$ 为初始对比度、$\phi$ 为脉冲相位约定的初始相位，并说明该简式采用理想 $1/2$ 概率基线，真实拟合可能需要偏置。

量纲核对：$\Delta t$ 无量纲；若 $\Delta f=1\,\mathrm{MHz}$ 且 $t=1\,\mu\mathrm{s}$，相位进动为 $2\pi$，不是 1 rad。Q3 已采用 $\Delta=\omega_0-\omega_d$ 的同一符号约定。未编辑共享练习附录、算法组文件、`sources/` 或阅读版。
