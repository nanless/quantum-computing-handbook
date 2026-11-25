#!/usr/bin/env python3
"""Generate five light/dark adaptive textbook SVG figures (Part 1b, Ch 05-08).

Run:
    python3 codes/practice/generate_v2_figures_part1b.py

Dependencies:
    Python 3 standard library only (cmath, html, math, pathlib, xml.etree.ElementTree).
    Deterministic numerical calculations (no RNG / no network / no cloud services).

Outputs (under handbook/assets/):
    1. v2-05-bloch-noise-channels.svg  (Ch 05: 2x2 Bloch x-z noise channel maps)
    2. v2-06-grover-geometry.svg       (Ch 06: 2D Grover / amplitude amplification geometry)
    3. v2-06-qft-circuit.svg           (Ch 06: 3-qubit QFT circuit with H, R2, R3, SWAP)
    4. v2-07-shor-hhl-pipeline.svg     (Ch 07: Shor N=15,a=2,Q=16 & HHL 3-stage skeleton)
    5. v2-08-qaoa-maxcut.svg           (Ch 08: 3-node path MaxCut & exact p=1 QAOA heatmap)

Verification & Boundaries:
    Every figure performs built-in analytical and matrix/statevector assertions
    (Kraus completeness & PSD, 2D reflection algebra, full 8x8 QFT unitary check,
    16-point Shor DFT & 2x2 HHL check, 8-amplitude QAOA statevector check vs closed form)
    and parses every emitted SVG via xml.etree.ElementTree.
    All coordinates use viewBox="0 0 1000 580" with all text kept >= 30 px from borders.
"""

from __future__ import annotations

import cmath
import html
import math
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT / "handbook" / "assets"
W, H = 1000, 580
TOL = 1e-11


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def sub(txt: str, size: float = 9.5) -> str:
    return f'<tspan dy="3" font-size="{size}">{esc(txt)}</tspan><tspan dy="-3">&#8203;</tspan>'


def sup(txt: str, size: float = 9.5) -> str:
    return f'<tspan dy="-5" font-size="{size}">{esc(txt)}</tspan><tspan dy="5">&#8203;</tspan>'


def arrow_poly(x1: float, y1: float, x2: float, y2: float, length: float = 10.0, width: float = 6.0) -> str:
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy)
    assert norm > 1e-9, "Zero-length arrow"
    ux, uy = dx / norm, dy / norm
    px, py = -uy, ux
    bx, by = x2 - length * ux, y2 - length * uy
    p1x, p1y = bx + (width / 2.0) * px, by + (width / 2.0) * py
    p2x, p2y = bx - (width / 2.0) * px, by - (width / 2.0) * py
    return f"M{x2:.2f} {y2:.2f}L{p1x:.2f} {p1y:.2f}L{p2x:.2f} {p2y:.2f}Z"


def base_style(extra_light: str = "", extra_dark: str = "") -> str:
    return f"""  <style>
    :root{{color-scheme:light dark}}
    .bg{{fill:#f8fafc}}
    .card{{fill:#ffffff;stroke:#cbd8e4;stroke-width:1.6}}
    .subcard{{fill:#f2f6fa;stroke:#d2dee9;stroke-width:1.2}}
    .pill{{fill:#ffffff;fill-opacity:.94;stroke:#8fa6ba;stroke-width:1.2}}
    .ink{{fill:#13263a}}
    .muted{{fill:#496176}}
    .accent{{fill:#0e6b8a}}
    .warn{{fill:#b93c3c}}
    .gold{{fill:#9c6510}}
    .purple{{fill:#5b42a6}}
    .green{{fill:#1d7557}}
    .axis{{stroke:#2b465e;stroke-width:1.8;fill:none}}
    .axishead{{fill:#2b465e}}
    .grid{{stroke:#d8e3ec;stroke-width:1;stroke-dasharray:4 4;fill:none}}
    .divider{{stroke:#c6d5e2;stroke-width:1.3;stroke-dasharray:5 5;fill:none}}
    .unit-circle{{stroke:#5d7890;stroke-width:1.8;stroke-dasharray:6 5;fill:none}}
    .region{{fill:#bae6fd;fill-opacity:.48;stroke:#0e6b8a;stroke-width:2.4}}
    .region-alt{{fill:#fde68a;fill-opacity:.44;stroke:#a8640b;stroke-width:2.4}}
    .vec-a{{stroke:#0e6b8a;stroke-width:2.8;fill:none}}
    .vec-a-head{{fill:#0e6b8a}}
    .vec-b{{stroke:#c04040;stroke-width:2.6;stroke-dasharray:8 4;fill:none}}
    .vec-b-head{{fill:#c04040}}
    .vec-c{{stroke:#5b42a6;stroke-width:3.0;fill:none}}
    .vec-c-head{{fill:#5b42a6}}
    .wire{{stroke:#1d3b54;stroke-width:2.2;fill:none}}
    .gate{{fill:#e6f4fa;stroke:#0e6b8a;stroke-width:2}}
    .gate-alt{{fill:#fef3d6;stroke:#a8640b;stroke-width:2}}
    .gate-inv{{fill:#ede9fe;stroke:#5b42a6;stroke-width:2}}
    .node-a{{fill:#0e6b8a;stroke:#0a5068;stroke-width:2}}
    .node-a-txt{{fill:#ffffff}}
    .ctrl{{fill:#13263a}}
    .fixed{{fill:#c04040;stroke:#ffffff;stroke-width:1.6}}
    .title{{font:700 20px 'PingFang SC','Noto Sans SC',system-ui,'STIX Two Math','Cambria Math','Apple Symbols',sans-serif}}
    .subtitle{{font:400 14px 'PingFang SC','Noto Sans SC',system-ui,'STIX Two Math','Cambria Math','Apple Symbols',sans-serif}}
    .h2{{font:600 14.5px 'PingFang SC','Noto Sans SC',system-ui,'STIX Two Math','Cambria Math','Apple Symbols',sans-serif}}
    .lbl{{font:500 13.5px 'PingFang SC','Noto Sans SC',system-ui,'STIX Two Math','Cambria Math','Apple Symbols',sans-serif}}
    .sm{{font:400 13px 'PingFang SC','Noto Sans SC',system-ui,'STIX Two Math','Cambria Math','Apple Symbols',sans-serif}}
    .mono{{font:500 12.8px 'SFMono-Regular',Menlo,Consolas,monospace}}
    .gate-txt{{font:700 15px Georgia,'Times New Roman',serif}}
    {extra_light}
    @media(prefers-color-scheme:dark){{
      .bg{{fill:#101820}}
      .card{{fill:#162330;stroke:#395066}}
      .subcard{{fill:#1d2e3d;stroke:#3d566d}}
      .pill{{fill:#14212c;fill-opacity:.94;stroke:#6d8ba3}}
      .ink{{fill:#eef6ff}}
      .muted{{fill:#b4c8da}}
      .accent{{fill:#6ed0f7}}
      .warn{{fill:#ff8585}}
      .gold{{fill:#f2c15a}}
      .purple{{fill:#c0adff}}
      .green{{fill:#6dd4aa}}
      .axis{{stroke:#b9d0e2}}
      .axishead{{fill:#b9d0e2}}
      .grid{{stroke:#32485c}}
      .divider{{stroke:#4a637a}}
      .unit-circle{{stroke:#8aa5bc}}
      .region{{fill:#17506e;fill-opacity:.58;stroke:#6ed0f7}}
      .region-alt{{fill:#5a4318;fill-opacity:.58;stroke:#f2c15a}}
      .vec-a{{stroke:#6ed0f7}}
      .vec-a-head{{fill:#6ed0f7}}
      .vec-b{{stroke:#ff8585}}
      .vec-b-head{{fill:#ff8585}}
      .vec-c{{stroke:#c0adff}}
      .vec-c-head{{fill:#c0adff}}
      .wire{{stroke:#c9deee}}
      .gate{{fill:#19425a;stroke:#6ed0f7}}
      .gate-alt{{fill:#493818;stroke:#f2c15a}}
      .gate-inv{{fill:#342859;stroke:#c0adff}}
      .node-a{{fill:#1b5c7a;stroke:#6ed0f7;stroke-width:2.2}}
      .node-a-txt{{fill:#eef6ff}}
      .ctrl{{fill:#eef6ff}}
      .fixed{{fill:#ff8585;stroke:#162330}}
      {extra_dark}
    }}
  </style>"""


def wrap_svg(svg_id: str, title: str, desc: str, body: str, extra_light: str = "", extra_dark: str = "", defs: str = "") -> str:
    t_id = f"{svg_id}-title"
    d_id = f"{svg_id}-desc"
    defs_block = f"  <defs>\n{defs}\n  </defs>\n" if defs else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'role="img" aria-labelledby="{t_id} {d_id}">\n'
        f'  <title id="{t_id}">{esc(title)}</title>\n'
        f'  <desc id="{d_id}">{esc(desc)}</desc>\n'
        f'{base_style(extra_light, extra_dark)}\n'
        f'{defs_block}'
        f'  <rect class="bg" width="{W}" height="{H}" rx="20"/>\n'
        f'{body}\n'
        f'</svg>\n'
    )


# ---------------------------------------------------------------------------
# Linear algebra helpers (pure Python standard library)
# ---------------------------------------------------------------------------
def matmul(a: list[list[complex]], b: list[list[complex]]) -> list[list[complex]]:
    n, m, p = len(a), len(b), len(b[0])
    assert len(a[0]) == m
    return [[sum(a[i][k] * b[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def dagger(a: list[list[complex]]) -> list[list[complex]]:
    return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]


def matadd(a: list[list[complex]], b: list[list[complex]]) -> list[list[complex]]:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def trace(a: list[list[complex]]) -> complex:
    return sum(a[i][i] for i in range(len(a)))


def scale_mat(s: complex, a: list[list[complex]]) -> list[list[complex]]:
    return [[s * v for v in row] for row in a]


I2 = [[1 + 0j, 0j], [0j, 1 + 0j]]
X2 = [[0j, 1 + 0j], [1 + 0j, 0j]]
Y2 = [[0j, -1j], [1j, 0j]]
Z2 = [[1 + 0j, 0j], [0j, -1 + 0j]]


def apply_channel(rho: list[list[complex]], kraus: list[list[list[complex]]]) -> list[list[complex]]:
    out = [[0j, 0j], [0j, 0j]]
    for k in kraus:
        out = matadd(out, matmul(matmul(k, rho), dagger(k)))
    return out


def verify_kraus(kraus: list[list[list[complex]]]) -> None:
    acc = [[0j, 0j], [0j, 0j]]
    for k in kraus:
        acc = matadd(acc, matmul(dagger(k), k))
    for i in range(2):
        for j in range(2):
            expected = 1.0 if i == j else 0.0
            assert abs(acc[i][j] - expected) < TOL, f"Kraus completeness failed: {acc}"


def rho_from_bloch(rx: float, ry: float, rz: float) -> list[list[complex]]:
    return [
        [0.5 * (1.0 + rz) + 0j, 0.5 * (rx - 1j * ry)],
        [0.5 * (rx + 1j * ry), 0.5 * (1.0 - rz) + 0j],
    ]


def bloch_from_rho(rho: list[list[complex]]) -> tuple[float, float, float]:
    assert abs(trace(rho) - 1.0) < TOL
    assert abs(rho[0][1] - rho[1][0].conjugate()) < TOL
    det = (rho[0][0] * rho[1][1] - rho[0][1] * rho[1][0]).real
    assert det >= -TOL, f"Non-PSD density matrix det={det}"
    rx = trace(matmul(X2, rho)).real
    ry = trace(matmul(Y2, rho)).real
    rz = trace(matmul(Z2, rho)).real
    return rx, ry, rz


# ===========================================================================
# Figure 1: v2-05-bloch-noise-channels.svg
# ===========================================================================
def build_fig1_bloch_noise_channels() -> tuple[str, dict]:
    p_bf, p_pf, p_dep, gamma_ad = 0.25, 0.25, 0.4, 0.5
    rx_s = f"r{sub('x')}"
    rz_s = f"r{sub('z')}"
    ry_s = f"r{sub('y')}"

    channels = [
        {
            "key": "a",
            "title": "(a) 比特翻转（Bit Flip, p = 0.25）",
            "formula": "ℰ(ρ) = (1−p)ρ + p XρX",
            "map_x": f"{rx_s}′ = {rx_s}",
            "map_z": f"{rz_s}′ = (1−2p){rz_s} = 0.50 {rz_s}",
            "geom": "半轴 (1.00, 0.50)，中心 (0, 0)",
            "phys": "不动点：|±⟩（x 轴）；z 轴缩至一半",
            "kraus": [scale_mat(math.sqrt(1 - p_bf), I2), scale_mat(math.sqrt(p_bf), X2)],
            "expected": (0.0, 0.0, 1.0, 0.5),
            "fixed": [(-1.0, 0.0), (1.0, 0.0)],
            "arrows": [(0.0, 1.0, 0.0, 0.5), (0.0, -1.0, 0.0, -0.5)],
            "region_cls": "region",
        },
        {
            "key": "b",
            "title": "(b) 相位翻转（Phase Flip, p = 0.25）",
            "formula": "ℰ(ρ) = (1−p)ρ + p ZρZ",
            "map_x": f"{rx_s}′ = (1−2p){rx_s} = 0.50 {rx_s}",
            "map_z": f"{rz_s}′ = {rz_s}",
            "geom": "半轴 (0.50, 1.00)，中心 (0, 0)",
            "phys": "不动点：|0⟩, |1⟩（布居不变，相干衰减）",
            "kraus": [scale_mat(math.sqrt(1 - p_pf), I2), scale_mat(math.sqrt(p_pf), Z2)],
            "expected": (0.0, 0.0, 0.5, 1.0),
            "fixed": [(0.0, 1.0), (0.0, -1.0)],
            "arrows": [(1.0, 0.0, 0.5, 0.0), (-1.0, 0.0, -0.5, 0.0)],
            "region_cls": "region",
        },
        {
            "key": "c",
            "title": "(c) 退极化（Depolarizing, p = 0.4）",
            "formula": f"𝒟{sub('p')}(ρ) = (1−p)ρ + p I/2",
            "map_x": f"{rx_s}′ = (1−p){rx_s} = 0.60 {rx_s}",
            "map_z": f"{rz_s}′ = (1−p){rz_s} = 0.60 {rz_s}",
            "geom": "各向同性半径 ‖r′‖ = 0.60，中心 (0, 0)",
            "phys": "唯一不动点：球心最大混态 I/2",
            "kraus": [
                scale_mat(math.sqrt(1 - 0.75 * p_dep), I2),
                scale_mat(math.sqrt(0.25 * p_dep), X2),
                scale_mat(math.sqrt(0.25 * p_dep), Y2),
                scale_mat(math.sqrt(0.25 * p_dep), Z2),
            ],
            "expected": (0.0, 0.0, 0.6, 0.6),
            "fixed": [(0.0, 0.0)],
            "arrows": [
                (0.0, 1.0, 0.0, 0.6),
                (0.0, -1.0, 0.0, -0.6),
                (1.0, 0.0, 0.6, 0.0),
                (-1.0, 0.0, -0.6, 0.0),
            ],
            "region_cls": "region",
        },
        {
            "key": "d",
            "title": "(d) 振幅阻尼（Amplitude Damping, γ = 0.5）",
            "formula": f"K{sub('0')}=diag(1,√(1−γ)), K{sub('1')}=√γ|0⟩⟨1|",
            "map_x": f"{rx_s}′ = √(1−γ) {rx_s} ≈ 0.707 {rx_s}",
            "map_z": f"{rz_s}′ = γ + (1−γ){rz_s} = 0.5 + 0.5 {rz_s}",
            "geom": "半轴 (0.707, 0.50)，中心 (0, 0.50)",
            "phys": "缩向北极不动点 |0⟩；|1⟩ 映至球心",
            "kraus": [
                [[1 + 0j, 0j], [0j, math.sqrt(1 - gamma_ad) + 0j]],
                [[0j, math.sqrt(gamma_ad) + 0j], [0j, 0j]],
            ],
            "expected": (0.0, 0.5, math.sqrt(0.5), 0.5),
            "fixed": [(0.0, 1.0)],
            "arrows": [
                (0.0, -1.0, 0.0, 0.0),
                (1.0, 0.0, math.sqrt(0.5), 0.5),
                (-1.0, 0.0, -math.sqrt(0.5), 0.5),
            ],
            "region_cls": "region-alt",
        },
    ]

    n_pts = 96
    for ch in channels:
        verify_kraus(ch["kraus"])
        cx0, cz0, ax_exp, az_exp = ch["expected"]
        pts = []
        for idx in range(n_pts):
            phi = 2.0 * math.pi * idx / n_pts
            rx, rz = math.cos(phi), math.sin(phi)
            rho_out = apply_channel(rho_from_bloch(rx, 0.0, rz), ch["kraus"])
            rx_p, ry_p, rz_p = bloch_from_rho(rho_out)
            assert abs(ry_p) < TOL
            assert abs(rx_p - (cx0 + ax_exp * rx)) < TOL
            assert abs(rz_p - (cz0 + az_exp * rz)) < TOL
            pts.append((rx_p, rz_p))
        ch["pts"] = pts
        for fx, fz in ch["fixed"]:
            rx_p, ry_p, rz_p = bloch_from_rho(apply_channel(rho_from_bloch(fx, 0.0, fz), ch["kraus"]))
            assert abs(rx_p - fx) < TOL and abs(ry_p) < TOL and abs(rz_p - fz) < TOL

    parts = [
        '  <text class="title ink" x="38" y="52">单比特四大噪声信道在 Bloch 球 x–z 截面上的几何变换</text>',
        f'  <text class="subtitle muted" x="38" y="76">外圈虚线：初始纯态单位圆 ({rx_s}² + {rz_s}² = 1，无量纲)；实线填充：经 CPTP 信道演化后区域；实心红点：不动点</text>',
    ]

    card_w, card_h = 456, 206
    positions = [(36, 94), (508, 94), (36, 314), (508, 314)]
    R = 56.0

    for ch, (x0, y0) in zip(channels, positions):
        cx = x0 + 98.0
        cy = y0 + 114.0
        parts.append(f'  <rect class="card" x="{x0}" y="{y0}" width="{card_w}" height="{card_h}" rx="12"/>')
        parts.append(f'  <text class="h2 ink" x="{x0 + 16}" y="{y0 + 25}">{esc(ch["title"])}</text>')

        # Axes
        ax_pad = 14.0
        parts.append(f'  <line class="axis" x1="{cx - R - ax_pad:.1f}" y1="{cy:.1f}" x2="{cx + R + ax_pad:.1f}" y2="{cy:.1f}"/>')
        parts.append(f'  <path class="axishead" d="{arrow_poly(cx, cy, cx + R + ax_pad, cy, 8, 5)}"/>')
        parts.append(f'  <line class="axis" x1="{cx:.1f}" y1="{cy + R + ax_pad:.1f}" x2="{cx:.1f}" y2="{cy - R - ax_pad:.1f}"/>')
        parts.append(f'  <path class="axishead" d="{arrow_poly(cx, cy, cx, cy - R - ax_pad, 8, 5)}"/>')

        # Unit circle (dashed)
        parts.append(f'  <circle class="unit-circle" cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}"/>')

        # Transformed region polygon computed from Kraus operators
        d_cmds = [f'{"M" if i == 0 else "L"}{cx + p[0] * R:.2f} {cy - p[1] * R:.2f}' for i, p in enumerate(ch["pts"])]
        d_cmds.append("Z")
        parts.append(f'  <path class="{ch["region_cls"]}" d="{"".join(d_cmds)}"/>')

        # Contraction arrows
        for sx, sz, tx, tz in ch["arrows"]:
            x1, y1 = cx + sx * R, cy - sz * R
            x2, y2 = cx + tx * R, cy - tz * R
            dx_a, dy_a = x2 - x1, y2 - y1
            dist = math.hypot(dx_a, dy_a)
            sx1, sy1 = x1 + 3.0 * dx_a / dist, y1 + 3.0 * dy_a / dist
            tx2, ty2 = x2 - 2.0 * dx_a / dist, y2 - 2.0 * dy_a / dist
            parts.append(f'  <line class="vec-b" style="stroke-width:1.7;stroke-dasharray:none" x1="{sx1:.1f}" y1="{sy1:.1f}" x2="{tx2:.1f}" y2="{ty2:.1f}"/>')
            parts.append(f'  <path class="vec-b-head" d="{arrow_poly(sx1, sy1, tx2, ty2, 7, 4.5)}"/>')

        # Shifted center marker for amplitude damping (placed cleanly inside ellipse)
        cx0, cz0, _, _ = ch["expected"]
        if abs(cz0) > 1e-6:
            mcx, mcy = cx + cx0 * R, cy - cz0 * R
            parts.append(f'  <line class="axis" style="stroke-width:1.6" x1="{mcx - 4.5:.1f}" y1="{mcy:.1f}" x2="{mcx + 4.5:.1f}" y2="{mcy:.1f}"/>')
            parts.append(f'  <line class="axis" style="stroke-width:1.6" x1="{mcx:.1f}" y1="{mcy - 4.5:.1f}" x2="{mcx:.1f}" y2="{mcy + 4.5:.1f}"/>')
            parts.append(f'  <text class="sm gold" style="font-size:11.5px" x="{mcx:.1f}" y="{mcy + 16.5:.1f}" text-anchor="middle">(0, 0.5)</text>')

        # Fixed point markers
        for fx, fz in ch["fixed"]:
            parts.append(f'  <circle class="fixed" cx="{cx + fx * R:.1f}" cy="{cy - fz * R:.1f}" r="4.6"/>')

        # Axis & pole labels
        parts.append(f'  <text class="sm ink" x="{cx + 8:.1f}" y="{cy - R - 7:.1f}">+z |0⟩</text>')
        parts.append(f'  <text class="sm muted" x="{cx + 8:.1f}" y="{cy + R + 16:.1f}">−z |1⟩</text>')
        parts.append(f'  <text class="sm ink" x="{cx + R + 6:.1f}" y="{cy + 16:.1f}">+x</text>')
        parts.append(f'  <text class="sm muted" x="{cx - R - 24:.1f}" y="{cy + 16:.1f}">−x</text>')

        # Right-hand formula & property block inside each card (wide & cleanly padded)
        sub_x, sub_w = x0 + 188, 254
        tx = sub_x + 12
        parts.append(f'  <rect class="subcard" x="{sub_x}" y="{y0 + 38}" width="{sub_w}" height="152" rx="8"/>')
        parts.append(f'  <text class="lbl accent" x="{tx}" y="{y0 + 62}">{ch["formula"]}</text>')
        parts.append(f'  <text class="lbl ink" x="{tx}" y="{y0 + 90}">{ch["map_x"]}</text>')
        parts.append(f'  <text class="lbl ink" x="{tx}" y="{y0 + 114}">{ch["map_z"]}</text>')
        parts.append(f'  <line class="divider" x1="{tx}" y1="{y0 + 128}" x2="{sub_x + sub_w - 12}" y2="{y0 + 128}"/>')
        parts.append(f'  <text class="sm ink" x="{tx}" y="{y0 + 150}">{esc(ch["geom"])}</text>')
        parts.append(f'  <text class="sm muted" x="{tx}" y="{y0 + 174}">{esc(ch["phys"])}</text>')

    parts.append(
        f'  <text class="sm muted" x="38" y="541">'
        f'注：横轴 {rx_s}、纵轴 {rz_s} 为无量纲 Bloch 坐标（{ry_s} = 0 截面）；退极化采用本书 §5.3 约定 𝒟{sub("p")}(ρ) = (1−p)ρ + pI/2（等价于随机 Pauli 概率 q = 3p/4 = 0.3）。'
        '</text>'
    )

    svg = wrap_svg(
        "v2-05-bloch-noise",
        "单比特四大噪声信道对 Bloch 球 x-z 截面圆的变换",
        "2x2 四联图展示比特翻转(p=0.25)、相位翻转(p=0.25)、退极化(p=0.4)与振幅阻尼(γ=0.5)对 Bloch 球 x-z 单位圆的精确仿射收缩与不动点，曲线均由 Kraus 算子逐点计算。",
        "\n".join(parts),
    )
    return svg, {"channels_verified": 4, "boundary_samples_per_channel": n_pts}


# ===========================================================================
# Figure 2: v2-06-grover-geometry.svg
# ===========================================================================
def build_fig2_grover_geometry() -> tuple[str, dict]:
    sin_t = 0.25
    theta = math.asin(sin_t)
    cos_t = math.cos(theta)
    theta_deg = math.degrees(theta)
    assert abs(theta_deg - 14.477512185929925) < 1e-9

    s_vec = [[cos_t + 0j], [sin_t + 0j]]
    O_mat = [[1 + 0j, 0j], [0j, -1 + 0j]]
    D_mat = [
        [2 * cos_t * cos_t - 1 + 0j, 2 * cos_t * sin_t + 0j],
        [2 * cos_t * sin_t + 0j, 2 * sin_t * sin_t - 1 + 0j],
    ]
    G_mat = matmul(D_mat, O_mat)
    c2, s2 = math.cos(2 * theta), math.sin(2 * theta)
    R2t = [[c2 + 0j, -s2 + 0j], [s2 + 0j, c2 + 0j]]
    for i in range(2):
        for j in range(2):
            assert abs(G_mat[i][j] - R2t[i][j]) < TOL
    GdG = matmul(dagger(G_mat), G_mat)
    assert abs(GdG[0][0] - 1) < TOL and abs(GdG[1][1] - 1) < TOL and abs(GdG[0][1]) < TOL

    os_vec = matmul(O_mat, s_vec)
    gs_vec = matmul(G_mat, s_vec)
    assert abs(os_vec[0][0].real - cos_t) < TOL and abs(os_vec[1][0].real + sin_t) < TOL
    assert abs(gs_vec[0][0].real - math.cos(3 * theta)) < TOL
    assert abs(gs_vec[1][0].real - 11.0 / 16.0) < TOL

    mx = 0.5 * (os_vec[0][0].real + gs_vec[0][0].real)
    my = 0.5 * (os_vec[1][0].real + gs_vec[1][0].real)
    assert abs(mx - 0.875 * cos_t) < TOL and abs(my - 0.875 * sin_t) < TOL
    dot_perp = (gs_vec[0][0].real - os_vec[0][0].real) * cos_t + (gs_vec[1][0].real - os_vec[1][0].real) * sin_t
    assert abs(dot_perp) < TOL

    rows = []
    cur = s_vec
    for k in range(5):
        ang = (2 * k + 1) * theta
        amp_g = cur[1][0].real
        assert abs(amp_g - math.sin(ang)) < TOL
        rows.append((k, math.degrees(ang), amp_g, amp_g * amp_g))
        cur = matmul(G_mat, cur)
    assert abs(rows[2][2] - 61.0 / 64.0) < TOL

    # Spacious geometry inside left card (x=36..584, y=94..520)
    ox, oy = 114.0, 396.0
    R = 216.0

    def pt(vx: float, vy: float) -> tuple[float, float]:
        return ox + vx * R, oy - vy * R

    def arc_path(r: float, deg_start: float, deg_end: float) -> str:
        a1, a2 = math.radians(deg_start), math.radians(deg_end)
        x1, y1 = ox + r * math.cos(a1), oy - r * math.sin(a1)
        x2, y2 = ox + r * math.cos(a2), oy - r * math.sin(a2)
        sweep = 0 if deg_end > deg_start else 1
        large = 1 if abs(deg_end - deg_start) > 180 else 0
        return f"M{x1:.2f} {y1:.2f}A{r:.2f} {r:.2f} 0 {large} {sweep} {x2:.2f} {y2:.2f}"

    sx, sy = pt(cos_t, sin_t)
    ox_p, oy_p = pt(cos_t, -sin_t)
    gx, gy = pt(gs_vec[0][0].real, gs_vec[1][0].real)
    mx_p, my_p = pt(mx, my)

    # Right-angle mark at M
    ra = 8.5
    us_x, us_y = cos_t, -sin_t
    uc_x, uc_y = -sin_t, -cos_t
    ra_p1 = (mx_p - ra * us_x, my_p - ra * us_y)
    ra_p2 = (ra_p1[0] + ra * uc_x, ra_p1[1] + ra * uc_y)
    ra_p3 = (mx_p + ra * uc_x, my_p + ra * uc_y)

    parts = [
        '  <text class="title ink" x="38" y="52">Grover / 振幅放大的二维几何旋转：两次反射等价于净旋 2θ</text>',
        '  <text class="subtitle muted" x="38" y="76">二维正交子空间 {|B⟩, |G⟩} 内的单位圆（振幅无量纲），取 θ = arcsin(1/4) ≈ 14.48°（对应初始成功率 a = 1/16）</text>',
        '  <rect class="card" x="36" y="94" width="548" height="426" rx="12"/>',
        '  <text class="h2 ink" x="54" y="120">几何演化图（实线圆点 |s⟩ · 虚线空圈 O|s⟩ · 粗线菱形 𝒬|s⟩）</text>',
    ]

    # Ticks on |B> and |G>
    px_half, _ = pt(0.5, 0.0)
    px_one, _ = pt(1.0, 0.0)
    _, py_half = pt(0.0, 0.5)
    _, py_one = pt(0.0, 1.0)
    for x_tk in (px_half, px_one):
        parts.append(f'  <line class="axis" style="stroke-width:1.4" x1="{x_tk:.1f}" y1="{oy - 4:.1f}" x2="{x_tk:.1f}" y2="{oy + 4:.1f}"/>')
    parts.append(f'  <text class="sm muted" x="{px_half:.1f}" y="{oy + 20:.1f}" text-anchor="middle">0.5</text>')
    parts.append(f'  <text class="sm muted" x="{px_one - 14:.1f}" y="{oy + 20:.1f}" text-anchor="middle">1.0</text>')
    for y_tk, lbl in ((py_half, "0.5"), (py_one, "1.0")):
        parts.append(f'  <line class="axis" style="stroke-width:1.4" x1="{ox - 4:.1f}" y1="{y_tk:.1f}" x2="{ox + 4:.1f}" y2="{y_tk:.1f}"/>')
        parts.append(f'  <text class="sm muted" x="{ox - 10:.1f}" y="{y_tk + 4:.1f}" text-anchor="end">{lbl}</text>')
    parts.append(f'  <text class="sm muted" x="{ox - 10:.1f}" y="{oy + 18:.1f}" text-anchor="end">0</text>')

    # Axes: |B> horizontal, |G> vertical
    parts.append(f'  <line class="axis" x1="{ox - 20:.1f}" y1="{oy:.1f}" x2="{ox + R + 122:.1f}" y2="{oy:.1f}"/>')
    parts.append(f'  <path class="axishead" d="{arrow_poly(ox, oy, ox + R + 122, oy, 9, 5.5)}"/>')
    parts.append(f'  <line class="axis" x1="{ox:.1f}" y1="{oy + 98:.1f}" x2="{ox:.1f}" y2="{oy - R - 26:.1f}"/>')
    parts.append(f'  <path class="axishead" d="{arrow_poly(ox, oy, ox, oy - R - 26, 9, 5.5)}"/>')
    parts.append(f'  <text class="lbl ink" x="{ox + 12:.1f}" y="{oy - R - 14:.1f}">|G⟩（目标态振幅，无量纲）</text>')
    parts.append(f'  <text class="lbl ink" x="{ox + R + 20:.1f}" y="{oy + 20:.1f}">|B⟩（非目标态）</text>')

    # Unit circle arc (-28 deg to +96 deg)
    parts.append(f'  <path class="unit-circle" d="{arc_path(R, -27.0, 95.0)}"/>')

    # Reflection construction chords + right-angle marks
    parts.append(f'  <line class="divider" style="stroke-width:1.6" x1="{sx:.1f}" y1="{sy:.1f}" x2="{ox_p:.1f}" y2="{oy_p:.1f}"/>')
    parts.append(f'  <path class="axis" style="stroke-width:1.2" d="M{sx - 8:.1f} {oy:.1f}V{oy - 8:.1f}H{sx:.1f}"/>')
    parts.append(f'  <line class="divider" style="stroke-width:1.6" x1="{ox_p:.1f}" y1="{oy_p:.1f}" x2="{gx:.1f}" y2="{gy:.1f}"/>')
    parts.append(
        f'  <path class="axis" style="stroke-width:1.2" '
        f'd="M{ra_p1[0]:.1f} {ra_p1[1]:.1f}L{ra_p2[0]:.1f} {ra_p2[1]:.1f}L{ra_p3[0]:.1f} {ra_p3[1]:.1f}"/>'
    )

    # Subtle extension of ray |s> past unit circle
    s_ext_x, s_ext_y = pt(1.12 * cos_t, 1.12 * sin_t)
    parts.append(f'  <line class="grid" x1="{sx:.1f}" y1="{sy:.1f}" x2="{s_ext_x:.1f}" y2="{s_ext_y:.1f}"/>')

    # Non-overlapping angle arcs
    parts.append(f'  <path class="vec-b" style="stroke-width:2.0;stroke-dasharray:5 3" d="{arc_path(62.0, 0.0, -theta_deg)}"/>')
    parts.append(f'  <text class="sm warn" x="{ox + 68:.1f}" y="{oy + 17:.1f}">−θ</text>')

    parts.append(f'  <path class="vec-a" style="stroke-width:2.0" d="{arc_path(74.0, 0.0, theta_deg)}"/>')
    parts.append(f'  <text class="sm accent" x="{ox + 82:.1f}" y="{oy - 7:.1f}">θ ≈ 14.48°</text>')

    # Net +2*theta rotation arc at r=112 with clean two-line label inside wedge
    r_arc = 112.0
    parts.append(f'  <path class="vec-c" style="stroke-width:2.4" d="{arc_path(r_arc, theta_deg, 3 * theta_deg)}"/>')
    a_end = math.radians(3 * theta_deg)
    a_prev = math.radians(3 * theta_deg - 4.5)
    parts.append(
        f'  <path class="vec-c-head" d="{arrow_poly(ox + r_arc * math.cos(a_prev), oy - r_arc * math.sin(a_prev), ox + r_arc * math.cos(a_end), oy - r_arc * math.sin(a_end), 8, 5)}"/>'
    )
    a_lbl = math.radians(2.25 * theta_deg)
    lx_2t = ox + (r_arc + 10.0) * math.cos(a_lbl)
    ly_2t = oy - (r_arc + 10.0) * math.sin(a_lbl)
    parts.append(f'  <text class="sm purple" style="font-weight:600" x="{lx_2t:.1f}" y="{ly_2t - 8:.1f}">净旋 +2θ</text>')
    parts.append(f'  <text class="sm purple" x="{lx_2t:.1f}" y="{ly_2t + 12:.1f}">(≈ 28.96°)</text>')

    # Three state vectors
    parts.append(f'  <line class="vec-a" x1="{ox:.1f}" y1="{oy:.1f}" x2="{sx:.1f}" y2="{sy:.1f}"/>')
    parts.append(f'  <path class="vec-a-head" d="{arrow_poly(ox, oy, sx, sy, 10, 6)}"/>')
    parts.append(f'  <circle class="vec-a-head" cx="{sx:.1f}" cy="{sy:.1f}" r="4.5"/>')

    parts.append(f'  <line class="vec-b" x1="{ox:.1f}" y1="{oy:.1f}" x2="{ox_p:.1f}" y2="{oy_p:.1f}"/>')
    parts.append(f'  <path class="vec-b-head" d="{arrow_poly(ox, oy, ox_p, oy_p, 10, 6)}"/>')
    parts.append(f'  <circle style="fill:none;stroke-width:2.2" class="vec-b" cx="{ox_p:.1f}" cy="{oy_p:.1f}" r="5.5"/>')

    parts.append(f'  <line class="vec-c" x1="{ox:.1f}" y1="{oy:.1f}" x2="{gx:.1f}" y2="{gy:.1f}"/>')
    parts.append(f'  <path class="vec-c-head" d="{arrow_poly(ox, oy, gx, gy, 10, 6)}"/>')
    parts.append(f'  <path class="vec-c-head" d="M{gx:.1f} {gy - 6:.1f}L{gx + 6:.1f} {gy:.1f}L{gx:.1f} {gy + 6:.1f}L{gx - 6:.1f} {gy:.1f}Z"/>')

    # Vector labels cleanly placed in open right-side space (21px vertical spacing avoids bbox touch)
    parts.append(f'  <text class="lbl accent" x="{sx + 18:.1f}" y="{sy - 9:.1f}">初态 |s⟩ (+θ)</text>')
    parts.append(f'  <text class="sm muted" x="{sx + 18:.1f}" y="{sy + 12:.1f}">坐标 (0.968, 0.250)</text>')

    parts.append(f'  <text class="lbl warn" x="{ox_p + 18:.1f}" y="{oy_p + 1:.1f}">O|s⟩ (−θ)</text>')
    parts.append(f'  <text class="sm muted" x="{ox_p + 18:.1f}" y="{oy_p + 22:.1f}">① 关于 |B⟩ 反射</text>')

    parts.append(f'  <text class="lbl purple" x="{gx + 14:.1f}" y="{gy - 11:.1f}">𝒬|s⟩ = DO|s⟩ (3θ ≈ 43.43°)</text>')
    parts.append(f'  <text class="sm muted" x="{gx + 14:.1f}" y="{gy + 10:.1f}">② 关于 |s⟩ 反射，⟨G|𝒬|s⟩ = 11/16</text>')

    # Right column: 3 info cards (x=600..964)
    rx0, rw = 600, 364
    parts.append(f'  <rect class="card" x="{rx0}" y="94" width="{rw}" height="132" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{rx0 + 16}" y="120">两步反射与净旋转矩阵（基序 |B⟩, |G⟩）</text>')
    parts.append(f'  <text class="sm ink" x="{rx0 + 16}" y="144">① 相位标记：O = S{sub("G")} = I − 2Π{sub("G")}（平面内关于 |B⟩ 反射）</text>')
    parts.append(f'  <text class="sm ink" x="{rx0 + 16}" y="168">② 扩散算符：D = 2|s⟩⟨s| − I（关于 |s⟩ 反射）</text>')
    parts.append(f'  <text class="sm purple" x="{rx0 + 16}" y="192">③ 单步迭代：𝒬 = DO = R(2θ)，净旋 +2θ</text>')
    parts.append(f'  <text class="sm muted" x="{rx0 + 16}" y="214">注：次序不可换，OD|s⟩ = O|s⟩ 首轮不增概率</text>')

    parts.append(f'  <rect class="card" x="{rx0}" y="238" width="{rw}" height="164" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{rx0 + 16}" y="264">逐轮精确演化（sin θ = 1/4, a = M/N = 1/16）</text>')
    parts.append(f'  <line class="divider" x1="{rx0 + 14}" y1="276" x2="{rx0 + rw - 14}" y2="276"/>')
    c1, c2_x, c3, c4 = rx0 + 16, rx0 + 64, rx0 + 164, rx0 + 236
    parts.append(f'  <text class="sm muted" x="{c1}" y="294">轮次</text>')
    parts.append(f'  <text class="sm muted" x="{c2_x}" y="294">角度 (2k+1)θ</text>')
    parts.append(f'  <text class="sm muted" x="{c3}" y="294">目标振幅</text>')
    parts.append(f'  <text class="sm muted" x="{c4}" y="294">成功率 P(G)</text>')
    for idx, (k, deg, amp, prob) in enumerate(rows[:4]):
        ry = 318 + idx * 24
        cls = "mono purple" if k == 1 else ("mono green" if k == 3 else "mono ink")
        tag = " (首峰)" if k == 3 else ""
        parts.append(f'  <text class="{cls}" x="{c1}" y="{ry}">k={k}</text>')
        parts.append(f'  <text class="{cls}" x="{c2_x}" y="{ry}">{2 * k + 1}θ={deg:5.2f}°</text>')
        parts.append(f'  <text class="{cls}" x="{c3}" y="{ry}">{amp:.4f}</text>')
        parts.append(f'  <text class="{cls}" x="{c4}" y="{ry}">{prob * 100:5.2f}%{tag}</text>')

    parts.append(f'  <rect class="card" x="{rx0}" y="414" width="{rw}" height="106" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{rx0 + 16}" y="440">首峰停步与过旋</text>')
    parts.append(f'  <text class="sm ink" x="{rx0 + 16}" y="464">k 轮后：𝒬ᵏ|s⟩ = cos((2k+1)θ)|B⟩ + sin((2k+1)θ)|G⟩</text>')
    parts.append(f'  <text class="sm ink" x="{rx0 + 16}" y="486">首峰连续步数约 2.61 → 就近取 k = 3</text>')
    parts.append(f'  <text class="sm warn" x="{rx0 + 16}" y="508">若继续至 k = 4 (9θ ≈ 130.3°)，P(G) 降至 {rows[4][3] * 100:.1f}%</text>')

    parts.append(
        '  <text class="sm muted" x="38" y="544">'
        '注：横纵轴均为无量纲实振幅分量；向量以实线圆点(|s⟩)、虚线空心圆(O|s⟩)与粗线菱形(𝒬|s⟩)区分，黑白阅读清晰。'
        '</text>'
    )

    svg = wrap_svg(
        "v2-06-grover-geometry",
        "Grover 振幅放大在 {|B⟩, |G⟩} 平面内的精确几何旋转",
        "取 θ = arcsin(1/4) ≈ 14.48°，精确绘出初态 |s⟩、关于 |B⟩ 反射的 O|s⟩ (-θ) 与再关于 |s⟩ 反射的 𝒬|s⟩ (3θ)，单步净旋 +2θ，并列出 k=0..3 的精确成功率。",
        "\n".join(parts),
    )
    return svg, {
        "theta_deg": round(theta_deg, 4),
        "sin_3theta": round(rows[1][2], 6),
        "best_k": 3,
        "best_prob": round(rows[3][3], 6),
    }


# ===========================================================================
# Figure 3: v2-06-qft-circuit.svg
# ===========================================================================
def build_fig3_qft_circuit() -> tuple[str, dict]:
    def single_qubit_op(u: list[list[complex]], q_idx: int) -> list[list[complex]]:
        mat = [[0j] * 8 for _ in range(8)]
        bit = 2 - q_idx
        for col in range(8):
            b_in = (col >> bit) & 1
            for b_out in (0, 1):
                row = (col & ~(1 << bit)) | (b_out << bit)
                mat[row][col] += u[b_out][b_in]
        return mat

    def ctrl_rk_op(ctrl_idx: int, targ_idx: int, k: int) -> list[list[complex]]:
        phase = cmath.exp(2j * math.pi / (2 ** k))
        mat = [[1 + 0j if i == j else 0j for j in range(8)] for i in range(8)]
        bc, bt = 2 - ctrl_idx, 2 - targ_idx
        for state in range(8):
            if ((state >> bc) & 1) == 1 and ((state >> bt) & 1) == 1:
                mat[state][state] = phase
        return mat

    def swap_op(i_idx: int, j_idx: int) -> list[list[complex]]:
        bi, bj = 2 - i_idx, 2 - j_idx
        mat = [[0j] * 8 for _ in range(8)]
        for col in range(8):
            vi, vj = (col >> bi) & 1, (col >> bj) & 1
            row = col
            if vi != vj:
                row ^= (1 << bi) | (1 << bj)
            mat[row][col] = 1 + 0j
        return mat

    H_gate = [[1 / math.sqrt(2) + 0j, 1 / math.sqrt(2) + 0j], [1 / math.sqrt(2) + 0j, -1 / math.sqrt(2) + 0j]]
    gates = [
        single_qubit_op(H_gate, 0),
        ctrl_rk_op(1, 0, 2),
        ctrl_rk_op(2, 0, 3),
        single_qubit_op(H_gate, 1),
        ctrl_rk_op(2, 1, 2),
        single_qubit_op(H_gate, 2),
        swap_op(0, 2),
    ]
    U_circ = [[1 + 0j if i == j else 0j for j in range(8)] for i in range(8)]
    for g in gates:
        U_circ = matmul(g, U_circ)

    F_exact = [[cmath.exp(2j * math.pi * x * y / 8.0) / math.sqrt(8.0) for x in range(8)] for y in range(8)]
    max_err = 0.0
    for y in range(8):
        for x in range(8):
            err = abs(U_circ[y][x] - F_exact[y][x])
            max_err = max(max_err, err)
            assert err < TOL

    for x in range(8):
        x2, x1, x0 = (x >> 2) & 1, (x >> 1) & 1, x & 1
        phi_top = 0.5 * x0
        phi_mid = 0.5 * x1 + 0.25 * x0
        phi_bot = 0.5 * x2 + 0.25 * x1 + 0.125 * x0
        f_top = [1 / math.sqrt(2), cmath.exp(2j * math.pi * phi_top) / math.sqrt(2)]
        f_mid = [1 / math.sqrt(2), cmath.exp(2j * math.pi * phi_mid) / math.sqrt(2)]
        f_bot = [1 / math.sqrt(2), cmath.exp(2j * math.pi * phi_bot) / math.sqrt(2)]
        for y in range(8):
            y2, y1, y0 = (y >> 2) & 1, (y >> 1) & 1, y & 1
            assert abs(f_top[y2] * f_mid[y1] * f_bot[y0] - U_circ[y][x]) < TOL

    ys = [174.0, 244.0, 314.0]
    x_wire_l, x_wire_r = 152.0, 738.0
    gw, gh = 46.0, 38.0

    def gate_box(cx: float, cy: float, label: str, cls: str = "gate", sub_txt: str = "") -> str:
        x_b, y_b = cx - gw / 2, cy - gh / 2
        if sub_txt:
            txt = f'<text class="gate-txt ink" x="{cx:.1f}" y="{cy + 5:.1f}" text-anchor="middle">{label}<tspan dy="3" font-size="11">{sub_txt}</tspan></text>'
        else:
            txt = f'<text class="gate-txt ink" x="{cx:.1f}" y="{cy + 6:.1f}" text-anchor="middle">{label}</text>'
        return f'  <rect class="{cls}" x="{x_b:.1f}" y="{y_b:.1f}" width="{gw:.1f}" height="{gh:.1f}" rx="7"/>\n  {txt}'

    def ctrl_gate(cx: float, y_ctrl: float, y_targ: float, sub_txt: str) -> str:
        y_edge = y_targ + gh / 2 if y_ctrl > y_targ else y_targ - gh / 2
        return "\n".join([
            f'  <line class="wire" x1="{cx:.1f}" y1="{y_ctrl:.1f}" x2="{cx:.1f}" y2="{y_edge:.1f}"/>',
            f'  <circle class="ctrl" cx="{cx:.1f}" cy="{y_ctrl:.1f}" r="6.0"/>',
            gate_box(cx, y_targ, "R", "gate-alt", sub_txt),
        ])

    def swap_gate(cx: float, y_top: float, y_bot: float) -> str:
        d = 9.0
        return "\n".join([
            f'  <line class="wire" x1="{cx:.1f}" y1="{y_top:.1f}" x2="{cx:.1f}" y2="{y_bot:.1f}"/>',
            f'  <line class="wire" style="stroke-width:2.6" x1="{cx - d:.1f}" y1="{y_top - d:.1f}" x2="{cx + d:.1f}" y2="{y_top + d:.1f}"/>',
            f'  <line class="wire" style="stroke-width:2.6" x1="{cx - d:.1f}" y1="{y_top + d:.1f}" x2="{cx + d:.1f}" y2="{y_top - d:.1f}"/>',
            f'  <line class="wire" style="stroke-width:2.6" x1="{cx - d:.1f}" y1="{y_bot - d:.1f}" x2="{cx + d:.1f}" y2="{y_bot + d:.1f}"/>',
            f'  <line class="wire" style="stroke-width:2.6" x1="{cx - d:.1f}" y1="{y_bot + d:.1f}" x2="{cx + d:.1f}" y2="{y_bot - d:.1f}"/>',
        ])

    parts = [
        '  <text class="title ink" x="38" y="52">3 比特量子傅里叶变换（QFT₃）完整量子线路与相位分解</text>',
        '  <text class="subtitle muted" x="38" y="76">大端序 |x⟩ = |x₂x₁x₀⟩（x = 4x₂ + 2x₁ + x₀）；时间自左向右（非等比例门时长），末尾 SWAP 校正高低位反转</text>',
        '  <rect class="card" x="36" y="94" width="928" height="278" rx="12"/>',
        '  <line class="axis" x1="772" y1="116" x2="934" y2="116"/>',
        f'  <path class="axishead" d="{arrow_poly(772, 116, 934, 116, 9, 5.5)}"/>',
        '  <text class="sm muted" x="850" y="110" text-anchor="middle">时间从左向右</text>',
    ]

    for sx in (410, 568, 658):
        parts.append(f'  <line class="divider" x1="{sx}" y1="138" x2="{sx}" y2="342"/>')
    parts.append('  <text class="sm accent" x="288" y="132" text-anchor="middle">阶段 ①：构造 q₂ 相位</text>')
    parts.append('  <text class="sm accent" x="490" y="132" text-anchor="middle">阶段 ②：构造 q₁</text>')
    parts.append('  <text class="sm accent" x="614" y="132" text-anchor="middle">阶段 ③</text>')
    parts.append('  <text class="sm purple" x="702" y="132" text-anchor="middle">SWAP 反转</text>')

    for lbl, wy in (("q₂ (高位) |x₂⟩", ys[0]), ("q₁ (中位) |x₁⟩", ys[1]), ("q₀ (低位) |x₀⟩", ys[2])):
        parts.append(f'  <line class="wire" x1="{x_wire_l:.1f}" y1="{wy:.1f}" x2="{x_wire_r:.1f}" y2="{wy:.1f}"/>')
        parts.append(f'  <text class="lbl ink" x="50" y="{wy + 5:.1f}">{esc(lbl)}</text>')

    parts.append(gate_box(204, ys[0], "H"))
    parts.append(ctrl_gate(286, ys[1], ys[0], "2"))
    parts.append(ctrl_gate(366, ys[2], ys[0], "3"))
    parts.append(gate_box(454, ys[1], "H"))
    parts.append(ctrl_gate(528, ys[2], ys[1], "2"))
    parts.append(gate_box(614, ys[2], "H"))
    parts.append(swap_gate(702, ys[0], ys[2]))

    for wy, pre, sup_txt, post in (
        (ys[0], "(|0⟩ + e", "2πi·0.x₀", "|1⟩)/√2"),
        (ys[1], "(|0⟩ + e", "2πi·0.x₁x₀", "|1⟩)/√2"),
        (ys[2], "(|0⟩ + e", "2πi·0.x₂x₁x₀", "|1⟩)/√2"),
    ):
        parts.append(
            f'  <text class="lbl ink" x="752" y="{wy + 5:.1f}">'
            f'{esc(pre)}<tspan dy="-6" font-size="11">{esc(sup_txt)}</tspan>'
            f'<tspan dy="6">{esc(post)}</tspan></text>'
        )

    parts.append(
        '  <text class="sm muted" x="50" y="358">'
        '符号说明：● = 控制端（仅 |1⟩ 触发）  |  [H] = Hadamard 门  |  [Rₖ] = 受控相位门  |  ×—× = 正向末尾的 SWAP'
        '</text>'
    )

    parts.append('  <rect class="card" x="36" y="386" width="298" height="134" rx="12"/>')
    parts.append('  <text class="h2 ink" x="50" y="411">受控相位门 Rₖ 定义（相位单位：rad）</text>')
    parts.append(f'  <text class="mono accent" x="50" y="437">Rₖ = diag(1, e{sup("2πi/2ᵏ", 10)})</text>')
    parts.append('  <text class="mono ink" x="50" y="461">R₂ = diag(1, i) = S（φ = π/2 rad）</text>')
    parts.append(f'  <text class="mono ink" x="50" y="484">R₃ = diag(1, e{sup("iπ/4", 10)}) = T（φ = π/4 rad）</text>')
    parts.append('  <text class="sm muted" x="50" y="507">受控 Rₖ 为对角门，控制端与目标端数学对称</text>')

    parts.append('  <rect class="card" x="346" y="386" width="304" height="134" rx="12"/>')
    parts.append('  <text class="h2 ink" x="360" y="411">二进制小数相位与整体变换</text>')
    parts.append('  <text class="mono ink" x="360" y="437">0.x₂x₁x₀ := x₂/2 + x₁/4 + x₀/8</text>')
    parts.append(f'  <text class="mono accent" x="360" y="461">QFT₈|x⟩ = (1/√8) ∑ᵧ e{sup("2πixy/8", 10)}|y⟩</text>')
    parts.append('  <text class="sm ink" x="360" y="485">逆 QFT 按倒序执行：先 SWAP，Rₖ 取共轭</text>')
    parts.append('  <text class="sm muted" x="360" y="507">QPE 省逆 QFT 的 SWAP 时须反接受控幂</text>')

    parts.append('  <rect class="card" x="662" y="386" width="302" height="134" rx="12"/>')
    parts.append('  <text class="h2 ink" x="676" y="411">门开销与精确核验</text>')
    parts.append('  <text class="sm ink" x="676" y="437">n = 3 精确门数：3 H + 3 CRₖ + 1 SWAP</text>')
    parts.append('  <text class="sm ink" x="676" y="461">一般 n 位：n(n+1)/2 门，另含 ⌊n/2⌋ 个 SWAP</text>')
    parts.append('  <text class="sm muted" x="676" y="485">有限硬件门集合成小角度旋转门数另计</text>')
    parts.append('  <text class="sm green" x="676" y="507">8×8 酉矩阵已逐元素核验（误差 &lt; 10⁻¹²）</text>')

    parts.append(
        '  <text class="sm muted" x="38" y="544">'
        '注：图示是正向 QFT。去掉末尾 SWAP 会倒序输出。逆 QFT 的 SWAP 在入口，QPE 须同时调整输入接线。'
        '</text>'
    )

    svg = wrap_svg(
        "v2-06-qft-circuit",
        "3 比特量子傅里叶变换（QFT₃）完整量子线路图",
        "展示大端序 3 比特 QFT 线路：依次在 q₂、q₁、q₀ 上施加 H 门与受控相位门 R₂、R₃，末尾通过 SWAP 反转高低位，附相位门定义与门复杂度说明。",
        "\n".join(parts),
    )
    return svg, {"qft8_max_matrix_error": max_err, "gates": {"H": 3, "CRk": 3, "SWAP": 1}}


# ===========================================================================
# Figure 4: v2-07-shor-hhl-pipeline.svg
# ===========================================================================
def build_fig4_shor_hhl_pipeline() -> tuple[str, dict]:
    N, a, Q = 15, 2, 16
    fx = [pow(a, x, N) for x in range(Q)]
    assert fx == [1, 2, 4, 8] * 4
    r = next(k for k in range(1, Q) if pow(a, k, N) == 1)
    assert r == 4

    probs = [0.0] * Q
    for x0 in range(r):
        xs = [x for x in range(Q) if fx[x] == fx[x0]]
        assert len(xs) == Q // r
        for y in range(Q):
            amp = sum(cmath.exp(2j * math.pi * x * y / Q) for x in xs) / math.sqrt(Q * len(xs))
            probs[y] += (abs(amp) ** 2) / r
    assert abs(sum(probs) - 1.0) < TOL
    peaks = [y for y, p in enumerate(probs) if p > 1e-6]
    assert peaks == [0, 4, 8, 12]
    for y in range(Q):
        expected = 0.25 if y in (0, 4, 8, 12) else 0.0
        assert abs(probs[y] - expected) < TOL
    f1, f2 = math.gcd(pow(a, r // 2) - 1, N), math.gcd(pow(a, r // 2) + 1, N)
    assert {f1, f2} == {3, 5}

    # Concrete 2x2 HHL check: A = diag(1, 2), |b> = |+>, C = 1
    lambdas = [1.0, 2.0]
    betas = [1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0)]
    C_hhl = 1.0
    anc1_amps = [b * (C_hhl / lam) for b, lam in zip(betas, lambdas)]
    p_success_hhl = sum(a_j ** 2 for a_j in anc1_amps)
    assert abs(p_success_hhl - 5.0 / 8.0) < TOL
    x_norm = [a_j / math.sqrt(p_success_hhl) for a_j in anc1_amps]
    assert abs(x_norm[0] - 2.0 / math.sqrt(5.0)) < TOL and abs(x_norm[1] - 1.0 / math.sqrt(5.0)) < TOL
    ax = [lam * xi for lam, xi in zip(lambdas, x_norm)]
    assert abs(ax[0] - ax[1]) < TOL

    lam_j = f"λ{sub('j')}"
    lam_tilde_j = f'<tspan font-family="\'STIX Two Math\',\'Cambria Math\',\'Times New Roman\',serif">λ\u0303</tspan>{sub("j")}'
    uj = f"u{sub('j')}"
    bet_j = f"β{sub('j')}"
    th_j = f"θ{sub('j')}"
    ry_lbl = f"R{sub('y')}"
    ket0t = f"|0⟩{sup('⊗t')}"

    defs = (
        '    <pattern id="hatch-muted" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">\n'
        '      <rect width="6" height="6" fill="#dbe6ef" class="hatch-bg"/>\n'
        '      <line x1="0" y1="0" x2="0" y2="6" stroke="#4f6c84" stroke-width="2.2" class="hatch-ln"/>\n'
        '    </pattern>'
    )
    extra_dark = ".hatch-bg{fill:#26394a}.hatch-ln{stroke:#9db8ce}"

    parts = [
        '  <text class="title ink" x="38" y="52">相位估计驱动的两大算法骨架：Shor 周期提取与 HHL 三阶段解态制备</text>',
        '  <text class="subtitle muted" x="38" y="76">左：Shor 找阶（N = 15, a = 2, Q = 16 教学网格的精确周期与 QFT 频谱）；右：HHL 线性方程求解三阶段电路骨架</text>',
    ]

    # ======================= LEFT PANEL: SHOR =======================
    lx, ly, lw, lh = 36, 94, 452, 426
    parts.append(f'  <rect class="card" x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{lx + 16}" y="{ly + 24}">（左）Shor 找阶：N = 15, a = 2 周期序列与 QFT 峰位</text>')

    # Sub-plot 1: f(x) = 2^x mod 15
    p1_x0, p1_x1 = lx + 56.0, lx + 432.0
    p1_y0, p1_y1 = ly + 152.0, ly + 56.0
    dx = (p1_x1 - p1_x0) / 15.0

    def map_p1(x_val: float, y_val: float) -> tuple[float, float]:
        return p1_x0 + x_val * dx, p1_y0 - (y_val / 10.6) * (p1_y0 - p1_y1)

    bx0, _ = map_p1(-0.32, 0)
    bx1, _ = map_p1(3.32, 0)
    parts.append(f'  <rect class="subcard" x="{bx0:.1f}" y="{p1_y1:.1f}" width="{bx1 - bx0:.1f}" height="{p1_y0 - p1_y1:.1f}" rx="4"/>')
    parts.append(f'  <text class="sm accent" x="{(bx0 + bx1) / 2:.1f}" y="{p1_y1 + 14:.1f}" text-anchor="middle">周期 r = 4</text>')

    for yv in (2, 4, 8):
        _, gy = map_p1(0, yv)
        parts.append(f'  <line class="grid" x1="{p1_x0:.1f}" y1="{gy:.1f}" x2="{p1_x1:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <text class="sm muted" x="{p1_x0 - 8:.1f}" y="{gy + 4:.1f}" text-anchor="end">{yv}</text>')
    parts.append(f'  <text class="sm muted" x="{p1_x0 - 8:.1f}" y="{p1_y0 + 4:.1f}" text-anchor="end">0</text>')

    parts.append(f'  <line class="axis" x1="{p1_x0:.1f}" y1="{p1_y0:.1f}" x2="{p1_x1 + 8:.1f}" y2="{p1_y0:.1f}"/>')
    parts.append(f'  <line class="axis" x1="{p1_x0:.1f}" y1="{p1_y0:.1f}" x2="{p1_x0:.1f}" y2="{p1_y1 - 8:.1f}"/>')
    parts.append(f'  <text class="sm ink" x="{p1_x0 + 6:.1f}" y="{p1_y1 - 10:.1f}">f(x) = 2ˣ mod 15（整数值）</text>')

    poly_pts = []
    for x, val in enumerate(fx):
        px, py = map_p1(x, val)
        poly_pts.append(f"{px:.1f},{py:.1f}")
        parts.append(f'  <line class="vec-a" style="stroke-width:1.4;opacity:0.55" x1="{px:.1f}" y1="{p1_y0:.1f}" x2="{px:.1f}" y2="{py:.1f}"/>')
    parts.append(f'  <polyline class="vec-a" style="stroke-width:1.8" points="{" ".join(poly_pts)}"/>')
    for x, val in enumerate(fx):
        px, py = map_p1(x, val)
        cls_dot = "vec-a-head" if x < 4 else "axishead"
        parts.append(f'  <circle class="{cls_dot}" cx="{px:.1f}" cy="{py:.1f}" r="3.6"/>')
        if x < 4:
            lx_v = px + 8 if x == 0 else px
            parts.append(f'  <text class="mono accent" x="{lx_v:.1f}" y="{py - 7:.1f}" text-anchor="middle">{val}</text>')

    for xt in (0, 4, 8, 12, 15):
        px, _ = map_p1(xt, 0)
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{px:.1f}" y1="{p1_y0:.1f}" x2="{px:.1f}" y2="{p1_y0 + 4:.1f}"/>')
        parts.append(f'  <text class="sm muted" x="{px:.1f}" y="{p1_y0 + 18:.1f}" text-anchor="middle">{xt}</text>')
    parts.append(f'  <text class="sm muted" x="{(p1_x0 + p1_x1) / 2:.1f}" y="{p1_y0 + 38:.1f}" text-anchor="middle">输入指数 x（整数，0–15）</text>')

    # Sub-plot 2: QFT probability P(y)
    p2_y0, p2_y1 = ly + 346.0, ly + 244.0

    def map_p2(y_idx: float, prob_val: float) -> tuple[float, float]:
        return p1_x0 + y_idx * dx, p2_y0 - (prob_val / 0.32) * (p2_y0 - p2_y1)

    _, gy25 = map_p2(0, 0.25)
    parts.append(f'  <line class="grid" x1="{p1_x0:.1f}" y1="{gy25:.1f}" x2="{p1_x1:.1f}" y2="{gy25:.1f}"/>')
    parts.append(f'  <text class="sm muted" x="{p1_x0 - 8:.1f}" y="{gy25 + 4:.1f}" text-anchor="end">0.25</text>')
    parts.append(f'  <text class="sm muted" x="{p1_x0 - 8:.1f}" y="{p2_y0 + 4:.1f}" text-anchor="end">0</text>')
    parts.append(f'  <line class="axis" x1="{p1_x0:.1f}" y1="{p2_y0:.1f}" x2="{p1_x1 + 8:.1f}" y2="{p2_y0:.1f}"/>')
    parts.append(f'  <line class="axis" x1="{p1_x0:.1f}" y1="{p2_y0:.1f}" x2="{p1_x0:.1f}" y2="{p2_y1 - 8:.1f}"/>')
    parts.append(f'  <text class="sm ink" x="{p1_x0 + 6:.1f}" y="{p2_y1 - 10:.1f}">QFT 测量概率 P(y)（Q = 16，无量纲）</text>')

    bar_w = 14.0
    for y_idx, p_val in enumerate(probs):
        px, py = map_p2(y_idx, p_val)
        if p_val > 1e-6:
            bh = p2_y0 - py
            if y_idx in (4, 12):
                parts.append(f'  <rect class="vec-a-head" x="{px - bar_w / 2:.1f}" y="{py:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="2"/>')
                lbl = "1/4 ★" if y_idx == 4 else "3/4 ★"
                parts.append(f'  <text class="sm accent" x="{px:.1f}" y="{py - 7:.1f}" text-anchor="middle">{lbl}</text>')
            else:
                parts.append(f'  <rect style="fill:url(#hatch-muted)" class="axis" x="{px - bar_w / 2:.1f}" y="{py:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="2"/>')
                if y_idx == 0:
                    parts.append(f'  <text class="sm muted" x="{px + 26:.1f}" y="{py - 7:.1f}" text-anchor="middle">0 (平凡)</text>')
                else:
                    parts.append(f'  <text class="sm muted" x="{px:.1f}" y="{py - 7:.1f}" text-anchor="middle">1/2 (约分)</text>')
        else:
            parts.append(f'  <circle class="muted" cx="{px:.1f}" cy="{p2_y0 - 2:.1f}" r="1.6"/>')

    for yt in (0, 4, 8, 12, 15):
        px, _ = map_p2(yt, 0)
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{px:.1f}" y1="{p2_y0:.1f}" x2="{px:.1f}" y2="{p2_y0 + 4:.1f}"/>')
        parts.append(f'  <text class="sm muted" x="{px:.1f}" y="{p2_y0 + 18:.1f}" text-anchor="middle">{yt}</text>')
    parts.append(f'  <text class="sm muted" x="{(p1_x0 + p1_x1) / 2:.1f}" y="{p2_y0 + 38:.1f}" text-anchor="middle">QFT 读出整数 y（峰位 0, 4, 8, 12，间隔 Q/r = 4）</text>')

    parts.append(f'  <rect class="subcard" x="{lx + 14}" y="{ly + 394}" width="{lw - 28}" height="24" rx="6"/>')
    parts.append(
        f'  <text class="sm ink" x="{lx + lw / 2:.1f}" y="{ly + 411}" text-anchor="middle">'
        '★ 实心柱直出 r = 4（单次 50%）→ gcd(2²±1, 15) = 3, 5'
        '</text>'
    )

    # ======================= RIGHT PANEL: HHL =======================
    rx, ry, rw, rh = 504, 94, 460, 426
    parts.append(f'  <rect class="card" x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{rx + 16}" y="{ry + 24}">（右）HHL 三阶段骨架：制备解态 |x⟩ ∝ A⁻¹|b⟩</text>')
    parts.append(f'  <text class="sm muted" x="{rx + 16}" y="{ry + 44}">厄米矩阵 A = ∑ {lam_j}|{uj}⟩⟨{uj}|，输入 |b⟩ = ∑ {bet_j}|{uj}⟩</text>')

    parts.append(f'  <line class="axis" x1="{rx + 332}" y1="{ry + 58}" x2="{rx + 442}" y2="{ry + 58}"/>')
    parts.append(f'  <path class="axishead" d="{arrow_poly(rx + 332, ry + 58, rx + 442, ry + 58, 8, 5)}"/>')
    parts.append(f'  <text class="sm muted" x="{rx + 382}" y="{ry + 52}" text-anchor="middle">时间 →</text>')

    wy_anc, wy_ph, wy_sys = ry + 95.0, ry + 154.0, ry + 210.0
    wx_l, wx_r = rx + 84.0, rx + 402.0

    for rlbl, wy in (("辅助 |0⟩", wy_anc), (f"相位 {ket0t}", wy_ph), ("系统 |b⟩", wy_sys)):
        parts.append(f'  <line class="wire" x1="{wx_l:.1f}" y1="{wy:.1f}" x2="{wx_r:.1f}" y2="{wy:.1f}"/>')
        parts.append(f'  <text class="sm ink" x="{rx + 14}" y="{wy + 4:.1f}">{rlbl}</text>')

    parts.append(f'  <line class="wire" style="stroke-width:1.6" x1="{wx_l + 10:.1f}" y1="{wy_ph + 6:.1f}" x2="{wx_l + 18:.1f}" y2="{wy_ph - 6:.1f}"/>')

    # Stage 1: QPE
    qpe1_x, qpe_w = rx + 108.0, 74.0
    parts.append(f'  <rect class="gate" x="{qpe1_x:.1f}" y="{wy_ph - 22:.1f}" width="{qpe_w:.1f}" height="{(wy_sys - wy_ph) + 44:.1f}" rx="8"/>')
    parts.append(f'  <text class="lbl ink" x="{qpe1_x + qpe_w / 2:.1f}" y="{(wy_ph + wy_sys) / 2 - 5:.1f}" text-anchor="middle">① QPE</text>')
    parts.append(f'  <text class="sm muted" x="{qpe1_x + qpe_w / 2:.1f}" y="{(wy_ph + wy_sys) / 2 + 16:.1f}" text-anchor="middle">读 |{lam_tilde_j}⟩</text>')

    # Stage 2: Controlled-Ry (taller box so two lines have clean breathing room)
    ry_cx = rx + 238.0
    parts.append(f'  <line class="wire" x1="{ry_cx:.1f}" y1="{wy_ph:.1f}" x2="{ry_cx:.1f}" y2="{wy_anc + 25:.1f}"/>')
    parts.append(f'  <circle class="ctrl" cx="{ry_cx:.1f}" cy="{wy_ph:.1f}" r="6.0"/>')
    parts.append(f'  <rect class="gate-alt" x="{ry_cx - 42:.1f}" y="{wy_anc - 25:.1f}" width="84" height="50" rx="8"/>')
    parts.append(f'  <text class="lbl ink" x="{ry_cx:.1f}" y="{wy_anc - 5:.1f}" text-anchor="middle">② {ry_lbl}({th_j})</text>')
    parts.append(f'  <text class="sm muted" x="{ry_cx:.1f}" y="{wy_anc + 16:.1f}" text-anchor="middle">写 C/{lam_j}</text>')

    # Stage 3: Inverse QPE
    qpe2_x = rx + 294.0
    parts.append(f'  <rect class="gate-inv" x="{qpe2_x:.1f}" y="{wy_ph - 22:.1f}" width="{qpe_w:.1f}" height="{(wy_sys - wy_ph) + 44:.1f}" rx="8"/>')
    parts.append(f'  <text class="lbl ink" x="{qpe2_x + qpe_w / 2:.1f}" y="{(wy_ph + wy_sys) / 2 - 5:.1f}" text-anchor="middle">③ QPE†</text>')
    parts.append(f'  <text class="sm muted" x="{qpe2_x + qpe_w / 2:.1f}" y="{(wy_ph + wy_sys) / 2 + 16:.1f}" text-anchor="middle">反计算</text>')

    # Measurement on ancilla
    mx_box = rx + 382.0
    parts.append(f'  <rect class="subcard" x="{mx_box:.1f}" y="{wy_anc - 18:.1f}" width="36" height="36" rx="6"/>')
    parts.append(f'  <path class="axis" style="stroke-width:1.6" d="M{mx_box + 6:.1f} {wy_anc + 8:.1f}A12 12 0 0 1 {mx_box + 30:.1f} {wy_anc + 8:.1f}"/>')
    parts.append(f'  <line class="axis" style="stroke-width:1.6" x1="{mx_box + 18:.1f}" y1="{wy_anc + 8:.1f}" x2="{mx_box + 26:.1f}" y2="{wy_anc - 6:.1f}"/>')
    parts.append(f'  <text class="sm warn" x="{mx_box + 42:.1f}" y="{wy_anc + 4:.1f}">=1</text>')

    parts.append(f'  <text class="sm muted" x="{wx_r + 6:.1f}" y="{wy_ph + 4:.1f}">{ket0t}</text>')
    parts.append(f'  <text class="lbl green" x="{wx_r + 6:.1f}" y="{wy_sys + 4:.1f}">|x⟩</text>')

    # Stage summary strips (50px tall, 24px baseline separation -> 0 bbox touch)
    strips = [
        ("① QPE 读特征值（线序：辅助—相位—系统）", f"∑ {bet_j}|0⟩{ket0t}|{uj}⟩  →  ∑ {bet_j}|0⟩|{lam_tilde_j}⟩|{uj}⟩", "gate", ry + 242),
        (f"② 受控 {ry_lbl} 编码倒数", f"{th_j} = 2 arcsin(C/{lam_j})，辅助位 |1⟩ 振幅写入 C/{lam_j}", "gate-alt", ry + 300),
        ("③ 逆 QPE 反计算并后选择", f"相位位归 {ket0t} 解除纠缠；测得辅助=1 得 |x⟩ ∝ ∑({bet_j}/{lam_j})|{uj}⟩", "gate-inv", ry + 358),
    ]
    for st_title, st_eq, badge_cls, sy_top in strips:
        parts.append(f'  <rect class="subcard" x="{rx + 14}" y="{sy_top}" width="{rw - 28}" height="52" rx="8"/>')
        parts.append(f'  <rect class="{badge_cls}" x="{rx + 22}" y="{sy_top + 10}" width="6" height="32" rx="3"/>')
        parts.append(f'  <text class="lbl ink" x="{rx + 36}" y="{sy_top + 19}">{st_title}</text>')
        parts.append(f'  <text class="sm muted" x="{rx + 36}" y="{sy_top + 43}">{st_eq}</text>')

    parts.append(
        f'  <text class="sm muted" x="38" y="541">'
        f'注：左图 Q=16 仅作整除教学示意（实用需 Q ≥ N² 并配连分数）；右图 0 &lt; C ≤ min|{lam_j}|，输出为量子解态而非经典全向量清单。'
        '</text>'
    )

    svg = wrap_svg(
        "v2-07-shor-hhl-pipeline",
        "Shor 周期提取（N=15, a=2, Q=16）与 HHL 三阶段解态制备骨架",
        "左半图精确绘制 f(x)=2^x mod 15 的周期序列(1,2,4,8，r=4)及 Q=16 下的 QFT 峰位(0,4,8,12)；右半图绘制 HHL 的 QPE、受控 R_y 编码 C/λ_j 与逆 QPE 反计算三阶段线路骨架。",
        "\n".join(parts),
        extra_dark=extra_dark,
        defs=defs,
    )
    return svg, {"shor_period": r, "shor_peaks": peaks, "hhl_demo_p_success": p_success_hhl}


# ===========================================================================
# Figure 5: v2-08-qaoa-maxcut.svg
# ===========================================================================
def build_fig5_qaoa_maxcut() -> tuple[str, dict]:
    edges = [(0, 1), (1, 2)]

    def cut_value(bitstring: int) -> int:
        bits = [(bitstring >> 2) & 1, (bitstring >> 1) & 1, bitstring & 1]
        return sum(1 for u, v in edges if bits[u] != bits[v])

    cuts = [cut_value(x) for x in range(8)]
    assert max(cuts) == 2
    opt_states = [x for x, c in enumerate(cuts) if c == 2]
    assert opt_states == [0b010, 0b101]

    def qaoa_statevector(gamma: float, beta: float) -> list[complex]:
        inv_sqrt8 = 1.0 / math.sqrt(8.0)
        psi = [inv_sqrt8 + 0j] * 8
        for x in range(8):
            psi[x] *= cmath.exp(-1j * gamma * cuts[x])
        cb, sb = math.cos(beta), math.sin(beta)
        for q_bit in (2, 1, 0):
            step = 1 << q_bit
            new_psi = [0j] * 8
            for x in range(8):
                if (x & step) == 0:
                    a0, a1 = psi[x], psi[x | step]
                    new_psi[x] = cb * a0 - 1j * sb * a1
                    new_psi[x | step] = -1j * sb * a0 + cb * a1
            psi = new_psi
        assert abs(sum(abs(amp) ** 2 for amp in psi) - 1.0) < TOL
        return psi

    def expected_cut(gamma: float, beta: float) -> float:
        psi = qaoa_statevector(gamma, beta)
        val = sum(cuts[x] * (abs(psi[x]) ** 2) for x in range(8))
        analytic = 1.0 + 0.5 * math.sin(4.0 * beta) * math.sin(gamma) * (1.0 + math.cos(gamma))
        assert abs(val - analytic) < TOL
        return val

    gamma_opt, beta_opt = math.pi / 3.0, math.pi / 8.0
    max_exp = expected_cut(gamma_opt, beta_opt)
    exact_max = 1.0 + 3.0 * math.sqrt(3.0) / 8.0
    assert abs(max_exp - exact_max) < TOL
    approx_ratio = max_exp / 2.0
    assert abs(max_exp - 1.649519052838329) < 1e-9
    assert abs(approx_ratio - 0.8247595264191645) < 1e-9

    psi_opt = qaoa_statevector(gamma_opt, beta_opt)
    p_opt_strings = sum(abs(psi_opt[x]) ** 2 for x in opt_states)

    min_exp = expected_cut(math.pi / 3.0, 3.0 * math.pi / 8.0)
    assert abs(min_exp - (1.0 - 3.0 * math.sqrt(3.0) / 8.0)) < TOL

    stops = [
        (0.00, (25, 42, 74)),
        (0.25, (38, 92, 138)),
        (0.50, (44, 146, 142)),
        (0.75, (124, 184, 104)),
        (0.92, (238, 192, 78)),
        (1.00, (254, 241, 166)),
    ]

    def color_for_val(v: float, vmin: float = 0.35, vmax: float = 1.65) -> str:
        t = max(0.0, min(1.0, (v - vmin) / (vmax - vmin)))
        for idx in range(len(stops) - 1):
            t0, c0 = stops[idx]
            t1, c1 = stops[idx + 1]
            if t <= t1 or idx == len(stops) - 2:
                u = 0.0 if t1 == t0 else (t - t0) / (t1 - t0)
                r = round(c0[0] + u * (c1[0] - c0[0]))
                g = round(c0[1] + u * (c1[1] - c0[1]))
                b = round(c0[2] + u * (c1[2] - c0[2]))
                return f"#{r:02x}{g:02x}{b:02x}"
        return "#fef1a6"

    nx, ny = 36, 24
    grid_vals = []
    grid_max = -1.0
    for j in range(ny):
        beta_c = (j + 0.5) * (math.pi / 2.0) / ny
        row_vals = []
        for i in range(nx):
            gamma_c = (i + 0.5) * math.pi / nx
            val = expected_cut(gamma_c, beta_c)
            grid_max = max(grid_max, val)
            row_vals.append(val)
        grid_vals.append(row_vals)
    assert grid_max <= max_exp + TOL

    uc_s = f"U{sub('C')}"
    ub_s = f"U{sub('B')}"
    cmax_s = f"C{sub('max')}"
    ecmax_s = f"⟨C⟩{sub('max')}"

    parts = [
        '  <text class="title ink" x="38" y="52">3 顶点路径图 MaxCut 与 p = 1 QAOA 期望割值景观</text>',
        '  <text class="subtitle muted" x="38" y="76">左：路径图 0–1–2 及其最大割（割值 2）；右：3 比特态矢量精确计算 ⟨C(γ, β)⟩ 热力图（含等值线，黑白可读）</text>',
    ]

    # ======================= LEFT PANEL: PATH GRAPH =======================
    lx, ly, lw, lh = 36, 94, 366, 426
    parts.append(f'  <rect class="card" x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{lx + 16}" y="{ly + 25}">（左）3 顶点路径图与最大割（割值 = 2）</text>')

    vy = 206.0
    vx0, vx1, vx2 = 96.0, 219.0, 342.0
    parts.append(f'  <line class="wire" style="stroke-width:3.2" x1="{vx0:.1f}" y1="{vy:.1f}" x2="{vx1:.1f}" y2="{vy:.1f}"/>')
    parts.append(f'  <line class="wire" style="stroke-width:3.2" x1="{vx1:.1f}" y1="{vy:.1f}" x2="{vx2:.1f}" y2="{vy:.1f}"/>')
    parts.append('  <path class="vec-b" style="stroke-width:2.4;stroke-dasharray:6 4" d="M158 256 C158 142, 280 142, 280 256"/>')
    parts.append('  <text class="sm warn" x="148" y="188" text-anchor="end">割 +1</text>')
    parts.append('  <text class="sm warn" x="290" y="188">割 +1</text>')

    for cx_n, idx_lbl in ((vx0, "0"), (vx2, "2")):
        parts.append(f'  <circle class="node-a" cx="{cx_n:.1f}" cy="{vy:.1f}" r="22"/>')
        parts.append(f'  <text class="gate-txt node-a-txt" x="{cx_n:.1f}" y="{vy + 6:.1f}" text-anchor="middle">{idx_lbl}</text>')
        parts.append(f'  <text class="sm accent" x="{cx_n:.1f}" y="{vy + 42:.1f}" text-anchor="middle">组 A (0)</text>')

    parts.append(f'  <circle class="gate-alt" style="stroke-width:3" cx="{vx1:.1f}" cy="{vy:.1f}" r="22"/>')
    parts.append(f'  <circle style="fill:none;stroke-width:1.4" class="gate-alt" cx="{vx1:.1f}" cy="{vy:.1f}" r="16"/>')
    parts.append(f'  <text class="gate-txt ink" x="{vx1:.1f}" y="{vy + 6:.1f}" text-anchor="middle">1</text>')
    parts.append(f'  <text class="sm gold" x="{vx1:.1f}" y="{vy + 42:.1f}" text-anchor="middle">组 B (1)</text>')

    parts.append('  <text class="sm muted" x="219" y="274" text-anchor="middle">● 实心 = 组 A(0)   ◎ 双圈 = 组 B(1)   ┄ 虚线 = 割边</text>')

    parts.append(f'  <rect class="subcard" x="{lx + 14}" y="292" width="{lw - 28}" height="214" rx="10"/>')
    parts.append(f'  <text class="h2 ink" x="{lx + 26}" y="316">p = 1 QAOA 算符与精确数值核对</text>')
    parts.append(f'  <text class="lbl ink" x="{lx + 26}" y="340">C = (I − Z₀Z₁)/2 + (I − Z₁Z₂)/2</text>')
    parts.append(f'  <text class="lbl ink" x="{lx + 26}" y="364">{uc_s} = e{sup("−iγC")},  {ub_s} = e{sup("−iβ(X₀+X₁+X₂)")}</text>')
    parts.append(f'  <line class="divider" x1="{lx + 24}" y1="378" x2="{lx + lw - 24}" y2="378"/>')
    parts.append(f'  <text class="sm ink" x="{lx + 26}" y="400">最优割串：|010⟩, |101⟩（{cmax_s} = 2）</text>')
    parts.append(f'  <text class="sm accent" x="{lx + 26}" y="424">全局最优点：γ* = π/3，β* = π/8</text>')
    parts.append(f'  <text class="lbl ink" x="{lx + 26}" y="448">{ecmax_s} = 1 + 3√3/8 ≈ {max_exp:.4f}</text>')
    parts.append(f'  <text class="lbl green" x="{lx + 26}" y="471">近似比 r = {ecmax_s}/2 ≈ {approx_ratio:.4f}</text>')
    parts.append(f'  <text class="sm muted" x="{lx + 26}" y="494">最优点处最优串概率 P(010)+P(101) ≈ {p_opt_strings:.4f}</text>')

    # ======================= RIGHT PANEL: HEATMAP =======================
    rx, ry, rw, rh = 418, 94, 546, 426
    parts.append(f'  <rect class="card" x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{rx + 16}" y="{ry + 24}">（右）p = 1 QAOA 期望割值热力图 ⟨C(γ, β)⟩</text>')

    # 36 x 24 exact integer-pixel cells (10.0 x 11.0 px -> 360 x 264)
    hm_x, hm_y, hm_w, hm_h = 486.0, 154.0, 360.0, 264.0
    cw, ch_cell = hm_w / nx, hm_h / ny

    for j in range(ny):
        cy_top = hm_y + hm_h - (j + 1) * ch_cell
        h_cell = ch_cell if j == 0 else ch_cell + 0.3
        for i in range(nx):
            cx_left = hm_x + i * cw
            w_cell = cw if i == nx - 1 else cw + 0.3
            fill_hex = color_for_val(grid_vals[j][i])
            parts.append(
                f'  <rect x="{cx_left:.1f}" y="{cy_top:.1f}" width="{w_cell:.1f}" height="{h_cell:.1f}" fill="{fill_hex}"/>'
            )

    def map_hm(gamma_v: float, beta_v: float) -> tuple[float, float]:
        return hm_x + (gamma_v / math.pi) * hm_w, hm_y + hm_h - (beta_v / (math.pi / 2.0)) * hm_h

    def contour_loop(level: float, upper_half: bool) -> str:
        target = 2.0 * (level - 1.0)
        pts_lo, pts_hi = [], []
        for s in range(1, 300):
            g = math.pi * s / 300.0
            denom = math.sin(g) * (1.0 + math.cos(g))
            if denom <= 1e-6:
                continue
            rhs = target / denom
            if abs(rhs) <= 1.0:
                a = math.asin(abs(rhs))
                if not upper_half:
                    b1, b2 = a / 4.0, (math.pi - a) / 4.0
                else:
                    b1, b2 = (math.pi + a) / 4.0, (2.0 * math.pi - a) / 4.0
                pts_lo.append(map_hm(g, b1))
                pts_hi.append(map_hm(g, b2))
        loop = pts_lo + list(reversed(pts_hi))
        assert len(loop) > 20
        cmds = [f'{"M" if k == 0 else "L"}{x:.1f} {y:.1f}' for k, (x, y) in enumerate(loop)]
        cmds.append("Z")
        return "".join(cmds)

    _, y_mid = map_hm(0.0, math.pi / 4.0)
    parts.append(f'  <line x1="{hm_x:.1f}" y1="{y_mid:.1f}" x2="{hm_x + hm_w:.1f}" y2="{y_mid:.1f}" stroke="#ffffff" stroke-width="1.6" stroke-dasharray="6 4"/>')
    parts.append(f'  <rect class="pill" x="{hm_x + hm_w - 134:.1f}" y="{y_mid - 11:.1f}" width="128" height="22" rx="6"/>')
    parts.append(f'  <text class="sm ink" x="{hm_x + hm_w - 70:.1f}" y="{y_mid + 4:.1f}" text-anchor="middle">基线 ⟨C⟩ = 1.0</text>')

    parts.append(f'  <path d="{contour_loop(1.4, False)}" fill="none" stroke="#13263a" stroke-width="1.5" stroke-dasharray="4 3"/>')
    parts.append(f'  <path d="{contour_loop(0.6, True)}" fill="none" stroke="#eef6ff" stroke-width="1.5" stroke-dasharray="4 3"/>')
    c14_x, c14_y = map_hm(0.45 * math.pi, 0.045 * math.pi)
    parts.append(f'  <text class="mono" style="fill:#13263a;font-size:11.5px" x="{c14_x + 4:.1f}" y="{c14_y + 11:.1f}">1.4</text>')
    c06_x, c06_y = map_hm(0.45 * math.pi, 0.455 * math.pi)
    parts.append(f'  <text class="mono" style="fill:#eef6ff;font-size:11.5px" x="{c06_x + 4:.1f}" y="{c06_y - 3:.1f}">0.6</text>')

    parts.append(f'  <rect class="axis" x="{hm_x:.1f}" y="{hm_y:.1f}" width="{hm_w:.1f}" height="{hm_h:.1f}"/>')

    # Global optimum marker at (pi/3, pi/8)
    opt_x, opt_y = map_hm(gamma_opt, beta_opt)
    parts.append(f'  <circle cx="{opt_x:.1f}" cy="{opt_y:.1f}" r="8.5" fill="#ffffff" stroke="#b93c3c" stroke-width="2.6"/>')
    parts.append(f'  <circle cx="{opt_x:.1f}" cy="{opt_y:.1f}" r="3.2" fill="#b93c3c"/>')
    call_x, call_y = 664.0, opt_y - 24.0
    parts.append(f'  <line x1="{opt_x + 9:.1f}" y1="{opt_y:.1f}" x2="{call_x:.1f}" y2="{opt_y:.1f}" stroke="#13263a" stroke-width="1.8"/>')
    parts.append(f'  <rect class="pill" x="{call_x:.1f}" y="{call_y:.1f}" width="174" height="48" rx="8"/>')
    parts.append(f'  <text class="sm warn" style="font-weight:700" x="{call_x + 10:.1f}" y="{call_y + 19:.1f}">★ 最优 (π/3, π/8)</text>')
    parts.append(f'  <text class="mono ink" x="{call_x + 10:.1f}" y="{call_y + 39:.1f}">⟨C⟩=1.6495 (r=0.8248)</text>')

    # Global minimum marker at (pi/3, 3*pi/8)
    min_x, min_y = map_hm(math.pi / 3.0, 3.0 * math.pi / 8.0)
    parts.append(f'  <circle cx="{min_x:.1f}" cy="{min_y:.1f}" r="6.0" fill="none" stroke="#ffffff" stroke-width="2.2"/>')
    parts.append(f'  <rect class="pill" x="{min_x + 36:.1f}" y="{min_y - 12:.1f}" width="122" height="24" rx="6"/>')
    parts.append(f'  <line x1="{min_x + 7:.1f}" y1="{min_y:.1f}" x2="{min_x + 36:.1f}" y2="{min_y:.1f}" stroke="#eef6ff" stroke-width="1.5"/>')
    parts.append(f'  <text class="sm ink" x="{min_x + 44:.1f}" y="{min_y + 4:.1f}">○ 极小 0.3505</text>')

    # X-axis ticks & label
    for g_val, lbl in ((0.0, "0"), (math.pi / 3.0, "π/3"), (math.pi / 2.0, "π/2"), (2.0 * math.pi / 3.0, "2π/3"), (math.pi, "π")):
        tx, _ = map_hm(g_val, 0.0)
        parts.append(f'  <line class="axis" style="stroke-width:1.4" x1="{tx:.1f}" y1="{hm_y + hm_h:.1f}" x2="{tx:.1f}" y2="{hm_y + hm_h + 5:.1f}"/>')
        parts.append(f'  <text class="sm ink" x="{tx:.1f}" y="{hm_y + hm_h + 22:.1f}" text-anchor="middle">{lbl}</text>')
    parts.append(f'  <text class="lbl ink" x="{hm_x + hm_w / 2:.1f}" y="{hm_y + hm_h + 48:.1f}" text-anchor="middle">代价层角 γ（弧度, rad）</text>')

    # Y-axis ticks & label
    for b_val, lbl in ((0.0, "0"), (math.pi / 8.0, "π/8"), (math.pi / 4.0, "π/4"), (3.0 * math.pi / 8.0, "3π/8"), (math.pi / 2.0, "π/2")):
        _, ty = map_hm(0.0, b_val)
        parts.append(f'  <line class="axis" style="stroke-width:1.4" x1="{hm_x - 5:.1f}" y1="{ty:.1f}" x2="{hm_x:.1f}" y2="{ty:.1f}"/>')
        parts.append(f'  <text class="sm ink" x="{hm_x - 9:.1f}" y="{ty + 4:.1f}" text-anchor="end">{lbl}</text>')
    parts.append(
        f'  <text class="lbl ink" x="438" y="{hm_y + hm_h / 2:.1f}" text-anchor="middle" '
        f'transform="rotate(-90 438 {hm_y + hm_h / 2:.1f})">混合层角 β（弧度, rad）</text>'
    )

    # Colorbar cleanly spaced below header and above ticks
    cb_x, cb_w, cb_steps = 870.0, 22.0, 26
    step_h = hm_h / cb_steps
    for s in range(cb_steps):
        v = 0.35 + (s + 0.5) * (1.65 - 0.35) / cb_steps
        sy = hm_y + hm_h - (s + 1) * step_h
        h_cb = step_h if s == 0 else step_h + 0.4
        parts.append(f'  <rect x="{cb_x:.1f}" y="{sy:.1f}" width="{cb_w:.1f}" height="{h_cb:.1f}" fill="{color_for_val(v)}"/>')
    parts.append(f'  <rect class="axis" x="{cb_x:.1f}" y="{hm_y:.1f}" width="{cb_w:.1f}" height="{hm_h:.1f}"/>')
    parts.append(f'  <text class="sm ink" x="{cb_x + 30:.1f}" y="{hm_y - 16:.1f}" text-anchor="middle">⟨C⟩ (无量纲)</text>')
    for v_lbl in (1.65, 1.40, 1.00, 0.60, 0.35):
        ty = hm_y + hm_h - ((v_lbl - 0.35) / (1.65 - 0.35)) * hm_h
        parts.append(f'  <line class="axis" style="stroke-width:1.2" x1="{cb_x + cb_w:.1f}" y1="{ty:.1f}" x2="{cb_x + cb_w + 4:.1f}" y2="{ty:.1f}"/>')
        parts.append(f'  <text class="mono muted" x="{cb_x + cb_w + 8:.1f}" y="{ty + 4:.1f}">{v_lbl:.2f}</text>')

    parts.append(
        f'  <text class="sm muted" x="{rx + 16}" y="502">'
        '36×24 态矢量网格与解析式 1 + ½sin(4β)sinγ(1+cosγ) 核验误差 &lt; 10⁻¹¹。'
        '</text>'
    )
    parts.append(
        '  <text class="sm muted" x="38" y="544">'
        '注：单层 p = 1 受局域邻域度数限制，最大期望割值 1.6495 低于最优割 2；且高期望值不保证每次采样都得到最优串。'
        '</text>'
    )

    svg = wrap_svg(
        "v2-08-qaoa-maxcut",
        "3 顶点路径图 MaxCut 与 p=1 QAOA 期望割值 2D 热力图",
        "左半绘出 3 顶点路径图 0-1-2 及其最大割(割值 2)；右半由 3 比特态矢量精确计算 p=1 QAOA 在 γ∈[0,π]、β∈[0,π/2] 上的期望割值热力图并标出全局最优点(π/3, π/8)，最大期望割值约 1.6495、近似比 0.8248。",
        "\n".join(parts),
    )
    return svg, {
        "max_expected_cut": round(max_exp, 6),
        "approx_ratio": round(approx_ratio, 6),
        "p_opt_strings": round(p_opt_strings, 6),
        "min_expected_cut": round(min_exp, 6),
    }


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    builders = [
        ("v2-05-bloch-noise-channels.svg", build_fig1_bloch_noise_channels),
        ("v2-06-grover-geometry.svg", build_fig2_grover_geometry),
        ("v2-06-qft-circuit.svg", build_fig3_qft_circuit),
        ("v2-07-shor-hhl-pipeline.svg", build_fig4_shor_hhl_pipeline),
        ("v2-08-qaoa-maxcut.svg", build_fig5_qaoa_maxcut),
    ]
    for filename, fn in builders:
        svg_text, stats = fn()
        root = ET.fromstring(svg_text)
        assert root.attrib.get("viewBox") == f"0 0 {W} {H}"
        out_path = ASSETS_DIR / filename
        out_path.write_text(svg_text, encoding="utf-8")
        print(f"[OK] {out_path.relative_to(ROOT)} ({len(svg_text)} bytes) -> {stats}")


if __name__ == "__main__":
    main()
