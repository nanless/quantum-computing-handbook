#!/usr/bin/env python3
"""Generate 4 light/dark-adaptive scientific SVG figures (part 2b) using Python stdlib only.

Outputs to handbook/assets/:
  1. v2-16-qsvt-unification.svg   (Ch.16: QSVT unification architecture & target functions)
  2. v2-17-mbqc-aqc.svg           (Ch.17: 3-qubit linear cluster MBQC feedforward & AQC avoided crossing)
  3. v2-18-cv-phase-space.svg     (Ch.18: CV phase-space uncertainty ellipses & Wigner negativity)
  4. v2-q4-qho-wavefunctions.svg  (Q4: 1D QHO parabolic potential, Hermite-Gaussian states & tunneling tails)

Run (pure Python stdlib):
  python3 codes/practice/generate_v2_figures_part2b.py

Optional Chromium getBBox() boundary & overlap audit (requires Playwright):
  python3 codes/practice/generate_v2_figures_part2b.py --check-bbox
"""

from __future__ import annotations

import argparse
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
.subtitle{font-size:13.5px;font-weight:400;fill:#3e566d}
.sec{font-size:14.5px;font-weight:700;fill:#13263a}
.lbl{font-size:13px;font-weight:500;fill:#19324d}
.lblb{font-size:13px;font-weight:700;fill:#13263a}
.sm{font-size:12px;font-weight:400;fill:#3e566d}
.smb{font-size:12px;font-weight:600;fill:#19324d}
.axis{stroke:#19324d;stroke-width:1.7;fill:none}
.axis-fill{fill:#19324d}
.grid{stroke:#d9e3ec;stroke-width:1;fill:none}
.guide{stroke:#7c93a8;stroke-width:1.2;stroke-dasharray:4 4;fill:none}
.c1{stroke:#1b6ca8;fill:none}
.c1-fill{fill:#1b6ca8}
.c1-txt{fill:#155585}
.c1-soft{fill:#dff0fa;stroke:#1b6ca8;stroke-width:1.5}
.c2{stroke:#c74b34;fill:none}
.c2-fill{fill:#c74b34}
.c2-txt{fill:#a63824}
.c2-soft{fill:#fce7e2;stroke:#c74b34;stroke-width:1.5}
.c3{stroke:#1e7a5c;fill:none}
.c3-fill{fill:#1e7a5c}
.c3-txt{fill:#176148}
.c3-soft{fill:#e1f5ed;stroke:#1e7a5c;stroke-width:1.5}
.c4{stroke:#b57614;fill:none}
.c4-fill{fill:#b57614}
.c4-txt{fill:#8c580b}
.c4-soft{fill:#fff4db;stroke:#b57614;stroke-width:1.5}
.note{fill:#fff8e6;stroke:#c98d24;stroke-width:1.4}
.pill{fill:#edf2f7;stroke:#9fb3c8;stroke-width:1.2}
.forbid{fill:#c74b34;fill-opacity:.15}
.area1{fill:#1b6ca8;fill-opacity:.13}
.area3{fill:#1e7a5c;fill-opacity:.16}
.node-bg{fill:#ffffff;stroke:#19324d;stroke-width:1.8}
.hatch-stroke1{stroke:#1b6ca8;stroke-width:1.2;stroke-opacity:.42}
.hatch-stroke2{stroke:#c74b34;stroke-width:1.3;stroke-opacity:.52}
.hatch-stroke3{stroke:#1e7a5c;stroke-width:1.2;stroke-opacity:.42}
.hatch-stroke4{stroke:#b57614;stroke-width:1.2;stroke-opacity:.42}
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
  .c4-soft{fill:#3b2d12;stroke:#f0ba5a}
  .note{fill:#332914;stroke:#d6a240}
  .pill{fill:#203142;stroke:#4f6b85}
  .forbid{fill:#f28872;fill-opacity:.22}
  .area1{fill:#6bc2f5;fill-opacity:.16}
  .area3{fill:#5dd1a8;fill-opacity:.19}
  .node-bg{fill:#16222e;stroke:#cde0f2}
  .hatch-stroke1{stroke:#6bc2f5;stroke-opacity:.48}
  .hatch-stroke2{stroke:#f28872;stroke-opacity:.60}
  .hatch-stroke3{stroke:#5dd1a8;stroke-opacity:.48}
  .hatch-stroke4{stroke:#f0ba5a;stroke-opacity:.48}
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
            '<pattern id="hatch-red" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">'
            '<line class="hatch-stroke2" x1="0" y1="0" x2="0" y2="7"/></pattern>',
            '<pattern id="hatch-green" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<line class="hatch-stroke3" x1="0" y1="0" x2="0" y2="8"/></pattern>',
            '<pattern id="hatch-amber" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(30)">'
            '<line class="hatch-stroke4" x1="0" y1="0" x2="0" y2="7"/></pattern>',
        ]
        self.body: list[str] = []

    def add(self, snippet: str) -> None:
        self.body.append(snippet)

    def add_header(self, title_text: str, subtitle_text: str, *, raw_sub: bool = False) -> None:
        self.add(f'<rect class="bg" width="{self.w}" height="{self.h}" rx="20"/>')
        self.add(f'<text class="title" x="34" y="54">{escape(title_text)}</text>')
        s_out = subtitle_text if raw_sub else escape(subtitle_text)
        self.add(f'<text class="subtitle" x="34" y="78">{s_out}</text>')

    def add_panel(self, x: float, y: float, w: float, h: float, heading: str) -> None:
        self.add(f'<rect class="panel" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="14"/>')
        self.add(
            f'<path class="phead" d="M {fmt(x + 14)} {fmt(y + 1)} H {fmt(x + w - 14)} '
            f'Q {fmt(x + w - 1)} {fmt(y + 1)} {fmt(x + w - 1)} {fmt(y + 14)} V {fmt(y + 38)} '
            f'H {fmt(x + 1)} V {fmt(y + 14)} Q {fmt(x + 1)} {fmt(y + 1)} {fmt(x + 14)} {fmt(y + 1)} Z"/>'
        )
        self.add(f'<line class="grid" x1="{fmt(x + 1)}" y1="{fmt(y + 38)}" x2="{fmt(x + w - 1)}" y2="{fmt(y + 38)}"/>')
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
# Figure 1 (Ch.16): QSVT Unification Architecture & Exact Target Functions
# ---------------------------------------------------------------------------
def build_fig1_qsvt_unification() -> tuple[str, dict[str, float]]:
    # Exact target function definitions on x in [-1, 1]
    def f_sim(x: float) -> float:
        return math.cos(3.0 * x)

    def f_inv(x: float) -> float:
        assert abs(x) >= 0.3 - 1e-12
        return 0.3 / x

    def f_step(x: float) -> float:
        return math.tanh(8.0 * x)

    # Built-in mathematical assertions
    assert abs(f_sim(0.0) - 1.0) < 1e-15
    assert abs(f_sim(math.pi / 6.0)) < 1e-15
    assert abs(f_sim(1.0) - math.cos(3.0)) < 1e-15
    assert abs(f_inv(0.3) - 1.0) < 1e-15
    assert abs(f_inv(-0.3) + 1.0) < 1e-15
    assert abs(f_inv(1.0) - 0.3) < 1e-15
    assert abs(f_step(0.0)) < 1e-15
    assert abs(f_step(1.0) - math.tanh(8.0)) < 1e-15
    assert abs(f_step(-1.0) + f_step(1.0)) < 1e-15

    # Verify boundedness |f(x)| <= 1 on respective domains
    xs_full = [-1.0 + 2.0 * i / 400.0 for i in range(401)]
    assert all(abs(f_sim(x)) <= 1.0 + 1e-12 for x in xs_full)
    assert all(abs(f_step(x)) <= 1.0 + 1e-12 for x in xs_full)
    xs_inv_neg = [-1.0 + 0.7 * i / 140.0 for i in range(141)]
    xs_inv_pos = [0.3 + 0.7 * i / 140.0 for i in range(141)]
    assert all(abs(f_inv(x)) <= 1.0 + 1e-12 for x in xs_inv_neg + xs_inv_pos)

    doc = SvgDoc(
        title="QSVT 统一架构与三类目标多项式函数",
        desc=(
            "左面板展示量子奇异值变换（QSVT）的统一三段架构：块编码 U_A 将归一化矩阵 A/α 嵌入酉算符左上块，"
            "随后交替施加投影相位旋转 e^(iφ_k Z) 与 U_A / U_A†，最终输出奇异值多项式变换 P(A)。"
            "右面板在 x ∈ [−1, 1] 上按精确公式绘制哈密顿量模拟 cos(3x)、|x| ≥ 0.3 截断求逆 0.3/x 与阈值阶跃近似 tanh(8x)。"
        ),
    )
    doc.add_header(
        "QSVT 统一框架：从块编码与交替相位到奇异值多项式变换",
        f"左：块编码 U{sub('A')} → 交替相位旋转 e{sup('iφₖZ')} → 输出 P(A) 架构；右：x ∈ [−1, 1] 上三类精确目标函数曲线",
        raw_sub=True,
    )

    doc.add_panel(28, 94, 452, 456, "QSVT 统一电路骨架（块编码 + 交替相位）")
    doc.add_panel(496, 94, 476, 456, "三类目标函数曲线（精确公式，|f(x)| ≤ 1）")

    # --- Left Panel: 3-stage QSVT architecture ---
    # Stage 1: Block encoding U_A
    doc.add('<rect class="c1-soft" x="44" y="148" width="154" height="122" rx="10"/>')
    doc.add(f'<text class="smb c1-txt" x="121" y="168" text-anchor="middle">① 块编码 U{sub("A")}</text>')
    # Mini 2x2 block matrix graphic
    doc.add('<path class="axis" stroke-width="1.5" d="M 74 182 H 68 V 236 H 74 M 168 182 H 174 V 236 H 168"/>')
    doc.add('<rect class="area1" x="76" y="185" width="44" height="23" rx="4"/>')
    doc.add('<text class="smb c1-txt" x="98" y="201" text-anchor="middle">A / α</text>')
    doc.add('<text class="sm" x="146" y="201" text-anchor="middle">*</text>')
    doc.add('<text class="sm" x="98" y="226" text-anchor="middle">*</text>')
    doc.add('<text class="sm" x="146" y="226" text-anchor="middle">*</text>')
    doc.add('<text class="sm" x="121" y="258" text-anchor="middle">‖A‖ ≤ α，左上块编码</text>')

    # Arrow 1 -> 2
    doc.add('<line class="axis" x1="198" y1="209" x2="218" y2="209"/>')
    doc.add(arrow_head(220, 209, 1, 0, 7.5))

    # Stage 2: Alternating phase rotations
    doc.add('<rect class="c4-soft" x="222" y="148" width="242" height="122" rx="10"/>')
    doc.add(f'<text class="smb c4-txt" x="343" y="168" text-anchor="middle">② 交替相位旋转 e{sup("iφₖZ")}</text>')
    # Mini circuit wires inside Stage 2 (split top wire around ellipsis so no line crosses text)
    doc.add('<text class="sm" x="231" y="200">|0ᵃ⟩</text>')
    doc.add('<text class="sm" x="231" y="234">|ψ⟩</text>')
    doc.add('<line class="axis" stroke-width="1.4" x1="255" y1="196" x2="413" y2="196"/>')
    doc.add('<line class="axis" stroke-width="1.4" x1="429" y1="196" x2="458" y2="196"/>')
    doc.add('<line class="axis" stroke-width="1.4" x1="255" y1="230" x2="458" y2="230"/>')
    # Gates: U_A, e^(iφ1 Z), U_A†, e^(iφ2 Z), ..., φ_d
    doc.add('<rect class="c1-soft" x="262" y="184" width="32" height="58" rx="5"/>')
    doc.add(f'<text class="smb c1-txt" x="278" y="217" text-anchor="middle">U{sub("A")}</text>')
    doc.add('<rect class="note" x="301" y="182" width="30" height="28" rx="5"/>')
    doc.add('<rect fill="url(#hatch-amber)" x="301" y="182" width="30" height="28" rx="5"/>')
    doc.add('<text class="smb c4-txt" x="316" y="200" text-anchor="middle">φ₁</text>')
    doc.add('<rect class="c1-soft" stroke-dasharray="4 2" x="338" y="184" width="32" height="58" rx="5"/>')
    doc.add(f'<text class="smb c1-txt" x="354" y="217" text-anchor="middle">U{sub("A")}†</text>')
    doc.add('<rect class="note" x="377" y="182" width="30" height="28" rx="5"/>')
    doc.add('<rect fill="url(#hatch-amber)" x="377" y="182" width="30" height="28" rx="5"/>')
    doc.add('<text class="smb c4-txt" x="392" y="200" text-anchor="middle">φ₂</text>')
    doc.add('<text class="smb" x="421" y="200" text-anchor="middle">⋯</text>')
    doc.add('<rect class="note" x="431" y="182" width="27" height="28" rx="5"/>')
    doc.add('<rect fill="url(#hatch-amber)" x="431" y="182" width="27" height="28" rx="5"/>')
    doc.add(f'<text class="smb c4-txt" x="444.5" y="200" text-anchor="middle">φ{sub("d")}</text>')
    doc.add(f'<text class="sm" x="343" y="258" text-anchor="middle">相位角 {{φ{sub("k")}}} 决定 d 次多项式 P</text>')

    # Arrow 2 -> 3
    doc.add('<line class="axis" x1="343" y1="270" x2="343" y2="294"/>')
    doc.add(arrow_head(343, 296, 0, 1, 7.5))
    doc.add('<text class="sm" x="353" y="287">辅助位后选择 |0ᵃ⟩</text>')

    # Stage 3: Output P(A)
    doc.add('<rect class="c3-soft" x="44" y="298" width="420" height="110" rx="10"/>')
    doc.add('<text class="smb c3-txt" x="254" y="320" text-anchor="middle">③ 输出：奇异值多项式变换 P(A)</text>')
    doc.add(
        f'<text class="lbl" x="254" y="346" text-anchor="middle">'
        f'A/α = ∑ σ{sub("j")}|u{sub("j")}⟩⟨v{sub("j")}| ↦ P{sup("(SV)")}(A/α) = ∑ P(σ{sub("j")})|u{sub("j")}⟩⟨v{sub("j")}|'
        f'</text>'
    )
    doc.add(
        '<text class="sm" x="254" y="371" text-anchor="middle">'
        '厄米且满足奇偶性与 |P(x)| ≤ 1 约束时，简记为 P(A/α)'
        '</text>'
    )
    doc.add(
        f'<text class="sm" x="254" y="394" text-anchor="middle">'
        f'成功概率 ‖P(A/α)|ψ⟩‖²；换任务只需替换经典预计算相位 {{φ{sub("k")}}}'
        f'</text>'
    )

    # Bottom unification table inside Left Panel
    doc.add('<rect class="note" x="44" y="422" width="420" height="114" rx="10"/>')
    doc.add('<text class="smb" x="58" y="443">同一电路骨架统一三类典型算法：</text>')
    # Row 1: Sim
    doc.add('<line class="c1" stroke-width="2.5" x1="58" y1="466" x2="86" y2="466"/>')
    doc.add('<circle class="c1-fill" cx="72" cy="466" r="3.8"/>')
    doc.add(f'<text class="sm" x="95" y="470">哈密顿量模拟：cos(tx)、sin(tx) 拼出 e{sup("−iAt")}</text>')
    # Row 2: Inversion
    doc.add('<line class="c2" stroke-width="2.4" stroke-dasharray="7 4" x1="58" y1="493" x2="86" y2="493"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(72, 493, 4.4)}"/>')
    doc.add('<text class="sm" x="95" y="497">矩阵求逆 HHL：|x| ≥ 1/κ 处逼近 1/(κx) → A⁻¹</text>')
    # Row 3: Threshold / Search
    doc.add('<line class="c3" stroke-width="2.4" stroke-dasharray="8 3 2 3" x1="58" y1="520" x2="86" y2="520"/>')
    doc.add(f'<polygon class="c3-fill" points="{square_pts(72, 520, 3.6)}"/>')
    doc.add('<text class="sm" x="95" y="524">阈值搜索 / 滤波：光滑阶跃 tanh(kx) 逼近 sgn(x)</text>')

    # --- Right Panel: Exact target function curves on x in [-1, 1] ---
    px0, px1 = 568.0, 944.0
    py_top, py_bot = 178.0, 452.0
    y_min_val, y_max_val = -1.18, 1.18

    def gx(x: float) -> float:
        return px0 + ((x + 1.0) / 2.0) * (px1 - px0)

    def gy(y: float) -> float:
        return py_bot - ((y - y_min_val) / (y_max_val - y_min_val)) * (py_bot - py_top)

    # Legend row cleanly above plot frame
    doc.add('<line class="c1" stroke-width="2.5" x1="516" y1="154" x2="544" y2="154"/>')
    doc.add('<circle class="c1-fill" cx="530" cy="154" r="3.6"/>')
    doc.add('<text class="sm" x="550" y="158">cos(3x)</text>')

    doc.add('<line class="c2" stroke-width="2.4" stroke-dasharray="7 4" x1="622" y1="154" x2="650" y2="154"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(636, 154, 4.2)}"/>')
    doc.add('<text class="sm" x="656" y="158">0.3/x (|x|≥0.3)</text>')

    doc.add('<line class="c3" stroke-width="2.4" stroke-dasharray="8 3 2 3" x1="794" y1="154" x2="822" y2="154"/>')
    doc.add(f'<polygon class="c3-fill" points="{square_pts(808, 154, 3.5)}"/>')
    doc.add('<text class="sm" x="828" y="158">tanh(8x)</text>')

    # Grid lines and ticks
    for xv in [-1.0, -0.5, 0.0, 0.5, 1.0]:
        xg = gx(xv)
        doc.add(f'<line class="grid" x1="{fmt(xg)}" y1="{fmt(py_top)}" x2="{fmt(xg)}" y2="{fmt(py_bot)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(xg)}" y1="{fmt(py_bot)}" x2="{fmt(xg)}" y2="{fmt(py_bot + 5)}"/>')
        lbl_x = "0" if xv == 0 else f"{xv:+.1f}".replace("-", "−").replace("+", "")
        doc.add(f'<text class="sm" x="{fmt(xg)}" y="{fmt(py_bot + 19)}" text-anchor="middle">{lbl_x}</text>')

    for yv in [-1.0, -0.5, 0.0, 0.5, 1.0]:
        yg = gy(yv)
        cls_g = "guide" if abs(yv) == 1.0 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(px0)}" y1="{fmt(yg)}" x2="{fmt(px1)}" y2="{fmt(yg)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(px0 - 5)}" y1="{fmt(yg)}" x2="{fmt(px0)}" y2="{fmt(yg)}"/>')
        lbl_y = "0" if yv == 0 else f"{yv:+.1f}".replace("-", "−").replace("+", "")
        doc.add(f'<text class="sm" x="{fmt(px0 - 9)}" y="{fmt(yg + 4)}" text-anchor="end">{lbl_y}</text>')

    # Shaded truncation band |x| < 0.3 for 0.3/x
    x_m03, x_p03 = gx(-0.3), gx(0.3)
    doc.add(f'<rect class="forbid" x="{fmt(x_m03)}" y="{fmt(py_top)}" width="{fmt(x_p03 - x_m03)}" height="{fmt(py_bot - py_top)}"/>')
    doc.add(f'<rect fill="url(#hatch-red)" x="{fmt(x_m03)}" y="{fmt(py_top)}" width="{fmt(x_p03 - x_m03)}" height="{fmt(py_bot - py_top)}"/>')
    doc.add(f'<line class="c2" stroke-width="1.1" stroke-dasharray="3 3" x1="{fmt(x_m03)}" y1="{fmt(py_top)}" x2="{fmt(x_m03)}" y2="{fmt(py_bot)}"/>')
    doc.add(f'<line class="c2" stroke-width="1.1" stroke-dasharray="3 3" x1="{fmt(x_p03)}" y1="{fmt(py_top)}" x2="{fmt(x_p03)}" y2="{fmt(py_bot)}"/>')

    # Zero reference axes inside plot
    doc.add(f'<line class="axis" stroke-width="1.1" stroke-opacity="0.55" x1="{fmt(px0)}" y1="{fmt(gy(0.0))}" x2="{fmt(px1)}" y2="{fmt(gy(0.0))}"/>')
    doc.add(f'<line class="axis" stroke-width="1.1" stroke-opacity="0.55" x1="{fmt(gx(0.0))}" y1="{fmt(py_top)}" x2="{fmt(gx(0.0))}" y2="{fmt(py_bot)}"/>')

    # Curves from exact formulas
    sim_pts = [(gx(x), gy(f_sim(x))) for x in xs_full]
    step_pts = [(gx(x), gy(f_step(x))) for x in xs_full]
    inv_neg_pts = [(gx(x), gy(f_inv(x))) for x in xs_inv_neg]
    inv_pos_pts = [(gx(x), gy(f_inv(x))) for x in xs_inv_pos]

    doc.add(f'<path class="c3" stroke-width="2.4" stroke-dasharray="9 3 2 3" d="{path_from_points(step_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.5" stroke-dasharray="8 4" d="{path_from_points(inv_neg_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.5" stroke-dasharray="8 4" d="{path_from_points(inv_pos_pts)}"/>')
    doc.add(f'<path class="c1" stroke-width="2.6" d="{path_from_points(sim_pts)}"/>')

    # Distinguishing markers along curves (grayscale accessibility)
    for xm in [-0.85, 0.0, 0.85]:
        doc.add(f'<circle class="c1-fill" cx="{fmt(gx(xm))}" cy="{fmt(gy(f_sim(xm)))}" r="4.2"/>')
    for xm in [-0.7, -0.3, 0.3, 0.7]:
        doc.add(f'<polygon class="c2-fill" points="{diamond_pts(gx(xm), gy(f_inv(xm)), 5.0)}"/>')
    for xm in [-0.6, 0.0, 0.6]:
        doc.add(f'<polygon class="c3-fill" points="{square_pts(gx(xm), gy(f_step(xm)), 4.0)}"/>')

    # Outer frame axes with arrows
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px1 + 8)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(px1 + 10, py_bot, 1, 0, 7.5))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(px0, py_top - 10, 0, -1, 7.5))
    doc.add(f'<text class="lbl" x="{fmt(0.5*(px0+px1))}" y="492" text-anchor="middle">归一化奇异值 x = σ / α（无量纲）</text>')
    doc.add(
        f'<text class="lbl" x="520" y="{fmt(0.5*(py_top+py_bot))}" text-anchor="middle" '
        f'transform="rotate(-90 520 {fmt(0.5*(py_top+py_bot))})">目标函数值 f(x)（无量纲）</text>'
    )

    # Clean non-overlapping in-plot callouts (verified empty regions)
    # Upper-left region x in [-0.95, -0.45], y in [0.35, 0.92] has zero curves
    doc.add('<rect class="pill" x="576" y="216" width="114" height="44" rx="7"/>')
    doc.add('<text class="smb" x="633" y="234" text-anchor="middle">酉有界约束</text>')
    doc.add('<text class="sm" x="633" y="252" text-anchor="middle">|f(x)| ≤ 1 虚线</text>')
    doc.add(f'<line class="guide" x1="633" y1="216" x2="633" y2="{fmt(gy(1.0) + 2)}"/>')

    # Lower-right empty pocket x in [0.06, 0.61], y in [-0.90, -0.42] has zero curves
    doc.add('<rect class="c2-soft" x="768" y="370" width="106" height="44" rx="7"/>')
    doc.add('<text class="smb c2-txt" x="821" y="388" text-anchor="middle">|x| &lt; 0.3 截断区</text>')
    doc.add('<text class="sm c2-txt" x="821" y="406" text-anchor="middle">保证 |0.3/x| ≤ 1</text>')
    doc.add('<line class="c2" stroke-width="1.3" x1="768" y1="392" x2="752" y2="392"/>')
    doc.add(arrow_head(750, 392, -1, 0, 6.5, "c2-fill"))

    # Bottom summary pill
    doc.add('<rect class="pill" x="514" y="505" width="442" height="32" rx="8"/>')
    doc.add(
        '<text class="sm" x="735" y="525" text-anchor="middle">'
        '三类曲线均满足 |f(x)| ≤ 1；次数 d 随精度与 1/0.3 截断区倒数（条件数 κ）增长'
        '</text>'
    )

    return doc.render(), {
        "cos_3": round(f_sim(1.0), 6),
        "inv_at_0p3": f_inv(0.3),
        "tanh_8": round(f_step(1.0), 8),
    }


# ---------------------------------------------------------------------------
# Figure 2 (Ch.17): 3-Qubit Linear Cluster MBQC Feedforward & AQC Gap
# ---------------------------------------------------------------------------
def build_fig2_mbqc_aqc() -> tuple[str, dict[str, float]]:
    # Exact two-level AQC Hamiltonian H(s) = -(1-s) X - s Z, s in [0, 1]
    def e_plus(s: float) -> float:
        return math.hypot(1.0 - s, s)

    def e_minus(s: float) -> float:
        return -math.hypot(1.0 - s, s)

    def gap(s: float) -> float:
        return e_plus(s) - e_minus(s)

    # Built-in exact assertions
    assert abs(e_plus(0.0) - 1.0) < 1e-15
    assert abs(e_minus(0.0) + 1.0) < 1e-15
    assert abs(e_plus(1.0) - 1.0) < 1e-15
    assert abs(e_minus(1.0) + 1.0) < 1e-15
    assert abs(e_plus(0.5) - 1.0 / math.sqrt(2.0)) < 1e-15
    assert abs(gap(0.5) - math.sqrt(2.0)) < 1e-15
    s_grid = [i / 400.0 for i in range(401)]
    min_gap_val = min(gap(s) for s in s_grid)
    assert abs(min_gap_val - math.sqrt(2.0)) < 1e-12

    doc = SvgDoc(
        title="MBQC 三比特线性簇态自适应前馈与 AQC 二能级绝热避免交叉",
        desc=(
            "左面板绘制三比特线性簇态 q₀(|ψ⟩)—CZ₀₁—q₁(|+⟩)—CZ₁₂—q₂(|+⟩)，标注 q₀ 测角 α 产出 m₀、"
            "经典虚线前馈控制 q₁ 物理测角 β_phys = (−1)^m₀ β 产出 m₁，以及末位 q₂ 施加逆序纠正 Z^m₀ X^m₁。"
            "右面板精确绘出绝热哈密顿量 H(s) = −(1−s)X − sZ 在 s ∈ [0, 1] 的两条本征能级 E_±(s) = ±√((1−s)²+s²)，"
            "标注 s = 0.5 处最小谱隙 Δ_min = √2 ≈ 1.414。"
        ),
    )
    doc.add_header(
        "MBQC 簇态自适应前馈 与 AQC 二能级绝热避免交叉",
        f"左：三比特线性簇态测量前馈与末位逆序纠正；右：H(s) = −(1−s)X − sZ 精确能谱与最小谱隙 Δ{sub('min')}",
        raw_sub=True,
    )

    doc.add_panel(28, 94, 466, 456, "基于测量的量子计算（MBQC）：三比特线性簇态")
    doc.add_panel(508, 94, 464, 456, "绝热量子计算（AQC）：二能级避免交叉（精确能谱）")

    # --- Left Panel: 3-qubit linear cluster state + planar feedforward ---
    # Compact legend at top of left panel
    doc.add('<line class="c1" stroke-width="2.6" x1="46" y1="152" x2="72" y2="152"/>')
    doc.add('<text class="sm" x="78" y="156">CZ 纠缠边</text>')
    doc.add('<line class="c4" stroke-width="2" stroke-dasharray="6 3" x1="156" y1="152" x2="184" y2="152"/>')
    doc.add(arrow_head(187, 152, 1, 0, 6.0, "c4-fill"))
    doc.add('<text class="sm" x="193" y="156">经典前馈线</text>')
    doc.add('<circle class="c3-soft" cx="290" cy="152" r="8"/>')
    doc.add('<circle class="c3" stroke-width="1.2" cx="290" cy="152" r="5"/>')
    doc.add('<text class="sm" x="304" y="156">输出比特 q₂（未测）</text>')

    # Cluster state chain at y=218
    cy_chain = 218.0
    x_q0, x_q1, x_q2 = 102.0, 250.0, 404.0
    r_node = 25.0

    # Step headings above nodes
    doc.add(f'<text class="smb c1-txt" x="{fmt(x_q0)}" y="182" text-anchor="middle">① 测 q₀</text>')
    doc.add(f'<text class="smb c1-txt" x="{fmt(x_q1)}" y="182" text-anchor="middle">② 自适应测 q₁</text>')
    doc.add(f'<text class="smb c3-txt" x="{fmt(x_q2)}" y="182" text-anchor="middle">③ 逆序纠正 q₂</text>')

    # CZ entangling edges
    doc.add(f'<line class="c1" stroke-width="2.8" x1="{fmt(x_q0 + r_node)}" y1="{fmt(cy_chain)}" x2="{fmt(x_q1 - r_node)}" y2="{fmt(cy_chain)}"/>')
    doc.add(f'<line class="c1" stroke-width="2.8" x1="{fmt(x_q1 + r_node)}" y1="{fmt(cy_chain)}" x2="{fmt(x_q2 - r_node)}" y2="{fmt(cy_chain)}"/>')

    # CZ badges on edges
    for x_mid, cz_lbl in [(0.5 * (x_q0 + x_q1), "CZ₀₁"), (0.5 * (x_q1 + x_q2), "CZ₁₂")]:
        doc.add(f'<rect class="pill" x="{fmt(x_mid - 23)}" y="{fmt(cy_chain - 12)}" width="46" height="24" rx="11"/>')
        doc.add(f'<text class="smb" x="{fmt(x_mid)}" y="{fmt(cy_chain + 4)}" text-anchor="middle">{cz_lbl}</text>')

    # Qubit nodes
    doc.add(f'<circle class="c1-soft" stroke-width="2.2" cx="{fmt(x_q0)}" cy="{fmt(cy_chain)}" r="{fmt(r_node)}"/>')
    doc.add(f'<text class="smb c1-txt" x="{fmt(x_q0)}" y="{fmt(cy_chain - 4)}" text-anchor="middle">q₀</text>')
    doc.add(f'<text class="sm" x="{fmt(x_q0)}" y="{fmt(cy_chain + 13)}" text-anchor="middle">|ψ⟩</text>')

    doc.add(f'<circle class="c1-soft" stroke-width="2.2" cx="{fmt(x_q1)}" cy="{fmt(cy_chain)}" r="{fmt(r_node)}"/>')
    doc.add(f'<text class="smb c1-txt" x="{fmt(x_q1)}" y="{fmt(cy_chain - 4)}" text-anchor="middle">q₁</text>')
    doc.add(f'<text class="sm" x="{fmt(x_q1)}" y="{fmt(cy_chain + 13)}" text-anchor="middle">|+⟩</text>')

    doc.add(f'<circle class="c3-soft" stroke-width="2.2" cx="{fmt(x_q2)}" cy="{fmt(cy_chain)}" r="{fmt(r_node)}"/>')
    doc.add(f'<circle class="c3" stroke-width="1.2" cx="{fmt(x_q2)}" cy="{fmt(cy_chain)}" r="{fmt(r_node - 4.5)}"/>')
    doc.add(f'<text class="smb c3-txt" x="{fmt(x_q2)}" y="{fmt(cy_chain - 4)}" text-anchor="middle">q₂</text>')
    doc.add(f'<text class="sm" x="{fmt(x_q2)}" y="{fmt(cy_chain + 13)}" text-anchor="middle">|+⟩</text>')

    # Arrows from nodes to operation boxes
    for xn in [x_q0, x_q1, x_q2]:
        doc.add(f'<line class="axis" x1="{fmt(xn)}" y1="{fmt(cy_chain + r_node)}" x2="{fmt(xn)}" y2="274"/>')
        doc.add(arrow_head(xn, 276, 0, 1, 7.0))

    # Operation boxes (y=276..342)
    # Box 1: q0 measurement
    doc.add('<rect class="c2-soft" x="42" y="276" width="120" height="66" rx="9"/>')
    doc.add('<rect fill="url(#hatch-red)" x="42" y="276" width="120" height="10" rx="4"/>')
    doc.add('<text class="smb c2-txt" x="102" y="301" text-anchor="middle">测角 α（XY 面）</text>')
    doc.add('<text class="smb" x="102" y="320" text-anchor="middle">产出 m₀ ∈ {0,1}</text>')
    doc.add('<text class="sm" x="102" y="336" text-anchor="middle">各占概率 1/2</text>')

    # Box 2: q1 adaptive measurement
    doc.add('<rect class="c2-soft" x="178" y="276" width="144" height="66" rx="9"/>')
    doc.add('<rect fill="url(#hatch-red)" x="178" y="276" width="144" height="10" rx="4"/>')
    doc.add(f'<text class="smb c2-txt" x="250" y="301" text-anchor="middle">β{sub("phys")} = (−1){sup("m₀")} β</text>')
    doc.add('<text class="smb" x="250" y="320" text-anchor="middle">产出 m₁ ∈ {0,1}</text>')
    doc.add('<text class="sm" x="250" y="336" text-anchor="middle">受 m₀ 前馈翻号</text>')

    # Box 3: q2 inverse-order Pauli correction
    doc.add('<rect class="c3-soft" x="336" y="276" width="144" height="66" rx="9"/>')
    doc.add('<rect fill="url(#hatch-green)" x="336" y="276" width="144" height="10" rx="4"/>')
    doc.add(f'<text class="smb c3-txt" x="408" y="301" text-anchor="middle">逆序纠正 Z{sup("m₀")} X{sup("m₁")}</text>')
    doc.add(f'<text class="sm" x="408" y="320" text-anchor="middle">先施 X{sup("m₁")} 再 Z{sup("m₀")}</text>')
    doc.add('<text class="sm c3-txt" x="408" y="336" text-anchor="middle">还原 J(β)J(α)|ψ⟩</text>')

    # Planar classical feedforward dashed routing (zero crossings)
    # Rail 1 (inner, y=378): m1 -> X^m1 on q2
    doc.add('<path class="c4" stroke-width="2" stroke-dasharray="6 4" d="M 268 342 V 378 H 376 V 344"/>')
    doc.add(arrow_head(376, 342, 0, -1, 7.0, "c4-fill"))
    doc.add(f'<text class="smb c4-txt" x="322" y="371" text-anchor="middle">m₁ → X{sup("m₁")}</text>')

    # Rail 2 (outer, y=416): m0 -> beta_phys on q1 AND Z^m0 on q2
    doc.add('<path class="c4" stroke-width="2" stroke-dasharray="6 4" d="M 102 342 V 416 H 440 V 344"/>')
    doc.add(arrow_head(440, 342, 0, -1, 7.0, "c4-fill"))
    doc.add('<line class="c4" stroke-width="2" stroke-dasharray="6 4" x1="230" y1="416" x2="230" y2="344"/>')
    doc.add(arrow_head(230, 342, 0, -1, 7.0, "c4-fill"))
    doc.add('<circle class="c4-fill" cx="230" cy="416" r="3.6"/>')
    doc.add(f'<text class="smb c4-txt" x="166" y="408" text-anchor="middle">m₀ 前馈控 β{sub("phys")}</text>')
    doc.add(f'<text class="smb c4-txt" x="342" y="408" text-anchor="middle">m₀ 前馈控 Z{sup("m₀")}</text>')

    # Bottom explanation card inside Left Panel
    doc.add('<rect class="note" x="42" y="444" width="438" height="90" rx="10"/>')
    doc.add(f'<text class="smb" x="261" y="466" text-anchor="middle">未纠正末态：exp[−i(α+β{sub("phys")})/2] X{sup("m₁")} Z{sup("m₀")} J(β)J(α)|ψ⟩</text>')
    doc.add(f'<text class="sm" x="261" y="490" text-anchor="middle">矩阵求逆逆序：(X{sup("m₁")} Z{sup("m₀")})⁻¹ = Z{sup("m₀")} X{sup("m₁")}（右起先 X{sup("m₁")}，后 Z{sup("m₀")}）</text>')
    doc.add(f'<text class="sm c2-txt" x="261" y="514" text-anchor="middle">若顺序颠倒成 X{sup("m₁")} Z{sup("m₀")}，m₀ = m₁ = 1 时因 XZ = −ZX 引入 −1 符号差</text>')

    # --- Right Panel: Exact AQC avoided crossing spectrum ---
    px0, px1 = 578.0, 938.0
    py_top, py_bot = 184.0, 452.0
    e_min_ax, e_max_ax = -1.25, 1.25

    def gx(s: float) -> float:
        return px0 + s * (px1 - px0)

    def gy(e_val: float) -> float:
        return py_bot - ((e_val - e_min_ax) / (e_max_ax - e_min_ax)) * (py_bot - py_top)

    # Legend above plot
    doc.add('<line class="c1" stroke-width="2.6" x1="524" y1="154" x2="554" y2="154"/>')
    doc.add('<circle class="c1-fill" cx="539" cy="154" r="3.8"/>')
    doc.add('<text class="sm" x="560" y="158">基态 E₋(s) = −√((1−s)²+s²)</text>')

    doc.add('<line class="c2" stroke-width="2.5" stroke-dasharray="8 4" x1="742" y1="154" x2="772" y2="154"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(757, 154, 4.4)}"/>')
    doc.add('<text class="sm" x="778" y="158">激发态 E₊(s) = +√((1−s)²+s²)</text>')

    # Grid & ticks
    for sv in [0.0, 0.25, 0.5, 0.75, 1.0]:
        xg = gx(sv)
        cls_g = "guide" if sv == 0.5 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(xg)}" y1="{fmt(py_top)}" x2="{fmt(xg)}" y2="{fmt(py_bot)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(xg)}" y1="{fmt(py_bot)}" x2="{fmt(xg)}" y2="{fmt(py_bot + 5)}"/>')
        lbl_s = f"{sv:.2f}".rstrip("0").rstrip(".") if sv not in (0.0, 1.0) else f"{sv:.0f}"
        doc.add(f'<text class="sm" x="{fmt(xg)}" y="{fmt(py_bot + 19)}" text-anchor="middle">{lbl_s}</text>')

    for ev in [-1.0, -0.5, 0.0, 0.5, 1.0]:
        yg = gy(ev)
        cls_g = "guide" if ev == 0.0 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(px0)}" y1="{fmt(yg)}" x2="{fmt(px1)}" y2="{fmt(yg)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(px0 - 5)}" y1="{fmt(yg)}" x2="{fmt(px0)}" y2="{fmt(yg)}"/>')
        lbl_e = "0" if ev == 0 else f"{ev:+.1f}".replace("-", "−").replace("+", "")
        doc.add(f'<text class="sm" x="{fmt(px0 - 9)}" y="{fmt(yg + 4)}" text-anchor="end">{lbl_e}</text>')

    # Soft translucent green band around s=0.5 highlighting minimum spectral gap
    x_mid = gx(0.5)
    y_ep_mid = gy(e_plus(0.5))
    y_em_mid = gy(e_minus(0.5))
    doc.add(f'<rect class="area3" x="{fmt(x_mid - 14)}" y="{fmt(y_ep_mid)}" width="28" height="{fmt(y_em_mid - y_ep_mid)}" rx="4"/>')

    # Exact energy level curves
    pts_plus = [(gx(s), gy(e_plus(s))) for s in s_grid]
    pts_minus = [(gx(s), gy(e_minus(s))) for s in s_grid]
    doc.add(f'<path class="c2" stroke-width="2.6" stroke-dasharray="9 5" d="{path_from_points(pts_plus)}"/>')
    doc.add(f'<path class="c1" stroke-width="2.8" d="{path_from_points(pts_minus)}"/>')

    # Key point markers
    for sm in [0.0, 0.5, 1.0]:
        doc.add(f'<circle class="c1-fill" cx="{fmt(gx(sm))}" cy="{fmt(gy(e_minus(sm)))}" r="4.6"/>')
        doc.add(f'<polygon class="c2-fill" points="{diamond_pts(gx(sm), gy(e_plus(sm)), 5.4)}"/>')

    # Minimum gap double-headed arrow at s = 0.5
    doc.add(f'<line class="c3" stroke-width="2.2" x1="{fmt(x_mid)}" y1="{fmt(y_ep_mid + 8)}" x2="{fmt(x_mid)}" y2="{fmt(y_em_mid - 8)}"/>')
    doc.add(arrow_head(x_mid, y_ep_mid + 6, 0, -1, 7.5, "c3-fill"))
    doc.add(arrow_head(x_mid, y_em_mid - 6, 0, 1, 7.5, "c3-fill"))

    # Gap callout box in the open central band (|E| < 0.65 is completely empty)
    doc.add('<rect class="c3-soft" x="774" y="290" width="152" height="54" rx="8"/>')
    doc.add(f'<text class="smb c3-txt" x="850" y="311" text-anchor="middle">最小谱隙 Δ{sub("min")} = √2</text>')
    doc.add('<text class="sm c3-txt" x="850" y="331" text-anchor="middle">≈ 1.414（s = 0.5）</text>')
    doc.add('<line class="c3" stroke-width="1.4" x1="774" y1="317" x2="760" y2="317"/>')

    # Endpoint eigenstate annotations (strictly inside open gap away from curves)
    doc.add('<text class="smb c2-txt" x="588" y="256">|−⟩（H(0)=−X）</text>')
    doc.add('<text class="smb c1-txt" x="588" y="392">|+⟩（初态基态）</text>')
    doc.add('<text class="smb c2-txt" x="928" y="256" text-anchor="end">|1⟩（H(1)=−Z）</text>')
    doc.add('<text class="smb c1-txt" x="928" y="392" text-anchor="end">|0⟩（目标基态）</text>')
    doc.add(f'<text class="sm" x="{fmt(x_mid - 20)}" y="266" text-anchor="end">+1/√2</text>')
    doc.add(f'<text class="sm" x="{fmt(x_mid - 20)}" y="376" text-anchor="end">−1/√2</text>')

    # Outer frame axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px1 + 8)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(px1 + 10, py_bot, 1, 0, 7.5))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(px0, py_top - 10, 0, -1, 7.5))
    doc.add(f'<text class="lbl" x="{fmt(0.5*(px0+px1))}" y="492" text-anchor="middle">插值参数 s ∈ [0,1]（线性调度时 s = t/T）</text>')
    doc.add(
        f'<text class="lbl" x="528" y="{fmt(0.5*(py_top+py_bot))}" text-anchor="middle" '
        f'transform="rotate(-90 528 {fmt(0.5*(py_top+py_bot))})">本征能量 E(s)（无量纲能量单位）</text>'
    )

    # Bottom summary pill
    doc.add('<rect class="pill" x="524" y="505" width="432" height="32" rx="8"/>')
    doc.add(
        f'<text class="sm" x="740" y="525" text-anchor="middle">'
        f'H(s) = −(1−s)X − sZ；s = 0.5 避免交叉处 Δ{sub("min")} 决定绝热演化时长下界'
        f'</text>'
    )

    return doc.render(), {
        "e_plus_mid": round(e_plus(0.5), 6),
        "gap_min": round(gap(0.5), 6),
        "gap_endpoints": gap(0.0),
    }


# ---------------------------------------------------------------------------
# Figure 3 (Ch.18): CV Phase-Space Uncertainty Ellipses & Wigner Negativity
# ---------------------------------------------------------------------------
def build_fig3_cv_phase_space() -> tuple[str, dict[str, float]]:
    # Convention: dimensionless [q_hat, p_hat] = i (hbar = 1), V_vac = (1/2) I_2
    r_sq = 0.7
    r_vac = 1.0 / math.sqrt(2.0)
    a_q = math.exp(-r_sq) / math.sqrt(2.0)
    b_p = math.exp(r_sq) / math.sqrt(2.0)
    q_coh, p_coh = 2.0, 1.0

    def w0_q(q: float) -> float:
        return math.exp(-q * q) / math.pi

    def w1_q(q: float) -> float:
        return (2.0 * q * q - 1.0) * math.exp(-q * q) / math.pi

    # Built-in mathematical assertions
    assert abs(r_vac * r_vac - 0.5) < 1e-15
    assert abs(a_q * b_p - 0.5) < 1e-15  # Minimum-uncertainty area preservation
    assert abs(math.pi * a_q * b_p - math.pi * r_vac * r_vac) < 1e-15
    assert abs(w0_q(0.0) - 1.0 / math.pi) < 1e-15
    assert abs(w1_q(0.0) + 1.0 / math.pi) < 1e-15
    q_zero = 1.0 / math.sqrt(2.0)
    assert abs(w1_q(q_zero)) < 1e-15
    assert abs(w1_q(-q_zero)) < 1e-15
    q_lobe = math.sqrt(1.5)
    assert abs(w1_q(q_lobe) - (2.0 / math.pi) * math.exp(-1.5)) < 1e-15

    # Numerical radial normalization check: 2*pi * integral_0^inf W_n(r) r dr == 1
    n_quad = 2000
    r_max = 8.0
    dr = r_max / n_quad
    int_w0 = 0.0
    int_w1 = 0.0
    for i in range(n_quad + 1):
        r_val = i * dr
        wt = 1.0 if i in (0, n_quad) else (4.0 if i % 2 == 1 else 2.0)
        int_w0 += wt * 2.0 * math.pi * r_val * (math.exp(-r_val * r_val) / math.pi)
        int_w1 += wt * 2.0 * math.pi * r_val * ((2.0 * r_val * r_val - 1.0) * math.exp(-r_val * r_val) / math.pi)
    int_w0 *= dr / 3.0
    int_w1 *= dr / 3.0
    assert abs(int_w0 - 1.0) < 1e-8
    assert abs(int_w1 - 1.0) < 1e-8

    doc = SvgDoc(
        title="连续变量相空间不确定度等高椭圆与 Wigner 函数非经典负值区",
        desc=(
            "在无量纲正则约定 [q̂, p̂] = i（ℏ = 1）下，左面板以 1:1 等比例绘出真空圆盘（半径 1/√2）、"
            "中心位于 (2, 1) 的位移相干态以及 r = 0.7 的 q 方向压缩态椭圆（半轴 e^(−0.7)/√2 与 e^(0.7)/√2）。"
            "右面板精确绘出真空态 W₀(q,0) = (1/π)e^(−q²) 与单光子 Fock 态 W₁(q,0) = (1/π)(2q²−1)e^(−q²)，"
            "并用阴影斜纹标出原点附近 |q| < 1/√2 的负值非经典区（W₁(0,0) = −1/π ≈ −0.318）。"
        ),
    )
    doc.add_header(
        "连续变量相空间不确定度椭圆与 Wigner 函数负值区",
        "无量纲约定 [q̂, p̂] = i（ℏ = 1）；左：1σ 相空间等高椭圆（1:1 等比例）；右：W₀(q,0) 与 W₁(q,0) 精确剖面",
    )

    doc.add_panel(28, 94, 456, 456, "相空间 (q, p) 不确定度等高椭圆（1:1 等比例）")
    doc.add_panel(500, 94, 472, 456, "Wigner 准概率剖面 W(q, 0) 与非经典负值区")

    # --- Left Panel: Phase-space ellipses (strict 1:1 aspect ratio) ---
    scale = 64.0  # px per dimensionless unit (both q and p)
    q_min, q_max = -2.0, 3.2
    p_min, p_max = -2.0, 2.2
    px0 = 104.0
    px1 = px0 + (q_max - q_min) * scale  # 436.8
    py_top = 182.0
    py_bot = py_top + (p_max - p_min) * scale  # 450.8

    def gx_l(qv: float) -> float:
        return px0 + (qv - q_min) * scale

    def gy_l(pv: float) -> float:
        return py_bot - (pv - p_min) * scale

    ox, oy = gx_l(0.0), gy_l(0.0)

    # Legend above left plot
    doc.add('<line class="c1" stroke-width="2.4" x1="42" y1="154" x2="66" y2="154"/>')
    doc.add('<circle class="c1-fill" cx="54" cy="154" r="3.2"/>')
    doc.add('<text class="sm" x="72" y="158">真空 |0⟩</text>')

    doc.add('<line class="c3" stroke-width="2.3" stroke-dasharray="7 3 2 3" x1="146" y1="154" x2="174" y2="154"/>')
    doc.add(f'<polygon class="c3-fill" points="{square_pts(160, 154, 3.2)}"/>')
    doc.add('<text class="sm" x="180" y="158">相干态 (2,1)</text>')

    doc.add('<line class="c2" stroke-width="2.3" stroke-dasharray="6 4" x1="278" y1="154" x2="306" y2="154"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(292, 154, 3.8)}"/>')
    doc.add('<text class="sm" x="312" y="158">q 压缩态 (r=0.7)</text>')

    # Grid and ticks (left panel)
    for qv in [-2, -1, 0, 1, 2, 3]:
        xg = gx_l(float(qv))
        cls_g = "guide" if qv == 0 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(xg)}" y1="{fmt(py_top)}" x2="{fmt(xg)}" y2="{fmt(py_bot)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(xg)}" y1="{fmt(py_bot)}" x2="{fmt(xg)}" y2="{fmt(py_bot + 5)}"/>')
        lbl_q = str(qv).replace("-", "−")
        doc.add(f'<text class="sm" x="{fmt(xg)}" y="{fmt(py_bot + 19)}" text-anchor="middle">{lbl_q}</text>')

    for pv in [-2, -1, 0, 1, 2]:
        yg = gy_l(float(pv))
        cls_g = "guide" if pv == 0 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(px0)}" y1="{fmt(yg)}" x2="{fmt(px1)}" y2="{fmt(yg)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(px0 - 5)}" y1="{fmt(yg)}" x2="{fmt(px0)}" y2="{fmt(yg)}"/>')
        lbl_p = str(pv).replace("-", "−")
        doc.add(f'<text class="sm" x="{fmt(px0 - 9)}" y="{fmt(yg + 4)}" text-anchor="end">{lbl_p}</text>')

    # 1) Displaced coherent state circle at (2, 1), radius 1/sqrt(2)
    cx_coh, cy_coh = gx_l(q_coh), gy_l(p_coh)
    r_vac_px = r_vac * scale
    doc.add(f'<circle class="area3" cx="{fmt(cx_coh)}" cy="{fmt(cy_coh)}" r="{fmt(r_vac_px)}"/>')
    doc.add(f'<circle fill="url(#hatch-green)" cx="{fmt(cx_coh)}" cy="{fmt(cy_coh)}" r="{fmt(r_vac_px)}"/>')
    doc.add(f'<circle class="c3" stroke-width="2.4" stroke-dasharray="9 3 2 3" cx="{fmt(cx_coh)}" cy="{fmt(cy_coh)}" r="{fmt(r_vac_px)}"/>')

    # 2) q-squeezed state ellipse at (0, 0), rx = e^{-0.7}/sqrt(2), ry = e^{0.7}/sqrt(2)
    rx_sq_px = a_q * scale
    ry_sq_px = b_p * scale
    doc.add(f'<ellipse class="forbid" cx="{fmt(ox)}" cy="{fmt(oy)}" rx="{fmt(rx_sq_px)}" ry="{fmt(ry_sq_px)}"/>')
    doc.add(f'<ellipse fill="url(#hatch-red)" cx="{fmt(ox)}" cy="{fmt(oy)}" rx="{fmt(rx_sq_px)}" ry="{fmt(ry_sq_px)}"/>')
    doc.add(f'<ellipse class="c2" stroke-width="2.4" stroke-dasharray="7 4" cx="{fmt(ox)}" cy="{fmt(oy)}" rx="{fmt(rx_sq_px)}" ry="{fmt(ry_sq_px)}"/>')

    # 3) Vacuum state circle at (0, 0), radius 1/sqrt(2)
    doc.add(f'<circle class="area1" cx="{fmt(ox)}" cy="{fmt(oy)}" r="{fmt(r_vac_px)}"/>')
    doc.add(f'<circle class="c1" stroke-width="2.5" cx="{fmt(ox)}" cy="{fmt(oy)}" r="{fmt(r_vac_px)}"/>')

    # Displacement vector from (0,0) to (2,1)
    vx, vy = cx_coh - ox, cy_coh - oy
    vlen = math.hypot(vx, vy)
    doc.add(
        f'<line class="c3" stroke-width="1.9" stroke-dasharray="5 3" '
        f'x1="{fmt(ox + 5 * vx / vlen)}" y1="{fmt(oy + 5 * vy / vlen)}" '
        f'x2="{fmt(cx_coh - 8 * vx / vlen)}" y2="{fmt(cy_coh - 8 * vy / vlen)}"/>'
    )
    doc.add(arrow_head(cx_coh - 5 * vx / vlen, cy_coh - 5 * vy / vlen, vx, vy, 7.5, "c3-fill"))

    # Center & semi-axis markers
    doc.add(f'<circle class="c1-fill" cx="{fmt(ox)}" cy="{fmt(oy)}" r="3.8"/>')
    doc.add(f'<polygon class="c3-fill" points="{square_pts(cx_coh, cy_coh, 4.0)}"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(ox, oy - ry_sq_px, 4.4)}"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(ox, oy + ry_sq_px, 4.4)}"/>')

    # Direct non-overlapping labels inside left plot
    doc.add('<text class="smb c2-txt" x="198" y="232" text-anchor="end">q 压缩态</text>')
    doc.add('<text class="sm c2-txt" x="198" y="248" text-anchor="end">Δq≈0.35</text>')
    doc.add('<text class="sm c2-txt" x="198" y="264" text-anchor="end">Δp≈1.42</text>')
    doc.add(f'<line class="c2" stroke-width="1.1" x1="201" y1="240" x2="{fmt(ox - rx_sq_px + 2)}" y2="250"/>')

    doc.add('<text class="smb c1-txt" x="180" y="400" text-anchor="end">真空 |0⟩</text>')
    doc.add('<text class="sm c1-txt" x="180" y="416" text-anchor="end">R=1/√2</text>')
    doc.add('<line class="c1" stroke-width="1.1" x1="183" y1="396" x2="200" y2="365"/>')

    doc.add('<text class="smb c3-txt" x="358" y="346" text-anchor="middle">位移相干态</text>')
    doc.add('<text class="sm c3-txt" x="358" y="362" text-anchor="middle">中心 (2, 1)</text>')
    doc.add(f'<line class="c3" stroke-width="1.1" x1="358" y1="331" x2="358" y2="{fmt(cy_coh + r_vac_px + 3)}"/>')

    # Outer frame axes (left panel)
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px1 + 8)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(px1 + 10, py_bot, 1, 0, 7.5))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(px0, py_top - 10, 0, -1, 7.5))
    doc.add(f'<text class="lbl" x="{fmt(0.5*(px0+px1))}" y="492" text-anchor="middle">位置正交分量 q（无量纲）</text>')
    doc.add(
        f'<text class="lbl" x="50" y="{fmt(0.5*(py_top+py_bot))}" text-anchor="middle" '
        f'transform="rotate(-90 50 {fmt(0.5*(py_top+py_bot))})">动量正交分量 p（无量纲）</text>'
    )

    doc.add('<rect class="pill" x="42" y="505" width="428" height="32" rx="8"/>')
    doc.add(
        '<text class="sm" x="256" y="525" text-anchor="middle">'
        '三态均饱和最小不确定度 Δq·Δp = 1/2，1σ 等高椭圆面积恒为 π/2'
        '</text>'
    )

    # --- Right Panel: Wigner function cross-sections W0(q,0) and W1(q,0) ---
    rx0, rx1 = 572.0, 944.0
    ry_top, ry_bot = 182.0, 452.0
    wq_min, wq_max = -3.0, 3.0
    wv_min, wv_max = -0.38, 0.38

    def gx_r(qv: float) -> float:
        return rx0 + ((qv - wq_min) / (wq_max - wq_min)) * (rx1 - rx0)

    def gy_r(wv: float) -> float:
        return ry_bot - ((wv - wv_min) / (wv_max - wv_min)) * (ry_bot - ry_top)

    # Legend above right plot
    doc.add('<line class="c1" stroke-width="2.6" x1="516" y1="154" x2="544" y2="154"/>')
    doc.add('<circle class="c1-fill" cx="530" cy="154" r="3.6"/>')
    doc.add(f'<text class="sm" x="550" y="158">真空态 W₀(q,0) = e{sup("−q²")}/π</text>')

    doc.add('<line class="c2" stroke-width="2.5" stroke-dasharray="8 4" x1="734" y1="154" x2="762" y2="154"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(748, 154, 4.2)}"/>')
    doc.add('<text class="sm" x="768" y="158">单光子 W₁(q,0)</text>')

    # Grid & ticks (right panel)
    for qv in [-3, -2, -1, 0, 1, 2, 3]:
        xg = gx_r(float(qv))
        cls_g = "guide" if qv == 0 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(xg)}" y1="{fmt(ry_top)}" x2="{fmt(xg)}" y2="{fmt(ry_bot)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(xg)}" y1="{fmt(ry_bot)}" x2="{fmt(xg)}" y2="{fmt(ry_bot + 5)}"/>')
        lbl_q = str(qv).replace("-", "−")
        doc.add(f'<text class="sm" x="{fmt(xg)}" y="{fmt(ry_bot + 19)}" text-anchor="middle">{lbl_q}</text>')

    for wv in [-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3]:
        yg = gy_r(wv)
        cls_g = "axis" if wv == 0.0 else "grid"
        sw_extra = ' stroke-width="1.2" stroke-opacity="0.6"' if wv == 0.0 else ""
        doc.add(f'<line class="{cls_g}"{sw_extra} x1="{fmt(rx0)}" y1="{fmt(yg)}" x2="{fmt(rx1)}" y2="{fmt(yg)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(rx0 - 5)}" y1="{fmt(yg)}" x2="{fmt(rx0)}" y2="{fmt(yg)}"/>')
        if wv in (-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3):
            lbl_w = "0" if wv == 0.0 else f"{wv:+.1f}".replace("-", "−").replace("+", "")
            doc.add(f'<text class="sm" x="{fmt(rx0 - 9)}" y="{fmt(yg + 4)}" text-anchor="end">{lbl_w}</text>')

    # Shaded negative non-classical region for W1(q, 0) on [-1/sqrt(2), +1/sqrt(2)]
    qs_neg = [-q_zero + (2.0 * q_zero) * i / 120.0 for i in range(121)]
    neg_poly = [(gx_r(-q_zero), gy_r(0.0))] + [(gx_r(q), gy_r(w1_q(q))) for q in qs_neg] + [(gx_r(q_zero), gy_r(0.0))]
    doc.add(f'<polygon class="forbid" points="{pts_str(neg_poly)}"/>')
    doc.add(f'<polygon fill="url(#hatch-red)" points="{pts_str(neg_poly)}"/>')

    # Exact W0 and W1 curves
    qs_all = [wq_min + (wq_max - wq_min) * i / 360.0 for i in range(361)]
    w0_pts = [(gx_r(q), gy_r(w0_q(q))) for q in qs_all]
    w1_pts = [(gx_r(q), gy_r(w1_q(q))) for q in qs_all]
    doc.add(f'<path class="c1" stroke-width="2.6" d="{path_from_points(w0_pts)}"/>')
    doc.add(f'<path class="c2" stroke-width="2.5" stroke-dasharray="8 4" d="{path_from_points(w1_pts)}"/>')

    # Key feature markers
    doc.add(f'<circle class="c1-fill" cx="{fmt(gx_r(0.0))}" cy="{fmt(gy_r(w0_q(0.0)))}" r="4.8"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(gx_r(0.0), gy_r(w1_q(0.0)), 5.4)}"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(gx_r(q_lobe), gy_r(w1_q(q_lobe)), 4.6)}"/>')
    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(gx_r(-q_lobe), gy_r(w1_q(-q_lobe)), 4.6)}"/>')
    doc.add(f'<circle class="node-bg" cx="{fmt(gx_r(-q_zero))}" cy="{fmt(gy_r(0.0))}" r="3.6"/>')
    doc.add(f'<circle class="node-bg" cx="{fmt(gx_r(q_zero))}" cy="{fmt(gy_r(0.0))}" r="3.6"/>')

    # Clean non-overlapping callouts
    doc.add(f'<line class="c1" stroke-width="1.2" x1="{fmt(gx_r(0.0) + 7)}" y1="{fmt(gy_r(w0_q(0.0)))}" x2="800" y2="{fmt(gy_r(w0_q(0.0)))}"/>')
    doc.add(f'<text class="smb c1-txt" x="804" y="{fmt(gy_r(w0_q(0.0)) + 4)}">W₀(0,0) = +1/π</text>')
    doc.add(f'<text class="sm c1-txt" x="804" y="{fmt(gy_r(w0_q(0.0)) + 20)}">≈ +0.318（全正）</text>')

    # Negative non-classical callout box in empty lower-right region
    doc.add('<rect class="c2-soft" x="796" y="384" width="146" height="54" rx="8"/>')
    doc.add('<text class="smb c2-txt" x="869" y="405" text-anchor="middle">非经典负值区</text>')
    doc.add('<text class="sm c2-txt" x="869" y="425" text-anchor="middle">W₁(0,0)=−1/π≈−0.318</text>')
    doc.add(f'<line class="c2" stroke-width="1.3" x1="796" y1="418" x2="{fmt(gx_r(0.0) + 10)}" y2="{fmt(gy_r(w1_q(0.0)) - 2)}"/>')
    doc.add(arrow_head(gx_r(0.0) + 8, gy_r(w1_q(0.0)) - 2, -1, 0.2, 6.5, "c2-fill"))

    # Zero-crossing callout in empty lower-left region
    doc.add('<text class="sm" x="640" y="392" text-anchor="middle">零点 q = ±1/√2</text>')
    doc.add('<text class="sm" x="640" y="408" text-anchor="middle">≈ ±0.707</text>')
    doc.add(f'<line class="guide" x1="654" y1="378" x2="{fmt(gx_r(-q_zero) - 3)}" y2="{fmt(gy_r(0.0) + 5)}"/>')

    # Outer frame axes (right panel)
    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry_bot)}" x2="{fmt(rx1 + 8)}" y2="{fmt(ry_bot)}"/>')
    doc.add(arrow_head(rx1 + 10, ry_bot, 1, 0, 7.5))
    doc.add(f'<line class="axis" x1="{fmt(rx0)}" y1="{fmt(ry_bot)}" x2="{fmt(rx0)}" y2="{fmt(ry_top - 8)}"/>')
    doc.add(arrow_head(rx0, ry_top - 10, 0, -1, 7.5))
    doc.add(f'<text class="lbl" x="{fmt(0.5*(rx0+rx1))}" y="492" text-anchor="middle">位置正交分量 q（无量纲，p = 0 剖面）</text>')
    doc.add(
        f'<text class="lbl" x="520" y="{fmt(0.5*(ry_top+ry_bot))}" text-anchor="middle" '
        f'transform="rotate(-90 520 {fmt(0.5*(ry_top+ry_bot))})">Wigner 准概率 W(q, 0)（无量纲）</text>'
    )

    doc.add('<rect class="pill" x="514" y="505" width="444" height="32" rx="8"/>')
    doc.add(
        '<text class="sm" x="736" y="525" text-anchor="middle">'
        '高斯态 W(q,p) ≥ 0；单光子 Fock 态 |1⟩ 出现负值，标志非高斯非经典性'
        '</text>'
    )

    return doc.render(), {
        "r_vac": round(r_vac, 6),
        "a_q": round(a_q, 6),
        "b_p": round(b_p, 6),
        "w1_origin": round(w1_q(0.0), 6),
        "w1_lobe": round(w1_q(q_lobe), 6),
    }


# ---------------------------------------------------------------------------
# Figure 4 (Q4): 1D QHO Parabolic Potential, Wavefunctions & Tunneling Tails
# ---------------------------------------------------------------------------
def build_fig4_qho_wavefunctions() -> tuple[str, dict[str, float]]:
    def hermite(n: int, xi: float) -> float:
        if n == 0:
            return 1.0
        if n == 1:
            return 2.0 * xi
        if n == 2:
            return 4.0 * xi * xi - 2.0
        if n == 3:
            return 8.0 * xi * xi * xi - 12.0 * xi
        raise ValueError(f"Unsupported n={n}")

    def psi_n(n: int, xi: float) -> float:
        norm = 1.0 / math.sqrt((2.0 ** n) * math.factorial(n) * math.sqrt(math.pi))
        return norm * hermite(n, xi) * math.exp(-0.5 * xi * xi)

    def prob_n(n: int, xi: float) -> float:
        val = psi_n(n, xi)
        return val * val

    def simpson(fn, a: float, b: float, steps: int = 2000) -> float:
        assert steps % 2 == 0
        h = (b - a) / steps
        acc = fn(a) + fn(b)
        for i in range(1, steps):
            acc += (4.0 if i % 2 == 1 else 2.0) * fn(a + i * h)
        return acc * h / 3.0

    # Built-in mathematical & physical assertions
    tunneling_probs: dict[int, float] = {}
    for n in range(4):
        norm_sq = simpson(lambda x, nn=n: prob_n(nn, x), -8.0, 8.0, 2000)
        assert abs(norm_sq - 1.0) < 1e-8, f"n={n} normalization failed: {norm_sq}"
        tp = math.sqrt(2.0 * n + 1.0)
        p_forbid = 2.0 * simpson(lambda x, nn=n: prob_n(nn, x), tp, 8.0, 1200)
        tunneling_probs[n] = p_forbid
        # Verify Schrodinger equation -0.5 psi'' + 0.5 xi^2 psi = (n + 0.5) psi
        eps = 1e-4
        for x_chk in (-1.3, 0.25, 1.7):
            d2 = (psi_n(n, x_chk + eps) - 2.0 * psi_n(n, x_chk) + psi_n(n, x_chk - eps)) / (eps * eps)
            lhs = -0.5 * d2 + 0.5 * x_chk * x_chk * psi_n(n, x_chk)
            rhs = (n + 0.5) * psi_n(n, x_chk)
            assert abs(lhs - rhs) < 1e-6, f"Schrodinger check failed at n={n}, xi={x_chk}"

    # Verify exact orthogonality between distinct eigenstates
    for m in range(4):
        for n in range(m + 1, 4):
            ov = simpson(lambda x, mm=m, nn=n: psi_n(mm, x) * psi_n(nn, x), -8.0, 8.0, 2000)
            assert abs(ov) < 1e-8, f"Orthogonality failed for ({m},{n}): {ov}"

    # Verify ground-state tunneling equals exact erfc(1) ~ 15.7299%
    assert abs(tunneling_probs[0] - math.erfc(1.0)) < 1e-7
    assert abs(tunneling_probs[1] - 0.111610225) < 1e-5
    assert tunneling_probs[0] > tunneling_probs[1] > tunneling_probs[2] > tunneling_probs[3] > 0.0

    # Amplitude visual scales (strictly non-overlapping across adjacent levels)
    amp_psi = 0.42
    amp_prob = 0.72
    xis_plot = [-4.0 + 8.0 * i / 480.0 for i in range(481)]
    for n in range(3):
        upper_n = max(max((n + 0.5) + amp_psi * psi_n(n, x), (n + 0.5) + amp_prob * prob_n(n, x)) for x in xis_plot)
        lower_np1 = min((n + 1.5) + amp_psi * psi_n(n + 1, x) for x in xis_plot)
        assert upper_n < lower_np1 - 0.2, f"Visual overlap between n={n} and n={n+1}: {upper_n} vs {lower_np1}"

    doc = SvgDoc(
        title="一维量子谐振子抛物势、Hermite–Gaussian 本征态与经典禁区隧穿拖尾",
        desc=(
            "按精确 Hermite–Gaussian 解析公式绘制一维量子谐振子抛物势 V(ξ) = ½ξ²（无量纲坐标 ξ = x/x₀）中"
            "前四个本征态 n = 0, 1, 2, 3 的等间距能级 Eₙ = (n + ½)ℏω、波函数 ψₙ(ξ)（实线）与概率密度 |ψₙ(ξ)|²（淡色填充），"
            "标出零点能 ½ℏω、经典转折点 ξ = ±√(2n+1) 以及转折点外的经典禁区隧穿拖尾（n=0 禁区概率 15.73%）。"
        ),
    )
    doc.add_header(
        "一维量子谐振子：能级梯、精确波函数与经典禁区隧穿拖尾",
        "无量纲坐标 ξ = x/x₀，势能 V(ξ) = ½ξ²（单位 ℏω）；实线示 ψₙ(ξ)，淡色填充示 |ψₙ(ξ)|²，红斜纹示转折点外隧穿区",
    )

    doc.add_panel(28, 94, 692, 456, "抛物势阱与前四个本征态（n = 0, 1, 2, 3，精确公式）")
    doc.add_panel(734, 94, 238, 456, "解析公式与定量对照")

    # --- Main Left Plot ---
    px0, px1 = 98.0, 696.0
    py_top, py_bot = 176.0, 468.0
    xi_min, xi_max = -4.0, 4.0
    e_min_ax, e_max_ax = 0.0, 4.25

    def gx(xi: float) -> float:
        return px0 + ((xi - xi_min) / (xi_max - xi_min)) * (px1 - px0)

    def gy(e_val: float) -> float:
        return py_bot - ((e_val - e_min_ax) / (e_max_ax - e_min_ax)) * (py_bot - py_top)

    # Legend cleanly above plot frame
    doc.add('<line class="c4" stroke-width="2.6" x1="44" y1="152" x2="70" y2="152"/>')
    doc.add('<text class="sm" x="76" y="156">抛物势 V(ξ)=½ξ²</text>')

    doc.add('<line class="c1" stroke-width="2.3" x1="194" y1="152" x2="220" y2="152"/>')
    doc.add('<text class="sm" x="226" y="156">波函数 ψₙ(ξ)</text>')

    doc.add('<rect class="area3" x="320" y="146" width="22" height="12" rx="2"/>')
    doc.add('<rect class="c3" stroke-width="1.1" stroke-dasharray="2 2" x="320" y="146" width="22" height="12" rx="2"/>')
    doc.add('<text class="sm" x="348" y="156">经典区 |ψₙ|²</text>')

    doc.add('<rect class="forbid" x="444" y="146" width="22" height="12" rx="2"/>')
    doc.add('<rect fill="url(#hatch-red)" x="444" y="146" width="22" height="12" rx="2"/>')
    doc.add('<rect class="c2" stroke-width="1.1" x="444" y="146" width="22" height="12" rx="2"/>')
    doc.add('<text class="sm" x="472" y="156">禁区隧穿拖尾</text>')

    doc.add(f'<polygon class="c2-fill" points="{diamond_pts(578, 152, 4.6)}"/>')
    doc.add('<text class="sm" x="588" y="156">经典转折点</text>')

    # Grid & axis ticks
    for xv in [-4, -3, -2, -1, 0, 1, 2, 3, 4]:
        xg = gx(float(xv))
        cls_g = "guide" if xv == 0 else "grid"
        doc.add(f'<line class="{cls_g}" x1="{fmt(xg)}" y1="{fmt(py_top)}" x2="{fmt(xg)}" y2="{fmt(py_bot)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(xg)}" y1="{fmt(py_bot)}" x2="{fmt(xg)}" y2="{fmt(py_bot + 5)}"/>')
        lbl_x = str(xv).replace("-", "−")
        doc.add(f'<text class="sm" x="{fmt(xg)}" y="{fmt(py_bot + 19)}" text-anchor="middle">{lbl_x}</text>')

    for ev, elbl in [(0.0, "0"), (0.5, "0.5"), (1.5, "1.5"), (2.5, "2.5"), (3.5, "3.5"), (4.0, "4.0")]:
        yg = gy(ev)
        doc.add(f'<line class="grid" x1="{fmt(px0)}" y1="{fmt(yg)}" x2="{fmt(px1)}" y2="{fmt(yg)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" x1="{fmt(px0 - 5)}" y1="{fmt(yg)}" x2="{fmt(px0)}" y2="{fmt(yg)}"/>')
        doc.add(f'<text class="sm" x="{fmt(px0 - 9)}" y="{fmt(yg + 4)}" text-anchor="end">{elbl}</text>')

    # Draw probability densities (allowed = soft green fill, forbidden tails = red fill + diagonal hatch)
    # and energy baselines + wavefunctions for n = 0, 1, 2, 3
    for n in range(4):
        en = n + 0.5
        tp = math.sqrt(2.0 * n + 1.0)
        y_base = gy(en)

        # Left forbidden tail: [-4.0, -tp]
        xs_left = [xi_min + (-tp - xi_min) * i / 80.0 for i in range(81)]
        poly_left = [(gx(xi_min), y_base)] + [(gx(x), gy(en + amp_prob * prob_n(n, x))) for x in xs_left] + [(gx(-tp), y_base)]
        doc.add(f'<polygon class="forbid" points="{pts_str(poly_left)}"/>')
        doc.add(f'<polygon fill="url(#hatch-red)" points="{pts_str(poly_left)}"/>')

        # Right forbidden tail: [tp, 4.0]
        xs_right = [tp + (xi_max - tp) * i / 80.0 for i in range(81)]
        poly_right = [(gx(tp), y_base)] + [(gx(x), gy(en + amp_prob * prob_n(n, x))) for x in xs_right] + [(gx(xi_max), y_base)]
        doc.add(f'<polygon class="forbid" points="{pts_str(poly_right)}"/>')
        doc.add(f'<polygon fill="url(#hatch-red)" points="{pts_str(poly_right)}"/>')

        # Classically allowed interior: [-tp, +tp]
        xs_in = [-tp + (2.0 * tp) * i / 160.0 for i in range(161)]
        poly_in = [(gx(-tp), y_base)] + [(gx(x), gy(en + amp_prob * prob_n(n, x))) for x in xs_in] + [(gx(tp), y_base)]
        doc.add(f'<polygon class="area3" points="{pts_str(poly_in)}"/>')

        # Dotted outline of |psi_n|^2 across entire domain (grayscale distinction from solid psi_n)
        prob_pts = [(gx(x), gy(en + amp_prob * prob_n(n, x))) for x in xis_plot]
        doc.add(f'<path class="c3" stroke-width="1.3" stroke-dasharray="3 3" d="{path_from_points(prob_pts)}"/>')

        # Energy level baseline: dashed outside parabola, solid inside
        doc.add(f'<line class="guide" x1="{fmt(px0)}" y1="{fmt(y_base)}" x2="{fmt(gx(-tp))}" y2="{fmt(y_base)}"/>')
        doc.add(f'<line class="guide" x1="{fmt(gx(tp))}" y1="{fmt(y_base)}" x2="{fmt(px1)}" y2="{fmt(y_base)}"/>')
        doc.add(f'<line class="axis" stroke-width="1.2" stroke-opacity="0.7" x1="{fmt(gx(-tp))}" y1="{fmt(y_base)}" x2="{fmt(gx(tp))}" y2="{fmt(y_base)}"/>')

        # Exact Hermite-Gaussian wavefunction psi_n(xi) (solid blue)
        psi_pts = [(gx(x), gy(en + amp_psi * psi_n(n, x))) for x in xis_plot]
        doc.add(f'<path class="c1" stroke-width="2.2" d="{path_from_points(psi_pts)}"/>')

        # Level tag neatly on far-left margin inside plot
        doc.add(f'<text class="smb c1-txt" x="{fmt(px0 + 8)}" y="{fmt(y_base - 6)}">n={n}</text>')

    # Parabolic potential V(xi) = 0.5 * xi^2 clipped smoothly at E = e_max_ax
    xi_parab_max = math.sqrt(2.0 * e_max_ax)
    xs_parab = [-xi_parab_max + (2.0 * xi_parab_max) * i / 200.0 for i in range(201)]
    parab_pts = [(gx(x), gy(0.5 * x * x)) for x in xs_parab]
    doc.add(f'<path class="c4" stroke-width="2.7" d="{path_from_points(parab_pts)}"/>')

    # Classical turning point diamond markers on the parabola intersections
    for n in range(4):
        en = n + 0.5
        tp = math.sqrt(2.0 * n + 1.0)
        doc.add(f'<polygon class="c2-fill" points="{diamond_pts(gx(-tp), gy(en), 4.8)}"/>')
        doc.add(f'<polygon class="c2-fill" points="{diamond_pts(gx(tp), gy(en), 4.8)}"/>')

    # Zero-point energy E0 = 1/2 hbar omega vertical double arrow at xi = 0 + callout in empty E in [0, 0.5) strip
    x_zero = gx(0.0)
    doc.add(f'<line class="c4" stroke-width="2.0" x1="{fmt(x_zero)}" y1="{fmt(gy(0.5) + 6)}" x2="{fmt(x_zero)}" y2="{fmt(gy(0.0) - 6)}"/>')
    doc.add(arrow_head(x_zero, gy(0.5) + 4, 0, -1, 6.2, "c4-fill"))
    doc.add(arrow_head(x_zero, gy(0.0) - 4, 0, 1, 6.2, "c4-fill"))
    doc.add('<rect class="c4-soft" x="506" y="438" width="178" height="24" rx="6"/>')
    doc.add('<text class="smb c4-txt" x="595" y="454" text-anchor="middle">零点能 E₀ = ½ℏω</text>')
    doc.add(f'<line class="c4" stroke-width="1.3" stroke-dasharray="4 3" x1="506" y1="450" x2="{fmt(x_zero + 7)}" y2="450"/>')

    # Turning point callout in empty bottom-left strip E in (0, 0.5) — zero overlap with n=0 label!
    doc.add('<rect class="pill" x="108" y="438" width="186" height="24" rx="6"/>')
    doc.add('<text class="smb" x="201" y="454" text-anchor="middle">经典转折点 ξ = ±√(2n+1)</text>')
    doc.add(f'<line class="c2" stroke-width="1.3" x1="294" y1="448" x2="{fmt(gx(-1.0) - 6)}" y2="{fmt(gy(0.5) + 3)}"/>')
    doc.add(arrow_head(gx(-1.0) - 5, gy(0.5) + 3, 1, -0.5, 6.0, "c2-fill"))

    # Tunneling tail callout in empty lower-right zone (x=544..690, y=378..420)
    doc.add('<rect class="c2-soft" x="544" y="378" width="146" height="42" rx="7"/>')
    doc.add('<text class="smb c2-txt" x="617" y="396" text-anchor="middle">经典禁区隧穿拖尾</text>')
    doc.add('<text class="sm c2-txt" x="617" y="413" text-anchor="middle">|ξ| &gt; √(2n+1)</text>')
    doc.add(f'<line class="c2" stroke-width="1.2" x1="544" y1="406" x2="{fmt(gx(1.38))}" y2="{fmt(gy(0.56))}"/>')
    doc.add(arrow_head(gx(1.36), gy(0.56), -1, 0.35, 6.0, "c2-fill"))
    doc.add(f'<line class="c2" stroke-width="1.2" x1="572" y1="378" x2="{fmt(gx(2.05))}" y2="{fmt(gy(1.56))}"/>')
    doc.add(arrow_head(gx(2.04), gy(1.56), -0.45, -1, 6.0, "c2-fill"))

    # Parabola label near top-right of parabola
    doc.add(f'<text class="smb c4-txt" x="{fmt(gx(2.96) + 6)}" y="{fmt(gy(4.02))}">V(ξ)=½ξ²</text>')

    # Outer frame axes
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px1 + 8)}" y2="{fmt(py_bot)}"/>')
    doc.add(arrow_head(px1 + 10, py_bot, 1, 0, 7.5))
    doc.add(f'<line class="axis" x1="{fmt(px0)}" y1="{fmt(py_bot)}" x2="{fmt(px0)}" y2="{fmt(py_top - 8)}"/>')
    doc.add(arrow_head(px0, py_top - 10, 0, -1, 7.5))
    doc.add(f'<text class="lbl" x="{fmt(0.5*(px0+px1))}" y="504" text-anchor="middle">无量纲位置坐标 ξ = x / x₀（无量纲）</text>')
    doc.add(
        f'<text class="lbl" x="50" y="{fmt(0.5*(py_top+py_bot))}" text-anchor="middle" '
        f'transform="rotate(-90 50 {fmt(0.5*(py_top+py_bot))})">能量 E / (ℏω)（无量纲）</text>'
    )
    doc.add('<rect class="pill" x="44" y="514" width="660" height="24" rx="7"/>')
    doc.add(
        '<text class="sm" x="374" y="530" text-anchor="middle">'
        '各能级间距恒为 ΔE = ℏω；节点数等于量子数 n，宇称按 (−1)ⁿ 交替'
        '</text>'
    )

    # --- Right Sidebar Panel: Exact Formulas & Quantitative Table ---
    doc.add('<rect class="c1-soft" x="746" y="144" width="214" height="94" rx="9"/>')
    doc.add('<text class="smb c1-txt" x="853" y="164" text-anchor="middle">Hermite–Gaussian 本征态</text>')
    doc.add(f'<text class="sm" x="853" y="185" text-anchor="middle">ψₙ(ξ) = (2ⁿn!√π){sup("−½")}·</text>')
    doc.add('<text class="sm" x="853" y="203" text-anchor="middle">Hₙ(ξ)·exp(−ξ²/2)</text>')
    doc.add('<text class="sm" x="853" y="224" text-anchor="middle">特征长度 x₀ = √(ℏ/(mω))</text>')

    # Quantitative table box
    doc.add('<rect class="panel" x="746" y="250" width="214" height="162" rx="9"/>')
    doc.add('<rect class="phead" x="747" y="251" width="212" height="28" rx="7"/>')
    doc.add('<text class="smb" x="762" y="269" text-anchor="middle">n</text>')
    doc.add('<text class="smb" x="802" y="269" text-anchor="middle">Eₙ/ℏω</text>')
    doc.add('<text class="smb" x="856" y="269" text-anchor="middle">转折点</text>')
    doc.add('<text class="smb" x="922" y="269" text-anchor="middle">禁区概率</text>')

    for idx in range(4):
        ry = 304 + idx * 31
        if idx > 0:
            doc.add(f'<line class="grid" x1="752" y1="{ry - 19}" x2="954" y2="{ry - 19}"/>')
        tp = math.sqrt(2.0 * idx + 1.0)
        pct = 100.0 * tunneling_probs[idx]
        doc.add(f'<text class="smb c1-txt" x="762" y="{ry}" text-anchor="middle">{idx}</text>')
        doc.add(f'<text class="sm" x="802" y="{ry}" text-anchor="middle">{idx + 0.5:.1f}</text>')
        doc.add(f'<text class="sm" x="856" y="{ry}" text-anchor="middle">±{tp:.2f}</text>')
        doc.add(f'<text class="smb c2-txt" x="922" y="{ry}" text-anchor="middle">{pct:.2f}%</text>')

    # Scale note & classical correspondence box
    doc.add('<rect class="note" x="746" y="424" width="214" height="114" rx="9"/>')
    doc.add('<text class="smb" x="853" y="444" text-anchor="middle">物理要点与叠加标度</text>')
    doc.add('<text class="sm" x="756" y="465">• ψₙ 纵向按 0.42·ℏω 叠加</text>')
    doc.add('<text class="sm" x="756" y="484">• |ψₙ|² 按 0.72·ℏω 填充</text>')
    doc.add('<text class="sm" x="756" y="503">• n=0 禁区概率 erfc(1)≈15.73%</text>')
    doc.add('<text class="sm" x="756" y="522">• n 增大，主峰向转折点聚集</text>')

    return doc.render(), {
        "p_forbid_n0_pct": round(100.0 * tunneling_probs[0], 4),
        "p_forbid_n1_pct": round(100.0 * tunneling_probs[1], 4),
        "p_forbid_n2_pct": round(100.0 * tunneling_probs[2], 4),
        "p_forbid_n3_pct": round(100.0 * tunneling_probs[3], 4),
    }


# ---------------------------------------------------------------------------
# XML well-formedness, margin & optional Chromium getBBox() verification
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


def verify_with_chromium_bbox(
    svg_paths: list[Path],
    screenshot_dir: Path | None = None,
) -> None:
    """Audit rendered <text> bounding boxes in headless Chromium via getBBox() / getBoundingClientRect()."""
    from playwright.sync_api import sync_playwright

    js_audit = """(margin) => {
      const svg = document.querySelector('svg');
      const svgRect = svg.getBoundingClientRect();
      const vb = svg.viewBox.baseVal;
      const sx = vb.width / svgRect.width;
      const sy = vb.height / svgRect.height;
      const texts = Array.from(svg.querySelectorAll('text'));
      const boxes = texts.map((el, idx) => {
        const r = el.getBoundingClientRect();
        const x1 = (r.left - svgRect.left) * sx;
        const y1 = (r.top - svgRect.top) * sy;
        const x2 = (r.right - svgRect.left) * sx;
        const y2 = (r.bottom - svgRect.top) * sy;
        const bb = el.getBBox();
        return {
          idx,
          text: (el.textContent || '').trim(),
          x1, y1, x2, y2,
          bbox: { x: bb.x, y: bb.y, w: bb.width, h: bb.height },
          rotated: (el.getAttribute('transform') || '').includes('rotate')
        };
      });
      const oob = [];
      for (const b of boxes) {
        if (b.x1 < margin - 0.5 || b.y1 < margin - 0.5 || b.x2 > vb.width - margin + 0.5 || b.y2 > vb.height - margin + 0.5) {
          oob.push(b);
        }
      }
      const overlaps = [];
      for (let i = 0; i < boxes.length; i++) {
        for (let j = i + 1; j < boxes.length; j++) {
          const a = boxes[i], b = boxes[j];
          const ox = Math.min(a.x2, b.x2) - Math.max(a.x1, b.x1);
          const oy = Math.min(a.y2, b.y2) - Math.max(a.y1, b.y1);
          if (ox > 1.0 && oy > 1.0) {
            overlaps.push({ a: a.text, b: b.text, ox: Number(ox.toFixed(2)), oy: Number(oy.toFixed(2)) });
          }
        }
      }
      return {
        count: boxes.length,
        min_x: Math.min(...boxes.map(b => b.x1)),
        min_y: Math.min(...boxes.map(b => b.y1)),
        max_x: Math.max(...boxes.map(b => b.x2)),
        max_y: Math.max(...boxes.map(b => b.y2)),
        oob,
        overlaps
      };
    }"""

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": W, "height": H})
            for svg_path in svg_paths:
                svg_content = svg_path.read_text(encoding="utf-8")
                html = (
                    "<!doctype html><html><head><meta charset='utf-8'>"
                    "<style>html,body{margin:0;padding:0;background:transparent;}svg{display:block;width:1000px;height:580px;}</style>"
                    f"</head><body>{svg_content}</body></html>"
                )
                page.emulate_media(color_scheme="light")
                page.set_content(html, wait_until="load")
                res = page.evaluate(js_audit, MARGIN)
                print(
                    f"[BBOX] {svg_path.name}: {res['count']} texts | "
                    f"span x=[{res['min_x']:.1f}, {res['max_x']:.1f}], y=[{res['min_y']:.1f}, {res['max_y']:.1f}] | "
                    f"oob={len(res['oob'])}, overlaps={len(res['overlaps'])}"
                )
                if res["oob"]:
                    for item in res["oob"]:
                        print(f"  [OOB] {item['text']!r}: ({item['x1']:.1f},{item['y1']:.1f})..({item['x2']:.1f},{item['y2']:.1f})")
                if res["overlaps"]:
                    for item in res["overlaps"]:
                        print(f"  [OVERLAP] {item['a']!r} <-> {item['b']!r} (ox={item['ox']}, oy={item['oy']})")

                if screenshot_dir is not None:
                    screenshot_dir.mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(screenshot_dir / f"{svg_path.stem}-light.png"))
                    page.emulate_media(color_scheme="dark")
                    page.screenshot(path=str(screenshot_dir / f"{svg_path.stem}-dark.png"))

                assert not res["oob"], f"{svg_path.name}: {len(res['oob'])} text out-of-bounds violations"
                assert not res["overlaps"], f"{svg_path.name}: {len(res['overlaps'])} text-overlap violations"
        finally:
            browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate 4 adaptive scientific SVG figures (part 2b).")
    parser.add_argument("--check-bbox", action="store_true", help="Run headless Chromium getBBox() audit.")
    parser.add_argument("--screenshots", type=Path, default=None, help="Directory to save light/dark PNG previews.")
    args = parser.parse_args()

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    builders = [
        ("v2-16-qsvt-unification.svg", build_fig1_qsvt_unification),
        ("v2-17-mbqc-aqc.svg", build_fig2_mbqc_aqc),
        ("v2-18-cv-phase-space.svg", build_fig3_cv_phase_space),
        ("v2-q4-qho-wavefunctions.svg", build_fig4_qho_wavefunctions),
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
