/* Module 03: Ramsey Detuning, Decoherence Steady-State (P0 -> 0.5) & Classical Fisher Information F_C */
(function (global) {
  'use strict';

  const M = global.QuantumLabModel;
  const Mods = (global.QuantumLabModules = global.QuantumLabModules || {});

  Mods.initRamsey = function initRamsey(ctx) {
    const { byId, f2, f4 } = ctx;
    let ramseyFdet = 1.0;
    let ramseyT2 = 1.5;
    let ramseyMap = 'correct';
    let ramseyCursorT = 1.5;

    // Plot geometry with safe top clearance (gy1=58, ymax=1.14) so playhead badge & curves NEVER collide
    const GX0 = 56, GX1 = 616, GY0 = 246, GY1 = 58, DUR = 4.0;
    const xOf = t => GX0 + (Math.max(0, Math.min(DUR, t)) / DUR) * (GX1 - GX0);
    const yOf = prob => GY0 - (prob / 1.14) * (GY0 - GY1);

    function formatFisherTag(pt) {
      const v2 = pt.vis * pt.vis;
      if (pt.t <= 1e-9) return `${f4(pt.fisherC)} (V=1 理想态)`;
      if (pt.fisherC < 0.02 * Math.max(0.05, v2)) return `${f4(pt.fisherC)} (峰谷盲点)`;
      if (pt.fisherC >= 0.92 * v2) return `${f4(pt.fisherC)} (近最大灵敏度 V²=${f4(v2)})`;
      return `${f4(pt.fisherC)} (上限 V²=${f4(v2)})`;
    }

    function updatePlayheadOnly() {
      const curX = xOf(ramseyCursorT);
      const pt = M.ramseyPoint(ramseyCursorT, ramseyFdet, ramseyT2);
      const isPitfall = ramseyMap === 'pitfall';
      const curY = yOf(isPitfall ? pt.pWrong : pt.pDecay);

      const line = byId('ramsey-playhead');
      const dot = byId('ramsey-playhead-dot');
      const box = byId('ramsey-playhead-box');
      const txt = byId('ramsey-playhead-txt');
      if (line) {
        line.setAttribute('x1', curX.toFixed(1));
        line.setAttribute('x2', curX.toFixed(1));
      }
      if (dot) {
        dot.setAttribute('cx', curX.toFixed(1));
        dot.setAttribute('cy', curY.toFixed(1));
      }
      const boxX = Math.min(GX1 - 74, Math.max(GX0 + 2, curX - 35));
      if (box) box.setAttribute('x', boxX.toFixed(1));
      if (txt) {
        txt.setAttribute('x', (boxX + 36).toFixed(1));
        txt.textContent = `t = ${f2(ramseyCursorT)}s`;
      }

      byId('ramsey-t-val').textContent = `${f2(ramseyCursorT)} s`;
      byId('ramsey-v-val').textContent = f4(pt.vis);
      byId('ramsey-p0-val').textContent = `${f4(pt.pDecay)} vs ${f4(pt.pWrong)}`;
      byId('ramsey-fc-val').textContent = formatFisherTag(pt);
    }

    function renderRamseySvg() {
      const ptsIdeal = [], ptsDecay = [], ptsWrong = [];
      const N = 240;
      for (let i = 0; i <= N; i++) {
        const t = (DUR * i) / N;
        const pt = M.ramseyPoint(t, ramseyFdet, ramseyT2);
        const x = xOf(t).toFixed(1);
        const cmd = i === 0 ? 'M' : 'L';
        ptsIdeal.push(`${cmd}${x} ${yOf(pt.pIdeal).toFixed(1)}`);
        ptsDecay.push(`${cmd}${x} ${yOf(pt.pDecay).toFixed(1)}`);
        ptsWrong.push(`${cmd}${x} ${yOf(pt.pWrong).toFixed(1)}`);
      }
      const asymY = yOf(0.5);
      const curX = xOf(ramseyCursorT);
      const curPt = M.ramseyPoint(ramseyCursorT, ramseyFdet, ramseyT2);
      const isPitfall = ramseyMap === 'pitfall';
      const curY = yOf(isPitfall ? curPt.pWrong : curPt.pDecay);

      const cueBands = [0.0, 0.5, 1.5, 2.5, 3.5].map(t => {
        const cx = xOf(t).toFixed(1);
        return `<line x1="${cx}" y1="${GY1}" x2="${cx}" y2="${GY0}" stroke="var(--svg-grid)" stroke-width="1.1" stroke-dasharray="3 3"/>`
          + `<text x="${cx}" y="${GY0 + 18}" text-anchor="middle" fill="var(--muted)" font-family="var(--mono)" font-size="10.5">${t.toFixed(1)}s</text>`;
      }).join('');

      const yTickHtml = [[0, '0.00'], [0.25, '0.25'], [0.5, '0.50'], [0.75, '0.75'], [1.0, '1.00']].map(([v, lbl]) => {
        const yy = yOf(v).toFixed(1);
        return `<line x1="${GX0}" y1="${yy}" x2="${GX1}" y2="${yy}" stroke="var(--svg-grid)" stroke-width="1"/>`
          + `<text x="${GX0 - 7}" y="${(Number(yy) + 4).toFixed(1)}" text-anchor="end" fill="var(--muted)" font-family="var(--mono)" font-size="10">${lbl}</text>`;
      }).join('');

      const boxX = Math.min(GX1 - 74, Math.max(GX0 + 2, curX - 35));

      byId('ramsey-svg').innerHTML = `
        <rect x="2" y="2" width="636" height="292" rx="8" fill="var(--svg-bg)" stroke="var(--line)" stroke-width="1"/>
        <text x="16" y="21" fill="var(--heading)" font-size="12" font-weight="700">Ramsey 概率条纹 P₀(t)（点击/拖动定位 t）</text>
        <line x1="290" y1="17" x2="308" y2="17" stroke="var(--blue)" stroke-width="1.6" stroke-dasharray="4 3"/>
        <text x="313" y="21" fill="var(--blue)" font-family="var(--mono)" font-size="10">理想 V=1</text>
        <line x1="378" y1="17" x2="396" y2="17" stroke="var(--teal)" stroke-width="2.5"/>
        <text x="401" y="21" fill="var(--teal)" font-family="var(--mono)" font-size="10" font-weight="700">真实退相干</text>
        <line x1="480" y1="17" x2="498" y2="17" stroke="var(--red)" stroke-width="2.2" stroke-dasharray="6 3"/>
        <text x="503" y="21" fill="var(--red)" font-family="var(--mono)" font-size="10" font-weight="700">误区 V·cos²</text>
        ${yTickHtml}
        ${cueBands}

        <!-- Asymptote P0 = 0.50 dashed guide -->
        <line x1="${GX0}" y1="${asymY.toFixed(1)}" x2="${GX1}" y2="${asymY.toFixed(1)}" stroke="var(--teal)" stroke-width="1.4" stroke-dasharray="5 4" opacity="0.78"/>

        <line x1="${GX0}" y1="${GY0}" x2="${GX1}" y2="${GY0}" stroke="var(--svg-axis)" stroke-width="1.3"/>
        <line x1="${GX0}" y1="${GY1}" x2="${GX0}" y2="${GY0}" stroke="var(--svg-axis)" stroke-width="1.3"/>

        <path d="${ptsIdeal.join('')}" fill="none" stroke="var(--blue)" stroke-width="1.4" stroke-dasharray="4 3" opacity="0.58"/>
        <path d="${ptsDecay.join('')}" fill="none" stroke="var(--teal)" stroke-width="${isPitfall ? '1.8' : '2.7'}" opacity="${isPitfall ? '0.52' : '1'}"/>
        <path d="${ptsWrong.join('')}" fill="none" stroke="var(--red)" stroke-width="${isPitfall ? '2.7' : '1.7'}" stroke-dasharray="7 4" opacity="${isPitfall ? '1' : '0.68'}"/>

        <!-- Asymptote label placed above all curves (y = 60..78 vs curve peak y = 81.1) so curves NEVER cross it -->
        <rect x="${GX1 - 196}" y="${GY1 + 2}" width="192" height="18" rx="9" fill="var(--teal-soft)" stroke="var(--teal)" stroke-width="1.1"/>
        <line x1="${GX1 - 187}" y1="${GY1 + 11}" x2="${GX1 - 173}" y2="${GY1 + 11}" stroke="var(--teal)" stroke-width="1.6" stroke-dasharray="4 2"/>
        <text x="${GX1 - 168}" y="${GY1 + 14.5}" fill="var(--teal)" font-family="var(--mono)" font-size="9.8" font-weight="700">纯退相位稳态 P₀ → 0.50 (混态)</text>

        <!-- Playhead Elements -->
        <line id="ramsey-playhead" x1="${curX.toFixed(1)}" y1="${GY1}" x2="${curX.toFixed(1)}" y2="${GY0}" stroke="var(--amber)" stroke-width="2.0"/>
        <circle id="ramsey-playhead-dot" cx="${curX.toFixed(1)}" cy="${curY.toFixed(1)}" r="5.5" fill="${isPitfall ? 'var(--red)' : 'var(--teal)'}" stroke="var(--panel)" stroke-width="2"/>
        <rect id="ramsey-playhead-box" x="${boxX.toFixed(1)}" y="${GY1 - 24}" width="72" height="19" rx="4" fill="var(--heading)"/>
        <text id="ramsey-playhead-txt" x="${(boxX + 36).toFixed(1)}" y="${GY1 - 11}" text-anchor="middle" fill="var(--bg)" font-family="var(--mono)" font-size="10" font-weight="700">t = ${f2(ramseyCursorT)}s</text>

        <text x="16" y="282" fill="var(--muted)" font-size="11">横轴：归一化演化时间 t (0–4.0 s) · 纵轴：测量概率 P₀(t) ∈ [0, 1]</text>
      `;
    }

    function updateRamseyStaticUi() {
      byId('ramsey-fdet-out').textContent = `${f2(ramseyFdet)} Hz`;
      byId('ramsey-t2-out').textContent = `${f2(ramseyT2)} s`;
      const isPitfall = ramseyMap === 'pitfall';
      byId('ramsey-map-correct').setAttribute('aria-pressed', String(!isPitfall));
      byId('ramsey-map-pitfall').setAttribute('aria-pressed', String(isPitfall));

      const noteEl = byId('ramsey-note');
      noteEl.className = isPitfall ? 'note-box warn' : 'note-box';
      if (isPitfall) {
        const v35 = Math.exp(-3.5 / ramseyT2);
        noteEl.textContent = `已高亮常见误区 V(t)cos²(πf_det t)：在 t = 3.5 s 处 V = ${f4(v35)}，误区曲线衰减趋近 0——但纯退相位不会让 |0⟩ 概率归零，真实结果是失去干涉起伏、收敛到均匀混合态 P₀ = P₁ = 0.50！`;
      } else {
        noteEl.textContent = '真实纯退相位 P₀(t) = [1 + V(t)cos(2πf_det t)]/2：条纹振幅按 V(t) = e^(−t/T₂*) 指数收缩，但平均值始终锚定在 0.50；拖动游标到半高腰（如 0.25 s）可观察最大 Fisher 灵敏度 F_C = V²。';
      }
      renderRamseySvg();
      updatePlayheadOnly();
    }

    function jumpRamseyTo(targetSec) {
      ramseyCursorT = Math.max(0, Math.min(DUR, targetSec));
      const pt = M.ramseyPoint(ramseyCursorT, ramseyFdet, ramseyT2);
      byId('ramsey-seek-status').textContent =
        `已定位至 t = ${f2(ramseyCursorT)} s：理想 P₀ = ${f4(pt.pIdeal)}，真实退相干 P₀ = ${f4(pt.pDecay)}（误区 ${f4(pt.pWrong)}），Fisher 信息 F_C = ${f4(pt.fisherC)}。`;
      updatePlayheadOnly();
    }

    // Click / drag on Ramsey SVG to scrub time cursor directly
    const rSvg = byId('ramsey-svg');
    let rScrub = false;
    function scrubT(e) {
      const rect = rSvg.getBoundingClientRect();
      if (!rect.width) return;
      const svgX = ((e.clientX - rect.left) / rect.width) * 640;
      const t = ((svgX - GX0) / (GX1 - GX0)) * DUR;
      ramseyCursorT = Math.max(0, Math.min(DUR, Math.round(t * 20) / 20));
      updatePlayheadOnly();
    }
    rSvg.style.cursor = 'ew-resize';
    rSvg.addEventListener('pointerdown', e => {
      rScrub = true;
      rSvg.setPointerCapture?.(e.pointerId);
      scrubT(e);
    });
    rSvg.addEventListener('pointermove', e => { if (rScrub) scrubT(e); });
    rSvg.addEventListener('pointerup', () => {
      if (rScrub) {
        rScrub = false;
        jumpRamseyTo(ramseyCursorT);
      }
    });

    byId('ramsey-fdet').addEventListener('input', e => {
      ramseyFdet = Number(e.target.value);
      updateRamseyStaticUi();
    });
    byId('ramsey-t2').addEventListener('input', e => {
      ramseyT2 = Number(e.target.value);
      updateRamseyStaticUi();
    });

    document.querySelectorAll('[data-ramsey-map]').forEach(btn => {
      btn.addEventListener('click', () => {
        ramseyMap = btn.dataset.ramseyMap;
        updateRamseyStaticUi();
      });
    });
    document.querySelectorAll('[data-ramsey-jump]').forEach(btn => {
      btn.addEventListener('click', () => jumpRamseyTo(Number(btn.dataset.ramseyJump)));
    });
    byId('ramsey-reset').addEventListener('click', () => {
      ramseyFdet = 1.0;
      ramseyT2 = 1.5;
      ramseyMap = 'correct';
      ramseyCursorT = 1.5;
      byId('ramsey-fdet').value = '1.0';
      byId('ramsey-t2').value = '1.5';
      updateRamseyStaticUi();
      byId('ramsey-seek-status').textContent = '已恢复默认参数（f_det = 1.00 Hz, T₂* = 1.50 s, 真实退相干曲线）。';
    });

    updateRamseyStaticUi();
    byId('ramsey-seek-status').textContent = '就绪：点击关键时刻或直接在条纹图上拖动游标 t，对比退相干稳态与 Fisher 灵敏度。';
  };
})(window);
