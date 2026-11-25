#!/usr/bin/env python3
"""Upgrade 7 legacy Matplotlib/pathified SVG figures in-place (V3 Part 2) using Python 3 stdlib.

Rebuilds these 7 figures in handbook/assets/ (exact filenames preserved) directly from
archived JSON/CSV outputs and exact analytical formulas, with pure <text> elements,
Chinese scientific labels, and @media (prefers-color-scheme: dark) dual themes:
  1. round72-systems-qec.svg      (Ch 10: d=3,5,7 X-memory circuit-level MWPM + 95% exact CI)
  2. round73-systems-qec.svg      (Ch 10: 18-point X/Z 7-round ordinary vs correlated MWPM)
  3. round72-systems-control.svg  (Ch 14: 2-level GRAPE waveform, 1 ns filter & 3-7 MHz sweep)
  4. round73-systems-control.svg  (Ch 14: 3-level GRAPE waveform, 1 ns filter & |2> leakage)
  5. round72-algorithms.svg       (Ch 16: P3 CTQW, symmetric QSP cubic, Fock cutoff tail)
  6. round73-algorithms.svg       (Ch 16: signed off-grid HHL QPE errors & 16-vertex SKW walk)
  7. lab-zero-failure.svg         (Ch 15/Lab: exact one-sided 95% zero-failure bound vs N)

Run (Python 3 standard library only):
  python3 codes/practice/upgrade_legacy_svgs_part2.py

Optional Playwright + System Chrome dual-theme getBBox() audit & PNG screenshots:
  python3 codes/practice/upgrade_legacy_svgs_part2.py --check-bbox --screenshots /tmp/v3_legacy_p2
"""

from __future__ import annotations

import argparse
import cmath
import csv
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT / "handbook" / "assets"
W, H = 1000, 580
MARGIN = 30
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

COMMON_CSS = """
:root{color-scheme:light dark}
text{font-family:system-ui,-apple-system,'PingFang SC','Microsoft YaHei',sans-serif}
.bg{fill:#f8fafc}
.panel{fill:#ffffff;stroke:#cbd5e1;stroke-width:1.4}
.phead{fill:#eef4f8}
.title{font-size:19.5px;font-weight:700;fill:#13263a}
.subtitle{font-size:13px;font-weight:400;fill:#3e566d}
.sec{font-size:14.5px;font-weight:700;fill:#13263a}
.lbl{font-size:13px;font-weight:500;fill:#19324d}
.lblb{font-size:13px;font-weight:700;fill:#13263a}
.sm{font-size:12px;font-weight:400;fill:#3e566d}
.smb{font-size:12px;font-weight:600;fill:#19324d}
.xs{font-size:11px;font-weight:400;fill:#3e566d}
.xsb{font-size:11px;font-weight:600;fill:#19324d}
.axis{stroke:#19324d;stroke-width:1.65;fill:none}
.axis-fill{fill:#19324d}
.grid{stroke:#dce5ee;stroke-width:1;fill:none}
.grid-minor{stroke:#e9eff5;stroke-width:0.8;stroke-dasharray:3 3;fill:none}
.guide{stroke:#7c93a8;stroke-width:1.25;stroke-dasharray:5 4;fill:none}
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
.pill-bg{fill:#ffffff;fill-opacity:.95;stroke:#9cb1c4;stroke-width:1.15}
.area3{fill:#1e7a5c;fill-opacity:.10}
.bar1{fill:#2678b5;fill-opacity:.86;stroke:#155585;stroke-width:1.3}
.bar2{fill:#d96248;fill-opacity:.82;stroke:#a63824;stroke-width:1.3}
.hollow-c1{fill:#ffffff;stroke:#1b6ca8;stroke-width:2.0}
.hollow-c2{fill:#ffffff;stroke:#c74b34;stroke-width:2.1}
.hollow-c3{fill:#ffffff;stroke:#1e7a5c;stroke-width:2.0}
.hollow-c4{fill:#ffffff;stroke:#b57614;stroke-width:2.1}
.hatch-bar{stroke:#ffffff;stroke-width:1.4;stroke-opacity:.55}
@media(prefers-color-scheme:dark){
  .bg{fill:#0f1720}
  .panel{fill:#16222e;stroke:#354c61}
  .phead{fill:#1c2d3d}
  .title,.sec,.lblb{fill:#eef6ff}
  .subtitle,.sm,.xs{fill:#b7cde0}
  .lbl,.smb,.xsb{fill:#d7e7f5}
  .axis{stroke:#cde0f2}
  .axis-fill{fill:#cde0f2}
  .grid{stroke:#293e52}
  .grid-minor{stroke:#213344}
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
  .c4-soft{fill:#3d3014;stroke:#f0ba5a}
  .note{fill:#332914;stroke:#d6a240}
  .pill{fill:#1c2c3b;stroke:#4f6b85}
  .pill-bg{fill:#16222e;fill-opacity:.95;stroke:#4f6b85}
  .area3{fill:#5dd1a8;fill-opacity:.14}
  .bar1{fill:#49a4df;fill-opacity:.88;stroke:#8fd4fa}
  .bar2{fill:#e47660;fill-opacity:.85;stroke:#f8a896}
  .hollow-c1{fill:#16222e;stroke:#6bc2f5}
  .hollow-c2{fill:#16222e;stroke:#f28872}
  .hollow-c3{fill:#16222e;stroke:#5dd1a8}
  .hollow-c4{fill:#16222e;stroke:#f0ba5a}
  .hatch-bar{stroke:#0f1720;stroke-opacity:.42}
}
""".strip()


def fmt(v: float) -> str:
    s = f"{v:.2f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def sub(txt: str) -> str:
    return f'<tspan dy="3" font-size="74%">{escape(txt)}</tspan><tspan dy="-3">&#8203;</tspan>'


def sup(txt: str) -> str:
    return f'<tspan dy="-4.5" font-size="74%">{escape(txt)}</tspan><tspan dy="4.5">&#8203;</tspan>'


def pts_str(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{fmt(x)},{fmt(y)}" for x, y in points)


def path_from_points(points: list[tuple[float, float]]) -> str:
    if not points:
        return ""
    head = f"M {fmt(points[0][0])} {fmt(points[0][1])}"
    tail = " ".join(f"L {fmt(x)} {fmt(y)}" for x, y in points[1:])
    return f"{head} {tail}".strip()


def step_path_post(ts: list[float], ys: list[float], t_end: float) -> list[tuple[float, float]]:
    """Build piecewise-constant post-step coordinates [(t0, y0), (t1, y0), (t1, y1), ...]."""
    assert len(ts) == len(ys) and len(ts) > 0
    pts: list[tuple[float, float]] = [(ts[0], ys[0])]
    for i in range(len(ts) - 1):
        pts.append((ts[i + 1], ys[i]))
        pts.append((ts[i + 1], ys[i + 1]))
    pts.append((t_end, ys[-1]))
    return pts


def diamond_pts(cx: float, cy: float, r: float) -> str:
    return pts_str([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)])


def tri_up_pts(cx: float, cy: float, r: float) -> str:
    return pts_str([(cx, cy - r), (cx + r * 0.92, cy + r * 0.78), (cx - r * 0.92, cy + r * 0.78)])


def tri_dn_pts(cx: float, cy: float, r: float) -> str:
    return pts_str([(cx, cy + r), (cx + r * 0.92, cy - r * 0.78), (cx - r * 0.92, cy - r * 0.78)])


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
            '<pattern id="hatch-bar" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<line class="hatch-bar" x1="0" y1="0" x2="0" y2="7"/></pattern>',
        ]
        self.body: list[str] = []

    def add(self, snippet: str) -> None:
        self.body.append(snippet)

    def add_header(self, title_text: str, subtitle_text: str, *, raw_sub: bool = False) -> None:
        self.add(f'<rect class="bg" width="{self.w}" height="{self.h}" rx="20"/>')
        self.add(f'<text class="title" x="34" y="52">{escape(title_text)}</text>')
        s_out = subtitle_text if raw_sub else escape(subtitle_text)
        self.add(f'<text class="subtitle" x="34" y="77">{s_out}</text>')

    def add_panel(self, x: float, y: float, w: float, h: float, heading: str) -> None:
        self.add(f'<rect class="panel" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="14"/>')
        self.add(
            f'<path class="phead" d="M {fmt(x + 14)} {fmt(y + 1)} H {fmt(x + w - 14)} '
            f'Q {fmt(x + w - 1)} {fmt(y + 1)} {fmt(x + w - 1)} {fmt(y + 14)} V {fmt(y + 38)} '
            f'H {fmt(x + 1)} V {fmt(y + 14)} Q {fmt(x + 1)} {fmt(y + 1)} {fmt(x + 14)} {fmt(y + 1)} Z"/>'
        )
        self.add(f'<line class="grid" x1="{fmt(x + 1)}" y1="{fmt(y + 38)}" x2="{fmt(x + w - 1)}" y2="{fmt(y + 38)}"/>')
        self.add(f'<text class="sec" x="{fmt(x + 16)}" y="{fmt(y + 24)}">{escape(heading)}</text>')

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
# Figure 1: round72-systems-qec.svg
# ---------------------------------------------------------------------------
def build_fig1_round72_qec() -> tuple[str, dict[str, object]]:
    src = ROOT / "codes" / "systems" / "sdk" / "stim-matching-results.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    rows = [r for r in data["cases"] if r["noise_each"] > 0]
    assert len(rows) == 3 and [r["distance"] for r in rows] == [3, 5, 7]
    assert [r["failures"] for r in rows] == [13, 2, 0]
    # Exact two-sided 95% Clopper-Pearson upper bound at k=0, N=20000: 1 - 0.025^(1/20000)
    expected_hi7 = -math.expm1(math.log(0.025) / rows[2]["shots"])
    assert math.isclose(rows[2]["exact_binomial_95"][1], expected_hi7, rel_tol=1e-12)
    for r in rows:
        lo, hi = r["exact_binomial_95"]
        assert lo <= r["p_experiment"] <= hi

    doc = SvgDoc(
        title="旋转表面码电路级抽样与 MWPM 解码：三种码距完整存储失败率与 95% 精确二项区间",
        desc=(
            "基于 Stim 与 PyMatching 归档数据绘制旋转表面码在合成 Pauli 电路级噪声 p = 0.001、"
            "X 基存储（轮数等于码距 d）、每点 N = 20,000 次独立抽样下的完整存储失败概率 q 及其双侧 95% 精确 Clopper-Pearson 区间。"
            "d = 3 为 13/20,000，d = 5 为 2/20,000，d = 7 为 0/20,000 并以空心下三角和向下箭头标示 95% 统计上界 1.84e-4。"
        ),
    )
    doc.add_header(
        "旋转表面码电路级抽样与 MWPM：三种码距 95% 精确二项区间",
        "合成 Pauli 电路级噪声 p = 0.001（X 基存储，轮数 = d，每点 N = 20,000 次独立完整电路抽样）",
    )
    doc.add_panel(28, 96, 944, 456, "完整 X 基存储失败概率 q（对数纵轴，双侧 95% 精确 Clopper–Pearson 区间）")

    px0, px1 = 126.0, 624.0
    py0, py1 = 434.0, 162.0
    d_min, d_max = 2.1, 7.9
    ly_min, ly_max = -6.0, -2.4  # 10^-6 to ~4e-3

    def map_d(d_val: float) -> float:
        return px0 + (d_val - d_min) / (d_max - d_min) * (px1 - px0)

    def map_q(q_val: float) -> float:
        return py0 - (math.log10(q_val) - ly_min) / (ly_max - ly_min) * (py0 - py1)

    # Minor horizontal gridlines (3e-6, 3e-5, 3e-4, 3e-3)
    for exp_v in (-6, -5, -4, -3):
        ym = map_q(3.0 * (10.0 ** exp_v))
        if py1 <= ym <= py0:
            doc.add(f'<line class="grid-minor" x1="{fmt(px0)}" y1="{fmt(ym)}" x2="{fmt(px1)}" y2="{fmt(ym)}"/>')

    # Major Y ticks & gridlines
    for exp_v in (-6, -5, -4, -3):
        yt = map_q(10.0 ** exp_v)
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(yt)}" x2="{fmt(px1)}" y2="{fmt(yt)}"/>')
        doc.add(f'<text class="sm" x="{fmt(px0 - 10)}" y="{fmt(yt + 4)}" text-anchor="end">10{sup(str(exp_v))}</text>')

    # X ticks & gridlines
    for d_val in (3, 5, 7):
        xd = map_d(float(d_val))
        doc.add(f'<line class="grid" x1="{fmt(xd)}" y1="{fmt(py1)}" x2="{fmt(xd)}" y2="{fmt(py0)}"/>')
        doc.add(f'<text class="smb" x="{fmt(xd)}" y="{fmt(py0 + 20)}" text-anchor="middle">d = {d_val}（{d_val} 轮）</text>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px1 + 8)}" y2="{fmt(py0)}"/>')
    doc.add(arrow_head(px1 + 8, py0, 1, 0))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px0)}" y2="{fmt(py1 - 10)}"/>')
    doc.add(arrow_head(px0, py1 - 10, 0, -1))
    doc.add(f'<text class="lbl" x="{fmt(0.5 * (px0 + px1))}" y="478" text-anchor="middle">码距 d（存储轮数 = d；物理比特数 2d² − 1 = 17, 49, 97）</text>')
    doc.add(
        f'<text class="lbl" x="58" y="{fmt(0.5 * (py0 + py1))}" text-anchor="middle" '
        f'transform="rotate(-90 58 {fmt(0.5 * (py0 + py1))})">每次完整 X 基存储失败概率 q（无量纲）</text>'
    )

    # Plot each archived distance point
    for r in rows:
        d_val = float(r["distance"])
        xd = map_d(d_val)
        q_est = r["p_experiment"]
        lo, hi = r["exact_binomial_95"]
        y_hi = map_q(hi)
        if q_est > 0:
            y_est = map_q(q_est)
            y_lo = map_q(lo)
            doc.add(f'<line class="c1" stroke-width="2.4" x1="{fmt(xd)}" y1="{fmt(y_lo)}" x2="{fmt(xd)}" y2="{fmt(y_hi)}"/>')
            doc.add(f'<line class="c1" stroke-width="2.2" x1="{fmt(xd - 8)}" y1="{fmt(y_hi)}" x2="{fmt(xd + 8)}" y2="{fmt(y_hi)}"/>')
            doc.add(f'<line class="c1" stroke-width="2.2" x1="{fmt(xd - 8)}" y1="{fmt(y_lo)}" x2="{fmt(xd + 8)}" y2="{fmt(y_lo)}"/>')
            doc.add(f'<circle class="c1-fill" cx="{fmt(xd)}" cy="{fmt(y_est)}" r="6.2"/>')
            doc.add(f'<text class="smb c1-txt" x="{fmt(xd)}" y="{fmt(y_hi - 24)}" text-anchor="middle">{r["failures"]} / 20,000</text>')
            doc.add(f'<text class="xs c1-txt" x="{fmt(xd)}" y="{fmt(y_hi - 9)}" text-anchor="middle">q̂ = {q_est:.2e}</text>')
        else:
            # Zero observed failures: hollow upper-bound triangle + downward arrow
            y_arrow_end = map_q(1.5e-6)
            doc.add(f'<line class="c2" stroke-width="2.2" x1="{fmt(xd)}" y1="{fmt(y_hi + 8)}" x2="{fmt(xd)}" y2="{fmt(y_arrow_end)}"/>')
            doc.add(arrow_head(xd, y_arrow_end + 2, 0, 1, 7.5, "c2-fill"))
            doc.add(f'<polygon class="hollow-c2" points="{tri_dn_pts(xd, y_hi, 7.5)}"/>')
            doc.add(f'<text class="smb c2-txt" x="{fmt(xd)}" y="{fmt(y_hi - 42)}" text-anchor="middle">0 / 20,000（上界标记）</text>')
            doc.add(f'<text class="xs c2-txt" x="{fmt(xd)}" y="{fmt(y_hi - 27)}" text-anchor="middle">95% 上界 {hi:.2e}</text>')
            doc.add(f'<text class="xs" x="{fmt(xd)}" y="{fmt(y_hi - 12)}" text-anchor="middle">点估计为 0，未绘于对数轴</text>')

    # Right summary card inside panel
    doc.add('<rect class="pill" x="648" y="154" width="308" height="326" rx="10"/>')
    doc.add('<text class="smb" x="664" y="177">图例与归档计数摘要</text>')
    doc.add('<line class="c1" stroke-width="2.2" x1="672" y1="192" x2="672" y2="210"/>')
    doc.add('<line class="c1" stroke-width="2.0" x1="667" y1="192" x2="677" y2="192"/>')
    doc.add('<line class="c1" stroke-width="2.0" x1="667" y1="210" x2="677" y2="210"/>')
    doc.add('<circle class="c1-fill" cx="672" cy="201" r="4.5"/>')
    doc.add('<text class="sm" x="690" y="205">失败频率与双侧 95% 精确区间</text>')
    doc.add(f'<polygon class="hollow-c2" points="{tri_dn_pts(672, 227, 6.2)}"/>')
    doc.add('<text class="sm" x="690" y="231">零失败 95% 统计上界（向下箭头）</text>')
    doc.add('<line class="grid" x1="662" y1="246" x2="942" y2="246"/>')

    y_row = 270.0
    for r in rows:
        lo, hi = r["exact_binomial_95"]
        q_str = f"{r['p_experiment']:.2e}" if r["failures"] > 0 else "0"
        ci_str = f"[{lo:.2e}, {hi:.2e}]" if lo > 0 else f"[0, {hi:.2e}]"
        doc.add(f'<text class="smb" x="664" y="{fmt(y_row)}">d = {r["distance"]}（{r["rounds"]} 轮，{r["detectors"]} 检测器，q̂ = {q_str}）</text>')
        doc.add(f'<text class="xs" x="664" y="{fmt(y_row + 18)}">失败 {r["failures"]}/20,000 · 95% CI {ci_str}</text>')
        y_row += 52.0

    doc.add('<line class="grid" x1="662" y1="422" x2="942" y2="422"/>')
    doc.add('<text class="xs" x="664" y="444">零噪声自检（d = 3, p = 0, N = 1,000）：0 次失败</text>')
    doc.add('<text class="xs" x="664" y="464">解码器：PyMatching 离线批处理 MWPM</text>')

    # Bottom takeaway note inside panel
    doc.add('<rect class="note" x="44" y="496" width="912" height="40" rx="9"/>')
    doc.add(
        '<text class="sm" x="500" y="520" text-anchor="middle">'
        '口径说明：本图报告的是完整 d 轮存储失败率 q，而非每周期逻辑错误率，亦未拟合纠错阈值；零失败仅给出正统计上界。'
        '</text>'
    )
    return doc.render(), {"d_failures": {r["distance"]: r["failures"] for r in rows}}


# ---------------------------------------------------------------------------
# Figure 2: round73-systems-qec.svg
# ---------------------------------------------------------------------------
def build_fig2_round73_qec() -> tuple[str, dict[str, object]]:
    src = ROOT / "codes" / "systems" / "sdk73" / "qec-grid-results.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    cases = data["cases"]
    assert len(cases) == 18
    for c in cases:
        assert c["rounds"] == 7 and c["shots"] == 10000
        for dec in ("ordinary", "correlated"):
            rate = c[f"{dec}_failures"] / c["shots"]
            lo, hi = c[f"{dec}_simultaneous_ci"]
            assert lo - 1e-12 <= rate <= hi + 1e-12

    # Spot-check key counts cited in Ch 10
    lookup = {(c["basis"], c["distance"], c["noise_each"]): c for c in cases}
    assert lookup[("x", 7, 0.006)]["ordinary_failures"] == 237
    assert lookup[("x", 7, 0.006)]["correlated_failures"] == 124
    assert lookup[("z", 3, 0.003)]["ordinary_failures"] == 136
    assert lookup[("z", 3, 0.003)]["correlated_failures"] == 177

    doc = SvgDoc(
        title="固定 7 轮旋转表面码双基对照：普通 MWPM 与相关匹配（18 工况点）",
        desc=(
            "基于 Stim 与 PyMatching 同样本配对实跑数据绘制 X 基与 Z 基固定 7 轮存储、码距 d = 3, 5, 7、"
            "电路级噪声 p = 0.001, 0.003, 0.006 共 18 个工况点（每点 10,000 次抽样）的完整存储失败率，"
            "实线为普通匹配，虚线为相关匹配，36 项错误率均附 Bonferroni 同时 95% 区间（α = 0.05/36）。"
        ),
    )
    doc.add_header(
        "固定 7 轮旋转表面码双基对照：普通 MWPM 与相关匹配",
        "同样本配对解码（18 工况点 × 10,000 次抽样）；误差棒为 36 项错误率 Bonferroni 同时 95% 区间（α = 0.05/36）",
    )

    panels = [
        ("x", 28.0, "X 基存储（7 轮，主检相位破坏）", "实线 = 普通 MWPM · 虚线 = 相关匹配（enable_correlations）"),
        ("z", 508.0, "Z 基存储（7 轮，主检位翻转）", "小码距 d = 3 Z 基三点相关匹配计数反高于普通匹配"),
    ]
    p_min, p_max = 0.0004, 0.0066
    y_min, y_max = -0.0025, 0.0725
    py0, py1 = 434.0, 158.0

    dist_styles = {
        3: ("c1", "circle", "square"),
        5: ("c2", "tri_up", "tri_dn"),
        7: ("c3", "diamond", "hollow_diamond"),
    }

    def draw_marker(cx: float, cy: float, cls: str, shape: str) -> str:
        if shape == "circle":
            return f'<circle class="{cls}-fill" cx="{fmt(cx)}" cy="{fmt(cy)}" r="4.3"/>'
        if shape == "square":
            return f'<rect class="{cls}-fill" x="{fmt(cx - 3.8)}" y="{fmt(cy - 3.8)}" width="7.6" height="7.6" rx="1"/>'
        if shape == "tri_up":
            return f'<polygon class="{cls}-fill" points="{tri_up_pts(cx, cy, 4.9)}"/>'
        if shape == "tri_dn":
            return f'<polygon class="{cls}-fill" points="{tri_dn_pts(cx, cy, 4.9)}"/>'
        if shape == "diamond":
            return f'<polygon class="{cls}-fill" points="{diamond_pts(cx, cy, 4.9)}"/>'
        return f'<polygon class="hollow-{cls}" points="{diamond_pts(cx, cy, 4.9)}"/>'

    for basis, panel_x, heading, foot_txt in panels:
        doc.add_panel(panel_x, 96, 464, 456, heading)
        px0 = panel_x + 74.0
        px1 = panel_x + 444.0

        def map_p(pv: float) -> float:
            return px0 + (pv - p_min) / (p_max - p_min) * (px1 - px0)

        def map_y(yv: float) -> float:
            return py0 - (yv - y_min) / (y_max - y_min) * (py0 - py1)

        # Minor & major Y gridlines
        for yt_v in (0.01, 0.03, 0.05, 0.07):
            ym = map_y(yt_v)
            doc.add(f'<line class="grid-minor" x1="{fmt(px0)}" y1="{fmt(ym)}" x2="{fmt(px1)}" y2="{fmt(ym)}"/>')
        for yt_v in (0.00, 0.02, 0.04, 0.06):
            yt = map_y(yt_v)
            doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(yt)}" x2="{fmt(px1)}" y2="{fmt(yt)}"/>')
            doc.add(f'<text class="sm" x="{fmt(px0 - 8)}" y="{fmt(yt + 4)}" text-anchor="end">{yt_v:.2f}</text>')

        # X ticks & gridlines
        for pt_v in (0.001, 0.003, 0.006):
            xt = map_p(pt_v)
            doc.add(f'<line class="grid" x1="{fmt(xt)}" y1="{fmt(py1)}" x2="{fmt(xt)}" y2="{fmt(py0)}"/>')
            doc.add(f'<text class="sm" x="{fmt(xt)}" y="{fmt(py0 + 18)}" text-anchor="middle">{pt_v:.3f}</text>')

        # Axes
        doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px1 + 7)}" y2="{fmt(py0)}"/>')
        doc.add(arrow_head(px1 + 7, py0, 1, 0, 7.0))
        doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px0)}" y2="{fmt(py1 - 8)}"/>')
        doc.add(arrow_head(px0, py1 - 8, 0, -1, 7.0))
        doc.add(f'<text class="lbl" x="{fmt(0.5 * (px0 + px1))}" y="476" text-anchor="middle">电路级噪声参数 p（无量纲）</text>')
        yl_x = panel_x + 22.0
        doc.add(
            f'<text class="lbl" x="{fmt(yl_x)}" y="{fmt(0.5 * (py0 + py1))}" text-anchor="middle" '
            f'transform="rotate(-90 {fmt(yl_x)} {fmt(0.5 * (py0 + py1))})">完整 7 轮存储失败率 k / N</text>'
        )

        # Plot 6 series (d=3,5,7 x ordinary/correlated)
        for dist in (3, 5, 7):
            cls, sh_ord, sh_cor = dist_styles[dist]
            rows_d = sorted([r for r in cases if r["basis"] == basis and r["distance"] == dist], key=lambda r: r["noise_each"])
            for dec, dash, offset, shape in (
                ("ordinary", "", -0.00010, sh_ord),
                ("correlated", ' stroke-dasharray="6 4"', 0.00010, sh_cor),
            ):
                pts: list[tuple[float, float]] = []
                for r in rows_d:
                    xv = map_p(r["noise_each"] + offset)
                    yv = map_y(r[f"{dec}_failures"] / r["shots"])
                    lo_y = map_y(r[f"{dec}_simultaneous_ci"][0])
                    hi_y = map_y(r[f"{dec}_simultaneous_ci"][1])
                    pts.append((xv, yv))
                    doc.add(f'<line class="{cls}" stroke-width="1.35" x1="{fmt(xv)}" y1="{fmt(lo_y)}" x2="{fmt(xv)}" y2="{fmt(hi_y)}"/>')
                    doc.add(f'<line class="{cls}" stroke-width="1.25" x1="{fmt(xv - 3.5)}" y1="{fmt(lo_y)}" x2="{fmt(xv + 3.5)}" y2="{fmt(lo_y)}"/>')
                    doc.add(f'<line class="{cls}" stroke-width="1.25" x1="{fmt(xv - 3.5)}" y1="{fmt(hi_y)}" x2="{fmt(xv + 3.5)}" y2="{fmt(hi_y)}"/>')
                doc.add(f'<path class="{cls}" stroke-width="2.0"{dash} d="{path_from_points(pts)}"/>')
                for xv, yv in pts:
                    doc.add(draw_marker(xv, yv, cls, shape))

        # Upper-left inset card (wide open area in both X and Z panels)
        if basis == "x":
            doc.add('<rect class="pill-bg" x="112" y="160" width="234" height="106" rx="9"/>')
            for idx, dist in enumerate((3, 5, 7)):
                cls, sh_ord, sh_cor = dist_styles[dist]
                ry = 180.0 + idx * 24.0
                doc.add(f'<line class="{cls}" stroke-width="2.0" x1="122" y1="{fmt(ry)}" x2="146" y2="{fmt(ry)}"/>')
                doc.add(draw_marker(134.0, ry, cls, sh_ord))
                doc.add(f'<text class="xs {cls}-txt" x="152" y="{fmt(ry + 4)}">d={dist} 普通</text>')
                doc.add(f'<line class="{cls}" stroke-width="2.0" stroke-dasharray="5 3" x1="226" y1="{fmt(ry)}" x2="250" y2="{fmt(ry)}"/>')
                doc.add(draw_marker(238.0, ry, cls, sh_cor))
                doc.add(f'<text class="xs {cls}-txt" x="256" y="{fmt(ry + 4)}">d={dist} 相关</text>')
            doc.add('<text class="xs" x="122" y="254">横轴微移仅防误差棒重叠（同一 p）</text>')
        else:
            doc.add('<rect class="note" x="592" y="160" width="246" height="106" rx="9"/>')
            doc.add('<text class="xsb" x="604" y="179">关键配对结论（同一批原始抽样）</text>')
            doc.add('<text class="xs c3-txt" x="604" y="199">• d=5,7 高噪区：相关匹配降错 3–5 成</text>')
            doc.add('<text class="xs" x="612" y="216">如 X 基 d=7, p=0.006：237 → 124</text>')
            doc.add('<text class="xs c2-txt" x="604" y="236">• d=3 Z 基三点：相关匹配反向略增</text>')
            doc.add('<text class="xs" x="612" y="253">如 p=0.003：136 → 177（净退 41）</text>')

        # Bottom pill note inside panel
        doc.add(f'<rect class="pill" x="{fmt(panel_x + 16)}" y="496" width="432" height="40" rx="9"/>')
        doc.add(f'<text class="xs" x="{fmt(panel_x + 232)}" y="520" text-anchor="middle">{escape(foot_txt)}</text>')

    return doc.render(), {"cases": len(cases), "max_x_rate": 597 / 10000, "max_z_rate": 511 / 10000}


# ---------------------------------------------------------------------------
# Figure 3: round72-systems-control.svg
# ---------------------------------------------------------------------------
def build_fig3_round72_control() -> tuple[str, dict[str, object]]:
    csv_src = ROOT / "codes" / "systems" / "sdk" / "grape-amplitudes.csv"
    json_src = ROOT / "codes" / "systems" / "sdk" / "grape-results.json"
    record = json.loads(json_src.read_text(encoding="utf-8"))

    ts: list[float] = []
    ux: list[float] = []
    uy: list[float] = []
    fux: list[float] = []
    fuy: list[float] = []
    with csv_src.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            ts.append(float(row["start_ns"]))
            ux.append(float(row["ux_rad_per_ns"]))
            uy.append(float(row["uy_rad_per_ns"]))
            fux.append(float(row["filtered_ux"]))
            fuy.append(float(row["filtered_uy"]))
    assert len(ts) == 80
    max_step = max(
        max(abs(ux[i + 1] - ux[i]) for i in range(len(ux) - 1)),
        max(abs(uy[i + 1] - uy[i]) for i in range(len(uy) - 1)),
    )
    assert math.isclose(max_step, record["max_adjacent_step_rad_per_ns"], rel_tol=1e-12)
    assert max(max(abs(v) for v in ux), max(abs(v) for v in uy)) <= record["bound_rad_per_ns"] + 1e-12
    sweep = record["detuning_sweep"]
    assert len(sweep) == 5 and [x["delta_MHz"] for x in sweep] == [3.0, 4.0, 5.0, 6.0, 7.0]

    doc = SvgDoc(
        title="二能级受界 GRAPE 脉冲波形、1 ns 低通滤波与 3–7 MHz 失谐敏感性",
        desc=(
            "左面板展示 40 ns、80 时间槽、幅度盒约束 ±0.12 rad/ns 下二能级 GRAPE 优化的 x/y 两路控制波形及其经 1 ns 离散一阶低通滤波后的变形。"
            "右面板展示同一优化波形在失谐 Δ/(2π) ∈ [3, 7] MHz 扫描下的平均门保真度 F_avg，显示仅在设定点 5 MHz 尖锐最优。"
        ),
    )
    doc.add_header(
        "二能级受界 GRAPE 波形、1 ns 离散滤波与失谐敏感性",
        "40 ns、80 时间槽（Δt = 0.5 ns）、盒约束 ±0.12 rad/ns、设定失谐 Δ/2π = 5 MHz（两能级无耗散合成模型）",
    )
    doc.add_panel(28, 96, 514, 456, "分段常值控制波形（原始 vs 1 ns 采样一阶滤波）")
    doc.add_panel(558, 96, 414, 456, "同一波形在 3–7 MHz 失谐下的平均门保真度")

    # --- Left panel: 80-slot step waveforms ---
    # Clean single-row legend bar above plot
    doc.add('<line class="c1" stroke-width="2.2" x1="46" y1="158" x2="66" y2="158"/>')
    doc.add(f'<text class="xs c1-txt" x="71" y="162">u{sub("x")} 原始</text>')
    doc.add('<line class="c2" stroke-width="2.2" stroke-dasharray="6 3" x1="128" y1="158" x2="148" y2="158"/>')
    doc.add(f'<text class="xs c2-txt" x="153" y="162">u{sub("y")} 原始</text>')
    doc.add('<line class="c3" stroke-width="1.9" x1="210" y1="158" x2="230" y2="158"/>')
    doc.add(f'<text class="xs c3-txt" x="235" y="162">u{sub("x")} 1 ns 滤后</text>')
    doc.add('<line class="c4" stroke-width="1.9" stroke-dasharray="5 2 1.5 2" x1="322" y1="158" x2="342" y2="158"/>')
    doc.add(f'<text class="xs c4-txt" x="347" y="162">u{sub("y")} 1 ns 滤后</text>')
    doc.add('<line class="guide" x1="436" y1="158" x2="454" y2="158"/>')
    doc.add('<text class="xs" x="459" y="162">±0.12 盒界</text>')

    lx0, lx1 = 104.0, 524.0
    ly0, ly1 = 434.0, 184.0
    u_min, u_max = -0.145, 0.145

    def map_t(tv: float) -> float:
        return lx0 + (tv / 40.0) * (lx1 - lx0)

    def map_u(uv: float) -> float:
        return ly0 - (uv - u_min) / (u_max - u_min) * (ly0 - ly1)

    for uv in (-0.12, -0.06, 0.0, 0.06, 0.12):
        yu = map_u(uv)
        cls_l = "guide" if abs(abs(uv) - 0.12) < 1e-9 else "grid"
        doc.add(f'<line class="{cls_l}" x1="{fmt(lx0)}" y1="{fmt(yu)}" x2="{fmt(lx1)}" y2="{fmt(yu)}"/>')
        lbl_u = f"{uv:+.2f}" if uv != 0.0 else "0.00"
        doc.add(f'<text class="xs" x="{fmt(lx0 - 8)}" y="{fmt(yu + 4)}" text-anchor="end">{lbl_u}</text>')

    for tv in (0, 10, 20, 30, 40):
        xt = map_t(float(tv))
        doc.add(f'<line class="grid" x1="{fmt(xt)}" y1="{fmt(ly1)}" x2="{fmt(xt)}" y2="{fmt(ly0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xt)}" y="{fmt(ly0 + 18)}" text-anchor="middle">{tv}</text>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(ly0)}" x2="{fmt(lx1 + 7)}" y2="{fmt(ly0)}"/>')
    doc.add(arrow_head(lx1 + 7, ly0, 1, 0, 7.0))
    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(ly0)}" x2="{fmt(lx0)}" y2="{fmt(ly1 - 8)}"/>')
    doc.add(arrow_head(lx0, ly1 - 8, 0, -1, 7.0))
    doc.add(f'<text class="lbl" x="{fmt(0.5 * (lx0 + lx1))}" y="476" text-anchor="middle">时间 t (ns)</text>')
    doc.add(
        f'<text class="lbl" x="48" y="{fmt(0.5 * (ly0 + ly1))}" text-anchor="middle" '
        f'transform="rotate(-90 48 {fmt(0.5 * (ly0 + ly1))})">控制角频率 u (rad/ns)</text>'
    )

    # Draw 4 exact step curves (filtered drawn underneath/thinner or crisp on top)
    for vals, cls, sw, dash in (
        (ux, "c1", "1.75", ""),
        (uy, "c2", "1.75", ' stroke-dasharray="6 3"'),
        (fux, "c3", "1.55", ""),
        (fuy, "c4", "1.55", ' stroke-dasharray="5 2 1.5 2"'),
    ):
        raw_pts = step_path_post(ts, vals, 40.0)
        mapped = [(map_t(t_v), map_u(u_v)) for t_v, u_v in raw_pts]
        doc.add(f'<path class="{cls}" stroke-width="{sw}"{dash} d="{path_from_points(mapped)}"/>')

    doc.add('<rect class="note" x="44" y="496" width="482" height="40" rx="9"/>')
    doc.add(
        f'<text class="xs" x="285" y="520" text-anchor="middle">'
        f'未限斜率：相邻槽最大跳变 {max_step:.4f} rad/ns；过 1 ns 滤波后 1−g 由 6.63×10{sup("−12")} 弹至 5.56×10{sup("−4")}'
        f'</text>'
    )

    # --- Right panel: 3-7 MHz detuning sweep ---
    rx0, rx1 = 640.0, 948.0
    ry0, ry1 = 434.0, 174.0
    dm_min, dm_max = 2.55, 7.45
    f_min, f_max = 0.975, 1.0035

    def map_dm(dm: float) -> float:
        return rx0 + (dm - dm_min) / (dm_max - dm_min) * (rx1 - rx0)

    def map_f(fv: float) -> float:
        return ry0 - (fv - f_min) / (f_max - f_min) * (ry0 - ry1)

    for fv in (0.975, 0.980, 0.985, 0.990, 0.995, 1.000):
        yf = map_f(fv)
        doc.add(f'<line class="grid" x1="{fmt(rx0)}" y1="{fmt(yf)}" x2="{fmt(rx1)}" y2="{fmt(yf)}"/>')
        doc.add(f'<text class="xs" x="{fmt(rx0 - 8)}" y="{fmt(yf + 4)}" text-anchor="end">{fv:.3f}</text>')

    for dm in (3, 4, 5, 6, 7):
        xd = map_dm(float(dm))
        if dm == 5:
            doc.add(f'<line class="guide" x1="{fmt(xd)}" y1="{fmt(map_f(1.0))}" x2="{fmt(xd)}" y2="{fmt(ry0)}"/>')
        else:
            doc.add(f'<line class="grid" x1="{fmt(xd)}" y1="{fmt(ry1)}" x2="{fmt(xd)}" y2="{fmt(ry0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xd)}" y="{fmt(ry0 + 18)}" text-anchor="middle">{dm}</text>')

    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry0)}" x2="{fmt(rx1 + 7)}" y2="{fmt(ry0)}"/>')
    doc.add(arrow_head(rx1 + 7, ry0, 1, 0, 7.0))
    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry0)}" x2="{fmt(rx0)}" y2="{fmt(ry1 - 8)}"/>')
    doc.add(arrow_head(rx0, ry1 - 8, 0, -1, 7.0))
    doc.add(f'<text class="lbl" x="{fmt(0.5 * (rx0 + rx1))}" y="476" text-anchor="middle">失谐 Δ / (2π) (MHz)</text>')
    doc.add(
        f'<text class="lbl" x="580" y="{fmt(0.5 * (ry0 + ry1))}" text-anchor="middle" '
        f'transform="rotate(-90 580 {fmt(0.5 * (ry0 + ry1))})">平均门保真度 F{sub("avg")}（无量纲）</text>'
    )

    sw_pts = [(map_dm(x["delta_MHz"]), map_f(x["avg_gate_fidelity"])) for x in sweep]
    doc.add(f'<path class="c1" stroke-width="2.5" d="{path_from_points(sw_pts)}"/>')
    for x_item, (px, py) in zip(sweep, sw_pts):
        doc.add(f'<circle class="c1-fill" cx="{fmt(px)}" cy="{fmt(py)}" r="5.2"/>')

    # Clean non-overlapping value labels at sweep points
    doc.add(f'<text class="xsb c1-txt" x="{fmt(sw_pts[2][0])}" y="{fmt(sw_pts[2][1] - 13)}" text-anchor="middle">设定点 5 MHz：F{sub("avg")} ≈ 1.0000</text>')
    doc.add(f'<text class="xs c1-txt" x="{fmt(sw_pts[1][0] - 8)}" y="{fmt(sw_pts[1][1] - 11)}" text-anchor="end">{sweep[1]["avg_gate_fidelity"]:.4f}</text>')
    doc.add(f'<text class="xs c1-txt" x="{fmt(sw_pts[3][0] + 8)}" y="{fmt(sw_pts[3][1] - 11)}" text-anchor="start">{sweep[3]["avg_gate_fidelity"]:.4f}</text>')
    doc.add(f'<text class="xs c1-txt" x="{fmt(sw_pts[0][0] + 10)}" y="{fmt(sw_pts[0][1] + 18)}" text-anchor="start">{sweep[0]["avg_gate_fidelity"]:.4f}</text>')
    doc.add(f'<text class="xs c1-txt" x="{fmt(sw_pts[4][0] - 10)}" y="{fmt(sw_pts[4][1] + 18)}" text-anchor="end">{sweep[4]["avg_gate_fidelity"]:.4f}</text>')

    # Open space under arch: 1 ns filtered reference pill
    f_filt = record["sampled_one_pole_1ns"]["avg_gate_fidelity"]
    doc.add('<rect class="pill-bg" x="716" y="346" width="156" height="48" rx="8"/>')
    doc.add('<text class="xsb c3-txt" x="794" y="366" text-anchor="middle">5 MHz 经 1 ns 滤波</text>')
    doc.add(f'<text class="xs" x="794" y="384" text-anchor="middle">F{sub("avg")} = {f_filt:.5f}</text>')

    doc.add('<rect class="pill" x="574" y="496" width="382" height="40" rx="9"/>')
    doc.add('<text class="xs" x="765" y="520" text-anchor="middle">纵轴放大至 [0.975, 1.000]；三能级泄漏另见下一节</text>')

    return doc.render(), {"slots": len(ts), "max_step": round(max_step, 5), "f_5mhz": sweep[2]["avg_gate_fidelity"]}


# ---------------------------------------------------------------------------
# Figure 4: round73-systems-control.svg
# ---------------------------------------------------------------------------
def build_fig4_round73_control() -> tuple[str, dict[str, object]]:
    csv_src = ROOT / "codes" / "systems" / "sdk73" / "grape-three-amplitudes.csv"
    json_src = ROOT / "codes" / "systems" / "sdk73" / "grape-three-results.json"
    record = json.loads(json_src.read_text(encoding="utf-8"))

    ts: list[float] = []
    ux: list[float] = []
    uy: list[float] = []
    fux: list[float] = []
    fuy: list[float] = []
    with csv_src.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            ts.append(float(row["start_ns"]))
            ux.append(float(row["ux_rad_per_ns"]))
            uy.append(float(row["uy_rad_per_ns"]))
            fux.append(float(row["filtered_ux"]))
            fuy.append(float(row["filtered_uy"]))
    assert len(ts) == 80
    max_step = max(
        max(abs(ux[i + 1] - ux[i]) for i in range(len(ux) - 1)),
        max(abs(uy[i + 1] - uy[i]) for i in range(len(uy) - 1)),
    )
    assert math.isclose(max_step, record["maximum_adjacent_step"], rel_tol=1e-12)

    leak_2lvl = record["previous_two_level_waveform"]["basis_leakage"]
    leak_3lvl = record["optimized"]["basis_leakage"]
    leak_filt = record["one_ns_discrete_filter"]["basis_leakage"]
    mean_filt_leak = 0.5 * (leak_filt[0] + leak_filt[1])
    assert math.isclose(mean_filt_leak, 0.007352647925225857, rel_tol=1e-9)

    doc = SvgDoc(
        title="三能级 GRAPE 控制波形、1 ns 离散滤波与 |2⟩ 末态泄漏对照",
        desc=(
            "左面板展示 40 ns、80 时间槽、Δ/2π = +5 MHz、非谐性 α/2π = −200 MHz 下三能级 GRAPE 优化的 x/y 控制波形与 1 ns 采样滤波波形。"
            "右面板以对数纵轴对比二能级波形放回三能级、三能级 GRAPE 理想模型与经 1 ns 离散滤波三种情形下输入 |0⟩、|1⟩ 的末态 |2⟩ 泄漏概率。"
        ),
    )
    doc.add_header(
        "三能级 GRAPE 两路波形、1 ns 滤波与 |2⟩ 末态泄漏对照",
        "40 ns 合成三能级旋波模型：Δ/2π = +5 MHz，非谐性 α/2π = −200 MHz，80 槽盒约束 ±0.12 rad/ns（无带宽约束）",
    )
    doc.add_panel(28, 96, 486, 456, "三能级优化两路波形（原始 vs 1 ns 一阶滤波）")
    doc.add_panel(530, 96, 442, 456, "输入 |0⟩ / |1⟩ 末态 |2⟩ 泄漏概率（对数纵轴）")

    # --- Left panel: 3-level waveforms ---
    doc.add('<line class="c1" stroke-width="2.1" x1="42" y1="158" x2="60" y2="158"/>')
    doc.add(f'<text class="xs c1-txt" x="64" y="162">u{sub("x")} 原始</text>')
    doc.add('<line class="c2" stroke-width="2.1" stroke-dasharray="6 3" x1="116" y1="158" x2="134" y2="158"/>')
    doc.add(f'<text class="xs c2-txt" x="138" y="162">u{sub("y")} 原始</text>')
    doc.add('<line class="c3" stroke-width="1.8" x1="190" y1="158" x2="208" y2="158"/>')
    doc.add(f'<text class="xs c3-txt" x="212" y="162">u{sub("x")} 1 ns 滤后</text>')
    doc.add('<line class="c4" stroke-width="1.8" stroke-dasharray="5 2 1.5 2" x1="296" y1="158" x2="314" y2="158"/>')
    doc.add(f'<text class="xs c4-txt" x="318" y="162">u{sub("y")} 1 ns 滤后</text>')
    doc.add('<line class="guide" x1="404" y1="158" x2="420" y2="158"/>')
    doc.add('<text class="xs" x="424" y="162">±0.12 盒界</text>')

    lx0, lx1 = 100.0, 496.0
    ly0, ly1 = 434.0, 184.0
    u_min, u_max = -0.145, 0.145

    def map_t(tv: float) -> float:
        return lx0 + (tv / 40.0) * (lx1 - lx0)

    def map_u(uv: float) -> float:
        return ly0 - (uv - u_min) / (u_max - u_min) * (ly0 - ly1)

    for uv in (-0.12, -0.06, 0.0, 0.06, 0.12):
        yu = map_u(uv)
        cls_l = "guide" if abs(abs(uv) - 0.12) < 1e-9 else "grid"
        doc.add(f'<line class="{cls_l}" x1="{fmt(lx0)}" y1="{fmt(yu)}" x2="{fmt(lx1)}" y2="{fmt(yu)}"/>')
        lbl_u = f"{uv:+.2f}" if uv != 0.0 else "0.00"
        doc.add(f'<text class="xs" x="{fmt(lx0 - 8)}" y="{fmt(yu + 4)}" text-anchor="end">{lbl_u}</text>')

    for tv in (0, 10, 20, 30, 40):
        xt = map_t(float(tv))
        doc.add(f'<line class="grid" x1="{fmt(xt)}" y1="{fmt(ly1)}" x2="{fmt(xt)}" y2="{fmt(ly0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xt)}" y="{fmt(ly0 + 18)}" text-anchor="middle">{tv}</text>')

    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(ly0)}" x2="{fmt(lx1 + 7)}" y2="{fmt(ly0)}"/>')
    doc.add(arrow_head(lx1 + 7, ly0, 1, 0, 7.0))
    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(ly0)}" x2="{fmt(lx0)}" y2="{fmt(ly1 - 8)}"/>')
    doc.add(arrow_head(lx0, ly1 - 8, 0, -1, 7.0))
    doc.add(f'<text class="lbl" x="{fmt(0.5 * (lx0 + lx1))}" y="476" text-anchor="middle">时间 t (ns)</text>')
    doc.add(
        f'<text class="lbl" x="48" y="{fmt(0.5 * (ly0 + ly1))}" text-anchor="middle" '
        f'transform="rotate(-90 48 {fmt(0.5 * (ly0 + ly1))})">控制角频率包络 u (rad/ns)</text>'
    )

    for vals, cls, sw, dash in (
        (ux, "c1", "1.7", ""),
        (uy, "c2", "1.7", ' stroke-dasharray="6 3"'),
        (fux, "c3", "1.5", ""),
        (fuy, "c4", "1.5", ' stroke-dasharray="5 2 1.5 2"'),
    ):
        raw_pts = step_path_post(ts, vals, 40.0)
        mapped = [(map_t(t_v), map_u(u_v)) for t_v, u_v in raw_pts]
        doc.add(f'<path class="{cls}" stroke-width="{sw}"{dash} d="{path_from_points(mapped)}"/>')

    doc.add('<rect class="pill" x="44" y="496" width="454" height="40" rx="9"/>')
    doc.add(f'<text class="xs" x="271" y="520" text-anchor="middle">未加斜率约束：相邻槽最大跳变 {max_step:.4f} rad/ns，经 1 ns 滤波显著展宽</text>')

    # --- Right panel: log-scale grouped leakage bar chart ---
    doc.add('<rect class="bar1" x="614" y="148" width="18" height="13" rx="2"/>')
    doc.add('<text class="sm" x="638" y="159">输入 |0⟩ 末态泄漏</text>')
    doc.add('<rect class="bar2" x="774" y="148" width="18" height="13" rx="2"/>')
    doc.add('<rect fill="url(#hatch-bar)" x="774" y="148" width="18" height="13" rx="2"/>')
    doc.add('<text class="sm" x="798" y="159">输入 |1⟩ 末态泄漏</text>')

    rx0, rx1 = 610.0, 952.0
    ry0, ry1 = 420.0, 184.0
    ly_min, ly_max = -11.0, -1.0

    def map_ly(val: float) -> float:
        return ry0 - (math.log10(val) - ly_min) / (ly_max - ly_min) * (ry0 - ry1)

    for exp_v in range(-11, 0):
        yt = map_ly(10.0 ** exp_v)
        if exp_v % 2 == 1:
            doc.add(f'<line class="grid" x1="{fmt(rx0)}" y1="{fmt(yt)}" x2="{fmt(rx1)}" y2="{fmt(yt)}"/>')
            doc.add(f'<text class="xs" x="{fmt(rx0 - 8)}" y="{fmt(yt + 4)}" text-anchor="end">10{sup(str(exp_v))}</text>')
        else:
            doc.add(f'<line class="grid-minor" x1="{fmt(rx0)}" y1="{fmt(yt)}" x2="{fmt(rx1)}" y2="{fmt(yt)}"/>')

    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry0)}" x2="{fmt(rx1 + 6)}" y2="{fmt(ry0)}"/>')
    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry0)}" x2="{fmt(rx0)}" y2="{fmt(ry1 - 8)}"/>')
    doc.add(arrow_head(rx0, ry1 - 8, 0, -1, 7.0))
    doc.add(
        f'<text class="lbl" x="552" y="{fmt(0.5 * (ry0 + ry1))}" text-anchor="middle" '
        f'transform="rotate(-90 552 {fmt(0.5 * (ry0 + ry1))})">末态 |2⟩ 泄漏概率（对数刻度）</text>'
    )

    groups = [
        (668.0, "二能级波形", "放回三能级", leak_2lvl, ("1.33%", "2.36%")),
        (781.0, "三能级 GRAPE", "理想模型", leak_3lvl, None),
        (894.0, "三能级波形", "过 1 ns 滤波", leak_filt, ("0.95%", "0.52%")),
    ]
    bw, gap = 36.0, 8.0
    for gx, l1, l2, vals, pair_lbl in groups:
        x_b0 = gx - gap * 0.5 - bw
        x_b1 = gx + gap * 0.5
        y_b0 = map_ly(vals[0])
        y_b1 = map_ly(vals[1])
        doc.add(f'<rect class="bar1" x="{fmt(x_b0)}" y="{fmt(y_b0)}" width="{fmt(bw)}" height="{fmt(ry0 - y_b0)}" rx="2"/>')
        doc.add(f'<rect class="bar2" x="{fmt(x_b1)}" y="{fmt(y_b1)}" width="{fmt(bw)}" height="{fmt(ry0 - y_b1)}" rx="2"/>')
        doc.add(f'<rect fill="url(#hatch-bar)" x="{fmt(x_b1)}" y="{fmt(y_b1)}" width="{fmt(bw)}" height="{fmt(ry0 - y_b1)}" rx="2"/>')
        if pair_lbl is not None:
            doc.add(f'<text class="xsb c1-txt" x="{fmt(x_b0 + bw * 0.5)}" y="{fmt(y_b0 - 7)}" text-anchor="middle">{pair_lbl[0]}</text>')
            doc.add(f'<text class="xsb c2-txt" x="{fmt(x_b1 + bw * 0.5)}" y="{fmt(y_b1 - 7)}" text-anchor="middle">{pair_lbl[1]}</text>')
        else:
            doc.add(f'<text class="xsb c1-txt" x="{fmt(gx)}" y="{fmt(y_b0 - 25)}" text-anchor="middle">|0⟩: 6.25×10{sup("−10")}</text>')
            doc.add(f'<text class="xsb c2-txt" x="{fmt(gx)}" y="{fmt(y_b0 - 8)}" text-anchor="middle">|1⟩: 6.15×10{sup("−10")}</text>')
        doc.add(f'<text class="xsb" x="{fmt(gx)}" y="440" text-anchor="middle">{escape(l1)}</text>')
        doc.add(f'<text class="xs" x="{fmt(gx)}" y="456" text-anchor="middle">{escape(l2)}</text>')

    # Highlight suppression magnitude in wide open center above Group 2 bars
    doc.add('<rect class="c3-soft" x="729" y="254" width="104" height="44" rx="8"/>')
    doc.add('<text class="xsb c3-txt" x="781" y="273" text-anchor="middle">模型内骤降</text>')
    doc.add('<text class="xs c3-txt" x="781" y="290" text-anchor="middle">约 7 个数量级</text>')
    doc.add('<line class="c3" stroke-width="1.5" stroke-dasharray="4 3" x1="781" y1="298" x2="781" y2="334"/>')
    doc.add(arrow_head(781, 336, 0, 1, 6.5, "c3-fill"))

    doc.add('<rect class="note" x="546" y="496" width="410" height="40" rx="9"/>')
    doc.add(
        f'<text class="xs" x="751" y="520" text-anchor="middle">'
        f'过 1 ns 滤波后平均泄漏反弹至 {mean_filt_leak * 100:.3f}%，f̄{sub("comp")} 跌回 {record["one_ns_discrete_filter"]["haar_unconditional_target_overlap"]:.4f}'
        f'</text>'
    )
    return doc.render(), {"max_step": round(max_step, 5), "mean_filt_leak": round(mean_filt_leak, 6)}


# ---------------------------------------------------------------------------
# Figure 5: round72-algorithms.svg
# ---------------------------------------------------------------------------
def build_fig5_round72_algorithms() -> tuple[str, dict[str, object]]:
    src = ROOT / "codes" / "algorithms" / "sdk" / "round72-results.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    phases = data["cases"]["pyqsp"]["result"]["phases_radians"]
    assert len(phases) == 4

    # Independent pure-Python complex 2x2 QSP reconstruction
    def qsp_eval_imag_u00(x_val: float) -> float:
        s = math.sqrt(max(0.0, 1.0 - x_val * x_val))
        w00, w01 = complex(x_val, 0.0), complex(0.0, s)
        w10, w11 = complex(0.0, s), complex(x_val, 0.0)
        u00, u01 = cmath.exp(1j * phases[0]), 0j
        u10, u11 = 0j, cmath.exp(-1j * phases[0])
        for phi in phases[1:]:
            ep, em = cmath.exp(1j * phi), cmath.exp(-1j * phi)
            # U <- U @ W @ diag(ep, em)
            t00 = u00 * w00 + u01 * w10
            t01 = u00 * w01 + u01 * w11
            t10 = u10 * w00 + u11 * w10
            t11 = u10 * w01 + u11 * w11
            u00, u01, u10, u11 = t00 * ep, t01 * em, t10 * ep, t11 * em
        unit_err = abs(abs(u00) ** 2 + abs(u10) ** 2 - 1.0)
        assert unit_err < 1e-13
        return u00.imag

    max_qsp_err = max(abs(qsp_eval_imag_u00(-1.0 + 2.0 * i / 200) - (0.8 * (-1.0 + 2.0 * i / 200) ** 3 - 0.3 * (-1.0 + 2.0 * i / 200))) for i in range(201))
    assert max_qsp_err < 1e-14

    # CTQW exact verification at t* = pi / sqrt(2)
    t_star = math.pi / math.sqrt(2.0)
    assert math.isclose(t_star, data["cases"]["quimb"]["result"]["path3_time"], rel_tol=1e-12)
    assert math.isclose((1.0 - math.cos(math.sqrt(2.0) * t_star)) ** 2 / 4.0, 1.0, abs_tol=1e-15)

    # Fock tail for coherent state |alpha|^2 = 1
    d_vals = list(range(2, 17))
    tails = [sum(math.exp(-1.0) / math.factorial(n) for n in range(d, 65)) for d in d_vals]
    tdists = [math.sqrt(v) for v in tails]
    assert 1e-14 < tails[-1] < 2e-14 and 1e-7 < tdists[-1] < 2e-7

    doc = SvgDoc(
        title="连续时间行走完美转移、对称 QSP 多项式合成与 Fock 截断误差",
        desc=(
            "三联科学图：左图展示三顶点路径连续时间量子行走在 t* = π/√2 实现 100% 完美转移；"
            "中图对比归档四相位对称 QSP 重建的 Im U₀₀ 与目标三次奇多项式 0.3T₁ + 0.2T₃ = 0.8x³ − 0.3x；"
            "右图以对数纵轴对照 |α|² = 1 相干态在不同 Fock 截断维数 d 下的遗漏尾概率 ε 与迹距离 √ε。"
        ),
    )
    doc.add_header(
        "连续时间行走完美转移、对称 QSP 合成与 Fock 截断误差",
        "左：P₃ 路径相干转移（t* = π/√2 达 100%）；中：四相位 QSP 合成 0.8x³ − 0.3x；右：|α|² = 1 相干态截断尾界",
    )

    # --- Panel A: P3 CTQW ---
    doc.add_panel(28, 96, 306, 456, "A. 三顶点路径连续时间行走")
    doc.add('<line class="c1" stroke-width="2.0" x1="39" y1="158" x2="55" y2="158"/>')
    doc.add('<text class="xs c1-txt" x="59" y="162">顶点 0</text>')
    doc.add('<line class="c2" stroke-width="2.0" stroke-dasharray="6 3" x1="104" y1="158" x2="120" y2="158"/>')
    doc.add('<text class="xs c2-txt" x="124" y="162">顶点 1</text>')
    doc.add('<line class="c3" stroke-width="2.0" stroke-dasharray="5 2 1.5 2" x1="169" y1="158" x2="185" y2="158"/>')
    doc.add('<text class="xs c3-txt" x="189" y="162">顶点 2</text>')
    doc.add('<line class="guide" x1="238" y1="158" x2="254" y2="158"/>')
    doc.add('<text class="xs" x="258" y="162">t* = π/√2</text>')

    ax0, ax1, ay0, ay1 = 84.0, 316.0, 432.0, 186.0
    t_end = math.sqrt(2.0) * math.pi

    def map_at(tv: float) -> float:
        return ax0 + (tv / t_end) * (ax1 - ax0)

    def map_ap(pv: float) -> float:
        return ay0 - (pv / 1.16) * (ay0 - ay1)

    for pv in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        yp = map_ap(pv)
        doc.add(f'<line class="grid" x1="{fmt(ax0)}" y1="{fmt(yp)}" x2="{fmt(ax1)}" y2="{fmt(yp)}"/>')
        doc.add(f'<text class="xs" x="{fmt(ax0 - 7)}" y="{fmt(yp + 4)}" text-anchor="end">{pv:.1f}</text>')
    for tv in (0, 1, 2, 3, 4):
        xt = map_at(float(tv))
        doc.add(f'<line class="grid" x1="{fmt(xt)}" y1="{fmt(ay1)}" x2="{fmt(xt)}" y2="{fmt(ay0)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xt)}" y="{fmt(ay0 + 17)}" text-anchor="middle">{tv}</text>')

    doc.add(f'<line class="guide" x1="{fmt(map_at(t_star))}" y1="{fmt(map_ap(1.0))}" x2="{fmt(map_at(t_star))}" y2="{fmt(ay0)}"/>')
    doc.add(f'<line class="axis" x1="{fmt(ax0)}" y1="{fmt(ay0)}" x2="{fmt(ax1 + 6)}" y2="{fmt(ay0)}"/>')
    doc.add(arrow_head(ax1 + 6, ay0, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(ax0)}" y1="{fmt(ay0)}" x2="{fmt(ax0)}" y2="{fmt(ay1 - 8)}"/>')
    doc.add(arrow_head(ax0, ay1 - 8, 0, -1, 6.5))
    doc.add(f'<text class="sm" x="{fmt(0.5 * (ax0 + ax1))}" y="472" text-anchor="middle">时间 t（无量纲模型单位）</text>')
    doc.add(f'<text class="sm" x="44" y="{fmt(0.5 * (ay0 + ay1))}" text-anchor="middle" transform="rotate(-90 44 {fmt(0.5 * (ay0 + ay1))})">位置概率 p(t)</text>')

    n_ct = 140
    p0_pts, p1_pts, p2_pts = [], [], []
    for i in range(n_ct + 1):
        tv = t_end * i / n_ct
        cv = math.cos(math.sqrt(2.0) * tv)
        sv = math.sin(math.sqrt(2.0) * tv)
        p0_pts.append((map_at(tv), map_ap((1.0 + cv) ** 2 / 4.0)))
        p1_pts.append((map_at(tv), map_ap(sv * sv / 2.0)))
        p2_pts.append((map_at(tv), map_ap((1.0 - cv) ** 2 / 4.0)))
    doc.add(f'<path class="c1" stroke-width="2.2" d="{path_from_points(p0_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.0" stroke-dasharray="6 3" d="{path_from_points(p1_pts)}"/>')
    doc.add(f'<path class="c3" stroke-width="2.2" stroke-dasharray="5 2 1.5 2" d="{path_from_points(p2_pts)}"/>')
    doc.add(f'<circle class="c3-fill" cx="{fmt(map_at(t_star))}" cy="{fmt(map_ap(1.0))}" r="4.8"/>')
    doc.add(f'<text class="xsb c3-txt" x="{fmt(map_at(t_star))}" y="{fmt(map_ap(1.0) - 12)}" text-anchor="middle">t* = π/√2：p₂ = 1.00</text>')

    doc.add('<rect class="pill" x="40" y="496" width="282" height="40" rx="8"/>')
    doc.add('<text class="xs" x="181" y="520" text-anchor="middle">相干干涉在 t* ≈ 2.22 实现 100% 端到端转移</text>')

    # --- Panel B: Symmetric QSP ---
    doc.add_panel(347, 96, 306, 456, "B. 对称 QSP 三次奇多项式")
    doc.add('<line class="c1" stroke-width="2.2" x1="364" y1="158" x2="384" y2="158"/>')
    doc.add('<text class="xs c1-txt" x="389" y="162">目标 0.3T₁ + 0.2T₃</text>')
    doc.add('<line class="c2" stroke-width="1.8" x1="513" y1="154" x2="521" y2="162"/>')
    doc.add('<line class="c2" stroke-width="1.8" x1="521" y1="154" x2="513" y2="162"/>')
    doc.add('<text class="xs c2-txt" x="527" y="162">QSP 独立相位重建</text>')

    bx0, bx1, by0, by1 = 408.0, 636.0, 432.0, 186.0

    def map_bx(xv: float) -> float:
        return bx0 + (xv + 1.06) / 2.12 * (bx1 - bx0)

    def map_by(yv: float) -> float:
        return by0 - (yv + 0.56) / 1.12 * (by0 - by1)

    for yv in (-0.4, -0.2, 0.0, 0.2, 0.4):
        yy = map_by(yv)
        cls_g = "guide" if yv == 0.0 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(bx0)}" y1="{fmt(yy)}" x2="{fmt(bx1)}" y2="{fmt(yy)}"/>')
        lbl_y = f"{yv:+.1f}" if yv != 0.0 else "0.0"
        doc.add(f'<text class="xs" x="{fmt(bx0 - 7)}" y="{fmt(yy + 4)}" text-anchor="end">{lbl_y}</text>')
    for xv in (-1.0, -0.5, 0.0, 0.5, 1.0):
        xx = map_bx(xv)
        cls_g = "guide" if xv == 0.0 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(xx)}" y1="{fmt(by1)}" x2="{fmt(xx)}" y2="{fmt(by0)}"/>')
        lbl_x = f"{xv:g}"
        doc.add(f'<text class="xs" x="{fmt(xx)}" y="{fmt(by0 + 17)}" text-anchor="middle">{lbl_x}</text>')

    doc.add(f'<line class="axis" x1="{fmt(bx0)}" y1="{fmt(by0)}" x2="{fmt(bx1 + 6)}" y2="{fmt(by0)}"/>')
    doc.add(arrow_head(bx1 + 6, by0, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(bx0)}" y1="{fmt(by0)}" x2="{fmt(bx0)}" y2="{fmt(by1 - 8)}"/>')
    doc.add(arrow_head(bx0, by1 - 8, 0, -1, 6.5))
    doc.add(f'<text class="sm" x="{fmt(0.5 * (bx0 + bx1))}" y="472" text-anchor="middle">信号变量 x（无量纲）</text>')
    doc.add(f'<text class="sm" x="362" y="{fmt(0.5 * (by0 + by1))}" text-anchor="middle" transform="rotate(-90 362 {fmt(0.5 * (by0 + by1))})">矩阵元虚部 Im U₀₀</text>')

    qsp_curve = [(map_bx(-1.0 + 2.0 * i / 120), map_by(0.8 * (-1.0 + 2.0 * i / 120) ** 3 - 0.3 * (-1.0 + 2.0 * i / 120))) for i in range(121)]
    doc.add(f'<path class="c1" stroke-width="2.3" d="{path_from_points(qsp_curve)}"/>')
    for i in range(17):
        xv = -1.0 + 2.0 * i / 16
        px, py = map_bx(xv), map_by(qsp_eval_imag_u00(xv))
        doc.add(f'<line class="c2" stroke-width="1.8" x1="{fmt(px - 3.8)}" y1="{fmt(py - 3.8)}" x2="{fmt(px + 3.8)}" y2="{fmt(py + 3.8)}"/>')
        doc.add(f'<line class="c2" stroke-width="1.8" x1="{fmt(px + 3.8)}" y1="{fmt(py - 3.8)}" x2="{fmt(px - 3.8)}" y2="{fmt(py + 3.8)}"/>')

    doc.add('<rect class="pill-bg" x="415" y="194" width="118" height="44" rx="7"/>')
    doc.add('<text class="xsb c1-txt" x="474" y="212" text-anchor="middle">P(x) = 0.8x³ − 0.3x</text>')
    doc.add(f'<text class="xs" x="474" y="229" text-anchor="middle">最大偏差 {max_qsp_err:.1e}</text>')

    doc.add('<rect class="pill" x="359" y="496" width="282" height="40" rx="8"/>')
    doc.add('<text class="xs" x="500" y="520" text-anchor="middle">四对称相位将多项式编码在虚部 Im U₀₀</text>')

    # --- Panel C: Fock cutoff tail ---
    doc.add_panel(666, 96, 306, 456, "C. 相干态 Fock 截断误差")
    doc.add('<line class="c1" stroke-width="2.0" x1="686" y1="158" x2="706" y2="158"/>')
    doc.add('<circle class="c1-fill" cx="696" cy="158" r="3.5"/>')
    doc.add('<text class="xs c1-txt" x="712" y="162">遗漏尾概率 ε</text>')
    doc.add('<line class="c2" stroke-width="2.0" stroke-dasharray="5 3" x1="808" y1="158" x2="828" y2="158"/>')
    doc.add('<rect class="c2-fill" x="814.5" y="154.5" width="7" height="7" rx="1"/>')
    doc.add('<text class="xs c2-txt" x="834" y="162">迹距离 √ε</text>')

    cx0, cx1, cy0, cy1 = 736.0, 956.0, 432.0, 186.0

    def map_cd(dv: float) -> float:
        return cx0 + (dv - 1.5) / 15.0 * (cx1 - cx0)

    def map_ce(ev: float) -> float:
        return cy0 - (math.log10(ev) + 15.4) / 16.0 * (cy0 - cy1)

    for exp_v in (0, -3, -6, -9, -12, -15):
        ye = map_ce(10.0 ** exp_v)
        doc.add(f'<line class="grid" x1="{fmt(cx0)}" y1="{fmt(ye)}" x2="{fmt(cx1)}" y2="{fmt(ye)}"/>')
        doc.add(f'<text class="xs" x="{fmt(cx0 - 7)}" y="{fmt(ye + 4)}" text-anchor="end">10{sup(str(exp_v))}</text>')
    for dv in (2, 6, 10, 14, 16):
        xd = map_cd(float(dv))
        doc.add(f'<line class="grid" x1="{fmt(xd)}" y1="{fmt(cy1)}" x2="{fmt(xd)}" y2="{fmt(cy0)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xd)}" y="{fmt(cy0 + 17)}" text-anchor="middle">{dv}</text>')

    doc.add(f'<line class="axis" x1="{fmt(cx0)}" y1="{fmt(cy0)}" x2="{fmt(cx1 + 6)}" y2="{fmt(cy0)}"/>')
    doc.add(arrow_head(cx1 + 6, cy0, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(cx0)}" y1="{fmt(cy0)}" x2="{fmt(cx0)}" y2="{fmt(cy1 - 8)}"/>')
    doc.add(arrow_head(cx0, cy1 - 8, 0, -1, 6.5))
    doc.add(f'<text class="sm" x="{fmt(0.5 * (cx0 + cx1))}" y="472" text-anchor="middle">Fock 截断维数 d（整数）</text>')
    doc.add(f'<text class="sm" x="681" y="{fmt(0.5 * (cy0 + cy1))}" text-anchor="middle" transform="rotate(-90 681 {fmt(0.5 * (cy0 + cy1))})">无量纲误差（对数刻度）</text>')

    tail_pts = [(map_cd(float(d)), map_ce(v)) for d, v in zip(d_vals, tails)]
    td_pts = [(map_cd(float(d)), map_ce(v)) for d, v in zip(d_vals, tdists)]
    doc.add(f'<path class="c1" stroke-width="2.1" d="{path_from_points(tail_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.0" stroke-dasharray="6 3" d="{path_from_points(td_pts)}"/>')
    for px, py in tail_pts:
        doc.add(f'<circle class="c1-fill" cx="{fmt(px)}" cy="{fmt(py)}" r="3.4"/>')
    for px, py in td_pts:
        doc.add(f'<rect class="c2-fill" x="{fmt(px - 3.1)}" y="{fmt(py - 3.1)}" width="6.2" height="6.2" rx="1"/>')

    doc.add('<rect class="pill-bg" x="744" y="368" width="114" height="44" rx="7"/>')
    doc.add('<text class="xsb" x="801" y="386" text-anchor="middle">|α|² = 1 相干态</text>')
    doc.add('<text class="xs c2-txt" x="801" y="403" text-anchor="middle">迹距离 = √(尾概率)</text>')

    doc.add('<rect class="pill" x="678" y="496" width="282" height="40" rx="8"/>')
    doc.add(f'<text class="xs" x="819" y="520" text-anchor="middle">d = 16：ε = {tails[-1]:.1e}，迹距离 √ε = {tdists[-1]:.1e}</text>')

    return doc.render(), {"max_qsp_err": max_qsp_err, "tail_d16": tails[-1]}


# ---------------------------------------------------------------------------
# Figure 6: round73-algorithms.svg
# ---------------------------------------------------------------------------
def build_fig6_round73_algorithms() -> tuple[str, dict[str, object]]:
    src = ROOT / "codes" / "algorithms" / "sdk73" / "results-all.json"
    data = json.loads(src.read_text(encoding="utf-8"))["cases"]
    hhl_rows = [c for c in data["hhl"]["cases"] if c["name"] == "signed-offgrid"]
    walk_rows = data["walk"]["rows"]
    assert len(hhl_rows) == 4 and [c["phase_bits"] for c in hhl_rows] == [3, 4, 5, 6]
    assert len(walk_rows) == 17 and [w["steps"] for w in walk_rows] == list(range(17))
    assert math.isclose(walk_rows[4]["marked_probability"], 25.0 / 64.0, abs_tol=1e-12)
    assert math.isclose(walk_rows[8]["marked_probability"], 1.0 / 256.0, abs_tol=1e-12)

    ideal_succ = hhl_rows[0]["ideal_success"]
    doc = SvgDoc(
        title="带负谱非网格 HHL 有限相位误差与 16 顶点离散量子行走搜索",
        desc=(
            "三联科学图基于本地精确模拟归档数据：左图对比非网格带负特征值 (−1.1, 2.3) 的 HHL 线路在相位寄存器位数 t = 3..6 下"
            "仅选标志位与同时要求相位归零两类成功概率；中图展示条件混态根保真度与残留非零相位垃圾占比；"
            "右图展示 4 维超立方体（16 顶点）SKW 离散量子行走的标记顶点概率，在第 4 步达最早峰值 25/64，第 8 步过步回落至 1/256。"
        ),
    )
    doc.add_header(
        "带负谱非网格 HHL 有限相位误差与 16 顶点离散行走搜索",
        "左/中：2×2 特征值 (−1.1, 2.3) 随相位位数 t 的成功事件与残留垃圾；右：4 维超立方体 SKW 行走峰值与过步回落",
    )

    # --- Panel A: Finite QPE two success events ---
    doc.add_panel(28, 96, 306, 456, "A. 有限 QPE：两类成功事件")
    doc.add('<line class="c1" stroke-width="2.0" x1="40" y1="154" x2="58" y2="154"/>')
    doc.add('<circle class="c1-fill" cx="49" cy="154" r="3.4"/>')
    doc.add('<text class="xs c1-txt" x="63" y="158">标志位 = 1</text>')
    doc.add('<line class="c2" stroke-width="2.0" stroke-dasharray="5 3" x1="140" y1="154" x2="158" y2="154"/>')
    doc.add('<rect class="c2-fill" x="145.5" y="150.5" width="7" height="7" rx="1"/>')
    doc.add('<text class="xs c2-txt" x="163" y="158">标志=1 且相位归零</text>')
    doc.add('<line class="guide" x1="40" y1="174" x2="58" y2="174"/>')
    doc.add(f'<text class="xs" x="63" y="178">理想倒数成功率（{ideal_succ:.4f}）</text>')

    ax0, ax1, ay0, ay1 = 92.0, 316.0, 432.0, 194.0

    def map_at(tv: float) -> float:
        return ax0 + (tv - 2.65) / 3.7 * (ax1 - ax0)

    def map_ap(pv: float) -> float:
        return ay0 - (pv - 0.115) / 0.060 * (ay0 - ay1)

    for pv in (0.12, 0.13, 0.14, 0.15, 0.16, 0.17):
        yp = map_ap(pv)
        doc.add(f'<line class="grid" x1="{fmt(ax0)}" y1="{fmt(yp)}" x2="{fmt(ax1)}" y2="{fmt(yp)}"/>')
        doc.add(f'<text class="xs" x="{fmt(ax0 - 7)}" y="{fmt(yp + 4)}" text-anchor="end">{pv:.2f}</text>')
    for tv in (3, 4, 5, 6):
        xt = map_at(float(tv))
        doc.add(f'<line class="grid" x1="{fmt(xt)}" y1="{fmt(ay1)}" x2="{fmt(xt)}" y2="{fmt(ay0)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xt)}" y="{fmt(ay0 + 17)}" text-anchor="middle">{tv}</text>')

    y_ideal = map_ap(ideal_succ)
    doc.add(f'<line class="guide" x1="{fmt(ax0)}" y1="{fmt(y_ideal)}" x2="{fmt(ax1)}" y2="{fmt(y_ideal)}"/>')
    doc.add(f'<line class="axis" x1="{fmt(ax0)}" y1="{fmt(ay0)}" x2="{fmt(ax1 + 6)}" y2="{fmt(ay0)}"/>')
    doc.add(arrow_head(ax1 + 6, ay0, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(ax0)}" y1="{fmt(ay0)}" x2="{fmt(ax0)}" y2="{fmt(ay1 - 8)}"/>')
    doc.add(arrow_head(ax0, ay1 - 8, 0, -1, 6.5))
    doc.add(f'<text class="sm" x="{fmt(0.5 * (ax0 + ax1))}" y="472" text-anchor="middle">相位寄存器位数 t (bit)</text>')
    doc.add(f'<text class="sm" x="44" y="{fmt(0.5 * (ay0 + ay1))}" text-anchor="middle" transform="rotate(-90 44 {fmt(0.5 * (ay0 + ay1))})">成功概率（无量纲）</text>')

    flag_pts = [(map_at(float(c["phase_bits"])), map_ap(c["flag_success"])) for c in hhl_rows]
    clean_pts = [(map_at(float(c["phase_bits"])), map_ap(c["phase_zero_and_flag_success"])) for c in hhl_rows]
    doc.add(f'<path class="c1" stroke-width="2.2" d="{path_from_points(flag_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.1" stroke-dasharray="6 3" d="{path_from_points(clean_pts)}"/>')
    for px, py in flag_pts:
        doc.add(f'<circle class="c1-fill" cx="{fmt(px)}" cy="{fmt(py)}" r="4.2"/>')
    for px, py in clean_pts:
        doc.add(f'<rect class="c2-fill" x="{fmt(px - 3.6)}" y="{fmt(py - 3.6)}" width="7.2" height="7.2" rx="1"/>')

    # Annotate the t=4 garbage gap cleanly inside open space left of t=4
    gx_bar = flag_pts[1][0] - 8.0
    doc.add(f'<line class="c4" stroke-width="1.5" x1="{fmt(gx_bar)}" y1="{fmt(flag_pts[1][1] + 2)}" x2="{fmt(gx_bar)}" y2="{fmt(clean_pts[1][1] - 2)}"/>')
    doc.add(f'<line class="c4" stroke-width="1.3" x1="{fmt(gx_bar - 3)}" y1="{fmt(flag_pts[1][1] + 2)}" x2="{fmt(gx_bar + 3)}" y2="{fmt(flag_pts[1][1] + 2)}"/>')
    doc.add(f'<line class="c4" stroke-width="1.3" x1="{fmt(gx_bar - 3)}" y1="{fmt(clean_pts[1][1] - 2)}" x2="{fmt(gx_bar + 3)}" y2="{fmt(clean_pts[1][1] - 2)}"/>')
    doc.add(f'<text class="xsb c4-txt" x="{fmt(gx_bar - 6)}" y="274" text-anchor="end">t=4 差值</text>')
    doc.add(f'<text class="xs c4-txt" x="{fmt(gx_bar - 6)}" y="289" text-anchor="end">0.024</text>')

    doc.add('<rect class="pill" x="40" y="496" width="282" height="40" rx="8"/>')
    doc.add('<text class="xs" x="181" y="520" text-anchor="middle">两曲线之差即逆 QPE 后残留的相位垃圾概率</text>')

    # --- Panel B: Root fidelity & conditional garbage ---
    doc.add_panel(347, 96, 306, 456, "B. 逆 QPE 无法消零相位垃圾")
    doc.add('<line class="c1" stroke-width="2.0" x1="360" y1="154" x2="380" y2="154"/>')
    doc.add('<circle class="c1-fill" cx="370" cy="154" r="3.4"/>')
    doc.add('<text class="xs c1-txt" x="386" y="158">仅选标志混态根保真度 F</text>')
    doc.add('<line class="c2" stroke-width="2.0" stroke-dasharray="5 3" x1="360" y1="174" x2="380" y2="174"/>')
    doc.add('<rect class="c2-fill" x="366.5" y="170.5" width="7" height="7" rx="1"/>')
    doc.add('<text class="xs c2-txt" x="386" y="178">条件垃圾 P(相位 ≠ 0 | 标志 = 1)</text>')

    bx0, bx1, by0, by1 = 406.0, 636.0, 432.0, 194.0

    def map_bt(tv: float) -> float:
        return bx0 + (tv - 2.65) / 3.7 * (bx1 - bx0)

    def map_bv(vv: float) -> float:
        return by0 - (vv / 1.08) * (by0 - by1)

    for vv in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        yv = map_bv(vv)
        doc.add(f'<line class="grid" x1="{fmt(bx0)}" y1="{fmt(yv)}" x2="{fmt(bx1)}" y2="{fmt(yv)}"/>')
        doc.add(f'<text class="xs" x="{fmt(bx0 - 7)}" y="{fmt(yv + 4)}" text-anchor="end">{vv:.1f}</text>')
    for tv in (3, 4, 5, 6):
        xt = map_bt(float(tv))
        doc.add(f'<line class="grid" x1="{fmt(xt)}" y1="{fmt(by1)}" x2="{fmt(xt)}" y2="{fmt(by0)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xt)}" y="{fmt(by0 + 17)}" text-anchor="middle">{tv}</text>')

    doc.add(f'<line class="axis" x1="{fmt(bx0)}" y1="{fmt(by0)}" x2="{fmt(bx1 + 6)}" y2="{fmt(by0)}"/>')
    doc.add(arrow_head(bx1 + 6, by0, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(bx0)}" y1="{fmt(by0)}" x2="{fmt(bx0)}" y2="{fmt(by1 - 8)}"/>')
    doc.add(arrow_head(bx0, by1 - 8, 0, -1, 6.5))
    doc.add(f'<text class="sm" x="{fmt(0.5 * (bx0 + bx1))}" y="472" text-anchor="middle">相位寄存器位数 t (bit)</text>')
    doc.add(f'<text class="sm" x="363" y="{fmt(0.5 * (by0 + by1))}" text-anchor="middle" transform="rotate(-90 363 {fmt(0.5 * (by0 + by1))})">无量纲指标</text>')

    fid_pts = [(map_bt(float(c["phase_bits"])), map_bv(c["mixed_root_fidelity"])) for c in hhl_rows]
    gar_pts = [(map_bt(float(c["phase_bits"])), map_bv(c["garbage_given_flag"])) for c in hhl_rows]
    doc.add(f'<path class="c1" stroke-width="2.2" d="{path_from_points(fid_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.1" stroke-dasharray="6 3" d="{path_from_points(gar_pts)}"/>')
    for px, py in fid_pts:
        doc.add(f'<circle class="c1-fill" cx="{fmt(px)}" cy="{fmt(py)}" r="4.2"/>')
    for px, py in gar_pts:
        doc.add(f'<rect class="c2-fill" x="{fmt(px - 3.6)}" y="{fmt(py - 3.6)}" width="7.2" height="7.2" rx="1"/>')

    # Callouts in wide-open center space between F (~0.98) and garbage (~0.14)
    doc.add(f'<text class="xsb c1-txt" x="{fmt(fid_pts[0][0] + 6)}" y="{fmt(fid_pts[0][1] + 22)}">t=3: F = {hhl_rows[0]["mixed_root_fidelity"]:.3f}</text>')
    doc.add(f'<text class="xsb c1-txt" x="{fmt(fid_pts[3][0] + 8)}" y="{fmt(fid_pts[3][1] + 24)}" text-anchor="end">t=6: F = {hhl_rows[3]["mixed_root_fidelity"]:.3f}</text>')
    doc.add(f'<text class="xsb c2-txt" x="{fmt(gar_pts[1][0])}" y="{fmt(gar_pts[1][1] - 14)}" text-anchor="middle">t=4: 14.5%</text>')
    doc.add(f'<text class="xsb c2-txt" x="{fmt(gar_pts[3][0] + 8)}" y="{fmt(gar_pts[3][1] - 16)}" text-anchor="end">t=6: 3.4%</text>')

    doc.add('<rect class="pill" x="359" y="496" width="282" height="40" rx="8"/>')
    doc.add('<text class="xs" x="500" y="520" text-anchor="middle">t = 4 垃圾先升至 14.5%，至 t = 6 才降至 3.4%</text>')

    # --- Panel C: 4D hypercube SKW walk ---
    doc.add_panel(666, 96, 306, 456, "C. 4 维超立方体 SKW 离散行走")
    doc.add('<line class="c1" stroke-width="2.0" x1="678" y1="154" x2="696" y2="154"/>')
    doc.add('<circle class="c1-fill" cx="687" cy="154" r="3.4"/>')
    doc.add('<text class="xs c1-txt" x="701" y="158">SKW 标记概率</text>')
    doc.add('<line class="guide" x1="788" y1="154" x2="804" y2="154"/>')
    doc.add('<text class="xs" x="809" y="158">无标记基线 1/16</text>')
    doc.add('<rect class="hollow-c2" x="683" y="169" width="8.5" height="8.5" rx="1"/>')
    doc.add('<text class="xs c2-txt" x="698" y="178">预选最早峰值（k = 4，p = 25/64）</text>')

    cx0, cx1, cy0, cy1 = 724.0, 956.0, 432.0, 194.0

    def map_ck(kv: float) -> float:
        return cx0 + (kv + 0.4) / 16.8 * (cx1 - cx0)

    def map_cp(pv: float) -> float:
        return cy0 - (pv + 0.015) / 0.475 * (cy0 - cy1)

    for pv in (0.0, 0.1, 0.2, 0.3, 0.4):
        yp = map_cp(pv)
        doc.add(f'<line class="grid" x1="{fmt(cx0)}" y1="{fmt(yp)}" x2="{fmt(cx1)}" y2="{fmt(yp)}"/>')
        doc.add(f'<text class="xs" x="{fmt(cx0 - 7)}" y="{fmt(yp + 4)}" text-anchor="end">{pv:.1f}</text>')
    for kv in (0, 4, 8, 12, 16):
        xk = map_ck(float(kv))
        doc.add(f'<line class="grid" x1="{fmt(xk)}" y1="{fmt(cy1)}" x2="{fmt(xk)}" y2="{fmt(cy0)}"/>')
        doc.add(f'<text class="xs" x="{fmt(xk)}" y="{fmt(cy0 + 17)}" text-anchor="middle">{kv}</text>')

    y_base = map_cp(1.0 / 16.0)
    doc.add(f'<line class="guide" x1="{fmt(cx0)}" y1="{fmt(y_base)}" x2="{fmt(cx1)}" y2="{fmt(y_base)}"/>')
    doc.add(f'<line class="axis" x1="{fmt(cx0)}" y1="{fmt(cy0)}" x2="{fmt(cx1 + 6)}" y2="{fmt(cy0)}"/>')
    doc.add(arrow_head(cx1 + 6, cy0, 1, 0, 6.5))
    doc.add(f'<line class="axis" x1="{fmt(cx0)}" y1="{fmt(cy0)}" x2="{fmt(cx0)}" y2="{fmt(cy1 - 8)}"/>')
    doc.add(arrow_head(cx0, cy1 - 8, 0, -1, 6.5))
    doc.add(f'<text class="sm" x="{fmt(0.5 * (cx0 + cx1))}" y="472" text-anchor="middle">完整行走步数 k（步）</text>')
    doc.add(f'<text class="sm" x="682" y="{fmt(0.5 * (cy0 + cy1))}" text-anchor="middle" transform="rotate(-90 682 {fmt(0.5 * (cy0 + cy1))})">标记顶点概率</text>')

    w_pts = [(map_ck(float(w["steps"])), map_cp(w["marked_probability"])) for w in walk_rows]
    doc.add(f'<path class="c1" stroke-width="2.1" d="{path_from_points(w_pts)}"/>')
    for px, py in w_pts:
        doc.add(f'<circle class="c1-fill" cx="{fmt(px)}" cy="{fmt(py)}" r="3.2"/>')

    # Highlight earliest peak k=4 and trough k=8
    pk4x, pk4y = w_pts[4]
    tr8x, tr8y = w_pts[8]
    doc.add(f'<rect class="hollow-c2" x="{fmt(pk4x - 5.5)}" y="{fmt(pk4y - 5.5)}" width="11" height="11" rx="1.5"/>')
    doc.add(f'<text class="xsb c2-txt" x="{fmt(pk4x + 7)}" y="{fmt(pk4y - 14)}" text-anchor="middle">k=4: 25/64 ≈ 0.391</text>')

    doc.add('<rect class="pill-bg" x="812" y="232" width="72" height="34" rx="6"/>')
    doc.add('<text class="xsb c2-txt" x="848" y="246" text-anchor="middle">k = 8 过步</text>')
    doc.add('<text class="xs" x="848" y="260" text-anchor="middle">跌至 1/256</text>')
    doc.add(f'<line class="c2" stroke-width="1.3" stroke-dasharray="3 2" x1="846" y1="266" x2="{fmt(tr8x)}" y2="{fmt(tr8y - 6)}"/>')

    doc.add('<rect class="note" x="678" y="496" width="282" height="40" rx="8"/>')
    doc.add('<text class="xs" x="819" y="520" text-anchor="middle">存在最优停步峰；多走 4 步即过旋跌至 0.39%</text>')

    return doc.render(), {"hhl_t6_fid": round(hhl_rows[3]["mixed_root_fidelity"], 5), "walk_k4": walk_rows[4]["marked_probability"]}


# ---------------------------------------------------------------------------
# Figure 7: lab-zero-failure.svg
# ---------------------------------------------------------------------------
def build_fig7_lab_zero_failure() -> tuple[str, dict[str, object]]:
    src = ROOT / "codes" / "practice" / "research-results.json"
    zf = json.loads(src.read_text(encoding="utf-8"))["zero_failure"]
    alpha = float(zf["alpha"])
    target = float(zf["target"])
    n_req = int(zf["required_n"])

    def zero_failure_upper(n_val: float) -> float:
        # Exact inversion of (1 - p_U)^N = alpha  =>  p_U = 1 - alpha^(1/N)
        return -math.expm1(math.log(alpha) / n_val)

    u1000 = zero_failure_upper(1000.0)
    u2995 = zero_failure_upper(float(n_req))
    assert alpha == 0.05 and target == 0.001 and n_req == 2995
    assert math.isclose(u1000, zf["upper"], rel_tol=1e-12)
    assert u2995 <= target < zero_failure_upper(float(n_req - 1))

    doc = SvgDoc(
        title="零失败测试的单侧 95% 错误概率上界与预定样本数 N",
        desc=(
            "双对数坐标精确绘制独立同分布试验观测到 0 次失败时的单侧 95% 错误概率上界 p_U = 1 − 0.05^(1/N)（N ∈ [100, 10000]），"
            "并标出目标门槛 p* = 0.001 以及两个关键里程碑：N = 1,000 时 p_U ≈ 0.299%，须至 N = 2,995 才首次压至 0.1% 以下。"
        ),
    )
    doc.add_header(
        "零失败测试的单侧 95% 错误概率上界与预定样本数 N",
        f'精确二项反演 p{sub("U")} = 1 − α{sup("1/N")}（α = 0.05，近乎“三倍法则” 3/N）：观测到 0 次失败不等于真实错误率为零',
        raw_sub=True,
    )
    doc.add_panel(28, 96, 944, 456, "双对数坐标下零失败 95% 上界曲线与 p* = 0.001 目标门槛（N ∈ [100, 10,000]）")

    px0, px1 = 122.0, 682.0
    py0, py1 = 434.0, 162.0
    lx_min, lx_max = 2.0, 4.0   # N in [100, 10000]
    ly_min, ly_max = -4.0, -1.0  # p_U in [1e-4, 1e-1]

    def map_n(nv: float) -> float:
        return px0 + (math.log10(nv) - lx_min) / (lx_max - lx_min) * (px1 - px0)

    def map_p(pv: float) -> float:
        return py0 - (math.log10(pv) - ly_min) / (ly_max - ly_min) * (py0 - py1)

    # Shaded target-achieved region p_U <= 0.001
    y_tgt = map_p(target)
    doc.add(f'<rect class="area3" x="{fmt(px0)}" y="{fmt(y_tgt)}" width="{fmt(px1 - px0)}" height="{fmt(py0 - y_tgt)}"/>')
    doc.add(f'<text class="xsb c3-txt" x="136" y="420">达标区：p{sub("U")} ≤ 0.001（0.1%）</text>')

    # Minor vertical & horizontal gridlines
    for mult in (2, 3, 5):
        for dec in (2, 3):
            xv = map_n(mult * (10.0 ** dec))
            if px0 < xv < px1:
                doc.add(f'<line class="grid-minor" x1="{fmt(xv)}" y1="{fmt(py1)}" x2="{fmt(xv)}" y2="{fmt(py0)}"/>')
        for dec in (-4, -3, -2):
            yv = map_p(mult * (10.0 ** dec))
            if py1 < yv < py0:
                doc.add(f'<line class="grid-minor" x1="{fmt(px0)}" y1="{fmt(yv)}" x2="{fmt(px1)}" y2="{fmt(yv)}"/>')

    # Major Y ticks
    for exp_v in (-4, -3, -2, -1):
        yt = map_p(10.0 ** exp_v)
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(yt)}" x2="{fmt(px1)}" y2="{fmt(yt)}"/>')
        doc.add(f'<text class="sm" x="{fmt(px0 - 10)}" y="{fmt(yt + 4)}" text-anchor="end">10{sup(str(exp_v))}</text>')

    # Major X ticks
    for nv, lbl_n in ((100, "100"), (300, "300"), (1000, "1,000"), (3000, "3,000"), (10000, "10,000")):
        xn = map_n(float(nv))
        doc.add(f'<line class="grid" x1="{fmt(xn)}" y1="{fmt(py1)}" x2="{fmt(xn)}" y2="{fmt(py0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xn)}" y="{fmt(py0 + 19)}" text-anchor="middle">{lbl_n}</text>')

    # Target threshold dashed line
    doc.add(f'<line class="c2" stroke-width="2.0" stroke-dasharray="7 4" x1="{fmt(px0)}" y1="{fmt(y_tgt)}" x2="{fmt(px1)}" y2="{fmt(y_tgt)}"/>')
    doc.add(f'<text class="xsb c2-txt" x="136" y="{fmt(y_tgt - 7)}">目标错误率门槛 p* = 0.001（0.1%）</text>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px1 + 8)}" y2="{fmt(py0)}"/>')
    doc.add(arrow_head(px1 + 8, py0, 1, 0))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px0)}" y2="{fmt(py1 - 10)}"/>')
    doc.add(arrow_head(px0, py1 - 10, 0, -1))
    doc.add(f'<text class="lbl" x="{fmt(0.5 * (px0 + px1))}" y="478" text-anchor="middle">预先固定的独立试验次数 N（对数刻度）</text>')
    doc.add(
        f'<text class="lbl" x="54" y="{fmt(0.5 * (py0 + py1))}" text-anchor="middle" '
        f'transform="rotate(-90 54 {fmt(0.5 * (py0 + py1))})">单侧 95% 错误概率上界 p{sub("U")}（对数刻度）</text>'
    )

    # Exact curve: 120 log-spaced points from N=100 to N=10000
    curve_pts = []
    for i in range(121):
        nv = 10.0 ** (2.0 + 2.0 * i / 120.0)
        curve_pts.append((map_n(nv), map_p(zero_failure_upper(nv))))
    doc.add(f'<path class="c1" stroke-width="2.8" d="{path_from_points(curve_pts)}"/>')

    # Milestone drop guides and points
    x1000, y1000 = map_n(1000.0), map_p(u1000)
    x2995, y2995 = map_n(float(n_req)), map_p(u2995)
    doc.add(f'<line class="guide" x1="{fmt(x1000)}" y1="{fmt(y1000 + 6)}" x2="{fmt(x1000)}" y2="{fmt(py0)}"/>')
    doc.add(f'<line class="guide" x1="{fmt(x2995)}" y1="{fmt(y2995 + 6)}" x2="{fmt(x2995)}" y2="{fmt(py0)}"/>')
    doc.add(f'<circle class="c2-fill" cx="{fmt(x1000)}" cy="{fmt(y1000)}" r="5.8"/>')
    doc.add(f'<circle class="c2-fill" cx="{fmt(x2995)}" cy="{fmt(y2995)}" r="5.8"/>')

    # Non-overlapping callout boxes in wide-open upper-right space above the curve
    doc.add('<rect class="c1-soft" x="436" y="190" width="212" height="46" rx="8"/>')
    doc.add('<text class="xsb c1-txt" x="542" y="209" text-anchor="middle">N = 1,000 次零失败</text>')
    doc.add(f'<text class="xs c1-txt" x="542" y="226" text-anchor="middle">p{sub("U")} = {u1000:.6f}（约 0.299%）</text>')
    doc.add(f'<line class="c1" stroke-width="1.4" x1="454" y1="236" x2="{fmt(x1000 + 5)}" y2="{fmt(y1000 - 5)}"/>')

    doc.add('<rect class="c2-soft" x="498" y="264" width="174" height="46" rx="8"/>')
    doc.add('<text class="xsb c2-txt" x="585" y="283" text-anchor="middle">N = 2,995 次零失败</text>')
    doc.add('<text class="xs c2-txt" x="585" y="300" text-anchor="middle">首次压至 0.001（0.1%）以下</text>')
    doc.add(f'<line class="c2" stroke-width="1.4" x1="{fmt(x2995)}" y1="310" x2="{fmt(x2995)}" y2="{fmt(y2995 - 7)}"/>')

    # Right summary & formula card
    doc.add('<rect class="pill" x="704" y="154" width="252" height="326" rx="10"/>')
    doc.add('<text class="smb" x="720" y="177">图例与精确二项公式</text>')
    doc.add('<line class="c1" stroke-width="2.6" x1="720" y1="198" x2="744" y2="198"/>')
    doc.add('<text class="xs" x="752" y="202">零失败单侧 95% 精确上界</text>')
    doc.add('<line class="c2" stroke-width="2.0" stroke-dasharray="6 3" x1="720" y1="220" x2="744" y2="220"/>')
    doc.add('<text class="xs" x="752" y="224">目标阈值 p* = 0.001</text>')
    doc.add('<circle class="c2-fill" cx="732" cy="242" r="4.5"/>')
    doc.add('<text class="xs" x="752" y="246">关键样本量验证点</text>')

    doc.add('<line class="grid" x1="718" y1="260" x2="942" y2="260"/>')
    doc.add(f'<text class="xsb" x="720" y="280">(1 − p{sub("U")}){sup("N")} = α （α = 0.05）</text>')
    doc.add(f'<text class="xs c1-txt" x="720" y="300">p{sub("U")} = 1 − 0.05{sup("1/N")} ≈ 3 / N</text>')
    doc.add('<text class="xs" x="720" y="320">N ≥ ⌈ln(α) / ln(1 − p*)⌉</text>')

    doc.add('<line class="grid" x1="718" y1="336" x2="942" y2="336"/>')
    doc.add('<text class="xsb" x="720" y="356">常见样本量速查（0 失败）</text>')
    doc.add(f'<text class="xs" x="720" y="378">N = 100     → p{sub("U")} ≈ {zero_failure_upper(100) * 100:.2f}%</text>')
    doc.add(f'<text class="xs" x="720" y="398">N = 1,000   → p{sub("U")} ≈ {u1000 * 100:.3f}%</text>')
    doc.add(f'<text class="xs c2-txt" x="720" y="418">N = 2,995   → p{sub("U")} ≤ 0.100%</text>')
    doc.add(f'<text class="xs" x="720" y="438">N = 10,000  → p{sub("U")} ≈ {zero_failure_upper(10000) * 100:.3f}%</text>')
    doc.add(f'<text class="xs" x="720" y="458">p* = 10{sup("−6")}   → 需 N ≥ 2,995,731</text>')

    # Bottom takeaway note inside panel
    doc.add('<rect class="note" x="44" y="496" width="912" height="40" rx="9"/>')
    doc.add(
        '<text class="sm" x="500" y="520" text-anchor="middle">'
        '前提边界：样本数 N 须在试验前预先固定且独立同分布；反复凑“连续零失败”区间再套用公式将破坏 95% 覆盖保证。'
        '</text>'
    )
    return doc.render(), {"u1000": round(u1000, 8), "u2995": round(u2995, 8), "n_req": n_req}


# ---------------------------------------------------------------------------
# XML, metadata hygiene & Playwright + System Chrome dual-theme getBBox() audit
# ---------------------------------------------------------------------------
FORBIDDEN_PATTERN = re.compile(r"round\s*7\d|matplotlib|rdf:RDF|dc:creator", re.IGNORECASE)


def verify_svg_xml(svg_text: str, filename: str) -> dict[str, int]:
    root = ET.fromstring(svg_text)
    vb = root.attrib.get("viewBox", "")
    assert vb == f"0 0 {W} {H}", f"{filename}: unexpected viewBox {vb!r}"
    assert ":root{color-scheme:light dark}" in svg_text, f"{filename}: missing color-scheme"
    assert "@media(prefers-color-scheme:dark)" in svg_text, f"{filename}: missing dark mode media query"
    bad = FORBIDDEN_PATTERN.findall(svg_text)
    assert not bad, f"{filename}: forbidden residual metadata/text found: {bad}"

    ns = {"svg": "http://www.w3.org/2000/svg"}
    title_el = root.find("svg:title", ns)
    desc_el = root.find("svg:desc", ns)
    assert title_el is not None and (title_el.text or "").strip(), f"{filename}: missing <title>"
    assert desc_el is not None and (desc_el.text or "").strip(), f"{filename}: missing <desc>"

    text_nodes = root.findall(".//svg:text", ns)
    assert len(text_nodes) >= 12, f"{filename}: too few <text> elements ({len(text_nodes)})"
    for el in text_nodes:
        x = float(el.attrib["x"])
        y = float(el.attrib["y"])
        assert MARGIN <= x <= W - MARGIN, f"{filename}: text x={x} out of margin ({''.join(el.itertext())!r})"
        assert MARGIN <= y <= H - MARGIN, f"{filename}: text y={y} out of margin ({''.join(el.itertext())!r})"

    return {"text_count": len(text_nodes), "bytes": len(svg_text.encode("utf-8"))}


def verify_with_chrome_bbox(
    svg_paths: list[Path],
    screenshot_dir: Path | None = None,
) -> list[dict[str, object]]:
    """Run dual-theme (light + dark) System Chrome getBBox() audit via Playwright."""
    from playwright.sync_api import sync_playwright

    js_audit = """(margin) => {
      const svg = document.querySelector('svg');
      const svgRect = svg.getBoundingClientRect();
      const vb = svg.viewBox.baseVal;
      const sx = vb.width / svgRect.width;
      const sy = vb.height / svgRect.height;
      const toBox = (el) => {
        const r = el.getBoundingClientRect();
        return {
          x1: (r.left - svgRect.left) * sx,
          y1: (r.top - svgRect.top) * sy,
          x2: (r.right - svgRect.left) * sx,
          y2: (r.bottom - svgRect.top) * sy,
        };
      };
      const bgEl = svg.querySelector('rect.bg');
      const bgFill = bgEl ? getComputedStyle(bgEl).fill : '';

      const texts = Array.from(svg.querySelectorAll('text')).map((el, idx) => {
        const b = toBox(el);
        const bb = el.getBBox();
        return {
          idx,
          text: (el.textContent || '').replace(/\\u200b/g, '').trim(),
          ...b,
          bbW: bb.width,
          bbH: bb.height,
        };
      });

      const boxSelector = 'rect.panel, rect.pill, rect.pill-bg, rect.note, rect.c1-soft, rect.c2-soft, rect.c3-soft, rect.c4-soft';
      const containers = Array.from(svg.querySelectorAll(boxSelector)).map((el, idx) => ({
        idx,
        cls: el.getAttribute('class') || '',
        ...toBox(el),
      }));

      const oob = [];
      for (const t of texts) {
        if (t.x1 < margin - 0.5 || t.y1 < margin - 0.5 || t.x2 > vb.width - margin + 0.5 || t.y2 > vb.height - margin + 0.5) {
          oob.push(t);
        }
      }

      const overlaps = [];
      for (let i = 0; i < texts.length; i++) {
        for (let j = i + 1; j < texts.length; j++) {
          const a = texts[i], b = texts[j];
          const ox = Math.min(a.x2, b.x2) - Math.max(a.x1, b.x1);
          const oy = Math.min(a.y2, b.y2) - Math.max(a.y1, b.y1);
          if (ox > 0.8 && oy > 0.8) {
            overlaps.push({ a: a.text, b: b.text, ox: Number(ox.toFixed(2)), oy: Number(oy.toFixed(2)) });
          }
        }
      }

      const pierces = [];
      for (const t of texts) {
        for (const c of containers) {
          const ox = Math.min(t.x2, c.x2) - Math.max(t.x1, c.x1);
          const oy = Math.min(t.y2, c.y2) - Math.max(t.y1, c.y1);
          if (ox > 1.0 && oy > 1.0) {
            const inside = (t.x1 >= c.x1 - 0.5 && t.y1 >= c.y1 - 0.5 && t.x2 <= c.x2 + 0.5 && t.y2 <= c.y2 + 0.5);
            if (!inside) {
              pierces.push({
                text: t.text,
                rectCls: c.cls,
                textBox: [Number(t.x1.toFixed(1)), Number(t.y1.toFixed(1)), Number(t.x2.toFixed(1)), Number(t.y2.toFixed(1))],
                rectBox: [Number(c.x1.toFixed(1)), Number(c.y1.toFixed(1)), Number(c.x2.toFixed(1)), Number(c.y2.toFixed(1))],
              });
            }
          }
        }
      }

      return {
        textCount: texts.length,
        bgFill,
        minX: Number(Math.min(...texts.map(t => t.x1)).toFixed(1)),
        minY: Number(Math.min(...texts.map(t => t.y1)).toFixed(1)),
        maxX: Number(Math.max(...texts.map(t => t.x2)).toFixed(1)),
        maxY: Number(Math.max(...texts.map(t => t.y2)).toFixed(1)),
        oob,
        overlaps,
        pierces,
      };
    }"""

    results: list[dict[str, object]] = []
    failures: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        try:
            page = browser.new_page(viewport={"width": W, "height": H})
            for svg_path in svg_paths:
                svg_content = svg_path.read_text(encoding="utf-8")
                html = (
                    "<!doctype html><html><head><meta charset='utf-8'>"
                    f"<style>html,body{{margin:0;padding:0;background:transparent;}}svg{{display:block;width:{W}px;height:{H}px;}}</style>"
                    f"</head><body>{svg_content}</body></html>"
                )
                scheme_fills: dict[str, str] = {}
                for scheme in ("light", "dark"):
                    page.emulate_media(color_scheme=scheme)
                    page.set_content(html, wait_until="load")
                    res = page.evaluate(js_audit, MARGIN)
                    scheme_fills[scheme] = res["bgFill"]
                    print(
                        f"[CHROME-{scheme.upper():5s}] {svg_path.name}: textCount={res['textCount']} | "
                        f"span x=[{res['minX']}, {res['maxX']}], y=[{res['minY']}, {res['maxY']}] | "
                        f"oob={len(res['oob'])}, overlap={len(res['overlaps'])}, pierce={len(res['pierces'])} | bg={res['bgFill']}"
                    )
                    for item in res["oob"]:
                        print(f"  [OOB] {item['text']!r}: ({item['x1']:.1f},{item['y1']:.1f})..({item['x2']:.1f},{item['y2']:.1f})")
                    for item in res["overlaps"]:
                        print(f"  [OVERLAP] {item['a']!r} <-> {item['b']!r} (ox={item['ox']}, oy={item['oy']})")
                    for item in res["pierces"]:
                        print(f"  [PIERCE] {item['text']!r} crosses .{item['rectCls']} {item['textBox']} vs {item['rectBox']}")

                    if screenshot_dir is not None:
                        screenshot_dir.mkdir(parents=True, exist_ok=True)
                        page.screenshot(path=str(screenshot_dir / f"{svg_path.stem}-{scheme}.png"))

                    if res["textCount"] <= 0 or res["oob"] or res["overlaps"] or res["pierces"]:
                        failures.append(
                            f"{svg_path.name} ({scheme}): text={res['textCount']} oob={len(res['oob'])} "
                            f"overlap={len(res['overlaps'])} pierce={len(res['pierces'])}"
                        )
                    results.append({"file": svg_path.name, "scheme": scheme, **res})

                if scheme_fills["light"] == scheme_fills["dark"]:
                    failures.append(f"{svg_path.name}: dark theme did not activate ({scheme_fills})")
        finally:
            browser.close()
    assert not failures, "Chrome getBBox() audit failed:\n  " + "\n  ".join(failures)
    return results


def main() -> None:
    if not __debug__:
        raise RuntimeError("Run without -O so scientific assertions stay enabled")
    parser = argparse.ArgumentParser(description="Upgrade 7 legacy SVGs (V3 Part 2) with dual-theme pure <text>.")
    parser.add_argument("--check-bbox", action="store_true", help="Run Playwright + System Chrome dual-theme getBBox() audit.")
    parser.add_argument("--screenshots", type=Path, default=None, help="Directory to save light/dark PNG previews.")
    args = parser.parse_args()

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    builders = [
        ("round72-systems-qec.svg", build_fig1_round72_qec),
        ("round73-systems-qec.svg", build_fig2_round73_qec),
        ("round72-systems-control.svg", build_fig3_round72_control),
        ("round73-systems-control.svg", build_fig4_round73_control),
        ("round72-algorithms.svg", build_fig5_round72_algorithms),
        ("round73-algorithms.svg", build_fig6_round73_algorithms),
        ("lab-zero-failure.svg", build_fig7_lab_zero_failure),
    ]

    out_paths: list[Path] = []
    for fname, fn in builders:
        svg_text, metrics = fn()
        check = verify_svg_xml(svg_text, fname)
        out_path = ASSETS_DIR / fname
        out_path.write_text(svg_text, encoding="utf-8")
        out_paths.append(out_path)
        print(f"[OK] {fname}: {check['bytes']} bytes, {check['text_count']} <text> | metrics={metrics}")

    if args.check_bbox:
        verify_with_chrome_bbox(out_paths, args.screenshots)


if __name__ == "__main__":
    main()
