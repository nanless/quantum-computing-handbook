#!/usr/bin/env python3
"""Generate seven light/dark adaptive textbook SVG figures (V3 Part 2, Ch 09/11/12/14/15).

Run:
    python3 codes/practice/generate_v3_figures_part2.py

Dependencies:
    Python 3 standard library only (cmath, html, math, pathlib, xml.etree.ElementTree).
    Deterministic analytical and numerical calculations (no RNG / no network / no cloud services).

Outputs (under handbook/assets/):
    1. v3-09-hardware-tradeoff-map.svg         (Ch 09: t_g vs T_2 log-log map & photonic eta^N avalanche)
    2. v3-09-entangling-gates-six-platforms.svg (Ch 09: 6-platform physical entangling gate mechanisms)
    3. v3-11-benchmark-scaling-eplg.svg        (Ch 11: RB P(m)=Aα^m+B, (1-r)^G, 100Q LF & PEC ceiling)
    4. v3-11-ftqc-resource-budget.svg          (Ch 11: Surface code d=3..31 scaling & RSA-2048 2021 vs 2025)
    5. v3-12-lwe-lattice-repeaters.svg         (Ch 12: LWE mod q=17 decoding ring & 1G/2G/3G 1000 km latency)
    6. v3-14-weyl-chamber-zx.svg               (Ch 14: SU(4) Weyl chamber tetrahedron & ZX rewrite rules)
    7. v3-15-wilson-wald-drift.svg             (Ch 15: N=100 Wald/Wilson/CP coverage & 10-batch drift)

Verification & Boundaries:
    Every figure performs built-in analytical / algebraic / exact-binomial assertions
    and parses every emitted SVG via xml.etree.ElementTree.
    All coordinates use viewBox="0 0 1000 580" with pure <text> elements (no pathified text)
    and CSS @media (prefers-color-scheme: dark) light/dark theme adaptation.
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


def sub(txt: str, size: float = 9.2) -> str:
    return f'<tspan dy="3" font-size="{size}">{esc(txt)}</tspan><tspan dy="-3">&#8203;</tspan>'


def sup(txt: str, size: float = 9.2) -> str:
    return f'<tspan dy="-4.5" font-size="{size}">{esc(txt)}</tspan><tspan dy="4.5">&#8203;</tspan>'


def arrow_poly(x1: float, y1: float, x2: float, y2: float, length: float = 9.0, width: float = 5.4) -> str:
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy)
    assert norm > 1e-9, "Zero-length arrow"
    ux, uy = dx / norm, dy / norm
    px, py = -uy, ux
    bx, by = x2 - length * ux, y2 - length * uy
    p1x, p1y = bx + (width / 2.0) * px, by + (width / 2.0) * py
    p2x, p2y = bx - (width / 2.0) * px, by - (width / 2.0) * py
    return f"M{x2:.2f} {y2:.2f}L{p1x:.2f} {p1y:.2f}L{p2x:.2f} {p2y:.2f}Z"


def clip_line_to_rect(
    x1: float, y1: float, x2: float, y2: float, xmin: float, ymin: float, xmax: float, ymax: float
) -> tuple[float, float, float, float] | None:
    """Liang-Barsky line clipping against an axis-aligned rectangle."""
    dx, dy = x2 - x1, y2 - y1
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x1 - xmin), (dx, xmax - x1), (-dy, y1 - ymin), (dy, ymax - y1)):
        if abs(p) < 1e-12:
            if q < 0:
                return None
        else:
            r = q / p
            if p < 0:
                if r > t1:
                    return None
                if r > t0:
                    t0 = r
            else:
                if r < t0:
                    return None
                if r < t1:
                    t1 = r
    return x1 + t0 * dx, y1 + t0 * dy, x1 + t1 * dx, y1 + t1 * dy


def polyline_d(pts: list[tuple[float, float]]) -> str:
    return "".join(f'{"M" if i == 0 else "L"}{x:.2f} {y:.2f}' for i, (x, y) in enumerate(pts))


def base_style(extra_light: str = "", extra_dark: str = "") -> str:
    return f"""  <style>
    :root{{color-scheme:light dark}}
    .bg{{fill:#f8fafc}}
    .card{{fill:#ffffff;stroke:#cbd8e4;stroke-width:1.6}}
    .subcard{{fill:#f2f6fa;stroke:#d2dee9;stroke-width:1.2}}
    .pill{{fill:#ffffff;fill-opacity:.96;stroke:#8fa6ba;stroke-width:1.2}}
    .ink{{fill:#13263a}}
    .muted{{fill:#496176}}
    .accent{{fill:#0e6b8a}}
    .warn{{fill:#b93c3c}}
    .gold{{fill:#9c6510}}
    .purple{{fill:#5b42a6}}
    .green{{fill:#1d7557}}
    .axis{{stroke:#2b465e;stroke-width:1.6;fill:none}}
    .axishead{{fill:#2b465e}}
    .grid{{stroke:#dce6ef;stroke-width:1;stroke-dasharray:4 4;fill:none}}
    .divider{{stroke:#c6d5e2;stroke-width:1.2;stroke-dasharray:5 4;fill:none}}
    .s-accent{{stroke:#0e6b8a;fill:none}}
    .s-warn{{stroke:#c04040;fill:none}}
    .s-gold{{stroke:#a8640b;fill:none}}
    .s-purple{{stroke:#5b42a6;fill:none}}
    .s-green{{stroke:#1d7557;fill:none}}
    .s-muted{{stroke:#688299;fill:none}}
    .f-accent{{fill:#bae6fd;fill-opacity:.48;stroke:#0e6b8a;stroke-width:1.8}}
    .f-warn{{fill:#fecaca;fill-opacity:.50;stroke:#c04040;stroke-width:1.8}}
    .f-gold{{fill:#fde68a;fill-opacity:.52;stroke:#a8640b;stroke-width:1.8}}
    .f-purple{{fill:#ddd6fe;fill-opacity:.50;stroke:#5b42a6;stroke-width:1.8}}
    .f-green{{fill:#bbf7d0;fill-opacity:.50;stroke:#1d7557;stroke-width:1.8}}
    .b-accent{{fill:#0e6b8a;fill-opacity:.82;stroke:#0a5068;stroke-width:1.4}}
    .b-warn{{fill:#c04040;fill-opacity:.82;stroke:#962b2b;stroke-width:1.4}}
    .b-gold{{fill:#c47a14;fill-opacity:.82;stroke:#8f5609;stroke-width:1.4}}
    .b-purple{{fill:#6448b5;fill-opacity:.82;stroke:#483287;stroke-width:1.4}}
    .b-green{{fill:#1d7557;fill-opacity:.82;stroke:#13543e;stroke-width:1.4}}
    .wire{{stroke:#1d3b54;stroke-width:2.0;fill:none}}
    .ctrl{{fill:#13263a}}
    .dot-ring{{stroke:#ffffff;stroke-width:1.5}}
    .title{{font:700 19.5px 'PingFang SC','Noto Sans SC',system-ui,'STIX Two Math','Cambria Math','Apple Symbols',sans-serif}}
    .subtitle{{font:400 13.2px 'PingFang SC','Noto Sans SC',system-ui,'STIX Two Math','Cambria Math','Apple Symbols',sans-serif}}
    .h2{{font:600 14px 'PingFang SC','Noto Sans SC',system-ui,'STIX Two Math','Cambria Math','Apple Symbols',sans-serif}}
    .lbl{{font:500 12.8px 'PingFang SC','Noto Sans SC',system-ui,'STIX Two Math','Cambria Math','Apple Symbols',sans-serif}}
    .sm{{font:400 12px 'PingFang SC','Noto Sans SC',system-ui,'STIX Two Math','Cambria Math','Apple Symbols',sans-serif}}
    .xs{{font:400 11px 'PingFang SC','Noto Sans SC',system-ui,'STIX Two Math','Cambria Math','Apple Symbols',sans-serif}}
    .mono{{font:500 11.8px 'SFMono-Regular',Menlo,Consolas,monospace}}
    .gate-txt{{font:700 13.5px Georgia,'Times New Roman',serif}}
    {extra_light}
    @media(prefers-color-scheme:dark){{
      .bg{{fill:#101820}}
      .card{{fill:#162330;stroke:#395066}}
      .subcard{{fill:#1d2e3d;stroke:#3d566d}}
      .pill{{fill:#14212c;fill-opacity:.96;stroke:#6d8ba3}}
      .ink{{fill:#eef6ff}}
      .muted{{fill:#b4c8da}}
      .accent{{fill:#6ed0f7}}
      .warn{{fill:#ff8585}}
      .gold{{fill:#f2c15a}}
      .purple{{fill:#c0adff}}
      .green{{fill:#6dd4aa}}
      .axis{{stroke:#b9d0e2}}
      .axishead{{fill:#b9d0e2}}
      .grid{{stroke:#304659}}
      .divider{{stroke:#4a637a}}
      .s-accent{{stroke:#6ed0f7}}
      .s-warn{{stroke:#ff8585}}
      .s-gold{{stroke:#f2c15a}}
      .s-purple{{stroke:#c0adff}}
      .s-green{{stroke:#6dd4aa}}
      .s-muted{{stroke:#8ca5ba}}
      .f-accent{{fill:#17506e;fill-opacity:.58;stroke:#6ed0f7}}
      .f-warn{{fill:#5c2228;fill-opacity:.60;stroke:#ff8585}}
      .f-gold{{fill:#5a4318;fill-opacity:.60;stroke:#f2c15a}}
      .f-purple{{fill:#372863;fill-opacity:.60;stroke:#c0adff}}
      .f-green{{fill:#174a3a;fill-opacity:.60;stroke:#6dd4aa}}
      .b-accent{{fill:#2e8eb3;fill-opacity:.88;stroke:#6ed0f7}}
      .b-warn{{fill:#c84b4b;fill-opacity:.88;stroke:#ff8585}}
      .b-gold{{fill:#b87e1b;fill-opacity:.88;stroke:#f2c15a}}
      .b-purple{{fill:#7a5cc7;fill-opacity:.88;stroke:#c0adff}}
      .b-green{{fill:#288c68;fill-opacity:.88;stroke:#6dd4aa}}
      .wire{{stroke:#c9deee}}
      .ctrl{{fill:#eef6ff}}
      .dot-ring{{stroke:#162330}}
      {extra_dark}
    }}
  </style>"""


def wrap_svg(
    svg_id: str, title: str, desc: str, body: str, extra_light: str = "", extra_dark: str = "", defs: str = ""
) -> str:
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


def matmul(a: list[list[complex]], b: list[list[complex]]) -> list[list[complex]]:
    n, m, p = len(a), len(b), len(b[0])
    assert len(a[0]) == m
    return [[sum(a[i][k] * b[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def kron(a: list[list[complex]], b: list[list[complex]]) -> list[list[complex]]:
    ra, ca, rb, cb = len(a), len(a[0]), len(b), len(b[0])
    return [[a[i // rb][j // cb] * b[i % rb][j % cb] for j in range(ca * cb)] for i in range(ra * rb)]


def binom_pmf(n: int, k: int, p: float) -> float:
    if p <= 0.0:
        return 1.0 if k == 0 else 0.0
    if p >= 1.0:
        return 1.0 if k == n else 0.0
    return math.exp(
        math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * math.log(p) + (n - k) * math.log(1.0 - p)
    )


# ===========================================================================
# Figure 1: v3-09-hardware-tradeoff-map.svg
# ===========================================================================
def build_fig1_hardware_tradeoff_map() -> tuple[str, dict]:
    # Mathematical assertions for photonic survival & ratio boundaries
    etas = [(0.999, "green", ""), (0.995, "accent", "7 4"), (0.99, "gold", "8 3 2 3"), (0.90, "warn", "3 3")]
    surv_100 = {e: e ** 100 for e, _, _ in etas}
    assert abs(surv_100[0.999] - 0.9047921471137089) < 1e-9
    assert abs(surv_100[0.995] - 0.6057704364907278) < 1e-9
    assert abs(surv_100[0.99] - 0.3660323412732292) < 1e-9
    assert abs(surv_100[0.90] - 2.6561398887587476e-5) < 1e-12

    parts = [
        '  <text class="title ink" x="34" y="44">六大硬件路线门时长–相干时间双对数相图与光子存活雪崩</text>',
        f'  <text class="subtitle muted" x="34" y="68">左：典型双比特门时长 t{sub("g")} 与回波相干时间 T{sub("2")} 双对数对照（斜虚线为 T{sub("2")}/t{sub("g")}）；右：N 颗光子全存活概率 η{sup("N")}</text>',
    ]

    # --- Left Panel: Log-Log Map ---
    lx0, ly0, lw, lh = 32, 84, 548, 446
    parts.append(f'  <rect class="card" x="{lx0}" y="{ly0}" width="{lw}" height="{lh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{lx0 + 16}" y="{ly0 + 24}">(a) 门时长 t{sub("g")} vs 相干时间 T{sub("2")}（双对数相图）</text>')

    px, py, pw, ph = 110.0, 126.0, 448.0, 314.0
    x_min, x_max = -9.0, -3.0  # 1 ns to 1 ms
    y_min, y_max = -5.0, 2.0   # 10 us to 100 s

    def sx(log_t: float) -> float:
        return px + (log_t - x_min) / (x_max - x_min) * pw

    def sy(log_t2: float) -> float:
        return py + ph - (log_t2 - y_min) / (y_max - y_min) * ph

    # Grid & ticks
    x_ticks = [(-9, "1 ns"), (-8, "10 ns"), (-7, "100 ns"), (-6, "1 μs"), (-5, "10 μs"), (-4, "100 μs"), (-3, "1 ms")]
    y_ticks = [(-5, "10 μs"), (-4, "100 μs"), (-3, "1 ms"), (-2, "10 ms"), (-1, "100 ms"), (0, "1 s"), (1, "10 s"), (2, "100 s")]
    for xv, lbl in x_ticks:
        gx = sx(xv)
        parts.append(f'  <line class="grid" x1="{gx:.1f}" y1="{py:.1f}" x2="{gx:.1f}" y2="{py + ph:.1f}"/>')
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{gx:.1f}" y1="{py + ph:.1f}" x2="{gx:.1f}" y2="{py + ph + 5:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{gx:.1f}" y="{py + ph + 22:.1f}" text-anchor="middle">{lbl}</text>')
    for yv, lbl in y_ticks:
        gy = sy(yv)
        parts.append(f'  <line class="grid" x1="{px:.1f}" y1="{gy:.1f}" x2="{px + pw:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{px - 5:.1f}" y1="{gy:.1f}" x2="{px:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{px - 9:.1f}" y="{gy + 4:.1f}" text-anchor="end">{lbl}</text>')

    # Iso-ratio diagonal lines T_2 / t_g = 10^k (k = 2, 3, 4, 5)
    for k in (2, 3, 4, 5):
        clipped = clip_line_to_rect(sx(x_min), sy(x_min + k), sx(x_max), sy(x_max + k), px, py, px + pw, py + ph)
        assert clipped is not None
        cx1, cy1, cx2, cy2 = clipped
        parts.append(f'  <line class="s-muted" style="stroke-width:1.3;stroke-dasharray:6 4;stroke-opacity:.85" x1="{cx1:.1f}" y1="{cy1:.1f}" x2="{cx2:.1f}" y2="{cy2:.1f}"/>')
        ly_lbl = sy(-3.0 + k) + (15.0 if k == 5 else 13.0)
        tag = f"T{sub('2')}/t{sub('g')}=10{sup(str(k))}" if k == 5 else f"10{sup(str(k))}"
        parts.append(f'  <text class="xs muted" x="{px + pw - 5:.1f}" y="{ly_lbl:.1f}" text-anchor="end">{tag}</text>')

    # Photonic vertical strip (~1-3 ns optical path, loss-limited)
    ph_w = sx(-8.52) - px
    parts.append(f'  <rect class="f-accent" style="fill-opacity:.22;stroke-dasharray:4 3;stroke-width:1.3" x="{px:.1f}" y="{py:.1f}" width="{ph_w:.1f}" height="{ph:.1f}"/>')
    parts.append(f'  <rect class="pill" x="{px + 8:.1f}" y="{py + 8:.1f}" width="142" height="44" rx="7"/>')
    parts.append(f'  <text class="xs accent" style="font-weight:600" x="{px + 15:.1f}" y="{py + 24:.1f}">光子（~ns 级光路）</text>')
    parts.append(f'  <text class="xs muted" x="{px + 15:.1f}" y="{py + 44:.1f}">受损耗 η{sup("N")} 截断 → 见(b)</text>')

    # Platform regions from Ch09 §5.1 table
    # 1. Neutral atoms: 200-300 ns, 1-12 s
    na_x1, na_x2 = sx(math.log10(2e-7)) - 4, sx(math.log10(3e-7)) + 4
    na_y1, na_y2 = sy(math.log10(12.0)), sy(0.0)
    parts.append(f'  <rect class="f-green" x="{na_x1:.1f}" y="{na_y1:.1f}" width="{na_x2 - na_x1:.1f}" height="{na_y2 - na_y1:.1f}" rx="6"/>')
    parts.append(f'  <text class="xs green" style="font-weight:700" x="{na_x1 - 8:.1f}" y="{na_y1 + 29:.1f}" text-anchor="end">中性原子（光镊钟态）</text>')
    parts.append(f'  <text class="xs muted" x="{na_x1 - 8:.1f}" y="{na_y1 + 48:.1f}" text-anchor="end">200–300 ns · 1–12 s</text>')

    # 2. Trapped ions: 10-100 us, 1-60 s
    ti_x1, ti_x2 = sx(-5.0), sx(-4.0)
    ti_y1, ti_y2 = sy(math.log10(60.0)), sy(0.0)
    parts.append(f'  <rect class="f-gold" x="{ti_x1:.1f}" y="{ti_y1:.1f}" width="{ti_x2 - ti_x1:.1f}" height="{ti_y2 - ti_y1:.1f}" rx="8"/>')
    ti_cx = 0.5 * (ti_x1 + ti_x2)
    parts.append(f'  <text class="xs gold" style="font-weight:700" x="{ti_cx:.1f}" y="{ti_y1 + 23:.1f}" text-anchor="middle">离子阱</text>')
    parts.append(f'  <text class="xs ink" x="{ti_cx:.1f}" y="{ti_y1 + 42:.1f}" text-anchor="middle">10–100 μs</text>')
    parts.append(f'  <text class="xs muted" x="{ti_cx:.1f}" y="{ti_y1 + 61:.1f}" text-anchor="middle">1–60 s</text>')

    # 3. Silicon spin (28Si): 20-200 ns, 0.5-20 ms
    si_x1, si_x2 = sx(math.log10(2e-8)), sx(math.log10(2e-7))
    si_y1, si_y2 = sy(math.log10(0.02)), sy(math.log10(5e-4))
    parts.append(f'  <rect class="f-purple" style="stroke-dasharray:5 3" x="{si_x1:.1f}" y="{si_y1:.1f}" width="{si_x2 - si_x1:.1f}" height="{si_y2 - si_y1:.1f}" rx="8"/>')
    parts.append(f'  <text class="xs purple" style="font-weight:700" x="{si_x2 + 8:.1f}" y="{si_y1 + 11:.1f}">硅自旋 {sup("28")}Si</text>')
    parts.append(f'  <text class="xs muted" x="{si_x2 + 8:.1f}" y="{si_y1 + 31:.1f}">20–200 ns · 0.5–20 ms</text>')

    # 4. Superconducting Fluxonium point marker (50-150 ns, 1-4 ms)
    fl_x, fl_y = sx(math.log10(1e-7)), sy(math.log10(2e-3))
    parts.append(f'  <path class="b-accent" d="M{fl_x:.1f} {fl_y - 6:.1f}L{fl_x + 6:.1f} {fl_y:.1f}L{fl_x:.1f} {fl_y + 6:.1f}L{fl_x - 6:.1f} {fl_y:.1f}Z"/>')
    parts.append(f'  <line class="s-accent" style="stroke-width:1.2" x1="{fl_x - 6:.1f}" y1="{fl_y - 4:.1f}" x2="188" y2="282"/>')
    parts.append(f'  <text class="xs accent" style="font-weight:600" x="116" y="257">Fluxonium</text>')
    parts.append(f'  <text class="xs muted" x="116" y="276">50–150 ns · 1–4 ms</text>')

    # 5. Superconducting Transmon: 20-100 ns, 100-300 us
    tr_x1, tr_x2 = sx(math.log10(2e-8)), sx(math.log10(1e-7))
    tr_y1, tr_y2 = sy(math.log10(3e-4)), sy(math.log10(1e-4))
    parts.append(f'  <rect class="f-accent" x="{tr_x1:.1f}" y="{tr_y1:.1f}" width="{tr_x2 - tr_x1:.1f}" height="{tr_y2 - tr_y1:.1f}" rx="6"/>')
    parts.append(f'  <text class="xs accent" style="font-weight:700" x="{tr_x2 + 8:.1f}" y="{tr_y1 + 12:.1f}">超导 Transmon</text>')
    parts.append(f'  <text class="xs muted" x="{tr_x2 + 8:.1f}" y="{tr_y1 + 31:.1f}">20–100 ns · 100–300 μs</text>')

    # 6. Topological candidate (parity readout ~3.7 us, residence >1 ms; no gate data)
    tp_x, tp_y = sx(math.log10(3.7e-6)), sy(-3.0)
    parts.append(f'  <path class="f-warn" style="stroke-dasharray:3 2" d="M{tp_x:.1f} {tp_y - 7:.1f}L{tp_x + 7:.1f} {tp_y:.1f}L{tp_x:.1f} {tp_y + 7:.1f}L{tp_x - 7:.1f} {tp_y:.1f}Z"/>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{tp_x + 12:.1f}" y="{tp_y - 4:.1f}">拓扑候选（尚无门数据）</text>')
    parts.append(f'  <text class="xs muted" x="{tp_x + 12:.1f}" y="{tp_y + 15:.1f}">宇称读出 ~3.7 μs, &gt;1 ms</text>')

    # Plot frame & axis labels
    parts.append(f'  <rect class="axis" x="{px:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}"/>')
    parts.append(f'  <text class="lbl ink" x="{px + pw / 2:.1f}" y="{py + ph + 44:.1f}" text-anchor="middle">典型双比特门时长 t{sub("g")}（对数刻度）</text>')
    parts.append(
        f'  <text class="lbl ink" x="50" y="{py + ph / 2:.1f}" text-anchor="middle" '
        f'transform="rotate(-90 50 {py + ph / 2:.1f})">典型回波相干时间 T{sub("2")}（对数刻度）</text>'
    )
    parts.append(f'  <text class="xs muted" x="{lx0 + 16}" y="{ly0 + lh - 12}">注：离子阱与中性原子搬运时钟为 ms 级；拓扑仅标出射频宇称读出时间与驻留寿命。</text>')

    # --- Right Panel: Photonic Survival Avalanche ---
    rx0, ry0, rw, rh = 596, 84, 372, 446
    parts.append(f'  <rect class="card" x="{rx0}" y="{ry0}" width="{rw}" height="{rh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{rx0 + 16}" y="{ry0 + 24}">(b) 光子全存活概率 η{sup("N")} 指数雪崩</text>')

    rpx, rpy, rpw, rph = 660.0, 126.0, 288.0, 314.0

    def rsx(n_val: float) -> float:
        return rpx + (n_val / 100.0) * rpw

    def rsy(prob: float) -> float:
        return rpy + rph - prob * rph

    for nv in (0, 20, 40, 60, 80, 100):
        gx = rsx(nv)
        parts.append(f'  <line class="grid" x1="{gx:.1f}" y1="{rpy:.1f}" x2="{gx:.1f}" y2="{rpy + rph:.1f}"/>')
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{gx:.1f}" y1="{rpy + rph:.1f}" x2="{gx:.1f}" y2="{rpy + rph + 5:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{gx:.1f}" y="{rpy + rph + 19:.1f}" text-anchor="middle">{nv}</text>')
    for pv in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        gy = rsy(pv)
        parts.append(f'  <line class="grid" x1="{rpx:.1f}" y1="{gy:.1f}" x2="{rpx + rpw:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{rpx - 5:.1f}" y1="{gy:.1f}" x2="{rpx:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{rpx - 9:.1f}" y="{gy + 4:.1f}" text-anchor="end">{int(round(pv * 100))}%</text>')

    # Plot curves N=1..100
    for eta, col, dash in etas:
        pts = [(rsx(n), rsy(eta ** n)) for n in range(1, 101)]
        dash_attr = f';stroke-dasharray:{dash}' if dash else ""
        parts.append(f'  <path class="s-{col}" style="stroke-width:2.6{dash_attr}" d="{polyline_d(pts)}"/>')
        ex, ey = pts[-1]
        if eta >= 0.99:
            parts.append(f'  <circle class="{col} dot-ring" cx="{ex:.1f}" cy="{ey:.1f}" r="4.2"/>')

    # Non-overlapping direct labels (strictly off curves)
    parts.append(f'  <text class="xs green" style="font-weight:700" x="{rsx(96):.1f}" y="{rsy(0.999**100) + 18:.1f}" text-anchor="end">η=0.999 → 90.5%</text>')
    parts.append(f'  <text class="xs accent" style="font-weight:700" x="{rsx(97):.1f}" y="{rsy(0.995**100) - 46:.1f}" text-anchor="end">η=0.995 → 60.6%</text>')
    parts.append(f'  <text class="xs gold" style="font-weight:700" x="{rsx(68):.1f}" y="{rsy(0.99**100) + 22:.1f}" text-anchor="end">η=0.990 → 36.6%</text>')
    parts.append(f'  <circle class="warn dot-ring" cx="{rsx(25):.1f}" cy="{rsy(0.90**25):.1f}" r="3.6"/>')
    parts.append(f'  <text class="xs warn" style="font-weight:600" x="{rsx(29):.1f}" y="{rsy(0.90**25) - 6:.1f}">η=0.90（N=100: 2.7×10{sup("-5")}）</text>')

    parts.append(f'  <rect class="axis" x="{rpx:.1f}" y="{rpy:.1f}" width="{rpw:.1f}" height="{rph:.1f}"/>')
    parts.append(f'  <text class="lbl ink" x="{rpx + rpw / 2:.1f}" y="{rpy + rph + 44:.1f}" text-anchor="middle">独立光子规模 N（颗）</text>')
    parts.append(
        f'  <text class="lbl ink" x="614" y="{rpy + rph / 2:.1f}" text-anchor="middle" '
        f'transform="rotate(-90 614 {rpy + rph / 2:.1f})">全存活概率 η{sup("N")}（%）</text>'
    )
    parts.append(f'  <text class="xs muted" x="{rx0 + 16}" y="{ry0 + rh - 12}">N=100：端到端 η 仅降 1% 即跌至 36.6%，需常数深度融合。</text>')

    parts.append('  <text class="sm muted" x="34" y="554">注：相干时间与门时长跨越 7 个数量级，硬件路线间存在固有权衡；光子路线核心红线为端到端损耗指数惩罚 ηᴺ。</text>')

    svg = wrap_svg(
        "v3-09-hardware-tradeoff-map",
        "六大硬件路线门时长与相干时间双对数相图及光子存活雪崩",
        "左面板绘出超导、离子阱、中性原子、硅自旋、光子与拓扑候选的双对数门时长-相干时间相图与等比值线 T2/tg=10^2..10^5；右面板精确绘出 N=1..100 时 eta=0.999, 0.995, 0.99, 0.90 的光子全存活概率曲线。",
        "\n".join(parts),
    )
    return svg, {k: round(v, 6) for k, v in surv_100.items()}


# ===========================================================================
# Figure 2: v3-09-entangling-gates-six-platforms.svg
# ===========================================================================
def build_fig2_entangling_gates_six_platforms() -> tuple[str, dict]:
    # Mathematical verification of core Hamiltonians & gate identities
    # 1. MS phase-space closure: alpha(t) = -(eta*Omega/(2*delta))*(e^{i*delta*t}-1)
    eta_ld, om_ms = 0.08, 2 * math.pi * 250e3
    delta_ms = 2.0 * eta_ld * om_ms
    tg_ms = 2.0 * math.pi / delta_ms
    alpha_end = -(eta_ld * om_ms / (2.0 * delta_ms)) * (cmath.exp(1j * delta_ms * tg_ms) - 1.0)
    theta_ms = 2.0 * math.pi * ((eta_ld * om_ms / delta_ms) ** 2)
    assert abs(alpha_end) < TOL and abs(theta_ms - math.pi / 2.0) < TOL

    # 2. Rydberg blockade 87Rb 70S: Rb = (862.7e9 / 5e6)^(1/6)
    rb_um = (862.7e9 / 5.0e6) ** (1.0 / 6.0)
    assert abs(rb_um - 7.458) < 0.01

    # 3. HOM interference: double-transmission (+1) + double-reflection (i^2 = -1) = 0
    assert abs(0.5 * (1.0 + 1j * 1j)) < TOL

    # 4. Heisenberg S1.S2 = SWAP/2 - I/4
    x2 = [[0j, 1 + 0j], [1 + 0j, 0j]]
    y2 = [[0j, -1j], [1j, 0j]]
    z2 = [[1 + 0j, 0j], [0j, -1 + 0j]]
    s1s2 = [[0.25 * (kron(x2, x2)[i][j] + kron(y2, y2)[i][j] + kron(z2, z2)[i][j]) for j in range(4)] for i in range(4)]
    swap4 = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
    for i in range(4):
        for j in range(4):
            exp_v = 0.5 * swap4[i][j] - (0.25 if i == j else 0.0)
            assert abs(s1s2[i][j] - exp_v) < TOL

    parts = [
        '  <text class="title ink" x="34" y="44">六大硬件平台双比特物理纠缠门核心机制对照</text>',
        '  <text class="subtitle muted" x="34" y="68">非等比例物理机理示意图：并排呈现六条硬件路线的耦合媒介、原生纠缠门哈密顿量与关键解耦边界</text>',
    ]

    xs = [32, 348, 664]
    ys = [84, 314]
    cw, ch = 304, 216

    def card_shell(col: int, row: int, head: str, meta: str, col_cls: str, f1: str, f2: str) -> tuple[float, float]:
        x0, y0 = xs[col], ys[row]
        parts.append(f'  <rect class="card" x="{x0}" y="{y0}" width="{cw}" height="{ch}" rx="12"/>')
        parts.append(f'  <text class="h2 {col_cls}" x="{x0 + 14}" y="{y0 + 22}">{head}</text>')
        parts.append(f'  <text class="xs muted" x="{x0 + 14}" y="{y0 + 42}">{meta}</text>')
        parts.append(f'  <rect class="subcard" x="{x0 + 10}" y="{y0 + 158}" width="{cw - 20}" height="48" rx="7"/>')
        parts.append(f'  <text class="xs {col_cls}" style="font-weight:600" x="{x0 + 18}" y="{y0 + 176}">{f1}</text>')
        parts.append(f'  <text class="xs muted" x="{x0 + 18}" y="{y0 + 198}">{f2}</text>')
        return float(x0), float(y0)

    # --- Panel 1: Superconducting CR / Tunable Coupler ---
    x0, y0 = card_shell(
        0, 0, "(1) 超导：CR / 可调耦合器", "原生 ECR(ZX) / CZ · 20–160 ns", "accent",
        f"g{sub('eff')}(ω{sub('c')}) = g{sub('12')} + g{sub('1c')}g{sub('2c')}(1/Δ{sub('1c')}+1/Δ{sub('2c')})/2",
        f"关断 g{sub('eff')}=0 抑 ZZ；CR 门依赖非谐性 α{sub('c')}",
    )
    # Left schematic: Q1 - Qc(tunable) - Q2 + direct g12 arc
    cy1 = y0 + 108
    parts.append(f'  <path class="s-muted" style="stroke-width:1.4;stroke-dasharray:4 3" d="M{x0+42:.1f} {cy1-20:.1f}Q{x0+104:.1f} {cy1-46:.1f} {x0+166:.1f} {cy1-20:.1f}"/>')
    parts.append(f'  <text class="xs muted" x="{x0+104:.1f}" y="{cy1-42:.1f}" text-anchor="middle">直接耦合 g{sub("12")}</text>')
    parts.append(f'  <line class="wire" x1="{x0+60:.1f}" y1="{cy1:.1f}" x2="{x0+88:.1f}" y2="{cy1:.1f}"/>')
    parts.append(f'  <line class="wire" x1="{x0+120:.1f}" y1="{cy1:.1f}" x2="{x0+148:.1f}" y2="{cy1:.1f}"/>')
    parts.append(f'  <rect class="f-accent" x="{x0+24:.1f}" y="{cy1-18:.1f}" width="36" height="36" rx="8"/>')
    parts.append(f'  <text class="lbl ink" x="{x0+42:.1f}" y="{cy1+5:.1f}" text-anchor="middle">Q{sub("1")}</text>')
    parts.append(f'  <path class="f-purple" d="M{x0+104:.1f} {cy1-20:.1f}L{x0+124:.1f} {cy1:.1f}L{x0+104:.1f} {cy1+20:.1f}L{x0+84:.1f} {cy1:.1f}Z"/>')
    parts.append(f'  <text class="xs purple" style="font-weight:700" x="{x0+104:.1f}" y="{cy1+4:.1f}" text-anchor="middle">Q{sub("c")}</text>')
    parts.append(f'  <text class="xs purple" x="{x0+104:.1f}" y="{cy1+35:.1f}" text-anchor="middle">磁通调 ω{sub("c")}</text>')
    parts.append(f'  <rect class="f-accent" x="{x0+148:.1f}" y="{cy1-18:.1f}" width="36" height="36" rx="8"/>')
    parts.append(f'  <text class="lbl ink" x="{x0+166:.1f}" y="{cy1+5:.1f}" text-anchor="middle">Q{sub("2")}</text>')
    # Right inset: avoided crossing |11> <-> |20>
    ax0, ay0 = x0 + 202, y0 + 62
    parts.append(f'  <line class="axis" style="stroke-width:1.2" x1="{ax0}" y1="{ay0+78}" x2="{ax0+86}" y2="{ay0+78}"/>')
    parts.append(f'  <line class="axis" style="stroke-width:1.2" x1="{ax0}" y1="{ay0+78}" x2="{ax0}" y2="{ay0}"/>')
    pts_hi, pts_lo = [], []
    for k in range(25):
        u = -1.0 + 2.0 * k / 24.0
        gap = math.hypot(u, 0.32)
        pts_hi.append((ax0 + 8 + (u + 1) * 36, ay0 + 38 - gap * 24))
        pts_lo.append((ax0 + 8 + (u + 1) * 36, ay0 + 38 + gap * 24))
    parts.append(f'  <path class="s-warn" style="stroke-width:2.0" d="{polyline_d(pts_hi)}"/>')
    parts.append(f'  <path class="s-accent" style="stroke-width:2.0" d="{polyline_d(pts_lo)}"/>')
    parts.append(f'  <text class="xs warn" x="{ax0+44}" y="{ay0+10}" text-anchor="middle">|20⟩</text>')
    parts.append(f'  <text class="xs accent" x="{ax0+44}" y="{ay0+70}" text-anchor="middle">|11⟩ → −|11⟩</text>')

    # --- Panel 2: Trapped Ions MS Gate ---
    x0, y0 = card_shell(
        1, 0, "(2) 离子阱：Mølmer–Sørensen 门", "原生 X₁X₂ 门 · 10–100 μs", "gold",
        f"H{sub('MS')} ∝ (X{sub('1')}+X{sub('2')})(a e{sup('−iδt')} + a† e{sup('iδt')})",
        f"t{sub('g')}=2πK/|δ| 令 α(t{sub('g')})=0 闭合，一阶免疫热声子",
    )
    # Left: two ions + collective phonon spring + laser beams
    iy = y0 + 108
    parts.append(f'  <circle class="f-gold" cx="{x0+42:.1f}" cy="{iy:.1f}" r="14"/>')
    parts.append(f'  <text class="lbl gold" style="font-weight:700" x="{x0+42:.1f}" y="{iy+5:.1f}" text-anchor="middle">+</text>')
    parts.append(f'  <circle class="f-gold" cx="{x0+130:.1f}" cy="{iy:.1f}" r="14"/>')
    parts.append(f'  <text class="lbl gold" style="font-weight:700" x="{x0+130:.1f}" y="{iy+5:.1f}" text-anchor="middle">+</text>')
    # Spring zig-zag
    sp = [(x0 + 56, iy)] + [(x0 + 62 + i * 8, iy + (-7 if i % 2 == 0 else 7)) for i in range(7)] + [(x0 + 116, iy)]
    parts.append(f'  <path class="s-muted" style="stroke-width:1.8" d="{polyline_d(sp)}"/>')
    parts.append(f'  <text class="xs muted" x="{x0+86:.1f}" y="{iy+28:.1f}" text-anchor="middle">集体声子模 ω{sub("m")}</text>')
    # Red/blue sideband beams
    parts.append(f'  <line class="s-warn" style="stroke-width:1.8;stroke-dasharray:4 2" x1="{x0+24:.1f}" y1="{y0+66:.1f}" x2="{x0+42:.1f}" y2="{iy-16:.1f}"/>')
    parts.append(f'  <line class="s-accent" style="stroke-width:1.8;stroke-dasharray:4 2" x1="{x0+148:.1f}" y1="{y0+66:.1f}" x2="{x0+130:.1f}" y2="{iy-16:.1f}"/>')
    parts.append(f'  <text class="xs warn" x="{x0+20:.1f}" y="{y0+63:.1f}">红边带 ω{sub("r")}</text>')
    parts.append(f'  <text class="xs accent" x="{x0+154:.1f}" y="{y0+63:.1f}" text-anchor="end">蓝边带 ω{sub("b")}</text>')
    # Right: closed phase-space circle alpha(t)
    pcx, pcy, pr = x0 + 230, y0 + 102, 26.0
    parts.append(f'  <line class="axis" style="stroke-width:1.1" x1="{pcx-42:.1f}" y1="{pcy+pr:.1f}" x2="{pcx+46:.1f}" y2="{pcy+pr:.1f}"/>')
    parts.append(f'  <line class="axis" style="stroke-width:1.1" x1="{pcx:.1f}" y1="{pcy+pr+10:.1f}" x2="{pcx:.1f}" y2="{pcy-pr-14:.1f}"/>')
    parts.append(f'  <circle class="f-gold" cx="{pcx:.1f}" cy="{pcy:.1f}" r="{pr:.1f}"/>')
    parts.append(f'  <circle class="ctrl" cx="{pcx:.1f}" cy="{pcy+pr:.1f}" r="3.6"/>')
    parts.append(f'  <path class="gold" d="{arrow_poly(pcx-8, pcy-pr, pcx+4, pcy-pr, 7, 4.5)}"/>')
    parts.append(f'  <text class="xs gold" style="font-weight:700" x="{pcx:.1f}" y="{pcy+4:.1f}" text-anchor="middle">面积∝θ</text>')
    parts.append(f'  <text class="xs ink" x="{pcx+38:.1f}" y="{pcy+pr+14:.1f}" text-anchor="middle">α(t{sub("g")})=0</text>')

    # --- Panel 3: Neutral Atoms Rydberg Blockade ---
    x0, y0 = card_shell(
        2, 0, "(3) 中性原子：里德堡阻塞", "全局并行 CZ · 200–300 ns", "green",
        f"V(R) = C{sub('6')}/R{sup('6')},  R{sub('b')} = (C{sub('6')}/ħΩ){sup('1/6')}",
        f"强阻塞 R≪R{sub('b')} 禁 |rr⟩，|11⟩↔|W⟩ 快 √2 倍",
    )
    # Left: blockade radius circle with 2 atoms
    bcx, bcy = x0 + 68, y0 + 104
    parts.append(f'  <circle class="f-green" style="fill-opacity:.22;stroke-dasharray:5 3" cx="{bcx:.1f}" cy="{bcy:.1f}" r="42"/>')
    parts.append(f'  <circle class="b-green" cx="{bcx-16:.1f}" cy="{bcy:.1f}" r="7.5"/>')
    parts.append(f'  <circle class="b-green" cx="{bcx+16:.1f}" cy="{bcy:.1f}" r="7.5"/>')
    parts.append(f'  <line class="axis" style="stroke-width:1.2" x1="{bcx-16:.1f}" y1="{bcy+14:.1f}" x2="{bcx+16:.1f}" y2="{bcy+14:.1f}"/>')
    parts.append(f'  <text class="xs ink" x="{bcx:.1f}" y="{bcy+27:.1f}" text-anchor="middle">R &lt; R{sub("b")}</text>')
    parts.append(f'  <text class="xs green" style="font-weight:600" x="{bcx:.1f}" y="{bcy-26:.1f}" text-anchor="middle">阻塞圈 R{sub("b")}</text>')
    # Right: level diagram |11> <-> |W> and shifted |rr>
    lx_l, lx_r = x0 + 150, x0 + 216
    parts.append(f'  <line class="wire" x1="{lx_l}" y1="{y0+142}" x2="{lx_r}" y2="{y0+142}"/>')
    parts.append(f'  <text class="xs ink" x="{lx_r+6}" y="{y0+146}">|11⟩</text>')
    parts.append(f'  <line class="wire" x1="{lx_l}" y1="{y0+104}" x2="{lx_r}" y2="{y0+104}"/>')
    parts.append(f'  <text class="xs green" style="font-weight:600" x="{lx_r+6}" y="{y0+108}">|W⟩</text>')
    parts.append(f'  <line class="s-muted" style="stroke-width:1.4;stroke-dasharray:4 3" x1="{lx_l}" y1="{y0+74}" x2="{lx_r}" y2="{y0+74}"/>')
    parts.append(f'  <line class="s-warn" style="stroke-width:2.2" x1="{lx_l}" y1="{y0+56}" x2="{lx_r}" y2="{y0+56}"/>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{lx_r+6}" y="{y0+60}">|rr⟩ 阻塞!</text>')
    parts.append(f'  <line class="s-green" style="stroke-width:2.0" x1="{lx_l+32}" y1="{y0+138}" x2="{lx_l+32}" y2="{y0+108}"/>')
    parts.append(f'  <path class="green" d="{arrow_poly(lx_l+32, y0+138, lx_l+32, y0+106, 7, 4.5)}"/>')
    parts.append(f'  <text class="xs green" style="font-weight:700" x="{lx_l+26}" y="{y0+127}" text-anchor="end">√2Ω</text>')
    parts.append(f'  <line class="s-warn" style="stroke-width:1.5" x1="{lx_l+12}" y1="{y0+74}" x2="{lx_l+12}" y2="{y0+58}"/>')
    parts.append(f'  <text class="xs warn" x="{lx_l+17}" y="{y0+70}">+C{sub("6")}/R{sup("6")}</text>')

    # --- Panel 4: Photonic HOM Bunching ---
    x0, y0 = card_shell(
        0, 1, "(4) 光子：HOM 双光子聚束", "概率性融合测量 · ~ns 光路", "purple",
        "|1,1⟩ → i(|2,0⟩ + |0,2⟩)/√2 （双透射+双反射=0）",
        "无直接相互作用；靠 50:50 分束器与探测反作用",
    )
    bx, by = x0 + 136, y0 + 104
    # 50:50 beam splitter plate
    parts.append(f'  <rect class="f-purple" x="{bx-26:.1f}" y="{by-5:.1f}" width="52" height="10" rx="3" transform="rotate(-35 {bx:.1f} {by:.1f})"/>')
    # Input photon paths (left-top and left-bottom)
    parts.append(f'  <line class="s-accent" style="stroke-width:2.2" x1="{x0+34:.1f}" y1="{by-34:.1f}" x2="{bx:.1f}" y2="{by:.1f}"/>')
    parts.append(f'  <line class="s-accent" style="stroke-width:2.2" x1="{x0+34:.1f}" y1="{by+34:.1f}" x2="{bx:.1f}" y2="{by:.1f}"/>')
    parts.append(f'  <circle class="b-accent" cx="{x0+68:.1f}" cy="{by-22:.1f}" r="5"/>')
    parts.append(f'  <circle class="b-accent" cx="{x0+68:.1f}" cy="{by+22:.1f}" r="5"/>')
    parts.append(f'  <text class="xs ink" x="{x0+28:.1f}" y="{by-36:.1f}">|1{sub("a")}⟩</text>')
    parts.append(f'  <text class="xs ink" x="{x0+28:.1f}" y="{by+46:.1f}">|1{sub("b")}⟩</text>')
    # Output bunched paths
    parts.append(f'  <line class="s-purple" style="stroke-width:2.2" x1="{bx:.1f}" y1="{by:.1f}" x2="{x0+226:.1f}" y2="{by-34:.1f}"/>')
    parts.append(f'  <line class="s-purple" style="stroke-width:2.2" x1="{bx:.1f}" y1="{by:.1f}" x2="{x0+226:.1f}" y2="{by+34:.1f}"/>')
    parts.append(f'  <circle class="b-purple" cx="{x0+196:.1f}" cy="{by-24:.1f}" r="4.5"/>')
    parts.append(f'  <circle class="b-purple" cx="{x0+208:.1f}" cy="{by-28:.1f}" r="4.5"/>')
    parts.append(f'  <text class="xs purple" style="font-weight:700" x="{x0+232:.1f}" y="{by-30:.1f}">|2,0⟩</text>')
    parts.append(f'  <text class="xs purple" style="font-weight:700" x="{x0+232:.1f}" y="{by+38:.1f}">|0,2⟩</text>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{x0+232:.1f}" y="{by+4:.1f}">× |1,1⟩ 相消</text>')
    parts.append(f'  <text class="xs muted" x="{bx:.1f}" y="{by+44:.1f}" text-anchor="middle">50:50 分束器</text>')

    # --- Panel 5: Silicon Spin Heisenberg Exchange ---
    x0, y0 = card_shell(
        1, 1, "(5) 硅自旋：海森堡交换", "√SWAP / CZ · 自旋 ↓ 对应 |0⟩", "accent",
        f"H{sub('ex')} = J(t) S{sub('1')}·S{sub('2')} = J(SWAP/2 − I/4)",
        f"ΔE{sub('Z')}≪J 得 √SWAP；|ΔE{sub('Z')}|≫J 抑翻转得 CZ",
    )
    # Double quantum dot potential well curve (SVG y increases downward => subtract v!)
    def well_pts(barrier_h: float) -> list[tuple[float, float]]:
        out = []
        for i in range(65):
            u = -2.2 + 4.4 * i / 64.0
            v = -1.0 * math.exp(-((u + 0.95) / 0.52) ** 2) - 1.0 * math.exp(-((u - 0.95) / 0.52) ** 2) + barrier_h * math.exp(-(u / 0.42) ** 2)
            out.append((x0 + 152 + u * 56, y0 + 106 - v * 28))
        return out

    hi_well = well_pts(0.65)
    lo_well = well_pts(-0.10)
    # Physical geometry assertions (SVG y increases downward):
    # - left/right dot valleys must lie strictly below (larger y) both edges and center barrier top
    # - high-barrier dashed peak must lie strictly above (smaller y) lowered-barrier solid curve
    y_edge = hi_well[0][1]
    y_bar_hi = hi_well[32][1]
    y_bar_lo = lo_well[32][1]
    y_well_l = max(pt[1] for pt in lo_well[:32])
    y_well_r = max(pt[1] for pt in lo_well[33:])
    assert y_well_l > y_edge + 20.0 and y_well_r > y_edge + 20.0, "Quantum dot wells must dip downward"
    assert y_well_l > y_bar_hi + 35.0 and y_well_r > y_bar_hi + 35.0, "Well bottoms must lie below barrier peak"
    assert y_bar_hi < y_bar_lo - 15.0, "High barrier (dashed) must rise above lowered barrier (solid)"

    parts.append(f'  <path class="s-muted" style="stroke-width:1.6;stroke-dasharray:5 3" d="{polyline_d(hi_well)}"/>')
    parts.append(f'  <path class="s-accent" style="stroke-width:2.4" d="{polyline_d(lo_well)}"/>')
    # Electron dots & spin arrows seated inside the left/right concave well bottoms (u = +-0.95)
    lx_dot, rx_dot = x0 + 152 - 0.95 * 56, x0 + 152 + 0.95 * 56
    parts.append(f'  <line class="s-warn" style="stroke-width:2.4" x1="{lx_dot:.1f}" y1="{y0+131:.1f}" x2="{lx_dot:.1f}" y2="{y0+104:.1f}"/>')
    parts.append(f'  <path class="warn" d="{arrow_poly(lx_dot, y0+131, lx_dot, y0+101, 7, 4.5)}"/>')
    parts.append(f'  <circle class="warn dot-ring" cx="{lx_dot:.1f}" cy="{y0+120:.1f}" r="4.6"/>')
    parts.append(f'  <line class="s-purple" style="stroke-width:2.4" x1="{rx_dot:.1f}" y1="{y0+103:.1f}" x2="{rx_dot:.1f}" y2="{y0+130:.1f}"/>')
    parts.append(f'  <path class="purple" d="{arrow_poly(rx_dot, y0+103, rx_dot, y0+133, 7, 4.5)}"/>')
    parts.append(f'  <circle class="purple dot-ring" cx="{rx_dot:.1f}" cy="{y0+116:.1f}" r="4.6"/>')
    # Gate electrode bar above central barrier peak (y_bar_hi ~ y0 + 89.8)
    parts.append(f'  <rect class="f-gold" x="{x0+132:.1f}" y="{y0+49:.1f}" width="40" height="16" rx="4"/>')
    parts.append(f'  <text class="xs gold" style="font-weight:700" x="{x0+152:.1f}" y="{y0+61:.1f}" text-anchor="middle">势垒栅</text>')
    parts.append(f'  <line class="s-gold" style="stroke-width:1.5" x1="{x0+152:.1f}" y1="{y0+65:.1f}" x2="{x0+152:.1f}" y2="{y0+84:.1f}"/>')
    parts.append(f'  <path class="gold" d="{arrow_poly(x0+152, y0+65, x0+152, y0+86, 6, 4)}"/>')
    parts.append(f'  <text class="xs muted" x="{x0+196:.1f}" y="{y0+84:.1f}">虚线:高势垒</text>')
    parts.append(f'  <text class="xs accent" style="font-weight:600" x="{x0+152:.1f}" y="{y0+153:.1f}" text-anchor="middle">实线拉低势垒 → 开启交换 J(t)</text>')

    # --- Panel 6: Topological Kitaev Chain ---
    x0, y0 = card_shell(
        2, 1, "(6) 拓扑候选：Kitaev 链零模", "编织为理论预言；器件宇称读出约 3.7 μs", "warn",
        f"H = it ∑ γ{sub('j,B')}γ{sub('j+1,A')}（甜点 μ=0, t=Δ）",
        f"端点零模脱钩 P{sub('12')}=−iγ{sub('1')}γ{sub('2')}；编织仅 Clifford",
    )
    ky = y0 + 114
    site_xs = [x0 + 48 + i * 68 for i in range(4)]
    for i, scx in enumerate(site_xs):
        parts.append(f'  <rect class="subcard" x="{scx-24:.1f}" y="{ky-16:.1f}" width="48" height="32" rx="14"/>')
        parts.append(f'  <text class="xs muted" x="{scx:.1f}" y="{ky+32:.1f}" text-anchor="middle">位点 {i+1}</text>')
    # Inter-site pairing bonds gamma_{j,B} -- gamma_{j+1,A}
    for i in range(3):
        bx1, bx2 = site_xs[i] + 12, site_xs[i + 1] - 12
        parts.append(f'  <line class="s-accent" style="stroke-width:3.0" x1="{bx1:.1f}" y1="{ky:.1f}" x2="{bx2:.1f}" y2="{ky:.1f}"/>')
    # Majorana dots inside sites
    for i, scx in enumerate(site_xs):
        cls_a = "b-warn" if i == 0 else "f-accent"
        cls_b = "b-warn" if i == 3 else "f-accent"
        parts.append(f'  <circle class="{cls_a}" cx="{scx-12:.1f}" cy="{ky:.1f}" r="{7.5 if i == 0 else 5.5}"/>')
        parts.append(f'  <circle class="{cls_b}" cx="{scx+12:.1f}" cy="{ky:.1f}" r="{7.5 if i == 3 else 5.5}"/>')
    # Unpaired end zero modes arc
    lx_z, rx_z = site_xs[0] - 12, site_xs[3] + 12
    parts.append(f'  <path class="s-warn" style="stroke-width:1.8;stroke-dasharray:5 3" d="M{lx_z:.1f} {ky-12:.1f}Q{x0+152:.1f} {y0+50:.1f} {rx_z:.1f} {ky-12:.1f}"/>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{x0+152:.1f}" y="{y0+66:.1f}" text-anchor="middle">非局域端点零模（劈裂 ∝ e{sup("−L/ξ")}）</text>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{lx_z:.1f}" y="{ky-25:.1f}" text-anchor="middle">γ{sub("1,A")}</text>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{rx_z:.1f}" y="{ky-25:.1f}" text-anchor="middle">γ{sub("N,B")}</text>')

    parts.append('  <text class="sm muted" x="34" y="554">注：六张机理图均为非等比例示意图；各平台原生门集、相干预算与可扩展工程瓶颈见第 09 章 §4.7 与第 19 章。</text>')

    svg = wrap_svg(
        "v3-09-entangling-gates-six-platforms",
        "六大硬件平台双比特物理纠缠门核心机制对照",
        "六宫格示意图并排展示超导 CR/可调耦合器、离子阱 MS 声子边带、中性原子里德堡阻塞、光子 HOM 聚束、硅自旋海森堡交换（低能自旋向下为 |0⟩）与理论 Kitaev 链端点零模机制。单器件宇称读出时间单列。",
        "\n".join(parts),
    )
    return svg, {"rb_um": round(rb_um, 3), "ms_theta_rad": round(theta_ms, 6)}


# ===========================================================================
# Figure 3: v3-11-benchmark-scaling-eplg.svg
# ===========================================================================
def build_fig3_benchmark_scaling_eplg() -> tuple[str, dict]:
    # Mathematical assertions for RB, (1-r)^G, LF=(1-EPLG)^99 and PEC overhead LF^{-4D}
    lf_05 = (1.0 - 0.005) ** 99
    lf_10 = (1.0 - 0.010) ** 99
    lf_eagle = (1.0 - 0.0166) ** 99
    assert abs(lf_05 - 0.608806) < 1e-4
    assert abs(lf_10 - 0.369730) < 1e-4
    assert abs(lf_eagle - 0.190695) < 5e-4
    pec_d5_05 = lf_05 ** (-20)
    pec_d5_10 = lf_10 ** (-20)
    assert 2.0e4 < pec_d5_05 < 2.1e4 and 4.3e8 < pec_d5_10 < 4.5e8

    parts = [
        '  <text class="title ink" x="34" y="44">随机基准指数衰减与 100 比特链 EPLG / PEC 采样模型预算</text>',
        f'  <text class="subtitle muted" x="34" y="68">左：RB 衰减 P(m)=Aα{sup("m")}+B 剥离 SPAM 截距及门数标度 (1−r){sup("G")}；右：100 比特链层保真度 LF 与 PEC 采样放大倍数</text>',
    ]

    # --- Left Card: RB Decay & (1-r)^G Scaling ---
    lx0, ly0, lw, lh = 32, 84, 452, 446
    parts.append(f'  <rect class="card" x="{lx0}" y="{ly0}" width="{lw}" height="{lh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{lx0 + 16}" y="{ly0 + 24}">(a) RB 剥离 SPAM 截距与 (1−r){sup("G")} 标度</text>')

    # Upper sub-plot: P(m) = A alpha^m + B
    px, py, pw, ph = 96.0, 122.0, 368.0, 148.0

    def ux(m: float) -> float:
        return px + (m / 200.0) * pw

    def uy(val: float) -> float:
        return py + ph - ((val - 0.45) / (1.02 - 0.45)) * ph

    for mv in (0, 50, 100, 150, 200):
        gx = ux(mv)
        parts.append(f'  <line class="grid" x1="{gx:.1f}" y1="{py:.1f}" x2="{gx:.1f}" y2="{py + ph:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{gx:.1f}" y="{py + ph + 15:.1f}" text-anchor="middle">{mv}</text>')
    for fv in (0.5, 0.7, 0.9, 1.0):
        gy = uy(fv)
        parts.append(f'  <line class="grid" x1="{px:.1f}" y1="{gy:.1f}" x2="{px + pw:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{px - 8:.1f}" y="{gy + 4:.1f}" text-anchor="end">{fv:.1f}</text>')

    # Asymptote B = 0.50
    yb = uy(0.50)
    parts.append(f'  <line class="s-muted" style="stroke-width:1.4;stroke-dasharray:5 4" x1="{px:.1f}" y1="{yb:.1f}" x2="{px + pw:.1f}" y2="{yb:.1f}"/>')
    parts.append(f'  <text class="xs muted" x="{px + 8:.1f}" y="{yb - 5:.1f}">渐近基线 B = 1/d = 0.50</text>')

    rb_specs = [
        (0.48, 0.992, 0.50, "accent", "", "α=0.992 (SPAM 2%, r=0.4%)"),
        (0.36, 0.992, 0.50, "green", "6 4", "同 α=0.992 (SPAM 14%, 同底数)"),
        (0.48, 0.980, 0.50, "warn", "7 3 2 3", "α=0.980 (SPAM 2%, r=1.0%)"),
    ]
    for A_v, p_v, B_v, col, dash, _ in rb_specs:
        pts = [(ux(m), uy(A_v * (p_v ** m) + B_v)) for m in range(0, 201, 4)]
        d_attr = f';stroke-dasharray:{dash}' if dash else ""
        parts.append(f'  <path class="s-{col}" style="stroke-width:2.4{d_attr}" d="{polyline_d(pts)}"/>')
        parts.append(f'  <circle class="{col} dot-ring" cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="3.6"/>')

    # SPAM intercept shift bracket at m=0 with clean pointer to lower-left open zone
    y_top_i, y_low_i = uy(0.98), uy(0.86)
    parts.append(f'  <line class="s-gold" style="stroke-width:1.8" x1="{px + 7:.1f}" y1="{y_top_i + 2:.1f}" x2="{px + 7:.1f}" y2="{y_low_i - 2:.1f}"/>')
    parts.append(f'  <line class="s-gold" style="stroke-width:1.2;stroke-dasharray:3 2" x1="{px + 7:.1f}" y1="{y_low_i + 2:.1f}" x2="{px + 14:.1f}" y2="218"/>')
    parts.append(f'  <text class="xs gold" style="font-weight:700" x="{px + 10:.1f}" y="232">SPAM 仅移截距</text>')

    # Legend pill cleanly placed in open upper-right above all curves
    parts.append('  <rect class="pill" x="248" y="128" width="212" height="60" rx="7"/>')
    for idx, (_, _, _, col, dash, lbl) in enumerate(rb_specs):
        ly_i = 143 + idx * 18
        d_attr = f';stroke-dasharray:{dash}' if dash else ""
        parts.append(f'  <line class="s-{col}" style="stroke-width:2.2{d_attr}" x1="256" y1="{ly_i - 3}" x2="274" y2="{ly_i - 3}"/>')
        parts.append(f'  <text class="xs {col}" x="280" y="{ly_i + 1}">{lbl}</text>')

    parts.append(f'  <rect class="axis" x="{px:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}"/>')
    parts.append(f'  <text class="xs ink" x="{px + pw / 2:.1f}" y="{py + ph + 35:.1f}" text-anchor="middle">Clifford 序列长度 m（P(m) = Aα{sup("m")} + B）</text>')
    parts.append(f'  <text class="xs ink" x="52" y="{py + ph / 2:.1f}" text-anchor="middle" transform="rotate(-90 52 {py + ph / 2:.1f})">生存概率 P(m)</text>')

    # Lower sub-plot: (1 - r)^G
    lpx, lpy, lpw, lph = 96.0, 340.0, 368.0, 126.0
    parts.append(f'  <text class="xs ink" style="font-weight:600" x="{lpx:.1f}" y="{lpy - 8:.1f}">无纠错整线路存活标度 S(G) = (1−r){sup("G")}</text>')

    def lx_g(g: float) -> float:
        return lpx + (g / 1000.0) * lpw

    def ly_g(s: float) -> float:
        return lpy + lph - s * lph

    for gv in (0, 200, 400, 600, 800, 1000):
        gx = lx_g(gv)
        parts.append(f'  <line class="grid" x1="{gx:.1f}" y1="{lpy:.1f}" x2="{gx:.1f}" y2="{lpy + lph:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{gx:.1f}" y="{lpy + lph + 15:.1f}" text-anchor="middle">{gv}</text>')
    for sv in (0.0, 0.5, 1.0):
        gy = ly_g(sv)
        parts.append(f'  <line class="grid" x1="{lpx:.1f}" y1="{gy:.1f}" x2="{lpx + lpw:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{lpx - 8:.1f}" y="{gy + 4:.1f}" text-anchor="end">{sv:.1f}</text>')

    # e^-1 reference line
    ye1 = ly_g(math.exp(-1.0))
    parts.append(f'  <line class="s-muted" style="stroke-width:1.2;stroke-dasharray:4 4" x1="{lpx:.1f}" y1="{ye1:.1f}" x2="{lpx + lpw:.1f}" y2="{ye1:.1f}"/>')
    parts.append(f'  <text class="xs muted" x="{lpx + lpw - 6:.1f}" y="{ye1 + 14:.1f}" text-anchor="end">1/e ≈ 36.8%（G ≈ 1/r）</text>')

    for r_val, col, dash in ((1e-3, "green", ""), (3e-3, "accent", "6 4"), (1e-2, "warn", "3 3")):
        pts = [(lx_g(g), ly_g((1.0 - r_val) ** g)) for g in range(0, 1001, 10)]
        d_attr = f';stroke-dasharray:{dash}' if dash else ""
        parts.append(f'  <path class="s-{col}" style="stroke-width:2.4{d_attr}" d="{polyline_d(pts)}"/>')

    parts.append(f'  <text class="xs green" style="font-weight:700" x="{lx_g(760):.1f}" y="{ly_g(0.999**760) - 10:.1f}" text-anchor="middle">r = 10{sup("-3")}</text>')
    parts.append(f'  <text class="xs accent" style="font-weight:700" x="{lx_g(360):.1f}" y="{ly_g(0.997**360) - 14:.1f}">r = 3×10{sup("-3")}</text>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{lx_g(215):.1f}" y="{ly_g(0.99**165) + 4:.1f}">r = 10{sup("-2")}</text>')

    parts.append(f'  <rect class="axis" x="{lpx:.1f}" y="{lpy:.1f}" width="{lpw:.1f}" height="{lph:.1f}"/>')
    parts.append(f'  <text class="xs ink" x="{lpx + lpw / 2:.1f}" y="{lpy + lph + 32:.1f}" text-anchor="middle">电路门总数 G（门数上限 G ~ 1/r）</text>')
    parts.append(f'  <text class="xs ink" x="52" y="{lpy + lph / 2:.1f}" text-anchor="middle" transform="rotate(-90 52 {lpy + lph / 2:.1f})">存活率 (1−r){sup("G")}</text>')
    parts.append(f'  <text class="xs muted" x="{lx0 + 16}" y="{ly0 + lh - 12}">注：α=1−p 为退极化保留底数（§3.1）；相干过旋转可按 O(√r) 偏离 RB。</text>')

    # --- Right Card: 100-Qubit Chain LF & PEC Overhead ---
    rx0, ry0, rw, rh = 500, 84, 468, 446
    parts.append(f'  <rect class="card" x="{rx0}" y="{ry0}" width="{rw}" height="{rh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{rx0 + 16}" y="{ry0 + 24}">(b) 100 比特链层保真度 LF 与 PEC 模型预算</text>')

    rpx, rpy, rpw, rph = 562.0, 134.0, 326.0, 306.0

    def rx_e(e_pct: float) -> float:
        return rpx + (e_pct / 2.0) * rpw

    def ry_lf(lf_val: float) -> float:
        return rpy + rph - lf_val * rph

    def ry_pec(log10_ov: float) -> float:
        return rpy + rph - (log10_ov / 12.0) * rph

    for ep in (0.0, 0.5, 1.0, 1.5, 2.0):
        gx = rx_e(ep)
        parts.append(f'  <line class="grid" x1="{gx:.1f}" y1="{rpy:.1f}" x2="{gx:.1f}" y2="{rpy + rph:.1f}"/>')
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{gx:.1f}" y1="{rpy + rph:.1f}" x2="{gx:.1f}" y2="{rpy + rph + 5:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{gx:.1f}" y="{rpy + rph + 22:.1f}" text-anchor="middle">{ep:.1f}%</text>')

    for lfv in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        gy = ry_lf(lfv)
        parts.append(f'  <line class="grid" x1="{rpx:.1f}" y1="{gy:.1f}" x2="{rpx + rpw:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <text class="xs accent" x="{rpx - 8:.1f}" y="{gy + 4:.1f}" text-anchor="end">{lfv:.1f}</text>')

    for exp_v in (0, 3, 6, 9, 12):
        gy = ry_pec(exp_v)
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{rpx + rpw:.1f}" y1="{gy:.1f}" x2="{rpx + rpw + 5:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <text class="xs warn" x="{rpx + rpw + 9:.1f}" y="{gy + 4:.1f}">10{sup(str(exp_v))}</text>')

    # Engineering ceiling at 10^8 (label cleanly below line on right open area)
    y_ceil = ry_pec(8.0)
    parts.append(f'  <line class="s-warn" style="stroke-width:1.4;stroke-dasharray:5 4" x1="{rpx:.1f}" y1="{y_ceil:.1f}" x2="{rpx + rpw:.1f}" y2="{y_ceil:.1f}"/>')
    parts.append(f'  <text class="xs warn" x="{rpx + rpw - 6:.1f}" y="{y_ceil + 16:.1f}" text-anchor="end">~10{sup("8")}× 采样工程天花板</text>')

    # LF curve: (1 - EPLG)^99
    lf_pts = [(rx_e(i * 0.02), ry_lf((1.0 - i * 0.0002) ** 99)) for i in range(101)]
    parts.append(f'  <path class="s-accent" style="stroke-width:2.8" d="{polyline_d(lf_pts)}"/>')

    # PEC D=5 (10 layers) and D=2 (4 layers): LF^{-4D}
    pec5_pts, pec2_pts = [], []
    for i in range(101):
        ep = i * 0.02
        eplg = ep / 100.0
        lf = (1.0 - eplg) ** 99
        log5 = -20.0 * math.log10(lf)
        log2 = -8.0 * math.log10(lf)
        if log5 <= 12.0:
            pec5_pts.append((rx_e(ep), ry_pec(log5)))
        if log2 <= 12.0:
            pec2_pts.append((rx_e(ep), ry_pec(log2)))
    # Add exact top boundary intersection for D=5 where log10(LF^-20) = 12
    e_top5 = (1.0 - 10.0 ** (-12.0 / (20.0 * 99.0))) * 100.0
    pec5_pts.append((rx_e(e_top5), ry_pec(12.0)))
    parts.append(f'  <path class="s-warn" style="stroke-width:2.8" d="{polyline_d(pec5_pts)}"/>')
    parts.append(f'  <path class="s-purple" style="stroke-width:2.4;stroke-dasharray:7 4" d="{polyline_d(pec2_pts)}"/>')

    # Key benchmark markers
    x_eg, y_eg = rx_e(1.66), ry_lf(lf_eagle)
    parts.append(f'  <path class="b-accent" d="M{x_eg:.1f} {y_eg - 5.5:.1f}L{x_eg + 5.5:.1f} {y_eg:.1f}L{x_eg:.1f} {y_eg + 5.5:.1f}L{x_eg - 5.5:.1f} {y_eg:.1f}Z"/>')
    parts.append(f'  <text class="xs accent" style="font-weight:700" x="{rpx + rpw - 6:.1f}" y="{rpy + rph - 10:.1f}" text-anchor="end">Eagle 100Q (1.66%, LF≈0.19)</text>')

    x_10, y_10_p5 = rx_e(1.0), ry_pec(-20.0 * math.log10(lf_10))
    parts.append(f'  <circle class="warn dot-ring" cx="{x_10:.1f}" cy="{y_10_p5:.1f}" r="4.2"/>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{x_10 + 10:.1f}" y="{y_10_p5 + 4:.1f}">EPLG=1%: 4.4×10{sup("8")}×</text>')

    # Direct curve labels in clean open regions
    parts.append(f'  <text class="xs accent" style="font-weight:700" x="{rx_e(0.18):.1f}" y="{rpy + 26:.1f}">LF = (1−EPLG){sup("99")}（左轴）</text>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{rx_e(1.38):.1f}" y="{rpy + 22:.1f}">PEC D=5 (10层)</text>')
    parts.append(f'  <text class="xs purple" style="font-weight:700" x="{rx_e(1.48):.1f}" y="{ry_pec(5.5) - 18:.1f}" text-anchor="middle">PEC D=2 (4层)</text>')

    parts.append(f'  <rect class="axis" x="{rpx:.1f}" y="{rpy:.1f}" width="{rpw:.1f}" height="{rph:.1f}"/>')
    parts.append(f'  <text class="lbl ink" x="{rpx + rpw / 2:.1f}" y="{rpy + rph + 44:.1f}" text-anchor="middle">每层门错误率 EPLG（%）</text>')
    parts.append(f'  <text class="lbl accent" x="518" y="{rpy + rph / 2:.1f}" text-anchor="middle" transform="rotate(-90 518 {rpy + rph / 2:.1f})">100 比特链层保真度 LF</text>')
    parts.append(f'  <text class="lbl warn" x="952" y="{rpy + rph / 2:.1f}" text-anchor="middle" transform="rotate(90 952 {rpy + rph / 2:.1f})">PEC 样本预算 LF{sup("−4D")}</text>')
    parts.append(f'  <text class="xs muted" x="{rx0 + 16}" y="{ry0 + rh - 12}">每周期含奇偶双层（99 边）；模型预算 LF{sup("−4D")}。</text>')

    parts.append('  <text class="sm muted" x="34" y="554">注：右图假设小噪声与独立的 Pauli 因子，实际 PEC 范数由所用逆信道决定。</text>')

    svg = wrap_svg(
        "v3-11-benchmark-scaling-eplg",
        "随机基准指数衰减与 100 比特链 EPLG/PEC 采样模型预算",
        "左面板展示随机基准 P(m)=Aα^m+B 剥离 SPAM 截距的指数衰减曲线与无纠错电路存活标度 (1-r)^G；右面板双轴展示 100 比特连通链层保真度 LF=(1-EPLG)^99 与 D=2, 5 周期 PEC 样本预算 LF^(-4D)。",
        "\n".join(parts),
    )
    return svg, {"lf_05": round(lf_05, 4), "lf_10": round(lf_10, 4), "pec_d5_10": f"{pec_d5_10:.2e}"}


# ===========================================================================
# Figure 4: v3-11-ftqc-resource-budget.svg
# ===========================================================================
def build_fig4_ftqc_resource_budget() -> tuple[str, dict]:
    # Mathematical assertions for surface code & RSA-2048 2021 vs 2025
    eps_d17 = 0.1 * (0.1 ** ((17 + 1) / 2))
    eps_d25_02 = 0.1 * (0.2 ** ((25 + 1) / 2))
    assert abs(eps_d17 - 1e-10) < 1e-22
    assert eps_d25_02 < 1e-10
    cold_q, hot_q, comp_q = 550_400, 177_112, 170_352
    tot_2025 = cold_q + hot_q + comp_q
    assert tot_2025 == 897_864
    comp_ratio = 20_000_000 / tot_2025
    assert abs(comp_ratio - 22.275088) < 1e-4

    parts = [
        '  <text class="title ink" x="34" y="44">表面码逻辑错率指数压制与 RSA-2048 容错资源演进</text>',
        f'  <text class="subtitle muted" x="34" y="68">左：ε{sub("L")} ≈ 0.1(p/p{sub("th")}){sup("(d+1)/2")} 随码距 d=3–31 压错曲线与 Willow 实测；右：Gidney 2021 vs 2025 三区物理比特分解</text>',
    ]

    # --- Left Card: Surface Code Exponential Suppression ---
    lx0, ly0, lw, lh = 32, 84, 456, 446
    parts.append(f'  <rect class="card" x="{lx0}" y="{ly0}" width="{lw}" height="{lh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{lx0 + 16}" y="{ly0 + 24}">(a) 表面码指数压错（d = 3–31）</text>')

    px, py, pw, ph = 104.0, 128.0, 364.0, 314.0

    def sx(d: float) -> float:
        return px + ((d - 3.0) / 28.0) * pw

    def sy(log_e: float) -> float:
        return py + ph - ((log_e + 16.0) / 15.0) * ph

    for dv in (3, 7, 11, 15, 19, 23, 27, 31):
        gx = sx(dv)
        parts.append(f'  <line class="grid" x1="{gx:.1f}" y1="{py:.1f}" x2="{gx:.1f}" y2="{py + ph:.1f}"/>')
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{gx:.1f}" y1="{py + ph:.1f}" x2="{gx:.1f}" y2="{py + ph + 5:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{gx:.1f}" y="{py + ph + 19:.1f}" text-anchor="middle">{dv}</text>')
    for ev in (-1, -4, -7, -10, -13, -16):
        gy = sy(ev)
        parts.append(f'  <line class="grid" x1="{px:.1f}" y1="{gy:.1f}" x2="{px + pw:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{px - 5:.1f}" y1="{gy:.1f}" x2="{px:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{px - 9:.1f}" y="{gy + 4:.1f}" text-anchor="end">10{sup(str(ev))}</text>')

    # 10^-10 practical FTQC algorithm threshold line
    y_alg = sy(-10.0)
    parts.append(f'  <line class="s-gold" style="stroke-width:1.6;stroke-dasharray:6 4" x1="{px:.1f}" y1="{y_alg:.1f}" x2="{px + pw:.1f}" y2="{y_alg:.1f}"/>')
    parts.append(f'  <text class="xs gold" style="font-weight:700" x="{px + 8:.1f}" y="{y_alg + 15:.1f}">10{sup("-10")} 实用算法门槛</text>')

    # Threshold flat line p/p_th = 1 (Lambda = 1)
    y_th = sy(-1.0)
    parts.append(f'  <line class="s-warn" style="stroke-width:2.0;stroke-dasharray:5 4" x1="{px:.1f}" y1="{y_th + 1.5:.1f}" x2="{px + pw:.1f}" y2="{y_th + 1.5:.1f}"/>')
    parts.append(f'  <text class="xs warn" style="font-weight:600" x="{px + pw - 6:.1f}" y="{y_th + 16:.1f}" text-anchor="end">p/p{sub("th")}=1（Λ=1，不降反增边界）</text>')

    # Three below-threshold scaling curves: 0.1 * (p/p_th)^((d+1)/2)
    curves = [
        (1.0 / 2.14, "purple", "6 4"),
        (0.2, "accent", "7 3 2 3"),
        (0.1, "green", ""),
    ]
    ds = list(range(3, 32, 2))
    for ratio, col, dash in curves:
        pts = []
        for d in ds:
            le = math.log10(0.1) + 0.5 * (d + 1) * math.log10(ratio)
            if le >= -16.0:
                pts.append((sx(d), sy(le)))
        d_attr = f';stroke-dasharray:{dash}' if dash else ""
        parts.append(f'  <path class="s-{col}" style="stroke-width:2.5{d_attr}" d="{polyline_d(pts)}"/>')
        for cx, cy in pts[::2]:
            parts.append(f'  <circle class="{col} dot-ring" cx="{cx:.1f}" cy="{cy:.1f}" r="3.0"/>')

    # Willow 2025 measured d=3,5,7 points (Lambda=2.14, eps_5=0.31%, eps_7=0.143%, eps_3~0.66%)
    willow_pts = [(sx(3), sy(math.log10(0.00663))), (sx(5), sy(math.log10(0.0031))), (sx(7), sy(math.log10(0.00143)))]
    parts.append(f'  <path class="s-purple" style="stroke-width:3.0" d="{polyline_d(willow_pts)}"/>')
    for wx, wy in willow_pts:
        parts.append(f'  <path class="b-purple" d="M{wx:.1f} {wy - 5.5:.1f}L{wx + 5.5:.1f} {wy:.1f}L{wx:.1f} {wy + 5.5:.1f}L{wx - 5.5:.1f} {wy:.1f}Z"/>')
    parts.append(f'  <line class="s-purple" style="stroke-width:1.2" x1="{willow_pts[2][0] + 5:.1f}" y1="{willow_pts[2][1]:.1f}" x2="210" y2="178"/>')
    parts.append('  <rect class="pill" x="210" y="156" width="186" height="46" rx="7"/>')
    parts.append(f'  <text class="xs purple" style="font-weight:700" x="218" y="173">Willow 实测 d=3→5→7</text>')
    parts.append(f'  <text class="xs muted" x="218" y="193">Λ=2.14, ε{sub("7")}=0.143%</text>')

    # Crossing highlights at d=17 (0.1) and d=25 (0.2)
    parts.append(f'  <circle class="f-green" cx="{sx(17):.1f}" cy="{sy(-10.0):.1f}" r="5.5"/>')
    parts.append(f'  <circle class="f-accent" cx="{sx(25):.1f}" cy="{sy(math.log10(eps_d25_02)):.1f}" r="5.5"/>')

    # Clean direct curve labels
    parts.append(f'  <text class="xs purple" style="font-weight:700" x="{px + pw - 6:.1f}" y="{sy(math.log10(0.1 * (1/2.14)**16)) + 16:.1f}" text-anchor="end">Λ = 2.14 模型</text>')
    parts.append(f'  <text class="xs accent" style="font-weight:700" x="{px + pw - 6:.1f}" y="{sy(-8.2):.1f}" text-anchor="end">p/p{sub("th")}=0.2 (d=25 达标)</text>')
    parts.append(f'  <text class="xs green" style="font-weight:700" x="{sx(25):.1f}" y="{sy(-14.0) + 14:.1f}" text-anchor="end">p/p{sub("th")}=0.1 (d=17 达标)</text>')

    parts.append(f'  <rect class="axis" x="{px:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}"/>')
    parts.append(f'  <text class="lbl ink" x="{px + pw / 2:.1f}" y="{py + ph + 44:.1f}" text-anchor="middle">表面码码距 d（奇数）</text>')
    parts.append(f'  <text class="lbl ink" x="50" y="{py + ph / 2:.1f}" text-anchor="middle" transform="rotate(-90 50 {py + ph / 2:.1f})">逻辑错误率 ε{sub("L")}（对数刻度）</text>')
    parts.append(f'  <text class="xs muted" x="{lx0 + 16}" y="{ly0 + lh - 12}">注：Willow 实测含预因子差异与约 10{sup("-10")} 稀有突发底板，不可线性外推。</text>')

    # --- Right Card: RSA-2048 Resource Estimation Evolution ---
    rx0, ry0, rw, rh = 504, 84, 464, 446
    parts.append(f'  <rect class="card" x="{rx0}" y="{ry0}" width="{rw}" height="{rh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{rx0 + 16}" y="{ry0 + 24}">(b) RSA-2048 资源演进（p=10{sup("-3")}, τ{sub("cyc")}=1 μs）</text>')

    bx, bw_max = 524.0, 422.0
    # 2021 bar: 20,000,000 qubits
    parts.append(f'  <text class="xs ink" style="font-weight:600" x="{bx:.1f}" y="142">Gidney–Ekerå 2021 [同行评审] · d=27 · 约 8 小时</text>')
    parts.append(f'  <rect class="f-warn" x="{bx:.1f}" y="150" width="{bw_max:.1f}" height="32" rx="6"/>')
    parts.append(f'  <text class="lbl warn" style="font-weight:700" x="{bx + bw_max / 2:.1f}" y="171" text-anchor="middle">约 20,000,000 物理比特（2,000 万）</text>')

    # 2025 bar: 897,864 qubits (strict linear scale = 4.489% of 422 px = 18.94 px)
    w_2025 = bw_max * (tot_2025 / 20_000_000.0)
    w_c0 = w_2025 * (cold_q / tot_2025)
    w_h0 = w_2025 * (hot_q / tot_2025)
    w_m0 = w_2025 - w_c0 - w_h0
    parts.append(f'  <text class="xs ink" style="font-weight:600" x="{bx:.1f}" y="206">Gidney 2025 [预印本] · 近似 RNS + 轭联码 + MSC · 约 4.96 天</text>')
    parts.append(f'  <rect class="b-accent" x="{bx:.1f}" y="214" width="{w_c0:.2f}" height="32"/>')
    parts.append(f'  <rect class="b-gold" x="{bx + w_c0:.2f}" y="214" width="{w_h0:.2f}" height="32"/>')
    parts.append(f'  <rect class="b-green" x="{bx + w_c0 + w_h0:.2f}" y="214" width="{w_m0:.2f}" height="32"/>')
    parts.append(f'  <text class="lbl green" style="font-weight:700" x="{bx + w_2025 + 12:.1f}" y="235">897,864 物理比特（线性尺度压缩 22.3×）</text>')

    # Zoom connector elbow (cleanly stays above centered caption)
    parts.append(f'  <line class="s-muted" style="stroke-width:1.2;stroke-dasharray:4 3" x1="{bx:.1f}" y1="246" x2="{bx:.1f}" y2="294"/>')
    parts.append(f'  <path class="s-muted" style="stroke-width:1.2;stroke-dasharray:4 3" d="M{bx + w_2025:.1f} 246V261H{bx + bw_max:.1f}V294"/>')
    parts.append(f'  <text class="xs accent" style="font-weight:600" x="{bx + bw_max / 2:.1f}" y="283" text-anchor="middle">放大拆解：Gidney 2025 三区精确占比（总计 897,864）</text>')

    # Zoomed 100% stacked bar
    wc = bw_max * (cold_q / tot_2025)
    wh = bw_max * (hot_q / tot_2025)
    wm = bw_max - wc - wh
    parts.append(f'  <rect class="f-accent" x="{bx:.1f}" y="294" width="{wc:.1f}" height="42" rx="4"/>')
    parts.append(f'  <rect class="f-gold" x="{bx + wc:.1f}" y="294" width="{wh:.1f}" height="42"/>')
    parts.append(f'  <rect class="f-green" x="{bx + wc + wh:.1f}" y="294" width="{wm:.1f}" height="42" rx="4"/>')
    parts.append(f'  <text class="lbl accent" style="font-weight:700" x="{bx + wc / 2:.1f}" y="320" text-anchor="middle">冷存储 61.3%</text>')
    parts.append(f'  <text class="xs gold" style="font-weight:700" x="{bx + wc + wh / 2:.1f}" y="319" text-anchor="middle">热区 19.7%</text>')
    parts.append(f'  <text class="xs green" style="font-weight:700" x="{bx + wc + wh + wm / 2:.1f}" y="319" text-anchor="middle">培育 19.0%</text>')

    # Detailed 3-zone breakdown subcard
    parts.append(f'  <rect class="subcard" x="{bx:.1f}" y="350" width="{bw_max:.1f}" height="148" rx="9"/>')
    rows_25 = [
        ("b-accent", "冷存储区（轭联表面码）", "1,280 槽 × 430", "550,400 (61.3%)"),
        ("b-gold", "热存储区（d=25 表面码）", "131 块 × 1,352", "177,112 (19.7%)"),
        ("b-green", "计算与魔法态培育区 (MSC)", "126 块 × 1,352", "170,352 (19.0%)"),
    ]
    for idx, (bcls, name, calc, val) in enumerate(rows_25):
        ry_r = 376 + idx * 32
        parts.append(f'  <rect class="{bcls}" x="{bx + 14:.1f}" y="{ry_r - 11:.1f}" width="12" height="12" rx="3"/>')
        parts.append(f'  <text class="xs ink" style="font-weight:600" x="{bx + 34:.1f}" y="{ry_r:.1f}">{name}</text>')
        parts.append(f'  <text class="xs muted" x="{bx + 206:.1f}" y="{ry_r:.1f}">{calc}</text>')
        parts.append(f'  <text class="mono ink" x="{bx + bw_max - 14:.1f}" y="{ry_r:.1f}" text-anchor="end">{val}</text>')
    parts.append(f'  <line class="divider" x1="{bx + 14:.1f}" y1="454" x2="{bx + bw_max - 14:.1f}" y2="454"/>')
    parts.append(f'  <text class="xs ink" style="font-weight:700" x="{bx + 14:.1f}" y="476">合计 897,864 物理比特（留 ~10% 工程余量概括为 &lt;100 万）</text>')
    parts.append(f'  <text class="xs muted" x="{rx0 + 16}" y="{ry0 + rh - 12}">注：理想均匀去极化理论估算，未含宇宙射线突发与百万级良率。</text>')

    parts.append('  <text class="sm muted" x="34" y="554">注：算法分解、轭联编码与魔法态培育协同带来 22.3× 空间压缩，同时以墙钟时长（8 h → 4.96 d）作时空交换。</text>')

    svg = wrap_svg(
        "v3-11-ftqc-resource-budget",
        "表面码指数压错与 RSA-2048 容错资源演进分解",
        "左面板绘出表面码逻辑错率随码距 d=3..31 的指数压制曲线并标注 Willow 实测与 10^-10 门槛；右面板线性对比 Gidney-Ekera 2021 的 2000 万物理比特与 Gidney 2025 的 897,864 物理比特并放大拆解冷存储、热存储与计算培育三区占比。",
        "\n".join(parts),
    )
    return svg, {"tot_2025": tot_2025, "compression_x": round(comp_ratio, 2)}


# ===========================================================================
# Figure 5: v3-12-lwe-lattice-repeaters.svg
# ===========================================================================
def build_fig5_lwe_lattice_repeaters() -> tuple[str, dict]:
    # Exact toy LWE mod 17 verification (Ch12 §2.3)
    q = 17
    A = [[5, 11], [9, 4]]
    s = [1, -1]
    e = [1, -1]
    b = [(A[i][0] * s[0] + A[i][1] * s[1] + e[i]) % q for i in range(2)]
    assert b == [12, 4]
    r = [1, -1]
    e1_ok, e2_ok = [0, 1], -1
    u_ok = [(A[0][i] * r[0] + A[1][i] * r[1] + e1_ok[i]) % q for i in range(2)]
    bt_r = b[0] * r[0] + b[1] * r[1]
    v0_ok = (bt_r + e2_ok + 0) % q
    v1_ok = (bt_r + e2_ok + 8) % q
    stu_ok = (s[0] * u_ok[0] + s[1] * u_ok[1]) % q
    assert (v0_ok - stu_ok) % q == 2 and (v1_ok - stu_ok) % q == 10
    # Failure counterexample: e1=[-1,1], e2=+1 => w=+5 crosses boundary into m=1 sector
    e1_bad, e2_bad = [-1, 1], 1
    u_bad = [(A[0][i] * r[0] + A[1][i] * r[1] + e1_bad[i]) % q for i in range(2)]
    v0_bad = (bt_r + e2_bad + 0) % q
    stu_bad = (s[0] * u_bad[0] + s[1] * u_bad[1]) % q
    dec_bad = (v0_bad - stu_bad) % q
    assert dec_bad == 5 and abs(dec_bad - 8) < abs(dec_bad - 0)
    # Odd modulus q=17 exact decoding boundary check:
    # m=0 (at 0) tolerates [-4, +4], m=1 (at 8) tolerates [-3, +4]; (m=1, w=-4) collides with (m=0, w=+4) at residue 4!
    m0_set = {13, 14, 15, 16, 0, 1, 2, 3, 4}
    m1_set = {5, 6, 7, 8, 9, 10, 11, 12}
    for w_ok in range(-3, 4):
        assert (0 + w_ok) % q in m0_set
        assert (8 + w_ok) % q in m1_set
    assert (0 + 4) % q == (8 - 4) % q == 4

    # Exact repeater latency & erasure bound (Ch12 §7.4)
    c_f = 2.0e5  # km/s
    t_1g_us = (2.0 * 1000.0 / c_f) * 1e6  # 10,000 us = 10 ms
    t_2g_us = (2.0 * 20.0 / c_f) * 1e6    # 200 us = 0.2 ms
    t_3g_us = 1.0                         # 1 us
    loss_max_db = 10.0 * math.log10(2.0)
    l0_max_km = loss_max_db / 0.2
    assert abs(t_1g_us - 10000.0) < TOL and abs(t_2g_us - 200.0) < TOL
    assert abs(l0_max_km - 15.05149978) < 1e-5

    parts = [
        '  <text class="title ink" x="34" y="44">LWE 模 17 解密容错圆环与三代量子中继 1000 km 时延对照</text>',
        f'  <text class="subtitle muted" x="34" y="68">左：ℤ{sub("17")} 奇数解码环对称安全界 |w| ≤ 3、余数 4 碰撞边界与 w=+5 越界反例；右：1000 km 三代中继时延</text>',
    ]

    # --- Left Card: LWE mod 17 Circular Decoding Ring ---
    lx0, ly0, lw, lh = 32, 84, 468, 446
    parts.append(f'  <rect class="card" x="{lx0}" y="{ly0}" width="{lw}" height="{lh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{lx0 + 16}" y="{ly0 + 24}">(a) LWE 模 q = 17 圆形解码环（对称界 |w| ≤ 3）</text>')

    cx, cy, R = 252.0, 276.0, 106.0

    def ring_pt(val: float, rad: float = R) -> tuple[float, float]:
        ang = -math.pi / 2.0 + 2.0 * math.pi * (val / 17.0)
        return cx + rad * math.cos(ang), cy + rad * math.sin(ang)

    def ring_arc(v1: float, v2: float, rad: float) -> str:
        x1, y1 = ring_pt(v1, rad)
        x2, y2 = ring_pt(v2, rad)
        large = 1 if abs(v2 - v1) > 8.5 else 0
        sweep = 1 if v2 > v1 else 0
        return f"M{x1:.2f} {y1:.2f}A{rad:.2f} {rad:.2f} 0 {large} {sweep} {x2:.2f} {y2:.2f}"

    # Upper semicircle (m=0: [-4.25, +4.25]) and lower semicircle (m=1: [4.25, 12.75])
    parts.append(f'  <path class="f-accent" style="fill-opacity:.22;stroke:none" d="M{cx - R:.1f} {cy:.1f}A{R:.1f} {R:.1f} 0 0 1 {cx + R:.1f} {cy:.1f}Z"/>')
    parts.append(f'  <path class="f-gold" style="fill-opacity:.22;stroke:none" d="M{cx + R:.1f} {cy:.1f}A{R:.1f} {R:.1f} 0 0 1 {cx - R:.1f} {cy:.1f}Z"/>')
    parts.append(f'  <circle class="axis" style="stroke-width:2.0" cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}"/>')

    # Horizontal decision boundary at ±4.25 (12.75 and 4.25)
    parts.append(f'  <line class="s-warn" style="stroke-width:1.8;stroke-dasharray:6 4" x1="{cx - R - 18:.1f}" y1="{cy:.1f}" x2="{cx + R + 18:.1f}" y2="{cy:.1f}"/>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{cx - R - 22:.1f}" y="{cy + 4:.1f}" text-anchor="end">−4.25</text>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{cx + R + 22:.1f}" y="{cy + 4:.1f}">+4.25 边界</text>')

    # Sector labels cleanly inside upper and lower semicircles
    parts.append(f'  <text class="xs accent" style="font-weight:700" x="{cx:.1f}" y="{cy - 44:.1f}" text-anchor="middle">m = 0 区间 [0 ± 4.25]</text>')
    parts.append(f'  <text class="xs muted" x="{cx:.1f}" y="{cy - 27:.1f}" text-anchor="middle">{{13..16, 0..4}} · 容 [−4,4]</text>')
    parts.append(f'  <text class="xs gold" style="font-weight:700" x="{cx:.1f}" y="{cy + 34:.1f}" text-anchor="middle">m = 1 区间 [8.5 ± 4.25]</text>')
    parts.append(f'  <text class="xs muted" x="{cx:.1f}" y="{cy + 51:.1f}" text-anchor="middle">编码点 8 · {{5..12}} · 容 [−3,4]</text>')

    # 17 integer ticks & labels around ring (clean style attribute without leading semicolon)
    for k in range(17):
        x_in, y_in = ring_pt(k, R - 4.0)
        x_out, y_out = ring_pt(k, R + 4.0)
        xl, yl = ring_pt(k, R + 17.0)
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{x_in:.1f}" y1="{y_in:.1f}" x2="{x_out:.1f}" y2="{y_out:.1f}"/>')
        tcls = "xs warn" if k in (4, 5) else ("xs green" if k in (2, 10) else ("xs accent" if k == 0 else ("xs gold" if k == 8 else "xs muted")))
        style_attr = ' style="font-weight:700"' if k in (0, 2, 4, 5, 8, 10) else ""
        parts.append(f'  <text class="{tcls}"{style_attr} x="{xl:.1f}" y="{yl + 4:.1f}" text-anchor="middle">{k}</text>')

    # 8.5 midpoint tick
    x85a, y85a = ring_pt(8.5, R - 6.0)
    x85b, y85b = ring_pt(8.5, R + 6.0)
    parts.append(f'  <line class="s-gold" style="stroke-width:1.6" x1="{x85a:.1f}" y1="{y85a:.1f}" x2="{x85b:.1f}" y2="{y85b:.1f}"/>')

    # Normal w=+2 arc (0 -> 2) and failure w=+5 arc (0 -> 5 crossing +4.25)
    parts.append(f'  <path class="s-green" style="stroke-width:2.6" d="{ring_arc(0.0, 2.0, R - 12.0)}"/>')
    p2_a, p2_b = ring_pt(1.85, R - 12.0), ring_pt(2.0, R - 12.0)
    parts.append(f'  <path class="green" d="{arrow_poly(p2_a[0], p2_a[1], p2_b[0], p2_b[1], 7, 4.5)}"/>')
    parts.append(f'  <path class="s-warn" style="stroke-width:2.6" d="{ring_arc(0.0, 5.0, R - 22.0)}"/>')
    p5_a, p5_b = ring_pt(4.85, R - 22.0), ring_pt(5.0, R - 22.0)
    parts.append(f'  <path class="warn" d="{arrow_poly(p5_a[0], p5_a[1], p5_b[0], p5_b[1], 7, 4.5)}"/>')

    # Key node markers on ring
    x0_r, y0_r = ring_pt(0)
    x2_r, y2_r = ring_pt(2)
    x4_r, y4_r = ring_pt(4)
    x5_r, y5_r = ring_pt(5)
    x8_r, y8_r = ring_pt(8)
    x10_r, y10_r = ring_pt(10)
    parts.append(f'  <path class="b-accent" d="M{x0_r:.1f} {y0_r - 6:.1f}L{x0_r + 6:.1f} {y0_r:.1f}L{x0_r:.1f} {y0_r + 6:.1f}L{x0_r - 6:.1f} {y0_r:.1f}Z"/>')
    parts.append(f'  <path class="b-gold" d="M{x8_r:.1f} {y8_r - 6:.1f}L{x8_r + 6:.1f} {y8_r:.1f}L{x8_r:.1f} {y8_r + 6:.1f}L{x8_r - 6:.1f} {y8_r:.1f}Z"/>')
    parts.append(f'  <circle class="green dot-ring" cx="{x2_r:.1f}" cy="{y2_r:.1f}" r="5.0"/>')
    parts.append(f'  <circle class="f-warn" cx="{x4_r:.1f}" cy="{y4_r:.1f}" r="4.6"/>')
    parts.append(f'  <circle class="green dot-ring" cx="{x10_r:.1f}" cy="{y10_r:.1f}" r="4.6"/>')
    parts.append(f'  <circle class="warn dot-ring" cx="{x5_r:.1f}" cy="{y5_r:.1f}" r="5.4"/>')

    # Clean non-overlapping outer callouts
    parts.append(f'  <text class="xs accent" style="font-weight:700" x="{cx:.1f}" y="138" text-anchor="middle">m=0 编码点 (0)</text>')
    parts.append(f'  <text class="xs gold" style="font-weight:700" x="{cx + 68:.1f}" y="420">m=1 编码点 8 (q/2=8.5)</text>')
    parts.append(f'  <line class="s-green" style="stroke-width:1.2" x1="{x2_r + 16:.1f}" y1="{y2_r - 12:.1f}" x2="386" y2="180"/>')
    parts.append('  <text class="xs green" style="font-weight:700" x="390" y="175">正常 w=+2</text>')
    parts.append('  <text class="xs muted" x="390" y="194">0→2 精准判 0</text>')

    parts.append(f'  <line class="s-warn" style="stroke-width:1.3" x1="{x5_r + 18:.1f}" y1="{y5_r + 8:.1f}" x2="392" y2="338"/>')
    parts.append('  <text class="xs warn" style="font-weight:700" x="396" y="333">越界 w=+5</text>')
    parts.append('  <text class="xs warn" x="396" y="352">落入 5→误判 1!</text>')

    parts.append(f'  <line class="s-green" style="stroke-width:1.2" x1="{x10_r - 16:.1f}" y1="{y10_r + 12:.1f}" x2="136" y2="392"/>')
    parts.append('  <text class="xs green" style="font-weight:700" x="132" y="387" text-anchor="end">8+2=10</text>')
    parts.append('  <text class="xs muted" x="132" y="406" text-anchor="end">精准判 1</text>')

    # Bottom formula subcard (4 concise lines, 0 overlap)
    parts.append(f'  <rect class="subcard" x="{lx0 + 14}" y="434" width="{lw - 28}" height="86" rx="8"/>')
    parts.append(f'  <text class="xs accent" style="font-weight:600" x="{lx0 + 24}" y="452">解密：v − s{sup("T")}u ≡ w + 8m (mod 17)，w = e{sup("T")}r + e{sub("2")} − s{sup("T")}e{sub("1")}</text>')
    parts.append(f'  <text class="xs ink" style="font-weight:700" x="{lx0 + 24}" y="472">对称无歧义充分界 |w| ≤ 3（m=0 容 [−4,4]，m=1 编于 8 容 [−3,4]）</text>')
    parts.append(f'  <text class="xs warn" x="{lx0 + 24}" y="492">碰撞边界：(m=1, w=−4) 与 (m=0, w=+4) 均落余数 4（等距歧义）</text>')
    parts.append(f'  <text class="xs muted" x="{lx0 + 24}" y="512">正常例 w=+2 (0→2, 8→10) 准判；反例 w=+5 落入 5，m=0 误判为 1</text>')

    # --- Right Card: 1G / 2G / 3G Repeaters 1000 km Log Latency ---
    rx0, ry0, rw, rh = 516, 84, 452, 446
    parts.append(f'  <rect class="card" x="{rx0}" y="{ry0}" width="{rw}" height="{rh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{rx0 + 16}" y="{ry0 + 24}">(b) 1000 km 中继算例的三个时标</text>')

    rpx, rpy, rpw, rph = 594.0, 128.0, 352.0, 240.0
    y_lo, y_hi = -1.0, 5.0  # log10(us): 0.1 us to 100 ms

    def rsy(log_us: float) -> float:
        return rpy + rph - ((log_us - y_lo) / (y_hi - y_lo)) * rph

    y_ticks = [(-1, "0.1 μs"), (0, "1 μs"), (1, "10 μs"), (2, "100 μs"), (3, "1 ms"), (4, "10 ms"), (5, "100 ms")]
    for lv, lbl in y_ticks:
        gy = rsy(lv)
        parts.append(f'  <line class="grid" x1="{rpx:.1f}" y1="{gy:.1f}" x2="{rpx + rpw:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{rpx - 5:.1f}" y1="{gy:.1f}" x2="{rpx:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{rpx - 9:.1f}" y="{gy + 4:.1f}" text-anchor="end">{lbl}</text>')

    bars = [
        (658.0, math.log10(t_1g_us), "b-warn", "warn", "10 ms", "1G 端到端纯化", f"2L/c{sub('f')} 双向 RTT"),
        (772.0, math.log10(t_2g_us), "b-accent", "accent", "0.2 ms", "2G 全邻跳往返", f"2L{sub('0')}/c{sub('f')} (20 km)"),
        (886.0, math.log10(t_3g_us), "b-green", "green", "1 μs", "3G 单个本地门", f"本地门 t{sub('local')}"),
    ]
    bw = 58.0
    tops = []
    for xc, lv, bcls, tcls, v_lbl, n1, n2 in bars:
        yt = rsy(lv)
        tops.append((xc, yt))
        parts.append(f'  <rect class="{bcls}" x="{xc - bw / 2:.1f}" y="{yt:.1f}" width="{bw:.1f}" height="{rpy + rph - yt:.1f}" rx="5"/>')
        parts.append(f'  <text class="xs {tcls}" style="font-weight:700" x="{xc:.1f}" y="{yt - 8:.1f}" text-anchor="middle">{v_lbl}</text>')
        parts.append(f'  <text class="xs ink" style="font-weight:600" x="{xc:.1f}" y="{rpy + rph + 17:.1f}" text-anchor="middle">{n1}</text>')
        parts.append(f'  <text class="xs muted" x="{xc:.1f}" y="{rpy + rph + 33:.1f}" text-anchor="middle">{n2}</text>')

    parts.append(f'  <rect class="axis" x="{rpx:.1f}" y="{rpy:.1f}" width="{rpw:.1f}" height="{rph:.1f}"/>')
    parts.append(f'  <text class="lbl ink" x="534" y="{rpy + rph / 2:.1f}" text-anchor="middle" transform="rotate(-90 534 {rpy + rph / 2:.1f})">分项时间（对数刻度）</text>')

    # 3G 50% erasure hard limit callout subcard
    parts.append(f'  <rect class="subcard" x="{rx0 + 14}" y="420" width="{rw - 28}" height="96" rx="8"/>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{rx0 + 24}" y="440">3G 物理硬红线：50% 擦除容量定理 Q(ℰ{sub("p")}) = max(0, 1 − 2p)</text>')
    parts.append(f'  <text class="xs ink" x="{rx0 + 24}" y="461">单跳最大损耗 −10 log{sub("10")}(0.5) ≈ 3.01 dB ⇒ 纯光纤站距上确界 ≈ 15.05 km</text>')
    parts.append(f'  <text class="xs muted" x="{rx0 + 24}" y="482">参数：L=1,000 km，c{sub("f")}=2×10{sup("5")} km/s，衰减 a=0.2 dB/km（2G 取 L{sub("0")}=20 km）</text>')
    parts.append(f'  <text class="xs muted" x="{rx0 + 24}" y="503">效率 1/.8/.6：15.05/10.21/3.96 km；等号处容量为零。</text>')

    parts.append('  <text class="sm muted" x="34" y="554">注：左图展示后量子格密码核心噪声界（与 FIPS 203 ML-KEM 同源），右图为三个分项时标。两层本地门需 2 μs，中点先兆为 100 μs。</text>')

    svg = wrap_svg(
        "v3-12-lwe-lattice-repeaters",
        "LWE 模 17 解密噪声界与三代量子中继 1000 km 时延对照",
        "左面板绘出模 q=17 圆形解码环、m=0 与 m=1 解码扇区、奇数模对称无歧义充分界 |w|<=3（m=0 容 [-4,4]、m=1 编于 8 容 [-3,4]，(m=1,w=-4) 与 (m=0,w=+4) 碰撞于余数 4）、正常解密 w=+2 及越界失败反例 w=+5；右面板用对数纵轴对比 1000 km 光纤上 1G(10 ms)、2G(0.2 ms)、3G(1 us) 的不同操作时标及器件效率改变后的距离上确界。",
        "\n".join(parts),
    )
    return svg, {"lwe_fail_val": dec_bad, "l0_max_km": round(l0_max_km, 2)}


# ===========================================================================
# Figure 6: v3-14-weyl-chamber-zx.svg
# ===========================================================================
def build_fig6_weyl_chamber_zx() -> tuple[str, dict]:
    # Exact 4x4 matrix checks for iSWAP 2-CNOT synthesis & ZX T-count 2 -> 0
    i2 = [[1 + 0j, 0j], [0j, 1 + 0j]]
    x2 = [[0j, 1 + 0j], [1 + 0j, 0j]]
    h2 = [[1 / math.sqrt(2) + 0j, 1 / math.sqrt(2) + 0j], [1 / math.sqrt(2) + 0j, -1 / math.sqrt(2) + 0j]]
    s2 = [[1 + 0j, 0j], [0j, 1j]]
    t2 = [[1 + 0j, 0j], [0j, cmath.exp(1j * math.pi / 4.0)]]
    cn01 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    cn10 = [[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]]

    iswap_syn = matmul(kron(i2, h2), matmul(cn10, matmul(cn01, matmul(kron(h2, i2), kron(s2, s2)))))
    iswap_ref = [[1, 0, 0, 0], [0, 0, 1j, 0], [0, 1j, 0, 0], [0, 0, 0, 1]]
    assert max(abs(iswap_syn[i][j] - iswap_ref[i][j]) for i in range(4) for j in range(4)) < TOL

    zx_lhs = matmul(cn01, matmul(kron(i2, t2), matmul(cn10, matmul(kron(i2, t2), cn01))))
    zx_rhs = matmul(cn01, matmul(kron(i2, s2), matmul(cn10, cn01)))
    assert max(abs(zx_lhs[i][j] - zx_rhs[i][j]) for i in range(4) for j in range(4)) < TOL

    pt_lhs = matmul(cn10, matmul(kron(t2, i2), matmul(cn10, matmul(kron(x2, x2), matmul(cn01, matmul(kron(i2, t2), cn01))))))
    pt_rhs = matmul(kron(x2, x2), matmul(cn01, matmul(kron(i2, s2), cn01)))
    assert max(abs(pt_lhs[i][j] - pt_rhs[i][j]) for i in range(4) for j in range(4)) < TOL

    parts = [
        '  <text class="title ink" x="34" y="44">两比特 Weyl 室三维几何与 ZX 演算蜘蛛融合 / 相位传送</text>',
        f'  <text class="subtitle muted" x="34" y="68">左：按整体相位取商的 Weyl 室 k{sub("z")}≥0 上半室正交投影（含镜像下半室 √SWAP）与 CNOT 数；右：ZX 重写与消 T 门（2 → 0）</text>',
    ]

    # --- Left Card: 3D Orthographic Weyl Chamber Tetrahedron ---
    lx0, ly0, lw, lh = 32, 84, 456, 446
    parts.append(f'  <rect class="card" x="{lx0}" y="{ly0}" width="{lw}" height="{lh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{lx0 + 16}" y="{ly0 + 24}">(a) 两比特 Weyl 室正交投影（k{sub("z")} ≥ 0 上半室）</text>')

    # Normalized coordinates (u, v, w) = (kx, ky, kz) / (pi/4)
    ox, oy = 110.0, 320.0

    def proj(u: float, v: float, w: float) -> tuple[float, float]:
        return ox + 168.0 * u + 86.0 * v, oy + 42.0 * u - 54.0 * v - 146.0 * w

    pO = proj(0.0, 0.0, 0.0)
    pA1 = proj(1.0, 0.0, 0.0)
    pA2 = proj(1.0, 1.0, 0.0)
    pB = proj(1.0, 0.5, 0.0)
    pA3 = proj(1.0, 1.0, 1.0)
    pSp = proj(0.5, 0.5, 0.5)
    pSm = proj(0.5, 0.5, -0.5)

    # Coordinate axes stubs from O (cleanly avoiding gate labels)
    ax_u = proj(1.18, 0.0, 0.0)
    ax_v = proj(0.0, 0.44, 0.0)
    ax_w = proj(0.0, 0.0, 0.36)
    for ax_end, albl, dx, dy in (
        (ax_u, f"k{sub('x')}", 6, 12),
        (ax_v, f"k{sub('y')}", 8, 12),
        (ax_w, f"k{sub('z')}", -14, 4),
    ):
        parts.append(f'  <line class="s-muted" style="stroke-width:1.2;stroke-dasharray:3 3" x1="{pO[0]:.1f}" y1="{pO[1]:.1f}" x2="{ax_end[0]:.1f}" y2="{ax_end[1]:.1f}"/>')
        parts.append(f'  <path class="axishead" d="{arrow_poly(pO[0], pO[1], ax_end[0], ax_end[1], 7, 4)}"/>')
        parts.append(f'  <text class="xs muted" x="{ax_end[0] + dx:.1f}" y="{ax_end[1] + dy:.1f}">{albl}</text>')

    # Shaded faces: base k_z=0 (2-CNOT reachable) & upper 3-CNOT tetrahedron faces
    parts.append(f'  <polygon class="f-purple" style="fill-opacity:.18;stroke:none" points="{pO[0]:.1f},{pO[1]:.1f} {pA2[0]:.1f},{pA2[1]:.1f} {pA3[0]:.1f},{pA3[1]:.1f}"/>')
    parts.append(f'  <polygon class="f-purple" style="fill-opacity:.14;stroke:none" points="{pA1[0]:.1f},{pA1[1]:.1f} {pA2[0]:.1f},{pA2[1]:.1f} {pA3[0]:.1f},{pA3[1]:.1f}"/>')
    parts.append(f'  <polygon class="f-accent" style="fill-opacity:.38;stroke:none" points="{pO[0]:.1f},{pO[1]:.1f} {pA1[0]:.1f},{pA1[1]:.1f} {pA2[0]:.1f},{pA2[1]:.1f}"/>')

    # Tetrahedron edges (back edge O-A2 dashed, front edges solid)
    parts.append(f'  <line class="s-accent" style="stroke-width:1.6;stroke-dasharray:5 4" x1="{pO[0]:.1f}" y1="{pO[1]:.1f}" x2="{pA2[0]:.1f}" y2="{pA2[1]:.1f}"/>')
    parts.append(f'  <line class="s-green" style="stroke-width:2.6" x1="{pO[0]:.1f}" y1="{pO[1]:.1f}" x2="{pA1[0]:.1f}" y2="{pA1[1]:.1f}"/>')
    parts.append(f'  <line class="s-accent" style="stroke-width:2.2" x1="{pA1[0]:.1f}" y1="{pA1[1]:.1f}" x2="{pA2[0]:.1f}" y2="{pA2[1]:.1f}"/>')
    parts.append(f'  <line class="s-purple" style="stroke-width:2.2" x1="{pO[0]:.1f}" y1="{pO[1]:.1f}" x2="{pA3[0]:.1f}" y2="{pA3[1]:.1f}"/>')
    parts.append(f'  <line class="s-purple" style="stroke-width:2.0" x1="{pA1[0]:.1f}" y1="{pA1[1]:.1f}" x2="{pA3[0]:.1f}" y2="{pA3[1]:.1f}"/>')
    parts.append(f'  <line class="s-purple" style="stroke-width:2.0" x1="{pA2[0]:.1f}" y1="{pA2[1]:.1f}" x2="{pA3[0]:.1f}" y2="{pA3[1]:.1f}"/>')
    # Symmetric lower edge O -> sqrt(SWAP) at k_z = -pi/8
    parts.append(f'  <line class="s-warn" style="stroke-width:1.8;stroke-dasharray:4 3" x1="{pO[0]:.1f}" y1="{pO[1]:.1f}" x2="{pSm[0]:.1f}" y2="{pSm[1]:.1f}"/>')

    # Gate markers (color-coded by CNOT count: 0 muted, 1 green, 2 accent, 3 warn)
    for pt_xy, cls, r_c in (
        (pO, "muted", 5.5),
        (pA1, "green", 6.2),
        (pA2, "accent", 6.2),
        (pB, "accent", 5.4),
        (pA3, "warn", 6.4),
        (pSp, "warn", 5.2),
        (pSm, "warn", 5.6),
    ):
        parts.append(f'  <circle class="{cls} dot-ring" cx="{pt_xy[0]:.1f}" cy="{pt_xy[1]:.1f}" r="{r_c}"/>')

    # Non-overlapping gate labels with coordinates & CNOT counts
    parts.append(f'  <text class="xs ink" style="font-weight:700" x="{pO[0] - 10:.1f}" y="{pO[1] - 8:.1f}" text-anchor="end">I (0,0,0)</text>')
    parts.append(f'  <text class="xs muted" x="{pO[0] - 10:.1f}" y="{pO[1] + 12:.1f}" text-anchor="end">I 与 iI 同坐标</text>')

    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{pA3[0] - 12:.1f}" y="{pA3[1] - 7:.1f}" text-anchor="end">SWAP (π/4,π/4,π/4)</text>')
    parts.append(f'  <text class="xs warn" x="{pA3[0] - 12:.1f}" y="{pA3[1] + 13:.1f}" text-anchor="end">3 CNOT（极点 A{sub("3")}）</text>')

    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{pSp[0] - 12:.1f}" y="{pSp[1] - 12:.1f}" text-anchor="end">√SWAP† (π/8,π/8,+π/8)</text>')
    parts.append(f'  <text class="xs muted" x="{pSp[0] - 12:.1f}" y="{pSp[1] + 8:.1f}" text-anchor="end">3 CNOT（棱 O—A{sub("3")}）</text>')

    parts.append(f'  <text class="xs accent" style="font-weight:700" x="{pA2[0] + 10:.1f}" y="{pA2[1] - 14:.1f}">iSWAP (A{sub("2")})</text>')
    parts.append(f'  <text class="xs muted" x="{pA2[0] + 10:.1f}" y="{pA2[1] + 6:.1f}">(π/4,π/4,0)</text>')
    parts.append(f'  <text class="xs accent" x="{pA2[0] + 10:.1f}" y="{pA2[1] + 25:.1f}">2 CNOT</text>')

    parts.append(f'  <line class="s-accent" style="stroke-width:1.2" x1="{pB[0] + 5:.1f}" y1="{pB[1] + 4:.1f}" x2="366" y2="362"/>')
    parts.append('  <text class="xs accent" style="font-weight:700" x="370" y="362">B (π/4,π/8,0)</text>')
    parts.append('  <text class="xs accent" x="370" y="381">2 CNOT</text>')

    parts.append(f'  <line class="s-green" style="stroke-width:1.2" x1="{pA1[0] + 4:.1f}" y1="{pA1[1] + 6:.1f}" x2="314" y2="404"/>')
    parts.append(f'  <text class="xs green" style="font-weight:700" x="318" y="405">CNOT/CZ (π/4,0,0)</text>')
    parts.append('  <text class="xs green" x="318" y="424">1 CNOT（顶点 A₁）</text>')

    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{pSm[0] - 10:.1f}" y="{pSm[1] + 1:.1f}" text-anchor="end">√SWAP (π/8,π/8,−π/8)</text>')
    parts.append(f'  <text class="xs muted" x="{pSm[0] - 10:.1f}" y="{pSm[1] + 21:.1f}" text-anchor="end">3 CNOT（镜像下半室 k{sub("z")}&lt;0）</text>')

    # Green edge O-A1 label: R_ZZ(theta) aligned parallel above O-A1; 2-line k_z=0 base label cleanly inside triangle
    parts.append(f'  <text class="xs green" style="font-weight:700" x="182" y="332" text-anchor="middle" transform="rotate(14 182 332)">R{sub("ZZ")}(θ)</text>')
    parts.append('  <text class="xs accent" style="font-weight:600" x="252" y="326" text-anchor="middle">2-CNOT 底面</text>')
    parts.append(f'  <text class="xs accent" style="font-weight:600" x="252" y="344" text-anchor="middle">k{sub("z")} = 0</text>')

    # Bottom summary subcard
    parts.append(f'  <rect class="subcard" x="{lx0 + 14}" y="440" width="{lw - 28}" height="76" rx="8"/>')
    parts.append(f'  <text class="xs accent" style="font-weight:600" x="{lx0 + 24}" y="459">U = e{sup("iφ")} (k{sub("1")}⊗k{sub("2")}) exp[i(k{sub("x")}XX + k{sub("y")}YY + k{sub("z")}ZZ)] (k{sub("3")}⊗k{sub("4")})</text>')
    parts.append(f'  <text class="xs ink" x="{lx0 + 24}" y="480">0/1 CNOT: I / A{sub("1")} · 绿棱 R{sub("ZZ")}(θ) · 2 CNOT: 底面 k{sub("z")}=0 (iSWAP, B)</text>')
    parts.append(f'  <text class="xs warn" x="{lx0 + 24}" y="501">主四面体绘 k{sub("z")}≥0 上半室；√SWAP 在镜像下半室，k{sub("z")}≠0 均需 3 CNOT</text>')

    # --- Right Card: ZX-Calculus Rewrite Rules & Phase Teleportation ---
    rx0, ry0, rw, rh = 504, 84, 464, 446
    parts.append(f'  <rect class="card" x="{rx0}" y="{ry0}" width="{rw}" height="{rh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{rx0 + 16}" y="{ry0 + 24}">(b) ZX 演算核心重写与相位传送消 T 门</text>')

    def spider(sx_c: float, sy_c: float, phase: str, color: str = "green", r_s: float = 12.5) -> None:
        parts.append(f'  <circle class="f-{color}" style="fill-opacity:.85" cx="{sx_c:.1f}" cy="{sy_c:.1f}" r="{r_s:.1f}"/>')
        if phase:
            parts.append(f'  <text class="xs ink" style="font-weight:700" x="{sx_c:.1f}" y="{sy_c + 4:.1f}" text-anchor="middle">{phase}</text>')

    def h_box(hx: float, hy: float, sz: float = 13.0) -> None:
        parts.append(f'  <rect class="f-gold" style="fill-opacity:.90" x="{hx - sz / 2:.1f}" y="{hy - sz / 2:.1f}" width="{sz:.1f}" height="{sz:.1f}" rx="2.5"/>')
        parts.append(f'  <text class="xs ink" style="font-weight:700;font-size:9.5px" x="{hx:.1f}" y="{hy + 3.3:.1f}" text-anchor="middle">H</text>')

    # Subcard 1: Spider Fusion (Green & Red)
    parts.append('  <rect class="subcard" x="518" y="120" width="436" height="84" rx="8"/>')
    parts.append('  <text class="xs ink" style="font-weight:700" x="530" y="138">① 红绿蜘蛛融合律（同色相连，相位相加 mod 2π）</text>')
    parts.append('  <line class="divider" x1="736" y1="146" x2="736" y2="196"/>')
    for base_x, col_s, basis_t in ((540.0, "green", "Z 绿"), (754.0, "warn", "X 红")):
        sy1 = 172.0
        parts.append(f'  <line class="wire" x1="{base_x:.1f}" y1="{sy1 - 12:.1f}" x2="{base_x + 24:.1f}" y2="{sy1:.1f}"/>')
        parts.append(f'  <line class="wire" x1="{base_x:.1f}" y1="{sy1 + 12:.1f}" x2="{base_x + 24:.1f}" y2="{sy1:.1f}"/>')
        parts.append(f'  <line class="wire" x1="{base_x + 24:.1f}" y1="{sy1:.1f}" x2="{base_x + 70:.1f}" y2="{sy1:.1f}"/>')
        parts.append(f'  <line class="wire" x1="{base_x + 70:.1f}" y1="{sy1:.1f}" x2="{base_x + 94:.1f}" y2="{sy1 - 12:.1f}"/>')
        parts.append(f'  <line class="wire" x1="{base_x + 70:.1f}" y1="{sy1:.1f}" x2="{base_x + 94:.1f}" y2="{sy1 + 12:.1f}"/>')
        spider(base_x + 24, sy1, "α", col_s, 11.5)
        spider(base_x + 70, sy1, "β", col_s, 11.5)
        parts.append(f'  <text class="lbl ink" style="font-weight:700" x="{base_x + 109:.1f}" y="{sy1 + 5:.1f}" text-anchor="middle">=</text>')
        parts.append(f'  <line class="wire" x1="{base_x + 124:.1f}" y1="{sy1 - 12:.1f}" x2="{base_x + 152:.1f}" y2="{sy1:.1f}"/>')
        parts.append(f'  <line class="wire" x1="{base_x + 124:.1f}" y1="{sy1 + 12:.1f}" x2="{base_x + 152:.1f}" y2="{sy1:.1f}"/>')
        parts.append(f'  <line class="wire" x1="{base_x + 152:.1f}" y1="{sy1:.1f}" x2="{base_x + 180:.1f}" y2="{sy1 - 12:.1f}"/>')
        parts.append(f'  <line class="wire" x1="{base_x + 152:.1f}" y1="{sy1:.1f}" x2="{base_x + 180:.1f}" y2="{sy1 + 12:.1f}"/>')
        spider(base_x + 152, sy1, "α+β", col_s, 15.0)

    # Subcard 2: Hadamard Color Change & CNOT Translation
    parts.append('  <rect class="subcard" x="518" y="212" width="436" height="84" rx="8"/>')
    parts.append(f'  <text class="xs ink" style="font-weight:700" x="530" y="230">② Hadamard 变色律（H R{sub("z")}(α) H = R{sub("x")}(α)）与 CNOT 翻译</text>')
    parts.append('  <line class="divider" x1="772" y1="238" x2="772" y2="288"/>')
    sy2 = 264.0
    parts.append(f'  <line class="wire" x1="538" y1="{sy2 - 14:.1f}" x2="604" y2="{sy2:.1f}"/>')
    parts.append(f'  <line class="wire" x1="538" y1="{sy2 + 14:.1f}" x2="604" y2="{sy2:.1f}"/>')
    parts.append(f'  <line class="wire" x1="604" y1="{sy2:.1f}" x2="660" y2="{sy2:.1f}"/>')
    h_box(568, sy2 - 7)
    h_box(568, sy2 + 7)
    h_box(636, sy2)
    spider(604, sy2, "α", "green", 12.0)
    parts.append(f'  <text class="lbl ink" style="font-weight:700" x="676" y="{sy2 + 5:.1f}" text-anchor="middle">=</text>')
    parts.append(f'  <line class="wire" x1="694" y1="{sy2 - 14:.1f}" x2="722" y2="{sy2:.1f}"/>')
    parts.append(f'  <line class="wire" x1="694" y1="{sy2 + 14:.1f}" x2="722" y2="{sy2:.1f}"/>')
    parts.append(f'  <line class="wire" x1="722" y1="{sy2:.1f}" x2="756" y2="{sy2:.1f}"/>')
    spider(722, sy2, "α", "warn", 12.0)
    # CNOT translation on right
    cy_t, cy_b = 250.0, 278.0
    parts.append(f'  <line class="wire" x1="790" y1="{cy_t:.1f}" x2="844" y2="{cy_t:.1f}"/>')
    parts.append(f'  <line class="wire" x1="790" y1="{cy_b:.1f}" x2="844" y2="{cy_b:.1f}"/>')
    parts.append(f'  <line class="wire" x1="817" y1="{cy_t:.1f}" x2="817" y2="{cy_b + 8:.1f}"/>')
    parts.append(f'  <circle class="ctrl" cx="817" cy="{cy_t:.1f}" r="4.5"/>')
    parts.append(f'  <circle class="wire" cx="817" cy="{cy_b:.1f}" r="8"/>')
    parts.append(f'  <line class="wire" x1="809" y1="{cy_b:.1f}" x2="825" y2="{cy_b:.1f}"/>')
    parts.append('  <text class="lbl ink" style="font-weight:700" x="862" y="268" text-anchor="middle">=</text>')
    parts.append(f'  <line class="wire" x1="880" y1="{cy_t:.1f}" x2="938" y2="{cy_t:.1f}"/>')
    parts.append(f'  <line class="wire" x1="880" y1="{cy_b:.1f}" x2="938" y2="{cy_b:.1f}"/>')
    parts.append(f'  <line class="wire" x1="909" y1="{cy_t:.1f}" x2="909" y2="{cy_b:.1f}"/>')
    spider(909, cy_t, "0", "green", 9.0)
    spider(909, cy_b, "0", "warn", 9.0)

    # Subcard 3: Cross-CNOT Spider Fusion & Phase Teleportation (T-count 2 -> 0)
    parts.append('  <rect class="subcard" x="518" y="304" width="436" height="212" rx="8"/>')
    parts.append('  <text class="xs ink" style="font-weight:700" x="530" y="323">③ 跨 CNOT 融合与相位传送（T-count：2 → 0）</text>')

    w0, w1 = 348.0, 386.0
    # Left: 5-gate circuit CNOT01 - (I x T) - CNOT10 - (I x T) - CNOT01
    parts.append(f'  <text class="xs muted" x="530" y="{w0 + 4:.1f}">q{sub("0")}</text>')
    parts.append(f'  <text class="xs muted" x="530" y="{w1 + 4:.1f}">q{sub("1")}</text>')
    parts.append(f'  <line class="wire" x1="548" y1="{w0:.1f}" x2="718" y2="{w0:.1f}"/>')
    parts.append(f'  <line class="wire" x1="548" y1="{w1:.1f}" x2="718" y2="{w1:.1f}"/>')
    for gx_c, top_ctrl in ((566, True), (633, False), (700, True)):
        yc, yt = (w0, w1) if top_ctrl else (w1, w0)
        parts.append(f'  <line class="wire" x1="{gx_c}" y1="{w0:.1f}" x2="{gx_c}" y2="{w1:.1f}"/>')
        parts.append(f'  <circle class="ctrl" cx="{gx_c}" cy="{yc:.1f}" r="4.2"/>')
        parts.append(f'  <circle class="pill" style="stroke-width:1.8" cx="{gx_c}" cy="{yt:.1f}" r="7.5"/>')
        parts.append(f'  <line class="wire" x1="{gx_c - 7.5}" y1="{yt:.1f}" x2="{gx_c + 7.5}" y2="{yt:.1f}"/>')
        parts.append(f'  <line class="wire" x1="{gx_c}" y1="{yt - 7.5:.1f}" x2="{gx_c}" y2="{yt + 7.5:.1f}"/>')
    for tx_g in (600, 666):
        parts.append(f'  <rect class="f-warn" style="fill-opacity:.88" x="{tx_g - 11}" y="{w1 - 11:.1f}" width="22" height="22" rx="4"/>')
        parts.append(f'  <text class="xs ink" style="font-weight:700" x="{tx_g}" y="{w1 + 4:.1f}" text-anchor="middle">T</text>')

    # Rewrite arrow
    parts.append('  <line class="s-green" style="stroke-width:2.2" x1="726" y1="367" x2="758" y2="367"/>')
    parts.append(f'  <path class="green" d="{arrow_poly(726, 367, 761, 367, 8, 5)}"/>')
    parts.append('  <text class="xs green" style="font-weight:700" x="743" y="357" text-anchor="middle">ZX</text>')
    parts.append('  <text class="xs green" style="font-weight:700" x="743" y="382" text-anchor="middle">融合</text>')

    # Right: Fused ZX diagram (q1 has single green pi/2 spider = S!)
    parts.append(f'  <line class="wire" x1="772" y1="{w0:.1f}" x2="942" y2="{w0:.1f}"/>')
    parts.append(f'  <line class="wire" x1="772" y1="{w1:.1f}" x2="942" y2="{w1:.1f}"/>')
    for gx_z, top_g, ph_b in ((794, True, "0"), (857, False, "π/2"), (920, True, "0")):
        parts.append(f'  <line class="wire" x1="{gx_z}" y1="{w0:.1f}" x2="{gx_z}" y2="{w1:.1f}"/>')
        if top_g:
            spider(gx_z, w0, "0", "green", 9.0)
            spider(gx_z, w1, "0", "warn", 9.0)
        else:
            spider(gx_z, w0, "0", "warn", 9.5)
            spider(gx_z, w1, ph_b, "green", 14.5)

    # Bottom explanation rows inside Subcard 3
    parts.append('  <line class="divider" x1="530" y1="414" x2="942" y2="414"/>')
    parts.append(f'  <text class="xs green" style="font-weight:700" x="530" y="434">融合结果：π/4 + 0 + π/4 = π/2（S 门），T-count 从 2 骤降为 0</text>')
    parts.append(f'  <text class="xs accent" style="font-weight:700" x="530" y="456">跨比特相位传送（Phase Teleportation）：</text>')
    parts.append(f'  <text class="xs ink" x="530" y="476">两相位小工具跨 X⊗X 合并为 (X⊗X)CNOT{sub("01")}(I⊗S)CNOT{sub("01")}</text>')
    parts.append(f'  <text class="xs muted" x="530" y="498">不仅 T-count 2→0，双比特 CNOT 亦从 4→2（线路提取须满足 gflow）。</text>')

    parts.append('  <text class="sm muted" x="34" y="554">注：左图 KAK 几何锁定任意两比特门最优双比特门数，右图 ZX 图重写突破局部窗口实现全局非 Clifford T 门削减。</text>')

    svg = wrap_svg(
        "v3-14-weyl-chamber-zx",
        "两比特 Weyl 室几何与 ZX 演算蜘蛛融合及相位传送",
        "左面板正交投影绘出两比特 SU(4) Weyl 室 k_z>=0 上半室四面体、绿棱 R_ZZ(θ)、I/CNOT/iSWAP/SWAP/B 门坐标以及镜像下半室对应位置的 √SWAP(π/8,π/8,-π/8) 与所需 CNOT 数；右面板展示 ZX 演算红绿蜘蛛融合、Hadamard 变色、CNOT 翻译及跨 CNOT 融合/相位传送消 T 门。",
        "\n".join(parts),
    )
    return svg, {"iswap_2cnot_ok": True, "zx_fusion_ok": True, "phase_teleport_ok": True}


# ===========================================================================
# Figure 7: v3-15-wilson-wald-drift.svg
# ===========================================================================
def build_fig7_wilson_wald_drift() -> tuple[str, dict]:
    # Exact binomial coverage at N = 100, nominal 95% (z = 1.959963984540054)
    n_bin = 100
    z95 = 1.959963984540054
    alpha = 0.05

    def wald_ci(k: int) -> tuple[float, float]:
        ph = k / n_bin
        h = z95 * math.sqrt(ph * (1.0 - ph) / n_bin)
        return ph - h, ph + h

    def wilson_ci(k: int) -> tuple[float, float]:
        ph = k / n_bin
        den = 1.0 + (z95 * z95) / n_bin
        c = (ph + (z95 * z95) / (2.0 * n_bin)) / den
        h = z95 * math.sqrt(ph * (1.0 - ph) / n_bin + (z95 * z95) / (4.0 * n_bin * n_bin)) / den
        return c - h, c + h

    def cp_ci(k: int) -> tuple[float, float]:
        if k == 0:
            lo = 0.0
        else:
            a, b = 0.0, 1.0
            for _ in range(56):
                m = 0.5 * (a + b)
                tail = sum(binom_pmf(n_bin, j, m) for j in range(k, n_bin + 1))
                if tail < alpha / 2.0:
                    a = m
                else:
                    b = m
            lo = 0.5 * (a + b)
        if k == n_bin:
            hi = 1.0
        else:
            a, b = 0.0, 1.0
            for _ in range(56):
                m = 0.5 * (a + b)
                tail = sum(binom_pmf(n_bin, j, m) for j in range(0, k + 1))
                if tail < alpha / 2.0:
                    b = m
                else:
                    a = m
            hi = 0.5 * (a + b)
        return lo, hi

    wald_ivs = [wald_ci(k) for k in range(n_bin + 1)]
    wils_ivs = [wilson_ci(k) for k in range(n_bin + 1)]
    cp_ivs = [cp_ci(k) for k in range(n_bin + 1)]

    def exact_cov(ivs: list[tuple[float, float]], p_val: float) -> float:
        return sum(binom_pmf(n_bin, k, p_val) for k in range(n_bin + 1) if ivs[k][0] <= p_val <= ivs[k][1])

    cov_w_05 = exact_cov(wald_ivs, 0.05)
    cov_w_03 = exact_cov(wald_ivs, 0.03)
    assert abs(cov_w_05 - 0.8775) < 5e-4
    assert abs(cov_w_03 - 0.8022) < 5e-4

    # Grid of p in [0.01, 0.50] (dense 246 points -> crisp jagged oscillations)
    p_grid = [0.01 + 0.002 * i for i in range(246)]
    wald_covs = [exact_cov(wald_ivs, pv) for pv in p_grid]
    wils_covs = [exact_cov(wils_ivs, pv) for pv in p_grid]
    cp_covs = [exact_cov(cp_ivs, pv) for pv in p_grid]
    assert min(cp_covs) >= 0.95 - 1e-9

    # Ch15 §3.3 exact 10-batch drift counts (seed 20260923, 200 shots/batch, linear p 0.50 -> 0.62)
    k00 = [110, 109, 106, 111, 95, 106, 120, 133, 117, 127]
    ps = [k / 200.0 for k in k00]
    p_pool = sum(ps) / 10.0
    p_first = sum(k00[:5]) / 1000.0
    p_last = sum(k00[5:]) / 1000.0
    se_diff = math.sqrt(p_pool * (1.0 - p_pool) * (2.0 / 1000.0))
    z_diff = (p_last - p_first) / se_diff
    naive_se = math.sqrt(p_pool * (1.0 - p_pool) / 2000.0)
    clust_se = math.sqrt(sum((x - p_pool) ** 2 for x in ps) / 9.0) / math.sqrt(10.0)
    se_ratio = clust_se / naive_se
    assert abs(p_first - 0.531) < 1e-9 and abs(p_last - 0.603) < 1e-9
    assert abs(z_diff - 3.249) < 1e-3 and abs(naive_se - 0.01108) < 1e-5
    assert abs(clust_se - 0.01756) < 1e-5 and abs(se_ratio - 1.585) < 0.01

    parts = [
        '  <text class="title ink" x="34" y="44">Wald 区间覆盖率崩塌与汇总柱图掩盖线性时间漂移</text>',
        '  <text class="subtitle muted" x="34" y="68">左：N=100 精确二项求和 95% 覆盖率（Wald vs Wilson vs Clopper–Pearson）；右：汇总直方图掩盖 10 批漂移与聚类 SE</text>',
    ]

    # --- Left Card: Exact Binomial Coverage (N = 100) ---
    lx0, ly0, lw, lh = 32, 84, 460, 446
    parts.append(f'  <rect class="card" x="{lx0}" y="{ly0}" width="{lw}" height="{lh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{lx0 + 16}" y="{ly0 + 24}">(a) N = 100 名义 95% 置信区间精确覆盖率</text>')

    px, py, pw, ph = 94.0, 128.0, 380.0, 314.0

    def sx(p_v: float) -> float:
        return px + (p_v / 0.50) * pw

    def sy(c_v: float) -> float:
        return py + ph - ((c_v - 0.60) / 0.40) * ph

    for pv in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
        gx = sx(pv)
        parts.append(f'  <line class="grid" x1="{gx:.1f}" y1="{py:.1f}" x2="{gx:.1f}" y2="{py + ph:.1f}"/>')
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{gx:.1f}" y1="{py + ph:.1f}" x2="{gx:.1f}" y2="{py + ph + 5:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{gx:.1f}" y="{py + ph + 19:.1f}" text-anchor="middle">{pv:.1f}</text>')
    for cv in (0.60, 0.70, 0.80, 0.90, 0.95, 1.00):
        gy = sy(cv)
        parts.append(f'  <line class="grid" x1="{px:.1f}" y1="{gy:.1f}" x2="{px + pw:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <line class="axis" style="stroke-width:1.3" x1="{px - 5:.1f}" y1="{gy:.1f}" x2="{px:.1f}" y2="{gy:.1f}"/>')
        tcls = "xs gold" if abs(cv - 0.95) < 1e-6 else "xs ink"
        parts.append(f'  <text class="{tcls}" x="{px - 9:.1f}" y="{gy + 4:.1f}" text-anchor="end">{int(round(cv * 100))}%</text>')

    # Nominal 95% line
    y95 = sy(0.95)
    parts.append(f'  <line class="s-gold" style="stroke-width:1.6;stroke-dasharray:6 4" x1="{px:.1f}" y1="{y95:.1f}" x2="{px + pw:.1f}" y2="{y95:.1f}"/>')

    # Coverage curves
    parts.append(f'  <path class="s-green" style="stroke-width:2.0" d="{polyline_d([(sx(p), sy(c)) for p, c in zip(p_grid, cp_covs)])}"/>')
    parts.append(f'  <path class="s-accent" style="stroke-width:2.0" d="{polyline_d([(sx(p), sy(c)) for p, c in zip(p_grid, wils_covs)])}"/>')
    parts.append(f'  <path class="s-warn" style="stroke-width:2.1" d="{polyline_d([(sx(p), sy(c)) for p, c in zip(p_grid, wald_covs)])}"/>')

    # Highlight p=0.05 (87.75%) and p=0.03 (80.22%) on Wald curve
    x05, y05 = sx(0.05), sy(cov_w_05)
    x03, y03 = sx(0.03), sy(cov_w_03)
    parts.append(f'  <circle class="warn dot-ring" cx="{x05:.1f}" cy="{y05:.1f}" r="4.6"/>')
    parts.append(f'  <circle class="warn dot-ring" cx="{x03:.1f}" cy="{y03:.1f}" r="4.6"/>')

    parts.append(f'  <line class="s-warn" style="stroke-width:1.4" x1="{x05 + 5:.1f}" y1="{y05:.1f}" x2="206" y2="{y05:.1f}"/>')
    parts.append(f'  <rect class="pill" x="206" y="{y05 - 13:.1f}" width="174" height="26" rx="6"/>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="214" y="{y05 + 4:.1f}">p = 0.05：Wald 跌至 87.75%</text>')

    parts.append(f'  <line class="s-warn" style="stroke-width:1.4" x1="{x03 + 5:.1f}" y1="{y03:.1f}" x2="206" y2="{y03:.1f}"/>')
    parts.append(f'  <rect class="pill" x="206" y="{y03 - 13:.1f}" width="174" height="26" rx="6"/>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="214" y="{y03 + 4:.1f}">p = 0.03：Wald 跌至 80.22%</text>')

    # Legend pill in clean lower-right open space
    parts.append('  <rect class="pill" x="254" y="346" width="212" height="86" rx="8"/>')
    leg = [
        ("green", "", "Clopper–Pearson（恒 ≥ 95%）"),
        ("accent", "", "Wilson 得分（稳贴 95% 线）"),
        ("warn", "", "Wald 区间（低 p 剧烈崩塌）"),
        ("gold", "6 4", "名义 95% 置信水平参考线"),
    ]
    for idx, (col, dash, txt) in enumerate(leg):
        ly_i = 364 + idx * 19
        da = f';stroke-dasharray:{dash}' if dash else ""
        parts.append(f'  <line class="s-{col}" style="stroke-width:2.2{da}" x1="264" y1="{ly_i - 3}" x2="284" y2="{ly_i - 3}"/>')
        parts.append(f'  <text class="xs {col}" x="290" y="{ly_i + 1}">{txt}</text>')

    parts.append(f'  <rect class="axis" x="{px:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}"/>')
    parts.append(f'  <text class="lbl ink" x="{px + pw / 2:.1f}" y="{py + ph + 44:.1f}" text-anchor="middle">真实二项概率 p（关于 p = 0.5 对称）</text>')
    parts.append(f'  <text class="lbl ink" x="48" y="{py + ph / 2:.1f}" text-anchor="middle" transform="rotate(-90 48 {py + ph / 2:.1f})">真实覆盖率（%）</text>')
    parts.append(f'  <text class="xs muted" x="{lx0 + 16}" y="{ly0 + lh - 12}">注：k=0 时 Wald 退化为 [0,0]；Wilson 与 CP 始终给出非零安全上界。</text>')

    # --- Right Card: Pooled Bar Chart Masks 10-Batch Linear Time Drift ---
    rx0, ry0, rw, rh = 508, 84, 460, 446
    parts.append(f'  <rect class="card" x="{rx0}" y="{ry0}" width="{rw}" height="{rh}" rx="12"/>')
    parts.append(f'  <text class="h2 ink" x="{rx0 + 16}" y="{ry0 + 24}">(b) 汇总柱状图掩盖 10 批次线性时间漂移</text>')

    # Left mini-plot: Pooled histogram (looks close to flat 50/50)
    hx, hy, hw, hh = 524.0, 146.0, 108.0, 214.0
    parts.append(f'  <text class="xs ink" style="font-weight:600" x="{hx + hw / 2:.1f}" y="136" text-anchor="middle">汇总柱图 (N=2000)</text>')
    parts.append(f'  <rect class="subcard" x="{hx:.1f}" y="{hy:.1f}" width="{hw:.1f}" height="{hh:.1f}" rx="6"/>')
    # 50/50 ideal reference line inside histogram
    y_50h = hy + hh - (0.50 / 0.75) * hh
    parts.append(f'  <line class="s-gold" style="stroke-width:1.4;stroke-dasharray:4 3" x1="{hx + 6:.1f}" y1="{y_50h:.1f}" x2="{hx + hw - 6:.1f}" y2="{y_50h:.1f}"/>')
    parts.append(f'  <text class="xs gold" x="{hx + hw - 8:.1f}" y="{y_50h - 5:.1f}" text-anchor="end">50/50 线</text>')
    # Two pooled bars: |00> = 56.7%, |11> = 43.3%
    h_00 = (p_pool / 0.75) * hh
    h_11 = ((1.0 - p_pool) / 0.75) * hh
    parts.append(f'  <rect class="b-accent" x="{hx + 16:.1f}" y="{hy + hh - h_00:.1f}" width="32" height="{h_00:.1f}" rx="4"/>')
    parts.append(f'  <rect class="b-purple" x="{hx + 60:.1f}" y="{hy + hh - h_11:.1f}" width="32" height="{h_11:.1f}" rx="4"/>')
    parts.append(f'  <text class="xs accent" style="font-weight:700" x="{hx + 32:.1f}" y="{hy + hh - h_00 - 6:.1f}" text-anchor="middle">56.7%</text>')
    parts.append(f'  <text class="xs purple" style="font-weight:700" x="{hx + 76:.1f}" y="{hy + hh - h_11 - 6:.1f}" text-anchor="middle">43.3%</text>')
    parts.append(f'  <text class="xs ink" x="{hx + 32:.1f}" y="{hy + hh + 16:.1f}" text-anchor="middle">|00⟩</text>')
    parts.append(f'  <text class="xs ink" x="{hx + 76:.1f}" y="{hy + hh + 16:.1f}" text-anchor="middle">|11⟩</text>')
    parts.append(f'  <text class="xs warn" x="{hx + hw / 2:.1f}" y="{hy + hh + 33:.1f}" text-anchor="middle">漂移完全隐匿</text>')

    # Connecting arrow -> time-series breakdown
    parts.append('  <line class="s-warn" style="stroke-width:2.0" x1="636" y1="252" x2="656" y2="252"/>')
    parts.append(f'  <path class="warn" d="{arrow_poly(636, 252, 659, 252, 7, 4.5)}"/>')

    # Right main plot: 10-batch time trajectory (seed 20260923)
    tx, ty, tw, th = 696.0, 146.0, 256.0, 214.0
    parts.append(f'  <text class="xs ink" style="font-weight:600" x="{tx + tw / 2:.1f}" y="136" text-anchor="middle">拆分为 10 个时间批次（每批 200 shots）</text>')

    def bsx(b_idx: float) -> float:
        return tx + ((b_idx - 0.5) / 10.0) * tw

    def bsy(pv: float) -> float:
        return ty + th - ((pv - 0.42) / 0.30) * th

    # Half-split shaded background (batches 1..5 vs 6..10)
    x_mid = tx + tw / 2.0
    parts.append(f'  <rect class="f-accent" style="fill-opacity:.14;stroke:none" x="{tx:.1f}" y="{ty:.1f}" width="{tw / 2:.1f}" height="{th:.1f}"/>')
    parts.append(f'  <rect class="f-warn" style="fill-opacity:.14;stroke:none" x="{x_mid:.1f}" y="{ty:.1f}" width="{tw / 2:.1f}" height="{th:.1f}"/>')

    for pv in (0.45, 0.50, 0.55, 0.60, 0.65, 0.70):
        gy = bsy(pv)
        parts.append(f'  <line class="grid" x1="{tx:.1f}" y1="{gy:.1f}" x2="{tx + tw:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'  <text class="xs ink" x="{tx - 6:.1f}" y="{gy + 4:.1f}" text-anchor="end">{pv:.2f}</text>')
    for b_i in range(1, 11):
        gx = bsx(b_i)
        parts.append(f'  <text class="xs ink" x="{gx:.1f}" y="{ty + th + 16:.1f}" text-anchor="middle">{b_i}</text>')

    # True linear drift line 0.50 -> 0.62
    parts.append(f'  <line class="s-gold" style="stroke-width:1.8;stroke-dasharray:5 3" x1="{bsx(1):.1f}" y1="{bsy(0.50):.1f}" x2="{bsx(10):.1f}" y2="{bsy(0.62):.1f}"/>')
    # First-half & second-half horizontal mean lines
    parts.append(f'  <line class="s-accent" style="stroke-width:2.0;stroke-dasharray:4 2" x1="{tx + 4:.1f}" y1="{bsy(p_first):.1f}" x2="{x_mid - 3:.1f}" y2="{bsy(p_first):.1f}"/>')
    parts.append(f'  <line class="s-warn" style="stroke-width:2.0;stroke-dasharray:4 2" x1="{x_mid + 3:.1f}" y1="{bsy(p_last):.1f}" x2="{tx + tw - 4:.1f}" y2="{bsy(p_last):.1f}"/>')

    # Observed 10-batch polyline & markers (fill:none via .axis, dark-mode adaptive)
    b_pts = [(bsx(i + 1), bsy(p_i)) for i, p_i in enumerate(ps)]
    parts.append(f'  <path class="axis" style="stroke-width:1.9" d="{polyline_d(b_pts)}"/>')
    for idx, (bx_p, by_p) in enumerate(b_pts):
        cls_d = "accent" if idx < 5 else "warn"
        parts.append(f'  <circle class="{cls_d} dot-ring" cx="{bx_p:.1f}" cy="{by_p:.1f}" r="4.0"/>')

    # Annotations inside clean top/bottom areas of time-series plot
    parts.append(f'  <text class="xs accent" style="font-weight:700" x="{tx + tw * 0.25:.1f}" y="{ty + 17:.1f}" text-anchor="middle">前 5 批 0.531</text>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{tx + tw * 0.75:.1f}" y="{ty + 17:.1f}" text-anchor="middle">后 5 批 0.603</text>')
    parts.append(f'  <text class="xs warn" style="font-weight:700" x="{tx + tw - 6:.1f}" y="{ty + th - 10:.1f}" text-anchor="end">z = 3.249 · χ{sup("2")} = 22.61</text>')

    parts.append(f'  <rect class="axis" x="{tx:.1f}" y="{ty:.1f}" width="{tw:.1f}" height="{th:.1f}"/>')
    parts.append(f'  <text class="xs ink" x="{tx + tw / 2:.1f}" y="{ty + th + 33:.1f}" text-anchor="middle">采集时间批次 b（虚线：真值 0.50→0.62）</text>')

    # Bottom SE comparison subcard (Naive SE 0.01108 vs Clustered SE 0.01756 = 1.59x)
    parts.append(f'  <rect class="subcard" x="{rx0 + 14}" y="408" width="{rw - 28}" height="108" rx="8"/>')
    parts.append(f'  <text class="xs ink" style="font-weight:700" x="{rx0 + 24}" y="427">忽略漂移合并算朴素 SE vs 按 10 批算聚类 SE（差距 1.59×）</text>')

    # Visual proportional error bars centered at x = 768
    ec_x = 766.0
    hw_naive = 32.0
    hw_clust = hw_naive * se_ratio
    parts.append(f'  <text class="xs warn" style="font-weight:600" x="{rx0 + 24}" y="452">朴素 SE = 0.01108</text>')
    parts.append(f'  <line class="s-warn" style="stroke-width:2.6" x1="{ec_x - hw_naive:.1f}" y1="448" x2="{ec_x + hw_naive:.1f}" y2="448"/>')
    parts.append(f'  <line class="s-warn" style="stroke-width:2.0" x1="{ec_x - hw_naive:.1f}" y1="443" x2="{ec_x - hw_naive:.1f}" y2="453"/>')
    parts.append(f'  <line class="s-warn" style="stroke-width:2.0" x1="{ec_x + hw_naive:.1f}" y1="443" x2="{ec_x + hw_naive:.1f}" y2="453"/>')
    parts.append(f'  <circle class="warn" cx="{ec_x:.1f}" cy="448" r="3.6"/>')
    parts.append('  <text class="xs muted" x="836" y="452">虚窄误差条</text>')

    parts.append(f'  <text class="xs green" style="font-weight:700" x="{rx0 + 24}" y="478">聚类 SE = 0.01756</text>')
    parts.append(f'  <line class="s-green" style="stroke-width:2.6" x1="{ec_x - hw_clust:.1f}" y1="474" x2="{ec_x + hw_clust:.1f}" y2="474"/>')
    parts.append(f'  <line class="s-green" style="stroke-width:2.0" x1="{ec_x - hw_clust:.1f}" y1="469" x2="{ec_x - hw_clust:.1f}" y2="479"/>')
    parts.append(f'  <line class="s-green" style="stroke-width:2.0" x1="{ec_x + hw_clust:.1f}" y1="469" x2="{ec_x + hw_clust:.1f}" y2="479"/>')
    parts.append(f'  <circle class="green" cx="{ec_x:.1f}" cy="474" r="3.6"/>')
    parts.append('  <text class="xs green" style="font-weight:700" x="836" y="478">真实宽 1.59×</text>')

    parts.append(f'  <text class="xs muted" x="{rx0 + 24}" y="504">对称漂移（如 0.40→0.60）更可汇总成精确 50/50 柱图，须分批交错采集。</text>')

    parts.append('  <text class="sm muted" x="34" y="554">注：左图由 N=100 精确二项概率求和计算（无蒙特卡洛误差）；右图严格复现第 15 章 §3.3 种子 20260923 数据。</text>')

    svg = wrap_svg(
        "v3-15-wilson-wald-drift",
        "Wald 置信区间覆盖率崩溃 vs Wilson 区间与时间漂移隐匿演示",
        "左面板精确计算 N=100 名义 95% 置信水平下 Wald、Wilson 与 Clopper-Pearson 覆盖率曲线，标注 p=0.05 跌至 87.75% 与 p=0.03 跌至 80.22%；右面板对比汇总直方图与 10 批线性时间漂移轨迹及朴素/聚类标准误 1.59 倍差距。",
        "\n".join(parts),
    )
    return svg, {
        "wald_cov_p05": round(cov_w_05 * 100, 2),
        "wald_cov_p03": round(cov_w_03 * 100, 2),
        "drift_z": round(z_diff, 3),
        "se_ratio": round(se_ratio, 2),
    }


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    builders = [
        ("v3-09-hardware-tradeoff-map.svg", build_fig1_hardware_tradeoff_map),
        ("v3-09-entangling-gates-six-platforms.svg", build_fig2_entangling_gates_six_platforms),
        ("v3-11-benchmark-scaling-eplg.svg", build_fig3_benchmark_scaling_eplg),
        ("v3-11-ftqc-resource-budget.svg", build_fig4_ftqc_resource_budget),
        ("v3-12-lwe-lattice-repeaters.svg", build_fig5_lwe_lattice_repeaters),
        ("v3-14-weyl-chamber-zx.svg", build_fig6_weyl_chamber_zx),
        ("v3-15-wilson-wald-drift.svg", build_fig7_wilson_wald_drift),
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
