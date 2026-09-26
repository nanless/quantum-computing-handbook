#!/usr/bin/env python3
"""Generate the r_z=0 Bloch-disk diagram from the diagnostic 02 fixed counts.
Pure standard library; writes only the owned handbook/assets SVG.
"""
import math
from pathlib import Path
from diagnostic_lab import case02


def main():
    data = case02()
    cx, cy, scale = 280, 272, 174
    def point(x, y):
        return cx+scale*x, cy-scale*y
    px, py = point(*data['bloch'][:2])
    qx, qy = point(*data['euclidean_projected_bloch'][:2])
    parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="940" height="535" viewBox="0 0 940 535" role="img" aria-labelledby="title desc">
<title id="title">Finite counts can put a linear state estimate outside the Bloch ball</title>
<desc id="desc">The r z equals zero section is a unit disk. Counts 9/1 for X, 9/1 for Y, 5/5 for Z give the raw point (0.8,0.8), outside the disk. Euclidean projection gives (0.7071,0.7071) on the boundary, but adds no measurement evidence.</desc>
<rect width="940" height="535" fill="#f7f9fc"/>
<g font-family="Arial, sans-serif" fill="#152842">
<text x="32" y="39" font-size="23" font-weight="700">Finite counts do not automatically yield a physical state</text>
<text x="32" y="66" font-size="15">r_z = 0 slice · dimensionless Bloch coordinates · fixed synthetic counts</text>
<rect x="30" y="89" width="480" height="398" rx="14" fill="white" stroke="#ccd8e8"/>
''']
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{scale}" fill="#e8f1fa" stroke="#386b9c" stroke-width="2"/>')
    parts.append(f'<path d="M {cx-scale-25} {cy} H {cx+scale+25} M {cx} {cy+scale+18} V {cy-scale-18}" stroke="#52657a" stroke-width="1.4"/>')
    for value in [-1, -.5, .5, 1]:
        x,y=point(value,0)
        parts.append(f'<path d="M {x} {cy-4} V {cy+4}" stroke="#52657a"/><text x="{x}" y="{cy+21}" font-size="12" text-anchor="middle">{value:g}</text>')
    parts.append('<text x="474" y="259" font-size="15">r_x</text><text x="291" y="109" font-size="15">r_y</text><text x="288" y="290" font-size="12">0</text>')
    parts.append(f'<path d="M {cx} {cy} L {px} {py}" stroke="#b34131" stroke-width="2" stroke-dasharray="6 4"/>')
    parts.append(f'<path d="M {cx} {cy} L {qx} {qy}" stroke="#176653" stroke-width="3"/>')
    parts.append(f'<rect x="{px-5}" y="{py-5}" width="10" height="10" fill="#b34131"/>')
    parts.append(f'<circle cx="{qx}" cy="{qy}" r="5" fill="white" stroke="#176653" stroke-width="3"/>')
    parts.append(f'<path d="M {px+9} {py} H 470 V 121" fill="none" stroke="#b34131"/><text x="390" y="116" fill="#b34131" font-size="13">Raw (0.8, 0.8)</text>')
    parts.append(f'<path d="M {qx-9} {qy} H 322 V 144" fill="none" stroke="#176653"/><text x="308" y="136" text-anchor="end" fill="#176653" font-size="13">Projected (0.7071, 0.7071)</text>')
    parts.append('''<text x="122" y="419" font-size="15" fill="#386b9c">Physical disk: r_x² + r_y² ≤ 1</text>
<g transform="translate(540 108)">
<text y="4" font-size="18" font-weight="700">1. Preserve the raw counts</text>
<text y="35" font-size="16">X: 9 plus, 1 minus</text><text y="61" font-size="16">Y: 9 plus, 1 minus</text><text y="87" font-size="16">Z: 5 plus, 5 minus</text>
<text y="134" font-size="18" font-weight="700">2. Check the entire matrix</text>
<text y="165" font-size="16">Raw radius = 1.13137 &gt; 1</text><text y="192" font-size="16">Eigenvalues: -0.06569, 1.06569</text>
<text y="240" font-size="18" font-weight="700">3. Name the correction method</text>
<text y="272" font-size="16">Euclidean projection → radius 1</text><text y="299" font-size="16">Eigenvalues after projection: 0, 1</text>
<text y="337" font-size="14" fill="#52657a">Correction adds no new observations.</text>
<text y="359" font-size="14" fill="#52657a">It is not a confidence interval.</text>
</g><text x="32" y="517" font-size="13" fill="#52657a">Generated from diagnostic_lab.py case 02. Each measurement basis uses a separate batch of 10 shots.</text>
</g></svg>''')
    dest=Path(__file__).resolve().parents[2]/'handbook/assets/round70-foundations-tomography.svg'
    dest.write_text('\n'.join(parts)+'\n',encoding='utf-8')
    print(dest)


if __name__ == '__main__':
    main()
