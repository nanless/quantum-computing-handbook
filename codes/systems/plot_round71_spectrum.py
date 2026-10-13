"""Generate original SVG from the S71-Q3 weak rectangular-drive formula.

Standard library only. Run from any directory:
  python3 codes/systems/plot_round71_spectrum.py
This is a synthetic isolated-transition plot, not a hardware spectrum.
"""
from html import escape
from pathlib import Path
import math


def probability(ns):
    x = math.pi * .2 * ns  # delta_f=0.2/ns; fixed area 0.1 rad
    sinc = math.sin(x)/x if x else 1.
    return .0025*sinc*sinc


def main():
    width, height = 960, 620
    x0, x1, y0, y1 = 105, 900, 135, 465
    to_x = lambda ns: x0+(x1-x0)*ns/15
    to_y = lambda p: y1-(y1-y0)*p/.0025
    elements = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                '<title id="title">矩形弱脉冲谱零点与时长</title>',
                '<desc id="desc">固定脉冲面积0.1rad，失谐200MHz。一阶跃迁概率随时长振荡，在5、10、15ns为零；完整高阶演化不保证零泄漏。</desc>',
                '<rect width="960" height="620" fill="#fff"/>',
                '<g font-family="Arial, PingFang SC, sans-serif" fill="#172c42">']
    def label(x, y, content, size=20, anchor='middle'):
        elements.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{escape(content)}</text>')
    label(480, 45, '矩形脉冲的频谱相消：零点依赖时长与失谐', 28)
    label(480, 82, '合成两态弱驱动；固定面积 0.1 rad；失谐 δf = 200 MHz', 20)
    for p in [.0, .0005, .001, .0015, .002, .0025]:
        y = to_y(p)
        elements.append(f'<path d="M{x0},{y} H{x1}" stroke="#e0e6ee"/>')
        label(x0-12, y+6, f'{p:.4f}', 18, 'end')
    for ns in range(0, 16, 5):
        x = to_x(ns)
        elements.append(f'<path d="M{x},{y0} V{y1}" stroke="#b6c2d1" stroke-dasharray="6 5"/>')
        label(x, y1+30, str(ns), 19)
    elements.append(f'<path d="M{x0},{y0} V{y1} H{x1}" fill="none" stroke="#172c42" stroke-width="2"/>')
    points = ' '.join(f'{to_x(i*15/1200):.3f},{to_y(probability(i*15/1200)):.3f}' for i in range(1201))
    elements.append(f'<polyline points="{points}" fill="none" stroke="#135d8c" stroke-width="3"/>')
    for ns in [2.5, 5, 10]:
        elements.append(f'<circle cx="{to_x(ns)}" cy="{to_y(probability(ns))}" r="6" fill="#fff" stroke="#172c42" stroke-width="2"/>')
    label(520, 530, '脉冲时长 τ（ns）', 21)
    elements.append('<text transform="translate(27,300) rotate(-90)" font-size="20" text-anchor="middle">一阶跃迁概率（无量纲）</text>')
    label(520, 566, 'P⁽¹⁾ = (0.1 / 2)² sinc²(π δf τ)；sinc(x) = sin(x) / x', 20)
    label(520, 602, '谱零点是此包络的一阶相消；不保证真实三能级门零泄漏。', 19)
    elements.extend(['</g>', '</svg>'])
    root = Path(__file__).resolve().parents[2]
    target = root/'handbook/assets/round71-systems-spectrum.svg'
    target.write_text('\n'.join(elements), encoding='utf-8')
    assert probability(5) < 1e-30 and probability(0) == .0025
    print(target)


if __name__ == '__main__':
    main()
