#!/usr/bin/env python3
"""Generate 7 light/dark-adaptive V4 scientific SVG figures (Part 1: Ch01/03/04/06/07/08/10)
using Python 3 standard library only.

Outputs to handbook/assets/:
  1. v4-01-tensor-partial-trace.svg     (Ch01: Tensor product block stamp vs partial trace Tr_A/Tr_B)
  2. v4-03-schmidt-entanglement-tree.svg (Ch03: 2-qubit Schmidt values & S(rho_A) + mixed-state decision tree)
  3. v4-04-toffoli-superdense.svg       (Ch04: Toffoli 6-CNOT/7-T circuit + superdense/teleportation duality)
  4. v4-06-aa-prepare-select.svg        (Ch06: Amplitude amplification +2*theta geometry + 6-gate LCU block encoding)
  5. v4-07-simon-trotter.svg            (Ch07: Simon XOR cosets s=101 + 1st vs 2nd order Trotter log-log error)
  6. v4-08-chem-encoding-thc.svg        (Ch08: JW O(N) vs BK O(log N) weight + DF/THC Toffoli compression)
  7. v4-10-color-xzzx-codes.svg         (Ch10: d=3 Steane & d=5 color codes + XZZX 1D diagonal repetition chains)

Run (pure Python 3 standard library):
  python3 codes/foundations/generate_v4_figures_part1.py

Optional System Chrome Playwright dual-theme getBBox() audit & PNG screenshots:
  python3 codes/foundations/generate_v4_figures_part1.py --check-bbox --screenshots /tmp/v4_part1_previews
"""

from __future__ import annotations

import argparse
import cmath
import math
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT / "handbook" / "assets"
W, H = 960, 460
MARGIN = 14
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


COMMON_CSS = """
:root{color-scheme:light dark}
text{font-family:system-ui,-apple-system,'PingFang SC','Microsoft YaHei',sans-serif}
.bg{fill:#FAF8F3}
.panel{fill:#ffffff;stroke:#d4cfc3;stroke-width:1.35}
.subpanel{fill:#f5f2ea;stroke:#d8d3c6;stroke-width:1.15}
.phead{fill:#edf3ef}
.title{font-size:18.5px;font-weight:700;fill:#14453d}
.subtitle{font-size:12.5px;font-weight:400;fill:#4a5f59}
.sec{font-size:13.8px;font-weight:700;fill:#14453d}
.lbl{font-size:12.5px;font-weight:500;fill:#1f3832}
.lblb{font-size:12.5px;font-weight:700;fill:#122b25}
.sm{font-size:12px;font-weight:400;fill:#435852}
.smb{font-size:12px;font-weight:600;fill:#1b332d}
.xs{font-size:11.5px;font-weight:500;fill:#485e58}
.xsb{font-size:11.5px;font-weight:700;fill:#19312b}
.math-txt{font-family:Georgia,'Times New Roman',serif;font-size:13px;font-weight:700;fill:#122b25}
.gate-txt{font-family:Georgia,'Times New Roman',serif;font-size:12.5px;font-weight:700;fill:#122b25}
.axis{stroke:#243d37;stroke-width:1.6;fill:none}
.axis-fill{fill:#243d37}
.wire{stroke:#243d37;stroke-width:1.8;fill:none}
.cwire{stroke:#5a706a;stroke-width:1.35;fill:none}
.ctrl{fill:#14453d}
.targ{fill:#ffffff;stroke:#14453d;stroke-width:1.9}
.grid{stroke:#e3ded2;stroke-width:1;fill:none}
.guide{stroke:#7e928c;stroke-width:1.2;stroke-dasharray:5 4;fill:none}
.unit-circle{stroke:#687f78;stroke-width:1.5;stroke-dasharray:5 4;fill:none}
.c1{stroke:#1f5a92;fill:none}
.c1-fill{fill:#1f5a92}
.c1-txt{fill:#174775}
.c1-soft{fill:#e6f0fa;stroke:#1f5a92;stroke-width:1.4}
.c2{stroke:#b3542d;fill:none}
.c2-fill{fill:#b3542d}
.c2-txt{fill:#96411e}
.c2-soft{fill:#fbeae3;stroke:#b3542d;stroke-width:1.4}
.c3{stroke:#14453d;fill:none}
.c3-fill{fill:#14453d}
.c3-txt{fill:#14453d}
.c3-soft{fill:#e3f2ec;stroke:#14453d;stroke-width:1.4}
.c4{stroke:#b07016;fill:none}
.c4-fill{fill:#b07016}
.c4-txt{fill:#8a550c}
.c4-soft{fill:#fcf2db;stroke:#b07016;stroke-width:1.4}
.c5{stroke:#644696;fill:none}
.c5-fill{fill:#644696}
.c5-txt{fill:#4e347a}
.c5-soft{fill:#f0eaf9;stroke:#644696;stroke-width:1.4}
.note{fill:#fdf6e6;stroke:#c89232;stroke-width:1.25}
.pill{fill:#f4f0e6;stroke:#b7b0a2;stroke-width:1.15}
.pill-bg{fill:#FAF8F3;fill-opacity:.95;stroke:#b7b0a2;stroke-width:1.1}
.area1{fill:#1f5a92;fill-opacity:.13}
.area2{fill:#b3542d;fill-opacity:.14}
.area3{fill:#14453d;fill-opacity:.13}
.badge-txt{fill:#ffffff;font-size:11.5px;font-weight:700}
.cc-r{fill:#b3542d;fill-opacity:.23;stroke:#b3542d;stroke-width:1.5}
.cc-g{fill:#1c7a5e;fill-opacity:.22;stroke:#14453d;stroke-width:1.5}
.cc-b{fill:#1f5a92;fill-opacity:.22;stroke:#1f5a92;stroke-width:1.5}
.qnode{fill:#ffffff;stroke:#14453d;stroke-width:1.6}
.qnode-err{fill:#b3542d;stroke:#ffffff;stroke-width:1.8}
.qnode-hi{fill:#14453d;stroke:#ffffff;stroke-width:1.6}
@media (prefers-color-scheme: dark) {
  .bg{fill:#111917}
  .panel{fill:#182420;stroke:#2f443d}
  .subpanel{fill:#1d2b26;stroke:#354d45}
  .phead{fill:#1c2b26}
  .title,.sec,.lblb,.math-txt,.gate-txt{fill:#edf6f2}
  .subtitle,.sm,.xs{fill:#a4bdb5}
  .lbl,.smb,.xsb{fill:#d9ebe5}
  .axis,.wire{stroke:#cde2db}
  .axis-fill,.ctrl{fill:#d9ebe5}
  .cwire{stroke:#8ea9a0}
  .targ{fill:#182420;stroke:#d9ebe5}
  .grid{stroke:#283b35}
  .guide,.unit-circle{stroke:#708c83}
  .c1{stroke:#74bdf5}
  .c1-fill{fill:#74bdf5}
  .c1-txt{fill:#96d0fa}
  .c1-soft{fill:#17354d;stroke:#74bdf5}
  .c2{stroke:#eb8863}
  .c2-fill{fill:#eb8863}
  .c2-txt{fill:#f5a789}
  .c2-soft{fill:#47251a;stroke:#eb8863}
  .c3{stroke:#5ed1ad}
  .c3-fill{fill:#5ed1ad}
  .c3-txt{fill:#84e3c5}
  .c3-soft{fill:#163b31;stroke:#5ed1ad}
  .c4{stroke:#f0bf5e}
  .c4-fill{fill:#f0bf5e}
  .c4-txt{fill:#f5cf84}
  .c4-soft{fill:#3b2e14;stroke:#f0bf5e}
  .c5{stroke:#b89ef2}
  .c5-fill{fill:#b89ef2}
  .c5-txt{fill:#cebbf7}
  .c5-soft{fill:#2c2145;stroke:#b89ef2}
  .note{fill:#2e2514;stroke:#d19c3d}
  .pill{fill:#1f2e29;stroke:#476158}
  .pill-bg{fill:#182420;fill-opacity:.95;stroke:#476158}
  .area1{fill:#74bdf5;fill-opacity:.18}
  .area2{fill:#eb8863;fill-opacity:.19}
  .area3{fill:#5ed1ad;fill-opacity:.17}
  .badge-txt{fill:#111917}
  .cc-r{fill:#eb8863;fill-opacity:.28;stroke:#eb8863}
  .cc-g{fill:#5ed1ad;fill-opacity:.25;stroke:#5ed1ad}
  .cc-b{fill:#74bdf5;fill-opacity:.26;stroke:#74bdf5}
  .qnode{fill:#182420;stroke:#d9ebe5}
  .qnode-err{fill:#eb8863;stroke:#111917}
  .qnode-hi{fill:#5ed1ad;stroke:#111917}
}
""".strip()


def svg_doc(title: str, desc: str, body: list[str], extra_defs: str = "") -> str:
    defs_block = f"  <defs>\n{extra_defs}\n  </defs>\n" if extra_defs else ""
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f"  <title id=\"title\">{escape(title)}</title>",
        f"  <desc id=\"desc\">{escape(desc)}</desc>",
        "  <style>",
        COMMON_CSS,
        "  </style>",
    ]
    if defs_block:
        parts.append(defs_block.rstrip("\n"))
    parts.append(f'  <rect class="bg" width="{W}" height="{H}" rx="16"/>')
    parts.extend(f"  {line}" for line in body)
    parts.append("</svg>\n")
    return "\n".join(parts)


def header(title: str, subtitle: str) -> list[str]:
    return [
        f'<text class="title" x="22" y="34">{escape(title)}</text>',
        f'<text class="subtitle" x="22" y="54">{escape(subtitle)}</text>',
    ]


def panel_shell(x: float, y: float, w: float, h: float, title: str, r: float = 12) -> list[str]:
    hx2 = x + w - 1
    hy_bot = y + 31
    return [
        f'<rect class="panel" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}"/>',
        (
            f'<path class="phead" d="M {x+r:.1f} {y+1:.1f} H {x+w-r:.1f} '
            f'Q {hx2:.1f} {y+1:.1f} {hx2:.1f} {y+r:.1f} V {hy_bot:.1f} '
            f'H {x+1:.1f} V {y+r:.1f} Q {x+1:.1f} {y+1:.1f} {x+r:.1f} {y+1:.1f} Z"/>'
        ),
        f'<line class="grid" x1="{x+1:.1f}" y1="{hy_bot:.1f}" x2="{hx2:.1f}" y2="{hy_bot:.1f}"/>',
        f'<text class="sec" x="{x+13:.1f}" y="{y+21.5:.1f}">{escape(title)}</text>',
    ]


def note_bar(x: float, y: float, w: float, text: str, h: float = 30) -> list[str]:
    return [
        f'<rect class="note" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="8"/>',
        f'<text class="xsb" x="{x+w/2:.1f}" y="{y+h/2+4.2:.1f}" text-anchor="middle">{escape(text)}</text>',
    ]


def arrow_head(x1: float, y1: float, x2: float, y2: float, fill_cls: str = "axis-fill", length: float = 8.0, half_w: float = 3.8) -> str:
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy)
    assert norm > 1e-9, "Zero-length arrow"
    ux, uy = dx / norm, dy / norm
    px, py = -uy, ux
    bx, by = x2 - length * ux, y2 - length * uy
    p1x, p1y = bx + half_w * px, by + half_w * py
    p2x, p2y = bx - half_w * px, by - half_w * py
    return f'<polygon class="{fill_cls}" points="{x2:.2f},{y2:.2f} {p1x:.2f},{p1y:.2f} {p2x:.2f},{p2y:.2f}"/>'


def arrow_line(
    x1: float, y1: float, x2: float, y2: float,
    stroke_cls: str = "axis", fill_cls: str = "axis-fill",
    sw: float = 1.7, dash: str = "", length: float = 8.0, half_w: float = 3.6
) -> list[str]:
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy)
    ux, uy = dx / norm, dy / norm
    ex, ey = x2 - (length * 0.55) * ux, y2 - (length * 0.55) * uy
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return [
        f'<line class="{stroke_cls}" stroke-width="{sw:.2f}"{da} x1="{x1:.2f}" y1="{y1:.2f}" x2="{ex:.2f}" y2="{ey:.2f}"/>',
        arrow_head(x1, y1, x2, y2, fill_cls=fill_cls, length=length, half_w=half_w),
    ]


def gate_box(cx: float, cy: float, label: str, box_cls: str = "c3-soft", txt_cls: str = "gate-txt", w: float = 28, h: float = 26) -> list[str]:
    return [
        f'<rect class="{box_cls}" x="{cx-w/2:.1f}" y="{cy-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="5"/>',
        f'<text class="{txt_cls}" x="{cx:.1f}" y="{cy+4.5:.1f}" text-anchor="middle">{escape(label)}</text>',
    ]


def cnot_elem(x: float, yc: float, yt: float, r_ctrl: float = 4.2, r_targ: float = 9.0, stroke_cls: str = "wire") -> list[str]:
    y_edge = yt - r_targ if yt > yc else yt + r_targ
    return [
        f'<line class="{stroke_cls}" x1="{x:.1f}" y1="{yc:.1f}" x2="{x:.1f}" y2="{y_edge:.1f}"/>',
        f'<circle class="ctrl" cx="{x:.1f}" cy="{yc:.1f}" r="{r_ctrl:.1f}"/>',
        f'<circle class="targ" cx="{x:.1f}" cy="{yt:.1f}" r="{r_targ:.1f}"/>',
        f'<line class="{stroke_cls}" x1="{x-r_targ+2:.1f}" y1="{yt:.1f}" x2="{x+r_targ-2:.1f}" y2="{yt:.1f}"/>',
        f'<line class="{stroke_cls}" x1="{x:.1f}" y1="{yt-r_targ+2:.1f}" x2="{x:.1f}" y2="{yt+r_targ-2:.1f}"/>',
    ]


def cz_elem(x: float, y1: float, y2: float, r_ctrl: float = 4.4, stroke_cls: str = "wire") -> list[str]:
    return [
        f'<line class="{stroke_cls}" x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2:.1f}"/>',
        f'<circle class="ctrl" cx="{x:.1f}" cy="{y1:.1f}" r="{r_ctrl:.1f}"/>',
        f'<circle class="ctrl" cx="{x:.1f}" cy="{y2:.1f}" r="{r_ctrl:.1f}"/>',
    ]


def meter_box(cx: float, cy: float, w: float = 26, h: float = 24) -> list[str]:
    x0, y0 = cx - w / 2, cy - h / 2
    return [
        f'<rect class="pill" x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" rx="4"/>',
        f'<path class="axis" stroke-width="1.3" d="M {cx-7.5:.1f} {cy+4.5:.1f} A 7.5 7.5 0 0 1 {cx+7.5:.1f} {cy+4.5:.1f}"/>',
        f'<line class="c2" stroke-width="1.5" x1="{cx:.1f}" y1="{cy+5:.1f}" x2="{cx+5.5:.1f}" y2="{cy-5.5:.1f}"/>',
    ]


def poly_d(pts: list[tuple[float, float]]) -> str:
    return " ".join(f'{"M" if i == 0 else "L"} {x:.2f} {y:.2f}' for i, (x, y) in enumerate(pts))


# =============================================================================
# Figure 1: v4-01-tensor-partial-trace.svg
# =============================================================================
def build_fig1_tensor_partial_trace() -> tuple[str, dict[str, object]]:
    # Exact algebraic verification for product state and Bell state |Phi+>
    rho_a = [[0.7, 0.0], [0.0, 0.3]]
    rho_b = [[0.5, 0.5], [0.5, 0.5]]
    prod = [[0.0] * 4 for _ in range(4)]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    prod[2 * i + k][2 * j + l] = rho_a[i][j] * rho_b[k][l]

    def tr_b(m: list[list[float]]) -> list[list[float]]:
        return [
            [m[2 * i][2 * j] + m[2 * i + 1][2 * j + 1] for j in range(2)]
            for i in range(2)
        ]

    def tr_a(m: list[list[float]]) -> list[list[float]]:
        return [
            [m[k][l] + m[2 + k][2 + l] for l in range(2)]
            for k in range(2)
        ]

    assert abs(sum(prod[i][i] for i in range(4)) - 1.0) < 1e-12
    assert all(abs(tr_b(prod)[i][j] - rho_a[i][j]) < 1e-12 for i in range(2) for j in range(2))
    assert all(abs(tr_a(prod)[i][j] - rho_b[i][j]) < 1e-12 for i in range(2) for j in range(2))

    rho_bell = [
        [0.5, 0.0, 0.0, 0.5],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.5, 0.0, 0.0, 0.5],
    ]
    bell_a = tr_b(rho_bell)
    bell_b = tr_a(rho_bell)
    half_i = [[0.5, 0.0], [0.0, 0.5]]
    assert all(abs(bell_a[i][j] - half_i[i][j]) < 1e-12 for i in range(2) for j in range(2))
    assert all(abs(bell_b[i][j] - half_i[i][j]) < 1e-12 for i in range(2) for j in range(2))

    el: list[str] = []
    el.extend(
        header(
            "张量积升维与偏迹降维的互逆结构",
            "左：印章分块法则将 2×2 矩阵张成 4×4 块矩阵；右：偏迹 Tr_B（逐块取迹）与 Tr_A（主对角块相加）压回 2×2 约化态",
        )
    )

    # Left panel: Tensor product lift (x=20..472, w=452)
    el.extend(panel_shell(20, 68, 452, 376, "1. 张量积升维（印章分块：2×2 ⊗ 2×2 → 4×4）"))

    # Matrix A (2x2)
    el.append('<text class="smb" x="77" y="124" text-anchor="middle">子系统 A (2×2)</text>')
    a_cells = [
        (36, 134, "c3-soft", "c3-txt", "a₀₀"),
        (77, 134, "c1-soft", "c1-txt", "a₀₁"),
        (36, 174, "c4-soft", "c4-txt", "a₁₀"),
        (77, 174, "c2-soft", "c2-txt", "a₁₁"),
    ]
    for cx, cy, bcls, tcls, txt in a_cells:
        el.append(f'<rect class="{bcls}" x="{cx}" y="{cy}" width="40" height="39" rx="4"/>')
        el.append(f'<text class="math-txt {tcls}" x="{cx+20}" y="{cy+24}" text-anchor="middle">{txt}</text>')

    el.append('<text class="title" x="132" y="180" text-anchor="middle">⊗</text>')

    # Matrix B (2x2 stamp)
    el.append('<text class="smb" x="186" y="124" text-anchor="middle">印章 B (2×2)</text>')
    b_vals = [("b₀₀", 148, 134), ("b₀₁", 186, 134), ("b₁₀", 148, 174), ("b₁₁", 186, 174)]
    for txt, cx, cy in b_vals:
        el.append(f'<rect class="pill" x="{cx}" y="{cy}" width="37" height="39" rx="4"/>')
        el.append(f'<text class="sm" x="{cx+18.5}" y="{cy+24}" text-anchor="middle">{txt}</text>')

    # Lift arrow
    el.append('<text class="xsb c3-txt" x="250" y="164" text-anchor="middle">升维</text>')
    el.extend(arrow_line(231, 174, 270, 174, stroke_cls="c3", fill_cls="c3-fill", sw=2.0))

    # 4x4 block matrix A \otimes B at x=278..458, y=134..286 (4 cols of 45px, 4 rows of 38px)
    col_lbls = ["|00⟩", "|01⟩", "|10⟩", "|11⟩"]
    for idx, cl in enumerate(col_lbls):
        el.append(f'<text class="xs" x="{278 + idx*45 + 22.5:.1f}" y="124" text-anchor="middle">{cl}</text>')

    blocks = [
        (278, 134, "c3-soft", "c3-txt", "M₀₀ = a₀₀·B", "2×2 子块"),
        (368, 134, "c1-soft", "c1-txt", "M₀₁ = a₀₁·B", "2×2 子块"),
        (278, 210, "c4-soft", "c4-txt", "M₁₀ = a₁₀·B", "2×2 子块"),
        (368, 210, "c2-soft", "c2-txt", "M₁₁ = a₁₁·B", "2×2 子块"),
    ]
    for bx, by, bcls, tcls, line1, line2 in blocks:
        el.append(f'<rect class="{bcls}" x="{bx}" y="{by}" width="89" height="75" rx="5"/>')
        el.append(f'<line class="grid" stroke-dasharray="3 3" x1="{bx+44.5:.1f}" y1="{by+2}" x2="{bx+44.5:.1f}" y2="{by+73}"/>')
        el.append(f'<line class="grid" stroke-dasharray="3 3" x1="{bx+2}" y1="{by+37.5:.1f}" x2="{bx+87}" y2="{by+37.5:.1f}"/>')
        el.append(f'<rect class="pill-bg" x="{bx+7}" y="{by+15}" width="75" height="44" rx="6"/>')
        el.append(f'<text class="xsb {tcls}" x="{bx+44.5:.1f}" y="{by+34}" text-anchor="middle">{line1}</text>')
        el.append(f'<text class="xs" x="{bx+44.5:.1f}" y="{by+51}" text-anchor="middle">{line2}</text>')

    # Outer frame & quadrant cross for 4x4 matrix
    el.append('<rect class="axis" stroke-width="1.6" x="278" y="134" width="179" height="151" rx="5"/>')
    el.append('<line class="axis" stroke-width="1.5" x1="367.5" y1="134" x2="367.5" y2="285"/>')
    el.append('<line class="axis" stroke-width="1.5" x1="278" y1="209.5" x2="457" y2="209.5"/>')

    # Small left note under A \otimes B explaining Kronecker rule
    el.append('<rect class="subpanel" x="34" y="226" width="228" height="59" rx="8"/>')
    el.append('<text class="xsb c3-txt" x="45" y="245">印章法则（Kronecker 积）</text>')
    el.append('<text class="xs" x="45" y="263">把 A 的每个元素 aᵢⱼ 当缩放系数，</text>')
    el.append('<text class="xs" x="45" y="279">整块盖上印章 B，生成 4×4 矩阵。</text>')

    # Lower concrete numeric check card
    el.append('<rect class="subpanel" x="34" y="298" width="424" height="96" rx="9"/>')
    el.append('<text class="smb c3-txt" x="46" y="318">数值回验：ρ_A = diag(0.7, 0.3)，ρ_B = |+⟩⟨+| = ½[1,1; 1,1]</text>')
    el.append('<text class="sm" x="46" y="340">M₀₀ = 0.35·[1,1; 1,1]，M₀₁ = M₁₀ = 0，M₁₁ = 0.15·[1,1; 1,1]</text>')
    el.append('<text class="sm" x="46" y="361">迹守恒：Tr(ρ_A ⊗ ρ_B) = Tr(M₀₀) + Tr(M₁₁) = 0.70 + 0.30 = 1</text>')
    el.append('<text class="xs c1-txt" x="46" y="383">混合乘积律：(U⊗V)(ρ_A⊗ρ_B)(U†⊗V†) = (Uρ_A U†) ⊗ (Vρ_B V†)</text>')

    el.extend(note_bar(34, 404, 424, "大端序 |q_A q_B⟩：外层按 A 分块、内层按 B 展开；维度相乘 2×2 → 4×4"))

    # Right panel: Partial trace reduction (x=488..940, w=452)
    el.extend(panel_shell(488, 68, 452, 376, "2. 偏迹降维（4×4 → 2×2）：逐块取迹与对角块相加"))

    el.append('<text class="smb" x="502" y="121">Bell 态 ρ_Φ⁺ = |Φ⁺⟩⟨Φ⁺|（整体纯态，Tr(ρ²)=1）</text>')

    # 4x4 grid for Bell state at x=504..672, y=132..244 (42x28 cells)
    gx, gy, cw, ch = 504, 132, 42, 28
    q_cls = [["c3-soft", "c1-soft"], ["c4-soft", "c2-soft"]]
    for br in range(2):
        for bc in range(2):
            el.append(
                f'<rect class="{q_cls[br][bc]}" x="{gx + bc*2*cw}" y="{gy + br*2*ch}" '
                f'width="{2*cw}" height="{2*ch}" rx="3"/>'
            )
    bell_str = [
        ["1/2", "0", "0", "1/2"],
        ["0", "0", "0", "0"],
        ["0", "0", "0", "0"],
        ["1/2", "0", "0", "1/2"],
    ]
    for r in range(4):
        for c in range(4):
            cx = gx + c * cw
            cy = gy + r * ch
            el.append(f'<rect class="grid" x="{cx}" y="{cy}" width="{cw}" height="{ch}"/>')
            val = bell_str[r][c]
            tcls = "xsb c2-txt" if val == "1/2" else "xs"
            el.append(f'<text class="{tcls}" x="{cx+cw/2:.1f}" y="{cy+ch/2+4.2:.1f}" text-anchor="middle">{val}</text>')
    el.append(f'<rect class="axis" stroke-width="1.6" x="{gx}" y="{gy}" width="{4*cw}" height="{4*ch}" rx="3"/>')
    el.append(f'<line class="axis" stroke-width="1.6" x1="{gx+2*cw}" y1="{gy}" x2="{gx+2*cw}" y2="{gy+4*ch}"/>')
    el.append(f'<line class="axis" stroke-width="1.6" x1="{gx}" y1="{gy+2*ch}" x2="{gx+4*cw}" y2="{gy+2*ch}"/>')

    # Right summary card beside Bell matrix
    el.append('<rect class="subpanel" x="688" y="132" width="238" height="112" rx="8"/>')
    el.append('<text class="xsb" x="700" y="151">四个 2×2 子块（读出偏迹的钥匙）</text>')
    el.append('<text class="xs c3-txt" x="700" y="172">M₀₀ = ½[1,0; 0,0]   → Tr(M₀₀) = 1/2</text>')
    el.append('<text class="xs c1-txt" x="700" y="191">M₀₁ = ½[0,1; 0,0]   → Tr(M₀₁) = 0</text>')
    el.append('<text class="xs c4-txt" x="700" y="210">M₁₀ = ½[0,0; 1,0]   → Tr(M₁₀) = 0</text>')
    el.append('<text class="xs c2-txt" x="700" y="229">M₁₁ = ½[0,0; 0,1]   → Tr(M₁₁) = 1/2</text>')

    # Branching arrows to Tr_B and Tr_A cards
    el.extend(arrow_line(605, 246, 605, 267, stroke_cls="c3", fill_cls="c3-fill", sw=1.9))
    el.extend(arrow_line(823, 246, 823, 267, stroke_cls="c1", fill_cls="c1-fill", sw=1.9))

    # Tr_B card (x=502..708, w=206, y=270..394, h=124)
    el.append('<rect class="c3-soft" x="502" y="270" width="206" height="124" rx="9"/>')
    el.append('<text class="smb c3-txt" x="605" y="290" text-anchor="middle">Tr_B(M)：丢弃 B，保留 A</text>')
    el.append('<text class="xsb" x="514" y="311">法则：对每个子块 Mᵢⱼ 求迹</text>')
    el.append('<text class="xs" x="514" y="330">ρ_A = [Tr(M₀₀)  Tr(M₀₁)]</text>')
    el.append('<text class="xs" x="514" y="347">      [Tr(M₁₀)  Tr(M₁₁)]</text>')
    el.append('<text class="xsb c2-txt" x="514" y="368">Bell 态 → diag(½, ½) = I/2</text>')
    el.append('<text class="xs" x="514" y="386">乘积态 A⊗B → A·Tr(B) = A</text>')

    # Tr_A card (x=720..926, w=206, y=270..394, h=124)
    el.append('<rect class="c1-soft" x="720" y="270" width="206" height="124" rx="9"/>')
    el.append('<text class="smb c1-txt" x="823" y="290" text-anchor="middle">Tr_A(M)：丢弃 A，保留 B</text>')
    el.append('<text class="xsb" x="732" y="311">法则：主对角两子块相加</text>')
    el.append('<text class="xs" x="732" y="330">ρ_B = M₀₀ + M₁₁</text>')
    el.append('<text class="xs" x="732" y="347">（非对角块 M₀₁, M₁₀ 不入和）</text>')
    el.append('<text class="xsb c2-txt" x="732" y="368">Bell 态 → diag(½, ½) = I/2</text>')
    el.append('<text class="xs" x="732" y="386">乘积态 A⊗B → Tr(A)·B = B</text>')

    el.extend(note_bar(502, 404, 424, "仅乘积态可无损还原 ρ_A⊗ρ_B；纠缠态偏迹丢弃关联相干，单端成混态 I/2"))

    svg = svg_doc(
        "张量积升维与偏迹降维的互逆结构",
        "左面板展示 2×2 矩阵 A 与印章 B 通过张量积生成 4×4 块矩阵的升维过程及数值验算；右面板以 Bell 态密度矩阵为例，展示偏迹 Tr_B（逐块取迹）与 Tr_A（主对角块相加）将 4×4 压回 2×2 约化密度矩阵 I/2 的降维结构。",
        el,
    )
    return svg, {"trace_prod": 1.0, "bell_tr_a": bell_a[0][0], "bell_tr_b": bell_b[0][0]}


# =============================================================================
# Figure 2: v4-03-schmidt-entanglement-tree.svg
# =============================================================================
def build_fig2_schmidt_entanglement_tree() -> tuple[str, dict[str, object]]:
    def binary_entropy(p: float) -> float:
        if p <= 1e-15 or p >= 1.0 - 1e-15:
            return 0.0
        return -(p * math.log2(p) + (1.0 - p) * math.log2(1.0 - p))

    # Verify key exact values
    assert abs(binary_entropy(0.5) - 1.0) < 1e-12
    assert abs(binary_entropy(0.0)) < 1e-12
    p_pi8 = math.cos(math.pi / 8.0) ** 2
    s_pi8 = binary_entropy(p_pi8)
    assert abs(s_pi8 - 0.6008760368112) < 1e-8

    el: list[str] = []
    el.extend(
        header(
            "双比特 Schmidt 分解曲线与混态纠缠判据决策树",
            "左：纯态 |ψ(θ)⟩ = cosθ|00⟩ + sinθ|11⟩ 的奇异值 (λ₀, λ₁) 与纠缠熵 S(ρ_A)；右：纯态与混态纠缠分层判据",
        )
    )

    # Left panel (x=20..464, w=444)
    el.extend(panel_shell(20, 68, 444, 376, "1. 双比特 Schmidt 奇异值与纠缠熵 S(ρ_A)"))

    # Legend above plot (y=114..128)
    el.append('<line class="c2" stroke-width="2.6" x1="74" y1="118" x2="96" y2="118"/>')
    el.append('<text class="xsb c2-txt" x="102" y="122">S(ρ_A) 纠缠熵</text>')
    el.append('<line class="c3" stroke-width="2.2" x1="202" y1="118" x2="224" y2="118"/>')
    el.append('<text class="xsb c3-txt" x="230" y="122">λ₀ = cosθ</text>')
    el.append('<line class="c1" stroke-width="2.2" stroke-dasharray="6 4" x1="316" y1="118" x2="338" y2="118"/>')
    el.append('<text class="xsb c1-txt" x="344" y="122">λ₁ = sinθ</text>')

    px0, px1 = 78.0, 444.0
    py0, py1 = 138.0, 352.0
    pw, ph = px1 - px0, py1 - py0

    def tx(theta: float) -> float:
        return px0 + (theta / (math.pi / 2.0)) * pw

    def ty(val: float) -> float:
        return py1 - val * ph

    # Gridlines and ticks
    for v in (0.0, 0.25, 0.50, 0.75, 1.00):
        yy = ty(v)
        el.append(f'<line class="grid" x1="{px0:.1f}" y1="{yy:.1f}" x2="{px1:.1f}" y2="{yy:.1f}"/>')
        el.append(f'<text class="xs" x="{px0-8:.1f}" y="{yy+4:.1f}" text-anchor="end">{v:.2f}</text>')

    x_ticks = [(0.0, "0"), (math.pi / 8, "π/8"), (math.pi / 4, "π/4"), (3 * math.pi / 8, "3π/8"), (math.pi / 2, "π/2")]
    for ang, lbl in x_ticks:
        xx = tx(ang)
        el.append(f'<line class="grid" x1="{xx:.1f}" y1="{py0:.1f}" x2="{xx:.1f}" y2="{py1:.1f}"/>')
        el.append(f'<line class="axis" stroke-width="1.2" x1="{xx:.1f}" y1="{py1:.1f}" x2="{xx:.1f}" y2="{py1+5:.1f}"/>')
        el.append(f'<text class="xs" x="{xx:.1f}" y="{py1+19:.1f}" text-anchor="middle">{lbl}</text>')

    # Shaded area under S(rho_A)
    n_pts = 120
    s_pts: list[tuple[float, float]] = []
    l0_pts: list[tuple[float, float]] = []
    l1_pts: list[tuple[float, float]] = []
    for k in range(n_pts + 1):
        th = (math.pi / 2.0) * k / n_pts
        c, s = math.cos(th), math.sin(th)
        ent = binary_entropy(c * c)
        s_pts.append((tx(th), ty(ent)))
        l0_pts.append((tx(th), ty(c)))
        l1_pts.append((tx(th), ty(s)))

    area_pts = [(px0, py1)] + s_pts + [(px1, py1)]
    el.append(f'<path class="area2" d="{poly_d(area_pts)} Z"/>')
    el.append(f'<path class="c3" stroke-width="2.2" d="{poly_d(l0_pts)}"/>')
    el.append(f'<path class="c1" stroke-width="2.2" stroke-dasharray="6 4" d="{poly_d(l1_pts)}"/>')
    el.append(f'<path class="c2" stroke-width="2.8" d="{poly_d(s_pts)}"/>')

    # Axes box
    el.append(f'<rect class="axis" stroke-width="1.4" x="{px0:.1f}" y="{py0:.1f}" width="{pw:.1f}" height="{ph:.1f}"/>')
    el.append(f'<text class="smb" x="{(px0+px1)/2:.1f}" y="391" text-anchor="middle">叠加角 θ（|ψ(θ)⟩ = cosθ|00⟩ + sinθ|11⟩）</text>')
    el.append('<text class="smb" x="34" y="245" transform="rotate(-90 34 245)" text-anchor="middle">奇异值 λᵢ / 纠缠熵 S (ebit)</text>')

    # Key point annotations at theta = pi/4
    x_mid = tx(math.pi / 4.0)
    y_peak = ty(1.0)
    y_cross = ty(1.0 / math.sqrt(2.0))
    el.append(f'<line class="guide" x1="{x_mid:.1f}" y1="{y_peak:.1f}" x2="{x_mid:.1f}" y2="275"/>')
    el.append(f'<circle class="c2-fill" cx="{x_mid:.1f}" cy="{y_peak:.1f}" r="4.6"/>')
    el.append(f'<circle class="c3-fill" cx="{x_mid:.1f}" cy="{y_cross:.1f}" r="4.4"/>')
    # Separable endpoints
    el.append(f'<circle class="qnode" cx="{px0:.1f}" cy="{py1:.1f}" r="4.0"/>')
    el.append(f'<circle class="qnode" cx="{px1:.1f}" cy="{py1:.1f}" r="4.0"/>')

    # Callout pill in empty lower-middle triangle (strictly below cos/sin curves)
    el.append('<rect class="pill-bg" x="172" y="275" width="178" height="62" rx="8"/>')
    el.append('<text class="xsb c2-txt" x="261" y="293" text-anchor="middle">θ = π/4（最大纠缠 Bell 态）</text>')
    el.append('<text class="xs" x="261" y="311" text-anchor="middle">λ₀ = λ₁ = 1/√2 ≈ 0.707</text>')
    el.append('<text class="xsb c3-txt" x="261" y="329" text-anchor="middle">S(ρ_A) = 1.00 ebit，r = 2</text>')

    el.extend(note_bar(34, 404, 416, "纯态充要：Schmidt 秩 r = 2 ⇔ S(ρ_A) > 0；混态中 S(ρ_A) 失效！"))

    # Right panel: Entanglement criteria decision tree (x=478..940, w=462)
    el.extend(panel_shell(478, 68, 462, 376, "2. 两体纠缠判据决策树（纯态 vs 混态分层）"))

    # Root node
    el.append('<rect class="pill" x="582" y="109" width="256" height="32" rx="8"/>')
    el.append('<text class="smb" x="710" y="129.5" text-anchor="middle">输入两体态 ρ_AB（先验纯度 Tr(ρ²)）</text>')

    # Split edges from root (710, 141) to left pure branch (570, 174) and right mixed branch (796, 174)
    el.append('<path class="axis" stroke-width="1.5" d="M 710 141 V 154 H 570 V 170"/>')
    el.append(arrow_head(570, 154, 570, 174, fill_cls="axis-fill", length=7.5, half_w=3.4))
    el.append('<path class="axis" stroke-width="1.5" d="M 710 141 V 154 H 796 V 170"/>')
    el.append(arrow_head(796, 154, 796, 174, fill_cls="axis-fill", length=7.5, half_w=3.4))
    el.append('<text class="xsb c3-txt" x="562" y="150" text-anchor="end">Tr(ρ²)=1</text>')
    el.append('<text class="xsb c1-txt" x="804" y="150">Tr(ρ²)&lt;1</text>')

    # Left column: Pure-state box (x=492..648, w=156, y=175..271)
    el.append('<rect class="c3-soft" x="492" y="175" width="156" height="96" rx="9"/>')
    el.append('<text class="smb c3-txt" x="570" y="196" text-anchor="middle">纯态分支（一步充要）</text>')
    el.append('<text class="xsb" x="570" y="216" text-anchor="middle">Schmidt 秩 r / ad−bc</text>')
    el.append('<text class="xs" x="570" y="236" text-anchor="middle">r ≥ 2 ⇔ S(ρ_A) &gt; 0</text>')
    el.append('<text class="xs c3-txt" x="570" y="256" text-anchor="middle">2×2 等价于 2|ad−bc|&gt;0</text>')

    # Lower-left box: Strict hierarchy card (x=492..648, w=156, y=285..392)
    el.append('<rect class="subpanel" x="492" y="285" width="156" height="107" rx="9"/>')
    el.append('<text class="xsb" x="570" y="304" text-anchor="middle">混态判据严格包含链</text>')
    el.append('<text class="xs c2-txt" x="504" y="324">CHSH 违背 (|S| &gt; 2)</text>')
    el.append('<text class="xs c4-txt" x="504" y="342">⊂ 纠缠见证 Tr(Wρ)&lt;0</text>')
    el.append('<text class="xs c1-txt" x="504" y="360">⊂ PPT 负特征值 N&gt;0</text>')
    el.append('<text class="xs c3-txt" x="504" y="378">⊂ 全部纠缠(含束缚)</text>')

    # Right column: Mixed-state 3-tier cascade (x=666..926, w=260)
    # Tier 1: PPT
    el.append('<rect class="c1-soft" x="666" y="175" width="260" height="58" rx="9"/>')
    el.append('<text class="xsb c1-txt" x="678" y="194">① PPT 判据：求部分转置 ρᵀᴮ 特征值</text>')
    el.append('<text class="xs" x="678" y="212">λ_min &lt; 0 ⇒ 必纠缠（负性 N(ρ) &gt; 0）</text>')
    el.append('<text class="xsb" x="678" y="227">2×2, 2×3 充要；d ≥ 3×3 仅充分</text>')

    el.extend(arrow_line(796, 234, 796, 253, stroke_cls="axis", fill_cls="axis-fill", sw=1.5, length=7.0, half_w=3.2))
    el.append('<text class="xs" x="804" y="247">λ_min≥0 或需少测</text>')

    # Tier 2: Entanglement witness
    el.append('<rect class="c4-soft" x="666" y="255" width="260" height="58" rx="9"/>')
    el.append('<text class="xsb c4-txt" x="678" y="274">② 纠缠见证 W（如 C_X + C_Z）</text>')
    el.append('<text class="xs" x="678" y="292">Tr(Wρ) &lt; 0 ⇒ 必纠缠（仅充分）</text>')
    el.append('<text class="xs" x="678" y="307">免完整层析，但依赖测量基校准可信</text>')

    el.extend(arrow_line(796, 314, 796, 333, stroke_cls="axis", fill_cls="axis-fill", sw=1.5, length=7.0, half_w=3.2))
    el.append('<text class="xs" x="804" y="327">零信任/黑盒检验</text>')

    # Tier 3: Bell-CHSH
    el.append('<rect class="c2-soft" x="666" y="335" width="260" height="57" rx="9"/>')
    el.append('<text class="xsb c2-txt" x="678" y="353">③ Bell–CHSH 检验（设备无关）</text>')
    el.append('<text class="xs" x="678" y="371">|S| &gt; 2 ⇒ 非局域且必纠缠（比纠缠更强）</text>')
    el.append('<text class="xs" x="678" y="386">仅充分：Werner 态 p∈(1/3, 1/√2] 不违背</text>')

    el.extend(note_bar(492, 404, 434, "速查：2×2 混态首选 PPT/共生度；省测选见证 W；设备无关必测 CHSH"))

    svg = svg_doc(
        "双比特 Schmidt 分解曲线与混态纠缠判据决策树",
        "左面板绘出双比特纯态 |ψ(θ)⟩ = cosθ|00⟩ + sinθ|11⟩ 的 Schmidt 奇异值 (cosθ, sinθ) 与纠缠熵 S(ρ_A) 实算曲线，在 θ=π/4 达最大纠缠 1 ebit；右面板整合纯态与混态纠缠判据决策树，依次覆盖 PPT、纠缠见证与设备无关 Bell-CHSH 检验。",
        el,
    )
    return svg, {"S_pi4": 1.0, "S_pi8": round(s_pi8, 6)}


# =============================================================================
# Figure 3: v4-04-toffoli-superdense.svg
# =============================================================================
def build_fig3_toffoli_superdense() -> tuple[str, dict[str, object]]:
    # Exact 8-basis-state verification of 6-CNOT / 7-T / 2-H Toffoli decomposition
    def apply_1q(state: list[complex], q: int, u: list[list[complex]]) -> list[complex]:
        out = [0j] * 8
        bit = 1 << (2 - q)
        for idx in range(8):
            b = 1 if (idx & bit) else 0
            out[idx] = u[b][0] * state[idx & ~bit] + u[b][1] * state[idx | bit]
        return out

    def apply_cx(state: list[complex], c: int, t: int) -> list[complex]:
        out = list(state)
        bc, bt = 1 << (2 - c), 1 << (2 - t)
        for idx in range(8):
            if (idx & bc) and not (idx & bt):
                out[idx], out[idx | bt] = state[idx | bt], state[idx]
        return out

    inv2 = 1.0 / math.sqrt(2.0)
    h_mat = [[inv2, inv2], [inv2, -inv2]]
    t_mat = [[1 + 0j, 0j], [0j, cmath.exp(1j * math.pi / 4.0)]]
    td_mat = [[1 + 0j, 0j], [0j, cmath.exp(-1j * math.pi / 4.0)]]

    for inp in range(8):
        st = [0j] * 8
        st[inp] = 1.0 + 0j
        st = apply_1q(st, 2, h_mat)
        st = apply_cx(st, 1, 2)
        st = apply_1q(st, 2, td_mat)
        st = apply_cx(st, 0, 2)
        st = apply_1q(st, 2, t_mat)
        st = apply_cx(st, 1, 2)
        st = apply_1q(st, 2, td_mat)
        st = apply_cx(st, 0, 2)
        st = apply_1q(st, 1, t_mat)
        st = apply_1q(st, 2, t_mat)
        st = apply_cx(st, 0, 1)
        st = apply_1q(st, 2, h_mat)
        st = apply_1q(st, 0, t_mat)
        st = apply_1q(st, 1, td_mat)
        st = apply_cx(st, 0, 1)
        a, b, c = (inp >> 2) & 1, (inp >> 1) & 1, inp & 1
        exp_idx = (a << 2) | (b << 1) | (c ^ (a & b))
        assert abs(st[exp_idx] - 1.0) < 1e-12, f"Toffoli mismatch on {inp}"

    el: list[str] = []
    el.extend(
        header(
            "Toffoli 门 6-CNOT / 7-T 标准分解与超密编码 / 隐形传态对偶电路",
            "左：无辅助 Toffoli 门精确 Clifford+T 线路（理论下界）；右：超密编码与隐形传态的镜像对偶结构",
        )
    )

    # Left panel: Toffoli 6-CNOT / 7-T circuit (x=20..508, w=488)
    el.extend(panel_shell(20, 68, 488, 376, "1. Toffoli 门标准 Clifford+T 分解（6 CNOT + 7 T/T† + 2 H）"))

    # Phase polynomial strip
    el.append('<rect class="subpanel" x="34" y="109" width="460" height="28" rx="7"/>')
    el.append('<text class="xsb" x="264" y="127" text-anchor="middle">CCZ 相位多项式：4abc = a + b + c − (a⊕b) − (a⊕c) − (b⊕c) + (a⊕b⊕c)</text>')

    # 3 wires
    ys = [174.0, 230.0, 286.0]
    in_lbls = ["|a⟩", "|b⟩", "|c⟩"]
    out_lbls = ["|a⟩", "|b⟩", "|c⊕ab⟩"]
    for y, il, ol in zip(ys, in_lbls, out_lbls):
        el.append(f'<line class="wire" x1="68" y1="{y:.1f}" x2="444" y2="{y:.1f}"/>')
        el.append(f'<text class="smb" x="62" y="{y+4.5:.1f}" text-anchor="end">{il}</text>')
        el.append(f'<text class="smb c3-txt" x="450" y="{y+4.5:.1f}">{ol}</text>')

    cols = [86.0 + k * 30.8 for k in range(12)]
    # Col 0: H on q3
    el.extend(gate_box(cols[0], ys[2], "H", box_cls="c1-soft", txt_cls="gate-txt c1-txt", w=25, h=24))
    # Col 1: CNOT(2->3)
    el.extend(cnot_elem(cols[1], ys[1], ys[2]))
    # Col 2: T^dag on q3
    el.extend(gate_box(cols[2], ys[2], "T†", box_cls="c2-soft", txt_cls="gate-txt c2-txt", w=25, h=24))
    # Col 3: CNOT(1->3)
    el.extend(cnot_elem(cols[3], ys[0], ys[2]))
    # Col 4: T on q3
    el.extend(gate_box(cols[4], ys[2], "T", box_cls="c2-soft", txt_cls="gate-txt c2-txt", w=25, h=24))
    # Col 5: CNOT(2->3)
    el.extend(cnot_elem(cols[5], ys[1], ys[2]))
    # Col 6: T^dag on q3
    el.extend(gate_box(cols[6], ys[2], "T†", box_cls="c2-soft", txt_cls="gate-txt c2-txt", w=25, h=24))
    # Col 7: CNOT(1->3)
    el.extend(cnot_elem(cols[7], ys[0], ys[2]))
    # Col 8: T on q2 and T on q3
    el.extend(gate_box(cols[8], ys[1], "T", box_cls="c2-soft", txt_cls="gate-txt c2-txt", w=25, h=24))
    el.extend(gate_box(cols[8], ys[2], "T", box_cls="c2-soft", txt_cls="gate-txt c2-txt", w=25, h=24))
    # Col 9: CNOT(1->2) and H on q3
    el.extend(cnot_elem(cols[9], ys[0], ys[1]))
    el.extend(gate_box(cols[9], ys[2], "H", box_cls="c1-soft", txt_cls="gate-txt c1-txt", w=25, h=24))
    # Col 10: T on q1 and T^dag on q2
    el.extend(gate_box(cols[10], ys[0], "T", box_cls="c2-soft", txt_cls="gate-txt c2-txt", w=25, h=24))
    el.extend(gate_box(cols[10], ys[1], "T†", box_cls="c2-soft", txt_cls="gate-txt c2-txt", w=25, h=24))
    # Col 11: CNOT(1->2)
    el.extend(cnot_elem(cols[11], ys[0], ys[1]))

    # Resource comparison cards below circuit
    el.append('<rect class="c2-soft" x="34" y="318" width="224" height="76" rx="8"/>')
    el.append('<text class="xsb c2-txt" x="46" y="337">无辅助理论下界（本电路）</text>')
    el.append('<text class="xs" x="46" y="357">6 CNOT + 4 T + 3 T† + 2 H = 15 门</text>')
    el.append('<text class="xs" x="46" y="377">Shende–Markov / Gosset 严格下界</text>')

    el.append('<rect class="c3-soft" x="270" y="318" width="224" height="76" rx="8"/>')
    el.append('<text class="xsb c3-txt" x="282" y="337">借 1 干净辅助位：4-T 临时逻辑与</text>')
    el.append('<text class="xs" x="282" y="357">正向仅耗 4 个 T 门（Jones/Gidney）</text>')
    el.append('<text class="xs" x="282" y="377">中段测量 + Clifford 反计算 0 个 T</text>')

    el.extend(note_bar(34, 404, 460, "两侧 H 将对称 CCZ 转为 CCNOT；赤陶色 T/T† 门主导容错魔法态开销"))

    # Right panel: Superdense vs Teleportation dual circuits (x=520..940, w=420)
    el.extend(panel_shell(520, 68, 420, 376, "2. 超密编码 vs 隐形传态：镜像对偶电路"))

    # --- Upper subpanel: Superdense Coding (y=108..244) ---
    el.append('<rect class="subpanel" x="532" y="108" width="396" height="136" rx="9"/>')
    el.append('<text class="smb c3-txt" x="544" y="127">A. 超密编码：1 ebit + 1 qubit → 2 cbits</text>')
    # Bell pair bracket & wires
    sy1, sy2 = 166.0, 210.0
    el.append('<text class="smb" x="556" y="192" text-anchor="middle">|Φ⁺⟩</text>')
    el.append(f'<path class="axis" stroke-width="1.3" d="M 578 {sy1:.0f} H 573 V {sy2:.0f} H 578"/>')
    el.append(f'<line class="wire" x1="578" y1="{sy1:.0f}" x2="862" y2="{sy1:.0f}"/>')
    el.append(f'<line class="wire" x1="578" y1="{sy2:.0f}" x2="862" y2="{sy2:.0f}"/>')
    el.append('<text class="xs" x="588" y="158">A</text>')
    el.append('<text class="xs" x="588" y="226">B</text>')

    # Alice Pauli encoding (forest dashed box)
    el.append('<rect class="c3" stroke-width="1.2" stroke-dasharray="4 3" x="606" y="142" width="84" height="48" rx="6"/>')
    el.extend(gate_box(648, sy1, "U(m₁m₂)", box_cls="c3-soft", txt_cls="xsb c3-txt", w=66, h=25))
    el.append('<text class="xs c3-txt" x="648" y="202" text-anchor="middle">Alice：Pauli 门</text>')

    # Quantum channel label
    el.append('<text class="xsb c2-txt" x="726" y="156" text-anchor="middle">寄 1 qubit</text>')
    el.append(arrow_head(700, sy1, 752, sy1, fill_cls="c2-fill", length=7.5, half_w=3.3))

    # Bob Bell measurement (blue dashed box)
    el.append('<rect class="c1" stroke-width="1.2" stroke-dasharray="4 3" x="758" y="142" width="124" height="84" rx="6"/>')
    el.extend(cnot_elem(778, sy1, sy2, r_ctrl=3.8, r_targ=8.2))
    el.extend(gate_box(812, sy1, "H", box_cls="c1-soft", txt_cls="gate-txt c1-txt", w=24, h=23))
    el.extend(meter_box(854, sy1, w=24, h=22))
    el.extend(meter_box(854, sy2, w=24, h=22))
    # Classical outputs
    for yy, ml in ((sy1, "m₁"), (sy2, "m₂")):
        el.append(f'<line class="cwire" x1="866" y1="{yy-1.6:.1f}" x2="894" y2="{yy-1.6:.1f}"/>')
        el.append(f'<line class="cwire" x1="866" y1="{yy+1.6:.1f}" x2="894" y2="{yy+1.6:.1f}"/>')
        el.append(f'<text class="xsb c1-txt" x="900" y="{yy+4:.1f}">{ml}</text>')
    el.append('<text class="xs c1-txt" x="820" y="238" text-anchor="middle">Bob：Bell 基测量</text>')

    # --- Lower subpanel: Quantum Teleportation (y=254..394) ---
    el.append('<rect class="subpanel" x="532" y="254" width="396" height="140" rx="9"/>')
    el.append('<text class="smb c1-txt" x="544" y="273">B. 量子隐形传态：1 ebit + 2 cbits → 1 qubit</text>')
    ty0, ty1, ty2 = 300.0, 334.0, 368.0
    el.append('<text class="smb c3-txt" x="556" y="304" text-anchor="middle">|ψ⟩</text>')
    el.append('<text class="smb" x="556" y="355" text-anchor="middle">|Φ⁺⟩</text>')
    el.append(f'<path class="axis" stroke-width="1.3" d="M 578 {ty1:.0f} H 573 V {ty2:.0f} H 578"/>')
    el.append(f'<line class="wire" x1="578" y1="{ty0:.0f}" x2="700" y2="{ty0:.0f}"/>')
    el.append(f'<line class="wire" x1="578" y1="{ty1:.0f}" x2="700" y2="{ty1:.0f}"/>')
    el.append(f'<line class="wire" x1="578" y1="{ty2:.0f}" x2="884" y2="{ty2:.0f}"/>')

    # Alice Bell measurement (blue dashed box)
    el.append('<rect class="c1" stroke-width="1.2" stroke-dasharray="4 3" x="596" y="282" width="128" height="68" rx="6"/>')
    el.extend(cnot_elem(616, ty0, ty1, r_ctrl=3.8, r_targ=8.0))
    el.extend(gate_box(652, ty0, "H", box_cls="c1-soft", txt_cls="gate-txt c1-txt", w=24, h=22))
    el.extend(meter_box(694, ty0, w=24, h=22))
    el.extend(meter_box(694, ty1, w=24, h=22))
    el.append('<text class="xs c1-txt" x="660" y="388" text-anchor="middle">Alice：Bell 基测量</text>')

    # Classical double wires to Bob's X and Z corrections
    # m1 (top, ty0) -> Z at x=846; m2 (mid, ty1) -> X at x=804
    el.append('<text class="xsb c2-txt" x="768" y="294" text-anchor="middle">传 2 cbits</text>')
    el.append(f'<path class="cwire" d="M 706 {ty0-1.5:.1f} H 847.5 V {ty2-12:.1f}"/>')
    el.append(f'<path class="cwire" d="M 706 {ty0+1.5:.1f} H 844.5 V {ty2-12:.1f}"/>')
    el.append(f'<path class="cwire" d="M 706 {ty1-1.5:.1f} H 805.5 V {ty2-12:.1f}"/>')
    el.append(f'<path class="cwire" d="M 706 {ty1+1.5:.1f} H 802.5 V {ty2-12:.1f}"/>')
    el.append('<text class="xs" x="734" y="326">m₂</text>')
    el.append('<text class="xs" x="854" y="318">m₁</text>')

    # Bob Pauli correction (forest dashed box)
    el.append('<rect class="c3" stroke-width="1.2" stroke-dasharray="4 3" x="782" y="350" width="88" height="36" rx="6"/>')
    el.extend(gate_box(804, ty2, "X", box_cls="c3-soft", txt_cls="gate-txt c3-txt", w=24, h=22))
    el.extend(gate_box(846, ty2, "Z", box_cls="c3-soft", txt_cls="gate-txt c3-txt", w=24, h=22))
    el.append('<text class="smb c3-txt" x="892" y="372">|ψ⟩</text>')

    el.extend(note_bar(532, 404, 396, "同色积木互换：超密“先 Pauli 后 Bell 测”，传态“先 Bell 测后 Pauli”"))

    svg = svg_doc(
        "Toffoli 门 6-CNOT 7-T 分解与超密编码隐形传态对偶电路",
        "左面板展示无辅助 Toffoli 门的标准 15 门 Clifford+T 分解（6 CNOT、7 个 T/T† 与 2 个 H），并对比 4-T 临时逻辑与优化；右面板上下对照超密编码（1 ebit + 1 qubit → 2 cbits）与量子隐形传态（1 ebit + 2 cbits → 1 qubit）的镜像对偶电路结构。",
        el,
    )
    return svg, {"toffoli_cnots": 6, "toffoli_t": 7, "verified_basis": 8}


# =============================================================================
# Figure 4: v4-06-aa-prepare-select.svg
# =============================================================================
def build_fig4_aa_prepare_select() -> tuple[str, dict[str, object]]:
    # Verify amplitude amplification angle theta = 18 deg = pi/10
    th_aa = math.pi / 10.0
    p0_aa = math.sin(th_aa) ** 2
    p1_aa = math.sin(3 * th_aa) ** 2
    p2_aa = math.sin(5 * th_aa) ** 2
    assert abs(p2_aa - 1.0) < 1e-12

    # Verify explicit 6-gate PREPARE / SELECT / PREPARE^dag for H = 0.6 X + 0.8 Z
    alpha = 0.6 + 0.8
    th_lcu = 2.0 * math.atan(math.sqrt(0.8 / 0.6))

    def apply_1q_2(state: list[complex], q: int, u: list[list[float]]) -> list[complex]:
        out = [0j] * 4
        bit = 1 << (1 - q)
        for idx in range(4):
            b = 1 if (idx & bit) else 0
            out[idx] = u[b][0] * state[idx & ~bit] + u[b][1] * state[idx | bit]
        return out

    def ry(ang: float) -> list[list[float]]:
        c, s = math.cos(ang / 2.0), math.sin(ang / 2.0)
        return [[c, -s], [s, c]]

    x_mat = [[0.0, 1.0], [1.0, 0.0]]
    block = [[0j, 0j], [0j, 0j]]
    for s_in in range(2):
        st = [0j] * 4
        st[s_in] = 1.0 + 0j
        st = apply_1q_2(st, 0, ry(th_lcu))
        st[3] = -st[3]  # CZ
        st = apply_1q_2(st, 0, x_mat)
        st[2], st[3] = st[3], st[2]  # CNOT(a->s)
        st = apply_1q_2(st, 0, x_mat)
        st = apply_1q_2(st, 0, ry(-th_lcu))
        block[0][s_in] = st[0]
        block[1][s_in] = st[1]

    assert abs(block[0][0] - 4.0 / 7.0) < 1e-12
    assert abs(block[0][1] - 3.0 / 7.0) < 1e-12
    assert abs(block[1][0] - 3.0 / 7.0) < 1e-12
    assert abs(block[1][1] + 4.0 / 7.0) < 1e-12
    p0_lcu = 1.0 / (alpha * alpha)

    el: list[str] = []
    el.extend(
        header(
            "振幅放大二维镜面旋转几何与 6 门 PREPARE/SELECT 块编码",
            "左：振幅放大在 {|B⟩, |G⟩} 平面由两次反射合成 +2θ 净旋转；右：H = 0.6X + 0.8Z 显式 6 门 LCU 块编码电路",
        )
    )

    # Left panel: Amplitude Amplification Geometry (x=20..448, w=428)
    el.extend(panel_shell(20, 68, 428, 376, "1. 振幅放大几何：{|B⟩, |G⟩} 平面旋转 +2θ"))

    ox, oy, rad = 82.0, 314.0, 174.0

    def pt(ang_deg: float, r: float = rad) -> tuple[float, float]:
        a = math.radians(ang_deg)
        return ox + r * math.cos(a), oy - r * math.sin(a)

    # Unit circle arc (-24 deg to +96 deg)
    arc_pts = [pt(a) for a in range(-24, 97, 3)]
    el.append(f'<path class="unit-circle" d="{poly_d(arc_pts)}"/>')

    # Axes |B> and |G>
    el.extend(arrow_line(ox - 18, oy, ox + rad + 36, oy, stroke_cls="axis", fill_cls="axis-fill", sw=1.6))
    el.extend(arrow_line(ox, oy + 68, ox, oy - rad - 24, stroke_cls="axis", fill_cls="axis-fill", sw=1.6))
    el.append(f'<text class="smb" x="{ox+rad+40:.0f}" y="{oy+4:.0f}">|B⟩ (坏态)</text>')
    el.append(f'<text class="smb" x="{ox+10:.0f}" y="{oy-rad-15:.0f}">|G⟩ (目标态)</text>')
    el.append(f'<text class="xs" x="{ox-10:.0f}" y="{oy+16:.0f}" text-anchor="end">O</text>')

    # Reflection chord (|psi0> -> S_chi|psi0>)
    p_psi0 = pt(18)
    p_ref = pt(-18)
    p_q1 = pt(54)
    p_q2 = pt(90)
    el.extend(arrow_line(p_psi0[0], p_psi0[1] + 5, p_ref[0], p_ref[1] - 5, stroke_cls="c2", fill_cls="c2-fill", sw=1.6, dash="4 3", length=7.0, half_w=3.2))

    # Curved net rotation arc (+18 -> +54 at r=128)
    rot_pts = [pt(a, 128) for a in range(18, 55, 2)]
    el.append(f'<path class="c3" stroke-width="2.2" d="{poly_d(rot_pts[:-1])}"/>')
    el.append(arrow_head(rot_pts[-3][0], rot_pts[-3][1], rot_pts[-1][0], rot_pts[-1][1], fill_cls="c3-fill", length=7.5, half_w=3.5))

    # Small angle arcs near origin (r=54)
    el.append(f'<path class="c1" stroke-width="1.4" d="{poly_d([pt(a, 54) for a in range(0, 19, 3)])}"/>')
    el.append(f'<path class="c2" stroke-width="1.4" d="{poly_d([pt(a, 54) for a in range(-18, 1, 3)])}"/>')
    el.append(f'<text class="xs c1-txt" x="{ox+62:.0f}" y="{oy-6:.0f}">+θ</text>')
    el.append(f'<text class="xs c2-txt" x="{ox+62:.0f}" y="{oy+16:.0f}">−θ</text>')

    # State vectors from origin
    el.extend(arrow_line(ox, oy, p_psi0[0], p_psi0[1], stroke_cls="c1", fill_cls="c1-fill", sw=2.5))
    el.extend(arrow_line(ox, oy, p_ref[0], p_ref[1], stroke_cls="c2", fill_cls="c2-fill", sw=2.2, dash="6 3"))
    el.extend(arrow_line(ox, oy, p_q1[0], p_q1[1], stroke_cls="c3", fill_cls="c3-fill", sw=2.6))
    el.extend(arrow_line(ox, oy, p_q2[0], p_q2[1], stroke_cls="c4", fill_cls="c4-fill", sw=2.2, dash="5 4"))

    # Endpoint markers
    el.append(f'<circle class="c1-fill" cx="{p_psi0[0]:.1f}" cy="{p_psi0[1]:.1f}" r="4.2"/>')
    el.append(f'<circle class="c2-fill" cx="{p_ref[0]:.1f}" cy="{p_ref[1]:.1f}" r="4.0"/>')
    el.append(f'<circle class="c3-fill" cx="{p_q1[0]:.1f}" cy="{p_q1[1]:.1f}" r="4.6"/>')
    el.append(f'<circle class="c4-fill" cx="{p_q2[0]:.1f}" cy="{p_q2[1]:.1f}" r="4.2"/>')

    # Clean non-overlapping labels
    el.append(f'<rect class="pill-bg" x="{ox+12:.0f}" y="{oy-rad-3:.0f}" width="184" height="20" rx="5"/>')
    el.append(f'<text class="xsb c4-txt" x="{ox+104:.0f}" y="{oy-rad+11:.0f}" text-anchor="middle">Q²|ψ₀⟩ = |G⟩ (5θ=90°, p₂=1)</text>')
    el.append(f'<text class="xsb c3-txt" x="{p_q1[0]+16:.0f}" y="{p_q1[1]-3:.0f}">Q|ψ₀⟩ (3θ = 54°)</text>')
    el.append(f'<text class="xs c3-txt" x="{p_q1[0]+16:.0f}" y="{p_q1[1]+13:.0f}">p₁ = sin²3θ ≈ 65.5%</text>')
    el.append('<rect class="pill-bg" x="206" y="210" width="128" height="24" rx="7"/>')
    el.append('<text class="xsb c3-txt" x="270" y="226" text-anchor="middle">Q = S₀S_χ：净转 +2θ</text>')
    el.append(f'<text class="xsb c1-txt" x="{p_psi0[0]+10:.0f}" y="{p_psi0[1]-2:.0f}">|ψ₀⟩ (θ = 18°)</text>')
    el.append(f'<text class="xs c1-txt" x="{p_psi0[0]+10:.0f}" y="{p_psi0[1]+14:.0f}">p₀ = sin²θ ≈ 9.5%</text>')
    el.append(f'<text class="xsb c2-txt" x="{p_ref[0]+10:.0f}" y="{p_ref[1]-2:.0f}">S_χ|ψ₀⟩ (−θ)</text>')
    el.append(f'<text class="xs c2-txt" x="{p_ref[0]+10:.0f}" y="{p_ref[1]+14:.0f}">① 沿 |B⟩ 反射</text>')

    el.extend(note_bar(34, 404, 400, "每步净转 +2θ；最优步数 k ≈ ⌊π/(4θ)⌋，超步将过冲回落"))

    # Right panel: Explicit 6-gate PREPARE/SELECT block encoding (x=460..940, w=480)
    el.extend(panel_shell(460, 68, 480, 376, "2. H = 0.6X + 0.8Z 显式 6 门 PREPARE/SELECT 电路"))

    # Stage dashed frames
    el.append('<rect class="c3" stroke-width="1.2" stroke-dasharray="4 3" x="526" y="114" width="76" height="132" rx="7"/>')
    el.append('<text class="xsb c3-txt" x="564" y="131" text-anchor="middle">PREPARE</text>')

    el.append('<rect class="c1" stroke-width="1.2" stroke-dasharray="4 3" x="612" y="114" width="154" height="132" rx="7"/>')
    el.append('<text class="xsb c1-txt" x="689" y="131" text-anchor="middle">SELECT = diag(X, Z)</text>')

    el.append('<rect class="c2" stroke-width="1.2" stroke-dasharray="4 3" x="776" y="114" width="82" height="132" rx="7"/>')
    el.append('<text class="xsb c2-txt" x="817" y="131" text-anchor="middle">PREPARE†</text>')

    # Wires (a: auxiliary, s: system)
    ya, ys = 166.0, 218.0
    el.append(f'<line class="wire" x1="516" y1="{ya:.0f}" x2="862" y2="{ya:.0f}"/>')
    el.append(f'<line class="wire" x1="516" y1="{ys:.0f}" x2="862" y2="{ys:.0f}"/>')
    el.append(f'<text class="smb" x="510" y="{ya+4.5:.0f}" text-anchor="end">|0⟩_a</text>')
    el.append(f'<text class="smb" x="510" y="{ys+4.5:.0f}" text-anchor="end">|ψ⟩_s</text>')
    el.append(f'<text class="xsb c2-txt" x="868" y="{ya+4:.0f}">⟨0|_a 投影</text>')
    el.append(f'<text class="xsb c3-txt" x="868" y="{ys+4:.0f}">(H/α)|ψ⟩</text>')

    # 6 explicit gates: Ry(theta), CZ, X, CNOT, X, Ry(-theta)
    el.extend(gate_box(564, ya, "Ry(θ)", box_cls="c3-soft", txt_cls="xsb c3-txt", w=54, h=26))
    el.extend(cz_elem(634, ya, ys))
    el.append(f'<text class="xs c1-txt" x="634" y="{ys+20:.0f}" text-anchor="middle">CZ</text>')
    el.extend(gate_box(668, ya, "X", box_cls="c1-soft", txt_cls="gate-txt c1-txt", w=25, h=24))
    el.extend(cnot_elem(706, ya, ys, r_ctrl=4.0, r_targ=8.5))
    el.append(f'<text class="xs c1-txt" x="706" y="{ys+20:.0f}" text-anchor="middle">CNOT</text>')
    el.extend(gate_box(744, ya, "X", box_cls="c1-soft", txt_cls="gate-txt c1-txt", w=25, h=24))
    el.extend(gate_box(817, ya, "Ry(−θ)", box_cls="c2-soft", txt_cls="xsb c2-txt", w=60, h=26))

    # Lower-left card: Explicit projected 2x2 matrix H / alpha
    el.append('<rect class="subpanel" x="474" y="260" width="220" height="134" rx="9"/>')
    el.append('<text class="xsb c3-txt" x="584" y="280" text-anchor="middle">投影块 ⟨0|_a U |0⟩_a = H / α</text>')
    el.append('<text class="xs" x="584" y="300" text-anchor="middle">= (3/7)X + (4/7)Z</text>')
    mx, my, mw, mh = 514, 312, 70, 34
    m_cells = [
        (0, 0, "c1-soft", "c1-txt", "+4/7"),
        (0, 1, "c3-soft", "c3-txt", "+3/7"),
        (1, 0, "c3-soft", "c3-txt", "+3/7"),
        (1, 1, "c1-soft", "c1-txt", "−4/7"),
    ]
    for r, c, bcls, tcls, lbl in m_cells:
        el.append(f'<rect class="{bcls}" x="{mx+c*mw}" y="{my+r*mh}" width="{mw-2}" height="{mh-2}" rx="4"/>')
        el.append(f'<text class="math-txt {tcls}" x="{mx+c*mw+mw/2-1:.1f}" y="{my+r*mh+21:.1f}" text-anchor="middle">{lbl}</text>')

    # Lower-right card: Parameter & probability ledger
    el.append('<rect class="subpanel" x="706" y="260" width="220" height="134" rx="9"/>')
    el.append('<text class="xsb c1-txt" x="718" y="280">参数设定与成功概率验算</text>')
    el.append('<text class="xs" x="718" y="303">1-范数缩放：α = 0.6 + 0.8 = 1.4</text>')
    el.append('<text class="xs" x="718" y="323">振幅分配：cos²(θ/2)=3/7, sin²=4/7</text>')
    el.append(f'<text class="xs" x="718" y="343">旋转角：θ = 2·atan(2/√3) ≈ {math.degrees(th_lcu):.2f}°</text>')
    el.append(f'<text class="xsb c2-txt" x="718" y="364">成功概率：p₀ = 1/α² ≈ {p0_lcu*100:.1f}%</text>')
    el.append('<text class="xs" x="718" y="383">（因 H² = (0.36+0.64)I = I 恒定）</text>')

    el.extend(note_bar(474, 404, 452, "6 门显式构造把抽象块编码落成硬件门，可直接衔接量子化与 QSVT"))

    svg = svg_doc(
        "振幅放大几何旋转与显式 6 门 PREPARE/SELECT 块编码电路",
        "左面板展示振幅放大在 {|B⟩, |G⟩} 二维平面内通过 S_χ 与 S₀ 两次反射合成 +2θ 净旋转的精确几何（θ=18° 时两步直达 |G⟩）；右面板给出 H = 0.6X + 0.8Z 的 6 门显式 PREPARE/SELECT 块编码电路、投影子块矩阵与成功概率 51.0% 验算。",
        el,
    )
    return svg, {"theta_lcu_deg": round(math.degrees(th_lcu), 3), "p0_lcu": round(p0_lcu, 4)}


# =============================================================================
# Figure 5: v4-07-simon-trotter.svg
# =============================================================================
def build_fig5_simon_trotter() -> tuple[str, dict[str, object]]:
    # 1. Verify Simon s = 101 (5) cosets and Walsh-Hadamard interference
    secret = 0b101
    cosets = []
    seen: set[int] = set()
    for x in range(8):
        if x not in seen:
            partner = x ^ secret
            cosets.append((x, partner))
            seen.add(x)
            seen.add(partner)
    assert len(cosets) == 4
    # Walsh-Hadamard on (|000> + |101>)/sqrt(2)
    def popcount_and(a: int, b: int) -> int:
        return bin(a & b).count("1") % 2

    nonzero_z = []
    for z in range(8):
        amp = (1.0 + ((-1.0) ** popcount_and(z, secret))) / 4.0
        if abs(amp) > 1e-12:
            assert abs(abs(amp) - 0.5) < 1e-12
            nonzero_z.append(f"{z:03b}")
    assert nonzero_z == ["000", "010", "101", "111"]

    # 2. Exact 2x2 operator norm errors for H = X + Z, t = 1.0
    def mm(a: list[list[complex]], b: list[list[complex]]) -> list[list[complex]]:
        return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

    def mpow(a: list[list[complex]], r: int) -> list[list[complex]]:
        res = [[1 + 0j, 0j], [0j, 1 + 0j]]
        base = a
        while r:
            if r & 1:
                res = mm(res, base)
            base = mm(base, base)
            r >>= 1
        return res

    def exp_pauli(axis: str, tau: float) -> list[list[complex]]:
        c, s = math.cos(tau), -1j * math.sin(tau)
        if axis == "X":
            return [[c, s], [s, c]]
        return [[c + s, 0j], [0j, c - s]]

    def op_norm_2(m: list[list[complex]]) -> float:
        md = [[m[j][i].conjugate() for j in range(2)] for i in range(2)]
        g = mm(md, m)
        tr = (g[0][0] + g[1][1]).real
        det = (g[0][0] * g[1][1] - g[0][1] * g[1][0]).real
        disc = max(0.0, tr * tr - 4.0 * det)
        return math.sqrt(max(0.0, 0.5 * (tr + math.sqrt(disc))))

    t_tot = 1.0
    w = math.sqrt(2.0) * t_tot
    c0, s0 = math.cos(w), -1j * math.sin(w) / math.sqrt(2.0)
    u_exact = [[c0 + s0, s0], [s0, c0 - s0]]

    r_vals = [1, 2, 4, 8, 16, 32, 64, 100]
    err1: list[float] = []
    err2: list[float] = []
    for r in r_vals:
        tau = t_tot / r
        s1 = mpow(mm(exp_pauli("X", tau), exp_pauli("Z", tau)), r)
        s2 = mpow(mm(exp_pauli("X", tau / 2.0), mm(exp_pauli("Z", tau), exp_pauli("X", tau / 2.0))), r)
        e1 = op_norm_2([[u_exact[i][j] - s1[i][j] for j in range(2)] for i in range(2)])
        e2 = op_norm_2([[u_exact[i][j] - s2[i][j] for j in range(2)] for i in range(2)])
        assert e1 <= (t_tot * t_tot) / r + 1e-12
        err1.append(e1)
        err2.append(e2)

    slope1 = math.log(err1[-1] / err1[2]) / math.log(r_vals[-1] / r_vals[2])
    slope2 = math.log(err2[-1] / err2[2]) / math.log(r_vals[-1] / r_vals[2])
    assert abs(slope1 + 1.0) < 0.03 and abs(slope2 + 2.0) < 0.03

    el: list[str] = []
    el.extend(
        header(
            "Simon 异或陪集干涉结构与 Suzuki–Trotter 误差双对数标度",
            "左：Simon 隐藏串 s = 101 将输入两两配对并在 H⊗³ 下滤出正交子空间 s⊥；右：一阶 vs 二阶对称 Trotter 实算误差",
        )
    )

    # Left panel: Simon coset pairing (x=20..464, w=444)
    el.extend(panel_shell(20, 68, 444, 376, "1. Simon 异或陪集配对（隐藏串 s = 101）"))
    el.append('<text class="xsb" x="34" y="121">2-to-1 承诺 f(x) = f(x ⊕ 101)：8 输入配成 4 组异或陪集</text>')

    coset_styles = [
        ("c3-soft", "c3-txt", "c3", "c3-fill", "y₀"),
        ("c1-soft", "c1-txt", "c1", "c1-fill", "y₁"),
        ("c4-soft", "c4-txt", "c4", "c4-fill", "y₂"),
        ("c2-soft", "c2-txt", "c2", "c2-fill", "y₃"),
    ]
    for idx, ((a, b), (bcls, tcls, scls, fcls, ylbl)) in enumerate(zip(cosets, coset_styles)):
        yy = 132 + idx * 48
        ym = yy + 20
        el.append(f'<rect class="{bcls}" x="34" y="{yy}" width="176" height="40" rx="8"/>')
        el.append(f'<text class="smb {tcls}" x="66" y="{ym+4}" text-anchor="middle">{a:03b}</text>')
        el.append(f'<text class="xs {tcls}" x="122" y="{ym+4}" text-anchor="middle">↔ ⊕101 ↔</text>')
        el.append(f'<text class="smb {tcls}" x="178" y="{ym+4}" text-anchor="middle">{b:03b}</text>')
        el.extend(arrow_line(212, ym, 240, ym, stroke_cls=scls, fill_cls=fcls, sw=1.7, length=7.0, half_w=3.2))
        el.append(f'<rect class="pill" x="242" y="{yy+5}" width="40" height="30" rx="7"/>')
        el.append(f'<text class="smb {tcls}" x="262" y="{ym+4}" text-anchor="middle">{ylbl}</text>')

    # Right column inside Left panel: Hadamard interference filter (x=294..450)
    el.append('<rect class="c3-soft" x="294" y="132" width="156" height="92" rx="9"/>')
    el.append('<text class="xsb c3-txt" x="372" y="151" text-anchor="middle">H⊗³ 相长干涉 (z·s = 0)</text>')
    el.append('<text class="xs" x="372" y="170" text-anchor="middle">满足 z₁ ⊕ z₃ = 0：</text>')
    el.append('<text class="xsb" x="372" y="191" text-anchor="middle">000, 010, 101, 111</text>')
    el.append('<text class="xs c3-txt" x="372" y="212" text-anchor="middle">每项测量概率均为 1/4</text>')

    el.append('<rect class="subpanel" x="294" y="234" width="156" height="86" rx="9"/>')
    el.append('<text class="xsb c2-txt" x="372" y="253" text-anchor="middle">H⊗³ 相消干涉 (z·s = 1)</text>')
    el.append('<text class="xs" x="372" y="272" text-anchor="middle">满足 z₁ ⊕ z₃ = 1：</text>')
    el.append('<text class="xs" x="372" y="291" text-anchor="middle">001, 011, 100, 110</text>')
    el.append('<text class="xs c2-txt" x="372" y="310" text-anchor="middle">正负振幅抵消，概率 = 0</text>')

    # Bottom F2 recovery box
    el.append('<rect class="subpanel" x="34" y="332" width="416" height="62" rx="9"/>')
    el.append('<text class="xsb c1-txt" x="46" y="352">经典 F₂ 线性方程恢复（仅需 n−1 = 2 个线性独立样本）：</text>')
    el.append('<text class="xs" x="46" y="372">测得 010 ⇒ s₂ = 0；测得 101 ⇒ s₁ ⊕ s₃ = 0；结合 s ≠ 000 得 s = 101</text>')
    el.append('<text class="xs" x="46" y="388">（量子干涉把指数搜索变成多项式线性消元）</text>')

    el.extend(note_bar(34, 404, 416, "量子仅需 O(n) 次查询；经典生日碰撞下界 Ω(2^(n/2))（指数分离）"))

    # Right panel: Trotter log-log error scaling (x=478..940, w=462)
    el.extend(panel_shell(478, 68, 462, 376, "2. 一阶 vs 二阶 Trotter 双对数误差（H = X+Z, t = 1）"))

    # Legend cleanly above plot
    el.append('<line class="c2" stroke-width="2.5" x1="504" y1="118" x2="526" y2="118"/>')
    el.append('<circle class="c2-fill" cx="515" cy="118" r="3.4"/>')
    el.append('<text class="xsb c2-txt" x="532" y="122">一阶 S₁: O(t²/r)</text>')

    el.append('<line class="c3" stroke-width="2.5" x1="650" y1="118" x2="672" y2="118"/>')
    el.append('<rect class="c3-fill" x="658" y="115" width="6.5" height="6.5" rx="1"/>')
    el.append('<text class="xsb c3-txt" x="678" y="122">二阶 S₂: O(t³/r²)</text>')

    el.append('<line class="guide" stroke-width="1.6" x1="802" y1="118" x2="826" y2="118"/>')
    el.append('<text class="xs" x="832" y="122">上界 t²/r</text>')

    px0, px1 = 548.0, 922.0
    py0, py1 = 138.0, 352.0
    pw, ph = px1 - px0, py1 - py0
    logr_min, logr_max = 0.0, 2.0
    loge_min, loge_max = -5.0, 0.2

    def tx(r: float) -> float:
        return px0 + (math.log10(r) - logr_min) / (logr_max - logr_min) * pw

    def ty(err: float) -> float:
        return py1 - (math.log10(err) - loge_min) / (loge_max - loge_min) * ph

    # Horizontal gridlines (10^0 down to 10^-5)
    exp_lbls = [(0, "10⁰"), (-1, "10⁻¹"), (-2, "10⁻²"), (-3, "10⁻³"), (-4, "10⁻⁴"), (-5, "10⁻⁵")]
    for e_pow, lbl in exp_lbls:
        yy = ty(10.0 ** e_pow)
        el.append(f'<line class="grid" x1="{px0:.1f}" y1="{yy:.1f}" x2="{px1:.1f}" y2="{yy:.1f}"/>')
        el.append(f'<text class="xs" x="{px0-8:.1f}" y="{yy+4:.1f}" text-anchor="end">{lbl}</text>')

    # Vertical gridlines
    for rv in (1, 2, 4, 10, 20, 50, 100):
        xx = tx(rv)
        el.append(f'<line class="grid" x1="{xx:.1f}" y1="{py0:.1f}" x2="{xx:.1f}" y2="{py1:.1f}"/>')
        el.append(f'<line class="axis" stroke-width="1.2" x1="{xx:.1f}" y1="{py1:.1f}" x2="{xx:.1f}" y2="{py1+5:.1f}"/>')
        el.append(f'<text class="xs" x="{xx:.1f}" y="{py1+19:.1f}" text-anchor="middle">{rv}</text>')

    # Commutator bound t^2/r dashed line
    bnd_pts = [(tx(1.0), ty(1.0)), (tx(100.0), ty(0.01))]
    el.append(f'<path class="guide" stroke-width="1.6" d="{poly_d(bnd_pts)}"/>')

    # S1 and S2 curves & markers
    s1_pts = [(tx(r), ty(e)) for r, e in zip(r_vals, err1)]
    s2_pts = [(tx(r), ty(e)) for r, e in zip(r_vals, err2)]
    el.append(f'<path class="c2" stroke-width="2.5" d="{poly_d(s1_pts)}"/>')
    el.append(f'<path class="c3" stroke-width="2.6" d="{poly_d(s2_pts)}"/>')
    for x, y in s1_pts:
        el.append(f'<circle class="c2-fill" cx="{x:.1f}" cy="{y:.1f}" r="3.6"/>')
    for x, y in s2_pts:
        el.append(f'<rect class="c3-fill" x="{x-3.3:.1f}" y="{y-3.3:.1f}" width="6.6" height="6.6" rx="1"/>')

    # Axes frame
    el.append(f'<rect class="axis" stroke-width="1.4" x="{px0:.1f}" y="{py0:.1f}" width="{pw:.1f}" height="{ph:.1f}"/>')
    el.append(f'<text class="smb" x="{(px0+px1)/2:.1f}" y="391" text-anchor="middle">Trotter 切片步数 r（对数坐标）</text>')
    el.append('<text class="smb" x="496" y="245" transform="rotate(-90 496 245)" text-anchor="middle">算符谱范数误差 ‖e⁻ⁱᴴᵗ − S_p‖₂</text>')

    # Clean non-overlapping callouts in upper-right & lower-left empty zones
    el.append('<rect class="pill-bg" x="742" y="145" width="170" height="42" rx="7"/>')
    el.append(f'<text class="xsb c2-txt" x="827" y="163" text-anchor="middle">一阶 S₁ 实测斜率 {slope1:.2f}</text>')
    el.append('<text class="xs" x="827" y="179" text-anchor="middle">紧贴对易子上界 t²/r</text>')

    el.append('<rect class="pill-bg" x="556" y="286" width="186" height="58" rx="7"/>')
    el.append(f'<text class="xsb c3-txt" x="649" y="304" text-anchor="middle">二阶 S₂ 实测斜率 {slope2:.2f}</text>')
    el.append(f'<text class="xs" x="649" y="321" text-anchor="middle">r=16: S₁≈{err1[4]:.3f}, S₂≈{err2[4]:.4f}</text>')
    el.append(f'<text class="xsb c1-txt" x="649" y="338" text-anchor="middle">r=100 精度提升 {err1[-1]/err2[-1]:.0f}×</text>')

    el.extend(note_bar(492, 404, 434, "S₂ 合并相邻半步仅需 2r+1 门（相对 S₁ 的 2r 仅多 1 门），误差跃升一阶"))

    svg = svg_doc(
        "Simon 异或陪集结构与 Trotter 误差双对数缩放曲线",
        "左面板展示 Simon 算法中隐藏串 s = 101 将 8 个 3 比特输入配成 4 组异或陪集，并经 H⊗³ 干涉滤出正交子空间 {000, 010, 101, 111}；右面板在双对数坐标下实算 H = X + Z (t = 1) 的一阶与二阶对称 Trotter 谱范数误差，验证斜率 −1 与 −2 缩放规律。",
        el,
    )
    return svg, {"slope1": round(slope1, 3), "slope2": round(slope2, 3), "gain_r100": round(err1[-1] / err2[-1], 1)}


# =============================================================================
# Figure 6: v4-08-chem-encoding-thc.svg
# =============================================================================
def build_fig6_chem_encoding_thc() -> tuple[str, dict[str, object]]:
    # Exact Fenwick / Bravyi-Kitaev parity matrix verification for N = 8
    n_orb = 8
    # BK lower-triangular parity-basis matrix B_8 (entry (i, j) = 1 iff qubit i includes orbital j)
    def bk_matrix(n: int) -> list[list[int]]:
        m = [[1]]
        while len(m) < n:
            k = len(m)
            nxt = [[0] * (2 * k) for _ in range(2 * k)]
            for r in range(k):
                for c in range(k):
                    nxt[r][c] = m[r][c]
                    nxt[r + k][c + k] = m[r][c]
            for c in range(k):
                nxt[2 * k - 1][c] = 1
            m = nxt
        return m

    b8 = bk_matrix(n_orb)
    # Parity of orbitals 0..6 equals q_3 ^ q_5 ^ q_6 in BK basis
    for occ in range(1 << n_orb):
        bits = [(occ >> j) & 1 for j in range(n_orb)]
        q = [sum(b8[i][j] * bits[j] for j in range(n_orb)) % 2 for i in range(n_orb)]
        prefix_par = sum(bits[:7]) % 2
        bk_par = (q[3] ^ q[5] ^ q[6]) % 2
        assert prefix_par == bk_par
    jw_weight_7 = 8
    bk_weight_7 = 4  # qubits {3, 5, 6, 7}

    el: list[str] = []
    el.extend(
        header(
            "量子化学费米子映射权重与双因子化 / THC 块编码压缩",
            "左：Jordan–Wigner 链式 O(N) vs Bravyi–Kitaev Fenwick 树 O(log₂ N)；右：四指标积分由 O(N⁴) 压至 THC 的 Õ(N)",
        )
    )

    # Left panel: JW vs BK encoding (x=20..464, w=444)
    el.extend(panel_shell(20, 68, 444, 376, "1. 费米子映射权重：JW O(N) vs BK O(log₂ N)"))

    # Upper subpanel: JW chain (y=108..194)
    el.append('<rect class="subpanel" x="34" y="108" width="416" height="86" rx="9"/>')
    el.append('<text class="xsb c2-txt" x="46" y="126">Jordan–Wigner 链式（a₇† 权重 = N = 8）：串联全部前缀 Z</text>')
    xs_q = [60.0 + i * 50.0 for i in range(8)]
    el.append(f'<line class="c2" stroke-width="2.2" x1="{xs_q[0]:.0f}" y1="154" x2="{xs_q[-1]:.0f}" y2="154"/>')
    for i, xq in enumerate(xs_q):
        is_tgt = i == 7
        bcls = "c3-soft" if is_tgt else "c2-soft"
        tcls = "xsb c3-txt" if is_tgt else "xsb c2-txt"
        lbl = "X,Y" if is_tgt else "Z"
        el.append(f'<rect class="{bcls}" x="{xq-16:.0f}" y="141" width="32" height="26" rx="5"/>')
        el.append(f'<text class="{tcls}" x="{xq:.0f}" y="158" text-anchor="middle">{lbl}</text>')
        el.append(f'<text class="xs" x="{xq:.0f}" y="184" text-anchor="middle">q{chr(0x2080+i)}</text>')

    # Middle subpanel: BK Fenwick tree (y=202..342)
    el.append('<rect class="subpanel" x="34" y="202" width="416" height="140" rx="9"/>')
    el.append('<text class="xsb c3-txt" x="46" y="220">Bravyi–Kitaev Fenwick 树（a₇† 权重 = 4，仅涉 {q₃, q₅, q₆, q₇}）</text>')

    # Fenwick levels: trailing 1-bits of index i -> height
    levels = [0, 1, 0, 2, 0, 1, 0, 3]
    ys_bk = [318.0 - lv * 24.0 for lv in levels]
    tree_edges = [(0, 1, False), (1, 3, False), (2, 3, False), (4, 5, False), (3, 7, True), (5, 7, True), (6, 7, True)]
    for u, v, active in tree_edges:
        cls = "c1" if active else "cwire"
        sw = 2.1 if active else 1.2
        dash = "" if active else ' stroke-dasharray="3 3"'
        el.append(f'<line class="{cls}" stroke-width="{sw:.1f}"{dash} x1="{xs_q[u]:.0f}" y1="{ys_bk[u]:.0f}" x2="{xs_q[v]:.0f}" y2="{ys_bk[v]:.0f}"/>')

    active_par = {3, 5, 6}
    for i, (xq, yq) in enumerate(zip(xs_q, ys_bk)):
        if i == 7:
            bcls, tcls, txt = "c3-soft", "xsb c3-txt", "7:XY"
        elif i in active_par:
            bcls, tcls, txt = "c1-soft", "xsb c1-txt", f"{i}:Z"
        else:
            bcls, tcls, txt = "pill", "xs", f"{i}:I"
        w_box = 38 if i == 7 else 32
        el.append(f'<rect class="{bcls}" x="{xq-w_box/2:.0f}" y="{yq-11:.0f}" width="{w_box}" height="22" rx="5"/>')
        el.append(f'<text class="{tcls}" x="{xq:.0f}" y="{yq+4:.0f}" text-anchor="middle">{txt}</text>')

    # Clean explanatory callout in empty top-left of BK subpanel (strictly left of q3 at x=194)
    el.append('<rect class="pill-bg" x="44" y="227" width="144" height="44" rx="7"/>')
    el.append('<text class="xsb c1-txt" x="52" y="245">P(7) = q₃ ⊕ q₅ ⊕ q₆</text>')
    el.append('<text class="xs" x="52" y="263">跳过 q₀–q₂, q₄（省半）</text>')

    # Compact 3-way mapping summary strip (y=350..394)
    cards = [
        (34, 134, "c2-soft", "c2-txt", "JW 映射", "占据局域 · 宇称 O(N)"),
        (175, 134, "c4-soft", "c4-txt", "Parity 映射", "宇称局域 · 占据 O(N)"),
        (316, 134, "c3-soft", "c3-txt", "BK 映射", "双者均衡 O(log₂ N)"),
    ]
    for cx, cw, bcls, tcls, t1, t2 in cards:
        el.append(f'<rect class="{bcls}" x="{cx}" y="350" width="{cw}" height="44" rx="7"/>')
        el.append(f'<text class="xsb {tcls}" x="{cx+cw/2:.0f}" y="367" text-anchor="middle">{t1}</text>')
        el.append(f'<text class="xs" x="{cx+cw/2:.0f}" y="385" text-anchor="middle">{t2}</text>')

    el.extend(note_bar(34, 404, 416, "BK 树形折中显著缩短泡利串长度，降低单步演化与测量电路深度"))

    # Right panel: DF / THC Tensor Compression (x=478..940, w=462)
    el.extend(panel_shell(478, 68, 462, 376, "2. 容错化学哈密顿量压缩：O(N⁴) → DF → THC Õ(N)"))

    # Tier 1: Sparse 4-index tensor (y=108..184)
    el.append('<rect class="c2-soft" x="492" y="108" width="434" height="76" rx="9"/>')
    # 4-leg tensor icon
    el.append('<line class="c2" stroke-width="1.7" x1="514" y1="126" x2="540" y2="140"/>')
    el.append('<line class="c2" stroke-width="1.7" x1="514" y1="166" x2="540" y2="152"/>')
    el.append('<line class="c2" stroke-width="1.7" x1="618" y1="126" x2="592" y2="140"/>')
    el.append('<line class="c2" stroke-width="1.7" x1="618" y1="166" x2="592" y2="152"/>')
    el.append('<rect class="pill-bg" x="536" y="132" width="60" height="28" rx="6"/>')
    el.append('<text class="xsb c2-txt" x="566" y="150" text-anchor="middle">h_pqrs</text>')
    el.append('<text class="xs c2-txt" x="506" y="128">p</text>')
    el.append('<text class="xs c2-txt" x="506" y="172">q</text>')
    el.append('<text class="xs c2-txt" x="622" y="128">r</text>')
    el.append('<text class="xs c2-txt" x="622" y="172">s</text>')
    # Tier 1 text
    el.append('<text class="smb c2-txt" x="646" y="128">① 朴素稀疏四指标积分（Sparse）</text>')
    el.append('<text class="xs" x="646" y="149">独立项数：O(N⁴)   |   1-范数 λ：O(N²–N³)</text>')
    el.append('<text class="xsb c2-txt" x="646" y="170">块编码：Õ(N²–N⁴) Toffoli（基线对照）</text>')

    # Arrow 1 -> 2
    el.extend(arrow_line(566, 185, 566, 209, stroke_cls="c1", fill_cls="c1-fill", sw=1.9, length=7.0, half_w=3.3))
    el.append('<text class="xsb c1-txt" x="580" y="202">Cholesky 分解 + 轨道酉旋转 U^(ℓ)（O(N) Givens 门）</text>')

    # Tier 2: Double Factorization (y=211..289)
    el.append('<rect class="c1-soft" x="492" y="211" width="434" height="78" rx="9"/>')
    # Split 2-node DF tensor diagram
    el.append('<line class="c1" stroke-width="2.0" x1="546" y1="248" x2="586" y2="248"/>')
    el.append('<rect class="pill-bg" x="504" y="234" width="44" height="28" rx="6"/>')
    el.append('<text class="xsb c1-txt" x="526" y="252" text-anchor="middle">L_pq</text>')
    el.append('<rect class="pill-bg" x="584" y="234" width="44" height="28" rx="6"/>')
    el.append('<text class="xsb c1-txt" x="606" y="252" text-anchor="middle">L_rs</text>')
    el.append('<text class="xsb c1-txt" x="566" y="241" text-anchor="middle">ℓ</text>')
    el.append('<text class="xs c1-txt" x="566" y="278" text-anchor="middle">L_DF = O(N)</text>')
    # Tier 2 text
    el.append('<text class="smb c1-txt" x="646" y="231">② 双因子化（DF / 正则化 RC-DF）</text>')
    el.append('<text class="xs" x="646" y="252">参数：O(N²–N³)   |   1-范数 λ：O(N^1.5)</text>')
    el.append('<text class="xsb c1-txt" x="646" y="273">块编码：Õ(N^1.5–N²) Toffoli（P450 主力）</text>')

    # Arrow 2 -> 3
    el.extend(arrow_line(566, 290, 566, 314, stroke_cls="c3", fill_cls="c3-fill", sw=1.9, length=7.0, half_w=3.3))
    el.append('<text class="xsb c3-txt" x="580" y="307">引入 M_THC = O(N) 非正交辅助格点 + 一元迭代 QROM</text>')

    # Tier 3: Tensor Hypercontraction (y=316..394)
    el.append('<rect class="c3-soft" x="492" y="316" width="434" height="78" rx="9"/>')
    # THC 3-block hypercontraction icon
    el.append('<line class="c3" stroke-width="1.9" x1="538" y1="353" x2="594" y2="353"/>')
    el.append('<rect class="pill-bg" x="502" y="340" width="38" height="26" rx="5"/>')
    el.append('<text class="xsb c3-txt" x="521" y="357" text-anchor="middle">χ_μ</text>')
    el.append('<rect class="c3-fill" x="548" y="339" width="36" height="28" rx="6"/>')
    el.append('<text class="badge-txt" x="566" y="357" text-anchor="middle">ζ_μν</text>')
    el.append('<rect class="pill-bg" x="592" y="340" width="38" height="26" rx="5"/>')
    el.append('<text class="xsb c3-txt" x="611" y="357" text-anchor="middle">χ_ν</text>')
    el.append('<text class="xs c3-txt" x="566" y="383" text-anchor="middle">双指标核 ζ_μν</text>')
    # Tier 3 text
    el.append('<text class="smb c3-txt" x="646" y="336">③ 张量超收缩（THC，渐近最优）</text>')
    el.append('<text class="xs" x="646" y="357">参数：O(N²)     |     1-范数 λ：O(N–N^1.5)</text>')
    el.append('<text class="xsb c3-txt" x="646" y="378">块编码：Õ(N) Toffoli（FeMoco ≈ 3.2×10¹⁰）</text>')

    el.extend(note_bar(492, 404, 434, "总容错 QPE 代价 ∝ λ · Cost_BE / ε；DF/THC 将开销压低数个数量级"))

    svg = svg_doc(
        "量子化学费米子编码与双因子化 THC 压缩结构",
        "左面板对比 N=8 轨道下 Jordan-Wigner 链式 O(N) 与 Bravyi-Kitaev Fenwick 树形 O(log₂ N) 的费米算符 Pauli 权重；右面板展示容错量子化学哈密顿量由朴素 O(N⁴) 经双因子化 DF 压缩至张量超收缩 THC（Õ(N) Toffoli 复杂度）的层级结构。",
        el,
    )
    return svg, {"jw_weight_7": jw_weight_7, "bk_weight_7": bk_weight_7}


# =============================================================================
# Figure 7: v4-10-color-xzzx-codes.svg
# =============================================================================
def build_fig7_color_xzzx_codes() -> tuple[str, dict[str, object]]:
    # 1. Exact 6.6.6 triangular color code generator (d=3 [[7,1,3]] and d=5 [[19,1,5]])
    s3 = math.sqrt(3.0)

    def build_666_triangle(c_cut: float) -> tuple[list[tuple[float, float]], list[tuple[int, list[tuple[float, float]]]]]:
        ox, oy = 0.5, 1.0 / (2.0 * s3)
        raw_faces = []
        for u in range(-4, 7):
            for v in range(-4, 7):
                cx = u + 0.5 * v
                cy = (s3 / 2.0) * v
                r = 1.0 / s3
                vs = [
                    (round(cx + r * math.cos(math.radians(30 + 60 * k)), 6),
                     round(cy + r * math.sin(math.radians(30 + 60 * k)), 6))
                    for k in range(6)
                ]
                raw_faces.append(((u - v) % 3, vs))
        all_v = sorted({pt for _, vs in raw_faces for pt in vs})
        kept_set = set()
        for x, y in all_v:
            dx, dy = x - ox, y - oy
            if max(dx, -0.5 * dx + (s3 / 2.0) * dy, -0.5 * dx - (s3 / 2.0) * dy) <= c_cut + 1e-4:
                kept_set.add((x, y))

        # Rotate (dx, dy) -> (dy, dx) so flat edge lies at bottom (+y in SVG) and apex points up (-y)
        def rot(pt: tuple[float, float]) -> tuple[float, float]:
            return (pt[1] - oy, pt[0] - ox)

        faces_out = []
        for col, vs in raw_faces:
            sub = [pt for pt in vs if pt in kept_set]
            if len(sub) >= 4:
                rsub = [rot(pt) for pt in sub]
                mx = sum(p[0] for p in rsub) / len(rsub)
                my = sum(p[1] for p in rsub) / len(rsub)
                rsub.sort(key=lambda p: math.atan2(p[1] - my, p[0] - mx))
                faces_out.append((col, rsub))

        verts_out = [rot(pt) for pt in sorted(kept_set)]
        # Verify pairwise even overlap (CSS self-duality condition H H^T = 0 mod 2)
        for i in range(len(faces_out)):
            si = {(round(p[0], 4), round(p[1], 4)) for p in faces_out[i][1]}
            for j in range(i + 1, len(faces_out)):
                sj = {(round(p[0], 4), round(p[1], 4)) for p in faces_out[j][1]}
                assert len(si & sj) % 2 == 0
        return verts_out, faces_out

    v3, f3 = build_666_triangle(0.5)
    v5, f5 = build_666_triangle(1.0)
    assert len(v3) == 7 and sorted(len(f[1]) for f in f3) == [4, 4, 4]
    assert len(v5) == 19 and sorted(len(f[1]) for f in f5) == [4, 4, 4, 4, 4, 4, 6, 6, 6]

    # 2. Verify XZZX d=3 commutation with pure Z_5 error (anticommutes ONLY with NW and SE faces)
    xzzx_faces = [
        ("NW", {1: "X", 2: "Z", 4: "Z", 5: "X"}),
        ("NE", {2: "X", 3: "Z", 5: "Z", 6: "X"}),
        ("SW", {4: "X", 5: "Z", 7: "Z", 8: "X"}),
        ("SE", {5: "X", 6: "Z", 8: "Z", 9: "X"}),
    ]
    lit_by_z5 = [name for name, ops in xzzx_faces if ops.get(5) == "X"]
    assert lit_by_z5 == ["NW", "SE"]

    el: list[str] = []
    el.extend(
        header(
            "二维三角颜色码三色面元与偏置噪声 XZZX 表面码对角线重复链",
            "左：d = 3 Steane [[7,1,3]] 与 d = 5 [[19,1,5]] 三角色码及三色超边；右：XZZX 表面码纯 Z 错解耦为 1D 对角重复链",
        )
    )

    # Left panel: d=3 and d=5 triangular color codes (x=20..480, w=460)
    el.extend(panel_shell(20, 68, 460, 376, "1. 二维三角颜色码：d = 3 (Steane) 与 d = 5 ([[19,1,5]])"))

    col_cls = ["cc-r", "cc-g", "cc-b"]

    def draw_color_code(
        verts: list[tuple[float, float]],
        faces: list[tuple[int, list[tuple[float, float]]]],
        cx: float, cy: float, scale: float, r_node: float
    ) -> None:
        for col, pts in faces:
            spts = [(cx + p[0] * scale, cy + p[1] * scale) for p in pts]
            pstr = " ".join(f"{x:.1f},{y:.1f}" for x, y in spts)
            el.append(f'<polygon class="{col_cls[col]}" points="{pstr}"/>')
        for px, py in verts:
            sx, sy = cx + px * scale, cy + py * scale
            is_center = math.hypot(px, py) < 1e-3
            ncls = "qnode-err" if is_center else "qnode"
            rad_n = r_node + 1.4 if is_center else r_node
            el.append(f'<circle class="{ncls}" cx="{sx:.1f}" cy="{sy:.1f}" r="{rad_n:.1f}"/>')

    # d=3 Steane [[7,1,3]] on left side
    el.append('<text class="smb c3-txt" x="116" y="124" text-anchor="middle">d = 3 Steane [[7, 1, 3]]</text>')
    el.append('<text class="xs" x="116" y="141" text-anchor="middle">3 面元（全权重 4）</text>')
    draw_color_code(v3, f3, cx=116.0, cy=252.0, scale=80.0, r_node=4.8)

    # Subtle vertical divider between d=3 and d=5
    el.append('<line class="grid" stroke-dasharray="4 4" x1="214" y1="112" x2="214" y2="318"/>')

    # d=5 [[19,1,5]] on right side
    el.append('<text class="smb c3-txt" x="344" y="124" text-anchor="middle">d = 5 三角色码 [[19, 1, 5]]</text>')
    el.append('<text class="xs" x="344" y="141" text-anchor="middle">6 边界权重 4 + 3 内部权重 6</text>')
    draw_color_code(v5, f5, cx=344.0, cy=260.0, scale=54.0, r_node=4.2)

    # Legend & structural summary card inside Left panel (y=328..394)
    el.append('<rect class="subpanel" x="34" y="328" width="432" height="66" rx="9"/>')
    el.append('<rect class="cc-r" x="46" y="339" width="14" height="12" rx="2"/>')
    el.append('<rect class="cc-g" x="65" y="339" width="14" height="12" rx="2"/>')
    el.append('<rect class="cc-b" x="84" y="339" width="14" height="12" rx="2"/>')
    el.append('<text class="xsb" x="106" y="349">红/绿/蓝面元各载 X 与 Z 稳定子（H_X = H_Z 自对偶）</text>')
    el.append('<circle class="qnode-err" cx="53" cy="368" r="4.8"/>')
    el.append('<text class="xs c2-txt" x="66" y="372">内部单比特错同时点亮 3 色面元（超边，需 Chromobius 解码）</text>')
    el.append('<text class="xs c3-txt" x="46" y="388">比特密度 (3d²+1)/4 省 ~25%；全 Clifford 横向（逻辑 S = (S†)⊗ⁿ）</text>')

    el.extend(note_bar(34, 404, 432, "二维颜色码以权重 6 校验与超边解码为代价，换取全 Clifford 群横向能力"))

    # Right panel: XZZX surface code under pure Z bias (x=492..940, w=448)
    el.extend(panel_shell(492, 68, 448, 376, "2. 偏置噪声 XZZX 表面码：纯 Z 错解耦为 1D 对角链"))

    # 3x3 rotated XZZX data lattice at x = 542, 614, 686; y = 148, 220, 292 (step 72px)
    gx0, gy0, step = 542.0, 148.0, 72.0

    # Weight-2 boundary semicircles (drawn behind plaquettes)
    # Top (1,2): Z1 X2
    el.append(f'<path class="pill" d="M {gx0:.0f} {gy0:.0f} A 36 22 0 0 1 {gx0+step:.0f} {gy0:.0f} Z"/>')
    el.append(f'<text class="xs" x="{gx0+step/2:.0f}" y="{gy0-6:.0f}" text-anchor="middle">Z₁X₂</text>')
    # Bottom (8,9): X8 Z9
    el.append(f'<path class="pill" d="M {gx0+step:.0f} {gy0+2*step:.0f} A 36 22 0 0 0 {gx0+2*step:.0f} {gy0+2*step:.0f} Z"/>')
    el.append(f'<text class="xs" x="{gx0+1.5*step:.0f}" y="{gy0+2*step+16:.0f}" text-anchor="middle">X₈Z₉</text>')
    # Right (3,6): X3 Z6
    el.append(f'<path class="pill" d="M {gx0+2*step:.0f} {gy0:.0f} A 22 36 0 0 1 {gx0+2*step:.0f} {gy0+step:.0f} Z"/>')
    el.append(f'<text class="xs" x="{gx0+2*step+11:.0f}" y="{gy0+step/2+4:.0f}" text-anchor="middle">XZ</text>')
    # Left (4,7): Z4 X7
    el.append(f'<path class="pill" d="M {gx0:.0f} {gy0+step:.0f} A 22 36 0 0 0 {gx0:.0f} {gy0+2*step:.0f} Z"/>')
    el.append(f'<text class="xs" x="{gx0-11:.0f}" y="{gy0+1.5*step+4:.0f}" text-anchor="middle">ZX</text>')

    # 4 internal weight-4 XZZX plaquettes
    plaq_defs = [
        (0, 0, True),   # NW (1,2,4,5) - LIT by Z5
        (1, 0, False),  # NE (2,3,5,6) - commutes
        (0, 1, False),  # SW (4,5,7,8) - commutes
        (1, 1, True),   # SE (5,6,8,9) - LIT by Z5
    ]
    for pc, pr, is_lit in plaq_defs:
        px = gx0 + pc * step
        py = gy0 + pr * step
        pcls = "cc-r" if is_lit else "cc-b"
        pstr = f"{px:.0f},{py:.0f} {px+step:.0f},{py:.0f} {px+step:.0f},{py+step:.0f} {px:.0f},{py+step:.0f}"
        el.append(f'<polygon class="{pcls}" points="{pstr}"/>')

    # Parallel 45-degree 1D repetition chains under pure Z noise (drawn behind badges & off-diagonal labels)
    el.append(f'<line class="c2" stroke-width="2.6" stroke-dasharray="5 4" x1="{gx0:.0f}" y1="{gy0:.0f}" x2="{gx0+2*step:.0f}" y2="{gy0+2*step:.0f}"/>')
    el.append(f'<line class="c3" stroke-width="2.0" stroke-dasharray="5 4" x1="{gx0+step:.0f}" y1="{gy0:.0f}" x2="{gx0+2*step:.0f}" y2="{gy0+step:.0f}"/>')
    el.append(f'<line class="c3" stroke-width="2.0" stroke-dasharray="5 4" x1="{gx0:.0f}" y1="{gy0+step:.0f}" x2="{gx0+step:.0f}" y2="{gy0+2*step:.0f}"/>')

    # Uniform XZZX corner Pauli labels (placed cleanly off the 45-deg NW-SE diagonals) & lit -1 badges
    for pc, pr, is_lit in plaq_defs:
        px = gx0 + pc * step
        py = gy0 + pr * step
        el.append(f'<text class="xsb c2-txt" x="{px+27:.0f}" y="{py+16:.0f}" text-anchor="middle">X</text>')
        el.append(f'<text class="xsb c1-txt" x="{px+step-14:.0f}" y="{py+20:.0f}" text-anchor="middle">Z</text>')
        el.append(f'<text class="xsb c1-txt" x="{px+14:.0f}" y="{py+step-10:.0f}" text-anchor="middle">Z</text>')
        el.append(f'<text class="xsb c2-txt" x="{px+step-27:.0f}" y="{py+step-6:.0f}" text-anchor="middle">X</text>')
        if is_lit:
            el.append(f'<circle class="c2-fill" cx="{px+step/2:.0f}" cy="{py+step/2:.0f}" r="11"/>')
            el.append(f'<text class="badge-txt" x="{px+step/2:.0f}" y="{py+step/2+4:.0f}" text-anchor="middle">−1</text>')

    # 9 data qubits q1..q9
    for idx in range(9):
        r, c = divmod(idx, 3)
        qx = gx0 + c * step
        qy = gy0 + r * step
        if idx == 4:  # q5 with pure Z_5 error
            el.append(f'<circle class="qnode-err" cx="{qx:.0f}" cy="{qy:.0f}" r="12.5"/>')
            el.append(f'<text class="badge-txt" x="{qx:.0f}" y="{qy+4:.0f}" text-anchor="middle">Z₅</text>')
        else:
            el.append(f'<circle class="qnode" cx="{qx:.0f}" cy="{qy:.0f}" r="10.5"/>')
            el.append(f'<text class="xsb" x="{qx:.0f}" y="{qy+4:.0f}" text-anchor="middle">{idx+1}</text>')

    # Right explanatory cards beside the 3x3 XZZX grid (x=726..928, w=202)
    el.append('<rect class="c2-soft" x="726" y="114" width="202" height="104" rx="9"/>')
    el.append('<text class="xsb c2-txt" x="738" y="133">纯 Z 错解耦机制（d = 3）</text>')
    el.append('<text class="xs" x="738" y="152">奇数位 {1,3,5,7,9} 施 H，</text>')
    el.append('<text class="xs" x="738" y="169">内部稳定子全变 XZZX 面元。</text>')
    el.append('<text class="xs" x="738" y="187">Z₅ 仅点亮 NW/SE 对角两面</text>')
    el.append('<text class="xsb c2-txt" x="738" y="206">（与 NE/SW 面元严格对易）</text>')

    el.append('<rect class="c3-soft" x="726" y="226" width="202" height="104" rx="9"/>')
    el.append('<text class="xsb c3-txt" x="738" y="245">1D 对角重复链与 50% 阈值</text>')
    el.append('<text class="xs" x="738" y="264">纯 Z 偏置（η = p_Z/p_X → ∞）</text>')
    el.append('<text class="xs" x="738" y="282">将二维格解耦为 d 条 45° 链：</text>')
    el.append('<text class="xsb c3-txt" x="738" y="301">码容量阈值飙升至 50%</text>')
    el.append('<text class="xs" x="738" y="319">（常规去极化表面码 ~10.9%）</text>')

    # Bottom caveat strip
    el.append('<rect class="subpanel" x="506" y="340" width="422" height="54" rx="9"/>')
    el.append('<text class="xsb c1-txt" x="518" y="359">硬前提——偏置保持门（Bias-Preserving Gates）：</text>')
    el.append('<text class="xs" x="518" y="379">校验门电路不得将 Z 错转化为 X 错（如猫态比特 CX），否则高阈值瓦解</text>')

    el.extend(note_bar(506, 404, 422, "纯 Z 偏置下 XZZX 表面码解耦为 1D 对角重复链，码容量阈值逼近 50%"))

    svg = svg_doc(
        "二维颜色码几何与偏置噪声 XZZX 表面码对角线重复链",
        "左面板对比 d=3 Steane [[7,1,3]] 与 d=5 [[19,1,5]] 三角颜色码的红绿蓝三着色面元及内部三色超边结构；右面板展示奇数位施加 Hadamard 后的 d=3 旋转 XZZX 表面码，中心 Z₅ 错仅点亮 45° 对角线两面元，纯 Z 偏置下解耦为 1D 对角线重复链并将码容量阈值推至 50%。",
        el,
    )
    return svg, {"d3_n": len(v3), "d5_n": len(v5), "xzzx_z5_lit": lit_by_z5}


# =============================================================================
# XML + Chromium Dual-Theme getBBox() Verification
# =============================================================================
def verify_svg_xml(svg_text: str, filename: str) -> dict[str, int]:
    root = ET.fromstring(svg_text)
    assert root.tag == "{http://www.w3.org/2000/svg}svg", f"{filename}: bad root tag"
    assert root.attrib.get("viewBox") == f"0 0 {W} {H}", f"{filename}: wrong viewBox"
    assert ":root{color-scheme:light dark}" in svg_text, f"{filename}: missing color-scheme"
    assert "@media (prefers-color-scheme: dark)" in svg_text, f"{filename}: missing dark media query"

    ns = {"svg": "http://www.w3.org/2000/svg"}
    title_el = root.find("svg:title", ns)
    desc_el = root.find("svg:desc", ns)
    assert title_el is not None and (title_el.text or "").strip(), f"{filename}: missing <title>"
    assert desc_el is not None and (desc_el.text or "").strip(), f"{filename}: missing <desc>"

    text_nodes = root.findall(".//svg:text", ns)
    assert len(text_nodes) >= 12, f"{filename}: too few text nodes"
    for el in text_nodes:
        x = float(el.attrib["x"])
        y = float(el.attrib["y"])
        assert MARGIN <= x <= W - MARGIN, f"{filename}: text x={x} OOB ({el.text!r})"
        assert MARGIN <= y <= H - MARGIN, f"{filename}: text y={y} OOB ({el.text!r})"

    return {"text_count": len(text_nodes), "bytes": len(svg_text.encode("utf-8"))}


def verify_with_chromium_bbox(svg_paths: list[Path], screenshot_dir: Path | None = None) -> None:
    """Audit rendered <text> bounding boxes and font-sizes in System Chrome (light & dark)."""
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
        const fs = parseFloat(window.getComputedStyle(el).fontSize || '0');
        return {
          idx,
          text: (el.textContent || '').trim(),
          cls: el.getAttribute('class') || '',
          fontSize: fs,
          ...b,
          cx: 0.5 * (b.x1 + b.x2),
          cy: 0.5 * (b.y1 + b.y2),
          rotated: (el.getAttribute('transform') || '').includes('rotate'),
        };
      });
      const minFont = Math.min(...texts.map(t => t.fontSize));
      const smallFonts = texts.filter(t => t.fontSize < 11.49);
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
      const frameClasses = new Set([
        'panel', 'subpanel', 'note', 'pill', 'pill-bg',
        'c1-soft', 'c2-soft', 'c3-soft', 'c4-soft', 'c5-soft'
      ]);
      const rects = Array.from(svg.querySelectorAll('rect')).filter(el => {
        const clsList = (el.getAttribute('class') || '').split(/\\s+/);
        if (!clsList.some(c => frameClasses.has(c))) return false;
        const w = parseFloat(el.getAttribute('width') || '0');
        const h = parseFloat(el.getAttribute('height') || '0');
        return w >= 24 && h >= 18;
      }).map(el => ({ cls: el.getAttribute('class') || '', ...toBox(el) }));
      const piercings = [];
      for (const t of texts) {
        if (t.rotated) continue;
        for (const r of rects) {
          const centerInside = t.cx > r.x1 && t.cx < r.x2 && t.cy > r.y1 && t.cy < r.y2;
          const ox = Math.min(t.x2, r.x2) - Math.max(t.x1, r.x1);
          const oy = Math.min(t.y2, r.y2) - Math.max(t.y1, r.y1);
          if (centerInside) {
            const maxSpill = Math.max(r.x1 - t.x1, t.x2 - r.x2, r.y1 - t.y1, t.y2 - r.y2);
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
            piercings.push({ kind: 'cross-border', text: t.text, rectCls: r.cls, ox: Number(ox.toFixed(1)), oy: Number(oy.toFixed(1)) });
          }
        }
      }
      return { count: texts.length, minFont, smallFonts, oob, overlaps, piercings };
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
                        f"minFont={res['minFont']:.1f}px | oob={len(res['oob'])} "
                        f"overlaps={len(res['overlaps'])} piercings={len(res['piercings'])}"
                    )
                    for item in res["smallFonts"]:
                        print(f"  [SMALL-FONT] {item['text']!r}: {item['fontSize']}px")
                    for item in res["oob"]:
                        print(f"  [OOB] {item['text']!r}: ({item['x1']:.1f},{item['y1']:.1f})..({item['x2']:.1f},{item['y2']:.1f})")
                    for item in res["overlaps"]:
                        print(f"  [OVERLAP] {item['a']!r} <-> {item['b']!r} (ox={item['ox']}, oy={item['oy']})")
                    for item in res["piercings"]:
                        print(f"  [PIERCE] {item}")
                    if screenshot_dir is not None:
                        screenshot_dir.mkdir(parents=True, exist_ok=True)
                        page.screenshot(path=str(screenshot_dir / f"{svg_path.stem}-{scheme}.png"))
                    if res["smallFonts"] or res["oob"] or res["overlaps"] or res["piercings"]:
                        failures.append(
                            f"{svg_path.name}({scheme}): small={len(res['smallFonts'])}, "
                            f"oob={len(res['oob'])}, overlaps={len(res['overlaps'])}, piercings={len(res['piercings'])}"
                        )
            assert not failures, "Audit failures: " + "; ".join(failures)
        finally:
            browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate 7 V4 scientific SVG figures (Part 1).")
    parser.add_argument("--check-bbox", action="store_true", help="Run System Chrome getBBox() dual-theme audit.")
    parser.add_argument("--screenshots", type=Path, default=None, help="Directory to save light/dark PNG previews.")
    args = parser.parse_args()

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    builders = [
        ("v4-01-tensor-partial-trace.svg", build_fig1_tensor_partial_trace),
        ("v4-03-schmidt-entanglement-tree.svg", build_fig2_schmidt_entanglement_tree),
        ("v4-04-toffoli-superdense.svg", build_fig3_toffoli_superdense),
        ("v4-06-aa-prepare-select.svg", build_fig4_aa_prepare_select),
        ("v4-07-simon-trotter.svg", build_fig5_simon_trotter),
        ("v4-08-chem-encoding-thc.svg", build_fig6_chem_encoding_thc),
        ("v4-10-color-xzzx-codes.svg", build_fig7_color_xzzx_codes),
    ]

    out_paths: list[Path] = []
    for fname, fn in builders:
        svg_text, metrics = fn()
        check = verify_svg_xml(svg_text, fname)
        out_path = ASSETS_DIR / fname
        out_path.write_text(svg_text, encoding="utf-8")
        out_paths.append(out_path)
        print(f"[OK] {fname}: {check['bytes']} bytes, {check['text_count']} text nodes | metrics={metrics}")

    if args.check_bbox or args.screenshots is not None:
        verify_with_chromium_bbox(out_paths, screenshot_dir=args.screenshots)


if __name__ == "__main__":
    main()
