#!/usr/bin/env python3
"""Generate 5 light/dark-adaptive scientific SVG figures (part 1a: Ch 01, Q1, Ch 02-04)
using Python standard library only.

Outputs to handbook/assets/:
  1. v2-01-complex-rotation.svg      (Ch 01: complex plane rotation, conjugate, |z|^2 vs z^2)
  2. v2-q1-double-slit-mzi.svg       (Q1: double-slit vs path detector + Mach-Zehnder)
  3. v2-02-rotation-half-angle.svg   (Ch 02: Bloch x-z Ry(theta) half-angle + equator Rz/T/S/Z)
  4. v2-03-chsh-game.svg             (Ch 03: CHSH cooperative game, angles, 50/75/85.36% bars)
  5. v2-04-deferred-measurement.svg  (Ch 04: CNOT/CZ/SWAP/Toffoli + deferred measurement)

Run:
  python3 codes/practice/generate_v2_figures_part1a.py

Dependencies:
  Python 3 standard library only (cmath, math, pathlib, xml.etree.ElementTree, xml.sax.saxutils).
  Deterministic numerical calculations (no RNG, no network, no cloud services).
"""

from __future__ import annotations

import cmath
import math
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT / "handbook" / "assets"
W, H = 1000, 580
MARGIN = 30
TOL = 1e-11


COMMON_CSS = """
:root{color-scheme:light dark}
text{font-family:system-ui,-apple-system,'PingFang SC','Microsoft YaHei',sans-serif}
.bg{fill:#f8fafc}
.panel{fill:#ffffff;stroke:#cbd5e1;stroke-width:1.4}
.subpanel{fill:#f4f8fb;stroke:#d1dde8;stroke-width:1.2}
.phead{fill:#eef4f8}
.title{font-size:20px;font-weight:700;fill:#13263a}
.subtitle{font-size:13.5px;font-weight:400;fill:#3e566d}
.sec{font-size:14.5px;font-weight:700;fill:#13263a}
.lbl{font-size:13.5px;font-weight:500;fill:#19324d}
.lblb{font-size:13.5px;font-weight:700;fill:#13263a}
.sm{font-size:12.5px;font-weight:400;fill:#3e566d}
.smb{font-size:12.5px;font-weight:600;fill:#19324d}
.xs{font-size:11.5px;font-weight:500;fill:#3e566d}
.gate-txt{font-family:Georgia,'Times New Roman',serif;font-size:15px;font-weight:700;fill:#13263a}
.axis{stroke:#19324d;stroke-width:1.7;fill:none}
.axis-fill{fill:#19324d}
.wire{stroke:#19324d;stroke-width:2.0;fill:none}
.cwire{stroke:#4a637a;stroke-width:1.5;fill:none}
.ctrl{fill:#13263a}
.targ{fill:#ffffff;stroke:#13263a;stroke-width:2.0}
.grid{stroke:#dce5ee;stroke-width:1;fill:none}
.guide{stroke:#7c93a8;stroke-width:1.25;stroke-dasharray:5 4;fill:none}
.unit-circle{stroke:#5b7790;stroke-width:1.6;stroke-dasharray:6 5;fill:none}
.bloch-circle{fill:#dff4ff;fill-opacity:.34;stroke:#2e6f95;stroke-width:2.2}
.c1{stroke:#1b6ca8;fill:none}
.c1-fill{fill:#1b6ca8}
.c1-txt{fill:#145282}
.c1-soft{fill:#e1f1fb;stroke:#1b6ca8;stroke-width:1.5}
.c2{stroke:#c74b34;fill:none}
.c2-fill{fill:#c74b34}
.c2-txt{fill:#a63824}
.c2-soft{fill:#fce8e3;stroke:#c74b34;stroke-width:1.5}
.c3{stroke:#1e7a5c;fill:none}
.c3-fill{fill:#1e7a5c}
.c3-txt{fill:#155e46}
.c3-soft{fill:#e2f5ee;stroke:#1e7a5c;stroke-width:1.5}
.c4{stroke:#b57614;fill:none}
.c4-fill{fill:#b57614}
.c4-txt{fill:#8a5609}
.c4-soft{fill:#fff4d8;stroke:#b57614;stroke-width:1.5}
.note{fill:#fff8e6;stroke:#c98d24;stroke-width:1.4}
.pill{fill:#f3f7fa;stroke:#9cb1c4;stroke-width:1.2}
.pill-bg{fill:#ffffff;fill-opacity:.94;stroke:#9cb1c4;stroke-width:1.1}
.area1{fill:#1b6ca8;fill-opacity:.11}
.bar-neutral{fill:#e2e8f0;stroke:#556b80;stroke-width:1.5}
.wall{fill:#334e68;stroke:#19324d;stroke-width:1.2}
.mirror{stroke:#19324d;stroke-width:3.2;stroke-linecap:round}
.bs-glass{fill:#bae6fd;fill-opacity:.58;stroke:#1b6ca8;stroke-width:1.6}
.det-body{fill:#e2f5ee;stroke:#1e7a5c;stroke-width:1.8}
.badge-txt{fill:#ffffff;font-size:12.5px;font-weight:700}
.hatch-stroke1{stroke:#1b6ca8;stroke-width:1.2;stroke-opacity:.42}
.hatch-stroke2{stroke:#c74b34;stroke-width:1.2;stroke-opacity:.42}
.hatch-stroke3{stroke:#1e7a5c;stroke-width:1.2;stroke-opacity:.42}
.hatch-stroke0{stroke:#556b80;stroke-width:1.1;stroke-opacity:.38}
@media(prefers-color-scheme:dark){
  .bg{fill:#0f1720}
  .panel{fill:#16222e;stroke:#354c61}
  .subpanel{fill:#1b2a38;stroke:#3b5369}
  .phead{fill:#1c2d3d}
  .title,.sec,.lblb,.gate-txt{fill:#eef6ff}
  .subtitle,.sm,.xs{fill:#b7cde0}
  .lbl,.smb{fill:#d7e7f5}
  .axis,.wire{stroke:#cde0f2}
  .axis-fill,.ctrl{fill:#cde0f2}
  .cwire{stroke:#9bb6ce}
  .targ{fill:#16222e;stroke:#cde0f2}
  .grid{stroke:#293e52}
  .guide,.unit-circle{stroke:#738fa8}
  .bloch-circle{fill:#164968;fill-opacity:.38;stroke:#7ed4ff}
  .c1{stroke:#6bc2f5}
  .c1-fill{fill:#6bc2f5}
  .c1-txt{fill:#8fd4fa}
  .c1-soft{fill:#173a52;stroke:#6bc2f5}
  .c2{stroke:#f28872}
  .c2-fill{fill:#f28872}
  .c2-txt{fill:#f8a896}
  .c2-soft{fill:#48241e;stroke:#f28872}
  .c3{stroke:#5dd1a8}
  .c3-fill{fill:#5dd1a8}
  .c3-txt{fill:#84e0bf}
  .c3-soft{fill:#163d31;stroke:#5dd1a8}
  .c4{stroke:#f0ba5a}
  .c4-fill{fill:#f0ba5a}
  .c4-txt{fill:#f5cc82}
  .c4-soft{fill:#3d3014;stroke:#f0ba5a}
  .note{fill:#332914;stroke:#d6a240}
  .pill{fill:#203142;stroke:#4f6b85}
  .pill-bg{fill:#16222e;fill-opacity:.94;stroke:#4f6b85}
  .area1{fill:#6bc2f5;fill-opacity:.15}
  .bar-neutral{fill:#2a3c4e;stroke:#8fa9c2}
  .wall{fill:#8ca5bc;stroke:#cde0f2}
  .mirror{stroke:#cde0f2}
  .bs-glass{fill:#1d5475;fill-opacity:.65;stroke:#6bc2f5}
  .det-body{fill:#163d31;stroke:#5dd1a8}
  .badge-txt{fill:#0f1720}
  .hatch-stroke1{stroke:#6bc2f5;stroke-opacity:.48}
  .hatch-stroke2{stroke:#f28872;stroke-opacity:.48}
  .hatch-stroke3{stroke:#5dd1a8;stroke-opacity:.48}
  .hatch-stroke0{stroke:#9ab4cc;stroke-opacity:.42}
}
""".strip()


def fmt(v: float) -> str:
    s = f"{v:.2f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def sub(txt: str) -> str:
    return f'<tspan dy="3" font-size="75%">{escape(txt)}</tspan><tspan dy="-3">&#8203;</tspan>'


def sup(txt: str) -> str:
    return f'<tspan dy="-4.5" font-size="75%">{escape(txt)}</tspan><tspan dy="4.5">&#8203;</tspan>'


def pts_str(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{fmt(x)},{fmt(y)}" for x, y in points)


def path_from_points(points: list[tuple[float, float]]) -> str:
    if not points:
        return ""
    head = f"M {fmt(points[0][0])} {fmt(points[0][1])}"
    tail = " ".join(f"L {fmt(x)} {fmt(y)}" for x, y in points[1:])
    return f"{head} {tail}".strip()


def diamond_pts(cx: float, cy: float, r: float) -> str:
    return pts_str([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)])


def triangle_pts(cx: float, cy: float, r: float) -> str:
    return pts_str([
        (cx, cy - r * 1.15),
        (cx + r * 1.0, cy + r * 0.8),
        (cx - r * 1.0, cy + r * 0.8),
    ])


def arrow_head(x: float, y: float, dx: float, dy: float, size: float = 8.0, cls: str = "axis-fill") -> str:
    norm = math.hypot(dx, dy)
    assert norm > 1e-12, "Zero-length arrow direction"
    ux, uy = dx / norm, dy / norm
    px, py = -uy, ux
    bx, by = x - ux * size, y - uy * size
    hw = size * 0.48
    p1 = (x, y)
    p2 = (bx + px * hw, by + py * hw)
    p3 = (bx - px * hw, by - py * hw)
    return f'<polygon class="{cls}" points="{pts_str([p1, p2, p3])}"/>'


def math_arc_points(
    cx: float, cy: float, r: float, a0_rad: float, a1_rad: float, steps: int = 36
) -> list[tuple[float, float]]:
    """Sample circular arc using standard mathematical angles (0 = +x right, +angle = CCW up)."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        a = a0_rad + (a1_rad - a0_rad) * i / steps
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    return pts


def mat_mul(a: list[list[complex]], b: list[list[complex]]) -> list[list[complex]]:
    n, m, p = len(a), len(b), len(b[0])
    assert len(a[0]) == m
    out: list[list[complex]] = []
    for i in range(n):
        row: list[complex] = []
        for j in range(p):
            row.append(sum(a[i][k] * b[k][j] for k in range(m)))
        out.append(row)
    return out


def mat_vec(a: list[list[complex]], v: list[complex]) -> list[complex]:
    return [sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a))]


def mat_dag(a: list[list[complex]]) -> list[list[complex]]:
    n, m = len(a), len(a[0])
    return [[a[j][i].conjugate() for j in range(n)] for i in range(m)]


def kron(a: list[list[complex]], b: list[list[complex]]) -> list[list[complex]]:
    na, ma = len(a), len(a[0])
    nb, mb = len(b), len(b[0])
    out = [[0j] * (ma * mb) for _ in range(na * nb)]
    for i in range(na):
        for j in range(ma):
            for p in range(nb):
                for q in range(mb):
                    out[i * nb + p][j * mb + q] = a[i][j] * b[p][q]
    return out


def max_mat_diff(a: list[list[complex]], b: list[list[complex]]) -> float:
    return max(abs(a[i][j] - b[i][j]) for i in range(len(a)) for j in range(len(a[0])))


class SvgDoc:
    def __init__(self, title: str, desc: str, width: int = W, height: int = H) -> None:
        self.w = width
        self.h = height
        self.title = title
        self.desc = desc
        self.defs: list[str] = [
            '<pattern id="hatch-blue" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<line class="hatch-stroke1" x1="0" y1="0" x2="0" y2="8"/></pattern>',
            '<pattern id="hatch-red" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">'
            '<line class="hatch-stroke2" x1="0" y1="0" x2="0" y2="8"/></pattern>',
            '<pattern id="hatch-green" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<line class="hatch-stroke3" x1="0" y1="0" x2="0" y2="8"/></pattern>',
            '<pattern id="hatch-neutral" width="7" height="7" patternUnits="userSpaceOnUse">'
            '<line class="hatch-stroke0" x1="0" y1="3.5" x2="7" y2="3.5"/></pattern>',
        ]
        self.body: list[str] = []

    def add(self, snippet: str) -> None:
        self.body.append(snippet)

    def add_header(
        self, title_text: str, subtitle_text: str, *, raw_title: bool = False, raw_sub: bool = False
    ) -> None:
        self.add(f'<rect class="bg" width="{self.w}" height="{self.h}" rx="20"/>')
        t_out = title_text if raw_title else escape(title_text)
        s_out = subtitle_text if raw_sub else escape(subtitle_text)
        self.add(f'<text class="title" x="34" y="54">{t_out}</text>')
        self.add(f'<text class="subtitle" x="34" y="79">{s_out}</text>')

    def add_panel(self, x: float, y: float, w: float, h: float, heading: str, *, raw_heading: bool = False) -> None:
        self.add(f'<rect class="panel" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="14"/>')
        self.add(
            f'<path class="phead" d="M {fmt(x + 14)} {fmt(y + 1)} H {fmt(x + w - 14)} '
            f'Q {fmt(x + w - 1)} {fmt(y + 1)} {fmt(x + w - 1)} {fmt(y + 14)} V {fmt(y + 38)} '
            f'H {fmt(x + 1)} V {fmt(y + 14)} Q {fmt(x + 1)} {fmt(y + 1)} {fmt(x + 14)} {fmt(y + 1)} Z"/>'
        )
        self.add(f'<line class="grid" x1="{fmt(x + 1)}" y1="{fmt(y + 38)}" x2="{fmt(x + w - 1)}" y2="{fmt(y + 38)}"/>')
        h_out = heading if raw_heading else escape(heading)
        self.add(f'<text class="sec" x="{fmt(x + 16)}" y="{fmt(y + 24)}">{h_out}</text>')

    def render(self) -> str:
        defs_xml = "\n    ".join(self.defs)
        body_xml = "\n  ".join(self.body)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'role="img" aria-labelledby="title desc">\n'
            f'  <title id="title">{escape(self.title)}</title>\n'
            f'  <desc id="desc">{escape(self.desc)}</desc>\n'
            f'  <style>\n{COMMON_CSS}\n  </style>\n'
            f'  <defs>\n    {defs_xml}\n  </defs>\n'
            f'  {body_xml}\n'
            f'</svg>\n'
        )


# ---------------------------------------------------------------------------
# Figure 1: Ch 01 — Complex plane rotation (z1, i*z1, z1*) & |z1|^2 vs z1^2
# ---------------------------------------------------------------------------
def build_fig1_complex_rotation() -> tuple[str, dict[str, float]]:
    z1 = complex(1.0, 1.0)
    z2 = 1j * z1
    z1_conj = z1.conjugate()
    mod_sq = (z1_conj * z1).real
    z1_sq = z1 * z1
    alpha = (1.0 + 1j) / 2.0

    # Exact mathematical assertions
    r_z1 = abs(z1)
    assert abs(r_z1 - math.sqrt(2.0)) < TOL
    assert abs(abs(z2) - r_z1) < TOL
    assert abs(abs(z1_conj) - r_z1) < TOL
    assert abs(z2 - complex(-1.0, 1.0)) < TOL
    assert abs(z1_conj - complex(1.0, -1.0)) < TOL
    assert abs(cmath.phase(z1) - math.pi / 4.0) < TOL
    assert abs(cmath.phase(z2) - 3.0 * math.pi / 4.0) < TOL
    assert abs(cmath.phase(z1_conj) + math.pi / 4.0) < TOL
    assert abs(mod_sq - 2.0) < TOL
    assert abs((z1_conj * z1).imag) < TOL
    assert abs(z1_sq - 2j) < TOL
    assert abs(abs(alpha) ** 2 - 0.5) < TOL
    assert abs(alpha * alpha - 0.5j) < TOL

    doc = SvgDoc(
        title="复平面上的旋转、共轭镜像与模平方辨析",
        desc=(
            "左图在等比例复平面上绘制 z₁ = 1 + i（模 √2，角度 45°）、乘以虚数单位 i 后逆时针旋转 90° 得到的 "
            "z₂ = −1 + i（135°），以及关于实轴镜像的共轭 z₁* = 1 − i（−45°），三点同位于半径 √2 的圆周。"
            "右图对比 Born 概率所需的非负实数模平方 |z₁|² = z₁*·z₁ = 2 与复数直接平方 z₁² = 2i。"
        ),
    )
    doc.add_header(
        "复平面上的旋转、共轭镜像与模平方辨析",
        "左：z₁ = 1 + i 乘 i 逆时针旋 90° 到 z₂ = −1 + i，共轭 z₁* = 1 − i 沿实轴镜像；右：|z₁|² 与 z₁² 的本质区别",
    )

    doc.add_panel(28, 96, 548, 456, "等比例复平面：乘 i 旋转 90° 与共轭实轴镜像")
    doc.add_panel(592, 96, 380, 456, "关键辨析：模平方 |z₁|² 与复数平方 z₁²")

    # --- Left Panel: Equal-aspect complex plane ---
    ox, oy = 302.0, 338.0
    scale = 92.0  # 1 unit = 92 px (strictly 1:1 aspect ratio)

    def cx(z: complex) -> float:
        return ox + z.real * scale

    def cy(z: complex) -> float:
        return oy - z.imag * scale

    # Subtle unit grid inside [-2, 2] x [-1.5, 1.5]
    for gx in [-2, -1, 1, 2]:
        x_g = ox + gx * scale
        doc.add(f'<line class="grid" x1="{fmt(x_g)}" y1="{fmt(oy - 1.55 * scale)}" x2="{fmt(x_g)}" y2="{fmt(oy + 1.48 * scale)}"/>')
    for gy in [-1, 1]:
        y_g = oy - gy * scale
        doc.add(f'<line class="grid" x1="{fmt(ox - 2.15 * scale)}" y1="{fmt(y_g)}" x2="{fmt(ox + 2.15 * scale)}" y2="{fmt(y_g)}"/>')

    # Concentric circles: unit circle r=1 and equal-modulus circle r=sqrt(2)
    doc.add(f'<circle class="grid" stroke-dasharray="3 4" cx="{fmt(ox)}" cy="{fmt(oy)}" r="{fmt(scale)}"/>')
    doc.add(f'<circle class="unit-circle" cx="{fmt(ox)}" cy="{fmt(oy)}" r="{fmt(r_z1 * scale)}"/>')
    doc.add(f'<text class="xs" x="{fmt(ox - 16)}" y="{fmt(oy + 56)}" text-anchor="end">单位圆 r = 1</text>')
    doc.add(f'<text class="xs" x="{fmt(ox - 1.32 * scale)}" y="{fmt(oy + 1.24 * scale)}" text-anchor="end">等模圆 r = √2</text>')

    # Real & Imaginary axes
    x_min, x_max = ox - 2.22 * scale, ox + 2.25 * scale
    y_min, y_max = oy - 1.66 * scale, oy + 1.56 * scale
    doc.add(f'<line class="axis" x1="{fmt(x_min)}" y1="{fmt(oy)}" x2="{fmt(x_max)}" y2="{fmt(oy)}"/>')
    doc.add(arrow_head(x_max, oy, 1, 0, 8.0))
    doc.add(f'<line class="axis" x1="{fmt(ox)}" y1="{fmt(y_max)}" x2="{fmt(ox)}" y2="{fmt(y_min)}"/>')
    doc.add(arrow_head(ox, y_min, 0, -1, 8.0))

    # Axis titles with units (dimensionless)
    doc.add(f'<rect class="pill-bg" x="{fmt(x_max - 110)}" y="{fmt(oy - 32)}" width="110" height="22" rx="8"/>')
    doc.add(f'<text class="xs" x="{fmt(x_max - 55)}" y="{fmt(oy - 17)}" text-anchor="middle">Re(z) (无量纲)</text>')
    doc.add(f'<text class="smb" x="{fmt(ox)}" y="{fmt(y_min - 11)}" text-anchor="middle">Im(z) (虚部，无量纲)</text>')

    # Ticks on axes
    for v_re, lbl_re in [(-2, "−2"), (-1, "−1"), (1, "1"), (2, "2")]:
        xt = ox + v_re * scale
        doc.add(f'<line class="axis" stroke-width="1.3" x1="{fmt(xt)}" y1="{fmt(oy - 4)}" x2="{fmt(xt)}" y2="{fmt(oy + 4)}"/>')
        y_lbl = oy + 19 if v_re != 1 else oy + 19
        x_shift = -8 if v_re == 1 else 0
        doc.add(f'<text class="sm" x="{fmt(xt + x_shift)}" y="{fmt(y_lbl)}" text-anchor="middle">{lbl_re}</text>')
    for v_im, lbl_im in [(-1, "−1"), (1, "1")]:
        yt = oy - v_im * scale
        doc.add(f'<line class="axis" stroke-width="1.3" x1="{fmt(ox - 4)}" y1="{fmt(yt)}" x2="{fmt(ox + 4)}" y2="{fmt(yt)}"/>')
        y_im_lbl = yt + 15 if v_im == 1 else yt + 4
        doc.add(f'<text class="sm" x="{fmt(ox - 10)}" y="{fmt(y_im_lbl)}" text-anchor="end">{lbl_im}</text>')
    doc.add(f'<text class="sm" x="{fmt(ox - 10)}" y="{fmt(oy + 18)}" text-anchor="end">0</text>')

    # Dashed coordinate projection & vertical conjugate mirror line
    p1 = (cx(z1), cy(z1))
    p2 = (cx(z2), cy(z2))
    pc = (cx(z1_conj), cy(z1_conj))
    doc.add(f'<line class="guide" x1="{fmt(p1[0])}" y1="{fmt(p1[1])}" x2="{fmt(pc[0])}" y2="{fmt(pc[1])}"/>')
    doc.add(f'<line class="guide" x1="{fmt(p2[0])}" y1="{fmt(p2[1])}" x2="{fmt(p1[0])}" y2="{fmt(p1[1])}"/>')
    doc.add(f'<line class="guide" x1="{fmt(p2[0])}" y1="{fmt(p2[1])}" x2="{fmt(p2[0])}" y2="{fmt(oy)}"/>')

    # Right-angle square marker between z1 (45 deg) and z2 (135 deg)
    sq_r = 16.0
    u1 = (math.cos(math.pi / 4), -math.sin(math.pi / 4))
    u2 = (math.cos(3 * math.pi / 4), -math.sin(3 * math.pi / 4))
    ra_pts = [
        (ox + sq_r * u1[0], oy + sq_r * u1[1]),
        (ox + sq_r * (u1[0] + u2[0]), oy + sq_r * (u1[1] + u2[1])),
        (ox + sq_r * u2[0], oy + sq_r * u2[1]),
    ]
    doc.add(f'<path class="c2" stroke-width="1.5" d="{path_from_points(ra_pts)}"/>')

    # Angle arcs: +45 deg, -45 deg, and +90 deg rotation arc from z1 to z2
    arc_p45 = math_arc_points(ox, oy, 44.0, 0.0, math.pi / 4.0, 18)
    doc.add(f'<path class="c1" stroke-width="1.7" d="{path_from_points(arc_p45)}"/>')
    doc.add(f'<text class="xs c1-txt" x="{fmt(ox + 50)}" y="{fmt(oy - 14)}">+45°</text>')

    arc_m45 = math_arc_points(ox, oy, 44.0, 0.0, -math.pi / 4.0, 18)
    doc.add(f'<path class="c3" stroke-width="1.7" d="{path_from_points(arc_m45)}"/>')
    doc.add(f'<text class="xs c3-txt" x="{fmt(ox + 50)}" y="{fmt(oy + 24)}">−45°</text>')

    arc_rot = math_arc_points(ox, oy, 110.0, math.pi / 4.0 + 0.04, 3.0 * math.pi / 4.0 - 0.04, 28)
    doc.add(f'<path class="c2" stroke-width="2.1" d="{path_from_points(arc_rot)}"/>')
    doc.add(
        arrow_head(
            arc_rot[-1][0], arc_rot[-1][1],
            arc_rot[-1][0] - arc_rot[-2][0], arc_rot[-1][1] - arc_rot[-2][1],
            7.5, "c2-fill",
        )
    )
    # Pill label on top of rotation arc (clear of Im axis)
    doc.add('<rect class="pill-bg" x="234" y="198" width="136" height="24" rx="12"/>')
    doc.add('<text class="smb c2-txt" x="302" y="214" text-anchor="middle">× i：逆时针 +90°</text>')

    # Vectors from origin to z1, z2, z1* (distinct color + line dash + tip marker)
    # z1: solid blue + filled circle
    doc.add(f'<line class="c1" stroke-width="2.8" x1="{fmt(ox)}" y1="{fmt(oy)}" x2="{fmt(p1[0])}" y2="{fmt(p1[1])}"/>')
    doc.add(arrow_head(p1[0], p1[1], p1[0] - ox, p1[1] - oy, 9.0, "c1-fill"))
    doc.add(f'<circle class="c1-fill" cx="{fmt(p1[0])}" cy="{fmt(p1[1])}" r="5.5"/>')

    # z2 = i*z1: dashed red + diamond
    doc.add(f'<line class="c2" stroke-width="2.7" stroke-dasharray="8 4" x1="{fmt(ox)}" y1="{fmt(oy)}" x2="{fmt(p2[0])}" y2="{fmt(p2[1])}"/>')
    doc.add(arrow_head(p2[0], p2[1], p2[0] - ox, p2[1] - oy, 9.0, "c2-fill"))
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(p2[0], p2[1], 6.2)}"/>')

    # z1*: dash-dot green + square
    doc.add(f'<line class="c3" stroke-width="2.6" stroke-dasharray="10 3 2 3" x1="{fmt(ox)}" y1="{fmt(oy)}" x2="{fmt(pc[0])}" y2="{fmt(pc[1])}"/>')
    doc.add(arrow_head(pc[0], pc[1], pc[0] - ox, pc[1] - oy, 9.0, "c3-fill"))
    doc.add(f'<rect class="c3-fill" x="{fmt(pc[0] - 5)}" y="{fmt(pc[1] - 5)}" width="10" height="10" rx="1.5"/>')

    # Point annotations (kept cleanly outside circle and clear of axes)
    doc.add('<text class="lblb c1-txt" x="408" y="238">z₁ = 1 + i</text>')
    doc.add('<text class="sm c1-txt" x="408" y="256">|z₁| = √2, θ = 45°</text>')

    doc.add('<text class="lblb c2-txt" x="196" y="238" text-anchor="end">z₂ = i·z₁ = −1 + i</text>')
    doc.add('<text class="sm c2-txt" x="196" y="256" text-anchor="end">|z₂| = √2, θ = 135°</text>')

    doc.add('<text class="lblb c3-txt" x="408" y="432">z₁* = 1 − i（共轭）</text>')
    doc.add('<text class="sm c3-txt" x="408" y="450">|z₁*| = √2, θ = −45°</text>')

    # Conjugate mirror callout on right side between z1 and z1*
    doc.add('<rect class="pill-bg" x="406" y="366" width="114" height="24" rx="10"/>')
    doc.add('<text class="xs c3-txt" x="463" y="382" text-anchor="middle">沿实轴上下镜像</text>')

    # Bottom summary bar inside left panel
    doc.add('<rect class="note" x="44" y="498" width="516" height="40" rx="10"/>')
    doc.add('<text class="sm" x="302" y="522" text-anchor="middle">乘法法则：长度相乘、角度相加；乘单位相位 e<tspan baseline-shift="super" font-size="72%">iφ</tspan> 只旋不缩，保概率总和为 1</text>')

    # --- Right Panel: |z1|^2 vs z1^2 comparison cards + mini vector diagram ---
    # Card 1: |z1|^2 (Correct Born probability quantity)
    doc.add('<rect class="c3-soft" x="608" y="150" width="348" height="108" rx="11"/>')
    doc.add('<rect class="c3-fill" x="620" y="162" width="60" height="22" rx="11"/>')
    doc.add('<text class="badge-txt" x="650" y="177" text-anchor="middle">✓ 模平方</text>')
    doc.add('<text class="lblb c3-txt" x="690" y="178">|z₁|² = z₁* · z₁ = 2</text>')
    doc.add('<text class="sm" x="622" y="206">代数：(1 − i)(1 + i) = 1² − i² = 1 + 1 = 2</text>')
    doc.add('<text class="sm" x="622" y="226">极坐标：(√2·e<tspan baseline-shift="super" font-size="72%">−iπ/4</tspan>)(√2·e<tspan baseline-shift="super" font-size="72%">+iπ/4</tspan>) = 2（相位抵消）</text>')
    doc.add('<text class="smb c3-txt" x="622" y="247">结果恒为非负实数 ∈ ℝ≥₀，归一化后作测量概率</text>')

    # Card 2: z1^2 (Common mistake)
    doc.add('<rect class="c2-soft" x="608" y="270" width="348" height="108" rx="11"/>')
    doc.add('<rect fill="url(#hatch-red)" x="608" y="270" width="348" height="108" rx="11" opacity="0.28"/>')
    doc.add('<rect class="c2-fill" x="620" y="282" width="68" height="22" rx="11"/>')
    doc.add('<text class="badge-txt" x="654" y="297" text-anchor="middle">✕ 复数平方</text>')
    doc.add('<text class="lblb c2-txt" x="698" y="298">z₁² = z₁ · z₁ = 2i</text>')
    doc.add('<text class="sm" x="622" y="326">代数：(1 + i)² = 1 + 2i + i² = 2i</text>')
    doc.add('<text class="sm" x="622" y="346">极坐标：(√2)²·e<tspan baseline-shift="super" font-size="72%">i(2×45°)</tspan> = 2·e<tspan baseline-shift="super" font-size="72%">iπ/2</tspan>（角度翻倍）</text>')
    doc.add('<text class="smb c2-txt" x="622" y="367">结果落在虚轴（非实数），不能当作测量概率</text>')

    # Mini geometric contrast plot (equal-scale 1 unit = 32 px)
    doc.add('<rect class="subpanel" x="608" y="390" width="348" height="96" rx="10"/>')
    mox, moy = 656.0, 470.0
    ms = 30.0
    # Axes
    doc.add(f'<line class="axis" stroke-width="1.4" x1="{fmt(mox - 12)}" y1="{fmt(moy)}" x2="{fmt(mox + 88)}" y2="{fmt(moy)}"/>')
    doc.add(arrow_head(mox + 88, moy, 1, 0, 6.0))
    doc.add(f'<line class="axis" stroke-width="1.4" x1="{fmt(mox)}" y1="{fmt(moy + 10)}" x2="{fmt(mox)}" y2="{fmt(moy - 74)}"/>')
    doc.add(arrow_head(mox, moy - 74, 0, -1, 6.0))
    # |z1|^2 = 2 on +Re
    doc.add(f'<line class="c3" stroke-width="3.0" x1="{fmt(mox)}" y1="{fmt(moy)}" x2="{fmt(mox + 2 * ms)}" y2="{fmt(moy)}"/>')
    doc.add(f'<circle class="c3-fill" cx="{fmt(mox + 2 * ms)}" cy="{fmt(moy)}" r="4.8"/>')
    doc.add(f'<text class="smb c3-txt" x="{fmt(mox + 2 * ms)}" y="{fmt(moy - 10)}" text-anchor="middle">|z₁|² = 2</text>')
    # z1^2 = 2i on +Im
    doc.add(f'<line class="c2" stroke-width="2.8" stroke-dasharray="6 3" x1="{fmt(mox)}" y1="{fmt(moy)}" x2="{fmt(mox)}" y2="{fmt(moy - 2 * ms)}"/>')
    doc.add(f'<polygon class="c2-fill" points="{triangle_pts(mox, moy - 2 * ms, 5.2)}"/>')
    doc.add(f'<text class="smb c2-txt" x="{fmt(mox + 12)}" y="{fmt(moy - 2 * ms + 5)}">z₁² = 2i</text>')
    # Mini plot side explanation
    doc.add('<text class="smb" x="770" y="420">几何对照（同长 2）</text>')
    doc.add('<text class="sm" x="770" y="442">|z₁|² 沿正实轴（0°）</text>')
    doc.add('<text class="sm" x="770" y="462">z₁² 沿正虚轴（90°）</text>')

    # Bottom Born-rule numerical example
    doc.add('<rect class="note" x="608" y="498" width="348" height="40" rx="10"/>')
    doc.add('<text class="sm" x="782" y="522" text-anchor="middle">算例：α = (1+i)/2 ⇒ |α|² = 1/2（概率），α² = i/2</text>')

    return doc.render(), {"abs_z1": r_z1, "mod_sq": mod_sq, "z1_sq_imag": z1_sq.imag}


# ---------------------------------------------------------------------------
# Figure 2: Q1 — Double-slit interference vs path detector + MZI
# ---------------------------------------------------------------------------
def build_fig2_double_slit_mzi() -> tuple[str, dict[str, float]]:
    # Double-slit exact model: u = x / Delta_x in [-2.5, 2.5]
    beta = 0.26

    def sinc_sq(arg: float) -> float:
        if abs(arg) < 1e-12:
            return 1.0
        val = math.sin(math.pi * arg) / (math.pi * arg)
        return val * val

    def i_coh(u: float) -> float:
        return sinc_sq(beta * u) * (math.cos(math.pi * u) ** 2)

    def i_path(u: float) -> float:
        return 0.5 * sinc_sq(beta * u)

    assert abs(i_coh(0.0) - 1.0) < TOL
    assert abs(i_coh(0.5)) < TOL
    assert abs(i_coh(-0.5)) < TOL
    assert abs(i_path(0.0) - 0.5) < TOL
    assert i_coh(1.0) > i_path(1.0) > 0.0

    # Exact MZI 2x2 matrix verification matching Q1 §3.1: B = H, U_phi = diag(1, e^{i phi})
    inv_s2 = 1.0 / math.sqrt(2.0)
    b_mat: list[list[complex]] = [[inv_s2, inv_s2], [inv_s2, -inv_s2]]
    ident2: list[list[complex]] = [[1.0 + 0j, 0j], [0j, 1.0 + 0j]]
    assert max_mat_diff(mat_mul(mat_dag(b_mat), b_mat), ident2) < TOL

    def mzi_probs(phi: float) -> tuple[float, float]:
        u_phi: list[list[complex]] = [[1.0 + 0j, 0j], [0j, cmath.exp(1j * phi)]]
        psi = mat_vec(b_mat, mat_vec(u_phi, mat_vec(b_mat, [1.0 + 0j, 0j])))
        p0, p1 = abs(psi[0]) ** 2, abs(psi[1]) ** 2
        return p0, p1

    for test_phi in [0.0, math.pi / 3.0, math.pi / 2.0, math.pi, 1.5 * math.pi, 2.0 * math.pi]:
        p0_m, p1_m = mzi_probs(test_phi)
        assert abs(p0_m - math.cos(test_phi / 2.0) ** 2) < TOL
        assert abs(p1_m - math.sin(test_phi / 2.0) ** 2) < TOL
        assert abs((p0_m + p1_m) - 1.0) < TOL

    doc = SvgDoc(
        title="双缝干涉路径互补性与 Mach–Zehnder 离散干涉仪",
        desc=(
            "左面板展示单粒子双缝实验装置及精确强度分布：无路径探测时相干叠加产生 env(x)·cos²(πx/Δx) 明暗条纹；"
            "放置路径探测器后交叉干涉项消失，退化为两单缝概率之和 ½env(x)。右面板展示离散双路径 Mach–Zehnder 干涉仪"
            "（两块 50:50 分束器 B 与下臂相位片 U_φ）及输出端口概率曲线 P(0) = cos²(φ/2)、P(1) = sin²(φ/2)。"
        ),
    )
    doc.add_header(
        "双缝干涉的路径互补性与 Mach–Zehnder 离散干涉仪",
        "左：相干叠加产生 cos² 亮暗条纹，加入路径探测后退化为经典概率相加；右：MZI 把相对相位 φ 映射为互补端口概率",
    )

    doc.add_panel(28, 96, 464, 456, "连续屏幕：双缝相干干涉与路径探测")
    doc.add_panel(508, 96, 464, 456, "离散双路径：Mach–Zehnder 干涉仪 (MZI)")

    # --- Left Panel Top: Double-slit schematic (y=146..270) ---
    doc.add('<rect class="subpanel" x="44" y="148" width="432" height="122" rx="10"/>')
    # Source
    doc.add('<rect class="c1-soft" x="56" y="191" width="54" height="36" rx="7"/>')
    doc.add('<text class="smb c1-txt" x="83" y="207" text-anchor="middle">单粒子</text>')
    doc.add('<text class="xs c1-txt" x="83" y="221" text-anchor="middle">发射源</text>')

    # Barrier with two slits S1 (y=186) and S2 (y=232)
    bx_wall = 172.0
    doc.add(f'<rect class="wall" x="{fmt(bx_wall)}" y="156" width="8" height="22" rx="1"/>')
    doc.add(f'<rect class="wall" x="{fmt(bx_wall)}" y="194" width="8" height="30" rx="1"/>')
    doc.add(f'<rect class="wall" x="{fmt(bx_wall)}" y="240" width="8" height="22" rx="1"/>')
    doc.add('<text class="xs" x="156" y="180" text-anchor="end">缝 1</text>')
    doc.add('<text class="xs" x="156" y="248" text-anchor="end">缝 2</text>')

    # Optional path detector box near slit 1
    doc.add('<rect class="c2-soft" stroke-dasharray="4 3" x="188" y="158" width="58" height="22" rx="5"/>')
    doc.add('<text class="xs c2-txt" x="217" y="173" text-anchor="middle">探测 D?</text>')

    # Paths from source -> slits -> screen (x=284)
    sx_scr = 286.0
    doc.add('<line class="c1" stroke-width="1.6" x1="110" y1="209" x2="172" y2="186"/>')
    doc.add('<line class="c1" stroke-width="1.6" x1="110" y1="209" x2="172" y2="232"/>')
    # Interference fan to bright/dark spots on screen
    for y_hit in [170.0, 202.0, 234.0]:
        doc.add(f'<line class="c1" stroke-width="1.3" stroke-opacity="0.72" x1="180" y1="186" x2="{fmt(sx_scr)}" y2="{fmt(y_hit)}"/>')
        doc.add(f'<line class="c1" stroke-width="1.3" stroke-opacity="0.72" x1="180" y1="232" x2="{fmt(sx_scr)}" y2="{fmt(y_hit)}"/>')

    # Detection screen bar with bright-dark fringe bands
    doc.add(f'<rect class="panel" x="{fmt(sx_scr)}" y="156" width="12" height="90" rx="3"/>')
    for y_b, op in [(167, 0.72), (184, 0.12), (201, 0.92), (218, 0.12), (235, 0.72)]:
        doc.add(f'<rect class="c1-fill" fill-opacity="{op}" x="{fmt(sx_scr + 1.5)}" y="{fmt(y_b - 5)}" width="9" height="10" rx="2"/>')
    doc.add(f'<text class="xs" x="{fmt(sx_scr + 6)}" y="261" text-anchor="middle">屏幕</text>')

    # Right summary inside top subpanel
    doc.add('<text class="smb c1-txt" x="314" y="174">━● 无探测（相干）</text>')
    doc.add('<text class="xs" x="322" y="191">P = |ψ₁ + ψ₂|²</text>')
    doc.add('<text class="xs" x="322" y="207">含交叉项 2Re(ψ₁*ψ₂)</text>')
    doc.add('<text class="smb c2-txt" x="314" y="232">┅◆ 有路径探测 D</text>')
    doc.add('<text class="xs" x="322" y="249">P = |ψ₁|² + |ψ₂|²</text>')
    doc.add('<text class="xs" x="322" y="264">条纹消失，无暗纹</text>')

    # --- Left Panel Bottom: Exact Intensity Curves (y=292..540) ---
    px0, px1 = 92.0, 466.0
    py0, py1 = 482.0, 316.0  # P=0 bottom, P=1 top
    u_min, u_max = -2.5, 2.5

    def map_u(u: float) -> float:
        return px0 + (u - u_min) / (u_max - u_min) * (px1 - px0)

    def map_i(val: float) -> float:
        return py0 - val * (py0 - py1)

    # Grid & ticks
    for y_tick in [0.0, 0.5, 1.0]:
        yt = map_i(y_tick)
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(yt)}" x2="{fmt(px1)}" y2="{fmt(yt)}"/>')
        doc.add(f'<text class="sm" x="{fmt(px0 - 8)}" y="{fmt(yt + 4)}" text-anchor="end">{y_tick:.1f}</text>')
    for u_tick in [-2, -1, 0, 1, 2]:
        xt = map_u(float(u_tick))
        doc.add(f'<line class="grid" x1="{fmt(xt)}" y1="{fmt(py1)}" x2="{fmt(xt)}" y2="{fmt(py0)}"/>')
        lbl_u = f"−{abs(u_tick)}" if u_tick < 0 else str(u_tick)
        doc.add(f'<text class="sm" x="{fmt(xt)}" y="{fmt(py0 + 18)}" text-anchor="middle">{lbl_u}</text>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px1 + 8)}" y2="{fmt(py0)}"/>')
    doc.add(arrow_head(px1 + 8, py0, 1, 0, 7.0))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px0)}" y2="{fmt(py1 - 12)}"/>')
    doc.add(arrow_head(px0, py1 - 12, 0, -1, 7.0))
    doc.add(f'<text class="sm" x="{fmt(0.5 * (px0 + px1))}" y="528" text-anchor="middle">屏幕位置 x / Δx (无量纲)</text>')
    doc.add(
        f'<text class="sm" x="48" y="{fmt(0.5 * (py0 + py1))}" text-anchor="middle" '
        f'transform="rotate(-90 48 {fmt(0.5 * (py0 + py1))})">探测概率密度 P(x) (归一化)</text>'
    )

    # Curves (251 samples)
    n_s = 251
    coh_pts = [(map_u(u_min + (u_max - u_min) * i / (n_s - 1)), map_i(i_coh(u_min + (u_max - u_min) * i / (n_s - 1)))) for i in range(n_s)]
    path_pts = [(map_u(u_min + (u_max - u_min) * i / (n_s - 1)), map_i(i_path(u_min + (u_max - u_min) * i / (n_s - 1)))) for i in range(n_s)]

    area_pts = [(px0, py0)] + coh_pts + [(px1, py0)]
    doc.add(f'<path class="area1" d="{path_from_points(area_pts)} Z"/>')
    doc.add(f'<path class="c1" stroke-width="2.5" d="{path_from_points(coh_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.3" stroke-dasharray="8 5" d="{path_from_points(path_pts)}"/>')

    # Distinct markers on key peaks/zeros
    for u_pk in [-1.0, 0.0, 1.0]:
        doc.add(f'<circle class="c1-fill" cx="{fmt(map_u(u_pk))}" cy="{fmt(map_i(i_coh(u_pk)))}" r="4.0"/>')
        doc.add(f'<polygon class="c2-fill" points="{diamond_pts(map_u(u_pk), map_i(i_path(u_pk)), 4.6)}"/>')
    for u_dk in [-0.5, 0.5]:
        doc.add(f'<circle class="panel" stroke="#1b6ca8" stroke-width="2" cx="{fmt(map_u(u_dk))}" cy="{fmt(py0)}" r="3.8"/>')

    # Clean annotations inside plot (pill badges so labels never clash with curves)
    doc.add(f'<text class="xs c1-txt" x="{fmt(map_u(0.0) + 12)}" y="{fmt(map_i(1.0) + 2)}">亮纹峰值 (cos² = 1)</text>')
    x_pd_t = map_u(-1.55)
    y_pd_t = map_i(i_path(-1.55))
    doc.add(f'<line class="guide" x1="{fmt(x_pd_t)}" y1="{fmt(y_pd_t - 4)}" x2="{fmt(x_pd_t)}" y2="334"/>')
    doc.add('<rect class="pill-bg" x="98" y="310" width="136" height="24" rx="7"/>')
    doc.add('<text class="xs c2-txt" x="166" y="326" text-anchor="middle">路径探测 |ψ₁|²+|ψ₂|²</text>')
    # Dark fringe pointer
    x_dk = map_u(0.5)
    doc.add(f'<line class="guide" x1="{fmt(x_dk)}" y1="{fmt(py0 - 5)}" x2="{fmt(x_dk + 40)}" y2="{fmt(py0 - 30)}"/>')
    doc.add(f'<rect class="pill-bg" x="{fmt(x_dk + 40)}" y="{fmt(py0 - 44)}" width="94" height="22" rx="6"/>')
    doc.add(f'<text class="xs c1-txt" x="{fmt(x_dk + 87)}" y="{fmt(py0 - 29)}" text-anchor="middle">暗纹相消 P = 0</text>')

    # --- Right Panel Top: Mach-Zehnder Interferometer Schematic (y=148..336) ---
    doc.add('<rect class="subpanel" x="524" y="148" width="432" height="186" rx="10"/>')

    # Coordinates of optical elements
    bs1 = (608.0, 184.0)
    m1 = (786.0, 184.0)   # Upper-right mirror (arm |0>)
    m2 = (608.0, 268.0)   # Lower-left mirror (arm |1>)
    bs2 = (786.0, 268.0)  # Recombining beam splitter
    d0 = (854.0, 268.0)   # Output detector 0 (right)
    d1 = (786.0, 314.0)   # Output detector 1 (down)

    # Beam paths
    # Input |0>
    doc.add(f'<line class="c1" stroke-width="2.4" x1="558" y1="{fmt(bs1[1])}" x2="{fmt(bs1[0])}" y2="{fmt(bs1[1])}"/>')
    doc.add(arrow_head(586, bs1[1], 1, 0, 6.5, "c1-fill"))
    doc.add('<text class="smb" x="534" y="188" text-anchor="start">|0⟩</text>')

    # Upper arm |0>: BS1 -> M1 -> BS2
    doc.add(f'<line class="c1" stroke-width="2.3" x1="{fmt(bs1[0])}" y1="{fmt(bs1[1])}" x2="{fmt(m1[0])}" y2="{fmt(m1[1])}"/>')
    doc.add(f'<line class="c1" stroke-width="2.3" x1="{fmt(m1[0])}" y1="{fmt(m1[1])}" x2="{fmt(bs2[0])}" y2="{fmt(bs2[1])}"/>')
    doc.add(arrow_head(704, bs1[1], 1, 0, 6.5, "c1-fill"))
    doc.add('<text class="xs c1-txt" x="698" y="173" text-anchor="middle">上臂 |0⟩（振幅 1/√2）</text>')

    # Lower arm |1>: BS1 -> M2 -> Phase Shifter -> BS2
    doc.add(f'<line class="c2" stroke-width="2.3" stroke-dasharray="7 4" x1="{fmt(bs1[0])}" y1="{fmt(bs1[1])}" x2="{fmt(m2[0])}" y2="{fmt(m2[1])}"/>')
    doc.add(f'<line class="c2" stroke-width="2.3" stroke-dasharray="7 4" x1="{fmt(m2[0])}" y1="{fmt(m2[1])}" x2="{fmt(bs2[0])}" y2="{fmt(bs2[1])}"/>')
    doc.add(arrow_head(652, m2[1], 1, 0, 6.5, "c2-fill"))
    doc.add('<text class="xs c2-txt" x="596" y="232" text-anchor="end">下臂 |1⟩</text>')

    # Phase shifter box on lower arm
    doc.add('<rect class="c4-soft" x="668" y="253" width="54" height="30" rx="6"/>')
    doc.add('<text class="smb c4-txt" x="695" y="272" text-anchor="middle">相位 φ</text>')
    doc.add('<text class="xs c4-txt" x="695" y="298" text-anchor="middle">乘 eⁱᵠ</text>')

    # Output beams BS2 -> D0 and BS2 -> D1
    doc.add(f'<line class="c1" stroke-width="2.3" x1="{fmt(bs2[0])}" y1="{fmt(bs2[1])}" x2="{fmt(d0[0])}" y2="{fmt(d0[1])}"/>')
    doc.add(arrow_head(838, d0[1], 1, 0, 6.5, "c1-fill"))
    doc.add(f'<line class="c2" stroke-width="2.3" stroke-dasharray="6 3" x1="{fmt(bs2[0])}" y1="{fmt(bs2[1])}" x2="{fmt(d1[0])}" y2="{fmt(d1[1])}"/>')
    doc.add(arrow_head(d1[0], 304, 0, 1, 6.5, "c2-fill"))

    # Beam splitters (tilted glass plates)
    for (bx, by, blbl, lx, ly) in [(bs1[0], bs1[1], "BS₁", 608, 162), (bs2[0], bs2[1], "BS₂", 814, 248)]:
        doc.add(f'<polygon class="bs-glass" points="{pts_str([(bx-14, by-10), (bx-10, by-14), (bx+14, by+10), (bx+10, by+14)])}"/>')
        doc.add(f'<text class="xs c1-txt" x="{lx}" y="{ly}" text-anchor="middle">{blbl}</text>')

    # Mirrors M1 (top-right) and M2 (bottom-left)
    doc.add(f'<line class="mirror" x1="{fmt(m1[0] - 12)}" y1="{fmt(m1[1] - 12)}" x2="{fmt(m1[0] + 12)}" y2="{fmt(m1[1] + 12)}"/>')
    doc.add('<text class="xs" x="808" y="176">镜 M₁</text>')
    doc.add(f'<line class="mirror" x1="{fmt(m2[0] - 12)}" y1="{fmt(m2[1] - 12)}" x2="{fmt(m2[0] + 12)}" y2="{fmt(m2[1] + 12)}"/>')
    doc.add('<text class="xs" x="594" y="286" text-anchor="end">镜 M₂</text>')

    # Detectors D0 (semicircle facing left) and D1 (semicircle facing up)
    doc.add(f'<path class="det-body" d="M {fmt(d0[0])} {fmt(d0[1] - 13)} A 13 13 0 0 1 {fmt(d0[0])} {fmt(d0[1] + 13)} Z"/>')
    doc.add('<text class="smb c1-txt" x="874" y="264">端口 0</text>')
    doc.add('<text class="xs c1-txt" x="874" y="280">cos²(φ/2)</text>')

    doc.add(f'<path class="det-body" d="M {fmt(d1[0] - 13)} {fmt(d1[1])} A 13 13 0 0 0 {fmt(d1[0] + 13)} {fmt(d1[1])} Z"/>')
    doc.add('<text class="smb c2-txt" x="808" y="322">端口 1：P(1) = sin²(φ/2)</text>')

    # Compact matrix chain note inside MZI box (lower-left corner)
    doc.add(f'<text class="xs" x="536" y="322">矩阵：B·U{sub("φ")}·B|0⟩</text>')

    # --- Right Panel Bottom: Exact MZI Probability Curves P(0), P(1) ---
    mx0, mx1 = 568.0, 944.0
    my0, my1 = 492.0, 382.0  # P=0 bottom, P=1 top

    def map_phi(phi: float) -> float:
        return mx0 + (phi / (2.0 * math.pi)) * (mx1 - mx0)

    def map_p(p_val: float) -> float:
        return my0 - p_val * (my0 - my1)

    # Legend above MZI plot
    doc.add('<line class="c1" stroke-width="2.5" x1="534" y1="358" x2="556" y2="358"/>')
    doc.add('<circle class="c1-fill" cx="545" cy="358" r="3.5"/>')
    doc.add('<text class="xs c1-txt" x="562" y="362">P(0) = cos²(φ/2)</text>')

    doc.add('<line class="c2" stroke-width="2.4" stroke-dasharray="6 3" x1="680" y1="358" x2="702" y2="358"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(691, 358, 4.0)}"/>')
    doc.add('<text class="xs c2-txt" x="708" y="362">P(1) = sin²(φ/2)</text>')

    doc.add('<line class="guide" x1="826" y1="358" x2="846" y2="358"/>')
    doc.add('<text class="xs" x="852" y="362">路径探测 0.5</text>')

    # Grid & ticks
    for p_tk in [0.0, 0.5, 1.0]:
        yp = map_p(p_tk)
        cls_g = "guide" if p_tk == 0.5 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(mx0)}" y1="{fmt(yp)}" x2="{fmt(mx1)}" y2="{fmt(yp)}"/>')
        doc.add(f'<text class="sm" x="{fmt(mx0 - 8)}" y="{fmt(yp + 4)}" text-anchor="end">{p_tk:.1f}</text>')
    for phi_v, phi_lbl in [(0.0, "0"), (0.5 * math.pi, "π/2"), (math.pi, "π"), (1.5 * math.pi, "3π/2"), (2.0 * math.pi, "2π")]:
        xp = map_phi(phi_v)
        doc.add(f'<line class="grid" x1="{fmt(xp)}" y1="{fmt(my1)}" x2="{fmt(xp)}" y2="{fmt(my0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xp)}" y="{fmt(my0 + 18)}" text-anchor="middle">{phi_lbl}</text>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(mx0)}" y1="{fmt(my0)}" x2="{fmt(mx1 + 8)}" y2="{fmt(my0)}"/>')
    doc.add(arrow_head(mx1 + 8, my0, 1, 0, 7.0))
    doc.add(f'<line class="axis" x1="{fmt(mx0)}" y1="{fmt(my0)}" x2="{fmt(mx0)}" y2="{fmt(my1 - 10)}"/>')
    doc.add(arrow_head(mx0, my1 - 10, 0, -1, 7.0))
    doc.add(f'<text class="sm" x="{fmt(0.5 * (mx0 + mx1))}" y="534" text-anchor="middle">相对相位 φ (rad)</text>')
    doc.add(
        f'<text class="sm" x="526" y="{fmt(0.5 * (my0 + my1))}" text-anchor="middle" '
        f'transform="rotate(-90 526 {fmt(0.5 * (my0 + my1))})">端口概率 P (无量纲)</text>'
    )

    # Exact MZI curves
    n_m = 181
    p0_pts = [(map_phi(2.0 * math.pi * i / (n_m - 1)), map_p(mzi_probs(2.0 * math.pi * i / (n_m - 1))[0])) for i in range(n_m)]
    p1_pts = [(map_phi(2.0 * math.pi * i / (n_m - 1)), map_p(mzi_probs(2.0 * math.pi * i / (n_m - 1))[1])) for i in range(n_m)]
    doc.add(f'<path class="c1" stroke-width="2.6" d="{path_from_points(p0_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.4" stroke-dasharray="8 5" d="{path_from_points(p1_pts)}"/>')

    for phi_mk in [0.0, 0.5 * math.pi, math.pi, 1.5 * math.pi, 2.0 * math.pi]:
        p0_v, p1_v = mzi_probs(phi_mk)
        doc.add(f'<circle class="c1-fill" cx="{fmt(map_phi(phi_mk))}" cy="{fmt(map_p(p0_v))}" r="4.0"/>')
        doc.add(f'<polygon class="c2-fill" points="{diamond_pts(map_phi(phi_mk), map_p(p1_v), 4.6)}"/>')

    return doc.render(), {"mzi_p0_at_pi3": mzi_probs(math.pi / 3.0)[0], "slit_coh_zero": i_coh(0.5)}


# ---------------------------------------------------------------------------
# Figure 3: Ch 02 — Bloch x-z half-angle Ry(theta) + equator Rz(phi), T, S, Z
# ---------------------------------------------------------------------------
def build_fig3_rotation_half_angle() -> tuple[str, dict[str, float]]:
    def ry(theta: float) -> list[list[complex]]:
        c, s = math.cos(theta / 2.0), math.sin(theta / 2.0)
        return [[complex(c), complex(-s)], [complex(s), complex(c)]]

    def rz(phi: float) -> list[list[complex]]:
        return [[cmath.exp(-0.5j * phi), 0j], [0j, cmath.exp(0.5j * phi)]]

    def bloch_xyz(psi: list[complex]) -> tuple[float, float, float]:
        a, b = psi[0], psi[1]
        rx = 2.0 * (a.conjugate() * b).real
        ry_v = 2.0 * (a.conjugate() * b).imag
        rz_v = abs(a) ** 2 - abs(b) ** 2
        return rx, ry_v, rz_v

    ket0: list[complex] = [1.0 + 0j, 0j]
    inv_s2 = 1.0 / math.sqrt(2.0)
    ket_plus: list[complex] = [complex(inv_s2), complex(inv_s2)]

    # Exact assertions for Ry(theta)|0> half-angle -> full Bloch angle theta
    for th in [0.0, math.pi / 3.0, math.pi / 2.0, math.pi, 2.0 * math.pi]:
        psi = mat_vec(ry(th), ket0)
        bx, by, bz = bloch_xyz(psi)
        assert abs(bx - math.sin(th)) < TOL
        assert abs(by) < TOL
        assert abs(bz - math.cos(th)) < TOL

    # 2*pi full Bloch turn gives -I in state space
    ry_2pi = ry(2.0 * math.pi)
    assert max_mat_diff(ry_2pi, [[-1.0 + 0j, 0j], [0j, -1.0 + 0j]]) < TOL

    # Exact assertions for Rz(phi)|+> and T, S, Z gates
    t_gate: list[list[complex]] = [[1.0 + 0j, 0j], [0j, cmath.exp(1j * math.pi / 4.0)]]
    s_gate: list[list[complex]] = [[1.0 + 0j, 0j], [0j, 1j]]
    z_gate: list[list[complex]] = [[1.0 + 0j, 0j], [0j, -1.0 + 0j]]
    assert max_mat_diff(mat_mul(t_gate, t_gate), s_gate) < TOL
    assert max_mat_diff(mat_mul(s_gate, s_gate), z_gate) < TOL
    # Global-phase exact match with Rz
    assert max_mat_diff(
        [[cmath.exp(1j * math.pi / 8.0) * v for v in row] for row in rz(math.pi / 4.0)],
        t_gate,
    ) < TOL
    assert max_mat_diff(
        [[cmath.exp(1j * math.pi / 4.0) * v for v in row] for row in rz(math.pi / 2.0)],
        s_gate,
    ) < TOL
    for ph in [0.0, math.pi / 4.0, math.pi / 2.0, math.pi, -math.pi / 2.0]:
        psi_eq = mat_vec(rz(ph), ket_plus)
        bx, by, bz = bloch_xyz(psi_eq)
        assert abs(bx - math.cos(ph)) < TOL
        assert abs(by - math.sin(ph)) < TOL
        assert abs(bz) < TOL

    doc = SvgDoc(
        title="单比特旋转的半角几何：Ry(θ) 旋转角与 Rz(φ) 赤道相位门",
        desc=(
            "左面板绘制 Bloch 球 x–z 截面圆：从北极 |0⟩ 施加 Ry(θ) 后振幅取半角 cos(θ/2)、sin(θ/2)，"
            "Bloch 向量却绕 +y 轴（指向纸内）顺时针转过整角 θ，依次经过 π/3、π/2(|+⟩)、π(|1⟩)、3π/2(|−⟩)，"
            "转满 2π 回到北极点却给态矢量乘上 −1（注：门旋转角 θ∈[0,2π]，而 Bloch 极角仅取 [0,π]）。"
            "右面板俯视赤道 x–y 截面，展示 Rz(φ) 与 T(π/4)、S(π/2)、Z(π) 门位置。"
        ),
    )
    doc.add_header(
        f"单比特旋转的半角几何：R{sub('y')}(θ) 旋转角与 R{sub('z')}(φ) 赤道相位门",
        "态空间矩阵以半角 θ/2、φ/2 演化，在三维 Bloch 球上转过整角 θ、φ；转满 2π 回到原球面点但给态矢量乘 −1",
        raw_title=True,
    )

    doc.add_panel(28, 96, 464, 456, f"Bloch 球 x–z 截面：R{sub('y')}(θ)|0⟩ = cos(θ/2)|0⟩ + sin(θ/2)|1⟩", raw_heading=True)
    doc.add_panel(508, 96, 464, 456, f"赤道 x–y 截面（俯视 +z）：R{sub('z')}(φ) 与 T、S、Z 相位门", raw_heading=True)

    # --- Left Panel: Bloch x-z cross section (+z up, +x right, +y into page) ---
    cx1, cy1, r1 = 256.0, 306.0, 112.0
    doc.add(f'<circle class="bloch-circle" cx="{fmt(cx1)}" cy="{fmt(cy1)}" r="{fmt(r1)}"/>')

    # Coordinate hand badge
    doc.add('<rect class="pill" x="42" y="144" width="114" height="22" rx="11"/>')
    doc.add('<text class="xs" x="99" y="159" text-anchor="middle">⊗ +y 轴指向纸内</text>')

    # Axes (+z up, +x right)
    doc.add(f'<line class="axis" x1="{fmt(cx1)}" y1="{fmt(cy1 + r1 + 22)}" x2="{fmt(cx1)}" y2="{fmt(cy1 - r1 - 24)}"/>')
    doc.add(arrow_head(cx1, cy1 - r1 - 24, 0, -1, 7.5))
    doc.add(f'<line class="axis" x1="{fmt(cx1 - r1 - 22)}" y1="{fmt(cy1)}" x2="{fmt(cx1 + r1 + 24)}" y2="{fmt(cy1)}"/>')
    doc.add(arrow_head(cx1 + r1 + 24, cy1, 1, 0, 7.5))

    doc.add(f'<text class="smb" x="{fmt(cx1)}" y="{fmt(cy1 - r1 - 32)}" text-anchor="middle">+z：|0⟩ (θ = 0)</text>')
    doc.add(f'<text class="smb" x="{fmt(cx1)}" y="{fmt(cy1 + r1 + 38)}" text-anchor="middle">−z：|1⟩ (θ = π)</text>')
    doc.add(f'<text class="smb" x="{fmt(cx1 + r1 + 30)}" y="{fmt(cy1 - 3)}">+x：|+⟩</text>')
    doc.add(f'<text class="xs" x="{fmt(cx1 + r1 + 30)}" y="{fmt(cy1 + 13)}">(θ = π/2)</text>')
    doc.add(f'<text class="smb" x="{fmt(cx1 - r1 - 28)}" y="{fmt(cy1 - 3)}" text-anchor="end">−x：|−⟩</text>')
    doc.add(f'<text class="xs" x="{fmt(cx1 - r1 - 24)}" y="{fmt(cy1 + 13)}" text-anchor="end">(转角 θ = 3π/2)</text>')

    # Example state vector at theta = pi/3 (60 deg from +z toward +x)
    th_ex = math.pi / 3.0
    ex_x = cx1 + r1 * math.sin(th_ex)
    ex_y = cy1 - r1 * math.cos(th_ex)

    # Projection guides for r_x = sin(theta), r_z = cos(theta)
    doc.add(f'<line class="guide" x1="{fmt(ex_x)}" y1="{fmt(ex_y)}" x2="{fmt(cx1)}" y2="{fmt(ex_y)}"/>')
    doc.add(f'<line class="guide" x1="{fmt(ex_x)}" y1="{fmt(ex_y)}" x2="{fmt(ex_x)}" y2="{fmt(cy1)}"/>')
    doc.add(f'<text class="xs c1-txt" x="{fmt(cx1 - 8)}" y="{fmt(ex_y + 4)}" text-anchor="end">cos θ</text>')
    doc.add(f'<text class="xs c1-txt" x="{fmt(ex_x - 10)}" y="{fmt(cy1 + 16)}" text-anchor="middle">sin θ</text>')

    # Polar angle arc from +z (math pi/2) to pi/2 - th_ex
    arc_th = math_arc_points(cx1, cy1, 46.0, math.pi / 2.0, math.pi / 2.0 - th_ex, 22)
    doc.add(f'<path class="c1" stroke-width="2.0" d="{path_from_points(arc_th)}"/>')
    doc.add(
        arrow_head(
            arc_th[-1][0], arc_th[-1][1],
            arc_th[-1][0] - arc_th[-2][0], arc_th[-1][1] - arc_th[-2][1],
            6.5, "c1-fill",
        )
    )
    doc.add(f'<text class="smb c1-txt" x="{fmt(cx1 + 16)}" y="{fmt(cy1 - 24)}">θ</text>')

    # Outer milestone arc: pi/2 -> pi (Q4, dashed coral red)
    arc_q4 = math_arc_points(cx1, cy1, r1 + 12.0, -0.06, -math.pi / 2.0 + 0.08, 24)
    doc.add(f'<path class="c2" stroke-width="2.0" stroke-dasharray="6 4" d="{path_from_points(arc_q4)}"/>')
    doc.add(
        arrow_head(
            arc_q4[-1][0], arc_q4[-1][1],
            arc_q4[-1][0] - arc_q4[-2][0], arc_q4[-1][1] - arc_q4[-2][1],
            6.5, "c2-fill",
        )
    )
    doc.add('<text class="xs c2-txt" x="358" y="408">θ = π → |1⟩</text>')
    doc.add('<text class="xs c2-txt" x="358" y="424">(振幅半角 π/2)</text>')

    # Outer return arc on left half: pi -> 2*pi (dotted green/slate showing 2*pi -> -I)
    arc_2pi = math_arc_points(cx1, cy1, r1 + 12.0, -math.pi / 2.0 - 0.12, -1.5 * math.pi + 0.12, 36)
    doc.add(f'<path class="c4" stroke-width="1.8" stroke-dasharray="3 4" d="{path_from_points(arc_2pi)}"/>')
    doc.add(
        arrow_head(
            arc_2pi[-1][0], arc_2pi[-1][1],
            arc_2pi[-1][0] - arc_2pi[-2][0], arc_2pi[-1][1] - arc_2pi[-2][1],
            6.5, "c4-fill",
        )
    )
    doc.add('<text class="xs c4-txt" x="150" y="206" text-anchor="end">转满 θ = 2π 回北极</text>')
    doc.add(f'<text class="xs c4-txt" x="150" y="222" text-anchor="end">R{sub("y")}(2π)|0⟩ = −|0⟩</text>')

    # Vector arrow for R_y(theta)|0>
    doc.add(f'<line class="c1" stroke-width="2.8" x1="{fmt(cx1)}" y1="{fmt(cy1)}" x2="{fmt(ex_x)}" y2="{fmt(ex_y)}"/>')
    doc.add(arrow_head(ex_x, ex_y, ex_x - cx1, ex_y - cy1, 8.5, "c1-fill"))

    # Milestone points on circle (distinct shapes)
    doc.add(f'<circle class="c1-fill" cx="{fmt(cx1)}" cy="{fmt(cy1 - r1)}" r="5.0"/>')
    doc.add(f'<circle class="c1-fill" cx="{fmt(ex_x)}" cy="{fmt(ex_y)}" r="5.0"/>')
    doc.add(f'<polygon class="c3-fill" points="{diamond_pts(cx1 + r1, cy1, 5.8)}"/>')
    doc.add(f'<rect class="c2-fill" x="{fmt(cx1 - 5)}" y="{fmt(cy1 + r1 - 5)}" width="10" height="10" rx="1.5"/>')

    # Label for R_y(theta)|0>
    doc.add(f'<text class="smb c1-txt" x="{fmt(ex_x + 10)}" y="{fmt(ex_y - 16)}">R{sub("y")}(θ)|0⟩</text>')
    doc.add(f'<text class="xs c1-txt" x="{fmt(ex_x + 10)}" y="{fmt(ex_y)}">球面角 θ = π/3</text>')
    doc.add(f'<text class="xs c1-txt" x="{fmt(ex_x + 10)}" y="{fmt(ex_y + 15)}">振幅角 θ/2 = π/6</text>')

    # Bottom explanation box inside left panel
    doc.add('<rect class="note" x="42" y="476" width="436" height="62" rx="10"/>')
    doc.add('<text class="smb" x="56" y="497">半角机制：正交态 |0⟩, |1⟩ 态空间夹 90°，Bloch 球面成 180°</text>')
    doc.add(f'<text class="xs" x="56" y="516">r{sub("x")} = 2cos(θ/2)sin(θ/2) = sin θ，r{sub("z")} = cos²(θ/2)−sin²(θ/2) = cos θ</text>')
    doc.add('<text class="xs" x="56" y="532">门旋转角 θ ∈ [0, 2π] (rad)；Bloch 极角仅取 θ ∈ [0, π]（坐标无量纲）</text>')

    # --- Right Panel: Equatorial x-y plane (looking down from +z, CCW = +phi) ---
    cx2, cy2, r2 = 740.0, 306.0, 110.0
    doc.add(f'<circle class="bloch-circle" cx="{fmt(cx2)}" cy="{fmt(cy2)}" r="{fmt(r2)}"/>')

    # Coordinate hand badge
    doc.add('<rect class="pill" x="522" y="144" width="114" height="22" rx="11"/>')
    doc.add('<text class="xs" x="579" y="159" text-anchor="middle">⊙ +z 轴指向纸外</text>')

    # Axes (+x right, +y up)
    doc.add(f'<line class="axis" x1="{fmt(cx2 - r2 - 22)}" y1="{fmt(cy2)}" x2="{fmt(cx2 + r2 + 24)}" y2="{fmt(cy2)}"/>')
    doc.add(arrow_head(cx2 + r2 + 24, cy2, 1, 0, 7.5))
    doc.add(f'<line class="axis" x1="{fmt(cx2)}" y1="{fmt(cy2 + r2 + 22)}" x2="{fmt(cx2)}" y2="{fmt(cy2 - r2 - 24)}"/>')
    doc.add(arrow_head(cx2, cy2 - r2 - 24, 0, -1, 7.5))

    doc.add(f'<text class="smb" x="{fmt(cx2 + r2 + 28)}" y="{fmt(cy2 - 3)}">+x：|+⟩</text>')
    doc.add(f'<text class="xs" x="{fmt(cx2 + r2 + 28)}" y="{fmt(cy2 + 13)}">(φ = 0)</text>')
    doc.add(f'<text class="smb c2-txt" x="{fmt(cx2 - r2 - 28)}" y="{fmt(cy2 - 3)}" text-anchor="end">−x：|−⟩</text>')
    doc.add(f'<text class="xs c2-txt" x="{fmt(cx2 - r2 - 28)}" y="{fmt(cy2 + 13)}" text-anchor="end">Z|+⟩ (π)</text>')
    doc.add(f'<text class="smb c3-txt" x="{fmt(cx2)}" y="{fmt(cy2 - r2 - 32)}" text-anchor="middle">+y：|+i⟩ = S|+⟩ (φ = π/2)</text>')
    doc.add(f'<text class="smb" x="{fmt(cx2)}" y="{fmt(cy2 + r2 + 38)}" text-anchor="middle">−y：|−i⟩ = S†|+⟩ (φ = −π/2)</text>')

    # Exact gate positions on equator (cos phi, sin phi)
    pt_0 = (cx2 + r2, cy2)
    pt_t = (cx2 + r2 * math.cos(math.pi / 4.0), cy2 - r2 * math.sin(math.pi / 4.0))
    pt_s = (cx2, cy2 - r2)
    pt_z = (cx2 - r2, cy2)
    pt_td = (cx2 + r2 * math.cos(-math.pi / 4.0), cy2 - r2 * math.sin(-math.pi / 4.0))

    # Radial lines to T, S, Z
    doc.add(f'<line class="c4" stroke-width="2.4" x1="{fmt(cx2)}" y1="{fmt(cy2)}" x2="{fmt(pt_t[0])}" y2="{fmt(pt_t[1])}"/>')
    doc.add(f'<line class="c3" stroke-width="2.3" stroke-dasharray="6 3" x1="{fmt(cx2)}" y1="{fmt(cy2)}" x2="{fmt(pt_s[0])}" y2="{fmt(pt_s[1])}"/>')
    doc.add(f'<line class="c2" stroke-width="2.3" stroke-dasharray="10 3 2 3" x1="{fmt(cx2)}" y1="{fmt(cy2)}" x2="{fmt(pt_z[0])}" y2="{fmt(pt_z[1])}"/>')
    doc.add(f'<line class="guide" x1="{fmt(cx2)}" y1="{fmt(cy2)}" x2="{fmt(pt_td[0])}" y2="{fmt(pt_td[1])}"/>')

    # Chained CCW rotation arcs at radius 64 px (0 -> pi/4 -> pi/2 -> pi)
    r_arc = 64.0
    arc_t = math_arc_points(cx2, cy2, r_arc, 0.04, math.pi / 4.0 - 0.04, 18)
    doc.add(f'<path class="c4" stroke-width="2.2" d="{path_from_points(arc_t)}"/>')
    doc.add(arrow_head(arc_t[-1][0], arc_t[-1][1], arc_t[-1][0] - arc_t[-2][0], arc_t[-1][1] - arc_t[-2][1], 6.0, "c4-fill"))
    doc.add(f'<text class="xs c4-txt" x="{fmt(cx2 + 78)}" y="{fmt(cy2 - 22)}">+π/4</text>')

    arc_s = math_arc_points(cx2, cy2, r_arc, math.pi / 4.0 + 0.05, math.pi / 2.0 - 0.05, 18)
    doc.add(f'<path class="c3" stroke-width="2.2" stroke-dasharray="5 3" d="{path_from_points(arc_s)}"/>')
    doc.add(arrow_head(arc_s[-1][0], arc_s[-1][1], arc_s[-1][0] - arc_s[-2][0], arc_s[-1][1] - arc_s[-2][1], 6.0, "c3-fill"))
    doc.add(f'<text class="xs c3-txt" x="{fmt(cx2 + 28)}" y="{fmt(cy2 - 74)}">+π/4</text>')

    arc_z = math_arc_points(cx2, cy2, r_arc, math.pi / 2.0 + 0.06, math.pi - 0.06, 26)
    doc.add(f'<path class="c2" stroke-width="2.2" stroke-dasharray="8 4" d="{path_from_points(arc_z)}"/>')
    doc.add(arrow_head(arc_z[-1][0], arc_z[-1][1], arc_z[-1][0] - arc_z[-2][0], arc_z[-1][1] - arc_z[-2][1], 6.5, "c2-fill"))
    doc.add(f'<text class="xs c2-txt" x="{fmt(cx2 - 96)}" y="{fmt(cy2 - 96)}" text-anchor="end">再转 +π/2</text>')
    doc.add(f'<text class="xs c2-txt" x="{fmt(cx2 - 96)}" y="{fmt(cy2 - 80)}" text-anchor="end">(累计 φ = π，即 Z)</text>')

    # Distinct markers at each gate
    doc.add(f'<circle class="c1-fill" cx="{fmt(pt_0[0])}" cy="{fmt(pt_0[1])}" r="5.0"/>')
    doc.add(f'<polygon class="c4-fill" points="{triangle_pts(pt_t[0], pt_t[1], 6.0)}"/>')
    doc.add(f'<polygon class="c3-fill" points="{diamond_pts(pt_s[0], pt_s[1], 6.0)}"/>')
    doc.add(f'<rect class="c2-fill" x="{fmt(pt_z[0] - 5)}" y="{fmt(pt_z[1] - 5)}" width="10" height="10" rx="1.5"/>')
    doc.add(f'<circle class="panel" stroke="#7c93a8" stroke-width="2" cx="{fmt(pt_td[0])}" cy="{fmt(pt_td[1])}" r="4.5"/>')
    doc.add(f'<circle class="panel" stroke="#7c93a8" stroke-width="2" cx="{fmt(cx2)}" cy="{fmt(cy2 + r2)}" r="4.5"/>')

    # Gate callouts
    doc.add(f'<text class="smb c4-txt" x="{fmt(pt_t[0] + 10)}" y="{fmt(pt_t[1] - 10)}">T 门 (φ = π/4)</text>')
    doc.add(f'<text class="xs c4-txt" x="{fmt(pt_t[0] + 10)}" y="{fmt(pt_t[1] + 6)}">T = diag(1, e<tspan baseline-shift="super" font-size="72%">iπ/4</tspan>)</text>')
    doc.add(f'<text class="xs" x="{fmt(pt_td[0] + 10)}" y="{fmt(pt_td[1] + 5)}">T† (−π/4)</text>')

    # Bottom explanation box inside right panel
    doc.add('<rect class="note" x="522" y="476" width="436" height="62" rx="10"/>')
    doc.add(f'<text class="smb" x="536" y="497">R{sub("z")}(φ) = diag(e<tspan baseline-shift="super" font-size="72%">−iφ/2</tspan>, e<tspan baseline-shift="super" font-size="72%">+iφ/2</tspan>)，仅差全局相位即 diag(1, e<tspan baseline-shift="super" font-size="72%">iφ</tspan>)</text>')
    doc.add('<text class="xs" x="536" y="516">门递进：T² = S (π/2)，S² = Z (π)；赤道转动不改变计算基概率</text>')
    doc.add(f'<text class="xs" x="536" y="532">坐标 r{sub("x")}, r{sub("y")} 无量纲；方位角 φ 单位为弧度 (rad)</text>')

    return doc.render(), {"ry_2pi_diag": ry_2pi[0][0].real, "t_sq_err": max_mat_diff(mat_mul(t_gate, t_gate), s_gate)}


# ---------------------------------------------------------------------------
# Figure 4: Ch 03 — CHSH cooperative game, measurement angles & bar chart
# ---------------------------------------------------------------------------
def build_fig4_chsh_game() -> tuple[str, dict[str, float]]:
    # 1. Exhaustive classical LHV check over all 2^4 = 16 deterministic strategies
    best_cl_wins = 0
    best_cl_s = 0
    for a0 in (0, 1):
        for a1 in (0, 1):
            for b0 in (0, 1):
                for b1 in (0, 1):
                    a_map = (a0, a1)
                    b_map = (b0, b1)
                    wins = sum(1 for x in (0, 1) for y in (0, 1) if (a_map[x] ^ b_map[y]) == (x & y))
                    pm_a = [1 if v == 0 else -1 for v in a_map]
                    pm_b = [1 if v == 0 else -1 for v in b_map]
                    s_val = pm_a[0] * pm_b[0] + pm_a[0] * pm_b[1] + pm_a[1] * pm_b[0] - pm_a[1] * pm_b[1]
                    best_cl_wins = max(best_cl_wins, wins)
                    best_cl_s = max(best_cl_s, abs(s_val))
    p_win_rand = 0.50
    p_win_cl = best_cl_wins / 4.0
    assert abs(p_win_cl - 0.75) < TOL
    assert best_cl_s == 2

    # 2. Exact 4x4 quantum computation on |Phi+> = (|00> + |11>)/sqrt(2)
    inv_s2 = 1.0 / math.sqrt(2.0)
    z_m: list[list[complex]] = [[1.0 + 0j, 0j], [0j, -1.0 + 0j]]
    x_m: list[list[complex]] = [[0j, 1.0 + 0j], [1.0 + 0j, 0j]]
    id2: list[list[complex]] = [[1.0 + 0j, 0j], [0j, 1.0 + 0j]]
    b0_m = [[inv_s2 * (z_m[i][j] + x_m[i][j]) for j in range(2)] for i in range(2)]
    b1_m = [[inv_s2 * (z_m[i][j] - x_m[i][j]) for j in range(2)] for i in range(2)]
    assert max_mat_diff(mat_mul(b0_m, b0_m), id2) < TOL
    assert max_mat_diff(mat_mul(b1_m, b1_m), id2) < TOL

    phi_plus: list[complex] = [complex(inv_s2), 0j, 0j, complex(inv_s2)]
    a_ops = [z_m, x_m]
    b_ops = [b0_m, b1_m]
    corrs: dict[tuple[int, int], float] = {}
    for x in (0, 1):
        for y in (0, 1):
            op = kron(a_ops[x], b_ops[y])
            v = mat_vec(op, phi_plus)
            exp_val = sum(phi_plus[k].conjugate() * v[k] for k in range(4))
            assert abs(exp_val.imag) < TOL
            corrs[(x, y)] = exp_val.real

    assert abs(corrs[(0, 0)] - inv_s2) < TOL
    assert abs(corrs[(0, 1)] - inv_s2) < TOL
    assert abs(corrs[(1, 0)] - inv_s2) < TOL
    assert abs(corrs[(1, 1)] + inv_s2) < TOL
    s_quantum = corrs[(0, 0)] + corrs[(0, 1)] + corrs[(1, 0)] - corrs[(1, 1)]
    p_win_q = 0.5 + s_quantum / 8.0
    assert abs(s_quantum - 2.0 * math.sqrt(2.0)) < TOL
    assert abs(p_win_q - math.cos(math.pi / 8.0) ** 2) < TOL
    assert abs(p_win_q - (2.0 + math.sqrt(2.0)) / 4.0) < TOL

    doc = SvgDoc(
        title="CHSH 合作博弈规则、最优测量角与赢率上限对比",
        desc=(
            "左面板展示 CHSH 合作博弈流程（裁判向隔绝的 Alice、Bob 发随机比特 x, y，赢条件 a ⊕ b = x·y）"
            "及量子最优策略的四组 Bloch x–z 测量轴（Alice 取 0 与 π/2，Bob 取 +π/4 与 −π/4）。"
            "右面板以精确柱状图对比随机猜 50.00%（S=0）、经典局域隐变量上限 75.00%（S=2）与共享 Bell 态量子策略 "
            "cos²(π/8) ≈ 85.36%（Tsirelson 界 S = 2√2）。"
        ),
    )
    doc.add_header(
        "CHSH 合作博弈：最优测量角与经典 75% 及量子 85.36% 上限",
        "左：禁止通信的 Alice/Bob 共享 Bell 态 |Φ⁺⟩ 与四组 Bloch x–z 测量轴；右：随机、经典上限与量子 Tsirelson 界精确对比",
    )

    doc.add_panel(28, 96, 504, 456, "CHSH 博弈规则与最优测量角（Bloch x–z 平面）")
    doc.add_panel(548, 96, 424, 456, "无通信条件下的赢率上限精确对比")

    # --- Left Panel Top: Cooperative Game Protocol Diagram (y=146..328) ---
    # Referee box
    doc.add('<rect class="pill" x="210" y="146" width="140" height="36" rx="9"/>')
    doc.add('<text class="smb" x="280" y="162" text-anchor="middle">裁判 (Referee)</text>')
    doc.add('<text class="xs" x="280" y="176" text-anchor="middle">均匀随机发 x, y ∈ {0,1}</text>')

    # Arrows Referee -> Alice and Bob
    doc.add('<line class="axis" stroke-width="1.6" x1="210" y1="168" x2="148" y2="198"/>')
    doc.add(arrow_head(148, 198, -62, 30, 7.0))
    doc.add('<text class="smb c1-txt" x="166" y="176" text-anchor="end">输入 x</text>')

    doc.add('<line class="axis" stroke-width="1.6" x1="350" y1="168" x2="412" y2="198"/>')
    doc.add(arrow_head(412, 198, 62, 30, 7.0))
    doc.add('<text class="smb c3-txt" x="394" y="176" text-anchor="start">输入 y</text>')

    # Alice card
    doc.add('<rect class="c1-soft" x="42" y="200" width="168" height="86" rx="10"/>')
    doc.add('<text class="lblb c1-txt" x="126" y="220" text-anchor="middle">Alice（输出 a）</text>')
    doc.add('<text class="xs" x="54" y="242">x = 0：测 A₀ = Z (0)</text>')
    doc.add('<text class="xs" x="54" y="261">x = 1：测 A₁ = X (π/2)</text>')
    doc.add('<text class="xs c1-txt" x="54" y="278">本征值 ±1 对应 a ∈ {0,1}</text>')

    # Bob card
    doc.add('<rect class="c3-soft" x="350" y="200" width="168" height="86" rx="10"/>')
    doc.add('<text class="lblb c3-txt" x="434" y="220" text-anchor="middle">Bob（输出 b）</text>')
    doc.add('<text class="xs" x="362" y="242">y = 0：B₀=(Z+X)/√2 (+π/4)</text>')
    doc.add('<text class="xs" x="362" y="261">y = 1：B₁=(Z−X)/√2 (−π/4)</text>')
    doc.add('<text class="xs c3-txt" x="362" y="278">本征值 ±1 对应 b ∈ {0,1}</text>')

    # Isolation wall & pre-shared entanglement link between Alice and Bob
    doc.add('<line class="c2" stroke-width="1.8" stroke-dasharray="5 4" x1="280" y1="194" x2="280" y2="254"/>')
    doc.add('<rect class="c2-soft" x="235" y="210" width="90" height="24" rx="12"/>')
    doc.add('<text class="xs c2-txt" x="280" y="226" text-anchor="middle">✕ 禁止通信</text>')

    doc.add('<line class="c4" stroke-width="2.0" stroke-dasharray="4 3" x1="210" y1="272" x2="350" y2="272"/>')
    doc.add('<rect class="c4-soft" x="232" y="260" width="96" height="24" rx="12"/>')
    doc.add('<text class="xs c4-txt" x="280" y="276" text-anchor="middle">共享 |Φ⁺⟩</text>')

    # Win condition bar
    doc.add('<rect class="note" x="42" y="296" width="476" height="30" rx="8"/>')
    doc.add('<text class="smb" x="280" y="315" text-anchor="middle">赢条件：a ⊕ b = x · y（仅 (1,1) 要异号 a ≠ b，其余三组要同号 a = b）</text>')

    # --- Left Panel Bottom: 4 Measurement Axes (Bloch x-z) + Correlation Table ---
    ccx, ccy, ccr = 148.0, 452.0, 62.0
    doc.add(f'<circle class="unit-circle" cx="{fmt(ccx)}" cy="{fmt(ccy)}" r="{fmt(ccr)}"/>')
    # Faint reference axes (+z up, +x right)
    doc.add(f'<line class="grid" x1="{fmt(ccx - ccr - 8)}" y1="{fmt(ccy)}" x2="{fmt(ccx + ccr + 12)}" y2="{fmt(ccy)}"/>')
    doc.add(f'<line class="grid" x1="{fmt(ccx)}" y1="{fmt(ccy + ccr + 8)}" x2="{fmt(ccx)}" y2="{fmt(ccy - ccr - 12)}"/>')

    # Helper for Bloch polar angle alpha from +z clockwise toward +x
    def bloch_pt(alpha_rad: float, radius: float) -> tuple[float, float]:
        return (ccx + radius * math.sin(alpha_rad), ccy - radius * math.cos(alpha_rad))

    # Alice A0 (0) & A1 (pi/2): solid blue + circles
    pa0 = bloch_pt(0.0, ccr)
    pa1 = bloch_pt(math.pi / 2.0, ccr)
    pb0 = bloch_pt(math.pi / 4.0, ccr)
    pb1 = bloch_pt(-math.pi / 4.0, ccr)

    # Small angle arcs between A0 and B0 (+pi/4), A0 and B1 (-pi/4)
    arc_ab0 = math_arc_points(ccx, ccy, 30.0, math.pi / 2.0, math.pi / 4.0, 14)
    doc.add(f'<path class="c4" stroke-width="1.6" d="{path_from_points(arc_ab0)}"/>')
    arc_ab1 = math_arc_points(ccx, ccy, 30.0, math.pi / 2.0, 3.0 * math.pi / 4.0, 14)
    doc.add(f'<path class="c4" stroke-width="1.6" d="{path_from_points(arc_ab1)}"/>')
    doc.add(f'<text class="xs c4-txt" x="{fmt(ccx + 10)}" y="{fmt(ccy - 38)}">π/4</text>')
    doc.add(f'<text class="xs c4-txt" x="{fmt(ccx - 10)}" y="{fmt(ccy - 38)}" text-anchor="end">π/4</text>')

    # Draw the 4 measurement axes
    doc.add(f'<line class="c1" stroke-width="2.6" x1="{fmt(ccx)}" y1="{fmt(ccy)}" x2="{fmt(pa0[0])}" y2="{fmt(pa0[1])}"/>')
    doc.add(arrow_head(pa0[0], pa0[1], 0, -1, 7.5, "c1-fill"))
    doc.add(f'<circle class="c1-fill" cx="{fmt(pa0[0])}" cy="{fmt(pa0[1])}" r="4.0"/>')

    doc.add(f'<line class="c1" stroke-width="2.6" x1="{fmt(ccx)}" y1="{fmt(ccy)}" x2="{fmt(pa1[0])}" y2="{fmt(pa1[1])}"/>')
    doc.add(arrow_head(pa1[0], pa1[1], 1, 0, 7.5, "c1-fill"))
    doc.add(f'<circle class="c1-fill" cx="{fmt(pa1[0])}" cy="{fmt(pa1[1])}" r="4.0"/>')

    doc.add(f'<line class="c3" stroke-width="2.5" stroke-dasharray="6 3" x1="{fmt(ccx)}" y1="{fmt(ccy)}" x2="{fmt(pb0[0])}" y2="{fmt(pb0[1])}"/>')
    doc.add(arrow_head(pb0[0], pb0[1], pb0[0] - ccx, pb0[1] - ccy, 7.5, "c3-fill"))
    doc.add(f'<polygon class="c3-fill" points="{diamond_pts(pb0[0], pb0[1], 4.8)}"/>')

    doc.add(f'<line class="c3" stroke-width="2.5" stroke-dasharray="9 3 2 3" x1="{fmt(ccx)}" y1="{fmt(ccy)}" x2="{fmt(pb1[0])}" y2="{fmt(pb1[1])}"/>')
    doc.add(arrow_head(pb1[0], pb1[1], pb1[0] - ccx, pb1[1] - ccy, 7.5, "c3-fill"))
    doc.add(f'<rect class="c3-fill" x="{fmt(pb1[0] - 4.2)}" y="{fmt(pb1[1] - 4.2)}" width="8.4" height="8.4" rx="1.2"/>')

    # Axis tip labels (carefully spaced)
    doc.add(f'<text class="smb c1-txt" x="{fmt(pa0[0])}" y="{fmt(pa0[1] - 12)}" text-anchor="middle">A₀ (0)</text>')
    doc.add(f'<text class="smb c1-txt" x="{fmt(pa1[0] + 10)}" y="{fmt(pa1[1] + 4)}">A₁ (π/2)</text>')
    doc.add(f'<text class="smb c3-txt" x="{fmt(pb0[0] + 8)}" y="{fmt(pb0[1] - 4)}">B₀ (+π/4)</text>')
    doc.add(f'<text class="smb c3-txt" x="{fmt(pb1[0] - 8)}" y="{fmt(pb1[1] - 4)}" text-anchor="end">B₁ (−π/4)</text>')
    doc.add(f'<text class="xs" x="{fmt(ccx)}" y="536" text-anchor="middle">Bloch x–z 测量角 (rad)</text>')

    # Right sub-panel inside Left Panel: 4 correlation rows
    doc.add('<rect class="subpanel" x="288" y="340" width="230" height="198" rx="10"/>')
    doc.add('<text class="smb" x="302" y="362">四组相关 E(x,y) = cos(Δθ)</text>')
    doc.add('<line class="grid" x1="296" y1="370" x2="510" y2="370"/>')
    rows_chsh = [
        ("(0,0) 同号", "Δθ = π/4", "+1/√2", "c3-txt"),
        ("(0,1) 同号", "Δθ = π/4", "+1/√2", "c3-txt"),
        ("(1,0) 同号", "Δθ = π/4", "+1/√2", "c3-txt"),
        ("(1,1) 异号", "Δθ = 3π/4", "−1/√2", "c2-txt"),
    ]
    for idx, (c_xy, c_ang, c_val, c_cls) in enumerate(rows_chsh):
        yr = 392 + idx * 24
        doc.add(f'<text class="xs" x="302" y="{yr}">{c_xy}</text>')
        doc.add(f'<text class="xs" x="378" y="{yr}">{c_ang}</text>')
        doc.add(f'<text class="smb {c_cls}" x="506" y="{yr}" text-anchor="end">{c_val}</text>')
    doc.add('<line class="grid" x1="296" y1="478" x2="510" y2="478"/>')
    doc.add('<text class="smb c1-txt" x="302" y="499">S = 3/√2 − (−1/√2) = 2√2</text>')
    doc.add('<text class="xs" x="302" y="518">四组赢率均等：cos²(π/8) ≈ 85.36%</text>')

    # --- Right Panel: Exact Win-Rate Bar Chart (50%, 75%, 85.36%) ---
    bx0, bx1 = 612.0, 948.0
    by0, by1 = 428.0, 174.0  # 0% bottom, 100% top (height = 254 px)

    def map_pct(p_frac: float) -> float:
        return by0 - p_frac * (by0 - by1)

    # Gridlines & Y-ticks
    for pct in [0, 25, 50, 75, 100]:
        yp = map_pct(pct / 100.0)
        doc.add(f'<line class="grid" x1="{fmt(bx0)}" y1="{fmt(yp)}" x2="{fmt(bx1)}" y2="{fmt(yp)}"/>')
        doc.add(f'<text class="sm" x="{fmt(bx0 - 8)}" y="{fmt(yp + 4)}" text-anchor="end">{pct}%</text>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(bx0)}" y1="{fmt(by0)}" x2="{fmt(bx1 + 6)}" y2="{fmt(by0)}"/>')
    doc.add(f'<line class="axis" x1="{fmt(bx0)}" y1="{fmt(by0)}" x2="{fmt(bx0)}" y2="{fmt(by1 - 12)}"/>')
    doc.add(arrow_head(bx0, by1 - 12, 0, -1, 7.0))
    doc.add(
        f'<text class="sm" x="568" y="{fmt(0.5 * (by0 + by1))}" text-anchor="middle" '
        f'transform="rotate(-90 568 {fmt(0.5 * (by0 + by1))})">博弈平均赢率 p{sub("win")} (%)</text>'
    )

    # Dashed benchmark lines at 75% (CHSH classic) and 85.36% (Tsirelson)
    y_75 = map_pct(p_win_cl)
    y_q = map_pct(p_win_q)
    doc.add(f'<line class="c2" stroke-width="1.4" stroke-dasharray="6 4" x1="{fmt(bx0)}" y1="{fmt(y_75)}" x2="{fmt(bx1)}" y2="{fmt(y_75)}"/>')
    doc.add(f'<line class="c1" stroke-width="1.4" stroke-dasharray="6 4" x1="{fmt(bx0)}" y1="{fmt(y_q)}" x2="{fmt(bx1)}" y2="{fmt(y_q)}"/>')

    # Three exact bars (distinct fill + hatch pattern for monochrome readability)
    bars = [
        (670.0, p_win_rand, "bar-neutral", "url(#hatch-neutral)", "50.00%", "S = 0", "随机猜测", "p = 1/2", "smb"),
        (780.0, p_win_cl, "c2-soft", "url(#hatch-red)", "75.00%", "S ≤ 2", "经典上限", "CHSH (3/4)", "smb c2-txt"),
        (890.0, p_win_q, "c1-soft", "url(#hatch-blue)", "85.36%", "S = 2√2", "量子纠缠", "cos²(π/8)", "smb c1-txt"),
    ]
    bw = 68.0
    for cx_b, frac, fill_cls, hatch_ref, pct_lbl, s_lbl, cat1, cat2, val_cls in bars:
        yt = map_pct(frac)
        bh = by0 - yt
        x_left = cx_b - bw / 2.0
        doc.add(f'<rect class="{fill_cls}" x="{fmt(x_left)}" y="{fmt(yt)}" width="{fmt(bw)}" height="{fmt(bh)}" rx="6"/>')
        doc.add(f'<rect fill="{hatch_ref}" x="{fmt(x_left)}" y="{fmt(yt)}" width="{fmt(bw)}" height="{fmt(bh)}" rx="6"/>')
        # Exact percentage label above bar
        doc.add(f'<text class="{val_cls}" x="{fmt(cx_b)}" y="{fmt(yt - 9)}" text-anchor="middle">{pct_lbl}</text>')
        # Clean pill inside bar for S value
        doc.add(f'<rect class="pill-bg" x="{fmt(cx_b - 28)}" y="{fmt(yt + 16)}" width="56" height="22" rx="6"/>')
        doc.add(f'<text class="xs" x="{fmt(cx_b)}" y="{fmt(yt + 31)}" text-anchor="middle">{s_lbl}</text>')
        # Two-line category label below axis
        doc.add(f'<text class="smb" x="{fmt(cx_b)}" y="{fmt(by0 + 20)}" text-anchor="middle">{cat1}</text>')
        doc.add(f'<text class="xs" x="{fmt(cx_b)}" y="{fmt(by0 + 36)}" text-anchor="middle">{cat2}</text>')

    # Quantum advantage gap bracket between 75% and 85.36% (at x=834, between bar 2 & bar 3)
    xg = 834.0
    doc.add(f'<line class="c3" stroke-width="1.9" x1="{fmt(xg)}" y1="{fmt(y_q + 2)}" x2="{fmt(xg)}" y2="{fmt(y_75 - 2)}"/>')
    doc.add(arrow_head(xg, y_q + 1, 0, -1, 5.5, "c3-fill"))
    doc.add(arrow_head(xg, y_75 - 1, 0, 1, 5.5, "c3-fill"))
    # Callout pill cleanly placed above gap (clear of bar 2 & 3 labels)
    doc.add(f'<line class="guide" x1="{fmt(xg)}" y1="{fmt(y_q)}" x2="{fmt(xg)}" y2="184"/>')
    doc.add('<rect class="c3-soft" x="764" y="160" width="140" height="24" rx="12"/>')
    doc.add('<text class="xs c3-txt" x="834" y="176" text-anchor="middle">高出 10.36 个百分点</text>')

    # Bottom takeaway note inside right panel
    doc.add('<rect class="note" x="564" y="482" width="392" height="56" rx="10"/>')
    doc.add(f'<text class="smb" x="578" y="503">赢率换算：p{sub("win")} = 1/2 + S/8（S = E₀₀ + E₀₁ + E₁₀ − E₁₁）</text>')
    doc.add('<text class="xs" x="578" y="523">局域隐变量上限 |S| ≤ 2 (75%)；量子 Tsirelson 界 |S| ≤ 2√2 (85.36%)</text>')

    return doc.render(), {"p_win_classical": p_win_cl, "p_win_quantum": p_win_q, "S_quantum": s_quantum}


# ---------------------------------------------------------------------------
# Figure 5: Ch 04 — CNOT / CZ / SWAP(=3 CNOT) / Toffoli + Deferred Measurement
# ---------------------------------------------------------------------------
def build_fig5_deferred_measurement() -> tuple[str, dict[str, float]]:
    # 1. Exact 4x4 matrix checks: CNOT_12, CNOT_21, CZ, SWAP
    cnot_12: list[list[complex]] = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ]
    cnot_21: list[list[complex]] = [
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
    ]
    swap_m: list[list[complex]] = [
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ]
    cz_m: list[list[complex]] = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1],
    ]
    # Verify SWAP == CNOT_12 @ CNOT_21 @ CNOT_12
    three_cnot = mat_mul(cnot_12, mat_mul(cnot_21, cnot_12))
    assert max_mat_diff(three_cnot, swap_m) < TOL
    # Verify CZ symmetry and CZ == (I x H) CNOT_12 (I x H)
    assert max_mat_diff(mat_mul(swap_m, mat_mul(cz_m, swap_m)), cz_m) < TOL
    inv_s2 = 1.0 / math.sqrt(2.0)
    id2: list[list[complex]] = [[1, 0], [0, 1]]
    h2: list[list[complex]] = [[inv_s2, inv_s2], [inv_s2, -inv_s2]]
    ih = kron(id2, h2)
    assert max_mat_diff(mat_mul(ih, mat_mul(cnot_12, ih)), cz_m) < TOL

    # 2. Exact 8x8 Toffoli matrix check
    toffoli: list[list[complex]] = [[0j] * 8 for _ in range(8)]
    for idx in range(8):
        x_b, y_b, z_b = (idx >> 2) & 1, (idx >> 1) & 1, idx & 1
        out_idx = (x_b << 2) | (y_b << 1) | (z_b ^ (x_b & y_b))
        toffoli[out_idx][idx] = 1.0 + 0j
    id8 = [[1.0 + 0j if i == j else 0j for j in range(8)] for i in range(8)]
    assert max_mat_diff(mat_mul(mat_dag(toffoli), toffoli), id8) < TOL
    assert toffoli[7][6] == 1.0 and toffoli[6][7] == 1.0

    # 3. Exact density-matrix proof of Principle of Deferred Measurement
    # Arbitrary normalized entangled state |Psi>_AB = |0>|alpha> + |1>|beta>
    raw_psi = [0.45 + 0.2j, -0.3 + 0.15j, 0.5 - 0.1j, 0.35 + 0.52j]
    norm_psi = math.sqrt(sum(abs(c) ** 2 for c in raw_psi))
    psi_ab = [c / norm_psi for c in raw_psi]
    # Arbitrary non-trivial unitary U = Ry(1.1) Rz(0.7)
    th_u, ph_u = 1.1, 0.7
    ry_u = [[complex(math.cos(th_u / 2)), complex(-math.sin(th_u / 2))],
            [complex(math.sin(th_u / 2)), complex(math.cos(th_u / 2))]]
    rz_u = [[cmath.exp(-0.5j * ph_u), 0j], [0j, cmath.exp(0.5j * ph_u)]]
    u_gate = mat_mul(ry_u, rz_u)
    assert max_mat_diff(mat_mul(mat_dag(u_gate), u_gate), id2) < TOL

    p0_proj: list[list[complex]] = [[1, 0], [0, 0]]
    p1_proj: list[list[complex]] = [[0, 0], [0, 1]]
    rho_in = [[psi_ab[i] * psi_ab[j].conjugate() for j in range(4)] for i in range(4)]

    # Path 1: Mid-circuit Z-measurement on A, then classical-controlled U on B
    op_m0 = kron(p0_proj, id2)
    op_m1 = kron(p1_proj, u_gate)
    rho_path1_0 = mat_mul(op_m0, mat_mul(rho_in, mat_dag(op_m0)))
    rho_path1_1 = mat_mul(op_m1, mat_mul(rho_in, mat_dag(op_m1)))
    rho_path1 = [[rho_path1_0[i][j] + rho_path1_1[i][j] for j in range(4)] for i in range(4)]
    p0_path1 = sum(rho_path1_0[i][i].real for i in range(4))

    # Path 2: Quantum C-U = |0><0| x I + |1><1| x U first, then terminal Z-measurement on A
    cu_gate = [[op_m0[i][j] + op_m1[i][j] for j in range(4)] for i in range(4)]
    rho_after_cu = mat_mul(cu_gate, mat_mul(rho_in, mat_dag(cu_gate)))
    m0_only = kron(p0_proj, id2)
    m1_only = kron(p1_proj, id2)
    rho_path2_0 = mat_mul(m0_only, mat_mul(rho_after_cu, mat_dag(m0_only)))
    rho_path2_1 = mat_mul(m1_only, mat_mul(rho_after_cu, mat_dag(m1_only)))
    rho_path2 = [[rho_path2_0[i][j] + rho_path2_1[i][j] for j in range(4)] for i in range(4)]
    p0_path2 = sum(rho_path2_0[i][i].real for i in range(4))

    dm_diff = max_mat_diff(rho_path1, rho_path2)
    assert dm_diff < TOL
    assert abs(p0_path1 - p0_path2) < TOL

    doc = SvgDoc(
        title="多比特核心量子门与延迟测量原理",
        desc=(
            "上面板展示四个多比特核心量子门的标准电路符号与计算基作用（时间从左到右）："
            "CNOT、对称受控相位门 CZ、三 CNOT 交替分解的 SWAP 门以及经典可逆通用的 Toffoli (CCNOT) 门。"
            "下面板比较中段测量后按标签反馈与相干控制后再读标签。"
            "画的是原控制线保留标签的情形。若数据线继续使用，可另设干净记录位。"
        ),
    )
    doc.add_header(
        "多比特核心量子门与延迟测量原理",
        "上：CNOT、CZ、SWAP (= 3 CNOT) 与 Toffoli (CCNOT) 门符号与作用；下：控制位保留读出标签时的延迟测量",
    )

    doc.add_panel(28, 96, 944, 208, "多比特核心量子门：符号、恒等分解与计算基作用（时间从左到右）")
    doc.add_panel(28, 316, 944, 236, "延迟测量原理（Principle of Deferred Measurement）：控制位保留原标签")

    # Helper drawing primitives for quantum circuits
    def draw_cnot(x_c: float, y_ctrl: float, y_targ: float, r_t: float = 10.0) -> None:
        doc.add(f'<line class="wire" x1="{fmt(x_c)}" y1="{fmt(y_ctrl)}" x2="{fmt(x_c)}" y2="{fmt(y_targ)}"/>')
        doc.add(f'<circle class="ctrl" cx="{fmt(x_c)}" cy="{fmt(y_ctrl)}" r="4.6"/>')
        doc.add(f'<circle class="targ" cx="{fmt(x_c)}" cy="{fmt(y_targ)}" r="{fmt(r_t)}"/>')
        doc.add(f'<line class="wire" x1="{fmt(x_c - r_t)}" y1="{fmt(y_targ)}" x2="{fmt(x_c + r_t)}" y2="{fmt(y_targ)}"/>')
        doc.add(f'<line class="wire" x1="{fmt(x_c)}" y1="{fmt(y_targ - r_t)}" x2="{fmt(x_c)}" y2="{fmt(y_targ + r_t)}"/>')

    def draw_swap_x(x_s: float, y_s: float, r_x: float = 5.5) -> None:
        doc.add(f'<line class="wire" x1="{fmt(x_s - r_x)}" y1="{fmt(y_s - r_x)}" x2="{fmt(x_s + r_x)}" y2="{fmt(y_s + r_x)}"/>')
        doc.add(f'<line class="wire" x1="{fmt(x_s - r_x)}" y1="{fmt(y_s + r_x)}" x2="{fmt(x_s + r_x)}" y2="{fmt(y_s - r_x)}"/>')

    def draw_meter(x_left: float, y_center: float, w_m: float = 40.0, h_m: float = 34.0) -> None:
        y_top = y_center - h_m / 2.0
        cx_m = x_left + w_m / 2.0
        doc.add(f'<rect class="c3-soft" x="{fmt(x_left)}" y="{fmt(y_top)}" width="{fmt(w_m)}" height="{fmt(h_m)}" rx="6"/>')
        # Meter dial arc
        arc_pts = math_arc_points(cx_m, y_center + 8.0, 12.0, math.radians(22), math.radians(158), 16)
        doc.add(f'<path class="axis" stroke-width="1.6" d="{path_from_points(arc_pts)}"/>')
        # Meter needle
        nx, ny = cx_m + 10.5, y_center - 7.0
        doc.add(f'<line class="c2" stroke-width="1.8" x1="{fmt(cx_m)}" y1="{fmt(y_center + 8.0)}" x2="{fmt(nx)}" y2="{fmt(ny)}"/>')
        doc.add(arrow_head(nx, ny, nx - cx_m, ny - (y_center + 8.0), 5.0, "c2-fill"))
        doc.add(f'<text class="xs c3-txt" x="{fmt(x_left + w_m - 5)}" y="{fmt(y_top + h_m - 4)}" text-anchor="end">Z</text>')

    # --- Top Panel: 4 Gate Cards (y=144..294) ---
    # Card 1: CNOT (x=42..262)
    doc.add('<rect class="subpanel" x="42" y="144" width="220" height="150" rx="10"/>')
    doc.add('<text class="smb c1-txt" x="152" y="165" text-anchor="middle">CNOT（受控非门）</text>')
    doc.add('<line class="wire" x1="80" y1="196" x2="196" y2="196"/>')
    doc.add('<line class="wire" x1="80" y1="238" x2="196" y2="238"/>')
    draw_cnot(138.0, 196.0, 238.0, 10.5)
    doc.add('<text class="sm" x="72" y="200" text-anchor="end">|x⟩</text>')
    doc.add('<text class="sm" x="72" y="242" text-anchor="end">|y⟩</text>')
    doc.add('<text class="sm" x="204" y="200">|x⟩</text>')
    doc.add('<text class="sm" x="204" y="242">|y⊕x⟩</text>')
    doc.add('<text class="xs" x="152" y="278" text-anchor="middle">|x, y⟩ ↦ |x, y ⊕ x⟩</text>')

    # Card 2: CZ (x=274..494)
    doc.add('<rect class="subpanel" x="274" y="144" width="220" height="150" rx="10"/>')
    doc.add('<text class="smb c1-txt" x="384" y="165" text-anchor="middle">CZ（对称受控相位门）</text>')
    # Left symmetric ●—●
    doc.add('<line class="wire" x1="298" y1="196" x2="366" y2="196"/>')
    doc.add('<line class="wire" x1="298" y1="238" x2="366" y2="238"/>')
    doc.add('<line class="wire" x1="332" y1="196" x2="332" y2="238"/>')
    doc.add('<circle class="ctrl" cx="332" cy="196" r="4.6"/>')
    doc.add('<circle class="ctrl" cx="332" cy="238" r="4.6"/>')
    # Equivalence symbol
    doc.add('<text class="lblb c1-txt" x="384" y="222" text-anchor="middle">≡</text>')
    # Right ●—[Z]
    doc.add('<line class="wire" x1="402" y1="196" x2="478" y2="196"/>')
    doc.add('<line class="wire" x1="402" y1="238" x2="478" y2="238"/>')
    doc.add('<line class="wire" x1="440" y1="196" x2="440" y2="224"/>')
    doc.add('<circle class="ctrl" cx="440" cy="196" r="4.6"/>')
    doc.add('<rect class="c1-soft" x="426" y="224" width="28" height="28" rx="5"/>')
    doc.add('<text class="gate-txt" x="440" y="243" text-anchor="middle">Z</text>')
    doc.add('<text class="xs" x="384" y="278" text-anchor="middle">|x, y⟩ ↦ (−1)ˣʸ|x, y⟩（两线对称）</text>')

    # Card 3: SWAP = 3 CNOT (x=506..726)
    doc.add('<rect class="subpanel" x="506" y="144" width="220" height="150" rx="10"/>')
    doc.add('<text class="smb c1-txt" x="616" y="165" text-anchor="middle">SWAP（三 CNOT 交替分解）</text>')
    # Left SWAP symbol
    doc.add('<line class="wire" x1="518" y1="196" x2="566" y2="196"/>')
    doc.add('<line class="wire" x1="518" y1="238" x2="566" y2="238"/>')
    doc.add('<line class="wire" x1="542" y1="196" x2="542" y2="238"/>')
    draw_swap_x(542.0, 196.0)
    draw_swap_x(542.0, 238.0)
    # Equivalence symbol
    doc.add('<text class="lblb c1-txt" x="582" y="222" text-anchor="middle">≡</text>')
    # Right 3 alternating CNOTs
    doc.add('<line class="wire" x1="598" y1="196" x2="716" y2="196"/>')
    doc.add('<line class="wire" x1="598" y1="238" x2="716" y2="238"/>')
    draw_cnot(618.0, 196.0, 238.0, 8.8)
    draw_cnot(657.0, 238.0, 196.0, 8.8)
    draw_cnot(696.0, 196.0, 238.0, 8.8)
    doc.add('<text class="xs" x="616" y="278" text-anchor="middle">|x, y⟩ ↦ |y, x⟩（恰好 3 个 CNOT）</text>')

    # Card 4: Toffoli / CCNOT (x=738..958)
    doc.add('<rect class="subpanel" x="738" y="144" width="220" height="150" rx="10"/>')
    doc.add('<text class="smb c1-txt" x="848" y="165" text-anchor="middle">Toffoli（双控非门 CCNOT）</text>')
    doc.add('<line class="wire" x1="774" y1="186" x2="884" y2="186"/>')
    doc.add('<line class="wire" x1="774" y1="214" x2="884" y2="214"/>')
    doc.add('<line class="wire" x1="774" y1="242" x2="884" y2="242"/>')
    doc.add('<line class="wire" x1="829" y1="186" x2="829" y2="242"/>')
    doc.add('<circle class="ctrl" cx="829" cy="186" r="4.4"/>')
    doc.add('<circle class="ctrl" cx="829" cy="214" r="4.4"/>')
    doc.add('<circle class="targ" cx="829" cy="242" r="9.5"/>')
    doc.add('<line class="wire" x1="819.5" y1="242" x2="838.5" y2="242"/>')
    doc.add('<line class="wire" x1="829" y1="232.5" x2="829" y2="251.5"/>')
    doc.add('<text class="xs" x="768" y="190" text-anchor="end">|x⟩</text>')
    doc.add('<text class="xs" x="768" y="218" text-anchor="end">|y⟩</text>')
    doc.add('<text class="xs" x="768" y="246" text-anchor="end">|z⟩</text>')
    doc.add('<text class="xs" x="890" y="190">|x⟩</text>')
    doc.add('<text class="xs" x="890" y="218">|y⟩</text>')
    doc.add('<text class="xs" x="890" y="246">|z⊕xy⟩</text>')
    doc.add('<text class="xs" x="848" y="278" text-anchor="middle">经典可逆通用；|z⟩ ↦ |z ⊕ x·y⟩</text>')

    # --- Bottom Panel: Principle of Deferred Measurement (y=362..540) ---
    # Left Circuit: Mid-circuit measurement + classical controlled-U
    doc.add('<rect class="subpanel" x="42" y="362" width="418" height="132" rx="10"/>')
    doc.add('<text class="smb c4-txt" x="56" y="382">方案一：中段测量 + 经典条件门 U（动态电路）</text>')

    ya, yb = 418.0, 468.0
    doc.add('<text class="xs" x="54" y="422">寄存器 A</text>')
    doc.add('<text class="xs" x="54" y="472">寄存器 B</text>')
    # Quantum wire A -> Meter
    doc.add(f'<line class="wire" x1="112" y1="{fmt(ya)}" x2="176" y2="{fmt(ya)}"/>')
    draw_meter(176.0, ya)
    # Double classical wire from Meter -> right output
    doc.add(f'<line class="cwire" x1="216" y1="{fmt(ya - 2.6)}" x2="384" y2="{fmt(ya - 2.6)}"/>')
    doc.add(f'<line class="cwire" x1="216" y1="{fmt(ya + 2.6)}" x2="384" y2="{fmt(ya + 2.6)}"/>')
    doc.add('<text class="xs c4-txt" x="304" y="405" text-anchor="middle">经典双线 k ∈ {0, 1}</text>')
    doc.add('<text class="sm" x="392" y="422">k</text>')

    # Quantum wire B through classical controlled U
    doc.add(f'<line class="wire" x1="112" y1="{fmt(yb)}" x2="288" y2="{fmt(yb)}"/>')
    doc.add(f'<line class="wire" x1="334" y1="{fmt(yb)}" x2="384" y2="{fmt(yb)}"/>')
    # Vertical double classical control line
    doc.add(f'<line class="cwire" x1="308.4" y1="{fmt(ya + 2.6)}" x2="308.4" y2="{fmt(yb - 18)}"/>')
    doc.add(f'<line class="cwire" x1="313.6" y1="{fmt(ya + 2.6)}" x2="313.6" y2="{fmt(yb - 18)}"/>')
    doc.add(f'<circle class="c4-fill" cx="311" cy="{fmt(ya)}" r="4.0"/>')
    doc.add('<text class="xs c4-txt" x="322" y="439">k = 1</text>')
    # Classical-controlled gate U box
    doc.add(f'<rect class="c4-soft" x="288" y="{fmt(yb - 18)}" width="46" height="36" rx="6"/>')
    doc.add(f'<text class="gate-txt" x="311" y="{fmt(yb + 6)}" text-anchor="middle">U</text>')
    doc.add(f'<text class="xs" x="390" y="465">U<tspan baseline-shift="super" font-size="72%">k</tspan>|ψ{sub("k")}⟩</text>')
    doc.add('<text class="xs" x="390" y="481">(归一条件态)</text>')

    # Center equivalence symbol
    doc.add('<text class="title c1-txt" x="500" y="430" text-anchor="middle">≡</text>')
    doc.add('<text class="xs c1-txt" x="500" y="450" text-anchor="middle">末端读出</text>')
    doc.add('<text class="xs c1-txt" x="500" y="465" text-anchor="middle">分支相同</text>')

    # Right Circuit: Quantum controlled-U + terminal measurement
    doc.add('<rect class="subpanel" x="540" y="362" width="418" height="132" rx="10"/>')
    doc.add('<text class="smb c1-txt" x="554" y="382">方案二：量子受控门 C-U + 末端统一测量</text>')

    doc.add('<text class="xs" x="552" y="422">寄存器 A</text>')
    doc.add('<text class="xs" x="552" y="472">寄存器 B</text>')
    # Quantum wire A all the way to terminal meter
    doc.add(f'<line class="wire" x1="610" y1="{fmt(ya)}" x2="796" y2="{fmt(ya)}"/>')
    # Quantum control dot -> vertical single quantum wire -> U
    doc.add(f'<line class="wire" x1="704" y1="{fmt(ya)}" x2="704" y2="{fmt(yb - 18)}"/>')
    doc.add(f'<circle class="ctrl" cx="704" cy="{fmt(ya)}" r="5.0"/>')
    doc.add('<text class="xs c1-txt" x="704" y="403" text-anchor="middle">量子受控 C-U</text>')
    # Terminal meter on A
    draw_meter(796.0, ya)
    # Short classical double wire after terminal meter
    doc.add(f'<line class="cwire" x1="836" y1="{fmt(ya - 2.6)}" x2="878" y2="{fmt(ya - 2.6)}"/>')
    doc.add(f'<line class="cwire" x1="836" y1="{fmt(ya + 2.6)}" x2="878" y2="{fmt(ya + 2.6)}"/>')
    doc.add('<text class="sm" x="886" y="422">k</text>')

    # Quantum wire B through quantum controlled U
    doc.add(f'<line class="wire" x1="610" y1="{fmt(yb)}" x2="681" y2="{fmt(yb)}"/>')
    doc.add(f'<line class="wire" x1="727" y1="{fmt(yb)}" x2="878" y2="{fmt(yb)}"/>')
    doc.add(f'<rect class="c1-soft" x="681" y="{fmt(yb - 18)}" width="46" height="36" rx="6"/>')
    doc.add(f'<text class="gate-txt" x="704" y="{fmt(yb + 6)}" text-anchor="middle">U</text>')
    doc.add(f'<text class="xs" x="884" y="465">U<tspan baseline-shift="super" font-size="72%">k</tspan>|ψ{sub("k")}⟩</text>')
    doc.add('<text class="xs" x="884" y="481">(归一条件态)</text>')

    # Bottom Proof & Trade-off Banner
    doc.add('<rect class="note" x="42" y="500" width="916" height="44" rx="9"/>')
    doc.add(
        f'<text class="xs" x="500" y="517" text-anchor="middle">'
        f'初态 √p{sub("0")}|0⟩|ψ{sub("0")}⟩ + √p{sub("1")}|1⟩|ψ{sub("1")}⟩（|ψ{sub("0")}⟩, |ψ{sub("1")}⟩ 归一）：'
        f'两方案皆得 ρ′{sub("AB")} = p{sub("0")}|0⟩⟨0|⊗|ψ{sub("0")}⟩⟨ψ{sub("0")}| + p{sub("1")}|1⟩⟨1|⊗U|ψ{sub("1")}⟩⟨ψ{sub("1")}|U†'
        f'</text>'
    )
    doc.add(
        '<text class="xs" x="500" y="535" text-anchor="middle">'
        '本图沿用控制位 A 保持标签。若继续操作数据位，可另设干净记录位；跨站点相干门另计通信资源。'
        '</text>'
    )

    return doc.render(), {"dm_diff": dm_diff, "p0_path1": p0_path1}


# ---------------------------------------------------------------------------
# XML well-formedness & static coordinate checks
# ---------------------------------------------------------------------------
def verify_svg_xml(svg_text: str, filename: str) -> dict[str, int]:
    root = ET.fromstring(svg_text)
    vb = root.attrib.get("viewBox", "")
    assert vb == f"0 0 {W} {H}", f"{filename}: unexpected viewBox {vb!r}"
    assert ":root{color-scheme:light dark}" in svg_text, f"{filename}: missing light/dark color-scheme"
    assert "@media(prefers-color-scheme:dark)" in svg_text, f"{filename}: missing dark mode media query"

    ns = {"svg": "http://www.w3.org/2000/svg"}
    title_el = root.find("svg:title", ns)
    desc_el = root.find("svg:desc", ns)
    assert title_el is not None and (title_el.text or "").strip(), f"{filename}: missing <title>"
    assert desc_el is not None and (desc_el.text or "").strip(), f"{filename}: missing <desc>"

    text_nodes = root.findall(".//svg:text", ns)
    assert len(text_nodes) >= 10, f"{filename}: too few text elements"
    for el in text_nodes:
        x = float(el.attrib["x"])
        y = float(el.attrib["y"])
        assert MARGIN <= x <= W - MARGIN, f"{filename}: text x={x} violates margin ({el.text!r})"
        assert MARGIN <= y <= H - MARGIN, f"{filename}: text y={y} violates margin ({el.text!r})"

    return {"text_count": len(text_nodes), "bytes": len(svg_text.encode("utf-8"))}


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    builders = [
        ("v2-01-complex-rotation.svg", build_fig1_complex_rotation),
        ("v2-q1-double-slit-mzi.svg", build_fig2_double_slit_mzi),
        ("v2-02-rotation-half-angle.svg", build_fig3_rotation_half_angle),
        ("v2-03-chsh-game.svg", build_fig4_chsh_game),
        ("v2-04-deferred-measurement.svg", build_fig5_deferred_measurement),
    ]

    for fname, fn in builders:
        svg_text, metrics = fn()
        check = verify_svg_xml(svg_text, fname)
        out_path = ASSETS_DIR / fname
        out_path.write_text(svg_text, encoding="utf-8")
        print(f"[OK] {fname}: {check['bytes']} bytes, {check['text_count']} text labels | metrics={metrics}")


if __name__ == "__main__":
    main()
