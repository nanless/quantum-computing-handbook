/* Module 02: 3D Right-Handed Bloch Sphere with Spherical Rotation Arcs, Undo, Orbit Drag & Sampling */
(function (global) {
  'use strict';

  const M = global.QuantumLabModel;
  const Mods = (global.QuantumLabModules = global.QuantumLabModules || {});

  Mods.initBloch = function initBloch(ctx) {
    const { byId, f3, f4, pct, fmtComplex } = ctx;
    const reducedMotion = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };

    let blochState = M.stateFromAngles(0, 0);
    let displayVec = M.blochVector(blochState);
    let undoStack = [];
    let blochHistory = ['|0⟩'];
    let lastArc = null; // { pts3d, axis, label }
    let camElev = M.BLOCH_ELEV;
    let camAzim = M.BLOCH_AZIM;
    let animFrame = null;
    let poleHintActive = false;

    function splitProjectedPath(pts3d, cx, cy, R) {
      const front = [], back = [];
      let cf = [], cb = [];
      for (const [x, y, z] of pts3d) {
        const p = M.projectBloch(x, y, z, cx, cy, R, camElev, camAzim);
        if (p.depth >= 0) {
          if (cb.length) { cb.push(p); back.push(cb); cb = []; }
          cf.push(p);
        } else {
          if (cf.length) { cf.push(p); front.push(cf); cf = []; }
          cb.push(p);
        }
      }
      if (cf.length) front.push(cf);
      if (cb.length) back.push(cb);
      const toD = segs => segs.filter(s => s.length > 1).map(seg =>
        seg.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.sx.toFixed(1)} ${p.sy.toFixed(1)}`).join('')
      ).join(' ');
      return { frontD: toD(front), backD: toD(back) };
    }

    function svgArrow(x1, y1, x2, y2, color, len = 10, hw = 4) {
      const dx = x2 - x1, dy = y2 - y1;
      const d = Math.hypot(dx, dy);
      if (d < 2) return '';
      const ux = dx / d, uy = dy / d;
      const px = -uy, py = ux;
      const bx = x2 - len * ux, by = y2 - len * uy;
      return `<polygon points="${x2.toFixed(1)},${y2.toFixed(1)} ${(bx + hw * px).toFixed(1)},${(by + hw * py).toFixed(1)} ${(bx - hw * px).toFixed(1)},${(by - hw * py).toFixed(1)}" fill="${color}"/>`;
    }

    function renderBlochSvg(vecOverride = null) {
      const cx = 280, cy = 222, R = 132;
      const proj = (x, y, z) => M.projectBloch(x, y, z, cx, cy, R, camElev, camAzim);
      const vec = vecOverride || displayVec;
      const thetaCur = Math.acos(Math.max(-1, Math.min(1, vec.rz)));
      const sinTh = Math.sin(thetaCur);
      const cosTh = Math.cos(thetaCur);
      let phiCur = Math.atan2(vec.ry, vec.rx);
      if (phiCur < 0) phiCur += 2 * Math.PI;

      const eqPts = [], merPts = [], latPts = [];
      for (let i = 0; i <= 120; i++) {
        const a = (2 * Math.PI * i) / 120;
        eqPts.push([Math.cos(a), Math.sin(a), 0]);
        merPts.push([Math.sin(a), 0, Math.cos(a)]);
        latPts.push([sinTh * Math.cos(a), sinTh * Math.sin(a), cosTh]);
      }
      const eq = splitProjectedPath(eqPts, cx, cy, R);
      const mer = splitProjectedPath(merPts, cx, cy, R);
      const lat = sinTh > 0.03 ? splitProjectedPath(latPts, cx, cy, R) : { frontD: '', backD: '' };

      const pZ = proj(0, 0, 1.32), nZ = proj(0, 0, -1.24);
      const pX = proj(1.36, 0, 0), nX = proj(-1.26, 0, 0);
      const pY = proj(0, 1.34, 0), nY = proj(0, -1.26, 0);
      const tip = proj(vec.rx, vec.ry, vec.rz);
      const eqProj = proj(vec.rx, vec.ry, 0);

      let thetaArc = '';
      if (thetaCur > 0.08 && sinTh > 0.02) {
        const pts = [];
        for (let i = 0; i <= 20; i++) {
          const t = (thetaCur * i) / 20;
          const p = proj(0.34 * Math.sin(t) * Math.cos(phiCur), 0.34 * Math.sin(t) * Math.sin(phiCur), 0.34 * Math.cos(t));
          pts.push(`${i === 0 ? 'M' : 'L'}${p.sx.toFixed(1)} ${p.sy.toFixed(1)}`);
        }
        thetaArc = `<path d="${pts.join('')}" fill="none" stroke="var(--red)" stroke-width="1.8"/>`;
      }

      let phiArc = '';
      if (sinTh > 0.06 && phiCur > 0.08) {
        const pts = [];
        const steps = Math.max(12, Math.round(phiCur * 16));
        for (let i = 0; i <= steps; i++) {
          const a = (phiCur * i) / steps;
          const p = proj(0.32 * Math.cos(a), 0.32 * Math.sin(a), 0);
          pts.push(`${i === 0 ? 'M' : 'L'}${p.sx.toFixed(1)} ${p.sy.toFixed(1)}`);
        }
        phiArc = `<path d="${pts.join('')}" fill="none" stroke="var(--blue)" stroke-width="1.8"/>`;
      }

      // True spherical rotation arc + rotation axis line
      let rotAxisHtml = '';
      let arcFrontHtml = '';
      let arcBackHtml = '';
      if (lastArc && lastArc.pts3d.length > 1) {
        const splitArc = splitProjectedPath(lastArc.pts3d, cx, cy, R);
        if (splitArc.backD) {
          arcBackHtml = `<path d="${splitArc.backD}" fill="none" stroke="var(--amber)" stroke-width="2.4" stroke-dasharray="4 4" opacity="0.65"/>`;
        }
        if (splitArc.frontD) {
          arcFrontHtml = `<path d="${splitArc.frontD}" fill="none" stroke="var(--amber)" stroke-width="2.8" stroke-linecap="round"/>`;
        }
        const [ax, ay, az] = lastArc.axis;
        const ap = proj(1.18 * ax, 1.18 * ay, 1.18 * az);
        const an = proj(-1.18 * ax, -1.18 * ay, -1.18 * az);
        rotAxisHtml = `<line x1="${an.sx.toFixed(1)}" y1="${an.sy.toFixed(1)}" x2="${ap.sx.toFixed(1)}" y2="${ap.sy.toFixed(1)}" stroke="var(--amber)" stroke-width="1.5" stroke-dasharray="6 4" opacity="0.8"/>`;
      }

      const pt0 = proj(0, 0, 1), pt1 = proj(0, 0, -1);
      const ptXp = proj(1, 0, 0), ptXm = proj(-1, 0, 0);
      const ptYp = proj(0, 1, 0), ptYm = proj(0, -1, 0);
      const tipFront = tip.depth >= 0;

      byId('bloch-svg').innerHTML = `
        <defs>
          <radialGradient id="bloch-grad" cx="38%" cy="30%" r="68%">
            <stop offset="0%" stop-color="var(--svg-sphere-0)" stop-opacity="0.92"/>
            <stop offset="58%" stop-color="var(--svg-sphere-1)" stop-opacity="0.72"/>
            <stop offset="100%" stop-color="var(--svg-sphere-2)" stop-opacity="0.58"/>
          </radialGradient>
        </defs>
        <rect x="2" y="2" width="556" height="436" rx="8" fill="var(--svg-bg)" stroke="var(--line)" stroke-width="1"/>
        <circle cx="${cx}" cy="${cy}" r="${R}" fill="url(#bloch-grad)" stroke="var(--svg-sphere-stroke)" stroke-width="2.2"/>
        <path d="${mer.backD}" fill="none" stroke="var(--svg-neg)" stroke-width="1.2" stroke-dasharray="4 4" opacity="0.65"/>
        <path d="${eq.backD}" fill="none" stroke="var(--svg-sphere-stroke)" stroke-width="1.5" stroke-dasharray="6 5" opacity="0.65"/>
        ${lat.backD ? `<path d="${lat.backD}" fill="none" stroke="var(--amber)" stroke-width="1.3" stroke-dasharray="4 4" opacity="0.48"/>` : ''}
        ${arcBackHtml}
        ${rotAxisHtml}
        <line x1="${cx}" y1="${cy}" x2="${nZ.sx.toFixed(1)}" y2="${nZ.sy.toFixed(1)}" stroke="var(--svg-neg)" stroke-width="1.5" stroke-dasharray="5 4"/>
        <line x1="${cx}" y1="${cy}" x2="${nX.sx.toFixed(1)}" y2="${nX.sy.toFixed(1)}" stroke="var(--svg-neg)" stroke-width="1.5" stroke-dasharray="5 4"/>
        <line x1="${cx}" y1="${cy}" x2="${nY.sx.toFixed(1)}" y2="${nY.sy.toFixed(1)}" stroke="var(--svg-neg)" stroke-width="1.5" stroke-dasharray="5 4"/>
        <circle cx="${pt1.sx.toFixed(1)}" cy="${pt1.sy.toFixed(1)}" r="4.5" fill="var(--svg-bg)" stroke="var(--teal)" stroke-width="2"/>
        <circle cx="${ptXm.sx.toFixed(1)}" cy="${ptXm.sy.toFixed(1)}" r="4.2" fill="var(--svg-bg)" stroke="var(--blue)" stroke-width="2"/>
        <circle cx="${ptYm.sx.toFixed(1)}" cy="${ptYm.sy.toFixed(1)}" r="4.2" fill="var(--svg-bg)" stroke="var(--amber)" stroke-width="2"/>
        <path d="${mer.frontD}" fill="none" stroke="var(--svg-neg)" stroke-width="1.3" opacity="0.8"/>
        <path d="${eq.frontD}" fill="none" stroke="var(--svg-sphere-stroke)" stroke-width="2.0"/>
        ${lat.frontD ? `<path d="${lat.frontD}" fill="none" stroke="var(--amber)" stroke-width="1.5" opacity="0.72"/>` : ''}
        <line x1="${cx}" y1="${cy}" x2="${pZ.sx.toFixed(1)}" y2="${pZ.sy.toFixed(1)}" stroke="var(--svg-axis)" stroke-width="2.0"/>
        ${svgArrow(cx, cy, pZ.sx, pZ.sy, 'var(--svg-axis)', 10, 3.8)}
        <line x1="${cx}" y1="${cy}" x2="${pX.sx.toFixed(1)}" y2="${pX.sy.toFixed(1)}" stroke="var(--svg-axis)" stroke-width="2.0"/>
        ${svgArrow(cx, cy, pX.sx, pX.sy, 'var(--svg-axis)', 10, 3.8)}
        <line x1="${cx}" y1="${cy}" x2="${pY.sx.toFixed(1)}" y2="${pY.sy.toFixed(1)}" stroke="var(--svg-axis)" stroke-width="2.0"/>
        ${svgArrow(cx, cy, pY.sx, pY.sy, 'var(--svg-axis)', 10, 3.8)}
        ${sinTh > 0.04 ? `
          <line x1="${tip.sx.toFixed(1)}" y1="${tip.sy.toFixed(1)}" x2="${eqProj.sx.toFixed(1)}" y2="${eqProj.sy.toFixed(1)}" stroke="var(--red)" stroke-width="1.3" stroke-dasharray="3 3" opacity="0.72"/>
          <line x1="${cx}" y1="${cy}" x2="${eqProj.sx.toFixed(1)}" y2="${eqProj.sy.toFixed(1)}" stroke="var(--blue)" stroke-width="1.3" stroke-dasharray="3 3" opacity="0.72"/>
        ` : ''}
        ${thetaArc}
        ${phiArc}
        ${arcFrontHtml}
        <circle cx="${pt0.sx.toFixed(1)}" cy="${pt0.sy.toFixed(1)}" r="5" fill="var(--teal)"/>
        <circle cx="${ptXp.sx.toFixed(1)}" cy="${ptXp.sy.toFixed(1)}" r="5" fill="var(--blue)"/>
        <circle cx="${ptYp.sx.toFixed(1)}" cy="${ptYp.sy.toFixed(1)}" r="5" fill="var(--amber)"/>
        <line x1="${cx}" y1="${cy}" x2="${tip.sx.toFixed(1)}" y2="${tip.sy.toFixed(1)}" stroke="var(--red)" stroke-width="3.2" stroke-linecap="round" ${tipFront ? '' : 'stroke-dasharray="6 3" opacity="0.82"'}/>
        ${svgArrow(cx, cy, tip.sx, tip.sy, 'var(--red)', 12, 4.8)}
        <circle cx="${cx}" cy="${cy}" r="4.0" fill="var(--svg-card)" stroke="var(--svg-axis)" stroke-width="1.8"/>
        <circle cx="${tip.sx.toFixed(1)}" cy="${tip.sy.toFixed(1)}" r="6.8" fill="${tipFront ? 'var(--red)' : 'var(--svg-bg)'}" stroke="${tipFront ? 'var(--panel)' : 'var(--red)'}" stroke-width="2.4"/>
        <text x="${(pZ.sx + 10).toFixed(1)}" y="${(pZ.sy + 5).toFixed(1)}" fill="var(--heading)" font-family="var(--mono)" font-size="13" font-weight="700">|0⟩ (+Z)</text>
        <text x="${(nZ.sx + 10).toFixed(1)}" y="${(nZ.sy + 6).toFixed(1)}" fill="var(--muted)" font-family="var(--mono)" font-size="12.5" font-weight="600">|1⟩ (−Z)</text>
        <text x="${(pX.sx - 12).toFixed(1)}" y="${(pX.sy + 20).toFixed(1)}" text-anchor="middle" fill="var(--heading)" font-family="var(--mono)" font-size="13" font-weight="700">|+⟩ (+X)</text>
        <text x="${(nX.sx + 10).toFixed(1)}" y="${(nX.sy + 3).toFixed(1)}" fill="var(--muted)" font-family="var(--mono)" font-size="12">|−⟩ (−X)</text>
        <text x="${(pY.sx + 12).toFixed(1)}" y="${(pY.sy + 20).toFixed(1)}" text-anchor="middle" fill="var(--heading)" font-family="var(--mono)" font-size="13" font-weight="700">|+i⟩ (+Y)</text>
        <text x="${(nY.sx - 10).toFixed(1)}" y="${(nY.sy - 4).toFixed(1)}" text-anchor="end" fill="var(--muted)" font-family="var(--mono)" font-size="12">|−i⟩ (−Y)</text>
        <text x="${(tip.sx + (tip.sx > cx ? 12 : -12)).toFixed(1)}" y="${(tip.sy - 10).toFixed(1)}" text-anchor="${tip.sx > cx ? 'start' : 'end'}" fill="var(--red)" font-family="var(--mono)" font-size="13.5" font-weight="800">|ψ⟩</text>
        <text x="16" y="424" fill="var(--muted)" font-size="11.2">${lastArc ? `球面真弧：${lastArc.label}` : (tipFront ? '前半球（实心红点）' : '后半球（空心红圈）')} · 可拖拽旋转观察视角</text>
      `;
    }

    function updateBlochReadouts() {
      const vec = M.blochVector(blochState);
      const thDeg = Math.round((blochState.theta * 180) / Math.PI);
      const phDeg = Math.round(((blochState.phi * 180) / Math.PI) % 360);

      byId('bloch-theta').value = String(thDeg);
      byId('bloch-phi').value = String(phDeg);
      byId('bloch-theta-out').textContent = `${thDeg}° (${f3(blochState.theta)} rad)`;
      byId('bloch-phi-out').textContent = `${phDeg}° (${f3(blochState.phi)} rad)`;

      byId('bloch-alpha').textContent = f4(blochState.aRe);
      byId('bloch-beta').textContent = fmtComplex(blochState.bRe, blochState.bIm);
      // Clean negative zero strictly!
      byId('bloch-vec').textContent = `(${M.fmtFixed(vec.rx, 3)}, ${M.fmtFixed(vec.ry, 3)}, ${M.fmtFixed(vec.rz, 3)})`;
      const probSum = blochState.aRe ** 2 + blochState.aIm ** 2 + blochState.bRe ** 2 + blochState.bIm ** 2;
      byId('bloch-norm').textContent = `${f4(probSum)} / ${f4(vec.norm)}`;

      byId('bloch-bar-z').style.width = (100 * vec.pZ0).toFixed(2) + '%';
      byId('bloch-bar-x').style.width = (100 * vec.pX0).toFixed(2) + '%';
      byId('bloch-bar-y').style.width = (100 * vec.pY0).toFixed(2) + '%';
      byId('bloch-pz').textContent = pct(vec.pZ0);
      byId('bloch-px').textContent = pct(vec.pX0);
      byId('bloch-py').textContent = pct(vec.pY0);

      byId('bloch-history').textContent = '线路序列：' + blochHistory.join(' → ');
      const undoBtn = byId('bloch-undo');
      if (undoBtn) undoBtn.disabled = undoStack.length === 0;

      const noteEl = byId('bloch-note');
      noteEl.className = 'note-box';
      if (poleHintActive && (vec.rz > 0.995 || vec.rz < -0.995)) {
        noteEl.classList.add('amber');
        noteEl.textContent = `极点全局相位提示：在 ${vec.rz > 0 ? '|0⟩（北极）' : '|1⟩（南极）'} 处，转动 φ 仅乘上不可观测全局相位 e^(iφ)，态点坐标与 X/Y/Z 三基概率完全不变！先调大 θ 离开极点再试。`;
      } else if (vec.rz > 0.995) {
        noteEl.textContent = '处于北极 |0⟩：Z 基测量 100% 得 0；X 与 Y 基测量均为 50%/50%。试试按顺序点击 H → S → T 观察球面真弧旋转！';
      } else if (vec.rz < -0.995) {
        noteEl.textContent = '处于南极 |1⟩：Z 基测量 100% 得 1；在两极点处方位角 φ 退化为不可观测全局相位。';
      } else if (Math.abs(vec.rz) < 0.02) {
        noteEl.textContent = `位于赤道等幅叠加圈（Z 基 50%/50%）：相对相位 φ = ${phDeg}° 决定 X 基（P|+⟩=${pct(vec.pX0)}）与 Y 基（P|+i⟩=${pct(vec.pY0)}）分布。`;
      } else {
        noteEl.textContent = '一般纯态：所有单比特酉门均沿固定旋转轴在球面上严格画圆弧，永不穿过球内混态区。';
      }
    }

    function animateRotation(startVecArr, axis, angleRad, onDone) {
      if (animFrame) cancelAnimationFrame(animFrame);
      if (reducedMotion.matches) {
        displayVec = M.blochVector(blochState);
        renderBlochSvg(displayVec);
        onDone?.();
        return;
      }
      const duration = 240;
      const t0 = performance.now();
      function step(now) {
        const u = Math.min(1, (now - t0) / duration);
        const eased = 1 - Math.pow(1 - u, 3);
        const [rx, ry, rz] = M.rodriguesRotate(startVecArr, axis, angleRad * eased);
        displayVec = { rx, ry, rz };
        renderBlochSvg(displayVec);
        if (u < 1) {
          animFrame = requestAnimationFrame(step);
        } else {
          animFrame = null;
          displayVec = M.blochVector(blochState);
          renderBlochSvg(displayVec);
          onDone?.();
        }
      }
      animFrame = requestAnimationFrame(step);
    }

    // Orbit camera drag on Bloch SVG
    const svgEl = byId('bloch-svg');
    let dragging = false, lastX = 0, lastY = 0;
    svgEl.style.cursor = 'grab';
    svgEl.addEventListener('pointerdown', e => {
      dragging = true;
      lastX = e.clientX;
      lastY = e.clientY;
      svgEl.style.cursor = 'grabbing';
      svgEl.setPointerCapture?.(e.pointerId);
    });
    svgEl.addEventListener('pointermove', e => {
      if (!dragging) return;
      const dx = e.clientX - lastX;
      const dy = e.clientY - lastY;
      lastX = e.clientX;
      lastY = e.clientY;
      camAzim -= dx * 0.01;
      camElev = Math.max(-1.1, Math.min(1.1, camElev + dy * 0.01));
      renderBlochSvg();
    });
    svgEl.addEventListener('pointerup', () => {
      dragging = false;
      svgEl.style.cursor = 'grab';
    });

    byId('bloch-view-reset')?.addEventListener('click', () => {
      camElev = M.BLOCH_ELEV;
      camAzim = M.BLOCH_AZIM;
      renderBlochSvg();
    });

    byId('bloch-theta').addEventListener('input', e => {
      poleHintActive = false;
      const th = (Number(e.target.value) * Math.PI) / 180;
      const ph = (Number(byId('bloch-phi').value) * Math.PI) / 180;
      blochState = M.stateFromAngles(th, ph);
      displayVec = M.blochVector(blochState);
      blochHistory = [`|ψ(${e.target.value}°,${byId('bloch-phi').value}°)⟩`];
      lastArc = null;
      undoStack = [];
      updateBlochReadouts();
      renderBlochSvg();
    });

    byId('bloch-phi').addEventListener('input', e => {
      const thDeg = Number(byId('bloch-theta').value);
      const th = (thDeg * Math.PI) / 180;
      const ph = (Number(e.target.value) * Math.PI) / 180;
      const atPole = thDeg <= 1 || thDeg >= 179;
      poleHintActive = atPole;
      blochState = M.stateFromAngles(th, ph);
      displayVec = M.blochVector(blochState);
      if (!atPole) {
        blochHistory = [`|ψ(${thDeg}°,${e.target.value}°)⟩`];
        undoStack = [];
      }
      lastArc = null;
      updateBlochReadouts();
      renderBlochSvg();
    });

    document.querySelectorAll('[data-gate]').forEach(btn => {
      btn.addEventListener('click', () => {
        poleHintActive = false;
        const g = btn.dataset.gate;
        if (g === 'RESET') {
          blochState = M.stateFromAngles(0, 0);
          displayVec = M.blochVector(blochState);
          blochHistory = ['|0⟩'];
          undoStack = [];
          lastArc = null;
          updateBlochReadouts();
          renderBlochSvg();
          return;
        }
        const prevState = blochState;
        const prevVec = M.blochVector(prevState);
        undoStack.push({ state: prevState, history: [...blochHistory], lastArc });
        if (undoStack.length > 24) undoStack.shift();

        blochState = M.applyGate(prevState, g);
        const labelMap = { Sdg: 'S†', Tdg: 'T†', Rx45: 'Rx(π/4)', Ry45: 'Ry(π/4)', Rz45: 'Rz(π/4)' };
        if (blochHistory.length >= 14) blochHistory = ['…', ...blochHistory.slice(-10)];
        blochHistory.push(labelMap[g] || g);

        const rot = M.GATE_ROTATIONS[g];
        if (rot) {
          const startArr = [prevVec.rx, prevVec.ry, prevVec.rz];
          lastArc = {
            pts3d: M.sphericalArcPoints(startArr, rot.axis, rot.angle, 36),
            axis: rot.axis,
            label: `${labelMap[g] || g} · ${rot.label}`,
          };
          updateBlochReadouts();
          animateRotation(startArr, rot.axis, rot.angle);
        } else {
          displayVec = M.blochVector(blochState);
          lastArc = null;
          updateBlochReadouts();
          renderBlochSvg();
        }
      });
    });

    byId('bloch-undo')?.addEventListener('click', () => {
      if (!undoStack.length) return;
      const snap = undoStack.pop();
      blochState = snap.state;
      blochHistory = snap.history;
      lastArc = snap.lastArc;
      displayVec = M.blochVector(blochState);
      poleHintActive = false;
      updateBlochReadouts();
      renderBlochSvg();
    });

    // Single-shot / 1,000-shot measurement sampling
    function runSampling(shots) {
      const basis = byId('bloch-meas-basis')?.value || 'Z';
      const vec = M.blochVector(blochState);
      const p0 = basis === 'X' ? vec.pX0 : basis === 'Y' ? vec.pY0 : vec.pZ0;
      const lbl0 = basis === 'X' ? '|+⟩' : basis === 'Y' ? '|+i⟩' : '|0⟩';
      const lbl1 = basis === 'X' ? '|−⟩' : basis === 'Y' ? '|−i⟩' : '|1⟩';
      const res = M.sampleMeasurement(p0, shots);
      const outEl = byId('bloch-sample-out');
      if (!outEl) return;
      if (shots === 1) {
        const outcome = res.c0 === 1 ? lbl0 : lbl1;
        outEl.textContent = `单次 ${basis} 基投影坍缩结果：${outcome}（理论 P(${lbl0}) = ${pct(p0)}；注意单次坍缩只给 1 bit，不暴露连续振幅）。`;
      } else {
        outEl.textContent = `${shots} 次 ${basis} 基独立采样：${lbl0} 占 ${res.c0}/${shots} = ${pct(res.freq0)}（95% Wilson 区间 [${pct(res.ci.lo)}, ${pct(res.ci.hi)}]，理论 ${pct(p0)}）。`;
      }
    }
    byId('bloch-sample-1')?.addEventListener('click', () => runSampling(1));
    byId('bloch-sample-1000')?.addEventListener('click', () => runSampling(1000));

    updateBlochReadouts();
    renderBlochSvg();
  };
})(window);
