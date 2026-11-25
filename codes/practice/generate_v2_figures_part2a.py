#!/usr/bin/env python3
"""Generate 5 light/dark-adaptive scientific SVG figures (part 2a) using Python stdlib only.

Outputs to handbook/assets/:
  1. v2-q3-anharmonic-rabi.svg
  2. v2-10-surface-lattice-surgery.svg
  3. v2-12-bb84-plob.svg
  4. v2-13-helstrom-entropy.svg
  5. v2-14-drag-dd-pulses.svg

Run:
  python3 codes/practice/generate_v2_figures_part2a.py
"""

from __future__ import annotations

import math
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT / "handbook" / "assets"
W, H = 1000, 580
MARGIN = 30


COMMON_CSS = """
:root{color-scheme:light dark}
text{font-family:system-ui,-apple-system,'PingFang SC','Microsoft YaHei',sans-serif}
.bg{fill:#f8fafc}
.panel{fill:#ffffff;stroke:#cbd5e1;stroke-width:1.4}
.phead{fill:#eef4f8}
.title{font-size:20px;font-weight:700;fill:#13263a}
.subtitle{font-size:14px;font-weight:400;fill:#3e566d}
.sec{font-size:15px;font-weight:700;fill:#13263a}
.lbl{font-size:13.5px;font-weight:500;fill:#19324d}
.lblb{font-size:13.5px;font-weight:700;fill:#13263a}
.sm{font-size:13px;font-weight:400;fill:#3e566d}
.smb{font-size:13px;font-weight:600;fill:#19324d}
.axis{stroke:#19324d;stroke-width:1.7;fill:none}
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
.note{fill:#fff8e6;stroke:#c98d24;stroke-width:1.4}
.pill{fill:#edf2f7;stroke:#9fb3c8;stroke-width:1.2}
.forbid{fill:#c74b34;fill-opacity:.09}
.area1{fill:#1b6ca8;fill-opacity:.11}
.data-node{fill:#ffffff;stroke:#19324d;stroke-width:2}
.badge-txt{fill:#ffffff;font-size:13px;font-weight:700}
.hatch-stroke1{stroke:#1b6ca8;stroke-width:1.2;stroke-opacity:.42}
.hatch-stroke2{stroke:#c74b34;stroke-width:1.2;stroke-opacity:.42}
.hatch-stroke3{stroke:#1e7a5c;stroke-width:1.2;stroke-opacity:.42}
@media(prefers-color-scheme:dark){
  .bg{fill:#0f1720}
  .panel{fill:#16222e;stroke:#354c61}
  .phead{fill:#1c2d3d}
  .title,.sec,.lblb{fill:#eef6ff}
  .subtitle,.sm{fill:#b7cde0}
  .lbl,.smb{fill:#d7e7f5}
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
  .note{fill:#332914;stroke:#d6a240}
  .pill{fill:#203142;stroke:#4f6b85}
  .forbid{fill:#f28872;fill-opacity:.12}
  .area1{fill:#6bc2f5;fill-opacity:.15}
  .data-node{fill:#16222e;stroke:#d7e7f5}
  .badge-txt{fill:#0f1720}
  .hatch-stroke1{stroke:#6bc2f5;stroke-opacity:.48}
  .hatch-stroke2{stroke:#f28872;stroke-opacity:.48}
  .hatch-stroke3{stroke:#5dd1a8;stroke-opacity:.48}
}
""".strip()


def fmt(v: float) -> str:
    s = f"{v:.2f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def sub(txt: str) -> str:
    return f'<tspan dy="3" font-size="75%">{escape(txt)}</tspan><tspan dy="-3">&#8203;</tspan>'


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


def arrow_head(x: float, y: float, dx: float, dy: float, size: float = 8.0, cls: str = "axis-fill") -> str:
    norm = math.hypot(dx, dy)
    ux, uy = dx / norm, dy / norm
    px, py = -uy, ux
    bx, by = x - ux * size, y - uy * size
    hw = size * 0.48
    p1 = (x, y)
    p2 = (bx + px * hw, by + py * hw)
    p3 = (bx - px * hw, by - py * hw)
    return f'<polygon class="{cls}" points="{pts_str([p1, p2, p3])}"/>'


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
        ]
        self.body: list[str] = []

    def add(self, snippet: str) -> None:
        self.body.append(snippet)

    def add_header(self, title_text: str, subtitle_text: str, *, raw_sub: bool = False) -> None:
        self.add(f'<rect class="bg" width="{self.w}" height="{self.h}" rx="20"/>')
        self.add(f'<text class="title" x="34" y="54">{escape(title_text)}</text>')
        s_out = subtitle_text if raw_sub else escape(subtitle_text)
        self.add(f'<text class="subtitle" x="34" y="79">{s_out}</text>')

    def add_panel(self, x: float, y: float, w: float, h: float, heading: str) -> None:
        self.add(f'<rect class="panel" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="14"/>')
        self.add(
            f'<path class="phead" d="M {fmt(x + 14)} {fmt(y + 1)} H {fmt(x + w - 14)} '
            f'Q {fmt(x + w - 1)} {fmt(y + 1)} {fmt(x + w - 1)} {fmt(y + 14)} V {fmt(y + 39)} '
            f'H {fmt(x + 1)} V {fmt(y + 14)} Q {fmt(x + 1)} {fmt(y + 1)} {fmt(x + 14)} {fmt(y + 1)} Z"/>'
        )
        self.add(f'<line class="grid" x1="{fmt(x + 1)}" y1="{fmt(y + 39)}" x2="{fmt(x + w - 1)}" y2="{fmt(y + 39)}"/>')
        self.add(f'<text class="sec" x="{fmt(x + 16)}" y="{fmt(y + 25)}">{escape(heading)}</text>')

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
# Figure 1: Q3 — Anharmonic potential vs Harmonic oscillator + Exact Rabi P1(t)
# ---------------------------------------------------------------------------
def build_fig1_anharmonic_rabi() -> tuple[str, dict[str, float]]:
    # Exact physics parameters for Rabi plot
    omega_mhz = 10.0  # Omega / (2 pi) = 10 MHz
    delta_mhz = 6.0   # Delta / (2 pi) = 6 MHz
    omega_eff_mhz = math.hypot(omega_mhz, delta_mhz)  # sqrt(136) MHz
    t_pi_res = 500.0 / omega_mhz                      # 50.0 ns
    t_peak_det = 500.0 / omega_eff_mhz                # ~42.8746 ns
    p_peak_det = (omega_mhz / omega_eff_mhz) ** 2     # 100 / 136 ~= 0.735294

    def p1_rabi(t_ns: float, det_mhz: float) -> float:
        w_eff = math.hypot(omega_mhz, det_mhz)
        # Omega_eff * t / 2 = pi * (w_eff [MHz] * 1e-3 [GHz]) * t [ns]
        return (omega_mhz / w_eff) ** 2 * (math.sin(math.pi * w_eff * 1e-3 * t_ns) ** 2)

    # Assertions on exact Rabi formula
    assert abs(p1_rabi(0.0, 0.0)) < 1e-15
    assert abs(p1_rabi(t_pi_res, 0.0) - 1.0) < 1e-12
    assert abs(p1_rabi(2.0 * t_pi_res, 0.0)) < 1e-12
    assert abs(t_pi_res - 50.0) < 1e-12
    assert abs(p_peak_det - 100.0 / 136.0) < 1e-12
    assert abs(p1_rabi(t_peak_det, delta_mhz) - p_peak_det) < 1e-12
    assert abs(t_peak_det - 42.874646285) < 1e-6

    doc = SvgDoc(
        title="谐振子与 transmon 非谐势能级对比及精确 Rabi 振荡曲线",
        desc=(
            "左面板对比理想谐振子抛物势（等间距能级 ℏω）与约瑟夫森结 transmon 余弦势（负非谐性 α < 0 使 ω₁₂ < ω₀₁，"
            "能量非等比例示意）。右面板按精确二能级公式绘制 Ω/2π = 10 MHz 下共振驱动（Δ = 0，首峰 50.0 ns、峰高 1.00）"
            "与失谐驱动（Δ/2π = 6 MHz，首峰 42.9 ns、峰高 100/136 ≈ 0.735）的激发态占据概率 P₁(t)。"
        ),
    )
    doc.add_header(
        "非谐势能级寻址与共振 / 失谐 Rabi 振荡",
        "左：抛物势（等间距）与 transmon 余弦势（负非谐性 α < 0）对比；右：精确二能级 Rabi 振荡 P₁(t)",
    )

    # Panels (stay within [28, 972] so inner text stays strictly >= 30px from edge)
    doc.add_panel(28, 96, 460, 456, "势阱与能级间距（非等比例示意）")
    doc.add_panel(508, 96, 464, 456, "二能级 Rabi 振荡：共振与失谐（精确公式）")

    # --- Left Panel: Two potential wells computed from exact math ---
    # Normalized well coordinates: E in [0, 3.0], phi in [-1.85, 1.85]
    ej = 2.6
    y_e0_base = 440.0
    y_etop = 188.0

    def map_e(e_val: float) -> float:
        return y_e0_base - (e_val / 3.0) * (y_e0_base - y_etop)

    # Sub-well 1: Harmonic oscillator V_HO(phi) = 0.5 * E_J * phi^2
    cx1 = 148.0
    sx = 44.0  # px per rad

    def map_x1(phi: float) -> float:
        return cx1 + phi * sx

    # Axes for well 1
    doc.add(f'<line class="axis" x1="66" y1="{fmt(y_e0_base + 4)}" x2="66" y2="184"/>')
    doc.add(arrow_head(66, 184, 0, -1, 7.5))
    doc.add(f'<line class="axis" x1="66" y1="{fmt(y_e0_base + 4)}" x2="236" y2="{fmt(y_e0_base + 4)}"/>')
    doc.add(arrow_head(236, y_e0_base + 4, 1, 0, 7.5))
    doc.add('<text class="sm" x="50" y="198" text-anchor="middle">能量</text>')
    doc.add('<text class="sm" x="50" y="214" text-anchor="middle">E</text>')
    doc.add('<text class="sm" x="150" y="464" text-anchor="middle">坐标 φ (rad)</text>')
    doc.add(f'<text class="smb c1-txt" x="156" y="160" text-anchor="middle">理想谐振子：½E{sub("J")}φ²</text>')

    phi_max_ho = math.sqrt(2.0 * 2.95 / ej)
    ho_pts = []
    for i in range(81):
        phi = -phi_max_ho + 2.0 * phi_max_ho * i / 80
        v = 0.5 * ej * phi * phi
        ho_pts.append((map_x1(phi), map_e(v)))
    doc.add(f'<path class="c1" stroke-width="2.4" d="{path_from_points(ho_pts)}"/>')

    ho_levels = [0.35, 1.35, 2.35]
    assert abs((ho_levels[1] - ho_levels[0]) - (ho_levels[2] - ho_levels[1])) < 1e-12
    for idx, en in enumerate(ho_levels):
        phi_t = math.sqrt(2.0 * en / ej)
        ye = map_e(en)
        doc.add(
            f'<line class="c1" stroke-width="2.2" x1="{fmt(map_x1(-phi_t))}" y1="{fmt(ye)}" '
            f'x2="{fmt(map_x1(phi_t))}" y2="{fmt(ye)}"/>'
        )
        doc.add(f'<text class="smb" x="{fmt(map_x1(-phi_t) - 6)}" y="{fmt(ye + 4)}" text-anchor="end">|{idx}⟩</text>')

    # Vertical double-arrows for equal spacing on well 1
    ax1 = cx1 + 4
    for e_lo, e_hi in [(ho_levels[0], ho_levels[1]), (ho_levels[1], ho_levels[2])]:
        ylo, yhi = map_e(e_lo) - 4, map_e(e_hi) + 4
        doc.add(f'<line class="c1" stroke-width="1.6" x1="{fmt(ax1)}" y1="{fmt(ylo)}" x2="{fmt(ax1)}" y2="{fmt(yhi)}"/>')
        doc.add(arrow_head(ax1, yhi, 0, -1, 6.0, "c1-fill"))
        doc.add(arrow_head(ax1, ylo, 0, 1, 6.0, "c1-fill"))
        doc.add(f'<text class="sm c1-txt" x="{fmt(ax1 + 8)}" y="{fmt(0.5 * (ylo + yhi) + 4)}">ℏω</text>')

    # Sub-well 2: Transmon cosine potential V_J(phi) = E_J * (1 - cos(phi))
    cx2 = 368.0

    def map_x2(phi: float) -> float:
        return cx2 + phi * sx

    doc.add(f'<line class="axis" x1="274" y1="{fmt(y_e0_base + 4)}" x2="274" y2="178"/>')
    doc.add(arrow_head(274, 178, 0, -1, 7.5))
    doc.add(f'<line class="axis" x1="274" y1="{fmt(y_e0_base + 4)}" x2="464" y2="{fmt(y_e0_base + 4)}"/>')
    doc.add(arrow_head(464, y_e0_base + 4, 1, 0, 7.5))
    doc.add('<text class="sm" x="340" y="464">相位差 φ (rad)</text>')
    doc.add(f'<text class="smb c2-txt" x="368" y="162" text-anchor="middle">transmon：E{sub("J")}(1−cos φ)</text>')

    # Faint dashed parabola reference inside well 2 to visualize potential softening
    ref_pts = []
    for i in range(81):
        phi = -phi_max_ho + 2.0 * phi_max_ho * i / 80
        v = 0.5 * ej * phi * phi
        ref_pts.append((map_x2(phi), map_e(v)))
    doc.add(f'<path class="guide" d="{path_from_points(ref_pts)}"/>')

    # Solid cosine curve for phi in [-1.85, 1.85]
    cos_pts = []
    for i in range(91):
        phi = -1.85 + 3.70 * i / 90
        v = ej * (1.0 - math.cos(phi))
        if v <= 2.98:
            cos_pts.append((map_x2(phi), map_e(v)))
    doc.add(f'<path class="c2" stroke-width="2.5" d="{path_from_points(cos_pts)}"/>')

    # Anharmonic levels: E0=0.35, E1=1.35, E2=2.09 (alpha < 0, w12 = 0.74 < w01 = 1.00)
    tr_levels = [0.35, 1.35, 2.09]
    assert (tr_levels[2] - tr_levels[1]) < (tr_levels[1] - tr_levels[0])
    for idx, en in enumerate(tr_levels):
        phi_t = math.acos(1.0 - en / ej)
        ye = map_e(en)
        cls_l = "c1" if idx < 2 else "c2"
        dash = ' stroke-dasharray="6 4"' if idx == 2 else ""
        doc.add(
            f'<line class="{cls_l}" stroke-width="2.2"{dash} x1="{fmt(map_x2(-phi_t))}" y1="{fmt(ye)}" '
            f'x2="{fmt(map_x2(phi_t))}" y2="{fmt(ye)}"/>'
        )
        doc.add(f'<text class="smb" x="{fmt(map_x2(-phi_t) - 6)}" y="{fmt(ye + 4)}" text-anchor="end">|{idx}⟩</text>')

    # Faint reference line showing where harmonic |2> would have been + clean right bracket for |alpha|
    ye2_ho = map_e(2.35)
    ye2_tr = map_e(2.09)
    doc.add(f'<line class="guide" x1="{fmt(cx2 - 54)}" y1="{fmt(ye2_ho)}" x2="{fmt(cx2 + 74)}" y2="{fmt(ye2_ho)}"/>')
    doc.add(f'<line class="guide" x1="{fmt(cx2 + 60)}" y1="{fmt(ye2_tr)}" x2="{fmt(cx2 + 74)}" y2="{fmt(ye2_tr)}"/>')
    doc.add(f'<line class="c2" stroke-width="1.5" x1="{fmt(cx2 + 74)}" y1="{fmt(ye2_ho)}" x2="{fmt(cx2 + 74)}" y2="{fmt(ye2_tr)}"/>')
    doc.add(f'<text class="smb c2-txt" x="{fmt(cx2 + 79)}" y="{fmt(0.5*(ye2_ho + ye2_tr) + 4.5)}">|α|</text>')

    # Transition arrows for w01 and w12
    ax2 = cx2 - 2
    for (e_lo, e_hi, lbl_t, cls_t, fill_t) in [
        (tr_levels[0], tr_levels[1], "ℏω₀₁", "c1", "c1-fill"),
        (tr_levels[1], tr_levels[2], "ℏω₁₂", "c2", "c2-fill"),
    ]:
        ylo, yhi = map_e(e_lo) - 4, map_e(e_hi) + 4
        doc.add(f'<line class="{cls_t}" stroke-width="1.6" x1="{fmt(ax2)}" y1="{fmt(ylo)}" x2="{fmt(ax2)}" y2="{fmt(yhi)}"/>')
        doc.add(arrow_head(ax2, yhi, 0, -1, 6.0, fill_t))
        doc.add(arrow_head(ax2, ylo, 0, 1, 6.0, fill_t))
        doc.add(f'<text class="sm {cls_t}-txt" x="{fmt(ax2 + 8)}" y="{fmt(0.5 * (ylo + yhi) + 4)}">{lbl_t}</text>')

    # Bottom takeaway note inside left panel
    doc.add('<rect class="note" x="44" y="482" width="428" height="54" rx="10"/>')
    doc.add('<text class="smb" x="58" y="504">α = ω₁₂ − ω₀₁ &lt; 0（典型算例：α/2π ≈ −200 MHz）</text>')
    doc.add('<text class="sm" x="58" y="525">虚线为同曲率抛物势参考；余弦软化拉低 |2⟩，允许按频寻址 |0⟩↔|1⟩</text>')

    # --- Right Panel: Exact Rabi Oscillations Plot ---
    px0, px1 = 582.0, 944.0
    py0, py1 = 446.0, 188.0  # py0=bottom (P1=0), py1=top (P1=1.0)
    t_max = 160.0

    def tx(t_ns: float) -> float:
        return px0 + (t_ns / t_max) * (px1 - px0)

    def ty(p_val: float) -> float:
        return py0 - p_val * (py0 - py1)

    # Grid & ticks
    for p_tick in [0.0, 0.25, 0.50, 0.75, 1.00]:
        yp = ty(p_tick)
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(yp)}" x2="{fmt(px1)}" y2="{fmt(yp)}"/>')
        doc.add(f'<text class="sm" x="{fmt(px0 - 8)}" y="{fmt(yp + 4)}" text-anchor="end">{p_tick:.2f}</text>')
    for t_tick in [0, 40, 80, 120, 160]:
        xt = tx(float(t_tick))
        doc.add(f'<line class="grid" x1="{fmt(xt)}" y1="{fmt(py1)}" x2="{fmt(xt)}" y2="{fmt(py0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xt)}" y="{fmt(py0 + 20)}" text-anchor="middle">{t_tick}</text>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px1 + 8)}" y2="{fmt(py0)}"/>')
    doc.add(arrow_head(px1 + 8, py0, 1, 0, 7.5))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px0)}" y2="{fmt(py1 - 12)}"/>')
    doc.add(arrow_head(px0, py1 - 12, 0, -1, 7.5))
    doc.add(f'<text class="lbl" x="{fmt(0.5*(px0+px1))}" y="{fmt(py0 + 44)}" text-anchor="middle">驱动时间 t (ns)</text>')
    doc.add(
        f'<text class="lbl" x="528" y="{fmt(0.5*(py0+py1))}" text-anchor="middle" '
        f'transform="rotate(-90 528 {fmt(0.5*(py0+py1))})">激发态概率 P₁(t) (无量纲)</text>'
    )

    # Horizontal dotted reference for detuned amplitude 100/136
    yp_det_max = ty(p_peak_det)
    doc.add(f'<line class="guide" x1="{fmt(px0)}" y1="{fmt(yp_det_max)}" x2="{fmt(px1)}" y2="{fmt(yp_det_max)}"/>')

    # Exact curves (321 points = 0.5 ns resolution)
    n_pts = 321
    res_pts = [(tx(t_max * i / (n_pts - 1)), ty(p1_rabi(t_max * i / (n_pts - 1), 0.0))) for i in range(n_pts)]
    det_pts = [(tx(t_max * i / (n_pts - 1)), ty(p1_rabi(t_max * i / (n_pts - 1), delta_mhz))) for i in range(n_pts)]

    doc.add(f'<path class="c1" stroke-width="2.6" d="{path_from_points(res_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.4" stroke-dasharray="8 5" d="{path_from_points(det_pts)}"/>')

    # Peak markers & clean drop lines
    xr1, yr1 = tx(t_pi_res), ty(1.0)
    xd1, yd1 = tx(t_peak_det), ty(p_peak_det)
    doc.add(f'<line class="guide" x1="{fmt(xr1)}" y1="{fmt(yr1)}" x2="{fmt(xr1)}" y2="{fmt(py0)}"/>')
    doc.add(f'<line class="guide" x1="{fmt(xd1)}" y1="{fmt(yd1)}" x2="{fmt(xd1)}" y2="{fmt(py0)}"/>')
    doc.add(f'<circle class="c1-fill" cx="{fmt(xr1)}" cy="{fmt(yr1)}" r="5.5"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(xd1, yd1, 6.5)}"/>')

    # Callouts positioned cleanly in open whitespace (strictly within plot bounds)
    doc.add(f'<text class="smb c1-txt" x="{fmt(xr1 + 10)}" y="{fmt(yr1 - 7)}">t{sub("π")} = 50.0 ns，峰高 1.00</text>')
    x_det_lbl = tx(100.0)
    doc.add(f'<text class="smb c2-txt" x="{fmt(x_det_lbl)}" y="{fmt(ty(0.87))}" text-anchor="middle">失谐首峰 42.9 ns</text>')
    doc.add(f'<text class="smb c2-txt" x="{fmt(x_det_lbl)}" y="{fmt(ty(0.80))}" text-anchor="middle">峰高 100/136 ≈ 0.735</text>')
    doc.add(
        f'<line class="c2" stroke-width="1.2" x1="{fmt(xd1 + 7)}" y1="{fmt(yd1 - 2)}" '
        f'x2="{fmt(x_det_lbl - 62)}" y2="{fmt(ty(0.83))}"/>'
    )

    # Legend bar neatly above the plot area inside right panel
    doc.add('<line class="c1" stroke-width="2.6" x1="532" y1="154" x2="562" y2="154"/>')
    doc.add('<circle class="c1-fill" cx="547" cy="154" r="4"/>')
    doc.add('<text class="sm" x="568" y="158">共振 Δ = 0</text>')

    doc.add('<line class="c2" stroke-width="2.4" stroke-dasharray="7 4" x1="664" y1="154" x2="694" y2="154"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(679, 154, 4.8)}"/>')
    doc.add('<text class="sm" x="700" y="158">失谐 Δ/2π = 6 MHz（Ω/2π = 10 MHz）</text>')

    # Formula bar at bottom of right panel
    doc.add('<rect class="pill" x="524" y="502" width="432" height="34" rx="8"/>')
    doc.add(
        f'<text class="sm" x="740" y="523" text-anchor="middle">'
        f'P₁(t) = (Ω²/Ω{sub("eff")}²) sin²(Ω{sub("eff")} t/2)，Ω{sub("eff")} = √(Ω²+Δ²) ≈ 2π × 11.66 MHz'
        f'</text>'
    )

    return doc.render(), {
        "t_pi_res_ns": t_pi_res,
        "t_peak_det_ns": t_peak_det,
        "p_peak_det": p_peak_det,
        "omega_eff_mhz": omega_eff_mhz,
    }


# ---------------------------------------------------------------------------
# Figure 2: Ch 10 — d=3 Rotated Surface Code + Lattice Surgery (ZZ Merge/Split)
# ---------------------------------------------------------------------------
def _verify_surface_code_algebra() -> dict[str, int]:
    """Verify exact stabilizer commutations & lattice surgery ZZ identity by Pauli algebra."""
    # Patch 1 data qubits: 1..9 (row-major on 3x3 grid)
    # Bulk Z: {1,2,4,5}, {5,6,8,9}; Boundary Z: {2,3} (top), {7,8} (bottom)
    # Bulk X: {2,3,5,6}, {4,5,7,8}; Boundary X: {1,4} (left), {6,9} (right)
    p1_z = [{1, 2, 4, 5}, {5, 6, 8, 9}, {2, 3}, {7, 8}]
    p1_x = [{2, 3, 5, 6}, {4, 5, 7, 8}, {1, 4}, {6, 9}]
    log_z1 = {3, 6, 9}  # right edge vertical Z chain
    log_x1 = {1, 2, 3}  # top edge horizontal X chain

    assert len(p1_z) == 4 and len(p1_x) == 4
    for sz in p1_z:
        for sx in p1_x:
            assert len(sz & sx) % 2 == 0, f"Non-commuting stabilizers {sz}, {sx}"
    for sx in p1_x:
        assert len(log_z1 & sx) % 2 == 0
    for sz in p1_z:
        assert len(log_x1 & sz) % 2 == 0
    assert len(log_z1 & log_x1) % 2 == 1

    # Patch 2 (horizontally mirrored, qubits 11..19):
    # Bulk X: {11,12,14,15}, {15,16,18,19}; Boundary X: {14,17} (left), {13,16} (right)
    # Bulk Z: {12,13,15,16}, {14,15,17,18}; Boundary Z: {11,12} (top), {18,19} (bottom)
    p2_x = [{11, 12, 14, 15}, {15, 16, 18, 19}, {14, 17}, {13, 16}]
    p2_z = [{12, 13, 15, 16}, {14, 15, 17, 18}, {11, 12}, {18, 19}]
    log_z2 = {11, 14, 17}  # left edge vertical Z chain (faces Patch 1's right edge!)
    log_x2 = {11, 12, 13}  # top edge horizontal X chain

    for sz in p2_z:
        for sx in p2_x:
            assert len(sz & sx) % 2 == 0
    for sx in p2_x:
        assert len(log_z2 & sx) % 2 == 0
    for sz in p2_z:
        assert len(log_x2 & sz) % 2 == 0
    assert len(log_z2 & log_x2) % 2 == 1

    # Merged lattice surgery seam between Patch 1 right col (3,6,9) and Patch 2 left col (11,14,17):
    m_z_top = {3, 6, 11, 14}
    m_z_bot = {9, 17}
    m_x_bot = {6, 9, 14, 17}  # merges {6,9} and {14,17}
    merged_z = p1_z + p2_z + [m_z_top, m_z_bot]
    merged_x = [s for s in p1_x if s != {6, 9}] + [s for s in p2_x if s != {14, 17}] + [m_x_bot]

    assert len(merged_z) + len(merged_x) == 17  # 18 data qubits - 17 stabilizers = 1 logical qubit
    for sz in merged_z:
        for sx in merged_x:
            assert len(sz & sx) % 2 == 0
    # Product of new seam Z stabilizers equals exact joint logical operator Z1 * Z2!
    assert (m_z_top ^ m_z_bot) == (log_z1 | log_z2)
    # Joint logical X1 * X2 commutes with all merged stabilizers and anticommutes with Z1
    log_x_merged = log_x1 | log_x2
    for sz in merged_z:
        assert len(log_x_merged & sz) % 2 == 0
    assert len(log_x_merged & log_z1) % 2 == 1

    return {"data_qubits": 9, "x_stabs": 4, "z_stabs": 4, "merged_data": 18, "merged_stabs": 17}


def _draw_mini_patch(
    doc: SvgDoc,
    ox: float,
    oy: float,
    step: float,
    mirrored: bool,
    tag: str,
    hide_inner_x_cap: bool = False,
    highlight_z_col: int | None = None,
) -> None:
    """Draw a compact d=3 rotated surface code patch for lattice surgery steps."""
    # 2x2 interior squares
    for r in range(2):
        for c in range(2):
            is_z = ((r + c) % 2 == 0) if not mirrored else ((r + c) % 2 == 1)
            x, y = ox + c * step, oy + r * step
            cls_fill = "c1-soft" if is_z else "c2-soft"
            pat = "url(#hatch-blue)" if is_z else "url(#hatch-red)"
            doc.add(f'<rect class="{cls_fill}" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(step)}" height="{fmt(step)}"/>')
            doc.add(f'<rect fill="{pat}" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(step)}" height="{fmt(step)}"/>')

    # Boundary semi-ellipses (radius = step/2, bulge = step*0.42)
    rad = step * 0.5
    bulge = step * 0.40

    def cap_h(x1: float, y1: float, up: bool, is_z: bool) -> None:
        cls_f = "c1-soft" if is_z else "c2-soft"
        pat_f = "url(#hatch-blue)" if is_z else "url(#hatch-red)"
        sweep = 1 if up else 0
        d = f"M {fmt(x1)} {fmt(y1)} A {fmt(rad)} {fmt(bulge)} 0 0 {sweep} {fmt(x1 + step)} {fmt(y1)} Z"
        doc.add(f'<path class="{cls_f}" d="{d}"/><path fill="{pat_f}" d="{d}"/>')

    def cap_v(x1: float, y1: float, left: bool, is_z: bool) -> None:
        cls_f = "c1-soft" if is_z else "c2-soft"
        pat_f = "url(#hatch-blue)" if is_z else "url(#hatch-red)"
        sweep = 0 if left else 1
        d = f"M {fmt(x1)} {fmt(y1)} A {fmt(bulge)} {fmt(rad)} 0 0 {sweep} {fmt(x1)} {fmt(y1 + step)} Z"
        doc.add(f'<path class="{cls_f}" d="{d}"/><path fill="{pat_f}" d="{d}"/>')

    if not mirrored:
        cap_h(ox + step, oy, True, True)             # top Z cap (2,3)
        cap_h(ox, oy + 2 * step, False, True)        # bottom Z cap (7,8)
        cap_v(ox, oy, True, False)                   # left X cap (1,4)
        if not hide_inner_x_cap:
            cap_v(ox + 2 * step, oy + step, False, False)  # right X cap (6,9)
    else:
        cap_h(ox, oy, True, True)                    # top Z cap (11,12)
        cap_h(ox + step, oy + 2 * step, False, True)  # bottom Z cap (18,19)
        if not hide_inner_x_cap:
            cap_v(ox, oy + step, True, False)        # left X cap (14,17)
        cap_v(ox + 2 * step, oy, False, False)       # right X cap (13,16)

    # Optional highlighted logical Z edge drawn underneath data qubit circles
    if highlight_z_col is not None:
        hx = ox + highlight_z_col * step
        doc.add(f'<line class="c1" stroke-width="3.6" x1="{fmt(hx)}" y1="{fmt(oy)}" x2="{fmt(hx)}" y2="{fmt(oy + 2*step)}"/>')

    # 9 data qubits
    for r in range(3):
        for c in range(3):
            doc.add(f'<circle class="data-node" cx="{fmt(ox + c * step)}" cy="{fmt(oy + r * step)}" r="3.6"/>')

    # Label underneath (clears bottom boundary cap cleanly)
    doc.add(f'<text class="smb" x="{fmt(ox + step)}" y="{fmt(oy + 2 * step + bulge + 15)}" text-anchor="middle">{escape(tag)}</text>')


def build_fig2_surface_lattice_surgery() -> tuple[str, dict[str, int]]:
    stats = _verify_surface_code_algebra()

    doc = SvgDoc(
        title="d = 3 旋转表面码结构与晶格手术联合测量示意",
        desc=(
            "左面板展示 [[9, 1, 3]] 旋转表面码棋盘格：9 个数据量子比特、4 个 Z 型稳定子面（蓝斜纹，含 2 个四体面与 2 个二体边帽）、"
            "4 个 X 型稳定子面（红反斜纹，含 2 个四体面与 2 个二体边帽）以及逻辑算符链 Z̄ = Z₃Z₆Z₉（沿 Z 边界）与 X̄ = X₁X₂X₃（沿 X 边界）。"
            "右面板分三步示意两块 d = 3 补丁的晶格手术：先面对面放置 Z 边界、再合并边界开启接缝 Z 稳定子（其乘积等于 Z̄₁Z̄₂）、最后分裂回两块独立补丁。"
        ),
    )
    doc.add_header(
        "d = 3 旋转表面码结构与晶格手术（Lattice Surgery）",
        "左：9 数据比特、4 X 稳定子面与 4 Z 稳定子面（[[9, 1, 3]]）；右：合并测联合 Z̄₁Z̄₂ 再分裂的三步流程",
    )
    doc.add_panel(28, 96, 444, 456, "d = 3 旋转表面码棋盘格（[[9, 1, 3]]）")
    doc.add_panel(488, 96, 484, 456, "晶格手术：合并测 Z̄₁Z̄₂ → 分裂（非等比例示意）")

    # --- Left Panel: Large d=3 Rotated Surface Code ---
    ox, oy, step = 148.0, 206.0, 92.0
    bulge = 34.0

    # Bulk plaquettes
    bulk_specs = [
        (0, 0, True, "Z₁"),
        (1, 1, True, "Z₂"),
        (1, 0, False, "X₁"),
        (0, 1, False, "X₂"),
    ]
    for c, r, is_z, name in bulk_specs:
        x, y = ox + c * step, oy + r * step
        cls_f = "c1-soft" if is_z else "c2-soft"
        pat = "url(#hatch-blue)" if is_z else "url(#hatch-red)"
        tcls = "c1-txt" if is_z else "c2-txt"
        doc.add(f'<rect class="{cls_f}" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(step)}" height="{fmt(step)}"/>')
        doc.add(f'<rect fill="{pat}" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(step)}" height="{fmt(step)}"/>')
        doc.add(f'<text class="lblb {tcls}" x="{fmt(x + step/2)}" y="{fmt(y + step/2 + 5)}" text-anchor="middle">{name}</text>')

    # Weight-2 boundary caps
    # Top Z cap on (q2, q3)
    d_top = f"M {fmt(ox + step)} {fmt(oy)} A {fmt(step/2)} {fmt(bulge)} 0 0 1 {fmt(ox + 2*step)} {fmt(oy)} Z"
    doc.add(f'<path class="c1-soft" d="{d_top}"/><path fill="url(#hatch-blue)" d="{d_top}"/>')
    doc.add(f'<text class="smb c1-txt" x="{fmt(ox + 1.5*step)}" y="{fmt(oy - 10)}" text-anchor="middle">Z₃</text>')

    # Bottom Z cap on (q7, q8)
    d_bot = f"M {fmt(ox)} {fmt(oy + 2*step)} A {fmt(step/2)} {fmt(bulge)} 0 0 0 {fmt(ox + step)} {fmt(oy + 2*step)} Z"
    doc.add(f'<path class="c1-soft" d="{d_bot}"/><path fill="url(#hatch-blue)" d="{d_bot}"/>')
    doc.add(f'<text class="smb c1-txt" x="{fmt(ox + 0.5*step)}" y="{fmt(oy + 2*step + 21)}" text-anchor="middle">Z₄</text>')

    # Left X cap on (q1, q4)
    d_lft = f"M {fmt(ox)} {fmt(oy)} A {fmt(bulge)} {fmt(step/2)} 0 0 0 {fmt(ox)} {fmt(oy + step)} Z"
    doc.add(f'<path class="c2-soft" d="{d_lft}"/><path fill="url(#hatch-red)" d="{d_lft}"/>')
    doc.add(f'<text class="smb c2-txt" x="{fmt(ox - 17)}" y="{fmt(oy + 0.5*step + 5)}" text-anchor="middle">X₃</text>')

    # Right X cap on (q6, q9)
    d_rgt = f"M {fmt(ox + 2*step)} {fmt(oy + step)} A {fmt(bulge)} {fmt(step/2)} 0 0 1 {fmt(ox + 2*step)} {fmt(oy + 2*step)} Z"
    doc.add(f'<path class="c2-soft" d="{d_rgt}"/><path fill="url(#hatch-red)" d="{d_rgt}"/>')
    doc.add(f'<text class="smb c2-txt" x="{fmt(ox + 2*step + 17)}" y="{fmt(oy + 1.5*step + 5)}" text-anchor="middle">X₄</text>')

    # Logical operator chains (distinct solid vs dashed + labels)
    # Logical Xbar = X1 X2 X3 (top row, dashed coral/vermilion)
    doc.add(
        f'<line class="c2" stroke-width="5" stroke-dasharray="10 6" stroke-linecap="round" '
        f'x1="{fmt(ox)}" y1="{fmt(oy)}" x2="{fmt(ox + 2*step)}" y2="{fmt(oy)}"/>'
    )
    # Logical Zbar = Z3 Z6 Z9 (right col, solid blue)
    doc.add(
        f'<line class="c1" stroke-width="5" stroke-linecap="round" '
        f'x1="{fmt(ox + 2*step)}" y1="{fmt(oy)}" x2="{fmt(ox + 2*step)}" y2="{fmt(oy + 2*step)}"/>'
    )

    # 9 Data qubits (drawn on top of chains)
    q_idx = 1
    for r in range(3):
        for c in range(3):
            qx, qy = ox + c * step, oy + r * step
            doc.add(f'<circle class="data-node" cx="{fmt(qx)}" cy="{fmt(qy)}" r="12.5"/>')
            doc.add(f'<text class="smb" x="{fmt(qx)}" y="{fmt(qy + 4.5)}" text-anchor="middle">{q_idx}</text>')
            q_idx += 1

    # Boundary & logical chain labels (clear open whitespace around patch)
    doc.add(f'<text class="smb c2-txt" x="{fmt(ox + 0.5*step - 26)}" y="{fmt(oy - 22)}" text-anchor="middle">逻辑 X̄ = X₁X₂X₃</text>')
    doc.add(f'<text class="smb c1-txt" x="{fmt(ox + 2*step + 48)}" y="{fmt(oy + 0.5*step + 4)}" text-anchor="middle">逻辑 Z̄</text>')
    doc.add(f'<text class="sm c1-txt" x="{fmt(ox + 2*step + 48)}" y="{fmt(oy + 0.5*step + 22)}" text-anchor="middle">Z₃Z₆Z₉</text>')
    doc.add(f'<text class="sm" x="{fmt(ox - 54)}" y="{fmt(oy + 1.5*step + 4)}" text-anchor="middle">Z 边界</text>')
    doc.add(f'<text class="sm" x="{fmt(ox + 1.5*step)}" y="{fmt(oy + 2*step + 24)}" text-anchor="middle">X 边界</text>')

    # Legend inside bottom of left panel
    doc.add('<rect class="pill" x="44" y="450" width="412" height="86" rx="10"/>')
    # Row 1: Z face, X face, Data qubit
    doc.add('<rect class="c1-soft" x="58" y="464" width="18" height="14" rx="2"/>')
    doc.add('<rect fill="url(#hatch-blue)" x="58" y="464" width="18" height="14" rx="2"/>')
    doc.add('<text class="sm" x="82" y="476">4 个 Z 稳定子面</text>')
    doc.add('<rect class="c2-soft" x="196" y="464" width="18" height="14" rx="2"/>')
    doc.add('<rect fill="url(#hatch-red)" x="196" y="464" width="18" height="14" rx="2"/>')
    doc.add('<text class="sm" x="220" y="476">4 个 X 稳定子面</text>')
    doc.add('<circle class="data-node" cx="348" cy="471" r="7"/>')
    doc.add('<text class="sm" x="362" y="476">9 数据比特</text>')
    # Row 2: Zbar solid, Xbar dashed
    doc.add('<line class="c1" stroke-width="4" x1="58" y1="504" x2="86" y2="504"/>')
    doc.add('<text class="sm" x="94" y="509">实线：逻辑 Z̄（权 3）</text>')
    doc.add('<line class="c2" stroke-width="4" stroke-dasharray="8 4" x1="242" y1="504" x2="270" y2="504"/>')
    doc.add('<text class="sm" x="278" y="509">虚线：逻辑 X̄（权 3）</text>')
    doc.add('<text class="sm" x="58" y="529">所有 X/Z 稳定子两两对易；X̄ 与 Z̄ 仅交于比特 3（反对易）</text>')

    # --- Right Panel: 3-Step Lattice Surgery ---
    ms = 23.0  # mini patch cell step (each patch 46x46 px, cap bulge 9.2 px)
    p1x = 524.0
    p2x_sep = 616.0
    p2x_mrg = p1x + 3 * ms  # 593.0 -> exact single seam column of width ms

    # Step 1: Separate patches
    doc.add('<rect class="pill" x="504" y="144" width="452" height="118" rx="10"/>')
    doc.add('<text class="smb" x="518" y="162">① 分离态：两块独立 d = 3 逻辑块（2 逻辑比特）</text>')
    p1_y1 = 180.0
    _draw_mini_patch(doc, p1x, p1_y1, ms, False, "块 1（L₁）", highlight_z_col=2)
    _draw_mini_patch(doc, p2x_sep, p1_y1, ms, True, "块 2（L₂）", highlight_z_col=0)
    doc.add('<text class="sm" x="694" y="196">面对面放置两块补丁的 Z 边界</text>')
    doc.add('<text class="sm c1-txt" x="694" y="218">两侧边各承载逻辑 Z̄₁ 与 Z̄₂</text>')
    doc.add('<text class="sm" x="694" y="240">共 18 数据比特、16 个稳定子</text>')

    # Down arrow 1->2
    doc.add('<line class="axis" x1="594" y1="263" x2="594" y2="276"/>')
    doc.add(arrow_head(594, 278, 0, 1, 6.5))

    # Step 2: Merge patches
    doc.add('<rect class="note" x="504" y="280" width="452" height="122" rx="10"/>')
    doc.add('<text class="smb" x="518" y="298">② 边界合并：开启接缝稳定子（维持 d = 3 轮容错测）</text>')
    seam_x = p1x + 2 * ms
    seam_y = 316.0
    _draw_mini_patch(doc, p1x, seam_y, ms, False, "合并后", hide_inner_x_cap=True)
    _draw_mini_patch(doc, p2x_mrg, seam_y, ms, True, "1 逻辑块", hide_inner_x_cap=True)
    # New weight-4 Z seam plaquette (top)
    doc.add(f'<rect class="c3-soft" stroke-width="2.0" x="{fmt(seam_x)}" y="{fmt(seam_y)}" width="{fmt(ms)}" height="{fmt(ms)}"/>')
    doc.add(f'<rect fill="url(#hatch-green)" x="{fmt(seam_x)}" y="{fmt(seam_y)}" width="{fmt(ms)}" height="{fmt(ms)}"/>')
    doc.add(f'<text class="smb c3-txt" x="{fmt(seam_x + ms/2)}" y="{fmt(seam_y + ms/2 + 4.5)}" text-anchor="middle">Z</text>')
    # Merged weight-4 X seam plaquette (bottom)
    doc.add(f'<rect class="c2-soft" stroke-width="1.8" x="{fmt(seam_x)}" y="{fmt(seam_y + ms)}" width="{fmt(ms)}" height="{fmt(ms)}"/>')
    doc.add(f'<rect fill="url(#hatch-red)" x="{fmt(seam_x)}" y="{fmt(seam_y + ms)}" width="{fmt(ms)}" height="{fmt(ms)}"/>')
    doc.add(f'<text class="sm c2-txt" x="{fmt(seam_x + ms/2)}" y="{fmt(seam_y + 1.5*ms + 4.5)}" text-anchor="middle">X</text>')
    # New weight-2 Z seam cap at bottom of seam (with matching green hatch)
    d_sz = f"M {fmt(seam_x)} {fmt(seam_y + 2*ms)} A {fmt(ms/2)} {fmt(ms*0.4)} 0 0 0 {fmt(seam_x + ms)} {fmt(seam_y + 2*ms)} Z"
    doc.add(f'<path class="c3-soft" stroke-width="2" d="{d_sz}"/>')
    doc.add(f'<path fill="url(#hatch-green)" d="{d_sz}"/>')
    # Re-draw seam corner data qubits cleanly on top
    for r in range(3):
        for sx_q in (seam_x, seam_x + ms):
            doc.add(f'<circle class="data-node" cx="{fmt(sx_q)}" cy="{fmt(seam_y + r * ms)}" r="3.4"/>')

    doc.add('<text class="smb c3-txt" x="676" y="328">新接缝 Z 面乘积 = Z̄₁Z̄₂</text>')
    doc.add('<text class="sm" x="676" y="349">读出联合本征值 m = ±1（不读单块 Z̄）</text>')
    doc.add('<text class="sm" x="676" y="370">独立稳定子增至 17 个 → 1 逻辑比特</text>')
    doc.add('<text class="sm" x="676" y="391">合并 X 面由原两二体 X 帽相乘决定</text>')

    # Down arrow 2->3
    doc.add('<line class="axis" x1="594" y1="403" x2="594" y2="416"/>')
    doc.add(arrow_head(594, 418, 0, 1, 6.5))

    # Step 3: Split back into two patches
    doc.add('<rect class="pill" x="504" y="420" width="452" height="118" rx="10"/>')
    doc.add('<text class="smb" x="518" y="438">③ 重新分裂：停测接缝 Z，恢复各自独立边界</text>')
    p1_y3 = 456.0
    _draw_mini_patch(doc, p1x, p1_y3, ms, False, "块 1（L₁′）")
    _draw_mini_patch(doc, p2x_sep, p1_y3, ms, True, "块 2（L₂′）")
    # Subtle correlation dashed bridge between separated patches
    doc.add(
        f'<line class="c3" stroke-width="2" stroke-dasharray="5 4" '
        f'x1="{fmt(p1x + 2*ms + 4)}" y1="{fmt(p1_y3 + ms)}" x2="{fmt(p2x_sep - 4)}" y2="{fmt(p1_y3 + ms)}"/>'
    )
    doc.add('<text class="smb c3-txt" x="694" y="472">恢复 2 逻辑比特，且已被投影至</text>')
    doc.add('<text class="smb c3-txt" x="694" y="493">联合本征子空间 Z̄₁Z̄₂ = m</text>')
    doc.add('<text class="sm" x="694" y="515">单边 X 边帽随机结果记入 Pauli 帧</text>')

    return doc.render(), stats


# ---------------------------------------------------------------------------
# Figure 3: Ch 12 — BB84 Protocol Workflow + Exact PLOB Capacity Bound
# ---------------------------------------------------------------------------
def build_fig3_bb84_plob() -> tuple[str, dict[str, float]]:
    def eta_fiber(dist_km: float) -> float:
        return 10.0 ** (-0.02 * dist_km)

    def c_plob(dist_km: float) -> float:
        eta = eta_fiber(dist_km)
        # Use log1p(-eta) for full precision at small eta (e.g., L=200, 300 km)
        return -math.log1p(-eta) / math.log(2.0)

    c50 = c_plob(50.0)
    c100 = c_plob(100.0)
    c200 = c_plob(200.0)
    c300 = c_plob(300.0)

    assert abs(eta_fiber(50.0) - 0.1) < 1e-15
    assert abs(eta_fiber(100.0) - 0.01) < 1e-15
    assert abs(eta_fiber(200.0) - 1e-4) < 1e-18
    assert abs(c50 - (-math.log2(0.9))) < 1e-12
    assert abs(c100 - 0.01449956969511509) < 1e-12
    assert abs(c200 - 1.44276718e-4) < 1e-9
    assert 1e-6 < c300 < 1e1

    # Distance where C_PLOB = 10 bit/mode (top of y-axis)
    eta_top = 1.0 - 2.0 ** (-10.0)
    l_top = -math.log10(eta_top) / 0.02
    assert abs(c_plob(l_top) - 10.0) < 1e-9

    doc = SvgDoc(
        title="BB84 协议关键流程与纯损耗光纤 PLOB 容量上限",
        desc=(
            "左面板展示 BB84 量子密钥分发四阶段流程：选基发态、随机选基测量、经已认证经典信道比基筛选、随机公开抽检估计 QBER。"
            "右面板以对数纵轴（10⁻⁶ 至 10¹ bit/模式）精确绘制 0.2 dB/km 光纤（透射率 η = 10⁻⁰·⁰²ᴸ）下无中继 PLOB 秘密密钥容量上限 "
            "C_PLOB = −log₂(1−η) 随距离 L ∈ [0, 300] km 的衰减曲线，并标出 50 km（0.152）、100 km（0.0145）与 200 km（1.44×10⁻⁴）数值。"
        ),
    )
    doc.add_header(
        "BB84 密钥分发流程与纯损耗光纤 PLOB 容量上限",
        "左：BB84 四阶段筛选与 QBER 抽检流程；右：光纤透射率 η = 10⁻⁰·⁰²ᴸ 下的无中继理论极限",
    )
    doc.add_panel(28, 96, 424, 456, "BB84 密钥分发关键步骤（非等比例流程）")
    doc.add_panel(468, 96, 504, 456, "PLOB 无中继秘密密钥容量上限（0.2 dB/km）")

    # --- Left Panel: BB84 4-Step Vertical Flow ---
    steps = [
        ("1", "选基与发态（Alice）", "随机选比特 b ∈ {0,1} 与基 Z / X", "发出单光子态 |0⟩,|1⟩ 或 |+⟩,|−⟩", "c1-soft", "c1-fill"),
        ("2", "随机选基测量（Bob）", "独立随机选 Z / X 基探测到达光子", "光纤损耗使单光子仅以概率 η 到达", "c2-soft", "c2-fill"),
        ("3", "经典比基筛选（Sifting）", "经已认证经典信道公开各自基选择", "同基结果保留（约 50%），异基丢弃", "c3-soft", "c3-fill"),
        ("4", "公开抽检估计 QBER", "牺牲随机子集测误码率 Q（重发攻击 25%）", "再行信息协调（纠错）与隐私放大", "pill", "axis-fill"),
    ]
    sy = 148.0
    box_h = 72.0
    gap = 18.0
    for idx, (num, head, line1, line2, box_cls, badge_cls) in enumerate(steps):
        y = sy + idx * (box_h + gap)
        doc.add(f'<rect class="{box_cls}" x="46" y="{fmt(y)}" width="388" height="{fmt(box_h)}" rx="10"/>')
        doc.add(f'<circle class="{badge_cls}" cx="70" cy="{fmt(y + 24)}" r="12"/>')
        doc.add(
            f'<text class="badge-txt" x="70" y="{fmt(y + 28.5)}" '
            f'text-anchor="middle">{num}</text>'
        )
        doc.add(f'<text class="smb" x="92" y="{fmt(y + 25)}">{escape(head)}</text>')
        doc.add(f'<text class="sm" x="92" y="{fmt(y + 45)}">{escape(line1)}</text>')
        doc.add(f'<text class="sm" x="92" y="{fmt(y + 63)}">{escape(line2)}</text>')
        if idx < len(steps) - 1:
            ay1 = y + box_h + 1
            ay2 = y + box_h + gap - 2
            doc.add(f'<line class="axis" x1="240" y1="{fmt(ay1)}" x2="240" y2="{fmt(ay2)}"/>')
            doc.add(arrow_head(240, ay2 + 1, 0, 1, 6.5))

    doc.add('<rect class="note" x="46" y="496" width="388" height="44" rx="9"/>')
    doc.add('<text class="sm" x="60" y="514">安全边界：经典信道须已认证；公开抽检比特须销毁。</text>')
    doc.add('<text class="sm" x="60" y="532">25% 为全截获重发期望值，不是“低于即安全”的门槛。</text>')

    # --- Right Panel: Exact Log-Y PLOB Plot ---
    px0, px1 = 552.0, 944.0
    py0, py1 = 446.0, 174.0  # log10(C) from -6 (py0) to +1 (py1)
    l_max = 300.0
    log_min, log_max = -6.0, 1.0

    def lx(dist: float) -> float:
        return px0 + (dist / l_max) * (px1 - px0)

    def ly(val: float) -> float:
        lv = math.log10(val)
        return py0 - ((lv - log_min) / (log_max - log_min)) * (py0 - py1)

    # Horizontal decade gridlines and labels
    sup_map = {
        -6: "10⁻⁶", -5: "10⁻⁵", -4: "10⁻⁴", -3: "10⁻³",
        -2: "10⁻²", -1: "10⁻¹", 0: "10⁰", 1: "10¹",
    }
    for exp in range(-6, 2):
        ye = ly(10.0 ** exp)
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(ye)}" x2="{fmt(px1)}" y2="{fmt(ye)}"/>')
        doc.add(f'<text class="sm" x="{fmt(px0 - 8)}" y="{fmt(ye + 4.5)}" text-anchor="end">{sup_map[exp]}</text>')

    # Vertical gridlines & ticks
    for d_tick in [0, 50, 100, 150, 200, 250, 300]:
        xd = lx(float(d_tick))
        doc.add(f'<line class="grid" x1="{fmt(xd)}" y1="{fmt(py1)}" x2="{fmt(xd)}" y2="{fmt(py0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xd)}" y="{fmt(py0 + 20)}" text-anchor="middle">{d_tick}</text>')

    # Sample PLOB curve densely near L=0 (log spacing) + linear up to 300 km
    l_samples: list[float] = []
    for i in range(60):
        frac = i / 59.0
        l_samples.append(l_top * ((15.0 / l_top) ** frac))
    for i in range(1, 144):
        l_samples.append(15.0 + (300.0 - 15.0) * i / 143.0)
    plob_pts = [(lx(dist), ly(c_plob(dist))) for dist in l_samples]

    # Forbidden upper region shading (above PLOB bound)
    forbid_poly = [(lx(l_top), py1), (px1, py1)] + list(reversed(plob_pts))
    doc.add(f'<polygon class="forbid" points="{pts_str(forbid_poly)}"/>')
    doc.add('<text class="smb c2-txt" x="836" y="200" text-anchor="middle">无中继不可逾越区域</text>')
    doc.add('<text class="sm c2-txt" x="836" y="219" text-anchor="middle">（需中点干涉站或量子中继器）</text>')
    doc.add('<text class="sm c2-txt" x="836" y="238" text-anchor="middle">单中点方案如 TF-QKD 遵循单中点界</text>')

    # Secondary dashed reference: raw transmittance eta(L) = 10^(-0.02 L)
    eta_pts = [(lx(d), ly(eta_fiber(d))) for d in [0.0, 50.0, 100.0, 150.0, 200.0, 250.0, 300.0]]
    doc.add(f'<path class="c2" stroke-width="1.8" stroke-dasharray="7 5" d="{path_from_points(eta_pts)}"/>')

    # Main solid PLOB curve
    doc.add(f'<path class="c1" stroke-width="2.8" d="{path_from_points(plob_pts)}"/>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px1 + 8)}" y2="{fmt(py0)}"/>')
    doc.add(arrow_head(px1 + 8, py0, 1, 0, 7.5))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px0)}" y2="{fmt(py1 - 12)}"/>')
    doc.add(arrow_head(px0, py1 - 12, 0, -1, 7.5))
    doc.add(f'<text class="lbl" x="{fmt(0.5*(px0+px1))}" y="{fmt(py0 + 44)}" text-anchor="middle">光纤距离 L (km)</text>')
    doc.add(
        f'<text class="lbl" x="492" y="{fmt(0.5*(py0+py1))}" text-anchor="middle" '
        f'transform="rotate(-90 492 {fmt(0.5*(py0+py1))})">容量上限 C{sub("PLOB")} (bit/模式) · 虚线 η (无量纲)</text>'
    )

    # Highlighted benchmark points at 50, 100, 200 km
    markers = [
        (50.0, c50, "50 km：0.152", 12, -14),
        (100.0, c100, "100 km：0.0145", 12, -14),
        (200.0, c200, "200 km：1.44×10⁻⁴", 6, -22),
    ]
    for d_m, c_m, label_m, dx_m, dy_m in markers:
        xm, ym = lx(d_m), ly(c_m)
        doc.add(f'<line class="guide" x1="{fmt(xm)}" y1="{fmt(ym)}" x2="{fmt(xm)}" y2="{fmt(py0)}"/>')
        doc.add(f'<circle class="c1-fill" cx="{fmt(xm)}" cy="{fmt(ym)}" r="5.2"/>')
        doc.add(
            f'<line class="c1" stroke-width="1.2" x1="{fmt(xm + 4)}" y1="{fmt(ym - 4)}" '
            f'x2="{fmt(xm + dx_m + 4)}" y2="{fmt(ym + dy_m + 3)}"/>'
        )
        doc.add(f'<text class="smb c1-txt" x="{fmt(xm + dx_m + 6)}" y="{fmt(ym + dy_m + 2)}">{label_m}</text>')

    # Legend inside top of right panel
    doc.add('<line class="c1" stroke-width="2.8" x1="564" y1="154" x2="594" y2="154"/>')
    doc.add(f'<text class="sm" x="600" y="158">C{sub("PLOB")} = −log₂(1−η)</text>')
    doc.add('<line class="c2" stroke-width="1.8" stroke-dasharray="7 5" x1="766" y1="154" x2="796" y2="154"/>')
    doc.add('<text class="sm" x="802" y="158">透射率 η = 10⁻⁰·⁰²ᴸ</text>')

    # Bottom disclaimer note in right panel
    doc.add('<rect class="pill" x="486" y="502" width="468" height="36" rx="8"/>')
    doc.add(
        f'<text class="sm" x="720" y="524" text-anchor="middle">'
        f'长距渐近 C{sub("PLOB")} ≈ η/ln 2 ≈ 1.443 η；纯损耗理论界不含探测效率与暗计数'
        f'</text>'
    )

    return doc.render(), {"c50": c50, "c100": c100, "c200": c200, "c300": c300}


# ---------------------------------------------------------------------------
# Figure 4: Ch 13 — Binary Shannon Entropy + Helstrom Axis & Holevo Gap
# ---------------------------------------------------------------------------
def build_fig4_helstrom_entropy() -> tuple[str, dict[str, float]]:
    def h2(p: float) -> float:
        if p <= 0.0 or p >= 1.0:
            return 0.0
        return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)

    # Equal-prior |0>, |+> exact quantities
    overlap = 1.0 / math.sqrt(2.0)
    trace_dist = math.sqrt(1.0 - overlap * overlap)
    p_succ = 0.5 * (1.0 + trace_dist)           # cos^2(pi/8) ~= 0.85355339
    p_err = 1.0 - p_succ                        # sin^2(pi/8) ~= 0.14644661
    chi_holevo = h2(p_succ)                     # ~= 0.60087604 bit
    i_acc = 1.0 - h2(p_err)                     # ~= 0.39912396 bit

    assert abs(h2(0.5) - 1.0) < 1e-15
    assert abs(p_succ - math.cos(math.pi / 8.0) ** 2) < 1e-12
    assert abs(p_succ - 0.853553390593) < 1e-9
    assert abs(chi_holevo - 0.600876036) < 1e-6
    assert abs(i_acc - 0.399123964) < 1e-6
    assert abs((chi_holevo + i_acc) - 1.0) < 1e-12

    doc = SvgDoc(
        title="二元香农熵、Helstrom 最优测量轴与 Holevo 界对比",
        desc=(
            "左面板精确绘制二元香农熵 H₂(p) = −p log₂p − (1−p)log₂(1−p) 在 p ∈ [0, 1] 的凹曲线，"
            "标出 p = 0.5 处最大值 1.00 bit 及 p_e ≈ 0.146 处 H₂(p_e) ≈ 0.601 bit。"
            "右面板上部在 Bloch x-z 截面标出等先验态 |0⟩ 与 |+⟩（Bloch 夹角 90°）以及最优 Helstrom 测量轴"
            "（Bloch 偏转 45°，对应态空间夹角 θ/2 = 22.5°，成功率 cos²22.5° = 85.36%）；"
            "下部柱状图对比 Holevo 上界 χ = 0.601 bit 与单次可访问信息 I_acc = 0.399 bit。"
        ),
    )
    doc.add_header(
        "二元香农熵、Helstrom 最优判别与 Holevo 界间隙",
        f"左：二元香农熵 H₂(p) 精确曲线；右：等先验 |0⟩ 与 |+⟩ 的最优测量轴及 χ 与 I{sub('acc')} 对比",
        raw_sub=True,
    )
    doc.add_panel(28, 96, 444, 456, "二元香农熵 H₂(p)（精确曲线）")
    doc.add_panel(488, 96, 484, 456, "等先验 |0⟩、|+⟩：Helstrom 判别与 Holevo 间隙")

    # --- Left Panel: Exact H2(p) Plot ---
    px0, px1 = 98.0, 442.0
    py0, py1 = 440.0, 178.0  # H2 in [0, 1.08]
    y_max = 1.08

    def hx(p: float) -> float:
        return px0 + p * (px1 - px0)

    def hy(val: float) -> float:
        return py0 - (val / y_max) * (py0 - py1)

    for y_t in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        yp = hy(y_t)
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(yp)}" x2="{fmt(px1)}" y2="{fmt(yp)}"/>')
        doc.add(f'<text class="sm" x="{fmt(px0 - 8)}" y="{fmt(yp + 4.5)}" text-anchor="end">{y_t:.1f}</text>')
    for x_t in [0.0, 0.25, 0.50, 0.75, 1.00]:
        xp = hx(x_t)
        doc.add(f'<line class="grid" x1="{fmt(xp)}" y1="{fmt(py1)}" x2="{fmt(xp)}" y2="{fmt(py0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xp)}" y="{fmt(py0 + 20)}" text-anchor="middle">{x_t:g}</text>')

    # Dense cosine-spaced sampling near 0 and 1 for crisp vertical tangents
    p_samples = [0.5 * (1.0 - math.cos(math.pi * i / 180.0)) for i in range(181)]
    h_pts = [(hx(p), hy(h2(p))) for p in p_samples]
    area_pts = [(px0, py0)] + h_pts + [(px1, py0)]
    doc.add(f'<polygon class="area1" points="{pts_str(area_pts)}"/>')
    doc.add(f'<path class="c1" stroke-width="2.8" d="{path_from_points(h_pts)}"/>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px1 + 8)}" y2="{fmt(py0)}"/>')
    doc.add(arrow_head(px1 + 8, py0, 1, 0, 7.5))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px0)}" y2="{fmt(py1 - 12)}"/>')
    doc.add(arrow_head(px0, py1 - 12, 0, -1, 7.5))
    doc.add(f'<text class="lbl" x="{fmt(0.5*(px0+px1))}" y="{fmt(py0 + 44)}" text-anchor="middle">二元事件概率 p (无量纲)</text>')
    doc.add(
        f'<text class="lbl" x="48" y="{fmt(0.5*(py0+py1))}" text-anchor="middle" '
        f'transform="rotate(-90 48 {fmt(0.5*(py0+py1))})">二元香农熵 H₂(p) (bit)</text>'
    )

    # Peak marker at (0.5, 1.0)
    x5, y5 = hx(0.5), hy(1.0)
    doc.add(f'<line class="guide" x1="{fmt(x5)}" y1="{fmt(y5)}" x2="{fmt(x5)}" y2="{fmt(py0)}"/>')
    doc.add(f'<circle class="c1-fill" cx="{fmt(x5)}" cy="{fmt(y5)}" r="5.5"/>')
    doc.add(f'<text class="smb c1-txt" x="{fmt(x5)}" y="{fmt(y5 - 12)}" text-anchor="middle">峰值：p = 0.5，H₂ = 1.00 bit</text>')

    # Bridge marker at (p_err, chi_holevo) showing H2(p_e) = 0.601 bit
    xe, ye = hx(p_err), hy(chi_holevo)
    doc.add(f'<line class="guide" x1="{fmt(xe)}" y1="{fmt(ye)}" x2="{fmt(xe)}" y2="{fmt(py0)}"/>')
    doc.add(f'<line class="guide" x1="{fmt(px0)}" y1="{fmt(ye)}" x2="{fmt(xe)}" y2="{fmt(ye)}"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(xe, ye, 6.2)}"/>')
    doc.add(f'<text class="smb c2-txt" x="{fmt(xe + 11)}" y="{fmt(ye + 18)}">p{sub("e")} ≈ 0.146</text>')
    doc.add(f'<text class="sm c2-txt" x="{fmt(xe + 11)}" y="{fmt(ye + 36)}">H₂ = 0.601 bit</text>')

    # Formula bar at bottom of left panel
    doc.add('<rect class="pill" x="44" y="502" width="412" height="36" rx="8"/>')
    doc.add(
        '<text class="sm" x="250" y="524" text-anchor="middle">'
        'H₂(p) = −p log₂p − (1−p) log₂(1−p)（对称严格凹函数）'
        '</text>'
    )

    # --- Right Panel Top: Bloch x-z Plane & Helstrom Measurement Axis ---
    cx, cy, r = 602.0, 256.0, 74.0
    doc.add(f'<circle class="c1-soft" fill-opacity=".35" cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}"/>')
    # Bloch x and z axes
    doc.add(f'<line class="axis" x1="{fmt(cx - r - 18)}" y1="{fmt(cy)}" x2="{fmt(cx + r + 18)}" y2="{fmt(cy)}"/>')
    doc.add(arrow_head(cx + r + 18, cy, 1, 0, 7.0))
    doc.add(f'<line class="axis" x1="{fmt(cx)}" y1="{fmt(cy + r + 18)}" x2="{fmt(cx)}" y2="{fmt(cy - r - 18)}"/>')
    doc.add(arrow_head(cx, cy - r - 18, 0, -1, 7.0))
    doc.add(f'<text class="smb" x="{fmt(cx + 8)}" y="{fmt(cy - r - 14)}">+Z：|0⟩</text>')
    doc.add(f'<text class="sm" x="{fmt(cx + 8)}" y="{fmt(cy + r + 19)}">−Z：|1⟩</text>')
    doc.add(f'<text class="smb" x="{fmt(cx + r + 22)}" y="{fmt(cy + 4.5)}">+X：|+⟩</text>')
    doc.add(f'<text class="sm" x="{fmt(cx - r - 22)}" y="{fmt(cy + 4.5)}" text-anchor="end">−X</text>')

    # Right angle square marker (90 deg between |0> and |+> on Bloch circle)
    doc.add(f'<path class="c1" stroke-width="1.6" d="M {fmt(cx)} {fmt(cy - 15)} H {fmt(cx + 15)} V {fmt(cy)}"/>')
    doc.add(f'<text class="sm c1-txt" x="{fmt(cx + 20)}" y="{fmt(cy - 10)}">90°</text>')

    # Signal state vectors |0> and |+>
    doc.add(f'<line class="c1" stroke-width="3.0" x1="{fmt(cx)}" y1="{fmt(cy)}" x2="{fmt(cx)}" y2="{fmt(cy - r)}"/>')
    doc.add(f'<circle class="c1-fill" cx="{fmt(cx)}" cy="{fmt(cy - r)}" r="5"/>')
    doc.add(f'<line class="c1" stroke-width="3.0" x1="{fmt(cx)}" y1="{fmt(cy)}" x2="{fmt(cx + r)}" y2="{fmt(cy)}"/>')
    doc.add(f'<circle class="c1-fill" cx="{fmt(cx + r)}" cy="{fmt(cy)}" r="5"/>')

    # Optimal Helstrom measurement axis: Bloch vector (+- 1/sqrt2)(-x, +z) -> 45 deg CCW from +Z
    d45 = r / math.sqrt(2.0)
    m0x, m0y = cx - d45, cy - d45
    mpx, mpy = cx + d45, cy + d45
    doc.add(
        f'<line class="c2" stroke-width="2.6" stroke-dasharray="8 4" '
        f'x1="{fmt(m0x)}" y1="{fmt(m0y)}" x2="{fmt(mpx)}" y2="{fmt(mpy)}"/>'
    )
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(m0x, m0y, 5.6)}"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(mpx, mpy, 5.6)}"/>')
    doc.add(f'<text class="smb c2-txt" x="{fmt(m0x - 8)}" y="{fmt(m0y - 6)}" text-anchor="end">|m₀⟩</text>')
    doc.add(f'<text class="smb c2-txt" x="{fmt(mpx + 8)}" y="{fmt(mpy + 14)}">|m₊⟩</text>')

    # Arc from +Z to |m0> (45 deg on Bloch = 22.5 deg in Hilbert space)
    ra = 30.0
    ax_end = cx - ra / math.sqrt(2.0)
    ay_end = cy - ra / math.sqrt(2.0)
    doc.add(
        f'<path class="c2" stroke-width="1.6" '
        f'd="M {fmt(cx)} {fmt(cy - ra)} A {fmt(ra)} {fmt(ra)} 0 0 0 {fmt(ax_end)} {fmt(ay_end)}"/>'
    )
    doc.add(f'<text class="sm c2-txt" x="{fmt(cx - 17)}" y="{fmt(cy - 39)}" text-anchor="middle">45°</text>')

    # Side callout card right of Bloch circle
    doc.add('<rect class="note" x="776" y="152" width="180" height="194" rx="10"/>')
    doc.add('<text class="smb" x="788" y="176">Bloch x-z 截面几何</text>')
    doc.add('<text class="sm" x="788" y="199">|0⟩ 与 |+⟩ 夹角：90°</text>')
    doc.add('<text class="sm c2-txt" x="788" y="222">Helstrom 最优轴：</text>')
    doc.add('<text class="sm" x="788" y="242">Bloch 偏角 45°</text>')
    doc.add('<text class="smb c2-txt" x="788" y="263">态空间夹角 22.5°</text>')
    doc.add('<text class="sm" x="788" y="287">最小错误率 14.64%</text>')
    doc.add('<text class="smb c3-txt" x="788" y="310">成功率 85.36%</text>')
    doc.add('<text class="sm" x="788" y="332">(cos² 22.5° = (2+√2)/4)</text>')

    # --- Right Panel Bottom: Holevo vs Accessible Info Bar Comparison ---
    doc.add('<line class="grid" x1="504" y1="378" x2="956" y2="378"/>')
    doc.add('<text class="smb" x="508" y="400">单次可访问信息与 Holevo 上界（单位：bit）</text>')

    bx0, bx1 = 618.0, 944.0  # 0 to 1.0 bit

    def bx(bits: float) -> float:
        return bx0 + bits * (bx1 - bx0)

    for b_tick in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        xb = bx(b_tick)
        doc.add(f'<line class="grid" x1="{fmt(xb)}" y1="412" x2="{fmt(xb)}" y2="500"/>')
        doc.add(f'<text class="sm" x="{fmt(xb)}" y="518" text-anchor="middle">{b_tick:.1f}</text>')
    doc.add(f'<line class="axis" x1="{fmt(bx0)}" y1="500" x2="{fmt(bx1 + 8)}" y2="500"/>')
    doc.add(arrow_head(bx1 + 8, 500, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(bx0)}" y1="412" x2="{fmt(bx0)}" y2="500"/>')
    doc.add('<text class="sm" x="781" y="540" text-anchor="middle">信息量 (bit)</text>')

    # Bar 1: Holevo bound chi = 0.601 bit
    w_chi = bx(chi_holevo) - bx0
    doc.add(f'<rect class="c1-soft" stroke-width="1.8" x="{fmt(bx0)}" y="418" width="{fmt(w_chi)}" height="28" rx="4"/>')
    doc.add(f'<rect fill="url(#hatch-blue)" x="{fmt(bx0)}" y="418" width="{fmt(w_chi)}" height="28" rx="4"/>')
    doc.add('<text class="smb" x="610" y="437" text-anchor="end">Holevo 上界 χ</text>')
    doc.add(f'<text class="smb c1-txt" x="{fmt(bx0 + w_chi + 8)}" y="437">{chi_holevo:.3f} bit</text>')

    # Bar 2: Single-shot accessible info I_acc = 0.399 bit (value centered inside bar; gap arrow to chi)
    w_acc = bx(i_acc) - bx0
    doc.add(f'<rect class="c2-soft" stroke-width="1.8" x="{fmt(bx0)}" y="458" width="{fmt(w_acc)}" height="28" rx="4"/>')
    doc.add(f'<rect fill="url(#hatch-red)" x="{fmt(bx0)}" y="458" width="{fmt(w_acc)}" height="28" rx="4"/>')
    doc.add(f'<text class="smb" x="610" y="477" text-anchor="end">可访问信息 I{sub("acc")}</text>')
    doc.add(f'<text class="smb c2-txt" x="{fmt(bx0 + w_acc * 0.5)}" y="477" text-anchor="middle">{i_acc:.3f} bit</text>')

    # Strict gap double-arrow between 0.399 and 0.601 + label right of dashed line
    gx1, gx2 = bx(i_acc), bx(chi_holevo)
    doc.add(f'<line class="guide" x1="{fmt(gx2)}" y1="446" x2="{fmt(gx2)}" y2="494"/>')
    doc.add(f'<line class="c3" stroke-width="1.8" x1="{fmt(gx1 + 4)}" y1="472" x2="{fmt(gx2 - 4)}" y2="472"/>')
    doc.add(arrow_head(gx1 + 3, 472, -1, 0, 5.5, "c3-fill"))
    doc.add(arrow_head(gx2 - 3, 472, 1, 0, 5.5, "c3-fill"))
    doc.add(f'<text class="smb c3-txt" x="{fmt(gx2 + 8)}" y="477">间隙 0.202 bit</text>')

    return doc.render(), {
        "p_succ": p_succ,
        "p_err": p_err,
        "chi_holevo": chi_holevo,
        "i_acc": i_acc,
    }


# ---------------------------------------------------------------------------
# Figure 5: Ch 14 — Gaussian + DRAG Waveform & Dynamic Decoupling Timelines
# ---------------------------------------------------------------------------
def build_fig5_drag_dd_pulses() -> tuple[str, dict[str, float]]:
    # Exact Gaussian + DRAG parameters (transmon example: alpha/2pi = -200 MHz)
    t_total = 16.0
    t0 = 8.0
    sigma = 2.0
    alpha_rad_ns = -2.0 * math.pi * 0.2  # -200 MHz in rad/ns
    beta = 1.0  # DRAG weighting coefficient

    def env_i(t_ns: float) -> float:
        return math.exp(-0.5 * ((t_ns - t0) / sigma) ** 2)

    def env_di(t_ns: float) -> float:
        return -((t_ns - t0) / (sigma * sigma)) * env_i(t_ns)

    def env_q(t_ns: float) -> float:
        # Q(t) = -(beta / alpha) * dI/dt
        return -(beta / alpha_rad_ns) * env_di(t_ns)

    q_peak_exact = beta / (abs(alpha_rad_ns) * sigma * math.sqrt(math.e))
    assert abs(env_i(t0) - 1.0) < 1e-15
    assert abs(env_q(t0)) < 1e-15
    assert abs(env_q(t0 - sigma) - q_peak_exact) < 1e-12
    assert abs(env_q(t0 + sigma) + q_peak_exact) < 1e-12
    assert env_q(t0 - sigma) > 0.0 and env_q(t0 + sigma) < 0.0

    # Verify CPMG-4 exact timing fractions sum to 1 and DC filter function cancels
    cpmg_intervals = [1 / 8, 1 / 4, 1 / 4, 1 / 4, 1 / 8]
    cpmg_signs = [1, -1, 1, -1, 1]
    assert abs(sum(cpmg_intervals) - 1.0) < 1e-15
    assert abs(sum(dt * s for dt, s in zip(cpmg_intervals, cpmg_signs))) < 1e-15

    doc = SvgDoc(
        title="DRAG 高斯整形脉冲波形与动态解耦时序对比",
        desc=(
            "左面板精确绘制高斯同相包络 I(t) = Ω₀ exp[−(t−t₀)²/(2σ²)]（实线，t₀ = 8 ns，σ = 2 ns）"
            "与 DRAG 正交导数修正 Q(t) = −(β/α) İ(t)（虚线，α/2π = −200 MHz，β = 1，正负峰位于 t₀ ± σ = 6、10 ns，"
            "幅值 ±0.241 Ω₀）。右面板对比相同总时长 T 下的三种时序：自由演化 Ramsey、Hahn 自旋回波（T/2 − π − T/2）"
            "与 CPMG 四脉冲序列（τ/2 − π_Y − τ − π_Y − τ − π_Y − τ − π_Y − τ/2，τ = T/4，初末脉冲为 π/2_X）。"
        ),
    )
    doc.add_header(
        "DRAG 抑制泄漏整形脉冲与动态解耦时序对比",
        "左：高斯包络 I(t) 与 DRAG 正交导数修正 Q(t) 精确波形；右：Ramsey、Hahn 回波与 CPMG-4 时序",
    )
    doc.add_panel(28, 96, 456, 456, "DRAG 脉冲包络（精确公式，σ = 2 ns）")
    doc.add_panel(500, 96, 472, 456, "动态解耦时序对比（相同总时长 T，非等比例示意）")

    # --- Left Panel: Exact Gaussian I(t) and DRAG Q(t) ---
    px0, px1 = 100.0, 460.0
    py0, py1 = 442.0, 184.0  # amplitude in [-0.35, 1.08]
    a_min, a_max = -0.35, 1.08

    def gx(t_ns: float) -> float:
        return px0 + (t_ns / t_total) * (px1 - px0)

    def gy(amp: float) -> float:
        return py0 - ((amp - a_min) / (a_max - a_min)) * (py0 - py1)

    for a_t in [-0.25, 0.0, 0.25, 0.50, 0.75, 1.00]:
        ya = gy(a_t)
        cls_g = "axis" if abs(a_t) < 1e-9 else "grid"
        sw = ' stroke-width="1.4"' if abs(a_t) < 1e-9 else ""
        doc.add(f'<line class="{cls_g}"{sw} x1="{fmt(px0)}" y1="{fmt(ya)}" x2="{fmt(px1)}" y2="{fmt(ya)}"/>')
        doc.add(f'<text class="sm" x="{fmt(px0 - 8)}" y="{fmt(ya + 4.5)}" text-anchor="end">{a_t:+.2f}</text>' if a_t < 0 else f'<text class="sm" x="{fmt(px0 - 8)}" y="{fmt(ya + 4.5)}" text-anchor="end">{a_t:.2f}</text>')

    for t_t in [0, 4, 8, 12, 16]:
        xt = gx(float(t_t))
        doc.add(f'<line class="grid" x1="{fmt(xt)}" y1="{fmt(py1)}" x2="{fmt(xt)}" y2="{fmt(py0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xt)}" y="{fmt(py0 + 20)}" text-anchor="middle">{t_t}</text>')

    # Curve points
    n_pts = 241
    i_pts = [(gx(t_total * k / (n_pts - 1)), gy(env_i(t_total * k / (n_pts - 1)))) for k in range(n_pts)]
    q_pts = [(gx(t_total * k / (n_pts - 1)), gy(env_q(t_total * k / (n_pts - 1)))) for k in range(n_pts)]

    # Shaded area under I(t) down to zero baseline
    y_zero = gy(0.0)
    i_area = [(px0, y_zero)] + i_pts + [(px1, y_zero)]
    doc.add(f'<polygon class="area1" points="{pts_str(i_area)}"/>')
    doc.add(f'<path class="c1" stroke-width="2.6" d="{path_from_points(i_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.4" stroke-dasharray="8 5" d="{path_from_points(q_pts)}"/>')

    # Frame axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px1 + 8)}" y2="{fmt(py0)}"/>')
    doc.add(arrow_head(px1 + 8, py0, 1, 0, 7.5))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px0)}" y2="{fmt(py1 - 12)}"/>')
    doc.add(arrow_head(px0, py1 - 12, 0, -1, 7.5))
    doc.add(f'<text class="lbl" x="{fmt(0.5*(px0+px1))}" y="{fmt(py0 + 44)}" text-anchor="middle">时间 t (ns)</text>')
    doc.add(
        f'<text class="lbl" x="48" y="{fmt(0.5*(py0+py1))}" text-anchor="middle" '
        f'transform="rotate(-90 48 {fmt(0.5*(py0+py1))})">归一化包络幅值 / Ω₀ (无量纲)</text>'
    )

    # Key feature markers: I peak (8, 1.0), Q extrema (6, +0.241) and (10, -0.241)
    doc.add(f'<line class="guide" x1="{fmt(gx(t0))}" y1="{fmt(gy(1.0))}" x2="{fmt(gx(t0))}" y2="{fmt(py0)}"/>')
    doc.add(f'<circle class="c1-fill" cx="{fmt(gx(t0))}" cy="{fmt(gy(1.0))}" r="5"/>')
    doc.add(f'<text class="smb c1-txt" x="{fmt(gx(t0) + 10)}" y="{fmt(gy(1.0) - 9)}">I{sub("max")} = Ω₀ (t₀ = 8 ns)</text>')

    xq1, yq1 = gx(t0 - sigma), gy(q_peak_exact)
    xq2, yq2 = gx(t0 + sigma), gy(-q_peak_exact)
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(xq1, yq1, 6.0)}"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(xq2, yq2, 6.0)}"/>')
    doc.add(f'<line class="c2" stroke-width="1.2" x1="{fmt(xq1 - 6)}" y1="{fmt(yq1 - 2)}" x2="{fmt(gx(3.4))}" y2="{fmt(gy(0.36))}"/>')
    doc.add(f'<text class="smb c2-txt" x="{fmt(gx(3.3))}" y="{fmt(gy(0.37))}" text-anchor="end">+{q_peak_exact:.3f} Ω₀</text>')
    doc.add(f'<text class="smb c2-txt" x="{fmt(xq2 + 10)}" y="{fmt(yq2 + 14)}">−{q_peak_exact:.3f} Ω₀</text>')

    # Legend above plot
    doc.add('<line class="c1" stroke-width="2.6" x1="56" y1="154" x2="86" y2="154"/>')
    doc.add('<text class="sm" x="92" y="158">同相 I(t)（高斯）</text>')
    doc.add('<line class="c2" stroke-width="2.4" stroke-dasharray="7 4" x1="226" y1="154" x2="256" y2="154"/>')
    doc.add('<text class="sm" x="262" y="158">正交 Q(t) = −(β/α) İ(t)</text>')

    # Bottom parameters box
    doc.add('<rect class="pill" x="44" y="502" width="424" height="36" rx="8"/>')
    doc.add(
        '<text class="sm" x="256" y="524" text-anchor="middle">'
        'α/2π = −200 MHz，β = 1；极值在 t₀ ± σ = 6、10 ns，压低 |1⟩→|2⟩ 泄漏'
        '</text>'
    )

    # --- Right Panel: 3 Dynamic Decoupling Pulse Sequences ---
    tx0, tx1 = 556.0, 892.0  # free evolution window [0, T] (width = 336 px)
    t_span = tx1 - tx0
    meas_x = 924.0

    # Vertical dashed alignment guides for t = 0, T/2, T (stop cleanly at CPMG axis y=456)
    for frac, tlbl in [(0.0, "0"), (0.5, "T/2"), (1.0, "T")]:
        xg = tx0 + frac * t_span
        doc.add(f'<line class="guide" x1="{fmt(xg)}" y1="170" x2="{fmt(xg)}" y2="456"/>')
        doc.add(f'<line class="axis" stroke-width="1.3" x1="{fmt(xg)}" y1="478" x2="{fmt(xg)}" y2="484"/>')
        doc.add(f'<text class="smb" x="{fmt(xg)}" y="497" text-anchor="middle">{tlbl}</text>')

    def draw_pi2(cx_p: float, base_y: float, lbl: str = "π/2") -> None:
        pw, ph = 20.0, 28.0
        doc.add(f'<rect class="c1-soft" stroke-width="1.8" x="{fmt(cx_p - pw/2)}" y="{fmt(base_y - ph)}" width="{fmt(pw)}" height="{fmt(ph)}" rx="4"/>')
        doc.add(f'<text class="sm c1-txt" x="{fmt(cx_p)}" y="{fmt(base_y - ph - 6)}" text-anchor="middle">{lbl}</text>')

    def draw_pi(cx_p: float, base_y: float, lbl: str = "π") -> None:
        pw, ph = 22.0, 46.0
        doc.add(f'<rect class="c2-soft" stroke-width="2" x="{fmt(cx_p - pw/2)}" y="{fmt(base_y - ph)}" width="{fmt(pw)}" height="{fmt(ph)}" rx="4"/>')
        doc.add(f'<rect fill="url(#hatch-red)" x="{fmt(cx_p - pw/2)}" y="{fmt(base_y - ph)}" width="{fmt(pw)}" height="{fmt(ph)}" rx="4"/>')
        doc.add(f'<text class="smb c2-txt" x="{fmt(cx_p)}" y="{fmt(base_y - ph - 6)}" text-anchor="middle">{lbl}</text>')

    def draw_meas(cx_m: float, base_y: float) -> None:
        mw, mh = 28.0, 28.0
        doc.add(f'<rect class="c3-soft" stroke-width="1.8" x="{fmt(cx_m - mw/2)}" y="{fmt(base_y - mh)}" width="{fmt(mw)}" height="{fmt(mh)}" rx="5"/>')
        doc.add(f'<text class="smb c3-txt" x="{fmt(cx_m)}" y="{fmt(base_y - 9)}" text-anchor="middle">测</text>')

    # Row 1: Ramsey (Free Evolution)
    r1y = 226.0
    doc.add('<text class="smb" x="518" y="164">① 自由演化 Ramsey（受准静态失谐退相干，尺度 T₂*）</text>')
    doc.add(f'<line class="axis" x1="522" y1="{fmt(r1y)}" x2="948" y2="{fmt(r1y)}"/>')
    draw_pi2(tx0, r1y, "π/2")
    draw_pi2(tx1, r1y, "π/2")
    draw_meas(meas_x, r1y)
    # Free evolution bar
    doc.add(f'<line class="c1" stroke-width="1.5" x1="{fmt(tx0 + 16)}" y1="{fmt(r1y - 12)}" x2="{fmt(tx1 - 16)}" y2="{fmt(r1y - 12)}"/>')
    doc.add(f'<text class="sm" x="{fmt(0.5*(tx0+tx1))}" y="{fmt(r1y - 18)}" text-anchor="middle">自由等待 T（相位累积 +δT）</text>')

    # Row 2: Hahn Spin Echo (T/2 - pi - T/2)
    r2y = 338.0
    doc.add(f'<text class="smb" x="518" y="266">② Hahn 自旋回波（T/2 − π − T/2，抵消静态失谐，T{sub("2,echo")} &gt; T₂*）</text>')
    doc.add(f'<line class="axis" x1="522" y1="{fmt(r2y)}" x2="948" y2="{fmt(r2y)}"/>')
    draw_pi2(tx0, r2y, "π/2")
    draw_pi(tx0 + 0.5 * t_span, r2y, "π")
    draw_pi2(tx1, r2y, "π/2")
    draw_meas(meas_x, r2y)
    doc.add(f'<text class="sm c1-txt" x="{fmt(tx0 + 0.25*t_span)}" y="{fmt(r2y - 12)}" text-anchor="middle">T/2（+δT/2）</text>')
    doc.add(f'<text class="sm c3-txt" x="{fmt(tx0 + 0.75*t_span)}" y="{fmt(r2y - 12)}" text-anchor="middle">T/2（−δT/2，抵消）</text>')

    # Row 3: CPMG-4 Sequence (tau = T/4, initial & final pi/2_X)
    r3y = 456.0
    doc.add(f'<text class="smb" x="518" y="382">③ CPMG-4（τ = T/4，π{sub("Y")} 重聚焦，滤除更宽低频噪声）</text>')
    doc.add(f'<line class="axis" x1="522" y1="{fmt(r3y)}" x2="948" y2="{fmt(r3y)}"/>')
    draw_pi2(tx0, r3y, 'π/2<tspan dy="3" font-size="9.5">X</tspan>')
    for k_f in [1 / 8, 3 / 8, 5 / 8, 7 / 8]:
        draw_pi(tx0 + k_f * t_span, r3y, 'π<tspan dy="3" font-size="9.5">Y</tspan>')
    draw_pi2(tx1, r3y, 'π/2<tspan dy="3" font-size="9.5">X</tspan>')
    draw_meas(meas_x, r3y)

    # Interval labels beneath CPMG line
    for (f_mid, lbl_i) in [(1 / 16, "τ/2"), (2 / 8, "τ"), (4 / 8, "τ"), (6 / 8, "τ"), (15 / 16, "τ/2")]:
        doc.add(f'<text class="sm" x="{fmt(tx0 + f_mid * t_span)}" y="{fmt(r3y + 17)}" text-anchor="middle">{lbl_i}</text>')

    # Bottom summary legend for right panel
    doc.add('<rect class="note" x="516" y="504" width="440" height="36" rx="8"/>')
    doc.add(
        '<text class="sm" x="736" y="526" text-anchor="middle">'
        '时间从左向右；蓝矮框 π/2，红斜纹高框 π（重聚焦），绿框为测量'
        '</text>'
    )

    return doc.render(), {"q_peak_ratio": q_peak_exact, "sigma_ns": sigma, "t0_ns": t0}


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
    assert len(text_nodes) >= 8, f"{filename}: too few text elements"
    for el in text_nodes:
        x = float(el.attrib["x"])
        y = float(el.attrib["y"])
        assert MARGIN <= x <= W - MARGIN, f"{filename}: text x={x} violates margin ({el.text!r})"
        assert MARGIN <= y <= H - MARGIN, f"{filename}: text y={y} violates margin ({el.text!r})"

    return {"text_count": len(text_nodes), "bytes": len(svg_text.encode("utf-8"))}


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    builders = [
        ("v2-q3-anharmonic-rabi.svg", build_fig1_anharmonic_rabi),
        ("v2-10-surface-lattice-surgery.svg", build_fig2_surface_lattice_surgery),
        ("v2-12-bb84-plob.svg", build_fig3_bb84_plob),
        ("v2-13-helstrom-entropy.svg", build_fig4_helstrom_entropy),
        ("v2-14-drag-dd-pulses.svg", build_fig5_drag_dd_pulses),
    ]

    for fname, fn in builders:
        svg_text, metrics = fn()
        check = verify_svg_xml(svg_text, fname)
        out_path = ASSETS_DIR / fname
        out_path.write_text(svg_text, encoding="utf-8")
        print(f"[OK] {fname}: {check['bytes']} bytes, {check['text_count']} text labels | metrics={metrics}")


if __name__ == "__main__":
    main()
