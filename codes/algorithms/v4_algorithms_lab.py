#!/usr/bin/env python3
"""第二篇核心算法与 QSVT 共享验证脚本（纯 Python 3 标准库，零第三方依赖）。

覆盖章节与验证目标：
  - 第 06 章：显式 6 门 PREPARE/SELECT 块编码（H = 0.6X + 0.8Z）、
              Babbush (PRX 2018) 4 项 QROM 一元迭代门级查表（无控与受控两版）、
              固定点振幅放大（L = 3, 7）闭式与显式二维矩阵双路核对、
              量子计数（N = 16, M = 4, t = 4, 5）。
  - 第 07 章：量子微分方程 LCHS 1D 耗散核（柯西核 vs 2024 改进速降核）、
              Carleman 线性化 2x2 截断（R < 1 指数收敛 vs R > 1 崩溃边界）、
              Shor N = 35 连分数与 Dirichlet 峰、E(F_7) 椭圆曲线 ECDLP、
              1D/2D/3D 泊松方程条件数精确标度。
  - 第 08 章：H_2 2-qubit UCCSD 与 4 轨道 SQD+S-CORE 变分阶梯、
              K_3 QAOA p = 1 精确最优解、WS-QAOA 倾斜混合器与 XY-mixer、
              3 物品背包 QUBO 罚项阈值 P > 2、2 比特 4 态看涨期权小角度编码与 VaR/CVaR、
              QNG Bloch 球度规、数据再上传 L = 2 傅里叶系数、DLA 2 比特反例。
  - 第 16 章共用：显式 4x4 负谱矩阵 QSVT（pyqsp W 约定与 PennyLane R 约定 4 相位角，
              矩阵元最大误差均 < 1e-8，含 8x8 相干实部提取成功概率 0.00444112）。

依赖：仅使用 Python 3 标准库（argparse, cmath, json, math），不联网、不调用云服务。
运行命令：
    python3 codes/algorithms/v4_algorithms_lab.py
    python3 codes/algorithms/v4_algorithms_lab.py 06   # 可选 all / 06 / 07 / 08 / 16
注意：必须用普通 python3 运行，不能加关闭断言的 -O 参数。

基序与约定（严格对齐《符号表》）：
  - 多比特计算基采用高位在左（大端序）：|q_0 q_1 ... q_{n-1}>；
  - 内积采用左反线性共轭 <u|v> = sum_j conj(u_j) * v_j；
  - 电路从左到右施加，矩阵乘积从右到左作用在态矢量上。
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
from typing import Dict, List, Sequence, Tuple

if not __debug__:
    raise RuntimeError("请勿使用 -O 参数运行：本脚本的 assert 语句是核心数学验收门禁。")

TOL = 1e-12
Matrix = List[List[complex]]
Vector = List[complex]

# =============================================================================
# 零、纯标准库线性代数与小规模态矢量工具
# =============================================================================

I2: Matrix = [[1 + 0j, 0j], [0j, 1 + 0j]]
X2: Matrix = [[0j, 1 + 0j], [1 + 0j, 0j]]
Y2: Matrix = [[0j, -1j], [1j, 0j]]
Z2: Matrix = [[1 + 0j, 0j], [0j, -1 + 0j]]


def ry_mat(theta: float) -> Matrix:
    c = math.cos(theta / 2.0)
    s = math.sin(theta / 2.0)
    return [[c + 0j, -s + 0j], [s + 0j, c + 0j]]


def rx_mat(theta: float) -> Matrix:
    c = math.cos(theta / 2.0)
    s = math.sin(theta / 2.0)
    return [[c + 0j, -1j * s], [-1j * s, c + 0j]]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    ra, ca = len(a), len(a[0])
    cb = len(b[0])
    out = [[0j] * cb for _ in range(ra)]
    for i in range(ra):
        for k in range(ca):
            aik = a[i][k]
            if aik == 0:
                continue
            for j in range(cb):
                out[i][j] += aik * b[k][j]
    return out


def matvec(a: Matrix, v: Sequence[complex]) -> Vector:
    return [sum(aij * vj for aij, vj in zip(row, v)) for row in a]


def dagger(a: Matrix) -> Matrix:
    r, c = len(a), len(a[0])
    return [[a[i][j].conjugate() for i in range(r)] for j in range(c)]


def kron(a: Matrix, b: Matrix) -> Matrix:
    ra, ca = len(a), len(a[0])
    rb, cb = len(b), len(b[0])
    out = [[0j] * (ca * cb) for _ in range(ra * rb)]
    for i in range(ra):
        for j in range(ca):
            aij = a[i][j]
            if aij == 0:
                continue
            for k in range(rb):
                for l in range(cb):
                    out[i * rb + k][j * cb + l] = aij * b[k][l]
    return out


def vdot(u: Sequence[complex], v: Sequence[complex]) -> complex:
    return sum(a.conjugate() * b for a, b in zip(u, v))


def norm2(v: Sequence[complex]) -> float:
    return sum(abs(x) ** 2 for x in v)


def max_mat_diff(a: Matrix, b: Matrix) -> float:
    return max(abs(a[i][j] - b[i][j]) for i in range(len(a)) for j in range(len(a[0])))


def eye(n: int) -> Matrix:
    return [[1 + 0j if i == j else 0j for j in range(n)] for i in range(n)]


def jacobi_sym_eigh(a_in: List[List[float]], max_iter: int = 200) -> Tuple[List[float], List[List[float]]]:
    """实对称小矩阵的纯标准库 Jacobi 本征值分解，返回升序特征值与对应列特征向量。"""
    n = len(a_in)
    a = [row[:] for row in a_in]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_iter):
        p, q, max_val = 0, 1, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > max_val:
                    max_val = abs(a[i][j])
                    p, q = i, j
        if max_val < 1e-15:
            break
        diff = a[q][q] - a[p][p]
        if abs(diff) < 1e-15:
            t = 1.0 if a[p][q] >= 0 else -1.0
        else:
            tau = diff / (2.0 * a[p][q])
            t = math.copysign(1.0 / (abs(tau) + math.hypot(1.0, tau)), tau)
        c = 1.0 / math.hypot(1.0, t)
        s = t * c
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        a[p][p] = app - t * apq
        a[q][q] = aqq + t * apq
        a[p][q] = a[q][p] = 0.0
        for k in range(n):
            if k != p and k != q:
                akp, akq = a[k][p], a[k][q]
                a[k][p] = a[p][k] = c * akp - s * akq
                a[k][q] = a[q][k] = s * akp + c * akq
        for k in range(n):
            vkp, vkq = v[k][p], v[k][q]
            v[k][p] = c * vkp - s * vkq
            v[k][q] = s * vkp + c * vkq
    order = sorted(range(n), key=lambda idx: a[idx][idx])
    evals = [a[i][i] for i in order]
    evecs = [[v[row][i] for i in order] for row in range(n)]
    return evals, evecs


def apply_x_sv(st: Vector, q: int, n: int) -> Vector:
    out = st[:]
    bit = 1 << (n - 1 - q)
    for i in range(1 << n):
        if not (i & bit):
            out[i], out[i | bit] = st[i | bit], st[i]
    return out


def apply_cnot_sv(st: Vector, c: int, t: int, n: int) -> Vector:
    out = st[:]
    cb = 1 << (n - 1 - c)
    tb = 1 << (n - 1 - t)
    for i in range(1 << n):
        if (i & cb) and not (i & tb):
            out[i], out[i | tb] = st[i | tb], st[i]
    return out


def apply_toffoli_sv(st: Vector, c1: int, c2: int, t: int, n: int) -> Vector:
    out = st[:]
    b1 = 1 << (n - 1 - c1)
    b2 = 1 << (n - 1 - c2)
    tb = 1 << (n - 1 - t)
    for i in range(1 << n):
        if (i & b1) and (i & b2) and not (i & tb):
            out[i], out[i | tb] = st[i | tb], st[i]
    return out


# =============================================================================
# 一、第 06 章验证：6 门 PREPARE/SELECT、4 项 QROM 一元迭代、固定点放大与量子计数
# =============================================================================

def check_ch06() -> Dict[str, object]:
    # 1. 显式 6 门 PREPARE/SELECT 块编码：H = 0.6 X + 0.8 Z，alpha = 1.4
    alpha = 1.4
    theta = 2.0 * math.acos(math.sqrt(3.0 / 7.0))
    prep = kron(ry_mat(theta), I2)
    prep_dag = kron(ry_mat(-theta), I2)
    xa = kron(X2, I2)
    cz: Matrix = [
        [1 + 0j, 0j, 0j, 0j],
        [0j, 1 + 0j, 0j, 0j],
        [0j, 0j, 1 + 0j, 0j],
        [0j, 0j, 0j, -1 + 0j],
    ]
    cnot: Matrix = [
        [1 + 0j, 0j, 0j, 0j],
        [0j, 1 + 0j, 0j, 0j],
        [0j, 0j, 0j, 1 + 0j],
        [0j, 0j, 1 + 0j, 0j],
    ]
    # 电路从左到右：CZ -> X_a -> CNOT -> X_a；矩阵从右到左相乘
    select_gate = matmul(xa, matmul(cnot, matmul(xa, cz)))
    select_expected: Matrix = [
        [0j, 1 + 0j, 0j, 0j],
        [1 + 0j, 0j, 0j, 0j],
        [0j, 0j, 1 + 0j, 0j],
        [0j, 0j, 0j, -1 + 0j],
    ]
    assert max_mat_diff(select_gate, select_expected) < TOL
    # 完整 6 门块编码 U = PREPARE^dag * SELECT * PREPARE
    u_be = matmul(prep_dag, matmul(select_gate, prep))
    assert max_mat_diff(matmul(dagger(u_be), u_be), eye(4)) < TOL
    h_over_alpha: Matrix = [
        [0.8 / alpha + 0j, 0.6 / alpha + 0j],
        [0.6 / alpha + 0j, -0.8 / alpha + 0j],
    ]
    top_left = [[u_be[i][j] for j in range(2)] for i in range(2)]
    be_err = max_mat_diff(top_left, h_over_alpha)
    assert be_err < TOL

    # 2. Babbush (PRX 2018) 4 项 QROM 一元迭代（穷举全部 16 张 4-bit 数据表）
    for mask in range(16):
        table = [(mask >> (3 - idx)) & 1 for idx in range(4)]
        # (a) 无外控 4 比特版 |a1 a0 w b>：仅 2 对临时逻辑与（8 个 T 门）+ 2 次 CNOT 翻转复用
        st = [0j] * 16
        for j in range(4):
            st[j << 2] = 0.5 + 0j
        st = apply_x_sv(st, 0, 4)
        st = apply_x_sv(st, 1, 4)
        st = apply_toffoli_sv(st, 0, 1, 2, 4)  # AND #1: w = [00]
        if table[0]:
            st = apply_cnot_sv(st, 2, 3, 4)
        st = apply_cnot_sv(st, 0, 2, 4)  # 0-T 翻转：w = [01]
        if table[1]:
            st = apply_cnot_sv(st, 2, 3, 4)
        st = apply_x_sv(st, 1, 4)
        st = apply_toffoli_sv(st, 0, 1, 2, 4)  # 反计算清零 w = 0
        st = apply_x_sv(st, 0, 4)
        st = apply_x_sv(st, 1, 4)
        st = apply_toffoli_sv(st, 0, 1, 2, 4)  # AND #2: w = [10]
        if table[2]:
            st = apply_cnot_sv(st, 2, 3, 4)
        st = apply_cnot_sv(st, 0, 2, 4)  # 0-T 翻转：w = [11]
        if table[3]:
            st = apply_cnot_sv(st, 2, 3, 4)
        st = apply_x_sv(st, 1, 4)
        st = apply_toffoli_sv(st, 0, 1, 2, 4)  # 反计算清零 w = 0
        assert abs(norm2(st) - 1.0) < TOL
        for j in range(4):
            expected_idx = (j << 2) | table[j]
            assert abs(st[expected_idx] - 0.5) < TOL

        # (b) 带外控 6 比特版 |c a1 a0 w1 w2 b>：严格 L - 1 = 3 对临时逻辑与（12 个 T 门）
        st6 = [0j] * 64
        amp = 1.0 / math.sqrt(8.0)
        for cbit in (0, 1):
            for j in range(4):
                st6[(cbit << 5) | (j << 3)] = amp + 0j
        st6 = apply_x_sv(st6, 1, 6)
        st6 = apply_x_sv(st6, 2, 6)
        st6 = apply_toffoli_sv(st6, 0, 1, 3, 6)  # AND #1: w1 = c & ~a1
        st6 = apply_toffoli_sv(st6, 3, 2, 4, 6)  # AND #2: w2 = c & [00]
        if table[0]:
            st6 = apply_cnot_sv(st6, 4, 5, 6)
        st6 = apply_cnot_sv(st6, 3, 4, 6)  # w2 = c & [01]
        if table[1]:
            st6 = apply_cnot_sv(st6, 4, 5, 6)
        st6 = apply_x_sv(st6, 2, 6)
        st6 = apply_toffoli_sv(st6, 3, 2, 4, 6)  # 清零 w2
        st6 = apply_cnot_sv(st6, 0, 3, 6)  # w1 = c & a1（0 T 门）
        st6 = apply_x_sv(st6, 1, 6)
        st6 = apply_x_sv(st6, 2, 6)
        st6 = apply_toffoli_sv(st6, 3, 2, 4, 6)  # AND #3: w2 = c & [10]
        if table[2]:
            st6 = apply_cnot_sv(st6, 4, 5, 6)
        st6 = apply_cnot_sv(st6, 3, 4, 6)  # w2 = c & [11]
        if table[3]:
            st6 = apply_cnot_sv(st6, 4, 5, 6)
        st6 = apply_x_sv(st6, 2, 6)
        st6 = apply_toffoli_sv(st6, 3, 2, 4, 6)  # 清零 w2
        st6 = apply_toffoli_sv(st6, 0, 1, 3, 6)  # 清零 w1
        assert abs(norm2(st6) - 1.0) < TOL
        for cbit in (0, 1):
            for j in range(4):
                bval = table[j] if cbit else 0
                assert abs(st6[(cbit << 5) | (j << 3) | bval] - amp) < TOL

    # 3. 固定点振幅放大（Yoder–Low–Chuang 2014）：L = 3, 7，delta = 0.2，闭式 vs 二维矩阵双路核对
    delta = 0.2
    fp_records = []
    for ell, test_as in [(1, [0.50, 0.75]), (3, [0.25, 0.50])]:
        L = 2 * ell + 1
        gamma_inv = math.cosh(math.acosh(1.0 / delta) / L)
        gamma = 1.0 / gamma_inv
        betas = [
            2.0 * math.atan2(1.0, math.tan(math.pi * j / L) * math.sqrt(1.0 - gamma * gamma))
            for j in range(1, ell + 1)
        ]
        alphas = list(reversed(betas))
        for a_val in test_as:
            # 路径 A：Chebyshev 闭式
            u = math.sqrt(1.0 - a_val) / gamma
            tl = math.cos(L * math.acos(u)) if u <= 1.0 else math.cosh(L * math.acosh(u))
            p_closed = 1.0 - (delta * tl) ** 2
            # 路径 B：显式二维矩阵连乘
            psi0 = [math.sqrt(1.0 - a_val) + 0j, math.sqrt(a_val) + 0j]
            state = psi0[:]
            for aj, bj in zip(alphas, betas):
                state = [state[0], cmath.exp(1j * aj) * state[1]]
                ov = vdot(psi0, state)
                fac = 1.0 - cmath.exp(1j * bj)
                state = [state[0] - fac * ov * psi0[0], state[1] - fac * ov * psi0[1]]
            p_mat = abs(state[1]) ** 2
            assert abs(p_closed - p_mat) < TOL
            assert p_closed >= 1.0 - delta * delta - TOL
            fp_records.append({"L": L, "a": a_val, "p_success": round(p_closed, 6)})
    # 检验精确最小 L vs 充分条件 ln(2/delta)/sqrt(lambda)
    lam_test = 0.25
    L_exact_min = math.acosh(1.0 / delta) / math.acosh(1.0 / math.sqrt(1.0 - lam_test))
    L_suff = math.log(2.0 / delta) / math.sqrt(lam_test)
    assert L_suff > L_exact_min

    # 4. 量子计数 N = 16, M = 4（t = 4, 5）
    qc_records = {}
    for t_bits, y_peak, p_expected, m_expected in [
        (4, 3, 0.6885, 4.94),
        (5, 5, 0.6852, 3.56),
    ]:
        Q = 1 << t_bits
        def amp_dir(y: int, phi: float) -> complex:
            return sum(cmath.exp(2j * math.pi * k * (phi - y / Q)) for k in range(Q)) / Q
        p_pair = (
            0.5 * (abs(amp_dir(y_peak, 1 / 6)) ** 2 + abs(amp_dir(y_peak, 5 / 6)) ** 2)
            + 0.5 * (abs(amp_dir(Q - y_peak, 1 / 6)) ** 2 + abs(amp_dir(Q - y_peak, 5 / 6)) ** 2)
        )
        m_hat = 16.0 * math.sin(math.pi * y_peak / Q) ** 2
        assert abs(p_pair - p_expected) < 5e-4
        assert abs(m_hat - m_expected) < 0.01
        qc_records[f"t={t_bits}"] = {"peak_pair_prob": round(p_pair, 4), "M_hat": round(m_hat, 2)}

    return {
        "prepare_select_theta_rad": round(theta, 6),
        "prepare_select_block_error": be_err,
        "qrom_4item_all16_tables_verified": True,
        "fixed_point_aa": fp_records,
        "fixed_point_L_exact_vs_sufficient_at_lam025": [round(L_exact_min, 4), round(L_suff, 4)],
        "quantum_counting": qc_records,
    }


# =============================================================================
# 二、第 07 章验证：LCHS 1D 耗散核、Carleman 2x2 截断、Shor 35、ECDLP、泊松条件数
# =============================================================================

def check_ch07() -> Dict[str, object]:
    # 1. LCHS 1D 耗散方程 du/dt = -gamma u (L = gamma = 1.0, H = 0, t = 1.5)
    gamma, t_evol = 1.0, 1.5
    u_exact = math.exp(-gamma * t_evol)

    def lchs_cauchy(K: float, M: int) -> complex:
        dk = 2.0 * K / M
        total = 0j
        for j in range(M):
            k = -K + (j + 0.5) * dk
            total += (1.0 / (math.pi * (1.0 + k * k))) * cmath.exp(-1j * k * gamma * t_evol) * dk
        return total

    def lchs_acl(K: float, M: int, beta: float = 0.8) -> complex:
        """An–Childs–Lin (2024) 改进核：f_beta(k) = e^{2^beta} / (2 pi (1 - ik) exp((1 + ik)^beta))。"""
        dk = 2.0 * K / M
        c_norm = math.exp(2.0 ** beta) / (2.0 * math.pi)
        total = 0j
        for j in range(M):
            k = -K + (j + 0.5) * dk
            fk = c_norm / ((1.0 - 1j * k) * cmath.exp((1.0 + 1j * k) ** beta))
            total += fk * cmath.exp(-1j * k * gamma * t_evol) * dk
        return total

    cauchy_10 = lchs_cauchy(10.0, 400)
    cauchy_50 = lchs_cauchy(50.0, 2000)
    cauchy_200 = lchs_cauchy(200.0, 8000)
    err_c10, err_c50, err_c200 = abs(cauchy_10 - u_exact), abs(cauchy_50 - u_exact), abs(cauchy_200 - u_exact)
    assert err_c200 < err_c50 < err_c10 and err_c200 < 2e-5
    acl_50 = lchs_acl(50.0, 2000, beta=0.8)
    err_acl50 = abs(acl_50 - u_exact)
    assert err_acl50 < 1e-5 and err_acl50 < err_c50

    # 2. Carleman 线性化 2x2 截断：du/dt = -u + eps * u^2，u(0) = u0
    def carleman_2x2_exp(eps: float, u0: float, tt: float) -> Tuple[float, float]:
        # 直接泰勒级数计算 exp(A_carl * t) * [u0, u0^2]^T，与解析闭式双路互验
        A = [[-1.0 + 0j, eps + 0j], [0j, -2.0 + 0j]]
        vec: Vector = [u0 + 0j, u0 * u0 + 0j]
        term = vec[:]
        out = vec[:]
        for k in range(1, 60):
            term = [z * tt / k for z in matvec(A, term)]
            out = [a + b for a, b in zip(out, term)]
        y1_closed = u0 * math.exp(-tt) * (1.0 + eps * u0 * (1.0 - math.exp(-tt)))
        assert abs(out[0].real - y1_closed) < TOL
        assert abs(out[1].real - u0 * u0 * math.exp(-2.0 * tt)) < TOL
        return y1_closed, out[0].real

    # 弱非线性 R = 0.2 < 1：二阶截断误差仅 ~0.0067，且高阶按 R^N 几何收敛
    y1_weak, _ = carleman_2x2_exp(0.2, 1.0, 1.0)
    u_ex_weak = math.exp(-1.0) / (1.0 - 0.2 * (1.0 - math.exp(-1.0)))
    err_weak = abs(y1_weak - u_ex_weak)
    assert err_weak < 0.01
    # 强非线性 R = 1.5 > 1：精确解在 t* = ln(3) ~ 1.0986 处爆破，t = 1.0 时已达 7.099，Carleman 却衰减至 0.717
    y1_strong, _ = carleman_2x2_exp(1.5, 1.0, 1.0)
    u_ex_strong = math.exp(-1.0) / (1.0 - 1.5 * (1.0 - math.exp(-1.0)))
    assert u_ex_strong > 7.0 and y1_strong < 1.0 and abs(y1_strong - u_ex_strong) > 6.0

    # 3. Shor N = 35, a = 2：连分数与 Dirichlet 峰概率
    order = 1
    while pow(2, order, 35) != 1:
        order += 1
    assert order == 12
    num, den = 171, 2048
    cf = []
    a_cf, b_cf = num, den
    while b_cf:
        cf.append(a_cf // b_cf)
        a_cf, b_cf = b_cf, a_cf % b_cf
    assert cf == [0, 11, 1, 41, 1, 3]
    p_171 = (math.sin(math.pi / 3.0) / (2048.0 * math.sin(math.pi / 6144.0))) ** 2
    assert abs(p_171 - 0.6839) < 2e-4

    # 4. E(F_7): y^2 = x^3 + x + 1 (mod 7) 群表与 ECDLP
    pts = [None]
    for x in range(7):
        rhs = (x * x * x + x + 1) % 7
        for y in range(7):
            if (y * y) % 7 == rhs:
                pts.append((x, y))
    assert len(pts) == 5

    def ec_add(p1, p2):
        if p1 is None:
            return p2
        if p2 is None:
            return p1
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2 and (y1 + y2) % 7 == 0:
            return None
        if p1 == p2:
            lam = ((3 * x1 * x1 + 1) * pow(2 * y1, -1, 7)) % 7
        else:
            lam = ((y2 - y1) * pow((x2 - x1) % 7, -1, 7)) % 7
        x3 = (lam * lam - x1 - x2) % 7
        y3 = (lam * (x1 - x3) - y1) % 7
        return (x3, y3)

    P = (0, 1)
    P2 = ec_add(P, P)
    P3 = ec_add(P2, P)
    P4 = ec_add(P3, P)
    P5 = ec_add(P4, P)
    assert P2 == (2, 5) and P3 == (2, 2) and P4 == (0, 6) and P5 is None
    assert (1 * pow(2, -1, 5)) % 5 == 3  # (u, v) = (2, 1) -> d = 3

    # 5. 泊松方程条件数 m = 100
    m = 100
    kappa_exact = (1.0 / math.tan(math.pi / (2.0 * (m + 1)))) ** 2
    kappa_approx = (4.0 / (math.pi ** 2)) * (m + 1) ** 2
    assert abs(kappa_exact - 4133.6) < 0.2 and abs(kappa_approx - 4134.3) < 0.2

    return {
        "lchs_exact_u": round(u_exact, 8),
        "lchs_cauchy_K50_err": round(err_c50, 7),
        "lchs_acl_beta08_K50_err": round(err_acl50, 8),
        "carleman_R02_t1_exact_vs_2x2": [round(u_ex_weak, 6), round(y1_weak, 6)],
        "carleman_R15_t1_exact_vs_2x2": [round(u_ex_strong, 6), round(y1_strong, 6)],
        "shor35_cf": cf,
        "shor35_p171": round(p_171, 4),
        "ecdlp_order": len(pts),
        "poisson_m100_kappa": round(kappa_exact, 2),
    }


# =============================================================================
# 三、第 08 章验证：H_2/SQD、K_3/WS-QAOA/背包、期权/VaR/CVaR、QNG/再上传/DLA
# =============================================================================

def check_ch08() -> Dict[str, object]:
    # 1. H_2 (O'Malley 2016 Table I, R = 0.75 A) 与 4 轨道 SQD + S-CORE 变分阶梯
    g0, g1, g2, g3, g4 = 0.2252, 0.3435, -0.4347, 0.5716, 0.0910
    h10 = g0 - g1 + g2 - g3
    h01 = g0 + g1 - g2 - g3
    assert abs(h10 - (-1.1246)) < 1e-12 and abs(h01 - 0.4318) < 1e-12
    theta_star = 0.5 * math.atan(-2.0 * g4 / (g1 - g2))
    e_fci_2q = (g0 - g3) - math.hypot(g1 - g2, 2.0 * g4)
    assert abs(theta_star - (-0.11487)) < 1e-4
    assert abs(e_fci_2q - (-1.1456)) < 1e-4
    # 4 轨道 SQD + S-CORE 投影矩阵
    h_sqd4 = [
        [-1.1246, 0.1820, 0.0800, 0.0800],
        [0.1820, 0.4318, -0.0500, -0.0500],
        [0.0800, -0.0500, -0.2000, 0.0400],
        [0.0800, -0.0500, 0.0400, -0.2000],
    ]
    e_s0 = jacobi_sym_eigh([row[:2] for row in h_sqd4[:2]])[0][0]
    e_s1 = jacobi_sym_eigh([row[:3] for row in h_sqd4[:3]])[0][0]
    e_full = jacobi_sym_eigh(h_sqd4)[0][0]
    assert abs(e_s0 - (-1.1456)) < 1e-4
    assert abs(e_s1 - (-1.1532)) < 1e-4
    assert abs(e_full - (-1.1601)) < 1e-4
    assert -1.1246 > e_s0 > e_s1 > e_full

    # 2. K_3 QAOA p = 1 精确态矢量验算 + WS-QAOA 倾斜混合器 + XY-mixer + 3 物品背包
    gamma_k3 = math.asin(1.0 / math.sqrt(3.0))
    beta_k3 = gamma_k3 / 2.0
    # 8 维态矢量：每个比特串的 K_3 割值
    cut_k3 = [0, 2, 2, 2, 2, 2, 2, 0]
    psi = [cmath.exp(-1j * gamma_k3 * c) / math.sqrt(8.0) for c in cut_k3]
    u_mix1 = rx_mat(2.0 * beta_k3)
    u_mix3 = kron(kron(u_mix1, u_mix1), u_mix1)
    psi_out = matvec(u_mix3, psi)
    probs_k3 = [abs(z) ** 2 for z in psi_out]
    exp_k3 = sum(p * c for p, c in zip(probs_k3, cut_k3))
    assert abs(exp_k3 - 2.0) < TOL
    assert probs_k3[0] < TOL and probs_k3[7] < TOL
    for idx in range(1, 7):
        assert abs(probs_k3[idx] - 1.0 / 6.0) < TOL

    # WS-QAOA 倾斜混合器验证：对任意 c* in (0, 1)，theta = 2 arcsin(sqrt(c*))
    c_star = 0.25
    th_ws = 2.0 * math.asin(math.sqrt(c_star))
    psi_ws = matvec(ry_mat(th_ws), [1 + 0j, 0j])
    h_ws: Matrix = [
        [-math.cos(th_ws) + 0j, -math.sin(th_ws) + 0j],
        [-math.sin(th_ws) + 0j, math.cos(th_ws) + 0j],
    ]
    # 验证 H_B^WS |psi_ws> = -|psi_ws>（精确基态，本征值 -1）
    out_ws = matvec(h_ws, psi_ws)
    assert max(abs(out_ws[i] + psi_ws[i]) for i in range(2)) < TOL
    # 标准混合器 -X 在 theta != pi/2 时不是本征态
    out_std = matvec([[-X2[i][j] for j in range(2)] for i in range(2)], psi_ws)
    assert abs(vdot(psi_ws, out_std).real + 1.0) > 0.1

    # n = 3, K = 1 one-hot XY-mixer 子空间不变性（仅检查 (X_0X_1+Y_0Y_1)/2 等保汉明重量）
    xy2: Matrix = [
        [0j, 0j, 0j, 0j],
        [0j, 0j, 1 + 0j, 0j],
        [0j, 1 + 0j, 0j, 0j],
        [0j, 0j, 0j, 0j],
    ]
    h_xy3 = [
        [
            kron(xy2, I2)[i][j] + kron(I2, xy2)[i][j]
            for j in range(8)
        ]
        for i in range(8)
    ]
    # 从 |100>（下标 4，汉明重 1）出发，H_xy3 作用后仅分布在汉明重 1 的基态 {1, 2, 4}
    v_one_hot = [1 + 0j if i == 4 else 0j for i in range(8)]
    v_after = matvec(h_xy3, v_one_hot)
    for idx in range(8):
        if bin(idx).count("1") != 1:
            assert abs(v_after[idx]) < TOL

    # 3 物品 0-1 背包临界罚项 P > 2
    values = [3, 2, 4]
    weights = [2, 3, 4]
    cap = 5
    for P_pen, expect_feasible_best in [(1.5, False), (2.5, True)]:
        best_val = 1e9
        best_x = None
        for xbits in range(8):
            x = [(xbits >> 2) & 1, (xbits >> 1) & 1, xbits & 1]
            w_tot = sum(a * b for a, b in zip(weights, x))
            v_tot = sum(a * b for a, b in zip(values, x))
            # 松弛变量 s in {0..5} 可最小化 (w_tot + s - cap)^2
            viol = max(0, w_tot - cap)
            f_min = -v_tot + P_pen * (viol ** 2)
            if f_min < best_val:
                best_val = f_min
                best_x = x
        assert (best_x == [1, 1, 0]) == expect_feasible_best

    # 3. 2 比特 4 态离散看涨期权小角度编码与 VaR / CVaR
    spots = [80.0, 95.0, 110.0, 130.0]
    strike = 100.0
    payoffs = [max(s - strike, 0.0) for s in spots]
    assert payoffs == [0.0, 0.0, 10.0, 30.0]
    exact_call = sum(payoffs) / 4.0
    assert abs(exact_call - 10.0) < TOL
    f_max = 30.0
    f_tilde = [p / f_max for p in payoffs]
    # 小角度线性旋转 R_y(pi/2 + 2 c (f_tilde - 1/2))：p(1) = sin^2(pi/4 + c(f_tilde - 1/2))
    biases = {}
    for c_scale in (0.2, 0.1, 0.05):
        p1 = sum(math.sin(math.pi / 4.0 + c_scale * (ft - 0.5)) ** 2 for ft in f_tilde) / 4.0
        est_tilde = 0.5 + (p1 - 0.5) / c_scale
        est_call = est_tilde * f_max
        biases[str(c_scale)] = round(abs(est_call - exact_call), 6)
    # 误差按 O(c^2) 缩小（因还原时除以 c，原始 O(c^3) 除以 c 得 O(c^2) 偏差）
    assert biases["0.05"] < biases["0.1"] < biases["0.2"]
    assert abs(biases["0.1"] / biases["0.05"] - 4.0) < 0.05

    # VaR vs CVaR（alpha = 0.75）
    losses = [0.0, 10.0, 20.0, 100.0]
    probs_l = [0.50, 0.25, 0.20, 0.05]
    cdf = 0.0
    var_75 = 0.0
    for loss, pr in zip(losses, probs_l):
        cdf += pr
        if cdf >= 0.75 - 1e-12:
            var_75 = loss
            break
    tail_prob = sum(pr for loss, pr in zip(losses, probs_l) if loss > var_75)
    cvar_75 = sum(loss * pr for loss, pr in zip(losses, probs_l) if loss > var_75) / tail_prob
    assert abs(var_75 - 10.0) < TOL and abs(cvar_75 - 36.0) < TOL

    # 4. QNG Bloch 度规、数据再上传 L = 2、DLA 2 比特反例
    th_qng = 0.2
    g_phiphi_inv = 4.0 / (math.sin(th_qng) ** 2)
    assert abs(g_phiphi_inv - 101.34) < 0.05

    # 数据再上传 L = 2：U_2(x; th1, th2) = Ry(th2) Rx(x) Ry(th1) Rx(x)
    for x_val, th1, th2 in [(0.7, 0.4, 1.1), (1.3, 0.0, 0.0), (0.9, math.pi, 0.0)]:
        u2 = matmul(ry_mat(th2), matmul(rx_mat(x_val), matmul(ry_mat(th1), rx_mat(x_val))))
        st2 = matvec(u2, [1 + 0j, 0j])
        exp_z = vdot(st2, matvec(Z2, st2)).real
        formula = (
            -math.sin(th2) * math.sin(th1) * math.cos(x_val)
            + math.cos(th2) * (0.5 * (math.cos(th1) - 1.0) + 0.5 * (math.cos(th1) + 1.0) * math.cos(2.0 * x_val))
        )
        assert abs(exp_z - formula) < TOL

    # DLA 2 比特反例：g = span{iX1, iY1, iZ1}, O = Z1 Z2 -> P_g(O) = 0，但真实方差 = 1/3
    z1z2 = kron(Z2, Z2)
    basis_g = [kron([[0.5 * p[i][j] for j in range(2)] for i in range(2)], I2) for p in (X2, Y2, Z2)]
    p_g_o = sum(abs(sum(matmul(b, z1z2)[k][k] for k in range(4))) ** 2 for b in basis_g)
    assert abs(p_g_o) < TOL  # 盲套简化公式得 0，但真实 SU(2) 均值 0、方差 1/3

    return {
        "h2_efci": round(e_fci_2q, 4),
        "sqd_ladder": [round(x, 4) for x in (-1.1246, e_s0, e_s1, e_full)],
        "k3_qaoa_max_cut": round(exp_k3, 6),
        "option_small_angle_biases": biases,
        "var_75": var_75,
        "cvar_75": cvar_75,
        "dla_counterexample_Pg_O": p_g_o,
    }


# =============================================================================
# 四、第 16 章共用验证：显式 4x4 负谱 QSVT（pyqsp W 约定 + PennyLane R 约定）
# =============================================================================

def check_ch16_qsvt() -> Dict[str, object]:
    """独立验证 A = [[0.2, 0.3], [0.3, -0.4]] 上 P(x) = 0.3 T_1(x) + 0.2 T_3(x) = 0.8x^3 - 0.3x。

    同时验证两套主流软件包的 4 相位角与 4x4 块编码矩阵（误差均严格 < 1e-8）：
      1. pyqsp 对称 W(A) 约定：Im[U_W[:2, :2]] = P(A)；
      2. PennyLane 反射 R(A) 约定：Re[U_R[:2, :2]] = P(A)，配 8x8 相干实部提取器得 p_succ = 0.00444112。
    """
    A_real = [[0.2, 0.3], [0.3, -0.4]]
    evals, evecs = jacobi_sym_eigh(A_real)
    assert abs(evals[0] - (-0.1 - 0.3 * math.sqrt(2.0))) < TOL
    assert abs(evals[1] - (-0.1 + 0.3 * math.sqrt(2.0))) < TOL

    # 精确目标矩阵 P(A) = 0.8 A^3 - 0.3 A
    A_c: Matrix = [[A_real[i][j] + 0j for j in range(2)] for i in range(2)]
    A3 = matmul(matmul(A_c, A_c), A_c)
    P_A: Matrix = [[0.8 * A3[i][j] - 0.3 * A_c[i][j] for j in range(2)] for i in range(2)]
    P_A_hand: Matrix = [[-0.0536 + 0j, -0.0396 + 0j], [-0.0396 + 0j, 0.0256 + 0j]]
    assert max_mat_diff(P_A, P_A_hand) < TOL

    # 构造 sqrt(I - A^2)
    S_c: Matrix = [[0j, 0j], [0j, 0j]]
    for k in range(2):
        sk = math.sqrt(1.0 - evals[k] ** 2)
        for i in range(2):
            for j in range(2):
                S_c[i][j] += sk * evecs[i][k] * evecs[j][k]
    # 核对 A^2 + S^2 = I_2
    assert max_mat_diff(
        [[matmul(A_c, A_c)[i][j] + matmul(S_c, S_c)[i][j] for j in range(2)] for i in range(2)],
        I2,
    ) < TOL

    def proj_phase(phi: float) -> Matrix:
        ep, em = cmath.exp(1j * phi), cmath.exp(-1j * phi)
        return [
            [ep if (i == j and i < 2) else (em if i == j else 0j) for j in range(4)]
            for i in range(4)
        ]

    # --- 约定 1：pyqsp W(A) = [[A, iS], [iS, A]] ---
    W_A: Matrix = [
        [A_c[i][j] for j in range(2)] + [1j * S_c[i][j] for j in range(2)] for i in range(2)
    ] + [
        [1j * S_c[i][j] for j in range(2)] + [A_c[i][j] for j in range(2)] for i in range(2)
    ]
    assert max_mat_diff(matmul(dagger(W_A), W_A), eye(4)) < TOL
    phi_pyqsp = [0.10328832343060845, 0.15851106436854098, 0.15851106436854098, 0.10328832343060845]
    U_w = proj_phase(phi_pyqsp[0])
    for phi in phi_pyqsp[1:]:
        U_w = matmul(matmul(U_w, W_A), proj_phase(phi))
    assert max_mat_diff(matmul(dagger(U_w), U_w), eye(4)) < TOL
    err_pyqsp_mat = max(abs(U_w[i][j].imag - P_A[i][j].real) for i in range(2) for j in range(2))
    assert err_pyqsp_mat < 1e-8

    # 标量网格 [-1, 1] 101 点复验
    max_scalar_err = 0.0
    for idx in range(101):
        xv = -1.0 + 2.0 * idx / 100.0
        sv = math.sqrt(max(0.0, 1.0 - xv * xv))
        Wx: Matrix = [[xv + 0j, 1j * sv], [1j * sv, xv + 0j]]
        Ux: Matrix = [[cmath.exp(1j * phi_pyqsp[0]), 0j], [0j, cmath.exp(-1j * phi_pyqsp[0])]]
        for phi in phi_pyqsp[1:]:
            pz = [[cmath.exp(1j * phi), 0j], [0j, cmath.exp(-1j * phi)]]
            Ux = matmul(matmul(Ux, Wx), pz)
        target_x = 0.8 * (xv ** 3) - 0.3 * xv
        max_scalar_err = max(max_scalar_err, abs(Ux[0][0].imag - target_x))
    assert max_scalar_err < 1e-8

    # --- 约定 2：PennyLane 反射块编码 R(A) = [[A, S], [S, -A]] ---
    R_A: Matrix = [
        [A_c[i][j] for j in range(2)] + [S_c[i][j] for j in range(2)] for i in range(2)
    ] + [
        [S_c[i][j] for j in range(2)] + [-A_c[i][j] for j in range(2)] for i in range(2)
    ]
    assert max_mat_diff(matmul(dagger(R_A), R_A), eye(4)) < TOL
    phi_pl = [-2.356194490192345, 1.5707963267948966, 1.2589132284153062, 0.5736824861793173]
    U_r = proj_phase(phi_pl[0])
    for phi in phi_pl[1:]:
        U_r = matmul(matmul(U_r, R_A), proj_phase(phi))
    assert max_mat_diff(matmul(dagger(U_r), U_r), eye(4)) < TOL
    err_pl_mat = max(abs(U_r[i][j].real - P_A[i][j].real) for i in range(2) for j in range(2))
    assert err_pl_mat < 1e-8

    # 8x8 相干实部提取器：(H x I_4) diag(U_r, U_r^*) (H x I_4) 左上 2x2 精确等于 P(A)
    h1: Matrix = [[1 / math.sqrt(2) + 0j, 1 / math.sqrt(2) + 0j], [1 / math.sqrt(2) + 0j, -1 / math.sqrt(2) + 0j]]
    hs = kron(h1, eye(4))
    sel = [[0j] * 8 for _ in range(8)]
    for i in range(4):
        for j in range(4):
            sel[i][j] = U_r[i][j]
            sel[i + 4][j + 4] = U_r[i][j].conjugate()
    combined = matmul(hs, matmul(sel, hs))
    err_extracted = max(abs(combined[i][j] - P_A[i][j]) for i in range(2) for j in range(2))
    assert err_extracted < 1e-8
    p_succ = abs(combined[0][0]) ** 2 + abs(combined[1][0]) ** 2
    assert abs(p_succ - 0.00444112) < 1e-10

    return {
        "pyqsp_W_4x4_max_error": err_pyqsp_mat,
        "pyqsp_W_scalar_grid_max_error": max_scalar_err,
        "pennylane_R_4x4_max_error": err_pl_mat,
        "coherent_real_extractor_error": err_extracted,
        "extracted_p_succ": round(p_succ, 8),
    }


CASES = {
    "06": check_ch06,
    "07": check_ch07,
    "08": check_ch08,
    "16": check_ch16_qsvt,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="第二篇核心算法与 QSVT 纯标准库验证脚本")
    parser.add_argument("case", nargs="?", default="all", choices=["all", *CASES])
    args = parser.parse_args()
    out = {k: fn() for k, fn in CASES.items() if args.case in ("all", k)}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
