#!/usr/bin/env python3
"""Generate dual-track (animated + static) cover banner SVGs for the
Quantum Computing Handbook using Python 3 standard library only.

Outputs to handbook/assets/:
  - cover-banner.svg         (CSS animations gated by prefers-reduced-motion)
  - cover-banner-static.svg  (zero SMIL / zero CSS animations for reduced motion)

Run:
  python3 codes/practice/generate_cover_banner.py
  python3 codes/practice/generate_cover_banner.py --check

Dependencies:
  Python 3 standard library only (argparse, math, pathlib, re, xml.etree.ElementTree).
  Deterministic geometry and physics calculations (no RNG, no network, no cloud calls).
"""

from __future__ import annotations

import argparse
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT / "handbook" / "assets"
W, H = 1200, 520

# Right-handed orthographic projection parameters (matching handbook/assets/bloch-sphere.svg)
BLOCH_ELEV_DEG = 19.0
BLOCH_AZIM_DEG = 34.0


def fmt(val: float) -> str:
    """Format floating-point coordinates deterministically."""
    s = f"{val:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def bloch_basis() -> tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]:
    """Return right-handed orthonormal screen basis (u_right, v_up, d_toward_viewer)."""
    a = math.radians(BLOCH_ELEV_DEG)
    b = math.radians(BLOCH_AZIM_DEG)
    u = (-math.sin(b), math.cos(b), 0.0)
    v = (-math.sin(a) * math.cos(b), -math.sin(a) * math.sin(b), math.cos(a))
    d = (math.cos(a) * math.cos(b), math.cos(a) * math.sin(b), math.sin(a))
    # Verify right-handedness: u x v == d and det([u, v, d]) == +1
    cx = u[1] * v[2] - u[2] * v[1]
    cy = u[2] * v[0] - u[0] * v[2]
    cz = u[0] * v[1] - u[1] * v[0]
    assert abs(cx - d[0]) < 1e-12 and abs(cy - d[1]) < 1e-12 and abs(cz - d[2]) < 1e-12
    det = u[0] * (v[1] * d[2] - v[2] * d[1]) - u[1] * (v[0] * d[2] - v[2] * d[0]) + u[2] * (v[0] * d[1] - v[1] * d[0])
    assert abs(det - 1.0) < 1e-12
    return u, v, d


def project_3d(
    x: float,
    y: float,
    z: float,
    cx: float,
    cy: float,
    radius: float,
    basis: tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]],
) -> tuple[float, float, float]:
    """Project 3D unit-sphere coordinates to 2D SVG (sx, sy) plus signed viewer depth."""
    u, v, d = basis
    sx = cx + radius * (u[0] * x + u[1] * y + u[2] * z)
    sy = cy - radius * (v[0] * x + v[1] * y + v[2] * z)
    depth = d[0] * x + d[1] * y + d[2] * z
    return sx, sy, depth


def split_front_back_paths(
    points_3d: list[tuple[float, float, float]],
    cx: float,
    cy: float,
    radius: float,
    basis: tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]],
) -> tuple[str, str]:
    """Split a closed or open 3D polyline into SVG path strings for front (depth>=0) and back (depth<0)."""
    front_segs: list[list[tuple[float, float]]] = []
    back_segs: list[list[tuple[float, float]]] = []
    cur_front: list[tuple[float, float]] = []
    cur_back: list[tuple[float, float]] = []

    for x, y, z in points_3d:
        sx, sy, depth = project_3d(x, y, z, cx, cy, radius, basis)
        if depth >= 0.0:
            if cur_back:
                cur_back.append((sx, sy))
                back_segs.append(cur_back)
                cur_back = []
            cur_front.append((sx, sy))
        else:
            if cur_front:
                cur_front.append((sx, sy))
                front_segs.append(cur_front)
                cur_front = []
            cur_back.append((sx, sy))

    if cur_front:
        front_segs.append(cur_front)
    if cur_back:
        back_segs.append(cur_back)

    def to_path(segs: list[list[tuple[float, float]]]) -> str:
        parts: list[str] = []
        for seg in segs:
            if len(seg) < 2:
                continue
            cmd = f"M{fmt(seg[0][0])} {fmt(seg[0][1])}" + "".join(
                f"L{fmt(px)} {fmt(py)}" for px, py in seg[1:]
            )
            parts.append(cmd)
        return " ".join(parts)

    return to_path(front_segs), to_path(back_segs)


def arrow_triangle(x1: float, y1: float, x2: float, y2: float, length: float = 9.0, half_w: float = 3.6) -> str:
    """Return SVG path for a crisp filled arrowhead pointing from (x1,y1) to (x2,y2)."""
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy)
    assert norm > 1e-9
    ux, uy = dx / norm, dy / norm
    px, py = -uy, ux
    bx, by = x2 - length * ux, y2 - length * uy
    p1 = (bx + half_w * px, by + half_w * py)
    p2 = (bx - half_w * px, by - half_w * py)
    return f"M{fmt(x2)} {fmt(y2)}L{fmt(p1[0])} {fmt(p1[1])}L{fmt(p2[0])} {fmt(p2[1])}Z"


def wave_packet_path(
    x_start: float,
    x_end: float,
    y_center: float,
    amp: float,
    cycles: float,
    phase: float,
    samples: int = 72,
) -> str:
    """Return SVG path for a Gaussian-enveloped cosine wave packet."""
    pts: list[str] = []
    span = x_end - x_start
    for i in range(samples + 1):
        u = i / samples  # 0 .. 1
        x = x_start + u * span
        env = math.exp(-((u - 0.5) / 0.27) ** 2)
        y = y_center - amp * env * math.cos(2.0 * math.pi * cycles * (u - 0.5) + phase)
        prefix = "M" if i == 0 else "L"
        pts.append(f"{prefix}{fmt(x)} {fmt(y)}")
    return "".join(pts)


def verify_surface_code_d3() -> None:
    """Independently verify [[9,1,3]] rotated surface code stabilizer commutativity."""
    # Data qubits indexed by (row, col) in {0,1,2} x {0,1,2}
    x_stabs = [
        {(0, 0), (0, 1)},  # top boundary
        {(0, 1), (0, 2), (1, 1), (1, 2)},  # interior TR
        {(1, 0), (1, 1), (2, 0), (2, 1)},  # interior BL
        {(2, 1), (2, 2)},  # bottom boundary
    ]
    z_stabs = [
        {(0, 0), (0, 1), (1, 0), (1, 1)},  # interior TL
        {(1, 1), (1, 2), (2, 1), (2, 2)},  # interior BR
        {(1, 0), (2, 0)},  # left boundary
        {(0, 2), (1, 2)},  # right boundary
    ]
    for xs in x_stabs:
        for zs in z_stabs:
            assert len(xs & zs) % 2 == 0, f"Non-commuting stabilizers: {xs} vs {zs}"
    # Logical Z along top row commutes with all X stabilizers
    logical_z = {(0, 0), (0, 1), (0, 2)}
    for xs in x_stabs:
        assert len(logical_z & xs) % 2 == 0
    # Logical X along left column commutes with all Z stabilizers and anticommutes with logical Z
    logical_x = {(0, 0), (1, 0), (2, 0)}
    for zs in z_stabs:
        assert len(logical_x & zs) % 2 == 0
    assert len(logical_x & logical_z) % 2 == 1
    # Single X error on center qubit (1,1) triggers exactly the two interior Z stabilizers
    triggered_z = [idx for idx, zs in enumerate(z_stabs) if (1, 1) in zs]
    assert triggered_z == [0, 1]


def build_mzi_panel() -> str:
    """Build Panel 01: Mach-Zehnder interferometer wave-packet + interference fringe plot."""
    phi_demo = math.pi / 3.0  # 60 deg -> P(0) = 0.75, P(1) = 0.25
    p0_demo = (1.0 + math.cos(phi_demo)) / 2.0
    p1_demo = (1.0 - math.cos(phi_demo)) / 2.0
    assert abs(p0_demo - 0.75) < 1e-12 and abs(p1_demo - 0.25) < 1e-12
    assert abs(p0_demo + p1_demo - 1.0) < 1e-12

    # Wave packets along upper arm (ref), lower arm (shifted by phi_demo), and outputs D0/D1
    wp_upper = wave_packet_path(582, 728, 142, amp=13.5, cycles=3.2, phase=0.0)
    wp_lower = wave_packet_path(582, 728, 200, amp=13.5, cycles=3.2, phase=phi_demo)
    wp_d0 = wave_packet_path(774, 834, 142, amp=15.0 * math.sqrt(p0_demo), cycles=2.2, phase=phi_demo / 2.0)
    wp_d1 = wave_packet_path(774, 834, 200, amp=15.0 * math.sqrt(p1_demo), cycles=2.2, phase=phi_demo / 2.0 + math.pi / 2.0)

    # Interference fringe mini-plot (right side of Panel 01)
    gx0, gx1 = 918.0, 1144.0
    gy0, gy1 = 214.0, 130.0  # gy0 = P=0, gy1 = P=1 (leaves clean top legend band)
    n_pts = 96
    p0_pts: list[str] = []
    p1_pts: list[str] = []
    for i in range(n_pts + 1):
        u = i / n_pts
        phi = 2.0 * math.pi * u
        x = gx0 + u * (gx1 - gx0)
        y0 = gy0 - ((1.0 + math.cos(phi)) / 2.0) * (gy0 - gy1)
        y1 = gy0 - ((1.0 - math.cos(phi)) / 2.0) * (gy0 - gy1)
        cmd = "M" if i == 0 else "L"
        p0_pts.append(f"{cmd}{fmt(x)} {fmt(y0)}")
        p1_pts.append(f"{cmd}{fmt(x)} {fmt(y1)}")
    p0_curve = "".join(p0_pts)
    p1_curve = "".join(p1_pts)
    p0_area = p0_curve + f"L{fmt(gx1)} {fmt(gy0)}L{fmt(gx0)} {fmt(gy0)}Z"

    # Marker at phi = pi/3 (u = 1/6)
    x_demo = gx0 + (phi_demo / (2.0 * math.pi)) * (gx1 - gx0)
    y_demo_0 = gy0 - p0_demo * (gy0 - gy1)
    y_demo_1 = gy0 - p1_demo * (gy0 - gy1)

    # Ticks on fringe plot
    tick_specs = [(0.0, "0"), (0.25, "π/2"), (0.5, "π"), (0.75, "3π/2"), (1.0, "2π")]
    tick_svg = []
    for u, label in tick_specs:
        tx = gx0 + u * (gx1 - gx0)
        tick_svg.append(f'<line x1="{fmt(tx)}" y1="{fmt(gy0)}" x2="{fmt(tx)}" y2="{fmt(gy0 + 4)}" stroke="#8A8275" stroke-width="1"/>')
        tick_svg.append(f'<text x="{fmt(tx)}" y="{fmt(gy0 + 16)}" text-anchor="middle" class="mono-xs">{label}</text>')

    return f"""
  <!-- Panel 01: Mach-Zehnder Interferometer & Fringe Plot -->
  <g id="panel-mzi">
    <rect x="474" y="70" width="700" height="182" rx="9" fill="#FFFFFF" stroke="#DDD7CB" stroke-width="1.2"/>
    <text x="490" y="92" class="panel-title">01 · Mach–Zehnder 干涉波包（振幅先相加再取模平方）</text>
    <text x="1158" y="92" text-anchor="end" class="mono-accent">H · P(φ) · H |0⟩  |  P(0) = cos²(φ/2)</text>

    <!-- Optical bench backdrop -->
    <rect x="488" y="104" width="398" height="134" rx="7" fill="#FAF8F3" stroke="#E5E0D5" stroke-width="1"/>

    <!-- Input port |0> -->
    <rect x="496" y="130" width="30" height="24" rx="5" fill="#1B2D2A"/>
    <text x="511" y="146" text-anchor="middle" class="badge-light">|0⟩</text>
    <line x1="526" y1="142" x2="544" y2="142" stroke="#1E6B5A" stroke-width="2.2"/>
    <line x1="518" y1="200" x2="544" y2="200" stroke="#C5BEB0" stroke-width="1.4" stroke-dasharray="3 3"/>
    <text x="510" y="204" text-anchor="middle" class="mono-xs">0</text>

    <!-- Beam Splitter BS1 (H) -->
    <rect x="544" y="122" width="32" height="98" rx="6" fill="#E6F1FA" stroke="#1F5A92" stroke-width="1.5"/>
    <line x1="549" y1="213" x2="571" y2="129" stroke="#1F5A92" stroke-width="1.4" stroke-dasharray="4 3" opacity="0.7"/>
    <text x="560" y="175" text-anchor="middle" class="gate-mini">H</text>
    <text x="560" y="116" text-anchor="middle" class="mono-xs">BS₁</text>

    <!-- Arms baselines -->
    <line x1="576" y1="142" x2="736" y2="142" stroke="#D5D0C5" stroke-width="1.3"/>
    <line x1="576" y1="200" x2="736" y2="200" stroke="#D5D0C5" stroke-width="1.3"/>

    <!-- Animated subtle energy flow guide lines -->
    <line class="mzi-flow-upper" x1="576" y1="142" x2="736" y2="142" stroke="#1E6B5A" stroke-width="2.2" stroke-dasharray="10 14" opacity="0.45"/>
    <line class="mzi-flow-lower" x1="576" y1="200" x2="736" y2="200" stroke="#C28524" stroke-width="2.2" stroke-dasharray="10 14" opacity="0.45"/>

    <!-- Wave packets in upper and lower arms -->
    <path d="{wp_upper}" fill="none" stroke="#1E6B5A" stroke-width="2.1" stroke-linejoin="round" stroke-linecap="round"/>
    <path d="{wp_lower}" fill="none" stroke="#C28524" stroke-width="2.1" stroke-linejoin="round" stroke-linecap="round"/>

    <!-- Arm labels -->
    <text x="656" y="121" text-anchor="middle" class="mono-teal">参考臂 |0⟩  (相位 0)</text>
    <!-- Phase shifter P(phi) on lower arm -->
    <rect x="633" y="188" width="46" height="24" rx="5" fill="#FBF3E0" stroke="#C28524" stroke-width="1.5"/>
    <text x="656" y="204" text-anchor="middle" class="mono-amber">P(φ)</text>
    <text x="656" y="229" text-anchor="middle" class="mono-xs">相位臂 |1⟩ · φ = π/3</text>

    <!-- Beam Splitter BS2 (H) -->
    <rect x="736" y="122" width="32" height="98" rx="6" fill="#E6F1FA" stroke="#1F5A92" stroke-width="1.5"/>
    <line x1="741" y1="213" x2="763" y2="129" stroke="#1F5A92" stroke-width="1.4" stroke-dasharray="4 3" opacity="0.7"/>
    <text x="752" y="175" text-anchor="middle" class="gate-mini">H</text>
    <text x="752" y="116" text-anchor="middle" class="mono-xs">BS₂</text>

    <!-- Output wave packets & detectors -->
    <line x1="768" y1="142" x2="838" y2="142" stroke="#D5D0C5" stroke-width="1.2"/>
    <line x1="768" y1="200" x2="838" y2="200" stroke="#D5D0C5" stroke-width="1.2"/>
    <path d="{wp_d0}" fill="none" stroke="#1E6B5A" stroke-width="2.3" stroke-linejoin="round" stroke-linecap="round"/>
    <path d="{wp_d1}" fill="none" stroke="#B84A2E" stroke-width="2.0" stroke-linejoin="round" stroke-linecap="round"/>

    <!-- Detector D0 -->
    <path d="M838 128 H848 A14 14 0 0 1 848 156 H838 Z" fill="#E5F3EE" stroke="#1E6B5A" stroke-width="1.6"/>
    <text x="849" y="146" text-anchor="middle" class="det-lbl-teal">D₀</text>
    <text x="849" y="121" text-anchor="middle" class="mono-teal">75%</text>

    <!-- Detector D1 -->
    <path d="M838 186 H848 A14 14 0 0 1 848 214 H838 Z" fill="#FAEAE4" stroke="#B84A2E" stroke-width="1.6"/>
    <text x="849" y="204" text-anchor="middle" class="det-lbl-red">D₁</text>
    <text x="849" y="230" text-anchor="middle" class="mono-red">25%</text>

    <!-- Right mini-plot: full interference fringe -->
    <rect x="896" y="104" width="264" height="134" rx="7" fill="#FAF8F3" stroke="#E5E0D5" stroke-width="1"/>
    <!-- Grid lines -->
    <line x1="{fmt(gx0)}" y1="{fmt(gy1)}" x2="{fmt(gx1)}" y2="{fmt(gy1)}" stroke="#E6E1D6" stroke-width="1"/>
    <line x1="{fmt(gx0)}" y1="{fmt((gy0 + gy1) / 2.0)}" x2="{fmt(gx1)}" y2="{fmt((gy0 + gy1) / 2.0)}" stroke="#E6E1D6" stroke-width="1" stroke-dasharray="3 3"/>
    <line x1="{fmt(gx0)}" y1="{fmt(gy0)}" x2="{fmt(gx1)}" y2="{fmt(gy0)}" stroke="#8A8275" stroke-width="1.2"/>
    <line x1="{fmt(gx0)}" y1="{fmt(gy1 - 4)}" x2="{fmt(gx0)}" y2="{fmt(gy0)}" stroke="#8A8275" stroke-width="1.2"/>

    <!-- Y labels -->
    <text x="{fmt(gx0 - 6)}" y="{fmt(gy1 + 4)}" text-anchor="end" class="mono-xs">1</text>
    <text x="{fmt(gx0 - 6)}" y="{fmt((gy0 + gy1) / 2.0 + 4)}" text-anchor="end" class="mono-xs">.5</text>
    <text x="{fmt(gx0 - 6)}" y="{fmt(gy0 + 4)}" text-anchor="end" class="mono-xs">0</text>
    {''.join(tick_svg)}

    <!-- Fringe curves -->
    <path d="{p0_area}" fill="#1E6B5A" fill-opacity="0.10"/>
    <path d="{p0_curve}" fill="none" stroke="#1E6B5A" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="{p1_curve}" fill="none" stroke="#B84A2E" stroke-width="1.7" stroke-dasharray="5 3" stroke-linejoin="round"/>

    <!-- Demo marker at phi = pi/3 -->
    <line x1="{fmt(x_demo)}" y1="{fmt(gy1)}" x2="{fmt(x_demo)}" y2="{fmt(gy0)}" stroke="#C28524" stroke-width="1.2" stroke-dasharray="3 3"/>
    <circle class="mzi-pulse-dot" cx="{fmt(x_demo)}" cy="{fmt(y_demo_0)}" r="4.5" fill="#1E6B5A" stroke="#FFFFFF" stroke-width="1.5"/>
    <circle cx="{fmt(x_demo)}" cy="{fmt(y_demo_1)}" r="4.0" fill="#B84A2E" stroke="#FFFFFF" stroke-width="1.4"/>

    <!-- Compact fringe legend in dedicated top band above gy1=130 -->
    <line x1="998" y1="117" x2="1016" y2="117" stroke="#1E6B5A" stroke-width="2.2"/>
    <text x="1021" y="121" class="mono-teal">P(0)</text>
    <line x1="1068" y1="117" x2="1086" y2="117" stroke="#B84A2E" stroke-width="1.7" stroke-dasharray="4 2"/>
    <text x="1091" y="121" class="mono-red">P(1)</text>
  </g>
"""


def build_bloch_panel() -> str:
    """Build Panel 02: Right-handed 3D orthographic Bloch sphere with Larmor precession orbit."""
    basis = bloch_basis()
    cx, cy, R = 584.0, 392.0, 62.0
    theta_deg, phi_deg = 52.0, 68.0
    theta = math.radians(theta_deg)
    phi = math.radians(phi_deg)

    # Equator points (z = 0)
    eq_pts = [(math.cos(2 * math.pi * i / 120), math.sin(2 * math.pi * i / 120), 0.0) for i in range(121)]
    eq_front, eq_back = split_front_back_paths(eq_pts, cx, cy, R, basis)

    # Prime meridian (x-z plane, y = 0)
    mer_pts = [(math.sin(2 * math.pi * i / 120), 0.0, math.cos(2 * math.pi * i / 120)) for i in range(121)]
    mer_front, mer_back = split_front_back_paths(mer_pts, cx, cy, R, basis)

    # Precession latitude circle at polar angle theta
    lat_pts = [
        (math.sin(theta) * math.cos(2 * math.pi * i / 120), math.sin(theta) * math.sin(2 * math.pi * i / 120), math.cos(theta))
        for i in range(121)
    ]
    lat_front, lat_back = split_front_back_paths(lat_pts, cx, cy, R, basis)

    # Positive & negative axes (extend cleanly beyond sphere silhouette)
    ax_len = 1.32
    pos_z = project_3d(0, 0, ax_len, cx, cy, R, basis)
    neg_z = project_3d(0, 0, -1.20, cx, cy, R, basis)
    pos_x = project_3d(ax_len, 0, 0, cx, cy, R, basis)
    neg_x = project_3d(-1.14, 0, 0, cx, cy, R, basis)
    pos_y = project_3d(0, ax_len, 0, cx, cy, R, basis)
    neg_y = project_3d(0, -1.14, 0, cx, cy, R, basis)

    # State vector |psi(theta, phi)>
    rx = math.sin(theta) * math.cos(phi)
    ry = math.sin(theta) * math.sin(phi)
    rz = math.cos(theta)
    assert abs(rx * rx + ry * ry + rz * rz - 1.0) < 1e-12
    tip = project_3d(rx, ry, rz, cx, cy, R, basis)
    eq_proj = project_3d(rx, ry, 0.0, cx, cy, R, basis)

    # Polar angle arc from +Z to state vector at radius 0.42*R
    th_arc_pts = [
        project_3d(
            0.42 * math.sin(theta * i / 20) * math.cos(phi),
            0.42 * math.sin(theta * i / 20) * math.sin(phi),
            0.42 * math.cos(theta * i / 20),
            cx,
            cy,
            R,
            basis,
        )
        for i in range(21)
    ]
    th_arc_d = "".join(("M" if i == 0 else "L") + f"{fmt(p[0])} {fmt(p[1])}" for i, p in enumerate(th_arc_pts))

    # Azimuthal arc from +X to phi on equator at radius 0.38*R
    ph_arc_pts = [
        project_3d(0.38 * math.cos(phi * i / 20), 0.38 * math.sin(phi * i / 20), 0.0, cx, cy, R, basis)
        for i in range(21)
    ]
    ph_arc_d = "".join(("M" if i == 0 else "L") + f"{fmt(p[0])} {fmt(p[1])}" for i, p in enumerate(ph_arc_pts))

    # Pole & equator benchmark points on sphere
    p_0 = project_3d(0, 0, 1, cx, cy, R, basis)
    p_1 = project_3d(0, 0, -1, cx, cy, R, basis)
    p_plus = project_3d(1, 0, 0, cx, cy, R, basis)
    p_plus_i = project_3d(0, 1, 0, cx, cy, R, basis)

    return f"""
  <!-- Panel 02: Bloch Sphere Precession -->
  <g id="panel-bloch">
    <rect x="474" y="262" width="344" height="232" rx="9" fill="#FFFFFF" stroke="#DDD7CB" stroke-width="1.2"/>
    <text x="490" y="284" class="panel-title">02 · Bloch 球进动（右手三维投影）</text>

    <!-- Sphere silhouette -->
    <circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(R)}" fill="url(#bloch-fill)" stroke="#2C6F88" stroke-width="1.8"/>

    <!-- Back hemisphere curves -->
    <path d="{mer_back}" fill="none" stroke="#9AB2BC" stroke-width="1.0" stroke-dasharray="4 4"/>
    <path d="{eq_back}" fill="none" stroke="#6B9FB4" stroke-width="1.2" stroke-dasharray="5 4"/>
    <path d="{lat_back}" fill="none" stroke="#D39D4A" stroke-width="1.3" stroke-dasharray="4 3" opacity="0.65"/>

    <!-- Negative dashed half-axes -->
    <line x1="{fmt(cx)}" y1="{fmt(cy)}" x2="{fmt(neg_z[0])}" y2="{fmt(neg_z[1])}" stroke="#7A8F99" stroke-width="1.15" stroke-dasharray="4 3"/>
    <line x1="{fmt(cx)}" y1="{fmt(cy)}" x2="{fmt(neg_x[0])}" y2="{fmt(neg_x[1])}" stroke="#7A8F99" stroke-width="1.15" stroke-dasharray="4 3"/>
    <line x1="{fmt(cx)}" y1="{fmt(cy)}" x2="{fmt(neg_y[0])}" y2="{fmt(neg_y[1])}" stroke="#7A8F99" stroke-width="1.15" stroke-dasharray="4 3"/>

    <!-- Front hemisphere curves -->
    <path d="{mer_front}" fill="none" stroke="#7A9CAB" stroke-width="1.1"/>
    <path d="{eq_front}" fill="none" stroke="#2C6F88" stroke-width="1.5"/>
    <path d="{lat_front}" fill="none" stroke="#C28524" stroke-width="1.9"/>
    <path class="bloch-orbit-flow" d="{lat_front}" fill="none" stroke="#B84A2E" stroke-width="2.1" stroke-dasharray="9 12" opacity="0.72"/>

    <!-- Positive axes with arrows -->
    <line x1="{fmt(cx)}" y1="{fmt(cy)}" x2="{fmt(pos_z[0])}" y2="{fmt(pos_z[1])}" stroke="#182C28" stroke-width="1.6"/>
    <path d="{arrow_triangle(cx, cy, pos_z[0], pos_z[1], 8.0, 3.0)}" fill="#182C28"/>
    <line x1="{fmt(cx)}" y1="{fmt(cy)}" x2="{fmt(pos_x[0])}" y2="{fmt(pos_x[1])}" stroke="#182C28" stroke-width="1.6"/>
    <path d="{arrow_triangle(cx, cy, pos_x[0], pos_x[1], 8.0, 3.0)}" fill="#182C28"/>
    <line x1="{fmt(cx)}" y1="{fmt(cy)}" x2="{fmt(pos_y[0])}" y2="{fmt(pos_y[1])}" stroke="#182C28" stroke-width="1.6"/>
    <path d="{arrow_triangle(cx, cy, pos_y[0], pos_y[1], 8.0, 3.0)}" fill="#182C28"/>

    <!-- Projection drop lines and angles -->
    <line x1="{fmt(tip[0])}" y1="{fmt(tip[1])}" x2="{fmt(eq_proj[0])}" y2="{fmt(eq_proj[1])}" stroke="#B84A2E" stroke-width="1.15" stroke-dasharray="3 3" opacity="0.78"/>
    <line x1="{fmt(cx)}" y1="{fmt(cy)}" x2="{fmt(eq_proj[0])}" y2="{fmt(eq_proj[1])}" stroke="#1F5A92" stroke-width="1.15" stroke-dasharray="3 3" opacity="0.78"/>
    <path d="{th_arc_d}" fill="none" stroke="#B84A2E" stroke-width="1.4"/>
    <path d="{ph_arc_d}" fill="none" stroke="#1F5A92" stroke-width="1.4"/>

    <!-- State vector |psi> -->
    <line x1="{fmt(cx)}" y1="{fmt(cy)}" x2="{fmt(tip[0])}" y2="{fmt(tip[1])}" stroke="#B84A2E" stroke-width="2.5" stroke-linecap="round"/>
    <path d="{arrow_triangle(cx, cy, tip[0], tip[1], 9.0, 3.6)}" fill="#B84A2E"/>
    <circle class="bloch-tip-halo" cx="{fmt(tip[0])}" cy="{fmt(tip[1])}" r="8.5" fill="#B84A2E" fill-opacity="0.18"/>
    <circle cx="{fmt(tip[0])}" cy="{fmt(tip[1])}" r="4.2" fill="#B84A2E" stroke="#FFFFFF" stroke-width="1.5"/>

    <!-- Benchmark dots & origin -->
    <circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="2.8" fill="#FFFFFF" stroke="#182C28" stroke-width="1.4"/>
    <circle cx="{fmt(p_0[0])}" cy="{fmt(p_0[1])}" r="3.2" fill="#1E6B5A"/>
    <circle cx="{fmt(p_1[0])}" cy="{fmt(p_1[1])}" r="2.8" fill="#FAF8F3" stroke="#1E6B5A" stroke-width="1.5"/>
    <circle cx="{fmt(p_plus[0])}" cy="{fmt(p_plus[1])}" r="3.0" fill="#1F5A92"/>
    <circle cx="{fmt(p_plus_i[0])}" cy="{fmt(p_plus_i[1])}" r="3.0" fill="#1F5A92"/>

    <!-- Clean non-overlapping axis labels -->
    <text x="{fmt(pos_z[0] + 9)}" y="{fmt(pos_z[1] + 4)}" class="mono-bold">|0⟩ (+Z)</text>
    <text x="{fmt(neg_z[0] + 9)}" y="{fmt(neg_z[1] + 5)}" class="mono-muted">|1⟩ (−Z)</text>
    <text x="{fmt(pos_x[0] - 10)}" y="{fmt(pos_x[1] + 15)}" text-anchor="middle" class="mono-bold">|+⟩ (+X)</text>
    <text x="{fmt(pos_y[0] + 10)}" y="{fmt(pos_y[1] + 15)}" text-anchor="middle" class="mono-bold">|+i⟩ (+Y)</text>
    <text x="{fmt(tip[0] + 11)}" y="{fmt(tip[1] - 4)}" class="mono-red">|ψ⟩</text>
    <text x="{fmt(th_arc_pts[11][0] + 2)}" y="{fmt(th_arc_pts[11][1] - 7)}" class="mono-red">θ</text>
    <text x="{fmt(ph_arc_pts[12][0] + 4)}" y="{fmt(ph_arc_pts[12][1] + 13)}" class="mono-accent">φ</text>

    <!-- Right-side compact specification card -->
    <rect x="692" y="302" width="114" height="178" rx="7" fill="#F6F3EB" stroke="#E0DACD" stroke-width="1"/>
    <text x="702" y="322" class="card-sub-head">Larmor 进动</text>
    <text x="702" y="340" class="mono-xs">dr/dt = ω × r</text>
    <line x1="702" y1="350" x2="796" y2="350" stroke="#DDD7CB" stroke-width="1"/>
    <text x="702" y="368" class="mono-red">θ = 52°</text>
    <text x="702" y="385" class="mono-amber">φ(t) = ω₀ t</text>
    <line x1="702" y1="395" x2="796" y2="395" stroke="#DDD7CB" stroke-width="1"/>
    <text x="702" y="413" class="card-sub-head">右手坐标系</text>
    <text x="702" y="430" class="mono-xs">+X × +Y = +Z</text>
    <text x="702" y="449" class="mono-teal">纯态 ‖r‖ = 1</text>
    <text x="702" y="466" class="mono-xs">混态 ‖r‖ &lt; 1</text>
  </g>
"""


def build_surface_code_panel() -> str:
    """Build Panel 03: Rotated d=3 Surface Code [[9,1,3]] lattice with X/Z stabilizers & syndrome."""
    verify_surface_code_d3()
    xs = [876.0, 926.0, 976.0]
    ys = [342.0, 392.0, 442.0]
    step = 50.0

    # Data qubit grid circles (3x3)
    data_svg: list[str] = []
    for r in range(3):
        for c in range(3):
            cx, cy = xs[c], ys[r]
            if r == 1 and c == 1:
                # Center data qubit with X error
                data_svg.append(
                    f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="9.0" fill="#B84A2E" stroke="#FFFFFF" stroke-width="2.0"/>'
                    f'<text x="{fmt(cx)}" y="{fmt(cy + 3.8)}" text-anchor="middle" class="err-q">X</text>'
                )
            else:
                data_svg.append(
                    f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="6.8" fill="#FAF8F3" stroke="#182C28" stroke-width="1.8"/>'
                )

    # Boundary semi-ellipses (radius rx=25, ry=19)
    # Top X boundary: (0,0)-(0,1), curves UP
    top_x_arc = f"M{fmt(xs[0])} {fmt(ys[0])} A25 19 0 0 1 {fmt(xs[1])} {fmt(ys[0])} Z"
    # Bottom X boundary: (2,1)-(2,2), curves DOWN
    bot_x_arc = f"M{fmt(xs[1])} {fmt(ys[2])} A25 19 0 0 0 {fmt(xs[2])} {fmt(ys[2])} Z"
    # Left Z boundary: (1,0)-(2,0), curves LEFT
    left_z_arc = f"M{fmt(xs[0])} {fmt(ys[1])} A19 25 0 0 0 {fmt(xs[0])} {fmt(ys[2])} Z"
    # Right Z boundary: (0,2)-(1,2), curves RIGHT
    right_z_arc = f"M{fmt(xs[2])} {fmt(ys[0])} A19 25 0 0 1 {fmt(xs[2])} {fmt(ys[1])} Z"

    # Triggered Z plaquette centers (TL and BR)
    tl_cx, tl_cy = xs[0] + step / 2.0, ys[0] + step / 2.0
    br_cx, br_cy = xs[1] + step / 2.0, ys[1] + step / 2.0
    tr_cx, tr_cy = xs[1] + step / 2.0, ys[0] + step / 2.0
    bl_cx, bl_cy = xs[0] + step / 2.0, ys[1] + step / 2.0

    return f"""
  <!-- Panel 03: Rotated d=3 Surface Code Lattice -->
  <g id="panel-surface">
    <rect x="830" y="262" width="344" height="232" rx="9" fill="#FFFFFF" stroke="#DDD7CB" stroke-width="1.2"/>
    <text x="846" y="284" class="panel-title">03 · 表面码网格（d = 3 旋转码 [[9,1,3]]）</text>

    <!-- Boundary weight-2 stabilizers -->
    <path d="{top_x_arc}" fill="#D9EFE7" stroke="#1E6B5A" stroke-width="1.3"/>
    <path d="{bot_x_arc}" fill="#D9EFE7" stroke="#1E6B5A" stroke-width="1.3"/>
    <path d="{left_z_arc}" fill="#DCEAF8" stroke="#1F5A92" stroke-width="1.3"/>
    <path d="{right_z_arc}" fill="#DCEAF8" stroke="#1F5A92" stroke-width="1.3"/>

    <!-- Interior weight-4 plaquettes -->
    <!-- TL: Z stabilizer (triggered defect -1) -->
    <rect x="{fmt(xs[0])}" y="{fmt(ys[0])}" width="{fmt(step)}" height="{fmt(step)}" fill="#FBE5DD" stroke="#B84A2E" stroke-width="1.6"/>
    <!-- TR: X stabilizer -->
    <rect x="{fmt(xs[1])}" y="{fmt(ys[0])}" width="{fmt(step)}" height="{fmt(step)}" fill="#D9EFE7" stroke="#1E6B5A" stroke-width="1.3"/>
    <!-- BL: X stabilizer -->
    <rect x="{fmt(xs[0])}" y="{fmt(ys[1])}" width="{fmt(step)}" height="{fmt(step)}" fill="#D9EFE7" stroke="#1E6B5A" stroke-width="1.3"/>
    <!-- BR: Z stabilizer (triggered defect -1) -->
    <rect x="{fmt(xs[1])}" y="{fmt(ys[1])}" width="{fmt(step)}" height="{fmt(step)}" fill="#FBE5DD" stroke="#B84A2E" stroke-width="1.6"/>

    <!-- Syndrome coupling highlight from center X error to both Z defects -->
    <line x1="{fmt(xs[1])}" y1="{fmt(ys[1])}" x2="{fmt(tl_cx)}" y2="{fmt(tl_cy)}" stroke="#B84A2E" stroke-width="1.5" stroke-dasharray="3 2.5"/>
    <line x1="{fmt(xs[1])}" y1="{fmt(ys[1])}" x2="{fmt(br_cx)}" y2="{fmt(br_cy)}" stroke="#B84A2E" stroke-width="1.5" stroke-dasharray="3 2.5"/>

    <!-- Animated pulsing syndrome halos on TL and BR Z-stabilizers -->
    <circle class="syndrome-halo" cx="{fmt(tl_cx)}" cy="{fmt(tl_cy)}" r="15" fill="#B84A2E" fill-opacity="0.16"/>
    <circle class="syndrome-halo" cx="{fmt(br_cx)}" cy="{fmt(br_cy)}" r="15" fill="#B84A2E" fill-opacity="0.16"/>

    <!-- Plaquette labels (crisp pills behind triggered Z-1 defects so dashed lines stay clean) -->
    <rect x="{fmt(tl_cx - 14)}" y="{fmt(tl_cy - 8)}" width="28" height="16" rx="4" fill="#FBE5DD" fill-opacity="0.92"/>
    <rect x="{fmt(br_cx - 14)}" y="{fmt(br_cy - 8)}" width="28" height="16" rx="4" fill="#FBE5DD" fill-opacity="0.92"/>
    <text x="{fmt(tl_cx)}" y="{fmt(tl_cy + 4)}" text-anchor="middle" class="stab-red">Z−1</text>
    <text x="{fmt(br_cx)}" y="{fmt(br_cy + 4)}" text-anchor="middle" class="stab-red">Z−1</text>
    <text x="{fmt(tr_cx)}" y="{fmt(tr_cy + 4)}" text-anchor="middle" class="stab-teal">X</text>
    <text x="{fmt(bl_cx)}" y="{fmt(bl_cy + 4)}" text-anchor="middle" class="stab-teal">X</text>
    <text x="{fmt(tl_cx)}" y="{fmt(ys[0] - 5)}" text-anchor="middle" class="stab-mini-teal">X</text>
    <text x="{fmt(br_cx)}" y="{fmt(ys[2] + 13)}" text-anchor="middle" class="stab-mini-teal">X</text>
    <text x="{fmt(xs[0] - 9)}" y="{fmt(bl_cy + 3.5)}" text-anchor="middle" class="stab-mini-blue">Z</text>
    <text x="{fmt(xs[2] + 9)}" y="{fmt(tr_cy + 3.5)}" text-anchor="middle" class="stab-mini-blue">Z</text>

    <!-- Logical Z-bar chain across top row (0,0)-(0,1)-(0,2) -->
    <line x1="{fmt(xs[0])}" y1="{fmt(ys[0])}" x2="{fmt(xs[2])}" y2="{fmt(ys[0])}" stroke="#C28524" stroke-width="2.8" stroke-dasharray="6 3.5"/>
    <text x="{fmt(xs[2] + 14)}" y="{fmt(ys[0] - 6)}" class="mono-amber">Z̄</text>

    <!-- 9 data qubits -->
    {''.join(data_svg)}

    <!-- Right-side compact legend card -->
    <rect x="1030" y="302" width="132" height="178" rx="7" fill="#F6F3EB" stroke="#E0DACD" stroke-width="1"/>
    <text x="1042" y="322" class="card-sub-head">稳定子与解码</text>

    <circle cx="1048" cy="342" r="5.0" fill="#FAF8F3" stroke="#182C28" stroke-width="1.5"/>
    <text x="1060" y="346" class="legend-txt">数据比特 (9)</text>

    <rect x="1043" y="359" width="10" height="10" rx="2" fill="#D9EFE7" stroke="#1E6B5A" stroke-width="1.2"/>
    <text x="1060" y="368" class="legend-txt">X 稳定子 (4)</text>

    <rect x="1043" y="381" width="10" height="10" rx="2" fill="#DCEAF8" stroke="#1F5A92" stroke-width="1.2"/>
    <text x="1060" y="390" class="legend-txt">Z 稳定子 (4)</text>

    <circle cx="1048" cy="408" r="5.2" fill="#B84A2E"/>
    <text x="1060" y="412" class="legend-txt">X 错 → 成对症状</text>

    <line x1="1042" y1="430" x2="1055" y2="430" stroke="#C28524" stroke-width="2.5" stroke-dasharray="4 2"/>
    <text x="1060" y="434" class="legend-txt">逻辑算符 Z̄</text>

    <line x1="1042" y1="448" x2="1150" y2="448" stroke="#DDD7CB" stroke-width="1"/>
    <text x="1042" y="466" class="mono-xs">码距 d=3 · 纠单错</text>
  </g>
"""


def render_svg(*, animated: bool) -> str:
    """Render complete cover banner SVG string (animated or pure static)."""
    base_css = """
    text { font-family: system-ui, -apple-system, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; }
    .eyebrow { font-size: 11.2px; font-weight: 700; fill: #154C40; letter-spacing: 0.4px; }
    .hero-main { font-size: 40px; font-weight: 800; fill: #142622; letter-spacing: -0.6px; }
    .hero-sub { font-size: 26.5px; font-weight: 700; fill: #1E6B5A; letter-spacing: -0.3px; }
    .deck { font-size: 13px; font-weight: 450; fill: #3E524D; }
    .stat-num { font-size: 20px; font-weight: 800; fill: #142622; }
    .stat-num-sm { font-size: 17.5px; font-weight: 800; fill: #142622; }
    .stat-sub { font-size: 11.2px; font-weight: 450; fill: #556661; }
    .dark-num { font-size: 18.5px; font-weight: 800; fill: #F8F5EE; }
    .dark-sub { font-size: 11.2px; font-weight: 450; fill: #C2D6CF; }
    .dark-pill { font-size: 10.6px; font-weight: 600; fill: #D7EBE4; }
    .foot-head { font-size: 11px; font-weight: 700; fill: #4E5E59; }
    .foot-mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 11px; font-weight: 600; fill: #1D342F; }
    .pipe-blue { font-size: 12px; font-weight: 700; fill: #1F5A92; }
    .pipe-teal { font-size: 12px; font-weight: 700; fill: #1E6B5A; }
    .pipe-red { font-size: 12px; font-weight: 700; fill: #B84A2E; }
    .pipe-arrow { font-size: 11.5px; font-weight: 600; fill: #8A8275; }
    .panel-title { font-size: 12.2px; font-weight: 700; fill: #182C28; }
    .mono-accent { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 10.8px; font-weight: 700; fill: #1F5A92; }
    .mono-teal { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 10.5px; font-weight: 700; fill: #1E6B5A; }
    .mono-red { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 10.5px; font-weight: 700; fill: #B84A2E; }
    .mono-amber { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 10.8px; font-weight: 700; fill: #9F6510; }
    .mono-bold { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 10.5px; font-weight: 700; fill: #182C28; }
    .mono-muted { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 10.2px; font-weight: 600; fill: #5E6E6A; }
    .mono-xs { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 10px; font-weight: 600; fill: #5A645F; }
    .badge-light { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 11.5px; font-weight: 700; fill: #FAF8F3; }
    .gate-mini { font-family: Georgia, 'Times New Roman', serif; font-size: 14px; font-weight: 700; fill: #1F5A92; }
    .det-lbl-teal { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 11px; font-weight: 800; fill: #154C40; }
    .det-lbl-red { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 11px; font-weight: 800; fill: #98361E; }
    .card-sub-head { font-size: 11.2px; font-weight: 700; fill: #182C28; }
    .stab-red { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 10.5px; font-weight: 800; fill: #9E341B; }
    .stab-teal { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 12px; font-weight: 800; fill: #155344; }
    .stab-mini-teal { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 9.5px; font-weight: 800; fill: #155344; }
    .stab-mini-blue { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 9.5px; font-weight: 800; fill: #174979; }
    .err-q { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 10.5px; font-weight: 800; fill: #FFFFFF; }
    .legend-txt { font-size: 10.5px; font-weight: 500; fill: #2B3C38; }
"""
    anim_css = """
    @media (prefers-reduced-motion: no-preference) {
      .mzi-flow-upper { animation: mziFlow 2.6s linear infinite; }
      .mzi-flow-lower { animation: mziFlow 2.6s linear infinite; animation-delay: -0.45s; }
      .bloch-orbit-flow { animation: orbitFlow 3.4s linear infinite; }
      .bloch-tip-halo { animation: pulseHalo 2.4s ease-in-out infinite; }
      .syndrome-halo { animation: pulseSyndrome 2.4s ease-in-out infinite; }
      .mzi-pulse-dot { animation: pulseDot 2.4s ease-in-out infinite; }
      @keyframes mziFlow { from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; } }
      @keyframes orbitFlow { from { stroke-dashoffset: 21; } to { stroke-dashoffset: 0; } }
      @keyframes pulseHalo { 0%, 100% { fill-opacity: 0.14; } 50% { fill-opacity: 0.36; } }
      @keyframes pulseSyndrome { 0%, 100% { fill-opacity: 0.10; } 50% { fill-opacity: 0.32; } }
      @keyframes pulseDot { 0%, 100% { opacity: 0.85; } 50% { opacity: 1; } }
    }
""" if animated else ""

    title_txt = "量子计算：从直觉到研究入口 — 主视觉原理图"
    desc_txt = (
        "封面左侧展示书名、章节、公式、矢量图、"
        "题答和离线验算入口。右侧三幅原理图依次呈现 Mach–Zehnder 干涉波包、"
        "右手三维 Bloch 球 Larmor 进动与 d=3 旋转表面码 [[9,1,3]] 稳定子解码网格。"
    )

    mzi_svg = build_mzi_panel()
    bloch_svg = build_bloch_panel()
    surface_svg = build_surface_code_panel()

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="cover-title cover-desc">
  <title id="cover-title">{escape(title_txt)}</title>
  <desc id="cover-desc">{escape(desc_txt)}</desc>
  <defs>
    <pattern id="drafting-dots" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#8D8577" opacity="0.22"/>
    </pattern>
    <radialGradient id="bloch-fill" cx="38%" cy="32%" r="65%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="55%" stop-color="#E4F4F7" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#C8E6EC" stop-opacity="0.58"/>
    </radialGradient>
  </defs>
  <style>{base_css}{anim_css}  </style>

  <!-- Warm Archival Drafting Workbench Plate -->
  <rect x="1" y="1" width="1198" height="518" rx="14" fill="#FAF8F3" stroke="#D3CDC0" stroke-width="1.6"/>
  <rect x="2" y="2" width="1196" height="516" rx="13" fill="url(#drafting-dots)"/>

  <!-- Top drafting hairline accent -->
  <rect x="26" y="12" width="428" height="3" rx="1.5" fill="#1E6B5A"/>
  <rect x="474" y="12" width="344" height="3" rx="1.5" fill="#1F5A92"/>
  <rect x="830" y="12" width="344" height="3" rx="1.5" fill="#C28524"/>

  <!-- Left Column: Title, Deck, and 5 Scale Metric Cards -->
  <g id="left-identity">
    <!-- Eyebrow Pill -->
    <rect x="26" y="26" width="284" height="26" rx="13" fill="#E5F2ED" stroke="#B6D5C9" stroke-width="1"/>
    <circle cx="40" cy="39" r="3.8" fill="#1E6B5A"/>
    <text x="51" y="43" class="eyebrow">QUANTUM COMPUTING · 系统教材与实验台</text>

    <!-- Title & Subtitle -->
    <text x="26" y="96" class="hero-main">量子计算</text>
    <text x="26" y="135" class="hero-sub">从直觉到研究入口</text>

    <!-- Three-tone drafting rule -->
    <rect x="26" y="149" width="88" height="3.5" rx="1.75" fill="#1E6B5A"/>
    <rect x="120" y="149" width="28" height="3.5" rx="1.75" fill="#C28524"/>
    <rect x="154" y="149" width="16" height="3.5" rx="1.75" fill="#B84A2E"/>

    <!-- Deck -->
    <text x="26" y="176" class="deck">从草稿纸能算透的二维小例出发，打通线性代数、</text>
    <text x="26" y="197" class="deck">量子干涉、核心算法、噪声信道与表面码容错全链路。</text>

    <!-- Scale Card 1: 26 章 -->
    <rect x="26" y="216" width="208" height="64" rx="8" fill="#FFFFFF" stroke="#DDD7CB" stroke-width="1.2"/>
    <rect x="28" y="224" width="3.8" height="48" rx="1.9" fill="#1E6B5A"/>
    <text x="42" y="246" class="stat-num">26 章</text>
    <text x="42" y="267" class="stat-sub">主篇 00–21 + 量子力学 Q1–Q4</text>

    <!-- Scale Card 2: 公式与推导 -->
    <rect x="246" y="216" width="208" height="64" rx="8" fill="#FFFFFF" stroke="#DDD7CB" stroke-width="1.2"/>
    <rect x="248" y="224" width="3.8" height="48" rx="1.9" fill="#1F5A92"/>
    <text x="262" y="246" class="stat-num">公式与推导</text>
    <text x="262" y="267" class="stat-sub">本地 KaTeX 预渲染 · 逐步演算</text>

    <!-- Scale Card 3: 科学矢量图 -->
    <rect x="26" y="290" width="208" height="64" rx="8" fill="#FFFFFF" stroke="#DDD7CB" stroke-width="1.2"/>
    <rect x="28" y="298" width="3.8" height="48" rx="1.9" fill="#C28524"/>
    <text x="42" y="320" class="stat-num">科学矢量图</text>
    <text x="42" y="341" class="stat-sub">公式驱动 SVG + 架构流程图</text>

    <!-- Scale Card 4: 271 题零跳步题答 -->
    <rect x="246" y="290" width="208" height="64" rx="8" fill="#FFFFFF" stroke="#DDD7CB" stroke-width="1.2"/>
    <rect x="248" y="298" width="3.8" height="48" rx="1.9" fill="#B84A2E"/>
    <text x="262" y="319" class="stat-num-sm">271 题零跳步题答</text>
    <text x="262" y="341" class="stat-sub">逐行矩阵展开与归一独立回验</text>

    <!-- Scale Card 5 (Full-Width Dark Anchor): 离线复算 -->
    <rect x="26" y="364" width="428" height="66" rx="8" fill="#1B2D2A" stroke="#2D4944" stroke-width="1.2"/>
    <rect x="28" y="372" width="4" height="50" rx="2" fill="#DDA03B"/>
    <text x="44" y="394" class="dark-num">离线复算</text>
    <rect x="224" y="376" width="216" height="22" rx="11" fill="#27403B" stroke="#3D615B" stroke-width="1"/>
    <text x="332" y="391" text-anchor="middle" class="dark-pill">纯标准库 · 零云依赖 · 6 模块实验台</text>
    <text x="44" y="417" class="dark-sub">纸笔手算 → 离线复算 → 开源项目对照</text>

    <!-- Bottom Contract Strip -->
    <rect x="26" y="440" width="428" height="54" rx="8" fill="#F1EDE4" stroke="#DDD7CB" stroke-width="1.1"/>
    <text x="40" y="460" class="foot-head">全书统一数学与物理契约</text>
    <text x="40" y="481" class="foot-mono">左共轭 ⟨u|v⟩ · 大端序 |q₁q₀⟩ · 根保真度 F(ρ,σ) · log₂/ln</text>
  </g>

  <!-- Right Workbench Header Bar -->
  <g id="right-header">
    <rect x="474" y="26" width="700" height="34" rx="7" fill="#F1EDE4" stroke="#DDD7CB" stroke-width="1.1"/>
    <text x="492" y="47" class="pipe-blue">01 · MZI 相位干涉波包</text>
    <text x="646" y="47" class="pipe-arrow">──▶</text>
    <text x="684" y="47" class="pipe-teal">02 · Bloch 球进动 |ψ(θ,φ)⟩</text>
    <text x="874" y="47" class="pipe-arrow">──▶</text>
    <text x="912" y="47" class="pipe-red">03 · 表面码网格 [[9,1,3]]</text>
  </g>
{mzi_svg}{bloch_svg}{surface_svg}</svg>
"""
    return svg


def validate_outputs(anim_svg: str, static_svg: str) -> None:
    """Validate XML structure and static-track zero-animation invariant."""
    ET.fromstring(anim_svg)
    ET.fromstring(static_svg)
    assert "prefers-reduced-motion: no-preference" in anim_svg
    assert "@keyframes" in anim_svg
    for forbidden in ("@keyframes", "animation:", "<animate", "<set "):
        assert forbidden not in static_svg, f"Static SVG must not contain {forbidden!r}"
    for svg in (anim_svg, static_svg):
        labels = {node.text for node in ET.fromstring(svg).iter("{http://www.w3.org/2000/svg}text")}
        for token in ("26 章", "公式与推导", "科学矢量图", "271 题零跳步题答", "离线复算"):
            assert token in labels, f"Missing cover label {token!r}"
    # Ensure no external http(s) URLs in href/src/url()
    for svg in (anim_svg, static_svg):
        urls = re.findall(r"https?://[^\s\"'<>)]+", svg)
        non_ns = [u for u in urls if u != "http://www.w3.org/2000/svg"]
        assert not non_ns, f"External URLs forbidden in offline SVG: {non_ns}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify generated files match disk byte-for-byte.")
    args = parser.parse_args()

    anim_svg = render_svg(animated=True)
    static_svg = render_svg(animated=False)
    validate_outputs(anim_svg, static_svg)

    outputs = {
        ASSETS_DIR / "cover-banner.svg": anim_svg.encode("utf-8"),
        ASSETS_DIR / "cover-banner-static.svg": static_svg.encode("utf-8"),
    }

    if args.check:
        for path, expected in outputs.items():
            if not path.exists() or path.read_bytes() != expected:
                raise SystemExit(f"Out of date or missing: {path}")
        print("OK: cover-banner.svg and cover-banner-static.svg match generator output.")
        return

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    for path, data in outputs.items():
        path.write_bytes(data)
        print(f"Wrote {path.relative_to(ROOT)} ({len(data):,} bytes)")


if __name__ == "__main__":
    main()
