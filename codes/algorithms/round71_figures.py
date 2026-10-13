#!/usr/bin/env python3
"""Rebuild the exact stationary rectangular-barrier plot; standard library only."""
from pathlib import Path
import math
from round71_checks import transmission, barrier_matching, close

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'handbook/assets/round71-barrier-transmission.svg'
W,H=1040,610
left,right,top,bottom=92,982,97,486
xlo,xhi=.05,4

def xx(e): return left+(e-xlo)/(xhi-xlo)*(right-left)
def yy(t): return bottom-t*(bottom-top)
def txt(x,y,text,size=18,anchor='start',fill='#223347'):
    return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}">{text}</text>'

parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
       '<title id="title">Rectangular barrier: continuous top and interference resonances</title>',
       '<desc id="desc">Transmission at width parameter g=4 approaches 0.2 continuously at E/V0=1. Above the barrier, two resonances at 1.61685 and 3.46740 reach probability one. Equal masses and external potentials, stationary single-particle model.</desc>',
       '<rect width="1040" height="610" fill="#f8fafc"/>',
       '<g font-family="Arial,Helvetica,sans-serif">',
       txt(left,37,'Rectangular barrier: the top is continuous',25),
       txt(left,66,'g = 4  |  equal masses and outer potentials  |  formula-derived, no measured data',16,fill='#59697c')]
for p in (0,.2,.4,.6,.8,1):
    y=yy(p)
    parts+=[f'<path d="M {left} {y} H {right}" stroke="#dce3eb"/>',txt(left-16,y+6,f'{p:.1f}',16,'end')]
for e in (.5,1,1.5,2,2.5,3,3.5,4):
    x=xx(e)
    parts+=[f'<path d="M {x} {top} V {bottom}" stroke="#edf0f4"/>',txt(x,bottom+31,f'{e:g}',16,'middle')]
parts.append(f'<path d="M {left} {top} V {bottom} H {right}" fill="none" stroke="#36475a" stroke-width="1.8"/>')
pts=[]
for k in range(1801):
    e=xlo+(xhi-xlo)*k/1800
    t=transmission(e,4)
    if k%100==0:
        matched,refl=barrier_matching(e,4)
        close(t,matched);close(matched+refl,1)
    pts.append(f'{xx(e):.3f},{yy(t):.3f}')
parts.append('<polyline points="'+' '.join(pts)+'" fill="none" stroke="#005e8f" stroke-width="3"/>')
parts+=[f'<path d="M {xx(1)} {top} V {bottom}" stroke="#545f70" stroke-width="1.6" stroke-dasharray="6 5"/>',
        f'<circle cx="{xx(1)}" cy="{yy(.2)}" r="6" fill="#f8fafc" stroke="#005e8f" stroke-width="2.5"/>',
        txt(xx(1)+15,yy(.2)+30,'Barrier top: T = 1/5',17)]
for l in (1,2):
    e=1+(l*math.pi/4)**2
    x,y=xx(e),yy(1)
    parts.append(f'<rect x="{x-5}" y="{y-5}" width="10" height="10" fill="#f8fafc" stroke="#005e8f" stroke-width="2.5"/>')
    # Put resonance annotations below their markers, away from the header.
    parts+=[f'<path d="M {x} {y+8} v {17 if l==1 else 46}" stroke="#59697c"/>',
            txt(x+12 if l==1 else x-12,y+(47 if l==1 else 76),
                f'Resonance {l}: E/V0 = {e:.5f}',16,'start' if l==1 else 'end')]
parts += [txt((left+right)/2,565,'Energy ratio E / V0 (dimensionless)',19,'middle'),
          '<text transform="translate(28 294) rotate(-90)" font-size="19" text-anchor="middle" fill="#223347">Transmission T (probability-current ratio)</text>',
          txt(left,596,'Below top: evanescent region. Above top: oscillating internal wave and boundary interference.',15,fill='#59697c'),
          '</g></svg>']
OUT.write_text('\n'.join(parts)+'\n')
print(OUT)
