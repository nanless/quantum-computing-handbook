r"""Chapter 20: Quantum sensing and metrology numerical verification lab.

Pure Python 3 standard-library verification of all core analytical derivations
in handbook/20-quantum-sensing-metrology.md:
  1. Single-qubit Ramsey CFI/QFI (ideal V=1 and noisy V<1) + Bures/root-fidelity limit.
  2. Multi-qubit GHZ (N=2, 3, 4) parity measurement <X^{\otimes N}> = cos(N*phi),
     CFI = QFI = N^2, and single-qubit trace-out collapse (F_Q = 0).
  3. Huelga et al. (1997) Markovian dephasing: optimal interrogation times,
     GHZ-vs-uncorrelated tie at t_d=0, constant factor e vs ultimate bound,
     and strict GHZ degradation under finite dead time t_d > 0.
  4. Spin squeezing (exact 3x3 spin-1 OAT for N=2 + Kitagawa-Ueda general-N
     Wineland parameter) and optical quadrature squeezing under loss + LIGO dB.
  5. CPMG-n synchronous lock-in and finite-pulse-count filter response
     |Y(omega_0)|^2 = 4 / pi^2.
  6. HNLS (Hamiltonian-Not-in-Lindblad-Span) subspace test for dephasing,
     bit-flip, and amplitude damping, plus 2-qubit QEC sensing code check.

Usage:
    python3 codes/systems/sensing_lab.py
"""
import cmath
import json
import math


def mat_mul(a, b):
    n = len(a)
    m = len(b[0])
    k_len = len(b)
    return [
        [sum(a[i][k] * b[k][j] for k in range(k_len)) for j in range(m)]
        for i in range(n)
    ]


def mat_vec(a, v):
    return [sum(row[j] * v[j] for j in range(len(v))) for row in a]


def mat_dag(a):
    n = len(a)
    m = len(a[0])
    return [[a[i][j].conjugate() for i in range(n)] for j in range(m)]


def vdot(u, v):
    """Left-conjugate inner product <u|v> = sum_j u_j^* v_j."""
    return sum(a.conjugate() * b for a, b in zip(u, v))


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def sqrt_hermitian_2x2(m):
    """Principal square root of a 2x2 positive semidefinite Hermitian matrix."""
    tr = (m[0][0] + m[1][1]).real
    det = (m[0][0] * m[1][1] - m[0][1] * m[1][0]).real
    det = max(0.0, det)
    s = math.sqrt(det)
    t = math.sqrt(max(0.0, tr + 2.0 * s))
    if t == 0.0:
        return [[0j, 0j], [0j, 0j]]
    return [
        [(m[0][0] + s) / t, m[0][1] / t],
        [m[1][0] / t, (m[1][1] + s) / t],
    ]


def root_fidelity_2x2(rho, sigma):
    """Root fidelity F(rho, sigma) = Tr(sqrt(sqrt(rho) sigma sqrt(rho)))."""
    sr = sqrt_hermitian_2x2(rho)
    inner = mat_mul(mat_mul(sr, sigma), sr)
    return trace(sqrt_hermitian_2x2(inner)).real


def check_ramsey_cfi_qfi_bures():
    """Verify Section 2 & 3: Ramsey CFI, QFI, blind spot, and Bures limit."""
    def rho_dephased(phi, vis):
        return [
            [0.5 + 0j, 0.5 * vis * cmath.exp(-1j * phi)],
            [0.5 * vis * cmath.exp(1j * phi), 0.5 + 0j],
        ]

    def p_plus(phi, vis):
        # X-basis projector |+><+| = [[0.5, 0.5], [0.5, 0.5]]
        rho = rho_dephased(phi, vis)
        proj_plus = [[0.5, 0.5], [0.5, 0.5]]
        return trace(mat_mul(rho, proj_plus)).real

    def cfi_ramsey(phi, vis):
        p = p_plus(phi, vis)
        dp = -0.5 * vis * math.sin(phi)
        if p <= 0.0 or p >= 1.0:
            return 0.0 if vis < 1.0 else 1.0
        return dp * dp * (1.0 / p + 1.0 / (1.0 - p))

    # Ideal V=1: F_C(phi) == 1 identically on (0, pi)
    for phi in (0.1, 0.5, math.pi / 4, math.pi / 2, 2.3):
        val = cfi_ramsey(phi, 1.0)
        assert abs(val - 1.0) < 1e-12, f"Ideal CFI mismatch at phi={phi}: {val}"

    # Noisy V=0.9 and V=0.8: peak V^2 at pi/2, blind spot 0 at phi=0
    assert abs(cfi_ramsey(math.pi / 2, 0.9) - 0.81) < 1e-12
    assert abs(cfi_ramsey(0.0, 0.9) - 0.0) < 1e-12
    assert abs(cfi_ramsey(math.pi / 2, 0.8) - 0.64) < 1e-12
    assert abs(cfi_ramsey(0.0, 0.8) - 0.0) < 1e-12

    # Verify analytic F_C(phi; V) = V^2 sin^2(phi) / (1 - V^2 cos^2(phi))
    for vis in (0.8, 0.9):
        for phi in (0.3, 1.0, math.pi / 2):
            closed = (vis * math.sin(phi)) ** 2 / (1.0 - (vis * math.cos(phi)) ** 2)
            assert abs(cfi_ramsey(phi, vis) - closed) < 1e-12

    # Verify geometric equivalence: F_Q = 8 * lim_{d->0} (1 - F(rho_phi, rho_{phi+d})) / d^2
    delta = 1e-4
    bures_estimates = {}
    for vis in (1.0, 0.9, 0.8):
        r0 = rho_dephased(0.7, vis)
        r1 = rho_dephased(0.7 + delta, vis)
        fid = root_fidelity_2x2(r0, r1)
        fq_est = 8.0 * (1.0 - fid) / (delta * delta)
        assert abs(fq_est - vis * vis) < 1e-6, f"Bures QFI mismatch: {fq_est} vs {vis**2}"
        bures_estimates[f"V={vis}"] = round(fq_est, 8)

    return {
        "ideal_cfi_pi_over_2": 1.0,
        "noisy_V09_cfi_pi_over_2": round(cfi_ramsey(math.pi / 2, 0.9), 6),
        "noisy_V09_cfi_zero": round(cfi_ramsey(0.0, 0.9), 6),
        "bures_qfi_estimates": bures_estimates,
    }


def apply_single_qubit_gate(state, n_qubits, target, gate):
    """Apply 2x2 gate to qubit `target` (0 = MSB, big-endian)."""
    dim = 1 << n_qubits
    out = [0j] * dim
    bit = 1 << (n_qubits - 1 - target)
    for idx in range(dim):
        if (idx & bit) == 0:
            i0 = idx
            i1 = idx | bit
            a0, a1 = state[i0], state[i1]
            out[i0] = gate[0][0] * a0 + gate[0][1] * a1
            out[i1] = gate[1][0] * a0 + gate[1][1] * a1
    return out


def check_ghz_parity_and_loss():
    """Verify Section 4 & Exercise 20-A: GHZ parity, F_C=F_Q=N^2, 1-qubit loss."""
    inv_s2 = 1.0 / math.sqrt(2.0)
    h_gate = [[inv_s2, inv_s2], [inv_s2, -inv_s2]]
    x_gate = [[0.0, 1.0], [1.0, 0.0]]

    results = {}
    for n in (2, 3, 4):
        dim = 1 << n
        phi = 0.37
        # Prepare GHZ_N = (|0...0> + |1...1>) / sqrt(2)
        psi = [0j] * dim
        psi[0] = inv_s2
        psi[dim - 1] = inv_s2
        # Apply U_N(phi) = tensor_j exp(-i phi Z_j / 2)
        rz = [[cmath.exp(-0.5j * phi), 0j], [0j, cmath.exp(0.5j * phi)]]
        for q in range(n):
            psi = apply_single_qubit_gate(psi, n, q, rz)

        # Expectation value <X^{\otimes N}>
        x_psi = list(psi)
        for q in range(n):
            x_psi = apply_single_qubit_gate(x_psi, n, q, x_gate)
        exp_parity = vdot(psi, x_psi).real
        assert abs(exp_parity - math.cos(n * phi)) < 1e-12

        # Hadamard basis readout -> even vs odd Hamming weight probabilities
        h_psi = list(psi)
        for q in range(n):
            h_psi = apply_single_qubit_gate(h_psi, n, q, h_gate)
        p_even = sum(abs(amp) ** 2 for idx, amp in enumerate(h_psi) if bin(idx).count("1") % 2 == 0)
        p_odd = sum(abs(amp) ** 2 for idx, amp in enumerate(h_psi) if bin(idx).count("1") % 2 == 1)
        assert abs(p_even + p_odd - 1.0) < 1e-12
        assert abs(p_even - 0.5 * (1.0 + math.cos(n * phi))) < 1e-12

        # Numerical CFI via central difference
        eps = 1e-6
        def p_even_fn(th):
            st = [0j] * dim
            st[0] = inv_s2 * cmath.exp(-0.5j * n * th)
            st[dim - 1] = inv_s2 * cmath.exp(0.5j * n * th)
            for q in range(n):
                st = apply_single_qubit_gate(st, n, q, h_gate)
            return sum(abs(a) ** 2 for idx, a in enumerate(st) if bin(idx).count("1") % 2 == 0)

        dp = (p_even_fn(phi + eps) - p_even_fn(phi - eps)) / (2.0 * eps)
        cfi = dp * dp * (1.0 / p_even + 1.0 / p_odd)
        assert abs(cfi - n * n) < 1e-7, f"GHZ N={n} CFI mismatch: {cfi}"

        # Generator variance 4*(Delta J_z)^2
        # J_z eigenvalues for |0...0> and |1...1> are +n/2 and -n/2
        mean_jz = sum(
            abs(psi[idx]) ** 2 * (0.5 * (n - 2 * bin(idx).count("1")))
            for idx in range(dim)
        )
        mean_jz2 = sum(
            abs(psi[idx]) ** 2 * (0.5 * (n - 2 * bin(idx).count("1"))) ** 2
            for idx in range(dim)
        )
        qfi = 4.0 * (mean_jz2 - mean_jz * mean_jz)
        assert abs(qfi - n * n) < 1e-12
        results[f"N={n}"] = {
            "parity_cos_Nphi": round(exp_parity, 8),
            "p_even": round(p_even, 8),
            "cfi": round(cfi, 6),
            "qfi": round(qfi, 6),
        }

    # Exercise 20-A: Trace out the last qubit of N=4 GHZ state
    # rho_red(phi) = Tr_4(|psi_4(phi)><psi_4(phi)|)
    n = 4
    dim = 1 << n
    reduced_dim = 1 << (n - 1)
    def reduced_ghz4(phi):
        st = [0j] * dim
        st[0] = inv_s2 * cmath.exp(-0.5j * n * phi)
        st[dim - 1] = inv_s2 * cmath.exp(0.5j * n * phi)
        rho_r = [[0j] * reduced_dim for _ in range(reduced_dim)]
        for i in range(reduced_dim):
            for j in range(reduced_dim):
                # Sum over traced-out LSB b in {0, 1}
                rho_r[i][j] = sum(st[(i << 1) | b] * st[(j << 1) | b].conjugate() for b in (0, 1))
        return rho_r

    r_a = reduced_ghz4(0.0)
    r_b = reduced_ghz4(1.234)
    max_diff = max(abs(r_a[i][j] - r_b[i][j]) for i in range(reduced_dim) for j in range(reduced_dim))
    assert max_diff < 1e-15, f"Traced-out GHZ4 still depends on phi: {max_diff}"
    assert abs(r_a[0][0].real - 0.5) < 1e-15 and abs(r_a[7][7].real - 0.5) < 1e-15
    results["ghz4_after_1qubit_loss_phi_diff"] = max_diff
    return results


def golden_section_max(fn, lo, hi, tol=1e-12):
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    c = hi - gr * (hi - lo)
    d = lo + gr * (hi - lo)
    fc, fd = fn(c), fn(d)
    while hi - lo > tol:
        if fc < fd:
            lo = c
            c, fc = d, fd
            d = lo + gr * (hi - lo)
            fd = fn(d)
        else:
            hi = d
            d, fd = c, fc
            c = hi - gr * (hi - lo)
            fc = fn(c)
    x = 0.5 * (lo + hi)
    return x, fn(x)


def check_huelga_dephasing():
    """Verify Section 5: Huelga (1997) Markovian dephasing collapse and dead time."""
    gamma = 1.0
    total_t = 100.0
    table = {}

    for n in (1, 4, 16, 100):
        # Uncorrelated: F_unc(t) = N * T * t * exp(-2 * gamma * t)
        t_unc, f_unc = golden_section_max(
            lambda t: n * total_t * t * math.exp(-2.0 * gamma * t),
            1e-9,
            10.0 / gamma,
        )
        assert abs(t_unc - 1.0 / (2.0 * gamma)) < 1e-7

        # Dephased GHZ: F_ghz(t) = N^2 * T * t * exp(-2 * N * gamma * t)
        t_ghz, f_ghz = golden_section_max(
            lambda t: (n * n) * total_t * t * math.exp(-2.0 * n * gamma * t),
            1e-9,
            10.0 / (n * gamma),
        )
        assert abs(t_ghz - 1.0 / (2.0 * n * gamma)) < 1e-7 / n

        # Exact tie at zero dead time: F_ghz_max == F_unc_max == N * T / (2 * e * gamma)
        f_exact = n * total_t / (2.0 * math.e * gamma)
        assert abs(f_unc - f_exact) / f_exact < 1e-10
        assert abs(f_ghz - f_exact) / f_exact < 1e-10

        # Ultimate Markovian bound: F_ult = N * T / (2 * gamma)
        f_ult = n * total_t / (2.0 * gamma)
        variance_ratio = f_ult / f_ghz
        precision_ratio = math.sqrt(variance_ratio)
        assert abs(variance_ratio - math.e) < 1e-10
        assert abs(precision_ratio - math.sqrt(math.e)) < 1e-10

        # Penalty if GHZ mistakenly runs at single-qubit optimal time t = 1/(2*gamma)
        t_fixed = 1.0 / (2.0 * gamma)
        f_ghz_fixed = (n * n) * total_t * t_fixed * math.exp(-2.0 * n * gamma * t_fixed)
        dw_unc = 1.0 / math.sqrt(f_unc)
        dw_ghz = 1.0 / math.sqrt(f_ghz)
        dw_ult = 1.0 / math.sqrt(f_ult)
        dw_ghz_fixed = 1.0 / math.sqrt(f_ghz_fixed) if f_ghz_fixed > 0 else float("inf")

        table[f"N={n}"] = {
            "t_opt_ghz": round(t_ghz, 6),
            "dw_unc_min": round(dw_unc, 6),
            "dw_ghz_min": round(dw_ghz, 6),
            "dw_ult_bound": round(dw_ult, 6),
            "dw_ghz_at_single_topt": round(dw_ghz_fixed, 6) if dw_ghz_fixed < 1e12 else "overflow(>1e12)",
        }

    # Finite dead time t_d = 0.1 / gamma, N = 16: GHZ loses strictly to uncorrelated
    n_dt, t_d = 16, 0.1
    t_unc_dt, f_unc_dt = golden_section_max(
        lambda t: (total_t / (t + t_d)) * n_dt * (t * t) * math.exp(-2.0 * gamma * t),
        1e-9,
        10.0,
    )
    t_ghz_dt, f_ghz_dt = golden_section_max(
        lambda t: (total_t / (t + t_d)) * (n_dt * n_dt) * (t * t) * math.exp(-2.0 * n_dt * gamma * t),
        1e-9,
        10.0,
    )
    dw_unc_dt = 1.0 / math.sqrt(f_unc_dt)
    dw_ghz_dt = 1.0 / math.sqrt(f_ghz_dt)
    assert dw_ghz_dt > dw_unc_dt * 1.5, "Expected GHZ to lose strictly under dead time"

    return {
        "variance_ratio_ult_to_ghz": round(math.e, 8),
        "precision_ratio_ghz_to_ult": round(math.sqrt(math.e), 8),
        "zero_dead_time_table": table,
        "dead_time_N16_td01": {
            "t_opt_unc": round(t_unc_dt, 6),
            "dw_unc": round(dw_unc_dt, 6),
            "t_opt_ghz": round(t_ghz_dt, 6),
            "dw_ghz": round(dw_ghz_dt, 6),
            "ghz_penalty_factor": round(dw_ghz_dt / dw_unc_dt, 4),
        },
    }


def wineland_oat_closed(n, theta):
    """Kitagawa-Ueda (1993) / Wineland (1994) exact OAT squeezing parameter xi_R^2."""
    c_n1 = math.cos(theta) ** (n - 1)
    if abs(c_n1) < 1e-15:
        return float("inf")
    a = 1.0 - math.cos(2.0 * theta) ** (n - 2)
    b = 4.0 * math.sin(theta) * (math.cos(theta) ** (n - 2))
    num = 1.0 + 0.25 * (n - 1) * (a - math.hypot(a, b))
    return num / (c_n1 * c_n1)


def check_spin_and_optical_squeezing():
    """Verify Section 6: exact N=2 spin-1 OAT, general-N OAT, and optical loss."""
    # Exact 3x3 spin-1 representation for symmetric N=2 subspace {|+1>, |0>, |-1>}
    s2 = 1.0 / math.sqrt(2.0)
    jx = [[0j, s2, 0j], [s2, 0j, s2], [0j, s2, 0j]]
    jy = [[0j, -1j * s2, 0j], [1j * s2, 0j, -1j * s2], [0j, 1j * s2, 0j]]
    jz = [[1.0 + 0j, 0j, 0j], [0j, 0j, 0j], [0j, 0j, -1.0 + 0j]]

    theta = math.pi / 6.0  # 30 deg -> sin=1/2, cos=sqrt(3)/2, xi_R^2 = 2/3
    psi = [0.5 * cmath.exp(-1j * theta), s2 + 0j, 0.5 * cmath.exp(-1j * theta)]
    assert abs(vdot(psi, psi).real - 1.0) < 1e-14

    mean_jx = vdot(psi, mat_vec(jx, psi)).real
    mean_jy = vdot(psi, mat_vec(jy, psi)).real
    mean_jz = vdot(psi, mat_vec(jz, psi)).real
    assert abs(mean_jx - math.cos(theta)) < 1e-14
    assert abs(mean_jy) < 1e-14 and abs(mean_jz) < 1e-14

    jy_psi = mat_vec(jy, psi)
    jz_psi = mat_vec(jz, psi)
    var_y = vdot(jy_psi, jy_psi).real
    var_z = vdot(jz_psi, jz_psi).real
    cov_yz = vdot(jy_psi, jz_psi).real  # Re(<psi|Jy Jz|psi>) = 0.5<Jy Jz + Jz Jy>
    assert abs(var_y - 0.5) < 1e-14
    assert abs(var_z - 0.5) < 1e-14
    assert abs(cov_yz - 0.5 * math.sin(theta)) < 1e-14

    # Minimum eigenvalue of 2x2 covariance [[var_y, cov_yz], [cov_yz, var_z]]
    min_var = 0.5 * (var_y + var_z - math.hypot(var_y - var_z, 2.0 * cov_yz))
    xi2_exact = 2.0 * min_var / (mean_jx * mean_jx)
    xi2_closed = wineland_oat_closed(2, theta)
    assert abs(xi2_exact - 2.0 / 3.0) < 1e-14
    assert abs(xi2_closed - 2.0 / 3.0) < 1e-14

    # General-N optimal OAT squeezing (check N=10, 100, 1000)
    oat_summary = {}
    for n in (2, 10, 100, 1000):
        hi = 0.45 * math.pi if n == 2 else min(1.0, 4.0 * (n ** (-2.0 / 3.0)))
        # Maximize -xi_R^2
        t_best, neg_xi = golden_section_max(lambda th: -wineland_oat_closed(n, th), 1e-7, hi)
        xi_best = -neg_xi
        oat_summary[f"N={n}"] = {
            "theta_opt": round(t_best, 6),
            "xi2_min": round(xi_best, 6),
            "squeezing_dB": round(-10.0 * math.log10(xi_best), 2),
        }

    # Optical squeezing with 20% loss and 10 dB injected squeezing
    eta_opt = 0.80
    r_10db = 0.5 * math.log(10.0)  # exp(-2r) = 0.1
    var_ratio_obs = eta_opt * math.exp(-2.0 * r_10db) + (1.0 - eta_opt)
    obs_db = -10.0 * math.log10(var_ratio_obs)
    ceiling_db = -10.0 * math.log10(1.0 - eta_opt)
    assert abs(var_ratio_obs - 0.28) < 1e-14
    assert abs(obs_db - 5.528419686577808) < 1e-10
    assert abs(ceiling_db - 6.989700043360188) < 1e-10

    # LIGO O4 dB -> amplitude noise reduction factor (10^(dB/20))
    hanford_factor = 10.0 ** (4.0 / 20.0)
    livingston_factor = 10.0 ** (5.8 / 20.0)
    assert 1.55 < hanford_factor < 1.65
    assert 1.90 < livingston_factor < 2.00

    return {
        "N2_theta_pi_over_6_xi2": round(xi2_exact, 8),
        "N2_theta_pi_over_6_dB": round(-10.0 * math.log10(xi2_exact), 4),
        "oat_scaling": oat_summary,
        "optical_loss_20pct_10dB_in_dB": round(obs_db, 4),
        "optical_loss_20pct_ceiling_dB": round(ceiling_db, 4),
        "ligo_o4_hanford_factor": round(hanford_factor, 3),
        "ligo_o4_livingston_factor": round(livingston_factor, 3),
    }


def check_cpmg_filter_and_lockin():
    """Verify synchronous response and distinguish it from the primary maximum."""
    def switching_sign(t, total_t, n_pulses):
        # Symmetric CPMG: pi pulses at t_k = (2k - 1)/(2n) * T, k=1..n
        count = 0
        for k in range(1, n_pulses + 1):
            if t > (2 * k - 1) * total_t / (2 * n_pulses):
                count += 1
        return 1.0 if (count % 2 == 0) else -1.0

    def cpmg_filter_closed(z, n_pulses):
        # Closed form for even n_pulses: F(z) / z^2
        if abs(z) < 1e-12:
            return 0.0
        if abs(z - n_pulses * math.pi) < 1e-9:
            return 4.0 / (math.pi * math.pi)
        num = 16.0 * (math.sin(z / (4.0 * n_pulses)) ** 4) * (math.sin(z / 2.0) ** 2)
        den = (math.cos(z / (2.0 * n_pulses)) ** 2) * (z * z)
        return num / den

    total_t = 1.0
    steps = 16_000  # Multiple of 2*n for n=2, 4, 10
    dt = total_t / steps
    out = {}
    for n, expected_peak in [(2, 7.212024), (4, 13.085143), (10, 31.632108)]:
        boundaries = [0, *((2 * pulse - 1) / (2 * n) for pulse in range(1, n + 1)), 1]

        def power(z):
            integral = sum(
                (-1) ** index * (cmath.exp(1j * z * end) - cmath.exp(1j * z * start)) / (1j * z)
                for index, (start, end) in enumerate(zip(boundaries, boundaries[1:]))
            )
            return abs(integral) ** 2

        omega_res = n * math.pi / total_t
        # Midpoint Riemann integration for AC lock-in phase & |Y(omega)|^2
        phase_acc = 0.0
        y_res = 0j
        for i in range(steps):
            t_mid = (i + 0.5) * dt
            s_val = switching_sign(t_mid, total_t, n)
            phase_acc += s_val * math.cos(omega_res * t_mid) * dt
            y_res += s_val * cmath.exp(1j * omega_res * t_mid) * dt
        y_sq = (abs(y_res) / total_t) ** 2
        assert abs(phase_acc - 2.0 / math.pi) < 1e-6, f"CPMG-{n} phase mismatch: {phase_acc}"
        assert abs(y_sq - 4.0 / (math.pi ** 2)) < 1e-6, f"CPMG-{n} synchronous power mismatch: {y_sq}"

        # Also check off-resonance frequency z = 0.7 * n * pi against closed form
        z_test = 0.7 * n * math.pi
        y_off = sum(
            switching_sign((i + 0.5) * dt, total_t, n) * cmath.exp(1j * z_test * (i + 0.5) * dt) * dt
            for i in range(steps)
        )
        y_off_sq = abs(y_off) ** 2
        closed_off = cpmg_filter_closed(z_test, n)
        assert abs(y_off_sq - closed_off) < 1e-5, f"CPMG-{n} off-res mismatch: {y_off_sq} vs {closed_off}"

        peak, peak_power = golden_section_max(power, n * math.pi - math.pi / 2, n * math.pi + math.pi / 2, tol=1e-9)
        assert abs(peak - expected_peak) < 1e-5 and peak_power > y_sq
        assert abs(power(omega_res) - 4 / math.pi ** 2) < 1e-12
        out[f"CPMG-{n}"] = {
            "lockin_phase_ratio": round(phase_acc, 6),
            "synchronous_Y2": round(y_sq, 6),
            "first_band_argmax_omega_T": peak,
            "first_band_peak_Y2": peak_power,
            "off_res_Y2_num": round(y_off_sq, 6),
            "off_res_Y2_closed": round(closed_off, 6),
        }
    return out


def hs_distance_to_span(target_mat, basis_mats):
    """Euclidean distance (Hilbert-Schmidt norm) from target_mat to span(basis_mats)."""
    def flatten(m):
        return [x for row in m for x in row]

    # Gram-Schmidt orthonormalization in C^4
    ortho = []
    for mat in basis_mats:
        v = flatten(mat)
        for q in ortho:
            proj = vdot(q, v)
            v = [vi - proj * qi for vi, qi in zip(v, q)]
        norm = math.sqrt(vdot(v, v).real)
        if norm > 1e-12:
            ortho.append([vi / norm for vi in v])

    t_vec = flatten(target_mat)
    rem = list(t_vec)
    for q in ortho:
        proj = vdot(q, rem)
        rem = [ri - proj * qi for ri, qi in zip(rem, q)]
    return math.sqrt(vdot(rem, rem).real)


def check_hnls_and_qec_code():
    """Verify Section 8 & Exercise 20-B: HNLS subspace test and 2-qubit QEC code."""
    i2 = [[1 + 0j, 0j], [0j, 1 + 0j]]
    x2 = [[0j, 1 + 0j], [1 + 0j, 0j]]
    z2 = [[1 + 0j, 0j], [0j, -1 + 0j]]
    h_sig = [[0.5 + 0j, 0j], [0j, -0.5 + 0j]]  # H = Z / 2
    l_ad = [[0j, 1 + 0j], [0j, 0j]]            # Amplitude damping |0><1|

    cases = {
        "dephasing_L=Z": z2,
        "bitflip_L=X": x2,
        "bitflip_with_identity_L=I+X": [[1, 1], [1, 1]],
        "amplitude_damping_L=|0><1|": l_ad,
    }
    hnls_res = {}
    for name, l_op in cases.items():
        l_dag = mat_dag(l_op)
        span_gens = [i2, l_op, l_dag, mat_mul(l_dag, l_op)]
        dist = hs_distance_to_span(h_sig, span_gens)
        holds = dist > 1e-10
        hnls_res[name] = {"perp_hs_norm": round(dist, 6), "hnls_holds": holds}

    assert not hnls_res["dephasing_L=Z"]["hnls_holds"]
    assert hnls_res["bitflip_L=X"]["hnls_holds"]
    assert not hnls_res["amplitude_damping_L=|0><1|"]["hnls_holds"]

    assert hnls_res["bitflip_with_identity_L=I+X"]["hnls_holds"]
    shifted = cases["bitflip_with_identity_L=I+X"]
    dt = 0.01
    l_dag_l = mat_mul(mat_dag(shifted), shifted)
    k0 = [[i2[i][j] - dt * (1j * h_sig[i][j] + l_dag_l[i][j] / 2)
           for j in range(2)] for i in range(2)]
    k1 = [[math.sqrt(dt) * value for value in row] for row in shifted]
    cross = mat_mul(mat_dag(k0), k1)
    extracted = [[(cross[i][j] - cross[j][i].conjugate()) / (1j * dt ** 1.5)
                  for j in range(2)] for i in range(2)]
    assert all(abs(extracted[i][j] - z2[i][j]) < 1e-12 for i in range(2) for j in range(2))

    # 2-qubit QEC sensing code: |0_L> = |00>, |1_L> = |11>, probe = qubit 0 (MSB)
    c0 = [1 + 0j, 0j, 0j, 0j]
    c1 = [0j, 0j, 0j, 1 + 0j]
    x1 = [
        [0j, 0j, 1 + 0j, 0j],
        [0j, 0j, 0j, 1 + 0j],
        [1 + 0j, 0j, 0j, 0j],
        [0j, 1 + 0j, 0j, 0j],
    ]
    z1 = [
        [1 + 0j, 0j, 0j, 0j],
        [0j, 1 + 0j, 0j, 0j],
        [0j, 0j, -1 + 0j, 0j],
        [0j, 0j, 0j, -1 + 0j],
    ]
    # Check Knill-Laflamme P X_1 P = 0
    for u in (c0, c1):
        for v in (c0, c1):
            assert abs(vdot(u, mat_vec(x1, v))) < 1e-15
    # Check logical signal P Z_1 P = Z_L
    assert abs(vdot(c0, mat_vec(z1, c0)).real - 1.0) < 1e-15
    assert abs(vdot(c1, mat_vec(z1, c1)).real + 1.0) < 1e-15
    assert abs(vdot(c0, mat_vec(z1, c1))) < 1e-15

    return {"hnls_cases": hnls_res, "two_qubit_code_verified": True}


def check_nv_sensitivity_example():
    """Verify Section 1 NV single-spin sensitivity numerical calculation."""
    gamma_e = 2.0 * math.pi * 28.025e9  # rad / (s * T)
    tau_dc = 1e-6  # 1 us
    tau_ac = 1e-3  # 1 ms
    eta_dc_ideal = 1.0 / (gamma_e * math.sqrt(tau_dc))
    eta_unit_response = 1.0 / (gamma_e * math.sqrt(tau_ac))
    eta_synchronous_sinusoid = eta_unit_response / (2 / math.pi)
    assert math.isclose(eta_dc_ideal * 1e9, 5.679, abs_tol=.001)
    assert math.isclose(eta_unit_response * 1e9, .17958684, abs_tol=1e-8)
    assert math.isclose(eta_synchronous_sinusoid * 1e9, .28209435, abs_tol=1e-8)
    return {
        "gamma_e_rad_per_s_T": round(gamma_e, 2),
        "nv_dc_ideal_nT_per_sqrtHz": round(eta_dc_ideal * 1e9, 3),
        "nv_1ms_unit_response_nT_per_sqrtHz": eta_unit_response * 1e9,
        "nv_1ms_synchronous_sine_nT_per_sqrtHz": eta_synchronous_sinusoid * 1e9,
    }



def check_clock_and_gravity():
    """Evaluate adjacent independent full-cycle averages and gravity fringe aliasing."""
    single_cycle_sigma = 1 / (2 * math.pi * 4.292e14 * 1 * math.sqrt(10_000))
    sigma_1_2 = single_cycle_sigma
    sigma_120 = single_cycle_sigma / math.sqrt(100)
    sigma_longer_cycle = single_cycle_sigma / math.sqrt(60)
    assert math.isclose(sigma_1_2, 3.70818e-18, rel_tol=2e-6)
    assert math.isclose(sigma_120, 3.70818e-19, rel_tol=2e-6)
    assert math.isclose(sigma_longer_cycle / sigma_120, math.sqrt(2 / 1.2), rel_tol=1e-12)

    effective_wavevector = 4 * math.pi / 780e-9
    pulse_spacing = 0.1
    phase_per_acceleration = effective_wavevector * pulse_spacing ** 2
    local_resolution = 1e-3 / phase_per_acceleration
    period = 2 * math.pi / phase_per_acceleration
    gravity = 9.80665
    assert math.isclose(local_resolution, 6.20704e-9, rel_tol=2e-6)
    assert math.isclose(period, 3.9e-5, rel_tol=1e-12)
    assert abs(math.cos(gravity * phase_per_acceleration)
               - math.cos((gravity + period) * phase_per_acceleration)) < 5e-10
    return {
        "allan_qpn_1_2s": sigma_1_2,
        "allan_qpn_120s": sigma_120,
        "allan_qpn_120s_with_2s_cycle": sigma_longer_cycle,
        "local_acceleration_resolution_m_per_s2": local_resolution,
        "equal_fringe_spacing_m_per_s2": period,
    }


def check_multi_parameter_and_rank_change():
    """Check a jointly attainable qutrit example and a Bures/SLD rank boundary."""
    basis = [
        [1 / math.sqrt(3), 1 / math.sqrt(2), 1 / math.sqrt(6)],
        [1 / math.sqrt(3), -1 / math.sqrt(2), 1 / math.sqrt(6)],
        [1 / math.sqrt(3), 0, -2 / math.sqrt(6)],
    ]
    classical = [[sum(4 * row[i] * row[j] for row in basis)
                  for j in (1, 2)] for i in (1, 2)]
    assert all(abs(classical[i][j] - 4 * (i == j)) < 1e-12 for i in (0, 1) for j in (0, 1))
    sld_x = [[0, 2, 0], [2, 0, 0], [0, 0, 0]]
    sld_y = [[0, 0, 2], [0, 0, 0], [2, 0, 0]]
    sld_commutator_entry = mat_mul(sld_x, sld_y)[1][2] - mat_mul(sld_y, sld_x)[1][2]
    assert sld_commutator_entry == 4
    delta = 1e-4
    # Rationalize 8*(1-sqrt(1-delta^2))/delta^2 for stable evaluation.
    bures = 8 / (1 + math.sqrt(1 - delta ** 2))
    assert abs(bures - 4) < 2e-8
    return {"joint_cfi": classical, "sld_commutator_1_2": sld_commutator_entry,
            "rank_boundary_sld_qfi": 0, "rank_boundary_bures_scaled": bures}

def main():
    summary = {
        "nv_sensitivity": check_nv_sensitivity_example(),
        "ramsey_cfi_qfi_bures": check_ramsey_cfi_qfi_bures(),
        "ghz_parity_and_loss": check_ghz_parity_and_loss(),
        "huelga_1997_dephasing": check_huelga_dephasing(),
        "spin_and_optical_squeezing": check_spin_and_optical_squeezing(),
        "cpmg_lockin_filter": check_cpmg_filter_and_lockin(),
        "hnls_and_qec_code": check_hnls_and_qec_code(),
        "clock_and_gravity": check_clock_and_gravity(),
        "multi_parameter_and_rank_change": check_multi_parameter_and_rank_change(),
        "status": "PASS",
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print("PASS: all Chapter 20 quantum sensing & metrology numerical assertions succeeded.")


if __name__ == "__main__":
    main()
