#!/usr/bin/env python3
"""Formula-generated Q1 quantum eraser figure; synthetic ideal probabilities."""
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'handbook/assets/round71-foundations-eraser.svg'
x0,y0,width,height=85,68,755,252


def point(phi,p):
    return x0+width*phi/(2*math.pi), y0+height*(1-p)


def curve(sign):
    pts=[point(2*math.pi*j/128,(1+sign*math.cos(2*math.pi*j/128))/2)
         for j in range(129)]
    return ' '.join(('M' if j==0 else 'L')+f'{x:.3f},{y:.3f}'
                    for j,(x,y) in enumerate(pts))


parts=['''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="445" viewBox="0 0 900 445" role="img" aria-labelledby="title desc">
<title id="title">Two opposite conditional fringes average to a flat marginal</title>
<desc id="desc">Ideal balanced two-path quantum eraser. Solid square-marked plus group and dashed circle-marked minus group have opposite cosine fringes. Their equal-weight average remains one half at every phase. Synthetic formula curves, not experimental data.</desc>
<rect width="900" height="445" fill="#fff"/>
<g font-family="Arial, sans-serif" font-size="15" fill="#202938">
<text x="85" y="29" font-size="21" font-weight="bold">Conditional fringes cancel in the full sample</text>
<text x="85" y="51" font-size="13">Ideal model: balanced paths, orthogonal accessible records, record measured in the +/- basis</text>''']
for p in (0,.25,.5,.75,1):
    _,y=point(0,p)
    parts.append(f'<path d="M85,{y} H840" stroke="#dce2e9"/><text x="69" y="{y+5}" text-anchor="end">{p:g}</text>')
for j,label in enumerate(('0','π/2','π','3π/2','2π')):
    x,_=point(j*math.pi/2,0)
    parts.append(f'<path d="M{x},68 V320" stroke="#edf0f5"/><text x="{x}" y="343" text-anchor="middle">{label}</text>')
parts.extend([
    '<path d="M85,68 V320 H840" fill="none" stroke="#202938" stroke-width="1.5"/>',
    '<text x="462" y="368" text-anchor="middle">Phase difference φ (rad)</text>',
    '<text transform="translate(24,194) rotate(-90)" text-anchor="middle">Probability of detector 0</text>',
    f'<path d="{curve(1)}" fill="none" stroke="#165a9f" stroke-width="2.6"/>',
    f'<path d="{curve(-1)}" fill="none" stroke="#a14a12" stroke-width="2.6" stroke-dasharray="9 6"/>',
    '<path d="M85,194 H840" fill="none" stroke="#333" stroke-width="2.2" stroke-dasharray="2 6"/>'])
for j in range(5):
    phi=j*math.pi/2
    x,y=point(phi,(1+math.cos(phi))/2)
    parts.append(f'<rect x="{x-4}" y="{y-4}" width="8" height="8" fill="#165a9f" stroke="#fff"/>')
    x,y=point(phi,(1-math.cos(phi))/2)
    parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#fff" stroke="#a14a12" stroke-width="2"/>')
parts.extend(['''<path d="M85,396 H124" stroke="#165a9f" stroke-width="3"/><rect x="100" y="392" width="8" height="8" fill="#165a9f"/>
<text x="133" y="401">P(0 | +)</text>
<path d="M320,396 H359" stroke="#a14a12" stroke-width="3" stroke-dasharray="9 6"/><circle cx="339" cy="396" r="4" fill="#fff" stroke="#a14a12" stroke-width="2"/>
<text x="368" y="401">P(0 | -)</text>
<path d="M558,396 H597" stroke="#333" stroke-width="2.2" stroke-dasharray="2 6"/>
<text x="606" y="401">P(0) = 1/2</text>
<text x="85" y="429" font-size="13">Each record group has probability 1/2. Matching record labels is required to see conditional fringes.</text>
</g></svg>'''])
DEST.write_text('\n'.join(parts)+'\n',encoding='utf-8')
print(DEST)
