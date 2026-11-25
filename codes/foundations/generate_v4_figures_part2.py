#!/usr/bin/env python3
"""Generate 6 light/dark-adaptive scientific SVG figures (V4 Part 2: Ch11, Ch13,
Ch16, Ch18, Ch20, Ch21) using Python 3 standard library only.

Outputs to handbook/assets/ (viewBox="0 0 960 460", all <text> >= 11.5px):
  1. v4-11-decoder-latency-budget.svg     (Ch11: 1 us decoder waterfall & qubit split)
  2. v4-13-entropy-dpi-chain.svg          (Ch13: DPI hub DAG & depolarizing curves)
  3. v4-16-walk-shadows.svg               (Ch16: t=30 Hadamard walk & classical shadows)
  4. v4-18-capacity-complexity-ladder.svg (Ch18: capacity/PLOB curves & complexity ladder)
  5. v4-20-sensing-ramsey-qfi.svg         (Ch20: Ramsey pulses/QFI & clock/gravimeter)
  6. v4-21-sim-engines-architecture.svg   (Ch21: Stabilizer / MPS-PEPS / Pauli engines)

Run:
  python3 codes/foundations/generate_v4_figures_part2.py

Dependencies:
  Python 3 standard library only (cmath, math, pathlib, xml.etree.ElementTree,
  xml.sax.saxutils). Deterministic exact mathematical evaluation (no RNG).
"""

from __future__ import annotations

import cmath
import math
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT / "handbook" / "assets"
W, H = 960, 460

COMMON_CSS = """
:root{color-scheme:light dark}
text{font-family:system-ui,-apple-system,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif}
.bg{fill:#FAF8F3}
.panel{fill:#FFFFFF;stroke:#D3CCC0;stroke-width:1.35}
.subpanel{fill:#F4F0E8;stroke:#D8D1C4;stroke-width:1.15}
.phead{fill:#EFECE2}
.title{font-size:18.5px;font-weight:700;fill:#14453d}
.subtitle{font-size:12px;font-weight:400;fill:#435B55}
.sec{font-size:13.5px;font-weight:700;fill:#14453d}
.lbl{font-size:12px;font-weight:500;fill:#1A3530}
.lblb{font-size:12px;font-weight:700;fill:#14453d}
.sm{font-size:11.5px;font-weight:400;fill:#435B55}
.smb{font-size:11.5px;font-weight:600;fill:#1A3530}
.math-txt{font-family:Georgia,'Times New Roman',serif;font-size:12.5px;font-weight:700;fill:#14453d}
.mono{font-family:ui-monospace,'SFMono-Regular',Menlo,Consolas,monospace;font-size:11.5px;font-weight:600;fill:#1A3530}
.axis{stroke:#1A3530;stroke-width:1.5;fill:none}
.axis-fill{fill:#1A3530}
.grid{stroke:#E2DDD2;stroke-width:1;fill:none}
.guide{stroke:#7A8E88;stroke-width:1.2;stroke-dasharray:5 4;fill:none}
.c1{stroke:#14453d;fill:none}
.c1-fill{fill:#14453d}
.c1-txt{fill:#14453d}
.c1-soft{fill:#E2F2EC;stroke:#14453d;stroke-width:1.4}
.c2{stroke:#C44B31;fill:none}
.c2-fill{fill:#C44B31}
.c2-txt{fill:#A43821}
.c2-soft{fill:#FCE8E2;stroke:#C44B31;stroke-width:1.4}
.c3{stroke:#1B6CA8;fill:none}
.c3-fill{fill:#1B6CA8}
.c3-txt{fill:#155485}
.c3-soft{fill:#E2F0FA;stroke:#1B6CA8;stroke-width:1.4}
.c4{stroke:#B57614;fill:none}
.c4-fill{fill:#B57614}
.c4-txt{fill:#8C580B}
.c4-soft{fill:#FDF3DC;stroke:#B57614;stroke-width:1.4}
.c5{stroke:#6B4EA8;fill:none}
.c5-fill{fill:#6B4EA8}
.c5-txt{fill:#51358A}
.c5-soft{fill:#EFE9FB;stroke:#6B4EA8;stroke-width:1.4}
.note{fill:#FAF3E0;stroke:#C48B22;stroke-width:1.25}
.pill{fill:#F3EFE6;stroke:#A8B5B0;stroke-width:1.15}
.pill-bg{fill:#FFFFFF;fill-opacity:.94;stroke:#A8B5B0;stroke-width:1.1}
.area1{fill:#14453d;fill-opacity:.14}
.area2{fill:#C44B31;fill-opacity:.13}
.area3{fill:#1B6CA8;fill-opacity:.13}
.area4{fill:#B57614;fill-opacity:.14}
.bar-neutral{fill:#E5E0D5;stroke:#5D706B;stroke-width:1.3}
.badge-txt{fill:#FAF8F3;font-size:11.5px;font-weight:700}
.hatch-stroke1{stroke:#14453d;stroke-width:1.1;stroke-opacity:.38}
.hatch-stroke2{stroke:#C44B31;stroke-width:1.1;stroke-opacity:.42}
.hatch-stroke3{stroke:#1B6CA8;stroke-width:1.1;stroke-opacity:.38}
@media(prefers-color-scheme:dark){
  .bg{fill:#111917}
  .panel{fill:#172320;stroke:#314842}
  .subpanel{fill:#1C2B27;stroke:#3A544D}
  .phead{fill:#1F312C}
  .title,.sec,.lblb,.math-txt{fill:#d9ebe5}
  .subtitle,.sm{fill:#9FBAB2}
  .lbl,.smb,.mono{fill:#CFE3DC}
  .axis{stroke:#C4DCD4}
  .axis-fill{fill:#C4DCD4}
  .grid{stroke:#283C36}
  .guide{stroke:#6F8F86}
  .c1{stroke:#5DD1A8}
  .c1-fill{fill:#5DD1A8}
  .c1-txt{fill:#84E2C0}
  .c1-soft{fill:#153B30;stroke:#5DD1A8}
  .c2{stroke:#F28872}
  .c2-fill{fill:#F28872}
  .c2-txt{fill:#F8AA99}
  .c2-soft{fill:#48241E;stroke:#F28872}
  .c3{stroke:#6BC2F5}
  .c3-fill{fill:#6BC2F5}
  .c3-txt{fill:#92D4FA}
  .c3-soft{fill:#173A52;stroke:#6BC2F5}
  .c4{stroke:#F0BA5A}
  .c4-fill{fill:#F0BA5A}
  .c4-txt{fill:#F6CE86}
  .c4-soft{fill:#3C2F14;stroke:#F0BA5A}
  .c5{stroke:#B99CF5}
  .c5-fill{fill:#B99CF5}
  .c5-txt{fill:#D0BAFA}
  .c5-soft{fill:#2D2147;stroke:#B99CF5}
  .note{fill:#312814;stroke:#D6A240}
  .pill{fill:#1E302B;stroke:#4B6B62}
  .pill-bg{fill:#172320;fill-opacity:.94;stroke:#4B6B62}
  .area1{fill:#5DD1A8;fill-opacity:.18}
  .area2{fill:#F28872;fill-opacity:.17}
  .area3{fill:#6BC2F5;fill-opacity:.17}
  .area4{fill:#F0BA5A;fill-opacity:.17}
  .bar-neutral{fill:#263833;stroke:#87A69D}
  .badge-txt{fill:#111917}
  .hatch-stroke1{stroke:#5DD1A8;stroke-opacity:.45}
  .hatch-stroke2{stroke:#F28872;stroke-opacity:.48}
  .hatch-stroke3{stroke:#6BC2F5;stroke-opacity:.45}
}
"""

COMMON_DEFS = """  <defs>
    <marker id="arr-ink" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
      <path d="M1,1.5 L8.5,5 L1,8.5 Z" class="axis-fill"/>
    </marker>
    <marker id="arr-c1" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
      <path d="M1,1.5 L8.5,5 L1,8.5 Z" class="c1-fill"/>
    </marker>
    <marker id="arr-c2" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
      <path d="M1,1.5 L8.5,5 L1,8.5 Z" class="c2-fill"/>
    </marker>
    <marker id="arr-c3" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
      <path d="M1,1.5 L8.5,5 L1,8.5 Z" class="c3-fill"/>
    </marker>
    <pattern id="hatch-c1" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line class="hatch-stroke1" x1="0" y1="0" x2="0" y2="7"/>
    </pattern>
    <pattern id="hatch-c2" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
      <line class="hatch-stroke2" x1="0" y1="0" x2="0" y2="7"/>
    </pattern>
    <pattern id="hatch-c3" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line class="hatch-stroke3" x1="0" y1="0" x2="0" y2="7"/>
    </pattern>
  </defs>"""


def h2(p: float) -> float:
    """Binary Shannon entropy in bits."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def fmt_pts(pts: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)


class SvgDoc:
    """Minimal deterministic SVG builder using Python stdlib only."""

    def __init__(self, title: str, desc: str, heading: str, subtitle: str, footer: str):
        self.title = title
        self.desc = desc
        self.footer = footer
        self.body: list[str] = []
        self.body.append(f'  <rect class="bg" x="0" y="0" width="{W}" height="{H}" rx="14"/>')
        self.body.append('  <rect class="c1-fill" x="20" y="8" width="320" height="3" rx="1.5"/>')
        self.body.append('  <rect class="c3-fill" x="348" y="8" width="290" height="3" rx="1.5"/>')
        self.body.append('  <rect class="c4-fill" x="646" y="8" width="294" height="3" rx="1.5"/>')
        self.text(22, 33, heading, "title")
        self.text(22, 52, subtitle, "subtitle")

    def add(self, raw: str) -> None:
        self.body.append("  " + raw)

    def rect(self, x: float, y: float, w: float, h: float, cls: str, rx: float = 6, extra: str = "") -> None:
        ex = f" {extra}" if extra else ""
        self.add(f'<rect class="{cls}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}"{ex}/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, cls: str, extra: str = "") -> None:
        ex = f" {extra}" if extra else ""
        self.add(f'<line class="{cls}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"{ex}/>')

    def polyline(self, pts: list[tuple[float, float]], cls: str, extra: str = "") -> None:
        ex = f" {extra}" if extra else ""
        self.add(f'<polyline class="{cls}" points="{fmt_pts(pts)}"{ex}/>')

    def polygon(self, pts: list[tuple[float, float]], cls: str, extra: str = "") -> None:
        ex = f" {extra}" if extra else ""
        self.add(f'<polygon class="{cls}" points="{fmt_pts(pts)}"{ex}/>')

    def circle(self, cx: float, cy: float, r: float, cls: str, extra: str = "") -> None:
        ex = f" {extra}" if extra else ""
        self.add(f'<circle class="{cls}" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}"{ex}/>')

    def text(self, x: float, y: float, content: str, cls: str = "lbl", anchor: str = "start", extra: str = "") -> None:
        ta = f' text-anchor="{anchor}"' if anchor != "start" else ""
        ex = f" {extra}" if extra else ""
        self.add(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}"{ta}{ex}>{escape(content)}</text>')

    def panel(self, x: float, y: float, w: float, h: float, title: str) -> None:
        self.rect(x, y, w, h, "panel", rx=10)
        self.rect(x + 1, y + 1, w - 2, 28, "phead", rx=9)
        self.line(x + 1, y + 29, x + w - 1, y + 29, "grid")
        self.text(x + 12, y + 20, title, "sec")

    def render(self) -> str:
        self.text(22, H - 10, self.footer, "sm")
        lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
            f'  <title id="title">{escape(self.title)}</title>',
            f'  <desc id="desc">{escape(self.desc)}</desc>',
            "  <style>",
            COMMON_CSS.strip(),
            "  </style>",
            COMMON_DEFS,
            *self.body,
            "</svg>",
        ]
        xml_str = "\n".join(lines) + "\n"
        ET.fromstring(xml_str)
        return xml_str


# ---------------------------------------------------------------------------
# Figure 1 (Ch 11): v4-11-decoder-latency-budget.svg
# ---------------------------------------------------------------------------
def fig_11_decoder_latency_budget() -> str:
    doc = SvgDoc(
        title="容错实时解码单轮延迟预算与物理比特资源分解",
        desc=(
            "左面板以瀑布条分解超导表面码单轮 1.0 μs 延迟预算（物理读出 300 ns、信号传输 140 ns、"
            "症状匹配 340 ns 及 p99 重尾风险、条件前馈 120 ns，合计 0.90 μs < 1.0 μs），并区分单轮吞吐"
            "与端到端反应时间 τ_react；右面板按第 11 章精确数据对比三种表面码架构（Litinski 方案 A、"
            "面积压缩方案 B 与 Gidney 2025 轭联+培育）的数据、路由与魔法态物理比特占比。"
        ),
        heading="容错实时解码单轮延迟预算与物理比特资源分解",
        subtitle="左：超导表面码 τ_cyc ≈ 1.0 μs 吞吐预算瀑布与 p99 重尾风险；右：表面码数据、路由与魔法态工厂物理比特占比",
        footer="数据口径：第 11 章 §7.3、§8.2–§8.3（p = 10⁻³、τ_cyc = 1 μs、单瓦片 2d²；非等比例硬件流程示意与精确占比对照）。",
    )

    # Left panel: waterfall latency budget
    doc.panel(20, 64, 456, 370, "(a) 单轮 ~1 μs 解码延迟预算瀑布（吞吐 vs 重尾）")
    x0, x1 = 114.0, 456.0
    t_max = 1.15

    def tx(t: float) -> float:
        return x0 + (t / t_max) * (x1 - x0)

    # Vertical grid lines
    for tv in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        gx = tx(tv)
        doc.line(gx, 114, gx, 302, "grid")
        doc.line(gx, 302, gx, 307, "axis")
        doc.text(gx, 321, f"{tv:.1f}", "sm", "middle")
    doc.text(x1 + 2, 321, "μs", "sm", "end")

    # 1.0 us red deadline
    x_dead = tx(1.0)
    doc.line(x_dead, 112, x_dead, 302, "c2", 'stroke-width="2" stroke-dasharray="6 4"')
    doc.text(x_dead + 4, 108, "红线 τ_cyc = 1.0 μs", "smb c2-txt", "end")

    # Waterfall stages: (name, t_start, t_end, cls, note, note_mode)
    stages = [
        ("物理读出", 0.00, 0.30, "c3-soft", "300 ns（读出腔/解调）", "right"),
        ("信号传输", 0.30, 0.44, "c4-soft", "140 ns（温区/总线）", "right"),
        ("症状匹配", 0.44, 0.78, "c1-soft", "340 ns（均值）", "inside"),
        ("条件前馈", 0.78, 0.90, "c5-soft", "120 ns（逻辑帧/脉冲）", "left"),
    ]
    ys = [122, 158, 194, 230]
    bar_h = 22.0
    for idx, ((name, ts, te, cls, note, mode), y) in enumerate(zip(stages, ys)):
        sx, ex = tx(ts), tx(te)
        doc.text(x0 - 8, y + 15.5, name, "lblb", "end")
        doc.rect(sx, y, ex - sx, bar_h, cls, rx=4)
        if idx > 0:
            doc.line(sx, ys[idx - 1] + bar_h, sx, y, "guide")
        if mode == "right":
            doc.text(ex + 6, y + 15.5, note, "sm")
        elif mode == "inside":
            doc.text((sx + ex) / 2, y + 15.5, note, "smb c1-txt", "middle")
            # Heavy tail p99 extension beyond 1.0 us
            xtail = tx(1.09)
            doc.rect(ex, y, xtail - ex, bar_h, "c2-soft", rx=4, extra='stroke-dasharray="4 3"')
            doc.text((ex + xtail) / 2, y + 15.5, "p99 重尾", "smb c2-txt", "middle")
        elif mode == "left":
            doc.text(sx - 6, y + 15.5, note, "sm", "end")

    # Total single-cycle bar
    y_tot = 268.0
    doc.line(tx(0.90), ys[-1] + bar_h, tx(0.90), y_tot, "guide")
    doc.text(x0 - 8, y_tot + 15.5, "单轮合计", "lblb c1-txt", "end")
    doc.rect(tx(0.0), y_tot, tx(0.90) - tx(0.0), bar_h, "c1-fill", rx=4)
    doc.text((tx(0.0) + tx(0.90)) / 2, y_tot + 15.5, "0.90 μs < 1.0 μs（+100 ns 余量）", "badge-txt", "middle")
    doc.line(x0, 302, x1, 302, "axis")

    # Left bottom callout
    doc.rect(30, 334, 436, 90, "note", rx=7)
    doc.text(40, 353, "吞吐底线：均值 t̄_dec < τ_cyc ≈ 1 μs，否则触发 Terhal 指数积压", "smb")
    doc.text(40, 373, "端到端反应时间：τ_react = τ_readout + τ_comm + τ_dec,win + τ_fb", "sm")
    doc.text(40, 393, "实测参照：Willow 流式平均 63 μs（周期 1.1 μs）；目标 ≤ 10 μs", "sm")
    doc.text(40, 413, "尾延迟陷阱：均值达标不等于 p99/max 尾延迟不击穿 τ_react 预算", "sm c2-txt")

    # Right panel: surface-code physical qubit breakdown (exact Ch11 numbers)
    doc.panel(488, 64, 452, 370, "(b) 表面码物理比特占比分解（数据 + 路由 + 工厂）")

    # Legend row
    leg_y = 104
    leg_items = [
        (502, "c1-fill", "数据比特（含冷存）"),
        (644, "c3-fill", "晶格路由（含热存）"),
        (786, "c4-fill", "魔法态工厂/培育"),
    ]
    for lx, lcls, ltxt in leg_items:
        doc.rect(lx, leg_y, 12, 12, lcls, rx=2.5)
        doc.text(lx + 17, leg_y + 10.5, ltxt, "sm")

    # Exact architectures from Ch11 §8.3 and §8.2
    arch_rows = [
        (
            "方案 A（速度优先，d=23，20 座工厂，共 1.07M 比特）",
            200 * 2 * 23 * 23,       # 211,600 data
            241 * 2 * 23 * 23,       # 254,978 routing
            600_000,                 # 600,000 factories
        ),
        (
            "方案 B（面积压缩，d=25，4 座工厂，共 671k，时长 5×）",
            200 * 2 * 25 * 25,       # 250,000 data
            241 * 2 * 25 * 25,       # 301,250 routing
            120_000,                 # 120,000 factories
        ),
        (
            "Gidney 2025 RSA-2048（轭联存储 + 培育，共 898k 比特）",
            550_400,                 # cold yoked storage
            177_112,                 # hot storage + routing
            170_352,                 # compute + magic-state cultivation
        ),
    ]
    bx0, bw = 502.0, 424.0
    row_ys = [150, 212, 274]
    bh = 28.0
    for (label, q_data, q_route, q_fac), ry in zip(arch_rows, row_ys):
        tot = q_data + q_route + q_fac
        assert tot > 0
        f_d, f_r, f_f = q_data / tot, q_route / tot, q_fac / tot
        w_d, w_r, w_f = bw * f_d, bw * f_r, bw * f_f
        doc.text(bx0, ry - 7, label, "smb")
        # Stacked bars with hatch overlay for grayscale distinction
        doc.rect(bx0, ry, w_d, bh, "c1-fill", rx=3)
        doc.rect(bx0 + w_d, ry, w_r, bh, "c3-fill", rx=0)
        doc.rect(bx0 + w_d, ry, w_r, bh, "none", rx=0, extra='fill="url(#hatch-c3)"')
        doc.rect(bx0 + w_d + w_r, ry, w_f, bh, "c4-fill", rx=3)
        # Percentage labels inside segments
        doc.text(bx0 + w_d / 2, ry + 18, f"{f_d * 100:.1f}%", "badge-txt", "middle")
        doc.text(bx0 + w_d + w_r / 2, ry + 18, f"{f_r * 100:.1f}%", "badge-txt", "middle")
        fac_txt = f"{f_f * 100:.1f}% (600k)" if q_fac == 600_000 else f"{f_f * 100:.1f}%"
        doc.text(bx0 + w_d + w_r + w_f / 2, ry + 18, fac_txt, "badge-txt", "middle")

    # Percentage scale ticks under bars
    axis_y = 314.0
    doc.line(bx0, axis_y, bx0 + bw, axis_y, "axis")
    for frac in [0.0, 0.25, 0.50, 0.75, 1.0]:
        px = bx0 + bw * frac
        doc.line(px, axis_y, px, axis_y + 5, "axis")
        doc.text(px, axis_y + 18, f"{int(frac * 100)}%", "sm", "middle")

    # Right bottom callout
    doc.rect(500, 342, 428, 82, "subpanel", rx=7)
    doc.text(510, 361, "① 传统双级 15-to-1 蒸馏工厂可占活跃物理比特的 56%（方案 A）", "smb")
    doc.text(510, 381, "② 缩减工厂数会拉长运行时长 5×，迫使存储区码距 d: 23 → 25", "sm")
    doc.text(510, 401, "③ 魔法态培育 (MSC) + 轭联冷存把数据区占比提至 61.3%", "sm")
    doc.text(510, 417, "注：三组均对应理论均匀噪声估算，尚未计入芯片良率与关联突发错。", "sm")

    return doc.render()


# ---------------------------------------------------------------------------
# Figure 2 (Ch 13): v4-13-entropy-dpi-chain.svg
# ---------------------------------------------------------------------------
def fig_13_entropy_dpi_chain() -> str:
    doc = SvgDoc(
        title="数据处理不等式（DPI）总枢纽：熵族、强次可加性与信道容量主链",
        desc=(
            "左面板展示以夹心量子 Rényi 散度广义数据处理不等式（DPI）为总枢纽的逻辑主链："
            "由 α=1/2、α→1 与 α→∞ 三分支分别导出根保真度单调、Umegaki 相对熵 D(ρ‖σ) 与互信息 I(A:B)、"
            "强次可加性 SSA、Holevo 界 χ、量子 Pinsker 界及有限长最小熵，并向上衔接第 18 章四类信道容量。"
            "右面板以精确 Python 计算绘制单比特退极化信道 ε_p 下 Holevo χ(p)、最优 Helstrom 互信息 I(X:Y)、"
            "相对熵 D(ε_p(ρ)‖I/2) 与 Pinsker 下界随噪声 p ∈ [0,1] 的单调收缩曲线。"
        ),
        heading="数据处理不等式（DPI）总枢纽：熵族、SSA、Holevo 界与容量主链",
        subtitle="左：广义 DPI 连接 D(ρ‖σ) → I(A:B) → SSA → Holevo χ → 信道容量；右：退极化信道 ε_p 数值单调验证",
        footer="数值口径：第 13 章 §4.1–§5.1；右图系综 {|0⟩,|+⟩}（等先验）算 χ 与 I(X:Y)，对角态 ρ=diag(3/4,1/4) 与 σ=I/2 算 D 与 Pinsker（对数以 2 为底）。",
    )

    # Left panel: DPI logic DAG
    doc.panel(20, 64, 542, 370, "(a) 广义 DPI 总枢纽逻辑推导网（CPTP 信道 ε 单调链）")

    # Top Renyi entropy ordering strip
    doc.rect(32, 100, 518, 25, "pill", rx=6)
    doc.text(291, 117, "Rényi 熵族序：S₀ ≥ H_max(α=½) ≥ S(ρ)(α=1) ≥ S₂ ≥ H_min(α→∞)", "smb", "middle")

    # Central DPI Hub
    doc.rect(58, 134, 466, 43, "c1-soft", rx=8, extra='stroke-width="2"')
    doc.text(291, 152, "总枢纽：夹心 Rényi 散度广义数据处理不等式 (DPI)", "lblb c1-txt", "middle")
    doc.text(291, 169, "D_α(ρ ‖ σ) ≥ D_α(ε(ρ) ‖ ε(σ))   （夹心 Rényi 散度，任意 CPTP 信道 ε，α ∈ [½, ∞]）", "sm", "middle")

    # Three branch arrows from Hub to Row 2
    for bx, lbl_x, lbl_t, anc in [
        (104, 96, "α = ½", "end"),
        (291, 300, "α → 1", "start"),
        (478, 486, "α → ∞", "start"),
    ]:
        doc.line(bx, 177, bx, 198, "c1", 'stroke-width="1.6" marker-end="url(#arr-c1)"')
        doc.text(lbl_x, 192, lbl_t, "smb c1-txt", anc)

    # Row 2: three alpha branches
    doc.rect(32, 200, 144, 44, "c4-soft", rx=7)
    doc.text(104, 218, "根保真度单调", "smb c4-txt", "middle")
    doc.text(104, 236, "F(ε(ρ),ε(σ)) ≥ F", "sm", "middle")

    doc.rect(188, 200, 206, 44, "c3-soft", rx=7, extra='stroke-width="1.8"')
    doc.text(291, 218, "相对熵 D(ρ‖σ) 与互信息", "smb c3-txt", "middle")
    doc.text(291, 236, "I(A:B) = D(ρ_AB ‖ ρ_A⊗ρ_B)", "sm", "middle")

    doc.rect(406, 200, 144, 44, "c5-soft", rx=7)
    doc.text(478, 218, "最大相对熵 D_max", "smb c5-txt", "middle")
    doc.text(478, 236, "H_min 有限长 QKD", "sm", "middle")

    # Fan-out arrows from D(rho||sigma) / I(A:B) to SSA, Holevo, Pinsker
    doc.line(291, 244, 291, 255, "c3", 'stroke-width="1.6"')
    doc.line(114, 255, 468, 255, "c3", 'stroke-width="1.6"')
    for tx_b in [114, 291, 468]:
        doc.line(tx_b, 255, tx_b, 267, "c3", 'stroke-width="1.6" marker-end="url(#arr-c3)"')

    # Row 3: SSA, Holevo, Pinsker
    doc.rect(32, 269, 164, 46, "c1-soft", rx=7)
    doc.text(114, 287, "强次可加性 (SSA)", "smb c1-txt", "middle")
    doc.text(114, 305, "ε=Tr_C ⇒ I(A:BC)≥I(A:B)", "sm", "middle")

    doc.rect(208, 269, 166, 46, "c2-soft", rx=7)
    doc.text(291, 287, "Holevo 界 χ", "smb c2-txt", "middle")
    doc.text(291, 305, "测 cq 态 ⇒ I(X:Y) ≤ χ", "sm", "middle")

    doc.rect(386, 269, 164, 46, "c4-soft", rx=7)
    doc.text(468, 287, "量子 Pinsker 界", "smb c4-txt", "middle")
    doc.text(468, 305, "D(ρ‖σ) ≥ (2/ln2) T²", "sm", "middle")

    # Arrows into Chapter 18 Capacities box
    doc.line(114, 315, 114, 335, "c1", 'stroke-width="1.6" marker-end="url(#arr-c1)"')
    doc.line(291, 315, 291, 335, "c2", 'stroke-width="1.6" marker-end="url(#arr-c2)"')

    # Row 4: Channel capacity convergence box
    doc.rect(32, 337, 518, 86, "subpanel", rx=8)
    doc.text(291, 356, "向上衔接第 18 章：四类量子信道容量（均受 DPI 单调锁死）", "lblb c1-txt", "middle")
    doc.text(44, 377, "• 经典容量 C（HSW）：Holevo 信息 χ 的正则化渐近极限", "sm")
    doc.text(44, 396, "• 纠缠辅助容量 C_E（BSST）：SSA 直接保证 max I(R:B) 单字母可加", "sm")
    doc.text(44, 415, "• 量子容量 Q（LSD）与私密容量 P：串接前后处理均满足 Cap(D∘ε∘A) ≤ Cap(ε)", "sm")

    # Right panel: exact depolarizing curves
    doc.panel(574, 64, 366, 370, "(b) 退极化 ε_p 数值验证（DPI 单调衰减）")

    px0, px1 = 626.0, 922.0
    py0, py1 = 114.0, 292.0
    y_max = 0.68

    def sx(p: float) -> float:
        return px0 + p * (px1 - px0)

    def sy(val: float) -> float:
        return py1 - (val / y_max) * (py1 - py0)

    # Grid and ticks
    for pv in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        gx = sx(pv)
        doc.line(gx, py0, gx, py1, "grid")
        doc.line(gx, py1, gx, py1 + 4, "axis")
        doc.text(gx, py1 + 17, f"{pv:.1f}", "sm", "middle")
    for yv in [0.0, 0.2, 0.4, 0.6]:
        gy = sy(yv)
        doc.line(px0, gy, px1, gy, "grid")
        doc.line(px0 - 4, gy, px0, gy, "axis")
        doc.text(px0 - 8, gy + 4, f"{yv:.1f}", "sm", "end")
    doc.text(px0 - 4, py0 - 6, "bit", "sm", "end")
    doc.text((px0 + px1) / 2, py1 + 33, "退极化噪声参数 p", "smb", "middle")

    # Compute exact curves over p in [0, 1]
    n_pts = 80
    pts_chi: list[tuple[float, float]] = []
    pts_iacc: list[tuple[float, float]] = []
    pts_rel: list[tuple[float, float]] = []
    pts_pin: list[tuple[float, float]] = []
    inv_sqrt2 = 1.0 / math.sqrt(2.0)
    inv_ln2 = 1.0 / math.log(2.0)

    for k in range(n_pts + 1):
        p = k / n_pts
        lam_bar = 0.5 + 0.5 * (1.0 - p) * inv_sqrt2
        chi_v = h2(lam_bar) - h2(0.5 * p)
        iacc_v = 1.0 - h2(lam_bar)
        q_diag = 0.5 + 0.25 * (1.0 - p)
        rel_v = 1.0 - h2(q_diag)
        t_dist = 0.25 * (1.0 - p)
        pin_v = 2.0 * inv_ln2 * (t_dist ** 2)
        assert chi_v + 1e-12 >= iacc_v >= -1e-12
        assert rel_v + 1e-12 >= pin_v >= -1e-12
        pts_chi.append((sx(p), sy(chi_v)))
        pts_iacc.append((sx(p), sy(iacc_v)))
        pts_rel.append((sx(p), sy(rel_v)))
        pts_pin.append((sx(p), sy(pin_v)))

    # Draw axes & curves
    doc.line(px0, py0, px0, py1, "axis")
    doc.line(px0, py1, px1, py1, "axis")
    doc.polyline(pts_chi, "c1", 'stroke-width="2.3"')
    doc.polyline(pts_iacc, "c3", 'stroke-width="2.0" stroke-dasharray="6 3.5"')
    doc.polyline(pts_rel, "c2", 'stroke-width="2.1"')
    doc.polyline(pts_pin, "c4", 'stroke-width="1.9" stroke-dasharray="2.5 3"')

    # Key p=0 markers
    doc.circle(pts_chi[0][0], pts_chi[0][1], 3.5, "c1-fill")
    doc.circle(pts_iacc[0][0], pts_iacc[0][1], 3.5, "c3-fill")
    doc.circle(pts_rel[0][0], pts_rel[0][1], 3.5, "c2-fill")

    # Legend in empty upper-right quadrant (x=720..920, y=114..210)
    doc.rect(722, 114, 198, 94, "pill-bg", rx=6)
    leg_rows = [
        (132, "c1", "", "Holevo χ(p)  {|0⟩,|+⟩}"),
        (154, "c3", 'stroke-dasharray="6 3.5"', "Helstrom 互信息 I(X:Y)"),
        (176, "c2", "", "相对熵 D(ε_p(ρ) ‖ I/2)"),
        (198, "c4", 'stroke-dasharray="2.5 3"', "Pinsker 下界 (2/ln2)T²"),
    ]
    for ly, lcls, ldash, ltxt in leg_rows:
        doc.line(732, ly - 4, 756, ly - 4, lcls, f'stroke-width="2.2" {ldash}')
        doc.text(762, ly, ltxt, "sm")

    # Bottom numerical audit box
    chi0 = h2(0.5 + 0.5 * inv_sqrt2)
    i0 = 1.0 - chi0
    d0 = 1.0 - h2(0.75)
    pin0 = 2.0 * inv_ln2 * (0.25 ** 2)
    doc.rect(586, 338, 342, 85, "note", rx=7)
    doc.text(596, 357, "精确数值回验（单比特退极化 ε_p，单位 bit）：", "smb")
    doc.text(596, 376, f"p=0：χ = {chi0:.3f} ≥ I_opt = {i0:.3f}（Holevo 界严格成立）", "sm")
    doc.text(596, 395, f"p=0：D = {d0:.3f} ≥ Pinsker {pin0:.3f}（对角态紧密夹逼）", "sm")
    doc.text(596, 414, "p→1：四量均随噪声单调压降至 0，完整印证 DPI。", "sm c1-txt")

    return doc.render()


# ---------------------------------------------------------------------------
# Figure 3 (Ch 16): v4-16-walk-shadows.svg
# ---------------------------------------------------------------------------
def _compute_walk_distributions(steps: int = 30) -> tuple[list[int], list[float], list[float], float, float]:
    """Exact 1D classical random walk vs symmetric Hadamard quantum walk at t=steps."""
    # Classical binomial distribution on even sites x = -steps, -steps+2, ..., steps
    xs = list(range(-steps, steps + 1, 2))
    denom = float(1 << steps)
    p_cl = [math.comb(steps, (steps + x) // 2) / denom for x in xs]

    # Exact unitary 1D Hadamard walk: |x=0> (x) (|R> + i|L>)/sqrt(2)
    inv_s2 = 1.0 / math.sqrt(2.0)
    state: dict[int, tuple[complex, complex]] = {0: (complex(inv_s2, 0.0), complex(0.0, inv_s2))}
    for _ in range(steps):
        nxt: dict[int, tuple[complex, complex]] = {}
        for pos, (ar, al) in state.items():
            # Hadamard coin H = (1/sqrt(2)) [[1, 1], [1, -1]]
            cr = (ar + al) * inv_s2
            cl = (ar - al) * inv_s2
            # Conditional shift: R -> pos+1, L -> pos-1
            pr = nxt.get(pos + 1, (0j, 0j))
            nxt[pos + 1] = (pr[0] + cr, pr[1])
            pl = nxt.get(pos - 1, (0j, 0j))
            nxt[pos - 1] = (pl[0], pl[1] + cl)
        state = nxt

    p_q = []
    for x in xs:
        ar, al = state.get(x, (0j, 0j))
        p_q.append(abs(ar) ** 2 + abs(al) ** 2)

    assert abs(sum(p_cl) - 1.0) < 1e-12
    assert abs(sum(p_q) - 1.0) < 1e-12
    for i in range(len(xs)):
        assert abs(p_q[i] - p_q[-(i + 1)]) < 1e-12

    sig_cl = math.sqrt(sum((x ** 2) * p for x, p in zip(xs, p_cl)))
    sig_q = math.sqrt(sum((x ** 2) * p for x, p in zip(xs, p_q)))
    return xs, p_cl, p_q, sig_cl, sig_q


def fig_16_walk_shadows() -> str:
    steps = 30
    xs, p_cl, p_q, sig_cl, sig_q = _compute_walk_distributions(steps)

    doc = SvgDoc(
        title="一维量子行走双峰弹道扩散与经典影子随机测量流程",
        desc=(
            f"左面板实算 t={steps} 步一维经典随机游走高斯分布（σ_cl={sig_cl:.2f}=√t）与对称初态 "
            f"1D Hadamard 量子行走双峰弹道扩散（σ_Q={sig_q:.2f}∝t，双峰位于 ±t/√2 附近）；"
            "右面板展示随机单比特 Clifford 经典影子（Classical Shadows）四步流程："
            "随机单比特旋转、计算基快照采样、离线逆通道重构及中位数均值估计 M 个局域观测量。"
        ),
        heading="一维量子行走双峰弹道扩散与经典影子采样流程",
        subtitle=f"左：t = {steps} 步经典随机游走（σ = √t）vs Hadamard 量子行走（σ ∝ t）实算；右：单比特 Clifford 经典影子工作流",
        footer="数学验证：第 16 章 §4.3、§8.3；t=30 偶数格点实算 ∑P_cl = ∑P_Q = 1.0000，量子行走标准差相对经典放大近 3 倍。",
    )

    # Left panel: exact t=30 walk distribution
    doc.panel(20, 64, 466, 370, f"(a) 经典游走 vs 1D Hadamard 量子行走（t = {steps} 实算）")
    px0, px1 = 72.0, 468.0
    py0, py1 = 112.0, 316.0
    y_max = 0.185

    def sx(x: float) -> float:
        return px0 + ((x + steps) / (2 * steps)) * (px1 - px0)

    def sy(val: float) -> float:
        return py1 - (val / y_max) * (py1 - py0)

    # Grid & ticks
    for xv in [-30, -20, -10, 0, 10, 20, 30]:
        gx = sx(xv)
        doc.line(gx, py0, gx, py1, "grid")
        doc.line(gx, py1, gx, py1 + 4, "axis")
        doc.text(gx, py1 + 17, str(xv), "sm", "middle")
    for yv in [0.0, 0.04, 0.08, 0.12, 0.16]:
        gy = sy(yv)
        doc.line(px0, gy, px1, gy, "grid")
        doc.line(px0 - 4, gy, px0, gy, "axis")
        doc.text(px0 - 8, gy + 4, f"{yv:.2f}", "sm", "end")
    doc.text(px0 - 4, py0 - 6, "P(x)", "sm", "end")
    doc.text((px0 + px1) / 2, py1 + 35, f"位置格点 x（t = {steps} 步偶数格点包络）", "smb", "middle")

    # Polygons and polylines
    pts_cl = [(sx(x), sy(p)) for x, p in zip(xs, p_cl)]
    pts_q = [(sx(x), sy(p)) for x, p in zip(xs, p_q)]
    doc.polygon([(px0, py1), *pts_cl, (px1, py1)], "area2")
    doc.polygon([(px0, py1), *pts_q, (px1, py1)], "area1")

    doc.line(px0, py0, px0, py1, "axis")
    doc.line(px0, py1, px1, py1, "axis")
    doc.polyline(pts_cl, "c2", 'stroke-width="2.0" stroke-dasharray="6 3.5"')
    doc.polyline(pts_q, "c1", 'stroke-width="2.3"')

    # Locate exact peaks for clean callouts
    i_max_q = max(range(len(xs) // 2 + 1, len(xs)), key=lambda i: p_q[i])
    xq_r, pq_r = xs[i_max_q], p_q[i_max_q]
    xq_l = -xq_r
    p0_cl = p_cl[len(xs) // 2]

    doc.circle(sx(0), sy(p0_cl), 3.6, "c2-fill")
    doc.circle(sx(xq_l), sy(pq_r), 3.6, "c1-fill")
    doc.circle(sx(xq_r), sy(pq_r), 3.6, "c1-fill")

    # Non-overlapping peak annotations in clear upper strip (y=114..148)
    doc.text(76, 126, "量子双峰 ≈ ±t/√2", "smb c1-txt")
    doc.line(124, 132, sx(xq_l) - 2, sy(pq_r) - 5, "c1", 'stroke-width="1.3"')

    doc.text(sx(0), 141, f"经典 σ_cl = √t ≈ {sig_cl:.2f}", "smb c2-txt", "middle")
    doc.line(sx(0), 145, sx(0), sy(p0_cl) - 5, "c2", 'stroke-width="1.3"')

    doc.text(464, 126, f"弹道 σ_Q ≈ {sig_q:.2f} ∝ t", "smb c1-txt", "end")
    doc.line(416, 132, sx(xq_r) + 2, sy(pq_r) - 5, "c1", 'stroke-width="1.3"')

    # Left bottom summary card
    doc.rect(32, 366, 442, 58, "subpanel", rx=7)
    doc.text(42, 386, "初态 |x=0⟩⊗(|R⟩+i|L⟩)/√2，每步 W = S(I⊗H) 严格保持酉演化", "sm")
    doc.text(42, 408, f"实算对比：σ_Q / σ_cl = {sig_q / sig_cl:.2f}×，相干干涉把扩散从 √t 推至弹道 t", "smb c1-txt")

    # Right panel: classical shadows workflow
    doc.panel(498, 64, 442, 370, "(b) 随机单比特 Clifford 经典影子采样与估计流程")

    stages = [
        (
            102, 50, "c3-soft", "c3-fill", "c3-txt", "1",
            "随机单比特 Clifford 旋转（硬件层）",
            "对 n 比特未知态 ρ 逐比特独立抽 U_j ∈ {I, H, HS†}（Z/X/Y 基）",
        ),
        (
            168, 48, "c1-soft", "c1-fill", "c1-txt", "2",
            "计算基单次投影快照（重复 N 轮）",
            "测得比特串 b̂^(m) ∈ {0,1}ⁿ，经典存储 {(U^(m), b̂^(m))}_{m=1}^N",
        ),
        (
            232, 54, "c4-soft", "c4-fill", "c4-txt", "3",
            "离线逆通道重构经典影子（经典层）",
            "ρ̂^(m) = ⊗_j (3 U_j† |b̂_j⟩⟨b̂_j| U_j − I)，无偏满足 E[ρ̂] = ρ",
        ),
        (
            302, 54, "c5-soft", "c5-fill", "c5-txt", "4",
            "中位数均值估计 M 个局域观测量 {O_i}",
            "ô_i = median_k Tr(O_i ρ̂̄_k) ｜ N = O(log(M/δ) · 3^w / ε²)",
        ),
    ]
    for idx, (sy_top, sh, box_cls, bdg_cls, txt_cls, num, head, desc_line) in enumerate(stages):
        doc.rect(510, sy_top, 418, sh, box_cls, rx=7)
        doc.rect(519, sy_top + (sh - 24) / 2, 24, 24, bdg_cls, rx=5)
        doc.text(531, sy_top + sh / 2 + 4.5, num, "badge-txt", "middle")
        doc.text(552, sy_top + 20, head, f"smb {txt_cls}")
        doc.text(552, sy_top + sh - 11, desc_line, "sm")
        if idx < len(stages) - 1:
            nxt_top = stages[idx + 1][0]
            doc.line(719, sy_top + sh, 719, nxt_top - 2, "axis", 'stroke-width="1.5" marker-end="url(#arr-ink)"')

    # Bottom trade-off note
    doc.rect(510, 368, 418, 56, "note", rx=7)
    doc.text(520, 388, "核心优势：先采样、后提问，样本数仅按 log M 缓慢增长", "smb")
    doc.text(520, 409, "适用边界：单比特随机 Pauli 影子方差按 3^w 增长（限于低权重 w）", "sm")

    return doc.render()


# ---------------------------------------------------------------------------
# Figure 4 (Ch 18): v4-18-capacity-complexity-ladder.svg
# ---------------------------------------------------------------------------
def fig_18_capacity_complexity_ladder() -> str:
    doc = SvgDoc(
        title="量子信道容量阶梯与核心计算复杂度类包含谱系",
        desc=(
            "左面板以精确解析公式绘出单比特擦除信道四类容量阶梯 Q = P = max(0,1−2ε) ≤ C = 1−ε ≤ C_E = 2(1−ε)、"
            "单比特退相位量子容量 Q_deph(p) = 1 − h₂(p) 与纯损耗玻色信道 PLOB 双向上界 −log₂(ε)（η = 1 − ε），"
            "并标出 ε = 1/2 处可降解/反降解相变点；右面板以嵌套层级展示 P ⊆ BPP ⊆ BQP ⊆ QCMA ⊆ QMA ⊆ QIP = PSPACE ⊆ MIP* = RE。"
        ),
        heading="量子信道容量阶梯与核心计算复杂度类谱系",
        subtitle="左：擦除/退相位容量阶梯 Q ≤ P ≤ C ≤ C_E 与纯损耗 PLOB 上界实算；右：P ⊆ BPP ⊆ BQP ⊆ QMA ⊆ PSPACE ⊆ MIP* = RE",
        footer="数学口径：第 18 章 §5.1–§5.2 与 §7；对数以 2 为底，纯损耗玻色信道透射率 η = 1 − ε，PLOB 上界 −log₂(1−η) 为无中继光纤双向量子容量极限。",
    )

    # Left panel: capacity ladder & PLOB bound
    doc.panel(20, 64, 464, 370, "(a) 信道容量阶梯（擦除/退相位）与 PLOB 上界")

    px0, px1 = 70.0, 466.0
    py0, py1 = 112.0, 306.0
    y_max = 2.20

    def sx(eps: float) -> float:
        return px0 + eps * (px1 - px0)

    def sy(cap: float) -> float:
        return py1 - (cap / y_max) * (py1 - py0)

    # Grid & ticks
    for ev in [0.0, 0.25, 0.50, 0.75, 1.0]:
        gx = sx(ev)
        doc.line(gx, py0, gx, py1, "grid")
        doc.line(gx, py1, gx, py1 + 4, "axis")
        doc.text(gx, py1 + 17, f"{ev:.2f}".rstrip("0").rstrip(".") if ev in (0.0, 1.0) else f"{ev:.2f}", "sm", "middle")
    for yv in [0.0, 0.5, 1.0, 1.5, 2.0]:
        gy = sy(yv)
        doc.line(px0, gy, px1, gy, "grid")
        doc.line(px0 - 4, gy, px0, gy, "axis")
        doc.text(px0 - 8, gy + 4, f"{yv:.1f}", "sm", "end")
    doc.text(px0 - 4, py0 - 6, "bit/use", "sm", "end")
    doc.text((px0 + px1) / 2, py1 + 35, "擦除/损耗率 ε（透射率 η = 1 − ε；退相位 p = ε）", "smb", "middle")

    # Degradable / antidegradable divider at eps = 0.5
    x_half = sx(0.5)
    doc.line(x_half, py0, x_half, py1, "guide")
    doc.text(x_half - 6, py0 + 13, "可降解 ε ≤ ½", "sm c1-txt", "end")

    # Compute exact curves
    n_pts = 100
    pts_ce = [(sx(i / n_pts), sy(2.0 * (1.0 - i / n_pts))) for i in range(n_pts + 1)]
    pts_c = [(sx(i / n_pts), sy(1.0 - i / n_pts)) for i in range(n_pts + 1)]
    pts_q = [(sx(i / n_pts), sy(max(0.0, 1.0 - 2.0 * (i / n_pts)))) for i in range(n_pts + 1)]

    # Dephasing quantum capacity Q_deph(p) = 1 - h2(p) on p in [0, 0.5]
    pts_deph = [(sx(0.5 * i / 60), sy(1.0 - h2(0.5 * i / 60))) for i in range(61)]

    # PLOB bound: -log2(eps) clipped at y_max = 2.20 => eps_min = 2^(-2.2)
    eps_min = 2.0 ** (-y_max)
    pts_plob = []
    for i in range(81):
        ev = eps_min + (1.0 - eps_min) * (i / 80.0)
        cap_plob = -math.log2(ev)
        pts_plob.append((sx(ev), sy(cap_plob)))

    # Assert key textbook checks at eps = 0.25
    assert abs(2.0 * (1.0 - 0.25) - 1.50) < 1e-12
    assert abs((1.0 - 0.25) - 0.75) < 1e-12
    assert abs((1.0 - 2.0 * 0.25) - 0.50) < 1e-12
    assert abs(-math.log2(0.25) - 2.00) < 1e-12

    # Axes & polylines
    doc.line(px0, py0, px0, py1, "axis")
    doc.line(px0, py1, px1, py1, "axis")
    doc.polyline(pts_ce, "c5", 'stroke-width="2.1"')
    doc.polyline(pts_plob, "c2", 'stroke-width="2.1" stroke-dasharray="6 3.5"')
    doc.polyline(pts_c, "c3", 'stroke-width="2.1"')
    doc.polyline(pts_q, "c1", 'stroke-width="2.4"')
    doc.polyline(pts_deph, "c4", 'stroke-width="2.0" stroke-dasharray="5 2.5 1.5 2.5"')

    # Reference dots at eps = 0.25 and eps = 0.50
    for val, fcls in [(1.50, "c5-fill"), (0.75, "c3-fill"), (0.50, "c1-fill"), (1.0 - h2(0.25), "c4-fill")]:
        doc.circle(sx(0.25), sy(val), 3.2, fcls)
    doc.circle(sx(0.50), sy(0.0), 3.6, "c1-fill")
    doc.circle(sx(0.50), sy(1.0), 3.4, "c2-fill")

    # Legend in empty upper-right quadrant (x=274..464, y=113..217)
    doc.rect(274, 113, 190, 104, "pill-bg", rx=6)
    leg_entries = [
        (130, "c2", 'stroke-dasharray="6 3.5"', "PLOB −log₂(ε)（纯损耗）"),
        (149, "c5", "", "C_E = 2(1−ε)（纠缠辅助）"),
        (168, "c3", "", "C = 1−ε（擦除经典）"),
        (187, "c1", "", "Q = P = (1−2ε)₊（擦除）"),
        (206, "c4", 'stroke-dasharray="5 2.5 1.5 2.5"', "Q_deph = 1−h₂(p)（退相位）"),
    ]
    for ly, lcls, ldash, ltxt in leg_entries:
        doc.line(282, ly - 4, 304, ly - 4, lcls, f'stroke-width="2.1" {ldash}')
        doc.text(310, ly, ltxt, "sm")

    # Left bottom summary box
    doc.rect(32, 355, 440, 69, "note", rx=7)
    doc.text(42, 374, "ε = ¼ 擦除阶梯：Q = P = 0.50 ≤ C = 0.75 ≤ C_E = 1.50 bit/use", "smb")
    doc.text(42, 394, "ε = ½ 相变点：右区反降解使 Q = P = 0，但预共享纠缠 C_E > 0 仍非零", "sm")
    doc.text(42, 414, "PLOB 上界 −log₂(1−η) 约束无量子中继的纯损耗光纤双向量子容量", "sm c2-txt")

    # Right panel: nested complexity class inclusion ladder
    doc.panel(496, 64, 444, 370, "(b) 量子与交互验证复杂度类包含层级")

    tiers = [
        (508, 102, 420, 270, "c2-soft", "c2-txt", "MIP* = RE", "纠缠多证明者交互验证（含停机问题）"),
        (518, 132, 400, 234, "c5-soft", "c5-txt", "QIP = IP = PSPACE", "多项式空间 / 3 轮量子交互"),
        (528, 162, 380, 198, "c4-soft", "c4-txt", "QMA", "量子见证态 + BQP（k-局域哈密顿量）"),
        (538, 192, 360, 162, "c3-soft", "c3-txt", "QCMA", "经典见证串 + BQP 验证（含 NP）"),
        (548, 222, 340, 126, "c1-soft", "c1-txt", "BQP", "量子多项式时间（Shor · QSVT · 模拟）"),
        (564, 258, 308, 82, "pill-bg", "lblb", "BPP", "经典随机多项式时间"),
        (584, 294, 268, 38, "subpanel", "lblb", "P", "经典确定性多项式时间"),
    ]
    for rx, ry, rw, rh, box_cls, txt_cls, cname, cdesc in tiers:
        doc.rect(rx, ry, rw, rh, box_cls, rx=8)
        y_txt = ry + 21 if rh > 42 else ry + 23
        c_lbl_cls = f"lblb {txt_cls}" if txt_cls != "lblb" else "lblb"
        doc.text(rx + 12, y_txt, cname, c_lbl_cls)
        doc.text(rx + rw - 10, y_txt, cdesc, "sm", "end")

    # Right bottom note on open questions & sampling
    doc.rect(508, 380, 420, 44, "subpanel", rx=7)
    doc.text(518, 398, "已证 P ⊆ NP ⊆ QCMA ⊆ QMA；BQP 与 NP 相互包含关系仍未决", "smb")
    doc.text(518, 416, "量子采样优势（RCS / IQP / BosonSampling）依赖 PH 不坍塌假设", "sm")

    return doc.render()


# ---------------------------------------------------------------------------
# Figure 5 (Ch 20): v4-20-sensing-ramsey-qfi.svg
# ---------------------------------------------------------------------------
def fig_20_sensing_ramsey_qfi() -> str:
    doc = SvgDoc(
        title="Ramsey 相位干涉、量子费舍尔信息标度与原子钟/重力仪机制",
        desc=(
            "左面板展示 Ramsey π/2–τ–π/2 脉冲时序及精确计算的含噪条纹 P_+(φ; V=0.85) 与经典 Fisher 信息 "
            "F_C(φ; V) = V²sin²φ/(1−V²cos²φ)，标出最大斜率灵敏点 φ=π/2（达到 F_Q=V²）与盲点 φ=0, π；"
            "右面板以双对数坐标对比标准量子极限 SQL (1/√N)、单轴扭转自旋压缩 OAT (N⁻⁵/⁶) 与海森堡极限 HL (1/N)，"
            "并拆解 ⁸⁷Sr 光晶格原子钟阿兰偏差与 ⁸⁷Rb 冷原子重力仪 Δφ = −k_eff g T² 灵敏度机制。"
        ),
        heading="Ramsey 干涉条纹、QFI 精度标度与原子钟 / 重力仪机制",
        subtitle="左：Ramsey π/2–τ–π/2 脉冲时序与条纹斜率 / Fisher 信息；右：SQL vs 海森堡标度与原子钟阿兰偏差 / 重力仪机理",
        footer="公式与算例口径：第 20 章 §2.3、§3.3、§6.1 与 §8.1（V=0.85 时 F_Q=V²=0.7225；⁸⁷Sr 钟 4.06×10⁻¹⁸；⁸⁷Rb T=0.1 s 得 1.58×10⁶ rad）。",
    )

    # Left panel: Ramsey sequence + fringe & CFI/QFI plot
    doc.panel(20, 64, 456, 370, "(a) Ramsey π/2–τ–π/2 脉冲时序与条纹斜率 / F_C")

    # Top pulse sequence schematic
    doc.rect(32, 99, 432, 54, "subpanel", rx=7)
    doc.text(44, 130, "|0⟩", "lblb")
    doc.line(63, 126, 77, 126, "axis", 'stroke-width="1.5" marker-end="url(#arr-ink)"')
    doc.rect(80, 110, 48, 30, "c1-soft", rx=5)
    doc.text(104, 129, "π/2", "lblb c1-txt", "middle")

    doc.line(128, 126, 294, 126, "c3", 'stroke-width="1.7" stroke-dasharray="4 3"')
    doc.text(211, 117, "自由演化 τ（积累 φ = Δω·τ）", "smb c3-txt", "middle")
    doc.text(211, 145, "(|0⟩ + e^(iφ)|1⟩) / √2", "sm", "middle")

    doc.rect(296, 110, 48, 30, "c1-soft", rx=5)
    doc.text(320, 129, "π/2", "lblb c1-txt", "middle")
    doc.line(344, 126, 360, 126, "axis", 'stroke-width="1.5" marker-end="url(#arr-ink)"')
    doc.rect(363, 110, 90, 30, "c3-soft", rx=5)
    doc.text(408, 129, "Z 读出 P₊(φ)", "smb c3-txt", "middle")

    # Horizontal legend row cleanly above plot
    doc.line(36, 168, 56, 168, "c3", 'stroke-width="2.2"')
    doc.text(61, 172, "P₊(φ; V=0.85)", "sm c3-txt")
    doc.line(166, 168, 186, 168, "c2", 'stroke-width="2.2"')
    doc.text(191, 172, "经典 Fisher F_C(φ)", "sm c2-txt")
    doc.line(316, 168, 336, 168, "c4", 'stroke-width="1.8" stroke-dasharray="4 3"')
    doc.text(341, 172, "QFI 上界 V²=0.723", "sm c4-txt")

    # Exact Ramsey fringe & CFI plot
    px0, px1 = 72.0, 458.0
    py0, py1 = 184.0, 340.0
    y_max = 1.08
    vis = 0.85
    v2 = vis * vis

    def sx(phi: float) -> float:
        return px0 + (phi / (2.0 * math.pi)) * (px1 - px0)

    def sy(val: float) -> float:
        return py1 - (val / y_max) * (py1 - py0)

    for mult, lbl in [(0.0, "0"), (0.5, "π/2"), (1.0, "π"), (1.5, "3π/2"), (2.0, "2π")]:
        gx = sx(mult * math.pi)
        doc.line(gx, py0, gx, py1, "grid")
        doc.line(gx, py1, gx, py1 + 4, "axis")
        doc.text(gx, py1 + 17, lbl, "sm", "middle")
    for yv in [0.0, 0.5, 1.0]:
        gy = sy(yv)
        doc.line(px0, gy, px1, gy, "grid")
        doc.line(px0 - 4, gy, px0, gy, "axis")
        doc.text(px0 - 8, gy + 4, f"{yv:.1f}", "sm", "end")
    doc.text((px0 + px1) / 2, py1 + 33, "相对相位 φ (rad)", "smb", "middle")

    # Exact curves
    n_pts = 120
    pts_p_ideal: list[tuple[float, float]] = []
    pts_p_vis: list[tuple[float, float]] = []
    pts_fc: list[tuple[float, float]] = []
    for i in range(n_pts + 1):
        phi = 2.0 * math.pi * i / n_pts
        c = math.cos(phi)
        s = math.sin(phi)
        p_id = 0.5 * (1.0 + c)
        p_v = 0.5 * (1.0 + vis * c)
        fc = (v2 * s * s) / (1.0 - v2 * c * c)
        assert fc <= v2 + 1e-12
        pts_p_ideal.append((sx(phi), sy(p_id)))
        pts_p_vis.append((sx(phi), sy(p_v)))
        pts_fc.append((sx(phi), sy(fc)))

    # QFI ceiling line at F_Q = V^2
    doc.line(px0, sy(v2), px1, sy(v2), "c4", 'stroke-width="1.6" stroke-dasharray="4 3"')
    doc.line(px0, py0, px0, py1, "axis")
    doc.line(px0, py1, px1, py1, "axis")
    doc.polyline(pts_p_ideal, "guide", 'stroke-width="1.2"')
    doc.polyline(pts_p_vis, "c3", 'stroke-width="2.2"')
    doc.polyline(pts_fc, "c2", 'stroke-width="2.3"')

    # Tangent slope segment at phi = pi/2 on P_+(phi; V)
    phi_opt = 0.5 * math.pi
    dphi = 0.52
    doc.line(
        sx(phi_opt - dphi), sy(0.5 + 0.5 * vis * dphi),
        sx(phi_opt + dphi), sy(0.5 - 0.5 * vis * dphi),
        "c1", 'stroke-width="2.0"',
    )
    doc.circle(sx(phi_opt), sy(0.5), 3.6, "c3-fill")
    doc.circle(sx(phi_opt), sy(v2), 3.8, "c2-fill")
    doc.circle(sx(math.pi), sy(0.0), 3.6, "c2-fill")

    # Clean annotations inside plot
    doc.text(248, 200, "灵敏点 φ=π/2（最大斜率，F_C=F_Q）", "smb c2-txt", "middle")
    doc.line(184, 206, sx(phi_opt) + 3, sy(v2) - 5, "c2", 'stroke-width="1.2"')

    doc.text(sx(math.pi), 298, "盲点 φ=π (F_C=0)", "smb c2-txt", "middle")
    doc.line(sx(math.pi), 303, sx(math.pi), sy(0.0) - 5, "c2", 'stroke-width="1.2"')

    # Left bottom summary strip
    doc.rect(32, 384, 432, 40, "note", rx=7)
    doc.text(42, 401, "F_C(φ;V) = V²sin²φ / (1−V²cos²φ)，在 φ = π/2 榨干全部 QFI = V²", "smb")
    doc.text(42, 418, "注：虚灰线为理想 V=1 条纹；φ = 0, π 处一阶斜率为 0，对微相移失明。", "sm")

    # Right panel: SQL vs HL scaling + Atomic clock & Cold-atom gravimeter
    doc.panel(488, 64, 452, 370, "(b) QFI 精度标度（SQL vs HL）与原子钟 / 重力仪机制")

    # Top log-log scaling plot (N = 1 .. 10^4, dphi = 10^-4.2 .. 10^0.2)
    rx0, rx1 = 550.0, 922.0
    ry0, ry1 = 106.0, 256.0
    log_n_min, log_n_max = 0.0, 4.0
    log_y_min, log_y_max = -4.2, 0.2

    def rx(log_n: float) -> float:
        return rx0 + ((log_n - log_n_min) / (log_n_max - log_n_min)) * (rx1 - rx0)

    def ry(log_y: float) -> float:
        return ry1 - ((log_y - log_y_min) / (log_y_max - log_y_min)) * (ry1 - ry0)

    # Grid & log ticks
    for k, lbl in [(0, "1"), (1, "10"), (2, "10²"), (3, "10³"), (4, "10⁴")]:
        gx = rx(float(k))
        doc.line(gx, ry0, gx, ry1, "grid")
        doc.line(gx, ry1, gx, ry1 + 4, "axis")
        doc.text(gx, ry1 + 17, lbl, "sm", "middle")
    for k, lbl in [(0, "10⁰"), (-1, "10⁻¹"), (-2, "10⁻²"), (-3, "10⁻³"), (-4, "10⁻⁴")]:
        gy = ry(float(k))
        doc.line(rx0, gy, rx1, gy, "grid")
        doc.line(rx0 - 4, gy, rx0, gy, "axis")
        doc.text(rx0 - 8, gy + 4, lbl, "sm", "end")
    doc.text(rx0 - 6, ry0 - 3, "Δφ (rad)", "sm", "end")
    doc.text((rx0 + rx1) / 2, ry1 + 32, "探针数 N（双对数坐标）", "smb", "middle")

    # Forbidden QCRB zone below HL (Delta phi < 1/N)
    hl_pts = [(rx(0.0), ry(0.0)), (rx(4.0), ry(-4.0))]
    doc.polygon([(rx(0.0), ry(0.0)), (rx(4.0), ry(-4.0)), (rx(4.0), ry1), (rx0, ry1)], "area2")

    # Scaling curves
    sql_pts = [(rx(0.0), ry(0.0)), (rx(4.0), ry(-2.0))]
    oat_pts = [(rx(0.0), ry(0.0)), (rx(4.0), ry(-4.0 * 5.0 / 6.0))]
    doc.line(rx0, ry0, rx0, ry1, "axis")
    doc.line(rx0, ry1, rx1, ry1, "axis")
    doc.polyline(sql_pts, "c3", 'stroke-width="2.2" stroke-dasharray="6 3.5"')
    doc.polyline(oat_pts, "c4", 'stroke-width="2.0" stroke-dasharray="5 2.5 1.5 2.5"')
    doc.polyline(hl_pts, "c1", 'stroke-width="2.4"')

    # Clean non-overlapping labels
    doc.text(918, 156, "SQL（独立探针）：1/√N", "smb c3-txt", "end")
    doc.text(918, 198, "自旋压缩 OAT：N⁻⁵/⁶", "smb c4-txt", "end")
    doc.text(704, 218, "海森堡极限 HL：1/N", "smb c1-txt", "end")
    doc.line(707, 213, rx(2.35) - 3, ry(-2.35) + 3, "c1", 'stroke-width="1.3"')
    doc.text(558, 246, "QCRB 禁区 (< 1/N)", "sm c2-txt")

    # Bottom dual mechanism cards: Optical Lattice Clock vs Cold-Atom Gravimeter
    doc.rect(500, 298, 210, 126, "c1-soft", rx=8)
    doc.text(510, 317, "⁸⁷Sr 光晶格原子钟", "lblb c1-txt")
    doc.text(510, 337, "阿兰偏差（QPN 极限）：", "smb")
    doc.text(510, 356, "σ_y = ξ_R / (ω₀√(N T_R τ))", "mono")
    doc.text(510, 377, "• 白频噪斜率 ∝ τ⁻¹/²", "sm")
    doc.text(510, 396, "• 死时间引起 Dick 混叠", "sm")
    doc.text(510, 415, "• N=10⁴, 1s ⇒ 4.1×10⁻¹⁸", "sm c1-txt")

    doc.rect(720, 298, 208, 126, "c4-soft", rx=8)
    doc.text(730, 317, "⁸⁷Rb 冷原子重力仪", "lblb c4-txt")
    doc.text(730, 337, "Mach–Zehnder 拉曼序列：", "smb")
    doc.text(730, 356, "π/2 — T — π — T — π/2", "mono")
    doc.text(730, 377, "• 净相位 Δφ = −k_eff·g·T²", "sm")
    doc.text(730, 396, "• 二阶差分抵消初位与初速", "sm")
    doc.text(730, 415, "• T=0.1s ⇒ 1.58×10⁶ rad", "sm c4-txt")

    return doc.render()


# ---------------------------------------------------------------------------
# Figure 6 (Ch 21): v4-21-sim-engines-architecture.svg
# ---------------------------------------------------------------------------
def fig_21_sim_engines_architecture() -> str:
    doc = SvgDoc(
        title="三大经典量子模拟引擎：数据结构、压缩机理与失效边界",
        desc=(
            "三列并排对比现代经典量子模拟的三大支柱引擎及其精确标度边界："
            "（1）稳定子表（CHP/Stim）：2n×(2n+1) 二元辛表，纯 Clifford 空间 O(n²)，"
            "非 Clifford T 门触发 2^(0.396t) 精确秩与 2^(0.228t) 近似展度指数壁垒；"
            "（2）MPS/2D PEPS 张量网络：1D 链 O(nχ²) 受面积律保护，深层 2D 体积律 χ~2^S 与环路树宽触发指数壁垒；"
            "（3）含噪海森堡 Pauli 传播（SPD）：借高权重截断与 (1−p)^w 噪声指数阻尼实现百比特 NISQ 模拟，低噪声深层大角门失效。"
        ),
        heading="三大经典量子模拟引擎：数据结构、压缩机理与能力边界",
        subtitle="对照稳定子表（T 门魔术度壁垒）、MPS/2D PEPS（纠缠键维与树宽壁垒）及含噪 Pauli 传播（权重截断与指数阻尼）",
        footer="标度与数据口径：第 21 章 §1–§6；稳定子秩指数 α=0.396（Qassim–Pashayan–Gosset 2021）与展度 0.228（Bravyi–Gosset 2016）；Pauli 阻尼 (1−p)^w。",
    )

    # ===== Column 1: Stabilizer Tableau =====
    doc.panel(20, 64, 298, 370, "1. 稳定子表（CHP / Stim）")
    doc.rect(32, 100, 274, 100, "subpanel", rx=7)
    doc.text(169, 116, "2n × (2n+1) 二元辛表（空间 O(n²)）", "smb", "middle")
    # Tableau matrix blocks
    doc.rect(44, 124, 98, 26, "c3-soft", rx=4)
    doc.text(93, 141, "去稳定子 X", "sm c3-txt", "middle")
    doc.rect(144, 124, 98, 26, "c3-soft", rx=4)
    doc.text(193, 141, "去稳定子 Z", "sm c3-txt", "middle")
    doc.rect(244, 124, 48, 26, "pill", rx=4)
    doc.text(268, 141, "相位 r", "sm", "middle")

    doc.rect(44, 152, 98, 26, "c1-soft", rx=4)
    doc.text(93, 169, "稳定子 X", "sm c1-txt", "middle")
    doc.rect(144, 152, 98, 26, "c1-soft", rx=4)
    doc.text(193, 169, "稳定子 Z", "sm c1-txt", "middle")
    doc.rect(244, 152, 48, 26, "pill", rx=4)
    doc.text(268, 169, "相位 r", "sm", "middle")
    doc.text(169, 194, "Clifford 门 {H,S,CNOT} 更新仅 O(n)", "sm", "middle")

    # Col 1 exact T-gate exponential wall plot (t = 0..60, log10 cost = 0..7.5)
    c1x0, c1x1 = 68.0, 304.0
    cy0, cy1 = 222.0, 316.0
    log_c_max = 7.5

    def s1x(t: float) -> float:
        return c1x0 + (t / 60.0) * (c1x1 - c1x0)

    def s1y(lg: float) -> float:
        return cy1 - (lg / log_c_max) * (cy1 - cy0)

    for tv in [0, 20, 40, 60]:
        gx = s1x(tv)
        doc.line(gx, cy0, gx, cy1, "grid")
        doc.line(gx, cy1, gx, cy1 + 4, "axis")
        doc.text(gx, cy1 + 16, str(tv), "sm", "middle")
    for lg, lbl in [(0.0, "10⁰"), (3.0, "10³"), (6.0, "10⁶")]:
        gy = s1y(lg)
        doc.line(c1x0, gy, c1x1, gy, "grid")
        doc.line(c1x0 - 4, gy, c1x0, gy, "axis")
        doc.text(c1x0 - 7, gy + 4, lbl, "sm", "end")
    doc.text(186, 345, "非 Clifford T 门数 t（对数开销）", "smb", "middle")

    pts_exact = [(s1x(t), s1y(0.3963 * t * math.log10(2.0))) for t in range(0, 61, 2)]
    pts_ext = [(s1x(t), s1y(0.228 * t * math.log10(2.0))) for t in range(0, 61, 2)]
    doc.line(c1x0, s1y(6.0), c1x1, s1y(6.0), "guide")
    doc.line(c1x0, cy0, c1x0, cy1, "axis")
    doc.line(c1x0, cy1, c1x1, cy1, "axis")
    doc.polyline(pts_exact, "c2", 'stroke-width="2.2"')
    doc.polyline(pts_ext, "c1", 'stroke-width="2.0" stroke-dasharray="5 3"')
    doc.text(74, 234, "— 精确秩 2^(0.396t)", "sm c2-txt")
    doc.text(74, 252, "-- 展度采样 2^(0.228t)", "sm c1-txt")

    doc.rect(32, 354, 274, 70, "c1-soft", rx=7)
    doc.text(42, 373, "优势：支持体积律纠缠与百万比特 QEC", "smb c1-txt")
    doc.text(42, 393, "壁垒：非 Clifford T 门数 t 指数爆发", "sm")
    doc.text(42, 413, "工具：Stim · 扩展稳定子 O(2^αt·poly)", "sm")

    # ===== Column 2: MPS / 2D PEPS Tensor Networks =====
    doc.panel(331, 64, 298, 370, "2. MPS / 2D PEPS 张量网络")
    doc.rect(343, 100, 274, 100, "subpanel", rx=7)

    # 1D MPS chain (left sub-schematic)
    doc.text(416, 116, "1D MPS 链（键维 χ）", "smb c3-txt", "middle")
    mps_xs = [362, 398, 434, 470]
    doc.line(mps_xs[0], 146, mps_xs[-1], 146, "c3", 'stroke-width="2.8"')
    for mx in mps_xs:
        doc.line(mx, 146, mx, 174, "axis", 'stroke-width="1.4"')
        doc.circle(mx, 146, 10, "c3-soft")
    doc.text(416, 193, "空间 O(nχ²) · 门 O(χ³)", "sm", "middle")

    # 2D PEPS grid (right sub-schematic)
    doc.text(556, 116, "2D PEPS 格点", "smb c2-txt", "middle")
    pxs = [526, 556, 586]
    pys = [132, 152, 172]
    for gy in pys:
        doc.line(pxs[0], gy, pxs[-1], gy, "c2", 'stroke-width="1.5"')
    for gx in pxs:
        doc.line(gx, pys[0], gx, pys[-1], "c2", 'stroke-width="1.5"')
    doc.rect(526, 132, 30, 20, "c2", rx=2, extra='stroke-width="2.2" stroke-dasharray="3 2"')
    for gx in pxs:
        for gy in pys:
            doc.circle(gx, gy, 4.5, "c2-soft")
    doc.text(556, 193, "环路树宽 tw 指数墙", "sm c2-txt", "middle")

    # Col 2 exact entanglement bond-dimension wall (S_cut = 0..16, log2(chi) = 0..16)
    c2x0, c2x1 = 379.0, 615.0

    def s2x(ent: float) -> float:
        return c2x0 + (ent / 16.0) * (c2x1 - c2x0)

    def s2y(lg2: float) -> float:
        return cy1 - (lg2 / 16.0) * (cy1 - cy0)

    for ev in [0, 4, 8, 12, 16]:
        gx = s2x(ev)
        doc.line(gx, cy0, gx, cy1, "grid")
        doc.line(gx, cy1, gx, cy1 + 4, "axis")
        doc.text(gx, cy1 + 16, str(ev), "sm", "middle")
    for lg2, lbl in [(0, "1"), (8, "2⁸"), (16, "2¹⁶")]:
        gy = s2y(lg2)
        doc.line(c2x0, gy, c2x1, gy, "grid")
        doc.line(c2x0 - 4, gy, c2x0, gy, "axis")
        doc.text(c2x0 - 7, gy + 4, lbl, "sm", "end")
    doc.text(497, 345, "二分纠缠熵 S_cut (bit) → 键维 χ", "smb", "middle")

    pts_vol = [(s2x(s), s2y(s)) for s in range(0, 17)]
    pts_bp = [(s2x(s), s2y(0.55 * s)) for s in range(0, 17)]
    pts_area = [(s2x(s), s2y(min(4.0, float(s)))) for s in range(0, 17)]
    doc.line(c2x0, s2y(10.0), c2x1, s2y(10.0), "guide")
    doc.line(c2x0, cy0, c2x0, cy1, "axis")
    doc.line(c2x0, cy1, c2x1, cy1, "axis")
    doc.polyline(pts_vol, "c2", 'stroke-width="2.2"')
    doc.polyline(pts_bp, "c4", 'stroke-width="2.0" stroke-dasharray="5 3"')
    doc.polyline(pts_area, "c3", 'stroke-width="2.2"')
    doc.text(385, 234, "— 体积律 χ = 2^S", "sm c2-txt")
    doc.text(385, 251, "-- BP-TN 弱环路", "sm c4-txt")
    doc.text(612, 309, "— 1D 面积律", "sm c3-txt", "end")

    doc.rect(343, 354, 274, 70, "c3-soft", rx=7)
    doc.text(353, 373, "优势：任意连续旋转 / T 门，低纠缠态", "smb c3-txt")
    doc.text(353, 393, "壁垒：深层体积律 χ ~ 2^S 与 2D 强环路", "sm")
    doc.text(353, 413, "工具：ITensor · quimb · BP-TN", "sm")

    # ===== Column 3: Noisy Heisenberg Pauli Propagation =====
    doc.panel(642, 64, 298, 370, "3. 含噪 Pauli 传播（SPD）")
    doc.rect(654, 100, 274, 100, "subpanel", rx=7)
    doc.text(791, 116, "海森堡反向算符树（截断 + 噪声阻尼）", "smb", "middle")

    # Operator branching schematic
    doc.rect(663, 142, 34, 26, "c5-soft", rx=5)
    doc.text(680, 159, "O", "lblb c5-txt", "middle")
    doc.line(697, 155, 720, 155, "axis", 'stroke-width="1.4" marker-end="url(#arr-ink)"')
    doc.rect(723, 142, 42, 26, "c1-soft", rx=5)
    doc.text(744, 159, "P", "lblb c1-txt", "middle")

    # Split at non-Clifford Rz(theta)
    doc.line(765, 150, 798, 137, "c1", 'stroke-width="1.6" marker-end="url(#arr-c1)"')
    doc.line(765, 160, 798, 173, "c2", 'stroke-width="1.5" stroke-dasharray="4 2" marker-end="url(#arr-c2)"')
    doc.rect(801, 124, 118, 24, "c1-soft", rx=5)
    doc.text(860, 140, "低权重 w≤w_max 保留", "sm c1-txt", "middle")
    doc.rect(801, 160, 118, 24, "c2-soft", rx=5, extra='stroke-dasharray="4 2"')
    doc.text(860, 176, "高权重 (1−p)^w 剪枝", "sm c2-txt", "middle")
    doc.text(791, 196, "非 Clifford 门分支由高权重阻尼压死", "sm", "middle")

    # Col 3 exact exponential damping plot: (1-p)^w for w=0..20
    c3x0, c3x1 = 690.0, 926.0

    def s3x(w: float) -> float:
        return c3x0 + (w / 20.0) * (c3x1 - c3x0)

    def s3y(amp: float) -> float:
        return cy1 - amp * (cy1 - cy0)

    for wv in [0, 5, 10, 15, 20]:
        gx = s3x(wv)
        doc.line(gx, cy0, gx, cy1, "grid")
        doc.line(gx, cy1, gx, cy1 + 4, "axis")
        doc.text(gx, cy1 + 16, str(wv), "sm", "middle")
    for av in [0.0, 0.5, 1.0]:
        gy = s3y(av)
        doc.line(c3x0, gy, c3x1, gy, "grid")
        doc.line(c3x0 - 4, gy, c3x0, gy, "axis")
        doc.text(c3x0 - 7, gy + 4, f"{av:.1f}", "sm", "end")
    doc.text(808, 345, "Pauli 串权重 w → 阻尼因子 (1−p)^w", "smb", "middle")

    pts_p01 = [(s3x(w), s3y((1.0 - 0.01) ** w)) for w in range(21)]
    pts_p08 = [(s3x(w), s3y((1.0 - 0.08) ** w)) for w in range(21)]
    pts_p20 = [(s3x(w), s3y((1.0 - 0.20) ** w)) for w in range(21)]

    # Weight cutoff guide at w_max = 12
    x_cut = s3x(12.0)
    doc.line(x_cut, cy0, x_cut, cy1, "guide")
    doc.line(c3x0, cy0, c3x0, cy1, "axis")
    doc.line(c3x0, cy1, c3x1, cy1, "axis")
    doc.polyline(pts_p01, "c2", 'stroke-width="2.2"')
    doc.polyline(pts_p08, "c4", 'stroke-width="2.0" stroke-dasharray="5 3"')
    doc.polyline(pts_p20, "c1", 'stroke-width="2.2"')

    doc.text(x_cut - 4, 249, "w_max", "sm", "end")
    doc.text(923, 255, "p=0.01（低噪）", "sm c2-txt", "end")
    doc.text(923, 286, "p=0.08", "sm c4-txt", "end")
    doc.text(768, 290, "p=0.20", "sm c1-txt")

    doc.rect(654, 354, 274, 70, "c4-soft", rx=7)
    doc.text(664, 373, "优势：百比特浅/含噪 NISQ 局域期望", "smb c4-txt")
    doc.text(664, 393, "壁垒：低噪声 + 深层大角非 Clifford", "sm")
    doc.text(664, 413, "工具：SPD · PauliPropagation.jl", "sm")

    return doc.render()


GENERATORS = [
    ("v4-11-decoder-latency-budget.svg", fig_11_decoder_latency_budget),
    ("v4-13-entropy-dpi-chain.svg", fig_13_entropy_dpi_chain),
    ("v4-16-walk-shadows.svg", fig_16_walk_shadows),
    ("v4-18-capacity-complexity-ladder.svg", fig_18_capacity_complexity_ladder),
    ("v4-20-sensing-ramsey-qfi.svg", fig_20_sensing_ramsey_qfi),
    ("v4-21-sim-engines-architecture.svg", fig_21_sim_engines_architecture),
]


def generate_all() -> list[Path]:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for filename, fn in GENERATORS:
        svg_xml = fn()
        out_path = ASSETS_DIR / filename
        out_path.write_text(svg_xml, encoding="utf-8")
        # Re-parse written file to verify strict XML well-formedness
        root = ET.parse(out_path).getroot()
        texts = root.findall(".//{http://www.w3.org/2000/svg}text")
        assert len(texts) >= 10, f"{filename} has unexpectedly few <text> nodes: {len(texts)}"
        written.append(out_path)
    return written


def main() -> int:
    paths = generate_all()
    print(f"[V4 Part 2] Generated and XML-validated {len(paths)} SVG figures:")
    for p in paths:
        print(f"  - {p.relative_to(ROOT)} ({p.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
