#!/usr/bin/env python3
"""Rebuild 7 legacy C2 scientific SVG figures (Part 1) with light/dark adaptive
styling, full Chinese typography, pure <text> labels, and exact data/formula
verification using Python 3 standard library only.

Outputs in place to handbook/assets/ (preserving original filenames):
  1. round70-foundations-tomography.svg  (Ch 02: finite-count tomography & Bloch projection)
  2. round70-amplitude-aliasing.svg      (Ch 07: single-depth Grover amplitude aliasing)
  3. round70-systems-cutoff.svg          (Ch 12: two-link memory cutoff rate-quality trade-off)
  4. round70-chain-strength.svg          (Ch 17: annealing chain strength & dynamic range)
  5. round71-foundations-eraser.svg      (Q1:    quantum eraser conditional fringes vs marginal)
  6. round71-systems-spectrum.svg        (Q3:    weak rectangular pulse spectral nulls vs exact Rabi)
  7. round71-barrier-transmission.svg    (Q4:    1D rectangular barrier 3-region transmission)

Run:
  python3 codes/practice/upgrade_legacy_svgs_part1.py

Dependencies:
  Python 3 standard library only (cmath, json, math, pathlib, xml.etree.ElementTree, xml.sax.saxutils).
  Deterministic numerical calculations verified against repository JSON fixtures (no RNG, no network).
"""

from __future__ import annotations

import cmath
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT / "handbook" / "assets"
W, H = 1000, 580
MARGIN = 30
TOL = 1e-10


COMMON_CSS = """
:root{color-scheme:light dark}
text{font-family:system-ui,-apple-system,'PingFang SC','Microsoft YaHei',sans-serif}
.bg{fill:#f8fafc}
.panel{fill:#ffffff;stroke:#cbd5e1;stroke-width:1.4}
.subpanel{fill:#f4f8fb;stroke:#d1dde8;stroke-width:1.2}
.phead{fill:#eef4f8}
.title{font-size:20px;font-weight:700;fill:#13263a}
.subtitle{font-size:13px;font-weight:400;fill:#3e566d}
.sec{font-size:14.5px;font-weight:700;fill:#13263a}
.lbl{font-size:13px;font-weight:500;fill:#19324d}
.lblb{font-size:13px;font-weight:700;fill:#13263a}
.sm{font-size:12px;font-weight:400;fill:#3e566d}
.smb{font-size:12px;font-weight:600;fill:#19324d}
.xs{font-size:11px;font-weight:500;fill:#3e566d}
.xsb{font-size:11px;font-weight:700;fill:#19324d}
.axis{stroke:#19324d;stroke-width:1.7;fill:none}
.axis-fill{fill:#19324d}
.grid{stroke:#dce5ee;stroke-width:1;fill:none}
.guide{stroke:#7c93a8;stroke-width:1.25;stroke-dasharray:5 4;fill:none}
.unit-circle{stroke:#5b7790;stroke-width:1.5;stroke-dasharray:6 5;fill:none}
.bloch-disk{fill:#dff4ff;fill-opacity:.38;stroke:#1b6ca8;stroke-width:2.2}
.c1{stroke:#1b6ca8;fill:none}
.c1-fill{fill:#1b6ca8}
.c1-txt{fill:#145282}
.c1-soft{fill:#e1f1fb;stroke:#1b6ca8;stroke-width:1.4}
.c2{stroke:#c74b34;fill:none}
.c2-fill{fill:#c74b34}
.c2-txt{fill:#a63824}
.c2-soft{fill:#fce8e3;stroke:#c74b34;stroke-width:1.4}
.c3{stroke:#1e7a5c;fill:none}
.c3-fill{fill:#1e7a5c}
.c3-txt{fill:#155e46}
.c3-soft{fill:#e2f5ee;stroke:#1e7a5c;stroke-width:1.4}
.c4{stroke:#b57614;fill:none}
.c4-fill{fill:#b57614}
.c4-txt{fill:#8a5609}
.c4-soft{fill:#fff4d8;stroke:#b57614;stroke-width:1.4}
.note{fill:#fff8e6;stroke:#c98d24;stroke-width:1.3}
.pill{fill:#f3f7fa;stroke:#9cb1c4;stroke-width:1.2}
.pill-bg{fill:#ffffff;fill-opacity:.94;stroke:#9cb1c4;stroke-width:1.1}
.node-bg{fill:#ffffff}
.area1{fill:#1b6ca8;fill-opacity:.13}
.area2{fill:#c74b34;fill-opacity:.12}
.area3{fill:#1e7a5c;fill-opacity:.13}
.forbid{fill:#c74b34;fill-opacity:.09}
.bar-bg{fill:#e2e8f0}
.hatch-stroke1{stroke:#1b6ca8;stroke-width:1.1;stroke-opacity:.42}
.hatch-stroke2{stroke:#c74b34;stroke-width:1.1;stroke-opacity:.45}
.hatch-stroke3{stroke:#1e7a5c;stroke-width:1.1;stroke-opacity:.42}
@media(prefers-color-scheme:dark){
  .bg{fill:#0f1720}
  .panel{fill:#16222e;stroke:#354c61}
  .subpanel{fill:#1b2a38;stroke:#3b5369}
  .phead{fill:#1c2d3d}
  .title,.sec,.lblb{fill:#eef6ff}
  .subtitle,.sm,.xs{fill:#b7cde0}
  .lbl,.smb,.xsb{fill:#d7e7f5}
  .axis{stroke:#cde0f2}
  .axis-fill{fill:#cde0f2}
  .grid{stroke:#293e52}
  .guide,.unit-circle{stroke:#738fa8}
  .bloch-disk{fill:#164968;fill-opacity:.40;stroke:#6bc2f5}
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
  .node-bg{fill:#16222e}
  .area1{fill:#6bc2f5;fill-opacity:.16}
  .area2{fill:#f28872;fill-opacity:.15}
  .area3{fill:#5dd1a8;fill-opacity:.16}
  .forbid{fill:#f28872;fill-opacity:.12}
  .bar-bg{fill:#273a4c}
  .hatch-stroke1{stroke:#6bc2f5;stroke-opacity:.48}
  .hatch-stroke2{stroke:#f28872;stroke-opacity:.52}
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


def square_pts(cx: float, cy: float, r: float) -> str:
    return pts_str([(cx - r, cy - r), (cx + r, cy - r), (cx + r, cy + r), (cx - r, cy + r)])


def triangle_pts(cx: float, cy: float, r: float) -> str:
    return pts_str([(cx, cy - r * 1.15), (cx + r, cy + r * 0.8), (cx - r, cy + r * 0.8)])


def arrow_head(x: float, y: float, dx: float, dy: float, size: float = 7.5, cls: str = "axis-fill") -> str:
    norm = math.hypot(dx, dy)
    assert norm > 1e-12
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
        ]
        self.body: list[str] = []

    def add(self, snippet: str) -> None:
        self.body.append(snippet)

    def add_header(self, title_text: str, subtitle_text: str, *, raw_sub: bool = False) -> None:
        self.add(f'<rect class="bg" width="{self.w}" height="{self.h}" rx="20"/>')
        self.add(f'<text class="title" x="34" y="52">{escape(title_text)}</text>')
        s_out = subtitle_text if raw_sub else escape(subtitle_text)
        self.add(f'<text class="subtitle" x="34" y="76">{s_out}</text>')

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


def load_json(rel_path: str) -> dict:
    return json.loads((ROOT / rel_path).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Figure 1 (Ch 02): Finite-count tomography & radial PSD Bloch projection
# ---------------------------------------------------------------------------
def build_fig1_tomography() -> tuple[str, dict[str, float]]:
    # Fixed synthetic counts from codes/foundations/diagnostic_lab.py case02
    counts = {"X": (9, 1), "Y": (9, 1), "Z": (5, 5)}
    rx = (counts["X"][0] - counts["X"][1]) / sum(counts["X"])
    ry = (counts["Y"][0] - counts["Y"][1]) / sum(counts["Y"])
    rz = (counts["Z"][0] - counts["Z"][1]) / sum(counts["Z"])
    r_len = math.sqrt(rx * rx + ry * ry + rz * rz)
    eig_hi = 0.5 * (1.0 + r_len)
    eig_lo = 0.5 * (1.0 - r_len)
    px_u, py_u = rx / r_len, ry / r_len

    assert abs(rx - 0.8) < TOL and abs(ry - 0.8) < TOL and abs(rz) < TOL
    assert abs(r_len - math.sqrt(1.28)) < TOL
    assert eig_lo < 0.0 and abs(eig_lo - (0.5 - math.sqrt(0.32))) < TOL
    assert abs(px_u - 1.0 / math.sqrt(2.0)) < TOL and abs(py_u - 1.0 / math.sqrt(2.0)) < TOL

    doc = SvgDoc(
        title="有限计数线性层析落在 Bloch 单位圆外与径向正半定投影",
        desc=(
            "左图以 1:1 等比例绘制 r_z = 0 赤道截面单位圆盘：三基独立 10 次测量计数（X 9/1、Y 9/1、Z 5/5）"
            "给出落在球外的原始线性估计（方形标记，(0.8, 0.8)，半径 1.13137，负本征值 −0.06569）；"
            "径向投影将其拉回物理边界圆周（圆形标记，(0.7071, 0.7071)，本征值 1 与 0），但不增加新的测量证据。"
        ),
    )
    doc.add_header(
        "单比特有限计数层析：球外线性重构与径向正半定投影",
        f"r{sub('z')} = 0 赤道截面（1:1 等比例，无量纲 Bloch 坐标）· 三基各独立 10 次测量：X 9/1、Y 9/1、Z 5/5",
        raw_sub=True,
    )
    doc.add_panel(28, 94, 478, 456, f"Bloch 球赤道截面（r{sub('z')} = 0，1:1 等比例）", raw_heading=True)
    doc.add_panel(522, 94, 450, 456, "三步诊断：从有限计数到合法物理密度矩阵")

    # --- Left Panel: Equal-aspect Bloch equatorial disk ---
    cx, cy, r_px = 250.0, 326.0, 134.0

    def pt(x_v: float, y_v: float) -> tuple[float, float]:
        return cx + x_v * r_px, cy - y_v * r_px

    # Subtle gridlines inside [-1, 1]^2
    for gv in (-1.0, -0.5, 0.5, 1.0):
        gx_v, _ = pt(gv, 0.0)
        _, gy_v = pt(0.0, gv)
        doc.add(f'<line class="grid" x1="{fmt(gx_v)}" y1="{fmt(cy - r_px)}" x2="{fmt(gx_v)}" y2="{fmt(cy + r_px)}"/>')
        doc.add(f'<line class="grid" x1="{fmt(cx - r_px)}" y1="{fmt(gy_v)}" x2="{fmt(cx + r_px)}" y2="{fmt(gy_v)}"/>')

    # Physical Bloch disk & r=0.5 dashed reference circle
    doc.add(f'<circle class="bloch-disk" cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r_px)}"/>')
    doc.add(f'<circle class="unit-circle" cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(0.5 * r_px)}"/>')

    # Axes
    x_lo, x_hi = cx - r_px - 26.0, cx + r_px + 34.0
    y_lo, y_hi = cy + r_px + 20.0, cy - r_px - 24.0
    doc.add(f'<line class="axis" x1="{fmt(x_lo)}" y1="{fmt(cy)}" x2="{fmt(x_hi)}" y2="{fmt(cy)}"/>')
    doc.add(arrow_head(x_hi + 2, cy, 1, 0))
    doc.add(f'<line class="axis" x1="{fmt(cx)}" y1="{fmt(y_lo)}" x2="{fmt(cx)}" y2="{fmt(y_hi)}"/>')
    doc.add(arrow_head(cx, y_hi - 2, 0, -1))

    # Ticks and axis titles (nudged clear of unit and r=0.5 circle arcs)
    for v_t, s_t, dx_x, dy_y in (
        (-1.0, "−1", -12.0, 14.0),
        (-0.5, "−0.5", -14.0, 12.0),
        (0.5, "0.5", 13.0, -7.0),
        (1.0, "1", 10.0, -7.0),
    ):
        xt, _ = pt(v_t, 0.0)
        doc.add(f'<line class="axis" stroke-width="1.3" x1="{fmt(xt)}" y1="{fmt(cy - 4)}" x2="{fmt(xt)}" y2="{fmt(cy + 4)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xt + dx_x)}" y="{fmt(cy + 18)}" text-anchor="middle">{s_t}</text>')
        _, yt = pt(0.0, v_t)
        doc.add(f'<line class="axis" stroke-width="1.3" x1="{fmt(cx - 4)}" y1="{fmt(yt)}" x2="{fmt(cx + 4)}" y2="{fmt(yt)}"/>')
        doc.add(f'<text class="xs" x="{fmt(cx - 9)}" y="{fmt(yt + dy_y)}" text-anchor="end">{s_t}</text>')
    doc.add(f'<text class="xs" x="{fmt(cx - 9)}" y="{fmt(cy + 16)}" text-anchor="end">0</text>')
    doc.add(f'<text class="smb" x="{fmt(cx)}" y="{fmt(y_hi - 11)}" text-anchor="middle">r{sub("y")}（无量纲）</text>')
    doc.add(f'<text class="smb" x="456" y="{fmt(cy - 10)}" text-anchor="middle">r{sub("x")}（无量纲）</text>')

    # Vectors from origin to projected point and raw point
    raw_pt = pt(rx, ry)
    proj_pt = pt(px_u, py_u)
    doc.add(f'<line class="c2" stroke-width="2.2" stroke-dasharray="6 4" x1="{fmt(proj_pt[0])}" y1="{fmt(proj_pt[1])}" x2="{fmt(raw_pt[0])}" y2="{fmt(raw_pt[1])}"/>')
    doc.add(f'<line class="c3" stroke-width="3.0" x1="{fmt(cx)}" y1="{fmt(cy)}" x2="{fmt(proj_pt[0])}" y2="{fmt(proj_pt[1])}"/>')

    # Markers: square for raw outside-ball estimate, circle for projected boundary state
    doc.add(f'<rect class="c2-fill" x="{fmt(raw_pt[0] - 5.5)}" y="{fmt(raw_pt[1] - 5.5)}" width="11" height="11" rx="1.5"/>')
    doc.add(f'<circle class="node-bg c3" stroke-width="3.0" cx="{fmt(proj_pt[0])}" cy="{fmt(proj_pt[1])}" r="5.5"/>')

    # Clean callouts (non-overlapping, strictly inside panel)
    doc.add('<rect class="c2-soft" x="358" y="144" width="136" height="42" rx="8"/>')
    doc.add('<text class="xsb c2-txt" x="426" y="162" text-anchor="middle">■ 原始估计 (0.8, 0.8)</text>')
    doc.add('<text class="xs c2-txt" x="426" y="178" text-anchor="middle">|r̂| ≈ 1.131 &gt; 1（球外）</text>')
    doc.add(f'<line class="c2" stroke-width="1.3" x1="{fmt(raw_pt[0] + 5)}" y1="{fmt(raw_pt[1] - 5)}" x2="394" y2="186"/>')

    doc.add('<rect class="c3-soft" x="352" y="246" width="144" height="42" rx="8"/>')
    doc.add('<text class="xsb c3-txt" x="424" y="264" text-anchor="middle">○ 径向投影 (0.707, 0.707)</text>')
    doc.add('<text class="xs c3-txt" x="424" y="280" text-anchor="middle">|r*| = 1（纯态圆周）</text>')
    doc.add(f'<line class="c3" stroke-width="1.3" x1="{fmt(proj_pt[0] + 6)}" y1="{fmt(proj_pt[1] + 2)}" x2="372" y2="246"/>')

    # Physical disk tag in open lower-left interior + bottom summary pill
    doc.add('<rect class="pill-bg" x="44" y="148" width="128" height="36" rx="8"/>')
    doc.add(f'<text class="xsb c1-txt" x="108" y="164" text-anchor="middle">物理圆盘可行域</text>')
    doc.add(f'<text class="xs c1-txt" x="108" y="178" text-anchor="middle">r{sub("x")}² + r{sub("y")}² ≤ 1</text>')

    doc.add('<rect class="pill" x="44" y="502" width="446" height="34" rx="8"/>')
    doc.add(
        f'<text class="sm" x="267" y="523" text-anchor="middle">'
        f'方形 = 球外线性估计，圆形 = 径向投影估计；投影沿半径拉回圆周'
        f'</text>'
    )

    # --- Right Panel: 3-step diagnostic cards ---
    # Card 1: Raw counts & mini probability bars
    doc.add('<rect class="c1-soft" x="538" y="144" width="418" height="118" rx="10"/>')
    doc.add('<text class="smb c1-txt" x="552" y="165">① 保留三组原始计数（每基各独立 10 次测量）</text>')
    bar_rows = [
        ("X 基", 9, 1, rx, "c1-fill"),
        ("Y 基", 9, 1, ry, "c1-fill"),
        ("Z 基", 5, 5, rz, "c3-fill"),
    ]
    for idx, (bname, n_p, n_m, r_est, bcls) in enumerate(bar_rows):
        yr = 192 + idx * 28
        doc.add(f'<text class="sm" x="552" y="{yr}">{bname}：{n_p} 正 / {n_m} 负</text>')
        bx_bar, bw_bar = 668.0, 152.0
        doc.add(f'<rect class="bar-bg" x="{fmt(bx_bar)}" y="{yr - 11}" width="{fmt(bw_bar)}" height="12" rx="4"/>')
        doc.add(f'<rect class="{bcls}" x="{fmt(bx_bar)}" y="{yr - 11}" width="{fmt(bw_bar * n_p / 10.0)}" height="12" rx="4"/>')
        sign_s = "+" if r_est > 0 else " "
        sub_ch = bname[0].lower()
        doc.add(f'<text class="smb" x="942" y="{yr}" text-anchor="end">r̂{sub(sub_ch)} = {sign_s}{r_est:.2f}</text>')

    # Card 2: Full matrix eigenvalue check
    doc.add('<rect class="c2-soft" x="538" y="272" width="418" height="94" rx="10"/>')
    doc.add('<text class="smb c2-txt" x="552" y="293">② 检验整张密度矩阵正半定性（不可只看对角元）</text>')
    doc.add('<text class="sm" x="552" y="316">线性重构 ρ̂ = ½(I + 0.8X + 0.8Y)，半径 |r̂| = √1.28 ≈ 1.13137</text>')
    doc.add(f'<text class="smb c2-txt" x="552" y="337">本征值 λ{sub("+")} ≈ 1.06569，λ{sub("−")} ≈ −0.06569 &lt; 0（非物理）</text>')
    doc.add('<text class="xs" x="552" y="356">有限样本统计涨落即可推出球外，不能把负本征值误判为设备故障</text>')

    # Card 3: Radial Euclidean projection
    doc.add('<rect class="c3-soft" x="538" y="376" width="418" height="84" rx="10"/>')
    doc.add('<text class="smb c3-txt" x="552" y="397">③ 径向欧氏投影（单比特 Frobenius 最近合法态）</text>')
    doc.add('<text class="sm" x="552" y="420">r* = r̂ / |r̂| = (1/√2, 1/√2, 0) ≈ (0.7071, 0.7071, 0)</text>')
    doc.add('<text class="smb c3-txt" x="552" y="443">投影后半径归 1，本征值恢复为 1 与 0（满足 ρ* ≽ 0）</text>')

    # Card 4: Methodological boundary
    doc.add('<rect class="note" x="538" y="470" width="418" height="66" rx="10"/>')
    doc.add('<text class="smb c4-txt" x="552" y="490">方法边界提醒（必须声明所用的物理修正方式）</text>')
    doc.add('<text class="sm" x="552" y="510">投影仅将点估计拉回物理可行域，不增加新的测量证据，也不是置信区间；</text>')
    doc.add('<text class="sm" x="552" y="527">多比特高维层析应使用带物理约束的最大似然估计（MLE）。</text>')

    return doc.render(), {"raw_radius": round(r_len, 5), "eig_min": round(eig_lo, 5)}


# ---------------------------------------------------------------------------
# Figure 2 (Ch 07): Single-depth Grover amplitude aliasing & disambiguation
# ---------------------------------------------------------------------------
def build_fig2_aliasing() -> tuple[str, dict[str, float]]:
    data = load_json("codes/algorithms/round70-results.json")["07"]

    def amp_prob(a: float, k: int) -> float:
        return min(1.0, max(0.0, math.sin((2 * k + 1) * math.asin(math.sqrt(a))) ** 2))

    def log_lik(a: float) -> float:
        total = 0.0
        for row in data["synthetic_counts"]:
            h, n = row["successes"], row["shots"]
            p = amp_prob(a, row["k"])
            if p <= 0.0:
                if h > 0:
                    return -math.inf
            elif p >= 1.0:
                if h < n:
                    return -math.inf
            else:
                total += h * math.log(p) + (n - h) * math.log1p(-p)
        return total

    assert abs(amp_prob(0.25, 1) - 1.0) < TOL
    assert abs(amp_prob(1.0, 1) - 1.0) < TOL
    assert abs(amp_prob(0.75, 1)) < TOL
    ll_opt = log_lik(0.25)
    assert abs(ll_opt - data["log_likelihood_a025"]) < 1e-9
    assert log_lik(1.0) == -math.inf
    assert data["A_and_inverse_calls"] == 400 and data["good_reflections"] == 100

    doc = SvgDoc(
        title="振幅估计的角度混叠：单一 Grover 深度无法唯一辨识初始概率",
        desc=(
            "左图在初始好态概率 a ∈ [0, 1] 上绘制 k = 0 直接采样（实线 p₀ = a）与 k = 1 一轮 Grover 放大"
            "（虚线 p₁ = a(3−4a)²），两个方形标记标出 a = 1/4 与 a = 1 同达 p₁ = 1 的混叠重合点。"
            "右图展示联合 k = 0（25/100）与 k = 1（100/100）的似然消歧尖峰（a = 0.25 唯一最大，a = 1 被排除）及 400 次查询账本。"
        ),
    )
    doc.add_header(
        "振幅估计的角度混叠：单一 Grover 深度无法唯一辨识初始概率",
        f"左：k = 0 直接采样（实线）与 k = 1 一轮放大（虚线）精确曲线；右：多深度联合似然消歧与完整查询账本",
        raw_sub=True,
    )
    doc.add_panel(28, 94, 578, 456, f"测量成功概率 p{sub('k')}(a) 与混叠重合点（精确公式）", raw_heading=True)
    doc.add_panel(622, 94, 350, 456, "多深度联合似然消歧与查询账本")

    # --- Left Panel: p0(a) vs p1(a) ---
    px0, px1 = 94.0, 582.0
    py_top, py_bot = 178.0, 458.0
    a_max, p_max = 1.03, 1.16

    def gx(a: float) -> float:
        return px0 + (a / a_max) * (px1 - px0)

    def gy(p: float) -> float:
        return py_bot - (p / p_max) * (py_bot - py_top)

    # Legend above plot frame
    doc.add('<line class="c1" stroke-width="2.6" x1="48" y1="154" x2="76" y2="154"/>')
    doc.add('<circle class="c1-fill" cx="62" cy="154" r="3.6"/>')
    doc.add('<text class="sm" x="82" y="158">k = 0：直接采样 p₀(a) = a</text>')

    doc.add('<line class="c2" stroke-width="2.5" stroke-dasharray="8 4" x1="274" y1="154" x2="302" y2="154"/>')
    doc.add(f'<rect class="c2-fill" x="284" y="150" width="8" height="8" rx="1"/>')
    doc.add('<text class="sm" x="308" y="158">k = 1：一轮放大 p₁(a) = a(3−4a)²</text>')

    # Grid & ticks
    for pv in (0.0, 0.25, 0.50, 0.75, 1.00):
        yg = gy(pv)
        cls_g = "guide" if pv == 1.0 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(px0)}" y1="{fmt(yg)}" x2="{fmt(px1)}" y2="{fmt(yg)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(px0 - 5)}" y1="{fmt(yg)}" x2="{fmt(px0)}" y2="{fmt(yg)}"/>')
        doc.add(f'<text class="sm" x="{fmt(px0 - 9)}" y="{fmt(yg + 4)}" text-anchor="end">{pv:.2f}</text>')

    for av, albl in ((0.0, "0"), (0.25, "0.25"), (0.50, "0.50"), (0.75, "0.75"), (1.0, "1.00")):
        xg = gx(av)
        cls_g = "guide" if av in (0.25, 0.75, 1.0) else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(xg)}" y1="{fmt(py_top)}" x2="{fmt(xg)}" y2="{fmt(py_bot)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(xg)}" y1="{fmt(py_bot)}" x2="{fmt(xg)}" y2="{fmt(py_bot + 5)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xg)}" y="{fmt(py_bot + 19)}" text-anchor="middle">{albl}</text>')

    # Exact curves (181 points)
    n_s = 181
    pts0 = [(gx(i / (n_s - 1)), gy(i / (n_s - 1))) for i in range(n_s)]
    pts1 = [(gx(i / (n_s - 1)), gy(amp_prob(i / (n_s - 1), 1))) for i in range(n_s)]
    doc.add(f'<path class="c1" stroke-width="2.6" d="{path_from_points(pts0)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.6" stroke-dasharray="8 4" d="{path_from_points(pts1)}"/>')

    # Aliasing square markers at a=0.25 and a=1.0 (both p1=1)
    x_a25, y_p1 = gx(0.25), gy(1.0)
    x_a10 = gx(1.0)
    doc.add(f'<line class="c2" stroke-width="1.5" stroke-dasharray="4 3" x1="{fmt(x_a25)}" y1="{fmt(y_p1)}" x2="{fmt(x_a10)}" y2="{fmt(y_p1)}"/>')
    doc.add(f'<rect class="c2-fill" x="{fmt(x_a25 - 5.5)}" y="{fmt(y_p1 - 5.5)}" width="11" height="11" rx="1.5"/>')
    doc.add(f'<rect class="c2-fill" x="{fmt(x_a10 - 5.5)}" y="{fmt(y_p1 - 5.5)}" width="11" height="11" rx="1.5"/>')

    # Aliasing callout strictly above p=1 line (y=176..202 vs y_p1=216.9)
    doc.add('<rect class="c2-soft" x="234" y="176" width="294" height="24" rx="10"/>')
    doc.add('<text class="xsb c2-txt" x="381" y="192" text-anchor="middle">混叠重合：a = 1/4 与 a = 1 均给出 p₁ = 1</text>')
    doc.add(f'<line class="c2" stroke-width="1.2" x1="254" y1="200" x2="{fmt(x_a25 + 3)}" y2="{fmt(y_p1 - 7)}"/>')
    doc.add(f'<line class="c2" stroke-width="1.2" x1="510" y1="200" x2="{fmt(x_a10 - 3)}" y2="{fmt(y_p1 - 7)}"/>')

    # Direct sampling comparison marker at a=0.25 (p0 = 0.25)
    doc.add(f'<circle class="c1-fill" cx="{fmt(x_a25)}" cy="{fmt(gy(0.25))}" r="4.8"/>')
    doc.add('<rect class="c1-soft" x="108" y="408" width="144" height="36" rx="7"/>')
    doc.add('<text class="xsb c1-txt" x="180" y="423" text-anchor="middle">k = 0 区分两者</text>')
    doc.add('<text class="xs c1-txt" x="180" y="438" text-anchor="middle">p₀(1/4)=0.25 ≠ p₀(1)=1</text>')
    doc.add(f'<line class="c1" stroke-width="1.2" x1="204" y1="408" x2="{fmt(x_a25 - 3)}" y2="{fmt(gy(0.25) + 6)}"/>')

    # Zero-crossing marker at a=0.75 (p1 = 0)
    x_a75, y_p0 = gx(0.75), gy(0.0)
    doc.add(f'<circle class="node-bg c2" stroke-width="2.4" cx="{fmt(x_a75)}" cy="{fmt(y_p0)}" r="4.8"/>')
    doc.add('<rect class="pill-bg" x="382" y="340" width="140" height="38" rx="7"/>')
    doc.add('<text class="xsb c2-txt" x="452" y="356" text-anchor="middle">过旋零点 a = 3/4</text>')
    doc.add('<text class="xs" x="452" y="371" text-anchor="middle">3θ = π ⇒ p₁ = 0</text>')
    doc.add(f'<line class="guide" x1="452" y1="378" x2="{fmt(x_a75)}" y2="{fmt(y_p0 - 6)}"/>')

    # Axes & labels
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px1 + 8)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(px1 + 10, py_bot, 1, 0))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(px0, py_top - 10, 0, -1))
    doc.add(f'<text class="lbl" x="{fmt(0.5 * (px0 + px1))}" y="497" text-anchor="middle">初始好态概率 a（无量纲）</text>')
    doc.add(
        f'<text class="lbl" x="46" y="{fmt(0.5 * (py_top + py_bot))}" text-anchor="middle" '
        f'transform="rotate(-90 46 {fmt(0.5 * (py_top + py_bot))})">测量成功概率 p{sub("k")}(a)（无量纲）</text>'
    )

    doc.add('<rect class="pill" x="44" y="510" width="546" height="28" rx="8"/>')
    doc.add('<text class="sm" x="317" y="528" text-anchor="middle">只测 k = 1 即使采样一亿次全成功，仍无法分辨 a = 1/4 与 a = 1（固有不可辨识性）</text>')

    # --- Right Panel: Disambiguation & Query Ledger ---
    # Box 1: Why aliasing happens
    doc.add('<rect class="c2-soft" x="638" y="144" width="318" height="84" rx="10"/>')
    doc.add('<text class="smb c2-txt" x="652" y="164">① 混叠根源：多对一角度折叠</text>')
    doc.add('<text class="sm" x="652" y="186">p₁(a) = sin²(3θ) = a(3 − 4a)²（θ = arcsin√a）</text>')
    doc.add('<text class="sm" x="652" y="206">a = 1/4 (θ = π/6) 与 a = 1 (θ = π/2) 同映至 1</text>')
    doc.add('<text class="xs" x="652" y="222">与统计噪声无关，须联合多组深度 k 消歧</text>')

    # Box 2: Joint normalized likelihood mini-plot
    doc.add('<rect class="subpanel" x="638" y="238" width="318" height="184" rx="10"/>')
    doc.add('<text class="smb" x="652" y="258">② 联合似然消歧（k=0: 25/100, k=1: 100/100）</text>')
    mx0, mx1 = 682.0, 938.0
    my_top, my_bot = 278.0, 372.0

    def lx(a: float) -> float:
        return mx0 + a * (mx1 - mx0)

    def ly(rel: float) -> float:
        return my_bot - rel * (my_bot - my_top)

    for av, al in ((0.0, "0"), (0.25, "0.25"), (0.5, "0.5"), (0.75, "0.75"), (1.0, "1")):
        x_m = lx(av)
        doc.add(f'<line class="grid" x1="{fmt(x_m)}" y1="{fmt(my_top)}" x2="{fmt(x_m)}" y2="{fmt(my_bot)}"/>')
        doc.add(f'<text class="xs" x="{fmt(x_m)}" y="{fmt(my_bot + 14)}" text-anchor="middle">{al}</text>')
    doc.add(f'<line class="grid" x1="{fmt(mx0)}" y1="{fmt(my_top)}" x2="{fmt(mx1)}" y2="{fmt(my_top)}"/>')
    doc.add(f'<text class="xs" x="{fmt(mx0 - 6)}" y="{fmt(my_top + 4)}" text-anchor="end">1</text>')
    doc.add(f'<text class="xs" x="{fmt(mx0 - 6)}" y="{fmt(my_bot + 4)}" text-anchor="end">0</text>')

    # Sample normalized likelihood densely around a=0.25
    a_grid = sorted(set(
        [i / 200.0 for i in range(1, 200)]
        + [0.20 + 0.10 * i / 80.0 for i in range(81)]
    ))
    lik_pts: list[tuple[float, float]] = [(lx(0.0), ly(0.0))]
    for av in a_grid:
        ll = log_lik(av)
        rel = 0.0 if ll == -math.inf else math.exp(max(-60.0, ll - ll_opt))
        lik_pts.append((lx(av), ly(rel)))
    lik_pts.append((lx(1.0), ly(0.0)))
    doc.add(f'<polygon class="area3" points="{pts_str(lik_pts)}"/>')
    doc.add(f'<path class="c3" stroke-width="2.2" d="{path_from_points(lik_pts)}"/>')
    doc.add(f'<circle class="c3-fill" cx="{fmt(lx(0.25))}" cy="{fmt(ly(1.0))}" r="4.2"/>')
    doc.add(f'<text class="xsb c3-txt" x="{fmt(lx(0.25) + 10)}" y="{fmt(ly(1.0) + 12)}">唯一峰 a = 0.25</text>')
    doc.add(f'<text class="xs c3-txt" x="{fmt(lx(0.25) + 10)}" y="{fmt(ly(1.0) + 26)}">ℓ = −56.23</text>')

    # Mark excluded a=1 with crimson X
    x_ex, y_ex = lx(1.0), ly(0.0)
    doc.add(f'<line class="c2" stroke-width="2.2" x1="{fmt(x_ex - 4.5)}" y1="{fmt(y_ex - 4.5)}" x2="{fmt(x_ex + 4.5)}" y2="{fmt(y_ex + 4.5)}"/>')
    doc.add(f'<line class="c2" stroke-width="2.2" x1="{fmt(x_ex - 4.5)}" y1="{fmt(y_ex + 4.5)}" x2="{fmt(x_ex + 4.5)}" y2="{fmt(y_ex - 4.5)}"/>')
    doc.add(f'<text class="xs c2-txt" x="{fmt(lx(0.96))}" y="{fmt(ly(0.18))}" text-anchor="end">L(1)=0 排除</text>')

    doc.add(f'<line class="axis" x1="{fmt(mx0)}" y1="{fmt(my_bot)}" x2="{fmt(mx1 + 6)}" y2="{fmt(my_bot)}"/>')
    doc.add(f'<line class="axis" x1="{fmt(mx0)}" y1="{fmt(my_bot)}" x2="{fmt(mx0)}" y2="{fmt(my_top - 4)}"/>')
    doc.add(f'<text class="xs" x="{fmt(0.5 * (mx0 + mx1))}" y="408" text-anchor="middle">候选概率 a（纵轴：归一化联合似然 L/L{sub("max")}）</text>')

    # Box 3: Full query ledger
    doc.add('<rect class="note" x="638" y="432" width="318" height="104" rx="10"/>')
    doc.add('<text class="smb c4-txt" x="652" y="452">③ 完整查询账本（勿把 shots 混作查询数）</text>')
    doc.add('<text class="sm" x="652" y="474">• k = 0：100 次 × (2·0+1) = 100 次 A/A†</text>')
    doc.add('<text class="sm" x="652" y="494">• k = 1：100 次 × (2·1+1) = 300 次 A/A†</text>')
    doc.add('<text class="smb" x="652" y="516">合计：400 次制备查询 + 100 次好态反射</text>')

    return doc.render(), {"grid_max_a": data["grid_max_a"], "ll_opt": round(ll_opt, 4)}


# ---------------------------------------------------------------------------
# Figure 3 (Ch 12): Two-link quantum memory cutoff rate-quality trade-off
# ---------------------------------------------------------------------------
def build_fig3_cutoff() -> tuple[str, dict[str, float]]:
    expected_rows = load_json("codes/systems/round70-expected-results.json")["network_cutoff"]
    p_link, tau_ms, t_mem = 0.1, 1.0, 20.0
    q_link = 1.0 - p_link

    def closed_form(cutoff: int) -> tuple[float, float]:
        den = p_link * p_link + 2.0 * p_link * q_link * (1.0 - q_link ** cutoff)
        wait = (1.0 + 2.0 * q_link * (1.0 - q_link ** cutoff)) / den
        coh = (
            p_link * p_link
            + 2.0 * p_link * q_link * sum(p_link * (q_link ** (d - 1)) * math.exp(-d * tau_ms / t_mem) for d in range(1, cutoff + 1))
        ) / den
        return wait, coh

    for row in expected_rows:
        w_v, c_v = closed_form(int(row["cutoff_slots"]))
        assert abs(w_v - row["expected_slots"]) < 1e-9
        assert abs(c_v - row["conditional_coherence"]) < 1e-9

    wait_inf = 2.0 / p_link - 1.0 / (1.0 - q_link * q_link)
    coh_inf = (p_link / (1.0 + q_link)) * (1.0 + q_link * math.exp(-tau_ms / t_mem)) / (1.0 - q_link * math.exp(-tau_ms / t_mem))
    ks = list(range(41))
    pairs = [closed_form(k) for k in ks]
    waits = [w for w, _ in pairs]
    cohs = [c for _, c in pairs]

    doc = SvgDoc(
        title="两段量子中继链路的存储超时截止速率—质量权衡",
        desc=(
            "按第 12 章合成更新过程闭式解绘制两段链路在 p = 0.1、时隙 1 ms、相干时间 20 ms 下的速率—质量权衡："
            "左图平均完成时间 E_K 从 K=0 的 100.0 ms 骤降至 K=5 的 20.75 ms 并趋近不设限 14.74 ms；"
            "右图成功样本平均额外存储相干因子 C̄_K 从 1.000 降至 K=5 的 0.887 并趋近 0.679。"
        ),
    )
    doc.add_header(
        "两段量子中继链路的存储超时截止（Cutoff）速率—质量权衡",
        f"更新过程闭式解：单链每轮成功率 p = 0.1，时隙 τ = 1 ms，存储相干时间 T{sub('mem')} = 20 ms（理想先兆与交换）",
        raw_sub=True,
    )
    doc.add_panel(28, 94, 464, 456, f"平均完成时间 E{sub('K')}（ms）随超时上限 K 变化", raw_heading=True)
    doc.add_panel(508, 94, 464, 456, f"成功样本平均额外相干因子 C̄{sub('K')} 随 K 变化", raw_heading=True)

    # --- Left Panel: Mean completion time E_K ---
    lx0, lx1 = 94.0, 468.0
    py_top, py_bot = 176.0, 444.0

    def gx_l(k_v: float) -> float:
        return lx0 + (k_v / 40.0) * (lx1 - lx0)

    def gy_w(w_v: float) -> float:
        return py_bot - (w_v / 108.0) * (py_bot - py_top)

    # Legend above left plot
    doc.add('<line class="c1" stroke-width="2.6" x1="48" y1="152" x2="76" y2="152"/>')
    doc.add('<circle class="c1-fill" cx="62" cy="152" r="3.5"/>')
    doc.add(f'<text class="sm" x="82" y="156">有限超时 E{sub("K")}</text>')
    doc.add('<line class="guide" stroke-width="1.8" x1="186" y1="152" x2="216" y2="152"/>')
    doc.add(f'<text class="sm" x="222" y="156">不设截止极限：{wait_inf:.2f} ms</text>')

    for w_t in (0, 20, 40, 60, 80, 100):
        yw = gy_w(float(w_t))
        doc.add(f'<line class="grid" x1="{fmt(lx0)}" y1="{fmt(yw)}" x2="{fmt(lx1)}" y2="{fmt(yw)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(lx0 - 5)}" y1="{fmt(yw)}" x2="{fmt(lx0)}" y2="{fmt(yw)}"/>')
        doc.add(f'<text class="sm" x="{fmt(lx0 - 9)}" y="{fmt(yw + 4)}" text-anchor="end">{w_t}</text>')
    for k_t in (0, 10, 20, 30, 40):
        xk = gx_l(float(k_t))
        doc.add(f'<line class="grid" x1="{fmt(xk)}" y1="{fmt(py_top)}" x2="{fmt(xk)}" y2="{fmt(py_bot)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(xk)}" y1="{fmt(py_bot)}" x2="{fmt(xk)}" y2="{fmt(py_bot + 5)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xk)}" y="{fmt(py_bot + 19)}" text-anchor="middle">{k_t}</text>')

    # Highlight K=5 sweet-spot vertical line
    doc.add(f'<line class="c3" stroke-width="1.3" stroke-dasharray="4 3" x1="{fmt(gx_l(5))}" y1="{fmt(py_top)}" x2="{fmt(gx_l(5))}" y2="{fmt(py_bot)}"/>')

    # Asymptote & curve
    y_winf = gy_w(wait_inf)
    doc.add(f'<line class="guide" stroke-width="1.6" x1="{fmt(lx0)}" y1="{fmt(y_winf)}" x2="{fmt(lx1)}" y2="{fmt(y_winf)}"/>')
    w_pts = [(gx_l(float(k)), gy_w(w)) for k, w in zip(ks, waits)]
    doc.add(f'<polygon class="area1" points="{pts_str([(lx0, py_bot)] + w_pts + [(lx1, py_bot)])}"/>')
    doc.add(f'<path class="c1" stroke-width="2.6" d="{path_from_points(w_pts)}"/>')

    for k_m in (0, 1, 5, 10, 15, 20, 25, 30, 35, 40):
        r_m = 4.6 if k_m in (0, 1, 5, 20) else 2.8
        cls_m = "c3-fill" if k_m == 5 else "c1-fill"
        doc.add(f'<circle class="{cls_m}" cx="{fmt(gx_l(k_m))}" cy="{fmt(gy_w(waits[k_m]))}" r="{fmt(r_m)}"/>')

    # Non-overlapping callouts
    doc.add('<rect class="pill-bg" x="132" y="182" width="128" height="24" rx="7"/>')
    doc.add('<text class="xsb c1-txt" x="196" y="198" text-anchor="middle">K = 0：100.0 ms</text>')
    doc.add(f'<line class="c1" stroke-width="1.2" x1="132" y1="195" x2="{fmt(gx_l(0) + 6)}" y2="{fmt(gy_w(waits[0]))}"/>')

    doc.add('<rect class="pill-bg" x="150" y="274" width="132" height="24" rx="7"/>')
    doc.add('<text class="xsb c1-txt" x="216" y="290" text-anchor="middle">K = 1：42.14 ms</text>')
    doc.add(f'<line class="c1" stroke-width="1.2" x1="150" y1="292" x2="{fmt(gx_l(1) + 5)}" y2="{fmt(gy_w(waits[1]) - 3)}"/>')

    doc.add('<rect class="c3-soft" x="192" y="322" width="142" height="24" rx="7"/>')
    doc.add('<text class="xsb c3-txt" x="263" y="338" text-anchor="middle">K = 5：20.75 ms</text>')
    doc.add(f'<line class="c3" stroke-width="1.2" x1="192" y1="340" x2="{fmt(gx_l(5) + 5)}" y2="{fmt(gy_w(waits[5]) - 4)}"/>')

    doc.add('<rect class="pill-bg" x="314" y="356" width="142" height="24" rx="7"/>')
    doc.add('<text class="xsb c1-txt" x="385" y="372" text-anchor="middle">K = 20：15.35 ms</text>')
    doc.add(f'<line class="c1" stroke-width="1.2" x1="314" y1="376" x2="{fmt(gx_l(20) + 4)}" y2="{fmt(gy_w(waits[20]) - 5)}"/>')

    doc.add(f'<text class="xs" x="464" y="{fmt(y_winf + 18)}" text-anchor="end">无截止极限 14.74 ms</text>')

    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(py_bot)}" x2="{fmt(lx1 + 8)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(lx1 + 10, py_bot, 1, 0))
    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(py_bot)}" x2="{fmt(lx0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(lx0, py_top - 10, 0, -1))
    doc.add(f'<text class="lbl" x="{fmt(0.5 * (lx0 + lx1))}" y="486" text-anchor="middle">超时上限 K（首链成功后最多额外等待轮数）</text>')
    doc.add(
        f'<text class="lbl" x="48" y="{fmt(0.5 * (py_top + py_bot))}" text-anchor="middle" '
        f'transform="rotate(-90 48 {fmt(0.5 * (py_top + py_bot))})">平均完成时间 E{sub("K")} (ms)</text>'
    )
    doc.add('<rect class="pill" x="44" y="502" width="432" height="34" rx="8"/>')
    doc.add('<text class="sm" x="260" y="523" text-anchor="middle">K 过短（如 K ≤ 1）触发频繁双链复位，等待时间暴涨</text>')

    # --- Right Panel: Conditional coherence factor ---
    rx0, rx1 = 574.0, 948.0

    def gx_r(k_v: float) -> float:
        return rx0 + (k_v / 40.0) * (rx1 - rx0)

    def gy_c(c_v: float) -> float:
        return py_bot - ((c_v - 0.62) / (1.04 - 0.62)) * (py_bot - py_top)

    # Legend above right plot
    doc.add('<line class="c2" stroke-width="2.6" stroke-dasharray="8 4" x1="528" y1="152" x2="556" y2="152"/>')
    doc.add('<rect class="c2-fill" x="538" y="148" width="8" height="8" rx="1"/>')
    doc.add(f'<text class="sm" x="562" y="156">有限超时 C̄{sub("K")}</text>')
    doc.add('<line class="guide" stroke-width="1.8" x1="668" y1="152" x2="698" y2="152"/>')
    doc.add(f'<text class="sm" x="704" y="156">不设截止极限：{coh_inf:.3f}</text>')

    for c_t in (0.65, 0.70, 0.80, 0.90, 1.00):
        yc = gy_c(c_t)
        doc.add(f'<line class="grid" x1="{fmt(rx0)}" y1="{fmt(yc)}" x2="{fmt(rx1)}" y2="{fmt(yc)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(rx0 - 5)}" y1="{fmt(yc)}" x2="{fmt(rx0)}" y2="{fmt(yc)}"/>')
        doc.add(f'<text class="sm" x="{fmt(rx0 - 9)}" y="{fmt(yc + 4)}" text-anchor="end">{c_t:.2f}</text>')
    for k_t in (0, 10, 20, 30, 40):
        xk = gx_r(float(k_t))
        doc.add(f'<line class="grid" x1="{fmt(xk)}" y1="{fmt(py_top)}" x2="{fmt(xk)}" y2="{fmt(py_bot)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(xk)}" y1="{fmt(py_bot)}" x2="{fmt(xk)}" y2="{fmt(py_bot + 5)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xk)}" y="{fmt(py_bot + 19)}" text-anchor="middle">{k_t}</text>')

    # Highlight K=5 vertical guide
    doc.add(f'<line class="c3" stroke-width="1.3" stroke-dasharray="4 3" x1="{fmt(gx_r(5))}" y1="{fmt(py_top)}" x2="{fmt(gx_r(5))}" y2="{fmt(py_bot)}"/>')

    y_cinf = gy_c(coh_inf)
    doc.add(f'<line class="guide" stroke-width="1.6" x1="{fmt(rx0)}" y1="{fmt(y_cinf)}" x2="{fmt(rx1)}" y2="{fmt(y_cinf)}"/>')
    c_pts = [(gx_r(float(k)), gy_c(c)) for k, c in zip(ks, cohs)]
    doc.add(f'<polygon class="area2" points="{pts_str([(rx0, py_bot)] + c_pts + [(rx1, py_bot)])}"/>')
    doc.add(f'<path class="c2" stroke-width="2.6" stroke-dasharray="8 4" d="{path_from_points(c_pts)}"/>')

    for k_m in (0, 1, 5, 10, 15, 20, 25, 30, 35, 40):
        sz = 4.5 if k_m in (0, 1, 5, 20) else 2.8
        cls_m = "c3-fill" if k_m == 5 else "c2-fill"
        doc.add(f'<polygon class="{cls_m}" points="{square_pts(gx_r(k_m), gy_c(cohs[k_m]), sz)}"/>')

    # Clean callouts
    doc.add('<rect class="pill-bg" x="614" y="182" width="116" height="24" rx="7"/>')
    doc.add('<text class="xsb c2-txt" x="672" y="198" text-anchor="middle">K = 0：1.000</text>')
    doc.add(f'<line class="c2" stroke-width="1.2" x1="614" y1="196" x2="{fmt(gx_r(0) + 6)}" y2="{fmt(gy_c(cohs[0]))}"/>')

    doc.add('<rect class="pill-bg" x="646" y="214" width="116" height="24" rx="7"/>')
    doc.add('<text class="xsb c2-txt" x="704" y="230" text-anchor="middle">K = 1：0.969</text>')
    doc.add(f'<line class="c2" stroke-width="1.2" x1="646" y1="224" x2="{fmt(gx_r(1) + 6)}" y2="{fmt(gy_c(cohs[1]))}"/>')

    doc.add('<rect class="c3-soft" x="688" y="252" width="186" height="40" rx="8"/>')
    doc.add('<text class="xsb c3-txt" x="781" y="268" text-anchor="middle">K = 5：C̄ = 0.887（折中优选）</text>')
    doc.add('<text class="xs c3-txt" x="781" y="284" text-anchor="middle">纯退相位 Bell 重叠 0.944</text>')
    doc.add(f'<line class="c3" stroke-width="1.2" x1="688" y1="272" x2="{fmt(gx_r(5) + 6)}" y2="{fmt(gy_c(cohs[5]))}"/>')

    doc.add('<rect class="pill-bg" x="794" y="324" width="136" height="24" rx="7"/>')
    doc.add('<text class="xsb c2-txt" x="862" y="340" text-anchor="middle">K = 20：0.736</text>')
    doc.add(f'<line class="c2" stroke-width="1.2" x1="794" y1="342" x2="{fmt(gx_r(20) + 5)}" y2="{fmt(gy_c(cohs[20]) - 5)}"/>')

    doc.add(f'<text class="xs" x="944" y="{fmt(y_cinf + 18)}" text-anchor="end">无截止极限 0.679</text>')

    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(py_bot)}" x2="{fmt(rx1 + 8)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(rx1 + 10, py_bot, 1, 0))
    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(py_bot)}" x2="{fmt(rx0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(rx0, py_top - 10, 0, -1))
    doc.add(f'<text class="lbl" x="{fmt(0.5 * (rx0 + rx1))}" y="486" text-anchor="middle">超时上限 K（额外等待轮数）</text>')
    doc.add(
        f'<text class="lbl" x="528" y="{fmt(0.5 * (py_top + py_bot))}" text-anchor="middle" '
        f'transform="rotate(-90 528 {fmt(0.5 * (py_top + py_bot))})">平均额外相干因子 C̄{sub("K")}（无量纲）</text>'
    )
    doc.add('<rect class="note" x="524" y="502" width="432" height="34" rx="8"/>')
    doc.add('<text class="sm" x="740" y="523" text-anchor="middle">取 K = 5 较不设限仅多等 6.0 ms，相干因子从 0.679 跃升至 0.887</text>')

    return doc.render(), {"wait_k5": round(waits[5], 3), "coh_k5": round(cohs[5], 5), "wait_inf": round(wait_inf, 3)}


# ---------------------------------------------------------------------------
# Figure 4 (Ch 17): Annealing chain strength J crossing & field dynamic range
# ---------------------------------------------------------------------------
def build_fig4_chain_strength() -> tuple[str, dict[str, float]]:
    rows17 = load_json("codes/algorithms/round70-results.json")["17"]
    by_j = {int(r["J"]): r for r in rows17}
    assert by_j[1]["broken_ground_states"] == 1 and by_j[1]["ground_energy"] == -3
    assert by_j[2]["broken_ground_states"] == 1 and by_j[2]["ground_energy"] == -2
    assert by_j[3]["broken_ground_states"] == 0 and abs(by_j[3]["scaled_field_magnitude"] - 2.0 / 3.0) < TOL
    assert by_j[8]["broken_ground_states"] == 0 and abs(by_j[8]["scaled_field_magnitude"] - 0.25) < TOL

    doc = SvgDoc(
        title="量子退火链强度能级交叉与归一化局域场幅度衰减",
        desc=(
            "两自旋教学模型 E = −2s_a + 2s_b − J s_a s_b（无量纲模型单位）："
            "左图展示链完整态 (+,+)/(−,−)（能量 −J）与断链态 (+,−)（J−4）、(−,+)（J+4）在 J = 2、E = −2 处精确交叉，仅 J > 2 保证所有基态链完整；"
            "右图展示全部系数统一缩放到 [−1, 1] 后，有效局域场幅 2/max(2, J) 在 J = 3 降至 2/3、在 J = 8 降至 1/4。"
        ),
    )
    doc.add_header(
        "量子退火链强度 J 的双刃剑：防断链门槛与有效动态范围压缩",
        f"两自旋教学模型 E = −2s{sub('a')} + 2s{sub('b')} − J s{sub('a')}s{sub('b')}（无量纲模型单位）· 左：能级交叉；右：缩放到 [−1, 1] 后的有效局域场",
        raw_sub=True,
    )
    doc.add_panel(28, 94, 468, 456, "A. 链完整与断链能级交叉（仅 J > 2 全基态合法）")
    doc.add_panel(512, 94, 460, 456, "B. 系数统一缩放到 [−1, 1] 后的有效局域场幅")

    # --- Left Panel: Energy crossing ---
    lx0, lx1 = 88.0, 472.0
    py_top, py_bot = 178.0, 444.0
    e_min, e_max = -9.0, 13.0

    def gx_l(j_v: float) -> float:
        return lx0 + (j_v / 8.0) * (lx1 - lx0)

    def gy_e(e_v: float) -> float:
        return py_bot - ((e_v - e_min) / (e_max - e_min)) * (py_bot - py_top)

    # Legend above left plot
    doc.add('<line class="c3" stroke-width="2.6" x1="42" y1="152" x2="66" y2="152"/>')
    doc.add('<circle class="c3-fill" cx="54" cy="152" r="3.4"/>')
    doc.add('<text class="xs" x="71" y="156">链完整(±,±): −J</text>')

    doc.add('<line class="c2" stroke-width="2.4" stroke-dasharray="7 4" x1="176" y1="152" x2="200" y2="152"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(188, 152, 4.0)}"/>')
    doc.add('<text class="xs" x="206" y="156">断链(+,−): J−4</text>')

    doc.add('<line class="c4" stroke-width="2.2" stroke-dasharray="3 3" x1="312" y1="152" x2="336" y2="152"/>')
    doc.add(f'<polygon class="c4-fill" points="{triangle_pts(324, 152, 4.0)}"/>')
    doc.add('<text class="xs" x="342" y="156">断链(−,+): J+4</text>')

    # Shaded danger band J <= 2
    x_j2 = gx_l(2.0)
    doc.add(f'<rect class="forbid" x="{fmt(lx0)}" y="{fmt(py_top)}" width="{fmt(x_j2 - lx0)}" height="{fmt(py_bot - py_top)}"/>')
    doc.add(f'<rect fill="url(#hatch-red)" x="{fmt(lx0)}" y="{fmt(py_top)}" width="{fmt(x_j2 - lx0)}" height="{fmt(py_bot - py_top)}"/>')

    # Grid & ticks
    for ev in (-8, -4, 0, 4, 8, 12):
        ye = gy_e(float(ev))
        cls_g = "guide" if ev == 0 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(lx0)}" y1="{fmt(ye)}" x2="{fmt(lx1)}" y2="{fmt(ye)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(lx0 - 5)}" y1="{fmt(ye)}" x2="{fmt(lx0)}" y2="{fmt(ye)}"/>')
        lbl_e = str(ev).replace("-", "−")
        doc.add(f'<text class="sm" x="{fmt(lx0 - 9)}" y="{fmt(ye + 4)}" text-anchor="end">{lbl_e}</text>')
    for jv in (0, 2, 4, 6, 8):
        xj = gx_l(float(jv))
        cls_g = "c2" if jv == 2 else "grid"
        extra = ' stroke-width="1.5" stroke-dasharray="5 4"' if jv == 2 else ""
        doc.add(f'<line class="{cls_g}"{extra} x1="{fmt(xj)}" y1="{fmt(py_top)}" x2="{fmt(xj)}" y2="{fmt(py_bot)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(xj)}" y1="{fmt(py_bot)}" x2="{fmt(xj)}" y2="{fmt(py_bot + 5)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xj)}" y="{fmt(py_bot + 19)}" text-anchor="middle">{jv}</text>')

    # Three exact energy lines
    doc.add(f'<line class="c4" stroke-width="2.2" stroke-dasharray="3 3" x1="{fmt(gx_l(0))}" y1="{fmt(gy_e(4))}" x2="{fmt(gx_l(8))}" y2="{fmt(gy_e(12))}"/>')
    doc.add(f'<line class="c2" stroke-width="2.6" stroke-dasharray="8 4" x1="{fmt(gx_l(0))}" y1="{fmt(gy_e(-4))}" x2="{fmt(gx_l(8))}" y2="{fmt(gy_e(4))}"/>')
    doc.add(f'<line class="c3" stroke-width="2.8" x1="{fmt(gx_l(0))}" y1="{fmt(gy_e(0))}" x2="{fmt(gx_l(8))}" y2="{fmt(gy_e(-8))}"/>')

    # Markers at J=1, 2, 3, 8
    for jm in (1, 3, 6):
        doc.add(f'<circle class="c3-fill" cx="{fmt(gx_l(jm))}" cy="{fmt(gy_e(-jm))}" r="4.0"/>')
        doc.add(f'<polygon class="c2-fill" points="{diamond_pts(gx_l(jm), gy_e(jm - 4), 4.6)}"/>')
        doc.add(f'<polygon class="c4-fill" points="{triangle_pts(gx_l(jm), gy_e(jm + 4), 4.5)}"/>')

    # Crossing marker at (2, -2)
    yc2 = gy_e(-2.0)
    doc.add(f'<circle class="node-bg axis" stroke-width="2.6" cx="{fmt(x_j2)}" cy="{fmt(yc2)}" r="5.5"/>')

    # Clean callouts in verified empty zones
    doc.add('<rect class="c2-soft" x="94" y="186" width="84" height="36" rx="7"/>')
    doc.add('<text class="xsb c2-txt" x="136" y="201" text-anchor="middle">J ≤ 2</text>')
    doc.add('<text class="xs c2-txt" x="136" y="216" text-anchor="middle">断链污染基态</text>')

    doc.add('<rect class="pill-bg" x="102" y="394" width="154" height="38" rx="7"/>')
    doc.add('<text class="xsb" x="179" y="410" text-anchor="middle">交叉点 (J=2, E=−2)</text>')
    doc.add('<text class="xs" x="179" y="425" text-anchor="middle">三态简并，仍含断链态</text>')
    doc.add(f'<line class="axis" stroke-width="1.2" x1="184" y1="394" x2="{fmt(x_j2)}" y2="{fmt(yc2 + 7)}"/>')

    doc.add('<rect class="c3-soft" x="310" y="340" width="154" height="38" rx="7"/>')
    doc.add('<text class="xsb c3-txt" x="387" y="356" text-anchor="middle">J &gt; 2：合法基态区</text>')
    doc.add('<text class="xs c3-txt" x="387" y="371" text-anchor="middle">保护能隙 ΔE = 2J − 4</text>')

    # Axes & bottom note
    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(py_bot)}" x2="{fmt(lx1 + 8)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(lx1 + 10, py_bot, 1, 0))
    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(py_bot)}" x2="{fmt(lx0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(lx0, py_top - 10, 0, -1))
    doc.add(f'<text class="lbl" x="{fmt(0.5 * (lx0 + lx1))}" y="486" text-anchor="middle">链强度 J（无量纲模型单位）</text>')
    doc.add(
        f'<text class="lbl" x="48" y="{fmt(0.5 * (py_top + py_bot))}" text-anchor="middle" '
        f'transform="rotate(-90 48 {fmt(0.5 * (py_top + py_bot))})">配置能量 E（无量纲模型单位）</text>'
    )
    doc.add('<rect class="pill" x="44" y="502" width="436" height="34" rx="8"/>')
    doc.add('<text class="sm" x="262" y="523" text-anchor="middle">J = 1 时断链态 (−3) 低于合法态 (−1)；J = 3 时打开能隙 2</text>')

    # --- Right Panel: Effective field amplitude after [-1, 1] hardware scaling ---
    rx0, rx1 = 578.0, 948.0

    def gx_r(j_v: float) -> float:
        return rx0 + (j_v / 8.0) * (rx1 - rx0)

    def gy_f(f_v: float) -> float:
        return py_bot - (f_v / 1.15) * (py_bot - py_top)

    # Legend above right plot
    doc.add('<line class="c1" stroke-width="2.6" x1="534" y1="152" x2="564" y2="152"/>')
    doc.add('<rect class="c1-fill" x="545" y="148" width="8" height="8" rx="1"/>')
    doc.add(f'<text class="sm" x="570" y="156">归一化有效局域场幅 h{sub("eff")}(J) = 2 / max(2, J)</text>')

    for fv in (0.0, 0.25, 0.50, 0.75, 1.00):
        yf = gy_f(fv)
        doc.add(f'<line class="grid" x1="{fmt(rx0)}" y1="{fmt(yf)}" x2="{fmt(rx1)}" y2="{fmt(yf)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(rx0 - 5)}" y1="{fmt(yf)}" x2="{fmt(rx0)}" y2="{fmt(yf)}"/>')
        doc.add(f'<text class="sm" x="{fmt(rx0 - 9)}" y="{fmt(yf + 4)}" text-anchor="end">{fv:.2f}</text>')
    for jv in (0, 2, 4, 6, 8):
        xj = gx_r(float(jv))
        cls_g = "guide" if jv == 2 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(xj)}" y1="{fmt(py_top)}" x2="{fmt(xj)}" y2="{fmt(py_bot)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(xj)}" y1="{fmt(py_bot)}" x2="{fmt(xj)}" y2="{fmt(py_bot + 5)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xj)}" y="{fmt(py_bot + 19)}" text-anchor="middle">{jv}</text>')

    # Exact curve 2 / max(2, J)
    js_r = [8.0 * i / 160.0 for i in range(161)]
    f_pts = [(gx_r(jv), gy_f(2.0 / max(2.0, jv))) for jv in js_r]
    doc.add(f'<polygon class="area1" points="{pts_str([(rx0, py_bot)] + f_pts + [(rx1, py_bot)])}"/>')
    doc.add(f'<path class="c1" stroke-width="2.8" d="{path_from_points(f_pts)}"/>')

    # Key square markers at J=2, 3, 8
    for jm, f_val, mcls in ((2.0, 1.0, "c1-fill"), (3.0, 2.0 / 3.0, "c3-fill"), (8.0, 0.25, "c2-fill")):
        doc.add(f'<polygon class="{mcls}" points="{square_pts(gx_r(jm), gy_f(f_val), 5.0)}"/>')

    # Callouts in verified open regions
    doc.add('<rect class="pill-bg" x="586" y="232" width="76" height="36" rx="7"/>')
    doc.add('<text class="xsb" x="624" y="247" text-anchor="middle">J ≤ 2</text>')
    doc.add('<text class="xs" x="624" y="262" text-anchor="middle">满幅 1.00</text>')

    doc.add('<rect class="c3-soft" x="748" y="218" width="186" height="38" rx="7"/>')
    doc.add('<text class="xsb c3-txt" x="841" y="234" text-anchor="middle">J = 3：有效场 2/3 ≈ 0.667</text>')
    doc.add('<text class="xs c3-txt" x="841" y="249" text-anchor="middle">保完整且保留 67% 动态范围</text>')
    doc.add(f'<line class="c3" stroke-width="1.3" x1="748" y1="242" x2="{fmt(gx_r(3.0) + 6)}" y2="{fmt(gy_f(2.0 / 3.0) - 4)}"/>')

    doc.add('<rect class="c2-soft" x="752" y="302" width="186" height="38" rx="7"/>')
    doc.add('<text class="xsb c2-txt" x="845" y="318" text-anchor="middle">J = 8：有效场 1/4 = 0.250</text>')
    doc.add('<text class="xs c2-txt" x="845" y="333" text-anchor="middle">相对模拟控制误差放大近 3 倍</text>')
    doc.add(f'<line class="c2" stroke-width="1.3" x1="910" y1="340" x2="{fmt(gx_r(8.0) - 3)}" y2="{fmt(gy_f(0.25) - 6)}"/>')

    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(py_bot)}" x2="{fmt(rx1 + 8)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(rx1 + 10, py_bot, 1, 0))
    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(py_bot)}" x2="{fmt(rx0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(rx0, py_top - 10, 0, -1))
    doc.add(f'<text class="lbl" x="{fmt(0.5 * (rx0 + rx1))}" y="486" text-anchor="middle">链强度 J（无量纲模型单位）</text>')
    doc.add(
        f'<text class="lbl" x="530" y="{fmt(0.5 * (py_top + py_bot))}" text-anchor="middle" '
        f'transform="rotate(-90 530 {fmt(0.5 * (py_top + py_bot))})">缩放后有效局域场幅（无量纲）</text>'
    )
    doc.add('<rect class="note" x="528" y="502" width="428" height="34" rx="8"/>')
    doc.add('<text class="sm" x="742" y="523" text-anchor="middle">J 越大越防断链，但按 2/J 压扁原题参数；须在门槛上方适度选取</text>')

    return doc.render(), {"j3_field": round(2.0 / 3.0, 4), "j8_field": 0.25}


# ---------------------------------------------------------------------------
# Figure 5 (Q1): Ideal quantum eraser opposite conditional fringes vs marginal
# ---------------------------------------------------------------------------
def build_fig5_eraser() -> tuple[str, dict[str, float]]:
    q1 = load_json("codes/foundations/round71-results.json")["cases"]["q1"]

    def p_plus(phi: float) -> float:
        return 0.5 * (1.0 + math.cos(phi))

    def p_minus(phi: float) -> float:
        return 0.5 * (1.0 - math.cos(phi))

    for row in q1["rows"]:
        ph = float(row["phi_radians"])
        assert abs(p_plus(ph) - row["detector_zero_given_plus"]) < 1e-9
        assert abs(p_minus(ph) - row["detector_zero_given_minus"]) < 1e-9
        assert abs(0.5 * (p_plus(ph) + p_minus(ph)) - row["detector_zero_nonselective"]) < 1e-9

    doc = SvgDoc(
        title="量子擦除的两条反相条件条纹与恒为二分之一的非选择边缘分布",
        desc=(
            "理想平衡双路径量子擦除模型：按擦除基测量记录端 D 得到等概率两组（各占 1/2），"
            "+ 组条件概率 P(0|+) = (1+cos φ)/2（实线方块）与 − 组条件概率 P(0|−) = (1−cos φ)/2（虚线圆圈）严格反相，"
            "二者等权平均后波峰填平波谷，非选择边缘分布 P(0) 恒为 1/2，无法超光速传信。"
        ),
    )
    doc.add_header(
        "量子擦除条件条纹对照：反相子集叠加恒归平坦边缘",
        "理想平衡双路径模型：路径与可访问正交记录纠缠，记录端按 |±⟩ 擦除基测量，两组权重各为 1/2",
    )
    doc.add_panel(28, 94, 634, 456, "端口 0 探测概率随路径相对相位 φ 变化（精确公式）")
    doc.add_panel(678, 94, 294, 456, "条件分解表与因果性边界")

    # --- Left Panel: Fringes & flat marginal ---
    px0, px1 = 94.0, 636.0
    py_top, py_bot = 178.0, 444.0
    p_hi = 1.06

    def gx(phi: float) -> float:
        return px0 + (phi / (2.0 * math.pi)) * (px1 - px0)

    def gy(p_val: float) -> float:
        return py_bot - (p_val / p_hi) * (py_bot - py_top)

    # Legend above plot
    doc.add('<line class="c1" stroke-width="2.6" x1="46" y1="152" x2="74" y2="152"/>')
    doc.add('<rect class="c1-fill" x="56" y="148" width="8" height="8" rx="1"/>')
    doc.add('<text class="sm" x="80" y="156">P(0 | +) = (1+cos φ)/2</text>')

    doc.add('<line class="c2" stroke-width="2.5" stroke-dasharray="8 4" x1="252" y1="152" x2="280" y2="152"/>')
    doc.add('<circle class="node-bg c2" stroke-width="2.2" cx="266" cy="152" r="4"/>')
    doc.add('<text class="sm" x="286" y="156">P(0 | −) = (1−cos φ)/2</text>')

    doc.add('<line class="c3" stroke-width="2.4" stroke-dasharray="3 4" x1="458" y1="152" x2="486" y2="152"/>')
    doc.add('<text class="sm" x="492" y="156">边缘 P(0) = 1/2</text>')

    # Grid & ticks
    for pv in (0.0, 0.25, 0.50, 0.75, 1.00):
        yp = gy(pv)
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(yp)}" x2="{fmt(px1)}" y2="{fmt(yp)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(px0 - 5)}" y1="{fmt(yp)}" x2="{fmt(px0)}" y2="{fmt(yp)}"/>')
        doc.add(f'<text class="sm" x="{fmt(px0 - 9)}" y="{fmt(yp + 4)}" text-anchor="end">{pv:.2f}</text>')
    for frac, plbl in ((0.0, "0"), (0.25, "π/2"), (0.5, "π"), (0.75, "3π/2"), (1.0, "2π")):
        xp = gx(frac * 2.0 * math.pi)
        doc.add(f'<line class="grid" x1="{fmt(xp)}" y1="{fmt(py_top)}" x2="{fmt(xp)}" y2="{fmt(py_bot)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(xp)}" y1="{fmt(py_bot)}" x2="{fmt(xp)}" y2="{fmt(py_bot + 5)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xp)}" y="{fmt(py_bot + 19)}" text-anchor="middle">{plbl}</text>')

    # Shaded peak-trough cancellation lobes around P = 0.5
    y_half = gy(0.5)
    n_s = 161
    phis = [2.0 * math.pi * i / (n_s - 1) for i in range(n_s)]
    pts_p = [(gx(ph), gy(p_plus(ph))) for ph in phis]
    pts_m = [(gx(ph), gy(p_minus(ph))) for ph in phis]

    # Shade central dome where P(0|-) > 0.5 (phi in [pi/2, 3pi/2]) and matching trough P(0|+) < 0.5
    phis_mid = [0.5 * math.pi + math.pi * i / 80.0 for i in range(81)]
    poly_m_dome = [(gx(0.5 * math.pi), y_half)] + [(gx(ph), gy(p_minus(ph))) for ph in phis_mid] + [(gx(1.5 * math.pi), y_half)]
    poly_p_trough = [(gx(0.5 * math.pi), y_half)] + [(gx(ph), gy(p_plus(ph))) for ph in phis_mid] + [(gx(1.5 * math.pi), y_half)]
    doc.add(f'<polygon class="area2" points="{pts_str(poly_m_dome)}"/>')
    doc.add(f'<polygon class="area1" points="{pts_str(poly_p_trough)}"/>')

    # Three curves
    doc.add(f'<line class="c3" stroke-width="2.6" stroke-dasharray="4 4" x1="{fmt(px0)}" y1="{fmt(y_half)}" x2="{fmt(px1)}" y2="{fmt(y_half)}"/>')
    doc.add(f'<path class="c1" stroke-width="2.7" d="{path_from_points(pts_p)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.6" stroke-dasharray="9 5" d="{path_from_points(pts_m)}"/>')

    # Key markers at 0, pi/3, pi/2, pi, 3pi/2, 2pi
    for ph_mk in (0.0, math.pi / 3.0, 0.5 * math.pi, math.pi, 1.5 * math.pi, 2.0 * math.pi):
        doc.add(f'<rect class="c1-fill" x="{fmt(gx(ph_mk) - 4.2)}" y="{fmt(gy(p_plus(ph_mk)) - 4.2)}" width="8.4" height="8.4" rx="1"/>')
        doc.add(f'<circle class="node-bg c2" stroke-width="2.4" cx="{fmt(gx(ph_mk))}" cy="{fmt(gy(p_minus(ph_mk)))}" r="4.5"/>')

    # Clean non-overlapping in-plot labels in open dome / trough / midline pockets
    doc.add('<rect class="c2-soft" x="294" y="246" width="142" height="26" rx="7"/>')
    doc.add('<text class="xsb c2-txt" x="365" y="263" text-anchor="middle">− 组亮峰：P(0|−) = 1</text>')

    doc.add('<rect class="c1-soft" x="294" y="364" width="142" height="26" rx="7"/>')
    doc.add('<text class="xsb c1-txt" x="365" y="381" text-anchor="middle">+ 组暗谷：P(0|+) = 0</text>')

    doc.add('<rect class="c3-soft" x="104" y="305" width="104" height="26" rx="7"/>')
    doc.add('<text class="xsb c3-txt" x="156" y="322" text-anchor="middle">边缘恒 = 0.50</text>')

    # Axes & bottom summary
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px1 + 8)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(px1 + 10, py_bot, 1, 0))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(px0, py_top - 10, 0, -1))
    doc.add(f'<text class="lbl" x="{fmt(0.5 * (px0 + px1))}" y="486" text-anchor="middle">路径相对相位 φ (rad)</text>')
    doc.add(
        f'<text class="lbl" x="46" y="{fmt(0.5 * (py_top + py_bot))}" text-anchor="middle" '
        f'transform="rotate(-90 46 {fmt(0.5 * (py_top + py_bot))})">端口 0 探测概率 P（无量纲）</text>'
    )
    doc.add('<rect class="pill" x="44" y="502" width="602" height="34" rx="8"/>')
    doc.add('<text class="sm" x="345" y="523" text-anchor="middle">两条反相条纹按各半权重相加，波峰恰好填平波谷：P(0) = ½P(0|+) + ½P(0|−) ≡ ½</text>')

    # --- Right Panel: Table & Causality Boundary ---
    doc.add('<rect class="c1-soft" x="692" y="144" width="266" height="92" rx="10"/>')
    doc.add('<text class="smb c1-txt" x="706" y="164">① 擦除基条件概率恒等式</text>')
    doc.add('<text class="sm" x="706" y="187">记录端 D 测 |+⟩ / |−⟩ 各占概率 1/2</text>')
    doc.add('<text class="sm" x="706" y="208">P(0|±) = (1 ± cos φ) / 2</text>')
    doc.add('<text class="smb c3-txt" x="706" y="228">非选择求和：P(0) ≡ 0.50（无条纹）</text>')

    # Exact 4-row table from round71-results.json
    doc.add('<rect class="panel" x="692" y="246" width="266" height="156" rx="10"/>')
    doc.add('<rect class="phead" x="693" y="247" width="264" height="28" rx="8"/>')
    doc.add('<text class="xsb" x="720" y="265" text-anchor="middle">φ</text>')
    doc.add('<text class="xsb c1-txt" x="782" y="265" text-anchor="middle">P(0|+)</text>')
    doc.add('<text class="xsb c2-txt" x="852" y="265" text-anchor="middle">P(0|−)</text>')
    doc.add('<text class="xsb c3-txt" x="920" y="265" text-anchor="middle">边缘 P(0)</text>')

    table_rows = [
        ("0", 1.00, 0.00, 0.50),
        ("π/3", 0.75, 0.25, 0.50),
        ("π/2", 0.50, 0.50, 0.50),
        ("π", 0.00, 1.00, 0.50),
    ]
    for idx, (ph_s, vp, vm, v0) in enumerate(table_rows):
        yr = 298 + idx * 30
        if idx > 0:
            doc.add(f'<line class="grid" x1="700" y1="{yr - 18}" x2="950" y2="{yr - 18}"/>')
        doc.add(f'<text class="smb" x="720" y="{yr}" text-anchor="middle">{ph_s}</text>')
        doc.add(f'<text class="sm c1-txt" x="782" y="{yr}" text-anchor="middle">{vp:.2f}</text>')
        doc.add(f'<text class="sm c2-txt" x="852" y="{yr}" text-anchor="middle">{vm:.2f}</text>')
        doc.add(f'<text class="smb c3-txt" x="920" y="{yr}" text-anchor="middle">{v0:.2f}</text>')

    doc.add('<rect class="note" x="692" y="412" width="266" height="124" rx="10"/>')
    doc.add('<text class="smb c4-txt" x="706" y="432">② 因果性边界（为何不能超光速传信）</text>')
    doc.add('<text class="sm" x="706" y="454">• 不按 D 分组时，总点击分布恒平坦</text>')
    doc.add('<text class="sm" x="706" y="475">• 延迟测 D 从不改写已记录的 P 点击</text>')
    doc.add('<text class="sm" x="706" y="496">• 须经经典信道（≤ c）符合筛选才见条纹</text>')
    doc.add('<text class="sm" x="706" y="517">• 记录泄入宏观环境则无法相干擦除</text>')

    return doc.render(), {"rows_verified": len(q1["rows"])}


# ---------------------------------------------------------------------------
# Figure 6 (Q3): Weak rectangular pulse spectral nulls vs exact 2-level Rabi
# ---------------------------------------------------------------------------
def build_fig6_spectrum() -> tuple[str, dict[str, float]]:
    q3 = load_json("codes/systems/round71-expected-results.json")["results"]["q3"]
    df_ghz = q3["detuning_Hz"] * 1e-9  # 0.2 GHz = 0.2 / ns
    area = q3["omega_duration_rad"]    # 0.1 rad

    def p_first(ns: float) -> float:
        x = math.pi * df_ghz * ns
        sinc = math.sin(x) / x if abs(x) > 1e-14 else 1.0
        return (0.5 * area) ** 2 * sinc * sinc

    def p_exact_rabi(ns: float) -> float:
        omega = area / (ns * 1e-9)
        delta = 2.0 * math.pi * q3["detuning_Hz"]
        w_eff = math.hypot(omega, delta)
        return (omega / w_eff) ** 2 * (math.sin(0.5 * w_eff * ns * 1e-9) ** 2)

    for row in q3["rows"]:
        t_ns = float(row["duration_ns"])
        assert abs(p_first(t_ns) - row["first_order_probability"]) < 1e-12
        assert abs(p_exact_rabi(t_ns) - row["isolated_transition_exact_probability"]) < 1e-12
    assert abs(p_first(0.0) - 0.0025) < TOL
    assert p_first(5.0) < 1e-30 and p_first(10.0) < 1e-30 and p_first(15.0) < 1e-30

    doc = SvgDoc(
        title="矩形弱驱动脉冲的一阶频谱相消零点与精确两态 Rabi 对比",
        desc=(
            "固定弱驱动面积 Ω_ab·τ = 0.1 rad、失谐 δf = 200 MHz 的合成孤立两态模型："
            "左图绘制一阶跃迁概率 P^(1)(τ) = 0.0025·sinc²(π δf τ) 随时长 τ ∈ [0, 15] ns 的振荡曲线，"
            "标出 τ = 2.5 ns（1.013×10⁻³）及 5、10、15 ns 三处一阶谱零点；"
            "右表对比精确两态 Rabi 解，说明谱零点处高阶项仍非零且工程上需改用平滑包络加 DRAG。"
        ),
    )
    doc.add_header(
        "矩形弱脉冲的频谱相消：一阶谱零点与精确两态对比",
        f"合成孤立两态弱驱动模型 · 固定面积 Ω{sub('ab')}τ = 0.1 rad，失谐 δf = 200 MHz（非真实三能级门）",
        raw_sub=True,
    )
    doc.add_panel(28, 94, 634, 456, f"一阶跃迁概率 P{sup('(1)')}(τ) 随脉冲时长 τ 振荡曲线", raw_heading=True)
    doc.add_panel(678, 94, 294, 456, "一阶微扰与精确 Rabi 对比及工程边界")

    # --- Left Panel: sinc^2 curve ---
    px0, px1 = 104.0, 638.0
    py_top, py_bot = 178.0, 444.0
    t_max, p_hi = 15.2, 0.00275

    def gx(ns: float) -> float:
        return px0 + (ns / t_max) * (px1 - px0)

    def gy(p_val: float) -> float:
        return py_bot - (p_val / p_hi) * (py_bot - py_top)

    # Legend above plot
    doc.add('<line class="c1" stroke-width="2.6" x1="46" y1="152" x2="74" y2="152"/>')
    doc.add('<circle class="c1-fill" cx="60" cy="152" r="3.6"/>')
    doc.add(f'<text class="sm" x="80" y="156">一阶概率 P{sup("(1)")}(τ) = (0.1/2)² sinc²(π δf τ)</text>')

    doc.add(f'<polygon class="node-bg c2" stroke-width="2.2" points="{diamond_pts(406, 152, 4.8)}"/>')
    doc.add('<text class="sm" x="418" y="156">一阶谱零点（5, 10, 15 ns）</text>')

    # Grid & ticks
    for pv in (0.0, 0.0005, 0.0010, 0.0015, 0.0020, 0.0025):
        yp = gy(pv)
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(yp)}" x2="{fmt(px1)}" y2="{fmt(yp)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(px0 - 5)}" y1="{fmt(yp)}" x2="{fmt(px0)}" y2="{fmt(yp)}"/>')
        doc.add(f'<text class="xs" x="{fmt(px0 - 9)}" y="{fmt(yp + 4)}" text-anchor="end">{pv:.4f}</text>')
    for tv in (0, 2.5, 5, 7.5, 10, 12.5, 15):
        xt = gx(float(tv))
        is_null = tv in (5, 10, 15)
        cls_g = "c2" if is_null else "grid"
        extra = ' stroke-width="1.2" stroke-dasharray="5 4" stroke-opacity="0.65"' if is_null else ""
        doc.add(f'<line class="{cls_g}"{extra} x1="{fmt(xt)}" y1="{fmt(py_top)}" x2="{fmt(xt)}" y2="{fmt(py_bot)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(xt)}" y1="{fmt(py_bot)}" x2="{fmt(xt)}" y2="{fmt(py_bot + 5)}"/>')
        lbl_t = f"{tv:g}"
        doc.add(f'<text class="sm" x="{fmt(xt)}" y="{fmt(py_bot + 19)}" text-anchor="middle">{lbl_t}</text>')

    # Smooth exact sinc^2 curve (241 samples)
    n_s = 241
    pts_sp = [(gx(15.0 * i / (n_s - 1)), gy(p_first(15.0 * i / (n_s - 1)))) for i in range(n_s)]
    doc.add(f'<polygon class="area1" points="{pts_str([(px0, py_bot)] + pts_sp + [(gx(15.0), py_bot)])}"/>')
    doc.add(f'<path class="c1" stroke-width="2.6" d="{path_from_points(pts_sp)}"/>')

    # Key markers: tau=0, 2.5, and nulls 5, 10, 15
    doc.add(f'<circle class="c1-fill" cx="{fmt(gx(2.5))}" cy="{fmt(gy(p_first(2.5)))}" r="5.0"/>')
    for t_null in (5.0, 10.0, 15.0):
        doc.add(f'<polygon class="node-bg c2" stroke-width="2.4" points="{diamond_pts(gx(t_null), gy(0.0), 5.6)}"/>')

    # Non-overlapping callouts in wide-open upper-right whitespace
    doc.add('<rect class="pill-bg" x="152" y="184" width="166" height="24" rx="7"/>')
    doc.add('<text class="xsb c1-txt" x="235" y="200" text-anchor="middle">τ → 0 极限：0.0025</text>')
    doc.add(f'<line class="c1" stroke-width="1.2" x1="152" y1="198" x2="{fmt(gx(0.0) + 5)}" y2="{fmt(gy(0.0025))}"/>')

    doc.add('<rect class="c1-soft" x="230" y="264" width="166" height="38" rx="7"/>')
    doc.add('<text class="xsb c1-txt" x="313" y="280" text-anchor="middle">τ = 2.5 ns（π δf τ = π/2）</text>')
    doc.add(f'<text class="xs c1-txt" x="313" y="295" text-anchor="middle">P{sup("(1)")} ≈ 1.013 × 10⁻³</text>')
    doc.add(f'<line class="c1" stroke-width="1.2" x1="230" y1="292" x2="{fmt(gx(2.5) + 6)}" y2="{fmt(gy(p_first(2.5)) - 3)}"/>')

    doc.add('<rect class="c2-soft" x="414" y="264" width="212" height="40" rx="8"/>')
    doc.add('<text class="xsb c2-txt" x="520" y="280" text-anchor="middle">一阶谱零点：|δf|·τ = 1, 2, 3</text>')
    doc.add(f'<text class="xs c2-txt" x="520" y="296" text-anchor="middle">τ = 5, 10, 15 ns 处 P{sup("(1)")} = 0</text>')
    doc.add(f'<line class="c2" stroke-width="1.2" x1="455" y1="304" x2="{fmt(gx(10.0))}" y2="{fmt(gy(0.0) - 8)}"/>')
    doc.add(arrow_head(gx(10.0), gy(0.0) - 7, 0, 1, 6.0, "c2-fill"))

    # First sidelobe callout (tau ~= 7.15 ns, P ~= 1.18e-4)
    t_sl = 7.1515
    p_sl = p_first(t_sl)
    doc.add('<rect class="pill-bg" x="302" y="366" width="146" height="24" rx="7"/>')
    doc.add('<text class="xs" x="375" y="382" text-anchor="middle">首旁瓣 ≈ 1.18 × 10⁻⁴</text>')
    doc.add(f'<line class="guide" x1="358" y1="390" x2="{fmt(gx(t_sl))}" y2="{fmt(gy(p_sl) - 4)}"/>')

    # Axes & bottom strip
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px1 + 8)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(px1 + 10, py_bot, 1, 0))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(px0, py_top - 10, 0, -1))
    doc.add(f'<text class="lbl" x="{fmt(0.5 * (px0 + px1))}" y="486" text-anchor="middle">脉冲时长 τ (ns)</text>')
    doc.add(
        f'<text class="lbl" x="44" y="{fmt(0.5 * (py_top + py_bot))}" text-anchor="middle" '
        f'transform="rotate(-90 44 {fmt(0.5 * (py_top + py_bot))})">一阶跃迁概率 P{sup("(1)")}（无量纲）</text>'
    )
    doc.add('<rect class="pill" x="44" y="502" width="602" height="34" rx="8"/>')
    doc.add(
        f'<text class="sm" x="345" y="523" text-anchor="middle">'
        f'τ → 0 仅是固定面积下 Ω{sub("ab")} = 0.1/τ → ∞ 的数学极限；真实控制器幅度受硬件上限约束'
        f'</text>'
    )

    # --- Right Panel: Table & Engineering Boundary ---
    doc.add('<rect class="c1-soft" x="692" y="144" width="266" height="78" rx="10"/>')
    doc.add('<text class="smb c1-txt" x="706" y="164">① 频宽量级 1/τ 与谱零点</text>')
    doc.add('<text class="sm" x="706" y="186">矩形包络频谱第一零点：|δf|·τ = 1</text>')
    doc.add('<text class="sm" x="706" y="207">δf = 200 MHz ⇒ 首零点 τ = 5.0 ns</text>')

    # Quantitative comparison table
    doc.add('<rect class="panel" x="692" y="232" width="266" height="142" rx="10"/>')
    doc.add('<rect class="phead" x="693" y="233" width="264" height="28" rx="8"/>')
    doc.add('<text class="xsb" x="724" y="251" text-anchor="middle">τ (ns)</text>')
    doc.add(f'<text class="xsb c1-txt" x="802" y="251" text-anchor="middle">一阶 P{sup("(1)")}</text>')
    doc.add(f'<text class="xsb c2-txt" x="900" y="251" text-anchor="middle">精确 P{sub("exact")}</text>')

    q3_table = [
        ("2.5", "1.013×10⁻³", "1.012×10⁻³"),
        ("5.0", "0（零点）", "4.01×10⁻¹¹"),
        ("10.0", "0（零点）", "2.51×10⁻¹²"),
    ]
    for idx, (ts, s1, se) in enumerate(q3_table):
        yr = 286 + idx * 34
        if idx > 0:
            doc.add(f'<line class="grid" x1="700" y1="{yr - 20}" x2="950" y2="{yr - 20}"/>')
        doc.add(f'<text class="smb" x="724" y="{yr}" text-anchor="middle">{ts}</text>')
        doc.add(f'<text class="sm c1-txt" x="802" y="{yr}" text-anchor="middle">{s1}</text>')
        doc.add(f'<text class="smb c2-txt" x="900" y="{yr}" text-anchor="middle">{se}</text>')

    doc.add('<rect class="c2-soft" x="692" y="384" width="266" height="152" rx="10"/>')
    doc.add('<text class="smb c2-txt" x="706" y="405">② 工程边界：谱零点 ≠ 零泄漏保证</text>')
    doc.add('<text class="sm" x="706" y="428">• 高阶 Rabi 项在零点处仍严格非零</text>')
    doc.add('<text class="sm" x="706" y="450">• 真实 π 门含大幅 |0⟩↔|1⟩ 翻转</text>')
    doc.add('<text class="sm" x="706" y="472">• 线路滤波失真与频漂会挪动零点</text>')
    doc.add('<text class="smb c3-txt" x="706" y="496">工程方案：平滑包络（高斯/余弦）</text>')
    doc.add('<text class="smb c3-txt" x="706" y="517">+ DRAG 正交导数修正压制泄漏</text>')

    return doc.render(), {"p1_at_2p5": round(p_first(2.5), 7), "p_exact_at_5": p_exact_rabi(5.0)}


# ---------------------------------------------------------------------------
# Figure 7 (Q4): 1D rectangular barrier 3-region transmission & resonances
# ---------------------------------------------------------------------------
def build_fig7_barrier() -> tuple[str, dict[str, float]]:
    q4 = load_json("codes/algorithms/round71-results.json")["chapters"]["q4"]
    g_val = 4.0

    def transmission(e_val: float, g: float = g_val) -> float:
        z = g * math.sqrt(abs(1.0 - e_val))
        if e_val < 1.0:
            ratio = math.sinh(z) / z if z > 1e-14 else 1.0
        elif e_val > 1.0:
            ratio = math.sin(z) / z if z > 1e-14 else 1.0
        else:
            ratio = 1.0
        return 1.0 / (1.0 + g * g * ratio * ratio / (4.0 * e_val))

    def solve_4x4(mat: list[list[complex]], rhs: list[complex]) -> list[complex]:
        rows = [list(row) + [b] for row, b in zip(mat, rhs)]
        n = len(rows)
        for j in range(n):
            piv = max(range(j, n), key=lambda k: abs(rows[k][j]))
            rows[j], rows[piv] = rows[piv], rows[j]
            d = rows[j][j]
            rows[j] = [v / d for v in rows[j]]
            for k in range(n):
                if k != j:
                    fac = rows[k][j]
                    rows[k] = [v - fac * w for v, w in zip(rows[k], rows[j])]
        return [r[-1] for r in rows]

    def barrier_matching(e_val: float, g: float = g_val) -> tuple[float, float]:
        k = g * math.sqrt(e_val)
        z = g * math.sqrt(abs(1.0 - e_val))
        if e_val < 1.0:
            c_m, s_m, cp_m, sp_m = math.cosh(z), math.sinh(z) / z, z * math.sinh(z), math.cosh(z)
        elif e_val > 1.0:
            c_m, s_m, cp_m, sp_m = math.cos(z), math.sin(z) / z, -z * math.sin(z), math.cos(z)
        else:
            c_m, s_m, cp_m, sp_m = 1.0, 1.0, 0.0, 1.0
        wave = cmath.exp(1j * k)
        mat = [
            [1 + 0j, -1 + 0j, 0j, 0j],
            [-1j * k, 0j, -1 + 0j, 0j],
            [0j, complex(c_m), complex(s_m), -wave],
            [0j, complex(cp_m), complex(sp_m), -1j * k * wave],
        ]
        r_amp, _, _, t_amp = solve_4x4(mat, [-1 + 0j, -1j * k, 0j, 0j])
        return abs(t_amp) ** 2, abs(r_amp) ** 2

    for row in q4["cases"]:
        if row["g"] == 4:
            e_c = float(row["e"])
            t_c = transmission(e_c, 4.0)
            t_m, r_m = barrier_matching(e_c, 4.0)
            assert abs(t_c - row["T_closed"]) < 1e-10
            assert abs(t_m - t_c) < 1e-10 and abs(t_m + r_m - 1.0) < 1e-10

    e1_res = 1.0 + (math.pi / g_val) ** 2
    e2_res = 1.0 + (2.0 * math.pi / g_val) ** 2
    assert abs(transmission(1.0) - 0.2) < TOL
    assert abs(transmission(e1_res) - 1.0) < TOL
    assert abs(transmission(e2_res) - 1.0) < TOL

    doc = SvgDoc(
        title="一维矩形方势垒透射率：连续势垒顶与高能干涉共振",
        desc=(
            "宽度参数 g = L√(2mV₀)/ℏ = 4 的一维矩形方势垒精确透射率 T(e)（e = E/V₀，两侧势能与质量相等）："
            "e < 1 为指数衰减隧穿区，e = 1 势垒顶处严格连续且 T(1) = 1/5 = 0.20（80% 被反射），"
            "e > 1 为内部振荡干涉区，在 e₁ = 1 + π²/16 ≈ 1.61685 与 e₂ = 1 + π²/4 ≈ 3.46740 处达到完全透明 T = 1。"
        ),
    )
    doc.add_header(
        "一维矩形方势垒透射率：连续势垒顶与高能干涉共振（g = 4）",
        "定态单粒子精确解（两侧势能与质量相等）· 无量纲强度 g = L√(2mV₀)/ℏ = 4，传播矩阵核验全能区 R + T = 1",
    )
    doc.add_panel(28, 94, 638, 456, "透射率 T(e) 随无量纲能量 e = E/V₀ 变化曲线（g = 4）")
    doc.add_panel(682, 94, 290, 456, "三能区闭式解与定量特征（g = 4）")

    # --- Left Panel: Transmission curve ---
    px0, px1 = 94.0, 640.0
    py_top, py_bot = 178.0, 444.0
    e_hi, t_hi = 4.05, 1.12

    def gx(e_v: float) -> float:
        return px0 + (e_v / e_hi) * (px1 - px0)

    def gy(t_v: float) -> float:
        return py_bot - (t_v / t_hi) * (py_bot - py_top)

    # Legend above plot
    doc.add('<line class="c1" stroke-width="2.7" x1="46" y1="152" x2="74" y2="152"/>')
    doc.add('<text class="sm" x="80" y="156">透射率 T(e)（g = 4 精确解）</text>')

    doc.add('<circle class="node-bg c4" stroke-width="2.4" cx="268" cy="152" r="4.5"/>')
    doc.add('<text class="sm" x="279" y="156">势垒顶 e = 1 (T = 1/5)</text>')

    doc.add('<rect class="c3-fill" x="436" y="148" width="9" height="9" rx="1"/>')
    doc.add('<text class="sm" x="451" y="156">干涉共振峰 (T = 1)</text>')

    # Shaded Region I (0 < e < 1)
    x_e1 = gx(1.0)
    doc.add(f'<rect class="forbid" x="{fmt(px0)}" y="{fmt(py_top)}" width="{fmt(x_e1 - px0)}" height="{fmt(py_bot - py_top)}"/>')
    doc.add(f'<rect fill="url(#hatch-red)" x="{fmt(px0)}" y="{fmt(py_top)}" width="{fmt(x_e1 - px0)}" height="{fmt(py_bot - py_top)}"/>')

    # Grid & ticks
    for tv in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        yt = gy(tv)
        cls_g = "guide" if tv == 1.0 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(px0)}" y1="{fmt(yt)}" x2="{fmt(px1)}" y2="{fmt(yt)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(px0 - 5)}" y1="{fmt(yt)}" x2="{fmt(px0)}" y2="{fmt(yt)}"/>')
        doc.add(f'<text class="sm" x="{fmt(px0 - 9)}" y="{fmt(yt + 4)}" text-anchor="end">{tv:.1f}</text>')
    for ev in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0):
        xe = gx(ev)
        cls_g = "c4" if ev == 1.0 else "grid"
        extra = ' stroke-width="1.6" stroke-dasharray="6 4"' if ev == 1.0 else ""
        doc.add(f'<line class="{cls_g}"{extra} x1="{fmt(xe)}" y1="{fmt(py_top)}" x2="{fmt(xe)}" y2="{fmt(py_bot)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(xe)}" y1="{fmt(py_bot)}" x2="{fmt(xe)}" y2="{fmt(py_bot + 5)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xe)}" y="{fmt(py_bot + 19)}" text-anchor="middle">{ev:g}</text>')

    # Sample exact transmission curve (221 points including exact feature points)
    es_grid = sorted(set(
        [0.04 + (4.0 - 0.04) * i / 220.0 for i in range(221)]
        + [0.5, 1.0, e1_res, e2_res]
    ))
    t_pts = [(gx(e_v), gy(transmission(e_v))) for e_v in es_grid]
    doc.add(f'<polygon class="area1" points="{pts_str([(gx(0.04), py_bot)] + t_pts + [(gx(4.0), py_bot)])}"/>')
    doc.add(f'<path class="c1" stroke-width="2.8" d="{path_from_points(t_pts)}"/>')

    # Feature markers
    y_top_b = gy(0.2)
    y_t1 = gy(1.0)
    doc.add(f'<circle class="node-bg c4" stroke-width="2.8" cx="{fmt(x_e1)}" cy="{fmt(y_top_b)}" r="5.5"/>')
    doc.add(f'<rect class="c3-fill" x="{fmt(gx(e1_res) - 5)}" y="{fmt(y_t1 - 5)}" width="10" height="10" rx="1.5"/>')
    doc.add(f'<rect class="c3-fill" x="{fmt(gx(e2_res) - 5)}" y="{fmt(y_t1 - 5)}" width="10" height="10" rx="1.5"/>')

    # Non-overlapping callouts in verified empty regions
    doc.add('<rect class="c2-soft" x="104" y="188" width="116" height="38" rx="7"/>')
    doc.add('<text class="xsb c2-txt" x="162" y="204" text-anchor="middle">能区 I (e &lt; 1)</text>')
    doc.add('<text class="xs c2-txt" x="162" y="219" text-anchor="middle">指数隧穿衰减区</text>')

    doc.add('<rect class="c3-soft" x="304" y="266" width="174" height="38" rx="7"/>')
    doc.add('<text class="xsb c3-txt" x="391" y="282" text-anchor="middle">共振 ℓ=1：e₁ ≈ 1.61685</text>')
    doc.add('<text class="xs c3-txt" x="391" y="297" text-anchor="middle">qL = π，T = 1（全透射）</text>')
    doc.add(f'<line class="c3" stroke-width="1.3" x1="330" y1="266" x2="{fmt(gx(e1_res))}" y2="{fmt(y_t1 + 7)}"/>')

    doc.add('<rect class="c3-soft" x="454" y="320" width="176" height="38" rx="7"/>')
    doc.add('<text class="xsb c3-txt" x="542" y="336" text-anchor="middle">共振 ℓ=2：e₂ ≈ 3.46740</text>')
    doc.add('<text class="xs c3-txt" x="542" y="351" text-anchor="middle">qL = 2π，T = 1（全透射）</text>')
    doc.add(f'<line class="c3" stroke-width="1.3" x1="556" y1="320" x2="{fmt(gx(e2_res))}" y2="{fmt(y_t1 + 7)}"/>')

    doc.add('<rect class="c4-soft" x="266" y="380" width="194" height="38" rx="7"/>')
    doc.add('<text class="xsb c4-txt" x="363" y="396" text-anchor="middle">势垒顶 (e = 1)：T = 1/5 = 0.20</text>')
    doc.add('<text class="xs c4-txt" x="363" y="411" text-anchor="middle">严格连续，但仍有 80% 被反射</text>')
    doc.add(f'<line class="c4" stroke-width="1.3" x1="266" y1="397" x2="{fmt(x_e1 + 7)}" y2="{fmt(y_top_b)}"/>')

    # Axes & bottom summary
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px1 + 8)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(px1 + 10, py_bot, 1, 0))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(px0, py_top - 10, 0, -1))
    doc.add(f'<text class="lbl" x="{fmt(0.5 * (px0 + px1))}" y="486" text-anchor="middle">无量纲能量比 e = E / V₀（无量纲）</text>')
    doc.add(
        f'<text class="lbl" x="46" y="{fmt(0.5 * (py_top + py_bot))}" text-anchor="middle" '
        f'transform="rotate(-90 46 {fmt(0.5 * (py_top + py_bot))})">透射率 T（概率流之比，无量纲）</text>'
    )
    doc.add('<rect class="pill" x="44" y="502" width="606" height="34" rx="8"/>')
    doc.add('<text class="sm" x="347" y="523" text-anchor="middle">低于势垒顶为衰减隧穿；高于势垒顶为内部振荡波，势垒宽装下整数半波长时边界反射相消</text>')

    # --- Right Panel: 3-region formulas & values ---
    doc.add('<rect class="c2-soft" x="696" y="144" width="262" height="86" rx="10"/>')
    doc.add('<text class="smb c2-txt" x="710" y="164">能区 I：0 &lt; e &lt; 1（指数隧穿）</text>')
    doc.add('<text class="sm" x="710" y="185">衰减相位 κL = g√(1−e)</text>')
    doc.add('<text class="sm" x="710" y="205">T = [1 + sinh²(κL)/(4e(1−e))]⁻¹</text>')
    doc.add('<text class="xs" x="710" y="222">势垒内增长与衰减两支指数缺一不可</text>')

    doc.add('<rect class="c4-soft" x="696" y="238" width="262" height="74" rx="10"/>')
    doc.add('<text class="smb c4-txt" x="710" y="258">能区 II：e = 1（临界线性解）</text>')
    doc.add('<text class="sm" x="710" y="280">T(1) = 1 / (1 + g²/4) = 1/5 = 0.20</text>')
    doc.add('<text class="xs" x="710" y="300">左右极限严格连续，恒满足 T(1) &lt; 1</text>')

    doc.add('<rect class="c3-soft" x="696" y="320" width="262" height="90" rx="10"/>')
    doc.add('<text class="smb c3-txt" x="710" y="340">能区 III：e &gt; 1（边界干涉共振）</text>')
    doc.add('<text class="sm" x="710" y="361">振荡相位 qL = g√(e−1)</text>')
    doc.add('<text class="sm" x="710" y="381">T = [1 + sin²(qL)/(4e(e−1))]⁻¹</text>')
    doc.add(f'<text class="xs" x="710" y="400">qL = ℓπ ⇒ e{sub("ℓ")} = 1 + (ℓπ/g)² 处 T = 1</text>')

    doc.add('<rect class="pill" x="696" y="418" width="262" height="118" rx="10"/>')
    doc.add('<text class="smb" x="710" y="438">关键特征点核验（R + T = 1）</text>')
    doc.add('<text class="sm" x="710" y="460">• e = 0.50：T = 0.0139，R = 0.9861</text>')
    doc.add('<text class="sm" x="710" y="481">• e = 1.00：T = 0.2000，R = 0.8000</text>')
    doc.add('<text class="sm c3-txt" x="710" y="502">• e₁ = 1.61685：T = 1.0000（ℓ = 1）</text>')
    doc.add('<text class="sm c3-txt" x="710" y="523">• e₂ = 3.46740：T = 1.0000（ℓ = 2）</text>')

    return doc.render(), {"t_top": transmission(1.0), "e1_res": round(e1_res, 5), "e2_res": round(e2_res, 5)}


# ---------------------------------------------------------------------------
# XML well-formedness & margin validation
# ---------------------------------------------------------------------------
def verify_svg_xml(svg_text: str, filename: str) -> dict[str, int]:
    root = ET.fromstring(svg_text)
    vb = root.attrib.get("viewBox", "")
    assert vb == f"0 0 {W} {H}", f"{filename}: unexpected viewBox {vb!r}"
    assert ":root{color-scheme:light dark}" in svg_text, f"{filename}: missing light/dark color-scheme"
    assert "@media(prefers-color-scheme:dark)" in svg_text, f"{filename}: missing dark mode media query"
    assert "round 7" not in svg_text.lower() and "round7" not in svg_text.lower(), f"{filename}: residual Round 7x string"

    ns = {"svg": "http://www.w3.org/2000/svg"}
    title_el = root.find("svg:title", ns)
    desc_el = root.find("svg:desc", ns)
    assert title_el is not None and (title_el.text or "").strip(), f"{filename}: missing <title>"
    assert desc_el is not None and (desc_el.text or "").strip(), f"{filename}: missing <desc>"

    text_nodes = root.findall(".//svg:text", ns)
    assert len(text_nodes) >= 15, f"{filename}: too few text elements"
    for el in text_nodes:
        x = float(el.attrib["x"])
        y = float(el.attrib["y"])
        assert MARGIN <= x <= W - MARGIN, f"{filename}: text x={x} violates margin ({el.text!r})"
        assert MARGIN <= y <= H - MARGIN, f"{filename}: text y={y} violates margin ({el.text!r})"

    return {"text_count": len(text_nodes), "bytes": len(svg_text.encode("utf-8"))}


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    builders = [
        ("round70-foundations-tomography.svg", build_fig1_tomography),
        ("round70-amplitude-aliasing.svg", build_fig2_aliasing),
        ("round70-systems-cutoff.svg", build_fig3_cutoff),
        ("round70-chain-strength.svg", build_fig4_chain_strength),
        ("round71-foundations-eraser.svg", build_fig5_eraser),
        ("round71-systems-spectrum.svg", build_fig6_spectrum),
        ("round71-barrier-transmission.svg", build_fig7_barrier),
    ]
    for fname, fn in builders:
        svg_text, metrics = fn()
        check = verify_svg_xml(svg_text, fname)
        out_path = ASSETS_DIR / fname
        out_path.write_text(svg_text, encoding="utf-8")
        print(f"[OK] {fname}: {check['bytes']} bytes ({check['bytes']/1024:.1f} KB), {check['text_count']} text labels | {metrics}")


if __name__ == "__main__":
    main()
