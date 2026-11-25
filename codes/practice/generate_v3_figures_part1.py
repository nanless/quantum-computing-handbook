#!/usr/bin/env python3
"""Generate 7 light/dark-adaptive scientific SVG figures (V3 Part 1: Ch00, Ch01, Q1, Q2, Ch05, Ch08)
using Python 3 standard library only.

Outputs to handbook/assets/:
  1. v3-00-amplitude-vs-memory.svg               (Ch00: classical probability vs amplitude interference & memory scaling)
  2. v3-01-svd-condition-ellipse.svg             (Ch01: SVD W*Sigma*V^dag geometry & readout condition number kappa_2)
  3. v3-q1-stern-gerlach-cascade.svg             (Q1:   3-stage Z->X->Z Stern-Gerlach cascade vs classical pre-labeled)
  4. v3-q2-uncertainty-robertson-schrodinger.svg (Q2:   Robertson vs Schrodinger saturation & non-commuting Bloch paths)
  5. v3-q2-lindblad-trajectories.svg             (Q2:   Lindblad decay, 8 MCWF jump steps & 64/512/4096 convergence)
  6. v3-05-superoperator-ptm-twirling.svg        (Ch05: 5 superoperator representations & Pauli twirling PTM heatmaps)
  7. v3-08-h2-vqe-barren-plateau.svg             (Ch08: Exact STO-3G H2 FCI/VQE/SQD vs RHF & DLA barren plateau scaling)

Run (pure Python 3 standard library):
  python3 codes/practice/generate_v3_figures_part1.py

Optional Playwright + System Chrome getBBox() audit & dual-theme PNG screenshots:
  python3 codes/practice/generate_v3_figures_part1.py --check-bbox --screenshots /tmp/v3_part1_previews

Dependencies:
  Generation uses Python 3 standard library only (argparse, cmath, math, random, pathlib,
  xml.etree.ElementTree, xml.sax.saxutils). Fixed RNG seed (202605) for MCWF trajectories.
"""

from __future__ import annotations

import argparse
import cmath
import math
import random
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT / "handbook" / "assets"
W, H = 1000, 580
MARGIN = 30
TOL = 1e-10
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


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
.math-txt{font-family:Georgia,'Times New Roman',serif;font-size:14px;font-weight:700;fill:#13263a}
.axis{stroke:#19324d;stroke-width:1.7;fill:none}
.axis-fill{fill:#19324d}
.grid{stroke:#dce5ee;stroke-width:1;fill:none}
.guide{stroke:#7c93a8;stroke-width:1.25;stroke-dasharray:5 4;fill:none}
.unit-circle{stroke:#5b7790;stroke-width:1.6;stroke-dasharray:6 5;fill:none}
.bloch-circle{fill:#dff4ff;fill-opacity:.34;stroke:#2e6f95;stroke-width:2.0}
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
.c5{stroke:#6b4ea8;fill:none}
.c5-fill{fill:#6b4ea8}
.c5-txt{fill:#51358a}
.c5-soft{fill:#efe9fb;stroke:#6b4ea8;stroke-width:1.5}
.note{fill:#fff8e6;stroke:#c98d24;stroke-width:1.3}
.pill{fill:#f3f7fa;stroke:#9cb1c4;stroke-width:1.2}
.pill-bg{fill:#ffffff;fill-opacity:.94;stroke:#9cb1c4;stroke-width:1.1}
.area1{fill:#1b6ca8;fill-opacity:.13}
.area2{fill:#c74b34;fill-opacity:.14}
.area3{fill:#1e7a5c;fill-opacity:.15}
.area4{fill:#b57614;fill-opacity:.13}
.bar-neutral{fill:#e2e8f0;stroke:#556b80;stroke-width:1.4}
.wall{fill:#334e68;stroke:#19324d;stroke-width:1.2}
.badge-txt{fill:#ffffff;font-size:11.5px;font-weight:700}
.hm-pos1{fill:#1b6ca8;stroke:#ffffff;stroke-width:1.4}
.hm-pos2{fill:#2d82bf;stroke:#ffffff;stroke-width:1.4}
.hm-pos3{fill:#f3b562;stroke:#ffffff;stroke-width:1.4}
.hm-neg3{fill:#d96b57;stroke:#ffffff;stroke-width:1.4}
.hm-zero{fill:#edf2f7;stroke:#cbd5e1;stroke-width:1.1}
.hm-hi{fill:none;stroke:#b57614;stroke-width:2.0;stroke-dasharray:4 2}
.hm-inv{fill:#ffffff;font-size:10.5px;font-weight:700}
.hm-dark{fill:#13263a;font-size:10.5px;font-weight:700}
.hm-muted{fill:#64748b;font-size:10.5px;font-weight:500}
.hatch-stroke1{stroke:#1b6ca8;stroke-width:1.2;stroke-opacity:.42}
.hatch-stroke2{stroke:#c74b34;stroke-width:1.2;stroke-opacity:.45}
.hatch-stroke3{stroke:#1e7a5c;stroke-width:1.2;stroke-opacity:.42}
.hatch-stroke0{stroke:#556b80;stroke-width:1.1;stroke-opacity:.38}
@media(prefers-color-scheme:dark){
  .bg{fill:#0f1720}
  .panel{fill:#16222e;stroke:#354c61}
  .subpanel{fill:#1b2a38;stroke:#3b5369}
  .phead{fill:#1c2d3d}
  .title,.sec,.lblb,.math-txt{fill:#eef6ff}
  .subtitle,.sm,.xs{fill:#b7cde0}
  .lbl,.smb,.xsb{fill:#d7e7f5}
  .axis{stroke:#cde0f2}
  .axis-fill{fill:#cde0f2}
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
  .c5{stroke:#b79ef5}
  .c5-fill{fill:#b79ef5}
  .c5-txt{fill:#cbb8fa}
  .c5-soft{fill:#2d2147;stroke:#b79ef5}
  .note{fill:#332914;stroke:#d6a240}
  .pill{fill:#203142;stroke:#4f6b85}
  .pill-bg{fill:#16222e;fill-opacity:.94;stroke:#4f6b85}
  .area1{fill:#6bc2f5;fill-opacity:.17}
  .area2{fill:#f28872;fill-opacity:.18}
  .area3{fill:#5dd1a8;fill-opacity:.18}
  .area4{fill:#f0ba5a;fill-opacity:.17}
  .bar-neutral{fill:#2a3c4e;stroke:#8fa9c2}
  .wall{fill:#8ca5bc;stroke:#cde0f2}
  .badge-txt{fill:#0f1720}
  .hm-pos1{fill:#2a7fb8;stroke:#16222e}
  .hm-pos2{fill:#3a92cc;stroke:#16222e}
  .hm-pos3{fill:#b87a24;stroke:#16222e}
  .hm-neg3{fill:#b84b3a;stroke:#16222e}
  .hm-zero{fill:#213243;stroke:#354c61}
  .hm-hi{stroke:#f0ba5a}
  .hm-inv{fill:#ffffff}
  .hm-dark{fill:#eef6ff}
  .hm-muted{fill:#8fa9c2}
  .hatch-stroke1{stroke:#6bc2f5;stroke-opacity:.48}
  .hatch-stroke2{stroke:#f28872;stroke-opacity:.50}
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
    hw = size * 0.46
    return f'<polygon class="{cls}" points="{pts_str([(x, y), (bx + px * hw, by + py * hw), (bx - px * hw, by - py * hw)])}"/>'


def mat_mul(a: list[list[complex]], b: list[list[complex]]) -> list[list[complex]]:
    n, m, p = len(a), len(b), len(b[0])
    assert len(a[0]) == m
    return [[sum(a[i][k] * b[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def mat_vec(a: list[list[complex]], v: list[complex]) -> list[complex]:
    return [sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a))]


def mat_dag(a: list[list[complex]]) -> list[list[complex]]:
    return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]


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
        self.add(f'<text class="title" x="34" y="52">{t_out}</text>')
        self.add(f'<text class="subtitle" x="34" y="76">{s_out}</text>')

    def add_panel(self, x: float, y: float, w: float, h: float, heading: str, *, raw_heading: bool = False) -> None:
        self.add(f'<rect class="panel" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="14"/>')
        self.add(
            f'<path class="phead" d="M {fmt(x + 14)} {fmt(y + 1)} H {fmt(x + w - 14)} '
            f'Q {fmt(x + w - 1)} {fmt(y + 1)} {fmt(x + w - 1)} {fmt(y + 14)} V {fmt(y + 36)} '
            f'H {fmt(x + 1)} V {fmt(y + 14)} Q {fmt(x + 1)} {fmt(y + 1)} {fmt(x + 14)} {fmt(y + 1)} Z"/>'
        )
        self.add(f'<line class="grid" x1="{fmt(x + 1)}" y1="{fmt(y + 36)}" x2="{fmt(x + w - 1)}" y2="{fmt(y + 36)}"/>')
        h_out = heading if raw_heading else escape(heading)
        self.add(f'<text class="sec" x="{fmt(x + 16)}" y="{fmt(y + 23)}">{h_out}</text>')

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
# Figure 1: Ch 00 — Classical probability vs complex amplitude interference & memory scaling
# ---------------------------------------------------------------------------
def build_fig1_amplitude_vs_memory() -> tuple[str, dict[str, float]]:
    # Exact Hadamard interference check: H|+> = |0>
    inv_s2 = 1.0 / math.sqrt(2.0)
    h_mat: list[list[complex]] = [[inv_s2, inv_s2], [inv_s2, -inv_s2]]
    plus = [inv_s2 + 0j, inv_s2 + 0j]
    out_plus = mat_vec(h_mat, plus)
    assert abs(out_plus[0] - 1.0) < TOL and abs(out_plus[1]) < TOL
    p_construct = abs(0.5 + 0.5) ** 2
    p_destruct = abs(0.5 - 0.5) ** 2
    assert abs(p_construct - 1.0) < TOL and abs(p_destruct) < TOL

    # Exact dense memory scaling (16 bytes per complex128)
    m_ket = lambda n: 16.0 * (2.0 ** n)
    m_rho = lambda n: 16.0 * (4.0 ** n)
    assert abs(m_ket(30) - 16.0 * (1024 ** 3)) < 1e-3  # exact 16 GiB
    n_10pb = math.log2(1e16 / 16.0)
    assert 49.0 < n_10pb < 49.3

    doc = SvgDoc(
        title="复振幅干涉叠加与经典态矢量内存指数标度",
        desc=(
            "左面板对照经典非负概率相加（1/2 + 1/2 = 1，恒增不消）与 H|+⟩ 门中两条路径复振幅的同向相长"
            "（|1/2 + 1/2|² = 1）和反向相消（|1/2 − 1/2|² = 0）；右面板在对数纵轴上绘出 n = 10 至 50 时"
            "稠密态矢量内存 M_ket = 16·2^n B 与稠密密度矩阵内存 M_ρ = 16·4^n B，并标出笔记本 16 GiB (n=30) "
            "与超算 10 PB (10¹⁶ B，n=49 对应 8 PiB ≈ 9.0 PB) 两条容量红线。"
        ),
    )
    doc.add_header(
        "复振幅干涉叠加与经典态矢量内存指数标度",
        "左：经典非负概率恒增不消 vs 量子复振幅同向相长、反向抵消；右：稠密态矢量与密度矩阵随比特数 n 对数飙升",
    )
    doc.add_panel(28, 94, 452, 458, "复振幅干涉：相长增强 vs 反向抵消")
    doc.add_panel(496, 94, 476, 458, "经典稠密模拟内存（16 字节/双精度复数）")

    # --- Left Panel: 3 stacked comparison cards ---
    # Card 1: Classical probability addition
    doc.add('<rect class="c4-soft" x="42" y="144" width="424" height="108" rx="11"/>')
    doc.add('<rect class="c4-fill" x="54" y="155" width="70" height="21" rx="10"/>')
    doc.add('<text class="badge-txt" x="89" y="169" text-anchor="middle">经典概率</text>')
    doc.add(f'<text class="lblb c4-txt" x="134" y="170">非负相加：p{sub("1")} + p{sub("2")} = 1/2 + 1/2 = 1</text>')
    # Bars showing 0.5 + 0.5 = 1.0
    doc.add('<rect class="c4-fill" fill-opacity="0.72" x="58" y="191" width="84" height="22" rx="4"/>')
    doc.add('<text class="badge-txt" x="100" y="206" text-anchor="middle">1/2</text>')
    doc.add('<text class="lblb" x="154" y="207" text-anchor="middle">+</text>')
    doc.add('<rect class="c4-fill" fill-opacity="0.72" x="166" y="191" width="84" height="22" rx="4"/>')
    doc.add('<text class="badge-txt" x="208" y="206" text-anchor="middle">1/2</text>')
    doc.add('<text class="lblb" x="263" y="207" text-anchor="middle">=</text>')
    doc.add('<rect class="c4-fill" x="278" y="191" width="168" height="22" rx="4"/>')
    doc.add('<text class="badge-txt" x="362" y="206" text-anchor="middle">P = 1（恒增不消）</text>')
    doc.add('<text class="sm" x="58" y="238">经典概率恒满足 p ≥ 0，多条互斥路径只能越加越大</text>')

    # Card 2: Constructive interference (H|+> -> |0>)
    doc.add('<rect class="c1-soft" x="42" y="264" width="424" height="110" rx="11"/>')
    doc.add('<rect class="c1-fill" x="54" y="275" width="70" height="21" rx="10"/>')
    doc.add('<text class="badge-txt" x="89" y="289" text-anchor="middle">相长干涉</text>')
    doc.add(f'<text class="lblb c1-txt" x="134" y="290">H|+⟩ → |0⟩：两路径同向相加 (Δφ = 0)</text>')
    # Feynman arrows: +1/2 + +1/2 = +1
    ay2 = 324.0
    doc.add(f'<line class="c1" stroke-width="3.0" x1="58" y1="{fmt(ay2)}" x2="112" y2="{fmt(ay2)}"/>')
    doc.add(arrow_head(116, ay2, 1, 0, 7.5, "c1-fill"))
    doc.add(f'<text class="xs c1-txt" x="86" y="313" text-anchor="middle">+1/2</text>')
    doc.add('<text class="lblb" x="130" y="329" text-anchor="middle">+</text>')
    doc.add(f'<line class="c1" stroke-width="3.0" x1="144" y1="{fmt(ay2)}" x2="198" y2="{fmt(ay2)}"/>')
    doc.add(arrow_head(202, ay2, 1, 0, 7.5, "c1-fill"))
    doc.add(f'<text class="xs c1-txt" x="172" y="313" text-anchor="middle">+1/2</text>')
    doc.add('<text class="lblb" x="216" y="329" text-anchor="middle">=</text>')
    doc.add(f'<line class="c1" stroke-width="3.4" x1="230" y1="{fmt(ay2)}" x2="322" y2="{fmt(ay2)}"/>')
    doc.add(arrow_head(328, ay2, 1, 0, 8.5, "c1-fill"))
    doc.add(f'<text class="xsb c1-txt" x="278" y="313" text-anchor="middle">合振幅 +1</text>')
    doc.add('<rect class="pill-bg" x="342" y="309" width="112" height="28" rx="8"/>')
    doc.add(f'<text class="smb c1-txt" x="398" y="327" text-anchor="middle">P(0) = |1|{sup("2")} = 1</text>')
    doc.add(f'<text class="sm" x="58" y="361">单步各含 1/√2 因子 ⇒ |1/2 + 1/2|{sup("2")} = 1（概率全部集中到 |0⟩）</text>')

    # Card 3: Destructive interference (H|+> -> |1>)
    doc.add('<rect class="c2-soft" x="42" y="386" width="424" height="110" rx="11"/>')
    doc.add('<rect class="c2-fill" x="54" y="397" width="70" height="21" rx="10"/>')
    doc.add('<text class="badge-txt" x="89" y="411" text-anchor="middle">相消干涉</text>')
    doc.add(f'<text class="lblb c2-txt" x="134" y="412">H|+⟩ → |1⟩：两路径反向抵消 (Δφ = π)</text>')
    ay3 = 446.0
    doc.add(f'<line class="c1" stroke-width="3.0" x1="58" y1="{fmt(ay3)}" x2="112" y2="{fmt(ay3)}"/>')
    doc.add(arrow_head(116, ay3, 1, 0, 7.5, "c1-fill"))
    doc.add('<text class="xs c1-txt" x="86" y="435" text-anchor="middle">+1/2</text>')
    doc.add('<text class="lblb" x="130" y="451" text-anchor="middle">+</text>')
    doc.add(f'<line class="c2" stroke-width="3.0" stroke-dasharray="6 3" x1="202" y1="{fmt(ay3)}" x2="148" y2="{fmt(ay3)}"/>')
    doc.add(arrow_head(144, ay3, -1, 0, 7.5, "c2-fill"))
    doc.add('<text class="xs c2-txt" x="174" y="435" text-anchor="middle">−1/2</text>')
    doc.add('<text class="lblb" x="216" y="451" text-anchor="middle">=</text>')
    doc.add(f'<circle class="c2-fill" cx="278" cy="{fmt(ay3)}" r="5.5"/>')
    doc.add('<text class="xsb c2-txt" x="278" y="433" text-anchor="middle">合振幅 0</text>')
    doc.add('<rect class="pill-bg" x="342" y="431" width="112" height="28" rx="8"/>')
    doc.add(f'<text class="smb c2-txt" x="398" y="449" text-anchor="middle">P(1) = |0|{sup("2")} = 0</text>')
    doc.add(f'<text class="sm" x="58" y="483">反向复振幅精确抵消 ⇒ |1/2 − 1/2|{sup("2")} = 0（量子加速根基）</text>')

    # Bottom banner inside left panel
    doc.add('<rect class="note" x="42" y="508" width="424" height="32" rx="8"/>')
    doc.add(f'<text class="xs" x="254" y="528" text-anchor="middle">合并公式：| (1/√2)·(1/√2 ± 1/√2) |{sup("2")} = |1/2 ± 1/2|{sup("2")} ∈ {{0, 1}}</text>')

    # --- Right Panel: Log-scale memory plot (n = 10..50, y = 10^4..10^20 B) ---
    px0, px1 = 574.0, 948.0
    py0, py1 = 456.0, 158.0
    n_min, n_max = 10.0, 50.0
    ly_min, ly_max = 4.0, 20.0

    def map_n(n_val: float) -> float:
        return px0 + (n_val - n_min) / (n_max - n_min) * (px1 - px0)

    def map_ly(log10_bytes: float) -> float:
        return py0 - (log10_bytes - ly_min) / (ly_max - ly_min) * (py0 - py1)

    # Grid lines & ticks
    for ly_t, unit_lbl in [(4, "4"), (8, "8"), (12, "12"), (16, "16"), (20, "20")]:
        yt = map_ly(float(ly_t))
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(yt)}" x2="{fmt(px1)}" y2="{fmt(yt)}"/>')
        doc.add(f'<text class="sm" x="{fmt(px0 - 8)}" y="{fmt(yt + 4)}" text-anchor="end">10{sup(unit_lbl)}</text>')
    for n_t in [10, 20, 30, 40, 50]:
        xt = map_n(float(n_t))
        doc.add(f'<line class="grid" x1="{fmt(xt)}" y1="{fmt(py1)}" x2="{fmt(xt)}" y2="{fmt(py0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xt)}" y="{fmt(py0 + 17)}" text-anchor="middle">{n_t}</text>')

    # Axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px1 + 8)}" y2="{fmt(py0)}"/>')
    doc.add(arrow_head(px1 + 8, py0, 1, 0, 7.0))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px0)}" y2="{fmt(py1 - 10)}"/>')
    doc.add(arrow_head(px0, py1 - 10, 0, -1, 7.0))
    doc.add(f'<text class="sm" x="{fmt(0.5 * (px0 + px1))}" y="494" text-anchor="middle">量子比特数 n (个)</text>')
    doc.add(
        f'<text class="sm" x="518" y="{fmt(0.5 * (py0 + py1))}" text-anchor="middle" '
        f'transform="rotate(-90 518 {fmt(0.5 * (py0 + py1))})">经典稠密存储内存 (字节 B, 对数刻度)</text>'
    )

    # Horizontal memory thresholds: Laptop 16 GiB (n=30) & Supercomputer 10 PB (n~49)
    ly_laptop = math.log10(m_ket(30))  # 10.235
    y_laptop = map_ly(ly_laptop)
    doc.add(f'<line class="c3" stroke-width="1.6" stroke-dasharray="6 4" x1="{fmt(px0)}" y1="{fmt(y_laptop)}" x2="{fmt(px1)}" y2="{fmt(y_laptop)}"/>')

    ly_super = 16.0  # 10 PB = 10^16 B
    y_super = map_ly(ly_super)
    doc.add(f'<line class="c4" stroke-width="1.6" stroke-dasharray="6 4" x1="{fmt(px0)}" y1="{fmt(y_super)}" x2="{fmt(px1)}" y2="{fmt(y_super)}"/>')

    # Exact curves: M_ket (n=10..50) and M_rho (n=10..31.22 where log10=20)
    ket_pts = [(map_n(float(n)), map_ly(math.log10(m_ket(n)))) for n in range(10, 51)]
    n_rho_end = (ly_max - math.log10(16.0)) / math.log10(4.0)
    rho_pts = [(map_n(10.0 + (n_rho_end - 10.0) * i / 40.0), map_ly(math.log10(m_rho(10.0 + (n_rho_end - 10.0) * i / 40.0)))) for i in range(41)]

    doc.add(f'<path class="c1" stroke-width="2.8" d="{path_from_points(ket_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.5" stroke-dasharray="8 4" d="{path_from_points(rho_pts)}"/>')

    # Key markers on M_ket and M_rho
    for n_m in [10, 20, 30, 40, 49]:
        doc.add(f'<circle class="c1-fill" cx="{fmt(map_n(n_m))}" cy="{fmt(map_ly(math.log10(m_ket(n_m))))}" r="4.5"/>')
    for n_m in [10, 15, 20, 25, 30]:
        doc.add(f'<polygon class="c2-fill" points="{diamond_pts(map_n(n_m), map_ly(math.log10(m_rho(n_m))), 4.8)}"/>')

    # Vertical guide drops for n=30 and n=49
    x30, y30 = map_n(30.0), map_ly(math.log10(m_ket(30)))
    x49, y49 = map_n(49.0), map_ly(math.log10(m_ket(49)))
    doc.add(f'<line class="guide" x1="{fmt(x30)}" y1="{fmt(y30 + 5)}" x2="{fmt(x30)}" y2="{fmt(py0)}"/>')
    doc.add(f'<line class="guide" x1="{fmt(x49)}" y1="{fmt(y49 + 5)}" x2="{fmt(x49)}" y2="{fmt(py0)}"/>')

    # Callout badges placed in open regions (zero curve overlap)
    # Legend in upper-left open box (n=10..24, y=162..222)
    doc.add('<rect class="pill-bg" x="582" y="156" width="150" height="58" rx="8"/>')
    doc.add('<line class="c1" stroke-width="2.6" x1="592" y1="175" x2="616" y2="175"/>')
    doc.add('<circle class="c1-fill" cx="604" cy="175" r="3.5"/>')
    doc.add(f'<text class="xs c1-txt" x="622" y="179">态矢量 16·2{sup("n")} B</text>')
    doc.add('<line class="c2" stroke-width="2.4" stroke-dasharray="6 3" x1="592" y1="199" x2="616" y2="199"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(604, 199, 4.0)}"/>')
    doc.add(f'<text class="xs c2-txt" x="622" y="203">密度矩阵 16·4{sup("n")} B</text>')

    # Supercomputer 10 PB badge (upper-right open space below line, x=760..940)
    doc.add('<rect class="c4-soft" x="760" y="182" width="180" height="36" rx="7"/>')
    doc.add('<text class="xsb c4-txt" x="850" y="197" text-anchor="middle">超算红线 10 PB (10¹⁶ B)</text>')
    doc.add('<text class="xs c4-txt" x="850" y="212" text-anchor="middle">n = 49 (8 PiB ≈ 9.0 PB)</text>')
    doc.add(f'<line class="c4" stroke-width="1.3" x1="934" y1="218" x2="{fmt(x49 - 2)}" y2="{fmt(y49 - 4)}"/>')

    # Laptop 16 GiB badge (lower-right open space below y_laptop)
    doc.add('<rect class="c3-soft" x="772" y="352" width="168" height="36" rx="7"/>')
    doc.add('<text class="xsb c3-txt" x="856" y="367" text-anchor="middle">笔记本红线 16 GiB</text>')
    doc.add('<text class="xs c3-txt" x="856" y="382" text-anchor="middle">态矢量 n = 30 · 密度阵 n = 15</text>')
    doc.add(f'<line class="c3" stroke-width="1.3" x1="772" y1="364" x2="{fmt(x30 + 5)}" y2="{fmt(y30 + 3)}"/>')

    # Density matrix slope note at n=26
    doc.add('<rect class="pill-bg" x="614" y="246" width="112" height="24" rx="6"/>')
    doc.add('<text class="xs c2-txt" x="670" y="262" text-anchor="middle">斜率翻倍 (4×/比特)</text>')

    # Bottom caution note inside right panel
    doc.add('<rect class="note" x="510" y="508" width="448" height="32" rx="8"/>')
    doc.add('<text class="xs" x="734" y="528" text-anchor="middle">注：纯 Clifford 与低纠缠线路可用稳定子或张量网络高效模拟，无需稠密数组</text>')

    return doc.render(), {"m_ket_30_GiB": m_ket(30) / (1024 ** 3), "n_at_10PB": round(n_10pb, 3)}


# ---------------------------------------------------------------------------
# Figure 2: Ch 01 — SVD geometric ellipse (A = W Sigma V^dag) & readout kappa_2
# ---------------------------------------------------------------------------
def build_fig2_svd_condition_ellipse() -> tuple[str, dict[str, float]]:
    # Exact SVD of shear matrix A = [[1, 1], [0, 1]]
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    s1 = phi
    s2 = 1.0 / phi
    norm_v = math.sqrt(1.0 + phi * phi)
    v1 = (1.0 / norm_v, phi / norm_v)
    v2 = (-phi / norm_v, 1.0 / norm_v)
    w1 = (phi / norm_v, 1.0 / norm_v)
    w2 = (-1.0 / norm_v, phi / norm_v)

    # Verify A = s1 |w1><v1| + s2 |w2><v2| and orthonormality
    a_mat = [[1.0, 1.0], [0.0, 1.0]]
    for i in range(2):
        for j in range(2):
            rec = s1 * w1[i] * v1[j] + s2 * w2[i] * v2[j]
            assert abs(rec - a_mat[i][j]) < TOL
    assert abs(v1[0] * v2[0] + v1[1] * v2[1]) < TOL
    assert abs(w1[0] * w2[0] + w1[1] * w2[1]) < TOL
    kappa_shear = s1 / s2
    assert abs(kappa_shear - phi * phi) < TOL

    # Symmetric readout matrices A(e) = [[1-e, e], [e, 1-e]]
    e_good, e_bad = 0.05, 0.45
    kappa_good = 1.0 / abs(1.0 - 2.0 * e_good)
    kappa_bad = 1.0 / abs(1.0 - 2.0 * e_bad)
    assert abs(kappa_good - 1.0 / 0.9) < TOL
    assert abs(kappa_bad - 10.0) < TOL

    doc = SvgDoc(
        title="奇异值分解几何椭圆与读出条件数噪声放大",
        desc=(
            "左面板在等比例平面绘制单位圆经实剪切矩阵 A = [[1,1],[0,1]] = WΣV† 的变换：先按右奇异基 V† 对齐，"
            "再沿主轴按黄金分割奇异值 σ₁ = φ ≈ 1.618 与 σ₂ = φ⁻¹ ≈ 0.618 拉伸压扁，最后经 W 旋成倾斜椭圆（κ₂ ≈ 2.618）。"
            "右面板对比对称读出矩阵 A(0.05)（κ₂ ≈ 1.11）与糟糕读出 A(0.45)（κ₂ = 10）的压缩椭圆，展示 1% 观测扰动 δq 反演放大倍数。"
        ),
    )
    doc.add_header(
        "奇异值分解（SVD）几何椭圆与条件数噪声放大",
        f'左：A = WΣV† 把单位圆经旋转—拉伸—再旋转映为倾斜椭圆；右：条件数 κ{sub("2")} = σ{sub("max")}/σ{sub("min")} 决定反演对观测扰动 δq 的放大倍率',
        raw_sub=True,
    )
    doc.add_panel(28, 94, 472, 458, "剪切阵 A = [[1,1],[0,1]] 的 SVD 几何分解（等比例）")
    doc.add_panel(516, 94, 456, 458, "条件数 κ₂ 对照：读出矩阵压缩椭圆与扰动放大")

    # --- Left Panel: Equal-aspect SVD geometry ---
    ox, oy = 258.0, 294.0
    sc = 74.0  # 1 unit = 74 px

    def lx(x: float) -> float:
        return ox + x * sc

    def ly(y: float) -> float:
        return oy - y * sc

    # Subtle grid
    for g in [-2, -1, 1, 2]:
        if abs(g) <= 2:
            xg = lx(float(g))
            if 48 <= xg <= 478:
                doc.add(f'<line class="grid" x1="{fmt(xg)}" y1="154" x2="{fmt(xg)}" y2="432"/>')
        if abs(g) <= 1:
            yg = ly(float(g))
            doc.add(f'<line class="grid" x1="56" y1="{fmt(yg)}" x2="474" y2="{fmt(yg)}"/>')

    # Axes
    doc.add(f'<line class="axis" x1="56" y1="{fmt(oy)}" x2="474" y2="{fmt(oy)}"/>')
    doc.add(arrow_head(474, oy, 1, 0, 7.0))
    doc.add(f'<line class="axis" x1="{fmt(ox)}" y1="432" x2="{fmt(ox)}" y2="152"/>')
    doc.add(arrow_head(ox, 152, 0, -1, 7.0))
    doc.add(f'<text class="xs" x="472" y="{fmt(oy + 16)}" text-anchor="end">x₁ (无量纲)</text>')
    doc.add(f'<text class="xs" x="{fmt(ox + 8)}" y="160">x₂ (无量纲)</text>')

    # Unit circle & A(unit circle) ellipse
    n_el = 144
    ell_pts = []
    for i in range(n_el + 1):
        t = 2.0 * math.pi * i / n_el
        cx_u, cy_u = math.cos(t), math.sin(t)
        ax, ay = cx_u + cy_u, cy_u
        ell_pts.append((lx(ax), ly(ay)))
    doc.add(f'<path class="area1" d="{path_from_points(ell_pts)} Z"/>')
    doc.add(f'<circle class="unit-circle" cx="{fmt(ox)}" cy="{fmt(oy)}" r="{fmt(sc)}"/>')
    doc.add(f'<path class="c1" stroke-width="2.6" d="{path_from_points(ell_pts)} Z"/>')

    # Right singular vectors |v1>, |v2> on unit circle (dashed green)
    for vec, lbl_v, tx, ty, anc in [
        (v1, f"|v{sub('1')}⟩", lx(v1[0]) - 2, ly(v1[1]) - 15, "end"),
        (v2, f"|v{sub('2')}⟩", lx(v2[0]) - 8, ly(v2[1]) - 8, "end"),
    ]:
        px, py = lx(vec[0]), ly(vec[1])
        doc.add(f'<line class="c3" stroke-width="1.9" stroke-dasharray="5 3" x1="{fmt(ox)}" y1="{fmt(oy)}" x2="{fmt(px)}" y2="{fmt(py)}"/>')
        doc.add(arrow_head(px, py, px - ox, py - oy, 6.5, "c3-fill"))
        doc.add(f'<text class="xsb c3-txt" x="{fmt(tx)}" y="{fmt(ty)}" text-anchor="{anc}">{lbl_v}</text>')

    # Left singular scaled semi-axes s1|w1> (blue) and s2|w2> (red)
    pw1 = (lx(s1 * w1[0]), ly(s1 * w1[1]))
    pw2 = (lx(s2 * w2[0]), ly(s2 * w2[1]))
    doc.add(f'<line class="c1" stroke-width="3.0" x1="{fmt(ox)}" y1="{fmt(oy)}" x2="{fmt(pw1[0])}" y2="{fmt(pw1[1])}"/>')
    doc.add(arrow_head(pw1[0], pw1[1], pw1[0] - ox, pw1[1] - oy, 8.0, "c1-fill"))
    doc.add(f'<line class="c2" stroke-width="2.8" x1="{fmt(ox)}" y1="{fmt(oy)}" x2="{fmt(pw2[0])}" y2="{fmt(pw2[1])}"/>')
    doc.add(arrow_head(pw2[0], pw2[1], pw2[0] - ox, pw2[1] - oy, 7.5, "c2-fill"))

    # Clean callout labels outside ellipse
    doc.add('<rect class="pill-bg" x="348" y="164" width="136" height="44" rx="7"/>')
    doc.add(f'<text class="xsb c1-txt" x="416" y="180" text-anchor="middle">长半轴 σ{sub("1")}|w{sub("1")}⟩</text>')
    doc.add(f'<text class="xs c1-txt" x="416" y="200" text-anchor="middle">σ{sub("1")} = φ ≈ 1.618</text>')
    doc.add(f'<line class="guide" x1="382" y1="208" x2="{fmt(pw1[0] - 4)}" y2="{fmt(pw1[1] - 4)}"/>')

    doc.add('<rect class="pill-bg" x="46" y="164" width="136" height="44" rx="7"/>')
    doc.add(f'<text class="xsb c2-txt" x="114" y="180" text-anchor="middle">短半轴 σ{sub("2")}|w{sub("2")}⟩</text>')
    doc.add(f'<text class="xs c2-txt" x="114" y="200" text-anchor="middle">σ{sub("2")} = φ{sup("−1")} ≈ 0.618</text>')
    doc.add(f'<line class="guide" x1="162" y1="208" x2="{fmt(pw2[0] - 3)}" y2="{fmt(pw2[1] - 2)}"/>')

    doc.add('<text class="xs" x="150" y="388" text-anchor="end">单位圆 ‖v‖ = 1</text>')
    doc.add('<text class="xs c1-txt" x="372" y="392">像椭圆 A·S¹</text>')

    # 3-step SVD pipeline banner at bottom of left panel
    doc.add('<rect class="subpanel" x="42" y="446" width="444" height="48" rx="9"/>')
    steps = [
        (52, 92, "① V† 旋转", "对齐奇异基", "c3-soft", "c3-txt"),
        (170, 146, "② Σ 拉伸压扁", "σ₁≈1.618, σ₂≈0.618", "c1-soft", "c1-txt"),
        (342, 134, "③ W 旋转输出", "映成倾斜椭圆", "c2-soft", "c2-txt"),
    ]
    for sx_b, sw_b, s_t1, s_t2, cls_b, cls_t in steps:
        doc.add(f'<rect class="{cls_b}" x="{sx_b}" y="453" width="{sw_b}" height="34" rx="6"/>')
        doc.add(f'<text class="xsb {cls_t}" x="{fmt(sx_b + sw_b / 2)}" y="467" text-anchor="middle">{s_t1}</text>')
        doc.add(f'<text class="xs" x="{fmt(sx_b + sw_b / 2)}" y="481" text-anchor="middle">{s_t2}</text>')
    doc.add('<line class="axis" stroke-width="1.5" x1="146" y1="470" x2="167" y2="470"/>')
    doc.add(arrow_head(168, 470, 1, 0, 5.5))
    doc.add('<line class="axis" stroke-width="1.5" x1="318" y1="470" x2="339" y2="470"/>')
    doc.add(arrow_head(340, 470, 1, 0, 5.5))

    doc.add('<rect class="note" x="42" y="504" width="444" height="34" rx="8"/>')
    doc.add(f'<text class="xs" x="264" y="525" text-anchor="middle">剪切阵条件数 κ{sub("2")}(A) = σ{sub("1")}/σ{sub("2")} = φ{sup("2")} ≈ 2.618（矩阵非正规，但 SVD 始终存在）</text>')

    # --- Right Panel Top: Readout ellipse contrast A(0.05) vs A(0.45) ---
    rox, roy = 744.0, 266.0
    rsc = 90.0

    def rx(x: float) -> float:
        return rox + x * rsc

    def ry(y: float) -> float:
        return roy - y * rsc

    doc.add(f'<line class="axis" stroke-width="1.4" x1="628" y1="{fmt(roy)}" x2="862" y2="{fmt(roy)}"/>')
    doc.add(arrow_head(862, roy, 1, 0, 6.5))
    doc.add(f'<line class="axis" stroke-width="1.4" x1="{fmt(rox)}" y1="376" x2="{fmt(rox)}" y2="154"/>')
    doc.add(arrow_head(rox, 154, 0, -1, 6.5))
    doc.add(f'<text class="xs" x="862" y="{fmt(roy + 15)}" text-anchor="end">q{sub("0")}</text>')
    doc.add(f'<text class="xs" x="{fmt(rox + 8)}" y="160">q{sub("1")}</text>')

    def sym_ellipse(err: float) -> list[tuple[float, float]]:
        pts = []
        for i in range(121):
            t = 2.0 * math.pi * i / 120.0
            p0, p1 = math.cos(t), math.sin(t)
            q0 = (1.0 - err) * p0 + err * p1
            q1 = err * p0 + (1.0 - err) * p1
            pts.append((rx(q0), ry(q1)))
        return pts

    good_pts = sym_ellipse(e_good)
    bad_pts = sym_ellipse(e_bad)

    doc.add(f'<circle class="unit-circle" cx="{fmt(rox)}" cy="{fmt(roy)}" r="{fmt(rsc)}"/>')
    doc.add(f'<path class="area3" d="{path_from_points(good_pts)} Z"/>')
    doc.add(f'<path class="c3" stroke-width="2.3" d="{path_from_points(good_pts)} Z"/>')
    doc.add(f'<path class="area2" d="{path_from_points(bad_pts)} Z"/>')
    doc.add(f'<path class="c2" stroke-width="2.6" stroke-dasharray="7 3" d="{path_from_points(bad_pts)} Z"/>')

    # Weak singular direction [1, -1]/sqrt(2): perturbation delta_b vs inverse A^-1 delta_b
    inv_s2 = 1.0 / math.sqrt(2.0)
    # On bad ellipse boundary along [1, -1]/sqrt(2), length = 0.10; inverse pulls it to 1.00!
    db_end = (rx(0.10 * inv_s2), ry(-0.10 * inv_s2))
    dx_end = (rx(1.00 * inv_s2), ry(-1.00 * inv_s2))
    doc.add(f'<line class="c2" stroke-width="2.6" x1="{fmt(rox)}" y1="{fmt(roy)}" x2="{fmt(dx_end[0])}" y2="{fmt(dx_end[1])}"/>')
    doc.add(arrow_head(dx_end[0], dx_end[1], dx_end[0] - rox, dx_end[1] - roy, 7.5, "c2-fill"))
    doc.add(f'<circle class="c4-fill" cx="{fmt(db_end[0])}" cy="{fmt(db_end[1])}" r="4.0"/>')

    # Labels around right ellipse
    doc.add('<rect class="pill-bg" x="528" y="152" width="126" height="40" rx="7"/>')
    doc.add('<text class="xsb c3-txt" x="591" y="168" text-anchor="middle">优质读出 A(0.05)</text>')
    doc.add(f'<text class="xs c3-txt" x="591" y="184" text-anchor="middle">σ{sub("2")} = 0.90 · κ{sub("2")} ≈ 1.11</text>')

    doc.add('<rect class="pill-bg" x="832" y="152" width="128" height="40" rx="7"/>')
    doc.add('<text class="xsb c2-txt" x="896" y="168" text-anchor="middle">糟糕读出 A(0.45)</text>')
    doc.add(f'<text class="xs c2-txt" x="896" y="184" text-anchor="middle">σ{sub("2")} = 0.10 · κ{sub("2")} = 10</text>')

    doc.add('<rect class="pill-bg" x="816" y="330" width="144" height="38" rx="7"/>')
    doc.add('<text class="xsb c2-txt" x="888" y="346" text-anchor="middle">短轴扰动 δq → A⁻¹δq</text>')
    doc.add('<text class="xs" x="888" y="361" text-anchor="middle">微小抖动被拉长 10×</text>')

    # --- Right Panel Bottom: Condition number perturbation bar chart ---
    doc.add('<rect class="subpanel" x="530" y="388" width="428" height="150" rx="10"/>')
    doc.add(f'<text class="smb" x="544" y="408">1% 观测扰动 δq 经 A{sup("−1")} 反演后的最坏相对误差上界</text>')
    bars = [
        ("酉门 U (κ₂ = 1.00)", 1.0, "1.0%", "c1-fill", "c1-txt", False),
        ("优质 A(0.05) (κ₂ = 1.11)", 1.11, "1.1%", "c3-fill", "c3-txt", False),
        ("剪切阵 A (κ₂ = 2.62)", 2.62, "2.6%", "c4-fill", "c4-txt", False),
        ("糟糕 A(0.45) (κ₂ = 10.0)", 10.0, "10.0% (可致负概率)", "c2-fill", "c2-txt", True),
    ]
    bx0 = 696.0
    max_bw = 144.0
    for idx, (label_b, kval, val_lbl, fill_c, txt_c, warn) in enumerate(bars):
        by = 423.0 + idx * 28.0
        bw = max_bw * (kval / 10.0)
        doc.add(f'<text class="xs" x="{fmt(bx0 - 8)}" y="{fmt(by + 13)}" text-anchor="end">{label_b}</text>')
        doc.add(f'<rect class="{fill_c}" x="{fmt(bx0)}" y="{fmt(by)}" width="{fmt(bw)}" height="18" rx="4"/>')
        if warn:
            doc.add(f'<rect fill="url(#hatch-red)" x="{fmt(bx0)}" y="{fmt(by)}" width="{fmt(bw)}" height="18" rx="4" opacity="0.35"/>')
        doc.add(f'<text class="xsb {txt_c}" x="{fmt(bx0 + bw + 6)}" y="{fmt(by + 13)}">{val_lbl}</text>')

    return doc.render(), {"sigma1": round(s1, 4), "sigma2": round(s2, 4), "kappa_shear": round(kappa_shear, 4), "kappa_bad": kappa_bad}


# ---------------------------------------------------------------------------
# Figure 3: Q1 — 3-stage Stern-Gerlach Z -> X -> Z cascade vs pre-labeled model
# ---------------------------------------------------------------------------
def build_fig3_stern_gerlach_cascade() -> tuple[str, dict[str, float]]:
    # Exact quantum cascade state & conditional probabilities (N = 8000)
    n0 = 8000
    inv_s2 = 1.0 / math.sqrt(2.0)
    z_plus = [1.0 + 0j, 0.0 + 0j]
    z_minus = [0.0 + 0j, 1.0 + 0j]
    x_plus = [inv_s2 + 0j, inv_s2 + 0j]
    p_x_given_z = abs(sum(a.conjugate() * b for a, b in zip(x_plus, z_plus))) ** 2
    p_zp_given_xp = abs(sum(a.conjugate() * b for a, b in zip(z_plus, x_plus))) ** 2
    p_zm_given_xp = abs(sum(a.conjugate() * b for a, b in zip(z_minus, x_plus))) ** 2
    assert abs(p_x_given_z - 0.5) < TOL
    assert abs(p_zp_given_xp - 0.5) < TOL
    assert abs(p_zm_given_xp - 0.5) < TOL
    n1 = n0 * 0.5
    n2 = n1 * p_x_given_z
    n3_zp = n2 * p_zp_given_xp
    n3_zm = n2 * p_zm_given_xp
    assert abs(n3_zp - 1000.0) < TOL and abs(n3_zm - 1000.0) < TOL

    doc = SvgDoc(
        title="Stern–Gerlach 三级级联实验与经典预贴标签假说对照",
        desc=(
            "上栏展示 8000 个未偏振银原子依次通过竖直 SGz（挡住 z−，留 4000 个 |z+⟩）、水平 SGx（挡住 x−，留 2000 个 |x+⟩）"
            "与末级竖直 SGz 的完整原子束与挡板；下栏左图以柱图正面对比经典预贴标签假说预言（100% z+, 0% z−）与量子理论预言"
            "（50% z+, 50% z−，被剔除的 z− 复活）；下栏右图给出互补基原理与相干重聚对照。"
        ),
    )
    doc.add_header(
        "Stern–Gerlach 三级级联实验：Z → X → Z 与经典预贴标签对照",
        "上：中间插入横向 SGx 筛选会抹去先前的 z+ 记忆；下：经典预贴标签预言 100% : 0% 与量子理论预言 50% : 50% 正面冲突",
    )
    doc.add_panel(28, 94, 944, 232, "三组级联装置：SGz（竖直）→ SGx（横向）→ SGz（竖直）原子束与挡板")
    doc.add_panel(28, 338, 534, 214, "末级 SGz 输出占比对照（以进入第 3 级的 2000 原子为 100%）")
    doc.add_panel(578, 338, 394, 214, "互补基机制与无挡板相干重聚对照")

    # --- Top Panel: 3-stage SG cascade ---
    # Oven source
    doc.add('<rect class="pill" x="44" y="182" width="76" height="50" rx="8"/>')
    doc.add('<text class="smb" x="82" y="201" text-anchor="middle">银原子源</text>')
    doc.add('<text class="xs" x="82" y="216" text-anchor="middle">N = 8000</text>')
    doc.add('<text class="xs" x="82" y="229" text-anchor="middle">未偏振</text>')

    # Beam: Source -> SG1
    doc.add('<line class="axis" stroke-width="2.6" x1="120" y1="207" x2="170" y2="207"/>')
    doc.add(arrow_head(170, 207, 1, 0, 7.0))

    # Stage 1: SGz magnet
    doc.add('<rect class="c1-soft" x="172" y="172" width="84" height="70" rx="9"/>')
    doc.add(f'<text class="lblb c1-txt" x="214" y="198" text-anchor="middle">SG{sub("z")} ①</text>')
    doc.add('<text class="xs c1-txt" x="214" y="216" text-anchor="middle">竖直磁场</text>')
    doc.add(f'<text class="xs" x="214" y="232" text-anchor="middle">按 S{sub("z")} 分束</text>')

    # Beams out of SG1: z+ (upper passes to SG2 at y=184), z- (lower blocked at y=242)
    doc.add('<path class="c1" stroke-width="2.8" d="M 256 196 L 296 184 L 424 184"/>')
    doc.add(arrow_head(424, 184, 1, 0, 7.5, "c1-fill"))
    doc.add('<text class="smb c1-txt" x="342" y="175" text-anchor="middle">|z+⟩：4000 (N/2)</text>')

    doc.add('<path class="guide" stroke-width="2.0" d="M 256 218 L 296 244 L 320 244"/>')
    doc.add('<rect class="wall" x="320" y="230" width="11" height="28" rx="2"/>')
    doc.add('<text class="xs" x="338" y="248">挡板阻断 z− (4000)</text>')

    # Stage 2: SGx magnet
    doc.add('<rect class="c4-soft" x="426" y="149" width="88" height="70" rx="9"/>')
    doc.add(f'<text class="lblb c4-txt" x="470" y="175" text-anchor="middle">SG{sub("x")} ②</text>')
    doc.add('<text class="xs c4-txt" x="470" y="193" text-anchor="middle">横向旋转 90°</text>')
    doc.add(f'<text class="xs" x="470" y="209" text-anchor="middle">按 S{sub("x")} 分束</text>')

    # Beams out of SG2: x+ (upper passes to SG3 at y=164), x- (lower blocked at y=218)
    doc.add('<path class="c4" stroke-width="2.8" d="M 514 174 L 552 164 L 678 164"/>')
    doc.add(arrow_head(678, 164, 1, 0, 7.5, "c4-fill"))
    doc.add('<text class="smb c4-txt" x="596" y="155" text-anchor="middle">|x+⟩：2000 (N/4)</text>')

    doc.add('<path class="guide" stroke-width="2.0" d="M 514 196 L 552 220 L 576 220"/>')
    doc.add('<rect class="wall" x="576" y="206" width="11" height="28" rx="2"/>')
    doc.add('<text class="xs" x="594" y="224">挡板阻断 x− (2000)</text>')

    # Stage 3: SGz magnet
    doc.add('<rect class="c1-soft" x="680" y="139" width="84" height="70" rx="9"/>')
    doc.add(f'<text class="lblb c1-txt" x="722" y="165" text-anchor="middle">SG{sub("z")} ③</text>')
    doc.add('<text class="xs c1-txt" x="722" y="183" text-anchor="middle">竖直复测</text>')
    doc.add('<text class="xs" x="722" y="199" text-anchor="middle">检验 z 成分</text>')

    # Output beams out of SG3 -> Detectors
    doc.add('<path class="c1" stroke-width="2.6" d="M 764 162 L 802 152 L 832 152"/>')
    doc.add(arrow_head(832, 152, 1, 0, 7.0, "c1-fill"))
    doc.add('<rect class="c1-soft" x="836" y="137" width="122" height="30" rx="7"/>')
    doc.add('<text class="xsb c1-txt" x="897" y="156" text-anchor="middle">z+：1000 (50%)</text>')

    doc.add('<path class="c2" stroke-width="2.8" stroke-dasharray="7 3" d="M 764 186 L 802 204 L 832 204"/>')
    doc.add(arrow_head(832, 204, 1, 0, 7.5, "c2-fill"))
    doc.add('<rect class="c2-soft" x="836" y="189" width="122" height="30" rx="7"/>')
    doc.add('<text class="xsb c2-txt" x="897" y="208" text-anchor="middle">z−：1000 (50% 复活)</text>')

    # Bottom chain banner inside top panel
    doc.add('<rect class="note" x="44" y="278" width="912" height="34" rx="8"/>')
    doc.add(
        '<text class="sm" x="500" y="299" text-anchor="middle">'
        '条件概率链：8000 未偏振 ─(×1/2)→ 4000 |z+⟩ ─(×1/2)→ 2000 |x+⟩ ─(×1/2)→ 1000 |z+⟩ + 1000 |z−⟩（相对总束各 N/8）'
        '</text>'
    )

    # --- Bottom-Left Panel: Classical vs Quantum Bar Chart ---
    bx0, bx1 = 104.0, 536.0
    by0, by1 = 508.0, 396.0  # 0% bottom, 100% top

    def map_pct(pct: float) -> float:
        return by0 - (pct / 100.0) * (by0 - by1)

    for pct in [0, 50, 100]:
        yp = map_pct(float(pct))
        doc.add(f'<line class="grid" x1="{fmt(bx0)}" y1="{fmt(yp)}" x2="{fmt(bx1)}" y2="{fmt(yp)}"/>')
        doc.add(f'<text class="sm" x="{fmt(bx0 - 8)}" y="{fmt(yp + 4)}" text-anchor="end">{pct}%</text>')
    doc.add(f'<line class="axis" x1="{fmt(bx0)}" y1="{fmt(by0)}" x2="{fmt(bx1)}" y2="{fmt(by0)}"/>')
    doc.add(f'<line class="axis" x1="{fmt(bx0)}" y1="{fmt(by0)}" x2="{fmt(bx0)}" y2="{fmt(by1 - 8)}"/>')
    doc.add(arrow_head(bx0, by1 - 8, 0, -1, 6.5))
    doc.add(
        f'<text class="sm" x="50" y="{fmt(0.5 * (by0 + by1))}" text-anchor="middle" '
        f'transform="rotate(-90 50 {fmt(0.5 * (by0 + by1))})">末级条件占比 (%)</text>'
    )

    # Grouped bars: z+ at center 216, z- at center 418
    bw = 54.0
    # z+ Classical 100%
    h_100 = by0 - map_pct(100.0)
    h_50 = by0 - map_pct(50.0)
    doc.add(f'<rect class="c2-soft" x="156" y="{fmt(map_pct(100.0))}" width="{fmt(bw)}" height="{fmt(h_100)}" rx="5"/>')
    doc.add(f'<rect fill="url(#hatch-red)" x="156" y="{fmt(map_pct(100.0))}" width="{fmt(bw)}" height="{fmt(h_100)}" rx="5" opacity="0.38"/>')
    doc.add('<text class="xsb c2-txt" x="183" y="391" text-anchor="middle">100% (2000)</text>')

    # z+ Quantum 50%
    doc.add(f'<rect class="c1-fill" x="222" y="{fmt(map_pct(50.0))}" width="{fmt(bw)}" height="{fmt(h_50)}" rx="5"/>')
    doc.add('<text class="xsb c1-txt" x="249" y="444" text-anchor="middle">50% (1000)</text>')
    doc.add('<text class="smb" x="216" y="530" text-anchor="middle">末级 z+ 端口</text>')

    # z- Classical 0%
    doc.add(f'<line class="c2" stroke-width="3.2" x1="358" y1="{fmt(by0 - 1)}" x2="412" y2="{fmt(by0 - 1)}"/>')
    doc.add('<text class="xsb c2-txt" x="385" y="497" text-anchor="middle">0% (0)</text>')

    # z- Quantum 50%
    doc.add(f'<rect class="c1-fill" x="424" y="{fmt(map_pct(50.0))}" width="{fmt(bw)}" height="{fmt(h_50)}" rx="5"/>')
    doc.add('<text class="xsb c1-txt" x="451" y="444" text-anchor="middle">50% (1000)</text>')
    doc.add('<text class="smb" x="418" y="530" text-anchor="middle">末级 z− 端口</text>')

    # Compact legend in top-right open zone of bar chart
    doc.add('<rect class="pill-bg" x="344" y="382" width="198" height="44" rx="7"/>')
    doc.add('<rect class="c2-soft" x="354" y="390" width="14" height="10" rx="2"/>')
    doc.add('<text class="xs c2-txt" x="374" y="399">经典预贴标签 (100% / 0%)</text>')
    doc.add('<rect class="c1-fill" x="354" y="408" width="14" height="10" rx="2"/>')
    doc.add('<text class="xs c1-txt" x="374" y="417">量子理论预言 (50% / 50%)</text>')

    # --- Bottom-Right Panel: Explanation cards ---
    doc.add('<rect class="c1-soft" x="594" y="388" width="362" height="72" rx="9"/>')
    doc.add('<text class="smb c1-txt" x="608" y="408">1. 互补基拆散了旧记忆</text>')
    doc.add(f'<text class="xs" x="608" y="427">|x+⟩ = (|z+⟩ + |z−⟩)/√2，满足 |⟨z±|x+⟩|{sup("2")} = 1/2</text>')
    doc.add('<text class="xs" x="608" y="445">强制筛选到 x+ 态后，z 方向结果立刻重新均分</text>')

    doc.add('<rect class="c3-soft" x="594" y="468" width="362" height="72" rx="9"/>')
    doc.add('<text class="smb c3-txt" x="608" y="488">2. 对照：撤掉 x− 挡板并相干重聚</text>')
    doc.add('<text class="xs" x="608" y="507">(|x+⟩⟨x+| + |x−⟩⟨x−|)|z+⟩ = I|z+⟩ = |z+⟩</text>')
    doc.add('<text class="xs" x="608" y="525">4000 原子 100% 重回 z+（与 MZI 路径干涉完全同源）</text>')

    return doc.render(), {"n_final_zp": n3_zp, "n_final_zm": n3_zm}


# ---------------------------------------------------------------------------
# Figure 4: Q2 — Robertson vs Schrodinger saturation & non-commuting Bloch paths
# ---------------------------------------------------------------------------
def build_fig4_uncertainty_robertson_schrodinger() -> tuple[str, dict[str, float]]:
    # Exact quantum verification on x-z meridian |psi(theta)> = cos(theta/2)|0> + sin(theta/2)|1>
    pauli_x: list[list[complex]] = [[0j, 1 + 0j], [1 + 0j, 0j]]
    pauli_y: list[list[complex]] = [[0j, -1j], [1j, 0j]]
    pauli_z: list[list[complex]] = [[1 + 0j, 0j], [0j, -1 + 0j]]

    def exp_val(op: list[list[complex]], psi: list[complex]) -> float:
        ov = mat_vec(op, psi)
        val = sum(a.conjugate() * b for a, b in zip(psi, ov))
        assert abs(val.imag) < TOL
        return val.real

    def bloch_vec(psi: list[complex]) -> tuple[float, float, float]:
        return exp_val(pauli_x, psi), exp_val(pauli_y, psi), exp_val(pauli_z, psi)

    # Verify theta = pi/4 (|phi> in Q2 Sec 4.3)
    th_star = math.pi / 4.0
    psi_phi = [math.cos(th_star / 2.0) + 0j, math.sin(th_star / 2.0) + 0j]
    mx, my, mz = bloch_vec(psi_phi)
    dx_phi = math.sqrt(max(0.0, 1.0 - mx * mx))
    dz_phi = math.sqrt(max(0.0, 1.0 - mz * mz))
    cov_phi = -mx * mz  # since {X, Z} = 0
    rob_phi = abs(my)   # since |[X, Z]|/2 = |<Y>|
    sch_phi = math.hypot(cov_phi, rob_phi)
    assert abs(dx_phi * dz_phi - 0.5) < TOL
    assert abs(rob_phi) < TOL
    assert abs(sch_phi - 0.5) < TOL

    # Exact rotation matrices Rx(a) and Rz(a)
    def rx_mat(a: float) -> list[list[complex]]:
        c, s = math.cos(a / 2.0), math.sin(a / 2.0)
        return [[c + 0j, -1j * s], [-1j * s, c + 0j]]

    def rz_mat(a: float) -> list[list[complex]]:
        return [[cmath.exp(-0.5j * a), 0j], [0j, cmath.exp(0.5j * a)]]

    ket0: list[complex] = [1.0 + 0j, 0.0 + 0j]
    psi_path1 = mat_vec(rz_mat(math.pi / 2.0), mat_vec(rx_mat(math.pi / 2.0), ket0))  # Rz Rx |0> -> |+>
    psi_path2 = mat_vec(rx_mat(math.pi / 2.0), mat_vec(rz_mat(math.pi / 2.0), ket0))  # Rx Rz |0> -> |-i>
    r_p1 = bloch_vec(psi_path1)
    r_p2 = bloch_vec(psi_path2)
    assert abs(r_p1[0] - 1.0) < TOL and abs(r_p1[1]) < TOL and abs(r_p1[2]) < TOL
    assert abs(r_p2[0]) < TOL and abs(r_p2[1] + 1.0) < TOL and abs(r_p2[2]) < TOL

    doc = SvgDoc(
        title="Robertson 与 Schrödinger 不确定度饱和曲线及脉冲换序 Bloch 分岔",
        desc=(
            "左面板精确绘制 x-z 子午线态 |ψ(θ)⟩ = cos(θ/2)|0⟩ + sin(θ/2)|1⟩ 在 θ ∈ [0, π] 上的 ΔX·ΔZ = ½|sin(2θ)|、"
            "贴零的 Robertson 下界 |⟨Y⟩| = 0 与全程精准饱和的 Schrödinger 协方差下界（在 θ = π/4 即子午线态 |φ⟩ 处峰值 1/2），"
            "并附赤道态 |ψ_eq(α)⟩（赤道方位角 α ∈ [0, π]）的对易子主导饱和曲线 |sin α|（在 |+i⟩ 处达 1）。右面板在右手三维 Bloch 球上对比"
            " Rz(π/2)Rx(π/2)|0⟩（终态 |+⟩）与 Rx(π/2)Rz(π/2)|0⟩（终态 |−i⟩，首段微偏便于视觉区分）两条分岔轨迹。"
        ),
    )
    doc.add_header(
        "Robertson / Schrödinger 不确定度饱和与脉冲换序 Bloch 分岔",
        "左：x-z 子午线上 Robertson 恒为零而 Schrödinger 精确饱和 ΔX·ΔZ；右：Rx(π/2) 与 Rz(π/2) 换序劈出截然不同的末态",
    )
    doc.add_panel(28, 94, 480, 458, "不确定度乘积 ΔX·ΔZ 与两条下界（θ, α ∈ [0, π]）")
    doc.add_panel(524, 94, 448, 458, "不对易旋转脉冲在 Bloch 球上的分岔路径")

    # --- Left Panel: Uncertainty curves ---
    px0, px1 = 92.0, 486.0
    py0, py1 = 456.0, 166.0  # y in [0, 1.12]
    y_max = 1.12

    def map_th(th: float) -> float:
        return px0 + (th / math.pi) * (px1 - px0)

    def map_u(u_val: float) -> float:
        return py0 - (u_val / y_max) * (py0 - py1)

    for y_t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        yt = map_u(y_t)
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(yt)}" x2="{fmt(px1)}" y2="{fmt(yt)}"/>')
        doc.add(f'<text class="sm" x="{fmt(px0 - 8)}" y="{fmt(yt + 4)}" text-anchor="end">{y_t:.2f}</text>')
    for th_v, th_lbl in [
        (0.0, "0"),
        (0.25 * math.pi, "π/4"),
        (0.5 * math.pi, "π/2"),
        (0.75 * math.pi, "3π/4"),
        (math.pi, "π"),
    ]:
        xt = map_th(th_v)
        doc.add(f'<line class="grid" x1="{fmt(xt)}" y1="{fmt(py1)}" x2="{fmt(xt)}" y2="{fmt(py0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xt)}" y="{fmt(py0 + 17)}" text-anchor="middle">{th_lbl}</text>')

    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px1 + 8)}" y2="{fmt(py0)}"/>')
    doc.add(arrow_head(px1 + 8, py0, 1, 0, 7.0))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py0)}" x2="{fmt(px0)}" y2="{fmt(py1 - 10)}"/>')
    doc.add(arrow_head(px0, py1 - 10, 0, -1, 7.0))
    doc.add(f'<text class="sm" x="{fmt(0.5 * (px0 + px1))}" y="494" text-anchor="middle">极角 θ / 赤道方位角 α (rad)</text>')
    doc.add(
        f'<text class="sm" x="46" y="{fmt(0.5 * (py0 + py1))}" text-anchor="middle" '
        f'transform="rotate(-90 46 {fmt(0.5 * (py0 + py1))})">不确定度与下界 (无量纲)</text>'
    )

    n_s = 181
    mer_pts = [(map_th(math.pi * i / (n_s - 1)), map_u(0.5 * abs(math.sin(2.0 * math.pi * i / (n_s - 1))))) for i in range(n_s)]
    eq_pts = [(map_th(math.pi * i / (n_s - 1)), map_u(math.sin(math.pi * i / (n_s - 1)))) for i in range(n_s)]

    # Shaded area under meridian curve
    doc.add(f'<path class="area1" d="{path_from_points([(px0, py0)] + mer_pts + [(px1, py0)])} Z"/>')
    # Equator curve (amber dotted)
    doc.add(f'<path class="c4" stroke-width="2.1" stroke-dasharray="3 4" d="{path_from_points(eq_pts)}"/>')
    # Meridian exact ΔX·ΔZ (solid blue) + coincident Schrödinger bound (dashed green)
    doc.add(f'<path class="c1" stroke-width="3.2" d="{path_from_points(mer_pts)}"/>')
    doc.add(f'<path class="c3" stroke-width="2.4" stroke-dasharray="7 5" d="{path_from_points(mer_pts)}"/>')
    # Meridian Robertson bound == 0 (thick red on axis)
    doc.add(f'<line class="c2" stroke-width="3.2" x1="{fmt(px0)}" y1="{fmt(py0 - 1)}" x2="{fmt(px1)}" y2="{fmt(py0 - 1)}"/>')

    # Key saturation markers
    x_q1, y_q1 = map_th(math.pi / 4.0), map_u(0.5)
    x_q3, y_q3 = map_th(0.75 * math.pi), map_u(0.5)
    x_mid, y_mid_eq = map_th(0.5 * math.pi), map_u(1.0)
    doc.add(f'<line class="guide" x1="{fmt(x_q1)}" y1="{fmt(y_q1 + 5)}" x2="{fmt(x_q1)}" y2="{fmt(py0 - 3)}"/>')
    doc.add(f'<circle class="c1-fill" cx="{fmt(x_q1)}" cy="{fmt(y_q1)}" r="5.2"/>')
    doc.add(f'<polygon class="c3-fill" points="{diamond_pts(x_q3, y_q3, 5.5)}"/>')
    doc.add(f'<circle class="c2-fill" cx="{fmt(x_q1)}" cy="{fmt(py0 - 1)}" r="4.6"/>')
    doc.add(f'<polygon class="c4-fill" points="{triangle_pts(x_mid, y_mid_eq, 5.2)}"/>')

    # Legend in open upper-left & callouts in open zones
    doc.add('<rect class="pill-bg" x="96" y="143" width="148" height="72" rx="7"/>')
    doc.add('<line class="c1" stroke-width="2.8" x1="104" y1="158" x2="124" y2="158"/>')
    doc.add('<text class="xs c1-txt" x="130" y="162">子午线 ΔX·ΔZ</text>')
    doc.add('<line class="c3" stroke-width="2.3" stroke-dasharray="6 4" x1="104" y1="176" x2="124" y2="176"/>')
    doc.add('<text class="xs c3-txt" x="130" y="180">Schrödinger（重合）</text>')
    doc.add('<line class="c2" stroke-width="2.8" x1="104" y1="194" x2="124" y2="194"/>')
    doc.add('<text class="xs c2-txt" x="130" y="198">子午线 Robertson = 0</text>')
    doc.add('<line class="c4" stroke-width="2.1" stroke-dasharray="3 3" x1="104" y1="208" x2="124" y2="208"/>')
    doc.add('<text class="xs c4-txt" x="130" y="211">赤道态 |sin α|</text>')

    # Equator |+i> callout (upper-right open space)
    doc.add('<rect class="pill-bg" x="336" y="148" width="146" height="36" rx="7"/>')
    doc.add('<text class="xsb c4-txt" x="409" y="163" text-anchor="middle">赤道 |+i⟩ (α = π/2)</text>')
    doc.add('<text class="xs" x="409" y="178" text-anchor="middle">对易子饱和 = 1.00</text>')
    doc.add(f'<line class="guide" x1="336" y1="176" x2="{fmt(x_mid + 6)}" y2="{fmt(y_mid_eq - 2)}"/>')

    # Valley callout between theta=pi/4 and theta=3pi/4
    doc.add('<rect class="pill-bg" x="218" y="348" width="144" height="54" rx="7"/>')
    doc.add('<text class="xsb c3-txt" x="290" y="363" text-anchor="middle">θ = π/4 (子午线态 |φ⟩)</text>')
    doc.add('<text class="xs c1-txt" x="290" y="378" text-anchor="middle">ΔX·ΔZ = Schrödinger = 1/2</text>')
    doc.add('<text class="xs c2-txt" x="290" y="393" text-anchor="middle">Robertson 下界贴零 = 0</text>')
    doc.add(f'<line class="guide" x1="218" y1="364" x2="{fmt(x_q1 + 5)}" y2="{fmt(y_q1 + 4)}"/>')
    doc.add(f'<line class="guide" x1="242" y1="402" x2="{fmt(x_q1 + 4)}" y2="{fmt(py0 - 5)}"/>')

    doc.add('<rect class="note" x="42" y="508" width="452" height="32" rx="8"/>')
    doc.add('<text class="xs" x="268" y="528" text-anchor="middle">子午线上 ⟨Y⟩ = 0 令对易子项归零，但实部协方差 Cov(X,Z) = −½sin(2θ) 精准补齐</text>')

    # --- Right Panel: 3D Right-handed Bloch sphere showing non-commuting pulse paths ---
    bcx, bcy, br = 748.0, 272.0, 108.0
    el = math.radians(20.0)
    phi_c = math.radians(-38.0)  # viewer in (+X, -Y, +Z) octant so |0>, |-i>, |+> are all front

    def bproj(x: float, y: float, z: float) -> tuple[float, float, float]:
        u = -x * math.sin(phi_c) + y * math.cos(phi_c)
        v = -x * math.cos(phi_c) * math.sin(el) - y * math.sin(phi_c) * math.sin(el) + z * math.cos(el)
        d = x * math.cos(phi_c) * math.cos(el) + y * math.sin(phi_c) * math.cos(el) + z * math.sin(el)
        return bcx + br * u, bcy - br * v, d

    # Sphere silhouette & equator
    ry_b = br * math.sin(el)
    doc.add(f'<circle class="bloch-circle" cx="{fmt(bcx)}" cy="{fmt(bcy)}" r="{fmt(br)}"/>')
    doc.add(f'<path class="guide" d="M {fmt(bcx - br)} {fmt(bcy)} A {fmt(br)} {fmt(ry_b)} 0 0 1 {fmt(bcx + br)} {fmt(bcy)}"/>')
    doc.add(f'<path class="c1" stroke-opacity="0.5" stroke-width="1.4" d="M {fmt(bcx - br)} {fmt(bcy)} A {fmt(br)} {fmt(ry_b)} 0 0 0 {fmt(bcx + br)} {fmt(bcy)}"/>')

    # Coordinate axes (+Z, +X, +Y, -Y)
    ax_tips = [
        ((0, 0, 1.24), "+Z |0⟩", 8, 6, "start"),
        ((1.28, 0, 0), "+X", 10, 15, "start"),
        ((0, -1.26, 0), "−Y", -8, 12, "end"),
        ((0, 1.18, 0), "+Y", 6, -4, "start"),
    ]
    for (ax_v, lbl_a, dx_l, dy_l, anc) in ax_tips:
        tx, ty, _ = bproj(*ax_v)
        cls_l = "axis" if lbl_a != "+Y" else "guide"
        doc.add(f'<line class="{cls_l}" stroke-width="1.4" x1="{fmt(bcx)}" y1="{fmt(bcy)}" x2="{fmt(tx)}" y2="{fmt(ty)}"/>')
        if lbl_a != "+Y":
            doc.add(arrow_head(tx, ty, tx - bcx, ty - bcy, 6.0))
        doc.add(f'<text class="xs" x="{fmt(tx + dx_l)}" y="{fmt(ty + dy_l)}" text-anchor="{anc}">{lbl_a}</text>')

    # Path 1: Rz(pi/2) Rx(pi/2) |0>  (|0> -> |-i> -> |+>) computed from exact unitaries
    p1_arc1 = []
    for i in range(37):
        a = (math.pi / 2.0) * i / 36.0
        r = bloch_vec(mat_vec(rx_mat(a), ket0))
        sx, sy, _ = bproj(*r)
        p1_arc1.append((sx, sy))
    p1_arc2 = []
    psi_mid = mat_vec(rx_mat(math.pi / 2.0), ket0)
    for i in range(37):
        b = (math.pi / 2.0) * i / 36.0
        r = bloch_vec(mat_vec(rz_mat(b), psi_mid))
        sx, sy, _ = bproj(*r)
        p1_arc2.append((sx, sy))

    doc.add(f'<path class="c1" stroke-width="3.2" d="{path_from_points(p1_arc1)}"/>')
    doc.add(f'<path class="c1" stroke-width="3.2" d="{path_from_points(p1_arc2)}"/>')
    doc.add(arrow_head(p1_arc1[20][0], p1_arc1[20][1], p1_arc1[20][0] - p1_arc1[18][0], p1_arc1[20][1] - p1_arc1[18][1], 7.0, "c1-fill"))
    doc.add(arrow_head(p1_arc2[-1][0], p1_arc2[-1][1], p1_arc2[-1][0] - p1_arc2[-3][0], p1_arc2[-1][1] - p1_arc2[-3][1], 8.0, "c1-fill"))

    # Path 2: Rx(pi/2) Rz(pi/2) |0>  (phase spin at |0>, then meridian to |-i>, offset -4px visually for clarity)
    p0_sx, p0_sy, _ = bproj(0.0, 0.0, 1.0)
    # Small phase-spin ellipse around North Pole
    doc.add(f'<ellipse class="c2" stroke-width="1.9" stroke-dasharray="4 2" cx="{fmt(p0_sx)}" cy="{fmt(p0_sy - 2)}" rx="15" ry="5.5"/>')
    p2_arc = [(x - 4.5, y - 2.5) for x, y in p1_arc1]
    doc.add(f'<path class="c2" stroke-width="2.6" stroke-dasharray="7 4" d="{path_from_points(p2_arc)}"/>')
    doc.add(arrow_head(p2_arc[-1][0], p2_arc[-1][1], p2_arc[-1][0] - p2_arc[-3][0], p2_arc[-1][1] - p2_arc[-3][1], 7.5, "c2-fill"))

    # Key state dots
    pmi_sx, pmi_sy, _ = bproj(0.0, -1.0, 0.0)
    pp_sx, pp_sy, _ = bproj(1.0, 0.0, 0.0)
    doc.add(f'<circle class="panel" stroke="#19324d" stroke-width="2.2" cx="{fmt(p0_sx)}" cy="{fmt(p0_sy)}" r="5.0"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(pmi_sx, pmi_sy, 6.2)}"/>')
    doc.add(f'<circle class="c1-fill" cx="{fmt(pp_sx)}" cy="{fmt(pp_sy)}" r="6.0"/>')

    # Clean non-overlapping callouts around Bloch sphere
    doc.add(f'<text class="xs c2-txt" x="652" y="164" text-anchor="end">先 R{sub("z")}：北极原地转相</text>')
    doc.add(f'<line class="guide" x1="658" y1="160" x2="{fmt(p0_sx - 18)}" y2="{fmt(p0_sy - 3)}"/>')
    doc.add(f'<text class="xs c1-txt" x="744" y="330" text-anchor="middle">再 R{sub("z")}(π/2) 沿赤道旋 90°</text>')
    doc.add('<rect class="pill-bg" x="536" y="346" width="114" height="36" rx="6"/>')
    doc.add('<text class="xsb c2-txt" x="593" y="361" text-anchor="middle">终态 2：|−i⟩</text>')
    doc.add(f'<text class="xs" x="593" y="375" text-anchor="middle">p{sub("X")}(+) = 50%</text>')
    doc.add(f'<line class="guide" x1="628" y1="346" x2="{fmt(pmi_sx - 3)}" y2="{fmt(pmi_sy + 6)}"/>')

    doc.add('<rect class="pill-bg" x="844" y="346" width="114" height="36" rx="6"/>')
    doc.add('<text class="xsb c1-txt" x="901" y="361" text-anchor="middle">终态 1：|+⟩</text>')
    doc.add(f'<text class="xs" x="901" y="375" text-anchor="middle">p{sub("X")}(+) = 100%</text>')
    doc.add(f'<line class="guide" x1="868" y1="346" x2="{fmt(pp_sx + 4)}" y2="{fmt(pp_sy + 6)}"/>')

    # Bottom comparison cards inside right panel
    doc.add('<rect class="c1-soft" x="538" y="408" width="420" height="58" rx="9"/>')
    doc.add(f'<text class="smb c1-txt" x="550" y="428">━● 路径 1（先 X 后 Z）：R{sub("z")}(π/2)R{sub("x")}(π/2)|0⟩ = e{sup("−iπ/4")}|+⟩</text>')
    doc.add('<text class="xs" x="550" y="449">先绕 X 轴转至 |−i⟩，再绕 Z 轴沿赤道转至 |+⟩（测 X 必得 +1）</text>')

    doc.add('<rect class="c2-soft" x="538" y="476" width="420" height="62" rx="9"/>')
    doc.add(f'<text class="smb c2-txt" x="550" y="496">┅◆ 路径 2（先 Z 后 X）：R{sub("x")}(π/2)R{sub("z")}(π/2)|0⟩ = e{sup("−iπ/4")}|−i⟩</text>')
    doc.add('<text class="xs" x="550" y="516">先绕 Z 轴只添全局相位，再绕 X 轴停在 |−i⟩（[X, Z] ≠ 0 致时间排序不可省）</text>')

    return doc.render(), {"schrodinger_pi4": sch_phi, "robertson_pi4": rob_phi}


# ---------------------------------------------------------------------------
# Figure 5: Q2 — Lindblad decay, 8 MCWF jump steps & 64/512/4096 convergence
# ---------------------------------------------------------------------------
def build_fig5_lindblad_trajectories() -> tuple[str, dict[str, float]]:
    # Deterministic pure-stdlib MCWF simulation (zero-temperature decay from |1>, tau = gamma*t in [0, 4])
    rng = random.Random(202605)
    t_max = 4.0
    n_steps = 200
    dt = t_max / n_steps
    p_step = 1.0 - math.exp(-dt)  # exact discrete-step jump probability matching rate gamma
    times = [i * dt for i in range(n_steps + 1)]
    exact_rho11 = [math.exp(-tau) for tau in times]

    n_total = 4096
    sum_64 = [0.0] * (n_steps + 1)
    sum_512 = [0.0] * (n_steps + 1)
    sum_4096 = [0.0] * (n_steps + 1)
    jump_times: list[float | None] = []

    for traj_idx in range(n_total):
        excited = True
        t_jump: float | None = None
        for s in range(n_steps + 1):
            val = 1.0 if excited else 0.0
            if traj_idx < 64:
                sum_64[s] += val
            if traj_idx < 512:
                sum_512[s] += val
            sum_4096[s] += val
            if excited and s < n_steps:
                if rng.random() < p_step:
                    excited = False
                    t_jump = (s + 1) * dt
        if traj_idx < 64:
            jump_times.append(t_jump)

    mean_64 = [v / 64.0 for v in sum_64]
    mean_512 = [v / 512.0 for v in sum_512]
    mean_4096 = [v / 4096.0 for v in sum_4096]

    def rmse(est: list[float]) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(est, exact_rho11)) / len(est))

    rmse_64 = rmse(mean_64)
    rmse_512 = rmse(mean_512)
    rmse_4096 = rmse(mean_4096)
    assert rmse_4096 < rmse_512 < rmse_64, f"Expected convergence: {rmse_64}, {rmse_512}, {rmse_4096}"
    assert rmse_4096 < 0.015

    # Pick 8 authentic trajectories from the first 64 spanning early, mid, late jumps & 1 survivor
    sorted_jumps = sorted(
        [(jt if jt is not None else t_max + 0.5, idx) for idx, jt in enumerate(jump_times)]
    )
    pick_indices = [0, 7, 16, 26, 36, 46, 55, 63]
    sample8_jumps = [jump_times[sorted_jumps[k][1]] for k in pick_indices]

    doc = SvgDoc(
        title="Lindblad 主方程光滑衰减与量子跳跃随机轨迹系综平均",
        desc=(
            "基于纯标准库固定种子 (202605) 蒙特卡洛波函数 (MCWF) 模拟：左面板绘制初态 |1⟩ 的零温弛豫解析解 "
            "ρ₁₁(t) = e^(−κt) 与 8 条初态 |1⟩ 单次量子跳跃阶梯轨迹，并附初态 |+⟩ 无跳跃贝叶斯下滑参考曲线 e^(−κt)/(1+e^(−κt))；"
            "右面板展示初态 |1⟩ 下 64、512 与 4096 条独立轨迹系综平均及其残差误差带按 1/√N 收敛至解析主方程解。"
        ),
    )
    doc.add_header(
        "Lindblad 主方程光滑衰减与单次量子跳跃轨迹收敛",
        f'左：初态 |1⟩ 解析解 ρ{sub("11")}(t) = e<tspan baseline-shift="super" font-size="72%">−κt</tspan> 与 8 条跳跃阶梯（绿虚线为初态 |+⟩）；右：64/512/4096 轨迹按 1/√N 收敛',
        raw_sub=True,
    )
    doc.add_panel(28, 94, 466, 458, "单次量子跳跃阶梯轨迹 vs 光滑主方程衰减")
    doc.add_panel(510, 94, 462, 458, "系综平均收敛与统计误差带（种子 202605）")

    # --- Left Panel: Smooth Lindblad decay + 8 MCWF jump step trajectories ---
    lx0, lx1 = 88.0, 470.0
    ly0, ly1 = 456.0, 168.0  # rho11 in [0, 1.08]
    y_hi = 1.08

    def lmap_t(tau: float) -> float:
        return lx0 + (tau / t_max) * (lx1 - lx0)

    def lmap_y(val: float) -> float:
        return ly0 - (val / y_hi) * (ly0 - ly1)

    for yt_v in [0.0, 0.25, 0.5, 0.75, 1.0]:
        yy = lmap_y(yt_v)
        doc.add(f'<line class="grid" x1="{fmt(lx0)}" y1="{fmt(yy)}" x2="{fmt(lx1)}" y2="{fmt(yy)}"/>')
        doc.add(f'<text class="sm" x="{fmt(lx0 - 8)}" y="{fmt(yy + 4)}" text-anchor="end">{yt_v:.2f}</text>')
    for tt_v in [0, 1, 2, 3, 4]:
        xx = lmap_t(float(tt_v))
        doc.add(f'<line class="grid" x1="{fmt(xx)}" y1="{fmt(ly1)}" x2="{fmt(xx)}" y2="{fmt(ly0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xx)}" y="{fmt(ly0 + 17)}" text-anchor="middle">{tt_v}</text>')

    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(ly0)}" x2="{fmt(lx1 + 8)}" y2="{fmt(ly0)}"/>')
    doc.add(arrow_head(lx1 + 8, ly0, 1, 0, 7.0))
    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(ly0)}" x2="{fmt(lx0)}" y2="{fmt(ly1 - 10)}"/>')
    doc.add(arrow_head(lx0, ly1 - 10, 0, -1, 7.0))
    doc.add(f'<text class="sm" x="{fmt(0.5 * (lx0 + lx1))}" y="494" text-anchor="middle">无量纲时间 κt</text>')
    doc.add(
        f'<text class="sm" x="45" y="{fmt(0.5 * (ly0 + ly1))}" text-anchor="middle" '
        f'transform="rotate(-90 45 {fmt(0.5 * (ly0 + ly1))})">激发态占据概率 ρ₁₁(t)</text>'
    )

    # 8 single quantum jump step trajectories (slight visual vertical stagger on top plateau for legibility)
    for idx, tj in enumerate(sample8_jumps):
        y_top = lmap_y(1.0) + (idx - 3.5) * 1.4
        y_bot = lmap_y(0.0) - (idx % 3) * 0.8
        cls_j = "c2" if idx % 2 == 0 else "c4"
        if tj is None or tj >= t_max:
            doc.add(f'<path class="{cls_j}" stroke-width="1.35" stroke-opacity="0.72" d="M {fmt(lx0)} {fmt(y_top)} H {fmt(lx1)}"/>')
        else:
            xj = lmap_t(tj)
            doc.add(
                f'<path class="{cls_j}" stroke-width="1.35" stroke-opacity="0.68" '
                f'd="M {fmt(lx0)} {fmt(y_top)} H {fmt(xj)} V {fmt(y_bot)} H {fmt(lx1)}"/>'
            )
            doc.add(f'<circle class="{cls_j}-fill" cx="{fmt(xj)}" cy="{fmt(y_top)}" r="3.2"/>')

    # Reference smooth Bayesian no-jump curve from |+> = (|0>+|1>)/sqrt(2): rho11_nojump = e^-t / (1 + e^-t)
    nojump_pts = [(lmap_t(tau), lmap_y(math.exp(-tau) / (1.0 + math.exp(-tau)))) for tau in times[::2]]
    doc.add(f'<path class="c3" stroke-width="1.8" stroke-dasharray="5 4" d="{path_from_points(nojump_pts)}"/>')

    # Exact smooth Lindblad analytic curve rho11(t) = e^{-gamma*t}
    exact_pts = [(lmap_t(tau), lmap_y(val)) for tau, val in zip(times[::2], exact_rho11[::2])]
    doc.add(f'<path class="c1" stroke-width="3.2" d="{path_from_points(exact_pts)}"/>')
    for t_mk in [0.0, 1.0, 2.0, 3.0]:
        doc.add(f'<circle class="c1-fill" cx="{fmt(lmap_t(t_mk))}" cy="{fmt(lmap_y(math.exp(-t_mk)))}" r="4.0"/>')

    # Legend in upper-right open space of left panel (right of jump at kappa*t = 2.0)
    doc.add('<rect class="pill-bg" x="264" y="210" width="214" height="72" rx="7"/>')
    doc.add('<line class="c1" stroke-width="3.0" x1="272" y1="227" x2="294" y2="227"/>')
    doc.add('<text class="xsb c1-txt" x="300" y="231">主方程 e<tspan baseline-shift="super" font-size="72%">−κt</tspan> (初态 |1⟩)</text>')
    doc.add('<line class="c2" stroke-width="1.8" x1="272" y1="246" x2="294" y2="246"/>')
    doc.add('<text class="xs c2-txt" x="300" y="250">8 条跳跃阶梯 (初态 |1⟩→|0⟩)</text>')
    doc.add('<line class="c3" stroke-width="1.8" stroke-dasharray="5 3" x1="272" y1="265" x2="294" y2="265"/>')
    doc.add('<text class="xs c3-txt" x="300" y="269">无跳跃贝叶斯下滑 (初态 |+⟩)</text>')

    doc.add('<rect class="note" x="42" y="508" width="438" height="32" rx="8"/>')
    doc.add('<text class="xs" x="261" y="528" text-anchor="middle">单次实验非跳即停（阶梯）；唯有对大量随机轨迹系综平均才还原光滑指数衰减</text>')

    # --- Right Panel Top: Ensemble average convergence (N = 64, 512, 4096) ---
    rx0, rx1 = 576.0, 952.0
    ry0, ry1 = 304.0, 154.0  # rho11 in [0, 1.05]

    def rmap_t(tau: float) -> float:
        return rx0 + (tau / t_max) * (rx1 - rx0)

    def rmap_y(val: float) -> float:
        return ry0 - (val / 1.05) * (ry0 - ry1)

    for yt_v in [0.0, 0.5, 1.0]:
        yy = rmap_y(yt_v)
        doc.add(f'<line class="grid" x1="{fmt(rx0)}" y1="{fmt(yy)}" x2="{fmt(rx1)}" y2="{fmt(yy)}"/>')
        doc.add(f'<text class="xs" x="{fmt(rx0 - 7)}" y="{fmt(yy + 4)}" text-anchor="end">{yt_v:.1f}</text>')
    for tt_v in [0, 1, 2, 3, 4]:
        xx = rmap_t(float(tt_v))
        doc.add(f'<line class="grid" x1="{fmt(xx)}" y1="{fmt(ry1)}" x2="{fmt(xx)}" y2="{fmt(ry0)}"/>')

    doc.add(f'<line class="axis" stroke-width="1.5" x1="{fmt(rx0)}" y1="{fmt(ry0)}" x2="{fmt(rx1 + 6)}" y2="{fmt(ry0)}"/>')
    doc.add(f'<line class="axis" stroke-width="1.5" x1="{fmt(rx0)}" y1="{fmt(ry0)}" x2="{fmt(rx0)}" y2="{fmt(ry1 - 8)}"/>')
    doc.add(arrow_head(rx0, ry1 - 8, 0, -1, 6.0))
    doc.add(
        f'<text class="xs" x="528" y="{fmt(0.5 * (ry0 + ry1))}" text-anchor="middle" '
        f'transform="rotate(-90 528 {fmt(0.5 * (ry0 + ry1))})">系综均值 ρ̄₁₁</text>'
    )

    # ±1 SE shaded band for N = 64 around exact e^{-tau}
    up64 = [(rmap_t(t), rmap_y(min(1.04, p + math.sqrt(max(0.0, p * (1.0 - p)) / 64.0)))) for t, p in zip(times[::4], exact_rho11[::4])]
    dn64 = [(rmap_t(t), rmap_y(max(0.0, p - math.sqrt(max(0.0, p * (1.0 - p)) / 64.0)))) for t, p in zip(times[::4], exact_rho11[::4])]
    doc.add(f'<path class="area2" d="{path_from_points(up64 + list(reversed(dn64)))} Z"/>')

    # Curves: N=64, N=512, N=4096, and exact analytic
    doc.add(f'<path class="c2" stroke-width="1.9" stroke-dasharray="6 3" d="{path_from_points([(rmap_t(t), rmap_y(v)) for t, v in zip(times[::2], mean_64[::2])])}"/>')
    doc.add(f'<path class="c3" stroke-width="2.0" stroke-dasharray="9 3 2 3" d="{path_from_points([(rmap_t(t), rmap_y(v)) for t, v in zip(times[::2], mean_512[::2])])}"/>')
    doc.add(f'<path class="c1" stroke-width="2.4" d="{path_from_points([(rmap_t(t), rmap_y(v)) for t, v in zip(times[::2], mean_4096[::2])])}"/>')
    doc.add(f'<path class="axis" stroke-width="1.3" stroke-dasharray="3 3" d="{path_from_points([(rmap_t(t), rmap_y(v)) for t, v in zip(times[::4], exact_rho11[::4])])}"/>')

    # Legend in upper-right open area (generous 19px line spacing for superscript)
    doc.add('<rect class="pill-bg" x="752" y="146" width="200" height="82" rx="7"/>')
    doc.add('<line class="c2" stroke-width="2.0" stroke-dasharray="5 3" x1="762" y1="162" x2="784" y2="162"/>')
    doc.add('<text class="xs c2-txt" x="790" y="166">N = 64 (±1 SE 带)</text>')
    doc.add('<line class="c3" stroke-width="2.0" stroke-dasharray="7 2 2 2" x1="762" y1="181" x2="784" y2="181"/>')
    doc.add('<text class="xs c3-txt" x="790" y="185">N = 512</text>')
    doc.add('<line class="c1" stroke-width="2.4" x1="762" y1="200" x2="784" y2="200"/>')
    doc.add('<text class="xs c1-txt" x="790" y="204">N = 4096（紧贴解析）</text>')
    doc.add('<line class="axis" stroke-width="1.3" stroke-dasharray="3 3" x1="762" y1="219" x2="784" y2="219"/>')
    doc.add('<text class="xs" x="790" y="222">解析真值 e<tspan baseline-shift="super" font-size="72%">−κt</tspan> (初态 |1⟩)</text>')

    # --- Right Panel Bottom: Residual plot (mean - exact) with ±1.96 SE bands ---
    ey0, ey1 = 458.0, 336.0  # residual in [-0.14, +0.14]
    e_lim = 0.14

    def emap_y(err: float) -> float:
        clamped = max(-e_lim, min(e_lim, err))
        return 0.5 * (ey0 + ey1) - (clamped / e_lim) * (0.5 * (ey0 - ey1))

    for ev, elbl in [(-0.10, "−0.10"), (0.0, "0"), (0.10, "+0.10")]:
        yy = emap_y(ev)
        cls_g = "axis" if ev == 0.0 else "grid"
        doc.add(f'<line class="{cls_g}" stroke-width="1.1" x1="{fmt(rx0)}" y1="{fmt(yy)}" x2="{fmt(rx1)}" y2="{fmt(yy)}"/>')
        doc.add(f'<text class="xs" x="{fmt(rx0 - 7)}" y="{fmt(yy + 4)}" text-anchor="end">{elbl}</text>')
    for tt_v in [0, 1, 2, 3, 4]:
        xx = rmap_t(float(tt_v))
        doc.add(f'<line class="grid" x1="{fmt(xx)}" y1="{fmt(ey1)}" x2="{fmt(xx)}" y2="{fmt(ey0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xx)}" y="{fmt(ey0 + 16)}" text-anchor="middle">{tt_v}</text>')

    doc.add(f'<line class="axis" stroke-width="1.5" x1="{fmt(rx0)}" y1="{fmt(ey0)}" x2="{fmt(rx1 + 6)}" y2="{fmt(ey0)}"/>')
    doc.add(arrow_head(rx1 + 6, ey0, 1, 0, 6.0))
    doc.add(f'<line class="axis" stroke-width="1.5" x1="{fmt(rx0)}" y1="{fmt(ey0)}" x2="{fmt(rx0)}" y2="{fmt(ey1 - 6)}"/>')
    doc.add(f'<text class="sm" x="{fmt(0.5 * (rx0 + rx1))}" y="497" text-anchor="middle">无量纲时间 κt</text>')
    doc.add(
        f'<text class="xs" x="528" y="{fmt(0.5 * (ey0 + ey1))}" text-anchor="middle" '
        f'transform="rotate(-90 528 {fmt(0.5 * (ey0 + ey1))})">残差 ρ̄₁₁ − e<tspan baseline-shift="super" font-size="72%">−κt</tspan></text>'
    )

    # ±1.96 SE envelopes for N=64 and N=512
    for n_b, a_cls in [(64, "area2"), (512, "area3")]:
        u_env = [(rmap_t(t), emap_y(1.96 * math.sqrt(max(0.0, p * (1.0 - p)) / n_b))) for t, p in zip(times[::4], exact_rho11[::4])]
        d_env = [(rmap_t(t), emap_y(-1.96 * math.sqrt(max(0.0, p * (1.0 - p)) / n_b))) for t, p in zip(times[::4], exact_rho11[::4])]
        doc.add(f'<path class="{a_cls}" d="{path_from_points(u_env + list(reversed(d_env)))} Z"/>')

    # Empirical residual curves
    doc.add(f'<path class="c2" stroke-width="1.6" stroke-dasharray="5 3" d="{path_from_points([(rmap_t(t), emap_y(v - p)) for t, v, p in zip(times[::2], mean_64[::2], exact_rho11[::2])])}"/>')
    doc.add(f'<path class="c3" stroke-width="1.8" d="{path_from_points([(rmap_t(t), emap_y(v - p)) for t, v, p in zip(times[::2], mean_512[::2], exact_rho11[::2])])}"/>')
    doc.add(f'<path class="c1" stroke-width="2.1" d="{path_from_points([(rmap_t(t), emap_y(v - p)) for t, v, p in zip(times[::2], mean_4096[::2], exact_rho11[::2])])}"/>')

    # Color-coded legend for red (N=64) and green (N=512) ±1.96 SE shaded bands in open strip between subplots
    doc.add('<rect class="area2" x="606" y="314" width="14" height="10" rx="2"/>')
    doc.add('<rect class="c2" stroke-width="1.1" x="606" y="314" width="14" height="10" rx="2"/>')
    doc.add('<text class="xs c2-txt" x="625" y="323">N = 64 (±1.96 SE)</text>')
    doc.add('<rect class="area3" x="742" y="314" width="14" height="10" rx="2"/>')
    doc.add('<rect class="c3" stroke-width="1.1" x="742" y="314" width="14" height="10" rx="2"/>')
    doc.add('<text class="xs c3-txt" x="761" y="323">N = 512 (±1.96 SE，95% 阴影带)</text>')

    doc.add('<rect class="note" x="524" y="508" width="434" height="32" rx="8"/>')
    doc.add(
        f'<text class="xs" x="741" y="528" text-anchor="middle">'
        f'实测 RMSE：64 ({rmse_64:.4f}) → 512 ({rmse_512:.4f}) → 4096 ({rmse_4096:.4f})，按 1/√N 缩放'
        f'</text>'
    )

    return doc.render(), {"rmse_64": round(rmse_64, 5), "rmse_512": round(rmse_512, 5), "rmse_4096": round(rmse_4096, 5)}


# ---------------------------------------------------------------------------
# Figure 6: Ch 05 — 5 superoperator representations & Pauli twirling PTM heatmaps
# ---------------------------------------------------------------------------
def build_fig6_superoperator_ptm_twirling() -> tuple[str, dict[str, float]]:
    # Exact 2x2 Pauli basis {I, X, Y, Z} and Rz(eps) PTM computation
    eps = 0.2
    paulis: list[list[list[complex]]] = [
        [[1 + 0j, 0j], [0j, 1 + 0j]],
        [[0j, 1 + 0j], [1 + 0j, 0j]],
        [[0j, -1j], [1j, 0j]],
        [[1 + 0j, 0j], [0j, -1 + 0j]],
    ]
    rz: list[list[complex]] = [[cmath.exp(-0.5j * eps), 0j], [0j, cmath.exp(0.5j * eps)]]
    rz_dag = mat_dag(rz)

    def trace2(m: list[list[complex]]) -> complex:
        return m[0][0] + m[1][1]

    def ptm_from_channel(chan_fn) -> list[list[float]]:
        out = [[0.0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                val = 0.5 * trace2(mat_mul(paulis[i], chan_fn(paulis[j])))
                assert abs(val.imag) < TOL
                out[i][j] = val.real
        return out

    def chan_rz(rho: list[list[complex]]) -> list[list[complex]]:
        return mat_mul(mat_mul(rz, rho), rz_dag)

    def chan_twirl(rho: list[list[complex]]) -> list[list[complex]]:
        acc = [[0j, 0j], [0j, 0j]]
        for p in paulis:
            inner = chan_rz(mat_mul(mat_mul(p, rho), p))
            term = mat_mul(mat_mul(p, inner), p)
            for r in range(2):
                for c in range(2):
                    acc[r][c] += 0.25 * term[r][c]
        return acc

    r_before = ptm_from_channel(chan_rz)
    r_after = ptm_from_channel(chan_twirl)

    # Exact assertions
    assert abs(r_before[1][1] - math.cos(eps)) < TOL
    assert abs(r_before[1][2] + math.sin(eps)) < TOL
    assert abs(r_before[2][1] - math.sin(eps)) < TOL
    assert abs(r_after[1][1] - math.cos(eps)) < TOL
    assert abs(r_after[1][2]) < TOL and abs(r_after[2][1]) < TOL
    f_avg_before = (3.0 + r_before[1][1] + r_before[2][2] + r_before[3][3]) / 6.0
    f_avg_after = (3.0 + r_after[1][1] + r_after[2][2] + r_after[3][3]) / 6.0
    assert abs(f_avg_before - f_avg_after) < TOL

    doc = SvgDoc(
        title="超算符五表示互转与 Pauli 旋转随机化 PTM 热力矩阵对照",
        desc=(
            "左面板展示 Stinespring 扩张、Kraus 算符和、Choi 矩阵、Liouville 超算符与 Pauli 转移矩阵 (PTM) "
            "五种等价量子信道表示的精确转换关系。右面板以 4×4 PTM 热力矩阵对照相干过旋转 Rz(0.2) 在 Pauli "
            "旋转随机化前后的元素变化：非对角旋转元 ∓0.199 彻底清零，主对角线与平均门保真度保持不变。"
        ),
    )
    doc.add_header(
        "超算符五种等价表示互转与 Pauli 旋转随机化 PTM 对照",
        "左：Stinespring ↔ Kraus ↔ Choi ↔ Liouville ↔ PTM 转换网络；右：Rz(0.2) 随机化后非对角相干元 ∓0.199 归零",
    )
    doc.add_panel(28, 94, 452, 458, "五种超算符表示的精确互转网络")
    doc.add_panel(496, 94, 476, 458, "Rz(0.2) 经 Pauli 旋转随机化前后 4×4 PTM 热力矩阵")

    # --- Left Panel: 5-node superoperator conversion graph ---
    # 1. Stinespring (top center)
    doc.add('<rect class="c5-soft" x="132" y="142" width="244" height="58" rx="9"/>')
    doc.add('<text class="smb c5-txt" x="254" y="161" text-anchor="middle">① Stinespring 扩张</text>')
    doc.add(f'<text class="xs" x="254" y="177" text-anchor="middle">Tr{sub("E")}[ U (ρ ⊗ |0⟩⟨0|{sub("E")}) U† ]</text>')
    doc.add('<text class="xs c5-txt" x="254" y="192" text-anchor="middle">自动满足 CP+TP · 微观物理图像</text>')

    # Bidirectional arrow 1 <-> 2
    doc.add('<line class="axis" stroke-width="1.6" x1="254" y1="201" x2="254" y2="235"/>')
    doc.add(arrow_head(254, 201, 0, -1, 5.5))
    doc.add(arrow_head(254, 235, 0, 1, 5.5))
    doc.add(f'<text class="xs" x="244" y="222" text-anchor="end">K{sub("k")} = {sub("E")}⟨k|U|0⟩{sub("E")}</text>')
    doc.add(f'<text class="xs" x="264" y="222">V = ∑ K{sub("k")} ⊗ |k⟩{sub("E")}</text>')

    # 2. Kraus (upper-mid center)
    doc.add('<rect class="c1-soft" x="132" y="238" width="244" height="58" rx="9"/>')
    doc.add('<text class="smb c1-txt" x="254" y="257" text-anchor="middle">② Kraus 算符和 {Kₖ}</text>')
    doc.add(f'<text class="xs" x="254" y="273" text-anchor="middle">E(ρ) = ∑ K{sub("k")} ρ K{sub("k")}†，∑ K{sub("k")}†K{sub("k")} = I</text>')
    doc.add('<text class="xs c1-txt" x="254" y="288" text-anchor="middle">极易判 TP · 适配量子跳跃轨迹</text>')

    # 3. Choi (lower-left) and 4. Liouville (lower-right)
    doc.add('<rect class="c3-soft" x="42" y="336" width="184" height="64" rx="9"/>')
    doc.add(f'<text class="smb c3-txt" x="134" y="356" text-anchor="middle">③ Choi 矩阵 J{sub("E")}</text>')
    doc.add(f'<text class="xs" x="134" y="373" text-anchor="middle">∑ vec(K{sub("k")}) vec(K{sub("k")})†</text>')
    doc.add(f'<text class="xs c3-txt" x="134" y="390" text-anchor="middle">最易判 CP：J{sub("E")} ⪰ 0</text>')

    doc.add('<rect class="c4-soft" x="282" y="336" width="184" height="64" rx="9"/>')
    doc.add(f'<text class="smb c4-txt" x="374" y="356" text-anchor="middle">④ Liouville 超算符 S{sub("E")}</text>')
    doc.add(f'<text class="xs" x="374" y="373" text-anchor="middle">∑ K{sub("k")}* ⊗ K{sub("k")} (列堆叠)</text>')
    doc.add(f'<text class="xs c4-txt" x="374" y="390" text-anchor="middle">串联即矩阵乘 S{sub("2")}S{sub("1")}</text>')

    # Arrows 2 <-> 3, 2 <-> 4, 3 <-> 4
    doc.add('<line class="axis" stroke-width="1.5" x1="194" y1="297" x2="148" y2="334"/>')
    doc.add(arrow_head(194, 297, 46, -37, 5.5))
    doc.add(arrow_head(148, 334, -46, 37, 5.5))
    doc.add('<text class="xs" x="150" y="314" text-anchor="end">谱分解 ↔ vec</text>')

    doc.add('<line class="axis" stroke-width="1.5" x1="314" y1="297" x2="360" y2="334"/>')
    doc.add(arrow_head(314, 297, -46, -37, 5.5))
    doc.add(arrow_head(360, 334, 46, 37, 5.5))
    doc.add('<text class="xs" x="358" y="314">张量求和</text>')

    doc.add('<line class="axis" stroke-width="1.6" x1="229" y1="368" x2="279" y2="368"/>')
    doc.add(arrow_head(229, 368, -1, 0, 5.5))
    doc.add(arrow_head(279, 368, 1, 0, 5.5))
    doc.add('<text class="xs" x="254" y="360" text-anchor="middle">重排</text>')
    doc.add('<text class="xs" x="254" y="384" text-anchor="middle">(p, n)</text>')

    # 5. PTM (bottom center-right)
    doc.add('<rect class="c2-soft" x="132" y="438" width="244" height="58" rx="9"/>')
    doc.add('<text class="smb c2-txt" x="254" y="457" text-anchor="middle">⑤ Pauli 转移矩阵 (PTM) R</text>')
    doc.add(f'<text class="xs" x="254" y="473" text-anchor="middle">R{sub("ij")} = ½Tr(σ{sub("i")} E(σ{sub("j")})) = (M† S{sub("E")} M){sub("ij")}</text>')
    doc.add('<text class="xs c2-txt" x="254" y="488" text-anchor="middle">全实数 · 装入 Bloch 仿射 · 随机化对角化</text>')

    # Arrow 4 <-> 5
    doc.add('<line class="axis" stroke-width="1.6" x1="352" y1="402" x2="314" y2="436"/>')
    doc.add(arrow_head(352, 402, 38, -34, 5.5))
    doc.add(arrow_head(314, 436, -38, 34, 5.5))
    doc.add('<text class="xs" x="354" y="426">酉换基 M† S M</text>')

    doc.add('<rect class="note" x="42" y="508" width="424" height="32" rx="8"/>')
    doc.add('<text class="xs" x="254" y="528" text-anchor="middle">五表示完全等价：判 CP 用 Choi，串联用 S / R，分析 Bloch 与随机化首选 PTM</text>')

    # --- Right Panel: Before vs After Pauli Twirling 4x4 PTM Heatmaps ---
    p_labels = ["I", "X", "Y", "Z"]
    cw, ch = 40.0, 38.0

    def draw_ptm_grid(gx: float, gy: float, mat: list[list[float]], heading: str, h_cls: str) -> None:
        doc.add(f'<text class="smb {h_cls}" x="{fmt(gx + 2 * cw)}" y="{fmt(gy - 22)}" text-anchor="middle">{heading}</text>')
        for j, col_lbl in enumerate(p_labels):
            doc.add(f'<text class="xsb" x="{fmt(gx + (j + 0.5) * cw)}" y="{fmt(gy - 6)}" text-anchor="middle">{col_lbl}</text>')
        for i, row_lbl in enumerate(p_labels):
            doc.add(f'<text class="xsb" x="{fmt(gx - 7)}" y="{fmt(gy + (i + 0.5) * ch + 4)}" text-anchor="end">{row_lbl}</text>')
            for j in range(4):
                v = mat[i][j]
                cx_cell = gx + j * cw
                cy_cell = gy + i * ch
                if abs(v - 1.0) < 1e-6:
                    c_cls, t_cls, v_txt = "hm-pos1", "hm-inv", "1.00"
                elif v > 0.5:
                    c_cls, t_cls, v_txt = "hm-pos2", "hm-inv", f"{v:.3f}"
                elif v > 0.05:
                    c_cls, t_cls, v_txt = "hm-pos3", "hm-dark", f"+{v:.3f}"
                elif v < -0.05:
                    c_cls, t_cls, v_txt = "hm-neg3", "hm-inv", f"−{abs(v):.3f}"
                else:
                    c_cls, t_cls, v_txt = "hm-zero", "hm-muted", "0"
                doc.add(f'<rect class="{c_cls}" x="{fmt(cx_cell)}" y="{fmt(cy_cell)}" width="{fmt(cw)}" height="{fmt(ch)}" rx="4"/>')
                doc.add(f'<text class="{t_cls}" x="{fmt(cx_cell + cw / 2)}" y="{fmt(cy_cell + ch / 2 + 4)}" text-anchor="middle">{v_txt}</text>')
        # Dashed highlight boxes on off-diagonal coherent entries (X,Y)=(1,2) and (Y,X)=(2,1)
        for (ri, cj) in [(1, 2), (2, 1)]:
            doc.add(
                f'<rect class="hm-hi" x="{fmt(gx + cj * cw + 1.5)}" y="{fmt(gy + ri * ch + 1.5)}" '
                f'width="{fmt(cw - 3)}" height="{fmt(ch - 3)}" rx="4"/>'
            )

    gy_hm = 186.0
    draw_ptm_grid(520.0, gy_hm, r_before, f'随机化前：相干 R{sub("z")}(0.2)', "c2-txt")
    draw_ptm_grid(794.0, gy_hm, r_after, f'随机化后：R{sub("twirl")}', "c3-txt")

    # Center arrow between heatmaps (x = 696..762, centered at 729)
    ay_mid = gy_hm + 2.0 * ch
    doc.add(f'<line class="c3" stroke-width="2.6" x1="696" y1="{fmt(ay_mid)}" x2="760" y2="{fmt(ay_mid)}"/>')
    doc.add(arrow_head(762, ay_mid, 1, 0, 7.5, "c3-fill"))
    doc.add(f'<text class="xsb c3-txt" x="729" y="{fmt(ay_mid - 10)}" text-anchor="middle">Twirl</text>')
    doc.add(f'<text class="xs" x="729" y="{fmt(ay_mid + 18)}" text-anchor="middle">¼∑ R{sub("P")} R R{sub("P")}</text>')

    # Colorbar legend strip (y = 352..376)
    swatches = [
        (524, "hm-pos1", "1.00"),
        (600, "hm-pos2", "0.980"),
        (686, "hm-pos3", "+0.199"),
        (782, "hm-neg3", "−0.199"),
        (878, "hm-zero", "0 (清零)"),
    ]
    for sx_w, sw_cls, sw_lbl in swatches:
        doc.add(f'<rect class="{sw_cls}" x="{sx_w}" y="355" width="16" height="14" rx="3"/>')
        doc.add(f'<text class="xs" x="{sx_w + 21}" y="366">{sw_lbl}</text>')

    # Bottom explanation cards inside right panel
    doc.add('<rect class="subpanel" x="510" y="384" width="448" height="114" rx="9"/>')
    doc.add('<text class="smb c3-txt" x="522" y="404">1. 非对角相干元精准清零（虚线框）</text>')
    doc.add('<text class="xs" x="522" y="422">I, Z 夹心保留 ±0.199，X, Y 翻号为 ∓0.199 ⇒ 四项平均精确抵消为 0</text>')
    doc.add('<text class="smb c1-txt" x="522" y="446">2. 相干二次方累积 → 温和线性退相位</text>')
    doc.add(f'<text class="xs" x="522" y="464">E{sub("twirl")}(ρ) = cos{sup("2")}(0.1)ρ + sin{sup("2")}(0.1)ZρZ（p{sub("Z")}≈1.0%），深 m 层 O(m²ε²)→O(mε²)</text>')
    doc.add(f'<text class="xs c4-txt" x="522" y="485">边界：主对角线不变 ⇒ 单步平均门保真度 F{sub("avg")} ≈ 0.9934 保持不变</text>')

    doc.add('<rect class="note" x="510" y="508" width="448" height="32" rx="8"/>')
    doc.add('<text class="xs" x="734" y="528" text-anchor="middle">工程桥梁：Pauli Twirling 把复杂相干误差转为稀疏 Pauli 信道，支撑 PEC 与 QEC 阈值</text>')

    return doc.render(), {"r_xx": round(r_after[1][1], 5), "r_xy_before": round(r_before[1][2], 5), "f_avg": round(f_avg_after, 5)}


# ---------------------------------------------------------------------------
# Figure 7: Ch 08 — Exact STO-3G H2 dissociation curve & DLA barren plateau scaling
# ---------------------------------------------------------------------------
def _boys_f0(t: float) -> float:
    if t < 1e-12:
        return 1.0 - t / 3.0
    return 0.5 * math.sqrt(math.pi / t) * math.erf(math.sqrt(t))


def _h2_sto3g_exact(r_ang: float) -> tuple[float, float, float]:
    """Exact ab-initio STO-3G H2 RHF & FCI/UCCSD/SQD energies (Ha) using Hehre-Stewart-Pople 1969 basis."""
    alpha_h = (3.42525091, 0.62391373, 0.16885540)
    coeff_h = (0.15432897, 0.53532814, 0.44463454)
    norms = [(2.0 * a / math.pi) ** 0.75 for a in alpha_h]
    r_bohr = r_ang / 0.529177210903
    coords = (0.0, r_bohr)

    s_ao = [[0.0, 0.0], [0.0, 0.0]]
    h_ao = [[0.0, 0.0], [0.0, 0.0]]
    for a_idx in range(2):
        for b_idx in range(2):
            rab2 = (coords[a_idx] - coords[b_idx]) ** 2
            for i in range(3):
                for j in range(3):
                    a, b = alpha_h[i], alpha_h[j]
                    w = coeff_h[i] * coeff_h[j] * norms[i] * norms[j]
                    p = a + b
                    mu = a * b / p
                    k_ab = math.exp(-mu * rab2)
                    s_ij = (math.pi / p) ** 1.5 * k_ab
                    t_ij = mu * (3.0 - 2.0 * mu * rab2) * s_ij
                    rp = (a * coords[a_idx] + b * coords[b_idx]) / p
                    v_ij = sum(
                        -2.0 * math.pi / p * k_ab * _boys_f0(p * (rp - coords[c_idx]) ** 2)
                        for c_idx in range(2)
                    )
                    s_ao[a_idx][b_idx] += w * s_ij
                    h_ao[a_idx][b_idx] += w * (t_ij + v_ij)

    def eri_ao(a_i: int, b_i: int, c_i: int, d_i: int) -> float:
        rab2 = (coords[a_i] - coords[b_i]) ** 2
        rcd2 = (coords[c_i] - coords[d_i]) ** 2
        acc = 0.0
        for i in range(3):
            for j in range(3):
                a, b = alpha_h[i], alpha_h[j]
                p = a + b
                rp = (a * coords[a_i] + b * coords[b_i]) / p
                k_ab = math.exp(-(a * b / p) * rab2)
                w1 = coeff_h[i] * coeff_h[j] * norms[i] * norms[j]
                for k in range(3):
                    for l in range(3):
                        c, d = alpha_h[k], alpha_h[l]
                        q = c + d
                        rq = (c * coords[c_i] + d * coords[d_i]) / q
                        k_cd = math.exp(-(c * d / q) * rcd2)
                        w2 = coeff_h[k] * coeff_h[l] * norms[k] * norms[l]
                        rpq2 = (rp - rq) ** 2
                        acc += (
                            w1 * w2 * (2.0 * math.pi ** 2.5) / (p * q * math.sqrt(p + q))
                            * k_ab * k_cd * _boys_f0(p * q / (p + q) * rpq2)
                        )
        return acc

    s12 = s_ao[0][1]
    c_mo = [
        [1.0 / math.sqrt(2.0 * (1.0 + s12)), 1.0 / math.sqrt(2.0 * (1.0 - s12))],
        [1.0 / math.sqrt(2.0 * (1.0 + s12)), -1.0 / math.sqrt(2.0 * (1.0 - s12))],
    ]
    h_mo = [
        [sum(c_mo[a][p] * c_mo[b][q] * h_ao[a][b] for a in range(2) for b in range(2)) for q in range(2)]
        for p in range(2)
    ]
    eri_cache = {
        (a, b, c, d): eri_ao(a, b, c, d)
        for a in range(2) for b in range(2) for c in range(2) for d in range(2)
    }

    def mo_eri(p: int, q: int, r: int, s: int) -> float:
        return sum(
            c_mo[a][p] * c_mo[b][q] * c_mo[c][r] * c_mo[d][s] * eri_cache[(a, b, c, d)]
            for a in range(2) for b in range(2) for c in range(2) for d in range(2)
        )

    j11, j22, k12 = mo_eri(0, 0, 0, 0), mo_eri(1, 1, 1, 1), mo_eri(0, 1, 0, 1)
    e_nuc = 1.0 / r_bohr
    h11 = 2.0 * h_mo[0][0] + j11 + e_nuc
    h22 = 2.0 * h_mo[1][1] + j22 + e_nuc
    e_fci = 0.5 * (h11 + h22) - math.hypot(0.5 * (h22 - h11), k12)
    return h11, e_fci, k12


def build_fig7_h2_vqe_barren_plateau() -> tuple[str, dict[str, float]]:
    # Exact STO-3G H2 dissociation curve for R in [0.40, 2.60] Angstrom
    r_vals = [0.40 + 2.20 * i / 88.0 for i in range(89)]
    rhf_vals: list[float] = []
    fci_vals: list[float] = []
    for r in r_vals:
        e_rhf, e_fci, _ = _h2_sto3g_exact(r)
        rhf_vals.append(e_rhf)
        fci_vals.append(e_fci)

    e_rhf_eq, e_fci_eq, _ = _h2_sto3g_exact(0.735)
    e_rhf_far, e_fci_far, _ = _h2_sto3g_exact(2.50)
    assert abs(e_fci_eq - (-1.13731)) < 5e-4
    assert e_rhf_far - e_fci_far > 0.20  # strong static correlation > 200 mHa

    # DLA gradient variance scaling Var(dC) ~ 1 / dim(g) for n = 2..16
    n_list = list(range(2, 17))
    var_so2n = [1.0 / (n * (2 * n - 1)) for n in n_list]
    var_poly3 = [1.0 / (math.comb(n + 3, 3) - 1) for n in n_list]
    var_su2n = [1.0 / (4 ** n - 1) for n in n_list]
    assert var_su2n[-1] < 1e-9 and var_so2n[-1] > 1e-3

    doc = SvgDoc(
        title="H₂ 分子 STO-3G 解离势能面与动力李代数贫瘠高原标度",
        desc=(
            "左面板从头计算最小基组 STO-3G 下 H₂ 分子解离势能面（R = 0.4–2.6 Å）：精确 FCI、单参数 UCCSD-VQE 与 "
            "SQD 曲线重合，并附化学精度带（±1.6 mHa，示意加宽）；限制 Hartree–Fock (RHF) 在拉键区因静关联误差剧烈飙升。"
            "右面板在对数纵轴展示单位纯度/全局观测量条件下的梯度方差标度 1/dim(g) 随量子比特数 n 的变化：指数 DLA su(2^n) 坠入采样噪声地板，"
            "而多项式 DLA so(2n) 与 O(n³) 保持缓慢衰减。"
        ),
    )
    doc.add_header(
        "H₂ (STO-3G) 分子解离势能面与动力李代数贫瘠高原标度",
        "左：第一性原理 STO-3G 精确 FCI / VQE / SQD vs 限制 RHF 解离失真；右：单位纯度/全局观测量条件 1/dim(g) 梯度方差标度",
    )
    doc.add_panel(28, 94, 472, 458, "H₂ (STO-3G) 解离势能面与化学精度 1.6 mHa")
    doc.add_panel(516, 94, 456, 458, "贫瘠高原标度：1/dim(g)（单位纯度/全局观测量条件）")

    # --- Left Panel: Exact H2 STO-3G Potential Energy Surface ---
    lx0, lx1 = 96.0, 480.0
    ly0, ly1 = 456.0, 162.0  # E in [-1.20, -0.60] Ha
    r_min, r_max = 0.40, 2.60
    e_min, e_max = -1.20, -0.60

    def lmap_r(r: float) -> float:
        return lx0 + (r - r_min) / (r_max - r_min) * (lx1 - lx0)

    def lmap_e(e: float) -> float:
        return ly0 - (e - e_min) / (e_max - e_min) * (ly0 - ly1)

    for e_t in [-1.2, -1.1, -1.0, -0.9, -0.8, -0.7, -0.6]:
        yy = lmap_e(e_t)
        doc.add(f'<line class="grid" x1="{fmt(lx0)}" y1="{fmt(yy)}" x2="{fmt(lx1)}" y2="{fmt(yy)}"/>')
        doc.add(f'<text class="sm" x="{fmt(lx0 - 8)}" y="{fmt(yy + 4)}" text-anchor="end">−{abs(e_t):.1f}</text>')
    for r_t in [0.5, 1.0, 1.5, 2.0, 2.5]:
        xx = lmap_r(r_t)
        doc.add(f'<line class="grid" x1="{fmt(xx)}" y1="{fmt(ly1)}" x2="{fmt(xx)}" y2="{fmt(ly0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xx)}" y="{fmt(ly0 + 17)}" text-anchor="middle">{r_t:.1f}</text>')

    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(ly0)}" x2="{fmt(lx1 + 8)}" y2="{fmt(ly0)}"/>')
    doc.add(arrow_head(lx1 + 8, ly0, 1, 0, 7.0))
    doc.add(f'<line class="axis" x1="{fmt(lx0)}" y1="{fmt(ly0)}" x2="{fmt(lx0)}" y2="{fmt(ly1 - 10)}"/>')
    doc.add(arrow_head(lx0, ly1 - 10, 0, -1, 7.0))
    doc.add(f'<text class="sm" x="{fmt(0.5 * (lx0 + lx1))}" y="494" text-anchor="middle">核间距键长 R (Å)</text>')
    doc.add(
        f'<text class="sm" x="45" y="{fmt(0.5 * (ly0 + ly1))}" text-anchor="middle" '
        f'transform="rotate(-90 45 {fmt(0.5 * (ly0 + ly1))})">分子总能量 E (Ha)</text>'
    )

    # Chemical accuracy band (±1.6 mHa = ±0.0016 Ha; drawn with minimum ±3.2px visual highlight halo + exact note)
    band_up = [(lmap_r(r), lmap_e(e + 0.006)) for r, e in zip(r_vals, fci_vals)]
    band_dn = [(lmap_r(r), lmap_e(e - 0.006)) for r, e in zip(r_vals, fci_vals)]
    doc.add(f'<path class="area3" d="{path_from_points(band_up + list(reversed(band_dn)))} Z"/>')

    # Curves: RHF (red dashed) and FCI (blue solid)
    rhf_pts = [(lmap_r(r), lmap_e(e)) for r, e in zip(r_vals, rhf_vals) if e_min <= e <= e_max]
    fci_pts = [(lmap_r(r), lmap_e(e)) for r, e in zip(r_vals, fci_vals) if e_min <= e <= e_max]
    doc.add(f'<path class="c2" stroke-width="2.4" stroke-dasharray="8 4" d="{path_from_points(rhf_pts)}"/>')
    doc.add(f'<path class="c1" stroke-width="2.8" d="{path_from_points(fci_pts)}"/>')

    # VQE (UCCSD) & SQD exact sample markers along FCI curve
    for r_vqe in [0.50, 0.735, 1.00, 1.40, 1.80, 2.20, 2.50]:
        _, e_v, _ = _h2_sto3g_exact(r_vqe)
        doc.add(f'<circle class="c1-fill" cx="{fmt(lmap_r(r_vqe))}" cy="{fmt(lmap_e(e_v))}" r="4.0"/>')
    for r_sqd in [0.60, 0.90, 1.20, 1.60, 2.00, 2.40]:
        _, e_s, _ = _h2_sto3g_exact(r_sqd)
        doc.add(f'<polygon class="c3-fill" points="{triangle_pts(lmap_r(r_sqd), lmap_e(e_s), 4.6)}"/>')

    # Vertical static correlation error gap at R = 2.5 A
    x_25 = lmap_r(2.50)
    y_rhf25, y_fci25 = lmap_e(e_rhf_far), lmap_e(e_fci_far)
    doc.add(f'<line class="c4" stroke-width="2.0" x1="{fmt(x_25)}" y1="{fmt(y_rhf25 + 5)}" x2="{fmt(x_25)}" y2="{fmt(y_fci25 - 5)}"/>')
    doc.add(arrow_head(x_25, y_rhf25 + 4, 0, -1, 6.0, "c4-fill"))
    doc.add(arrow_head(x_25, y_fci25 - 4, 0, 1, 6.0, "c4-fill"))
    doc.add('<rect class="pill-bg" x="330" y="254" width="124" height="36" rx="6"/>')
    doc.add('<text class="xsb c4-txt" x="392" y="269" text-anchor="middle">静关联误差 233 mHa</text>')
    doc.add('<text class="xs" x="392" y="284" text-anchor="middle">(145× 化学精度)</text>')

    # Legend in upper-left open zone (R=0.8..1.9, E=-0.82..-0.60)
    doc.add('<rect class="pill-bg" x="150" y="150" width="224" height="78" rx="7"/>')
    doc.add('<line class="c2" stroke-width="2.3" stroke-dasharray="7 3" x1="160" y1="166" x2="184" y2="166"/>')
    doc.add('<text class="xs c2-txt" x="190" y="170">限制 RHF（单行列式）</text>')
    doc.add('<line class="c1" stroke-width="2.6" x1="160" y1="184" x2="184" y2="184"/>')
    doc.add('<circle class="c1-fill" cx="172" cy="184" r="3.4"/>')
    doc.add('<text class="xs c1-txt" x="190" y="188">精确 FCI / UCCSD-VQE</text>')
    doc.add(f'<polygon class="c3-fill" points="{triangle_pts(172, 202, 4.2)}"/>')
    doc.add('<text class="xs c3-txt" x="190" y="206">SQD 子空间精确对角化</text>')
    doc.add('<rect class="area3" stroke="#1e7a5c" stroke-width="0.9" x="160" y="214" width="24" height="7" rx="2"/>')
    doc.add('<text class="xs" x="190" y="221">化学精度带 (±1.6 mHa，示意加宽)</text>')

    # Equilibrium point annotation (R=0.735 A, E=-1.137 Ha)
    x_eq, y_eq = lmap_r(0.735), lmap_e(e_fci_eq)
    doc.add('<rect class="pill-bg" x="174" y="408" width="156" height="36" rx="6"/>')
    doc.add('<text class="xsb c1-txt" x="252" y="423" text-anchor="middle">平衡键长 R = 0.735 Å</text>')
    doc.add(f'<text class="xs" x="252" y="438" text-anchor="middle">E{sub("FCI")} = −1.137 Ha</text>')
    doc.add(f'<line class="guide" x1="174" y1="426" x2="{fmt(x_eq + 5)}" y2="{fmt(y_eq + 1)}"/>')

    doc.add('<rect class="note" x="42" y="508" width="444" height="32" rx="8"/>')
    doc.add('<text class="xs" x="264" y="528" text-anchor="middle">阴影带示意加宽（真实 ±1.6 mHa 窄于线宽）；RHF 拉键混入离子态失真</text>')

    # --- Right Panel: Barren Plateau Log-Variance Scaling vs DLA dim(g) ---
    rx0, rx1 = 586.0, 954.0
    ry0, ry1 = 456.0, 162.0  # log10(Var) in [-10, 0]
    lv_min, lv_max = -10.0, 0.0

    def rmap_n(n_v: float) -> float:
        return rx0 + (n_v - 2.0) / (16.0 - 2.0) * (rx1 - rx0)

    def rmap_lv(lv: float) -> float:
        return ry0 - (lv - lv_min) / (lv_max - lv_min) * (ry0 - ry1)

    for lv_t, lbl_s in [(0, "0"), (-2, "−2"), (-4, "−4"), (-6, "−6"), (-8, "−8"), (-10, "−10")]:
        yy = rmap_lv(float(lv_t))
        doc.add(f'<line class="grid" x1="{fmt(rx0)}" y1="{fmt(yy)}" x2="{fmt(rx1)}" y2="{fmt(yy)}"/>')
        doc.add(f'<text class="sm" x="{fmt(rx0 - 8)}" y="{fmt(yy + 4)}" text-anchor="end">10{sup(lbl_s)}</text>')
    for nt in [2, 4, 6, 8, 10, 12, 14, 16]:
        xx = rmap_n(float(nt))
        doc.add(f'<line class="grid" x1="{fmt(xx)}" y1="{fmt(ry1)}" x2="{fmt(xx)}" y2="{fmt(ry0)}"/>')
        doc.add(f'<text class="sm" x="{fmt(xx)}" y="{fmt(ry0 + 17)}" text-anchor="middle">{nt}</text>')

    # Shot-noise floor shaded region below 10^-6 (S = 10^6 shots)
    y_floor = rmap_lv(-6.0)
    doc.add(f'<rect class="area2" x="{fmt(rx0)}" y="{fmt(y_floor)}" width="{fmt(rx1 - rx0)}" height="{fmt(ry0 - y_floor)}"/>')
    doc.add(f'<line class="c2" stroke-width="1.5" stroke-dasharray="6 4" x1="{fmt(rx0)}" y1="{fmt(y_floor)}" x2="{fmt(rx1)}" y2="{fmt(y_floor)}"/>')

    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry0)}" x2="{fmt(rx1 + 8)}" y2="{fmt(ry0)}"/>')
    doc.add(arrow_head(rx1 + 8, ry0, 1, 0, 7.0))
    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry0)}" x2="{fmt(rx0)}" y2="{fmt(ry1 - 10)}"/>')
    doc.add(arrow_head(rx0, ry1 - 10, 0, -1, 7.0))
    doc.add(f'<text class="sm" x="{fmt(0.5 * (rx0 + rx1))}" y="494" text-anchor="middle">量子比特数 n (个)</text>')
    doc.add(
        f'<text class="sm" x="530" y="{fmt(0.5 * (ry0 + ry1))}" text-anchor="middle" '
        f'transform="rotate(-90 530 {fmt(0.5 * (ry0 + ry1))})">梯度方差 Var(∂θC) (对数刻度)</text>'
    )

    # Plot the 3 DLA curves
    pts_so = [(rmap_n(float(n)), rmap_lv(math.log10(v))) for n, v in zip(n_list, var_so2n)]
    pts_p3 = [(rmap_n(float(n)), rmap_lv(math.log10(v))) for n, v in zip(n_list, var_poly3)]
    pts_su = [(rmap_n(float(n)), rmap_lv(math.log10(v))) for n, v in zip(n_list, var_su2n)]

    doc.add(f'<path class="c3" stroke-width="2.6" d="{path_from_points(pts_so)}"/>')
    doc.add(f'<path class="c1" stroke-width="2.4" stroke-dasharray="8 3 2 3" d="{path_from_points(pts_p3)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.8" stroke-dasharray="7 4" d="{path_from_points(pts_su)}"/>')

    for idx in range(0, len(n_list), 2):
        doc.add(f'<polygon class="c3-fill" points="{triangle_pts(pts_so[idx][0], pts_so[idx][1], 4.4)}"/>')
        doc.add(f'<circle class="c1-fill" cx="{fmt(pts_p3[idx][0])}" cy="{fmt(pts_p3[idx][1])}" r="3.8"/>')
        doc.add(f'<polygon class="c2-fill" points="{diamond_pts(pts_su[idx][0], pts_su[idx][1], 4.6)}"/>')

    # Legend in middle-right open triangle (below O(n^3) curve & completely above HEA red curve)
    doc.add('<rect class="pill-bg" x="756" y="258" width="194" height="68" rx="7"/>')
    doc.add('<line class="c3" stroke-width="2.4" x1="765" y1="274" x2="785" y2="274"/>')
    doc.add(f'<polygon class="c3-fill" points="{triangle_pts(775, 274, 3.8)}"/>')
    doc.add(f'<text class="xs c3-txt" x="791" y="278">so(2n) 多项式 O(n{sup("2")})</text>')
    doc.add('<line class="c1" stroke-width="2.2" stroke-dasharray="7 2 2 2" x1="765" y1="293" x2="785" y2="293"/>')
    doc.add('<circle class="c1-fill" cx="775" cy="293" r="3.2"/>')
    doc.add(f'<text class="xs c1-txt" x="791" y="297">守恒子空间 O(n{sup("3")})</text>')
    doc.add('<line class="c2" stroke-width="2.5" stroke-dasharray="6 3" x1="765" y1="312" x2="785" y2="312"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(775, 312, 4.0)}"/>')
    doc.add(f'<text class="xs c2-txt" x="791" y="316">HEA su(2{sup("n")}) 指数 4{sup("n")}−1</text>')

    # Floor & exponential plunge callout in lower-left open zone
    doc.add('<rect class="pill-bg" x="594" y="384" width="214" height="54" rx="7"/>')
    doc.add(f'<text class="xsb c2-txt" x="701" y="401" text-anchor="middle">采样噪声地板 (S = 10{sup("6")} 次采样)</text>')
    doc.add('<text class="xs" x="701" y="418" text-anchor="middle">单位纯度/全局观测量：n ≥ 10 淹没</text>')
    doc.add(f'<text class="xs" x="701" y="433" text-anchor="middle">局域 Z{sub("0")} 按 1/(2{sup("n")}+1)：n ≈ 20</text>')

    doc.add('<rect class="note" x="530" y="508" width="428" height="32" rx="8"/>')
    doc.add('<text class="xs" x="744" y="528" text-anchor="middle">多项式 dim(g) 避开指数贫瘠高原，却常落入经典可高效模拟区（可训练-可模拟权衡）</text>')

    return doc.render(), {"h2_fci_eq": round(e_fci_eq, 5), "h2_corr_25_mHa": round((e_fci_far - e_rhf_far) * 1000.0, 2)}


# ---------------------------------------------------------------------------
# XML well-formedness & Playwright + System Chrome getBBox() dual-theme audit
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
    assert len(text_nodes) >= 12, f"{filename}: too few text elements"
    for el in text_nodes:
        x = float(el.attrib["x"])
        y = float(el.attrib["y"])
        assert MARGIN <= x <= W - MARGIN, f"{filename}: text x={x} violates margin ({el.text!r})"
        assert MARGIN <= y <= H - MARGIN, f"{filename}: text y={y} violates margin ({el.text!r})"

    return {"text_count": len(text_nodes), "bytes": len(svg_text.encode("utf-8"))}


def verify_with_chromium_bbox(
    svg_paths: list[Path],
    screenshot_dir: Path | None = None,
) -> None:
    """Audit rendered <text> bounding boxes in System Chrome (light & dark) for 0 OOB, 0 Overlap, 0 Piercing."""
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
      const texts = Array.from(svg.querySelectorAll('text')).map((el, idx) => {
        const b = toBox(el);
        const bb = el.getBBox();
        return {
          idx,
          text: (el.textContent || '').replace(/\\u200b/g, '').trim(),
          cls: el.getAttribute('class') || '',
          ...b,
          cx: 0.5 * (b.x1 + b.x2),
          cy: 0.5 * (b.y1 + b.y2),
          bbox: { x: bb.x, y: bb.y, w: bb.width, h: bb.height },
          rotated: (el.getAttribute('transform') || '').includes('rotate'),
        };
      });
      const oob = texts.filter(
        b => b.x1 < margin - 0.5 || b.y1 < margin - 0.5 || b.x2 > vb.width - margin + 0.5 || b.y2 > vb.height - margin + 0.5
      );
      const overlaps = [];
      for (let i = 0; i < texts.length; i++) {
        for (let j = i + 1; j < texts.length; j++) {
          const a = texts[i], b = texts[j];
          const ox = Math.min(a.x2, b.x2) - Math.max(a.x1, b.x1);
          const oy = Math.min(a.y2, b.y2) - Math.max(a.y1, b.y1);
          if (ox > 1.0 && oy > 1.0) {
            overlaps.push({ a: a.text, b: b.text, ox: Number(ox.toFixed(2)), oy: Number(oy.toFixed(2)) });
          }
        }
      }
      // Box-piercing check: every text whose center falls inside a framed box must stay inside it;
      // and no text may clip across a panel/card/pill border.
      const frameClasses = new Set([
        'panel', 'subpanel', 'note', 'pill', 'pill-bg',
        'c1-soft', 'c2-soft', 'c3-soft', 'c4-soft', 'c5-soft',
        'hm-pos1', 'hm-pos2', 'hm-pos3', 'hm-neg3', 'hm-zero'
      ]);
      const rects = Array.from(svg.querySelectorAll('rect')).filter(el => {
        const clsList = (el.getAttribute('class') || '').split(/\\s+/);
        if (!clsList.some(c => frameClasses.has(c))) return false;
        const w = parseFloat(el.getAttribute('width') || '0');
        const h = parseFloat(el.getAttribute('height') || '0');
        return w >= 28 && h >= 18;  // ignore small legend color swatches
      }).map(el => ({
        cls: el.getAttribute('class') || '',
        ...toBox(el),
      }));
      const piercings = [];
      for (const t of texts) {
        if (t.rotated) continue;
        for (const r of rects) {
          const centerInside = t.cx > r.x1 && t.cx < r.x2 && t.cy > r.y1 && t.cy < r.y2;
          const ox = Math.min(t.x2, r.x2) - Math.max(t.x1, r.x1);
          const oy = Math.min(t.y2, r.y2) - Math.max(t.y1, r.y1);
          if (centerInside) {
            const spillL = r.x1 - t.x1;
            const spillR = t.x2 - r.x2;
            const spillT = r.y1 - t.y1;
            const spillB = t.y2 - r.y2;
            const maxSpill = Math.max(spillL, spillR, spillT, spillB);
            if (maxSpill > 1.5) {
              piercings.push({
                kind: 'overflow-box',
                text: t.text,
                rectCls: r.cls,
                spill: Number(maxSpill.toFixed(1)),
                tBox: [Number(t.x1.toFixed(1)), Number(t.y1.toFixed(1)), Number(t.x2.toFixed(1)), Number(t.y2.toFixed(1))],
                rBox: [Number(r.x1.toFixed(1)), Number(r.y1.toFixed(1)), Number(r.x2.toFixed(1)), Number(r.y2.toFixed(1))],
              });
            }
          } else if (ox > 2.0 && oy > 2.0) {
            piercings.push({
              kind: 'cross-border',
              text: t.text,
              rectCls: r.cls,
              ox: Number(ox.toFixed(1)),
              oy: Number(oy.toFixed(1)),
            });
          }
        }
      }
      return {
        count: texts.length,
        min_x: Math.min(...texts.map(b => b.x1)),
        min_y: Math.min(...texts.map(b => b.y1)),
        max_x: Math.max(...texts.map(b => b.x2)),
        max_y: Math.max(...texts.map(b => b.y2)),
        oob,
        overlaps,
        piercings,
      };
    }"""

    launch_kwargs: dict[str, object] = {"headless": True}
    if Path(CHROME_PATH).exists():
        launch_kwargs["executable_path"] = CHROME_PATH

    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs)
        try:
            page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
            failures: list[str] = []
            for svg_path in svg_paths:
                svg_content = svg_path.read_text(encoding="utf-8")
                html = (
                    "<!doctype html><html><head><meta charset='utf-8'>"
                    "<style>html,body{margin:0;padding:0;background:transparent;}"
                    f"svg{{display:block;width:{W}px;height:{H}px;}}</style>"
                    f"</head><body>{svg_content}</body></html>"
                )
                for scheme in ("light", "dark"):
                    page.emulate_media(color_scheme=scheme)
                    page.set_content(html, wait_until="load")
                    page.evaluate("() => document.fonts.ready")
                    res = page.evaluate(js_audit, MARGIN)
                    print(
                        f"[BBOX-{scheme.upper()}] {svg_path.name}: {res['count']} texts | "
                        f"span x=[{res['min_x']:.1f},{res['max_x']:.1f}] y=[{res['min_y']:.1f},{res['max_y']:.1f}] | "
                        f"oob={len(res['oob'])} overlaps={len(res['overlaps'])} piercings={len(res['piercings'])}"
                    )
                    for item in res["oob"]:
                        print(f"  [OOB] {item['text']!r}: ({item['x1']:.1f},{item['y1']:.1f})..({item['x2']:.1f},{item['y2']:.1f})")
                    for item in res["overlaps"]:
                        print(f"  [OVERLAP] {item['a']!r} <-> {item['b']!r} (ox={item['ox']}, oy={item['oy']})")
                    for item in res["piercings"]:
                        print(f"  [PIERCE] {item}")
                    if screenshot_dir is not None:
                        screenshot_dir.mkdir(parents=True, exist_ok=True)
                        page.screenshot(path=str(screenshot_dir / f"{svg_path.stem}-{scheme}.png"))
                    if res["oob"] or res["overlaps"] or res["piercings"]:
                        failures.append(
                            f"{svg_path.name}({scheme}): oob={len(res['oob'])}, "
                            f"overlaps={len(res['overlaps'])}, piercings={len(res['piercings'])}"
                        )
            assert not failures, "Audit failures: " + "; ".join(failures)
        finally:
            browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate 7 V3 scientific SVG figures (Part 1).")
    parser.add_argument("--check-bbox", action="store_true", help="Run System Chrome getBBox() dual-theme audit.")
    parser.add_argument("--screenshots", type=Path, default=None, help="Directory to save light/dark PNG previews.")
    args = parser.parse_args()

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    builders = [
        ("v3-00-amplitude-vs-memory.svg", build_fig1_amplitude_vs_memory),
        ("v3-01-svd-condition-ellipse.svg", build_fig2_svd_condition_ellipse),
        ("v3-q1-stern-gerlach-cascade.svg", build_fig3_stern_gerlach_cascade),
        ("v3-q2-uncertainty-robertson-schrodinger.svg", build_fig4_uncertainty_robertson_schrodinger),
        ("v3-q2-lindblad-trajectories.svg", build_fig5_lindblad_trajectories),
        ("v3-05-superoperator-ptm-twirling.svg", build_fig6_superoperator_ptm_twirling),
        ("v3-08-h2-vqe-barren-plateau.svg", build_fig7_h2_vqe_barren_plateau),
    ]

    out_paths: list[Path] = []
    for fname, fn in builders:
        svg_text, metrics = fn()
        check = verify_svg_xml(svg_text, fname)
        out_path = ASSETS_DIR / fname
        out_path.write_text(svg_text, encoding="utf-8")
        out_paths.append(out_path)
        print(f"[OK] {fname}: {check['bytes']} bytes, {check['text_count']} text labels | metrics={metrics}")

    if args.check_bbox or args.screenshots is not None:
        verify_with_chromium_bbox(out_paths, screenshot_dir=args.screenshots)


if __name__ == "__main__":
    main()
