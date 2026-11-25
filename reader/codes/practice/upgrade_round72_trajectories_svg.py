#!/usr/bin/env python3
"""Rebuild handbook/assets/round72-foundations-trajectories.svg as a crisp,
dual-theme (light/dark), real-<text>, pure-stdlib SVG directly from the saved
official QuTiP trajectory data in codes/foundations/sdk/all-results.json.
"""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "codes/foundations/sdk/all-results.json"
OUT_PATH = ROOT / "handbook/assets/round72-foundations-trajectories.svg"


def build_svg() -> str:
    d = json.loads(DATA_PATH.read_text(encoding="utf-8"))["cases"]["qutip"]["result"]
    times = d["times_us"]
    exact = d["exact_expect"][0]
    mc = d["mcsolve_mean_expect"][0]
    se = d["empirical_standard_errors"][0]
    me = [row[1][1][0] for row in d["mesolve_density_matrices"]]
    ntraj = d["trajectory_count"]
    max_me_err = d["mesolve_max_matrix_error"]
    max_mc_err = d["mcsolve_max_matrix_error"]
    assert len(times) == 41 and abs(times[-1] - 4.0) < 1e-12
    assert max(abs(a - b) for a, b in zip(exact, me)) < 1e-6

    W, H = 960, 560
    # Top panel: population vs time
    px0, px1 = 96, 676
    py0, py1 = 98, 314
    # Bottom panel: residual (MC - analytic) vs time
    ry0, ry1 = 368, 496

    def mx(t: float) -> float:
        return px0 + (t / 4.0) * (px1 - px0)

    def my(val: float) -> float:
        # y in [0.0, 0.27]
        return py1 - (val / 0.27) * (py1 - py0)

    def mry(diff: float) -> float:
        # diff in [-0.004, +0.004]
        return ry1 - ((diff + 0.004) / 0.008) * (ry1 - ry0)

    exact_pts = " ".join(f"{mx(t):.1f},{my(v):.1f}" for t, v in zip(times, exact))
    me_pts = " ".join(f"{mx(t):.1f},{my(v):.1f}" for t, v in zip(times, me))

    mc_err_svg = []
    for i in range(0, len(times), 4):
        cx, cy = mx(times[i]), my(mc[i])
        y_hi, y_lo = my(mc[i] + se[i]), my(mc[i] - se[i])
        mc_err_svg.append(
            f'<line x1="{cx:.1f}" y1="{y_hi:.1f}" x2="{cx:.1f}" y2="{y_lo:.1f}" class="errbar"/>'
            f'<line x1="{cx-4:.1f}" y1="{y_hi:.1f}" x2="{cx+4:.1f}" y2="{y_hi:.1f}" class="errbar"/>'
            f'<line x1="{cx-4:.1f}" y1="{y_lo:.1f}" x2="{cx+4:.1f}" y2="{y_lo:.1f}" class="errbar"/>'
            f'<rect x="{cx-3.5:.1f}" y="{cy-3.5:.1f}" width="7" height="7" rx="1.2" class="mc-dot"/>'
        )

    res_pts = " ".join(f"{mx(t):.1f},{mry(m - e):.1f}" for t, m, e in zip(times, mc, exact))
    res_err_svg = []
    for i in range(0, len(times), 2):
        diff = mc[i] - exact[i]
        cx, cy = mx(times[i]), mry(diff)
        y_hi, y_lo = mry(diff + se[i]), mry(diff - se[i])
        res_err_svg.append(
            f'<line x1="{cx:.1f}" y1="{y_hi:.1f}" x2="{cx:.1f}" y2="{y_lo:.1f}" class="errbar"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.7" class="mc-dot"/>'
        )

    top_grid = []
    for yv in [0.0, 0.05, 0.10, 0.15, 0.20, 0.25]:
        yy = my(yv)
        top_grid.append(f'<line x1="{px0}" y1="{yy:.1f}" x2="{px1}" y2="{yy:.1f}" class="grid"/>')
        top_grid.append(f'<text x="{px0-10}" y="{yy+4:.1f}" text-anchor="end" class="tick">{yv:.2f}</text>')
    for tv in [0, 1, 2, 3, 4]:
        xx = mx(tv)
        top_grid.append(f'<line x1="{xx:.1f}" y1="{py0}" x2="{xx:.1f}" y2="{py1}" class="grid"/>')
        top_grid.append(f'<line x1="{xx:.1f}" y1="{ry0}" x2="{xx:.1f}" y2="{ry1}" class="grid"/>')
        top_grid.append(f'<text x="{xx:.1f}" y="{ry1+20}" text-anchor="middle" class="tick">{tv}.0</text>')

    res_grid = []
    for dv, lbl in [(-0.003, "-0.003"), (0.0, "0.000"), (0.003, "+0.003")]:
        yy = mry(dv)
        cls = "zero-line" if dv == 0.0 else "grid"
        res_grid.append(f'<line x1="{px0}" y1="{yy:.1f}" x2="{px1}" y2="{yy:.1f}" class="{cls}"/>')
        res_grid.append(f'<text x="{px0-10}" y="{yy+4:.1f}" text-anchor="end" class="tick">{lbl}</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">量子轨迹平均逼近主方程系综态（4096 条 QuTiP 实跑轨迹对照）</title>
  <desc id="desc">基于保存的 QuTiP 实跑数据绘制：上图对比解析解、mesolve 与 4096 条 mcsolve 轨迹均值及 ±1 SE 误差棒，下图给出 4,096 条轨迹 ρ₁₁ 残差（同批轨迹跨时刻相关），右侧误差账本列明全密度矩阵最大元误差（含非对角项）。</desc>
  <style>
    svg {{ font-family: "PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC",sans-serif; }}
    .bg {{ fill: #fbfaf6; }}
    .panel {{ fill: #ffffff; stroke: #d8d4c8; stroke-width: 1.2; }}
    .card {{ fill: #f4f1e8; stroke: #d5cfc0; stroke-width: 1.2; }}
    .title {{ font-size: 20px; font-weight: 700; fill: #162421; }}
    .sub {{ font-size: 13px; fill: #4c5c57; }}
    .sec {{ font-size: 13.5px; font-weight: 700; fill: #14453d; }}
    .axis-lbl {{ font-size: 12.5px; font-weight: 600; fill: #263733; }}
    .tick {{ font-size: 11.5px; fill: #4a5a55; }}
    .note {{ font-size: 12px; fill: #2b3a36; }}
    .mono {{ font-size: 12px; font-family: "SFMono-Regular","Menlo","Consolas",monospace; fill: #14453d; font-weight: 600; }}
    .grid {{ stroke: #e5e1d6; stroke-width: 1; }}
    .axis {{ stroke: #4b5c57; stroke-width: 1.3; fill: none; }}
    .zero-line {{ stroke: #1a365d; stroke-width: 1.2; stroke-dasharray: 4 3; }}
    .exact {{ fill: none; stroke: #1a365d; stroke-width: 2.4; }}
    .me {{ fill: none; stroke: #c05621; stroke-width: 2; stroke-dasharray: 7 4; }}
    .res-line {{ fill: none; stroke: #1f7a68; stroke-width: 1.5; opacity: 0.8; }}
    .errbar {{ stroke: #1f7a68; stroke-width: 1.3; }}
    .mc-dot {{ fill: #1f7a68; stroke: #ffffff; stroke-width: 0.9; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #121716; }}
      .panel {{ fill: #18201e; stroke: #2f3e3a; }}
      .card {{ fill: #1b2522; stroke: #31423d; }}
      .title {{ fill: #ecf3f0; }}
      .sub {{ fill: #a4b7b1; }}
      .sec {{ fill: #6cd3bc; }}
      .axis-lbl {{ fill: #d7e4df; }}
      .tick {{ fill: #9fb3ac; }}
      .note {{ fill: #d0ddd8; }}
      .mono {{ fill: #84e0cb; }}
      .grid {{ stroke: #273531; }}
      .axis {{ stroke: #7f9790; }}
      .zero-line {{ stroke: #7bb4f0; }}
      .exact {{ stroke: #7bb4f0; }}
      .me {{ stroke: #f29d5b; }}
      .res-line {{ stroke: #55d0b4; }}
      .errbar {{ stroke: #55d0b4; }}
      .mc-dot {{ fill: #55d0b4; stroke: #18201e; }}
    }}
  </style>
  <rect width="{W}" height="{H}" rx="12" class="bg"/>
  <text x="34" y="38" class="title">量子轨迹平均逼近主方程系综态（4,096 条实跑轨迹对照）</text>
  <text x="34" y="60" class="sub">数据来源：codes/foundations/sdk/all-results.json（QuTiP mesolve / mcsolve 实跑存档，κ = 0.70 μs⁻¹，seed 锁定）</text>

  <!-- Top Plot Panel -->
  <text x="{px0}" y="{py0-10}" class="sec">上图：激发态布居数 ρ₁₁(t) 随时间衰减</text>
  <rect x="{px0}" y="{py0}" width="{px1-px0}" height="{py1-py0}" class="panel"/>
  {"".join(top_grid)}
  <polyline points="{exact_pts}" class="exact"/>
  <polyline points="{me_pts}" class="me"/>
  {"".join(mc_err_svg)}
  <rect x="{px0}" y="{py0}" width="{px1-px0}" height="{py1-py0}" class="axis"/>
  <text x="32" y="{(py0+py1)/2:.0f}" transform="rotate(-90 32 {(py0+py1)/2:.0f})" text-anchor="middle" class="axis-lbl">激发态布居数（无量纲）</text>

  <!-- Legend inside top-right -->
  <rect x="466" y="110" width="198" height="74" rx="8" class="card"/>
  <line x1="480" y1="129" x2="512" y2="129" class="exact"/>
  <text x="520" y="133" class="note">解析主方程系综解</text>
  <line x1="480" y1="149" x2="512" y2="149" class="me"/>
  <text x="520" y="153" class="note">mesolve 密度矩阵解</text>
  <rect x="492" y="165" width="7" height="7" rx="1.2" class="mc-dot"/>
  <text x="520" y="173" class="note">mcsolve 均值 ± 1 SE</text>

  <!-- Bottom Residual Panel -->
  <text x="{px0}" y="{ry0-12}" class="sec">下图：4,096 条轨迹 ρ₁₁ 残差（同批轨迹跨时刻相关）</text>
  <rect x="{px0}" y="{ry0}" width="{px1-px0}" height="{ry1-ry0}" class="panel"/>
  {"".join(res_grid)}
  <polyline points="{res_pts}" class="res-line"/>
  {"".join(res_err_svg)}
  <rect x="{px0}" y="{ry0}" width="{px1-px0}" height="{ry1-ry0}" class="axis"/>
  <text x="32" y="{(ry0+ry1)/2:.0f}" transform="rotate(-90 32 {(ry0+ry1)/2:.0f})" text-anchor="middle" class="axis-lbl">残差 Δρ₁₁</text>
  <text x="{(px0+px1)/2:.0f}" y="{ry1+44}" text-anchor="middle" class="axis-lbl">演化时间 t（μs）</text>

  <!-- Right Diagnostic Cards -->
  <rect x="694" y="98" width="244" height="190" rx="10" class="card"/>
  <text x="708" y="121" class="sec">1. 实跑误差账本</text>
  <text x="708" y="146" class="note">轨迹样本量：</text>
  <text x="708" y="165" class="mono">N = {ntraj:,} 条独立轨迹</text>
  <text x="708" y="191" class="note">mesolve 全密度矩阵最大元误差：</text>
  <text x="708" y="210" class="mono">{max_me_err:.2e}</text>
  <text x="708" y="236" class="note">mcsolve 全密度矩阵最大元误差</text>
  <text x="708" y="253" class="note">（含非对角项）：</text>
  <text x="708" y="273" class="mono">{max_mc_err:.2e}</text>

  <rect x="694" y="302" width="244" height="194" rx="10" class="card"/>
  <text x="708" y="328" class="sec">2. 物理与统计边界</text>
  <text x="708" y="356" class="note">• 单条轨迹随机量子跃迁，</text>
  <text x="708" y="376" class="note">  始终保持纯态而非混态。</text>
  <text x="708" y="404" class="note">• 仅当对大量独立轨迹求平均，</text>
  <text x="708" y="424" class="note">  才以 1/√N 速率收敛到主方程。</text>
  <text x="708" y="452" class="note">• 标准误 SE 由实证轨迹方差</text>
  <text x="708" y="472" class="note">  直接估计，不混淆单次波动。</text>
</svg>
'''
    ET.fromstring(svg)
    return svg


if __name__ == "__main__":
    OUT_PATH.write_text(build_svg(), encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")
