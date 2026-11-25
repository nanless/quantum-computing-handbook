#!/usr/bin/env python3
"""第 15 章与第 08 章统计/误差缓解/等价性验证脚本（纯 Python 3 标准库，零第三方依赖）。

覆盖验证目标：
  1. ZNE 固定总 shots 预算精确倍率：
     - 两点线性 c = (1, 2)（权重 2, -1）：单档方差 5v，固定总预算均分 10x、最优 2:1 为 9x；
     - 两点线性 c = (1, 3)（权重 3/2, -1/2）：固定总预算均分 5x、最优 3:1 为 4x；
     - 三点 Richardson c = (1, 2, 3)（权重 3, -3, 1）：单档方差 19v，固定总预算均分 57x、最优 3:3:1 为 49x；
     - 指数衰减噪声曲线偏差对比与单比特退极化 PEC 因子。
  2. Bootstrap（百分位、BCa、Cluster Bootstrap）vs Wilson / Clopper–Pearson：
     - Wald vs Wilson 精确二项覆盖率（N = 100, p = 0.05 -> 87.75%, p = 0.03 -> 80.22%）；
     - 零失败边界（k = 0, N = 1000）反例：朴素 Bootstrap 与 Wald 均崩溃至 [0, 0]，
       而 Wilson 给出 [0, 0.003827]，单侧 Clopper–Pearson 给出 0.002991；
     - Bell 三基原始计数非线性根保真度 F = sqrt(f) 的 95% 百分位与 BCa Bootstrap 区间
       vs Hoeffding 保守下界 0.7675；
     - 10 批漂移序列 Pearson chi^2、Cluster SE（1.59 倍）与 Cluster Bootstrap 对比。
  3. 少聚类自由度 t_{B-1} 分位数与蒙特卡洛覆盖率检验（B = 4 与 B = 10）：
     - 纯标准库精确计算 t_{3, 0.975} = 3.1824 与 t_{9, 0.975} = 2.2622；
     - 10,000 次固定种子蒙特卡洛试验核验：B = 4 时错用 z = 1.96 导致覆盖率跌至 ~85.5%，
       换用 t_{3, 0.975} 精确恢复至 ~95.0%；同步核验 Holm–Bonferroni 与 BH-FDR 五项表。
  4. 纯标准库 O(2^n) 张量切片态矢量引擎与线路等价性验证（QCEC 第一层随机乘积态快速证伪 +
     容许比特置换与全局相位的精确酉等价检查）。

依赖：仅使用 Python 3 标准库（cmath, json, math, random, statistics），不联网、不调用云服务。
运行命令：
    python3 codes/practice/v4_practice_lab.py
注意：必须用普通 python3 运行，不能加关闭断言的 -O 参数。
"""

from __future__ import annotations

import cmath
import json
import math
import random
import statistics
from typing import Dict, List, Sequence, Tuple

if not __debug__:
    raise RuntimeError("请勿使用 -O 参数运行：本脚本的 assert 语句是核心统计验收门禁。")

TOL = 1e-12
SEED = 20261125
Z_975 = 1.959963984540054


# =============================================================================
# 零、纯标准库正态与学生 t 分布分位数（无 SciPy 依赖）
# =============================================================================

def norm_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def norm_ppf(p: float) -> float:
    assert 0.0 < p < 1.0
    lo, hi = -10.0, 10.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if norm_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def student_t_cdf(t: float, df: int) -> float:
    """用复合 Simpson 积分精确计算自由度为 df 的学生 t 分布 CDF。"""
    if t == 0.0:
        return 0.5
    c_norm = math.gamma(0.5 * (df + 1)) / (math.sqrt(df * math.pi) * math.gamma(0.5 * df))
    x_abs = abs(t)
    n_steps = 800  # 偶数，满足 Simpson 精度 < 1e-11
    h = x_abs / n_steps
    acc = 1.0 + (1.0 + (x_abs * x_abs) / df) ** (-0.5 * (df + 1))
    for k in range(1, n_steps):
        xk = k * h
        w = 4.0 if (k % 2 == 1) else 2.0
        acc += w * ((1.0 + (xk * xk) / df) ** (-0.5 * (df + 1)))
    integral = c_norm * acc * h / 3.0
    return 0.5 + integral if t > 0.0 else 0.5 - integral


def student_t_ppf(p: float, df: int) -> float:
    assert 0.5 < p < 1.0
    lo, hi = 0.0, 30.0
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        if student_t_cdf(mid, df) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def wilson_ci(k: int, n: int, z: float = Z_975) -> Tuple[float, float]:
    phat = k / n
    den = 1.0 + (z * z) / n
    center = (phat + (z * z) / (2.0 * n)) / den
    half = z * math.sqrt(phat * (1.0 - phat) / n + (z * z) / (4.0 * n * n)) / den
    return (max(0.0, center - half), min(1.0, center + half))


def wald_ci(k: int, n: int, z: float = Z_975) -> Tuple[float, float]:
    phat = k / n
    half = z * math.sqrt(phat * (1.0 - phat) / n)
    return (phat - half, phat + half)


# =============================================================================
# 一、ZNE 固定总预算采样倍率与 PEC 核验
# =============================================================================

def check_zne_and_pec() -> Dict[str, object]:
    def richardson_weights(cs: Sequence[float]) -> List[float]:
        ws = []
        for k, ck in enumerate(cs):
            prod = 1.0
            for j, cj in enumerate(cs):
                if j != k:
                    prod *= cj / (cj - ck)
            ws.append(prod)
        return ws

    # 1. 两点线性 c = (1, 2)
    w12 = richardson_weights([1.0, 2.0])
    assert abs(w12[0] - 2.0) < TOL and abs(w12[1] - (-1.0)) < TOL
    var_per_point_12 = sum(w * w for w in w12)  # 每档各投入 S 发（合计 2S 发）
    total_equal_12 = len(w12) * var_per_point_12  # 固定总 shots N 均分：m * sum(w_k^2) = 10x
    total_opt_12 = sum(abs(w) for w in w12) ** 2  # Cauchy-Schwarz 最优配比 2:1：(2+1)^2 = 9x
    assert abs(var_per_point_12 - 5.0) < TOL
    assert abs(total_equal_12 - 10.0) < TOL
    assert abs(total_opt_12 - 9.0) < TOL

    # 2. 两点线性 c = (1, 3)（对应 P15-B）
    w13 = richardson_weights([1.0, 3.0])
    assert abs(w13[0] - 1.5) < TOL and abs(w13[1] - (-0.5)) < TOL
    total_equal_13 = len(w13) * sum(w * w for w in w13)  # 2 * 2.5 = 5x
    total_opt_13 = sum(abs(w) for w in w13) ** 2  # (1.5 + 0.5)^2 = 4x
    assert abs(total_equal_13 - 5.0) < TOL and abs(total_opt_13 - 4.0) < TOL

    # 3. 三点 Richardson c = (1, 2, 3)
    w123 = richardson_weights([1.0, 2.0, 3.0])
    assert [round(w, 12) for w in w123] == [3.0, -3.0, 1.0]
    var_per_point_123 = sum(w * w for w in w123)  # 19v
    total_equal_123 = len(w123) * var_per_point_123  # 3 * 19 = 57x
    total_opt_123 = sum(abs(w) for w in w123) ** 2  # (3 + 3 + 1)^2 = 49x
    assert abs(var_per_point_123 - 19.0) < TOL
    assert abs(total_equal_123 - 57.0) < TOL
    assert abs(total_opt_123 - 49.0) < TOL
    # 独立直接代入 N_k = N * |w_k| / sum|w| 复核最优方差上界
    N_tot = 7000
    n_opt_123 = [3000, 3000, 1000]
    assert sum(n_opt_123) == N_tot
    var_opt_direct = sum(w * w / nk for w, nk in zip(w123, n_opt_123))
    assert abs(var_opt_direct - 49.0 / N_tot) < TOL

    # 4. 指数衰减曲线 E(c) = -exp(-0.15 c) 残余偏差核对
    e1, e2, e3 = (-math.exp(-0.15 * c) for c in (1, 2, 3))
    bias_raw = abs(e1 - (-1.0))
    bias_lin = abs((2 * e1 - e2) - (-1.0))
    bias_rich = abs((3 * e1 - 3 * e2 + e3) - (-1.0))
    assert abs(bias_raw - 0.139292) < 1e-6
    assert abs(bias_lin - 0.019402) < 1e-6
    assert abs(bias_rich - 0.002703) < 1e-6

    # 5. 单比特退极化 PEC 因子与多深度放大
    p_dep = 0.02
    gamma_pec = (1.0 + p_dep / 2.0) / (1.0 - p_dep)
    assert abs(gamma_pec - 1.0306122449) < 1e-8
    assert abs(1.15 ** 100 - 1.1743e6) < 1e3

    return {
        "zne_c12_equal_vs_opt_total_shots": [total_equal_12, total_opt_12],
        "zne_c13_equal_vs_opt_total_shots": [total_equal_13, total_opt_13],
        "zne_c123_equal_vs_opt_total_shots": [total_equal_123, total_opt_123],
        "exp_decay_biases": [round(bias_raw, 6), round(bias_lin, 6), round(bias_rich, 6)],
        "pec_gamma_p002": round(gamma_pec, 6),
    }


# =============================================================================
# 二、Bootstrap（百分位 / BCa / Cluster）vs Wilson / Clopper–Pearson
# =============================================================================

def check_bootstrap_vs_wilson() -> Dict[str, object]:
    # 1. Wald vs Wilson 精确二项覆盖率（N = 100, p = 0.05 & 0.03）
    def exact_coverage(ci_fn, n: int, p: float) -> float:
        cov = 0.0
        for k in range(n + 1):
            lo, hi = ci_fn(k, n)
            if lo - 1e-14 <= p <= hi + 1e-14:
                cov += math.comb(n, k) * (p ** k) * ((1.0 - p) ** (n - k))
        return cov

    wald_05 = exact_coverage(wald_ci, 100, 0.05)
    wald_03 = exact_coverage(wald_ci, 100, 0.03)
    wilson_05 = exact_coverage(wilson_ci, 100, 0.05)
    assert abs(wald_05 - 0.8775) < 5e-4
    assert abs(wald_03 - 0.8022) < 5e-4
    assert wilson_05 > 0.94

    # 2. 零失败反例（k = 0, N = 1000）：朴素 Bootstrap 退化为 [0, 0]
    n_zero = 1000
    data_zero = [0] * n_zero
    rng = random.Random(SEED)
    boot_zero = [sum(rng.choices(data_zero, k=n_zero)) / n_zero for _ in range(500)]
    assert min(boot_zero) == 0.0 and max(boot_zero) == 0.0
    assert wald_ci(0, n_zero) == (0.0, 0.0)
    w_zero = wilson_ci(0, n_zero)
    cp_zero_upper = -math.expm1(math.log(0.05) / n_zero)
    assert abs(w_zero[1] - 0.003827) < 2e-5
    assert abs(cp_zero_upper - 0.002991) < 2e-5

    # 3. 非线性统计量：Bell 根保真度 F = sqrt(f_Phi+) 的 95% 百分位与 BCa Bootstrap
    # 三基原始计数 (N_+, N_-): XX=(775,225), YY=(250,750), ZZ=(800,200)
    counts = [(775, 225), (250, 750), (800, 200)]

    def root_fidelity_from_counts(c_list: Sequence[Tuple[int, int]]) -> float:
        corrs = [(p - m) / (p + m) for p, m in c_list]
        f_sq = 0.25 * (1.0 + corrs[0] - corrs[1] + corrs[2])
        return math.sqrt(max(0.0, f_sq))

    f_hat = root_fidelity_from_counts(counts)
    assert abs(f_hat - math.sqrt(0.6625)) < TOL

    # 参数化/非参数等价二项重采样 B = 5000（每基有放回抽 N_i 个 +-1 等价于 Binomial(N_i, p_hat_i)）
    B = 5000
    rng_b = random.Random(SEED)
    boot_f = []
    for _ in range(B):
        sim_c = []
        for n_plus, n_minus in counts:
            n_tot = n_plus + n_minus
            p_emp = n_plus / n_tot
            k_sim = sum(1 for _ in range(n_tot) if rng_b.random() < p_emp)
            sim_c.append((k_sim, n_tot - k_sim))
        boot_f.append(root_fidelity_from_counts(sim_c))
    boot_f.sort()
    pct_lo = boot_f[int(0.025 * B)]
    pct_hi = boot_f[int(0.975 * B)]

    # 精确计算 BCa 偏移校正 z0 与留一 Jackknife 加速系数 a
    prop_less = sum(1 for x in boot_f if x < f_hat) / B
    z0 = norm_ppf(prop_less)
    # 留一法共有 3000 个样本，但仅有 6 种不同取值，精确按重数加权算 Jackknife 均与三阶矩
    jack_vals: List[Tuple[float, int]] = []
    for g_idx, (n_plus, n_minus) in enumerate(counts):
        for delta_p, delta_m, mult in [(-1, 0, n_plus), (0, -1, n_minus)]:
            c_mod = list(counts)
            c_mod[g_idx] = (n_plus + delta_p, n_minus + delta_m)
            jack_vals.append((root_fidelity_from_counts(c_mod), mult))
    n_all = sum(mult for _, mult in jack_vals)
    theta_dot = sum(val * mult for val, mult in jack_vals) / n_all
    num_a = sum(mult * ((theta_dot - val) ** 3) for val, mult in jack_vals)
    den_a = 6.0 * (sum(mult * ((theta_dot - val) ** 2) for val, mult in jack_vals) ** 1.5)
    accel = num_a / den_a

    def bca_alpha(z_a: float) -> float:
        return norm_cdf(z0 + (z0 + z_a) / (1.0 - accel * (z0 + z_a)))

    a_lo = bca_alpha(-Z_975)
    a_hi = bca_alpha(+Z_975)
    bca_lo = boot_f[max(0, min(B - 1, int(a_lo * B)))]
    bca_hi = boot_f[max(0, min(B - 1, int(a_hi * B)))]
    hoeffding_root_lo = math.sqrt(0.6625 - 0.75 * math.sqrt(2.0 * math.log(6.0 / 0.05) / 1000.0))
    # Bootstrap / BCa 区间远比无分布假设的 Hoeffding 保守下界紧凑，且稳稳高于 1/sqrt(2) ~ 0.7071
    assert hoeffding_root_lo < bca_lo < f_hat < bca_hi
    assert abs(hoeffding_root_lo - 0.7675) < 5e-4
    assert 0.790 < bca_lo < 0.805 and 0.825 < bca_hi < 0.840

    # 4. 10 批漂移序列：Pearson chi^2、Cluster SE 与 Cluster Bootstrap
    k_batches = [110, 109, 106, 111, 95, 106, 120, 133, 117, 127]
    n_per_batch = 200
    p_hat_pool = sum(k_batches) / (10 * n_per_batch)
    chi2 = sum(((k - n_per_batch * p_hat_pool) ** 2) / (n_per_batch * p_hat_pool * (1.0 - p_hat_pool)) for k in k_batches)
    naive_se = math.sqrt(p_hat_pool * (1.0 - p_hat_pool) / 2000.0)
    batch_rates = [k / n_per_batch for k in k_batches]
    cluster_se = statistics.stdev(batch_rates) / math.sqrt(len(batch_rates))
    assert abs(chi2 - 22.61) < 0.05
    assert abs(naive_se - 0.01108) < 1e-4
    assert abs(cluster_se - 0.01756) < 1e-4
    assert abs(cluster_se / naive_se - 1.585) < 0.01
    # Cluster Bootstrap：整批有放回重采样 10 批，标准差接近 cluster_se（明显高于 naive_se）
    rng_cb = random.Random(SEED + 1)
    cb_means = [sum(rng_cb.choices(batch_rates, k=10)) / 10.0 for _ in range(4000)]
    cb_se = statistics.stdev(cb_means)
    assert cb_se > 1.35 * naive_se

    return {
        "wald_exact_coverage_p005_p003": [round(wald_05, 4), round(wald_03, 4)],
        "zero_failure_boot_vs_wilson_vs_cp": {
            "bootstrap": [0.0, 0.0],
            "wilson_upper": round(w_zero[1], 6),
            "cp_onesided_upper": round(cp_zero_upper, 6),
        },
        "bell_root_fidelity": {
            "point": round(f_hat, 4),
            "hoeffding_lower": round(hoeffding_root_lo, 4),
            "percentile_95": [round(pct_lo, 4), round(pct_hi, 4)],
            "bca_95": [round(bca_lo, 4), round(bca_hi, 4)],
        },
        "drift_10batch": {
            "chi2": round(chi2, 2),
            "naive_se": round(naive_se, 5),
            "cluster_se": round(cluster_se, 5),
            "cluster_bootstrap_se": round(cb_se, 5),
        },
    }


# =============================================================================
# 三、少聚类 t_{B-1} 覆盖率验证 + Holm–Bonferroni / BH-FDR
# =============================================================================

def check_small_cluster_t_and_fdr() -> Dict[str, object]:
    t3 = student_t_ppf(0.975, df=3)
    t9 = student_t_ppf(0.975, df=9)
    assert abs(t3 - 3.182446) < 1e-4
    assert abs(t9 - 2.262157) < 1e-4

    # 蒙特卡洛覆盖率检验（固定种子，10,000 次独立重复）
    rng = random.Random(SEED + 2)
    n_trials = 10000
    cov_report = {}
    for B, t_crit in [(4, t3), (10, t9)]:
        hit_z = 0
        hit_t = 0
        for _ in range(n_trials):
            xs = [rng.gauss(0.0, 1.0) for _ in range(B)]
            mean = sum(xs) / B
            se = statistics.stdev(xs) / math.sqrt(B)
            if abs(mean) <= Z_975 * se:
                hit_z += 1
            if abs(mean) <= t_crit * se:
                hit_t += 1
        cov_z = hit_z / n_trials
        cov_t = hit_t / n_trials
        assert 0.942 <= cov_t <= 0.958, f"t 覆盖率偏离 95%: {cov_t}"
        if B == 4:
            assert cov_z < 0.875, f"B=4 时正态分位数应显著欠覆盖: {cov_z}"
        else:
            assert cov_z < 0.930, f"B=10 时正态分位数应欠覆盖: {cov_z}"
        cov_report[f"B={B}"] = {
            "t_crit": round(t_crit, 4),
            "normal_196_coverage": round(cov_z, 4),
            "student_t_coverage": round(cov_t, 4),
        }

    # Holm–Bonferroni 与 BH-FDR 五项检验表核对
    pvals = [0.008, 0.011, 0.025, 0.042, 0.210]
    m = len(pvals)
    alpha = 0.05
    bonf_rej = sum(1 for p in pvals if p <= alpha / m)
    holm_rej = 0
    for k, p in enumerate(pvals, 1):
        if p <= alpha / (m - k + 1):
            holm_rej += 1
        else:
            break
    bh_rej = 0
    for k, p in enumerate(pvals, 1):
        if p <= (k / m) * alpha:
            bh_rej = k
    assert (bonf_rej, holm_rej, bh_rej) == (1, 2, 3)

    return {
        "small_cluster_coverage": cov_report,
        "multiple_testing_rejections": {"bonferroni": bonf_rej, "holm": holm_rej, "bh_fdr": bh_rej},
    }


# =============================================================================
# 四、纯标准库 O(2^n) 张量切片引擎与线路等价性验证（QCEC 第一层证伪原型）
# =============================================================================

def check_tensor_engine_and_qcec() -> Dict[str, object]:
    def apply_1q(state: List[complex], U: List[List[complex]], q: int, n: int) -> List[complex]:
        out = [0j] * (1 << n)
        bit = 1 << (n - 1 - q)
        for idx in range(1 << n):
            if not (idx & bit):
                a0, a1 = state[idx], state[idx | bit]
                out[idx] = U[0][0] * a0 + U[0][1] * a1
                out[idx | bit] = U[1][0] * a0 + U[1][1] * a1
        return out

    def apply_2q(state: List[complex], U4: List[List[complex]], q1: int, q2: int, n: int) -> List[complex]:
        assert q1 != q2
        out = [0j] * (1 << n)
        b1, b2 = 1 << (n - 1 - q1), 1 << (n - 1 - q2)
        for idx in range(1 << n):
            if not (idx & b1) and not (idx & b2):
                i00 = idx
                i01 = idx | b2
                i10 = idx | b1
                i11 = idx | b1 | b2
                v = [state[i00], state[i01], state[i10], state[i11]]
                for r, target in enumerate((i00, i01, i10, i11)):
                    out[target] = sum(U4[r][c] * v[c] for c in range(4))
        return out

    def measure_qubit_collapse(state: List[complex], q: int, n: int, rng: random.Random) -> Tuple[int, List[complex]]:
        bit = 1 << (n - 1 - q)
        p0 = sum(abs(state[idx]) ** 2 for idx in range(1 << n) if not (idx & bit))
        p0 = min(1.0, max(0.0, p0))
        if p0 <= 0.0:
            outcome = 1
        elif p0 >= 1.0:
            outcome = 0
        else:
            outcome = 0 if rng.random() < p0 else 1
        post = [
            state[idx] if (((idx & bit) != 0) == (outcome == 1)) else 0j
            for idx in range(1 << n)
        ]
        norm = math.sqrt(sum(abs(z) ** 2 for z in post))
        assert norm > 1e-12
        return outcome, [z / norm for z in post]

    H = [[1 / math.sqrt(2) + 0j, 1 / math.sqrt(2) + 0j], [1 / math.sqrt(2) + 0j, -1 / math.sqrt(2) + 0j]]
    Z = [[1 + 0j, 0j], [0j, -1 + 0j]]
    X = [[0j, 1 + 0j], [1 + 0j, 0j]]
    CNOT = [
        [1 + 0j, 0j, 0j, 0j],
        [0j, 1 + 0j, 0j, 0j],
        [0j, 0j, 0j, 1 + 0j],
        [0j, 0j, 1 + 0j, 0j],
    ]
    SWAP = [
        [1 + 0j, 0j, 0j, 0j],
        [0j, 0j, 1 + 0j, 0j],
        [0j, 1 + 0j, 0j, 0j],
        [0j, 0j, 0j, 1 + 0j],
    ]

    # 1. 基础回归：HZH|0> = |1>，Bell 态坍缩保护
    st1 = apply_1q(apply_1q(apply_1q([1 + 0j, 0j], H, 0, 1), Z, 0, 1), H, 0, 1)
    assert abs(st1[1] - 1.0) < TOL
    out_bit, post_st = measure_qubit_collapse(st1, 0, 1, random.Random(SEED))
    assert out_bit == 1 and abs(post_st[1] - 1.0) < TOL

    # 2. QCEC 第一层：随机乘积态证伪（3 比特线性链 0-1-2 路由 CNOT(0 -> 2)）
    # 原线路 C：直接执行 CNOT(0 -> 2)
    def run_orig(st: List[complex]) -> List[complex]:
        return apply_2q(st, CNOT, 0, 2, 3)

    # 合法编译线路 C'：仅用最近邻门 SWAP(0, 1) -> CNOT(1 -> 2)，并附全局相位 e^{i*0.3}，
    # 最终逻辑->物理布局为 (q0->1, q1->0, q2->2)
    def run_compiled_valid(st: List[complex]) -> List[complex]:
        s = apply_2q(st, SWAP, 0, 1, 3)
        s = apply_2q(s, CNOT, 1, 2, 3)
        phase = cmath.exp(0.3j)
        return [z * phase for z in s]

    # 错误编译线路 C_bad：路由后漏记 SWAP 引起的逻辑置换（错当成恒等布局），或把 CNOT 方向写反
    def run_compiled_buggy(st: List[complex]) -> List[complex]:
        s = apply_2q(st, SWAP, 0, 1, 3)
        s = apply_2q(s, CNOT, 2, 1, 3)  # 错误：控制/目标写反
        return s

    def permute_to_logical(st: List[complex], log_to_phys: Tuple[int, int, int]) -> List[complex]:
        out = [0j] * 8
        for log_idx in range(8):
            lbits = [(log_idx >> (2 - k)) & 1 for k in range(3)]
            pbits = [0, 0, 0]
            for lq, pq in enumerate(log_to_phys):
                pbits[pq] = lbits[lq]
            phys_idx = (pbits[0] << 2) | (pbits[1] << 1) | pbits[2]
            out[log_idx] = st[phys_idx]
        return out

    rng_q = random.Random(SEED + 3)
    max_valid_infid = 0.0
    buggy_detected_count = 0
    n_probes = 16
    for _ in range(n_probes):
        # 构造随机 3 比特乘积纯态
        singles = []
        for _ in range(3):
            th = math.acos(1.0 - 2.0 * rng_q.random())
            ph = 2.0 * math.pi * rng_q.random()
            singles.append([math.cos(th / 2.0) + 0j, cmath.exp(1j * ph) * math.sin(th / 2.0)])
        psi_in = [
            singles[0][(i >> 2) & 1] * singles[1][(i >> 1) & 1] * singles[2][i & 1]
            for i in range(8)
        ]
        out_ref = run_orig(psi_in)
        out_val = permute_to_logical(run_compiled_valid(psi_in), (1, 0, 2))
        ov_val = abs(sum(a.conjugate() * b for a, b in zip(out_ref, out_val)))
        max_valid_infid = max(max_valid_infid, abs(1.0 - ov_val))

        out_bug = permute_to_logical(run_compiled_buggy(psi_in), (1, 0, 2))
        ov_bug = abs(sum(a.conjugate() * b for a, b in zip(out_ref, out_bug)))
        if abs(1.0 - ov_bug) > 1e-6:
            buggy_detected_count += 1

    assert max_valid_infid < TOL
    assert buggy_detected_count == n_probes  # 全部 16 条随机探针 100% 瞬间抓出编译 Bug

    return {
        "qcec_random_probes": n_probes,
        "valid_routed_max_infidelity": max_valid_infid,
        "buggy_circuit_detected_probes": buggy_detected_count,
    }


def main() -> None:
    report = {
        "zne_and_pec": check_zne_and_pec(),
        "bootstrap_vs_wilson": check_bootstrap_vs_wilson(),
        "small_cluster_t_and_fdr": check_small_cluster_t_and_fdr(),
        "tensor_engine_and_qcec": check_tensor_engine_and_qcec(),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
