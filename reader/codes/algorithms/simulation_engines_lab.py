#!/usr/bin/env python3
"""第 21 章配套纯 Python 标准库教学验证脚本：三大经典模拟迷你引擎与精确对照。

依赖：仅使用 Python 3 标准库（cmath, math, random, json），不依赖 NumPy 或任何第三方包。
默认不联网、不调用云服务。

运行命令：
    python3 codes/algorithms/simulation_engines_lab.py

基序与约定（与全书《符号表》严格一致）：
    - 多比特计算基采用大端序（高位在左）：|q_0 q_1 ... q_{n-1}>；
      两比特基序为 |00>, |01>, |10>, |11>，三比特基序为 |000>, |001>, ..., |111>。
    - 内积采用左共轭 <u|v> = sum_j conj(u_j) * v_j。
    - 单比特退极化信道采用全书主定义 D_p(rho) = (1 - p) rho + p * I / 2（0 <= p <= 1），
      与随机 Pauli 形式 D~_q 的换算为 p = 4q / 3。
    - 态保真度采用全书统一的根保真度 F(|psi>, |phi>) = |<psi|phi>|；平方重叠显式记作 F^2。

包含三大教学迷你引擎及与独立态矢量/密度矩阵精确解的逐格断言（容差 < 1e-12）：
    1. Aaronson–Gottesman 稳定子表引擎（含去稳定子、O(n) Clifford 门更新、O(n^2) 确定性测量）；
    2. 3 比特矩阵乘积态（MPS）逐键精确 SVD 构造、左正则化校验、张量收缩与截断误差核算；
    3. 海森堡绘景 Pauli 传播与含噪稀疏 Pauli 动力学（SPD）引擎及权重截断算符范数误差界检验。
"""

from __future__ import annotations

import cmath
import json
import math
import random
from typing import Dict, List, Optional, Sequence, Tuple

TOL = 1e-12

# =============================================================================
# 零、独立精确参考引擎（纯标准库态矢量与密度矩阵）
# =============================================================================

Matrix = List[List[complex]]
Vector = List[complex]

I2: Matrix = [[1 + 0j, 0j], [0j, 1 + 0j]]
X2: Matrix = [[0j, 1 + 0j], [1 + 0j, 0j]]
Y2: Matrix = [[0j, -1j], [1j, 0j]]
Z2: Matrix = [[1 + 0j, 0j], [0j, -1 + 0j]]
H2: Matrix = [
    [1 / math.sqrt(2) + 0j, 1 / math.sqrt(2) + 0j],
    [1 / math.sqrt(2) + 0j, -1 / math.sqrt(2) + 0j],
]
S2: Matrix = [[1 + 0j, 0j], [0j, 1j]]
T2: Matrix = [[1 + 0j, 0j], [0j, cmath.exp(1j * math.pi / 4)]]

PAULI_MAP: Dict[str, Matrix] = {"I": I2, "X": X2, "Y": Y2, "Z": Z2}


def rx_matrix(theta: float) -> Matrix:
    c = math.cos(theta / 2.0)
    s = math.sin(theta / 2.0)
    return [[c + 0j, -1j * s], [-1j * s, c + 0j]]


def rz_matrix(theta: float) -> Matrix:
    return [[cmath.exp(-0.5j * theta), 0j], [0j, cmath.exp(0.5j * theta)]]


def vdot(u: Sequence[complex], v: Sequence[complex]) -> complex:
    """左共轭内积 <u|v> = sum_j u_j^* v_j。"""
    return sum(a.conjugate() * b for a, b in zip(u, v))


def norm2(v: Sequence[complex]) -> float:
    return sum(abs(a) ** 2 for a in v)


def kron_mat(a: Matrix, b: Matrix) -> Matrix:
    ra, ca = len(a), len(a[0])
    rb, cb = len(b), len(b[0])
    out = [[0j] * (ca * cb) for _ in range(ra * rb)]
    for i in range(ra):
        for j in range(ca):
            aij = a[i][j]
            if aij == 0:
                continue
            for k in range(rb):
                row = out[i * rb + k]
                bk = b[k]
                for l in range(cb):
                    row[j * cb + l] = aij * bk[l]
    return out


def matmul(a: Matrix, b: Matrix) -> Matrix:
    ra, ca = len(a), len(a[0])
    cb = len(b[0])
    out = [[0j] * cb for _ in range(ra)]
    for i in range(ra):
        ai = a[i]
        oi = out[i]
        for k in range(ca):
            aik = ai[k]
            if aik == 0:
                continue
            bk = b[k]
            for j in range(cb):
                oi[j] += aik * bk[j]
    return out


def dagger(a: Matrix) -> Matrix:
    r, c = len(a), len(a[0])
    return [[a[i][j].conjugate() for i in range(r)] for j in range(c)]


def trace(a: Matrix) -> complex:
    return sum(a[i][i] for i in range(len(a)))


def pauli_string_matrix(pstr: str) -> Matrix:
    mat: Matrix = [[1 + 0j]]
    for ch in pstr:
        mat = kron_mat(mat, PAULI_MAP[ch])
    return mat


class ExactStatevector:
    """独立大端序态矢量精确参考引擎（纯标准库，O(2^n) 原地门作用）。"""

    def __init__(self, n: int, amps: Optional[Sequence[complex]] = None) -> None:
        self.n = n
        if amps is None:
            self.state: Vector = [0j] * (1 << n)
            self.state[0] = 1 + 0j
        else:
            assert len(amps) == (1 << n)
            self.state = [complex(x) for x in amps]

    def copy(self) -> "ExactStatevector":
        return ExactStatevector(self.n, self.state)

    def apply_1q(self, u: Matrix, q: int) -> None:
        bit = 1 << (self.n - 1 - q)
        u00, u01 = u[0][0], u[0][1]
        u10, u11 = u[1][0], u[1][1]
        st = self.state
        dim = 1 << self.n
        for idx in range(dim):
            if (idx & bit) == 0:
                idx1 = idx | bit
                a0, a1 = st[idx], st[idx1]
                st[idx] = u00 * a0 + u01 * a1
                st[idx1] = u10 * a0 + u11 * a1

    def apply_cnot(self, ctrl: int, tgt: int) -> None:
        assert ctrl != tgt
        cbit = 1 << (self.n - 1 - ctrl)
        tbit = 1 << (self.n - 1 - tgt)
        st = self.state
        dim = 1 << self.n
        for idx in range(dim):
            if (idx & cbit) and not (idx & tbit):
                j = idx | tbit
                st[idx], st[j] = st[j], st[idx]

    def measure_z(self, q: int, forced_outcome: int) -> float:
        """按指定结果 forced_outcome in {0, 1} 投影坍缩，返回该结果的 Born 概率。"""
        bit = 1 << (self.n - 1 - q)
        prob = 0.0
        for idx, amp in enumerate(self.state):
            b = 1 if (idx & bit) else 0
            if b == forced_outcome:
                prob += abs(amp) ** 2
        assert prob > TOL, f"测量结果 {forced_outcome} 概率为零"
        inv = 1.0 / math.sqrt(prob)
        for idx in range(len(self.state)):
            b = 1 if (idx & bit) else 0
            if b == forced_outcome:
                self.state[idx] *= inv
            else:
                self.state[idx] = 0j
        return prob

    def expectation_pauli(self, pstr: str) -> float:
        assert len(pstr) == self.n
        phi = self.copy()
        for q, ch in enumerate(pstr):
            if ch != "I":
                phi.apply_1q(PAULI_MAP[ch], q)
        val = vdot(self.state, phi.state)
        assert abs(val.imag) < TOL
        return val.real


class ExactDensityMatrix:
    """独立大端序密度矩阵精确参考引擎（纯标准库，支持含噪 CPTP 演化）。"""

    def __init__(self, n: int, state: Sequence[complex]) -> None:
        self.n = n
        dim = 1 << n
        assert len(state) == dim
        self.rho: Matrix = [
            [state[i] * state[j].conjugate() for j in range(dim)]
            for i in range(dim)
        ]

    def _embed_1q(self, u: Matrix, q: int) -> Matrix:
        mat: Matrix = [[1 + 0j]]
        for idx in range(self.n):
            mat = kron_mat(mat, u if idx == q else I2)
        return mat

    def _cnot_matrix(self, ctrl: int, tgt: int) -> Matrix:
        dim = 1 << self.n
        cbit = 1 << (self.n - 1 - ctrl)
        tbit = 1 << (self.n - 1 - tgt)
        mat = [[0j] * dim for _ in range(dim)]
        for col in range(dim):
            row = (col ^ tbit) if (col & cbit) else col
            mat[row][col] = 1 + 0j
        return mat

    def apply_unitary(self, u: Matrix) -> None:
        self.rho = matmul(matmul(u, self.rho), dagger(u))

    def apply_1q(self, u: Matrix, q: int) -> None:
        self.apply_unitary(self._embed_1q(u, q))

    def apply_cnot(self, ctrl: int, tgt: int) -> None:
        self.apply_unitary(self._cnot_matrix(ctrl, tgt))

    def apply_depolarizing(self, q: int, p: float) -> None:
        """单比特退极化信道 D_p(rho) = (1-p)rho + p * (I_q/2) tensor Tr_q(rho)
        等价于随机 Pauli 形式 (1 - 3p/4)rho + (p/4)(X_q rho X_q + Y_q rho Y_q + Z_q rho Z_q)。
        """
        assert 0.0 <= p <= 1.0
        dim = 1 << self.n
        w0 = 1.0 - 0.75 * p
        wp = 0.25 * p
        ex = self._embed_1q(X2, q)
        ey = self._embed_1q(Y2, q)
        ez = self._embed_1q(Z2, q)
        rx = matmul(matmul(ex, self.rho), ex)
        ry = matmul(matmul(ey, self.rho), ey)
        rz = matmul(matmul(ez, self.rho), ez)
        new_rho = [[0j] * dim for _ in range(dim)]
        for i in range(dim):
            for j in range(dim):
                new_rho[i][j] = (
                    w0 * self.rho[i][j] + wp * (rx[i][j] + ry[i][j] + rz[i][j])
                )
        self.rho = new_rho
        assert abs(trace(self.rho) - 1.0) < TOL

    def expectation_pauli(self, pstr: str) -> float:
        op = pauli_string_matrix(pstr)
        val = trace(matmul(op, self.rho))
        assert abs(val.imag) < TOL
        return val.real


# =============================================================================
# 引擎一：Aaronson–Gottesman 稳定子表模拟器（含去稳定子）
# =============================================================================


def _phase_g(x1: int, z1: int, x2: int, z2: int) -> int:
    """计算单比特 Pauli 乘积 sigma(x1,z1) * sigma(x2,z2) = i^g * sigma(x1^x2, z1^z2) 中的指数 g in {-1, 0, +1}。"""
    if x1 == 0 and z1 == 0:
        return 0
    if x1 == 1 and z1 == 1:
        return z2 - x2
    if x1 == 1 and z1 == 0:
        return z2 * (2 * x2 - 1)
    # x1 == 0 and z1 == 1
    return x2 * (1 - 2 * z2)


class StabilizerTableau:
    """Aaronson–Gottesman (2004) 2n x (2n+1) 稳定子表引擎（外加 1 条暂存行用于确定性测量）。

    行编号约定：
        - 0 .. n-1     : 去稳定子（destabilizer）行 D_0 .. D_{n-1}
        - n .. 2n-1    : 稳定子（stabilizer）行 S_0 .. S_{n-1}
        - 2n           : 暂存行（scratch row），仅在确定性测量时使用
    列编号约定：
        - 0 .. n-1     : 对应大端序比特 q_0 .. q_{n-1} 的 X 比特 x_{i,q} 与 Z 比特 z_{i,q}
        - 相位位 r_i in {0, 1} 表示符号 (-1)^{r_i}；单比特编码 (0,0)=I, (1,0)=X, (0,1)=Z, (1,1)=Y=iXZ。
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.x: List[List[int]] = [[0] * n for _ in range(2 * n + 1)]
        self.z: List[List[int]] = [[0] * n for _ in range(2 * n + 1)]
        self.r: List[int] = [0] * (2 * n + 1)
        # 初态 |0...0>：D_j = +X_j，S_j = +Z_j
        for j in range(n):
            self.x[j][j] = 1
            self.z[n + j][j] = 1

    def symplectic_inner(self, row_a: int, row_b: int) -> int:
        """计算两行的二元辛内积（0 表示对易，1 表示反对易）。"""
        acc = 0
        xa, za = self.x[row_a], self.z[row_a]
        xb, zb = self.x[row_b], self.z[row_b]
        for j in range(self.n):
            acc ^= (xa[j] & zb[j]) ^ (za[j] & xb[j])
        return acc

    def _rowsum(self, h: int, i: int) -> None:
        """将第 h 行更新为 P_i * P_h（要求 P_i 与 P_h 对易，保证结果为厄米 Pauli）。"""
        phase_sum = 2 * self.r[h] + 2 * self.r[i]
        xi, zi = self.x[i], self.z[i]
        xh, zh = self.x[h], self.z[h]
        for j in range(self.n):
            phase_sum += _phase_g(xi[j], zi[j], xh[j], zh[j])
            xh[j] ^= xi[j]
            zh[j] ^= zi[j]
        mod4 = phase_sum % 4
        assert mod4 in (0, 2), f"非法反厄米乘积：phase_sum mod 4 = {mod4}"
        self.r[h] = 0 if mod4 == 0 else 1

    def h(self, a: int) -> None:
        """对第 a 个比特施加 Hadamard 门：O(n) 更新。"""
        for i in range(2 * self.n):
            self.r[i] ^= self.x[i][a] & self.z[i][a]
            self.x[i][a], self.z[i][a] = self.z[i][a], self.x[i][a]

    def s(self, a: int) -> None:
        """对第 a 个比特施加相位门 S = diag(1, i)：O(n) 更新。"""
        for i in range(2 * self.n):
            self.r[i] ^= self.x[i][a] & self.z[i][a]
            self.z[i][a] ^= self.x[i][a]

    def cnot(self, ctrl: int, tgt: int) -> None:
        """施加受控非门 CNOT(ctrl -> tgt)：O(n) 更新（务必先更新相位位再改 X/Z 位）。"""
        assert ctrl != tgt
        for i in range(2 * self.n):
            xc, zc = self.x[i][ctrl], self.z[i][ctrl]
            xt, zt = self.x[i][tgt], self.z[i][tgt]
            self.r[i] ^= xc & zt & (xt ^ zc ^ 1)
            self.x[i][tgt] = xt ^ xc
            self.z[i][ctrl] = zc ^ zt

    def measure_z(
        self,
        a: int,
        forced_outcome: Optional[int] = None,
        rng: Optional[random.Random] = None,
    ) -> Tuple[int, bool]:
        """在计算基测量第 a 个比特（测 Z_a），返回 (测量结果 0/1, 是否随机分支)。"""
        n = self.n
        # 查找第一个与 Z_a 反对易（即 x[p][a] == 1）的稳定子行 p in [n, 2n-1]
        p = -1
        for row in range(n, 2 * n):
            if self.x[row][a] == 1:
                p = row
                break

        if p != -1:
            # 情形 1：随机分支（0 和 1 概率各 1/2）
            # 跳过 p 与 p - n：p - n 是唯一与 S_p 反对易的去稳定子行，随后将直接被旧 S_p 覆盖
            for i in range(2 * n):
                if i != p and i != p - n and self.x[i][a] == 1:
                    self._rowsum(i, p)
            # D_{p-n} <- 旧 S_p
            self.x[p - n] = self.x[p][:]
            self.z[p - n] = self.z[p][:]
            self.r[p - n] = self.r[p]
            # S_p <- (-1)^m Z_a
            self.x[p] = [0] * n
            self.z[p] = [0] * n
            self.z[p][a] = 1
            if forced_outcome is not None:
                outcome = int(forced_outcome)
            else:
                sampler = rng if rng is not None else random
                outcome = sampler.randrange(2)
            self.r[p] = outcome
            return outcome, True

        # 情形 2：确定性分支，利用去稳定子 O(n^2) 直接读出线性组合系数 c_k = x[k][a]
        scratch = 2 * n
        self.x[scratch] = [0] * n
        self.z[scratch] = [0] * n
        self.r[scratch] = 0
        for k in range(n):
            if self.x[k][a] == 1:
                self._rowsum(scratch, k + n)
        # 严格校验暂存行精确还原出 +/- Z_a
        assert all(bit == 0 for bit in self.x[scratch])
        assert all(
            self.z[scratch][j] == (1 if j == a else 0) for j in range(n)
        )
        return self.r[scratch], False

    def expectation_pauli(self, pstr: str) -> float:
        """直接由稳定子表精确计算任意 n 比特 Pauli 串的期望值（必为 -1, 0 或 +1）。"""
        n = self.n
        assert len(pstr) == n
        px = [1 if ch in ("X", "Y") else 0 for ch in pstr]
        pz = [1 if ch in ("Z", "Y") else 0 for ch in pstr]
        # 若 P 与任意一条稳定子反对易，则 <psi|P|psi> = 0
        for row in range(n, 2 * n):
            comm = 0
            for j in range(n):
                comm ^= (px[j] & self.z[row][j]) ^ (pz[j] & self.x[row][j])
            if comm == 1:
                return 0.0
        # 否则 P 必为稳定子群元素的 +/-1 倍，利用去稳定子 O(n^2) 读出系数并累乘求符号
        scratch = 2 * n
        self.x[scratch] = [0] * n
        self.z[scratch] = [0] * n
        self.r[scratch] = 0
        for k in range(n):
            comm = 0
            for j in range(n):
                comm ^= (px[j] & self.z[k][j]) ^ (pz[j] & self.x[k][j])
            if comm == 1:
                self._rowsum(scratch, k + n)
        assert self.x[scratch] == px and self.z[scratch] == pz
        return -1.0 if self.r[scratch] == 1 else 1.0

    def row_to_string(self, row: int) -> str:
        sign = "-" if self.r[row] else "+"
        chars = []
        for j in range(self.n):
            pair = (self.x[row][j], self.z[row][j])
            chars.append({(0, 0): "I", (1, 0): "X", (0, 1): "Z", (1, 1): "Y"}[pair])
        return sign + "".join(chars)

    def stabilizers(self) -> List[str]:
        return [self.row_to_string(i) for i in range(self.n, 2 * self.n)]

    def destabilizers(self) -> List[str]:
        return [self.row_to_string(i) for i in range(self.n)]

    def assert_symplectic_invariants(self) -> None:
        """核验全部 2n x 2n 对易/反对易不变量：D_i 与 S_j 对易当且仅当 i != j。"""
        n = self.n
        for i in range(n):
            for j in range(n):
                assert self.symplectic_inner(i, j) == 0
                assert self.symplectic_inner(n + i, n + j) == 0
                assert self.symplectic_inner(i, n + j) == (1 if i == j else 0)


# =============================================================================
# 引擎二：纯标准库 3 比特矩阵乘积态（MPS）逐键精确 SVD 与截断引擎
# =============================================================================


def _hermitian_2x2_eig(h: Matrix) -> Tuple[List[float], Matrix]:
    """对 2x2 厄米正半定矩阵做解析精确本征分解，按本征值降序返回 (evals, U)。"""
    a = h[0][0].real
    d = h[1][1].real
    b = h[0][1]
    assert abs(h[0][0].imag) < 1e-11 and abs(h[1][1].imag) < 1e-11
    assert abs(h[1][0] - b.conjugate()) < 1e-11

    b_abs = abs(b)
    tr = a + d
    diff = a - d
    disc = math.hypot(diff, 2.0 * b_abs)
    lam1 = 0.5 * (tr + disc)
    lam2 = 0.5 * (tr - disc)

    if b_abs < 1e-15:
        if a >= d:
            u = [[1 + 0j, 0j], [0j, 1 + 0j]]
        else:
            u = [[0j, 1 + 0j], [1 + 0j, 0j]]
        return [max(0.0, lam1), max(0.0, lam2)], u

    # 对应 lam1 的特征向量：选取数值最稳妥的一行求解
    if diff >= 0.0:
        v0 = lam1 - d + 0j
        v1 = b.conjugate()
    else:
        v0 = b
        v1 = lam1 - a + 0j
    inv = 1.0 / math.sqrt(abs(v0) ** 2 + abs(v1) ** 2)
    u00, u10 = v0 * inv, v1 * inv
    # 正交伙伴列（满足 u[:,0]^dagger u[:,1] = 0 且单位范数）
    u01, u11 = -u10.conjugate(), u00.conjugate()
    return [max(0.0, lam1), max(0.0, lam2)], [[u00, u01], [u10, u11]]


def _svd_2x4(m: Matrix) -> Tuple[Matrix, List[float], Matrix]:
    """对 2x4 复矩阵 M 做精简精确 SVD：M = U (2xr) @ diag(s) @ Vh (rx4)。"""
    gram = matmul(m, dagger(m))  # 2x2 厄米半正定
    evals, u_full = _hermitian_2x2_eig(gram)
    sigmas = [math.sqrt(ev) for ev in evals]
    kept = [idx for idx, s in enumerate(sigmas) if s > TOL]
    u_cols = [[u_full[r][c] for c in kept] for r in range(2)]
    s_kept = [sigmas[c] for c in kept]
    # Vh = diag(1/s) @ U^dagger @ M
    uh_m = matmul(dagger(u_cols), m)
    vh = [[uh_m[i][j] / s_kept[i] for j in range(4)] for i in range(len(kept))]
    return u_cols, s_kept, vh


def _svd_4x2(m: Matrix) -> Tuple[Matrix, List[float], Matrix]:
    """对 4x2 复矩阵 M 做精简精确 SVD：M = U (4xr) @ diag(s) @ Vh (rx2)。"""
    gram = matmul(dagger(m), m)  # 2x2 厄米半正定
    evals, v_full = _hermitian_2x2_eig(gram)
    sigmas = [math.sqrt(ev) for ev in evals]
    kept = [idx for idx, s in enumerate(sigmas) if s > TOL]
    v_cols = [[v_full[r][c] for c in kept] for r in range(2)]
    s_kept = [sigmas[c] for c in kept]
    # U = M @ V @ diag(1/s)
    mv = matmul(m, v_cols)
    u = [[mv[i][j] / s_kept[j] for j in range(len(kept))] for i in range(4)]
    vh = dagger(v_cols)
    return u, s_kept, vh


class MPS3:
    """3 比特开放边界左正则矩阵乘积态（纯标准库实现，支持任意 3 比特纯态精确拆解与截断）。"""

    def __init__(
        self,
        a0: List[Matrix],
        a1: List[Matrix],
        a2: List[Matrix],
        sigma1: List[float],
        sigma2: List[float],
    ) -> None:
        self.a0 = a0  # a0[s0]: 1 x chi1
        self.a1 = a1  # a1[s1]: chi1 x chi2
        self.a2 = a2  # a2[s2]: chi2 x 1
        self.sigma1 = sigma1
        self.sigma2 = sigma2

    @classmethod
    def from_statevector(cls, psi: Sequence[complex]) -> "MPS3":
        assert len(psi) == 8
        assert abs(norm2(psi) - 1.0) < TOL

        # 键 1 切分：(q0 | q1 q2)，重排为 2x4 矩阵
        psi_0_12 = [[psi[s0 * 4 + rest] for rest in range(4)] for s0 in range(2)]
        u0, s1, vh12 = _svd_2x4(psi_0_12)
        chi1 = len(s1)
        a0 = [[[u0[s0][a] for a in range(chi1)]] for s0 in range(2)]

        # 吸收 Sigma1 到右侧并重排为 (chi1 * 2) x 2 矩阵（当 chi1 == 1 时补零到 4x2 或直接处理）
        sv12 = [[s1[a] * vh12[a][col] for col in range(4)] for a in range(chi1)]
        m12_full = [[0j, 0j] for _ in range(4)]
        for a in range(chi1):
            for s1_phys in range(2):
                row_idx = a * 2 + s1_phys
                for s2_phys in range(2):
                    m12_full[row_idx][s2_phys] = sv12[a][s1_phys * 2 + s2_phys]
        u1_full, s2, vh2 = _svd_4x2(m12_full)
        chi2 = len(s2)

        a1 = [
            [
                [u1_full[a * 2 + s1_phys][b] for b in range(chi2)]
                for a in range(chi1)
            ]
            for s1_phys in range(2)
        ]
        # 将 Sigma2 吸收进末格点 A^[2]
        a2 = [
            [[s2[b] * vh2[b][s2_phys]] for b in range(chi2)]
            for s2_phys in range(2)
        ]
        return cls(a0, a1, a2, s1, s2)

    def contract_statevector(self) -> Vector:
        """逐格收缩 A^[0]s0 * A^[1]s1 * A^[2]s2 还原全部 8 个复振幅。"""
        out: Vector = []
        for s0 in range(2):
            for s1 in range(2):
                m01 = matmul(self.a0[s0], self.a1[s1])
                for s2 in range(2):
                    val = matmul(m01, self.a2[s2])[0][0]
                    out.append(val)
        return out

    def assert_left_canonical(self) -> None:
        """验证格点 0 与格点 1 的左正则等距条件 sum_s (A^s)^dagger A^s = I。"""
        for tensors in (self.a0, self.a1):
            chi_r = len(tensors[0][0])
            acc = [[0j] * chi_r for _ in range(chi_r)]
            for s in range(2):
                prod = matmul(dagger(tensors[s]), tensors[s])
                for i in range(chi_r):
                    for j in range(chi_r):
                        acc[i][j] += prod[i][j]
            for i in range(chi_r):
                for j in range(chi_r):
                    target = 1.0 if i == j else 0.0
                    assert abs(acc[i][j] - target) < TOL

    @staticmethod
    def truncate_bond1(psi: Sequence[complex], chi_max: int) -> Tuple[Vector, Vector, float]:
        """在键 1 (q0 | q1 q2) 处保留前 chi_max 个最大奇异值，返回：
        (未归一化截断态, 重归一化截断态, 理论截断误差 eps_trunc = sum_{i > chi_max} sigma_i^2)。
        """
        psi_0_12 = [[psi[s0 * 4 + rest] for rest in range(4)] for s0 in range(2)]
        u0, s1, vh12 = _svd_2x4(psi_0_12)
        k = min(chi_max, len(s1))
        eps_trunc = sum(s ** 2 for s in s1[k:])
        raw = [0j] * 8
        for s0 in range(2):
            for rest in range(4):
                val = 0j
                for a in range(k):
                    val += u0[s0][a] * s1[a] * vh12[a][rest]
                raw[s0 * 4 + rest] = val
        nrm = math.sqrt(norm2(raw))
        renorm = [x / nrm for x in raw]
        return raw, renorm, eps_trunc


# =============================================================================
# 引擎三：海森堡绘景 Pauli 传播与稀疏 Pauli 动力学（SPD）引擎
# =============================================================================

_CNOT_ADJ_TABLE: Dict[Tuple[str, str], Tuple[int, str, str]] = {
    ("I", "I"): (1, "I", "I"),
    ("I", "X"): (1, "I", "X"),
    ("I", "Y"): (1, "Z", "Y"),
    ("I", "Z"): (1, "Z", "Z"),
    ("X", "I"): (1, "X", "X"),
    ("X", "X"): (1, "X", "I"),
    ("X", "Y"): (1, "Y", "Z"),
    ("X", "Z"): (-1, "Y", "Y"),
    ("Y", "I"): (1, "Y", "X"),
    ("Y", "X"): (1, "Y", "I"),
    ("Y", "Y"): (-1, "X", "Z"),
    ("Y", "Z"): (1, "X", "Y"),
    ("Z", "I"): (1, "Z", "I"),
    ("Z", "X"): (1, "Z", "X"),
    ("Z", "Y"): (1, "I", "Y"),
    ("Z", "Z"): (1, "I", "Z"),
}


def pauli_weight(pstr: str) -> int:
    return sum(1 for ch in pstr if ch != "I")


class PauliPropagator:
    """海森堡绘景 Pauli 反向传播与稀疏 Pauli 动力学（SPD）迷你引擎。"""

    def __init__(self, observable: Dict[str, float]) -> None:
        self.terms: Dict[str, float] = {
            k: float(v) for k, v in observable.items() if abs(v) > 1e-15
        }
        self.pruned_l1_bound: float = 0.0

    def apply_depolarizing_adj(self, p: float, qubits: Optional[Sequence[int]] = None) -> None:
        """施加单比特退极化信道伴随映射 D_p^dagger：每命中 1 个非 I 比特，系数乘 (1 - p)。"""
        eta = 1.0 - p
        new_terms: Dict[str, float] = {}
        for pstr, coeff in self.terms.items():
            if qubits is None:
                w = pauli_weight(pstr)
            else:
                w = sum(1 for q in qubits if pstr[q] != "I")
            val = coeff * (eta ** w)
            if abs(val) > 1e-15:
                new_terms[pstr] = val
        self.terms = new_terms

    def apply_rx_adj(self, q: int, theta: float) -> None:
        """海森堡反向传播 R_x(theta)^dagger P R_x(theta)：Z -> cZ + sY，Y -> cY - sZ，I/X 不变。"""
        c = math.cos(theta)
        s = math.sin(theta)
        new_terms: Dict[str, float] = {}
        for pstr, coeff in self.terms.items():
            ch = pstr[q]
            if ch in ("I", "X"):
                new_terms[pstr] = new_terms.get(pstr, 0.0) + coeff
            elif ch == "Z":
                pz = pstr[:q] + "Z" + pstr[q + 1 :]
                py = pstr[:q] + "Y" + pstr[q + 1 :]
                new_terms[pz] = new_terms.get(pz, 0.0) + coeff * c
                new_terms[py] = new_terms.get(py, 0.0) + coeff * s
            elif ch == "Y":
                py = pstr[:q] + "Y" + pstr[q + 1 :]
                pz = pstr[:q] + "Z" + pstr[q + 1 :]
                new_terms[py] = new_terms.get(py, 0.0) + coeff * c
                new_terms[pz] = new_terms.get(pz, 0.0) - coeff * s
        self.terms = {k: v for k, v in new_terms.items() if abs(v) > 1e-15}

    def apply_rz_adj(self, q: int, theta: float) -> None:
        """海森堡反向传播 R_z(theta)^dagger P R_z(theta)：X -> cX - sY，Y -> cY + sX，I/Z 不变。"""
        c = math.cos(theta)
        s = math.sin(theta)
        new_terms: Dict[str, float] = {}
        for pstr, coeff in self.terms.items():
            ch = pstr[q]
            if ch in ("I", "Z"):
                new_terms[pstr] = new_terms.get(pstr, 0.0) + coeff
            elif ch == "X":
                px = pstr[:q] + "X" + pstr[q + 1 :]
                py = pstr[:q] + "Y" + pstr[q + 1 :]
                new_terms[px] = new_terms.get(px, 0.0) + coeff * c
                new_terms[py] = new_terms.get(py, 0.0) - coeff * s
            elif ch == "Y":
                py = pstr[:q] + "Y" + pstr[q + 1 :]
                px = pstr[:q] + "X" + pstr[q + 1 :]
                new_terms[py] = new_terms.get(py, 0.0) + coeff * c
                new_terms[px] = new_terms.get(px, 0.0) + coeff * s
        self.terms = {k: v for k, v in new_terms.items() if abs(v) > 1e-15}

    def apply_cnot_adj(self, ctrl: int, tgt: int) -> None:
        """海森堡反向传播 CNOT^dagger P CNOT（Clifford 门，单串映单串，不增加项数）。"""
        new_terms: Dict[str, float] = {}
        for pstr, coeff in self.terms.items():
            sign, na, nb = _CNOT_ADJ_TABLE[(pstr[ctrl], pstr[tgt])]
            chars = list(pstr)
            chars[ctrl] = na
            chars[tgt] = nb
            npstr = "".join(chars)
            new_terms[npstr] = new_terms.get(npstr, 0.0) + sign * coeff
        self.terms = {k: v for k, v in new_terms.items() if abs(v) > 1e-15}

    def truncate_weight(self, max_weight: int) -> float:
        """裁去全部权重 > max_weight 的高权重 Pauli 串，返回本次裁掉项的 l1 系数和并累加到总误差界。"""
        kept: Dict[str, float] = {}
        pruned_l1 = 0.0
        for pstr, coeff in self.terms.items():
            if pauli_weight(pstr) <= max_weight:
                kept[pstr] = coeff
            else:
                pruned_l1 += abs(coeff)
        self.terms = kept
        self.pruned_l1_bound += pruned_l1
        return pruned_l1

    def expectation_product_state(self, basis_labels: str) -> float:
        """在初态 |b_0 b_1 ... b_{n-1}>（每个字符取 '0','1','+','-'）上求期望值。"""
        total = 0.0
        for pstr, coeff in self.terms.items():
            prod = 1.0
            for ch, st in zip(pstr, basis_labels):
                if ch == "I":
                    continue
                if st == "0":
                    if ch != "Z":
                        prod = 0.0
                        break
                elif st == "1":
                    if ch != "Z":
                        prod = 0.0
                        break
                    prod *= -1.0
                elif st == "+":
                    if ch != "X":
                        prod = 0.0
                        break
                elif st == "-":
                    if ch != "X":
                        prod = 0.0
                        break
                    prod *= -1.0
                else:
                    raise ValueError(f"不支持的初态标签: {st}")
            total += coeff * prod
        return total


# =============================================================================
# 全套逐格断言验算（全部对齐正文第 21 章算例与练习）
# =============================================================================


def verify_tableau_engine() -> dict:
    """验证 1：稳定子表手算算例、多比特随机 Clifford 压测、魔法态分解与练 21-A。"""
    # 1a. 正文 §3 零跳步手算：|00> --H_0--> --CNOT_01--> |Phi^+> --> 测 Z_0
    tab = StabilizerTableau(2)
    tab.h(0)
    tab.cnot(0, 1)
    tab.assert_symplectic_invariants()
    assert tab.stabilizers() == ["+XX", "+ZZ"]
    assert tab.destabilizers() == ["+ZI", "+IX"]

    # 分支 m=0 与 m=1
    for m in (0, 1):
        t_branch = StabilizerTableau(2)
        t_branch.h(0)
        t_branch.cnot(0, 1)
        out0, is_rand0 = t_branch.measure_z(0, forced_outcome=m)
        assert out0 == m and is_rand0 is True
        t_branch.assert_symplectic_invariants()
        out1, is_rand1 = t_branch.measure_z(1)
        assert out1 == m and is_rand1 is False  # 确定性关联！

        # 与态矢量精确对照
        sv = ExactStatevector(2)
        sv.apply_1q(H2, 0)
        sv.apply_cnot(0, 1)
        p0 = sv.measure_z(0, forced_outcome=m)
        assert abs(p0 - 0.5) < TOL
        p1 = sv.measure_z(1, forced_outcome=m)
        assert abs(p1 - 1.0) < TOL
        for pstr in ("ZI", "IZ", "ZZ", "XX", "YY", "XZ"):
            assert abs(t_branch.expectation_pauli(pstr) - sv.expectation_pauli(pstr)) < TOL

    # 1b. 4 比特随机 Clifford + 中段测量压测（12 组电路，全量 256 个 Pauli 期望值逐格断言 < 1e-12）
    rng = random.Random(20261125)
    max_err_4q = 0.0
    paulis_4q = [
        a + b + c + d
        for a in "IXYZ"
        for b in "IXYZ"
        for c in "IXYZ"
        for d in "IXYZ"
    ]
    det_count = 0
    rand_count = 0
    for trial in range(12):
        tab4 = StabilizerTableau(4)
        sv4 = ExactStatevector(4)
        for _ in range(28):
            g = rng.choice(["H", "S", "CNOT"])
            if g == "H":
                q = rng.randrange(4)
                tab4.h(q)
                sv4.apply_1q(H2, q)
            elif g == "S":
                q = rng.randrange(4)
                tab4.s(q)
                sv4.apply_1q(S2, q)
            else:
                a = rng.randrange(4)
                b = rng.randrange(4)
                while b == a:
                    b = rng.randrange(4)
                tab4.cnot(a, b)
                sv4.apply_cnot(a, b)
        tab4.assert_symplectic_invariants()
        # 在一半电路中插入中段测量（测完再施 5 个 Clifford 门）
        if trial % 2 == 1:
            mq = rng.randrange(4)
            # 先看表判是否随机，若是随机则与态矢量共享同一结果
            chosen = rng.randint(0, 1)
            out, is_rand = tab4.measure_z(mq, forced_outcome=chosen)
            if is_rand:
                rand_count += 1
                prob = sv4.measure_z(mq, forced_outcome=out)
                assert abs(prob - 0.5) < TOL
            else:
                det_count += 1
                prob = sv4.measure_z(mq, forced_outcome=out)
                assert abs(prob - 1.0) < TOL
            tab4.assert_symplectic_invariants()
            for _ in range(5):
                q = rng.randrange(4)
                tab4.h(q)
                sv4.apply_1q(H2, q)
        for pstr in paulis_4q:
            diff = abs(tab4.expectation_pauli(pstr) - sv4.expectation_pauli(pstr))
            if diff > max_err_4q:
                max_err_4q = diff
            assert diff < TOL

    # 1c. 正文 §4 魔法态 |T> 与 |T>^{\otimes 2} 稳定子分解精确验证
    sv_t = ExactStatevector(1)
    sv_t.apply_1q(H2, 0)
    sv_t.apply_1q(T2, 0)
    # 分解 1（计算基）：(1/sqrt(2))|0> + (e^{i pi/4}/sqrt(2))|1>
    decomp_z = [1 / math.sqrt(2) + 0j, cmath.exp(1j * math.pi / 4) / math.sqrt(2)]
    assert max(abs(a - b) for a, b in zip(sv_t.state, decomp_z)) < TOL
    # 分解 2（赤道最优稳定子展度）：(e^{i pi/8}|+> + e^{-i pi/8}|+i>) / (2 cos(pi/8))
    c1 = cmath.exp(1j * math.pi / 8) / (2 * math.cos(math.pi / 8))
    c2 = cmath.exp(-1j * math.pi / 8) / (2 * math.cos(math.pi / 8))
    plus = [1 / math.sqrt(2) + 0j, 1 / math.sqrt(2) + 0j]
    plus_i = [1 / math.sqrt(2) + 0j, 1j / math.sqrt(2)]
    decomp_eq = [c1 * a + c2 * b for a, b in zip(plus, plus_i)]
    assert max(abs(a - b) for a, b in zip(sv_t.state, decomp_eq)) < TOL
    extent_t = (abs(c1) + abs(c2)) ** 2
    assert abs(extent_t - (4.0 - 2.0 * math.sqrt(2))) < TOL
    # 两份魔法态 |T>^{\otimes 2} = (1/sqrt(2))|psi_i> + (e^{i pi/4}/sqrt(2))|Psi^+>（稳定子秩 = 2！）
    sv_tt = ExactStatevector(2)
    sv_tt.apply_1q(H2, 0)
    sv_tt.apply_1q(H2, 1)
    sv_tt.apply_1q(T2, 0)
    sv_tt.apply_1q(T2, 1)
    psi_i = [1 / math.sqrt(2), 0j, 0j, 1j / math.sqrt(2)]
    psi_plus = [0j, 1 / math.sqrt(2), 1 / math.sqrt(2), 0j]
    decomp_tt = [
        (1 / math.sqrt(2)) * a + (cmath.exp(1j * math.pi / 4) / math.sqrt(2)) * b
        for a, b in zip(psi_i, psi_plus)
    ]
    assert max(abs(a - b) for a, b in zip(sv_tt.state, decomp_tt)) < TOL

    # 1d. 练 21-A：3 比特 GHZ 稳定子表 + 测 Z_0=1 后测 Z_2（确定性得 1）
    t_ghz = StabilizerTableau(3)
    t_ghz.h(0)
    t_ghz.cnot(0, 1)
    t_ghz.cnot(1, 2)
    t_ghz.assert_symplectic_invariants()
    assert t_ghz.stabilizers() == ["+XXX", "+ZZI", "+IZZ"]
    o0, r0 = t_ghz.measure_z(0, forced_outcome=1)
    assert o0 == 1 and r0 is True
    o2, r2 = t_ghz.measure_z(2)
    assert o2 == 1 and r2 is False

    return {
        "bell_stabilizers": ["+XX", "+ZZ"],
        "max_error_4q_256_paulis": max_err_4q,
        "mid_measurements": {"deterministic": det_count, "random": rand_count},
        "magic_extent_T": round(extent_t, 10),
        "log2_extent_T": round(math.log2(extent_t), 10),
        "ghz3_practice_passed": True,
    }


def verify_mps_engine() -> dict:
    """验证 2：3 比特 GHZ 态、W 态与随机非对称态的 MPS 精确构造、左正则化与截断误差。"""
    # 2a. |GHZ_3> = (|000> + |111>) / sqrt(2)
    ghz = [1 / math.sqrt(2) + 0j, 0j, 0j, 0j, 0j, 0j, 0j, 1 / math.sqrt(2) + 0j]
    mps_ghz = MPS3.from_statevector(ghz)
    mps_ghz.assert_left_canonical()
    rec_ghz = mps_ghz.contract_statevector()
    err_ghz = max(abs(a - b) for a, b in zip(ghz, rec_ghz))
    assert err_ghz < TOL
    assert len(mps_ghz.sigma1) == 2 and len(mps_ghz.sigma2) == 2
    assert all(abs(s - 1 / math.sqrt(2)) < TOL for s in mps_ghz.sigma1 + mps_ghz.sigma2)
    raw_g, renorm_g, eps_g = MPS3.truncate_bond1(ghz, chi_max=1)
    assert abs(eps_g - 0.5) < TOL
    assert abs(norm2([a - b for a, b in zip(ghz, raw_g)]) - eps_g) < TOL
    assert abs(abs(vdot(ghz, renorm_g)) - math.sqrt(0.5)) < TOL

    # 2b. |W_3> = (|001> + |010> + |100>) / sqrt(3)
    inv_sq3 = 1 / math.sqrt(3)
    w3 = [0j, inv_sq3 + 0j, inv_sq3 + 0j, 0j, inv_sq3 + 0j, 0j, 0j, 0j]
    mps_w3 = MPS3.from_statevector(w3)
    mps_w3.assert_left_canonical()
    rec_w3 = mps_w3.contract_statevector()
    err_w3 = max(abs(a - b) for a, b in zip(w3, rec_w3))
    assert err_w3 < TOL
    assert len(mps_w3.sigma1) == 2 and len(mps_w3.sigma2) == 2
    assert abs(mps_w3.sigma1[0] - math.sqrt(2 / 3)) < TOL
    assert abs(mps_w3.sigma1[1] - math.sqrt(1 / 3)) < TOL
    assert abs(mps_w3.sigma2[0] - math.sqrt(2 / 3)) < TOL
    assert abs(mps_w3.sigma2[1] - math.sqrt(1 / 3)) < TOL
    s_ent_w3 = -(2 / 3) * math.log2(2 / 3) - (1 / 3) * math.log2(1 / 3)
    raw_w, renorm_w, eps_w = MPS3.truncate_bond1(w3, chi_max=1)
    assert abs(eps_w - 1 / 3) < TOL
    assert abs(norm2([a - b for a, b in zip(w3, raw_w)]) - eps_w) < TOL
    fid_w = abs(vdot(w3, renorm_w))
    assert abs(fid_w - math.sqrt(2 / 3)) < TOL
    assert abs(fid_w ** 2 - (1.0 - eps_w)) < TOL

    # 2c. 通用 3 比特复振幅随机态（固定种子）精确构造 + 截断恒等式验证
    rng = random.Random(20261125)
    max_err_rand = 0.0
    for _ in range(10):
        vec = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(8)]
        inv = 1.0 / math.sqrt(norm2(vec))
        vec = [x * inv for x in vec]
        mps_r = MPS3.from_statevector(vec)
        mps_r.assert_left_canonical()
        rec_r = mps_r.contract_statevector()
        err_r = max(abs(a - b) for a, b in zip(vec, rec_r))
        max_err_rand = max(max_err_rand, err_r)
        assert err_r < TOL
        raw_r, renorm_r, eps_r = MPS3.truncate_bond1(vec, chi_max=1)
        assert abs(norm2([a - b for a, b in zip(vec, raw_r)]) - eps_r) < TOL
        assert abs(abs(vdot(vec, renorm_r)) - math.sqrt(1.0 - eps_r)) < TOL

    return {
        "ghz3_bond_dims": [len(mps_ghz.sigma1), len(mps_ghz.sigma2)],
        "ghz3_max_error": err_ghz,
        "w3_bond_dims": [len(mps_w3.sigma1), len(mps_w3.sigma2)],
        "w3_max_error": err_w3,
        "w3_bond1_entropy_bits": round(s_ent_w3, 10),
        "w3_chi1_trunc_error": round(eps_w, 10),
        "w3_chi1_root_fidelity": round(fid_w, 10),
        "random_3q_max_error": max_err_rand,
    }


def verify_pauli_propagation_engine() -> dict:
    """验证 3：2 比特 2 层含噪反向树手算、3 比特 3 层含噪砖墙与密度矩阵逐格对照及练 21-B。"""
    # 3a. 正文 §6 零跳步手算：初态 |0+>，2 层 [CNOT_01 -> Rx(pi/6)^2 -> D_p^2]，观测 O = Z_0 I_1
    theta = math.pi / 6.0
    p_err = 0.2

    # 独立密度矩阵正向演化
    sv0 = ExactStatevector(2)
    sv0.apply_1q(H2, 1)  # |0+>
    dm = ExactDensityMatrix(2, sv0.state)
    rx = rx_matrix(theta)
    for _ in range(2):
        dm.apply_cnot(0, 1)
        dm.apply_1q(rx, 0)
        dm.apply_1q(rx, 1)
        dm.apply_depolarizing(0, p_err)
        dm.apply_depolarizing(1, p_err)
    dm_val = dm.expectation_pauli("ZI")

    # 闭式解析公式：(1-p)^2 cos^2(theta) - (1-p)^3 sin^2(theta) = 0.48 - 0.128 = 0.352
    closed_form = ((1 - p_err) ** 2) * (math.cos(theta) ** 2) - (
        (1 - p_err) ** 3
    ) * (math.sin(theta) ** 2)
    assert abs(dm_val - closed_form) < TOL

    # 海森堡 Pauli 传播精确演化（不截断）
    prop_exact = PauliPropagator({"ZI": 1.0})
    for _ in range(2):
        prop_exact.apply_depolarizing_adj(p_err)
        prop_exact.apply_rx_adj(1, theta)
        prop_exact.apply_rx_adj(0, theta)
        prop_exact.apply_cnot_adj(0, 1)
    pp_exact_val = prop_exact.expectation_product_state("0+")
    err_2q = abs(pp_exact_val - dm_val)
    assert err_2q < TOL

    # 海森堡 Pauli 传播（噪声优先权重截断 w <= 1）
    prop_trunc = PauliPropagator({"ZI": 1.0})
    # 第 2 层反向
    prop_trunc.apply_depolarizing_adj(p_err)
    prop_trunc.apply_rx_adj(1, theta)
    prop_trunc.apply_rx_adj(0, theta)
    prop_trunc.apply_cnot_adj(0, 1)
    # 第 1 层反向：先施加噪声衰减 (1-p)^w，再按 w <= 1 截断
    prop_trunc.apply_depolarizing_adj(p_err)
    pruned_l1 = prop_trunc.truncate_weight(max_weight=1)
    prop_trunc.apply_rx_adj(1, theta)
    prop_trunc.apply_rx_adj(0, theta)
    prop_trunc.apply_cnot_adj(0, 1)
    pp_trunc_val = prop_trunc.expectation_product_state("0+")
    trunc_err = abs(pp_exact_val - pp_trunc_val)
    assert abs(pp_trunc_val - 0.48) < TOL
    assert abs(trunc_err - 0.128) < TOL
    assert abs(pruned_l1 - 0.256) < TOL
    assert trunc_err <= prop_trunc.pruned_l1_bound + TOL

    # 3b. 练 21-B 参数核验：theta = pi/4, p = 0.5
    theta_b, p_b = math.pi / 4.0, 0.5
    exact_b = ((1 - p_b) ** 2) * 0.5 - ((1 - p_b) ** 3) * 0.5  # 0.125 - 0.0625 = 0.0625
    trunc_b = ((1 - p_b) ** 2) * 0.5  # 0.125
    bound_b = ((1 - p_b) ** 3) * math.sin(theta_b)  # 0.125 * sqrt(2)/2 = 0.0883883476...
    assert abs(exact_b - 0.0625) < TOL
    assert abs(trunc_b - 0.125) < TOL
    assert abs(exact_b - trunc_b) <= bound_b + TOL

    # 3c. 3 比特 3 层含噪砖墙电路（Rx + Rz + 交替 CNOT + 退极化）全量误差 < 1e-12 对照密度矩阵
    angles_x = [0.35, 0.50, 0.25]
    angles_z = [0.40, -0.30, 0.60]
    layers_cnot = [(0, 1), (1, 2), (0, 1)]
    max_err_3q = 0.0
    noise_sweep = {}
    for p_test in (0.0, 0.05, 0.15, 0.30):
        sv3 = ExactStatevector(3)
        sv3.apply_1q(H2, 1)  # |0+0>
        dm3 = ExactDensityMatrix(3, sv3.state)
        for l_idx, (c, t) in enumerate(layers_cnot):
            dm3.apply_cnot(c, t)
            for q in range(3):
                dm3.apply_1q(rx_matrix(angles_x[q] * (l_idx + 1) * 0.5), q)
                dm3.apply_1q(rz_matrix(angles_z[q]), q)
                if p_test > 0.0:
                    dm3.apply_depolarizing(q, p_test)
        for obs in ("ZII", "IZI", "ZZZ"):
            ref = dm3.expectation_pauli(obs)
            # 精确 Pauli 传播
            pe = PauliPropagator({obs: 1.0})
            for l_idx in reversed(range(3)):
                c, t = layers_cnot[l_idx]
                if p_test > 0.0:
                    pe.apply_depolarizing_adj(p_test)
                for q in range(3):
                    pe.apply_rz_adj(q, angles_z[q])
                    pe.apply_rx_adj(q, angles_x[q] * (l_idx + 1) * 0.5)
                pe.apply_cnot_adj(c, t)
            val_e = pe.expectation_product_state("0+0")
            max_err_3q = max(max_err_3q, abs(val_e - ref))
            assert abs(val_e - ref) < TOL

            # 权重截断 w <= 2 检验算符范数误差界
            pt = PauliPropagator({obs: 1.0})
            for l_idx in reversed(range(3)):
                c, t = layers_cnot[l_idx]
                if p_test > 0.0:
                    pt.apply_depolarizing_adj(p_test)
                pt.truncate_weight(max_weight=2)
                for q in range(3):
                    pt.apply_rz_adj(q, angles_z[q])
                    pt.apply_rx_adj(q, angles_x[q] * (l_idx + 1) * 0.5)
                pt.apply_cnot_adj(c, t)
            val_t = pt.expectation_product_state("0+0")
            assert abs(val_t - ref) <= pt.pruned_l1_bound + TOL
            if obs == "ZII":
                noise_sweep[f"p={p_test:.2f}"] = {
                    "exact": round(ref, 8),
                    "trunc_w2": round(val_t, 8),
                    "actual_err": round(abs(val_t - ref), 8),
                    "l1_bound": round(pt.pruned_l1_bound, 8),
                }

    return {
        "example_2q_exact": round(pp_exact_val, 10),
        "example_2q_trunc_w1": round(pp_trunc_val, 10),
        "example_2q_trunc_err": round(trunc_err, 10),
        "example_2q_l1_bound": round(pruned_l1, 10),
        "example_2q_vs_dm_err": err_2q,
        "example_3q_vs_dm_max_err": max_err_3q,
        "practice_21B_exact": round(exact_b, 10),
        "practice_21B_l1_bound": round(bound_b, 10),
        "noise_sweep_3q_ZII": noise_sweep,
    }


def main() -> None:
    report = {
        "script": "codes/algorithms/simulation_engines_lab.py",
        "dependencies": "Python 3 standard library only (no NumPy)",
        "tolerance": TOL,
        "engine_1_stabilizer_tableau": verify_tableau_engine(),
        "engine_2_mps_3qubit": verify_mps_engine(),
        "engine_3_pauli_propagation": verify_pauli_propagation_engine(),
        "status": "ALL_ASSERTIONS_PASSED",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
