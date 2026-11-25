#!/usr/bin/env python3
"""Reproduce handbook/assets/bloch-sphere.svg via right-handed 3D orthographic projection.

Uses Python 3 standard library only (argparse, hashlib, math, pathlib, xml.etree.ElementTree).
Projection parameters match the accepted textbook figure:
  - Canvas viewBox: 0 0 900 620, sphere center (336, 344), radius R = 180
  - Right-handed Cartesian frame: +X x +Y = +Z
  - Camera elevation alpha = 19 deg, azimuth beta = 34 deg
    Screen right u = (-sin(beta), cos(beta), 0)
    Screen up    v = (-cos(beta)*sin(alpha), -sin(beta)*sin(alpha), cos(alpha))
    Viewer dir   d = u x v = (cos(beta)*cos(alpha), sin(beta)*cos(alpha), sin(alpha))

Run:
  python3 codes/practice/generate_bloch_sphere.py --check
  python3 codes/practice/generate_bloch_sphere.py --output /path/to/out.svg
"""

from __future__ import annotations

import argparse
import hashlib
import math
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "handbook" / "assets" / "bloch-sphere.svg"

W, H = 900, 620
CX, CY, R = 336.0, 344.0, 180.0
ELEV_DEG = 19.0
AZIM_DEG = 34.0
TOL = 1e-12


def fmt(val: float) -> str:
    s = f"{val:.2f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def project_3d(x: float, y: float, z: float) -> tuple[float, float, float]:
    """Orthographically project 3D Bloch point (x, y, z) to (sx, sy, depth)."""
    el = math.radians(ELEV_DEG)
    az = math.radians(AZIM_DEG)
    u = -x * math.sin(az) + y * math.cos(az)
    v = -x * math.cos(az) * math.sin(el) - y * math.sin(az) * math.sin(el) + z * math.cos(el)
    d = x * math.cos(az) * math.cos(el) + y * math.sin(az) * math.cos(el) + z * math.sin(el)
    return CX + R * u, CY - R * v, d


def arrow_triangle_path(
    x0: float, y0: float, x1: float, y1: float, length: float, half_width: float
) -> str:
    dx, dy = x1 - x0, y1 - y0
    norm = math.hypot(dx, dy)
    assert norm > TOL
    ux, uy = dx / norm, dy / norm
    px, py = -uy, ux
    bx, by = x1 - ux * length, y1 - uy * length
    w1x, w1y = bx + px * half_width, by + py * half_width
    w2x, w2y = bx - px * half_width, by - py * half_width
    return f"M{fmt(x1)} {fmt(y1)}L{fmt(w1x)} {fmt(w1y)}L{fmt(w2x)} {fmt(w2y)}Z"


def polyline_path(segments: list[list[tuple[float, float]]]) -> str:
    chunks: list[str] = []
    for seg in segments:
        if not seg:
            continue
        head = f"M{fmt(seg[0][0])} {fmt(seg[0][1])}"
        tail = "".join(f"L{fmt(x)} {fmt(y)}" for x, y in seg[1:])
        chunks.append(head + tail)
    return " ".join(chunks)


def verify_projection_basis() -> None:
    """Verify orthonormality and right-handedness of (u, v, d) camera basis."""
    el = math.radians(ELEV_DEG)
    az = math.radians(AZIM_DEG)
    u = (-math.sin(az), math.cos(az), 0.0)
    v = (-math.cos(az) * math.sin(el), -math.sin(az) * math.sin(el), math.cos(el))
    d = (math.cos(az) * math.cos(el), math.sin(az) * math.cos(el), math.sin(el))

    def dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def cross(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
        return (
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        )

    for vec in (u, v, d):
        assert abs(dot(vec, vec) - 1.0) < TOL
    assert abs(dot(u, v)) < TOL and abs(dot(u, d)) < TOL and abs(dot(v, d)) < TOL
    uxv = cross(u, v)
    assert all(abs(uxv[i] - d[i]) < TOL for i in range(3)), "Camera basis must be right-handed"

    # Confirm front hemisphere (+X, +Y, +Z) vs back hemisphere (-X, -Y, -Z)
    for vec in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
        assert project_3d(*vec)[2] > 0.0
    for vec in [(-1, 0, 0), (0, -1, 0), (0, 0, -1)]:
        assert project_3d(*vec)[2] < 0.0


def build_bloch_sphere_svg() -> str:
    verify_projection_basis()

    # XZ meridian (y = 0, theta = 0..360 deg), split into front (depth >= 0) and back (depth < 0)
    front_segs: list[list[tuple[float, float]]] = []
    back_segs: list[list[tuple[float, float]]] = []
    cur_front: list[tuple[float, float]] = []
    cur_back: list[tuple[float, float]] = []
    for deg in range(361):
        rad = math.radians(deg)
        sx, sy, depth = project_3d(math.sin(rad), 0.0, math.cos(rad))
        if depth >= 0.0:
            cur_front.append((sx, sy))
            if cur_back:
                back_segs.append(cur_back)
                cur_back = []
        else:
            cur_back.append((sx, sy))
            if cur_front:
                front_segs.append(cur_front)
                cur_front = []
    if cur_front:
        front_segs.append(cur_front)
    if cur_back:
        back_segs.append(cur_back)

    meridian_back_d = polyline_path(back_segs)
    meridian_front_d = polyline_path(front_segs)
    ry_eq = R * math.sin(math.radians(ELEV_DEG))

    # Azimuthal CCW angle arc (+X -> +Y) at radius 0.42 in equatorial plane z = 0
    phi_r = 0.42
    phi0, phi1 = 0.08, math.pi / 2.0 - 0.08
    phi_pts: list[tuple[float, float]] = []
    for i in range(31):
        ph = phi0 + (phi1 - phi0) * i / 30.0
        sx, sy, _ = project_3d(phi_r * math.cos(ph), phi_r * math.sin(ph), 0.0)
        phi_pts.append((sx, sy))
    phi_arc_d = polyline_path([phi_pts])
    phi_head_d = arrow_triangle_path(
        phi_pts[-2][0], phi_pts[-2][1], phi_pts[-1][0], phi_pts[-1][1], 9.0, 3.1
    )

    # Positive and negative axis tip coordinates
    pz_x, pz_y, _ = project_3d(0.0, 0.0, 1.29)
    px_x, px_y, _ = project_3d(1.82, 0.0, 0.0)
    py_x, py_y, _ = project_3d(0.0, 1.38, 0.0)
    nz_x, nz_y, _ = project_3d(0.0, 0.0, -1.16)
    nx_x, nx_y, _ = project_3d(-1.72, 0.0, 0.0)
    ny_x, ny_y, _ = project_3d(0.0, -1.20, 0.0)

    # Six cardinal benchmark states on the unit Bloch sphere
    p0_x, p0_y, _ = project_3d(0.0, 0.0, 1.0)
    p1_x, p1_y, _ = project_3d(0.0, 0.0, -1.0)
    pp_x, pp_y, _ = project_3d(1.0, 0.0, 0.0)
    pm_x, pm_y, _ = project_3d(-1.0, 0.0, 0.0)
    ppi_x, ppi_y, _ = project_3d(0.0, 1.0, 0.0)
    pmi_x, pmi_y, _ = project_3d(0.0, -1.0, 0.0)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Bloch 球上的六个基准量子态（右手坐标系）</title>
  <desc id="desc">采用标准右手三维正交投影（俯角 19°、方位角 34°）绘制单位 Bloch 球：+Z 朝上，+X 朝前左，+Y 朝前右，从 +Z 俯视 +X 到 +Y 为逆时针方向；四个赤道基准态 |+⟩、|−⟩、|+i⟩、|−i⟩ 严格落在赤道椭圆上，纯态在球面、混态在球内。</desc>
  <style>
    :root{{color-scheme:light dark}}
    .bg{{fill:#f8fafc}}
    .sphere{{stroke:#2e6f95;stroke-width:3;fill:#dff4ff;fill-opacity:.50}}
    .equator-front{{stroke:#2e6f95;stroke-width:2.2;fill:none}}
    .equator-back{{stroke:#5397ba;stroke-width:1.8;stroke-dasharray:7 6;fill:none}}
    .meridian-front{{stroke:#7c9bb0;stroke-width:1.4;fill:none}}
    .meridian-back{{stroke:#9ab2c4;stroke-width:1.2;stroke-dasharray:5 5;fill:none}}
    .axis{{stroke:#19324d;stroke-width:2.2;fill:none}}
    .axis-neg{{stroke:#5a758c;stroke-width:1.6;stroke-dasharray:5 4;fill:none}}
    .axishead{{fill:#19324d}}
    .phi-arc{{stroke:#1b6ca8;stroke-width:2;fill:none}}
    .phi-head{{fill:#1b6ca8}}
    .phi-lbl{{font:600 17px Georgia,'Times New Roman',serif;fill:#145282}}
    .origin{{fill:#ffffff;stroke:#19324d;stroke-width:2}}
    .point-front{{fill:#d04a4a;stroke:#ffffff;stroke-width:1.8}}
    .point-back{{fill:#f8fafc;stroke:#d04a4a;stroke-width:2.8}}
    .title{{font:700 22px 'PingFang SC',system-ui,sans-serif;fill:#13263a}}
    .label{{font:600 19px 'PingFang SC',system-ui,sans-serif;fill:#13263a}}
    .label-back{{font:500 18px 'PingFang SC',system-ui,sans-serif;fill:#3e566d}}
    .small{{font:400 16.5px 'PingFang SC',system-ui,sans-serif;fill:#3e566d}}
    .note{{fill:#fff7dc;stroke:#c18b21;stroke-width:1.5}}
    @media(prefers-color-scheme:dark){{
      .bg{{fill:#101820}}
      .sphere{{fill:#164968;fill-opacity:.54;stroke:#7ed4ff}}
      .equator-front{{stroke:#7ed4ff}}
      .equator-back{{stroke:#5ba6cc}}
      .meridian-front{{stroke:#6f93ad}}
      .meridian-back{{stroke:#527187}}
      .axis{{stroke:#d7e8f5}}
      .axis-neg{{stroke:#7e9bb3}}
      .axishead{{fill:#d7e8f5}}
      .phi-arc{{stroke:#6bc2f5}}
      .phi-head{{fill:#6bc2f5}}
      .phi-lbl{{fill:#8fd4fa}}
      .origin{{fill:#101820;stroke:#d7e8f5}}
      .point-front{{fill:#f07171;stroke:#101820}}
      .point-back{{fill:#101820;stroke:#f07171}}
      .title,.label{{fill:#eef6ff}}
      .label-back,.small{{fill:#bdd0e1}}
      .note{{fill:#3b3218;stroke:#d6aa4b}}
    }}
  </style>
  <rect class="bg" width="{W}" height="{H}" rx="28"/>
  <text class="title" x="38" y="52">单量子比特的 Bloch 球（右手坐标系）</text>
  <text class="small" x="38" y="80">纯态位于球面，混态位于球内；实线为前半球可见弧，虚线为后半球遮挡弧，+X → +Y 沿赤道逆时针。</text>

  <!-- Sphere silhouette -->
  <circle class="sphere" cx="{fmt(CX)}" cy="{fmt(CY)}" r="{fmt(R)}"/>

  <!-- Back hidden curves (meridian & equator) -->
  <path class="meridian-back" d="{meridian_back_d}"/>
  <path class="equator-back" d="M{fmt(CX - R)} {fmt(CY)}A{fmt(R)} {fmt(ry_eq)} 0 0 1 {fmt(CX + R)} {fmt(CY)}"/>

  <!-- Negative half-axes (dashed) -->
  <line class="axis-neg" x1="{fmt(CX)}" y1="{fmt(CY)}" x2="{fmt(nz_x)}" y2="{fmt(nz_y)}"/>
  <line class="axis-neg" x1="{fmt(CX)}" y1="{fmt(CY)}" x2="{fmt(nx_x)}" y2="{fmt(nx_y)}"/>
  <line class="axis-neg" x1="{fmt(CX)}" y1="{fmt(CY)}" x2="{fmt(ny_x)}" y2="{fmt(ny_y)}"/>

  <!-- Back benchmark points (-Z, -X, -Y) -->
  <circle class="point-back" cx="{fmt(p1_x)}" cy="{fmt(p1_y)}" r="6.8"/>
  <circle class="point-back" cx="{fmt(pm_x)}" cy="{fmt(pm_y)}" r="6.8"/>
  <circle class="point-back" cx="{fmt(pmi_x)}" cy="{fmt(pmi_y)}" r="6.8"/>

  <!-- Front visible curves (meridian & equator) -->
  <path class="meridian-front" d="{meridian_front_d}"/>
  <path class="equator-front" d="M{fmt(CX - R)} {fmt(CY)}A{fmt(R)} {fmt(ry_eq)} 0 0 0 {fmt(CX + R)} {fmt(CY)}"/>

  <!-- Azimuthal CCW angle arc (+X -> +Y) -->
  <path class="phi-arc" d="{phi_arc_d}"/>
  <path class="phi-head" d="{phi_head_d}"/>
  <text class="phi-lbl" x="360.5" y="381.62" text-anchor="middle">φ</text>

  <!-- Positive half-axes (solid with arrowheads) -->
  <line class="axis" x1="{fmt(CX)}" y1="{fmt(CY)}" x2="{fmt(pz_x)}" y2="{fmt(pz_y)}"/>
  <line class="axis" x1="{fmt(CX)}" y1="{fmt(CY)}" x2="{fmt(px_x)}" y2="{fmt(px_y)}"/>
  <line class="axis" x1="{fmt(CX)}" y1="{fmt(CY)}" x2="{fmt(py_x)}" y2="{fmt(py_y)}"/>
  <path class="axishead" d="{arrow_triangle_path(CX, CY, pz_x, pz_y, 15.0, 5.25)}"/>
  <path class="axishead" d="{arrow_triangle_path(CX, CY, px_x, px_y, 15.0, 5.25)}"/>
  <path class="axishead" d="{arrow_triangle_path(CX, CY, py_x, py_y, 15.0, 5.25)}"/>

  <!-- Origin (maximally mixed state I/2) -->
  <circle class="origin" cx="{fmt(CX)}" cy="{fmt(CY)}" r="4.5"/>

  <!-- Front benchmark points (+Z, +X, +Y) -->
  <circle class="point-front" cx="{fmt(p0_x)}" cy="{fmt(p0_y)}" r="7.5"/>
  <circle class="point-front" cx="{fmt(pp_x)}" cy="{fmt(pp_y)}" r="7.5"/>
  <circle class="point-front" cx="{fmt(ppi_x)}" cy="{fmt(ppi_y)}" r="7.5"/>

  <!-- Six benchmark state labels -->
  <text class="label" x="{fmt(pz_x + 14)}" y="{fmt(pz_y + 14)}">|0⟩ (+Z)</text>
  <text class="label-back" x="{fmt(nz_x + 14)}" y="{fmt(nz_y + 6)}">|1⟩ (−Z)</text>
  <text class="label" x="{fmt(px_x - 8)}" y="{fmt(px_y + 24)}" text-anchor="middle">|+⟩ (+X)</text>
  <text class="label-back" x="{fmt(nx_x + 8)}" y="{fmt(nx_y + 2)}">|−⟩ (−X)</text>
  <text class="label" x="{fmt(py_x - 8)}" y="{fmt(py_y + 28)}">|+i⟩ (+Y)</text>
  <text class="label-back" x="{fmt(ny_x - 8)}" y="{fmt(ny_y - 6)}" text-anchor="end">|−i⟩ (−Y)</text>

  <!-- Right parameterization card -->
  <rect class="note" x="634" y="156" width="234" height="302" rx="18"/>
  <text class="label" x="656" y="194">参数化与手性</text>
  <text class="small" x="656" y="232">|ψ⟩ = cos(θ/2)|0⟩</text>
  <text class="small" x="688" y="259">+ eⁱᵠ sin(θ/2)|1⟩</text>
  <text class="small" x="656" y="302">θ：从 +Z 轴量起</text>
  <text class="small" x="656" y="332">φ：赤道方位角（逆时针）</text>
  <text class="small" x="656" y="362">右手系：+X × +Y = +Z</text>
  <text class="small" x="656" y="400">球心 I/2：最大混态</text>
  <circle class="point-front" cx="662" cy="427" r="5.5"/>
  <text class="small" x="674" y="433">前半球</text>
  <circle class="point-back" cx="754" cy="427" r="5.0"/>
  <text class="small" x="766" y="433">后半球</text>
</svg>
"""
    ET.fromstring(svg)
    return svg


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce right-handed Bloch sphere SVG.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify generated SVG matches existing handbook/assets/bloch-sphere.svg without overwriting.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUT,
        help="Output SVG path (default: handbook/assets/bloch-sphere.svg).",
    )
    args = parser.parse_args()

    svg = build_bloch_sphere_svg()
    new_sha = hashlib.sha256(svg.encode("utf-8")).hexdigest()

    if args.check:
        existing = DEFAULT_OUT.read_text(encoding="utf-8")
        old_sha = hashlib.sha256(existing.encode("utf-8")).hexdigest()
        assert svg == existing, (
            f"Generated SVG differs from {DEFAULT_OUT} "
            f"(new sha256={new_sha[:12]}, existing={old_sha[:12]})"
        )
        print(f"[OK] byte-identical match with {DEFAULT_OUT.name} (sha256={new_sha[:16]}...)")
        return

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    print(f"[OK] wrote {args.output} ({len(svg.encode('utf-8'))} bytes, sha256={new_sha[:16]}...)")


if __name__ == "__main__":
    main()
