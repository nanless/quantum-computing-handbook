#!/usr/bin/env python3
"""Unified entry point for generating all V4 scientific SVG figures.

Invokes part1 (codes/foundations/generate_v4_figures_part1.py) and
part2 (codes/foundations/generate_v4_figures_part2.py) sequentially using
Python 3 standard library only, then validates every generated SVG as well-formed
XML containing live <text> nodes.

Run:
  python3 codes/foundations/generate_v4_figures.py
"""

from __future__ import annotations

import runpy
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ASSETS_DIR = ROOT / "handbook" / "assets"

PART1_SCRIPT = HERE / "generate_v4_figures_part1.py"
PART2_SCRIPT = HERE / "generate_v4_figures_part2.py"

SVG_NS = "{http://www.w3.org/2000/svg}"


def run_part(script_path: Path, required: bool = True) -> bool:
    if not script_path.exists():
        if required:
            raise FileNotFoundError(f"Missing required generator script: {script_path.name}")
        print(f"[WARN] Optional part script not found yet: {script_path.name} (skipping)")
        return False
    print(f"[RUN] {script_path.name}")
    try:
        runpy.run_path(str(script_path), run_name="__main__")
    except SystemExit as exc:
        if exc.code not in (None, 0):
            raise
    return True


def verify_v4_svgs() -> list[Path]:
    svgs = sorted(ASSETS_DIR.glob("v4-*.svg"))
    if not svgs:
        raise RuntimeError("No v4-*.svg files found in handbook/assets/")
    for svg_path in svgs:
        root = ET.parse(svg_path).getroot()
        texts = root.findall(f".//{SVG_NS}text")
        if not texts:
            raise RuntimeError(f"{svg_path.name} has zero <text> nodes")
    return svgs


def main() -> int:
    ran_p1 = run_part(PART1_SCRIPT, required=False)
    ran_p2 = run_part(PART2_SCRIPT, required=True)
    svgs = verify_v4_svgs()
    print(
        f"[OK] Verified {len(svgs)} V4 SVG figures "
        f"(part1={'ran' if ran_p1 else 'pending'}, part2={'ran' if ran_p2 else 'skipped'}):"
    )
    for p in svgs:
        print(f"  - {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
