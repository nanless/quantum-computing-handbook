#!/usr/bin/env python3
"""Generate 7 light/dark-adaptive V3 scientific SVG figures (part 3) using Python stdlib only.

Outputs to handbook/assets/:
  1. v3-17-anyons-landau-zener.svg
  2. v3-18-gkp-grid-sampling.svg
  3. v3-19-cryo-thermal-budget.svg
  4. v3-19-queue-tail-latency.svg
  5. v3-q4-double-well-splitting.svg
  6. v3-20-sensing-limits.svg
  7. v3-21-classical-sim-boundaries.svg

Run:
  python3 codes/practice/generate_v3_figures_part3.py
"""

from __future__ import annotations

import math
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT / "handbook" / "assets"
W, H = 1000, 580
MARGIN = 26


COMMON_CSS = """
:root{color-scheme:light dark}
text{font-family:system-ui,-apple-system,'PingFang SC','Microsoft YaHei',sans-serif}
.bg{fill:#f8fafc}
.panel{fill:#ffffff;stroke:#cbd5e1;stroke-width:1.4}
.phead{fill:#eef4f8}
.halo{stroke:#ffffff;fill:none}
.title{font-size:20px;font-weight:700;fill:#13263a}
.subtitle{font-size:13.5px;font-weight:400;fill:#3e566d}
.sec{font-size:14.5px;font-weight:700;fill:#13263a}
.lbl{font-size:13px;font-weight:500;fill:#19324d}
.lblb{font-size:13px;font-weight:700;fill:#13263a}
.sm{font-size:12px;font-weight:400;fill:#3e566d}
.smb{font-size:12px;font-weight:600;fill:#19324d}
.xs{font-size:11px;font-weight:400;fill:#3e566d}
.xsb{font-size:11px;font-weight:600;fill:#19324d}
.axis{stroke:#19324d;stroke-width:1.6;fill:none}
.axis-fill{fill:#19324d}
.grid{stroke:#d9e3ec;stroke-width:1;fill:none}
.guide{stroke:#7c93a8;stroke-width:1.2;stroke-dasharray:4 4;fill:none}
.c1{stroke:#1b6ca8;fill:none}
.c1-fill{fill:#1b6ca8}
.c1-txt{fill:#155585}
.c1-soft{fill:#dff0fa;stroke:#1b6ca8;stroke-width:1.4}
.c2{stroke:#c74b34;fill:none}
.c2-fill{fill:#c74b34}
.c2-txt{fill:#a63824}
.c2-soft{fill:#fce7e2;stroke:#c74b34;stroke-width:1.4}
.c3{stroke:#1e7a5c;fill:none}
.c3-fill{fill:#1e7a5c}
.c3-txt{fill:#176148}
.c3-soft{fill:#e1f5ed;stroke:#1e7a5c;stroke-width:1.4}
.c4{stroke:#b57614;fill:none}
.c4-fill{fill:#b57614}
.c4-txt{fill:#8c580b}
.c4-soft{fill:#fdf2dc;stroke:#b57614;stroke-width:1.4}
.c5{stroke:#744ea6;fill:none}
.c5-fill{fill:#744ea6}
.c5-txt{fill:#5b3987}
.c5-soft{fill:#efe8fa;stroke:#744ea6;stroke-width:1.4}
.note{fill:#fff8e6;stroke:#c98d24;stroke-width:1.4}
.pill{fill:#edf2f7;stroke:#9fb3c8;stroke-width:1.2}
.forbid{fill:#c74b34;fill-opacity:.10}
.area1{fill:#1b6ca8;fill-opacity:.12}
.area3{fill:#1e7a5c;fill-opacity:.11}
.area4{fill:#b57614;fill-opacity:.12}
.data-node{fill:#ffffff;stroke:#19324d;stroke-width:1.8}
.badge-txt{fill:#ffffff;font-size:12px;font-weight:700}
.hatch-stroke1{stroke:#1b6ca8;stroke-width:1.1;stroke-opacity:.38}
.hatch-stroke2{stroke:#c74b34;stroke-width:1.1;stroke-opacity:.38}
.hatch-stroke3{stroke:#1e7a5c;stroke-width:1.1;stroke-opacity:.38}
.hatch-stroke4{stroke:#b57614;stroke-width:1.1;stroke-opacity:.40}
@media(prefers-color-scheme:dark){
  .bg{fill:#0f1720}
  .panel{fill:#16222e;stroke:#354c61}
  .phead{fill:#1c2d3d}
  .halo{stroke:#16222e}
  .title,.sec,.lblb{fill:#eef6ff}
  .subtitle,.sm,.xs{fill:#b7cde0}
  .lbl,.smb,.xsb{fill:#d7e7f5}
  .axis{stroke:#cde0f2}
  .axis-fill{fill:#cde0f2}
  .grid{stroke:#293e52}
  .guide{stroke:#738fa8}
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
  .c4-soft{fill:#3b2d13;stroke:#f0ba5a}
  .c5{stroke:#b999f0}
  .c5-fill{fill:#b999f0}
  .c5-txt{fill:#d0b8fa}
  .c5-soft{fill:#2d2045;stroke:#b999f0}
  .note{fill:#332914;stroke:#d6a240}
  .pill{fill:#203142;stroke:#4f6b85}
  .forbid{fill:#f28872;fill-opacity:.14}
  .area1{fill:#6bc2f5;fill-opacity:.16}
  .area3{fill:#5dd1a8;fill-opacity:.14}
  .area4{fill:#f0ba5a;fill-opacity:.15}
  .data-node{fill:#16222e;stroke:#d7e7f5}
  .badge-txt{fill:#0f1720}
  .hatch-stroke1{stroke:#6bc2f5;stroke-opacity:.45}
  .hatch-stroke2{stroke:#f28872;stroke-opacity:.45}
  .hatch-stroke3{stroke:#5dd1a8;stroke-opacity:.45}
  .hatch-stroke4{stroke:#f0ba5a;stroke-opacity:.45}
}
""".strip()


def fmt(v: float) -> str:
    s = f"{v:.2f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def sub(txt: str) -> str:
    return f'<tspan dy="2.8" font-size="74%">{escape(txt)}</tspan><tspan dy="-2.8">&#8203;</tspan>'


def sup(txt: str) -> str:
    return f'<tspan dy="-4" font-size="72%">{escape(txt)}</tspan><tspan dy="4">&#8203;</tspan>'


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


def tri_pts(cx: float, cy: float, r: float) -> str:
    return pts_str([(cx, cy - r), (cx + r * 0.92, cy + r * 0.78), (cx - r * 0.92, cy + r * 0.78)])


def arrow_head(x: float, y: float, dx: float, dy: float, size: float = 7.5, cls: str = "axis-fill") -> str:
    norm = math.hypot(dx, dy)
    ux, uy = dx / norm, dy / norm
    px, py = -uy, ux
    bx, by = x - ux * size, y - uy * size
    hw = size * 0.48
    return f'<polygon class="{cls}" points="{pts_str([(x, y), (bx + px * hw, by + py * hw), (bx - px * hw, by - py * hw)])}"/>'


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
            '<pattern id="hatch-amber" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">'
            '<line class="hatch-stroke4" x1="0" y1="0" x2="0" y2="9"/></pattern>',
        ]
        self.body: list[str] = []

    def add(self, snippet: str) -> None:
        self.body.append(snippet)

    def add_header(self, title_text: str, subtitle_text: str, *, raw_sub: bool = False) -> None:
        self.add(f'<rect class="bg" width="{self.w}" height="{self.h}" rx="20"/>')
        self.add(f'<text class="title" x="32" y="52">{escape(title_text)}</text>')
        s_out = subtitle_text if raw_sub else escape(subtitle_text)
        self.add(f'<text class="subtitle" x="32" y="77">{s_out}</text>')

    def add_panel(self, x: float, y: float, w: float, h: float, heading: str, *, raw_head: bool = False) -> None:
        self.add(f'<rect class="panel" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="14"/>')
        self.add(
            f'<path class="phead" d="M {fmt(x + 14)} {fmt(y + 1)} H {fmt(x + w - 14)} '
            f'Q {fmt(x + w - 1)} {fmt(y + 1)} {fmt(x + w - 1)} {fmt(y + 14)} V {fmt(y + 38)} '
            f'H {fmt(x + 1)} V {fmt(y + 14)} Q {fmt(x + 1)} {fmt(y + 1)} {fmt(x + 14)} {fmt(y + 1)} Z"/>'
        )
        self.add(f'<line class="grid" x1="{fmt(x + 1)}" y1="{fmt(y + 38)}" x2="{fmt(x + w - 1)}" y2="{fmt(y + 38)}"/>')
        h_out = heading if raw_head else escape(heading)
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


def _solve_quartic_double_well(a: float, n_grid: int = 241, x_lim: float | None = None) -> tuple[list[float], float, float, list[float], list[float]]:
    """Exact 1D finite-difference Sturm-bisection + inverse-iteration solver for
    H = -(1/2) d^2/dx^2 + (x^2 - a^2)^2 / (8 a^2) (hbar = m = omega = 1).
    """
    if x_lim is None:
        x_lim = a + 4.2
    xs = [-x_lim + 2.0 * x_lim * i / (n_grid - 1) for i in range(n_grid)]
    h = xs[1] - xs[0]
    m = n_grid - 2
    diag = [1.0 / (h * h) + ((x * x - a * a) ** 2) / (8.0 * a * a) for x in xs[1:-1]]
    off = -0.5 / (h * h)
    off2 = off * off

    def count_below(lam: float) -> int:
        cnt = 0
        q = diag[0] - lam
        if q < 0.0:
            cnt += 1
        for i in range(1, m):
            if abs(q) < 1e-30:
                q = -1e-30 if q <= 0.0 else 1e-30
            q = (diag[i] - lam) - off2 / q
            if q < 0.0:
                cnt += 1
        return cnt

    def bisect_eig(k: int) -> float:
        lo, hi = 0.0, 2.0
        while count_below(hi) <= k:
            hi *= 1.5
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            if count_below(mid) <= k:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def inv_iter(lam: float, parity: int) -> list[float]:
        shift = lam - 1e-10
        v = [math.exp(-0.5 * (x - a) ** 2) + parity * math.exp(-0.5 * (x + a) ** 2) for x in xs[1:-1]]
        for _ in range(6):
            # Thomas algorithm for tridiagonal (H - shift*I) y = v
            c_p = [0.0] * m
            d_p = [0.0] * m
            b0 = diag[0] - shift
            c_p[0] = off / b0
            d_p[0] = v[0] / b0
            for i in range(1, m):
                denom = (diag[i] - shift) - off * c_p[i - 1]
                if abs(denom) < 1e-30:
                    denom = 1e-30
                c_p[i] = off / denom if i < m - 1 else 0.0
                d_p[i] = (v[i] - off * d_p[i - 1]) / denom
            y = [0.0] * m
            y[-1] = d_p[-1]
            for i in range(m - 2, -1, -1):
                y[i] = d_p[i] - c_p[i] * y[i + 1]
            # Enforce exact parity & normalize in L2
            y = [0.5 * (y[i] + parity * y[m - 1 - i]) for i in range(m)]
            norm = math.sqrt(sum(val * val for val in y) * h)
            v = [val / norm for val in y]
        # Fix canonical sign: positive in right well
        if v[int(0.72 * m)] < 0.0:
            v = [-val for val in v]
        return [0.0] + v + [0.0]

    e0 = bisect_eig(0)
    e1 = bisect_eig(1)
    psi0 = inv_iter(e0, +1)
    psi1 = inv_iter(e1, -1)
    return xs, e0, e1, psi0, psi1


# ---------------------------------------------------------------------------
# Figure 1: Ch 17 — Ising vs Fibonacci Anyon Braiding + Exact Landau-Zener
# ---------------------------------------------------------------------------
def build_fig1_anyons_landau_zener() -> tuple[str, dict[str, float]]:
    # Exact Landau-Zener tunneling formula: P_LZ(x) = exp(-pi / (2 x)), x = hbar * v / Delta^2
    def p_lz(x: float, gap_ratio: float = 1.0) -> float:
        if x <= 1e-12:
            return 0.0
        return math.exp(-math.pi * (gap_ratio ** 2) / (2.0 * x))

    x_half = math.pi / (2.0 * math.log(2.0))  # ~2.26618
    p_slow = p_lz(0.5, 1.0)                   # exp(-pi) ~ 0.043214
    p_one = p_lz(1.0, 1.0)                    # exp(-pi/2) ~ 0.207880
    p_narrow_1 = p_lz(1.0, 0.6)               # exp(-0.18*pi) ~ 0.56808
    phi_golden = 0.5 * (1.0 + math.sqrt(5.0))

    assert abs(p_lz(x_half, 1.0) - 0.5) < 1e-12
    assert abs(p_slow - math.exp(-math.pi)) < 1e-12
    assert abs(p_narrow_1 - math.exp(-0.18 * math.pi)) < 1e-12 and p_narrow_1 > p_one
    assert abs(phi_golden * phi_golden - (phi_golden + 1.0)) < 1e-12

    doc = SvgDoc(
        title="拓扑任意子编织通用性与 Landau-Zener 非绝热隧穿",
        desc=(
            "左面板对比 2+1 维非阿贝尔任意子世界线编织：Ising 任意子（σ×σ = 1+ψ）仅生成有限 Clifford 门群，"
            "非通用；Fibonacci 任意子（τ×τ = 1+τ，量子维数 φ ≈ 1.618）编织群在 SU(2) 稠密，纯编织即可通用。"
            "右面板上部绘制 Landau-Zener 避免交叉精确双曲线能级 E±(t) = ±½√((vt)²+Δ²)，下部精确绘制非绝热隧穿概率 "
            "P_LZ = exp(−πΔ²/(2ℏv)) 随共同坐标 ℏv/Δ_ref² 变化，在同一物理扫速 v 比较两种最小能隙 Δ_ref 和 0.6Δ_ref。"
        ),
    )
    doc.add_header(
        "拓扑任意子世界线编织与 Landau–Zener 非绝热隧穿",
        f"左：Ising（Clifford 受限）与 Fibonacci（稠密通用）编织对比；右：避免交叉能级与精确 P{sub('LZ')} 曲线",
        raw_sub=True,
    )
    doc.add_panel(28, 96, 452, 456, "2+1 维任意子世界线编织对比（示意）")
    doc.add_panel(496, 96, 476, 456, "Landau–Zener 避免交叉与隧穿概率（精确公式）")

    # --- Left Panel: 2+1D Worldline Braids ---
    # Vertical time arrow on left
    doc.add('<line class="axis" x1="50" y1="422" x2="50" y2="162"/>')
    doc.add(arrow_head(50, 158, 0, -1, 7.0))
    doc.add('<text class="xsb" x="41" y="294" text-anchor="middle" transform="rotate(-90 41 294)">演化时间 t</text>')

    def draw_braid_step(x_a: float, x_b: float, y_bot: float, y_top: float, cls_over: str, cls_under: str, a_over: bool) -> None:
        ym = 0.5 * (y_bot + y_top)
        d_a = f"M {fmt(x_a)} {fmt(y_bot)} C {fmt(x_a)} {fmt(ym)} {fmt(x_b)} {fmt(ym)} {fmt(x_b)} {fmt(y_top)}"
        d_b = f"M {fmt(x_b)} {fmt(y_bot)} C {fmt(x_b)} {fmt(ym)} {fmt(x_a)} {fmt(ym)} {fmt(x_a)} {fmt(y_top)}"
        if a_over:
            doc.add(f'<path class="{cls_under}" stroke-width="2.8" d="{d_b}"/>')
            doc.add(f'<path class="halo" stroke-width="8.5" d="{d_a}"/>')
            doc.add(f'<path class="{cls_over}" stroke-width="2.8" d="{d_a}"/>')
        else:
            doc.add(f'<path class="{cls_under}" stroke-width="2.8" d="{d_a}"/>')
            doc.add(f'<path class="halo" stroke-width="8.5" d="{d_b}"/>')
            doc.add(f'<path class="{cls_over}" stroke-width="2.8" d="{d_b}"/>')

    # Sub-card A: Ising Anyons
    doc.add('<rect class="c1-soft" fill-opacity=".22" x="60" y="148" width="206" height="288" rx="10"/>')
    doc.add('<text class="smb c1-txt" x="163" y="168" text-anchor="middle">Ising 任意子（σ×σ = 1+ψ）</text>')
    ix = [105.0, 163.0, 221.0]
    iy = [354.0, 306.0, 258.0, 210.0]
    # Segment 1 (bottom): swap 0,1 (0 over 1), strand 2 straight
    draw_braid_step(ix[0], ix[1], iy[0], iy[1], "c1", "c5", True)
    doc.add(f'<line class="c4" stroke-width="2.8" x1="{fmt(ix[2])}" y1="{fmt(iy[0])}" x2="{fmt(ix[2])}" y2="{fmt(iy[1])}"/>')
    # Segment 2 (mid): strand 0 straight, swap 1,2 (2 over 1)
    doc.add(f'<line class="c5" stroke-width="2.8" x1="{fmt(ix[0])}" y1="{fmt(iy[1])}" x2="{fmt(ix[0])}" y2="{fmt(iy[2])}"/>')
    draw_braid_step(ix[1], ix[2], iy[1], iy[2], "c4", "c1", False)
    # Segment 3 (top): swap 0,1 (0 over 1), strand 2 straight
    draw_braid_step(ix[0], ix[1], iy[2], iy[3], "c5", "c4", True)
    doc.add(f'<line class="c1" stroke-width="2.8" x1="{fmt(ix[2])}" y1="{fmt(iy[2])}" x2="{fmt(ix[2])}" y2="{fmt(iy[3])}"/>')
    # Crossing badges & endpoint circles
    for x_p in ix:
        doc.add(f'<circle class="data-node" cx="{fmt(x_p)}" cy="{fmt(iy[0])}" r="9.5"/>')
        doc.add(f'<text class="xsb" x="{fmt(x_p)}" y="{fmt(iy[0] + 3.5)}" text-anchor="middle">σ</text>')
        doc.add(f'<circle class="c1-soft" cx="{fmt(x_p)}" cy="{fmt(iy[3])}" r="9.5"/>')
        doc.add(f'<text class="xsb c1-txt" x="{fmt(x_p)}" y="{fmt(iy[3] + 3.5)}" text-anchor="middle">σ</text>')
    doc.add('<text class="xs" x="163" y="191" text-anchor="middle">融合通道读出：1 或 ψ</text>')
    doc.add('<text class="xs c1-txt" x="163" y="384" text-anchor="middle">相对相位 π/2 (Clifford S) · 有限编织群</text>')
    doc.add('<text class="smb c1-txt" x="163" y="405" text-anchor="middle">仅生成 Clifford 门</text>')
    doc.add('<text class="xs" x="163" y="424" text-anchor="middle">非通用，仍需魔法态注入</text>')

    # Sub-card B: Fibonacci Anyons
    doc.add('<rect class="c3-soft" fill-opacity=".22" x="274" y="148" width="194" height="288" rx="10"/>')
    doc.add('<text class="smb c3-txt" x="371" y="168" text-anchor="middle">Fibonacci（τ×τ = 1+τ）</text>')
    fx = [313.0, 371.0, 429.0]
    # Segment 1: swap 0,1 (0 over 1), strand 2 straight
    draw_braid_step(fx[0], fx[1], iy[0], iy[1], "c3", "c2", True)
    doc.add(f'<line class="c1" stroke-width="2.8" x1="{fmt(fx[2])}" y1="{fmt(iy[0])}" x2="{fmt(fx[2])}" y2="{fmt(iy[1])}"/>')
    # Segment 2: strand 0 straight, swap 1,2 (1 over 2)
    doc.add(f'<line class="c2" stroke-width="2.8" x1="{fmt(fx[0])}" y1="{fmt(iy[1])}" x2="{fmt(fx[0])}" y2="{fmt(iy[2])}"/>')
    draw_braid_step(fx[1], fx[2], iy[1], iy[2], "c3", "c1", True)
    # Segment 3: swap 0,1 (1 over 0), strand 2 straight
    draw_braid_step(fx[0], fx[1], iy[2], iy[3], "c1", "c2", False)
    doc.add(f'<line class="c3" stroke-width="2.8" x1="{fmt(fx[2])}" y1="{fmt(iy[2])}" x2="{fmt(fx[2])}" y2="{fmt(iy[3])}"/>')
    for x_p in fx:
        doc.add(f'<circle class="data-node" cx="{fmt(x_p)}" cy="{fmt(iy[0])}" r="9.5"/>')
        doc.add(f'<text class="xsb" x="{fmt(x_p)}" y="{fmt(iy[0] + 3.5)}" text-anchor="middle">τ</text>')
        doc.add(f'<circle class="c3-soft" cx="{fmt(x_p)}" cy="{fmt(iy[3])}" r="9.5"/>')
        doc.add(f'<text class="xsb c3-txt" x="{fmt(x_p)}" y="{fmt(iy[3] + 3.5)}" text-anchor="middle">τ</text>')
    doc.add(f'<text class="xs" x="371" y="191" text-anchor="middle">编码子空间 |0{sub("L")}⟩(1), |1{sub("L")}⟩(τ)</text>')
    doc.add(f'<text class="xs c3-txt" x="371" y="384" text-anchor="middle">量子维数 d{sub("τ")} = φ ≈ 1.618</text>')
    doc.add('<text class="smb c3-txt" x="371" y="405" text-anchor="middle">编织群在 SU(2) 稠密</text>')
    doc.add('<text class="xs" x="371" y="424" text-anchor="middle">纯编织逼近任意通用门</text>')

    # Bottom takeaway note in Left Panel
    doc.add('<rect class="pill" x="44" y="448" width="424" height="88" rx="10"/>')
    doc.add('<text class="smb" x="58" y="470">拓扑保护机制：体能隙抑制局域扰动，逻辑门只依赖扭结拓扑</text>')
    doc.add('<text class="xs" x="58" y="492">• Ising（Majorana 零模对应）：可做拓扑 Clifford，但须非拓扑 T 门</text>')
    doc.add('<text class="xs" x="58" y="514">• Fibonacci：融合维数按 1, 1, 2, 3, 5, 8… 增长，编织可实现 BQP 通用</text>')

    # --- Right Panel Upper: Exact Avoided Crossing E_pm(u) ---
    ux0, ux1 = 564.0, 948.0
    uy_top, uy_bot = 166.0, 286.0
    uy_mid = 0.5 * (uy_top + uy_bot)
    u_lim = 3.2
    e_lim = 1.85

    def ax_u(u: float) -> float:
        return ux0 + ((u + u_lim) / (2.0 * u_lim)) * (ux1 - ux0)

    def ay_e(e: float) -> float:
        return uy_mid - (e / e_lim) * (0.5 * (uy_bot - uy_top))

    # Legend row cleanly above upper plot
    doc.add('<line class="c1" stroke-width="2.4" x1="518" y1="150" x2="544" y2="150"/>')
    doc.add(f'<text class="xs" x="550" y="154">绝热基态 E{sub("−")}(t)</text>')
    doc.add('<line class="c2" stroke-width="2.4" x1="658" y1="150" x2="684" y2="150"/>')
    doc.add(f'<text class="xs" x="690" y="154">激发态 E{sub("+")}(t)</text>')
    doc.add('<line class="guide" x1="794" y1="150" x2="820" y2="150"/>')
    doc.add('<text class="xs" x="826" y="154">透热能级 ±vt/2</text>')

    # Axes for upper plot
    doc.add(f'<line class="grid" x1="{fmt(ux0)}" y1="{fmt(uy_mid)}" x2="{fmt(ux1)}" y2="{fmt(uy_mid)}"/>')
    doc.add(f'<line class="grid" x1="{fmt(ax_u(0.0))}" y1="{fmt(uy_top)}" x2="{fmt(ax_u(0.0))}" y2="{fmt(uy_bot)}"/>')
    doc.add(f'<line class="axis" x1="{fmt(ux0)}" y1="{fmt(uy_bot)}" x2="{fmt(ux1 + 6)}" y2="{fmt(uy_bot)}"/>')
    doc.add(arrow_head(ux1 + 6, uy_bot, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(ux0)}" y1="{fmt(uy_bot)}" x2="{fmt(ux0)}" y2="{fmt(uy_top - 6)}"/>')
    doc.add(arrow_head(ux0, uy_top - 6, 0, -1, 6.5))
    doc.add(f'<text class="xs" x="520" y="{fmt(uy_mid + 4)}" text-anchor="middle" transform="rotate(-90 520 {fmt(uy_mid)})">能量 E / Δ</text>')
    doc.add(f'<text class="xs" x="{fmt(ux0 - 6)}" y="{fmt(ay_e(1.0) + 3.5)}" text-anchor="end">+1</text>')
    doc.add(f'<text class="xs" x="{fmt(ux0 - 6)}" y="{fmt(uy_mid + 3.5)}" text-anchor="end">0</text>')
    doc.add(f'<text class="xs" x="{fmt(ux0 - 6)}" y="{fmt(ay_e(-1.0) + 3.5)}" text-anchor="end">−1</text>')
    doc.add(f'<text class="xs" x="{fmt(ax_u(0.0))}" y="{fmt(uy_bot + 15)}" text-anchor="middle">扫频坐标 vt / Δ = 0（交叉中心）</text>')

    # Diabatic dashed asymptotes ±u/2
    doc.add(f'<line class="guide" x1="{fmt(ax_u(-u_lim))}" y1="{fmt(ay_e(-0.5*u_lim))}" x2="{fmt(ax_u(u_lim))}" y2="{fmt(ay_e(0.5*u_lim))}"/>')
    doc.add(f'<line class="guide" x1="{fmt(ax_u(-u_lim))}" y1="{fmt(ay_e(0.5*u_lim))}" x2="{fmt(ax_u(u_lim))}" y2="{fmt(ay_e(-0.5*u_lim))}"/>')

    # Exact adiabatic hyperbolas
    u_pts_hi = [(ax_u(-u_lim + 2.0 * u_lim * i / 120), ay_e(0.5 * math.hypot(-u_lim + 2.0 * u_lim * i / 120, 1.0))) for i in range(121)]
    u_pts_lo = [(ax_u(-u_lim + 2.0 * u_lim * i / 120), ay_e(-0.5 * math.hypot(-u_lim + 2.0 * u_lim * i / 120, 1.0))) for i in range(121)]
    doc.add(f'<path class="c2" stroke-width="2.5" d="{path_from_points(u_pts_hi)}"/>')
    doc.add(f'<path class="c1" stroke-width="2.5" d="{path_from_points(u_pts_lo)}"/>')

    # Minimum gap Delta double-arrow at u = 0
    x_zero = ax_u(0.0)
    y_gap_hi, y_gap_lo = ay_e(0.5) + 4, ay_e(-0.5) - 4
    doc.add(f'<line class="c3" stroke-width="1.8" x1="{fmt(x_zero)}" y1="{fmt(y_gap_hi)}" x2="{fmt(x_zero)}" y2="{fmt(y_gap_lo)}"/>')
    doc.add(arrow_head(x_zero, y_gap_hi - 2, 0, -1, 5.5, "c3-fill"))
    doc.add(arrow_head(x_zero, y_gap_lo + 2, 0, 1, 5.5, "c3-fill"))
    doc.add(f'<text class="smb c3-txt" x="{fmt(x_zero - 18)}" y="{fmt(uy_mid + 4)}" text-anchor="end">最小隙 Δ</text>')

    # Non-adiabatic jump arrow
    jx1, jy1 = ax_u(0.25), ay_e(-0.52)
    jx2, jy2 = ax_u(0.85), ay_e(0.65)
    doc.add(f'<path class="c2" stroke-width="1.8" stroke-dasharray="4 3" d="M {fmt(jx1)} {fmt(jy1)} Q {fmt(ax_u(0.75))} {fmt(uy_mid)} {fmt(jx2)} {fmt(jy2)}"/>')
    doc.add(arrow_head(jx2, jy2, 0.25, -1.0, 5.8, "c2-fill"))
    doc.add(f'<text class="xsb c2-txt" x="{fmt(ax_u(1.88))}" y="{fmt(uy_mid + 4)}" text-anchor="middle">非绝热隧穿 P{sub("LZ")}</text>')

    # --- Right Panel Lower: Exact P_LZ vs Dimensionless Sweep Rate ---
    lx0, lx1 = 564.0, 948.0
    ly_bot, ly_top = 462.0, 336.0
    x_max = 5.0

    def px_r(xv: float) -> float:
        return lx0 + (xv / x_max) * (lx1 - lx0)

    def py_r(pv: float) -> float:
        return ly_bot - pv * (ly_bot - ly_top)

    # Shaded adiabatic safe region x in [0, 0.5]
    doc.add(f'<rect class="area3" x="{fmt(lx0)}" y="{fmt(ly_top)}" width="{fmt(px_r(0.5) - lx0)}" height="{fmt(ly_bot - ly_top)}"/>')

    for pt in [0.0, 0.5, 1.0]:
        yp = py_r(pt)
        doc.add(f'<line class="grid" x1="{fmt(lx0)}" y1="{fmt(yp)}" x2="{fmt(lx1)}" y2="{fmt(yp)}"/>')
        doc.add(f'<text class="xs" x="{fmt(lx0 - 6)}" y="{fmt(yp + 3.5)}" text-anchor="end">{pt:.1f}</text>')
    for xt in [0, 1, 2, 3, 4, 5]:
        xp = px_r(float(xt))
        doc.add(f'<line class="grid" x1="{fmt(xp)}" y1="{fmt(ly_top)}" x2="{fmt(xp)}" y2="{fmt(ly_bot)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xp)}" y="{fmt(ly_bot + 15)}" text-anchor="middle">{xt}</text>')

    # Exact curves
    xs_r = [x_max * i / 160.0 for i in range(161)]
    pts_std = [(px_r(xv), py_r(p_lz(xv, 1.0))) for xv in xs_r]
    pts_nar = [(px_r(xv), py_r(p_lz(xv, 0.6))) for xv in xs_r]
    doc.add(f'<path class="c1" stroke-width="2.6" d="{path_from_points(pts_std)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.2" stroke-dasharray="7 4" d="{path_from_points(pts_nar)}"/>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(ly_bot)}" x2="{fmt(lx1 + 6)}" y2="{fmt(ly_bot)}"/>')
    doc.add(arrow_head(lx1 + 6, ly_bot, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(ly_bot)}" x2="{fmt(lx0)}" y2="{fmt(ly_top - 8)}"/>')
    doc.add(arrow_head(lx0, ly_top - 8, 0, -1, 6.5))
    doc.add(f'<text class="xs" x="{fmt(0.5*(lx0+lx1))}" y="{fmt(ly_bot + 32)}" text-anchor="middle">共同扫速坐标 ℏv / Δ_ref²</text>')
    doc.add(f'<text class="xs" x="520" y="{fmt(0.5*(ly_bot+ly_top))}" text-anchor="middle" transform="rotate(-90 520 {fmt(0.5*(ly_bot+ly_top))})">跃迁概率 P{sub("LZ")}</text>')

    # Markers & callouts in clean open spaces
    xh, yh = px_r(x_half), py_r(0.5)
    doc.add(f'<line class="guide" x1="{fmt(xh)}" y1="{fmt(yh)}" x2="{fmt(xh)}" y2="{fmt(ly_bot)}"/>')
    doc.add(f'<circle class="c1-fill" cx="{fmt(xh)}" cy="{fmt(yh)}" r="4.8"/>')
    doc.add(f'<text class="xsb c1-txt" x="{fmt(xh + 12)}" y="{fmt(yh + 24)}">参考隙 Δ_ref（P=0.5 在 2.27）</text>')

    xn, yn = px_r(1.0), py_r(p_narrow_1)
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(xn, yn, 5.5)}"/>')
    doc.add(f'<text class="xsb c2-txt" x="{fmt(px_r(1.92))}" y="{fmt(py_r(0.95))}">窄隙 0.6Δ_ref</text>')
    doc.add(f'<line class="c2" stroke-width="1.1" x1="{fmt(xn + 5)}" y1="{fmt(yn - 3)}" x2="{fmt(px_r(1.88))}" y2="{fmt(py_r(0.93))}"/>')

    xs0, ys0 = px_r(0.5), py_r(p_slow)
    doc.add(f'<circle class="c3-fill" cx="{fmt(xs0)}" cy="{fmt(ys0)}" r="4.5"/>')
    doc.add(f'<text class="xsb c3-txt" x="{fmt(px_r(0.88))}" y="{fmt(py_r(0.08))}">绝热区 4.3%</text>')

    # Formula pill at bottom of right panel
    doc.add('<rect class="pill" x="512" y="506" width="444" height="32" rx="8"/>')
    doc.add(
        f'<text class="xs" x="734" y="526" text-anchor="middle">'
        f'P{sub("LZ")} = exp(−πΔ² / (2ℏv))；保证 P{sub("LZ")} ≤ ε 须满足 v ≤ πΔ² / (2ℏ ln(1/ε))'
        f'</text>'
    )

    return doc.render(), {"x_half": x_half, "p_slow_0p5": p_slow, "p_one": p_one, "phi_golden": phi_golden}


# ---------------------------------------------------------------------------
# Figure 2: Ch 18 — GKP Phase-Space Grid Stabilizers + Sampling Complexity Chain
# ---------------------------------------------------------------------------
def build_fig2_gkp_grid_sampling() -> tuple[str, dict[str, float]]:
    sqrt_pi = math.sqrt(math.pi)
    half_voronoi = 0.5 * sqrt_pi
    cell_area = (2.0 * sqrt_pi) ** 2
    assert abs(cell_area - 4.0 * math.pi) < 1e-12
    assert abs(half_voronoi - 0.88622692545) < 1e-9

    doc = SvgDoc(
        title="GKP 相空间网格稳定子与量子采样复杂度反证链",
        desc=(
            "左面板在 [q̂, p̂] = i（ℏ = 1）相空间精确绘制方形 GKP 晶格：逻辑 |0_L⟩ 位于 q = 2s√π（蓝圆），"
            "|1_L⟩ 位于 q = (2s+1)√π（红菱），稳定子平移 S_p, S_q 步长 2√π 围出面积 4π = 2×2πℏ 的单逻辑比特晶胞，"
            "原点周围标出可纠错 Voronoi 域 [−√π/2, √π/2]²。右面板展示 BosonSampling/IQP/RCS 经 Stockmeyer 计数与反集中推向 PH 坍塌的反证链，并标出恒定门噪声抹平 Porter–Thomas 散斑涨落与 #P 难干涉信号（分布坍向均匀态）的经典边界。"
        ),
    )
    doc.add_header(
        "GKP 相空间网格稳定子与量子采样复杂度反证链",
        "左：[q, p] = i 方形 GKP 晶格、稳定子位移与 Voronoi 纠错域；右：采样优越性四步反证链与噪声边界",
    )
    doc.add_panel(28, 96, 456, 456, "方形 GKP 相空间晶格（[q, p] = i，ℏ = 1）")
    doc.add_panel(500, 96, 472, 456, "量子采样复杂度反证链与恒定门噪声边界")

    # --- Left Panel: Exact Square GKP Phase-Space Lattice ---
    # Framed axes: q/sqrt(pi) in [-2.35, 2.45], p/sqrt(pi) in [-2.2, 2.3] with exact square aspect ratio
    u = 54.0  # px per sqrt(pi)
    cx, cy = 266.0, 294.0
    px0, px1 = cx - 2.35 * u, cx + 2.45 * u  # 139.1 .. 398.3
    py0, py1 = cy + 2.20 * u, cy - 2.30 * u  # 412.8 .. 169.8

    def gx(q_u: float) -> float:
        return cx + q_u * u

    def gp(p_u: float) -> float:
        return cy - p_u * u

    # Grid lines and outer tick labels
    tick_names = {-2: "−2√π", -1: "−√π", 0: "0", 1: "√π", 2: "2√π"}
    for k in (-2, -1, 0, 1, 2):
        xk, yk = gx(float(k)), gp(float(k))
        cls_l = "guide" if k == 0 else "grid"
        doc.add(f'<line class="{cls_l}" x1="{fmt(xk)}" y1="{fmt(py1)}" x2="{fmt(xk)}" y2="{fmt(py0)}"/>')
        doc.add(f'<line class="{cls_l}" x1="{fmt(px0)}" y1="{fmt(yk)}" x2="{fmt(px1)}" y2="{fmt(yk)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xk)}" y="{fmt(py0 + 16)}" text-anchor="middle">{tick_names[k]}</text>')
        doc.add(f'<text class="xs" x="{fmt(px0 - 7)}" y="{fmt(yk + 3.5)}" text-anchor="end">{tick_names[k]}</text>')

    # Shaded unit cell [0, 2] x [0, 2] of area 4 pi = 2 * 2 pi hbar
    doc.add(
        f'<rect class="area1" x="{fmt(gx(0))}" y="{fmt(gp(2))}" width="{fmt(2*u)}" height="{fmt(2*u)}"/>'
    )
    doc.add(
        f'<rect class="c1" stroke-width="1.5" stroke-dasharray="5 4" '
        f'x="{fmt(gx(0))}" y="{fmt(gp(2))}" width="{fmt(2*u)}" height="{fmt(2*u)}"/>'
    )

    # Shaded Voronoi error-correction square [-0.5, 0.5]^2 around (0, 0)
    doc.add(f'<rect class="c3-soft" x="{fmt(gx(-0.5))}" y="{fmt(gp(0.5))}" width="{fmt(u)}" height="{fmt(u)}"/>')
    doc.add(f'<rect fill="url(#hatch-green)" x="{fmt(gx(-0.5))}" y="{fmt(gp(0.5))}" width="{fmt(u)}" height="{fmt(u)}"/>')

    # Outer frame axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px1 + 10)}" y2="{fmt(py0)}"/>')
    doc.add(arrow_head(px1 + 10, py0, 1, 0, 7.0))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px0)}" y2="{fmt(py1 - 10)}"/>')
    doc.add(arrow_head(px0, py1 - 10, 0, -1, 7.0))
    doc.add(f'<text class="sm" x="{fmt(0.5*(px0+px1))}" y="{fmt(py0 + 34)}" text-anchor="middle">位置正交分量 q（单位：√π）</text>')
    doc.add(f'<text class="sm" x="54" y="{fmt(0.5*(py0+py1))}" text-anchor="middle" transform="rotate(-90 54 {fmt(0.5*(py0+py1))})">动量正交分量 p（单位：√π）</text>')

    # Stabilizer vectors S_p (along +q by 2 sqrt(pi)) and S_q (along +p by 2 sqrt(pi))
    doc.add(f'<line class="c1" stroke-width="2.8" x1="{fmt(gx(0))}" y1="{fmt(gp(0))}" x2="{fmt(gx(2) - 7)}" y2="{fmt(gp(0))}"/>')
    doc.add(arrow_head(gx(2) - 5, gp(0), 1, 0, 7.0, "c1-fill"))
    doc.add(f'<line class="c1" stroke-width="2.8" x1="{fmt(gx(0))}" y1="{fmt(gp(0))}" x2="{fmt(gx(0))}" y2="{fmt(gp(2) + 7)}"/>')
    doc.add(arrow_head(gx(0), gp(2) + 5, 0, -1, 7.0, "c1-fill"))

    # Logical vectors Xbar (along +q by sqrt(pi)) and Zbar (along +p by sqrt(pi))
    doc.add(f'<line class="c2" stroke-width="2.4" x1="{fmt(gx(-2))}" y1="{fmt(gp(-1))}" x2="{fmt(gx(-1) - 7)}" y2="{fmt(gp(-1))}"/>')
    doc.add(arrow_head(gx(-1) - 5, gp(-1), 1, 0, 6.5, "c2-fill"))
    doc.add(f'<line class="c2" stroke-width="2.4" x1="{fmt(gx(-2))}" y1="{fmt(gp(0))}" x2="{fmt(gx(-2))}" y2="{fmt(gp(1) + 7)}"/>')
    doc.add(arrow_head(gx(-2), gp(1) + 5, 0, -1, 6.5, "c2-fill"))

    # Lattice Dirac comb peaks (|0_L> even q blue circles, |1_L> odd q coral diamonds)
    for iq in (-2, -1, 0, 1, 2):
        for ip in (-2, -1, 0, 1, 2):
            xq, yp = gx(float(iq)), gp(float(ip))
            if iq % 2 == 0:
                doc.add(f'<circle class="c1-fill" cx="{fmt(xq)}" cy="{fmt(yp)}" r="4.8"/>')
            else:
                doc.add(f'<polygon class="c2-fill" points="{diamond_pts(xq, yp, 5.4)}"/>')

    # Clean non-overlapping annotations inside phase space
    doc.add(f'<text class="xsb c1-txt" x="{fmt(gx(1.0))}" y="{fmt(gp(1.56))}" text-anchor="middle">晶胞面积 4π</text>')
    doc.add(f'<text class="xs c1-txt" x="{fmt(gx(1.0))}" y="{fmt(gp(1.26))}" text-anchor="middle">= 2×2πℏ (1 比特)</text>')
    doc.add(f'<text class="xsb c1-txt" x="{fmt(gx(1.32))}" y="{fmt(gp(-0.34))}" text-anchor="middle">S{sub("p")} (移 2√π)</text>')
    doc.add(f'<text class="xsb c1-txt" x="{fmt(gx(-0.14))}" y="{fmt(gp(1.48))}" text-anchor="end">S{sub("q")} (移 2√π)</text>')
    doc.add(f'<text class="xsb c2-txt" x="{fmt(gx(-1.50))}" y="{fmt(gp(-0.74))}" text-anchor="middle">X̄ (√π)</text>')
    doc.add(f'<text class="xsb c2-txt" x="{fmt(gx(-1.84))}" y="{fmt(gp(0.50))}">Z̄ (√π)</text>')
    doc.add(f'<text class="xsb c3-txt" x="{fmt(gx(0.95))}" y="{fmt(gp(-1.42))}" text-anchor="middle">Voronoi 纠错域</text>')
    doc.add(f'<text class="xs c3-txt" x="{fmt(gx(0.95))}" y="{fmt(gp(-1.72))}" text-anchor="middle">|δq|, |δp| &lt; √π/2 ≈ 0.886</text>')
    doc.add(f'<line class="c3" stroke-width="1.2" x1="{fmt(gx(0.38))}" y1="{fmt(gp(-0.50))}" x2="{fmt(gx(0.75))}" y2="{fmt(gp(-1.20))}"/>')

    # Top concise legend above plot
    doc.add('<circle class="c1-fill" cx="62" cy="151" r="4.5"/>')
    doc.add(f'<text class="xs" x="72" y="155">|0{sub("L")}⟩ (q = 2s√π)</text>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(182, 151, 5.2)}"/>')
    doc.add(f'<text class="xs" x="192" y="155">|1{sub("L")}⟩ (q = (2s+1)√π)</text>')
    doc.add('<rect class="c3-soft" x="330" y="145" width="14" height="12" rx="2"/>')
    doc.add('<text class="xs" x="350" y="155">Voronoi 可纠错窗</text>')

    # Bottom algebra summary pill
    doc.add('<rect class="pill" x="44" y="458" width="424" height="80" rx="10"/>')
    doc.add(f'<text class="xsb" x="58" y="479">Weyl-BCH 三组对易相因子（严禁混写 4πi / 2πi / πi）：</text>')
    doc.add(f'<text class="xs" x="58" y="501">• 稳定子对易：[S{sub("q")}, S{sub("p")}] = 0（e{sup("4πi")}=1）；逻辑保子空间：[Z̄, S{sub("p")}] = 0（e{sup("2πi")}=1）</text>')
    doc.add(f'<text class="xs c2-txt" x="58" y="523">• 逻辑反对易：Z̄ X̄ = e{sup("iπ")} X̄ Z̄ = −X̄ Z̄（连续相空间切出离散 Pauli 代数）</text>')

    # --- Right Panel: Sampling Complexity Proof-by-Contradiction Chain ---
    cards = [
        (
            "1",
            "假设存在经典多项式近似采样器",
            "对 BosonSampling（积和式）/ IQP / RCS 输出分布，以总变差距离 ε 采样",
            "c1-soft",
            "c1-fill",
            "Stockmeyer 近似计数定理",
        ),
        (
            "2",
            f"Stockmeyer 计数落入 BPP{sup('NP')}（PH 第 3 层）",
            f"借隐匿性将单串输出概率 p{sub('x')} 估计至平均加性误差 O(ε / 2{sup('n')})",
            "c3-soft",
            "c3-fill",
            "反集中性（Anti-concentration）",
        ),
        (
            "3",
            "反集中 + 平均情形 #P-难猜想（PGC / RCS）",
            f"多数串满足 p{sub('x')} ≥ Ω(2{sup('−n')}) ⇒ 加性误差转为乘性相对误差，攻破 #P-难",
            "note",
            "c4-fill",
            f"Toda 定理（PH ⊆ P{sup('#P')}）",
        ),
        (
            "4",
            "矛盾：整座多项式谱系 PH 坍塌至第 3 层！",
            "被复杂度理论视为极不可能 ⇒ 无噪理想采样不存在经典多项式算法",
            "c2-soft",
            "c2-fill",
            None,
        ),
    ]
    cy_start = 148.0
    ch = 58.0
    cgap = 22.0
    for idx, (num, hd, desc_l, box_c, bdg_c, arrow_lbl) in enumerate(cards):
        y = cy_start + idx * (ch + cgap)
        doc.add(f'<rect class="{box_c}" x="516" y="{fmt(y)}" width="440" height="{fmt(ch)}" rx="10"/>')
        doc.add(f'<circle class="{bdg_c}" cx="538" cy="{fmt(y + 22)}" r="11"/>')
        doc.add(f'<text class="badge-txt" x="538" y="{fmt(y + 26)}" text-anchor="middle">{num}</text>')
        doc.add(f'<text class="smb" x="558" y="{fmt(y + 24)}">{hd}</text>')
        doc.add(f'<text class="xs" x="558" y="{fmt(y + 45)}">{desc_l}</text>')
        if arrow_lbl is not None:
            ay1 = y + ch + 1
            ay2 = y + ch + cgap - 3
            doc.add(f'<line class="axis" x1="600" y1="{fmt(ay1)}" x2="600" y2="{fmt(ay2)}"/>')
            doc.add(arrow_head(600, ay2 + 1, 0, 1, 6.0))
            doc.add(f'<text class="xsb" x="614" y="{fmt(0.5*(ay1 + ay2) + 4)}">{arrow_lbl}</text>')

    # Bottom noise boundary callout box
    doc.add('<rect class="pill" x="516" y="466" width="440" height="74" rx="10"/>')
    doc.add('<text class="smb c2-txt" x="528" y="487">物理边界：恒定门噪声斩断第 ③ 步（Aharonov 等, STOC 2023）</text>')
    doc.add('<text class="xs" x="528" y="508">• 恒定门噪声抹平 Porter–Thomas 散斑涨落与 #P 难干涉信号（分布坍向均匀态）</text>')
    doc.add('<text class="xs" x="528" y="528">• 均匀态仍平凡满足反集中，被摧毁的是 #P 难性；含噪 RCS 具经典多项式算法</text>')

    return doc.render(), {"sqrt_pi": sqrt_pi, "half_voronoi": half_voronoi, "cell_area": cell_area}


# ---------------------------------------------------------------------------
# Figure 3: Ch 19 — Dilution Fridge 5-Stage Cooling Waterfall + 100 mK Squeeze
# ---------------------------------------------------------------------------
def build_fig3_cryo_thermal_budget() -> tuple[str, dict[str, float]]:
    # Exact Ch19 cooling stages (W) and 100 mK active-channel budget formula
    stages = [
        ("50 K", "PT1", 30.0, "30 W", "c4-soft", "c4-txt"),
        ("4 K", "PT2", 1.5, "1.5 W", "c2-soft", "c2-txt"),
        ("~1 K", "Still", 20e-3, "20 mW", "c3-soft", "c3-txt"),
        ("100 mK", "冷板*", 600e-6, "600 μW*", "c1-soft", "c1-txt"),
        ("20 mK", "MXC", 19e-6, "19 μW", "c5-soft", "c5-txt"),
    ]
    drop_ratio = stages[0][2] / stages[-1][2]
    assert drop_ratio > 1e6

    # Ch19 §4.1 exact 100 mK thermal budget (uW)
    p_budget = 600.0
    p_wire_io = 120.0
    f_floor = p_wire_io / p_budget  # 0.20
    # Baseline: P_static = 80 uW, p_ch = 0.4 uW -> f = 200/600 = 1/3, N = 1000
    f_base = (80.0 + p_wire_io) / p_budget
    n_base = (p_budget - 80.0 - p_wire_io) / 0.4
    # Doubled static: P_static = 160 uW, p_ch = 0.2 uW -> f = 280/600 = 7/15, N = 1600
    f_dbl = (160.0 + p_wire_io) / p_budget
    n_dbl = (p_budget - 160.0 - p_wire_io) / 0.2
    # Nonlinear static-mux trade-off envelope: P_static * p_ch = 80 * 0.4 = 32 uW^2
    # N_env(f) = 600*(1-f)*(600*f - 120) / 32 = 11250 * (1-f) * (f - 0.2)
    def n_env(f: float) -> float:
        return max(0.0, 11250.0 * (1.0 - f) * (f - f_floor))

    assert abs(n_base - 1000.0) < 1e-12
    assert abs(n_dbl - 1600.0) < 1e-12
    assert abs(n_env(f_base) - 1000.0) < 1e-10
    assert abs(n_env(f_dbl) - 1600.0) < 1e-10
    assert abs(n_env(0.6) - 1800.0) < 1e-10

    doc = SvgDoc(
        title="稀释制冷机五温区冷量瀑布与 100 mK 静态基荷通道挤压",
        desc=(
            "左面板以对数纵轴（1 μW 至 100 W）呈现稀释制冷机五温区可用冷量瀑布：50 K 板 30 W、4 K 板 1.5 W、"
            "1 K 蒸馏室 20 mW、100 mK 冷板 600 μW（多脉管大型稀释制冷机参考；单脉管 XLD400 约 200 μW @ 140 mK）与 20 mK 混合室 19 μW，跨越逾 6 个数量级。"
            "右面板基于 100 mK 总预算 600 μW 与 120 μW 线缆/I/O 底荷，绘制单通道功耗 0.4 μW、0.2 μW 直线与静态-复用耦合非线性挤压包络，"
            "精确标出基线（33.3% → 1,000 通道）、静态翻倍（46.7% → 1,600 通道）与理论峰值（60% → 1,800 通道）。"
        ),
    )
    doc.add_header(
        "稀释制冷机五温区冷量瀑布与 100 mK 通道挤压",
        "左：50 K 至 20 mK 跨越 6 个数量级的可用冷量悬崖；右：100 mK 冷板（600 μW）静态基荷对通道上限的挤压",
    )
    doc.add_panel(28, 96, 464, 456, "五温区典型可用制冷功率瀑布（对数纵轴）")
    doc.add_panel(508, 96, 464, 456, "100 mK 活跃通道上限随静态基荷的挤压（精确公式）")

    # --- Left Panel: Log-Y 5-Stage Cooling Waterfall ---
    px0, px1 = 104.0, 472.0
    py_bot, py_top = 418.0, 166.0  # log10(W) in [-6, +2] = 8 decades
    log_lo, log_hi = -6.0, 2.0

    def wy(watts: float) -> float:
        lv = math.log10(watts)
        return py_bot - ((lv - log_lo) / (log_hi - log_lo)) * (py_bot - py_top)

    y_ticks = [(-6, "1 μW"), (-4, "100 μW"), (-2, "10 mW"), (0, "1 W"), (2, "100 W")]
    for exp in range(-6, 3):
        ye = wy(10.0 ** exp)
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(ye)}" x2="{fmt(px1)}" y2="{fmt(ye)}"/>')
    for exp, lbl_y in y_ticks:
        ye = wy(10.0 ** exp)
        doc.add(f'<text class="xs" x="{fmt(px0 - 7)}" y="{fmt(ye + 3.5)}" text-anchor="end">{lbl_y}</text>')

    bar_w = 46.0
    col_step = (px1 - px0) / 5.0
    bar_tops: list[tuple[float, float]] = []
    for idx, (temp_lbl, sub_lbl, val_w, val_txt, box_c, txt_c) in enumerate(stages):
        xc = px0 + (idx + 0.5) * col_step
        yt = wy(val_w)
        bar_tops.append((xc, yt))
        doc.add(f'<rect class="{box_c}" stroke-width="1.6" x="{fmt(xc - bar_w/2)}" y="{fmt(yt)}" width="{fmt(bar_w)}" height="{fmt(py_bot - yt)}" rx="4"/>')
        if idx == 4:
            doc.add(f'<rect fill="url(#hatch-blue)" x="{fmt(xc - bar_w/2)}" y="{fmt(yt)}" width="{fmt(bar_w)}" height="{fmt(py_bot - yt)}" rx="4"/>')
        doc.add(f'<text class="xsb {txt_c}" x="{fmt(xc)}" y="{fmt(yt - 7)}" text-anchor="middle">{val_txt}</text>')
        doc.add(f'<text class="xsb" x="{fmt(xc)}" y="{fmt(py_bot + 16)}" text-anchor="middle">{temp_lbl}</text>')
        doc.add(f'<text class="xs" x="{fmt(xc)}" y="{fmt(py_bot + 31)}" text-anchor="middle">{sub_lbl}</text>')

    # Waterfall connector dashed steps between adjacent stage tops
    for i in range(4):
        x_a, y_a = bar_tops[i]
        x_b, y_b = bar_tops[i + 1]
        doc.add(f'<path class="guide" d="M {fmt(x_a + bar_w/2)} {fmt(y_a)} H {fmt(x_b)} V {fmt(y_b - 20)}"/>')

    # 6-decade drop callout arrow in clean upper-right whitespace
    doc.add('<path class="c2" stroke-width="1.8" stroke-dasharray="6 4" d="M 180 184 Q 332 214 426 346"/>')
    doc.add(arrow_head(428, 349, 0.55, 0.85, 6.5, "c2-fill"))
    doc.add(f'<text class="smb c2-txt" x="358" y="210" text-anchor="middle">冷量骤降 ~1.6×10{sup("6")} 倍</text>')
    doc.add('<text class="xs c2-txt" x="358" y="229" text-anchor="middle">（跨越逾 6 个数量级）</text>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px1 + 6)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(px1 + 6, py_bot, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px0)}" y2="{fmt(py_top - 10)}"/>')
    doc.add(arrow_head(px0, py_top - 10, 0, -1, 6.5))
    doc.add(f'<text class="sm" x="43" y="{fmt(0.5*(py_bot+py_top))}" text-anchor="middle" transform="rotate(-90 43 {fmt(0.5*(py_bot+py_top))})">局部可用制冷功率 P{sub("cool")} (W，对数)</text>')

    # Bottom hardware load anchor note (including explicit multi-PT vs single-PT XLD400 caliber note)
    doc.add('<rect class="note" x="44" y="458" width="432" height="86" rx="10"/>')
    doc.add(f'<text class="xsb" x="56" y="476">温区锚点与热预算红线（P{sub("s")} &lt; P{sub("cool")}；20 dB 衰减器 99% 转焦耳热）：</text>')
    doc.add('<text class="xs" x="56" y="495">• 4 K：Cryo-CMOS / HEMT | 100–150 mK：热自旋芯片 | 20 mK：超导芯片</text>')
    doc.add('<text class="xs c1-txt" x="56" y="514">• *100 mK 600 μW 为多脉管大型稀释制冷机参考（对齐右图算例），</text>')
    doc.add('<text class="xs c1-txt" x="64" y="532">单脉管 XLD400 实测约 200 μW @ 140 mK（与正文表口径一致）</text>')

    # --- Right Panel: 100 mK Channel Limit vs Fixed Base-Load Fraction ---
    rx0, rx1 = 582.0, 950.0
    ry_bot, ry_top = 434.0, 192.0  # N in [0, 3000], f in [0, 1.0]
    n_max_y = 3000.0

    def rx(frac: float) -> float:
        return rx0 + frac * (rx1 - rx0)

    def ry(n_val: float) -> float:
        return ry_bot - (n_val / n_max_y) * (ry_bot - ry_top)

    # Legend cleanly above plot (2 compact rows inside y=144..180)
    doc.add('<line class="c1" stroke-width="2.2" x1="524" y1="152" x2="550" y2="152"/>')
    doc.add(f'<text class="xs" x="556" y="156">基线 p{sub("ch")} = 0.4 μW</text>')
    doc.add('<line class="c2" stroke-width="2.2" stroke-dasharray="6 4" x1="684" y1="152" x2="710" y2="152"/>')
    doc.add(f'<text class="xs" x="716" y="156">降功耗 p{sub("ch")} = 0.2 μW</text>')
    doc.add('<line class="c3" stroke-width="2.8" x1="524" y1="172" x2="550" y2="172"/>')
    doc.add(f'<text class="xs" x="556" y="176">静态–复用耦合非线性挤压包络（P{sub("static")}·p{sub("ch")} = 32 μW²）</text>')

    # Forbidden wire + I/O base-load zone f < 20%
    doc.add(f'<rect class="forbid" x="{fmt(rx0)}" y="{fmt(ry_top)}" width="{fmt(rx(f_floor) - rx0)}" height="{fmt(ry_bot - ry_top)}"/>')
    doc.add(f'<line class="c2" stroke-width="1.3" stroke-dasharray="4 4" x1="{fmt(rx(f_floor))}" y1="{fmt(ry_top)}" x2="{fmt(rx(f_floor))}" y2="{fmt(ry_bot)}"/>')
    doc.add(f'<text class="xs c2-txt" x="{fmt(rx(0.10))}" y="{fmt(ry(2250))}" text-anchor="middle">线缆+I/O</text>')
    doc.add(f'<text class="xs c2-txt" x="{fmt(rx(0.10))}" y="{fmt(ry(2030))}" text-anchor="middle">20% 底荷</text>')

    for nt in [0, 600, 1200, 1800, 2400, 3000]:
        yn = ry(float(nt))
        doc.add(f'<line class="grid" x1="{fmt(rx0)}" y1="{fmt(yn)}" x2="{fmt(rx1)}" y2="{fmt(yn)}"/>')
        doc.add(f'<text class="xs" x="{fmt(rx0 - 7)}" y="{fmt(yn + 3.5)}" text-anchor="end">{nt}</text>')
    for ft in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        xf = rx(ft)
        doc.add(f'<line class="grid" x1="{fmt(xf)}" y1="{fmt(ry_top)}" x2="{fmt(xf)}" y2="{fmt(ry_bot)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xf)}" y="{fmt(ry_bot + 16)}" text-anchor="middle">{int(ft*100)}%</text>')

    # Exact linear bounds & nonlinear envelope over f in [0.20, 1.00]
    line_04 = [(rx(0.20), ry(1500.0 * 0.80)), (rx(1.0), ry(0.0))]
    line_02 = [(rx(0.20), ry(3000.0 * 0.80)), (rx(1.0), ry(0.0))]
    env_pts = [(rx(0.20 + 0.80 * i / 120.0), ry(n_env(0.20 + 0.80 * i / 120.0))) for i in range(121)]
    env_poly = [(rx(0.20), ry_bot)] + env_pts + [(rx(1.0), ry_bot)]
    doc.add(f'<polygon class="area3" points="{pts_str(env_poly)}"/>')
    doc.add(f'<path class="c1" stroke-width="2.1" d="{path_from_points(line_04)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.1" stroke-dasharray="6 4" d="{path_from_points(line_02)}"/>')
    doc.add(f'<path class="c3" stroke-width="2.8" d="{path_from_points(env_pts)}"/>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry_bot)}" x2="{fmt(rx1 + 6)}" y2="{fmt(ry_bot)}"/>')
    doc.add(arrow_head(rx1 + 6, ry_bot, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry_bot)}" x2="{fmt(rx0)}" y2="{fmt(ry_top - 8)}"/>')
    doc.add(arrow_head(rx0, ry_top - 8, 0, -1, 6.5))
    doc.add(f'<text class="sm" x="{fmt(0.5*(rx0+rx1))}" y="{fmt(ry_bot + 35)}" text-anchor="middle">固定基荷占比 P{sub("fix")} / P{sub("budget")}（总预算 600 μW）</text>')
    doc.add(f'<text class="sm" x="526" y="{fmt(0.5*(ry_bot+ry_top))}" text-anchor="middle" transform="rotate(-90 526 {fmt(0.5*(ry_bot+ry_top))})">活跃通道上限 N{sub("active")} (条)</text>')

    # Key operating points from Ch19 §4.1
    x1, y1 = rx(f_base), ry(n_base)
    x2, y2 = rx(f_dbl), ry(n_dbl)
    xp, yp = rx(0.60), ry(1800.0)
    doc.add(f'<circle class="c1-fill" cx="{fmt(x1)}" cy="{fmt(y1)}" r="5.2"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(x2, y2, 6.0)}"/>')
    doc.add(f'<polygon class="c3-fill" points="{tri_pts(xp, yp, 6.0)}"/>')

    # Clean non-overlapping callouts
    doc.add(f'<line class="c1" stroke-width="1.1" x1="{fmt(x1 - 4)}" y1="{fmt(y1 + 5)}" x2="{fmt(rx(0.32))}" y2="{fmt(ry(450))}"/>')
    doc.add(f'<text class="xsb c1-txt" x="{fmt(rx(0.33))}" y="{fmt(ry(340))}">基线 33.3% → 1,000 条</text>')

    doc.add(f'<line class="c2" stroke-width="1.1" x1="{fmt(x2 + 4)}" y1="{fmt(y2 - 5)}" x2="{fmt(rx(0.54))}" y2="{fmt(ry(2520))}"/>')
    doc.add(f'<text class="xsb c2-txt" x="{fmt(rx(0.55))}" y="{fmt(ry(2620))}">静态翻倍 46.7% → 1,600 条</text>')
    doc.add(f'<text class="xs c2-txt" x="{fmt(rx(0.55))}" y="{fmt(ry(2410))}">（通道仅 +60%，并非翻倍）</text>')

    doc.add(f'<line class="c3" stroke-width="1.1" x1="{fmt(xp + 4)}" y1="{fmt(yp - 4)}" x2="{fmt(rx(0.74))}" y2="{fmt(ry(2020))}"/>')
    doc.add(f'<text class="xsb c3-txt" x="{fmt(rx(0.75))}" y="{fmt(ry(2030))}">峰值 1,800 条</text>')
    doc.add(f'<text class="xs c3-txt" x="{fmt(rx(0.75))}" y="{fmt(ry(1820))}">超 60% 反坍塌</text>')

    # Bottom formula box
    doc.add('<rect class="pill" x="522" y="486" width="436" height="52" rx="9"/>')
    doc.add(f'<text class="xsb" x="740" y="506" text-anchor="middle">N{sub("active")} ≤ (600 − P{sub("static")} − 120) / p{sub("ch")}；静态基荷挤占净预算</text>')
    doc.add('<text class="xs" x="740" y="526" text-anchor="middle">用更高静态逻辑换取更低每通道功耗，只有在跨过盈亏平衡点后才划算</text>')

    return doc.render(), {"drop_ratio": drop_ratio, "n_base": n_base, "n_dbl": n_dbl, "n_peak": n_env(0.6)}


# ---------------------------------------------------------------------------
# Figure 4: Ch 19 — 20-Task FIFO Burst Latency + Tail Quantiles & Union Downtime
# ---------------------------------------------------------------------------
def build_fig4_queue_tail_latency() -> tuple[str, dict[str, float]]:
    # Exact 20-job FIFO queue from codes/systems/round72_checks.py (case19)
    services = [Fraction(4, 5)] * 20
    services[2] = Fraction(4, 1)
    end = Fraction(0)
    jobs: list[dict[str, float]] = []
    for n, s in enumerate(services):
        arr = Fraction(n)
        start = max(arr, end)
        end = start + s
        lat = end - arr
        wait = start - arr
        jobs.append({"n": n, "s": float(s), "w": float(wait), "lat": float(lat), "miss": float(lat > 2)})
    misses = sum(int(j["miss"]) for j in jobs)
    mean_s = float(sum(services) / 20)
    assert misses == 10
    assert abs(mean_s - 0.96) < 1e-12
    assert abs(jobs[2]["lat"] - 4.0) < 1e-12
    assert abs(jobs[12]["lat"] - 2.0) < 1e-12

    # Exact service_timeline.py downtime union (hours in [0, 24])
    def union_len(ivs: list[tuple[int, int]]) -> int:
        merged: list[list[int]] = []
        for a, b in sorted(ivs):
            if merged and a <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], b)
            else:
                merged.append([a, b])
        return sum(b - a for a, b in merged)

    unavail = union_len([(2, 5), (4, 6)])
    out_spec = union_len([(2, 5), (4, 6), (10, 12)])
    assert unavail == 4 and out_spec == 6
    online_pct = (24 - unavail) / 24.0
    qual_pct = (24 - out_spec) / 24.0
    naive_pct = (21 / 24.0) * (22 / 24.0)

    # Calibrated log-normal density matching Ch19 §8.4 archived d=7 decoder stats (p50=14.917, p99=38.500)
    mu_ln = math.log(14.917)
    sig_ln = math.log(38.500 / 14.917) / 2.326348
    def ln_pdf(t: float) -> float:
        if t <= 1e-6:
            return 0.0
        return math.exp(-0.5 * ((math.log(t) - mu_ln) / sig_ln) ** 2) / (t * sig_ln * math.sqrt(2.0 * math.pi))

    doc = SvgDoc(
        title="20 任务 FIFO 实时解码排队尾延迟与停机并集可用率",
        desc=(
            "左面板按精确有理数复算 20 任务单服务台 FIFO 队列（每 1 μs 到达、常规服务 0.8 μs、n=2 突发 4.0 μs）："
            "尽管平均服务 0.96 μs < 1 μs，单次突发仍致 n=2 至 n=11 共 10 项（50%）击穿 2.0 μs 硬反馈截止线。"
            "右面板上部标出 d=7 归档解码的 p50 = 14.9 μs、p99 = 38.5 μs、max = 59.1 μs 及 SLA 预算。曲线是以 p50 和 p99 校准的对数正态示意。"
            "下部绘制 service_timeline.py 的 24 小时合成重叠停机区间并集时间轴（在线 83.3%、合格 75.0%）。"
        ),
    )
    doc.add_header(
        "20 任务 FIFO 解码排队尾延迟与停机并集可用率",
        "左：突发排队使均速达标队列半数超时（2.0 μs 截止线）；右：解码尾延迟分位与 24 h 停机区间并集核算",
    )
    doc.add_panel(28, 96, 464, 456, "20 任务 FIFO 实时解码响应时延（平均服务 0.96 μs）")
    doc.add_panel(508, 96, 464, 456, "解码尾延迟分布与 24 h 停机并集可用率")

    # --- Left Panel: 20-Job FIFO Stacked Wait + Service & Sawtooth Latency ---
    px0, px1 = 82.0, 474.0
    py_bot, py_top = 424.0, 178.0  # latency in [0, 4.5] us
    lat_max = 4.5
    slot_w = (px1 - px0) / 20.0
    bw = slot_w * 0.66

    def qx(idx: float) -> float:
        return px0 + (idx + 0.5) * slot_w

    def qy(val: float) -> float:
        return py_bot - (val / lat_max) * (py_bot - py_top)

    # Legend above left plot
    doc.add('<rect class="c1-soft" x="48" y="147" width="13" height="11" rx="2"/>')
    doc.add(f'<text class="xs" x="66" y="157">服务 s{sub("n")}</text>')
    doc.add('<rect class="c4-soft" x="128" y="147" width="13" height="11" rx="2"/>')
    doc.add(f'<text class="xs" x="146" y="157">排队等待 w{sub("n")}</text>')
    doc.add('<rect class="c2-soft" x="234" y="147" width="13" height="11" rx="2"/>')
    doc.add('<text class="xs" x="252" y="157">突发 / 超时项</text>')
    doc.add('<line class="c2" stroke-width="2" stroke-dasharray="5 3" x1="354" y1="152" x2="378" y2="152"/>')
    doc.add('<text class="xs c2-txt" x="384" y="157">截止 2.0 μs</text>')

    # Shaded miss zone above 2.0 us
    y_dead = qy(2.0)
    doc.add(f'<rect class="forbid" x="{fmt(px0)}" y="{fmt(py_top)}" width="{fmt(px1 - px0)}" height="{fmt(y_dead - py_top)}"/>')

    for yt_v in [0.0, 1.0, 2.0, 3.0, 4.0]:
        yy = qy(yt_v)
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(yy)}" x2="{fmt(px1)}" y2="{fmt(yy)}"/>')
        doc.add(f'<text class="xs" x="{fmt(px0 - 6)}" y="{fmt(yy + 3.5)}" text-anchor="end">{yt_v:.1f}</text>')
    for nt in [0, 2, 5, 8, 11, 12, 15, 19]:
        doc.add(f'<text class="xs" x="{fmt(qx(nt))}" y="{fmt(py_bot + 16)}" text-anchor="middle">{nt}</text>')

    # Stacked bars: bottom = wait w_n, top = service s_n
    saw_pts: list[tuple[float, float]] = []
    for j in jobs:
        xc = qx(j["n"])
        x_l = xc - bw / 2.0
        y_w = qy(j["w"])
        y_l = qy(j["lat"])
        saw_pts.append((xc, y_l))
        if j["w"] > 1e-9:
            w_cls = "c4-soft"
            doc.add(f'<rect class="{w_cls}" x="{fmt(x_l)}" y="{fmt(y_w)}" width="{fmt(bw)}" height="{fmt(py_bot - y_w)}" rx="1.5"/>')
        s_cls = "c2-soft" if j["miss"] else "c1-soft"
        doc.add(f'<rect class="{s_cls}" x="{fmt(x_l)}" y="{fmt(y_l)}" width="{fmt(bw)}" height="{fmt(y_w - y_l)}" rx="1.5"/>')
        if j["n"] == 2:
            doc.add(f'<rect fill="url(#hatch-red)" x="{fmt(x_l)}" y="{fmt(y_l)}" width="{fmt(bw)}" height="{fmt(y_w - y_l)}" rx="1.5"/>')

    # Sawtooth envelope & deadline/mean reference lines
    doc.add(f'<path class="axis" stroke-width="1.6" d="{path_from_points(saw_pts)}"/>')
    doc.add(f'<line class="c2" stroke-width="2.2" stroke-dasharray="7 4" x1="{fmt(px0)}" y1="{fmt(y_dead)}" x2="{fmt(px1)}" y2="{fmt(y_dead)}"/>')
    y_mean = qy(mean_s)
    doc.add(f'<line class="c3" stroke-width="1.7" stroke-dasharray="3 3" x1="{fmt(px0)}" y1="{fmt(y_mean)}" x2="{fmt(px1)}" y2="{fmt(y_mean)}"/>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px1 + 6)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(px1 + 6, py_bot, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(px0, py_top - 8, 0, -1, 6.5))
    doc.add(f'<text class="sm" x="{fmt(0.5*(px0+px1))}" y="{fmt(py_bot + 34)}" text-anchor="middle">到达任务编号 n（到达间隔 1.0 μs）</text>')
    doc.add(f'<text class="sm" x="44" y="{fmt(0.5*(py_bot+py_top))}" text-anchor="middle" transform="rotate(-90 44 {fmt(0.5*(py_bot+py_top))})">响应时延 ℓ{sub("n")} = f{sub("n")} − a{sub("n")} (μs)</text>')

    # Non-overlapping callouts inside open upper-right space
    doc.add(f'<text class="xsb c2-txt" x="218" y="200">n=2 突发 s₂ = 4.0 μs</text>')
    doc.add(f'<line class="c2" stroke-width="1.1" x1="{fmt(qx(2) + 8)}" y1="{fmt(qy(4.0))}" x2="213" y2="196"/>')
    doc.add('<text class="xsb c2-txt" x="356" y="232" text-anchor="middle">n = 2–11 共 10 项超时 (50%)</text>')
    doc.add('<text class="xs c2-txt" x="356" y="250" text-anchor="middle">每项仅消化 1.0 − 0.8 = 0.2 μs</text>')
    doc.add(f'<text class="xsb c3-txt" x="406" y="{fmt(y_dead - 8)}" text-anchor="middle">n=12 恢复 ≤ 2.0 μs</text>')
    doc.add(f'<text class="xsb c3-txt" x="468" y="{fmt(qy(1.32))}" text-anchor="end">均值 0.96 μs</text>')
    doc.add(f'<line class="c3" stroke-width="1.1" x1="452" y1="{fmt(qy(1.22))}" x2="452" y2="{fmt(y_mean - 2)}"/>')

    # Bottom takeaway pill in Left Panel
    doc.add('<rect class="pill" x="44" y="476" width="432" height="62" rx="10"/>')
    doc.add(f'<text class="xsb" x="58" y="497">FIFO 递推：b{sub("n")} = max(a{sub("n")}, f{sub("n−1")})，ℓ{sub("n")} = b{sub("n")} + s{sub("n")} − a{sub("n")}</text>')
    doc.add('<text class="xs" x="58" y="517">增配第二台解码器可即时消除 n≥3 排队积压，但仍无法把 s₂ = 4.0 μs 压进 2.0 μs</text>')

    # --- Right Panel Top: Decoder Tail Latency Distribution ---
    doc.add('<text class="xsb" x="522" y="154">① 归档分位点与示意密度（d=7；固定通信 +8 μs）</text>')
    dx0, dx1 = 562.0, 950.0
    dy_bot, dy_top = 290.0, 174.0
    t_max_d = 70.0
    pdf_peak = ln_pdf(math.exp(mu_ln - sig_ln * sig_ln))

    def dx(tv: float) -> float:
        return dx0 + (tv / t_max_d) * (dx1 - dx0)

    def dy(pv: float) -> float:
        return dy_bot - (pv / (pdf_peak * 1.15)) * (dy_bot - dy_top)

    # Grid & ticks
    for tv in [0, 15, 30, 45, 60]:
        xt = dx(float(tv))
        doc.add(f'<line class="grid" x1="{fmt(xt)}" y1="{fmt(dy_top)}" x2="{fmt(xt)}" y2="{fmt(dy_bot)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xt)}" y="{fmt(dy_bot + 14)}" text-anchor="middle">{tv} μs</text>')

    # Density curve & SLA breach shading (t >= 42 us, since 42 + 8 = 50 us SLA)
    ts_all = [t_max_d * i / 180.0 for i in range(181)]
    pdf_pts = [(dx(t), dy(ln_pdf(t))) for t in ts_all]
    doc.add(f'<polygon class="area1" points="{pts_str([(dx0, dy_bot)] + pdf_pts + [(dx1, dy_bot)])}"/>')
    breach_pts = [(dx(t), dy(ln_pdf(t))) for t in ts_all if t >= 42.0]
    if breach_pts:
        doc.add(f'<polygon class="forbid" points="{pts_str([(dx(42.0), dy_bot)] + breach_pts + [(dx1, dy_bot)])}"/>')
    doc.add(f'<path class="c1" stroke-width="2.3" d="{path_from_points(pdf_pts)}"/>')

    # Quantile markers: p50=14.9, p99=38.5, SLA=42, max=59.1
    for qv, cls_q, fill_q in [(14.917, "c1", "c1-fill"), (38.500, "c4", "c4-fill"), (59.125, "c2", "c2-fill")]:
        xq, yq = dx(qv), dy(ln_pdf(qv))
        doc.add(f'<line class="guide" x1="{fmt(xq)}" y1="{fmt(yq)}" x2="{fmt(xq)}" y2="{fmt(dy_bot)}"/>')
        doc.add(f'<circle class="{fill_q}" cx="{fmt(xq)}" cy="{fmt(yq)}" r="4.2"/>')
    doc.add(f'<line class="c2" stroke-width="1.9" stroke-dasharray="5 3" x1="{fmt(dx(42.0))}" y1="{fmt(dy_top)}" x2="{fmt(dx(42.0))}" y2="{fmt(dy_bot)}"/>')

    # Clean non-overlapping quantile labels
    doc.add(f'<text class="xsb c1-txt" x="{fmt(dx(15.5))}" y="182">p50 = 14.9 μs</text>')
    doc.add(f'<text class="xsb c4-txt" x="{fmt(dx(36.2))}" y="236" text-anchor="end">p99 = 38.5</text>')
    doc.add(f'<line class="c4" stroke-width="1.1" x1="{fmt(dx(35.8))}" y1="241" x2="{fmt(dx(38.5) - 2)}" y2="{fmt(dy(ln_pdf(38.5)) - 4)}"/>')
    doc.add(f'<text class="xsb c2-txt" x="{fmt(dx(43.5))}" y="190">SLA 预算 42 μs</text>')
    doc.add(f'<text class="xs c2-txt" x="{fmt(dx(43.5))}" y="207">(+8 通信 = 50 μs)</text>')
    doc.add('<text class="xsb c2-txt" x="954" y="252" text-anchor="end">max = 59.1 μs (N=1,000)</text>')
    doc.add('<text class="xs c2-txt" x="954" y="268" text-anchor="end">（超 SLA 违约!）</text>')
    doc.add(f'<line class="c2" stroke-width="1.1" x1="{fmt(dx(59.125))}" y1="272" x2="{fmt(dx(59.125))}" y2="{fmt(dy(ln_pdf(59.125)) - 5)}"/>')

    doc.add(f'<line class="axis" x1="{fmt(dx0)}" y1="{fmt(dy_bot)}" x2="{fmt(dx1 + 6)}" y2="{fmt(dy_bot)}"/>')
    doc.add(arrow_head(dx1 + 6, dy_bot, 1, 0, 6.0))
    doc.add(f'<line class="axis" x1="{fmt(dx0)}" y1="{fmt(dy_bot)}" x2="{fmt(dx0)}" y2="{fmt(dy_top - 6)}"/>')
    doc.add(arrow_head(dx0, dy_top - 6, 0, -1, 6.0))
    doc.add('<text class="xs" x="526" y="232" text-anchor="middle" transform="rotate(-90 526 232)">对数正态示意</text>')

    # --- Right Panel Bottom: 24-Hour Overlapping Downtime Union Timeline ---
    doc.add('<line class="grid" x1="520" y1="322" x2="958" y2="322"/>')
    doc.add('<text class="xsb" x="522" y="342">② 24 h 合成日志的停机并集（service_timeline.py）</text>')
    tx0, tx1 = 594.0, 948.0
    th_h = 17.0

    def hx(hr: float) -> float:
        return tx0 + (hr / 24.0) * (tx1 - tx0)

    for hr in [0, 4, 8, 12, 16, 20, 24]:
        xh = hx(float(hr))
        doc.add(f'<line class="grid" x1="{fmt(xh)}" y1="354" x2="{fmt(xh)}" y2="458"/>')
        doc.add(f'<text class="xs" x="{fmt(xh)}" y="473" text-anchor="middle">{hr}h</text>')

    tracks = [
        (356.0, "计划校准", [(2, 5, "c1-soft")]),
        (381.0, "故障停机", [(4, 6, "c2-soft")]),
        (406.0, "降级超标", [(10, 12, "c4-soft")]),
        (431.0, "并集结果", [(0, 2, "c3-soft"), (2, 6, "c2-soft"), (6, 10, "c3-soft"), (10, 12, "c4-soft"), (12, 24, "c3-soft")]),
    ]
    for ty, tname, segs in tracks:
        doc.add(f'<text class="xsb" x="586" y="{fmt(ty + 12.5)}" text-anchor="end">{tname}</text>')
        doc.add(f'<rect class="pill" fill-opacity=".35" x="{fmt(tx0)}" y="{fmt(ty)}" width="{fmt(tx1 - tx0)}" height="{fmt(th_h)}" rx="3"/>')
        for a, b, scls in segs:
            doc.add(f'<rect class="{scls}" x="{fmt(hx(a))}" y="{fmt(ty)}" width="{fmt(hx(b) - hx(a))}" height="{fmt(th_h)}" rx="3"/>')
    # Hatch the union outage [2,6) on track 4 & mark [4,5) overlap
    doc.add(f'<rect fill="url(#hatch-red)" x="{fmt(hx(2))}" y="431" width="{fmt(hx(6) - hx(2))}" height="{fmt(th_h)}" rx="3"/>')
    doc.add(f'<text class="xs c2-txt" x="{fmt(hx(6.5))}" y="394">← [4,5) 重叠 1 h（去重防误乘）</text>')
    doc.add(f'<text class="xs c4-txt" x="{fmt(hx(12.5))}" y="419">← 降级 2 h（不计合格）</text>')
    doc.add(f'<text class="xsb c3-txt" x="{fmt(hx(18.0))}" y="443.5" text-anchor="middle">合格 18 h (75%)</text>')

    # Bottom availability summary pill
    doc.add('<rect class="pill" x="522" y="486" width="436" height="52" rx="9"/>')
    doc.add(f'<text class="xsb" x="740" y="506" text-anchor="middle">并集在线 20/24 = {online_pct*100:.1f}%（非朴素独立积 {naive_pct*100:.1f}%）</text>')
    doc.add(f'<text class="xs" x="740" y="526" text-anchor="middle">合格运行 18/24 = {qual_pct*100:.1f}% → 墙钟合格吞吐 75 k shot/s（峰值 100 k）</text>')

    return doc.render(), {"mean_s": mean_s, "misses": float(misses), "online_pct": online_pct, "qual_pct": qual_pct}


# ---------------------------------------------------------------------------
# Figure 5: Q4 — Symmetric Double-Well Splitting + Free Gaussian Wavepacket
# ---------------------------------------------------------------------------
def build_fig5_double_well_splitting() -> tuple[str, dict[str, float]]:
    # Finite-difference reference for V(x) = (x^2 - a^2)^2 / (8 a^2), at a = 2.4.
    a_vis = 2.4
    xs, e_plus, e_minus, psi_p, psi_m = _solve_quartic_double_well(a_vis, n_grid=241, x_lim=4.4)
    delta_vis = e_minus - e_plus
    assert delta_vis > 0.01 and e_minus < (a_vis ** 2) / 8.0
    # Verify parity numerically
    assert max(abs(psi_p[i] - psi_p[-1 - i]) for i in range(len(xs))) < 1e-10
    assert max(abs(psi_m[i] + psi_m[-1 - i]) for i in range(len(xs))) < 1e-10

    # Finite differences vs. Garg and Landau-Lifshitz WKB over a in [3.0, 5.0].
    def wkb_action(a_val: float, e_avg: float) -> float:
        # Turning point b where (b^2 - a^2)^2 / (8 a^2) = e_avg -> b^2 = a^2 - a*sqrt(8*e_avg)
        rad = a_val * a_val - a_val * math.sqrt(8.0 * e_avg)
        if rad <= 0.0:
            return 0.0
        b = math.sqrt(rad)
        n_steps = 200
        dx = b / n_steps
        # Integrate 2 * int_0^b sqrt(2*(V(x) - e_avg)) dx via midpoint rule
        acc = 0.0
        for i in range(n_steps):
            x = (i + 0.5) * dx
            vx = ((x * x - a_val * a_val) ** 2) / (8.0 * a_val * a_val)
            acc += math.sqrt(max(0.0, 2.0 * (vx - e_avg)))
        return 2.0 * acc * dx

    a_scan = [3.0, 3.4, 3.8, 4.2, 4.6, 5.0]
    wkb_rows: list[tuple[float, float, float, float]] = []
    for av in a_scan:
        _, ep, em, _, _ = _solve_quartic_double_well(av, n_grid=321, x_lim=av + 4.0)
        de_ex = em - ep
        s_tp = wkb_action(av, 0.5 * (ep + em))
        de_garg = math.exp(-s_tp) / math.sqrt(math.e * math.pi)
        de_ll = math.exp(-s_tp) / math.pi
        wkb_rows.append((av, de_ex, de_garg, de_ll))
    # Verify the reference range and the change in sign of the LL error.
    assert 1.2e-2 < wkb_rows[0][1] < 1.5e-2
    assert 5.0e-7 < wkb_rows[-1][1] < 7.5e-7
    assert wkb_rows[0][3] > wkb_rows[0][1] and wkb_rows[-1][3] < wkb_rows[-1][1]
    assert abs((wkb_rows[-1][2] / wkb_rows[-1][3]) - math.sqrt(math.pi / math.e)) < 1e-10

    # Exact Gaussian wavepacket normalization check at tau = 0, 1, 2, 3
    def gauss_rho(u_pos: float, tau: float) -> float:
        sig = math.sqrt(1.0 + tau * tau)
        return math.exp(-0.5 * (u_pos / sig) ** 2) / (math.sqrt(2.0 * math.pi) * sig)

    for tau_chk in (0.0, 1.0, 2.0, 3.0):
        du = 0.05
        area = sum(gauss_rho(-18.0 + i * du, tau_chk) * du for i in range(721))
        assert abs(area - 1.0) < 1e-6

    doc = SvgDoc(
        title="对称双势阱隧穿能级劈裂与自由高斯波包色散展宽",
        desc=(
            "左面板上部用有限差分绘制四次对称双势阱 V(ξ) = (ξ²−a²)²/(8a²)（a = 2.4）、"
            "偶基态波函数 ψ₊(ξ)（无节点）与奇第一激发态 ψ₋(ξ)（原点过零）及隧穿劈裂 ΔE；"
            "中部对数图对比 a = 3.0–5.0 有限差分参考值与 Garg、Landau-Lifshitz 两条 WKB 曲线；底部标出 NH₃ 与 Fluxonium Φ₀/2 甜点。"
            "右面板绘制自由高斯波包在无量纲时间 τ = 0, 1, 2, 3 的精确概率密度 |ψ(x,t)|² 及宽度展宽 σ(t)/σ₀ = √(1+τ²)。"
        ),
    )
    doc.add_header(
        "对称双势阱隧穿能级劈裂与自由高斯波包色散展宽",
        f"左：双势阱 V(ξ)、偶/奇杂化态 ψ{sub('+')} / ψ{sub('−')} 与 WKB 劈裂；右：自由高斯波包精确概率密度与展宽轨迹",
        raw_sub=True,
    )
    doc.add_panel(28, 96, 464, 456, "对称双势阱、偶/奇态与 WKB 劈裂（精确求解）")
    doc.add_panel(508, 96, 464, 456, "自由高斯波包色散展宽（精确概率密度演化）")

    # --- Left Panel Upper: Double Well V(x) & Exact psi_+, psi_- ---
    wx0, wx1 = 84.0, 472.0
    wy_bot, wy_top = 314.0, 168.0
    x_span = 4.0
    v_max = 1.25

    def dw_x(xi: float) -> float:
        return wx0 + ((xi + x_span) / (2.0 * x_span)) * (wx1 - wx0)

    def dw_y(ev: float) -> float:
        return wy_bot - (ev / v_max) * (wy_bot - wy_top)

    # Legend above upper plot
    doc.add('<line class="axis" stroke-width="2.0" x1="48" y1="150" x2="72" y2="150"/>')
    doc.add('<text class="xs" x="78" y="154">势阱 V(ξ)</text>')
    doc.add('<line class="c1" stroke-width="2.3" x1="152" y1="150" x2="176" y2="150"/>')
    doc.add(f'<text class="xs c1-txt" x="182" y="154">偶基态 ψ{sub("+")}(ξ)</text>')
    doc.add('<line class="c2" stroke-width="2.2" stroke-dasharray="6 4" x1="286" y1="150" x2="310" y2="150"/>')
    doc.add(f'<text class="xs c2-txt" x="316" y="154">奇激发态 ψ{sub("−")}(ξ)</text>')

    # Light grid & symmetry axis xi = 0
    doc.add(f'<line class="guide" x1="{fmt(dw_x(0.0))}" y1="{fmt(wy_top)}" x2="{fmt(dw_x(0.0))}" y2="{fmt(wy_bot)}"/>')
    # Potential curve V(xi) clipped to v_max
    v_pts = []
    for i in range(161):
        xi = -x_span + 2.0 * x_span * i / 160.0
        vx = ((xi * xi - a_vis * a_vis) ** 2) / (8.0 * a_vis * a_vis)
        if vx <= v_max:
            v_pts.append((dw_x(xi), dw_y(vx)))
    doc.add(f'<path class="axis" stroke-width="2.0" d="{path_from_points(v_pts)}"/>')

    # Energy baselines E_+ and E_- (slight display separation for wavefunctions; exact E lines shown)
    ye_p, ye_m = dw_y(e_plus), dw_y(e_minus)
    doc.add(f'<line class="c1" stroke-width="1.2" stroke-dasharray="3 3" x1="{fmt(dw_x(-3.35))}" y1="{fmt(ye_p)}" x2="{fmt(dw_x(3.55))}" y2="{fmt(ye_p)}"/>')
    doc.add(f'<line class="c2" stroke-width="1.2" stroke-dasharray="3 3" x1="{fmt(dw_x(-3.35))}" y1="{fmt(ye_m)}" x2="{fmt(dw_x(3.55))}" y2="{fmt(ye_m)}"/>')

    # Exact normalized eigenfunctions (scaled cleanly around their energy levels)
    amp_scale = 0.40
    p_pts = [(dw_x(xi), dw_y(e_plus + amp_scale * pv)) for xi, pv in zip(xs, psi_p) if abs(xi) <= 3.55]
    m_pts = [(dw_x(xi), dw_y(e_minus + amp_scale * mv)) for xi, mv in zip(xs, psi_m) if abs(xi) <= 3.55]
    doc.add(f'<path class="c1" stroke-width="2.4" d="{path_from_points(p_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.2" stroke-dasharray="7 4" d="{path_from_points(m_pts)}"/>')

    # Zero-node dot for psi_- at origin
    doc.add(f'<circle class="c2-fill" cx="{fmt(dw_x(0.0))}" cy="{fmt(ye_m)}" r="3.6"/>')

    # Splitting bracket on right side
    bx_d = dw_x(3.64)
    doc.add(f'<line class="c3" stroke-width="1.8" x1="{fmt(bx_d)}" y1="{fmt(ye_m)}" x2="{fmt(bx_d)}" y2="{fmt(ye_p)}"/>')
    doc.add(f'<text class="xsb c3-txt" x="{fmt(bx_d + 6)}" y="{fmt(0.5*(ye_m+ye_p) + 4)}">ΔE</text>')

    # Axes & labels
    doc.add(f'<line class="axis" x1="{fmt(wx0)}" y1="{fmt(wy_bot)}" x2="{fmt(wx1 + 6)}" y2="{fmt(wy_bot)}"/>')
    doc.add(arrow_head(wx1 + 6, wy_bot, 1, 0, 6.0))
    doc.add(f'<line class="axis" x1="{fmt(wx0)}" y1="{fmt(wy_bot)}" x2="{fmt(wx0)}" y2="{fmt(wy_top - 6)}"/>')
    doc.add(arrow_head(wx0, wy_top - 6, 0, -1, 6.0))
    doc.add(f'<text class="xs" x="48" y="{fmt(0.5*(wy_bot+wy_top))}" text-anchor="middle" transform="rotate(-90 48 {fmt(0.5*(wy_bot+wy_top))})">能量 E / ℏω</text>')
    doc.add(f'<text class="xsb" x="{fmt(dw_x(-a_vis))}" y="{fmt(wy_bot + 14)}" text-anchor="middle">−a (|L⟩)</text>')
    doc.add(f'<text class="xs" x="{fmt(dw_x(0.0))}" y="{fmt(wy_bot + 14)}" text-anchor="middle">0 (势垒)</text>')
    doc.add(f'<text class="xsb" x="{fmt(dw_x(a_vis))}" y="{fmt(wy_bot + 14)}" text-anchor="middle">+a (|R⟩)</text>')
    doc.add(f'<text class="xs c2-txt" x="{fmt(dw_x(0.0))}" y="{fmt(dw_y(0.72) - 10)}" text-anchor="middle">势垒 V₀（奇态过零节点）</text>')

    # --- Left Panel Lower: Log-Y Exact Splitting vs Garg & LL WKB ---
    doc.add('<text class="xsb" x="52" y="346">隧穿劈裂 ΔE / ℏω 随井距 a 指数骤降（精确解 vs WKB）</text>')
    kx0, kx1 = 84.0, 472.0
    ky_bot, ky_top = 446.0, 358.0  # log10 in [-7, -1]
    def kx(av: float) -> float:
        return kx0 + ((av - 3.0) / 2.0) * (kx1 - kx0)
    def ky(val: float) -> float:
        lv = math.log10(val)
        return ky_bot - ((lv - (-7.0)) / 6.0) * (ky_bot - ky_top)

    for exp, lbl in [(-7, "10⁻⁷"), (-5, "10⁻⁵"), (-3, "10⁻³"), (-1, "10⁻¹")]:
        yy = ky(10.0 ** exp)
        doc.add(f'<line class="grid" x1="{fmt(kx0)}" y1="{fmt(yy)}" x2="{fmt(kx1)}" y2="{fmt(yy)}"/>')
        doc.add(f'<text class="xs" x="{fmt(kx0 - 6)}" y="{fmt(yy + 3.5)}" text-anchor="end">{lbl}</text>')
    for at in [3.0, 3.5, 4.0, 4.5, 5.0]:
        xx = kx(at)
        doc.add(f'<line class="grid" x1="{fmt(xx)}" y1="{fmt(ky_top)}" x2="{fmt(xx)}" y2="{fmt(ky_bot)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xx)}" y="{fmt(ky_bot + 16)}" text-anchor="middle">{at:g}</text>')

    garg_pts = [(kx(r[0]), ky(r[2])) for r in wkb_rows]
    ll_pts = [(kx(r[0]), ky(r[3])) for r in wkb_rows]
    doc.add(f'<path class="c3" stroke-width="2.2" d="{path_from_points(garg_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="1.8" stroke-dasharray="5 4" d="{path_from_points(ll_pts)}"/>')
    for av, de_ex, _, _ in wkb_rows:
        doc.add(f'<circle class="c1-fill" cx="{fmt(kx(av))}" cy="{fmt(ky(de_ex))}" r="3.6"/>')

    doc.add(f'<line class="axis" x1="{fmt(kx0)}" y1="{fmt(ky_bot)}" x2="{fmt(kx1 + 6)}" y2="{fmt(ky_bot)}"/>')
    doc.add(arrow_head(kx1 + 6, ky_bot, 1, 0, 5.5))
    doc.add(f'<line class="axis" x1="{fmt(kx0)}" y1="{fmt(ky_bot)}" x2="{fmt(kx0)}" y2="{fmt(ky_top - 6)}"/>')
    doc.add(arrow_head(kx0, ky_top - 6, 0, -1, 5.5))
    doc.add('<text class="xs c3-txt" x="308" y="376">● 差分参考  — Garg (1/√(eπ))</text>')
    doc.add('<text class="xs c2-txt" x="308" y="393">-- LL (1/π，偏差随 a 变号)</text>')

    # Bottom physical bridge pill in Left Panel
    doc.add('<rect class="note" x="44" y="478" width="432" height="60" rx="10"/>')
    doc.add(f'<text class="xsb" x="58" y="499">物理硬件桥梁：氨分子 NH{sub("3")} 反转劈裂 23.78 GHz（首台 Maser）</text>')
    doc.add(f'<text class="xs" x="58" y="521">超导 Fluxonium（Φ{sub("ext")} = Φ₀/2 甜点）：大非谐性且对低频磁通噪声一阶免疫</text>')

    # --- Right Panel Upper: Exact Gaussian Wavepacket Dispersion ---
    gx0, gx1 = 568.0, 950.0
    gy_bot, gy_top = 314.0, 168.0  # rho * sigma0 in [0, 0.45], u in [-6, 6]
    u_lim = 6.0
    rho_max = 0.45

    def gwx(u_v: float) -> float:
        return gx0 + ((u_v + u_lim) / (2.0 * u_lim)) * (gx1 - gx0)

    def gwy(rv: float) -> float:
        return gy_bot - (rv / rho_max) * (gy_bot - gy_top)

    # Legend above plot
    leg_g = [(522, "c1", "", "τ=0"), (596, "c3", "6 4", "τ=1 (√2σ₀)"), (718, "c4", "7 3 2 3", "τ=2"), (804, "c2", "2 3", "τ=3")]
    for lx_g, lcls, ldash, ltxt in leg_g:
        da = f' stroke-dasharray="{ldash}"' if ldash else ""
        doc.add(f'<line class="{lcls}" stroke-width="2.3"{da} x1="{lx_g}" y1="150" x2="{lx_g + 22}" y2="150"/>')
        doc.add(f'<text class="xs" x="{lx_g + 27}" y="154">{ltxt}</text>')

    for rv in [0.0, 0.2, 0.4]:
        yr = gwy(rv)
        doc.add(f'<line class="grid" x1="{fmt(gx0)}" y1="{fmt(yr)}" x2="{fmt(gx1)}" y2="{fmt(yr)}"/>')
        doc.add(f'<text class="xs" x="{fmt(gx0 - 6)}" y="{fmt(yr + 3.5)}" text-anchor="end">{rv:.1f}</text>')
    for uv in [-6, -3, 0, 3, 6]:
        xu = gwx(float(uv))
        doc.add(f'<line class="grid" x1="{fmt(xu)}" y1="{fmt(gy_top)}" x2="{fmt(xu)}" y2="{fmt(gy_bot)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xu)}" y="{fmt(gy_bot + 14)}" text-anchor="middle">{uv}</text>')

    # Exact probability density curves for tau = 0, 1, 2, 3
    u_grid = [-u_lim + 2.0 * u_lim * i / 160.0 for i in range(161)]
    pts_t0 = [(gwx(uv), gwy(gauss_rho(uv, 0.0))) for uv in u_grid]
    doc.add(f'<polygon class="area1" points="{pts_str([(gx0, gy_bot)] + pts_t0 + [(gx1, gy_bot)])}"/>')
    for tau_v, cls_g, dash_g, sw_g in [
        (0.0, "c1", "", 2.6),
        (1.0, "c3", "7 4", 2.3),
        (2.0, "c4", "8 3 2 3", 2.2),
        (3.0, "c2", "2.5 3.5", 2.3),
    ]:
        pts_t = [(gwx(uv), gwy(gauss_rho(uv, tau_v))) for uv in u_grid]
        da = f' stroke-dasharray="{dash_g}"' if dash_g else ""
        doc.add(f'<path class="{cls_g}" stroke-width="{sw_g}"{da} d="{path_from_points(pts_t)}"/>')

    doc.add(f'<line class="axis" x1="{fmt(gx0)}" y1="{fmt(gy_bot)}" x2="{fmt(gx1 + 6)}" y2="{fmt(gy_bot)}"/>')
    doc.add(arrow_head(gx1 + 6, gy_bot, 1, 0, 6.0))
    doc.add(f'<line class="axis" x1="{fmt(gx0)}" y1="{fmt(gy_bot)}" x2="{fmt(gx0)}" y2="{fmt(gy_top - 6)}"/>')
    doc.add(arrow_head(gx0, gy_top - 6, 0, -1, 6.0))
    doc.add(f'<text class="xs" x="{fmt(0.5*(gx0+gx1))}" y="{fmt(gy_bot + 29)}" text-anchor="middle">随动坐标 (x − v{sub("g")}t) / σ₀</text>')
    doc.add(f'<text class="xs" x="526" y="{fmt(0.5*(gy_bot+gy_top))}" text-anchor="middle" transform="rotate(-90 526 {fmt(0.5*(gy_bot+gy_top))})">密度 |ψ|² σ₀</text>')
    doc.add('<text class="xsb c1-txt" x="866" y="190" text-anchor="middle">面积 ∫|ψ|²dx ≡ 1</text>')
    doc.add('<text class="xs" x="866" y="207" text-anchor="middle">峰值下降、宽度矮胖展宽</text>')

    # --- Right Panel Lower: Exact Width Growth sigma(tau)/sigma0 ---
    doc.add(f'<text class="xsb" x="524" y="362">波包宽度演化 σ(t)/σ₀ = √(1 + τ²)（τ = ℏt / (2mσ₀²)）</text>')
    sx0, sx1 = 568.0, 950.0
    sy_bot, sy_top = 466.0, 374.0  # sigma/sigma0 in [0, 4.5], tau in [0, 4.0]

    def s_x(tv: float) -> float:
        return sx0 + (tv / 4.0) * (sx1 - sx0)

    def s_y(sv: float) -> float:
        return sy_bot - (sv / 4.5) * (sy_bot - sy_top)

    for sv in [0, 2, 4]:
        ys = s_y(float(sv))
        doc.add(f'<line class="grid" x1="{fmt(sx0)}" y1="{fmt(ys)}" x2="{fmt(sx1)}" y2="{fmt(ys)}"/>')
        doc.add(f'<text class="xs" x="{fmt(sx0 - 6)}" y="{fmt(ys + 3.5)}" text-anchor="end">{sv}</text>')
    for tv in [0, 1, 2, 3, 4]:
        xt = s_x(float(tv))
        doc.add(f'<line class="grid" x1="{fmt(xt)}" y1="{fmt(sy_top)}" x2="{fmt(xt)}" y2="{fmt(sy_bot)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xt)}" y="{fmt(sy_bot + 16)}" text-anchor="middle">{tv}</text>')

    # Linear asymptote sigma/sigma0 = tau
    doc.add(f'<line class="guide" x1="{fmt(s_x(0.0))}" y1="{fmt(s_y(0.0))}" x2="{fmt(s_x(4.0))}" y2="{fmt(s_y(4.0))}"/>')
    sig_pts = [(s_x(4.0 * i / 100.0), s_y(math.hypot(1.0, 4.0 * i / 100.0))) for i in range(101)]
    doc.add(f'<path class="c1" stroke-width="2.5" d="{path_from_points(sig_pts)}"/>')

    # Mark tau = 1 (sqrt(2) * sigma0)
    x_t1, y_t1 = s_x(1.0), s_y(math.sqrt(2.0))
    doc.add(f'<circle class="c3-fill" cx="{fmt(x_t1)}" cy="{fmt(y_t1)}" r="4.5"/>')
    doc.add(f'<text class="xsb c3-txt" x="{fmt(x_t1 + 10)}" y="{fmt(y_t1 + 16)}">τ = 1 → √2 σ₀</text>')
    doc.add(f'<text class="xs" x="852" y="454" text-anchor="middle">1 nm 电子 τ{sub("spread")} ≈ 17.3 fs</text>')
    doc.add(f'<text class="xs" x="646" y="394" text-anchor="middle">渐近线 σ/σ₀ ≈ τ</text>')

    doc.add(f'<line class="axis" x1="{fmt(sx0)}" y1="{fmt(sy_bot)}" x2="{fmt(sx1 + 6)}" y2="{fmt(sy_bot)}"/>')
    doc.add(arrow_head(sx1 + 6, sy_bot, 1, 0, 5.5))
    doc.add(f'<line class="axis" x1="{fmt(sx0)}" y1="{fmt(sy_bot)}" x2="{fmt(sx0)}" y2="{fmt(sy_top - 6)}"/>')
    doc.add(arrow_head(sx0, sy_top - 6, 0, -1, 5.5))
    doc.add('<text class="xs" x="526" y="420" text-anchor="middle" transform="rotate(-90 526 420)">σ(t) / σ₀</text>')

    # Bottom formula pill in Right Panel
    doc.add('<rect class="pill" x="522" y="498" width="436" height="40" rx="9"/>')
    doc.add(f'<text class="xs" x="740" y="522" text-anchor="middle">自由空间 Δp = ℏ/(2σ₀) 恒定，二次色散相位使 Δx(t)Δp = (ℏ/2)√(1+τ²) 单调增大</text>')

    return doc.render(), {"delta_vis": delta_vis, "de_a3": wkb_rows[0][1], "de_a5": wkb_rows[-1][1]}


# ---------------------------------------------------------------------------
# Figure 6: Ch 20 — Quantum Sensing Scaling Limits + Ramsey Working Points
# ---------------------------------------------------------------------------
def build_fig6_sensing_limits() -> tuple[str, dict[str, float]]:
    # Exact Kitagawa-Ueda (1993) OAT Wineland squeezing parameter optimization
    def xi_r2_oat(n: int, theta: float) -> float:
        if theta <= 0.0 or theta >= 0.49 * math.pi:
            return 1.0
        c1 = math.cos(theta)
        c2 = math.cos(2.0 * theta)
        if c1 <= 1e-12:
            return 1e9
        c1_nm2 = math.exp((n - 2) * math.log(c1))
        c1_2nm2 = math.exp((2 * n - 2) * math.log(c1))
        c2_nm2 = math.copysign(math.exp((n - 2) * math.log(abs(c2))), c2 ** ((n - 2) % 2)) if abs(c2) > 1e-12 else 0.0
        a_val = 1.0 - c2_nm2
        b_val = 4.0 * math.sin(theta) * c1_nm2
        num = 1.0 + 0.25 * (n - 1) * (a_val - math.hypot(a_val, b_val))
        return max(1e-12, num / c1_2nm2)

    def opt_oat_dphi(n: int) -> tuple[float, float]:
        if n <= 1:
            return 1.0, 1.0
        if n == 2:
            # Match sensing_lab.py finite-contrast bound theta <= 0.45*pi (avoids |<Jx>| -> 0 kink)
            xi2 = 1.0 / (1.0 + math.sin(0.45 * math.pi))
            return xi2, math.sqrt(xi2 / 2.0)
        scale = n ** (-2.0 / 3.0)
        best_th, best_xi2 = scale, xi_r2_oat(n, scale)
        for i in range(1, 80):
            th = min(0.45 * math.pi, scale * (0.12 + 3.5 * i / 79.0))
            val = xi_r2_oat(n, th)
            if val < best_xi2:
                best_xi2, best_th = val, th
        # Golden-section refinement around best_th
        lo, hi = max(1e-7, best_th * 0.75), min(0.48 * math.pi, best_th * 1.25)
        gr = 0.5 * (math.sqrt(5.0) - 1.0)
        for _ in range(36):
            m1 = hi - gr * (hi - lo)
            m2 = lo + gr * (hi - lo)
            if xi_r2_oat(n, m1) < xi_r2_oat(n, m2):
                hi = m2
            else:
                lo = m1
        xi2_min = xi_r2_oat(n, 0.5 * (lo + hi))
        return xi2_min, math.sqrt(xi2_min / n)

    xi10, _ = opt_oat_dphi(10)
    xi100, _ = opt_oat_dphi(100)
    xi1000, _ = opt_oat_dphi(1000)
    assert abs(xi10 - 0.310) < 0.005
    assert abs(xi100 - 0.0629) < 0.002
    assert abs(xi1000 - 0.0120) < 0.001

    # Unified fixed-total-time T frequency uncertainty: dimensionless y = T * Delta_omega
    # (for noiseless single round t = T, y = Delta_phi identically!).
    # Markovian independent dephasing with gamma * T = 2.0 (so 2*gamma*T = 4 >= 1):
    # - Uncorrelated optimal t_opt = 1/(2*gamma) = T/4 (4 rounds) -> y_unc(N) = sqrt(2*e*gamma*T / N)
    # - Huelga GHZ optimal t_opt = 1/(2*N*gamma) = T/(4N) (4N rounds) -> y_GHZ(N) = sqrt(2*e*gamma*T / N) == y_unc(N)
    # - Exact Escher noisy ultimate bound retaining full denominator N(1-eta^2)+eta^2:
    #     F_tot^Escher(N; t) = (T/t) * N^2 t^2 / [N(exp(2*gamma*t) - 1) + 1]
    #     => y_Escher(N) = min_{0 < t <= T} sqrt( (T/t)/N^2 + (T/t)*(exp(2*gamma*t) - 1)/N )
    gamma_t_tot = 2.0

    def y_noisy_unc(n_val: float) -> float:
        t_frac = min(1.0, 1.0 / (2.0 * gamma_t_tot))
        return math.exp(gamma_t_tot * t_frac) / math.sqrt(n_val * t_frac)

    def y_huelga_ghz(n_val: float) -> float:
        t_frac = min(1.0, 1.0 / (2.0 * n_val * gamma_t_tot))
        return math.exp(n_val * gamma_t_tot * t_frac) / (n_val * math.sqrt(t_frac))

    def y_escher_exact(n_val: float) -> float:
        # Minimize f(u) = (2*a/N)*(exp(u)-1)/u + (2*a)/(N^2 * u) over u = 2*gamma*t in (0, 2*a]
        u_max = 2.0 * gamma_t_tot

        def obj(u: float) -> float:
            return (u_max / n_val) * (math.expm1(u) / u) + u_max / (n_val * n_val * u)

        best_u, best_v = u_max, obj(u_max)
        for i in range(1, 160):
            u = u_max * ((i / 160.0) ** 2)
            v = obj(u)
            if v < best_v:
                best_v, best_u = v, u
        lo = max(1e-10, best_u * 0.2)
        hi = min(u_max, best_u * 2.5)
        gr = 0.5 * (math.sqrt(5.0) - 1.0)
        for _ in range(56):
            m1 = hi - gr * (hi - lo)
            m2 = lo + gr * (hi - lo)
            if obj(m1) < obj(m2):
                hi = m2
            else:
                lo = m1
        u_opt = 0.5 * (lo + hi)
        return math.sqrt(min(obj(u_opt), obj(u_max)))

    # Strict physical invariants for ALL N >= 1:
    # 1. N=1: Huelga GHZ == Noisy single-qubit == Exact Escher bound (zero entanglement for 1 qubit!)
    assert abs(y_huelga_ghz(1.0) - y_noisy_unc(1.0)) < 1e-12
    assert abs(y_escher_exact(1.0) - y_huelga_ghz(1.0)) < 1e-7
    # 2. All N >= 1: Huelga GHZ == Noisy Uncorrelated > Exact Escher > Noiseless SQL >= Noiseless HL = 1/N
    ns_cont = [10.0 ** (4.0 * i / 80.0) for i in range(81)]
    for nv in ns_cont:
        hl_v = 1.0 / nv
        sql_v = nv ** -0.5
        ghz_v = y_huelga_ghz(nv)
        unc_v = y_noisy_unc(nv)
        esc_v = y_escher_exact(nv)
        assert abs(ghz_v - unc_v) < 1e-12
        assert ghz_v >= esc_v - 1e-7
        assert esc_v > sql_v >= hl_v - 1e-12
    # 3. Large-N asymptotic ratio GHZ / Escher approaches sqrt(e) ~ 1.6487
    ratio_1e4 = y_huelga_ghz(10000.0) / y_escher_exact(10000.0)
    assert 1.60 < ratio_1e4 < math.sqrt(math.e)
    # 4. 6 dB optical squeezing starts in macroscopic coherent regime N >= 10 (n_bar >> sinh^2 r), strictly > HL
    ns_opt = [10.0 ** (1.0 + 3.0 * i / 60.0) for i in range(61)]
    for nv in ns_opt:
        assert 0.5 * (nv ** -0.5) > 1.0 / nv
    # 5. OAT spin squeezing strictly >= HL for all plotted N >= 1
    ns_oat = [1, 2, 3, 5, 8, 12, 20, 35, 60, 100, 180, 320, 600, 1000, 2000, 4000, 7000, 10000]
    for nv in ns_oat:
        assert opt_oat_dphi(nv)[1] >= 1.0 / nv - 1e-12

    # Ramsey Fisher info exact checks at V = 0.90
    vis = 0.90
    def ramsey_fc(phi: float, v: float = vis) -> float:
        s, c = math.sin(phi), math.cos(phi)
        return (v * v * s * s) / (1.0 - v * v * c * c)
    assert abs(ramsey_fc(0.5 * math.pi) - 0.81) < 1e-12
    assert abs(ramsey_fc(0.0)) < 1e-15

    doc = SvgDoc(
        title="量子精密测量标度极限与 Ramsey 干涉灵敏度工作点",
        desc=(
            "左面板在统一纵轴（固定总探测时长 T 下的归一化频率不确定度 T·Δω；无噪单轮等价于 Δφ，双对数 N = 1 至 10⁴）精确对比："
            "无噪标准量子极限 SQL（N⁻¹/²）、无噪海森堡极限 HL（N⁻¹）、Kitagawa-Ueda 单轴扭转 OAT（∝ N⁻⁵/⁶）、"
            "强相干光区（N ≥ 10，n̄ ≫ sinh²r）6 dB 光学压缩（0.5 N⁻¹/²）、独立马尔可夫退相位（γT = 2）下 Huelga 最优 GHZ 与含噪独立比特重合曲线"
            "（在 N=1 与单比特精确重合为 2√e，全程严格位于 HL 上方），以及保留完整分母的 Escher 有限 N 精度下界（N=1 等于 2√e，大 N 渐近比 GHZ 低 √e 倍）。"
            "右面板绘制单比特 Ramsey 条纹 P(+|φ) 与经典 Fisher 信息 F_C(φ; V=0.90)，标出最大斜率点 φ = π/2 与盲点 φ = 0。"
        ),
    )
    doc.add_header(
        "量子精密测量标度极限与 Ramsey 干涉灵敏工作点",
        f"左：固定总时长 T 下 T·Δω 标度对照（无噪单轮即 Δφ，γT=2 含噪均 ≥ HL）；右：Ramsey 条纹与 F{sub('C')}(φ)",
        raw_sub=True,
    )
    doc.add_panel(28, 96, 490, 456, "归一化不确定度 T·Δω 标度极限（双对数，N = 1–10⁴）")
    doc.add_panel(534, 96, 438, 456, "单比特 Ramsey 条纹与经典 Fisher 信息（V = 0.90）")

    # --- Left Panel: Log-Log Sensing Limits Plot ---
    px0, px1 = 96.0, 498.0
    py_bot, py_top = 428.0, 188.0  # log10(N) in [0, 4], log10(T*Delta_omega) in [-4.0, 0.70]
    y_lo, y_hi = -4.0, 0.70

    def sx_n(n_val: float) -> float:
        return px0 + (math.log10(n_val) / 4.0) * (px1 - px0)

    def sy_p(dp: float) -> float:
        return py_bot - ((math.log10(dp) - y_lo) / (y_hi - y_lo)) * (py_bot - py_top)

    # Legend cleanly above plot (2 rows inside y=144..178)
    doc.add('<line class="c2" stroke-width="2.4" stroke-dasharray="6 4" x1="42" y1="151" x2="66" y2="151"/>')
    doc.add('<text class="xs c2-txt" x="72" y="155">含噪 GHZ = 独立比特 (γT=2)</text>')
    doc.add('<line class="guide" x1="264" y1="151" x2="288" y2="151"/>')
    doc.add('<text class="xs" x="294" y="155">Escher 有限 N 精度下界 (γT=2)</text>')

    doc.add('<line class="c1" stroke-width="2.4" x1="42" y1="171" x2="64" y2="171"/>')
    doc.add('<text class="xs c1-txt" x="69" y="175">无噪 SQL</text>')
    doc.add('<line class="c5" stroke-width="2.1" stroke-dasharray="2.5 3.5" x1="138" y1="171" x2="160" y2="171"/>')
    doc.add('<text class="xs c5-txt" x="165" y="175">6 dB 压缩 (N≥10)</text>')
    doc.add('<line class="c4" stroke-width="2.4" stroke-dasharray="7 3 2 3" x1="286" y1="171" x2="308" y2="171"/>')
    doc.add(f'<text class="xs c4-txt" x="313" y="175">OAT ∝ N{sup("−5/6")}</text>')
    doc.add('<line class="c3" stroke-width="2.6" x1="406" y1="171" x2="428" y2="171"/>')
    doc.add(f'<text class="xs c3-txt" x="433" y="175">无噪 HL N{sup("−1")}</text>')

    # Gridlines & ticks
    y_sups = {0: "10⁰", -1: "10⁻¹", -2: "10⁻²", -3: "10⁻³", -4: "10⁻⁴"}
    for e_y in range(-4, 1):
        yy = sy_p(10.0 ** e_y)
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(yy)}" x2="{fmt(px1)}" y2="{fmt(yy)}"/>')
        doc.add(f'<text class="xs" x="{fmt(px0 - 7)}" y="{fmt(yy + 3.5)}" text-anchor="end">{y_sups[e_y]}</text>')
    x_sups = {0: "1", 1: "10", 2: "10²", 3: "10³", 4: "10⁴"}
    for e_x in range(0, 5):
        xx = sx_n(10.0 ** e_x)
        doc.add(f'<line class="grid" x1="{fmt(xx)}" y1="{fmt(py_top)}" x2="{fmt(xx)}" y2="{fmt(py_bot)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xx)}" y="{fmt(py_bot + 16)}" text-anchor="middle">{x_sups[e_x]}</text>')

    # Sample curves cleanly
    sql_pts = [(sx_n(nv), sy_p(nv ** -0.5)) for nv in ns_cont]
    hl_pts = [(sx_n(nv), sy_p(nv ** -1.0)) for nv in ns_cont]
    ghz_pts = [(sx_n(nv), sy_p(y_huelga_ghz(nv))) for nv in ns_cont]
    ult_pts = [(sx_n(nv), sy_p(y_escher_exact(nv))) for nv in ns_cont]
    opt_pts = [(sx_n(nv), sy_p(0.5 * (nv ** -0.5))) for nv in ns_opt]
    oat_pts = [(sx_n(float(nv)), sy_p(opt_oat_dphi(nv)[1])) for nv in ns_oat]

    # Draw curves (strictly ordered: noisy curves > noiseless SQL > 6 dB opt >= OAT >= HL)
    doc.add(f'<path class="guide" stroke-width="1.8" d="{path_from_points(ult_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.5" stroke-dasharray="6 4" d="{path_from_points(ghz_pts)}"/>')
    doc.add(f'<path class="c1" stroke-width="2.4" d="{path_from_points(sql_pts)}"/>')
    doc.add(f'<path class="c5" stroke-width="2.2" stroke-dasharray="2.5 3.5" d="{path_from_points(opt_pts)}"/>')
    doc.add(f'<path class="c4" stroke-width="2.4" stroke-dasharray="8 3 2 3" d="{path_from_points(oat_pts)}"/>')
    doc.add(f'<path class="c3" stroke-width="2.6" d="{path_from_points(hl_pts)}"/>')

    # Coincidence marker at N = 1 (noisy GHZ == noisy single qubit == Escher bound = 2*sqrt(e))
    doc.add(f'<circle class="c2-fill" cx="{fmt(sx_n(1.0))}" cy="{fmt(sy_p(y_huelga_ghz(1.0)))}" r="4.2"/>')
    doc.add(f'<circle class="c1-fill" cx="{fmt(sx_n(1.0))}" cy="{fmt(sy_p(1.0))}" r="4.0"/>')
    # Starting marker for macroscopic coherent 6 dB optical squeezing at N = 10
    doc.add(f'<circle class="c5-fill" cx="{fmt(sx_n(10.0))}" cy="{fmt(sy_p(0.5 * 10.0**-0.5))}" r="3.8"/>')

    # Benchmark markers at N = 10, 100, 1000
    for nm in (10, 100, 1000):
        doc.add(f'<polygon class="c2-fill" points="{tri_pts(sx_n(nm), sy_p(y_huelga_ghz(nm)), 4.6)}"/>')
        doc.add(f'<rect class="c4-fill" x="{fmt(sx_n(nm) - 3.5)}" y="{fmt(sy_p(opt_oat_dphi(nm)[1]) - 3.5)}" width="7.0" height="7.0"/>')
        doc.add(f'<polygon class="c3-fill" points="{diamond_pts(sx_n(nm), sy_p(1.0 / nm), 4.8)}"/>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px1 + 6)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(px1 + 6, py_bot, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(px0, py_top - 8, 0, -1, 6.5))
    doc.add(f'<text class="sm" x="{fmt(0.5*(px0+px1))}" y="{fmt(py_bot + 35)}" text-anchor="middle">探针粒子数 / 平均光子数 N（对数）</text>')
    doc.add(f'<text class="sm" x="45" y="{fmt(0.5*(py_bot+py_top))}" text-anchor="middle" transform="rotate(-90 45 {fmt(0.5*(py_bot+py_top))})">归一化不确定度 T·Δω（对数）</text>')

    # Non-overlapping physical annotations strictly inside curve-free open wedges
    doc.add(f'<text class="xsb c2-txt" x="{fmt(sx_n(360))}" y="{fmt(sy_p(1.75))}" text-anchor="middle">含噪 GHZ = 独立比特（斜率 −1/2）</text>')
    doc.add(f'<line class="c2" stroke-width="1.1" x1="{fmt(sx_n(220))}" y1="{fmt(sy_p(1.22))}" x2="{fmt(sx_n(110))}" y2="{fmt(sy_p(y_huelga_ghz(110)) - 5)}"/>')
    doc.add(f'<text class="xs" x="{fmt(sx_n(1750))}" y="{fmt(sy_p(0.45))}" text-anchor="middle">Escher 精确界（大 N 差 √e）</text>')
    doc.add(f'<line class="guide" x1="{fmt(sx_n(2100))}" y1="{fmt(sy_p(0.30))}" x2="{fmt(sx_n(2100))}" y2="{fmt(sy_p(y_escher_exact(2100)) - 3)}"/>')
    doc.add('<text class="xsb c5-txt" x="493" y="357" text-anchor="end" transform="rotate(14 493 357)">6 dB 压缩 (n̄≫sinh²r)</text>')
    doc.add('<text class="xsb c4-txt" x="444" y="391" text-anchor="middle" transform="rotate(23 444 391)">OAT 斜率 −5/6</text>')
    doc.add(f'<text class="xsb c3-txt" x="{fmt(sx_n(38))}" y="{fmt(sy_p(0.00055))}" text-anchor="start">无噪 HL 斜率 −1</text>')

    # Bottom takeaway pill in Left Panel
    doc.add('<rect class="pill" x="42" y="484" width="462" height="54" rx="9"/>')
    doc.add(f'<text class="xsb" x="273" y="505" text-anchor="middle">统一口径 T·Δω：N=1 含噪 GHZ、单比特与 Escher 严格重合（2√e）；全段 ≥ HL</text>')
    doc.add(f'<text class="xs" x="273" y="525" text-anchor="middle">Huelga (1997)：t{sub("opt")}=1/(2Nγ) 致 GHZ 沦回 SQL；大 N 终极界至多省 √e ≈ 1.65×</text>')

    # --- Right Panel Upper: Ramsey Fringe P(+|phi) ---
    rx0, rx1 = 592.0, 952.0
    ry1_bot, ry1_top = 304.0, 174.0

    def r_x(phi: float) -> float:
        return rx0 + (phi / (2.0 * math.pi)) * (rx1 - rx0)

    def r_y1(prob: float) -> float:
        return ry1_bot - prob * (ry1_bot - ry1_top)

    doc.add('<line class="c1" stroke-width="2.4" x1="552" y1="152" x2="576" y2="152"/>')
    doc.add('<text class="xs" x="582" y="156">V = 0.90 条纹</text>')
    doc.add('<line class="guide" x1="684" y1="152" x2="708" y2="152"/>')
    doc.add('<text class="xs" x="714" y="156">理想 V = 1.00</text>')
    doc.add('<circle class="c3-fill" cx="826" cy="152" r="4"/>')
    doc.add('<text class="xs c3-txt" x="835" y="156">最灵敏</text>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(894, 152, 4.6)}"/>')
    doc.add('<text class="xs c2-txt" x="903" y="156">盲点</text>')

    for pv in [0.0, 0.5, 1.0]:
        yy = r_y1(pv)
        doc.add(f'<line class="grid" x1="{fmt(rx0)}" y1="{fmt(yy)}" x2="{fmt(rx1)}" y2="{fmt(yy)}"/>')
        doc.add(f'<text class="xs" x="{fmt(rx0 - 6)}" y="{fmt(yy + 3.5)}" text-anchor="end">{pv:.1f}</text>')
    phi_ticks = [(0.0, "0"), (0.5 * math.pi, "π/2"), (math.pi, "π"), (1.5 * math.pi, "3π/2"), (2.0 * math.pi, "2π")]
    for pt_v, pt_s in phi_ticks:
        xp = r_x(pt_v)
        doc.add(f'<line class="grid" x1="{fmt(xp)}" y1="{fmt(ry1_top)}" x2="{fmt(xp)}" y2="{fmt(ry1_bot)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xp)}" y="{fmt(ry1_bot + 14)}" text-anchor="middle">{pt_s}</text>')

    phis = [2.0 * math.pi * i / 120.0 for i in range(121)]
    id_pts = [(r_x(ph), r_y1(0.5 * (1.0 + math.cos(ph)))) for ph in phis]
    v_pts = [(r_x(ph), r_y1(0.5 * (1.0 + vis * math.cos(ph)))) for ph in phis]
    doc.add(f'<path class="guide" d="{path_from_points(id_pts)}"/>')
    doc.add(f'<path class="c1" stroke-width="2.5" d="{path_from_points(v_pts)}"/>')

    # Tangent at phi=pi/2 (max slope -V/2) and flat tangent at phi=0 & phi=pi
    x_h, y_h = r_x(0.5 * math.pi), r_y1(0.5)
    doc.add(f'<line class="c3" stroke-width="2.0" x1="{fmt(r_x(0.5*math.pi - 0.55))}" y1="{fmt(r_y1(0.5 + 0.55*vis/2))}" x2="{fmt(r_x(0.5*math.pi + 0.55))}" y2="{fmt(r_y1(0.5 - 0.55*vis/2))}"/>')
    doc.add(f'<circle class="c3-fill" cx="{fmt(x_h)}" cy="{fmt(y_h)}" r="5.0"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(r_x(0.0), r_y1(0.5*(1+vis)), 5.4)}"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(r_x(math.pi), r_y1(0.5*(1-vis)), 5.4)}"/>')
    doc.add(f'<text class="xsb c3-txt" x="{fmt(r_x(0.95*math.pi))}" y="{fmt(r_y1(0.68))}">最陡工作点 φ = π/2</text>')
    doc.add(f'<text class="xsb c2-txt" x="{fmt(r_x(0.18*math.pi))}" y="{fmt(r_y1(0.96))}">盲点 φ=0 (斜率=0)</text>')

    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry1_bot)}" x2="{fmt(rx1 + 6)}" y2="{fmt(ry1_bot)}"/>')
    doc.add(arrow_head(rx1 + 6, ry1_bot, 1, 0, 6.0))
    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry1_bot)}" x2="{fmt(rx0)}" y2="{fmt(ry1_top - 6)}"/>')
    doc.add(arrow_head(rx0, ry1_top - 6, 0, -1, 6.0))
    doc.add(f'<text class="xs" x="550" y="{fmt(0.5*(ry1_bot+ry1_top))}" text-anchor="middle" transform="rotate(-90 550 {fmt(0.5*(ry1_bot+ry1_top))})">测量概率 P(+|φ)</text>')

    # --- Right Panel Lower: Classical Fisher Information F_C(phi; V) ---
    ry2_bot, ry2_top = 466.0, 352.0  # F_C in [0, 1.24]

    def r_y2(fv: float) -> float:
        return ry2_bot - (fv / 1.24) * (ry2_bot - ry2_top)

    for fv in [0.0, 0.5, 1.0]:
        yy = r_y2(fv)
        doc.add(f'<line class="grid" x1="{fmt(rx0)}" y1="{fmt(yy)}" x2="{fmt(rx1)}" y2="{fmt(yy)}"/>')
        doc.add(f'<text class="xs" x="{fmt(rx0 - 6)}" y="{fmt(yy + 3.5)}" text-anchor="end">{fv:.1f}</text>')
    for pt_v, pt_s in phi_ticks:
        xp = r_x(pt_v)
        doc.add(f'<line class="grid" x1="{fmt(xp)}" y1="{fmt(ry2_top)}" x2="{fmt(xp)}" y2="{fmt(ry2_bot)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xp)}" y="{fmt(ry2_bot + 14)}" text-anchor="middle">{pt_s}</text>')

    # Ideal F_C = 1 guide & V = 0.90 curve
    doc.add(f'<line class="guide" x1="{fmt(rx0)}" y1="{fmt(r_y2(1.0))}" x2="{fmt(rx1)}" y2="{fmt(r_y2(1.0))}"/>')
    fc_pts = [(r_x(ph), r_y2(ramsey_fc(ph))) for ph in phis]
    doc.add(f'<polygon class="area3" points="{pts_str([(rx0, ry2_bot)] + fc_pts + [(rx1, ry2_bot)])}"/>')
    doc.add(f'<path class="c3" stroke-width="2.5" d="{path_from_points(fc_pts)}"/>')

    # Peak and zero markers
    doc.add(f'<circle class="c3-fill" cx="{fmt(r_x(0.5*math.pi))}" cy="{fmt(r_y2(0.81))}" r="4.6"/>')
    doc.add(f'<circle class="c3-fill" cx="{fmt(r_x(1.5*math.pi))}" cy="{fmt(r_y2(0.81))}" r="4.6"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(r_x(math.pi), r_y2(0.0), 5.0)}"/>')
    doc.add(f'<text class="xsb c3-txt" x="{fmt(r_x(0.5*math.pi))}" y="{fmt(r_y2(1.09))}" text-anchor="middle">峰值 V² = 0.81</text>')
    doc.add(f'<text class="xsb c2-txt" x="{fmt(r_x(math.pi))}" y="{fmt(r_y2(1.09))}" text-anchor="middle">盲点 F{sub("C")} = 0</text>')
    doc.add(f'<line class="c2" stroke-width="1.2" stroke-dasharray="3 2" x1="{fmt(r_x(math.pi))}" y1="{fmt(r_y2(0.95))}" x2="{fmt(r_x(math.pi))}" y2="{fmt(r_y2(0.07))}"/>')

    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry2_bot)}" x2="{fmt(rx1 + 6)}" y2="{fmt(ry2_bot)}"/>')
    doc.add(arrow_head(rx1 + 6, ry2_bot, 1, 0, 6.0))
    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry2_bot)}" x2="{fmt(rx0)}" y2="{fmt(ry2_top - 6)}"/>')
    doc.add(arrow_head(rx0, ry2_top - 6, 0, -1, 6.0))
    doc.add(f'<text class="xs" x="550" y="{fmt(0.5*(ry2_bot+ry2_top))}" text-anchor="middle" transform="rotate(-90 550 {fmt(0.5*(ry2_bot+ry2_top))})">Fisher 信息 F{sub("C")}(φ)</text>')

    # Bottom formula pill in Right Panel
    doc.add('<rect class="pill" x="548" y="498" width="410" height="40" rx="9"/>')
    doc.add(f'<text class="xs" x="753" y="522" text-anchor="middle">F{sub("C")}(φ; V) = V² sin²φ / (1 − V² cos²φ)；V &lt; 1 时 0/0 奇迹破功</text>')

    return doc.render(), {"xi2_10": xi10, "xi2_100": xi100, "xi2_1000": xi1000, "fc_peak": ramsey_fc(0.5 * math.pi)}


# ---------------------------------------------------------------------------
# Figure 7: Ch 21 — Four Classical Sim Islands, Four-Wall Phase Diagram & Spectra
# ---------------------------------------------------------------------------
def build_fig7_classical_sim_boundaries() -> tuple[str, dict[str, float]]:
    # Exact Pauli weight decay checks (Ch21 §6.1)
    decay_ft = (1.0 - 0.001) ** 20
    decay_p05 = (1.0 - 0.05) ** 20
    decay_p15 = (1.0 - 0.15) ** 20
    decay_p30 = (1.0 - 0.30) ** 20
    assert decay_ft > 0.98 and decay_p30 < 1e-3

    # Exact normalized MPS singular value squared spectra (k = 1..16, sum = 1)
    raw_area = [math.exp(-0.82 * k) for k in range(16)]
    z_area = sum(raw_area)
    spec_area = [v / z_area for v in raw_area]
    spec_vol = [1.0 / 16.0] * 16
    eps_area_chi8 = sum(spec_area[8:])
    eps_vol_chi8 = sum(spec_vol[8:])
    assert abs(sum(spec_area) - 1.0) < 1e-12
    assert abs(sum(spec_vol) - 1.0) < 1e-12
    assert eps_area_chi8 < 2e-3 and abs(eps_vol_chi8 - 0.5) < 1e-12

    doc = SvgDoc(
        title="经典模拟的适用条件与截断谱",
        desc=(
            "左面板绘制非 Clifford T 门数与纠缠键维 χ 相图，划分几类经典方法（Clifford/稳定子表、低纠缠张量网络 MPS/BP-TN、"
            "含噪 Pauli 传播 SPD，以及位于高纠缠高连续旋转角区的独立代数可解口袋——匹配门/高斯孤岛），并列比较量子与经典方法时需要固定的任务条件。区域和边界为示意。"
            "右面板上部精确绘制退极化噪声伴随映射按 Pauli 权重指数衰减 (1−p)^w（p = 0.001, 0.05, 0.15, 0.30），"
            "下部精确对比两种归一化的 MPS 奇异值谱（指数衰减、平坦） σ_k² 及 χ′=8 截断误差。"
        ),
    )
    doc.add_header(
        "经典模拟的适用条件与截断谱",
        f"左：T 门数 × 纠缠键维 χ 与经典方法示意；右：含噪 Pauli 衰减 (1−p){sup('w')} 与 MPS 奇异值谱",
        raw_sub=True,
    )
    doc.add_panel(28, 96, 486, 456, "经典方法的适用条件（示意）")
    doc.add_panel(530, 96, 442, 456, f"含噪 Pauli 衰减 (1−p){sup('w')} 与 MPS 奇异值截断谱", raw_head=True)

    # --- Left Panel: Clean Non-Overlapping 4-Island + FTQC Advantage Phase Diagram ---
    px0, px1 = 94.0, 500.0
    py_bot, py_top = 424.0, 152.0

    # Region 1 (Left vertical): Clifford / Extended Stabilizer (x: 94..234, y: 152..346)
    doc.add('<rect class="c1-soft" x="94" y="152" width="140" height="194" rx="6"/>')
    doc.add('<rect fill="url(#hatch-blue)" x="94" y="152" width="140" height="194" rx="6"/>')
    doc.add('<text class="xsb c1-txt" x="164" y="192" text-anchor="middle">Clifford / 稳定子表</text>')
    doc.add('<text class="xs c1-txt" x="164" y="216" text-anchor="middle">Stim: 门 O(n) / 空间 O(n²)</text>')
    doc.add(f'<text class="xs c1-txt" x="164" y="242" text-anchor="middle">少 T 分解另计精度</text>')
    doc.add('<text class="xs" x="164" y="274" text-anchor="middle">任意高纠缠</text>')
    doc.add('<text class="xs" x="164" y="294" text-anchor="middle">仍可用稳定子表</text>')

    # Region 2 (Upper-middle): Noisy Pauli Propagation / SPD (x: 238..336, y: 152..346)
    doc.add('<rect class="c4-soft" x="238" y="152" width="98" height="194" rx="6"/>')
    doc.add('<rect fill="url(#hatch-amber)" x="238" y="152" width="98" height="194" rx="6"/>')
    doc.add('<text class="xsb c4-txt" x="287" y="192" text-anchor="middle">含噪 Pauli 传播</text>')
    doc.add('<text class="xs c4-txt" x="287" y="216" text-anchor="middle">SPD / 按权重截断</text>')
    doc.add(f'<text class="xs c4-txt" x="287" y="244" text-anchor="middle">按 (1−p){sup("w")} 剪枝</text>')
    doc.add('<text class="xs" x="287" y="274" text-anchor="middle">给定局部退极化</text>')
    doc.add('<text class="xs" x="287" y="294" text-anchor="middle">短层内高权项衰减</text>')

    # Region 3 (Top-right fortress): FTQC 4D Quantum Advantage (x: 340..500, y: 152..250)
    doc.add('<rect class="c2-soft" stroke-width="2.4" x="340" y="152" width="160" height="98" rx="6"/>')
    doc.add('<rect fill="url(#hatch-red)" x="340" y="152" width="160" height="98" rx="6"/>')
    doc.add('<text class="xsb c2-txt" x="420" y="170" text-anchor="middle">量子与经典方法对照</text>')
    doc.add('<text class="xs" x="420" y="188" text-anchor="middle">固定电路族与输入</text>')
    doc.add('<text class="xs" x="420" y="206" text-anchor="middle">对齐输出及允许误差</text>')
    doc.add(f'<text class="xsb c2-txt" x="420" y="224" text-anchor="middle">记录运行时间与内存</text>')
    doc.add('<text class="xs c2-txt" x="420" y="241" text-anchor="middle">加入测量与经典开销</text>')

    # Region 5 (Right high-t, high-chi independent algebraic pocket): Matchgates / Gaussian
    doc.add('<rect class="c5-soft" stroke-width="1.8" stroke-dasharray="5 3" x="340" y="256" width="160" height="90" rx="7"/>')
    doc.add('<text class="xsb c5-txt" x="420" y="274" text-anchor="middle">匹配门 / 高斯口袋</text>')
    doc.add('<text class="xs" x="420" y="292" text-anchor="middle">允许可保结构的旋转</text>')
    doc.add('<text class="xs c5-txt" x="420" y="310" text-anchor="middle">自由费米子/高斯结构封闭</text>')
    doc.add('<text class="xs c5-txt" x="420" y="328" text-anchor="middle">复杂度依赖输入与输出</text>')

    # Region 4 (Bottom horizontal): MPS / 1D Brickwork / BP-TN (x: 94..500, y: 352..424)
    doc.add('<rect class="c3-soft" x="94" y="352" width="406" height="72" rx="6"/>')
    doc.add('<rect fill="url(#hatch-green)" x="94" y="352" width="406" height="72" rx="6"/>')
    doc.add('<text class="xsb c3-txt" x="297" y="373" text-anchor="middle">张量网络 MPS / 1D 砖墙 / BP-TN（低秩或谱尾快衰减）</text>')
    doc.add('<text class="xs c3-txt" x="297" y="393" text-anchor="middle">单比特 T 门不改变已有切分的键维 χ</text>')
    doc.add('<text class="xs" x="297" y="413" text-anchor="middle">（2026：在已公开地址计算振幅与 log-XEB）</text>')

    # Frame axes & qualitative tick marks
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px1 + 7)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(px1 + 7, py_bot, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(px0, py_top - 8, 0, -1, 6.5))

    doc.add('<text class="xs" x="106" y="441" text-anchor="middle">t = 0</text>')
    doc.add('<text class="xs" x="230" y="441" text-anchor="middle">较少 T</text>')
    doc.add('<text class="xs" x="454" y="441" text-anchor="middle">较多 T</text>')
    doc.add('<text class="sm" x="297" y="462" text-anchor="middle">非 Clifford T 门数 t</text>')

    doc.add('<text class="xs" x="86" y="416" text-anchor="end">小</text>')
    doc.add('<text class="xs" x="86" y="355" text-anchor="end">中</text>')
    doc.add(f'<text class="xs" x="86" y="168" text-anchor="end">大</text>')
    doc.add('<text class="sm" x="44" y="288" text-anchor="middle" transform="rotate(-90 44 288)">切分键维 χ</text>')

    # Bottom four-wall summary pill
    doc.add('<rect class="pill" x="44" y="480" width="454" height="58" rx="9"/>')
    doc.add('<text class="xsb" x="271" y="501" text-anchor="middle">比较条件：规模、代数结构、收缩宽度与噪声模型</text>')
    doc.add('<text class="xs" x="271" y="522" text-anchor="middle">分别记录指定振幅、全串采样与局域期望的误差和成本</text>')

    # --- Right Panel Upper: Exact Noisy Pauli Propagation Decay (1-p)^w ---
    doc.add(f'<text class="xsb" x="546" y="152">① 单层退极化伴随衰减 (1−p){sup("w")}（对数纵轴，w = 0–20）</text>')
    ux0, ux1 = 594.0, 952.0
    uy_bot, uy_top = 294.0, 168.0  # log10 in [-3, +0.35]

    def ux(wv: float) -> float:
        return ux0 + (wv / 20.0) * (ux1 - ux0)

    def uy(val: float) -> float:
        lv = max(-3.0, math.log10(max(val, 1e-6)))
        return uy_bot - ((lv - (-3.0)) / 3.35) * (uy_bot - uy_top)

    for exp, lbl in [(0, "10⁰"), (-1, "10⁻¹"), (-2, "10⁻²"), (-3, "10⁻³")]:
        yy = uy(10.0 ** exp)
        doc.add(f'<line class="grid" x1="{fmt(ux0)}" y1="{fmt(yy)}" x2="{fmt(ux1)}" y2="{fmt(yy)}"/>')
        doc.add(f'<text class="xs" x="{fmt(ux0 - 6)}" y="{fmt(yy + 3.5)}" text-anchor="end">{lbl}</text>')
    for wt in [0, 5, 10, 15, 20]:
        xw = ux(float(wt))
        doc.add(f'<line class="grid" x1="{fmt(xw)}" y1="{fmt(uy_top)}" x2="{fmt(xw)}" y2="{fmt(uy_bot)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xw)}" y="{fmt(uy_bot + 14)}" text-anchor="middle">{wt}</text>')

    # Pruning cutoff zone below 10^-2
    y_cut = uy(1e-2)
    doc.add(f'<rect class="forbid" x="{fmt(ux0)}" y="{fmt(y_cut)}" width="{fmt(ux1 - ux0)}" height="{fmt(uy_bot - y_cut)}"/>')
    doc.add(f'<line class="c2" stroke-width="1.3" stroke-dasharray="4 4" x1="{fmt(ux0)}" y1="{fmt(y_cut)}" x2="{fmt(ux1)}" y2="{fmt(y_cut)}"/>')

    # 4 exact curves
    p_specs = [
        (0.001, "c3", "", "p = 0.001 (低噪存活)", 14.5, 1.28),
        (0.05, "c1", "6 4", "p = 0.05", 17.5, 0.21),
        (0.15, "c4", "7 3 2 3", "p = 0.15", 16.0, 0.023),
        (0.30, "c2", "2.5 3", "p = 0.30 (强衰减)", 15.2, 0.0067),
    ]
    for p_v, cls_p, dash_p, lbl_p, lx_w, ly_v in p_specs:
        pts_p = [(ux(float(w)), uy((1.0 - p_v) ** w)) for w in range(21) if (1.0 - p_v) ** w >= 1e-3]
        if len(pts_p) < 21:
            # Exact crossing point with 10^-3
            w_end = -3.0 / math.log10(1.0 - p_v)
            pts_p.append((ux(w_end), uy(1e-3)))
        da = f' stroke-dasharray="{dash_p}"' if dash_p else ""
        doc.add(f'<path class="{cls_p}" stroke-width="2.3"{da} d="{path_from_points(pts_p)}"/>')
        doc.add(f'<text class="xsb {cls_p}-txt" x="{fmt(ux(lx_w))}" y="{fmt(uy(ly_v))}" text-anchor="middle">{lbl_p}</text>')

    doc.add(f'<text class="xs c2-txt" x="{fmt(ux(3.8))}" y="{fmt(uy(0.0032))}" text-anchor="middle">剪枝丢弃区 (&lt;10⁻²)</text>')
    doc.add(f'<line class="axis" x1="{fmt(ux0)}" y1="{fmt(uy_bot)}" x2="{fmt(ux1 + 6)}" y2="{fmt(uy_bot)}"/>')
    doc.add(arrow_head(ux1 + 6, uy_bot, 1, 0, 5.5))
    doc.add(f'<line class="axis" x1="{fmt(ux0)}" y1="{fmt(uy_bot)}" x2="{fmt(ux0)}" y2="{fmt(uy_top - 6)}"/>')
    doc.add(arrow_head(ux0, uy_top - 6, 0, -1, 5.5))
    doc.add(f'<text class="xs" x="{fmt(0.5*(ux0+ux1))}" y="{fmt(uy_bot + 27)}" text-anchor="middle">Pauli 权重 w（非 I 比特个数）</text>')
    doc.add('<text class="xs" x="548" y="230" text-anchor="middle" transform="rotate(-90 548 230)">保留因子</text>')

    # --- Right Panel Lower: Exact MPS Singular Value Spectrum sigma_k^2 ---
    doc.add(f'<text class="xsb" x="546" y="344">② MPS 奇异值谱 σ{sub("k")}²（面积律速降 vs 体积律平坦拖尾）</text>')
    mx0, mx1 = 594.0, 952.0
    my_bot, my_top = 468.0, 356.0  # log10 in [-5, 0], k in [1, 16]

    def mx(k: float) -> float:
        return mx0 + ((k - 1.0) / 15.0) * (mx1 - mx0)

    def my(val: float) -> float:
        lv = max(-5.0, math.log10(max(val, 1e-8)))
        return my_bot - ((lv - (-5.0)) / 5.0) * (my_bot - my_top)

    for exp, lbl in [(0, "10⁰"), (-2, "10⁻²"), (-4, "10⁻⁴")]:
        yy = my(10.0 ** exp)
        doc.add(f'<line class="grid" x1="{fmt(mx0)}" y1="{fmt(yy)}" x2="{fmt(mx1)}" y2="{fmt(yy)}"/>')
        doc.add(f'<text class="xs" x="{fmt(mx0 - 6)}" y="{fmt(yy + 3.5)}" text-anchor="end">{lbl}</text>')
    for kt in [1, 4, 8, 12, 16]:
        xk = mx(float(kt))
        doc.add(f'<line class="grid" x1="{fmt(xk)}" y1="{fmt(my_top)}" x2="{fmt(xk)}" y2="{fmt(my_bot)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xk)}" y="{fmt(my_bot + 14)}" text-anchor="middle">{kt}</text>')

    # Truncation wall at chi' = 8 and shaded discarded tail k > 8
    x_chi = mx(8.0)
    doc.add(f'<rect class="forbid" x="{fmt(x_chi)}" y="{fmt(my_top)}" width="{fmt(mx1 - x_chi)}" height="{fmt(my_bot - my_top)}"/>')
    doc.add(f'<line class="c2" stroke-width="1.6" stroke-dasharray="5 4" x1="{fmt(x_chi)}" y1="{fmt(my_top)}" x2="{fmt(x_chi)}" y2="{fmt(my_bot)}"/>')

    area_pts = [(mx(k + 1), my(spec_area[k])) for k in range(16)]
    vol_pts = [(mx(k + 1), my(spec_vol[k])) for k in range(16)]
    doc.add(f'<path class="c3" stroke-width="2.4" d="{path_from_points(area_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.3" stroke-dasharray="6 4" d="{path_from_points(vol_pts)}"/>')
    for k in range(0, 16, 2):
        doc.add(f'<circle class="c3-fill" cx="{fmt(area_pts[k][0])}" cy="{fmt(area_pts[k][1])}" r="3.4"/>')
        doc.add(f'<polygon class="c2-fill" points="{diamond_pts(vol_pts[k][0], vol_pts[k][1], 4.0)}"/>')

    # Exact W_3 benchmark points (k=1: 2/3, k=2: 1/3)
    doc.add(f'<circle class="c1-fill" cx="{fmt(mx(1.0))}" cy="{fmt(my(2.0/3.0))}" r="4.5"/>')
    doc.add(f'<circle class="c1-fill" cx="{fmt(mx(2.0))}" cy="{fmt(my(1.0/3.0))}" r="4.5"/>')

    doc.add(f'<text class="xsb c1-txt" x="{fmt(mx(3.0))}" y="{fmt(my(0.45))}">|W₃⟩ 仅 2 项 (χ=2)</text>')
    doc.add(f'<text class="xsb c2-txt" x="{fmt(mx(12.2))}" y="{fmt(my(0.18))}" text-anchor="middle">体积律：截断丢 50%!</text>')
    doc.add(f'<text class="xsb c3-txt" x="{fmt(mx(12.2))}" y="{fmt(my(0.0022))}" text-anchor="middle">面积律：误差 &lt; 0.2%</text>')
    doc.add(f'<text class="xsb c2-txt" x="{fmt(x_chi - 6)}" y="{fmt(my(0.00018))}" text-anchor="end">截断 χ′=8 →</text>')

    doc.add(f'<line class="axis" x1="{fmt(mx0)}" y1="{fmt(my_bot)}" x2="{fmt(mx1 + 6)}" y2="{fmt(my_bot)}"/>')
    doc.add(arrow_head(mx1 + 6, my_bot, 1, 0, 5.5))
    doc.add(f'<line class="axis" x1="{fmt(mx0)}" y1="{fmt(my_bot)}" x2="{fmt(mx0)}" y2="{fmt(my_top - 6)}"/>')
    doc.add(arrow_head(mx0, my_top - 6, 0, -1, 5.5))
    doc.add(f'<text class="xs" x="548" y="412" text-anchor="middle" transform="rotate(-90 548 412)">权重 σ{sub("k")}²</text>')

    # Bottom formula pill in Right Panel
    doc.add('<rect class="pill" x="546" y="498" width="412" height="40" rx="9"/>')
    doc.add(f'<text class="xs" x="752" y="522" text-anchor="middle">SPD 误差界 ≤ Σ|c{sub("pruned")}|；MPS 截断平方保真度 F² = 1 − Σ{sub("k>χ′")} σ{sub("k")}²</text>')

    return doc.render(), {"decay_ft": decay_ft, "decay_p30": decay_p30, "eps_area_chi8": eps_area_chi8, "eps_vol_chi8": eps_vol_chi8}


# ---------------------------------------------------------------------------
# XML well-formedness & margin validation
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
        ("v3-17-anyons-landau-zener.svg", build_fig1_anyons_landau_zener),
        ("v3-18-gkp-grid-sampling.svg", build_fig2_gkp_grid_sampling),
        ("v3-19-cryo-thermal-budget.svg", build_fig3_cryo_thermal_budget),
        ("v3-19-queue-tail-latency.svg", build_fig4_queue_tail_latency),
        ("v3-q4-double-well-splitting.svg", build_fig5_double_well_splitting),
        ("v3-20-sensing-limits.svg", build_fig6_sensing_limits),
        ("v3-21-classical-sim-boundaries.svg", build_fig7_classical_sim_boundaries),
    ]

    for fname, fn in builders:
        svg_text, metrics = fn()
        check = verify_svg_xml(svg_text, fname)
        out_path = ASSETS_DIR / fname
        out_path.write_text(svg_text, encoding="utf-8")
        print(f"[OK] {fname}: {check['bytes']} bytes, {check['text_count']} text labels | metrics={metrics}")


if __name__ == "__main__":
    main()
