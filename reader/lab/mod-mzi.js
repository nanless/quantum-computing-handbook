/* Module 01: Mach-Zehnder Interferometer, Density Matrix & Live PCM WAV Sonification */
(function (global) {
  'use strict';

  const M = global.QuantumLabModel;
  const Mods = (global.QuantumLabModules = global.QuantumLabModules || {});

  Mods.initMzi = function initMzi(ctx) {
    const { byId, f2, f3, f4, pct, fmtComplex, setAudioWav, pauseAllAudio } = ctx;
    let mziPhiDeg = 0;
    let mziVis = 1.0;

    function drawPhasorDial(cx, cy, r, re, im, colorVar, label) {
      const ex = cx + r * re;
      const ey = cy - r * im;
      const mag = Math.hypot(re, im);
      let arrow = '';
      if (mag > 0.04) {
        const ux = (ex - cx) / (r * mag);
        const uy = (ey - cy) / (r * mag);
        const px = -uy, py = ux;
        const al = Math.min(7, r * mag * 0.45);
        const aw = 3;
        const bx = ex - al * ux, by = ey - al * uy;
        arrow = `<line x1="${cx}" y1="${cy}" x2="${ex.toFixed(1)}" y2="${ey.toFixed(1)}" stroke="${colorVar}" stroke-width="2.2" stroke-linecap="round"/>`
          + `<polygon points="${ex.toFixed(1)},${ey.toFixed(1)} ${(bx + aw * px).toFixed(1)},${(by + aw * py).toFixed(1)} ${(bx - aw * px).toFixed(1)},${(by - aw * py).toFixed(1)}" fill="${colorVar}"/>`;
      } else {
        arrow = `<circle cx="${cx}" cy="${cy}" r="3.2" fill="${colorVar}"/>`;
      }
      return `<g>
        <circle cx="${cx}" cy="${cy}" r="${r}" fill="var(--svg-card)" stroke="var(--line-strong)" stroke-width="1.2"/>
        <line x1="${cx - r}" y1="${cy}" x2="${cx + r}" y2="${cy}" stroke="var(--svg-grid)" stroke-width="1"/>
        <line x1="${cx}" y1="${cy - r}" x2="${cx}" y2="${cy + r}" stroke="var(--svg-grid)" stroke-width="1"/>
        ${arrow}
        <text x="${cx}" y="${cy + r + 14}" text-anchor="middle" fill="var(--muted)" font-family="var(--mono)" font-size="10.5">${label}</text>
      </g>`;
    }

    function renderMziDiagrams(m) {
      const phiDeg = mziPhiDeg;
      const s = Math.SQRT1_2;
      const cPhi = Math.cos(m.phiRad);
      const sPhi = Math.sin(m.phiRad);
      const pathDetOpacity = (0.12 + 0.88 * m.dMax).toFixed(2);

      // When V < 0.995, show mixed-state density-matrix badge instead of misleading pure-state vector sum
      const outputPhaseHtml = m.isMixed
        ? `<g>
            <rect x="408" y="60" width="68" height="48" rx="6" fill="var(--amber-soft)" stroke="var(--amber)" stroke-width="1.4"/>
            <text x="442" y="79" text-anchor="middle" fill="var(--amber)" font-family="var(--mono)" font-size="10" font-weight="700">混态 ρ₀₀</text>
            <text x="442" y="96" text-anchor="middle" fill="var(--heading)" font-family="var(--mono)" font-size="11" font-weight="800">${f3(m.rho00)}</text>
            <rect x="408" y="168" width="68" height="48" rx="6" fill="var(--amber-soft)" stroke="var(--amber)" stroke-width="1.4"/>
            <text x="442" y="187" text-anchor="middle" fill="var(--amber)" font-family="var(--mono)" font-size="10" font-weight="700">|ρ₀₁|=V/2</text>
            <text x="442" y="204" text-anchor="middle" fill="var(--heading)" font-family="var(--mono)" font-size="11" font-weight="800">${f3(m.rho01ArmAbs)}</text>
          </g>`
        : `<g>
            ${drawPhasorDial(442, 83, 22, m.amp0Re, m.amp0Im, 'var(--teal)', '端口 0 矢量和')}
            ${drawPhasorDial(442, 192, 22, m.amp1Re, m.amp1Im, 'var(--red)', '端口 1 矢量差')}
          </g>`;

      byId('mzi-svg').innerHTML = `
        <rect x="2" y="2" width="636" height="272" rx="8" fill="var(--svg-bg)" stroke="var(--line)" stroke-width="1"/>
        <text x="16" y="23" fill="var(--heading)" font-size="12.5" font-weight="700">MZI 光路与${m.isMixed ? '密度矩阵相干度' : '复振幅合成'}（φ = ${phiDeg}°, V = ${f2(m.visibility)}）</text>

        <!-- Input |0> (uses var(--svg-badge-ink) for >10:1 contrast in dark mode) -->
        <rect x="16" y="70" width="38" height="26" rx="5" fill="var(--teal)"/>
        <text x="35" y="87" text-anchor="middle" fill="var(--svg-badge-ink)" font-family="var(--mono)" font-size="12" font-weight="800">|0⟩</text>
        <line x1="54" y1="83" x2="90" y2="83" stroke="var(--teal)" stroke-width="2.4"/>
        <line x1="54" y1="192" x2="90" y2="192" stroke="var(--line-strong)" stroke-width="1.4" stroke-dasharray="4 3"/>
        <text x="35" y="196" text-anchor="middle" fill="var(--muted)" font-family="var(--mono)" font-size="11">0</text>

        <!-- BS1 -->
        <rect x="90" y="60" width="36" height="156" rx="7" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="1.6"/>
        <line x1="96" y1="208" x2="120" y2="68" stroke="var(--blue)" stroke-width="1.4" stroke-dasharray="4 3" opacity="0.7"/>
        <text x="108" y="143" text-anchor="middle" fill="var(--blue)" font-family="Georgia,serif" font-size="16" font-weight="700">H</text>
        <text x="108" y="52" text-anchor="middle" fill="var(--muted)" font-family="var(--mono)" font-size="10.5">BS₁</text>

        <!-- Arms -->
        <line x1="126" y1="83" x2="364" y2="83" stroke="var(--teal)" stroke-width="2.4"/>
        <line x1="126" y1="192" x2="364" y2="192" stroke="var(--amber)" stroke-width="2.4"/>

        <!-- Phase shifter -->
        <rect x="198" y="176" width="66" height="32" rx="6" fill="var(--amber-soft)" stroke="var(--amber)" stroke-width="1.6"/>
        <text x="231" y="196" text-anchor="middle" fill="var(--amber)" font-family="var(--mono)" font-size="11.5" font-weight="700">P(${phiDeg}°)</text>

        <!-- Path detector indicator -->
        <rect x="190" y="114" width="122" height="30" rx="6" fill="var(--red-soft)" stroke="var(--red)" stroke-width="1.3" opacity="${pathDetOpacity}"/>
        <text x="251" y="133" text-anchor="middle" fill="var(--red)" font-family="var(--mono)" font-size="10.5" font-weight="700" opacity="${pathDetOpacity}">路径标记 D≤${f2(m.dMax)}</text>

        <!-- Arm phasor dials -->
        ${drawPhasorDial(162, 83, 21, s, 0, 'var(--teal)', '1/√2')}
        ${drawPhasorDial(312, 83, 21, s, 0, 'var(--teal)', '臂 0')}
        ${drawPhasorDial(312, 192, 21, s * cPhi, s * sPhi, 'var(--amber)', 'eⁱᵠ/√2')}

        <!-- BS2 -->
        <rect x="364" y="60" width="36" height="156" rx="7" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="1.6"/>
        <line x1="370" y1="208" x2="394" y2="68" stroke="var(--blue)" stroke-width="1.4" stroke-dasharray="4 3" opacity="0.7"/>
        <text x="382" y="143" text-anchor="middle" fill="var(--blue)" font-family="Georgia,serif" font-size="16" font-weight="700">H</text>
        <text x="382" y="52" text-anchor="middle" fill="var(--muted)" font-family="var(--mono)" font-size="10.5">BS₂</text>

        <!-- Outputs -->
        <line x1="400" y1="83" x2="486" y2="83" stroke="var(--teal)" stroke-width="${(1.4 + 2.4 * m.p0).toFixed(1)}"/>
        <line x1="400" y1="192" x2="486" y2="192" stroke="var(--red)" stroke-width="${(1.4 + 2.4 * m.p1).toFixed(1)}"/>
        ${outputPhaseHtml}

        <!-- Detectors -->
        <rect x="486" y="56" width="140" height="58" rx="7" fill="var(--svg-card)" stroke="var(--teal)" stroke-width="1.5"/>
        <text x="496" y="75" fill="var(--teal)" font-family="var(--mono)" font-size="11" font-weight="700">D₀: P(0) = ${pct(m.p0)}</text>
        <rect x="496" y="86" width="120" height="14" rx="7" fill="var(--stone)"/>
        <rect x="496" y="86" width="${Math.round(120 * m.p0)}" height="14" rx="7" fill="var(--teal)"/>

        <rect x="486" y="165" width="140" height="58" rx="7" fill="var(--svg-card)" stroke="var(--red)" stroke-width="1.5"/>
        <text x="496" y="184" fill="var(--red)" font-family="var(--mono)" font-size="11" font-weight="700">D₁: P(1) = ${pct(m.p1)}</text>
        <rect x="496" y="195" width="120" height="14" rx="7" fill="var(--stone)"/>
        <rect x="496" y="195" width="${Math.round(120 * m.p1)}" height="14" rx="7" fill="var(--red)"/>

        <text x="16" y="258" fill="var(--muted)" font-size="11">${m.isMixed ? '混态模式（V < 1）：不再存在单一纯态振幅，由密度矩阵对角元 ρ₀₀ 与相干项 |ρ₀₁| = V/2 共同决定条纹。' : '纯态模式（V = 1）：两路复振幅严格相加/相减；可点击下方条纹图任意位置直接设置相位 φ。'}</text>
      `;

      // Fringe curve SVG (clickable/draggable)
      const gx0 = 56, gx1 = 612, gy0 = 158, gy1 = 36;
      const pts0 = [], pts1 = [], ptsIdeal = [];
      const N = 120;
      for (let i = 0; i <= N; i++) {
        const u = i / N;
        const phi = 2 * Math.PI * u;
        const x = gx0 + u * (gx1 - gx0);
        const y0 = gy0 - ((1 + m.visibility * Math.cos(phi)) / 2) * (gy0 - gy1);
        const y1 = gy0 - ((1 - m.visibility * Math.cos(phi)) / 2) * (gy0 - gy1);
        const yId = gy0 - ((1 + Math.cos(phi)) / 2) * (gy0 - gy1);
        const cmd = i === 0 ? 'M' : 'L';
        pts0.push(`${cmd}${x.toFixed(1)} ${y0.toFixed(1)}`);
        pts1.push(`${cmd}${x.toFixed(1)} ${y1.toFixed(1)}`);
        ptsIdeal.push(`${cmd}${x.toFixed(1)} ${yId.toFixed(1)}`);
      }
      const curX = gx0 + (mziPhiDeg / 360) * (gx1 - gx0);
      const curY0 = gy0 - m.p0 * (gy0 - gy1);
      const curY1 = gy0 - m.p1 * (gy0 - gy1);
      const ticks = [[0, '0'], [0.25, 'π/2 (90°)'], [0.5, 'π (180°)'], [0.75, '3π/2 (270°)'], [1, '2π (360°)']];
      const tickHtml = ticks.map(([u, lbl]) => {
        const tx = (gx0 + u * (gx1 - gx0)).toFixed(1);
        return `<line x1="${tx}" y1="${gy1}" x2="${tx}" y2="${gy0}" stroke="var(--svg-grid)" stroke-width="1"/>`
          + `<text x="${tx}" y="${gy0 + 18}" text-anchor="middle" fill="var(--muted)" font-family="var(--mono)" font-size="10.5">${lbl}</text>`;
      }).join('');

      byId('mzi-fringe-svg').innerHTML = `
        <rect x="2" y="2" width="636" height="194" rx="8" fill="var(--svg-bg)" stroke="var(--line)" stroke-width="1"/>
        <text x="16" y="22" fill="var(--heading)" font-size="12" font-weight="700">完整干涉条纹 P(0; φ) 与 P(1; φ)（可点击/拖动设 φ）</text>
        <line x1="366" y1="18" x2="386" y2="18" stroke="var(--teal)" stroke-width="2.4"/>
        <text x="392" y="22" fill="var(--teal)" font-family="var(--mono)" font-size="10.5" font-weight="700">P(0)</text>
        <line x1="436" y1="18" x2="456" y2="18" stroke="var(--red)" stroke-width="1.8" stroke-dasharray="5 3"/>
        <text x="462" y="22" fill="var(--red)" font-family="var(--mono)" font-size="10.5" font-weight="700">P(1)</text>
        <line x1="506" y1="18" x2="526" y2="18" stroke="var(--muted)" stroke-width="1.2" stroke-dasharray="2 3"/>
        <text x="532" y="22" fill="var(--muted)" font-family="var(--mono)" font-size="10.5">V=1 参考</text>
        ${tickHtml}
        <line x1="${gx0}" y1="${gy1}" x2="${gx1}" y2="${gy1}" stroke="var(--svg-grid)" stroke-width="1"/>
        <line x1="${gx0}" y1="${((gy0 + gy1) / 2).toFixed(1)}" x2="${gx1}" y2="${((gy0 + gy1) / 2).toFixed(1)}" stroke="var(--svg-grid)" stroke-width="1" stroke-dasharray="4 3"/>
        <line x1="${gx0}" y1="${gy0}" x2="${gx1}" y2="${gy0}" stroke="var(--svg-axis)" stroke-width="1.2"/>
        <line x1="${gx0}" y1="${gy1}" x2="${gx0}" y2="${gy0}" stroke="var(--svg-axis)" stroke-width="1.2"/>
        <text x="${gx0 - 8}" y="${gy1 + 4}" text-anchor="end" fill="var(--muted)" font-family="var(--mono)" font-size="10.5">1.0</text>
        <text x="${gx0 - 8}" y="${((gy0 + gy1) / 2 + 4).toFixed(1)}" text-anchor="end" fill="var(--muted)" font-family="var(--mono)" font-size="10.5">0.5</text>
        <text x="${gx0 - 8}" y="${gy0 + 4}" text-anchor="end" fill="var(--muted)" font-family="var(--mono)" font-size="10.5">0.0</text>
        <path d="${ptsIdeal.join('')}" fill="none" stroke="var(--muted)" stroke-width="1.2" stroke-dasharray="2 3" opacity="0.6"/>
        <path d="${pts0.join('')}" fill="none" stroke="var(--teal)" stroke-width="2.5"/>
        <path d="${pts1.join('')}" fill="none" stroke="var(--red)" stroke-width="1.9" stroke-dasharray="6 4"/>
        <line x1="${curX.toFixed(1)}" y1="${gy1}" x2="${curX.toFixed(1)}" y2="${gy0}" stroke="var(--amber)" stroke-width="1.5" stroke-dasharray="3 3"/>
        <circle cx="${curX.toFixed(1)}" cy="${curY0.toFixed(1)}" r="5.5" fill="var(--teal)" stroke="var(--panel)" stroke-width="2"/>
        <circle cx="${curX.toFixed(1)}" cy="${curY1.toFixed(1)}" r="4.8" fill="var(--red)" stroke="var(--panel)" stroke-width="1.8"/>
      `;
    }

    function synthMziClip(mode = 'current', autoPlay = false) {
      const phiRad = mziPhiDeg * Math.PI / 180;
      const res = M.synthesizeMzi(phiRad, mziVis, mode);
      const audioEl = byId('mzi-audio');
      setAudioWav(audioEl, 'mzi', res.bytes);
      const label = mode === 'compare'
        ? `对比 WAV（前 1.4s 相长 0° → 后 1.4s φ=${mziPhiDeg}°, V=${f2(mziVis)}）`
        : `当前参数 WAV（φ=${mziPhiDeg}°, V=${f2(mziVis)}）`;
      const metaEl = byId('mzi-audio-meta');
      metaEl.textContent = `${label} · 22050 Hz 16-bit PCM · ${res.duration.toFixed(2)}s · Peak ${f4(res.peak)} · RMS ${f4(res.rms)}`;
      if (autoPlay) {
        pauseAllAudio(audioEl);
        const playPromise = audioEl.play();
        if (playPromise && typeof playPromise.catch === 'function') {
          playPromise.catch(() => {
            metaEl.textContent += '（浏览器拦截自动播放，请点播放器 ▶ 试听）';
          });
        }
      }
    }

    function updateMzi(refreshAudio = false) {
      const phiRad = mziPhiDeg * Math.PI / 180;
      const m = M.mziMetrics(phiRad, mziVis);
      byId('mzi-phi').value = String(mziPhiDeg);
      byId('mzi-vis').value = String(mziVis);
      byId('mzi-phi-out').textContent = `${mziPhiDeg}° (${f3(phiRad)} rad)`;
      byId('mzi-vis-out').textContent = `V = ${f2(mziVis)}`;

      byId('mzi-bar-0').style.width = (100 * m.p0).toFixed(2) + '%';
      byId('mzi-bar-1').style.width = (100 * m.p1).toFixed(2) + '%';
      byId('mzi-p0-out').textContent = pct(m.p0);
      byId('mzi-p1-out').textContent = pct(m.p1);

      const ampLbl = byId('mzi-amp0-lbl');
      const ampVal = byId('mzi-amp0');
      if (m.isMixed) {
        if (ampLbl) ampLbl.textContent = '混态密度矩阵 ρ₀₀ / Tr(ρ²)';
        ampVal.textContent = `ρ₀₀=${f4(m.rho00)} · 纯度 ${f3(m.purity)}`;
      } else {
        if (ampLbl) ampLbl.textContent = '纯态相干分支振幅 (1 + eⁱᵠ)/2';
        ampVal.textContent = fmtComplex(m.amp0Re, m.amp0Im);
      }

      byId('mzi-dmax').textContent = `${f3(m.dMax)} (V²+D² ≤ 1)`;
      byId('mzi-coh').textContent = `${f3(m.coh)} (Tr(ρ²)=${f3(m.purity)})`;
      byId('mzi-sum').textContent = f4(m.p0 + m.p1);

      const noteEl = byId('mzi-note');
      noteEl.className = 'note-box';
      if (mziVis < 0.05) {
        noteEl.classList.add('amber');
        noteEl.textContent = `完全路径标记（V ≈ 0）：系统退化为经典混态 ρ = diag(0.5, 0.5)，非对角相干项 |ρ₀₁| = 0，无论怎么转动 φ，P(0) 与 P(1) 都固定为 50% / 50%。`;
      } else if (m.isMixed) {
        noteEl.classList.add('amber');
        noteEl.textContent = `部分退相干混态（V = ${f2(mziVis)}）：相干项 |ρ₀₁| = V/2 = ${f3(m.coh)}，纯度 Tr(ρ²) = ${f3(m.purity)} < 1，条纹对比度按 V 线性压缩。`;
      } else if (m.p0 > 0.98) {
        noteEl.textContent = '相长干涉（φ ≈ 0°）：两臂复振幅同向相加，全部概率汇入端口 0，端口 1 相消归零。';
      } else if (m.p0 < 0.02) {
        noteEl.classList.add('warn');
        noteEl.textContent = '相消干涉（φ ≈ 180°，即 H·Z·H|0⟩ = |1⟩）：端口 0 振幅精确抵消为零，输出全部转向端口 1！';
      } else if (Math.abs(mziPhiDeg - 120) <= 2) {
        noteEl.textContent = '手册 A01 经典例题（φ = 120° = 2π/3）：端口 0 振幅模为 1/2，概率与声波均方功率比均为 (1/2)² = 1/4 = 25.0%。';
      } else {
        noteEl.textContent = `当前纯态：P(0) = ${f4(m.p0)}，P(1) = ${f4(m.p1)}；调节可见度 V 可直观观察路径标记对非对角相干项的压缩。`;
      }

      renderMziDiagrams(m);
      if (refreshAudio) synthMziClip('current', false);
    }

    // Pointer scrubbing on #mzi-fringe-svg
    const fringeSvg = byId('mzi-fringe-svg');
    let scrubbing = false;
    function scrubPhi(e) {
      const rect = fringeSvg.getBoundingClientRect();
      if (!rect.width) return;
      const svgX = ((e.clientX - rect.left) / rect.width) * 640;
      const u = Math.max(0, Math.min(1, (svgX - 56) / (612 - 56)));
      mziPhiDeg = Math.round(u * 360);
      updateMzi(false);
    }
    fringeSvg.style.cursor = 'ew-resize';
    fringeSvg.addEventListener('pointerdown', e => {
      scrubbing = true;
      fringeSvg.setPointerCapture?.(e.pointerId);
      scrubPhi(e);
    });
    fringeSvg.addEventListener('pointermove', e => {
      if (scrubbing) scrubPhi(e);
    });
    fringeSvg.addEventListener('pointerup', () => {
      if (scrubbing) {
        scrubbing = false;
        synthMziClip('current', false);
      }
    });

    byId('mzi-phi').addEventListener('input', e => {
      mziPhiDeg = Number(e.target.value);
      updateMzi(false);
    });
    byId('mzi-phi').addEventListener('change', () => synthMziClip('current', false));
    byId('mzi-vis').addEventListener('input', e => {
      mziVis = Number(e.target.value);
      updateMzi(false);
    });
    byId('mzi-vis').addEventListener('change', () => synthMziClip('current', false));

    document.querySelectorAll('[data-mzi-phi]').forEach(btn => {
      btn.addEventListener('click', () => {
        mziPhiDeg = Number(btn.dataset.mziPhi);
        updateMzi(true);
      });
    });
    document.querySelectorAll('[data-mzi-vis]').forEach(btn => {
      btn.addEventListener('click', () => {
        mziVis = Number(btn.dataset.mziVis);
        updateMzi(true);
      });
    });
    byId('mzi-synth-current').addEventListener('click', () => synthMziClip('current', true));
    byId('mzi-synth-compare').addEventListener('click', () => synthMziClip('compare', true));

    updateMzi(true);
  };
})(window);
